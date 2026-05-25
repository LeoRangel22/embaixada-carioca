#!/usr/bin/env python3
"""
Sprint 2 Locale Quality Fix — Embaixada Carioca

Corrige efeitos colaterais do Sprint 2:
- blocos GEO em EN/ES não podem exibir rótulos em português;
- landings novas de café da manhã precisam ter navegação, CTA, explicação e footer no idioma correto;
- gera relatório de validação de texto visível para evitar falso 10/10.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT: list[str] = []
WARNINGS: list[str] = []
COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "en_fixes": 0,
    "es_fixes": 0,
    "pt_fixes": 0,
    "warnings": 0,
}

HTML_LANG_RE = re.compile(r"<html\b[^>]*\blang=[\"']([^\"']+)[\"']", re.IGNORECASE)
NON_VISIBLE_RE = re.compile(r"<script\b[\s\S]*?</script>|<style\b[\s\S]*?</style>|<!--[^>]*-->", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")

EN_REPLACEMENTS = {
    'aria-label="Resposta direta para busca e IA"': 'aria-label="Direct answer for search and AI"',
    "Resposta direta · SEO + GEO": "Direct answer · SEO + GEO",
    ">Café<": ">Breakfast<",
    ">Almoço<": ">Lunch<",
    ">Entardecer<": ">Sunset<",
    ">Cardápio<": ">Menu<",
    'href="/cafe-da-manha.html"': 'href="/en/cafe-da-manha.html"',
    'href="/almoco.html"': 'href="/en/almoco.html"',
    'href="/entardecer.html"': 'href="/en/entardecer.html"',
    'href="/cardapio.html"': 'href="/en/cardapio.html"',
    '<a class="brand" href="/">Embaixada Carioca</a>': '<a class="brand" href="/en/">Embaixada Carioca</a>',
    "Morro da Urca · Parque Bondinho Pão de Açúcar": "Urca Hill · Sugarloaf Cable Car Park",
    ">Como chegar<": ">How to get there<",
    'href="/guia-do-rio.html"': 'href="/en/guia-do-rio.html"',
    "Por que essa página existe?": "Why does this page exist?",
    "Esta landing foi criada para responder diretamente às buscas de alta intenção sobre café da manhã com vista, restaurantes no Morro da Urca e experiências dentro do Parque Bondinho Pão de Açúcar.": "This page was created to answer high-intent searches about breakfast with a view, restaurants at Urca Hill and experiences inside Sugarloaf Cable Car Park.",
    "Embaixada Carioca · Morro da Urca · Parque Bondinho Pão de Açúcar": "Embaixada Carioca · Urca Hill · Sugarloaf Cable Car Park",
}

ES_REPLACEMENTS = {
    'aria-label="Resposta direta para busca e IA"': 'aria-label="Respuesta directa para búsqueda e IA"',
    "Resposta direta · SEO + GEO": "Respuesta directa · SEO + GEO",
    ">Café<": ">Desayuno<",
    ">Almoço<": ">Almuerzo<",
    ">Entardecer<": ">Atardecer<",
    ">Cardápio<": ">Menú<",
    'href="/cafe-da-manha.html"': 'href="/es/cafe-da-manha.html"',
    'href="/almoco.html"': 'href="/es/almoco.html"',
    'href="/entardecer.html"': 'href="/es/entardecer.html"',
    'href="/cardapio.html"': 'href="/es/cardapio.html"',
    '<a class="brand" href="/">Embaixada Carioca</a>': '<a class="brand" href="/es/">Embaixada Carioca</a>',
    "Morro da Urca · Parque Bondinho Pão de Açúcar": "Morro da Urca · Parque Bondinho Pan de Azúcar",
    ">Como chegar<": ">Cómo llegar<",
    'href="/guia-do-rio.html"': 'href="/es/guia-do-rio.html"',
    "Por que essa página existe?": "¿Por qué existe esta página?",
    "Esta landing foi criada para responder diretamente às buscas de alta intenção sobre café da manhã com vista, restaurantes no Morro da Urca e experiências dentro do Parque Bondinho Pão de Açúcar.": "Esta página fue creada para responder directamente a búsquedas de alta intención sobre desayuno con vista, restaurantes en el Morro da Urca y experiencias dentro del Parque Bondinho Pan de Azúcar.",
    "Embaixada Carioca · Morro da Urca · Parque Bondinho Pão de Açúcar": "Embaixada Carioca · Morro da Urca · Parque Bondinho Pan de Azúcar",
}

PT_REPLACEMENTS = {
    "Direct answer · SEO + GEO": "Resposta direta · SEO + GEO",
    "Respuesta directa · SEO + GEO": "Resposta direta · SEO + GEO",
}

VISIBLE_FORBIDDEN = {
    "en": [
        "Resposta direta", "Como chegar", "Por que essa página existe", "Esta landing foi criada", ">Café<", ">Almoço<", ">Entardecer<", ">Cardápio<",
        "café da manhã com vista", "restaurantes no Morro da Urca", "experiências dentro do Parque Bondinho",
    ],
    "es": [
        "Resposta direta", "Como chegar", "Por que essa página existe", "Esta landing foi criada", ">Café<", ">Almoço<", ">Entardecer<", ">Cardápio<",
        "Breakfast with a view", "Where to have breakfast", "Lunch", "Menu",
    ],
    "pt": ["Direct answer · SEO + GEO", "Respuesta directa · SEO + GEO"],
}


def detect_lang(rel: str, text: str) -> str:
    match = HTML_LANG_RE.search(text)
    if match:
        value = match.group(1).lower()
        if value.startswith("en"):
            return "en"
        if value.startswith("es"):
            return "es"
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt"


def visible_text(html: str) -> str:
    text = NON_VISIBLE_RE.sub(" ", html)
    # Preserve link-label checks by leaving actual visible anchor content after tag removal.
    text = TAG_RE.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def apply_replacements(text: str, rel: str, lang: str) -> str:
    if lang == "en":
        repl = EN_REPLACEMENTS
        counter = "en_fixes"
    elif lang == "es":
        repl = ES_REPLACEMENTS
        counter = "es_fixes"
    else:
        repl = PT_REPLACEMENTS
        counter = "pt_fixes"

    for old, new in repl.items():
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            COUNTERS[counter] += count
            REPORT.append(f"{counter.upper()}: {rel} | {old!r} -> {new!r} | {count}")
    return text


def audit_visible(text: str, rel: str, lang: str) -> None:
    visible = visible_text(text)
    for token in VISIBLE_FORBIDDEN.get(lang, []):
        needle = token.replace(">", "").replace("<", "")
        if needle in visible:
            WARNINGS.append(f"VISIBLE_LANG_WARNING: {rel} [{lang}] contém {needle!r}")
            COUNTERS["warnings"] += 1


def process(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix != ".html" or ".git" in path.parts or rel.startswith("_"):
        return
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    lang = detect_lang(rel, original)
    text = apply_replacements(original, rel, lang)
    audit_visible(text, rel, lang)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1
        REPORT.append(f"UPDATED: {rel}")


def write_report() -> None:
    out = ROOT / "_audit_reports"
    out.mkdir(exist_ok=True)
    report = out / "sprint2_locale_quality_fix_report.md"
    lines = [
        "# Sprint 2 Locale Quality Fix",
        "",
        "## Objetivo",
        "Corrigir rótulos visíveis em PT que vazaram para páginas EN/ES nos blocos GEO e landings de café da manhã.",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Correções"])
    lines.extend(f"- {x}" for x in REPORT) if REPORT else lines.append("- Nenhuma correção necessária.")
    lines.extend(["", "## Alertas remanescentes"])
    lines.extend(f"- {x}" for x in WARNINGS) if WARNINGS else lines.append("- Nenhum alerta visível remanescente encontrado.")
    lines.append("")
    report.write_text("\n".join(lines), encoding="utf-8")
    print(report.read_text(encoding="utf-8"))


def main() -> int:
    for path in sorted(ROOT.rglob("*.html")):
        process(path)
    write_report()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
