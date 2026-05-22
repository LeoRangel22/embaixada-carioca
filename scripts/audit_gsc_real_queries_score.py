#!/usr/bin/env python3
"""Audit based on real Google Search Console organic queries from 15–21 May 2026."""
from __future__ import annotations

import csv, json, re
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_audit_reports"
MD = OUT / "gsc_real_queries_score_audit.md"
CSV = OUT / "gsc_real_queries_score_audit.csv"
JS = OUT / "gsc_real_queries_score_audit.json"
THRESHOLD = 90

# Manual extraction from GSC screenshot: last 7 days, 15–21 May 2026.
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

TARGET_REQUIREMENTS = {
    "index.html": ["embaixada carioca", "restaurante pão de açúcar", "restaurante no pão de açúcar", "restaurante bondinho", "av pasteur 520", "avaliações"],
    "restaurante-morro-da-urca.html": ["restaurante morro da urca", "restaurante no morro da urca", "restaurante urca", "restaurantes na urca", "morro da urca rio de janeiro"],
    "cafe-da-manha.html": ["cafe da manha pao de acucar", "cafe da manha na urca", "café da manhã na urca", "café da manhã pão de açúcar"],
    "como-chegar.html": ["av pasteur 520", "avenida pasteur 520", "urca rio de janeiro", "como chegar"],
}

ACC = str.maketrans({"á":"a","à":"a","ã":"a","â":"a","é":"e","ê":"e","í":"i","ó":"o","õ":"o","ô":"o","ú":"u","ç":"c"})
TAG = re.compile(r"<[^>]+>")
HIDDEN = re.compile(r"<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>", re.I|re.S)
SPACE = re.compile(r"\s+")
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I|re.S)
DESC = re.compile(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', re.I)
H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.I|re.S)


def norm(s: str) -> str:
    return s.lower().translate(ACC)

def visible(html: str) -> str:
    return SPACE.sub(" ", TAG.sub(" ", HIDDEN.sub(" ", html))).strip()

def phrase_present(needle: str, haystack: str) -> bool:
    n = norm(needle)
    h = norm(haystack)
    return n in h

@dataclass
class QueryResult:
    query: str
    cluster: str
    target: str
    clicks: int
    impressions: int
    ctr: float
    present_in_target: bool
    present_in_title: bool
    present_in_description: bool
    present_in_h1: bool
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
        return QueryResult(q["query"], q["cluster"], q["target"], q["clicks"], q["impressions"], q["ctr"], False, False, False, False, 0, "Página-alvo inexistente.")
    html = path.read_text(encoding="utf-8", errors="ignore")
    text = visible(html)
    title = TITLE.search(html)
    desc = DESC.search(html)
    h1 = H1.search(html)
    p_text = phrase_present(q["query"], text)
    p_title = phrase_present(q["query"], title.group(1) if title else "")
    p_desc = phrase_present(q["query"], desc.group(1) if desc else "")
    p_h1 = phrase_present(q["query"], h1.group(1) if h1 else "")
    score = 0
    if p_text: score += 50
    if p_title: score += 20
    if p_desc: score += 15
    if p_h1: score += 15
    rec = "OK"
    if score < 90:
        missing = []
        if not p_text: missing.append("texto visível")
        if not p_title: missing.append("title")
        if not p_desc: missing.append("meta description")
        if not p_h1: missing.append("H1")
        rec = "Reforçar consulta em: " + ", ".join(missing)
    return QueryResult(q["query"], q["cluster"], q["target"], q["clicks"], q["impressions"], q["ctr"], p_text, p_title, p_desc, p_h1, score, rec)


def audit_page(page: str, terms: list[str]) -> PageSummary:
    path = ROOT / page
    if not path.exists():
        return PageSummary(page, 0, "FAIL", 0, len(terms), terms)
    text = visible(path.read_text(encoding="utf-8", errors="ignore"))
    missing = [t for t in terms if not phrase_present(t, text)]
    covered = len(terms) - len(missing)
    score = round(100 * covered / max(1, len(terms)))
    return PageSummary(page, score, "PASS" if score >= THRESHOLD else "FAIL", covered, len(terms), missing)


def write_reports(query_results: list[QueryResult], page_results: list[PageSummary]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    min_query_score = min((r.score for r in query_results), default=0)
    min_page_score = min((r.score for r in page_results), default=0)
    status = "PASS" if min_query_score >= THRESHOLD and min_page_score >= THRESHOLD else "FAIL"
    JS.write_text(json.dumps({"status":status,"threshold":THRESHOLD,"min_score":min(min_query_score,min_page_score),"queries":QUERIES,"query_results":[asdict(r) for r in query_results],"page_results":[asdict(r) for r in page_results]}, ensure_ascii=False, indent=2), encoding="utf-8")
    with CSV.open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f, fieldnames=list(asdict(query_results[0]).keys()) if query_results else [])
        if query_results:
            w.writeheader(); [w.writerow(asdict(r)) for r in query_results]
    lines=["# GSC Real Organic Queries Score Audit","",f"Status geral: **{status}**",f"Score mínimo: **{min(min_query_score,min_page_score)}**",f"Threshold: **{THRESHOLD}**","","## Base","- Fonte: print do Search Console / Google organic search queries","- Período: 15–21 mai. 2026","- Total visível no print: 75 cliques, 1.888 impressões, CTR 3,97%","","## Páginas-alvo"]
    for p in page_results:
        lines.append(f"- `{p.page}` — {p.status} — score {p.score} — cobertos {p.covered}/{p.required}")
        if p.missing: lines.append(f"  - Faltando: {', '.join(p.missing)}")
    lines += ["", "## Consultas abaixo de 90"]
    lows=[r for r in query_results if r.score<THRESHOLD]
    if lows:
        for r in sorted(lows, key=lambda x:(x.score, -x.impressions)):
            lines.append(f"- `{r.query}` → `{r.target}` — score {r.score}, impr. {r.impressions}, cliques {r.clicks}, CTR {r.ctr}% — {r.recommendation}")
    else:
        lines.append("Nenhuma consulta abaixo de 90.")
    lines += ["", "## Todas as consultas"]
    for r in query_results:
        lines.append(f"- `{r.query}` → `{r.target}` — score {r.score} — text={r.present_in_target}, title={r.present_in_title}, desc={r.present_in_description}, h1={r.present_in_h1}")
    MD.write_text("\n".join(lines)+"\n", encoding="utf-8")


def main() -> int:
    qr=[audit_query(q) for q in QUERIES]
    pr=[audit_page(p, terms) for p,terms in TARGET_REQUIREMENTS.items()]
    write_reports(qr, pr)
    min_score = min([r.score for r in qr] + [p.score for p in pr])
    print(f"GSC real queries score audit: min_score={min_score}")
    return 0 if min_score >= THRESHOLD else 1

if __name__ == "__main__":
    raise SystemExit(main())
