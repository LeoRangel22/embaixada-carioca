#!/usr/bin/env python3
"""Apply safe Phase 2 quick fixes.

Current scope:
- shorten home title to safer SERP length;
- remove the experimental Home light-background lock if present;
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

LOCK_RE = re.compile(
    r"\n?<!-- EC Home Light Background Final Contrast Lock -->\s*<style id=\"ec-home-light-bg-final-contrast-lock\">.*?</style>",
    re.DOTALL,
)


def remove_home_light_lock(text: str) -> tuple[str, str]:
    if HOME_LOCK_ID not in text:
        return text, "unsafe home light-background contrast lock not present"
    new_text, count = LOCK_RE.subn("", text)
    if count:
        return new_text, "unsafe home light-background contrast lock removed"
    return text, "unsafe home light-background contrast lock found but not removed"


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

    text, lock_note = remove_home_light_lock(text)
    HOME.write_text(text, encoding="utf-8")
    lines.append(f"- index.html: {lock_note}")

    text = HOME.read_text(encoding="utf-8")
    checks = {
        "index.html has reservation CTA": "tagme" in text.lower() or "reserv" in text.lower(),
        "index.html has JSON-LD": "application/ld+json" in text,
        "index.html has canonical": 'rel="canonical"' in text,
        "index.html keeps stabilization CSS": "ec-stabilization-base.css" in text,
        "index.html unsafe home light contrast lock absent": HOME_LOCK_ID not in text,
    }
    for label, ok in checks.items():
        lines.append(f"- {label}: {'PASS' if ok else 'FAIL'}")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
