#!/usr/bin/env python3
"""Validate the restaurant/restaurants SEO cluster without changing HTML."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "restaurant_restaurants_search_cluster_2026-08-27.md"
TODAY = "2026-08-27"

PAGES = {
    "restaurante-morro-da-urca.html": {
        "intent": "restaurante na Urca / restaurante no Morro da Urca",
        "title_terms": ("Restaurante na Urca", "Morro da Urca"),
        "differentiator": "único restaurante do Parque Bondinho com vista direta para o Pão de Açúcar",
    },
    "restaurante-bondinho-pao-de-acucar.html": {
        "intent": "restaurante no/do Bondinho Pão de Açúcar",
        "title_terms": ("Restaurante no Bondinho", "Pão de Açúcar"),
        "differentiator": "único restaurante do Parque Bondinho com vista direta para o Pão de Açúcar",
    },
    "restaurantes-perto-do-pao-de-acucar.html": {
        "intent": "restaurantes na Urca / perto e no Pão de Açúcar",
        "title_terms": ("Restaurantes Perto", "Pão de Açúcar"),
        "differentiator": "único restaurante do Parque Bondinho com vista direta para o Pão de Açúcar",
    },
    "en/restaurant-at-urca-hill.html": {
        "intent": "restaurant at Urca Hill",
        "title_terms": ("Restaurant at Urca Hill",),
        "differentiator": "only restaurant in the park with a direct view of Sugarloaf Mountain",
    },
    "en/sugarloaf-cable-car-restaurant.html": {
        "intent": "Sugarloaf Cable Car restaurant",
        "title_terms": ("Sugarloaf Cable Car Restaurant",),
        "differentiator": "only restaurant in Sugarloaf Cable Car Park with a direct view of Sugarloaf Mountain",
    },
    "en/restaurants-near-sugarloaf-mountain.html": {
        "intent": "restaurants near Sugarloaf Mountain",
        "title_terms": ("Restaurants Near Sugarloaf Mountain",),
        "differentiator": "only restaurant in the park with a direct view of Sugarloaf Mountain",
    },
    "es/restaurante-morro-da-urca.html": {
        "intent": "restaurante en Urca / Morro da Urca",
        "title_terms": ("Restaurante en Urca", "Morro da Urca"),
        "differentiator": "único restaurante del parque con vista directa al Pan de Azúcar",
    },
    "es/restaurante-bondinho-pan-de-azucar.html": {
        "intent": "restaurante del Bondinho / teleférico Pan de Azúcar",
        "title_terms": ("Restaurante Teleférico Pan de Azúcar",),
        "differentiator": "único restaurante del Parque Bondinho con vista directa al Pan de Azúcar",
    },
    "es/restaurantes-cerca-del-pan-de-azucar.html": {
        "intent": "restaurantes cerca del Pan de Azúcar",
        "title_terms": ("Restaurantes Cerca del Pan de Azúcar",),
        "differentiator": "único restaurante del parque con vista directa al Pan de Azúcar",
    },
}

FORBIDDEN_TYPES = {"Review", "Rating", "AggregateRating"}
FORBIDDEN_KEYS = {
    "review",
    "aggregateRating",
    "ratingValue",
    "reviewCount",
    "ratingCount",
    "bestRating",
    "worstRating",
}


def first(pattern: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.I | re.S)
    if not match:
        return ""
    value = next((group for group in match.groups() if group is not None), "")
    return re.sub(r"\s+", " ", value).strip()


def schema_issues(node: object, path: str = "$") -> list[str]:
    issues: list[str] = []
    if isinstance(node, dict):
        node_type = node.get("@type")
        types = node_type if isinstance(node_type, list) else [node_type]
        for value in types:
            if value in FORBIDDEN_TYPES:
                issues.append(f"{path}.@type={value}")
        for key, value in node.items():
            if key in FORBIDDEN_KEYS:
                issues.append(f"{path}.{key}")
            issues.extend(schema_issues(value, f"{path}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            issues.extend(schema_issues(value, f"{path}[{index}]"))
    return issues


def main() -> int:
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    rows: list[dict[str, object]] = []
    failures: list[str] = []

    for relative, config in PAGES.items():
        path = ROOT / relative
        html = path.read_text(encoding="utf-8")
        title = first(r"<title>(.*?)</title>", html)
        description = first(
            r"<meta\s+(?:content=\"([^\"]*)\"\s+name=\"description\"|name=\"description\"\s+content=\"([^\"]*)\")\s*/?>",
            html,
        )
        if not description:
            match = re.search(
                r"<meta\s+(?:content=\"([^\"]*)\"\s+name=\"description\"|name=\"description\"\s+content=\"([^\"]*)\")\s*/?>",
                html,
                flags=re.I,
            )
            description = next((group for group in match.groups() if group), "") if match else ""
        canonicals = re.findall(r"<link[^>]+rel=\"canonical\"[^>]*>", html, flags=re.I)
        h1_count = len(re.findall(r"<h1\b", html, flags=re.I))
        title_ok = all(term.casefold() in title.casefold() for term in config["title_terms"])
        differentiator_ok = config["differentiator"].casefold() in html.casefold()
        claims_ok = not re.search(r"#1 rated|#1 choice|the best restaurant|el mejor restaurante", title + " " + description, flags=re.I)

        json_issues: list[str] = []
        for index, raw in enumerate(
            re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, flags=re.I | re.S)
        ):
            try:
                json_issues.extend(schema_issues(json.loads(raw), f"jsonld[{index}]"))
            except json.JSONDecodeError as error:
                json_issues.append(f"jsonld[{index}] parse error: {error.msg}")

        url = "https://www.embaixadacarioca.com/" + relative.replace("\\", "/")
        sitemap_block = first(rf"<url>\s*<loc>{re.escape(url)}</loc>(.*?)</url>", sitemap)
        lastmod_ok = f"<lastmod>{TODAY}</lastmod>" in sitemap_block
        passed = all(
            (
                title_ok,
                bool(description),
                len(canonicals) == 1,
                h1_count == 1,
                differentiator_ok,
                claims_ok,
                not json_issues,
                lastmod_ok,
            )
        )
        if not passed:
            failures.append(relative)
        rows.append(
            {
                "page": relative,
                "intent": config["intent"],
                "title": title,
                "canonical": len(canonicals) == 1,
                "h1": h1_count == 1,
                "differentiator": differentiator_ok,
                "safe_schema": not json_issues,
                "lastmod": lastmod_ok,
                "passed": passed,
                "json_issues": json_issues,
            }
        )

    status = "PASS" if not failures else "FAIL"
    lines = [
        "# Restaurante / Restaurantes — Search Console SEO Cluster",
        "",
        f"**Data:** {TODAY}",
        f"**Status geral:** {status}",
        "",
        "## Sinais que orientaram o lote",
        "",
        "Fonte: exportação Google Search Console, últimos 28 dias, arquivo `embaixadacarioca.com-Performance-on-Search-2026-08-11.xlsx`.",
        "",
        "| Consulta | Cliques | Impressões | CTR | Página responsável |",
        "|---|---:|---:|---:|---|",
        "| restaurante na urca | 3 | 265 | 1,13% | `restaurante-morro-da-urca.html` |",
        "| restaurante urca | 1 | 351 | 0,28% | `restaurante-morro-da-urca.html` |",
        "| restaurantes na urca | 0 | 131 | 0,00% | `restaurantes-perto-do-pao-de-acucar.html` |",
        "| restaurantes na urca com vista | 0 | 103 | 0,00% | `restaurantes-perto-do-pao-de-acucar.html` |",
        "| restaurante bondinho | 2 | 97 | 2,06% | `restaurante-bondinho-pao-de-acucar.html` |",
        "| restaurante no pão de açúcar | 6 | 229 | 2,62% | `/` (home; preservada) |",
        "",
        "## Mapa canônico de intenção",
        "",
        "- A home continua responsável pela intenção principal e de marca: **restaurante no Pão de Açúcar**.",
        "- As páginas Morro/Urca concentram as variações singulares locais.",
        "- As páginas Bondinho concentram as buscas pelo teleférico e pelo parque.",
        "- As páginas plurais funcionam como guia de escolha, sem superlativos não comprovados.",
        "",
        "## Validação página a página",
        "",
        "| Página | Intenção | Title | Canonical | 1 H1 | Diferencial | JSON-LD seguro | lastmod | Status |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        mark = lambda value: "✅" if value else "❌"
        title_cell = str(row["title"]).replace("|", "\\|")
        lines.append(
            f"| `{row['page']}` | {row['intent']} | {title_cell} | {mark(row['canonical'])} | "
            f"{mark(row['h1'])} | {mark(row['differentiator'])} | {mark(row['safe_schema'])} | "
            f"{mark(row['lastmod'])} | {mark(row['passed'])} |"
        )
        if row["json_issues"]:
            lines.append(f"| ↳ schema | `{' ; '.join(row['json_issues'])}` |  |  |  |  |  |  |  |")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Nenhuma página pode inserir `Review`, `Rating`, `AggregateRating` ou campos derivados em JSON-LD.",
            "- O diferencial factual deve ser expresso sem atacar ou nomear concorrentes.",
            "- Não criar novas páginas para essas intenções sem revisar canibalização e Search Console.",
            "- Titles e descriptions não devem usar `#1`, “melhor restaurante” ou equivalentes sem comprovação independente atual.",
            "",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"{status}: {len(rows)} pages; failures={len(failures)}")
    if failures:
        print("Failed: " + ", ".join(failures))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
