#!/usr/bin/env python3
"""Safe fixer for current Embaixada Carioca pages before creating new landing pages.

Fixes applied:
- Inject consolidated stabilization CSS link.
- Normalize multiple H1 headings by keeping the first H1 and demoting the rest to H2.
- Add strategic image alt texts when missing/generic/non-strategic.
- Insert a compact strategic internal-link block when missing.
- Produce a report.

Intentionally NOT applied automatically:
- Copy deletion/deduplication, because current GEO/AIO density is a ranking asset and needs editorial review.
"""
from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "existing_pages_content_structure_fix_report.md"
CSS_HREF = "/assets/css/ec-stabilization-base.css"
CSS_LINK = f'<link rel="stylesheet" href="{CSS_HREF}">'
MARKER_START = "<!-- EC STRATEGIC INTERNAL LINKS START -->"
MARKER_END = "<!-- EC STRATEGIC INTERNAL LINKS END -->"

PAGES = [
    "index.html",
    "cafe-da-manha.html",
    "almoco.html",
    "cardapio.html",
    "como-chegar.html",
    "eventos.html",
    "guia-do-rio.html",
]

PAGE_CONTEXT = {
    "index.html": {
        "alt_base": "Embaixada Carioca, restaurante no Morro da Urca com vista para o Pão de Açúcar no Rio de Janeiro",
        "links": [
            ("Café da manhã com vista", "cafe-da-manha.html"),
            ("Almoço no Morro da Urca", "almoco.html"),
            ("Cardápio completo", "cardapio.html"),
            ("Eventos com vista", "eventos.html"),
            ("Como chegar", "como-chegar.html"),
        ],
    },
    "cafe-da-manha.html": {
        "alt_base": "Café da manhã da Embaixada Carioca com vista para o Pão de Açúcar no Morro da Urca",
        "links": [
            ("Reservar almoço no Morro da Urca", "almoco.html"),
            ("Ver cardápio completo", "cardapio.html"),
            ("Como chegar ao Parque Bondinho", "como-chegar.html"),
            ("Conhecer a Embaixada Carioca", "index.html"),
        ],
    },
    "almoco.html": {
        "alt_base": "Almoço brasileiro na Embaixada Carioca no Morro da Urca com vista para o Pão de Açúcar",
        "links": [
            ("Ver cardápio completo", "cardapio.html"),
            ("Café da manhã com vista", "cafe-da-manha.html"),
            ("Como chegar", "como-chegar.html"),
            ("Conhecer o restaurante", "index.html"),
        ],
    },
    "cardapio.html": {
        "alt_base": "Cardápio da Embaixada Carioca no Morro da Urca com pratos brasileiros, caipirinhas e vista para o Pão de Açúcar",
        "links": [
            ("Café da manhã", "cafe-da-manha.html"),
            ("Almoço com vista", "almoco.html"),
            ("Eventos com vista", "eventos.html"),
            ("Como chegar", "como-chegar.html"),
        ],
    },
    "como-chegar.html": {
        "alt_base": "Como chegar à Embaixada Carioca no Morro da Urca dentro do Parque Bondinho Pão de Açúcar",
        "links": [
            ("Café da manhã no Morro da Urca", "cafe-da-manha.html"),
            ("Almoço com vista", "almoco.html"),
            ("Cardápio", "cardapio.html"),
            ("Página inicial", "index.html"),
        ],
    },
    "eventos.html": {
        "alt_base": "Eventos na Embaixada Carioca no Morro da Urca com vista para o Pão de Açúcar no Rio de Janeiro",
        "links": [
            ("Cardápio para eventos", "cardapio.html"),
            ("Como chegar", "como-chegar.html"),
            ("Conhecer o restaurante", "index.html"),
            ("Guia do Rio", "guia-do-rio.html"),
        ],
    },
    "guia-do-rio.html": {
        "alt_base": "Guia do Rio de Janeiro da Embaixada Carioca com restaurantes, Morro da Urca e Pão de Açúcar",
        "links": [
            ("Restaurante no Morro da Urca", "index.html"),
            ("Café da manhã com vista", "cafe-da-manha.html"),
            ("Almoço no Pão de Açúcar", "almoco.html"),
            ("Eventos com vista no Rio", "eventos.html"),
            ("Como chegar", "como-chegar.html"),
        ],
    },
}

GENERIC_ALT_VALUES = {"", "foto", "imagem", "img", "banner", "hero", "restaurante", "café", "cafe", "mesa", "prato", "view", "image", "photo"}
STRATEGIC_TERMS = ("Embaixada Carioca", "Morro da Urca", "Pão de Açúcar", "Rio de Janeiro", "Bondinho", "vista", "Urca")


class ImgParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.imgs: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "img":
            return
        self.imgs.append({k.lower(): v or "" for k, v in attrs})


def inject_css(html: str) -> tuple[str, bool]:
    if CSS_HREF in html:
        return html, False
    font_link = re.search(r"<link[^>]+fonts\.css[^>]*>", html, flags=re.I)
    if font_link:
        pos = font_link.end()
        return html[:pos] + "\n" + CSS_LINK + html[pos:], True
    return re.sub(r"</head>", CSS_LINK + "\n</head>", html, count=1, flags=re.I), True


def normalize_h1(html: str) -> tuple[str, int]:
    matches = list(re.finditer(r"<h1\b([^>]*)>(.*?)</h1>", html, flags=re.I | re.S))
    if len(matches) <= 1:
        return html, 0
    changed = html
    demoted = 0
    # Work from the end so offsets stay valid.
    for m in reversed(matches[1:]):
        attrs = m.group(1)
        inner = m.group(2)
        replacement = f"<h2{attrs}>{inner}</h2>"
        changed = changed[:m.start()] + replacement + changed[m.end():]
        demoted += 1
    return changed, demoted


def needs_alt_fix(alt: str) -> bool:
    clean = re.sub(r"\s+", " ", alt.strip())
    if clean.lower() in GENERIC_ALT_VALUES:
        return True
    if len(clean) < 18:
        return True
    if not any(term.lower() in clean.lower() for term in STRATEGIC_TERMS):
        return True
    return False


def alt_for_src(src: str, context: str) -> str:
    s = src.lower()
    if "cafe" in s or "café" in s:
        return "Café da manhã da Embaixada Carioca com vista para o Pão de Açúcar no Morro da Urca"
    if "almoco" in s or "almoço" in s or "feijoada" in s or "picanha" in s:
        return "Almoço brasileiro da Embaixada Carioca no Morro da Urca com vista para o Pão de Açúcar"
    if "evento" in s:
        return "Evento na Embaixada Carioca no Morro da Urca com vista panorâmica para o Rio de Janeiro"
    if "hero" in s or "vista" in s or "pao" in s or "pão" in s:
        return "Vista do Pão de Açúcar e da Baía de Guanabara a partir da Embaixada Carioca no Morro da Urca"
    if "cardapio" in s or "menu" in s:
        return "Cardápio da Embaixada Carioca no Morro da Urca com gastronomia brasileira e caipirinhas"
    return context


def fix_img_alts(html: str, filename: str) -> tuple[str, int]:
    context = PAGE_CONTEXT[filename]["alt_base"]
    fixed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal fixed
        tag = match.group(0)
        src_m = re.search(r"\bsrc\s*=\s*(['\"])(.*?)\1", tag, flags=re.I | re.S)
        alt_m = re.search(r"\balt\s*=\s*(['\"])(.*?)\1", tag, flags=re.I | re.S)
        src = src_m.group(2) if src_m else ""
        current_alt = alt_m.group(2) if alt_m else ""
        if not needs_alt_fix(current_alt):
            return tag
        new_alt = alt_for_src(src, context)
        fixed += 1
        if alt_m:
            return tag[:alt_m.start()] + f'alt="{new_alt}"' + tag[alt_m.end():]
        return tag[:-1].rstrip() + f' alt="{new_alt}">'

    new_html = re.sub(r"<img\b[^>]*>", repl, html, flags=re.I | re.S)
    return new_html, fixed


def link_exists(html: str, href: str) -> bool:
    patterns = [href, "/" + href]
    if href == "index.html":
        patterns.extend(["/", "https://www.embaixadacarioca.com/"])
    return any(p in html for p in patterns)


def strategic_links_block(filename: str, missing: list[tuple[str, str]]) -> str:
    links_html = "\n".join([f'        <a href="{href}">{label}</a>' for label, href in missing])
    return f"""
{MARKER_START}
<section class="ec-strategic-links" aria-label="Navegação estratégica Embaixada Carioca">
  <div class="ec-strategic-links-inner">
    <p class="ec-strategic-links-kicker">Continue explorando</p>
    <h2>Planeje melhor sua visita à Embaixada Carioca</h2>
    <nav class="ec-strategic-links-nav" aria-label="Links internos recomendados">
{links_html}
    </nav>
  </div>
</section>
<style>
.ec-strategic-links{{padding:clamp(32px,5vw,64px) clamp(20px,4vw,56px);background:#f6efde;border-top:1px solid rgba(0,64,90,.12)}}
.ec-strategic-links-inner{{max-width:1120px;margin:0 auto;text-align:center}}
.ec-strategic-links-kicker{{margin:0 0 8px;color:#9a6500;font:800 12px/1.2 Catamaran,system-ui,sans-serif;letter-spacing:.16em;text-transform:uppercase}}
.ec-strategic-links h2{{margin:0 0 18px;color:#00405a;font:800 clamp(24px,3vw,38px)/1.05 Catamaran,system-ui,sans-serif}}
.ec-strategic-links-nav{{display:flex;flex-wrap:wrap;justify-content:center;gap:10px}}
.ec-strategic-links-nav a{{display:inline-flex;align-items:center;min-height:42px;padding:10px 14px;border:1px solid rgba(0,64,90,.18);border-radius:999px;background:#fff;color:#00405a!important;text-decoration:none;font:800 13px/1.1 Catamaran,system-ui,sans-serif}}
.ec-strategic-links-nav a:hover{{border-color:#f59b1e;box-shadow:0 8px 22px rgba(0,64,90,.12)}}
</style>
{MARKER_END}
""".strip()


def fix_internal_links(html: str, filename: str) -> tuple[str, int]:
    if MARKER_START in html:
        return html, 0
    desired = PAGE_CONTEXT[filename]["links"]
    missing = [(label, href) for label, href in desired if not link_exists(html, href)]
    if not missing:
        return html, 0
    block = strategic_links_block(filename, missing)
    # Insert before footer if present, otherwise before scripts/body end.
    for needle in ["<footer", "</main>", "</body>"]:
        idx = html.lower().find(needle)
        if idx != -1:
            return html[:idx] + block + "\n" + html[idx:], len(missing)
    return html + "\n" + block, len(missing)


def fix_page(filename: str) -> dict[str, int | bool]:
    path = ROOT / filename
    html = path.read_text(encoding="utf-8")
    original = html
    html, css_added = inject_css(html)
    html, h1_demoted = normalize_h1(html)
    html, alt_fixed = fix_img_alts(html, filename)
    html, links_added = fix_internal_links(html, filename)
    if html != original:
        path.write_text(html, encoding="utf-8")
    return {
        "changed": html != original,
        "css_added": css_added,
        "h1_demoted": h1_demoted,
        "alt_fixed": alt_fixed,
        "links_added": links_added,
    }


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Existing Pages Content Structure Fix Report", "", "Scope: current pages only. No new landing pages were created.", ""]
    totals = {"changed": 0, "css_added": 0, "h1_demoted": 0, "alt_fixed": 0, "links_added": 0}
    for filename in PAGES:
        path = ROOT / filename
        lines.append(f"## {filename}")
        if not path.exists():
            lines.append("- missing file")
            lines.append("")
            continue
        result = fix_page(filename)
        for key in totals:
            totals[key] += int(result[key])
        lines.append(f"- changed: {result['changed']}")
        lines.append(f"- consolidated CSS added: {result['css_added']}")
        lines.append(f"- extra H1 demoted to H2: {result['h1_demoted']}")
        lines.append(f"- image alt texts fixed: {result['alt_fixed']}")
        lines.append(f"- strategic internal links added: {result['links_added']}")
        lines.append("")
    lines.append("## Totals")
    for key, value in totals.items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Not automatically changed")
    lines.append("- Repetitive copy was not deleted automatically. It needs editorial review to preserve SEO/GEO authority while improving human readability.")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
