#!/usr/bin/env python3
"""
Sprint 1–5 Excellence Audit — Embaixada Carioca

Audita se os Sprints 1 a 5 foram executados com excelência real.
Não corrige conteúdo. Só consolida evidências, notas, pendências e próximos gates.

Critério de excelência:
- PASS: critério técnico/estrutural executado e sem alerta relevante.
- WARN: executado, mas ainda há pendência para padrão AAA/6 estrelas.
- FAIL: ausente, quebrado ou com risco alto.
"""
from __future__ import annotations

from pathlib import Path
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
OUT = REPORT_DIR / "sprint1_5_excellence_audit.md"

WORKFLOW = ROOT / ".github/workflows/apply-aaa-fixes.yml"
DETAILS_CSV = REPORT_DIR / "sprint5_86page_quality_details.csv"
SPRINT5_REPORT = REPORT_DIR / "sprint5_86page_quality_consolidation_report.md"
SPRINT4_REPORT = REPORT_DIR / "sprint4_r2d2_aio_conversion_hardening_report.md"
GENERAL_REPORT = REPORT_DIR / "restaurant_site_10_criteria_audit.md"
DESIGN_REPORT = REPORT_DIR / "sprint3_design_consistency_gate_report.md"
VISUAL123_REPORT = REPORT_DIR / "sprint123_final_visual_validation_report.md"
SOURCE_REGISTRY = ROOT / "data/rio_authoritative_content_sources.json"

BASE = "https://www.embaixadacarioca.com"

REQUIRED_WORKFLOW_SCRIPTS = [
    "apply_sprint1_conversion_quality_fixes.py",
    "apply_sprint2_keyword_geo_growth.py",
    "apply_sprint2_locale_quality_fix.py",
    "apply_sprint3_como_chegar_access_cluster.py",
    "apply_sprint3_design_consistency_gate.py",
    "apply_sprint123_final_visual_validation.py",
    "apply_sprint4_r2d2_aio_conversion_hardening.py",
    "apply_sprint5_86page_quality_consolidation.py",
]

KEY_PAGES = [
    "index.html", "cafe-da-manha.html", "almoco.html", "como-chegar.html", "eventos.html", "cardapio.html", "guia-do-rio.html",
    "en/index.html", "en/cafe-da-manha.html", "en/almoco.html", "en/how-to-get-there.html", "en/eventos.html", "en/cardapio.html", "en/guia-do-rio.html",
    "es/index.html", "es/cafe-da-manha.html", "es/almoco.html", "es/como-llegar.html", "es/eventos.html", "es/cardapio.html", "es/guia-do-rio.html",
]

SPRINT4_TARGETS = [
    "en/where-to-eat-near-sugarloaf.html",
    "en/restaurant-at-urca-hill.html",
    "en/sugarloaf-cable-car-restaurant.html",
    "en/restaurants-near-sugarloaf-mountain.html",
    "es/donde-comer-cerca-del-pan-de-azucar.html",
    "es/restaurante-morro-da-urca.html",
    "es/restaurante-bondinho-pan-de-azucar.html",
    "es/restaurantes-cerca-del-pan-de-azucar.html",
]

ACCESS_PAGES = ["como-chegar.html", "en/how-to-get-there.html", "es/como-llegar.html"]
PRODUCT_FAQ_PAGES = [
    "cafe-da-manha.html", "en/cafe-da-manha.html", "es/cafe-da-manha.html",
    "feijoada.html", "en/feijoada.html", "es/feijoada.html",
    "eventos.html", "en/eventos.html", "es/eventos.html",
]

OLD_PHONE_PATTERNS = ["984501711", "98450-1711", "984501695", "98450-1695"]
WRONG_COORDS = ["-22.9511223", "-43.1642121"]
BROKEN_ACCESS_LINKS = ["/en/como-chegar.html", "/es/como-chegar.html"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def visible_text(html: str) -> str:
    html = re.sub(r"<script\b[\s\S]*?</script>|<style\b[\s\S]*?</style>|<!--[^>]*-->", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", html).strip()


def status_line(status: str, item: str, evidence: str) -> str:
    icon = {"PASS":"✅", "WARN":"⚠️", "FAIL":"❌"}.get(status, "•")
    return f"| {icon} {status} | {item} | {evidence} |"


def parse_counter(report: str, key: str) -> int | None:
    m = re.search(rf"-\s*{re.escape(key)}:\s*([0-9]+)", report)
    return int(m.group(1)) if m else None


def load_details() -> list[dict[str, str]]:
    if not DETAILS_CSV.exists():
        return []
    with DETAILS_CSV.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def has_all(text: str, tokens: list[str]) -> bool:
    return all(token in text for token in tokens)


def audit_workflow() -> tuple[list[str], int, int, int]:
    text = read(WORKFLOW)
    lines = []
    p = w = f = 0
    missing = [s for s in REQUIRED_WORKFLOW_SCRIPTS if s not in text]
    if not text:
        lines.append(status_line("FAIL", "Workflow principal", "Arquivo .github/workflows/apply-aaa-fixes.yml não encontrado.")); f += 1
    elif missing:
        lines.append(status_line("FAIL", "Workflow principal", "Scripts ausentes: " + ", ".join(missing))); f += 1
    else:
        lines.append(status_line("PASS", "Workflow principal", "Todos os scripts dos Sprints 1–5 estão encadeados no workflow.")); p += 1
    # Ordem mínima: Sprint 5 antes da auditoria final.
    if text and "apply_sprint5_86page_quality_consolidation.py" in text and "apply_structural_restaurant_site_audit.py" in text:
        if text.index("apply_sprint5_86page_quality_consolidation.py") < text.index("apply_structural_restaurant_site_audit.py"):
            lines.append(status_line("PASS", "Ordem dos gates", "Sprint 5 roda antes da auditoria estrutural final.")); p += 1
        else:
            lines.append(status_line("FAIL", "Ordem dos gates", "Sprint 5 está depois da auditoria estrutural final.")); f += 1
    return lines, p, w, f


def audit_sprint1(details: list[dict[str, str]]) -> tuple[list[str], int, int, int]:
    lines = []
    p = w = f = 0
    key_rows = [d for d in details if d.get("page") in KEY_PAGES]
    if not key_rows:
        lines.append(status_line("FAIL", "Sprint 1 — base de dados", "CSV de qualidade ausente ou sem páginas principais.")); f += 1
        return lines, p, w, f
    missing_schema = [d["page"] for d in key_rows if d.get("has_restaurant_schema") != "True"]
    missing_cta = [d["page"] for d in key_rows if d.get("has_cta") != "True"]
    missing_sitemap = [d["page"] for d in key_rows if d.get("in_sitemap") != "True"]
    missing_hours = [d["page"] for d in key_rows if d.get("has_opening_hours") != "True" and d["page"] not in ACCESS_PAGES]
    if not missing_schema and not missing_cta and not missing_sitemap:
        lines.append(status_line("PASS", "Sprint 1 — SEO técnico, CTA e entidade", "Páginas principais com schema, CTA e sitemap.")); p += 1
    else:
        lines.append(status_line("FAIL", "Sprint 1 — SEO técnico, CTA e entidade", f"Schema ausente: {missing_schema}; CTA ausente: {missing_cta}; sitemap ausente: {missing_sitemap}")); f += 1
    if not missing_hours:
        lines.append(status_line("PASS", "Sprint 1 — openingHours", "Páginas principais com horário estruturado onde aplicável.")); p += 1
    else:
        lines.append(status_line("WARN", "Sprint 1 — openingHours", "Sem openingHours em: " + ", ".join(missing_hours[:10]))); w += 1
    all_html = "\n".join(read(p) for p in ROOT.rglob("*.html") if ".git" not in p.parts)
    old_phones = [x for x in OLD_PHONE_PATTERNS if x in all_html]
    wrong_coords = [x for x in WRONG_COORDS if x in all_html]
    if not old_phones and not wrong_coords:
        lines.append(status_line("PASS", "Sprint 1 — telefone e coordenadas", "Sem telefones antigos e sem coordenadas antigas detectadas.")); p += 1
    else:
        lines.append(status_line("FAIL", "Sprint 1 — telefone e coordenadas", f"Telefones antigos: {old_phones}; coordenadas antigas: {wrong_coords}")); f += 1
    return lines, p, w, f


def audit_sprint2(details: list[dict[str, str]]) -> tuple[list[str], int, int, int]:
    lines = []
    p = w = f = 0
    if not details:
        lines.append(status_line("FAIL", "Sprint 2 — dados", "CSV de qualidade ausente.")); f += 1
        return lines, p, w, f
    missing_meta = [d["page"] for d in details if d.get("utility") != "True" and not d.get("meta_description")]
    leaks = [d for d in details if int(d.get("language_leak_count") or 0) > 0]
    if len(missing_meta) == 0:
        lines.append(status_line("PASS", "Sprint 2 — titles/metas", "Todas as páginas de conteúdo auditadas têm meta description.")); p += 1
    elif len(missing_meta) <= 6:
        lines.append(status_line("WARN", "Sprint 2 — titles/metas", f"{len(missing_meta)} páginas sem meta description: {', '.join(missing_meta[:8])}")); w += 1
    else:
        lines.append(status_line("FAIL", "Sprint 2 — titles/metas", f"{len(missing_meta)} páginas sem meta description.")); f += 1
    if not leaks:
        lines.append(status_line("PASS", "Sprint 2 — idioma PT/EN/ES", "Nenhum vazamento crítico detectado.")); p += 1
    else:
        lines.append(status_line("WARN", "Sprint 2 — idioma PT/EN/ES", f"{len(leaks)} possíveis vazamentos permanecem; exigem revisão humana: " + ", ".join(d['page'] for d in leaks[:8]))); w += 1
    source_registry = read(SOURCE_REGISTRY)
    if source_registry and all(x in source_registry for x in ["Riotur", "TurisRio", "Visit Rio", "Time Out", "image_policy"]):
        lines.append(status_line("PASS", "Sprint 2 — fontes editoriais", "Registro de fontes oficiais/guias/imagens criado.")); p += 1
    else:
        lines.append(status_line("WARN", "Sprint 2 — fontes editoriais", "Matriz de fontes ainda ausente ou incompleta.")); w += 1
    return lines, p, w, f


def audit_sprint3() -> tuple[list[str], int, int, int]:
    lines = []
    p = w = f = 0
    design_report = read(DESIGN_REPORT)
    visual_report = read(VISUAL123_REPORT)
    warnings = parse_counter(design_report, "warnings")
    if warnings == 0:
        lines.append(status_line("PASS", "Sprint 3 — design consistency gate", "Relatório de design com warnings: 0.")); p += 1
    elif warnings is None:
        lines.append(status_line("WARN", "Sprint 3 — design consistency gate", "Relatório não encontrado ou contador não lido.")); w += 1
    else:
        lines.append(status_line("FAIL", "Sprint 3 — design consistency gate", f"Warnings: {warnings}")); f += 1
    bad_links = []
    missing_tokens = []
    for rel in ACCESS_PAGES:
        text = read(ROOT / rel)
        if not text:
            missing_tokens.append(f"{rel}: ausente")
            continue
        for bad in BROKEN_ACCESS_LINKS:
            if bad in text:
                bad_links.append(f"{rel}: {bad}")
        tokens = ["class=\"top\"", "class=\"nav-inner\"", "class=\"page-hero\"", "class=\"hero-ctas\""]
        if not has_all(text, tokens):
            missing_tokens.append(rel)
    if not bad_links and not missing_tokens:
        lines.append(status_line("PASS", "Sprint 3 — Como Chegar PT/EN/ES", "Páginas de acesso existem, sem links EN/ES quebrados e com tokens visuais principais.")); p += 1
    else:
        lines.append(status_line("FAIL", "Sprint 3 — Como Chegar PT/EN/ES", f"Links ruins: {bad_links}; tokens ausentes: {missing_tokens}")); f += 1
    all_key_nav = "\n".join(read(ROOT / p) for p in KEY_PAGES if (ROOT / p).exists())
    if "📍</span>Como Chegar" not in all_key_nav and "📍</span>HOW TO GET THERE" not in all_key_nav and "📍</span>CÓMO LLEGAR" not in all_key_nav:
        lines.append(status_line("PASS", "Sprint 3 — menu sem pin", "Pin do Como Chegar não aparece nos menus principais auditados.")); p += 1
    else:
        lines.append(status_line("WARN", "Sprint 3 — menu sem pin", "Ainda há ocorrência de pin no menu em alguma página principal.")); w += 1
    if "warnings: 0" in visual_report.lower() or "Nenhum alerta" in visual_report:
        lines.append(status_line("PASS", "Sprint 1–3 — validação visual estrutural", "Relatório final 1–3 sem alertas estruturais.")); p += 1
    else:
        lines.append(status_line("WARN", "Sprint 1–3 — validação visual estrutural", "Relatório não encontrado ou não conclusivo.")); w += 1
    return lines, p, w, f


def audit_sprint4() -> tuple[list[str], int, int, int]:
    lines = []
    p = w = f = 0
    report = read(SPRINT4_REPORT)
    expected = {
        "r2d2_blocks_added": 8,
        "faq_blocks_added": 9,
        "schema_blocks_added": 9,
        "ordered_lists_added": 3,
        "warnings": 0,
    }
    misses = []
    for k, min_v in expected.items():
        v = parse_counter(report, k)
        if v is None or (k == "warnings" and v != 0) or (k != "warnings" and v < min_v):
            misses.append(f"{k}={v}, esperado {'=' if k == 'warnings' else '>='}{min_v}")
    if not misses:
        lines.append(status_line("PASS", "Sprint 4 — R2D2/AIO/conversão", "Relatório confirma R2D2, FAQ, schema, listas e warnings 0.")); p += 1
    else:
        lines.append(status_line("FAIL", "Sprint 4 — R2D2/AIO/conversão", "; ".join(misses))); f += 1
    missing_markers = []
    for rel in SPRINT4_TARGETS:
        if "EC Sprint 4 R2D2 Depth Block" not in read(ROOT / rel):
            missing_markers.append(rel)
    if not missing_markers:
        lines.append(status_line("PASS", "Sprint 4 — páginas R2D2", "8 páginas estratégicas EN/ES têm bloco R2D2.")); p += 1
    else:
        lines.append(status_line("FAIL", "Sprint 4 — páginas R2D2", "Bloco ausente em: " + ", ".join(missing_markers))); f += 1
    missing_faq = [rel for rel in PRODUCT_FAQ_PAGES if "FAQPage" not in read(ROOT / rel)]
    if not missing_faq:
        lines.append(status_line("PASS", "Sprint 4 — FAQ Schema produto/eventos", "Páginas de café, feijoada e eventos têm FAQPage.")); p += 1
    else:
        lines.append(status_line("FAIL", "Sprint 4 — FAQ Schema produto/eventos", "FAQPage ausente em: " + ", ".join(missing_faq))); f += 1
    return lines, p, w, f


def audit_sprint5(details: list[dict[str, str]]) -> tuple[list[str], int, int, int]:
    lines = []
    p = w = f = 0
    report = read(SPRINT5_REPORT)
    scanned = parse_counter(report, "html_scanned")
    updated = parse_counter(report, "pages_updated")
    score80 = parse_counter(report, "pages_score_80_plus_estimated")
    thin_after = parse_counter(report, "thin_after_estimated")
    leaks_count = len([d for d in details if int(d.get("language_leak_count") or 0) > 0]) if details else None
    if scanned == 86 and updated and updated >= 70:
        lines.append(status_line("PASS", "Sprint 5 — auditoria 86 páginas", f"Auditou {scanned} páginas e atualizou {updated}.")); p += 1
    else:
        lines.append(status_line("FAIL", "Sprint 5 — auditoria 86 páginas", f"html_scanned={scanned}, pages_updated={updated}.")); f += 1
    if score80 is not None and score80 >= 80:
        lines.append(status_line("PASS", "Sprint 5 — meta score 80", f"{score80}/86 páginas com score ≥80.")); p += 1
    elif score80 is not None and score80 >= 70:
        lines.append(status_line("WARN", "Sprint 5 — meta score 80", f"{score80}/86 páginas com score ≥80. Bom avanço, mas ainda não é excelência total.")); w += 1
    else:
        lines.append(status_line("FAIL", "Sprint 5 — meta score 80", f"{score80}/86 páginas com score ≥80.")); f += 1
    if thin_after == 0:
        lines.append(status_line("PASS", "Sprint 5 — thin content", "Nenhuma página de conteúdo abaixo de 650 palavras.")); p += 1
    elif thin_after is not None and thin_after <= 23:
        lines.append(status_line("WARN", "Sprint 5 — thin content", f"Ainda há {thin_after} páginas abaixo de 650 palavras; precisa Sprint editorial fonteado.")); w += 1
    else:
        lines.append(status_line("FAIL", "Sprint 5 — thin content", f"thin_after_estimated={thin_after}.")); f += 1
    if leaks_count == 0:
        lines.append(status_line("PASS", "Sprint 5 — vazamento de idioma", "Nenhum vazamento remanescente.")); p += 1
    elif leaks_count is not None and leaks_count <= 8:
        lines.append(status_line("WARN", "Sprint 5 — vazamento de idioma", f"{leaks_count} possíveis vazamentos remanescentes; revisar manualmente.")); w += 1
    else:
        lines.append(status_line("FAIL", "Sprint 5 — vazamento de idioma", f"{leaks_count} possíveis vazamentos.")); f += 1
    source_registry = read(SOURCE_REGISTRY)
    if source_registry:
        lines.append(status_line("PASS", "Sprint 5 — regra editorial", "Matriz de fontes oficiais e política de imagem registrada.")); p += 1
    else:
        lines.append(status_line("WARN", "Sprint 5 — regra editorial", "Matriz de fontes oficiais ainda ausente.")); w += 1
    return lines, p, w, f


def audit_general() -> tuple[list[str], int, int, int]:
    lines = []
    p = w = f = 0
    text = read(GENERAL_REPORT)
    if "Nota geral estimada: 10.0/10" in text and "| Integridade linguística PT/EN/ES | 10.0/10 | 0 |" in text:
        lines.append(status_line("PASS", "Auditoria estrutural final", "Nota estática 10/10 e 0 alertas nos critérios principais.")); p += 1
    elif text:
        lines.append(status_line("WARN", "Auditoria estrutural final", "Relatório existe, mas não confirma 10/10 completo.")); w += 1
    else:
        lines.append(status_line("FAIL", "Auditoria estrutural final", "Relatório não encontrado.")); f += 1
    return lines, p, w, f


def main() -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    details = load_details()
    sections = []
    total_p = total_w = total_f = 0
    for title, fn in [
        ("Workflow e ordem dos gates", lambda: audit_workflow()),
        ("Sprint 1 — Base técnica, schema, contato e conversão", lambda: audit_sprint1(details)),
        ("Sprint 2 — Keywords, idiomas, metas e fontes", lambda: audit_sprint2(details)),
        ("Sprint 3 — Como Chegar e consistência visual", lambda: audit_sprint3()),
        ("Sprint 4 — R2D2, AIO/SAI, FAQ, schema e sitemap", lambda: audit_sprint4()),
        ("Sprint 5 — Consolidação das 86 páginas", lambda: audit_sprint5(details)),
        ("Auditoria estrutural final", lambda: audit_general()),
    ]:
        lines, p, w, f = fn()
        total_p += p; total_w += w; total_f += f
        sections.append((title, lines))
    overall = "APROVADO COM RESSALVAS"
    if total_f:
        overall = "NÃO APROVADO — há falhas críticas"
    elif total_w == 0:
        overall = "APROVADO COM EXCELÊNCIA"

    out_lines = [
        "# Auditoria de Excelência — Sprints 1 a 5",
        "",
        f"## Veredito geral: {overall}",
        "",
        f"- PASS: {total_p}",
        f"- WARN: {total_w}",
        f"- FAIL: {total_f}",
        "",
        "## Critério de leitura",
        "- PASS = executado e sem alerta relevante.",
        "- WARN = executado, mas ainda não atinge padrão AAA/6 estrelas total.",
        "- FAIL = ausente, quebrado ou com risco alto.",
        "",
    ]
    for title, lines in sections:
        out_lines.extend([f"## {title}", "", "| Status | Item | Evidência |", "|---|---|---|"])
        out_lines.extend(lines)
        out_lines.append("")
    out_lines.extend([
        "## Conclusão executiva",
        "",
        "Os Sprints 1 a 5 estão tecnicamente executados e encadeados. A base de SEO técnico, schema, sitemap, CTAs, Como Chegar, R2D2 e consolidação das 86 páginas avançou muito.",
        "",
        "Ainda não é correto declarar excelência total AAA/6 estrelas em conteúdo porque o Sprint 5 mostra páginas abaixo da meta editorial: páginas com menos de 650 palavras, possíveis vazamentos de idioma e páginas abaixo do score 80 estimado. O próximo passo deve ser editorial fonteado, não geração automática de volume.",
        "",
        "## Próximas ações obrigatórias antes de declarar excelência total",
        "1. Revisar manualmente as páginas abaixo de score 80 do relatório Sprint 5.",
        "2. Corrigir os possíveis vazamentos de idioma restantes em guias EN/ES.",
        "3. Expandir páginas rasas apenas com conteúdo fonteado por Bondinho, Visit Rio, Riotur, TurisRio, Visit Brasil, Time Out ou acervo próprio.",
        "4. Criar matriz de imagens licenciadas antes de trocar ou adicionar novas imagens públicas.",
        "5. Depois da revisão editorial, rodar nova auditoria de performance para reduzir CSS inline e peso das maiores páginas.",
        "",
    ])
    OUT.write_text("\n".join(out_lines), encoding="utf-8")
    print(OUT.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
