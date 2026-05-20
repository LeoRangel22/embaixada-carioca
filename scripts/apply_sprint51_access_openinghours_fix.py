#!/usr/bin/env python3
"""
Sprint 5.1 — Access Pages OpeningHours Fix | Embaixada Carioca

Corrige a última ressalva do Excellence Gate: as páginas Como Chegar PT/EN/ES
já tinham Restaurant schema, mas não traziam openingHours/openingHoursSpecification.
Como o gate do Sprint 1 exige openingHours nas páginas principais, este script injeta
um schema complementar idempotente nas três páginas de acesso.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
MARK_START = "<!-- EC Sprint 5.1 Access OpeningHours Schema -->"
MARK_END = "<!-- /EC Sprint 5.1 Access OpeningHours Schema -->"
MARK_RE = re.compile(r"\n*<!-- EC Sprint 5\.1 Access OpeningHours Schema -->[\s\S]*?<!-- /EC Sprint 5\.1 Access OpeningHours Schema -->\s*", re.I)
HEAD_CLOSE_RE = re.compile(r"</head>", re.I)

PAGES = {
    "como-chegar.html": "pt-BR",
    "en/how-to-get-there.html": "en",
    "es/como-llegar.html": "es",
}

BASE = "https://www.embaixadacarioca.com"

COUNTERS = {"pages_checked": 0, "pages_updated": 0, "schema_injected": 0, "warnings": 0}
ACTIONS: list[str] = []
WARNINGS: list[str] = []


def schema(rel: str, lang: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Restaurant",
                "@id": f"{BASE}/#restaurant",
                "name": "Embaixada Carioca",
                "url": BASE + "/",
                "telephone": "+55 21 96683-7556",
                "acceptsReservations": True,
                "hasMenu": f"{BASE}/cardapio.html",
                "openingHours": ["Mo-Su 08:30-21:00"],
                "openingHoursSpecification": [
                    {
                        "@type": "OpeningHoursSpecification",
                        "dayOfWeek": [
                            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
                        ],
                        "opens": "08:30",
                        "closes": "21:00",
                    }
                ],
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "Av. Pasteur, 520 — Morro da Urca",
                    "addressLocality": "Rio de Janeiro",
                    "addressRegion": "RJ",
                    "addressCountry": "BR",
                },
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": -22.9508333,
                    "longitude": -43.1641667,
                },
            },
            {
                "@type": "WebPage",
                "@id": f"{BASE}/{rel}#webpage",
                "url": BASE + "/" + rel,
                "inLanguage": lang,
                "isPartOf": {"@id": f"{BASE}/#website"},
            },
        ],
    }
    return f"{MARK_START}\n<script type=\"application/ld+json\">{json.dumps(data, ensure_ascii=False, separators=(',', ':'))}</script>\n{MARK_END}"


def process(rel: str, lang: str) -> None:
    path = ROOT / rel
    COUNTERS["pages_checked"] += 1
    if not path.exists():
        COUNTERS["warnings"] += 1
        WARNINGS.append(f"Página ausente: {rel}")
        return
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = MARK_RE.sub("\n", original)
    if HEAD_CLOSE_RE.search(text):
        text = HEAD_CLOSE_RE.sub(schema(rel, lang) + "\n</head>", text, count=1)
    else:
        COUNTERS["warnings"] += 1
        WARNINGS.append(f"Sem </head>: {rel}")
        return
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["pages_updated"] += 1
        COUNTERS["schema_injected"] += 1
        ACTIONS.append(f"OPENING_HOURS_SCHEMA: {rel}")


def write_report() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    out = REPORT_DIR / "sprint51_access_openinghours_fix_report.md"
    lines = [
        "# Sprint 5.1 — Access OpeningHours Fix",
        "",
        "## Objetivo",
        "Adicionar openingHours/openingHoursSpecification às páginas Como Chegar PT/EN/ES para remover a última ressalva do Sprint 1 no Excellence Gate.",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Ações"])
    lines.extend(f"- {a}" for a in ACTIONS) if ACTIONS else lines.append("- Nenhuma ação necessária.")
    lines.extend(["", "## Warnings"])
    lines.extend(f"- {w}" for w in WARNINGS) if WARNINGS else lines.append("- Nenhum warning.")
    lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


def main() -> int:
    for rel, lang in PAGES.items():
        process(rel, lang)
    write_report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
