#!/usr/bin/env python3
"""
Sprint 1+2+3 Final Visual QA Hardening — Embaixada Carioca

Objetivo:
- validar de forma mais rígida os Sprints 1, 2 e 3 antes de avançar;
- corrigir duplicações editoriais remanescentes na home;
- corrigir resíduo de idioma visível em português;
- reforçar que o menu principal use Como Chegar, não Entardecer;
- validar que as páginas Como Chegar PT/EN/ES seguem a base visual da home:
  topo/nav, rating, idioma, reservar, hero, pedra livre, chips e CTAs.

Observação:
Esta validação é estrutural/HTML/CSS. Prints visuais reais continuam exigindo conferência no navegador.
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
    "editorial_fixes": 0,
    "language_fixes": 0,
    "nav_fixes": 0,
    "visual_checks_passed": 0,
    "warnings": 0,
}

HTML_LANG_RE = re.compile(r"<html\b[^>]*\blang=[\"']([^\"']+)[\"']", re.IGNORECASE)
NAV_LINKS_RE = re.compile(r"<ul\s+class=[\"']nav-links[\"'][^>]*>[\s\S]*?</ul>", re.IGNORECASE)
TOP_NAV_RE = re.compile(r"<nav\b[^>]*class=[\"'][^\"']*\btop\b[^\"']*[\"'][\s\S]*?</nav>", re.IGNORECASE)

MAIN_PAGES = [
    "index.html", "cafe-da-manha.html", "almoco.html", "como-chegar.html", "eventos.html", "cardapio.html", "guia-do-rio.html",
    "en/index.html", "en/cafe-da-manha.html", "en/almoco.html", "en/how-to-get-there.html", "en/eventos.html", "en/cardapio.html", "en/guia-do-rio.html",
    "es/index.html", "es/cafe-da-manha.html", "es/almoco.html", "es/como-llegar.html", "es/eventos.html", "es/cardapio.html", "es/guia-do-rio.html",
]

ACCESS_PAGES = {
    "como-chegar.html": ("pt", "Como Chegar", "/como-chegar.html"),
    "en/how-to-get-there.html": ("en", "HOW TO GET THERE", "/en/how-to-get-there.html"),
    "es/como-llegar.html": ("es", "CÓMO LLEGAR", "/es/como-llegar.html"),
}

TOP_NAV_TARGETS = {
    "pt": ("/como-chegar.html", "Como Chegar"),
    "en": ("/en/how-to-get-there.html", "HOW TO GET THERE"),
    "es": ("/es/como-llegar.html", "CÓMO LLEGAR"),
}

BAD_VISIBLE_TOKENS = {
    "pt": ["Reuniones matinais", "Para quién", "recibidos con", "vista más impresionante"],
    "en": ["Resposta direta", "Como chegar", "Por que essa página existe", "Solicitar orçamento", "Falar com nossa equipe"],
    "es": ["Resposta direta", "Como chegar", "Por que essa página existe", "Breakfast with a view", "Reserve a table"],
}

LANG_FIXES = {
    "pt": {
        "Reuniones matinais": "Reuniões matinais",
        "Reuniones matutinas": "Reuniões matinais",
        "Para quién": "Para quem",
        "recibidos con": "recebidos com",
        "vista más impresionante": "vista mais impressionante",
    },
    "en": {},
    "es": {},
}

EDITORIAL_REGEX_FIXES = [
    (
        re.compile(
            r"Entre os\s+<strong>restaurantes com vista no Rio de Janeiro</strong>,\s*a Embaixada Carioca ocupa um lugar único:\s*Entre os restaurantes com vista no Rio de Janeiro,\s*a Embaixada Carioca ocupa um lugar único:\s*fica dentro do Parque Bondinho Pão de Açúcar,\s*na primeira parada do teleférico,\s*com vista direta para o Pão de Açúcar e Baía de Guanabara,\s*na 1ª parada do teleférico,\s*a 227 metros de altitude\.\s*Projeto arquitetônico assinado pelo\s+<strong>Engelhaus Arquitetura</strong>\s*e identidade visual pela\s+<strong>Refinaria Design</strong>\s*— com janelões de piso a teto voltados para o Pão de Açúcar e Baía de Guanabara\.\s*A missão da casa: ser o consulado da gastronomia e da cultura brasileira para o planeta\.",
            re.IGNORECASE,
        ),
        "Entre os <strong>restaurantes com vista no Rio de Janeiro</strong>, a Embaixada Carioca ocupa um lugar único: fica dentro do Parque Bondinho Pão de Açúcar, no Morro da Urca, com vista direta para o Pão de Açúcar e a Baía de Guanabara, a 227 metros de altitude. Projeto arquitetônico assinado pelo <strong>Engelhaus Arquitetura</strong> e identidade visual pela <strong>Refinaria Design</strong> — com janelões de piso a teto voltados para o Pão de Açúcar. A missão da casa é ser o consulado da gastronomia e da cultura brasileira para o planeta.",
    ),
    (
        re.compile(
            r"Entre os restaurantes com vista no Rio de Janeiro,\s*a Embaixada Carioca ocupa um lugar único:\s*Entre os restaurantes com vista no Rio de Janeiro,\s*a Embaixada Carioca ocupa um lugar único:",
            re.IGNORECASE,
        ),
        "Entre os restaurantes com vista no Rio de Janeiro, a Embaixada Carioca ocupa um lugar único:",
    ),
]


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


def fix_editorial(text: str, rel: str) -> str:
    for pattern, replacement in EDITORIAL_REGEX_FIXES:
        text, count = pattern.subn(replacement, text)
        if count:
            COUNTERS["editorial_fixes"] += count
            REPORT.append(f"EDITORIAL: {rel} | duplicate story paragraph fixed | {count}")
    return text


def fix_language(text: str, rel: str, lang: str) -> str:
    for old, new in LANG_FIXES.get(lang, {}).items():
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            COUNTERS["language_fixes"] += count
            REPORT.append(f"LANG: {rel} | {old!r} -> {new!r} | {count}")
    return text


def ensure_top_nav(text: str, rel: str, lang: str) -> str:
    href, label = TOP_NAV_TARGETS[lang]

    def repl(match: re.Match[str]) -> str:
        nav = match.group(0)
        original = nav
        nav = re.sub(
            r"<li><a\s+href=[\"'][^\"']*(?:entardecer|sunset|atardecer)\.html[\"'][^>]*>[\s\S]*?</a></li>",
            f'<li><a href="{href}"><span class="drawer-icon">📍</span>{label}</a></li>',
            nav,
            count=1,
            flags=re.IGNORECASE,
        )
        # Corrige alvo errado criado por scripts anteriores.
        if lang == "en":
            nav = nav.replace('href="/en/como-chegar.html"', 'href="/en/how-to-get-there.html"')
        if lang == "es":
            nav = nav.replace('href="/es/como-chegar.html"', 'href="/es/como-llegar.html"')
        if nav != original:
            COUNTERS["nav_fixes"] += 1
            REPORT.append(f"NAV: {rel} | menu principal reforçado para {label}")
        return nav

    return NAV_LINKS_RE.sub(repl, text, count=1)


def visible_like(text: str) -> str:
    text = re.sub(r"<script\b[\s\S]*?</script>|<style\b[\s\S]*?</style>|<!--[^>]*-->", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    COUNTERS["warnings"] += 1


def validate_page(rel: str, text: str, lang: str) -> None:
    top_match = TOP_NAV_RE.search(text)
    nav_match = NAV_LINKS_RE.search(text)
    visible = visible_like(text)
    if not top_match:
        warn(f"{rel}: sem nav.top")
    if not nav_match:
        warn(f"{rel}: sem ul.nav-links")
    else:
        nav = nav_match.group(0)
        href, label = TOP_NAV_TARGETS[lang]
        if href not in nav or label.split()[0] not in nav:
            warn(f"{rel}: menu principal não contém {label} com {href}")
        if re.search(r"href=[\"'][^\"']*(?:entardecer|sunset|atardecer)\.html[\"']", nav, re.IGNORECASE):
            warn(f"{rel}: menu principal ainda contém Entardecer/Sunset/Atardecer")
    for required in ["nav-rating-badge", "lang-switcher", "Reservar"]:
        if required not in text and required.upper() not in text:
            warn(f"{rel}: falta elemento de topo {required}")
    for bad in BAD_VISIBLE_TOKENS.get(lang, []):
        if bad in visible:
            warn(f"{rel}: texto visível contém resíduo `{bad}`")
    COUNTERS["visual_checks_passed"] += 1


def validate_access_page(rel: str, text: str) -> None:
    required_tokens = [
        "class=\"top\"", "class=\"nav-inner\"", "class=\"page-hero\"", "class=\"page-hero-photo\"",
        "class=\"page-hero-overlay\"", "class=\"hero-chips\"", "class=\"hero-ctas\"",
        "page-hero h1", "right:clamp", "max-width:min", "page-hero-photo img",
    ]
    for token in required_tokens:
        if token not in text:
            warn(f"{rel}: Como Chegar sem token visual esperado `{token}`")


def process_html(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix != ".html" or ".git" in path.parts or rel.startswith("_"):
        return
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    lang = detect_lang(rel, original)
    text = original
    text = fix_editorial(text, rel)
    text = fix_language(text, rel, lang)
    if rel in MAIN_PAGES:
        text = ensure_top_nav(text, rel, lang)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1
        REPORT.append(f"UPDATED: {rel}")


def validate_all() -> None:
    for rel in MAIN_PAGES:
        path = ROOT / rel
        if not path.exists():
            warn(f"{rel}: página principal ausente")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        lang = detect_lang(rel, text)
        validate_page(rel, text, lang)
    for rel in ACCESS_PAGES:
        path = ROOT / rel
        if not path.exists():
            warn(f"{rel}: página Como Chegar ausente")
            continue
        validate_access_page(rel, path.read_text(encoding="utf-8", errors="ignore"))


def write_report() -> None:
    out = ROOT / "_audit_reports"
    out.mkdir(exist_ok=True)
    report = out / "sprint123_final_visual_validation_report.md"
    lines = [
        "# Sprint 1+2+3 — Final Visual Validation",
        "",
        "## Objetivo",
        "Validar menu principal, botões, idioma, duplicações editoriais e padrão visual das páginas Como Chegar antes de avançar.",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Correções aplicadas"])
    lines.extend(f"- {item}" for item in REPORT) if REPORT else lines.append("- Nenhuma correção necessária.")
    lines.extend(["", "## Alertas"])
    lines.extend(f"- {item}" for item in WARNINGS) if WARNINGS else lines.append("- Nenhum alerta estrutural/visual encontrado.")
    lines.append("")
    report.write_text("\n".join(lines), encoding="utf-8")
    print(report.read_text(encoding="utf-8"))


def main() -> int:
    for path in sorted(ROOT.rglob("*.html")):
        process_html(path)
    validate_all()
    write_report()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
