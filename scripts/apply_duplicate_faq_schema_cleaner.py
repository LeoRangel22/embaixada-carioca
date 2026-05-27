#!/usr/bin/env python3
"""Remove duplicate FAQPage JSON-LD on priority pages.

Keeps one FAQPage per URL and preserves non-FAQ JSON-LD nodes. This is a
post-pipeline guard for Search Console/Rich Results stability.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "duplicate_faq_schema_cleaner_report.md"

JSONLD_RE = re.compile(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)
SCRIPT_ID_RE = re.compile(r'\bid=["\']([^"\']+)["\']', re.I)

STATIC_ID = "ec-static-product-schema-faq"
SPECIAL_KEEP_STATIC = {"es/cardapio.html", "es/almoco.html"}
TARGETS = [
    "index.html",
    "en/index.html",
    "es/index.html",
    "feijoada.html",
    "cafe-da-manha.html",
    "eventos.html",
    "en/cardapio.html",
    "es/cardapio.html",
    "en/almoco.html",
    "es/almoco.html",
    "parque-bondinho.html",
]


@dataclass
class Result:
    page: str
    status: str
    changed: bool
    faq_pages_before: int
    faq_questions_before: int
    faq_pages_after: int
    faq_questions_after: int
    removed_faq_nodes: int
    notes: str


def script_id(opener: str) -> str:
    m = SCRIPT_ID_RE.search(opener or "")
    return m.group(1) if m else ""


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


def count_faq(obj: Any) -> tuple[int, int]:
    pages = 0
    questions = 0
    if isinstance(obj, dict):
        if is_faq(obj):
            pages += 1
            items = obj.get("mainEntity")
            if isinstance(items, list):
                questions += len(items)
        for value in obj.values():
            p, q = count_faq(value)
            pages += p
            questions += q
    elif isinstance(obj, list):
        for item in obj:
            p, q = count_faq(item)
            pages += p
            questions += q
    return pages, questions


def strip_faq(obj: Any) -> tuple[Any | None, int]:
    if is_faq(obj):
        return None, 1
    if isinstance(obj, dict):
        removed = 0
        cleaned: dict[str, Any] = {}
        for key, value in obj.items():
            new_value, count = strip_faq(value)
            removed += count
            if new_value is None:
                continue
            if isinstance(new_value, list) and not new_value:
                continue
            cleaned[key] = new_value
        if not cleaned:
            return None, removed
        return cleaned, removed
    if isinstance(obj, list):
        kept = []
        removed = 0
        for item in obj:
            new_item, count = strip_faq(item)
            removed += count
            if new_item is not None:
                kept.append(new_item)
        return kept, removed
    return obj, 0


def serialize(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def should_keep_faq(page: str, sid: str, faq_questions: int, kept: bool) -> bool:
    if page in SPECIAL_KEEP_STATIC:
        if sid == STATIC_ID and faq_questions >= 8:
            return True
        return False
    if sid == STATIC_ID:
        return False
    if not kept and faq_questions >= 8:
        return True
    if not kept and faq_questions > 0:
        return True
    return False


def clean_page(page: str) -> Result:
    path = ROOT / page
    if not path.exists():
        return Result(page, "missing", False, 0, 0, 0, 0, 0, "file missing")
    original = path.read_text(encoding="utf-8", errors="ignore")
    before_pages = 0
    before_questions = 0
    after_pages = 0
    after_questions = 0
    removed_nodes = 0
    kept_faq = False
    out: list[str] = []
    last = 0
    notes: list[str] = []

    for m in JSONLD_RE.finditer(original):
        opener, raw, closer = m.groups()
        obj = parse_json(raw)
        if obj is None:
            continue
        p, q = count_faq(obj)
        if p == 0:
            continue
        before_pages += p
        before_questions += q
        sid = script_id(opener)
        keep = should_keep_faq(page, sid, q, kept_faq)
        out.append(original[last:m.start()])
        if keep:
            out.append(m.group(0))
            kept_faq = True
            after_pages += p
            after_questions += q
            notes.append(f"kept:{sid or 'no-id'}:{q}")
        else:
            cleaned, removed = strip_faq(obj)
            removed_nodes += removed
            if cleaned is not None and count_faq(cleaned)[0] == 0:
                out.append(opener + serialize(cleaned) + closer)
                notes.append(f"stripped-faq-preserved-nonfaq:{sid or 'no-id'}:{q}")
            else:
                notes.append(f"removed:{sid or 'no-id'}:{q}")
        last = m.end()

    if before_pages == 0:
        return Result(page, "ok", False, 0, 0, 0, 0, 0, "no FAQPage found")

    out.append(original[last:])
    updated = "".join(out)
    # Recount after from the final source, including untouched FAQ scripts if any.
    after_pages = 0
    after_questions = 0
    for _, raw, _ in JSONLD_RE.findall(updated):
        obj = parse_json(raw)
        p, q = count_faq(obj)
        after_pages += p
        after_questions += q

    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    status = "ok" if after_pages <= 1 and (after_pages == 0 or after_questions >= 8) else "fail"
    return Result(page, status, changed, before_pages, before_questions, after_pages, after_questions, removed_nodes, "; ".join(notes))


def write_report(results: list[Result]) -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    failures = [r for r in results if r.status != "ok"]
    status = "PASS" if not failures else "FAIL"
    lines = [
        "# Duplicate FAQ Schema Cleaner",
        "",
        f"Status geral: **{status}**",
        "",
        "## Objetivo",
        "Garantir no máximo um `FAQPage` por URL nas páginas críticas apontadas pelo relatório de FAQ duplicado.",
        "",
        "## Guardrails",
        "- Nós não-FAQ em JSON-LD são preservados.",
        "- Nenhum AggregateRating, Rating ou Review é inserido.",
        "- Casos especiais `es/cardapio.html` e `es/almoco.html` mantêm o bloco estático completo de 8 perguntas.",
        "",
        "## Resumo",
        f"- Páginas analisadas: **{len(results)}**",
        f"- Páginas com PASS: **{len([r for r in results if r.status == 'ok'])}**",
        f"- Páginas com falha: **{len(failures)}**",
        f"- Páginas alteradas: **{len([r for r in results if r.changed])}**",
        "",
        "## Resultados por página",
        "",
        "| Página | Status | Changed | FAQ antes | Perguntas antes | FAQ depois | Perguntas depois | FAQ removidos | Notas |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for r in results:
        lines.append(f"| `{r.page}` | {r.status} | {r.changed} | {r.faq_pages_before} | {r.faq_questions_before} | {r.faq_pages_after} | {r.faq_questions_after} | {r.removed_faq_nodes} | {r.notes} |")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Duplicate FAQ schema cleaner: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    return write_report([clean_page(page) for page in TARGETS])


if __name__ == "__main__":
    raise SystemExit(main())
