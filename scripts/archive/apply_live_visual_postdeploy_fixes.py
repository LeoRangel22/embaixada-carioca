#!/usr/bin/env python3
"""
Live Visual Post-Deploy Fixes — Embaixada Carioca

Corrige problemas identificados na validação real pós-deploy:
- coordenadas visíveis antigas na hero bottom bar;
- seta residual no botão Reservar do topo em EN/ES;
- resíduos visuais de idioma/typos na home em espanhol e inglês;
- reforço do item Como Chegar no menu principal PT/EN/ES.

Este script roda depois do Excellence Gate para que o site publicado reflita a validação visual real.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT: list[str] = []
COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "coordinate_fixes": 0,
    "top_button_arrow_fixes": 0,
    "menu_fixes": 0,
    "language_visual_fixes": 0,
}

HTML_LANG_RE = re.compile(r"<html\b[^>]*lang=[\"']([^\"']+)[\"']", re.I)
NAV_LINKS_RE = re.compile(r"<ul\s+class=[\"']nav-links[\"'][^>]*>[\s\S]*?</ul>", re.I)
TOP_NAV_RE = re.compile(r"<nav\b[^>]*class=[\"'][^\"']*\btop\b[^\"']*[\"'][\s\S]*?</nav>", re.I)

# Pedido visual: coordenadas em DMS corrigidas.
PT_ES_COORD = "22°57′03″S · 43°09′51″O"
EN_COORD = "22°57′03″S · 43°09′51″W"
COORD_PATTERNS = [
    re.compile(r"22°56[′']58[″\"]S\s*·\s*43°09[′']55[″\"]W"),
    re.compile(r"22°56[′']58[″\"]S\s*·\s*43°09[′']55[″\"]O"),
    re.compile(r"22°\s*56\s*[′']\s*58\s*[″\"]?\s*S\s*·\s*43°\s*09\s*[′']\s*55\s*[″\"]?\s*[WO]"),
]

VISUAL_REPLACEMENTS = {
    "en": {
        "Events corporativos.": "Corporate events.",
        "Menu completo": "Complete menu",
        "Roteiro Rio de Janeiro O Guia Definitivo.": "Rio de Janeiro itinerary — the definitive guide.",
    },
    "es": {
        "Bondinhel": "Bondinho",
        "O Morro da Urca é o seu evento — o espaço mais bonito do Rio de Janeiro.": "El Morro da Urca es el escenario de tu evento — un espacio panorámico inolvidable en Río de Janeiro.",
        "Venha nos visitar.": "Ven a visitarnos.",
        "Endereço & Acesso": "Dirección y acceso",
        "Acceso vía teleférico (teleférico) ou a pé pela Praia Vermelha": "Acceso en Bondinho con entrada del parque, o por el sendero de Praia Vermelha cuando esté abierto",
        "Roteiros & grupos.": "Itinerarios y grupos.",
        "Roteiros & grupos": "Itinerarios y grupos",
        "Quando Todos los días": "Cuándo Todos los días",
        "Harmonização Cachaças y vinos": "Maridaje Cachaças y vinos",
        "Inauguração": "Inauguración",
        "227 metros · sobre a Baía": "227 metros · sobre la bahía",
        "★ melhor feijoada ★ PRÊMIO": "★ mejor feijoada ★ PREMIO",
        "vista panorámica mais bonita do mundo": "vista panorámica más bonita del mundo",
        "vistas panorâmicas": "vistas panorámicas",
        "Reciba a su equipo": "Recibe a tu equipo",
        "Confraternizaciones": "Celebraciones",
        "reserve ★ via": "reserva ★ vía",
        "Tagme ★ embaixada ★": "Tagme ★ Embaixada ★",
    },
}


def lang_for(rel: str, text: str) -> str:
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
    return "pt-BR"


def target_nav(lang: str) -> tuple[str, str]:
    if lang == "en":
        return "/en/how-to-get-there.html", "HOW TO GET THERE"
    if lang == "es":
        return "/es/como-llegar.html", "CÓMO LLEGAR"
    return "/como-chegar.html", "COMO CHEGAR"


def fix_coordinates(text: str, rel: str, lang: str) -> str:
    original = text
    target = EN_COORD if lang == "en" else PT_ES_COORD
    for pattern in COORD_PATTERNS:
        text = pattern.sub(target, text)
    if text != original:
        COUNTERS["coordinate_fixes"] += 1
        REPORT.append(f"COORDINATES: {rel} -> {target}")
    return text


def fix_top_reserve_button(text: str, rel: str) -> str:
    original = text

    def repl_nav(match: re.Match[str]) -> str:
        nav = match.group(0)
        nav = re.sub(r">\s*(Reservar|Reserve)\s*[→›»]\s*</a>", lambda m: f">{m.group(1)}</a>", nav, flags=re.I)
        return nav

    text = TOP_NAV_RE.sub(repl_nav, text, count=1)
    if text != original:
        COUNTERS["top_button_arrow_fixes"] += 1
        REPORT.append(f"TOP_BUTTON_ARROW: {rel}")
    return text


def fix_menu(text: str, rel: str, lang: str) -> str:
    href, label = target_nav(lang)
    original = text

    def repl(match: re.Match[str]) -> str:
        nav = match.group(0)
        nav = nav.replace('/en/como-chegar.html', '/en/how-to-get-there.html').replace('/es/como-chegar.html', '/es/como-llegar.html')
        nav = re.sub(r'<span\s+class=["\']drawer-icon["\']>📍</span>\s*', '', nav, flags=re.I)
        if href in nav:
            nav = re.sub(rf'(<a\s+href=["\']{re.escape(href)}["\'][^>]*>)[\s\S]*?(</a>)', rf'\1{label}\2', nav, count=1, flags=re.I)
            return nav
        nav2, count = re.subn(r'<li><a\s+href=["\'][^"\']*(?:entardecer|sunset|atardecer)\.html["\'][^>]*>[\s\S]*?</a></li>', f'<li><a href="{href}">{label}</a></li>', nav, count=1, flags=re.I)
        return nav2 if count else nav

    text = NAV_LINKS_RE.sub(repl, text, count=1)
    if text != original:
        COUNTERS["menu_fixes"] += 1
        REPORT.append(f"MENU: {rel}")
    return text


def fix_visual_language(text: str, rel: str, lang: str) -> str:
    original = text
    for old, new in VISUAL_REPLACEMENTS.get(lang, {}).items():
        text = text.replace(old, new)
    if text != original:
        COUNTERS["language_visual_fixes"] += 1
        REPORT.append(f"VISUAL_LANGUAGE: {rel}")
    return text


def process(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix != ".html" or rel.startswith("_") or ".git" in path.parts:
        return
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    lang = lang_for(rel, original)
    text = original
    text = fix_coordinates(text, rel, lang)
    text = fix_top_reserve_button(text, rel)
    text = fix_menu(text, rel, lang)
    text = fix_visual_language(text, rel, lang)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1


def write_report() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    out = REPORT_DIR / "live_visual_postdeploy_fixes_report.md"
    lines = [
        "# Live Visual Post-Deploy Fixes",
        "",
        "## Objetivo",
        "Corrigir problemas encontrados na validação real pós-deploy: coordenadas visíveis, seta no botão Reservar do topo, menu Como Chegar e resíduos visuais de idioma.",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Ações"])
    lines.extend(f"- {item}" for item in REPORT) if REPORT else lines.append("- Nenhuma ação necessária.")
    lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


def main() -> int:
    for path in sorted(ROOT.rglob("*.html")):
        process(path)
    write_report()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
