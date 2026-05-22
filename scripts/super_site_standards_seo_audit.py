#!/usr/bin/env python3
"""
Embaixada Carioca — Super Site Standards + SEO Audit

Auditoria estática consolidada para as 80+ páginas HTML do site.

Objetivo:
- Transformar os aprendizados das últimas correções visuais da Home em uma trava de site inteiro.
- Detectar regressões de contraste por contexto claro/escuro.
- Auditar SEO técnico e JSON-LD/rich snippets.
- Gerar relatório Markdown + CSV para GitHub Actions.

Saídas:
- _audit_reports/super_site_standards_seo_audit.md
- _audit_reports/super_site_standards_seo_audit_details.csv

A auditoria é deliberadamente conservadora: ela detecta padrões de risco que já apareceram no site,
em especial texto creme/branco em fundo claro e texto azul/verde/cinza em fundo escuro.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "super_site_standards_seo_audit.md"
REPORT_CSV = REPORT_DIR / "super_site_standards_seo_audit_details.csv"

EXCLUDED_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "_audit_reports",
    "visual_browser_screenshots",
    "dist",
    "build",
    "coverage",
}

COMMERCIAL_UTILITY_PAGES = {"404.html", "offline.html", "home-preview.html"}

RECENT_LEARNING_MAP = [
    ("home_lower_contrast", "Home: seções inferiores não podem herdar texto creme/branco sobre areia."),
    ("home_dark_contrast", "Home: seções escuras não podem herdar azul/verde/cinza escuro."),
    ("sunset_info_cards", "Sunset: cards escuros precisam de texto creme e labels laranja."),
    ("como_chegar_visibility", "Como chegar: cards e FAQs precisam de texto visível sem camada cobrindo."),
    ("nav_underline", "Menu: sublinhado amarelo só no hover, alinhado à palavra."),
    ("hero_eyebrow", "Eyebrow do hero deve alinhar com o início do primeiro item do menu."),
    ("hero_side_frame", "Card lateral do hero deve usar texto claro sobre vidro escuro, sem blocos opacos grosseiros."),
    ("italics_orange", "Itálicos editoriais devem usar o laranja do botão Reservar, não creme invisível."),
    ("review_schema_single_rating", "Schema: apenas um aggregateRating canônico por página elegível."),
    ("manifest_scope", "Manifest: shortcuts precisam ficar dentro do escopo do manifesto."),
]

SCRIPT_RE = re.compile(
    r'<script[^>]+type=["\\']application/ld\+json["\\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
META_DESC_RE = re.compile(r'<meta[^>]+name=["\\']description["\\'][^>]+content=["\\']([^"\\']+)["\\']', re.IGNORECASE)
CANONICAL_RE = re.compile(r'<link[^>]+rel=["\\']canonical["\\'][^>]+href=["\\']([^"\\']+)["\\']', re.IGNORECASE)
H1_RE = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
ALT_RE = re.compile(r"\salt=[\"']([^\"']*)[\"']", re.IGNORECASE)

HEX_LIGHT_TEXT = re.compile(r"color\s*:\s*(#fff|#ffffff|#f6efde|#f5edd6|#ede2c9|var\(--areia(?:-pale)?\)|var\(--paper\))", re.I)
HEX_DARK_TEXT = re.compile(r"color\s*:\s*(#00405a|#003f5a|#002f3f|#061a26|#335d4a|#485156|var\(--azul1\)|var\(--azul-escuro\)|var\(--verde\)|var\(--cinza1\))", re.I)
LIGHT_BG = re.compile(r"background(?:-color)?\s*:\s*(#fff|#ffffff|#fffaf0|#f8f4ed|#f6efde|#ede2c9|var\(--areia(?:-pale)?\)|var\(--paper\))", re.I)
DARK_BG = re.compile(r"background(?:-color)?\s*:\s*(#00405a|#003f5a|#002f3f|#061a26|#0d1b2a|#10263a|var\(--azul1\)|var\(--azul-escuro\))", re.I)
LOW_OPACITY = re.compile(r"opacity\s*:\s*0\.(?:[0-5][0-9]?|6[0-4])", re.I)
LOW_ALPHA_WHITE = re.compile(r"rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*0\.(?:[0-5][0-9]?|6[0-4])\s*\)", re.I)
LOW_ALPHA_DARK = re.compile(r"rgba\(\s*(?:0|51|72)\s*,\s*(?:64|81|93)\s*,\s*(?:74|86|90)\s*,\s*0\.(?:[0-5][0-9]?|6[0-4])\s*\)", re.I)
STYLE_ATTR_RE = re.compile(r"style=[\"']([^\"']+)[\"']", re.I | re.DOTALL)

HOME_PATTERN_CLASSES = [
    "hero-meta-card",
    "sunset-info-item",
    "sunset-info-text",
    "quick-facts",
    "quick-answers-section",
    "geo-aio-section",
    "gsc-ctr-block",
    "ec-wrap",
    "faq-item",
    "ig-card",
]

SEO_REQUIRED_META = [
    "og:title",
    "og:description",
    "og:image",
    "twitter:title",
    "twitter:description",
]

@dataclass
class Finding:
    page: str
    severity: str
    category: str
    check: str
    message: str
    evidence: str = ""

@dataclass
class PageResult:
    path: Path
    findings: list[Finding] = field(default_factory=list)

    @property
    def status(self) -> str:
        return "FAIL" if any(f.severity == "FAIL" for f in self.findings) else ("WARN" if self.findings else "PASS")


def strip_tags(value: str) -> str:
    value = re.sub(r"<script.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def find_html_pages() -> list[Path]:
    pages: list[Path] = []
    for path in ROOT.rglob("*.html"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        pages.append(path)
    return sorted(pages, key=lambda p: rel(p))


def add(result: PageResult, severity: str, category: str, check: str, message: str, evidence: str = "") -> None:
    result.findings.append(Finding(rel(result.path), severity, category, check, message, evidence[:220].replace("\n", " ")))


def parse_json_ld_blocks(html: str) -> list[Any]:
    data: list[Any] = []
    for raw in SCRIPT_RE.findall(html):
        raw = raw.strip()
        if not raw:
            continue
        try:
            data.append(json.loads(raw))
        except json.JSONDecodeError:
            data.append({"__parse_error__": raw[:200]})
    return data


def walk_json(value: Any):
    if isinstance(value, dict):
        yield value
        for v in value.values():
            yield from walk_json(v)
    elif isinstance(value, list):
        for item in value:
            yield from walk_json(item)


def audit_seo(result: PageResult, html: str) -> None:
    title = TITLE_RE.search(html)
    if not title or not strip_tags(title.group(1)):
        add(result, "FAIL", "SEO", "title", "Página sem <title> válido.")
    else:
        title_text = strip_tags(title.group(1))
        if len(title_text) < 18:
            add(result, "WARN", "SEO", "title_length", "Title curto demais para busca orgânica.", title_text)
        if len(title_text) > 72:
            add(result, "WARN", "SEO", "title_length", "Title longo demais; pode truncar no Google.", title_text)

    desc = META_DESC_RE.search(html)
    if not desc:
        add(result, "FAIL", "SEO", "meta_description", "Página sem meta description.")
    else:
        desc_text = desc.group(1).strip()
        if len(desc_text) < 70:
            add(result, "WARN", "SEO", "meta_description_length", "Meta description curta demais.", desc_text)
        if len(desc_text) > 180:
            add(result, "WARN", "SEO", "meta_description_length", "Meta description longa demais.", desc_text)

    canonical = CANONICAL_RE.search(html)
    if not canonical:
        add(result, "FAIL", "SEO", "canonical", "Página sem canonical.")
    elif not canonical.group(1).startswith("https://www.embaixadacarioca.com"):
        add(result, "FAIL", "SEO", "canonical_domain", "Canonical fora do domínio oficial.", canonical.group(1))

    h1s = [strip_tags(x) for x in H1_RE.findall(html) if strip_tags(x)]
    if not h1s:
        add(result, "FAIL", "SEO", "h1", "Página sem H1 visível no HTML.")
    elif len(h1s) > 1:
        add(result, "WARN", "SEO", "h1_multiple", f"Página com {len(h1s)} H1. Avaliar hierarquia.", " | ".join(h1s[:4]))

    for prop in SEO_REQUIRED_META:
        if f'property="{prop}"' not in html and f"property='{prop}'" not in html and f'name="{prop}"' not in html and f"name='{prop}'" not in html:
            add(result, "WARN", "SEO", "social_meta", f"Meta social ausente: {prop}.")

    if "hreflang" not in html:
        add(result, "WARN", "SEO", "hreflang", "Página sem hreflang; importante para PT/EN/ES.")


def audit_images(result: PageResult, html: str) -> None:
    imgs = IMG_RE.findall(html)
    missing = []
    for img in imgs:
        alt = ALT_RE.search(img)
        if not alt or not alt.group(1).strip():
            if "aria-hidden" not in img and "role=\"presentation\"" not in img:
                missing.append(img[:120])
    if missing:
        add(result, "WARN", "SEO", "image_alt", f"{len(missing)} imagem(ns) sem alt útil.", missing[0])


def audit_json_ld(result: PageResult, html: str) -> None:
    blocks = parse_json_ld_blocks(html)
    if not blocks:
        add(result, "WARN", "SEO_SCHEMA", "jsonld_missing", "Página sem JSON-LD; avaliar se deveria ter schema.")
        return

    parse_errors = [b for b in blocks if isinstance(b, dict) and "__parse_error__" in b]
    if parse_errors:
        add(result, "FAIL", "SEO_SCHEMA", "jsonld_parse", f"{len(parse_errors)} bloco(s) JSON-LD inválido(s).", str(parse_errors[0])[:160])

    aggregate_nodes = []
    restaurant_type_arrays = []
    faq_pages = 0
    breadcrumbs = 0

    for block in blocks:
        for node in walk_json(block):
            if not isinstance(node, dict):
                continue
            if "aggregateRating" in node:
                aggregate_nodes.append(node)
            node_type = node.get("@type")
            if isinstance(node_type, list) and "Restaurant" in node_type and any(t in node_type for t in ["LocalBusiness", "FoodEstablishment"]):
                restaurant_type_arrays.append(node)
            if node_type == "FAQPage":
                faq_pages += 1
            if node_type == "BreadcrumbList":
                breadcrumbs += 1

    if len(aggregate_nodes) > 1:
        add(result, "FAIL", "SEO_SCHEMA", "aggregate_rating_duplicate", f"Página tem {len(aggregate_nodes)} aggregateRating; risco de erro em snippets de avaliação.")
    if restaurant_type_arrays:
        add(result, "FAIL", "SEO_SCHEMA", "restaurant_type_array", "Restaurant aparece em @type múltiplo junto de LocalBusiness/FoodEstablishment; pode duplicar rich result.")

    for node in aggregate_nodes:
        rating = node.get("aggregateRating")
        if isinstance(rating, dict):
            for key in ["ratingValue", "reviewCount", "bestRating"]:
                if key not in rating:
                    add(result, "FAIL", "SEO_SCHEMA", "aggregate_rating_incomplete", f"aggregateRating sem {key}.")
            if isinstance(rating.get("ratingValue"), str) or isinstance(rating.get("reviewCount"), str):
                add(result, "WARN", "SEO_SCHEMA", "aggregate_rating_numeric", "ratingValue/reviewCount estão como string; preferível número.", json.dumps(rating, ensure_ascii=False))

    if "faq" in result.path.name.lower() or "pergunta" in html.lower():
        if faq_pages == 0:
            add(result, "WARN", "SEO_SCHEMA", "faq_schema", "Página com conteúdo de FAQ sem FAQPage JSON-LD detectado.")

    if breadcrumbs == 0 and result.path.name not in COMMERCIAL_UTILITY_PAGES:
        add(result, "WARN", "SEO_SCHEMA", "breadcrumb_schema", "Página sem BreadcrumbList JSON-LD.")


def audit_visual_static(result: PageResult, html: str) -> None:
    # 1) Padrões globais de risco que já causaram bugs reais.
    if LOW_OPACITY.search(html):
        add(result, "WARN", "VISUAL", "low_opacity_text", "Há opacity baixa em CSS/inline. Conferir se não está aplicada a texto real.", LOW_OPACITY.search(html).group(0))
    if LOW_ALPHA_WHITE.search(html):
        add(result, "WARN", "VISUAL", "low_alpha_white", "Texto branco/creme com alpha baixo detectado; risco em fundo claro.", LOW_ALPHA_WHITE.search(html).group(0))
    if LOW_ALPHA_DARK.search(html):
        add(result, "WARN", "VISUAL", "low_alpha_dark", "Texto azul/verde/cinza com alpha baixo detectado; risco em fundo escuro.", LOW_ALPHA_DARK.search(html).group(0))

    # 2) Inline styles: contexto claro/escuro com cor errada no mesmo style.
    for match in STYLE_ATTR_RE.finditer(html):
        style = match.group(1)
        if LIGHT_BG.search(style) and HEX_LIGHT_TEXT.search(style):
            add(result, "FAIL", "VISUAL", "light_bg_light_text_inline", "Texto claro sobre fundo claro no mesmo style.", style)
        if DARK_BG.search(style) and HEX_DARK_TEXT.search(style):
            add(result, "FAIL", "VISUAL", "dark_bg_dark_text_inline", "Texto escuro sobre fundo escuro no mesmo style.", style)

    # 3) Section windows: detecta risco por proximidade dentro de blocos grandes.
    section_chunks = re.findall(r"<section\b.*?</section>", html, flags=re.I | re.S)
    for chunk in section_chunks:
        section_id = re.search(r'id=["\\']([^"\\']+)["\\']', chunk, flags=re.I)
        section_name = section_id.group(1) if section_id else "section"
        if LIGHT_BG.search(chunk) and HEX_LIGHT_TEXT.search(chunk):
            add(result, "WARN", "VISUAL", "light_section_light_text", f"Seção clara com texto claro: {section_name}.", chunk[:180])
        if DARK_BG.search(chunk) and HEX_DARK_TEXT.search(chunk):
            add(result, "WARN", "VISUAL", "dark_section_dark_text", f"Seção escura com texto escuro: {section_name}.", chunk[:180])

    # 4) Classes/padrões aprendidos da Home: se aparecem em páginas internas, precisam de trava visual.
    for cls in HOME_PATTERN_CLASSES:
        if cls in html:
            if cls in {"sunset-info-item", "sunset-info-text", "quick-facts", "gsc-ctr-block", "ig-card"}:
                if "#f59b1e" not in html and "--amarelo" not in html:
                    add(result, "WARN", "VISUAL", "home_pattern_without_accent", f"Classe aprendida da Home sem cor de destaque clara: {cls}.")

    # 5) Seleção visual: não deve ser usada como solução permanente.
    if "::selection" in html and "background:var(--amarelo)" not in html and "background: var(--amarelo)" not in html:
        add(result, "WARN", "VISUAL", "selection_style", "Estilo de seleção fora do padrão laranja/azul.")


def audit_performance(result: PageResult, html: str) -> None:
    preload_count = len(re.findall(r'rel=["\\']preload["\\']', html, flags=re.I))
    if preload_count > 8:
        add(result, "WARN", "PERFORMANCE", "too_many_preloads", f"Página com {preload_count} preloads; risco de warning no Chrome/Lighthouse.")

    if "https://www.googletagmanager.com/gtag/js" in html and "requestIdleCallback" not in html:
        add(result, "WARN", "PERFORMANCE", "ga4_not_deferred", "GA4 detectado sem carregamento adiado por interação/idle.")

    style_blocks = len(re.findall(r"<style\b", html, flags=re.I))
    if style_blocks > 25:
        add(result, "WARN", "PERFORMANCE", "many_inline_styles", f"Página com {style_blocks} blocos <style>; risco de cascata frágil e peso alto.")

    scripts = len(re.findall(r"<script\b", html, flags=re.I))
    if scripts > 35:
        add(result, "WARN", "PERFORMANCE", "many_scripts", f"Página com {scripts} scripts; revisar impacto.")


def audit_page(path: Path) -> PageResult:
    result = PageResult(path=path)
    html = path.read_text(encoding="utf-8", errors="ignore")
    audit_seo(result, html)
    audit_images(result, html)
    audit_json_ld(result, html)
    audit_visual_static(result, html)
    audit_performance(result, html)
    return result


def score_page(result: PageResult) -> int:
    score = 100
    for f in result.findings:
        score -= 12 if f.severity == "FAIL" else 4
    return max(score, 0)


def write_reports(results: list[PageResult]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    all_findings = [f for r in results for f in r.findings]
    fails = [f for f in all_findings if f.severity == "FAIL"]
    warns = [f for f in all_findings if f.severity == "WARN"]
    pages_fail = [r for r in results if r.status == "FAIL"]
    pages_warn = [r for r in results if r.status == "WARN"]
    pages_pass = [r for r in results if r.status == "PASS"]

    with REPORT_CSV.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=["page", "status", "score", "severity", "category", "check", "message", "evidence"])
        writer.writeheader()
        for r in results:
            if not r.findings:
                writer.writerow({
                    "page": rel(r.path), "status": r.status, "score": score_page(r),
                    "severity": "", "category": "", "check": "", "message": "", "evidence": "",
                })
            for f in r.findings:
                writer.writerow({
                    "page": f.page,
                    "status": r.status,
                    "score": score_page(r),
                    "severity": f.severity,
                    "category": f.category,
                    "check": f.check,
                    "message": f.message,
                    "evidence": f.evidence,
                })

    by_category: dict[str, int] = {}
    for f in all_findings:
        by_category[f.category] = by_category.get(f.category, 0) + 1

    md: list[str] = []
    status = "PASS" if not fails else "FAIL"
    md.append("# Super Site Standards + SEO Audit\n")
    md.append(f"Status geral: **{status}**\n")
    md.append("## Resumo executivo\n")
    md.append(f"- Páginas HTML auditadas: **{len(results)}**")
    md.append(f"- PASS: **{len(pages_pass)}**")
    md.append(f"- WARN: **{len(pages_warn)}**")
    md.append(f"- FAIL: **{len(pages_fail)}**")
    md.append(f"- Findings FAIL: **{len(fails)}**")
    md.append(f"- Findings WARN: **{len(warns)}**\n")

    md.append("## Aprendizados das últimas correções incorporados\n")
    for key, description in RECENT_LEARNING_MAP:
        md.append(f"- **{key}** — {description}")
    md.append("")

    md.append("## Categorias de findings\n")
    if by_category:
        for cat, count in sorted(by_category.items(), key=lambda x: (-x[1], x[0])):
            md.append(f"- {cat}: {count}")
    else:
        md.append("- Nenhum finding.")
    md.append("")

    md.append("## Páginas com falha\n")
    if pages_fail:
        for r in pages_fail[:80]:
            md.append(f"- **{rel(r.path)}** — score {score_page(r)} — {len(r.findings)} finding(s)")
    else:
        md.append("Nenhuma página com FAIL.")
    md.append("")

    md.append("## Top findings\n")
    for f in all_findings[:120]:
        md.append(f"- **{f.severity}** `{f.page}` — {f.category}/{f.check}: {f.message}")
        if f.evidence:
            md.append(f"  - Evidência: `{f.evidence}`")
    if not all_findings:
        md.append("Nenhum finding encontrado.")
    md.append("")

    md.append("## Arquivos gerados\n")
    md.append(f"- `{REPORT_MD.relative_to(ROOT)}`")
    md.append(f"- `{REPORT_CSV.relative_to(ROOT)}`")
    md.append("")

    REPORT_MD.write_text("\n".join(md), encoding="utf-8")


def main() -> int:
    pages = find_html_pages()
    results = [audit_page(p) for p in pages]
    write_reports(results)
    fails = [f for r in results for f in r.findings if f.severity == "FAIL"]
    print(f"Audited HTML pages: {len(results)}")
    print(f"FAIL findings: {len(fails)}")
    print(f"Report: {REPORT_MD.relative_to(ROOT)}")
    print(f"CSV: {REPORT_CSV.relative_to(ROOT)}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
