#!/usr/bin/env python3
"""Extend static Restaurant + FAQ schema coverage to all product language variants.

This complements apply_static_product_schema_faq.py by covering product URLs that were
not part of the first priority batch, especially EN/ES variants for feijoada,
breakfast, sunset/events and duplicate language aliases.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any
import html
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import apply_static_product_schema_faq as base  # noqa: E402

REPORT_MD = ROOT / "_audit_reports" / "static_schema_product_full_coverage_report.md"
SITE = base.SITE
JSONLD_RE = base.JSONLD_RE

PAGES: dict[str, dict[str, Any]] = {
    "en/eventos.html": {"lang": "en", "topic": "events at Morro da Urca", "restaurant": True, "faq": True, "url": SITE + "/en/eventos.html"},
    "es/eventos.html": {"lang": "es", "topic": "eventos en Morro da Urca", "restaurant": True, "faq": True, "url": SITE + "/es/eventos.html"},
    "en/entardecer.html": {"lang": "en", "topic": "sunset at Morro da Urca", "restaurant": True, "faq": True, "url": SITE + "/en/entardecer.html"},
    "es/entardecer.html": {"lang": "es", "topic": "atardecer en Morro da Urca", "restaurant": True, "faq": True, "url": SITE + "/es/entardecer.html"},
    "en/feijoada.html": {"lang": "en", "topic": "Brazilian feijoada at Morro da Urca", "restaurant": True, "faq": True, "url": SITE + "/en/feijoada.html"},
    "es/feijoada.html": {"lang": "es", "topic": "feijoada brasileña en Morro da Urca", "restaurant": True, "faq": True, "url": SITE + "/es/feijoada.html"},
    "en/cafe-da-manha.html": {"lang": "en", "topic": "breakfast at Morro da Urca", "restaurant": True, "faq": True, "url": SITE + "/en/cafe-da-manha.html"},
    "es/cafe-da-manha.html": {"lang": "es", "topic": "desayuno en Morro da Urca", "restaurant": True, "faq": True, "url": SITE + "/es/cafe-da-manha.html"},
}


def has_type(value: Any, schema_type: str) -> bool:
    if isinstance(value, str):
        return value == schema_type
    if isinstance(value, list):
        return any(str(item) == schema_type for item in value)
    return False


def remove_schema_type(obj: Any, schema_type: str) -> Any:
    if isinstance(obj, dict):
        if has_type(obj.get("@type"), schema_type):
            return None
        cleaned: dict[str, Any] = {}
        for key, value in obj.items():
            next_value = remove_schema_type(value, schema_type)
            if next_value is None:
                continue
            if isinstance(next_value, list) and not next_value:
                continue
            cleaned[key] = next_value
        return cleaned
    if isinstance(obj, list):
        return [item for item in (remove_schema_type(item, schema_type) for item in obj) if item is not None]
    return obj


def remove_existing_faqpage(source: str) -> str:
    def repl(match: re.Match[str]) -> str:
        opener, raw, closer = match.groups()
        try:
            obj = json.loads(html.unescape(raw.strip()))
        except Exception:
            return match.group(0)
        cleaned = remove_schema_type(obj, "FAQPage")
        if cleaned is None or cleaned == [] or cleaned == {}:
            return ""
        return opener + json.dumps(cleaned, ensure_ascii=False, separators=(",", ":")) + closer
    return JSONLD_RE.sub(repl, source)


def count_faq_pages(source: str) -> int:
    count = 0
    for _, raw, _ in JSONLD_RE.findall(source):
        try:
            obj = json.loads(html.unescape(raw.strip()))
        except Exception:
            continue
        types: list[str] = []
        base.walk_schema(obj, types, [])
        count += sum(1 for item in types if item == "FAQPage")
    return count


def apply_page(rel: str, cfg: dict[str, Any]) -> tuple[str, str, bool, list[str]]:
    path = ROOT / rel
    if not path.exists():
        return rel, "SKIP", False, ["file missing"]
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated = base.strip_old_block(original)
    updated = base.sanitize_jsonld(updated)
    updated = remove_existing_faqpage(updated)
    updated = base.insert_block(updated, base.schema_block(cfg))
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")

    restaurant_found, faq_found, faq_questions, forbidden = base.audit_html(updated)
    faq_count = count_faq_pages(updated)
    warnings: list[str] = []
    if cfg.get("restaurant") and not restaurant_found:
        warnings.append("Restaurant schema missing")
    if cfg.get("faq") and (not faq_found or faq_questions < 8):
        warnings.append("FAQPage missing or below 8 questions")
    if cfg.get("faq") and faq_count != 1:
        warnings.append(f"FAQPage count must be 1, found {faq_count}")
    if forbidden:
        warnings.append("forbidden rating/review schema terms found")
    return rel, ("PASS" if not warnings else "FAIL"), changed, warnings


def main() -> int:
    REPORT_MD.parent.mkdir(exist_ok=True)
    rows = [apply_page(rel, cfg) for rel, cfg in PAGES.items()]
    status = "PASS" if all(row[1] in {"PASS", "SKIP"} for row in rows) else "FAIL"
    lines = [
        "# Static Schema Product Full Coverage",
        "",
        f"Status geral: **{status}**",
        "",
        "## Escopo",
        "Complemento de Restaurant Schema + FAQPage para variantes de produto PT/EN/ES que não estavam no primeiro lote.",
        "",
        "## Resultados",
    ]
    for rel, row_status, changed, warnings in rows:
        lines.append(f"- `{rel}` — **{row_status}** — changed={changed}")
        for warning in warnings:
            lines.append(f"  - {warning}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Static schema product full coverage: {status}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
