#!/usr/bin/env python3
"""Apply final CSS contrast lock for hero side frame boxes.

This script is CSS-only and idempotent.
It inserts or replaces the final lock before </body> so it loads after page-level styles.

Important visual rule:
- The outer .ec-page-hero-side-frame may have a translucent dark glass background.
- The inner .hmc blocks must NOT receive solid blue backgrounds.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "hero_side_frame_final_lock_report.md"
PAGES = [
    "index.html",
    "cafe-da-manha.html",
    "almoco.html",
    "cardapio.html",
    "como-chegar.html",
    "eventos.html",
    "guia-do-rio.html",
]
LOCK_ID = "ec-hero-side-frame-final-contrast-lock"

LOCK = f'''<!-- EC Hero Side Frame Final Contrast Lock -->
<style id="{LOCK_ID}">
html body .ec-page-hero-side-frame,
html body .hero-summary-card {{
  background: rgba(0,32,46,.74) !important;
  border-color: rgba(246,239,222,.34) !important;
  box-shadow: 0 22px 64px rgba(0,0,0,.46) !important;
  color: #f6efde !important;
  -webkit-text-fill-color: #f6efde !important;
  text-shadow: none !important;
  opacity: 1 !important;
}}
html body .ec-page-hero-side-frame .hmc,
html body .hero-summary-card .hmc,
html body .hmc {{
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  color: inherit !important;
  -webkit-text-fill-color: inherit !important;
}}
html body .ec-page-hero-side-frame *,
html body .hero-summary-card *,
html body .hmc * {{
  opacity: 1 !important;
}}
html body .ec-page-hero-side-frame .l,
html body .ec-page-hero-side-frame .label,
html body .ec-page-hero-side-frame .kicker,
html body .ec-page-hero-side-frame .eyebrow,
html body .hero-summary-card .l,
html body .hero-summary-card .label,
html body .hero-summary-card .kicker,
html body .hero-summary-card .eyebrow,
html body .hmc .l,
html body .hmc .label,
html body .hmc .kicker,
html body .hmc .eyebrow {{
  color: #f2b24a !important;
  -webkit-text-fill-color: #f2b24a !important;
  text-shadow: 0 2px 10px rgba(0,0,0,.56) !important;
  font-weight: 900 !important;
  letter-spacing: .26em !important;
}}
html body .ec-page-hero-side-frame .v,
html body .ec-page-hero-side-frame .value,
html body .ec-page-hero-side-frame p,
html body .hero-summary-card .v,
html body .hero-summary-card .value,
html body .hero-summary-card p,
html body .hmc .v,
html body .hmc .value,
html body .hmc p {{
  color: #f6efde !important;
  -webkit-text-fill-color: #f6efde !important;
  text-shadow: 0 2px 12px rgba(0,0,0,.62) !important;
  font-weight: 750 !important;
  font-size: clamp(15px, 4vw, 18px) !important;
  line-height: 1.35 !important;
}}
</style>'''

LOCK_RE = re.compile(
    r"\n?<!-- EC Hero Side Frame Final Contrast Lock -->\s*<style id=\"ec-hero-side-frame-final-contrast-lock\">.*?</style>",
    re.DOTALL,
)


def apply_lock(path: Path) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    if not any(token in text for token in ("ec-page-hero-side-frame", "hero-summary-card", "hmc")):
        return False, "no hero side frame found"
    if LOCK_ID in text:
        new_text, count = LOCK_RE.subn("\n" + LOCK, text, count=1)
        if count and new_text != text:
            path.write_text(new_text, encoding="utf-8")
            return True, "final lock replaced"
        return False, "already present"
    if "</body>" in text:
        text = text.replace("</body>", LOCK + "\n</body>", 1)
    else:
        text = text + "\n" + LOCK + "\n"
    path.write_text(text, encoding="utf-8")
    return True, "final lock inserted"


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Hero Side Frame Final Lock Report", ""]
    changed = 0
    for page in PAGES:
        path = ROOT / page
        if not path.exists():
            lines.append(f"- {page}: missing")
            continue
        did_change, note = apply_lock(path)
        changed += int(did_change)
        lines.append(f"- {page}: {note}")
    lines.append("")
    lines.append(f"Changed pages: {changed}")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
