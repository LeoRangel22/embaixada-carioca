#!/usr/bin/env python3
"""Read-only release gate for the multilingual P2 visit hub."""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "planeje-sua-visita.html": {
        "lang": "pt-BR",
        "canonical": "https://www.embaixadacarioca.com/planeje-sua-visita.html",
        "faq_id": "perguntas-visita",
    },
    "en/plan-your-visit.html": {
        "lang": "en",
        "canonical": "https://www.embaixadacarioca.com/en/plan-your-visit.html",
        "faq_id": "visit-faq",
    },
    "es/planifica-tu-visita.html": {
        "lang": "es",
        "canonical": "https://www.embaixadacarioca.com/es/planifica-tu-visita.html",
        "faq_id": "preguntas-visita",
    },
}
REQUIRED_HREFLANGS = {"pt-BR", "en", "es", "x-default"}
REQUIRED_SCHEMA = {"WebPage", "Restaurant", "HowTo", "BreadcrumbList", "FAQPage"}


class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.main = 0
        self.images_without_alt = []
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        elif tag == "main":
            self.main += 1
        elif tag == "img" and not data.get("alt"):
            self.images_without_alt.append(data.get("src", "unknown"))
        elif tag == "a":
            self.links.append(data)
        if data.get("id"):
            self.ids.add(data["id"])


def schema_types(value):
    found = set()
    if isinstance(value, dict):
        kind = value.get("@type")
        if isinstance(kind, str):
            found.add(kind)
        elif isinstance(kind, list):
            found.update(kind)
        for child in value.values():
            found.update(schema_types(child))
    elif isinstance(value, list):
        for child in value:
            found.update(schema_types(child))
    return found


def fail(errors, page, message):
    errors.append(f"{page}: {message}")


def main():
    errors = []
    for rel, expected in PAGES.items():
        source = (ROOT / rel).read_text(encoding="utf-8")
        parser = AuditParser()
        parser.feed(source)
        if not re.search(fr'<html[^>]+lang="{re.escape(expected["lang"])}"', source, re.I):
            fail(errors, rel, "incorrect html lang")
        if parser.h1 != 1:
            fail(errors, rel, f"expected 1 H1, found {parser.h1}")
        if parser.main != 1:
            fail(errors, rel, f"expected 1 main, found {parser.main}")
        if parser.images_without_alt:
            fail(errors, rel, f"images missing alt: {parser.images_without_alt}")
        if expected["faq_id"] not in parser.ids:
            fail(errors, rel, "visible FAQ anchor missing")
        canonical = re.findall(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', source, re.I)
        if canonical != [expected["canonical"]]:
            fail(errors, rel, f"canonical mismatch: {canonical}")
        hreflangs = set(re.findall(r'<link[^>]+rel="alternate"[^>]+hreflang="([^"]+)"', source, re.I))
        if hreflangs != REQUIRED_HREFLANGS:
            fail(errors, rel, f"hreflang mismatch: {sorted(hreflangs)}")
        raw_schemas = re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', source, re.I | re.S)
        if len(raw_schemas) != 1:
            fail(errors, rel, f"expected 1 JSON-LD block, found {len(raw_schemas)}")
        found_types = set()
        for raw in raw_schemas:
            try:
                found_types.update(schema_types(json.loads(raw)))
            except json.JSONDecodeError as exc:
                fail(errors, rel, f"invalid JSON-LD: {exc}")
        if not REQUIRED_SCHEMA.issubset(found_types):
            fail(errors, rel, f"schema types missing: {sorted(REQUIRED_SCHEMA - found_types)}")
        for token in ("G-9GRXVZ55CB", "conversion-tracking.js", "web-vitals-tracking.js", "data-intent=", "bondinho.com.br"):
            if token not in source:
                fail(errors, rel, f"required token missing: {token}")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    for rel, expected in PAGES.items():
        if expected["canonical"] not in sitemap:
            fail(errors, "sitemap.xml", f"missing {expected['canonical']}")
        if expected["canonical"] not in llms:
            fail(errors, "llms.txt", f"missing {expected['canonical']}")
    if "/planeje-sua-visita.html" not in home:
        fail(errors, "index.html", "visit hub is not internally linked")

    if errors:
        print("P2 visit hub audit: FAIL")
        print("\n".join(f"- {item}" for item in errors))
        return 1
    print("P2 visit hub audit: PASS")
    print("3 locales; canonical/hreflang; FAQ/HowTo/Restaurant schema; GA4/CTA/CWV; sitemap/llms/internal links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
