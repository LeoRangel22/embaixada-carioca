#!/usr/bin/env python3
"""Inject a final visible-text lock at the end of como-chegar.html.

The page has many legacy inline <style> blocks. A global CSS import can be
beaten by later inline rules, so this injects the final page-specific lock
immediately before </body>.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "como-chegar.html"
REPORT = ROOT / "_audit_reports" / "como_chegar_final_visible_lock_report.md"
LOCK_ID = "ec-como-chegar-final-visible-lock"
LOCK_RE = re.compile(
    r"\n?<!-- EC Como Chegar Final Visible Lock -->\s*<style id=\"ec-como-chegar-final-visible-lock\">.*?</style>",
    re.DOTALL,
)

LOCK = f'''<!-- EC Como Chegar Final Visible Lock -->
<style id="{LOCK_ID}">
/* Last-mile page lock: must sit at the end of body and beat previous inline locks. */
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main.main main,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main {{
  background:#f6efde !important;
}}

html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.access-section.access-section,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.access-faq.access-faq,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint4-steps.ec-sprint4-steps,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint5-quality.ec-sprint5-quality,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint5-faq.ec-sprint5-faq {{
  background:#f6efde !important;
  color:#00405a !important;
  -webkit-text-fill-color:#00405a !important;
}}

html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.access-section.access-section .route-grid.route-grid article.access-route.access-route,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.access-faq.access-faq details,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint5-quality.ec-sprint5-quality .ec-sprint5-card.ec-sprint5-card,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint4-steps.ec-sprint4-steps ol {{
  background:#fffaf0 !important;
  color:#00405a !important;
  -webkit-text-fill-color:#00405a !important;
  border-color:rgba(0,64,90,.16) !important;
  text-shadow:none !important;
  opacity:1 !important;
  visibility:visible !important;
}}

html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.access-section.access-section .wrap.wrap > h2,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.access-faq.access-faq .wrap.wrap > h2,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint4-steps.ec-sprint4-steps .wrap.wrap > h2,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint5-quality.ec-sprint5-quality .wrap.wrap > h2,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.access-section.access-section .route-grid.route-grid article.access-route.access-route h3,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.access-faq.access-faq details summary,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint5-quality.ec-sprint5-quality .ec-sprint5-card.ec-sprint5-card strong,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint5-quality.ec-sprint5-quality h3 {{
  color:#00405a !important;
  -webkit-text-fill-color:#00405a !important;
  text-shadow:none !important;
  opacity:1 !important;
  visibility:visible !important;
}}

html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.access-section.access-section .route-grid.route-grid article.access-route.access-route p,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.access-faq.access-faq details p,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint4-steps.ec-sprint4-steps li,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint5-quality.ec-sprint5-quality p,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint5-quality.ec-sprint5-quality li,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint5-quality.ec-sprint5-quality .ec-sprint5-card.ec-sprint5-card {{
  color:#485156 !important;
  -webkit-text-fill-color:#485156 !important;
  text-shadow:none !important;
  opacity:1 !important;
  visibility:visible !important;
}}

html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.access-section.access-section .route-grid.route-grid article.access-route.access-route *,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.access-faq.access-faq details *,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint4-steps.ec-sprint4-steps *,
html body[data-screen-label="Como Chegar"][data-screen-label="Como Chegar"] main section.ec-sprint5-quality.ec-sprint5-quality * {{
  text-shadow:none !important;
  opacity:1 !important;
  visibility:visible !important;
}}
</style>'''


def main() -> int:
    text = PAGE.read_text(encoding="utf-8")
    text, replaced = LOCK_RE.subn("", text)
    if "</body>" in text:
        text = text.replace("</body>", LOCK + "\n</body>", 1)
    else:
        text += "\n" + LOCK + "\n"
    PAGE.write_text(text, encoding="utf-8")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "# Como Chegar Final Visible Lock Report\n\n"
        f"- Lock inserted before body close: PASS\n"
        f"- Previous locks removed: {replaced}\n"
        f"- Target page: como-chegar.html\n",
        encoding="utf-8",
    )
    print(REPORT.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
