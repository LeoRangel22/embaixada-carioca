#!/usr/bin/env python3
"""Final AAA Closeout Fixes — Embaixada Carioca.

Fecha os pontos apontados pela auditoria mestre:
1. Recalibrar/facilitar integridade técnica sem falso positivo por JSON-LD.
2. Garantir final_design_lock/button_hierarchy_lock nas páginas de território.
3. Inserir viewport/meta description ausentes ou fora de faixa em páginas pontuais.
4. Tratar páginas utilitárias com metadados básicos.
5. Corrigir pequena marcação órfã detectada no sunset EN.
"""
from __future__ import annotations

from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "final_aaa_closeout_fixes_report.md"
REPORT_CSV = REPORT_DIR / "final_aaa_closeout_fixes_details.csv"

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next"}
UTILITY_DESCRIPTIONS = {
    "404.html": "Página não encontrada no site da Embaixada Carioca. Volte para a home, consulte o cardápio ou faça sua reserva.",
    "offline.html": "Você está offline. A Embaixada Carioca carrega informações essenciais para reserva, cardápio e como chegar quando a conexão voltar.",
    "home-preview.html": "Prévia interna da home da Embaixada Carioca para validação visual de design, conteúdo, reservas e experiência do visitante.",
}
TARGET_DESCRIPTIONS = {
    "en/sunset.html": "Sunset drinks and romantic views on Urca Hill, inside Sugarloaf Cable Car Park. Caipirinhas, snacks and tables with Rio scenery.",
    "es/eventos.html": "Eventos en el Morro da Urca, dentro del Parque Bondinho Pan de Azúcar, con vista, gastronomía brasileña y atención para grupos.",
}

HEAD_RE = re.compile(r"</head>", re.I)
BODY_RE = re.compile(r"</body>", re.I)
VIEWPORT_RE = re.compile(r"<meta\b(?=[^>]*name=[\"']viewport[\"'])[^>]*>", re.I)
DESC_RE = re.compile(r"<meta\b(?=[^>]*name=[\"']description[\"'])[^>]*>", re.I)
DESC_CONTENT_RE = re.compile(r"content=([\"'])(.*?)\1", re.I | re.S)
FINAL_DESIGN_MARKER = "EC Final Design Consistency Lock"
BRAND_CLOSEOUT_MARKER = "EC AAA Closeout Design Lock"
ORPHAN_SUNSET_RE = re.compile(r"\n?\s*<sunset-style visit on Urca Hill with Sugarloaf Mountain in the foreground>\s*\n?", re.I)

CLOSEOUT_CSS = f"""<!-- {BRAND_CLOSEOUT_MARKER} -->
<style id="ec-aaa-closeout-design-lock">
/* Final AAA closeout — Somente reserva / TagMe fica laranja; botões secundários são vazados e invertem no hover. */
:root{{--ec-blue:#00405a;--ec-green:#335d4a;--ec-yellow:#f59b1e;--ec-sand:#ede2c9;--ec-paper:#f6efde;--ec-gray:#485156;}}
html body nav.top .nav-links a{{color:var(--ec-blue);}}
html body nav.top a.btn[href*="tagme"],html body a.btn[href*="tagme"],html body a.btn[href*="reserv"],html body .ctas a[href*="tagme"],html body .hero-ctas a[href*="tagme"]{{background:var(--ec-yellow)!important;border-color:var(--ec-yellow)!important;color:var(--ec-blue)!important;-webkit-text-fill-color:var(--ec-blue)!important;}}
html body .btn-secondary,html body a.btn-secondary,html body .ctas a:not([href*="tagme"]):not([href*="reserv"]),html body .hero-ctas a:not([href*="tagme"]):not([href*="reserv"]){{background:rgba(0,64,90,.18)!important;border:1px solid rgba(246,239,222,.82)!important;color:var(--ec-paper)!important;-webkit-text-fill-color:var(--ec-paper)!important;}}
html body .btn-secondary:hover,html body a.btn-secondary:hover,html body .ctas a:not([href*="tagme"]):not([href*="reserv"]):hover,html body .hero-ctas a:not([href*="tagme"]):not([href*="reserv"]):hover{{background:var(--ec-paper)!important;color:var(--ec-blue)!important;-webkit-text-fill-color:var(--ec-blue)!important;}}
</style>
<!-- /{BRAND_CLOSEOUT_MARKER} -->"""

COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "viewport_added": 0,
    "description_added": 0,
    "description_rewritten": 0,
    "closeout_design_lock_added": 0,
    "orphan_markup_fixed": 0,
}
DETAILS: list[dict[str, object]] = []


def is_html(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return path.suffix.lower() == ".html" and not rel.startswith("_") and not any(part in SKIP_DIRS for part in path.parts)


def add_viewport(text: str, rel: str) -> str:
    if VIEWPORT_RE.search(text):
        return text
    meta = '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    if HEAD_RE.search(text):
        COUNTERS["viewport_added"] += 1
        DETAILS.append({"file": rel, "action": "viewport_added", "detail": "responsive viewport inserted"})
        return HEAD_RE.sub(meta + "</head>", text, count=1)
    return text


def set_description(text: str, rel: str, desc: str) -> str:
    if DESC_RE.search(text):
        def repl(match: re.Match[str]) -> str:
            tag = match.group(0)
            if DESC_CONTENT_RE.search(tag):
                return DESC_CONTENT_RE.sub(f'content="{desc}"', tag, count=1)
            return tag.rstrip(" />") + f' content="{desc}">'
        COUNTERS["description_rewritten"] += 1
        DETAILS.append({"file": rel, "action": "description_rewritten", "detail": desc})
        return DESC_RE.sub(repl, text, count=1)
    meta = f'<meta name="description" content="{desc}">\n'
    if HEAD_RE.search(text):
        COUNTERS["description_added"] += 1
        DETAILS.append({"file": rel, "action": "description_added", "detail": desc})
        return HEAD_RE.sub(meta + "</head>", text, count=1)
    return text


def ensure_descriptions(text: str, rel: str) -> str:
    if rel in UTILITY_DESCRIPTIONS:
        return set_description(text, rel, UTILITY_DESCRIPTIONS[rel])
    if rel in TARGET_DESCRIPTIONS:
        return set_description(text, rel, TARGET_DESCRIPTIONS[rel])
    return text


def add_closeout_design_lock(text: str, rel: str) -> str:
    # Garante o marcador final em páginas de território antigas, sem duplicar onde já existe.
    if FINAL_DESIGN_MARKER in text or BRAND_CLOSEOUT_MARKER in text:
        return text
    if HEAD_RE.search(text):
        COUNTERS["closeout_design_lock_added"] += 1
        DETAILS.append({"file": rel, "action": "closeout_design_lock_added", "detail": "button hierarchy + design marker"})
        return HEAD_RE.sub(CLOSEOUT_CSS + "\n</head>", text, count=1)
    return text


def fix_orphan_markup(text: str, rel: str) -> str:
    if not ORPHAN_SUNSET_RE.search(text):
        return text
    replacement = '\n<meta property="og:image:alt" content="Sunset-style visit on Urca Hill with Sugarloaf Mountain in the foreground">\n'
    text = ORPHAN_SUNSET_RE.sub(replacement, text)
    COUNTERS["orphan_markup_fixed"] += 1
    DETAILS.append({"file": rel, "action": "orphan_markup_fixed", "detail": "sunset image alt meta restored"})
    return text


def process(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    text = fix_orphan_markup(text, rel)
    text = add_viewport(text, rel)
    text = ensure_descriptions(text, rel)
    text = add_closeout_design_lock(text, rel)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1


def write_reports() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    lines = [
        "# Final AAA Closeout Fixes",
        "",
        "## Objetivo",
        "Fechar os pontos da auditoria mestre: viewport/meta description, design lock em páginas de território, botão hierarchy lock e correção de marcação órfã.",
        "",
        "## Contadores",
    ]
    lines.extend(f"- {k}: {v}" for k, v in COUNTERS.items())
    lines.extend(["", "## Ações aplicadas"])
    if DETAILS:
        for d in DETAILS:
            lines.append(f"- {d['file']}: {d['action']} — {d['detail']}")
    else:
        lines.append("- Nenhuma alteração necessária.")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    with REPORT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "action", "detail"])
        writer.writeheader()
        writer.writerows(DETAILS)
    print(REPORT_MD.read_text(encoding="utf-8"))


def main() -> int:
    for path in sorted(ROOT.rglob("*.html")):
        if is_html(path):
            process(path)
    write_reports()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
