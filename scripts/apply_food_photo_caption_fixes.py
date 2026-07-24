#!/usr/bin/env python3
"""Correct food photo captions and alt text in PT/EN/ES galleries.

The fixes are keyed by the actual image asset, not by the old caption. This
prevents a misleading label from surviving in translated or duplicated pages.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "food_photo_caption_fixes_report.md"
EXCLUDED = {".git", "_backups", "_templates", "_site", "node_modules", "dist", "build"}
SHARED_CSS = (
    ROOT / "assets" / "css" / "ec-shared.css",
    ROOT / "assets" / "css" / "ec-subpages-shared.css",
    ROOT / "assets" / "css" / "ec-index-inline.css",
)

CAPTIONS = {
    "carne-seca-mandioca.webp": {
        "pt": (
            "Carne seca acebolada com mandioca frita e o Pão de Açúcar ao fundo",
            "Carne seca acebolada com mandioca frita — com vista para o Pão de Açúcar",
        ),
        "en": (
            "Brazilian sun-dried beef with onions and fried cassava, with Sugarloaf Mountain in the background",
            "Brazilian sun-dried beef with onions and fried cassava",
        ),
        "es": (
            "Carne seca brasileña con cebolla y yuca frita, con el Pan de Azúcar al fondo",
            "Carne seca con cebolla y yuca frita",
        ),
    },
    "bobo-camarao-real.webp": {
        "pt": (
            "Risoto cremoso de camarão finalizado com ervas",
            "Risoto cremoso de camarão",
        ),
        "en": (
            "Creamy shrimp risotto finished with fresh herbs",
            "Creamy shrimp risotto",
        ),
        "es": (
            "Risotto cremoso de camarones terminado con hierbas frescas",
            "Risotto cremoso de camarones",
        ),
    },
    "fabio-almoco-mesa-completa.webp": {
        "pt": (
            "Mesa de almoço com pratos brasileiros, acompanhamentos e bebidas na Embaixada Carioca",
            "Almoço brasileiro completo para compartilhar",
        ),
        "en": (
            "Brazilian lunch spread with main dishes, sides and drinks at Embaixada Carioca",
            "Complete Brazilian lunch spread",
        ),
        "es": (
            "Mesa de almuerzo brasileño con platos, acompañamientos y bebidas en Embaixada Carioca",
            "Almuerzo brasileño completo para compartir",
        ),
    },
    "fabio-almoco-salmao-pao-acucar.webp": {
        "pt": (
            "Salmão com molho de maracujá e Carioquinha de peixe, com vista para o Pão de Açúcar",
            "Salmão com molho de maracujá e Carioquinha de peixe",
        ),
        "en": (
            "Salmon with passion fruit sauce and fish carioquinha, with a view of Sugarloaf Mountain",
            "Salmon with passion fruit sauce and fish carioquinha",
        ),
        "es": (
            "Salmón con salsa de maracuyá y carioquinha de pescado, con vista al Pan de Azúcar",
            "Salmón con salsa de maracuyá y carioquinha de pescado",
        ),
    },
    "fabio-almoco-salmao-maracuja.webp": {
        "pt": (
            "Salmão com molho de maracujá, arroz de brócolis e legumes grelhados",
            "Salmão com molho de maracujá e arroz de brócolis",
        ),
        "en": (
            "Salmon with passion fruit sauce, broccoli rice and grilled vegetables",
            "Salmon with passion fruit sauce and broccoli rice",
        ),
        "es": (
            "Salmón con salsa de maracuyá, arroz de brócoli y vegetales a la parrilla",
            "Salmón con salsa de maracuyá y arroz de brócoli",
        ),
    },
    "fabio-almoco-picanha-fritas.webp": {
        "pt": (
            "Carioquinha de filé mignon com arroz, feijão, farofa e batata frita",
            "Carioquinha de filé mignon",
        ),
        "en": (
            "Filet mignon carioquinha with rice, beans, farofa and French fries",
            "Filet mignon carioquinha",
        ),
        "es": (
            "Carioquinha de filete mignon con arroz, frijoles, farofa y papas fritas",
            "Carioquinha de filete mignon",
        ),
    },
    "fabio-feijoada-caldeiron.webp": {
        "pt": (
            "Feijoada completa no caldeirão, servida com acompanhamentos tradicionais",
            "Feijoada completa no caldeirão",
        ),
        "en": (
            "Brazilian feijoada served in a pot with traditional side dishes",
            "Brazilian feijoada served in a pot",
        ),
        "es": (
            "Feijoada brasileña servida en una olla con acompañamientos tradicionales",
            "Feijoada brasileña servida en una olla",
        ),
    },
}

FIGURE_RE = re.compile(r"<figure\b.*?</figure>", re.I | re.S)
IMG_RE = re.compile(r"(<img\b[^>]*\balt=[\"'])([^\"']*)([\"'][^>]*>)", re.I | re.S)
CAPTION_RE = re.compile(r"(<figcaption\b[^>]*>)(.*?)(</figcaption>)", re.I | re.S)


def language(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return "en" if rel.startswith("en/") else "es" if rel.startswith("es/") else "pt"


def replace_figure(match: re.Match[str], lang: str) -> tuple[str, bool, str | None]:
    block = match.group(0)
    asset = next((name for name in CAPTIONS if name in block), None)
    if not asset:
        return block, False, None
    alt, caption = CAPTIONS[asset][lang]
    updated, alt_count = IMG_RE.subn(lambda m: m.group(1) + alt + m.group(3), block, count=1)
    updated, caption_count = CAPTION_RE.subn(
        lambda m: m.group(1) + "\n          " + caption + "\n        " + m.group(3),
        updated,
        count=1,
    )
    changed = updated != block
    return updated, changed and alt_count == 1 and caption_count == 1, asset


def normalize_placeholder_mapping(text: str) -> tuple[str, int]:
    count = 0
    pattern = re.compile(
        r"html body(?: main)? \.photo-ph\[data-label\*=\"Bobó\"\],"
        r"html body(?: main)? \.photo-ph\[data-label\*=\"Bobo\"\],"
        r"html body(?: main)? \.photo-ph\[data-label\*=\"camarão\"\],"
        r"html body(?: main)? \.photo-ph\[data-label\*=\"camarao\"\]"
    )
    replacement = (
        'html body main .photo-ph[data-label*="Risoto"],'
        'html body main .photo-ph[data-label*="risoto"],'
        'html body main .photo-ph[data-label*="Risotto"],'
        'html body main .photo-ph[data-label*="risotto"]'
    )
    text, changed = pattern.subn(replacement, text)
    count += changed

    asset_rules = (
        ("Feijoada", "feijoada-panela-close-acompanhamentos.webp"),
        ("Picanha", "almoco-picanha-grelhada.webp"),
        ("Salmão", "fabio-almoco-salmao-maracuja.webp"),
    )
    for label, asset in asset_rules:
        rule = re.compile(
            rf'(html body(?: main)? \.photo-ph\[data-label\*="{label}"\].*?'
            rf'\{{background-image:[^{{}}]*?url\([\'"])/assets/[^\'"]+([\'"]\)!important;\}})'
        )
        text, changed = rule.subn(rf"\1/assets/{asset}\2", text)
        count += changed

    picadinho = re.compile(
        r'html body(?: main)? \.photo-ph\[data-label\*="Picadinho"\],'
        r'html body(?: main)? \.photo-ph\[data-label\*="picadinho"\]'
        r'(?P<body>\{background-image:[^{}]*?url\([\'"])/assets/[^\'"]+(?P<end>[\'"]\)!important;\})'
    )
    carioquinha = (
        'html body main .photo-ph[data-label*="Carioquinha"],'
        'html body main .photo-ph[data-label*="carioquinha"]'
        r'\g<body>/assets/fabio-almoco-picanha-fritas.webp\g<end>'
    )
    text, changed = picadinho.subn(carioquinha, text)
    count += changed
    return text, count


def process(path: Path) -> tuple[bool, int, int, set[str]]:
    original = path.read_text(encoding="utf-8", errors="ignore")
    lang = language(path)
    figure_count = 0
    assets: set[str] = set()

    def repl(match: re.Match[str]) -> str:
        nonlocal figure_count
        updated, changed, asset = replace_figure(match, lang)
        if changed and asset:
            figure_count += 1
            assets.add(asset)
        return updated

    updated = FIGURE_RE.sub(repl, original)
    updated, mapping_count = normalize_placeholder_mapping(updated)
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return changed, figure_count, mapping_count, assets


def main() -> int:
    results = []
    for path in sorted(ROOT.rglob("*.html")):
        rel_parts = path.relative_to(ROOT).parts
        if any(part in EXCLUDED for part in rel_parts):
            continue
        changed, figures, mappings, assets = process(path)
        if changed:
            results.append((path.relative_to(ROOT).as_posix(), figures, mappings, assets))
    for path in SHARED_CSS:
        if not path.exists():
            continue
        changed, figures, mappings, assets = process(path)
        if changed:
            results.append((path.relative_to(ROOT).as_posix(), figures, mappings, assets))

    remaining_wrong = []
    for path in sorted(ROOT.rglob("*.html")):
        rel_parts = path.relative_to(ROOT).parts
        if any(part in EXCLUDED for part in rel_parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for term in (
            "Bobó de camarão — especialidade da casa",
            "Picanha grelhada com arroz, farofa e fritas",
            "Salmão grelhado with a view",
            "Salmão ao molho de maracujá",
        ):
            if term in text and path.relative_to(ROOT).as_posix().startswith("en/"):
                remaining_wrong.append(f"{path.relative_to(ROOT).as_posix()}: {term}")

    status = "PASS" if not remaining_wrong else "FAIL"
    REPORT.parent.mkdir(exist_ok=True)
    lines = [
        "# Food Photo Caption Fixes",
        "",
        f"Status geral: **{status}**",
        "",
        "## Resultado",
        f"- Arquivos alterados: **{len(results)}**",
        f"- Figuras corrigidas: **{sum(item[1] for item in results)}**",
        f"- Mapeamentos globais Bobó/camarão → risoto corrigidos: **{sum(item[2] for item in results)}**",
        "- Legendas e textos alternativos revisados em PT, EN e ES.",
        "",
        "## Arquivos",
        "",
        "| Página | Figuras | Mapeamentos | Imagens revisadas |",
        "|---|---:|---:|---|",
    ]
    for rel, figures, mappings, assets in results:
        lines.append(f"| `{rel}` | {figures} | {mappings} | {', '.join(sorted(assets)) or '-'} |")
    lines.extend(["", "## Pendências", ""])
    lines.extend(f"- {item}" for item in remaining_wrong) if remaining_wrong else lines.append("- Nenhuma.")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Food photo caption fixes: {status}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
