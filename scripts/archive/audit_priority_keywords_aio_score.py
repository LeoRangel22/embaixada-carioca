#!/usr/bin/env python3
"""Priority Keywords AIO Score Audit — syntax-safe version."""
from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "priority_keywords_aio_score_audit.md"
REPORT_CSV = REPORT_DIR / "priority_keywords_aio_score_audit.csv"
REPORT_JSON = REPORT_DIR / "priority_keywords_aio_score_audit.json"
THRESHOLD = 90

PRIORITY_KEYWORDS = [
    "restaurante pão de açúcar",
    "restaurante morro da urca",
    "restaurante no pão de açúcar",
    "av pasteur 520 urca rio de janeiro",
    "restaurante pao de acucar",
    "restaurante no morro da urca",
    "cafe da manha na urca",
    "restaurante no pao de acucar rj",
]

TARGETS = {
    "index.html": {
        "keywords": ["restaurante pão de açúcar", "restaurante pao de acucar", "restaurante no pão de açúcar", "restaurante no pao de acucar rj", "av pasteur 520 urca rio de janeiro"],
        "min_words": 3500,
        "min_faq": 8,
        "requires_ol": True,
        "requires_video": False,
        "requires_awards": True,
        "requires_restaurant_schema": True,
        "requires_single_aggregate_rating": True,
        "notes": "Home deve ser fonte completa para IA, com FAQs estruturadas, listas e schema canônico.",
    },
    "restaurante-morro-da-urca.html": {
        "keywords": ["restaurante morro da urca", "restaurante no morro da urca", "restaurante pão de açúcar", "restaurante no pão de açúcar"],
        "min_words": 1200,
        "min_faq": 8,
        "requires_ol": True,
        "requires_video": True,
        "requires_awards": True,
        "requires_restaurant_schema": True,
        "requires_single_aggregate_rating": False,
        "notes": "Página de captação deve expandir conteúdo, E-E-A-T e FAQ para competir com agregadores.",
    },
    "cafe-da-manha.html": {
        "keywords": ["cafe da manha na urca", "café da manhã na urca", "café da manhã pão de açúcar", "cafe da manha pao de acucar"],
        "min_words": 2000,
        "min_faq": 8,
        "requires_ol": True,
        "requires_video": True,
        "requires_awards": False,
        "requires_restaurant_schema": True,
        "requires_single_aggregate_rating": False,
        "notes": "Página de produto deve ter passo a passo em OL e VideoObject para chegar a 90+.",
    },
}

AWARD_TERMS = ["Veja Rio", "Prazeres da Mesa", "melhor chope", "Heineken", "feijoada premiada", "caipirinha", "Magnífica", "picanha"]

SCRIPT_RE = re.compile(r"<script[^>]+type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")
HIDDEN_RE = re.compile(r"<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>", re.I | re.S)
QUESTION_ITEM_RE = re.compile(r"itemtype=[\"']https://schema\.org/Question[\"']", re.I)
FAQ_ITEM_RE = re.compile(r"class=[\"'][^\"']*faq-item", re.I)
FAQ_QUESTION_RE = re.compile(r"class=[\"'][^\"']*faq-question", re.I)

ACCENT_MAP = str.maketrans({
    "á": "a", "à": "a", "ã": "a", "â": "a", "ä": "a",
    "é": "e", "ê": "e", "è": "e", "ë": "e",
    "í": "i", "ì": "i", "î": "i", "ï": "i",
    "ó": "o", "ò": "o", "õ": "o", "ô": "o", "ö": "o",
    "ú": "u", "ù": "u", "û": "u", "ü": "u",
    "ç": "c",
})


def normalize(text: str) -> str:
    return text.lower().translate(ACCENT_MAP)


def visible_text(html: str) -> str:
    cleaned = HIDDEN_RE.sub(" ", html)
    cleaned = TAG_RE.sub(" ", cleaned)
    return SPACE_RE.sub(" ", cleaned).strip()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\wÀ-ÿ]{2,}\b", text))


def load_json_ld(html: str) -> list[Any]:
    blocks: list[Any] = []
    for raw in SCRIPT_RE.findall(html):
        try:
            blocks.append(json.loads(raw.strip()))
        except Exception:
            blocks.append({"__parse_error__": raw[:200]})
    return blocks


def walk_json(value: Any):
    if isinstance(value, dict):
        yield value
        for v in value.values():
            yield from walk_json(v)
    elif isinstance(value, list):
        for item in value:
            yield from walk_json(item)


def node_types(blocks: list[Any]) -> list[str]:
    out: list[str] = []
    for block in blocks:
        for node in walk_json(block):
            if not isinstance(node, dict):
                continue
            t = node.get("@type")
            if isinstance(t, str):
                out.append(t)
            elif isinstance(t, list):
                out.extend(str(x) for x in t)
    return out


def faq_count(html: str, blocks: list[Any]) -> int:
    counts: list[int] = [len(QUESTION_ITEM_RE.findall(html)), len(FAQ_ITEM_RE.findall(html)), len(FAQ_QUESTION_RE.findall(html))]
    for block in blocks:
        for node in walk_json(block):
            if isinstance(node, dict) and node.get("@type") == "FAQPage" and isinstance(node.get("mainEntity"), list):
                counts.append(len(node["mainEntity"]))
    return max(counts) if counts else 0


def aggregate_rating_count(blocks: list[Any]) -> int:
    return sum(1 for block in blocks for node in walk_json(block) if isinstance(node, dict) and "aggregateRating" in node)


def has_restaurant_schema(types: list[str]) -> bool:
    return any(t in {"Restaurant", "FoodEstablishment", "LocalBusiness"} for t in types)


def has_video_schema(types: list[str]) -> bool:
    return "VideoObject" in types


def has_ordered_list(html: str) -> bool:
    return bool(re.search(r"<ol\b", html, re.I))


def coverage(text_norm: str, terms: list[str]) -> tuple[list[str], list[str]]:
    present, missing = [], []
    for term in terms:
        (present if normalize(term) in text_norm else missing).append(term)
    return present, missing


@dataclass
class PageAudit:
    page: str
    exists: bool
    score: int
    status: str
    word_count: int
    faq_count: int
    keyword_present: list[str]
    keyword_missing: list[str]
    award_present: list[str]
    award_missing: list[str]
    has_ol: bool
    has_restaurant_schema: bool
    has_video_schema: bool
    aggregate_rating_count: int
    findings: list[str]


def audit_page(page: str, cfg: dict[str, Any]) -> PageAudit:
    path = ROOT / page
    if not path.exists():
        return PageAudit(page, False, 0, "FAIL", 0, 0, [], cfg["keywords"], [], AWARD_TERMS, False, False, False, 0, ["Página-alvo não encontrada."])

    html = path.read_text(encoding="utf-8", errors="ignore")
    text = visible_text(html)
    text_norm = normalize(text)
    blocks = load_json_ld(html)
    types = node_types(blocks)

    wc = word_count(text)
    fq = faq_count(html, blocks)
    kw_present, kw_missing = coverage(text_norm, cfg["keywords"])
    award_present, award_missing = coverage(text_norm, AWARD_TERMS)
    ol = has_ordered_list(html)
    restaurant_schema = has_restaurant_schema(types)
    video_schema = has_video_schema(types)
    ar_count = aggregate_rating_count(blocks)

    findings: list[str] = []
    score = 10

    score += round(15 * len(kw_present) / max(1, len(cfg["keywords"])))
    if kw_missing:
        findings.append("Keywords ausentes ou pouco literais: " + ", ".join(kw_missing))

    if wc >= cfg["min_words"]:
        score += 15
    else:
        score += round(15 * min(1, wc / cfg["min_words"]))
        findings.append(f"Conteúdo curto: {wc} palavras; meta {cfg['min_words']}.")

    if fq >= cfg["min_faq"]:
        score += 20
    else:
        score += round(20 * min(1, fq / cfg["min_faq"]))
        findings.append(f"FAQ insuficiente: {fq}; meta {cfg['min_faq']}.")

    if not cfg["requires_ol"] or ol:
        score += 10
    else:
        findings.append("Falta lista numerada <ol> para Featured Snippet.")

    if not cfg["requires_awards"]:
        score += 10
    elif len(award_present) >= 4:
        score += 10
    else:
        score += round(10 * min(1, len(award_present) / 4))
        findings.append(f"E-E-A-T/premiações insuficientes: {len(award_present)}/4 termos mínimos.")

    if not cfg["requires_restaurant_schema"] or restaurant_schema:
        score += 10
    else:
        findings.append("Falta schema Restaurant/LocalBusiness/FoodEstablishment.")

    if not cfg["requires_video"] or video_schema:
        score += 10
    else:
        findings.append("Falta VideoObject schema recomendado.")

    if cfg["requires_single_aggregate_rating"]:
        if ar_count == 1:
            score += 10
        else:
            findings.append(f"aggregateRating deve ser único; encontrado {ar_count}.")
    else:
        if ar_count <= 1:
            score += 10
        else:
            findings.append(f"Possível duplicidade de aggregateRating: {ar_count}.")

    score = max(0, min(100, score))
    status = "PASS" if score >= THRESHOLD else "FAIL"
    return PageAudit(page, True, score, status, wc, fq, kw_present, kw_missing, award_present, award_missing, ol, restaurant_schema, video_schema, ar_count, findings)


def write_reports(results: list[PageAudit]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    min_score = min((r.score for r in results), default=0)
    status = "PASS" if min_score >= THRESHOLD and all(r.status == "PASS" for r in results) else "FAIL"

    REPORT_JSON.write_text(json.dumps({
        "status": status,
        "threshold": THRESHOLD,
        "min_score": min_score,
        "priority_keywords": PRIORITY_KEYWORDS,
        "targets": TARGETS,
        "results": [asdict(r) for r in results],
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    with REPORT_CSV.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=["page", "status", "score", "word_count", "faq_count", "has_ol", "has_restaurant_schema", "has_video_schema", "aggregate_rating_count", "keyword_present", "keyword_missing", "award_present", "findings"])
        writer.writeheader()
        for r in results:
            writer.writerow({
                "page": r.page,
                "status": r.status,
                "score": r.score,
                "word_count": r.word_count,
                "faq_count": r.faq_count,
                "has_ol": r.has_ol,
                "has_restaurant_schema": r.has_restaurant_schema,
                "has_video_schema": r.has_video_schema,
                "aggregate_rating_count": r.aggregate_rating_count,
                "keyword_present": " | ".join(r.keyword_present),
                "keyword_missing": " | ".join(r.keyword_missing),
                "award_present": " | ".join(r.award_present),
                "findings": " | ".join(r.findings),
            })

    lines = [
        "# Priority Keywords AIO Score Audit",
        "",
        f"Status geral: **{status}**",
        f"Score mínimo: **{min_score}**",
        f"Threshold: **{THRESHOLD}**",
        "",
        "## Palavras-chave prioritárias",
    ]
    lines.extend(f"- `{kw}`" for kw in PRIORITY_KEYWORDS)
    lines += ["", "## Resultado por página", "", "| Página | Status | Score | Palavras | FAQ | OL | Restaurant Schema | VideoObject | aggregateRating |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in results:
        lines.append(f"| `{r.page}` | {r.status} | {r.score} | {r.word_count} | {r.faq_count} | {r.has_ol} | {r.has_restaurant_schema} | {r.has_video_schema} | {r.aggregate_rating_count} |")
    lines += ["", "## Findings"]
    for r in results:
        lines.append(f"### `{r.page}` — {r.score}")
        lines.append(TARGETS.get(r.page, {}).get("notes", ""))
        lines.append("")
        if r.findings:
            lines.extend(f"- {item}" for item in r.findings)
        else:
            lines.append("- Nenhum gargalo crítico encontrado.")
        lines.append("")
    lines += ["## Arquivos", f"- `{REPORT_MD.relative_to(ROOT)}`", f"- `{REPORT_CSV.relative_to(ROOT)}`", f"- `{REPORT_JSON.relative_to(ROOT)}`", ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    results = [audit_page(page, cfg) for page, cfg in TARGETS.items()]
    write_reports(results)
    min_score = min((r.score for r in results), default=0)
    print(f"Priority Keywords AIO Score Audit: min_score={min_score}, threshold={THRESHOLD}")
    for r in results:
        print(f"{r.page}: {r.status} score={r.score}")
    return 0 if min_score >= THRESHOLD and all(r.status == "PASS" for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
