#!/usr/bin/env python3
"""Stabilize current pages before creating new landing pages.

Focus:
- SEO titles and meta descriptions based on real keyword demand.
- Canonical/Open Graph/Twitter consistency.
- Existing pages only; no new landing pages.
- Produces a clear report for Codex/GitHub Actions/manual review.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "existing_pages_stabilization_report.md"

PAGES = {
    "index.html": {
        "title": "Restaurante Morro da Urca com Vista para o Pão de Açúcar | Embaixada Carioca",
        "description": "Restaurante no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. Café da manhã, almoço brasileiro, caipirinhas, chope e eventos com vista no Rio.",
        "canonical": "https://www.embaixadacarioca.com/",
    },
    "cafe-da-manha.html": {
        "title": "Café da Manhã com Vista para o Pão de Açúcar | Embaixada Carioca",
        "description": "Café da manhã com vista para o Pão de Açúcar, no Morro da Urca. Servido todos os dias a partir de 8h30, dentro do Parque Bondinho. Reserve sua mesa.",
        "canonical": "https://www.embaixadacarioca.com/cafe-da-manha.html",
    },
    "almoco.html": {
        "title": "Almoço no Morro da Urca com Vista para o Pão de Açúcar | Embaixada Carioca",
        "description": "Almoço brasileiro no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. Feijoada, picanha, frutos do mar, caipirinhas e vista no Rio.",
        "canonical": "https://www.embaixadacarioca.com/almoco.html",
    },
    "cardapio.html": {
        "title": "Cardápio do Restaurante no Bondinho Pão de Açúcar | Embaixada Carioca",
        "description": "Cardápio da Embaixada Carioca no Morro da Urca: café da manhã, almoço, feijoada, picanha, bobó de camarão, caipirinhas e chope com vista.",
        "canonical": "https://www.embaixadacarioca.com/cardapio.html",
    },
    "como-chegar.html": {
        "title": "Como Chegar à Embaixada Carioca no Morro da Urca | Parque Bondinho",
        "description": "Veja como chegar à Embaixada Carioca, restaurante no Morro da Urca dentro do Parque Bondinho Pão de Açúcar, por bondinho, trilha ou Praia Vermelha.",
        "canonical": "https://www.embaixadacarioca.com/como-chegar.html",
    },
    "eventos.html": {
        "title": "Eventos com Vista no Rio de Janeiro | Embaixada Carioca Morro da Urca",
        "description": "Espaço para eventos corporativos, aniversários e experiências gastronômicas no Morro da Urca, com vista para o Pão de Açúcar. Solicite orçamento.",
        "canonical": "https://www.embaixadacarioca.com/eventos.html",
    },
    "guia-do-rio.html": {
        "title": "Onde Comer no Rio de Janeiro | Guia da Embaixada Carioca",
        "description": "Guia para saber onde comer no Rio de Janeiro, com restaurantes com vista, Morro da Urca, Pão de Açúcar, café da manhã, almoço e experiências cariocas.",
        "canonical": "https://www.embaixadacarioca.com/guia-do-rio.html",
    },
}


def replace_or_insert(pattern: str, replacement: str, text: str, insert_after: str | None = None) -> tuple[str, bool]:
    new, count = re.subn(pattern, replacement, text, count=1, flags=re.I | re.S)
    if count:
        return new, True
    if insert_after and insert_after in text:
        return text.replace(insert_after, insert_after + "\n" + replacement, 1), True
    return text, False


def update_page(path: Path, data: dict[str, str]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    original = text
    notes: list[str] = []

    text, ok = replace_or_insert(r"<title>.*?</title>", f"<title>{data['title']}</title>", text)
    notes.append(f"title: {'updated' if ok else 'missing'}")

    text, ok = replace_or_insert(
        r"<meta\s+name=[\"']description[\"']\s+content=[\"'].*?[\"']\s*/?>",
        f"<meta name=\"description\" content=\"{data['description']}\">",
        text,
        "<meta charset=\"utf-8\"/>",
    )
    notes.append(f"meta description: {'updated' if ok else 'missing'}")

    text, ok = replace_or_insert(
        r"<link\s+rel=[\"']canonical[\"']\s+href=[\"'].*?[\"']\s*/?>|<link\s+href=[\"'].*?[\"']\s+rel=[\"']canonical[\"']\s*/?>",
        f"<link rel=\"canonical\" href=\"{data['canonical']}\">",
        text,
        "<head>",
    )
    notes.append(f"canonical: {'updated' if ok else 'missing'}")

    # OG/Twitter titles and descriptions should mirror the main page intent.
    og_replacements = {
        r"<meta\s+property=[\"']og:title[\"']\s+content=[\"'].*?[\"']\s*/?>": f"<meta property=\"og:title\" content=\"{data['title']}\">",
        r"<meta\s+property=[\"']og:description[\"']\s+content=[\"'].*?[\"']\s*/?>": f"<meta property=\"og:description\" content=\"{data['description']}\">",
        r"<meta\s+name=[\"']twitter:title[\"']\s+content=[\"'].*?[\"']\s*/?>": f"<meta name=\"twitter:title\" content=\"{data['title']}\">",
        r"<meta\s+name=[\"']twitter:description[\"']\s+content=[\"'].*?[\"']\s*/?>": f"<meta name=\"twitter:description\" content=\"{data['description']}\">",
    }
    for pattern, repl in og_replacements.items():
        text, _ = replace_or_insert(pattern, repl, text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        notes.append("file changed")
    else:
        notes.append("no changes needed")
    return notes


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Existing Pages Stabilization Report", "", "No new landing pages were created.", ""]

    for filename, data in PAGES.items():
        path = ROOT / filename
        lines.append(f"## {filename}")
        if not path.exists():
            lines.append("- missing file")
            lines.append("")
            continue
        notes = update_page(path, data)
        for note in notes:
            lines.append(f"- {note}")
        lines.append(f"- final title: {data['title']}")
        lines.append(f"- final description: {data['description']}")
        lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
