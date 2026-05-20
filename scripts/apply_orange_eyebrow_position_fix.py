#!/usr/bin/env python3
"""
Orange Eyebrow Position Fix — Embaixada Carioca

Move a linha laranja do hero conforme ajuste visual fino:
- base anterior: translate(35px, -31px);
- ajuste atual solicitado: 16px para baixo e 6px para a direita.

Resultado final: translate(41px, -15px).
Aplica como override final para não ser sobrescrito pelos demais scripts.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CSS_START = "<!-- EC Orange Eyebrow Position Fix -->"
CSS_END = "<!-- /EC Orange Eyebrow Position Fix -->"
CSS_RE = re.compile(r"\n*<!-- EC Orange Eyebrow Position Fix -->[\s\S]*?<!-- /EC Orange Eyebrow Position Fix -->\s*", re.IGNORECASE)
HEAD_CLOSE_RE = re.compile(r"</head>", re.IGNORECASE)

CSS_BLOCK = f"""{CSS_START}
<style id="ec-orange-eyebrow-position-fix">
@media (min-width: 961px) {{
  .hero .hero-eyebrow,
  .page-hero .hero-eyebrow {{
    position: relative !important;
    transform: translate(41px, -15px) !important;
    will-change: transform;
  }}
}}
</style>
{CSS_END}"""

REPORT: list[str] = []
COUNTERS = {"html_scanned": 0, "html_updated": 0, "css_injected": 0}


def process(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix != ".html" or ".git" in path.parts or rel.startswith("_"):
        return
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = CSS_RE.sub("\n", original)
    if HEAD_CLOSE_RE.search(text):
        text = HEAD_CLOSE_RE.sub(CSS_BLOCK + "\n</head>", text, count=1)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1
        COUNTERS["css_injected"] += 1
        REPORT.append(f"UPDATED: {rel}")


def write_report() -> None:
    out = ROOT / "_audit_reports"
    out.mkdir(exist_ok=True)
    report = out / "orange_eyebrow_position_fix_report.md"
    lines = [
        "# Orange Eyebrow Position Fix",
        "",
        "## Objetivo",
        "Mover a linha laranja do hero 16px para baixo e 6px para a direita em relação ao ajuste anterior.",
        "",
        "## Resultado técnico",
        "- transform: translate(41px, -15px)",
        "",
        "## Contadores",
    ]
    for key, value in COUNTERS.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Ações"])
    lines.extend(f"- {item}" for item in REPORT) if REPORT else lines.append("- Nenhuma ação necessária.")
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
