#!/usr/bin/env python3
"""
Correção global do link de avaliações Google.

Troca links genéricos de Maps pelo link direto de avaliação informado pela operação.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORRECT_REVIEW_URL = "https://g.page/r/CU-tJiJIjBUcEAE/review"
OLD_URLS = [
    "https://www.google.com/maps/place/Embaixada+Carioca",
    "https://www.google.com/maps/place/Embaixada%20Carioca",
    "https://maps.google.com/?q=Embaixada+Carioca",
    "https://www.google.com/search?q=Embaixada+Carioca+Google+Reviews",
]

TITLE_REPLACEMENTS = {
    "Ver avaliações no Google": "Deixar avaliação no Google",
    "View reviews on Google": "Leave a review on Google",
    "Ver reseñas en Google": "Dejar una reseña en Google",
    "4.8 estrelas · mais de 7.779 avaliações no Google": "4.8 estrelas · 7.779 avaliações · avaliar no Google",
    "4.8 stars · more than 7,779 Google reviews": "4.8 stars · 7,779 reviews · leave a Google review",
    "4.8 estrellas · más de 7.779 reseñas en Google": "4.8 estrellas · 7.779 reseñas · dejar una reseña en Google",
}

REPORT = []


def process(path: Path) -> None:
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    changes = 0

    for old in OLD_URLS:
        c = text.count(old)
        if c:
            text = text.replace(old, CORRECT_REVIEW_URL)
            changes += c

    for old, new in TITLE_REPLACEMENTS.items():
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            changes += c

    if text != original:
        path.write_text(text, encoding="utf-8")
        REPORT.append(f"UPDATED: {path.relative_to(ROOT)} | changes={changes}")


def main() -> int:
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" not in path.parts:
            process(path)

    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report = report_dir / "google_review_link_report.md"
    report.write_text(
        "# Correção do Link de Avaliação Google\n\n"
        f"## Link correto\n- {CORRECT_REVIEW_URL}\n\n"
        "## Alterações aplicadas\n"
        + ("\n".join(f"- {line}" for line in REPORT) if REPORT else "- Nenhuma ocorrência antiga encontrada")
        + "\n",
        encoding="utf-8",
    )
    print(report.read_text(encoding="utf-8"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
