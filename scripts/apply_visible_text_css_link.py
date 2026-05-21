#!/usr/bin/env python3
"""Insert the visible-text CSS lock in current public pages."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "visible_text_css_link_report.md"
PAGES = [
    "index.html",
    "cafe-da-manha.html",
    "almoco.html",
    "cardapio.html",
    "como-chegar.html",
    "eventos.html",
    "guia-do-rio.html",
]
LINK = '<link rel="stylesheet" href="/assets/css/ec-visible-text-lock.css">'


def apply(path: Path) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    if "/assets/css/ec-visible-text-lock.css" in text:
        return False, "already linked"
    if "</head>" in text:
        text = text.replace("</head>", LINK + "\n</head>", 1)
    else:
        text = LINK + "\n" + text
    path.write_text(text, encoding="utf-8")
    return True, "link inserted"


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Visible Text CSS Link Report", ""]
    changed = 0
    for page in PAGES:
        path = ROOT / page
        if not path.exists():
            lines.append(f"- {page}: missing")
            continue
        did_change, note = apply(path)
        changed += int(did_change)
        lines.append(f"- {page}: {note}")
    lines.append("")
    lines.append(f"Changed pages: {changed}")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
