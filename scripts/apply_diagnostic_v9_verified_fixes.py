#!/usr/bin/env python3
"""Apply only the repository fixes verified while reviewing diagnostic v9."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "diagnostico_v9_verified_fixes_2026-08-24.md"

UNVERIFIED_SAME_AS = (
    "https://g.co/kgs/embaixadacarioca",
    "https://www.tripadvisor.com.br/Restaurant_Review-g303506-d6502345",
)

REFERENCE_REPLACEMENTS = {
    ROOT / "llms.txt": (
        ("(+100K seguidores)", "(84 mil seguidores)"),
        ("Seguidores Instagram: +100K", "Seguidores Instagram: 84 mil"),
        ("mais de +100.000 seguidores", "84 mil seguidores"),
        ("avaliação de 4.8 estrelas no Google e TripAdvisor", "avaliação de 4,8 estrelas no Google, com 8.847 avaliações"),
        ("Melhor do Brasil pelo Prêmio Prazeres da Mesa.", "Melhor do Brasil pela revista Prazeres da Mesa em 2017."),
        ("Melhor feijoada do Brasil — Revista Prazeres da Mesa (Academia da Cachaça)", "Melhor feijoada do Brasil — Revista Prazeres da Mesa 2017 (Academia da Cachaça)"),
        ("Grupo fundado em: 1984 (Academia da Cachaça)", "Grupo fundado em: 1985 (Academia da Cachaça)"),
        ("eleita melhor do Brasil pela Revista Prazeres da Mesa.", "eleita melhor do Brasil pela Revista Prazeres da Mesa em 2017."),
    ),
    ROOT / "en" / "llms.txt": (
        ("Rating: 4.8★ (Google and TripAdvisor)", "Rating: 4.8★ on Google (8,847 reviews)"),
        ("(+100K followers)", "(84K followers)"),
        ("over +100,000 Instagram followers", "84,000 Instagram followers"),
        ("a 4.8-star rating on Google and TripAdvisor", "a 4.8-star rating on Google based on 8,847 reviews"),
        ("Lunch: 12:00pm – 4:00pm", "Lunch: 11:30am – 5:00pm"),
        ("Sunset experience: 4:00pm – 9:00pm", "Sunset experience: 5:00pm – 9:00pm"),
        ("lunch from 12pm to 4pm, and sunset drinks from 4pm to 9pm", "lunch from 11:30am to 5pm, and sunset drinks from 5pm to 9pm"),
        (
            "The cable car ticket is required for access.",
            "The usual access is by cable car. When the Urca Hill trail is open, visitors may hike up without buying a ticket if they remain on Urca Hill; a ticket is required to use the cable car, continue to Sugarloaf Mountain, or descend by cable car.",
        ),
    ),
    ROOT / "es" / "llms.txt": (
        ("Calificación: 4.8★ (Google y TripAdvisor)", "Calificación: 4,8★ en Google (8.847 reseñas)"),
        ("(+100K seguidores)", "(84 mil seguidores)"),
        ("más de +100.000 seguidores", "84 mil seguidores"),
        ("una calificación de 4.8 estrellas en Google y TripAdvisor", "una calificación de 4,8 estrellas en Google basada en 8.847 reseñas"),
        ("Almuerzo: 12:00 – 16:00", "Almuerzo: 11:30 – 17:00"),
        ("Atardecer: 16:00 – 21:00", "Atardecer: 17:00 – 21:00"),
        ("el almuerzo de 12:00 a 16:00, y el atardecer de 16:00 a 21:00", "el almuerzo de 11:30 a 17:00 y el atardecer de 17:00 a 21:00"),
        (
            "Se requiere el boleto del teleférico para el acceso.",
            "El acceso habitual es por teleférico. Cuando el sendero del Morro da Urca está abierto, se puede subir caminando sin comprar boleto si se permanece en el Morro da Urca; el boleto es necesario para usar el teleférico, continuar al Pan de Azúcar o bajar en teleférico.",
        ),
    ),
}


def public_html() -> list[Path]:
    paths = list(ROOT.glob("*.html"))
    paths.extend((ROOT / "en").glob("*.html"))
    paths.extend((ROOT / "es").glob("*.html"))
    return sorted(paths)


def remove_json_list_value(text: str, value: str) -> tuple[str, int]:
    if value not in text:
        return text, 0
    lines = text.splitlines()
    removed = 0
    index = 0
    while index < len(lines):
        if value not in lines[index]:
            index += 1
            continue
        has_trailing_comma = lines[index].rstrip().endswith(",")
        del lines[index]
        removed += 1
        if not has_trailing_comma:
            previous = index - 1
            while previous >= 0 and not lines[previous].strip():
                previous -= 1
            if previous >= 0:
                lines[previous] = lines[previous].rstrip().removesuffix(",")
    return "\n".join(lines) + "\n", removed


def main() -> int:
    html_changed: list[str] = []
    removed_urls = 0
    for path in public_html():
        original = path.read_text(encoding="utf-8")
        updated = original
        for value in UNVERIFIED_SAME_AS:
            updated, count = remove_json_list_value(updated, value)
            removed_urls += count
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            html_changed.append(path.relative_to(ROOT).as_posix())

    references_changed: list[str] = []
    replacement_count = 0
    for path, replacements in REFERENCE_REPLACEMENTS.items():
        original = path.read_text(encoding="utf-8")
        updated = original
        for old, new in replacements:
            count = updated.count(old)
            if count:
                updated = updated.replace(old, new)
                replacement_count += count
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            references_changed.append(path.relative_to(ROOT).as_posix())

    public_text = "\n".join(path.read_text(encoding="utf-8") for path in public_html())
    reference_text = "\n".join(path.read_text(encoding="utf-8") for path in REFERENCE_REPLACEMENTS)
    checks = {
        "Links sameAs não verificados removidos": not any(value in public_text for value in UNVERIFIED_SAME_AS),
        "Seguidores padronizados em 84 mil/84K": "+100K" not in reference_text and "+100.000" not in reference_text,
        "Avaliação associada somente ao Google": "Google and TripAdvisor" not in reference_text and "Google y TripAdvisor" not in reference_text and "Google e TripAdvisor" not in reference_text,
        "Total de 8.847 avaliações presente nos três idiomas": reference_text.count("8.847") + reference_text.count("8,847") >= 3,
    }
    status = "PASS" if all(checks.values()) else "FAIL"

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Correções verificadas do diagnóstico v9",
        "",
        "Data: 2026-08-24",
        "",
        f"Status geral: **{status}**",
        "",
        "## Resultado",
        "",
        f"- Páginas HTML alteradas: **{len(html_changed)}**",
        f"- Referências `sameAs` não verificadas removidas: **{removed_urls}**",
        f"- Arquivos de referência para IA alterados: **{len(references_changed)}**",
        f"- Substituições factuais nos arquivos de IA: **{replacement_count}**",
        "- Relação formal com Academia da Cachaça e Cantina do MAM: **preservada**",
        "- Review/Rating/AggregateRating: **não inseridos**",
        "",
        "## Validações",
        "",
    ]
    lines.extend(f"- {'PASS' if ok else 'FAIL'} — {label}" for label, ok in checks.items())
    lines.extend(["", "## HTML alterado", ""])
    lines.extend(f"- `{name}`" for name in html_changed)
    lines.extend(["", "## Referências para IA alteradas", ""])
    lines.extend(f"- `{name}`" for name in references_changed)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{status}: html={len(html_changed)} sameAs={removed_urls} references={len(references_changed)}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
