#!/usr/bin/env python3
"""Apply final CSS contrast lock for hero side frame boxes.

This script is intentionally CSS-only and idempotent.
It inserts the final lock before </body> so it loads after page-level styles.
"""
from __future__ import annotations

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
html body .hero-summary-card,
html body .hmc {{
  background: rgba(0,32,46,.92) !important;
  border-color: rgba(246,239,222,.42) !important;
  box-shadow: 0 22px 64px rgba(0,0,0,.58) !important;
  color: #f6efde !important;
  -webkit-text-fill-color: #f6efde !important;
  text-shadow: none !important;
  opacity: 1 !important;
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
  text-shadow: 0 2px 10px rgba(0,0,0,.66) !important;
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
  text-shadow: 0 2px 12px rgba(0,0,0,.70) !important;
  font-weight: 750 !important;
  font-size: clamp(15px, 4vw, 18px) !important;
  line-height: 1.35 !important;
}}
</style>'''


def apply_lock(path: Path) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    if LOCK_ID in text:
        return False, "already present"
    if not any(token in text for token in ("ec-page-hero-side-frame", "hero-summary-card", "hmc")):
        return False, "no hero side frame found"
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
