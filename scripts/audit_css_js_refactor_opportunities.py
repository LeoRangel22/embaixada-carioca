#!/usr/bin/env python3
"""Audit CSS/JS refactor opportunities for Embaixada Carioca.

This audit is diagnostic only. It does not modify HTML/CSS/JS.

It identifies:
- pages with the highest number of inline style/script blocks;
- exact repeated inline CSS/JS blocks;
- recurring style/script markers by id/comment/class keywords;
- safe extraction candidates;
- high-risk blocks that should remain page-specific until visual QA.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "css_js_refactor_opportunity_audit.md"

STYLE_RE = re.compile(r"<style\b(?P<attrs>[^>]*)>(?P<body>.*?)</style>", re.I | re.S)
SCRIPT_RE = re.compile(r"<script\b(?P<attrs>[^>]*)>(?P<body>.*?)</script>", re.I | re.S)
LINK_CSS_RE = re.compile(r"<link\b(?=[^>]*rel=[\"']stylesheet[\"'])[^>]*>", re.I | re.S)
IMG_RE = re.compile(r"<img\b[^>]*>", re.I | re.S)
JSONLD_RE = re.compile(r"<script\b(?=[^>]*type=[\"']application/ld\+json[\"'])[^>]*>.*?</script>", re.I | re.S)

RISK_KEYWORDS = {
    "low": [
        "lang-switcher",
        "lang-dropdown",
        "nav-rating-badge",
        "google-review-badge",
        "wa-widget",
        "mobile-bottom-nav",
        "nav-drawer",
        "focus-visible",
    ],
    "medium": [
        "nav.top",
        "hero-ctas",
        "btn",
        "section",
        "wrap",
        "grid",
        "faq",
        "accordion",
    ],
    "high": [
        "readability",
        "contrast",
        "visual_readability",
        "legibility",
        "emergency",
        "lock",
        "page-hero",
        "hero-photo",
        "menu-item",
        "cardapio",
        "almoco",
    ],
}

GLOBAL_CANDIDATE_KEYWORDS = [
    "lang-switcher",
    "lang-dropdown",
    "nav-drawer",
    "mobile-bottom-nav",
    "wa-widget",
    "google-review-badge",
    "nav-rating-badge",
    "focus-visible",
    "touch targets",
    "whatsapp",
    "idioma",
    "drawer",
]


@dataclass
class PageStats:
    rel: str
    inline_styles: int
    inline_scripts: int
    jsonld_scripts: int
    external_css: int
    images: int
    inline_style_bytes: int
    inline_script_bytes: int


def html_files() -> list[Path]:
    return [
        p for p in sorted(ROOT.rglob("*.html"))
        if ".git" not in p.parts and not p.relative_to(ROOT).as_posix().startswith("_")
    ]


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def block_hash(text: str) -> str:
    return sha256(compact(text).encode("utf-8", errors="ignore")).hexdigest()[:12]


def classify(text: str) -> tuple[str, str, str]:
    lower = text.lower()
    score = "medium"
    reason = "global/layout styles or scripts require visual QA before extraction"
    for keyword in RISK_KEYWORDS["low"]:
        if keyword in lower:
            score = "low"
            reason = f"recurring utility pattern: {keyword}"
            break
    for keyword in RISK_KEYWORDS["high"]:
        if keyword in lower:
            score = "high"
            reason = f"visual/readability/page-critical pattern: {keyword}"
            break
    extract = "yes" if score == "low" else ("partial" if score == "medium" else "no/partial")
    return score, extract, reason


def marker_name(attrs: str, body: str, fallback: str) -> str:
    marker = re.search(r"\bid=[\"']([^\"']+)[\"']", attrs, re.I)
    if marker:
        return marker.group(1)
    comment = re.search(r"/\*\s*([^*\n]{8,80})", body)
    if comment:
        return comment.group(1).strip()
    html_comment = re.search(r"<!--\s*([^>\n]{8,80})", body)
    if html_comment:
        return html_comment.group(1).strip()
    for keyword in GLOBAL_CANDIDATE_KEYWORDS:
        if keyword in body.lower():
            return keyword
    return fallback


def page_stats(rel: str, source: str) -> PageStats:
    styles = STYLE_RE.findall(source)
    scripts = SCRIPT_RE.findall(source)
    jsonld = JSONLD_RE.findall(source)
    external_css = LINK_CSS_RE.findall(source)
    images = IMG_RE.findall(source)
    return PageStats(
        rel=rel,
        inline_styles=len(styles),
        inline_scripts=len(scripts),
        jsonld_scripts=len(jsonld),
        external_css=len(external_css),
        images=len(images),
        inline_style_bytes=sum(len(body) for _, body in styles),
        inline_script_bytes=sum(len(body) for _, body in scripts),
    )


def collect() -> tuple[list[PageStats], dict[str, dict], dict[str, dict], Counter[str]]:
    pages: list[PageStats] = []
    css_blocks: dict[str, dict] = {}
    js_blocks: dict[str, dict] = {}
    marker_counter: Counter[str] = Counter()

    for path in html_files():
        rel = path.relative_to(ROOT).as_posix()
        source = path.read_text(encoding="utf-8", errors="ignore")
        pages.append(page_stats(rel, source))

        for attrs, body in STYLE_RE.findall(source):
            h = block_hash(body)
            entry = css_blocks.setdefault(h, {"pages": set(), "bytes": len(body), "sample": compact(body)[:220], "markers": Counter(), "body": body})
            entry["pages"].add(rel)
            marker = marker_name(attrs, body, f"style:{h}")
            entry["markers"][marker] += 1
            marker_counter[f"css:{marker}"] += 1

        for attrs, body in SCRIPT_RE.findall(source):
            if "application/ld+json" in attrs.lower():
                continue
            h = block_hash(body)
            entry = js_blocks.setdefault(h, {"pages": set(), "bytes": len(body), "sample": compact(body)[:220], "markers": Counter(), "body": body})
            entry["pages"].add(rel)
            marker = marker_name(attrs, body, f"script:{h}")
            entry["markers"][marker] += 1
            marker_counter[f"js:{marker}"] += 1

    return pages, css_blocks, js_blocks, marker_counter


def top_pages(pages: list[PageStats], limit: int = 12) -> list[PageStats]:
    return sorted(pages, key=lambda p: (p.inline_styles + p.inline_scripts, p.inline_style_bytes + p.inline_script_bytes), reverse=True)[:limit]


def repeated_blocks(blocks: dict[str, dict], min_pages: int = 2, limit: int = 20) -> list[tuple[str, dict]]:
    rows = [(h, data) for h, data in blocks.items() if len(data["pages"]) >= min_pages]
    rows.sort(key=lambda item: (len(item[1]["pages"]), item[1]["bytes"]), reverse=True)
    return rows[:limit]


def write_report() -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    pages, css_blocks, js_blocks, marker_counter = collect()
    heavy = top_pages(pages)
    repeated_css = repeated_blocks(css_blocks)
    repeated_js = repeated_blocks(js_blocks)

    total_html = len(pages)
    total_styles = sum(p.inline_styles for p in pages)
    total_scripts = sum(p.inline_scripts for p in pages)
    total_css_bytes = sum(p.inline_style_bytes for p in pages)
    total_js_bytes = sum(p.inline_script_bytes for p in pages)

    lines: list[str] = [
        "# CSS/JS Refactor Opportunity Audit",
        "",
        "Status geral: **PASS**",
        "",
        "## Objetivo",
        "Mapear oportunidades reais de refactor de CSS/JS sem mexer no visual antes de uma validação controlada no navegador.",
        "",
        "## Resumo executivo",
        f"- Arquivos HTML analisados: **{total_html}**",
        f"- Blocos `<style>` inline: **{total_styles}**",
        f"- Blocos `<script>` inline, incluindo JSON-LD: **{total_scripts}**",
        f"- Peso estimado de CSS inline: **{total_css_bytes:,} bytes**".replace(",", "."),
        f"- Peso estimado de scripts inline: **{total_js_bytes:,} bytes**".replace(",", "."),
        f"- Blocos CSS exatos repetidos em 2+ páginas: **{len(repeated_css)}**",
        f"- Blocos JS exatos repetidos em 2+ páginas: **{len(repeated_js)}**",
        "",
        "## Páginas com maior oportunidade técnica",
        "",
        "| Página | Styles inline | Scripts inline | JSON-LD | CSS externo | Imagens | CSS bytes | JS bytes | Prioridade |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for p in heavy:
        total_blocks = p.inline_styles + p.inline_scripts
        priority = "alta" if total_blocks >= 35 else ("média" if total_blocks >= 25 else "baixa")
        lines.append(
            f"| `{p.rel}` | {p.inline_styles} | {p.inline_scripts} | {p.jsonld_scripts} | {p.external_css} | {p.images} | {p.inline_style_bytes} | {p.inline_script_bytes} | {priority} |"
        )

    lines.extend([
        "",
        "## Blocos CSS repetidos — candidatos a extração",
        "",
        "| Hash | Páginas | Bytes | Marker provável | Risco | Pode extrair? | Motivo |",
        "|---|---:|---:|---|---|---|---|",
    ])
    if repeated_css:
        for h, data in repeated_css:
            marker = data["markers"].most_common(1)[0][0]
            risk, extract, reason = classify(data["body"])
            lines.append(f"| `{h}` | {len(data['pages'])} | {data['bytes']} | `{marker}` | {risk} | {extract} | {reason} |")
    else:
        lines.append("| — | 0 | 0 | — | — | — | Nenhum bloco CSS exato repetido em 2+ páginas. |")

    lines.extend([
        "",
        "## Blocos JS repetidos — candidatos a extração",
        "",
        "| Hash | Páginas | Bytes | Marker provável | Risco | Pode extrair? | Motivo |",
        "|---|---:|---:|---|---|---|---|",
    ])
    if repeated_js:
        for h, data in repeated_js:
            marker = data["markers"].most_common(1)[0][0]
            risk, extract, reason = classify(data["body"])
            lines.append(f"| `{h}` | {len(data['pages'])} | {data['bytes']} | `{marker}` | {risk} | {extract} | {reason} |")
    else:
        lines.append("| — | 0 | 0 | — | — | — | Nenhum bloco JS exato repetido em 2+ páginas, excluindo JSON-LD. |")

    lines.extend([
        "",
        "## Padrões recorrentes por marcador",
        "",
        "| Marcador | Ocorrências | Leitura |",
        "|---|---:|---|",
    ])
    for marker, qty in marker_counter.most_common(20):
        label = "candidato a asset global" if any(k in marker.lower() for k in GLOBAL_CANDIDATE_KEYWORDS) else "avaliar no refactor"
        lines.append(f"| `{marker}` | {qty} | {label} |")

    lines.extend([
        "",
        "## Plano de refactor recomendado",
        "",
        "### Lote 1 — baixo risco",
        "Extrair para assets globais os padrões de idioma, WhatsApp, navegação mobile, bottom nav, badge de Google Reviews e foco acessível. Esses blocos tendem a ser utilitários e repetíveis.",
        "",
        "### Lote 2 — risco médio",
        "Consolidar nav desktop, botões, grids, espaçamentos de seção e cards comuns. Exige teste visual em home, cardápio, almoço, café, eventos e guia.",
        "",
        "### Lote 3 — alto risco",
        "Só depois de QA visual: readability locks, contrast locks, hero/page-hero, cardápio e overrides de menu. Esses blocos foram criados para corrigir problemas visuais reais e não devem ser removidos em massa.",
        "",
        "## Entrega operacional sugerida",
        "1. Criar `assets/css/ec-components-global.css` para idioma, WhatsApp, nav drawer, bottom nav e badges.",
        "2. Criar `assets/js/ec-ui-global.js` para interações repetidas de menu/idioma/WhatsApp.",
        "3. Incluir os assets globais nas páginas prioritárias.",
        "4. Remover apenas os blocos inline já cobertos, página por página.",
        "5. Rodar auditoria final e validação visual real antes do deploy definitivo.",
    ])

    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("CSS/JS refactor opportunity audit: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(write_report())
