#!/usr/bin/env python3
"""
Nav UX Fixes — Embaixada Carioca

Corrige três pontos visuais do topo:
1. Dropdown de idiomas sempre abrindo para baixo e dentro da tela.
2. Remove o pin/ícone antes de Como Chegar no menu principal/drawer.
3. Substitui o badge de avaliação por padrão compacto Google Reviews:
   G menor, 4.8 menor, estrelas e contagem discreta.

Roda após os gates dos Sprints 1/2/3 para não ser sobrescrito.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT: list[str] = []
COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "css_injected": 0,
    "pins_removed": 0,
    "rating_badges_replaced": 0,
}

CSS_START = "<!-- EC Nav UX Fixes -->"
CSS_END = "<!-- /EC Nav UX Fixes -->"
CSS_RE = re.compile(r"\n*<!-- EC Nav UX Fixes -->[\s\S]*?<!-- /EC Nav UX Fixes -->\s*", re.IGNORECASE)
HEAD_CLOSE_RE = re.compile(r"</head>", re.IGNORECASE)
RATING_RE = re.compile(r"<a\b(?=[^>]*class=[\"'][^\"']*\bnav-rating-badge\b[^\"']*[\"'])[^>]*>[\s\S]*?</a>", re.IGNORECASE)

CSS_BLOCK = f"""{CSS_START}
<style id="ec-nav-ux-fixes">
/* Idiomas: abre para baixo, sem cortar fora da página */
nav.top,
nav.top .nav-inner,
nav.top .lang-switcher{{
  overflow:visible!important;
}}
nav.top .lang-switcher{{
  position:relative!important;
  z-index:4000!important;
}}
nav.top .lang-dropdown{{
  position:absolute!important;
  top:calc(100% + 8px)!important;
  bottom:auto!important;
  right:0!important;
  left:auto!important;
  transform:none!important;
  min-width:190px!important;
  max-width:min(240px,calc(100vw - 24px))!important;
  max-height:calc(100vh - 96px)!important;
  overflow-y:auto!important;
  z-index:99999!important;
  border-radius:0 0 16px 16px!important;
  box-shadow:0 18px 42px rgba(0,32,46,.26)!important;
}}
nav.top .lang-switcher:hover .lang-dropdown,
nav.top .lang-switcher:focus-within .lang-dropdown{{
  transform:none!important;
}}
@media(max-width:960px){{
  nav.top .lang-dropdown{{
    right:auto!important;
    left:0!important;
    top:calc(100% + 6px)!important;
    max-width:calc(100vw - 24px)!important;
  }}
}}

/* Como Chegar: sem pin no menu principal */
nav.top .nav-links .drawer-icon,
nav.top a[href*="como-chegar"] .drawer-icon,
nav.top a[href*="how-to-get-there"] .drawer-icon,
nav.top a[href*="como-llegar"] .drawer-icon{{
  display:none!important;
}}

/* Google Reviews compacto no topo */
nav.top .nav-rating-badge.google-review-badge{{
  width:auto!important;
  min-width:154px!important;
  height:42px!important;
  padding:5px 11px!important;
  border-radius:14px!important;
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  gap:8px!important;
  text-decoration:none!important;
  background:rgba(246,239,222,.13)!important;
  border:1px solid rgba(246,239,222,.30)!important;
  color:rgba(246,239,222,.94)!important;
  backdrop-filter:blur(9px)!important;
  -webkit-backdrop-filter:blur(9px)!important;
}}
nav.top.scrolled .nav-rating-badge.google-review-badge{{
  background:rgba(0,64,90,.06)!important;
  border-color:rgba(0,64,90,.18)!important;
  color:#00405a!important;
}}
.google-review-badge .google-g{{
  flex:0 0 17px!important;
  width:17px!important;
  height:17px!important;
  border-radius:50%!important;
  display:inline-grid!important;
  place-items:center!important;
  font-family:Arial,Helvetica,sans-serif!important;
  font-size:17px!important;
  line-height:1!important;
  font-weight:700!important;
  color:#4285f4!important;
  background:transparent!important;
}}
.google-review-badge .gr-copy{{
  display:flex!important;
  flex-direction:column!important;
  gap:1px!important;
  min-width:0!important;
}}
.google-review-badge .gr-label{{
  font-family:Catamaran,Verdana,system-ui,sans-serif!important;
  font-size:9px!important;
  line-height:1!important;
  font-weight:700!important;
  letter-spacing:.01em!important;
  text-transform:none!important;
  opacity:.88!important;
  white-space:nowrap!important;
}}
.google-review-badge .gr-row{{
  display:flex!important;
  align-items:center!important;
  gap:5px!important;
  line-height:1!important;
  white-space:nowrap!important;
}}
.google-review-badge .gr-score{{
  font-family:Catamaran,Verdana,system-ui,sans-serif!important;
  font-size:16px!important;
  line-height:.95!important;
  font-weight:800!important;
  letter-spacing:.01em!important;
}}
.google-review-badge .gr-stars{{
  color:#fbbc04!important;
  font-size:8px!important;
  letter-spacing:.02em!important;
  line-height:1!important;
}}
.google-review-badge .gr-count{{
  font-size:8.5px!important;
  line-height:1!important;
  opacity:.78!important;
  letter-spacing:.01em!important;
}}
@media(max-width:1180px){{
  nav.top .nav-rating-badge.google-review-badge{{
    min-width:86px!important;
    width:86px!important;
    padding:5px 7px!important;
    gap:5px!important;
  }}
  .google-review-badge .gr-label,
  .google-review-badge .gr-count{{display:none!important;}}
  .google-review-badge .gr-score{{font-size:14px!important;}}
}}
</style>
{CSS_END}"""

RATING_BADGE = """<a aria-label="Google Reviews: 4.8 estrelas · 7.779 avaliações" class="nav-rating-badge google-review-badge" href="https://g.page/r/CU-tJiJIjBUcEAE/review" rel="noopener" target="_blank" title="Google Reviews · 4.8 estrelas">
<span class="google-g" aria-hidden="true">G</span>
<span class="gr-copy"><span class="gr-label">Google Reviews</span><span class="gr-row"><strong class="gr-score">4.8</strong><span class="gr-stars" aria-hidden="true">★★★★★</span><span class="gr-count">7.779 avaliações</span></span></span>
</a>"""

PIN_PATTERNS = [
    (re.compile(r"<span\s+class=[\"']drawer-icon[\"']>📍</span>\s*(Como Chegar)", re.IGNORECASE), r"\1"),
    (re.compile(r"<span\s+class=[\"']drawer-icon[\"']>📍</span>\s*(HOW TO GET THERE)", re.IGNORECASE), r"\1"),
    (re.compile(r"<span\s+class=[\"']drawer-icon[\"']>📍</span>\s*(How to Get There)", re.IGNORECASE), r"\1"),
    (re.compile(r"<span\s+class=[\"']drawer-icon[\"']>📍</span>\s*(CÓMO LLEGAR)", re.IGNORECASE), r"\1"),
    (re.compile(r"<span\s+class=[\"']drawer-icon[\"']>📍</span>\s*(Cómo Llegar)", re.IGNORECASE), r"\1"),
]


def inject_css(text: str, rel: str) -> str:
    original = text
    text = CSS_RE.sub("\n", text)
    if HEAD_CLOSE_RE.search(text):
        text = HEAD_CLOSE_RE.sub(CSS_BLOCK + "\n</head>", text, count=1)
    if text != original:
        COUNTERS["css_injected"] += 1
        REPORT.append(f"CSS: {rel}")
    return text


def remove_pins(text: str, rel: str) -> str:
    for pattern, replacement in PIN_PATTERNS:
        text, count = pattern.subn(replacement, text)
        if count:
            COUNTERS["pins_removed"] += count
            REPORT.append(f"PIN: {rel} | {count}")
    return text


def replace_rating(text: str, rel: str) -> str:
    text, count = RATING_RE.subn(RATING_BADGE, text)
    if count:
        COUNTERS["rating_badges_replaced"] += count
        REPORT.append(f"RATING: {rel} | {count}")
    return text


def process(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix != ".html" or ".git" in path.parts or rel.startswith("_"):
        return
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    text = remove_pins(text, rel)
    text = replace_rating(text, rel)
    text = inject_css(text, rel)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1


def write_report() -> None:
    out = ROOT / "_audit_reports"
    out.mkdir(exist_ok=True)
    report = out / "nav_language_review_fixes_report.md"
    lines = [
        "# Nav Language + Google Review Fixes",
        "",
        "## Objetivo",
        "Corrigir dropdown de idiomas, remover pin do Como Chegar e trocar o badge para Google Reviews compacto.",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Ações"])
    lines.extend(f"- {x}" for x in REPORT) if REPORT else lines.append("- Nenhuma ação necessária.")
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
