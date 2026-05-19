#!/usr/bin/env python3
"""
Final Quality Repairs — Embaixada Carioca.

Correções finais antes da auditoria estrutural:
- repara tokens técnicos quebrados;
- remove preload duplicado de hero.jpg quando já existe WebP;
- corrige portunhol/inglês residual seguro em páginas PT;
- corrige links internos recorrentes quebrados;
- cria fallback assets/style.css para páginas legadas;
- normaliza referências de hero-bg/hero.jpg para assets existentes.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT: list[str] = []
COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "technical_repairs": 0,
    "duplicate_preloads_removed": 0,
    "text_repairs": 0,
    "link_repairs": 0,
    "fallback_assets_created": 0,
}

TECH_REPAIRS = {
    "send_page_vista": "send_page_view",
    "page_vista": "page_view",
    "vistaport-fit": "viewport-fit",
    "name=\"vistaport\"": "name=\"viewport\"",
    "name='vistaport'": "name='viewport'",
}

TEXT_REPAIRS = {
    "Eventos en el ": "Eventos no ",
    "Hablar con nuestro equipo": "Falar com nossa equipe",
    "todos recibidos con": "todos recebidos com",
    "vista más impresionante": "vista mais impressionante",
    "Reuniones matutinas": "Reuniões matinais",
    "main dining room": "salão principal",
    "panoramic terraces": "terraços panorâmicos",
    "hospitality team": "equipe receptiva",
    "Capacity varies": "Capacidade variável",
    "Structure &amp; capacity": "Estrutura e capacidade",
    "Structure & capacity": "Estrutura e capacidade",
    "para Baía de Guanabara": "para a Baía de Guanabara",
    "para Baía": "para a Baía",
}

LINK_REPAIRS = {
    'href="assets/style.css"': 'href="/assets/style.css"',
    "href='assets/style.css'": "href='/assets/style.css'",
    'href="../assets/style.css"': 'href="/assets/style.css"',
    "href='../assets/style.css'": "href='/assets/style.css'",
    'href="/assets/hero-bg.webp"': 'href="/assets/hero.webp"',
    "href='/assets/hero-bg.webp'": "href='/assets/hero.webp'",
    'src="/assets/hero-bg.webp"': 'src="/assets/hero.webp"',
    "src='/assets/hero-bg.webp'": "src='/assets/hero.webp'",
    'href="assets/hero.jpg"': 'href="/assets/hero.webp"',
    "href='assets/hero.jpg'": "href='/assets/hero.webp'",
    'src="assets/hero.jpg"': 'src="/assets/hero.webp"',
    "src='assets/hero.jpg'": "src='/assets/hero.webp'",
    'href="../sunset.html"': 'href="/en/entardecer.html"',
    "href='../sunset.html'": "href='/en/entardecer.html'",
    'href="../atardecer.html"': 'href="/es/entardecer.html"',
    "href='../atardecer.html'": "href='/es/entardecer.html'",
    'href="../en/atardecer.html"': 'href="/en/entardecer.html"',
    "href='../en/atardecer.html'": "href='/en/entardecer.html'",
}

HERO_JPG_PRELOAD_RE = re.compile(r'\n?\s*<link\b(?=[^>]*rel=["\']preload["\'])(?=[^>]*as=["\']image["\'])(?=[^>]*href=["\']/assets/hero\.jpg["\'])[^>]*>\s*', re.IGNORECASE)
A_SPAM_RE = re.compile(r'\bA(?:\s+A){3,}\s+referência', re.IGNORECASE)


def create_fallback_assets() -> None:
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    style = assets / "style.css"
    if not style.exists():
        style.write_text("@import url('/assets/fonts/fonts.css');\nhtml,body{margin:0;padding:0;}\nimg{max-width:100%;height:auto;}\n", encoding="utf-8")
        COUNTERS["fallback_assets_created"] += 1
        REPORT.append("CREATED: assets/style.css fallback")


def process_html(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if ".git" in path.parts or rel.startswith("_") or path.suffix != ".html":
        return
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original

    for old, new in TECH_REPAIRS.items():
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            COUNTERS["technical_repairs"] += count
            REPORT.append(f"TECH: {rel} | {old} -> {new} | {count}")

    before = text
    text = HERO_JPG_PRELOAD_RE.sub("\n", text)
    removed = before.count('/assets/hero.jpg') - text.count('/assets/hero.jpg')
    if removed > 0:
        COUNTERS["duplicate_preloads_removed"] += removed
        REPORT.append(f"PRELOAD: {rel} | hero.jpg preload removido | {removed}")

    for old, new in TEXT_REPAIRS.items():
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            COUNTERS["text_repairs"] += count
            REPORT.append(f"TEXT: {rel} | {old!r} -> {new!r} | {count}")

    text, spam_count = A_SPAM_RE.subn("A referência", text)
    if spam_count:
        COUNTERS["text_repairs"] += spam_count
        REPORT.append(f"TEXT: {rel} | sequência 'A A A...' corrigida | {spam_count}")

    for old, new in LINK_REPAIRS.items():
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            COUNTERS["link_repairs"] += count
            REPORT.append(f"LINK: {rel} | {old} -> {new} | {count}")

    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1
        REPORT.append(f"UPDATED: {rel}")


def write_report() -> None:
    out = ROOT / "_audit_reports"
    out.mkdir(exist_ok=True)
    report = out / "final_quality_repairs_report.md"
    lines = ["# Final Quality Repairs", "", "## Contadores"]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Ações"])
    lines.extend(f"- {x}" for x in REPORT) if REPORT else lines.append("- Nenhuma ação necessária.")
    lines.append("")
    report.write_text("\n".join(lines), encoding="utf-8")
    print(report.read_text(encoding="utf-8"))


def main() -> int:
    create_fallback_assets()
    for path in sorted(ROOT.rglob("*.html")):
        process_html(path)
    write_report()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
