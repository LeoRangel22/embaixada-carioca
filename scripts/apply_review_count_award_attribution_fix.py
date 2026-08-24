#!/usr/bin/env python3
"""Normalize Google review counts and clarify feijoada award attribution.

The owner confirmed 8,847 Google reviews on 2026-08-24. This one-off fixer
updates published HTML in PT/EN/ES and the shared navigation include. It also
rewrites ambiguous award badges so they credit Academia da Cachaca while
making clear that the feijoada is served at Embaixada Carioca.

Guardrails:
- does not add or edit rating/review structured-data properties;
- does not change canonical or hreflang links;
- does not change prices, opening hours or menu items.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "review_count_award_attribution_fix_report.md"
EXCLUDED_DIRS = {
    ".git",
    ".codex-work",
    "node_modules",
    "_audit_reports",
    "_backups",
    "_templates",
    "_site",
    "dist",
    "build",
    "scripts",
    "tests",
}
JSONLD_RE = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)


@dataclass
class Result:
    path: str
    changed: bool
    review_replacements: int
    award_replacements: int


def published_html() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.html")
        if not any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts)
    )


def language(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    parts = path.relative_to(ROOT).parts
    if rel.startswith("en/") or ("partials" in parts and "en" in parts):
        return "en"
    if rel.startswith("es/") or ("partials" in parts and "es" in parts):
        return "es"
    return "pt"


OLD_NUMBER = r"(?:7[.,](?:700|779)|8[.,](?:000|200|255|600)|8\s*mil|8\s*thousand)"


def replace_count(text: str, path: Path) -> tuple[str, int]:
    lang = language(path)
    replacement = "8,847" if lang == "en" else "8.847"
    nouns = r"(?:Google\s+)?(?:reviews|avaliações|reseñas)"
    qualifiers = r"(?:(?:mais|más)\s+de\s+|more\s+than\s+|over\s+)?"
    pattern = re.compile(
        rf"{qualifiers}{OLD_NUMBER}\+?(?=\s+{nouns}\b)",
        re.I,
    )
    updated, count = pattern.subn(replacement, text)

    # Fix the language of the review noun in the most common generated badges.
    if lang == "en":
        updated, extra = re.subn(r"8[.,]847\s+(?:avaliações|reseñas)", "8,847 reviews", updated, flags=re.I)
        count += extra
        updated = updated.replace("Google Reviews: 4.8 estrelas", "Google Reviews: 4.8 stars")
        updated = updated.replace("Google Reviews · 4.8 estrelas", "Google Reviews · 4.8 stars")
    elif lang == "es":
        updated, extra = re.subn(r"8[.,]847\s+(?:avaliações|reviews)", "8.847 reseñas", updated, flags=re.I)
        count += extra
        updated = updated.replace("Google Reviews: 4.8 estrelas", "Google Reviews: 4.8 estrellas")
        updated = updated.replace("Google Reviews · 4.8 estrelas", "Google Reviews · 4.8 estrellas")
    else:
        updated, extra = re.subn(r"8\.847\s+(?:reviews|reseñas)", "8.847 avaliações", updated, flags=re.I)
        count += extra
    return updated, count


AWARD_REPLACEMENTS: dict[str, list[tuple[str, str]]] = {
    "pt": [
        (
            "🏆 Premiado · Veja Rio Comer & Beber 2025",
            "🏆 Academia da Cachaça · Melhor Feijoada · Veja Rio 2025",
        ),
        (
            "🏆 Prêmio Veja Rio Comer & Beber 2025 · Melhor Feijoada do Rio",
            "🏆 Academia da Cachaça · Melhor Feijoada · Veja Rio 2025",
        ),
        (
            "🏆 Veja Rio Comer &amp; Beber 2025 · Melhor Feijoada do Rio",
            "🏆 Academia da Cachaça · Melhor Feijoada · Veja Rio 2025",
        ),
        (
            "🏆 Melhor Feijoada do Río — Veja Rio Comer & Beber 2025",
            "🏆 Feijoada da Academia da Cachaça · Melhor Feijoada · Veja Rio 2025",
        ),
        (
            "🏆 Melhor Feijoada do Rio · Veja Rio Comer & Beber 2025",
            "🏆 Feijoada da Academia da Cachaça · Melhor Feijoada · Veja Rio 2025",
        ),
        (
            "<strong>🏆 Melhor Feijoada do Rio de Janeiro</strong> — Veja Rio Comer &amp; Beber 2025",
            "<strong>🏆 Feijoada da Academia da Cachaça</strong> — vencedora da categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025",
        ),
    ],
    "en": [
        (
            "🏆 Award winner · Veja Rio Comer & Beber 2025",
            "🏆 Academia da Cachaça · Best Feijoada · Veja Rio 2025",
        ),
        (
            "🏆 Veja Rio Comer & Beber 2025 · Best Feijoada in Rio de Janeiro",
            "🏆 Academia da Cachaça · Best Feijoada · Veja Rio 2025",
        ),
        (
            "🏆 Best Feijoada in Rio de Janeiro · Veja Rio Comer & Beber 2025",
            "🏆 Academia da Cachaça · Best Feijoada · Veja Rio 2025",
        ),
    ],
    "es": [
        (
            "🏆 Premiada · Veja Rio Comer & Beber 2025",
            "🏆 Academia da Cachaça · Mejor Feijoada · Veja Rio 2025",
        ),
        (
            "🏆 Mejor Feijoada de Río de Janeiro · Veja Rio Comer & Beber 2025",
            "🏆 Academia da Cachaça · Mejor Feijoada · Veja Rio 2025",
        ),
        (
            "🏆 Mejor Feijoada de Río · Veja Rio Comer & Beber 2025",
            "🏆 Academia da Cachaça · Mejor Feijoada · Veja Rio 2025",
        ),
    ],
}


def replace_awards(text: str, path: Path) -> tuple[str, int]:
    updated = text
    count = 0
    for old, new in AWARD_REPLACEMENTS[language(path)]:
        occurrences = updated.count(old)
        if occurrences:
            updated = updated.replace(old, new)
            count += occurrences
    return updated, count


def has_forbidden_type(value: Any) -> bool:
    if isinstance(value, str):
        return value in {"Review", "Rating", "AggregateRating"}
    if isinstance(value, list):
        return any(has_forbidden_type(item) for item in value)
    return False


def unsafe_jsonld(text: str) -> list[str]:
    problems: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in {
                    "aggregateRating",
                    "ratingValue",
                    "reviewCount",
                    "ratingCount",
                    "bestRating",
                    "worstRating",
                    "review",
                }:
                    problems.append(key)
                if key == "@type" and has_forbidden_type(child):
                    problems.append(f"@type={child}")
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    for match in JSONLD_RE.finditer(text):
        try:
            walk(json.loads(match.group(1)))
        except json.JSONDecodeError as exc:
            problems.append(f"JSON parse error: {exc}")
    return problems


def stale_review_count(text: str) -> bool:
    nouns = r"(?:Google\s+)?(?:reviews|avaliações|reseñas)"
    return bool(re.search(rf"{OLD_NUMBER}\+?\s+{nouns}\b", text, re.I))


def main() -> int:
    targets = published_html()
    shared_nav = ROOT / "_includes" / "nav.html"
    if shared_nav.exists():
        targets.append(shared_nav)

    results: list[Result] = []
    problems: list[str] = []
    for path in targets:
        original = path.read_text(encoding="utf-8")
        updated, review_count = replace_count(original, path)
        updated, award_count = replace_awards(updated, path)
        changed = updated != original
        if changed:
            path.write_text(updated, encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        results.append(Result(rel, changed, review_count, award_count))
        if stale_review_count(updated):
            problems.append(f"{rel}: stale review count")
        for problem in unsafe_jsonld(updated):
            problems.append(f"{rel}: {problem}")

    changed_results = [result for result in results if result.changed]
    status = "PASS" if not problems else "FAIL"
    lines = [
        "# Review Count and Feijoada Award Attribution Fix",
        "",
        f"- Status geral: **{status}**",
        "- Número confirmado pelo proprietário: **8.847 avaliações no Google**",
        f"- Arquivos verificados: **{len(results)}**",
        f"- Arquivos alterados: **{len(changed_results)}**",
        f"- Substituições de contagem: **{sum(item.review_replacements for item in results)}**",
        f"- Substituições de atribuição do prêmio: **{sum(item.award_replacements for item in results)}**",
        "- JSON-LD: nenhum Review, Rating ou AggregateRating permitido",
        "",
        "## Arquivos alterados",
        "",
        "| Arquivo | Avaliações | Prêmio |",
        "|---|---:|---:|",
    ]
    lines.extend(
        f"| `{item.path}` | {item.review_replacements} | {item.award_replacements} |"
        for item in changed_results
    )
    lines.extend(["", "## Pendências", ""])
    lines.extend(f"- {problem}" for problem in problems)
    if not problems:
        lines.append("- Nenhuma.")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{status}: {len(changed_results)} files changed; report={REPORT.relative_to(ROOT)}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
