#!/usr/bin/env python3
"""Apply safe Phase 2 quick fixes.

Current scope:
- shorten home title to safer SERP length;
- add final Home light-background contrast lock;
- generate guardrail report;
- preserve reservation CTA, JSON-LD, canonical and stabilization CSS.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "phase2_quick_fixes_report.md"
HOME = ROOT / "index.html"

OLD_TITLE = "Restaurante Morro da Urca com Vista para o Pão de Açúcar | Embaixada Carioca"
NEW_TITLE = "Restaurante no Morro da Urca | Embaixada Carioca"
HOME_LOCK_ID = "ec-home-light-bg-final-contrast-lock"

HOME_LIGHT_LOCK = f'''<!-- EC Home Light Background Final Contrast Lock -->
<style id="{HOME_LOCK_ID}">
body[data-screen-label="Home"] :is(section,main,article,div):not(header):not(.hero):not(.page-hero):not(.ec-page-hero-side-frame):not(.hero-summary-card):not(.hmc):not(.nav-drawer):not(.wa-preview) :is(p,li,span,small,dd,dt,.lede,.copy,.description,.faq-answer) {{
  color: #485156 !important;
  -webkit-text-fill-color: #485156 !important;
  text-shadow: none !important;
}}
body[data-screen-label="Home"] :is(section,main,article,div):not(header):not(.hero):not(.page-hero):not(.ec-page-hero-side-frame):not(.hero-summary-card):not(.hmc):not(.nav-drawer):not(.wa-preview) :is(h1,h2,h3,h4,h5,h6,.title,.headline,.section-title,.card-title) {{
  color: #335d4a !important;
  -webkit-text-fill-color: #335d4a !important;
  text-shadow: none !important;
}}
body[data-screen-label="Home"] :is(section,main,article,div):not(header):not(.hero):not(.page-hero):not(.ec-page-hero-side-frame):not(.hero-summary-card):not(.hmc):not(.nav-drawer):not(.wa-preview) :is(strong,b,a:not(.btn),.eyebrow,.kicker,.tag) {{
  color: #9a6500 !important;
  -webkit-text-fill-color: #9a6500 !important;
  text-shadow: none !important;
}}
body[data-screen-label="Home"] :is(.btn,a.btn,.hero-ctas a,.ctas a) {{
  -webkit-text-fill-color: currentColor !important;
}}
</style>'''

LOCK_RE = re.compile(
    r"\n?<!-- EC Home Light Background Final Contrast Lock -->\s*<style id=\"ec-home-light-bg-final-contrast-lock\">.*?</style>",
    re.DOTALL,
)


def apply_home_light_lock(text: str) -> tuple[str, str]:
    if HOME_LOCK_ID in text:
        new_text, count = LOCK_RE.subn("\n" + HOME_LIGHT_LOCK, text, count=1)
        if count and new_text != text:
            return new_text, "home light-background contrast lock replaced"
        return text, "home light-background contrast lock already present"
    if "</body>" in text:
        return text.replace("</body>", HOME_LIGHT_LOCK + "\n</body>", 1), "home light-background contrast lock inserted"
    return text + "\n" + HOME_LIGHT_LOCK + "\n", "home light-background contrast lock appended"


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Phase 2 Quick Fixes Report", ""]
    text = HOME.read_text(encoding="utf-8")

    if OLD_TITLE in text:
        text = text.replace(OLD_TITLE, NEW_TITLE)
        lines.append("- index.html: title reduced to safer SERP length")
    elif NEW_TITLE in text:
        lines.append("- index.html: title already fixed")
    else:
        lines.append("- index.html: title target not found")

    text, lock_note = apply_home_light_lock(text)
    HOME.write_text(text, encoding="utf-8")
    lines.append(f"- index.html: {lock_note}")

    text = HOME.read_text(encoding="utf-8")
    checks = {
        "index.html has reservation CTA": "tagme" in text.lower() or "reserv" in text.lower(),
        "index.html has JSON-LD": "application/ld+json" in text,
        "index.html has canonical": 'rel="canonical"' in text,
        "index.html keeps stabilization CSS": "ec-stabilization-base.css" in text,
        "index.html has home light contrast lock": HOME_LOCK_ID in text,
    }
    for label, ok in checks.items():
        lines.append(f"- {label}: {'PASS' if ok else 'FAIL'}")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
