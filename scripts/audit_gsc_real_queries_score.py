#!/usr/bin/env python3
"""GSC real organic queries audit — intent-cluster scoring version."""
from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_audit_reports"
MD = OUT / "gsc_real_queries_score_audit.md"
CSV = OUT / "gsc_real_queries_score_audit.csv"
JS = OUT / "gsc_real_queries_score_audit.json"
THRESHOLD = 90

QUERIES = [
    {"query":"embaixada carioca", "clicks":45, "impressions":293, "ctr":15.36, "cluster":"brand", "target":"index.html"},
    {"query":"avaliações sobre embaixada carioca", "clicks":0, "impressions":112, "ctr":0.00, "cluster":"reviews", "target":"index.html"},
    {"query":"morro da urca", "clicks":0, "impressions":88, "ctr":0.00, "cluster":"geo", "target":"restaurante-morro-da-urca.html"},
    {"query":"restaurante urca", "clicks":0, "impressions":62, "ctr":0.00, "cluster":"restaurant_urca", "target":"restaurante-morro-da-urca.html"},
    {"query":"restaurante pão de açucar", "clicks":1, "impressions":49, "ctr":2.04, "cluster":"pao_de_acucar", "target":"index.html"},
    {"query":"restaurante morro da urca", "clicks":1, "impressions":45, "ctr":2.22, "cluster":"morro_da_urca_restaurant", "target":"restaurante-morro-da-urca.html"},
    {"query":"restaurante na urca", "clicks":0, "impressions":39, "ctr":0.00, "cluster":"restaurant_urca", "target":"restaurante-morro-da-urca.html"},
    {"query":"restaurante no pão de açúcar", "clicks":0, "impressions":34, "ctr":0.00, "cluster":"pao_de_acucar", "target":"index.html"},
    {"query":"embaixada", "clicks":2, "impressions":30, "ctr":6.67, "cluster":"brand", "target":"index.html"},
    {"query":"restaurante no morro da urca", "clicks":4, "impressions":25, "ctr":16.00, "cluster":"morro_da_urca_restaurant", "target":"restaurante-morro-da-urca.html"},
    {"query":"restaurantes urca", "clicks":0, "impressions":25, "ctr":0.00, "cluster":"restaurant_urca", "target":"restaurante-morro-da-urca.html"},
    {"query":"av pasteur 520 - urca rio de janeiro", "clicks":0, "impressions":22, "ctr":0.00, "cluster":"address", "target":"como-chegar.html"},
    {"query":"restaurante pao de acucar", "clicks":1, "impressions":21, "ctr":4.76, "cluster":"pao_de_acucar", "target":"index.html"},
    {"query":"cafe da manha pao de acucar", "clicks":1, "impressions":19, "ctr":5.26, "cluster":"breakfast", "target":"cafe-da-manha.html"},
    {"query":"avenida pasteur 520", "clicks":0, "impressions":17, "ctr":0.00, "cluster":"address", "target":"como-chegar.html"},
    {"query":"cafe da manha na urca", "clicks":0, "impressions":17, "ctr":0.00, "cluster":"breakfast", "target":"cafe-da-manha.html"},
    {"query":"restaurantes na urca", "clicks":1, "impressions":17, "ctr":5.88, "cluster":"restaurant_urca", "target":"restaurante-morro-da-urca.html"},
    {"query":"morro da urca rio de janeiro", "clicks":0, "impressions":16, "ctr":0.00, "cluster":"geo", "target":"restaurante-morro-da-urca.html"},
    {"query":"restaurante no pao de açucar rj", "clicks":1, "impressions":16, "ctr":6.25, "cluster":"pao_de_acucar", "target":"index.html"},
    {"query":"café da manhã na urca", "clicks":0, "impressions":15, "ctr":0.00, "cluster":"breakfast", "target":"cafe-da-manha.html"},
    {"query":"restaurante bondinho", "clicks":1, "impressions":15, "ctr":6.67, "cluster":"bondinho", "target":"index.html"},
]

CLUSTER_TERMS = {
    "brand": ["embaixada", "carioca"],
    "reviews": ["avaliacoes", "avaliacao", "google", "estrelas", "visitantes", "premios", "bem-avaliado"],
    "geo": ["morro da urca", "urca", "rio de janeiro", "pao de acucar"],
    "restaurant_urca": ["restaurante", "restaurantes", "urca", "morro da urca"],
    "pao_de_acucar": ["restaurante", "pao de acucar", "bondinho", "morro da urca"],
    "morro_da_urca_restaurant": ["restaurante", "morro da urca", "pao de acucar"],
    "address": ["av pasteur", "av. pasteur", "avenida pasteur", "520", "urca", "rio de janeiro", "como chegar"],
    "breakfast": ["cafe da manha", "urca", "pao de acucar", "morro da urca"],
    "bondinho": ["restaurante", "bondinho", "pao de acucar", "morro da urca"],
}

PAGE_REQUIREMENTS = {
    "index.html": ["embaixada carioca", "restaurante", "pao de acucar", "bondinho", "morro da urca", "av pasteur", "avaliacoes"],
    "restaurante-morro-da-urca.html": ["restaurante", "morro da urca", "urca", "pao de acucar", "rio de janeiro"],
    "cafe-da-manha.html": ["cafe da manha", "urca", "pao de acucar", "morro da urca"],
    "como-chegar.html": ["av pasteur", "520", "urca", "rio de janeiro", "como chegar"],
}

ACC = str.maketrans({"á":"a","à":"a","ã":"a","â":"a","é":"e","ê":"e","í":"i","ó":"o","õ":"o","ô":"o","ú":"u","ç":"c"})
TAG = re.compile(r"<[^>]+>")
HIDDEN = re.compile(r"<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>", re.I|re.S)
SPACE = re.compile(r"\s+")
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I|re.S)
DESC = re.compile(r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"']([^\"']+)[\"']", re.I)
DESC_ALT = re.compile(r"<meta[^>]+content=[\"']([^\"']+)[\"'][^>]*name=[\"']description[\"']", re.I)
H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.I|re.S)


def norm(s: str) -> str:
    return SPACE.sub(" ", s.lower().translate(ACC)).strip()


def visible(html: str) -> str:
    return norm(TAG.sub(" ", HIDDEN.sub(" ", html)))


def strip(s: str) -> str:
    return norm(TAG.sub(" ", s))


def has(term: str, text: str) -> bool:
    return norm(term) in text


def term_hit_score(terms: list[str], text: str) -> tuple[int, list[str], list[str]]:
    present = [t for t in terms if has(t, text)]
    missing = [t for t in terms if not has(t, text)]
    return round(100 * len(present) / max(1, len(terms))), present, missing


@dataclass
class QueryResult:
    query: str
    cluster: str
    target: str
    clicks: int
    impressions: int
    ctr: float
    exact_query_in_text: bool
    cluster_score: int
    title_score: int
    description_score: int
    h1_score: int
    score: int
    recommendation: str


@dataclass
class PageSummary:
    page: str
    score: int
    status: str
    covered: int
    required: int
    missing: list[str]


def audit_query(q: dict) -> QueryResult:
    path = ROOT / q["target"]
    if not path.exists():
        return QueryResult(q["query"], q["cluster"], q["target"], q["clicks"], q["impressions"], q["ctr"], False, 0, 0, 0, 0, 0, "Página-alvo inexistente.")

    html = path.read_text(encoding="utf-8", errors="ignore")
    text = visible(html)
    title = strip(TITLE.search(html).group(1)) if TITLE.search(html) else ""
    _desc_m = DESC.search(html) or DESC_ALT.search(html)
    desc = norm(_desc_m.group(1)) if _desc_m else ""
    h1 = strip(H1.search(html).group(1)) if H1.search(html) else ""

    cluster_terms = CLUSTER_TERMS[q["cluster"]]
    cluster_score, present, missing = term_hit_score(cluster_terms, text)
    exact = has(q["query"], text)

    # Title/description/H1 are scored by cluster intent, not by exact long-tail repetition.
    title_score = 100 if any(has(t, title) for t in cluster_terms[:3]) else 70 if any(has(t, title) for t in cluster_terms) else 0
    description_score = 100 if any(has(t, desc) for t in cluster_terms[:3]) else 70 if any(has(t, desc) for t in cluster_terms) else 0
    h1_score = 100 if any(has(t, h1) for t in cluster_terms[:3]) else 70 if any(has(t, h1) for t in cluster_terms) else 0

    score = round(cluster_score * 0.55 + title_score * 0.15 + description_score * 0.15 + h1_score * 0.10 + (100 if exact else 80) * 0.05)
    recommendation = "OK"
    if score < THRESHOLD:
        recommendation = "Reforçar cluster na página: " + ", ".join(missing[:5])
    return QueryResult(q["query"], q["cluster"], q["target"], q["clicks"], q["impressions"], q["ctr"], exact, cluster_score, title_score, description_score, h1_score, score, recommendation)


def audit_page(page: str, terms: list[str]) -> PageSummary:
    path = ROOT / page
    if not path.exists():
        return PageSummary(page, 0, "FAIL", 0, len(terms), terms)
    text = visible(path.read_text(encoding="utf-8", errors="ignore"))
    score, present, missing = term_hit_score(terms, text)
    return PageSummary(page, score, "PASS" if score >= THRESHOLD else "FAIL", len(present), len(terms), missing)


def write_reports(query_results: list[QueryResult], page_results: list[PageSummary]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    min_query_score = min((r.score for r in query_results), default=0)
    min_page_score = min((r.score for r in page_results), default=0)
    min_score = min(min_query_score, min_page_score)
    status = "PASS" if min_score >= THRESHOLD else "FAIL"

    JS.write_text(json.dumps({
        "status": status,
        "threshold": THRESHOLD,
        "min_score": min_score,
        "queries": QUERIES,
        "query_results": [asdict(r) for r in query_results],
        "page_results": [asdict(r) for r in page_results],
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    with CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(query_results[0]).keys()) if query_results else [])
        if query_results:
            writer.writeheader()
            for r in query_results:
                writer.writerow(asdict(r))

    lines = [
        "# GSC Real Organic Queries Score Audit",
        "",
        f"Status geral: **{status}**",
        f"Score mínimo: **{min_score}**",
        f"Threshold: **{THRESHOLD}**",
        "",
        "## Base",
        "- Fonte: print do Search Console / Google organic search queries",
        "- Período: 15–21 mai. 2026",
        "- Total visível no print: 75 cliques, 1.888 impressões, CTR 3,97%",
        "",
        "## Critério de score",
        "- 55% cobertura do cluster de intenção no texto visível",
        "- 15% title alinhado à intenção",
        "- 15% meta description alinhada à intenção",
        "- 10% H1 alinhado à intenção",
        "- 5% presença exata ou semântica da consulta",
        "",
        "## Páginas-alvo",
    ]
    for p in page_results:
        lines.append(f"- `{p.page}` — {p.status} — score {p.score} — cobertos {p.covered}/{p.required}")
        if p.missing:
            lines.append(f"  - Faltando: {', '.join(p.missing)}")
    lines += ["", "## Consultas abaixo de 90"]
    lows = [r for r in query_results if r.score < THRESHOLD]
    if lows:
        for r in sorted(lows, key=lambda x: (x.score, -x.impressions)):
            lines.append(f"- `{r.query}` → `{r.target}` — score {r.score}, cluster {r.cluster}, impr. {r.impressions}, cliques {r.clicks}, CTR {r.ctr}% — {r.recommendation}")
    else:
        lines.append("Nenhuma consulta abaixo de 90.")
    lines += ["", "## Todas as consultas"]
    for r in query_results:
        lines.append(f"- `{r.query}` → `{r.target}` — score {r.score} — cluster={r.cluster_score}, title={r.title_score}, desc={r.description_score}, h1={r.h1_score}, exact={r.exact_query_in_text}")
    MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    query_results = [audit_query(q) for q in QUERIES]
    page_results = [audit_page(p, terms) for p, terms in PAGE_REQUIREMENTS.items()]
    write_reports(query_results, page_results)
    min_score = min([r.score for r in query_results] + [p.score for p in page_results])
    print(f"GSC real queries score audit: min_score={min_score}")
    return 0 if min_score >= THRESHOLD else 1


if __name__ == "__main__":
    raise SystemExit(main())
