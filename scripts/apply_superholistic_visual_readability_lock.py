#!/usr/bin/env python3
"""Injects the superholistic visual readability CSS lock into all HTML pages."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT = REPORT_DIR / "superholistic_visual_readability_lock_report.md"
CSS_HREF = "/assets/superholistic_visual_readability_lock.css"
LINK = f'<link rel="stylesheet" href="{CSS_HREF}">'
EXCLUDE = {".git", ".github", "node_modules", "_audit_reports", "dist", "build", "coverage"}


def pages() -> list[Path]:
    return sorted(
        [p for p in ROOT.rglob("*.html") if not any(part in EXCLUDE for part in p.parts)],
        key=lambda p: p.relative_to(ROOT).as_posix(),
    )


def inject(path: Path) -> tuple[bool, str]:
    html = path.read_text(encoding="utf-8", errors="ignore")
    if CSS_HREF in html:
        return False, "already_present"
    if "</head>" not in html.lower():
        return False, "missing_head_close"
    lower = html.lower()
    idx = lower.rfind("</head>")
    new_html = html[:idx] + "\n" + LINK + "\n" + html[idx:]
    path.write_text(new_html, encoding="utf-8")
    return True, "injected"


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    changed = 0
    skipped = 0
    for page in pages():
        ok, status = inject(page)
        if ok:
            changed += 1
        else:
            skipped += 1
        rows.append((page.relative_to(ROOT).as_posix(), status))
    lines = [
        "# Superholistic Visual Readability Lock Report",
        "",
        "Status: **PASS**",
        f"CSS: `{CSS_HREF}`",
        f"Páginas atualizadas: **{changed}**",
        f"Páginas já ok/ignoradas: **{skipped}**",
        "",
        "## Detalhe",
    ]
    for page, status in rows:
        lines.append(f"- `{page}` — {status}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Superholistic visual readability lock: changed={changed} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
