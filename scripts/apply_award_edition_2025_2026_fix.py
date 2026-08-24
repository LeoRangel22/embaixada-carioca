#!/usr/bin/env python3
"""Normaliza a edição do prêmio Veja Rio sem alterar a atribuição factual."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "award_edition_2025_2026_fix_report.md"
SKIP_PARTS = {"_backups", "_templates", "sources", ".codex-work", "node_modules"}
OLD_EDITION = re.compile(r"(Veja Rio[^\r\n]{0,220}?)\b2025\b(?!/2026)", re.I)


def public_html_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.html")
        if not any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts)
    )


def normalize(text: str) -> tuple[str, int]:
    return OLD_EDITION.subn(r"\g<1>2025/2026", text)


def main() -> int:
    changed: list[tuple[str, int]] = []
    total = 0

    for path in public_html_files():
        original = path.read_text(encoding="utf-8")
        updated, count = normalize(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="")
            rel = path.relative_to(ROOT).as_posix()
            changed.append((rel, count))
            total += count

    remaining: list[str] = []
    for path in public_html_files():
        if OLD_EDITION.search(path.read_text(encoding="utf-8")):
            remaining.append(path.relative_to(ROOT).as_posix())

    status = "PASS" if not remaining else "FAIL"
    lines = [
        "# Normalização da edição do prêmio Veja Rio",
        "",
        "Data: 2026-08-24",
        f"Status geral: **{status}**",
        "",
        "## Regra factual",
        "",
        "- Academia da Cachaça: **Melhor Feijoada do Rio — Veja Rio Comer & Beber 2025/2026**.",
        "- Academia da Cachaça: **Melhor Feijoada do Brasil — Prazeres da Mesa 2017**.",
        "- A mesma feijoada é servida na Embaixada Carioca por meio de parceria formal.",
        "",
        "## Resultado",
        "",
        f"- Arquivos HTML alterados: **{len(changed)}**",
        f"- Menções atualizadas de 2025 para 2025/2026: **{total}**",
        f"- Arquivos com edição antiga remanescente: **{len(remaining)}**",
        "",
        "## Arquivos alterados",
        "",
    ]
    lines.extend(f"- `{rel}` — {count} ajuste(s)" for rel, count in changed)
    if remaining:
        lines.extend(["", "## Pendências", ""])
        lines.extend(f"- `{rel}`" for rel in remaining)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
    print(f"Award edition normalization: {status} changed={len(changed)} replacements={total}")
    print(f"Report: {REPORT}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
