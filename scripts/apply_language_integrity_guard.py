#!/usr/bin/env python3
"""
Language Integrity Guard — Embaixada Carioca.

Objetivo:
- impedir contaminação de idioma nas páginas PT / EN / ES;
- corrigir imediatamente trechos em espanhol/inglês dentro de páginas em português;
- auditar home e páginas diretamente ligadas à home;
- gerar relatório de suspeitas remanescentes.

Regra operacional:
- PT raiz deve estar em português do Brasil.
- /en/ deve estar em inglês.
- /es/ deve estar em espanhol.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAIN_PAGES = {
    "index.html",
    "cafe-da-manha.html",
    "almoco.html",
    "entardecer.html",
    "eventos.html",
    "cardapio.html",
    "guia-do-rio.html",
    "en/index.html",
    "en/cafe-da-manha.html",
    "en/almoco.html",
    "en/entardecer.html",
    "en/eventos.html",
    "en/cardapio.html",
    "en/guia-do-rio.html",
    "es/index.html",
    "es/cafe-da-manha.html",
    "es/almoco.html",
    "es/entardecer.html",
    "es/eventos.html",
    "es/cardapio.html",
    "es/guia-do-rio.html",
}

PT_REPLACEMENTS = {
    # Hero/eventos — espanhol no português
    "Eventos en el ": "Eventos no ",
    "Espacio panorámico": "Espaço panorâmico",
    "todos recibidos con": "todos recebidos com",
    "vista más impresionante": "vista mais impressionante",
    "Hablar con nuestro equipo": "Falar com nossa equipe",
    "Para quién": "Para quem",
    "Dos universos, <span class=\"serif\">una vista</span>": "Dois universos, <span class=\"serif\">uma vista</span>",
    "Del evento corporativo al itinerario premium": "Do evento corporativo ao roteiro premium",
    "Reuniones matutinas": "Reuniões matinais",
    "con vista para o Pão de Açúcar": "com vista para o Pão de Açúcar",
    "equipo de bar": "equipe de bar",
    "recibidos": "recebidos",
    "una vista": "uma vista",
    "Del evento": "Do evento",
    "al itinerario": "ao roteiro",
    "para quién": "para quem",
    # Inglês no português
    "Corporate events e privados e festas": "Eventos corporativos, eventos privados e festas",
    "Corporate events e privados": "Eventos corporativos e privados",
    "Corporate events": "Eventos corporativos",
    "private events": "eventos privados",
    "Private events": "Eventos privados",
    "main dining room": "salão principal",
    "panoramic terraces": "terraços panorâmicos",
    "panoramic terrace": "terraço panorâmico",
    "hospitality team": "equipe receptiva",
    "Hospitality team": "Equipe receptiva",
    "Structure &amp; capacity": "Estrutura e capacidade",
    "Structure & capacity": "Estrutura e capacidade",
    "Capacity varies": "Capacidade variável",
    "Rooms": "Espaços",
    "Languages": "Idiomas",
    "Travel agency partnership": "Parceria com agências de viagens",
    "Corporate event venue": "Espaço para eventos corporativos",
    "Breakfast": "Café da manhã",
    "Brazilian lunch": "almoço brasileiro",
    "draft beer": "chope",
    "Food &amp; beverage": "Comidas e bebidas",
    "Food & beverage": "Comidas e bebidas",
    "view": "vista",
    "View": "Vista",
    # Portunhol recorrente
    "no alto do Morro da Urca, a 227 metros": "no alto do Morro da Urca, a 227 metros",
    "a vista mais impressionante da cidade": "a vista mais impressionante da cidade",
}

EVENTOS_PT_EXACT = {
    "<title>Eventos no Rio de Janeiro com Vista | Embaixada Carioca</title>": "<title>Eventos no Rio de Janeiro com Vista | Embaixada Carioca</title>",
}

PT_HERO_EVENTOS_H1_RE = re.compile(r"<h1>\s*Eventos\s+(?:en el|no)\s+<span class=\"serif\">Morro da Urca</span><br/>\s*—\s*com vista para o Pão de Açúcar\.\s*</h1>", re.IGNORECASE)
PT_HERO_EVENTOS_LEDE_RE = re.compile(r"<p class=\"lede\">\s*O <strong>espaço para eventos mais bonito do Rio de Janeiro</strong>[\s\S]*?</p>", re.IGNORECASE)
PT_AUDIENCE_HEAD_RE = re.compile(r"<div class=\"num\"><b>01</b>[^<]*</div>\s*<h2>[\s\S]*?</h2>\s*<p class=\"lede\">[\s\S]*?</p>", re.IGNORECASE)
PT_CAPACITY_HEAD_RE = re.compile(r"<div class=\"num\"><b>02</b>[^<]*</div>\s*<h2>[\s\S]*?</h2>\s*<p class=\"lede\">[\s\S]*?</p>", re.IGNORECASE)

PT_MAIN_FIXES = {
    "eventos.html": [
        (PT_HERO_EVENTOS_H1_RE, '<h1>Eventos no <span class="serif">Morro da Urca</span><br/>— com vista para o Pão de Açúcar.</h1>'),
        (PT_HERO_EVENTOS_LEDE_RE, '<p class="lede">O <strong>espaço para eventos mais bonito do Rio de Janeiro</strong> — no alto do Morro da Urca, a 227 metros, com vista panorâmica para o Pão de Açúcar e a Baía de Guanabara. Reuniões executivas, almoços corporativos, lançamentos, aniversários e roteiros para grupos internacionais — todos recebidos com gastronomia brasileira premiada e uma das vistas mais impressionantes da cidade.</p>'),
        (PT_AUDIENCE_HEAD_RE, '<div class="num"><b>01</b> Para quem</div>\n<h2>Dois universos, <span class="serif">uma vista</span> — eventos no Morro da Urca para empresas e agências.</h2>\n<p class="lede">Do evento corporativo ao roteiro premium para grupos internacionais — recebemos cada formato com curadoria sob medida no <strong>espaço para eventos do Morro da Urca</strong>. Entre os <strong>lugares para celebrar no Rio de Janeiro</strong>, este é o único com vista panorâmica para o Pão de Açúcar e a Baía de Guanabara. A gastronomia brasileira premiada é parte central da experiência.</p>'),
        (PT_CAPACITY_HEAD_RE, '<div class="num"><b>02</b> Estrutura e capacidade</div>\n<h2>Da reunião íntima ao <span class="serif">grande lançamento</span> — o espaço para eventos no Morro da Urca.</h2>\n<p class="lede">Múltiplos ambientes e terraços panorâmicos no <strong>Morro da Urca</strong>, com vista para o Pão de Açúcar e a Baía de Guanabara. Infraestrutura completa de gastronomia, bar, apoio técnico e equipe receptiva. Um dos lugares mais especiais para celebrar aniversários, encontros corporativos e eventos de marca no Rio de Janeiro.</p>'),
    ]
}

# Padrões suspeitos por idioma. São auditados; nem todos são substituídos automaticamente porque podem aparecer em nomes próprios, URLs ou schema técnico.
SUSPICIOUS_PT = [
    r"\ben el\b", r"\bnuestro\b", r"\bhablar\b", r"\bcon vista\b", r"\bpara qui[eé]n\b", r"\buna vista\b", r"\bdel evento\b", r"\breuniones\b", r"\brecibidos\b", r"\bm[aá]s impresionante\b",
    r"\bmain dining room\b", r"\bpanoramic terraces?\b", r"\bhospitality team\b", r"\bcapacity varies\b", r"\brooms\b", r"\blanguages\b", r"\bcorporate events\b", r"\btravel agency partnership\b",
]
SUSPICIOUS_EN = [r"\bSolicitar orçamento\b", r"\bReservar mesa\b", r"\bFalar com nossa equipe\b", r"\bCafé da manhã\b", r"\bAlmoço\b"]
SUSPICIOUS_ES = [r"\bSolicitar orçamento\b", r"\bReservar mesa\b", r"\bFalar com nossa equipe\b", r"\bBreakfast\b", r"\bLunch\b"]

REPORT: list[str] = []
WARNINGS: list[str] = []
COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "pt_replacements": 0,
    "targeted_blocks_fixed": 0,
    "warnings": 0,
}


def detect_lang(rel: str, text: str) -> str:
    if rel.startswith("en/") or 'lang="en"' in text:
        return "en"
    if rel.startswith("es/") or 'lang="es"' in text:
        return "es"
    return "pt"


def is_html(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return path.suffix == ".html" and ".git" not in path.parts and not rel.startswith("_")


def apply_pt_replacements(text: str, rel: str) -> str:
    for old, new in PT_REPLACEMENTS.items():
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            COUNTERS["pt_replacements"] += n
            REPORT.append(f"PT_REPLACE: {rel} | {old!r} -> {new!r} | {n}")
    if rel in PT_MAIN_FIXES:
        for pattern, replacement in PT_MAIN_FIXES[rel]:
            text, n = pattern.subn(replacement, text, count=1)
            if n:
                COUNTERS["targeted_blocks_fixed"] += n
                REPORT.append(f"PT_TARGET_BLOCK: {rel} | {pattern.pattern[:60]}...")
    return text


def audit_text(text: str, rel: str, lang: str) -> None:
    patterns = {"pt": SUSPICIOUS_PT, "en": SUSPICIOUS_EN, "es": SUSPICIOUS_ES}.get(lang, [])
    for pat in patterns:
        if re.search(pat, text, flags=re.IGNORECASE):
            WARNINGS.append(f"LANG_WARNING: {rel} [{lang}] contém padrão suspeito: {pat}")
            COUNTERS["warnings"] += 1


def process(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if not is_html(path):
        return
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    lang = detect_lang(rel, original)
    text = original

    if lang == "pt":
        text = apply_pt_replacements(text, rel)

    audit_text(text, rel, lang)

    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1
        REPORT.append(f"UPDATED: {rel}")


def write_report() -> None:
    d = ROOT / "_audit_reports"
    d.mkdir(exist_ok=True)
    p = d / "language_integrity_guard_report.md"
    lines = [
        "# Language Integrity Guard — Embaixada Carioca",
        "",
        "## Escopo",
        "- Home e páginas diretamente ligadas à home.",
        "- Páginas PT, EN e ES.",
        "- Correção automática de contaminação PT por espanhol/inglês.",
        "- Relatório de alertas remanescentes para revisão manual.",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Correções aplicadas"])
    lines.extend(f"- {x}" for x in REPORT) if REPORT else lines.append("- Nenhuma correção automática necessária.")
    lines.extend(["", "## Alertas remanescentes"])
    lines.extend(f"- {x}" for x in WARNINGS) if WARNINGS else lines.append("- Nenhum alerta remanescente encontrado.")
    lines.append("")
    p.write_text("\n".join(lines), encoding="utf-8")
    print(p.read_text(encoding="utf-8"))


def main() -> int:
    for path in sorted(ROOT.rglob("*.html")):
        process(path)
    write_report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
