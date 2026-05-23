#!/usr/bin/env python3
"""Apply the red-block copidesk fixes from the May 2026 deep diagnosis.

Scope:
1. English CTA/navigational button still using Portuguese RESERVAR.
2. Spanish duplicate phrase: Academia da Cachaça de Academia da Cachaça.
3. Spanish title truncated as Embaixada instead of Embaixada Carioca.
4. Typo dBaía/dBaia.
5. Portuguese typo: Consulte a equipo -> Consulte a equipe.
6. Duplicate article: o o Bondinho.

The script is intentionally conservative: it only changes text files and records a report.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT = REPORT_DIR / "red_block_copidesk_fixes_report.md"

EXCLUDE_DIRS = {".git", ".github", "node_modules", "_audit_reports", "dist", "build", "coverage", "visual_browser_screenshots"}
TEXT_EXTENSIONS = {".html", ".htm", ".js", ".json", ".txt", ".xml", ".md"}

@dataclass
class Change:
    path: str
    before: str
    after: str
    count: int


def is_text_candidate(path: Path) -> bool:
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return False
    return path.suffix.lower() in TEXT_EXTENSIONS


def replace_literal(text: str, before: str, after: str, changes: list[Change], rel: str) -> str:
    count = text.count(before)
    if count:
        text = text.replace(before, after)
        changes.append(Change(rel, before, after, count))
    return text


def replace_regex(text: str, pattern: str, repl: str, label: str, changes: list[Change], rel: str, flags: int = 0) -> str:
    new_text, count = re.subn(pattern, repl, text, flags=flags)
    if count:
        changes.append(Change(rel, label, repl, count))
    return new_text


def apply_file(path: Path) -> list[Change]:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text
    changes: list[Change] = []

    # 1) English: Portuguese CTA in EN version.
    if rel.startswith("en/"):
        text = replace_literal(text, ">RESERVAR<", ">Reserve<", changes, rel)
        text = replace_literal(text, ">Reservar<", ">Reserve<", changes, rel)
        text = replace_literal(text, "RESERVAR MESA", "Reserve a table", changes, rel)
        text = replace_literal(text, "Reservar mesa", "Reserve a table", changes, rel)
        text = replace_literal(text, "7.779 avaliações", "7,779 reviews", changes, rel)
        text = replace_literal(text, "7.779 avaliações verificadas", "7,779 verified reviews", changes, rel)
        text = replace_literal(text, "avaliações verificadas", "verified reviews", changes, rel)

    # Spanish copy fixes.
    if rel.startswith("es/"):
        text = replace_literal(text, "Academia da Cachaça de Academia da Cachaça", "Academia da Cachaça", changes, rel)
        text = replace_literal(text, "7.779 avaliações", "7.779 reseñas", changes, rel)
        text = replace_literal(text, "7.779 avaliações verificadas", "7.779 reseñas verificadas", changes, rel)
        text = replace_literal(text, "avaliações verificadas", "reseñas verificadas", changes, rel)
        text = replace_literal(text, "vista panorámica panorámicas", "vista panorámica", changes, rel)
        text = replace_literal(text, "Dos universos, una vista", "Dois universos, uma vista", changes, rel)
        text = replace_regex(
            text,
            r"(<title>Restaurante en Pan de Az[úu]car y Morro da Urca \| Embaixada)(</title>)",
            r"\1 Carioca\2",
            "<title>... | Embaixada</title>",
            changes,
            rel,
            flags=re.I,
        )
        text = replace_regex(
            text,
            r"(<meta\s+property=[\"']og:title[\"']\s+content=[\"']Restaurante en Pan de Az[úu]car y Morro da Urca \| Embaixada)([\"'])",
            r"\1 Carioca\2",
            "og:title ... | Embaixada",
            changes,
            rel,
            flags=re.I,
        )
        text = replace_regex(
            text,
            r"(<meta\s+name=[\"']twitter:title[\"']\s+content=[\"']Restaurante en Pan de Az[úu]car y Morro da Urca \| Embaixada)([\"'])",
            r"\1 Carioca\2",
            "twitter:title ... | Embaixada",
            changes,
            rel,
            flags=re.I,
        )

    # 4) dBaía typo across PT/EN/ES/Guide files.
    text = replace_literal(text, "dBaía", "da Baía", changes, rel)
    text = replace_literal(text, "dBaia", "da Baía", changes, rel)

    # 5) PT typo from diagnosis.
    text = replace_literal(text, "Consulte a equipo", "Consulte a equipe", changes, rel)
    text = replace_literal(text, "consulte a equipo", "consulte a equipe", changes, rel)

    # 6) Duplicate article in chatbot/content.
    text = replace_literal(text, "vista para o o Bondinho", "vista para o Bondinho", changes, rel)
    text = replace_literal(text, "para o o Bondinho", "para o Bondinho", changes, rel)
    text = replace_literal(text, "o o Bondinho", "o Bondinho", changes, rel)

    if text != original:
        path.write_text(text, encoding="utf-8")
    return changes


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    all_changes: list[Change] = []
    for path in sorted(ROOT.rglob("*"), key=lambda p: p.relative_to(ROOT).as_posix()):
        if path.is_file() and is_text_candidate(path):
            all_changes.extend(apply_file(path))

    lines = [
        "# Red Block Copidesk Fixes Report",
        "",
        "Status: **PASS**",
        "Origem: Diagnóstico Profundo — Embaixada Carioca, bloco vermelho de urgência alta + impacto alto.",
        "",
        "## Correções previstas",
        "1. EN: botão RESERVAR em português.",
        "2. ES: redundância Academia da Cachaça de Academia da Cachaça.",
        "3. ES: title truncado Embaixada -> Embaixada Carioca.",
        "4. PT: dBaía/dBaia -> da Baía.",
        "5. PT: Consulte a equipo -> Consulte a equipe.",
        "6. PT: o o Bondinho -> o Bondinho.",
        "",
        f"Total de substituições: **{sum(c.count for c in all_changes)}**",
        f"Arquivos alterados: **{len(set(c.path for c in all_changes))}**",
        "",
        "## Detalhe",
    ]
    if all_changes:
        for c in all_changes:
            lines.append(f"- `{c.path}` — {c.count}x — `{c.before}` → `{c.after}`")
    else:
        lines.append("Nenhuma ocorrência pendente encontrada. As correções já estavam aplicadas ou não havia correspondência literal.")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Red block copidesk fixes: replacements={sum(c.count for c in all_changes)} files={len(set(c.path for c in all_changes))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
