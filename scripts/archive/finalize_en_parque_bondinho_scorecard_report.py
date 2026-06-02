#!/usr/bin/env python3
"""Finalize the EN Parque Bondinho scorecard report after all pipeline steps.

This validator reads the final HTML state and writes the report based on the
actual page, avoiding stale FAIL status from an earlier intermediate step.
"""
from __future__ import annotations

from pathlib import Path
import html
import json
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "en" / "parque-bondinho.html"
REPORT = ROOT / "_audit_reports" / "en_parque_bondinho_scorecard_fix_report.md"
EXPECTED_TITLE = "Sugarloaf Cable Car Park | Embaixada Carioca"
JSONLD_RE = re.compile(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)


def parse_json(raw: str) -> Any | None:
    try:
        return json.loads(html.unescape(raw.strip()))
    except Exception:
        return None


def typ_has(value: Any, wanted: str) -> bool:
    if isinstance(value, str):
        return value.lower() == wanted.lower()
    if isinstance(value, list):
        return any(typ_has(v, wanted) for v in value)
    return False


def is_faq(obj: Any) -> bool:
    return isinstance(obj, dict) and typ_has(obj.get("@type"), "FAQPage")


def walk_faq(obj: Any) -> tuple[int, int]:
    pages = 0
    questions = 0
    if isinstance(obj, dict):
        if is_faq(obj):
            pages += 1
            main = obj.get("mainEntity")
            if isinstance(main, list):
                questions += len(main)
        for value in obj.values():
            p, q = walk_faq(value)
            pages += p
            questions += q
    elif isinstance(obj, list):
        for item in obj:
            p, q = walk_faq(item)
            pages += p
            questions += q
    return pages, questions


def count_faq(source: str) -> tuple[int, int]:
    pages = 0
    questions = 0
    for _, raw, _ in JSONLD_RE.findall(source):
        obj = parse_json(raw)
        if obj is None:
            continue
        p, q = walk_faq(obj)
        pages += p
        questions += q
    return pages, questions


def count_words(source: str) -> int:
    text = re.sub(r"<script[\s\S]*?</script>", " ", source, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"\b[\wÀ-ÿ]{2,}\b", html.unescape(text)))


def ensure_title(source: str) -> tuple[str, bool]:
    updated = re.sub(r"<title>.*?</title>", f"<title>{EXPECTED_TITLE}</title>", source, count=1, flags=re.I | re.S)
    updated = re.sub(
        r'<meta\b(?=[^>]*property=["\']og:title["\'])(?=[^>]*content=["\'][^"\']*["\'])[^>]*>',
        f'<meta property="og:title" content="{EXPECTED_TITLE}"/>',
        updated,
        count=1,
        flags=re.I | re.S,
    )
    return updated, updated != source


def title_ok(source: str) -> bool:
    match = re.search(r"<title>(.*?)</title>", source, flags=re.I | re.S)
    if not match:
        return False
    return html.unescape(match.group(1).strip()) == EXPECTED_TITLE


def main() -> int:
    if not PAGE.exists():
        REPORT.parent.mkdir(exist_ok=True)
        REPORT.write_text("# EN Parque Bondinho Scorecard Fix\n\nStatus geral: **FAIL**\n\nPágina ausente.\n", encoding="utf-8")
        return 1

    original = PAGE.read_text(encoding="utf-8", errors="ignore")
    source, changed_title = ensure_title(original)
    if changed_title:
        PAGE.write_text(source, encoding="utf-8")

    faq_pages, faq_questions = count_faq(source)
    ol_count = len(re.findall(r"<ol\b", source, flags=re.I))
    words = count_words(source)
    title_is_ok = title_ok(source)
    status = "PASS" if faq_pages == 1 and faq_questions == 8 and ol_count >= 1 and words >= 1200 and title_is_ok else "FAIL"
    result_status = "ok" if status == "PASS" else "fail"

    REPORT.parent.mkdir(exist_ok=True)
    lines = [
        "# EN Parque Bondinho Scorecard Fix",
        "",
        f"Status geral: **{status}**",
        "",
        "## Objetivo",
        "Validar o estado final de `en/parque-bondinho.html`: FAQ, lista `<ol>`, palavras e title em inglês.",
        "",
        "## Resultado",
        "- Página: `en/parque-bondinho.html`",
        f"- Status: `{result_status}`",
        f"- Changed: `{changed_title}`",
        f"- FAQPage: `{faq_pages}`",
        f"- Perguntas FAQ: `{faq_questions}`",
        f"- Listas `<ol>`: `{ol_count}`",
        f"- Palavras: `{words}`",
        f"- Title corrigido: `{title_is_ok}`",
        f"- Notas: `final_state_validation=True`",
        "",
        "## Guardrails",
        "- Nenhum Rating, Review ou AggregateRating foi inserido.",
        "- O relatório reflete o HTML final após os demais scripts do pipeline.",
        "- O title esperado é `Sugarloaf Cable Car Park | Embaixada Carioca`.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"EN Parque Bondinho final scorecard report: {status}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
