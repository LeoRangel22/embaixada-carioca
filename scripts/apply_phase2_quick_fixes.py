#!/usr/bin/env python3
"""Apply safe Phase 2 quick fixes.

Scope:
- shorten home title to safer SERP length;
- remove the unsafe experimental Home hero lock if present;
- add a final light-content contrast lock scoped only to main content;
- preserve reservation CTA, JSON-LD, canonical and stabilization CSS.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "phase2_quick_fixes_report.md"
PAGES = [
    "index.html",
    "cafe-da-manha.html",
    "almoco.html",
    "cardapio.html",
    "como-chegar.html",
    "eventos.html",
    "guia-do-rio.html",
]
HOME = ROOT / "index.html"

OLD_TITLE = "Restaurante Morro da Urca com Vista para o Pão de Açúcar | Embaixada Carioca"
NEW_TITLE = "Restaurante no Morro da Urca | Embaixada Carioca"
HOME_LOCK_ID = "ec-home-light-bg-final-contrast-lock"
LIGHT_LOCK_ID = "ec-light-content-final-contrast-lock"

UNSAFE_HOME_RE = re.compile(
    r"\n?<!-- EC Home Light Background Final Contrast Lock -->\s*<style id=\"ec-home-light-bg-final-contrast-lock\">.*?</style>",
    re.DOTALL,
)
LIGHT_LOCK_RE = re.compile(
    r"\n?<!-- EC Light Content Final Contrast Lock -->\s*<style id=\"ec-light-content-final-contrast-lock\">.*?</style>",
    re.DOTALL,
)

LIGHT_LOCK = f'''<!-- EC Light Content Final Contrast Lock -->
<style id="{LIGHT_LOCK_ID}">
/* Main-content only. Never touch nav, header, hero, hero chips, hero side frame or CTAs. */
html body main :is(.access-direct,.access-section,.access-faq,.light-section,.paper-section,.section-paper,.bg-paper,.menu-section,.gallery-section,.ec-sprint4-steps,.ec-sprint5-quality,.ec-sprint5-faq,.ec-r2d2-depth,.ec-sprint4-faq) {{
  background:#f6efde !important;
  color:#00405a !important;
  -webkit-text-fill-color:initial !important;
}}
html body main :is(.box,.access-fact,.access-route,details,.card,.faq-item,.faq-card,.info-card,.content-card,.copy-card,.route-card,.guide-card,.place-card,.beach-card,.experience-card,.ec-sprint5-card,.ec-r2d2-card) {{
  position:relative !important;
  z-index:1 !important;
  background:#fffaf0 !important;
  color:#00405a !important;
  -webkit-text-fill-color:#00405a !important;
  text-shadow:none !important;
  opacity:1 !important;
  visibility:visible !important;
  filter:none !important;
  mix-blend-mode:normal !important;
}}
html body main :is(.box,.access-fact,.access-route,details,.card,.faq-item,.faq-card,.info-card,.content-card,.copy-card,.route-card,.guide-card,.place-card,.beach-card,.experience-card,.ec-sprint5-card,.ec-r2d2-card)::before,
html body main :is(.box,.access-fact,.access-route,details,.card,.faq-item,.faq-card,.info-card,.content-card,.copy-card,.route-card,.guide-card,.place-card,.beach-card,.experience-card,.ec-sprint5-card,.ec-r2d2-card)::after {{
  pointer-events:none !important;
  opacity:0 !important;
  display:none !important;
}}
html body main :is(.box,.access-fact,.access-route,details,.card,.faq-item,.faq-card,.info-card,.content-card,.copy-card,.route-card,.guide-card,.place-card,.beach-card,.experience-card,.ec-sprint5-card,.ec-r2d2-card) > *,
html body main :is(.box,.access-fact,.access-route,details,.card,.faq-item,.faq-card,.info-card,.content-card,.copy-card,.route-card,.guide-card,.place-card,.beach-card,.experience-card,.ec-sprint5-card,.ec-r2d2-card) :is(h1,h2,h3,h4,h5,h6,p,li,span,small,dd,dt,summary,strong,b,a) {{
  position:relative !important;
  z-index:3 !important;
  opacity:1 !important;
  visibility:visible !important;
  filter:none !important;
  mix-blend-mode:normal !important;
  text-shadow:none !important;
}}
html body main :is(.access-direct,.access-section,.access-faq,.light-section,.paper-section,.section-paper,.bg-paper,.menu-section,.gallery-section,.ec-sprint4-steps,.ec-sprint5-quality,.ec-sprint5-faq,.ec-r2d2-depth,.ec-sprint4-faq,.box,.access-fact,.access-route,details,.card,.faq-item,.faq-card,.info-card,.content-card,.copy-card,.route-card,.guide-card,.place-card,.beach-card,.experience-card,.ec-sprint5-card,.ec-r2d2-card) :is(h1,h2,h3,h4,h5,h6,.title,.headline,.section-title,.card-title,summary) {{
  color:#00405a !important;
  -webkit-text-fill-color:#00405a !important;
  text-shadow:none !important;
  opacity:1 !important;
  visibility:visible !important;
}}
html body main :is(.access-direct,.access-section,.access-faq,.light-section,.paper-section,.section-paper,.bg-paper,.menu-section,.gallery-section,.ec-sprint4-steps,.ec-sprint5-quality,.ec-sprint5-faq,.ec-r2d2-depth,.ec-sprint4-faq,.box,.access-fact,.access-route,details,.card,.faq-item,.faq-card,.info-card,.content-card,.copy-card,.route-card,.guide-card,.place-card,.beach-card,.experience-card,.ec-sprint5-card,.ec-r2d2-card) :is(p,li,span,small,dd,dt,.lede,.copy,.description,.faq-answer) {{
  color:#485156 !important;
  -webkit-text-fill-color:#485156 !important;
  text-shadow:none !important;
  opacity:1 !important;
  visibility:visible !important;
}}
html body main :is(.access-direct,.access-section,.access-faq,.light-section,.paper-section,.section-paper,.bg-paper,.menu-section,.gallery-section,.ec-sprint4-steps,.ec-sprint5-quality,.ec-sprint5-faq,.ec-r2d2-depth,.ec-sprint4-faq,.box,.access-fact,.access-route,details,.card,.faq-item,.faq-card,.info-card,.content-card,.copy-card,.route-card,.guide-card,.place-card,.beach-card,.experience-card,.ec-sprint5-card,.ec-r2d2-card) :is(strong,b,a:not(.btn),.kicker,.eyebrow,.tag) {{
  color:#9a6500 !important;
  -webkit-text-fill-color:#9a6500 !important;
  text-shadow:none !important;
  opacity:1 !important;
  visibility:visible !important;
}}
/* Specific access page visible text rescue */
html body[data-screen-label="Como Chegar"] main .box .kicker,
html body[data-screen-label="Como Chegar"] main .box h2,
html body[data-screen-label="Como Chegar"] main .box p,
html body[data-screen-label="Como Chegar"] main .access-fact h3,
html body[data-screen-label="Como Chegar"] main .access-fact p,
html body[data-screen-label="Como Chegar"] main .access-route h3,
html body[data-screen-label="Como Chegar"] main .access-route p {{
  display:block !important;
  opacity:1 !important;
  visibility:visible !important;
  transform:none !important;
}}
html body[data-screen-label="Como Chegar"] main .box h2,
html body[data-screen-label="Como Chegar"] main .access-fact h3,
html body[data-screen-label="Como Chegar"] main .access-route h3 {{
  color:#00405a !important;
  -webkit-text-fill-color:#00405a !important;
}}
html body[data-screen-label="Como Chegar"] main .box p,
html body[data-screen-label="Como Chegar"] main .access-fact p,
html body[data-screen-label="Como Chegar"] main .access-route p {{
  color:#485156 !important;
  -webkit-text-fill-color:#485156 !important;
}}
html body main :is(.menu-item,.menu-card,.dish-card) :is(h1,h2,h3,h4,.title,.menu-item-name) {{ color:#335d4a !important; -webkit-text-fill-color:#335d4a !important; }}
html body main :is(.menu-item,.menu-card,.dish-card) :is(p,li,span,small,.description,.menu-item-desc) {{ color:#485156 !important; -webkit-text-fill-color:#485156 !important; }}
html body main :is(.menu-item,.menu-card,.dish-card) :is(.price,.menu-item-price,strong,b) {{ color:#9a6500 !important; -webkit-text-fill-color:#9a6500 !important; }}
</style>'''


def remove_unsafe_home_lock(text: str) -> tuple[str, str]:
    if HOME_LOCK_ID not in text:
        return text, "unsafe home light-background contrast lock not present"
    new_text, count = UNSAFE_HOME_RE.subn("", text)
    return new_text, "unsafe home light-background contrast lock removed" if count else "unsafe home lock found but not removed"


def apply_light_lock(text: str) -> tuple[str, str]:
    if LIGHT_LOCK_ID in text:
        new_text, count = LIGHT_LOCK_RE.subn("\n" + LIGHT_LOCK, text, count=1)
        return new_text, "light content contrast lock replaced" if count else "light lock found but not replaced"
    if "</body>" in text:
        return text.replace("</body>", LIGHT_LOCK + "\n</body>", 1), "light content contrast lock inserted"
    return text + "\n" + LIGHT_LOCK + "\n", "light content contrast lock appended"


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Phase 2 Quick Fixes Report", ""]

    home_text = HOME.read_text(encoding="utf-8")
    if OLD_TITLE in home_text:
        home_text = home_text.replace(OLD_TITLE, NEW_TITLE)
        lines.append("- index.html: title reduced to safer SERP length")
    elif NEW_TITLE in home_text:
        lines.append("- index.html: title already fixed")
    else:
        lines.append("- index.html: title target not found")
    home_text, home_note = remove_unsafe_home_lock(home_text)
    HOME.write_text(home_text, encoding="utf-8")
    lines.append(f"- index.html: {home_note}")

    changed = 0
    for page in PAGES:
        path = ROOT / page
        if not path.exists():
            lines.append(f"- {page}: missing")
            continue
        original = path.read_text(encoding="utf-8")
        text, lock_note = apply_light_lock(original)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
        lines.append(f"- {page}: {lock_note}")

    final_home = HOME.read_text(encoding="utf-8")
    checks = {
        "index.html has reservation CTA": "tagme" in final_home.lower() or "reserv" in final_home.lower(),
        "index.html has JSON-LD": "application/ld+json" in final_home,
        "index.html has canonical": 'rel="canonical"' in final_home,
        "index.html keeps stabilization CSS": "ec-stabilization-base.css" in final_home,
        "index.html unsafe home light contrast lock absent": HOME_LOCK_ID not in final_home,
        "light content contrast lock applied to pages": all(LIGHT_LOCK_ID in (ROOT / p).read_text(encoding="utf-8") for p in PAGES if (ROOT / p).exists()),
    }
    lines.append(f"- Light lock changed pages: {changed}")
    for label, ok in checks.items():
        lines.append(f"- {label}: {'PASS' if ok else 'FAIL'}")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
