#!/usr/bin/env python3
"""
Embaixada Carioca — Priority Keywords AIO Score Audit

Inclui no super workflow a auditoria derivada do relatório:
"Análise Profunda: Palavras-Chave Prioritárias (Score 90+) — Maio 2026".

Foco:
- 8 palavras-chave prioritárias de fundo de funil.
- Páginas-alvo: index.html, restaurante-morro-da-urca.html, cafe-da-manha.html.
- Score AIO mínimo: 90.

Saídas:
- _audit_reports/priority_keywords_aio_score_audit.md
- _audit_reports/priority_keywords_aio_score_audit.csv
- _audit_reports/priority_keywords_aio_score_audit.json
"""

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

# Páginas e requisitos extraídos do relatório enviado.
TARGETS = {
    "index.html": {
        "keywords": [
            "restaurante pão de açúcar",
            "restaurante pao de acucar",
            "restaurante no pão de açúcar",
            "restaurante no pao de acucar rj",
            "av pasteur 520 urca rio de janeiro",
        ],
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
        "keywords": [
            "restaurante morro da urca",
            "restaurante no morro da urca",
            "restaurante pão de açúcar",
            "restaurante no pão de açúcar",
        ],
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
        "keywords": [
            "cafe da manha na urca",
            "café da manhã na urca",
            "café da manhã pão de açúcar",
            "cafe da manha pao de acucar",
        ],
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

AWARD_TERMS = [
    "Veja Rio",
    "Prazeres da Mesa",
    "melhor chope",
    "Heineken",
    "feijoada premiada",
    "caipirinha",
    "Magnífica",
    "picanha",
]

SCRIPT_RE = re.compile(r'<script[^>]+type=["\\']application/ld\+json["\\'][^>]*>(.*?)</script>', re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")
HIDDEN_RE = re.compile(r"<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>", re.I | re.S)


def normalize(text: str) -> str:
    repl = str.maketrans({
        "á": "a", "à": "a", "ã": "a", "â": "a", "ä": "a",
        "é": "e", "ê": "e", "è": "e", "ë": "e",
        "í": "i", "ì": "i", "î": "i", "ï": "i",
        "ó": "o", "ò": "o", "õ": "o", "ô": "o", "ö": "o",
        "ú": "u", "ù": "u", "û": "u", "ü": "u",
        "ç": "c",
    })
    return text.lower().translate(repl)


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
    counts: list[int] = []
    for block in blocks:
        for node in walk_json(block):
            if not isinstance(node, dict):
                continue
            if node.get("@type") == "FAQPage":
                main = node.get("mainEntity")
                if isinstance(main, list):
                    counts.append(len(main))
    # Fallbacks para HTML renderizado.
    counts.append(len(re.findall(r'itemtype=["\\']https://schema\.org/Question["\\']', html, re.I)))
    counts.append(len(re.findall(r'class=["\\'][^"\\']*faq-item', html, re.I)))
    counts.append(len(re.findall(r'class=["\\'][^"\\']*faq-question', html, re.I)))
    return max(counts) if counts else 0


def aggregate_rating_count(blocks: list[Any]) -> int:
    count = 0
    for block in blocks:
        for node in walk_json(block):
            if isinstance(node, dict) and "aggregateRating" in node:
                count += 1
    return count


def has_restaurant_schema(types: list[str]) -> bool:
    wanted = {"Restaurant", "FoodEstablishment", "LocalBusiness"}
    return any(t in wanted for t in types)


def has_video_schema(types: list[str]) -> bool:
    return "VideoObject" in types


def has_ordered_list(html: str) -> bool:
    return bool(re.search(r"<ol\b", html, re.I))


def keyword_coverage(text_norm: str, keywords: list[str]) -> tuple[int, list[str], list[str]]:
    present = []
    missing = []
    for kw in keywords:
        if normalize(kw) in text_norm:
            present.append(kw)
        else:
            missing.append(kw)
    return len(present), present, missing


def award_coverage(text_norm: str) -> tuple[int, list[str], list[str]]:
    present = []
    missing = []
    for term in AWARD_TERMS:
        if normalize(term) in text_norm:
            present.append(term)
        else:
            missing.append(term)
    return len(present), present, missing


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
        return PageAudit(
            page=page,
            exists=False,
            score=0,
            status="FAIL",
            word_count=0,
            faq_count=0,
            keyword_present=[],
            keyword_missing=cfg["keywords"],
            award_present=[],
            award_missing=AWARD_TERMS,
            has_ol=False,
            has_restaurant_schema=False,
            has_video_schema=False,
            aggregate_rating_count=0,
            findings=["Página-alvo não encontrada."],
        )

    html = path.read_text(encoding="utf-8", errors="ignore")
    text = visible_text(html)
    text_norm = normalize(text)
    blocks = load_json_ld(html)
    types = node_types(blocks)

    wc = word_count(text)
    fq = faq_count(html, blocks)
    kw_count, kw_present, kw_missing = keyword_coverage(text_norm, cfg["keywords"])
    aw_count, aw_present, aw_missing = award_coverage(text_norm)
    ol = has_ordered_list(html)
    restaurant_schema = has_restaurant_schema(types)
    video_schema = has_video_schema(types)
    ar_count = aggregate_rating_count(blocks)

    score = 0
    findings: list[str] = []

    # 100 pontos distribuídos para refletir os gargalos do relatório.
    score += 10  # página existe

    keyword_score = round(15 * (kw_count / max(1, len(cfg["keywords"]))))
    score += keyword_score
    if kw_missing:
        findings.append(f"Keywords ausentes ou pouco literais: {', '.join(kw_missing)}")

    if wc >= cfg["min_words"]:
        score += 15
    else:
        partial = round(15 * min(1, wc / cfg["min_words"]))
        score += partial
        findings.append(f"Conteúdo curto para Score 90+: {wc} palavras; meta {cfg['min_words']}.")

    if fq >= cfg["min_faq"]:
        score += 20
    else:
        score += round(20 * min(1, fq / cfg["min_faq"]))
        findings.append(f"FAQ insuficiente: {fq}; meta {cfg['min_faq']}.")

    if cfg["requires_ol"]:
        if ol:
            score += 10
        else:
            findings.append("Falta lista numerada <ol> para captura de Featured Snippet.")
    else:
        score += 10

    if cfg["requires_awards"]:
        if aw_count >= 4:
            score += 10
        else:
            score += round(10 * min(1, aw_count / 4))
            findings.append(f"E-E-A-T/premiações insuficientes em texto HTML; encontrados {aw_count}/4 termos mínimos.")
    else:
        score += 10

    if cfg["requires_restaurant_schema"]:
        if restaurant_schema:
            score += 10
        else:
            findings.append("Falta schema Restaurant/LocalBusiness/FoodEstablishment.")
    else:
        score += 10

    if cfg["requires_video"]:
        if video_schema:
            score += 10
        else:
            findings.append("Falta VideoObject schema recomendado para Score AIO 90+.")
    else:
        score += 10

    if cfg["requires_single_aggregate_rating"]:
        if ar_count == 1:
            score += 10
        else:
            findings.append(f"aggregateRating deve ser único na página; encontrado {ar_count}.")
    else:
        # Para páginas sem obrigação de rating, penaliza só duplicidade crítica.
        if ar_count <= 1:
            score += 10
        else:
            findings.append(f"Possível duplicidade de aggregateRating: {ar_count}.")

    score = max(0, min(100, score))
    status = "PASS" if score >= THRESHOLD else "FAIL"

    return PageAudit(
        page=page,
        exists=True,
        score=score,
        status=status,
        word_count=wc,
        faq_count=fq,
        keyword_present=kw_present,
        keyword_missing=kw_missing,
        award_present=aw_present,
        award_missing=aw_missing,
        has_ol=ol,
        has_restaurant_schema=restaurant_schema,
        has_video_schema=video_schema,
        aggregate_rating_count=ar_count,
        findings=findings,
    )


def write_reports(results: list[PageAudit]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    min_score = min((r.score for r in results), default=0)
    status = "PASS" if min_score >= THRESHOLD and all(r.status == "PASS" for r in results) else "FAIL"

    REPORT_JSON.write_text(
        json.dumps({
            "status": status,
            "threshold": THRESHOLD,
            "min_score": min_score,
            "priority_keywords": PRIORITY_KEYWORDS,
            "targets": TARGETS,
            "results": [asdict(r) for r in results],
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with REPORT_CSV.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=[
            "page", "status", "score", "word_count", "faq_count", "has_ol",
            "has_restaurant_schema", "has_video_schema", "aggregate_rating_count",
            "keyword_present", "keyword_missing", "award_present", "findings",
        ])
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

    lines: list[str] = []
    lines.append("# Priority Keywords AIO Score Audit")
    lines.append("")
    lines.append(f"Status geral: **{status}**")
    lines.append(f"Score mínimo: **{min_score}**")
    lines.append(f"Threshold: **{THRESHOLD}**")
    lines.append("")
    lines.append("## Palavras-chave prioritárias")
    for kw in PRIORITY_KEYWORDS:
        lines.append(f"- `{kw}`")
    lines.append("")
    lines.append("## Resultado por página")
    lines.append("")
    lines.append("| Página | Status | Score | Palavras | FAQ | OL | Restaurant Schema | VideoObject | aggregateRating |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in results:
        lines.append(
            f"| `{r.page}` | {r.status} | {r.score} | {r.word_count} | {r.faq_count} | "
            f"{str(r.has_ol)} | {str(r.has_restaurant_schema)} | {str(r.has_video_schema)} | {r.aggregate_rating_count} |"
        )
    lines.append("")
    lines.append("## Findings")
    for r in results:
        lines.append(f"### `{r.page}` — {r.score}")
        lines.append(TARGETS.get(r.page, {}).get("notes", ""))
        lines.append("")
        if r.findings:
            for item in r.findings:
                lines.append(f"- {item}")
        else:
            lines.append("- Nenhum gargalo crítico encontrado.")
        if r.keyword_missing:
            lines.append(f"- Keywords faltantes: {', '.join(r.keyword_missing)}")
        lines.append("")
    lines.append("## Arquivos")
    lines.append(f"- `{REPORT_MD.relative_to(ROOT)}`")
    lines.append(f"- `{REPORT_CSV.relative_to(ROOT)}`")
    lines.append(f"- `{REPORT_JSON.relative_to(ROOT)}`")
    lines.append("")
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
