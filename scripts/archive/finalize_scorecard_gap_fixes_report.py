#!/usr/bin/env python3
"""Finalize the scorecard gap report from final HTML state.

The early scorecard fixer writes a useful diagnostic, but later pipeline steps can
change the final HTML. This script adds the remaining useful Eventos depth block
and rewrites the scorecard report from the final state.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "scorecard_gap_fixes_report.md"
JSONLD_RE = re.compile(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)
EVENTOS_START = "<!-- EC EVENTOS SCORECARD DEPTH FINAL FIX -->"
EVENTOS_END = "<!-- /EC EVENTOS SCORECARD DEPTH FINAL FIX -->"

TARGETS = ["index.html", "eventos.html", "en/cardapio.html", "en/almoco.html", "parque-bondinho.html"]


@dataclass
class PageResult:
    page: str
    status: str
    changed: bool
    faq_pages: int
    faq_questions: int
    ol_count: int
    words: int
    notes: str


def parse_json(raw: str) -> Any | None:
    try:
        return json.loads(html.unescape(raw.strip()))
    except Exception:
        return None


def type_has(value: Any, wanted: str) -> bool:
    if isinstance(value, str):
        return value.lower() == wanted.lower()
    if isinstance(value, list):
        return any(type_has(v, wanted) for v in value)
    return False


def is_faq(obj: Any) -> bool:
    return isinstance(obj, dict) and type_has(obj.get("@type"), "FAQPage")


def walk_faq(obj: Any) -> tuple[int, int]:
    pages = 0
    questions = 0
    if isinstance(obj, dict):
        if is_faq(obj):
            pages += 1
            main = obj.get("mainEntity")
            if isinstance(main, list):
                questions += len(main)
        for value in obj.values():
            p, q = walk_faq(value)
            pages += p
            questions += q
    elif isinstance(obj, list):
        for item in obj:
            p, q = walk_faq(item)
            pages += p
            questions += q
    return pages, questions


def count_faq(source: str) -> tuple[int, int]:
    pages = 0
    questions = 0
    for _, raw, _ in JSONLD_RE.findall(source):
        obj = parse_json(raw)
        if obj is None:
            continue
        p, q = walk_faq(obj)
        pages += p
        questions += q
    return pages, questions


def count_words(source: str) -> int:
    text = re.sub(r"<script[\s\S]*?</script>", " ", source, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"\b[\wÀ-ÿ]{2,}\b", html.unescape(text)))


def count_ol(source: str) -> int:
    return len(re.findall(r"<ol\b", source, flags=re.I))


def strip_eventos_block(source: str) -> str:
    return re.sub(re.escape(EVENTOS_START) + r"[\s\S]*?" + re.escape(EVENTOS_END) + r"\s*", "", source, flags=re.I)


def eventos_depth_block() -> str:
    return f"""
{EVENTOS_START}
<section class="content-section section-below-fold" aria-label="Planejamento detalhado de eventos na Embaixada Carioca">
  <div class="wrap-narrow">
    <h2>Como transformar o evento em uma experiência no Morro da Urca</h2>
    <p>Um evento na Embaixada Carioca deve ser pensado como uma experiência completa, não apenas como uma reserva de mesa. O diferencial está em combinar a chegada pelo Parque Bondinho, a vista do Morro da Urca, o serviço de salão e um cardápio que represente o Rio de Janeiro com clareza para convidados brasileiros e estrangeiros.</p>
    <p>Para eventos corporativos, o melhor resultado costuma vir de formatos objetivos: café da manhã executivo, welcome drink, coquetel de relacionamento, almoço para grupos, entrega de troféus, ação de marca ou encontro com clientes. A operação fica mais eficiente quando o briefing informa horário de chegada, tempo de permanência, necessidade de fala institucional, circulação do grupo e expectativa de consumo.</p>
    <p>Para celebrações sociais, como aniversário, noivado, pedido de casamento ou casamento com vista, o planejamento deve equilibrar emoção e praticidade. O horário, a luz natural, a circulação do parque, a necessidade de fotógrafo, decoração leve, música e mesa de apoio devem ser definidos antes da proposta final para evitar improvisos no dia.</p>
    <p>A equipe de eventos pode adaptar o formato conforme o objetivo: receber bem um grupo de turismo, criar uma pausa gastronômica durante o passeio, oferecer uma recepção elegante antes do pôr do sol ou montar um almoço especial com identidade carioca. Quanto mais claro for o contexto, mais precisa será a proposta comercial e operacional.</p>
  </div>
</section>
{EVENTOS_END}
""".strip()


def insert_before_close(source: str, payload: str) -> str:
    if "</main>" in source:
        return source.replace("</main>", payload + "\n</main>", 1)
    if "</body>" in source:
        return source.replace("</body>", payload + "\n</body>", 1)
    return source + "\n" + payload


def ensure_eventos_depth() -> bool:
    path = ROOT / "eventos.html"
    if not path.exists():
        return False
    original = path.read_text(encoding="utf-8", errors="ignore")
    base = strip_eventos_block(original)
    updated = insert_before_close(base, eventos_depth_block())
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return changed


def analyze_page(rel: str, changed_hint: bool = False) -> PageResult:
    path = ROOT / rel
    if not path.exists():
        return PageResult(rel, "missing", False, 0, 0, 0, 0, "file missing")
    source = path.read_text(encoding="utf-8", errors="ignore")
    faq_pages, faq_questions = count_faq(source)
    ol_count = count_ol(source)
    words = count_words(source)
    checks = [faq_questions >= 8, faq_pages <= 1]
    if rel == "eventos.html":
        checks.append(words >= 1200)
    if rel == "parque-bondinho.html":
        checks.append(ol_count >= 1)
    status = "ok" if all(checks) else "fail"
    notes = []
    if rel == "eventos.html":
        notes.append("visible_depth_block=True")
    if faq_pages <= 1:
        notes.append("no_duplicate_faq=True")
    return PageResult(rel, status, changed_hint, faq_pages, faq_questions, ol_count, words, "; ".join(notes))


def write_report(results: list[PageResult]) -> int:
    REPORT.parent.mkdir(exist_ok=True)
    failures = [r for r in results if r.status != "ok"]
    status = "PASS" if not failures else "FAIL"
    lines = [
        "# Scorecard Gap Fixes",
        "",
        f"Status geral: **{status}**",
        "",
        "## Objetivo",
        "Validar os gaps apontados no scorecard visual no estado final do HTML: FAQ incompleto, `parque-bondinho.html` sem FAQ/OL e conteúdo fino em `eventos.html`.",
        "",
        "## Guardrails",
        "- Nenhum AggregateRating, Rating ou Review foi inserido.",
        "- Nenhum Restaurant schema foi removido.",
        "- O relatório final valida também que não há mais de um FAQPage por página-alvo.",
        "- A alteração visível adicional foi aplicada apenas em `eventos.html` para corrigir conteúdo fino.",
        "",
        "## Resumo",
        f"- Páginas configuradas: **{len(results)}**",
        f"- Páginas com PASS: **{len([r for r in results if r.status == 'ok'])}**",
        f"- Páginas com falha: **{len(failures)}**",
        f"- Páginas alteradas nesta etapa: **{len([r for r in results if r.changed])}**",
        "",
        "## Resultados por página",
        "",
        "| Página | Status | Changed | FAQPage | FAQ perguntas | OL | Palavras | Notas |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for r in results:
        lines.append(f"| `{r.page}` | {r.status} | {r.changed} | {r.faq_pages} | {r.faq_questions} | {r.ol_count} | {r.words} | {r.notes} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Final scorecard gap report: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    eventos_changed = ensure_eventos_depth()
    results = [analyze_page(rel, changed_hint=(rel == "eventos.html" and eventos_changed)) for rel in TARGETS]
    return write_report(results)


if __name__ == "__main__":
    raise SystemExit(main())
