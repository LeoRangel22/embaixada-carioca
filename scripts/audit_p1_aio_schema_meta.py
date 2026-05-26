#!/usr/bin/env python3
"""Audit P1 AIO/SEO fixes for Embaixada Carioca.

Checks:
- FAQPage schema with at least 8 questions on PT/EN/ES home pages.
- Restaurant schema on critical pages when the page exists.
- Meta description present and within a practical SEO range.
- No rating/review fields in JSON-LD.
"""
from __future__ import annotations

from pathlib import Path
import json
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_audit_reports"
REPORT_MD = OUT / "p1_aio_schema_meta_audit.md"
REPORT_JSON = OUT / "p1_aio_schema_meta_audit.json"

HOME_PAGES = ["index.html", "en/index.html", "es/index.html"]
CRITICAL_PAGES = [
    "index.html", "en/index.html", "es/index.html",
    "eventos.html", "cardapio.html", "almoco.html", "cafe-da-manha.html", "entardecer.html",
    "en/eventos.html", "en/almoco.html", "en/cafe-da-manha.html", "en/sunset.html",
    "es/eventos.html", "es/almoco.html", "es/cafe-da-manha.html", "es/atardecer.html",
]
FORBIDDEN = {"aggregateRating", "ratingValue", "reviewCount", "ratingCount", "bestRating", "worstRating"}
SCRIPT_RE = re.compile(r'<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
META_RE = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']\s*/?>', re.I)


def walk(obj: Any, types: set[str], forbidden: set[str], faq_questions: list[int]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in FORBIDDEN:
                forbidden.add(key)
            if key == "@type":
                if isinstance(value, str):
                    types.add(value)
                    if value == "AggregateRating":
                        forbidden.add("AggregateRating")
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str):
                            types.add(item)
            if key == "mainEntity" and isinstance(value, list):
                if obj.get("@type") == "FAQPage":
                    faq_questions.append(len(value))
            walk(value, types, forbidden, faq_questions)
    elif isinstance(obj, list):
        for item in obj:
            walk(item, types, forbidden, faq_questions)


def audit_page(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    result: dict[str, Any] = {
        "page": rel,
        "exists": path.exists(),
        "meta_description": None,
        "meta_length": 0,
        "meta_ok": False,
        "types": [],
        "has_restaurant": False,
        "has_faq": False,
        "faq_questions": 0,
        "faq_ok": True,
        "forbidden": [],
        "json_valid_blocks": 0,
        "status": "PASS",
        "warnings": [],
    }
    if not path.exists():
        result["status"] = "SKIP"
        result["warnings"].append("file missing")
        return result

    html = path.read_text(encoding="utf-8", errors="ignore")
    meta = META_RE.search(html)
    if meta:
        desc = meta.group(1).strip()
        result["meta_description"] = desc
        result["meta_length"] = len(desc)
        result["meta_ok"] = 70 <= len(desc) <= 170
    else:
        result["warnings"].append("missing meta description")

    types: set[str] = set()
    forbidden: set[str] = set()
    faq_counts: list[int] = []
    for raw in SCRIPT_RE.findall(html):
        try:
            obj = json.loads(raw.strip())
            result["json_valid_blocks"] += 1
            walk(obj, types, forbidden, faq_counts)
        except Exception:
            result["warnings"].append("invalid JSON-LD block")

    result["types"] = sorted(types)
    result["has_restaurant"] = "Restaurant" in types or "FoodEstablishment" in types
    result["has_faq"] = "FAQPage" in types
    result["faq_questions"] = max(faq_counts or [0])
    result["forbidden"] = sorted(forbidden)

    fails = []
    if rel in HOME_PAGES:
        result["faq_ok"] = result["has_faq"] and result["faq_questions"] >= 8
        if not result["faq_ok"]:
            fails.append("home FAQPage missing or below 8 questions")
    if rel in CRITICAL_PAGES and path.exists():
        if not result["has_restaurant"]:
            fails.append("Restaurant schema missing")
    if forbidden:
        fails.append("forbidden rating/review fields in JSON-LD")
    if not meta:
        fails.append("meta description missing")
    if meta and not result["meta_ok"]:
        result["warnings"].append("meta description outside 70-170 characters")

    if fails:
        result["status"] = "FAIL"
        result["warnings"].extend(fails)
    return result


def main() -> int:
    OUT.mkdir(exist_ok=True)
    pages = list(dict.fromkeys(HOME_PAGES + CRITICAL_PAGES))
    rows = [audit_page(page) for page in pages]
    failures = [r for r in rows if r["status"] == "FAIL"]
    status = "PASS" if not failures else "FAIL"

    REPORT_JSON.write_text(json.dumps({"status": status, "results": rows}, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# P1 AIO Schema + Meta Audit",
        "",
        f"Status geral: **{status}**",
        "",
        "## Critérios",
        "- Homes PT/EN/ES com FAQPage e pelo menos 8 perguntas.",
        "- Páginas críticas existentes com Restaurant ou FoodEstablishment schema.",
        "- Meta description presente nas páginas prioritárias.",
        "- Proibido usar aggregateRating/ratingValue/reviewCount/ratingCount/bestRating/worstRating no JSON-LD.",
        "",
        "## Resultados",
    ]
    for r in rows:
        lines.append(f"- `{r['page']}` — {r['status']} — meta {r['meta_length']} chars — Restaurant={r['has_restaurant']} — FAQ={r['has_faq']} ({r['faq_questions']})")
        for warning in r.get("warnings", []):
            lines.append(f"  - {warning}")
        if r.get("forbidden"):
            lines.append("  - forbidden: " + ", ".join(r["forbidden"]))
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"P1 AIO schema/meta audit: {status}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
