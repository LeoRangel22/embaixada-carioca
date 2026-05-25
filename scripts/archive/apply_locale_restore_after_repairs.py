#!/usr/bin/env python3
"""
Locale Restore After Repairs — Embaixada Carioca.

Corrige efeitos colaterais de reparos globais:
- páginas /en/ voltam para inglês;
- páginas /es/ voltam para espanhol;
- páginas PT mantêm português;
- repara tokens técnicos e links residuais.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT: list[str] = []
COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "en_restored": 0,
    "es_restored": 0,
    "pt_repaired": 0,
    "tech_repaired": 0,
    "link_repaired": 0,
}

TECH_REPAIRS = {
    "send_page_vista": "send_page_view",
    "page_vista": "page_view",
    "vistaport-fit": "viewport-fit",
    "name=\"vistaport\"": "name=\"viewport\"",
    "name='vistaport'": "name='viewport'",
}

EN_RESTORE = {
    "Capacidade variável": "Capacity varies",
    "Estrutura e capacidade": "Structure & capacity",
    "salão principal": "main dining room",
    "terraços panorâmicos": "panoramic terraces",
    "terraço panorâmico": "panoramic terrace",
    "equipe receptiva": "hospitality team",
    "Reuniões matinais": "Morning meetings",
    "Falar com nossa equipe": "Talk to our team",
    "Solicitar orçamento": "Request a quote",
    "Aberto todos os dias": "Open daily",
    "Café da manhã": "Breakfast",
    "Almoço": "Lunch",
}

ES_RESTORE = {
    "Eventos no ": "Eventos en el ",
    "Capacidade variável": "Capacidad variable",
    "Estrutura e capacidade": "Estructura y capacidad",
    "salão principal": "salón principal",
    "terraços panorâmicos": "terrazas panorámicas",
    "terraço panorâmico": "terraza panorámica",
    "equipe receptiva": "equipo de recepción",
    "Reuniões matinais": "Reuniones matutinas",
    "Falar com nossa equipe": "Hablar con nuestro equipo",
    "Solicitar orçamento": "Solicitar presupuesto",
    "Aberto todos os dias": "Abierto todos los días",
    "Breakfast": "Desayuno",
    "Lunch": "Almuerzo",
}

PT_REPAIRS = {
    "Eventos en el ": "Eventos no ",
    "Hablar con nuestro equipo": "Falar com nossa equipe",
    "Solicitar presupuesto": "Solicitar orçamento",
    "Abierto todos los días": "Aberto todos os dias",
    "todos recibidos con": "todos recebidos com",
    "vista más impresionante": "vista mais impressionante",
    "main dining room": "salão principal",
    "panoramic terraces": "terraços panorâmicos",
    "hospitality team": "equipe receptiva",
    "Capacity varies": "Capacidade variável",
    "Structure & capacity": "Estrutura e capacidade",
    "Structure &amp; capacity": "Estrutura e capacidade",
}

LINK_REPAIRS = {
    'href="../es/sunset.html"': 'href="/es/entardecer.html"',
    "href='../es/sunset.html'": "href='/es/entardecer.html'",
    'href="../en/atardecer.html"': 'href="/en/entardecer.html"',
    "href='../en/atardecer.html'": "href='/en/entardecer.html'",
    'href="../sunset.html"': 'href="/en/entardecer.html"',
    "href='../sunset.html'": "href='/en/entardecer.html'",
    'href="../atardecer.html"': 'href="/es/entardecer.html"',
    "href='../atardecer.html'": "href='/es/entardecer.html'",
}

HTML_LANG_RE = re.compile(r"<html\b[^>]*\blang=[\"']([^\"']+)[\"']", re.IGNORECASE)


def detect_lang(rel: str, text: str) -> str:
    match = HTML_LANG_RE.search(text)
    if match:
        val = match.group(1).lower()
        if val.startswith("en"):
            return "en"
        if val.startswith("es"):
            return "es"
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt"


def apply_map(text: str, rel: str, repl: dict[str, str], counter: str) -> str:
    for old, new in repl.items():
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            COUNTERS[counter] += count
            REPORT.append(f"{counter.upper()}: {rel} | {old!r} -> {new!r} | {count}")
    return text


def process(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix != ".html" or ".git" in path.parts or rel.startswith("_"):
        return
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    text = apply_map(text, rel, TECH_REPAIRS, "tech_repaired")
    text = apply_map(text, rel, LINK_REPAIRS, "link_repaired")
    lang = detect_lang(rel, text)
    if lang == "en":
        text = apply_map(text, rel, EN_RESTORE, "en_restored")
    elif lang == "es":
        text = apply_map(text, rel, ES_RESTORE, "es_restored")
    else:
        text = apply_map(text, rel, PT_REPAIRS, "pt_repaired")

    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1
        REPORT.append(f"UPDATED: {rel}")


def write_report() -> None:
    out = ROOT / "_audit_reports"
    out.mkdir(exist_ok=True)
    report = out / "locale_restore_after_repairs_report.md"
    lines = ["# Locale Restore After Repairs", "", "## Contadores"]
    for key, value in COUNTERS.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Ações"])
    lines.extend(f"- {item}" for item in REPORT) if REPORT else lines.append("- Nenhuma ação necessária.")
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
