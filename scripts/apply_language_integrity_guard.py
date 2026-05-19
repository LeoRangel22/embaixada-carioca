#!/usr/bin/env python3
"""
Language Integrity Guard — Embaixada Carioca.

Finalidade:
- corrigir contaminação de idioma em conteúdo editorial visível;
- evitar substituições perigosas em código, atributos, analytics, viewport e tokens técnicos;
- gerar relatório de alertas remanescentes.

Regra:
- PT raiz deve estar em português do Brasil.
- /en/ deve estar em inglês.
- /es/ deve estar em espanhol.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPORT: list[str] = []
WARNINGS: list[str] = []
COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "safe_replacements": 0,
    "targeted_blocks_fixed": 0,
    "technical_repairs": 0,
    "warnings": 0,
}

# Substituições seguras: apenas frases/fragmentos específicos.
# Não usar termos genéricos como "view", "menu", "rooms", etc.
PT_SAFE_REPLACEMENTS = {
    "Eventos en el ": "Eventos no ",
    "Espacio panorámico": "Espaço panorâmico",
    "todos recibidos con": "todos recebidos com",
    "vista más impresionante": "vista mais impressionante",
    "Hablar con nuestro equipo": "Falar com nossa equipe",
    "Para quién": "Para quem",
    "para quién": "para quem",
    "Dos universos, <span class=\"serif\">una vista</span>": "Dois universos, <span class=\"serif\">uma vista</span>",
    "Del evento corporativo al itinerario premium": "Do evento corporativo ao roteiro premium",
    "Reuniones matutinas": "Reuniões matinais",
    "Reuniones executivas": "Reuniões executivas",
    "todos recibidos": "todos recebidos",
    "recibidos": "recebidos",
    "equipo de bar": "equipe de bar",
    "Corporate events e privados e festas": "Eventos corporativos, eventos privados e festas",
    "Corporate events e privados": "Eventos corporativos e privados",
    "Corporate events": "Eventos corporativos",
    "main dining room": "salão principal",
    "panoramic terraces": "terraços panorâmicos",
    "panoramic terrace": "terraço panorâmico",
    "hospitality team": "equipe receptiva",
    "Structure &amp; capacity": "Estrutura e capacidade",
    "Structure & capacity": "Estrutura e capacidade",
    "Capacity varies": "Capacidade variável",
    "Travel agency partnership": "Parceria com agências de viagens",
    "Corporate event venue": "Espaço para eventos corporativos",
    "equipo": "equipe",
}

TECHNICAL_REPAIRS = {
    "send_page_vista": "send_page_view",
    "name=\"vistaport\"": "name=\"viewport\"",
    "name='vistaport'": "name='viewport'",
    "meta name=\"vistaport\"": "meta name=\"viewport\"",
    "page_vista": "page_view",
}

PT_HERO_EVENTOS_H1_RE = re.compile(
    r"<h1>\s*Eventos\s+(?:en el|no)\s+<span class=\"serif\">Morro da Urca</span><br/>\s*—\s*com vista para o Pão de Açúcar\.\s*</h1>",
    re.IGNORECASE,
)
PT_HERO_EVENTOS_LEDE_RE = re.compile(
    r"<p class=\"lede\">\s*O <strong>espaço para eventos mais bonito do Rio de Janeiro</strong>[\s\S]*?</p>",
    re.IGNORECASE,
)
PT_AUDIENCE_HEAD_RE = re.compile(
    r"<div class=\"num\"><b>01</b>[^<]*</div>\s*<h2>[\s\S]*?</h2>\s*<p class=\"lede\">[\s\S]*?</p>",
    re.IGNORECASE,
)
PT_CAPACITY_HEAD_RE = re.compile(
    r"<div class=\"num\"><b>02</b>[^<]*</div>\s*<h2>[\s\S]*?</h2>\s*<p class=\"lede\">[\s\S]*?</p>",
    re.IGNORECASE,
)

TARGETED_PT_FIXES = {
    "eventos.html": [
        (PT_HERO_EVENTOS_H1_RE, '<h1>Eventos no <span class="serif">Morro da Urca</span><br/>— com vista para o Pão de Açúcar.</h1>'),
        (PT_HERO_EVENTOS_LEDE_RE, '<p class="lede">O <strong>espaço para eventos mais bonito do Rio de Janeiro</strong> — no alto do Morro da Urca, a 227 metros, com vista panorâmica para o Pão de Açúcar e a Baía de Guanabara. Reuniões executivas, almoços corporativos, lançamentos, aniversários e roteiros para grupos internacionais — todos recebidos com gastronomia brasileira premiada e uma das vistas mais impressionantes da cidade.</p>'),
        (PT_AUDIENCE_HEAD_RE, '<div class="num"><b>01</b> Para quem</div>\n<h2>Dois universos, <span class="serif">uma vista</span> — eventos no Morro da Urca para empresas e agências.</h2>\n<p class="lede">Do evento corporativo ao roteiro premium para grupos internacionais — recebemos cada formato com curadoria sob medida no <strong>espaço para eventos do Morro da Urca</strong>. Entre os <strong>lugares para celebrar no Rio de Janeiro</strong>, este é o único com vista panorâmica para o Pão de Açúcar e a Baía de Guanabara. A gastronomia brasileira premiada é parte central da experiência.</p>'),
        (PT_CAPACITY_HEAD_RE, '<div class="num"><b>02</b> Estrutura e capacidade</div>\n<h2>Da reunião íntima ao <span class="serif">grande lançamento</span> — o espaço para eventos no Morro da Urca.</h2>\n<p class="lede">Múltiplos ambientes e terraços panorâmicos no <strong>Morro da Urca</strong>, com vista para o Pão de Açúcar e a Baía de Guanabara. Infraestrutura completa de gastronomia, bar, apoio técnico e equipe receptiva. Um dos lugares mais especiais para celebrar aniversários, encontros corporativos e eventos de marca no Rio de Janeiro.</p>'),
    ]
}

SUSPICIOUS = {
    "pt": [
        r"\ben el\b", r"\bnuestro\b", r"\bhablar\b", r"\bpara qui[eé]n\b", r"\bdel evento\b", r"\breuniones\b", r"\brecibidos\b", r"\bm[aá]s impresionante\b",
        r"\bmain dining room\b", r"\bpanoramic terraces?\b", r"\bhospitality team\b", r"\bcapacity varies\b", r"\bcorporate events\b", r"\btravel agency partnership\b",
    ],
    "en": [r"\bSolicitar orçamento\b", r"\bFalar com nossa equipe\b", r"\bAberto todos os dias\b"],
    "es": [r"\bSolicitar orçamento\b", r"\bFalar com nossa equipe\b", r"\bBreakfast\b", r"\bLunch\b"],
}


def lang_for(rel: str, text: str) -> str:
    if rel.startswith("en/") or 'lang="en"' in text:
        return "en"
    if rel.startswith("es/") or 'lang="es"' in text:
        return "es"
    return "pt"


def is_html(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return path.suffix == ".html" and ".git" not in path.parts and not rel.startswith("_")


def repair_technical_tokens(text: str, rel: str) -> str:
    for old, new in TECHNICAL_REPAIRS.items():
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            COUNTERS["technical_repairs"] += count
            REPORT.append(f"TECH_REPAIR: {rel} | {old!r} -> {new!r} | {count}")
    return text


def apply_pt_safe_replacements(text: str, rel: str) -> str:
    for old, new in PT_SAFE_REPLACEMENTS.items():
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            COUNTERS["safe_replacements"] += count
            REPORT.append(f"PT_SAFE_REPLACE: {rel} | {old!r} -> {new!r} | {count}")
    if rel in TARGETED_PT_FIXES:
        for pattern, replacement in TARGETED_PT_FIXES[rel]:
            text, count = pattern.subn(replacement, text, count=1)
            if count:
                COUNTERS["targeted_blocks_fixed"] += count
                REPORT.append(f"PT_TARGET_BLOCK: {rel} | {pattern.pattern[:70]}...")
    return text


def audit(text: str, rel: str, lang: str) -> None:
    for pattern in SUSPICIOUS.get(lang, []):
        if re.search(pattern, text, flags=re.IGNORECASE):
            COUNTERS["warnings"] += 1
            WARNINGS.append(f"LANG_WARNING: {rel} [{lang}] contém padrão suspeito: {pattern}")


def process(path: Path) -> None:
    if not is_html(path):
        return
    rel = path.relative_to(ROOT).as_posix()
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = repair_technical_tokens(original, rel)
    lang = lang_for(rel, text)
    if lang == "pt":
        text = apply_pt_safe_replacements(text, rel)
    audit(text, rel, lang)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1
        REPORT.append(f"UPDATED: {rel}")


def write_report() -> None:
    out = ROOT / "_audit_reports"
    out.mkdir(exist_ok=True)
    report = out / "language_integrity_guard_report.md"
    lines = [
        "# Language Integrity Guard — Embaixada Carioca",
        "",
        "## Contadores",
    ]
    for key, value in COUNTERS.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Correções aplicadas"])
    lines.extend(f"- {item}" for item in REPORT) if REPORT else lines.append("- Nenhuma correção automática necessária.")
    lines.extend(["", "## Alertas remanescentes"])
    lines.extend(f"- {item}" for item in WARNINGS) if WARNINGS else lines.append("- Nenhum alerta remanescente encontrado.")
    lines.append("")
    report.write_text("\n".join(lines), encoding="utf-8")
    print(report.read_text(encoding="utf-8"))


def main() -> int:
    for path in sorted(ROOT.rglob("*.html")):
        process(path)
    write_report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
