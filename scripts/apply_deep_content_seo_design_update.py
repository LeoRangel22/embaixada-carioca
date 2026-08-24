#!/usr/bin/env python3
"""Apply the August 2026 content/SEO/design integrity closeout.

This is deliberately conservative: it fixes exact, confirmed strings and
metadata without touching JSON-LD, canonical URLs, hreflang or page layout.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "deep_content_seo_design_update_2026-08-24.md"


def public_html() -> list[tuple[Path, str]]:
    pages: list[tuple[Path, str]] = []
    pages.extend((path, "pt") for path in ROOT.glob("*.html"))
    pages.extend((path, "en") for path in (ROOT / "en").glob("*.html"))
    pages.extend((path, "es") for path in (ROOT / "es").glob("*.html"))
    return sorted(pages, key=lambda item: item[0].relative_to(ROOT).as_posix())


LANG_REPLACEMENTS: dict[str, tuple[tuple[str, str], ...]] = {
    "pt": (
        ("A trilha del Morro da Urca", "A trilha do Morro da Urca"),
        ("en lo alto del Morro da Urca", "no alto do Morro da Urca"),
    ),
    "en": (
        ("Google Reviews: 4.8 estrelas", "Google Reviews: 4.8 stars"),
        ("Google Reviews · 4.8 estrelas", "Google Reviews · 4.8 stars"),
        ('aria-label="Selecionar idioma"', 'aria-label="Select language"'),
        ('aria-label="Abrir menu de navegação"', 'aria-label="Open navigation menu"'),
        ('aria-label="Idioma atual: EN"', 'aria-label="Current language: EN"'),
        (
            "O consulado da gastronomia e da cultura brasileira para o mundo — en lo alto del Morro da Urca, Rio de Janeiro.",
            "Brazilian food and culture, shared with the world — high above Rio on Urca Hill.",
        ),
        (
            "O consulado da gastronomia e da cultura brasileira para o mundo — atop Urca Hill, Rio de Janeiro.",
            "Brazilian food and culture, shared with the world — high above Rio on Urca Hill.",
        ),
    ),
    "es": (
        ("Google Reviews: 4.8 estrelas", "Google Reviews: 4.8 estrellas"),
        ("Google Reviews · 4.8 estrelas", "Google Reviews · 4.8 estrellas"),
        ('aria-label="Selecionar idioma"', 'aria-label="Seleccionar idioma"'),
        ('aria-label="Abrir menu de navegação"', 'aria-label="Abrir menú de navegación"'),
        ('aria-label="Idioma atual: ES"', 'aria-label="Idioma actual: ES"'),
        (
            "O consulado da gastronomia e da cultura brasileira para o mundo —",
            "La gastronomía y la cultura brasileña para el mundo —",
        ),
        (
            "O consulado da gastronomia e da cultura brasileira para o mundo — en lo alto del Morro da Urca, Río de Janeiro.",
            "La gastronomía y la cultura brasileña para el mundo — en lo alto del Morro da Urca, Río de Janeiro.",
        ),
    ),
}


def replace_exact(text: str, replacements: tuple[tuple[str, str], ...]) -> tuple[str, int]:
    total = 0
    for old, new in replacements:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            total += count
    return text, total


def update_metadata(path: Path, title: str, description: str) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    text, title_count = re.subn(r"<title>.*?</title>", f"<title>{title}</title>", text, count=1, flags=re.S)
    text, description_count = re.subn(
        r'<meta\s+content="[^"]*"\s+name="description"\s*/?>',
        f'<meta content="{description}" name="description"/>',
        text,
        count=1,
        flags=re.I,
    )
    path.write_text(text, encoding="utf-8")
    return title_count, description_count


def main() -> int:
    changed: list[str] = []
    replacement_total = 0

    for path, lang in public_html():
        original = path.read_text(encoding="utf-8")
        updated, replacements = replace_exact(original, LANG_REPLACEMENTS[lang])
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())
            replacement_total += replacements

    partials = (
        (ROOT / "src" / "partials" / "pt" / "footer.html", "pt"),
        (ROOT / "src" / "partials" / "en" / "footer.html", "en"),
        (ROOT / "src" / "partials" / "en" / "nav.html", "en"),
        (ROOT / "src" / "partials" / "es" / "footer.html", "es"),
        (ROOT / "src" / "partials" / "es" / "nav.html", "es"),
    )
    for path, lang in partials:
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        updated, replacements = replace_exact(original, LANG_REPLACEMENTS[lang])
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())
            replacement_total += replacements

    cafe_title = "Café da Manhã no Morro da Urca | Embaixada Carioca"
    cafe_description = (
        "Café da manhã todos os dias, das 8h30 às 11h30, no Morro da Urca, "
        "com vista direta para o Pão de Açúcar. Reserve sua mesa."
    )
    route_title = "Como Chegar ao Morro da Urca | Embaixada Carioca"
    route_description = (
        "Veja como chegar à Embaixada Carioca no Morro da Urca: entrada pela Av. Pasteur, 520, "
        "acesso pelo Bondinho ou pela trilha quando aberta."
    )
    metadata_updates = 0
    for path, title, description in (
        (ROOT / "cafe-da-manha.html", cafe_title, cafe_description),
        (ROOT / "como-chegar.html", route_title, route_description),
    ):
        before = path.read_text(encoding="utf-8")
        title_count, description_count = update_metadata(path, title, description)
        after = path.read_text(encoding="utf-8")
        if after != before and path.relative_to(ROOT).as_posix() not in changed:
            changed.append(path.relative_to(ROOT).as_posix())
        metadata_updates += title_count + description_count

    eventos = ROOT / "eventos.html"
    eventos_text = eventos.read_text(encoding="utf-8")
    anchor_added = False
    if 'href="#conteudo-principal"' in eventos_text and 'id="conteudo-principal"' not in eventos_text:
        eventos_text, count = re.subn(r"<main(\s*)>", r'<main id="conteudo-principal"\1>', eventos_text, count=1)
        if count:
            eventos.write_text(eventos_text, encoding="utf-8")
            anchor_added = True
            if "eventos.html" not in changed:
                changed.append("eventos.html")

    residuals: list[str] = []
    for path, lang in public_html():
        text = path.read_text(encoding="utf-8")
        for old, _ in LANG_REPLACEMENTS[lang]:
            if old in text:
                residuals.append(f"{path.relative_to(ROOT).as_posix()}: {old}")

    cafe_html = (ROOT / "cafe-da-manha.html").read_text(encoding="utf-8")
    route_html = (ROOT / "como-chegar.html").read_text(encoding="utf-8")
    eventos_html = eventos.read_text(encoding="utf-8")
    checks = {
        "Contaminações exatas de idioma removidas": not residuals,
        "Metadados de Café da Manhã atualizados": cafe_title in cafe_html and cafe_description in cafe_html,
        "Metadados de Como Chegar atualizados": route_title in route_html and route_description in route_html,
        "Destino do skip link em Eventos presente": 'id="conteudo-principal"' in eventos_html,
        "Avaliações atuais preservadas": "8.847 avaliações" in cafe_html and "8.847 avaliações" in route_html,
    }
    status = "PASS" if all(checks.values()) else "FAIL"

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Atualização profunda de conteúdo, SEO e integridade visual",
        "",
        "Data: 2026-08-24",
        "",
        f"Status geral: **{status}**",
        "",
        "## Resultado",
        "",
        f"- Arquivos alterados: **{len(changed)}**",
        f"- Substituições editoriais/localização: **{replacement_total}**",
        f"- Campos de metadata processados: **{metadata_updates}**",
        f"- Âncora de acessibilidade adicionada em Eventos: **{'Sim' if anchor_added else 'Já existia'}**",
        "- JSON-LD, canonical e hreflang: **não alterados**",
        "",
        "## Validações",
        "",
    ]
    lines.extend(f"- {'PASS' if ok else 'FAIL'} — {label}" for label, ok in checks.items())
    lines.extend(["", "## Arquivos alterados", ""])
    lines.extend(f"- `{name}`" for name in sorted(changed))
    if residuals:
        lines.extend(["", "## Resíduos encontrados", ""])
        lines.extend(f"- {item}" for item in residuals)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{status}: {len(changed)} files changed; report={REPORT.relative_to(ROOT)}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
