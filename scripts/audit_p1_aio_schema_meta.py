#!/usr/bin/env python3
"""Audit P0 readiness and P1 AIO/SEO fixes for Embaixada Carioca.

Checks:
- P0 visual/operational runtime is present in the repository.
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


def audit_p0_runtime() -> dict[str, Any]:
    geo = ROOT / "assets" / "geo-proximity.js"
    cafe = ROOT / "cafe-da-manha.html"
    result: dict[str, Any] = {
        "name": "P0 visual/operational runtime",
        "status": "PASS",
        "checks": {},
        "warnings": [],
    }

    geo_text = geo.read_text(encoding="utf-8", errors="ignore") if geo.exists() else ""
    cafe_text = cafe.read_text(encoding="utf-8", errors="ignore") if cafe.exists() else ""

    checks = {
        "geo_proximity_exists": geo.exists(),
        "cafe_page_exists": cafe.exists(),
        "cafe_loads_geo_proximity": "geo-proximity.js" in cafe_text,
        "has_ecCafeCardapioContrast": "ecCafeCardapioContrast" in geo_text,
        "has_ecBondinhoCopyFix": "ecBondinhoCopyFix" in geo_text,
        "has_background_aware_strategy": "runtime-background-aware-via-geo-proximity" in geo_text,
        "has_dark_card_detection": "getComputedStyle" in geo_text and "darkCards" in geo_text,
    }
    result["checks"] = checks
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        result["status"] = "FAIL"
        result["warnings"].extend(failed)
    return result


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
                            if item == "AggregateRating":
                                forbidden.add("AggregateRating")
            if key == "mainEntity" and isinstance(value, list) and obj.get("@type") == "FAQPage":
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

    source = path.read_text(encoding="utf-8", errors="ignore")
    meta = META_RE.search(source)
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
    for raw in SCRIPT_RE.findall(source):
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

    fails: list[str] = []
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
    p0 = audit_p0_runtime()
    rows = [audit_page(page) for page in pages]
    failures = [row for row in rows if row["status"] == "FAIL"]
    status = "PASS" if p0["status"] == "PASS" and not failures else "FAIL"

    REPORT_JSON.write_text(json.dumps({
        "status": status,
        "p0": p0,
        "results": rows,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# P0 + P1 AIO Schema + Meta Audit",
        "",
        f"Status geral: **{status}**",
        "",
        "## Critérios",
        "- P0 runtime de contraste/copy presente no repositório e carregado pelo `cafe-da-manha.html`.",
        "- Homes PT/EN/ES com FAQPage e pelo menos 8 perguntas.",
        "- Páginas críticas existentes com Restaurant ou FoodEstablishment schema.",
        "- Meta description presente nas páginas prioritárias.",
        "- Proibido usar aggregateRating/ratingValue/reviewCount/ratingCount/bestRating/worstRating no JSON-LD.",
        "",
        "## P0 visual/operacional",
        f"- Status: **{p0['status']}**",
    ]
    for check, passed in p0["checks"].items():
        lines.append(f"  - {check}: {passed}")
    if p0["warnings"]:
        lines.append("  - Pendências: " + ", ".join(p0["warnings"]))

    lines.extend(["", "## P1 FAQ Schema, Restaurant Schema e Meta descriptions"])
    for row in rows:
        lines.append(f"- `{row['page']}` — {row['status']} — meta {row['meta_length']} chars — Restaurant={row['has_restaurant']} — FAQ={row['has_faq']} ({row['faq_questions']})")
        for warning in row.get("warnings", []):
            lines.append(f"  - {warning}")
        if row.get("forbidden"):
            lines.append("  - forbidden: " + ", ".join(row["forbidden"]))

    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"P0 + P1 AIO schema/meta audit: {status}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
