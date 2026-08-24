#!/usr/bin/env python3
"""Padroniza a atribuição factual do prêmio da feijoada em PT/EN/ES."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "feijoada_award_attribution_fix_2026-08-23.md"
SKIP_PARTS = {"_backups", "_templates", "sources", ".codex-work"}

CANONICAL = {
    "pt": "Feijoada da Academia da Cachaça — Melhor Feijoada do Brasil, Prazeres da Mesa 2017; vencedora da categoria Melhor Feijoada no Veja Rio Comer & Beber 2025 — servida na Embaixada Carioca por meio de parceria formal",
    "en": "Academia da Cachaça's feijoada — Best Feijoada in Brazil, Prazeres da Mesa 2017; winner of Veja Rio Comer & Beber's Best Feijoada category in 2025 — served at Embaixada Carioca through a formal partnership",
    "es": "Feijoada de Academia da Cachaça — Mejor Feijoada de Brasil, Prazeres da Mesa 2017; ganadora de la categoría Mejor Feijoada de Veja Rio Comer & Beber 2025 — servida en Embaixada Carioca mediante una colaboración formal",
}

JSON_CANONICAL = {
    "pt": "Academia da Cachaça — Melhor Feijoada do Brasil, Prazeres da Mesa 2017; vencedora da categoria Melhor Feijoada no Veja Rio Comer & Beber 2025",
    "en": "Academia da Cachaça — Best Feijoada in Brazil, Prazeres da Mesa 2017; winner of Veja Rio Comer & Beber's Best Feijoada category in 2025",
    "es": "Academia da Cachaça — Mejor Feijoada de Brasil, Prazeres da Mesa 2017; ganadora de la categoría Mejor Feijoada de Veja Rio Comer & Beber 2025",
}

ENTITY_TYPES = {"Restaurant", "LocalBusiness", "FoodEstablishment", "Organization"}
DISH_TYPES = {"Recipe", "MenuItem", "Product"}
AWARD_SIGNAL = re.compile(r"feijoada|veja\s+rio", re.I)
JSON_LD_RE = re.compile(
    r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.I | re.S,
)


def language(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt"


def html_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.html")
        if not any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts)
    )


def replace_copy(text: str, lang: str) -> tuple[str, int]:
    original = text

    direct_patterns: dict[str, list[tuple[str, str]]] = {
        "pt": [
            (
                r"A Melhor Feijoada do Rio de Janeiro — Veja Rio Comer &(?:amp;)? Beber 2025, em parceria com a Academia da Cachaça no Morro da Urca",
                "Feijoada premiada da Academia da Cachaça, servida na Embaixada Carioca no Morro da Urca",
            ),
            (
                r"Melhor Feijoada do Rio de Janeiro — Veja Rio Comer &(?:amp;)? Beber 2025, em parceria com a Academia da Cachaça, servida na Embaixada Carioca, com acompanhamentos, servida no Morro da Urca",
                "Feijoada premiada da Academia da Cachaça, servida na Embaixada Carioca no Morro da Urca, com acompanhamentos",
            ),
            (
                r"A Melhor Feijoada do Rio de Janeiro — Veja Rio Comer & Beber 2025, em parceria com a Academia da Cachaça é servida na Embaixada Carioca, por meio de parceria formal",
                "A feijoada da Academia da Cachaça, vencedora da categoria Melhor Feijoada no Veja Rio Comer & Beber 2025, é servida na Embaixada Carioca por meio de parceria formal",
            ),
            (
                r"Eleita <strong>Melhor Feijoada do Rio</strong> pela Revista Veja Rio Comer &amp; Beber 2025\.",
                "Feijoada da <strong>Academia da Cachaça</strong>, vencedora da categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025.",
            ),
            (
                r"a <strong>feijoada premiada Veja Rio é exclusiva da Embaixada Carioca</strong>, em parceria com a Academia da Cachaça",
                "a <strong>feijoada premiada da Academia da Cachaça é servida no Parque Bondinho pela Embaixada Carioca</strong>, por meio de parceria formal",
            ),
            (
                r"A feijoada premiada da Embaixada Carioca é servida todos os dias",
                "A feijoada premiada da Academia da Cachaça é servida na Embaixada Carioca, por meio de parceria formal, todos os dias",
            ),
            (
                r"A feijoada premiada da Embaixada Carioca no Morro da Urca",
                "A feijoada premiada da Academia da Cachaça no Morro da Urca",
            ),
            (
                r"A feijoada premiada eleita Melhor Feijoada do Rio de Janeiro pela Veja Rio Comer & Beber 2025\. Receita da Academia da Cachaça, servida diariamente na Embaixada Carioca",
                "A feijoada da Academia da Cachaça, vencedora da categoria Melhor Feijoada no Veja Rio Comer & Beber 2025, é servida diariamente na Embaixada Carioca por meio de parceria formal",
            ),
            (
                r"Feijoada premiada da Embaixada Carioca com acompanhamentos",
                "Feijoada premiada da Academia da Cachaça, servida na Embaixada Carioca, com acompanhamentos",
            ),
            (
                r"A feijoada da Embaixada Carioca foi eleita a <strong>Melhor Feijoada do Rio de Janeiro</strong> pela <strong>Veja Rio Comer &amp; Beber 2025/2026</strong>",
                "A Embaixada Carioca serve a feijoada da Academia da Cachaça, vencedora da categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025, por meio de parceria formal",
            ),
            (
                r"A feijoada da Embaixada Carioca foi eleita a <strong>Melhor Feijoada do Rio de Janeiro</strong> pela <strong>Veja Rio Comer & Beber 2025/2026</strong>",
                "A Embaixada Carioca serve a feijoada da <strong>Academia da Cachaça</strong>, vencedora da categoria <strong>Melhor Feijoada</strong> no <strong>Veja Rio Comer & Beber 2025</strong>, por meio de parceria formal",
            ),
            (
                r"A feijoada da Embaixada Carioca foi eleita a Melhor Feijoada do Rio de Janeiro pela Veja Rio Comer & Beber 2025/2026",
                "A Embaixada Carioca serve a feijoada da Academia da Cachaça, vencedora da categoria Melhor Feijoada no Veja Rio Comer & Beber 2025, por meio de parceria formal",
            ),
            (
                r"A Embaixada Carioca foi eleita pela <strong>Veja Rio Comer &amp; Beber 2025/2026</strong> como o restaurante com a <strong>Melhor Feijoada do Rio de Janeiro</strong>",
                "A <strong>Academia da Cachaça</strong> venceu a categoria <strong>Melhor Feijoada</strong> do <strong>Veja Rio Comer &amp; Beber 2025</strong>, e a mesma feijoada é servida na Embaixada Carioca por meio de parceria formal",
            ),
            (
                r"servida pela <strong>Embaixada Carioca</strong>, vencedora do prêmio Veja Rio Comer &amp; Beber 2025/2026 em parceria com a Academia da Cachaça",
                "feijoada da <strong>Academia da Cachaça</strong>, vencedora da categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025, servida pela <strong>Embaixada Carioca</strong> por meio de parceria formal",
            ),
            (
                r"Premiada como premiada pela Revista Veja Rio Comer & Beber 2025/2026 na Academia da Cachaça",
                "Feijoada da Academia da Cachaça, vencedora da categoria Melhor Feijoada no Veja Rio Comer & Beber 2025",
            ),
            (
                r"a feijoada eleita premiada pela Revista Veja Rio Comer & Beber 2025/2026 na Academia da Cachaça",
                "a feijoada da Academia da Cachaça, vencedora da categoria Melhor Feijoada no Veja Rio Comer & Beber 2025",
            ),
            (
                r"eleita a premiada pela Revista Veja Rio Comer & Beber 2025/2026 na Academia da Cachaça",
                "vencedora da categoria Melhor Feijoada no Veja Rio Comer & Beber 2025",
            ),
            (
                r"A feijoada da Embaixada Carioca foi eleita uma das melhores do Rio de Janeiro pela revista Veja Rio \(Comer &amp; Beber 2025 e 2026\)",
                "A feijoada da Academia da Cachaça, vencedora da categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025, é servida na Embaixada Carioca por meio de parceria formal",
            ),
            (
                r"A feijoada foi eleita uma das melhores do Rio de Janeiro pela revista Veja Rio \(Comer & Beber 2025 e 2026\)",
                "A feijoada da Academia da Cachaça, vencedora da categoria Melhor Feijoada no Veja Rio Comer & Beber 2025, é servida na Embaixada Carioca por meio de parceria formal",
            ),
            (
                r"A feijoada premiada no Morro da Urca é servida na Embaixada Carioca, restaurante dentro do Parque Bondinho Pão de Açúcar\. A receita é feita em parceria com a Academia da Cachaça e foi eleita a Melhor Feijoada do Rio de Janeiro pela Veja Rio Comer & Beber 2025/2026\.",
                "A feijoada premiada no Morro da Urca é a feijoada da Academia da Cachaça, vencedora da categoria Melhor Feijoada no Veja Rio Comer & Beber 2025, servida na Embaixada Carioca por meio de parceria formal dentro do Parque Bondinho Pão de Açúcar.",
            ),
            (
                r"A feijoada da Embaixada Carioca — feita em parceria com a Academia da Cachaça — foi eleita a Melhor Feijoada do Rio de Janeiro pela Veja Rio Comer & Beber 2025/2026\.",
                "A Embaixada Carioca serve, por meio de parceria formal, a feijoada da Academia da Cachaça — vencedora da categoria Melhor Feijoada no Veja Rio Comer & Beber 2025.",
            ),
            (
                r"<strong>A feijoada servida no Morro da Urca é a feijoada da Academia da Cachaça, servida na Embaixada Carioca — restaurante dentro do Parque Bondinho Pão de Açúcar\.</strong> Foi eleita a Melhor Feijoada do Rio de Janeiro pela Veja Rio Comer &amp; Beber 2025/2026\.",
                "<strong>A feijoada servida no Morro da Urca é a feijoada da Academia da Cachaça — vencedora da categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025 — servida na Embaixada Carioca por meio de parceria formal dentro do Parque Bondinho Pão de Açúcar.</strong>",
            ),
            (
                r"A receita é da <strong>Academia da Cachaça</strong> e foi eleita a <strong>Melhor Feijoada do Rio de Janeiro pela Veja Rio Comer &amp; Beber 2025/2026</strong>",
                "A receita é da <strong>Academia da Cachaça</strong>, vencedora da categoria <strong>Melhor Feijoada no Veja Rio Comer &amp; Beber 2025</strong>",
            ),
            (
                r"A receita é da Academia da Cachaça e foi eleita a Melhor Feijoada do Rio pela Veja Rio Comer &amp; Beber 2025/2026",
                "A receita é da Academia da Cachaça, vencedora da categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025",
            ),
            (
                r"— eleita premiada pela Revista Veja Rio Comer &amp; Beber 2025/2026 na Academia da Cachaça — é servida <strong>todos os dias das 11h30 às 17h</strong>\. Servida pela Embaixada Carioca e premiada pela Veja Rio Comer &amp; Beber 2025/2026, em parceria com a Academia da Cachaça\.",
                "— vencedora da categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025 — é servida <strong>todos os dias das 11h30 às 17h</strong> na Embaixada Carioca por meio de parceria formal.",
            ),
            (
                r"é a mesma Feijoada da Academia da Cachaça — vencedora da categoria Melhor Feijoada no Veja Rio Comer & Beber 2025 — servida na Embaixada Carioca por meio de parceria formal, eleita a premiada pela Revista Veja Rio Comer &amp; Beber 2025/2026 na Academia da Cachaça",
                "é a feijoada da Academia da Cachaça — vencedora da categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025 — servida na Embaixada Carioca por meio de parceria formal",
            ),
            (
                r"Premiado pela Veja Rio \(Melhor Feijoada do Rio 2025/2026\)",
                "A casa serve a feijoada premiada da Academia da Cachaça, vencedora do Veja Rio Comer &amp; Beber 2025",
            ),
        ],
        "en": [
            (
                r"Winner of <strong>Best Feijoada in Rio de Janeiro</strong> — Veja Rio Comer &amp; Beber 2025\.",
                "Academia da Cachaça's feijoada, winner of <strong>Best Feijoada in Rio de Janeiro</strong> at Veja Rio Comer &amp; Beber 2025.",
            ),
            (
                r"Our second best-seller\. Embaixada Carioca's feijoada, named Best Feijoada in Rio de Janeiro by Veja Rio Comer & Beber 2025, in partnership with Academia da Cachaça\.",
                "Our second best-seller. Academia da Cachaça's feijoada, winner of Veja Rio Comer & Beber's Best Feijoada category in 2025, served at Embaixada Carioca through a formal partnership.",
            ),
            (
                r"Embaixada Carioca's feijoada was voted <strong>Best Feijoada in Rio de Janeiro</strong> by <strong>Veja Rio Comer &amp; Beber 2025/2026</strong>",
                "Embaixada Carioca serves <strong>Academia da Cachaça's feijoada</strong>, winner of the <strong>Best Feijoada</strong> category at <strong>Veja Rio Comer &amp; Beber 2025</strong>, through a formal partnership",
            ),
            (
                r"Winner of Best Feijoada in Rio de Janeiro — Veja Rio Comer & Beber 2025/2026",
                "Academia da Cachaça's feijoada, winner of Veja Rio Comer & Beber's Best Feijoada category in 2025",
            ),
            (
                r"the winner of Best Feijoada in Rio de Janeiro — Veja Rio Comer & Beber 2025/2026 —",
                "Academia da Cachaça's award-winning feijoada — Best Feijoada, Veja Rio Comer & Beber 2025 —",
            ),
        ],
        "es": [
            (
                r"La feijoada de Embaixada Carioca fue elegida la <strong>Mejor Feijoada de Río de Janeiro</strong> por <strong>Veja Rio Comer &amp; Beber 2025/2026</strong>",
                "Embaixada Carioca sirve la feijoada de <strong>Academia da Cachaça</strong>, ganadora de la categoría <strong>Mejor Feijoada</strong> de <strong>Veja Rio Comer &amp; Beber 2025</strong>, mediante una colaboración formal",
            ),
            (
                r"servida por <strong>Embaixada Carioca</strong>, ganadora del premio Veja Rio Comer & Beber 2025/2026 en colaboración con Academia da Cachaça",
                "feijoada de <strong>Academia da Cachaça</strong>, ganadora de la categoría Mejor Feijoada de Veja Rio Comer & Beber 2025, servida en <strong>Embaixada Carioca</strong> mediante una colaboración formal",
            ),
            (
                r"Embaixada Carioca fue elegida por la revista <strong>Veja Rio</strong> como el restaurante con la mejor feijoada de Río de Janeiro",
                "Academia da Cachaça ganó la categoría <strong>Mejor Feijoada</strong> de <strong>Veja Rio Comer &amp; Beber 2025</strong>, y Embaixada Carioca sirve esa misma feijoada mediante una colaboración formal",
            ),
            (
                r"La <a ([^>]+)>feijoada de Embaixada Carioca</a> fue elegida Mejor Feijoada de Río de Janeiro por Veja Rio Comer & Beber 2025/2026, en colaboración con Academia da Cachaça",
                r"La <a \1>feijoada de Academia da Cachaça servida en Embaixada Carioca</a> ganó la categoría Mejor Feijoada de Veja Rio Comer & Beber 2025",
            ),
            (
                r"La <a ([^>]+)>feijoada de Embaixada Carioca</a> fue elegida Mejor Feijoada de Río de Janeiro por Veja Rio Comer &amp; Beber 2025/2026, en colaboración con Academia da Cachaça",
                r"La <a \1>feijoada de Academia da Cachaça servida en Embaixada Carioca</a> ganó la categoría Mejor Feijoada de Veja Rio Comer &amp; Beber 2025",
            ),
            (
                r"O prato mais emblemático do Brasil\. Na Embaixada Carioca, servimos a feijoada elegida Mejor Feijoada de Río de Janeiro por Veja Rio Comer & Beber 2025/2026, en colaboración con Academia da Cachaça — eleita a premiada pela Revista Veja Rio Comer & Beber 2025/2026 na Academia da Cachaça\. Servida todos los días no almuerzo\.",
                "El plato más emblemático de Brasil. Embaixada Carioca sirve la feijoada de Academia da Cachaça — ganadora de la categoría Mejor Feijoada de Veja Rio Comer & Beber 2025 — mediante una colaboración formal. Disponible todos los días durante el almuerzo.",
            ),
            (
                r"premiada por Veja Rio Comer & Beber 2025/2026 en colaboración con Academia da Cachaça",
                "de Academia da Cachaça, ganadora de la categoría Mejor Feijoada de Veja Rio Comer & Beber 2025 y servida en Embaixada Carioca mediante una colaboración formal",
            ),
        ],
    }

    count = 0
    for pattern, replacement in direct_patterns[lang]:
        text, made = re.subn(pattern, replacement, text, flags=re.I)
        count += made

    global_replacements = {
        "pt": [
            (
                "Melhor Feijoada do Rio de Janeiro — Veja Rio Comer & Beber 2025/2026, em parceria com a Academia da Cachaça",
                CANONICAL["pt"],
            ),
            (
                "Melhor Feijoada do Rio de Janeiro — Veja Rio Comer & Beber 2025/2026",
                "Feijoada da Academia da Cachaça — Melhor Feijoada do Rio, Veja Rio Comer & Beber 2025",
            ),
            (
                "Melhor Feijoada do Rio — Veja Rio Comer & Beber 2025/2026",
                "Feijoada da Academia da Cachaça — Melhor Feijoada do Rio, Veja Rio Comer & Beber 2025",
            ),
            (
                "Feijoada premiada pela Veja Rio",
                "Feijoada premiada da Academia da Cachaça",
            ),
            (
                "Entre todas as feijoadas do Rio avaliadas pela Veja Rio Comer &amp; Beber, a da Academia da Cachaça servida na Embaixada Carioca foi eleita a melhor da cidade.",
                "A Academia da Cachaça venceu a categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025; por meio de parceria formal, essa mesma feijoada é servida na Embaixada Carioca.",
            ),
        ],
        "en": [
            (
                "Best Feijoada in Rio de Janeiro — Veja Rio Comer & Beber 2025/2026",
                "Academia da Cachaça's feijoada — Best Feijoada in Rio, Veja Rio Comer & Beber 2025",
            ),
            (
                "Melhor Feijoada do Rio de Janeiro — Revista Veja Rio Comer & Beber 2025/2026",
                "Academia da Cachaça's feijoada — Best Feijoada in Rio, Veja Rio Comer & Beber 2025",
            ),
            (
                "Feijoada premiada pela Veja Rio",
                "Award-winning feijoada from Academia da Cachaça",
            ),
        ],
        "es": [
            (
                "Mejor Feijoada de Río de Janeiro — Veja Rio Comer & Beber 2025/2026",
                "Feijoada de Academia da Cachaça — Mejor Feijoada de Río, Veja Rio Comer & Beber 2025",
            ),
            (
                "Mejor Feijoada de Río — Veja Rio Comer & Beber 2025/2026",
                "Feijoada de Academia da Cachaça — Mejor Feijoada de Río, Veja Rio Comer & Beber 2025",
            ),
            (
                "Melhor Feijoada do Rio — Veja Rio Comer & Beber 2025/2026",
                "Feijoada de Academia da Cachaça — Mejor Feijoada de Río, Veja Rio Comer & Beber 2025",
            ),
            (
                "Feijoada premiada pela Veja Rio",
                "Feijoada premiada de Academia da Cachaça",
            ),
        ],
    }
    for old, new in global_replacements[lang]:
        made = text.count(old)
        text = text.replace(old, new)
        count += made

    # A edição oficial comprovada é a de 2025. Normaliza apenas referências
    # ligadas à Veja Rio/feijoada, sem alterar anos de outros conteúdos.
    year_patterns = [
        (r"(Veja Rio(?: Comer &(?:amp;)? Beber)?(?: Award| Prêmio| Premio)?\s*)2025/2026", r"\g<1>2025"),
        (r"((?:Award-winning|Feijoada premiada|feijoada premiada) (?:feijoada )?(?:from|da|de) Academia da Cachaça\s*)2025/2026", r"\g<1>2025"),
    ]
    for pattern, replacement in year_patterns:
        text, made = re.subn(pattern, replacement, text, flags=re.I)
        count += made

    # Correções editoriais amplas para variantes introduzidas por scripts
    # antigos. Mantêm a autoria do prêmio na Academia e a disponibilidade do
    # prato na Embaixada por parceria formal.
    editorial_patterns: dict[str, list[tuple[str, str]]] = {
        "pt": [
            (
                r"A <strong>feijoada premiada da Embaixada Carioca</strong>, eleita <strong>Melhor Feijoada do Rio de Janeiro</strong> pela <strong>Veja Rio Comer &amp; Beber 2025</strong>, é feita em parceria com a <strong>Academia da Cachaça</strong>",
                "A Embaixada Carioca serve a feijoada da <strong>Academia da Cachaça</strong>, vencedora da categoria <strong>Melhor Feijoada</strong> no <strong>Veja Rio Comer &amp; Beber 2025</strong>, por meio de parceria formal",
            ),
            (
                r"da <strong>feijoada premiada</strong> — eleita <strong>Melhor Feijoada do Rio</strong> pela Veja Rio Comer &amp; Beber 2025 —",
                "da <strong>feijoada da Academia da Cachaça</strong> — vencedora da categoria <strong>Melhor Feijoada</strong> no Veja Rio Comer &amp; Beber 2025 e servida aqui por meio de parceria formal —",
            ),
            (
                r"A <strong>segunda mais vendida</strong> e a mais premiada\. Eleita a <strong>Melhor Feijoada do Rio de Janeiro</strong> pela <strong>Veja Rio Comer &amp; Beber 2025</strong>\.",
                "A <strong>segunda mais vendida</strong>: feijoada da Academia da Cachaça, vencedora da categoria <strong>Melhor Feijoada</strong> no <strong>Veja Rio Comer &amp; Beber 2025</strong>, servida aqui por meio de parceria formal.",
            ),
            (
                r"nossa <strong>Melhor Feijoada do Rio de Janeiro</strong> — Veja Rio Comer &amp; Beber 2025, em parceria com a Academia da Cachaça",
                "a <strong>feijoada da Academia da Cachaça</strong>, vencedora da categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025 e servida aqui por meio de parceria formal,",
            ),
            (
                r"A <strong>Melhor Feijoada do Rio de Janeiro</strong> — Veja Rio Comer &amp; Beber 2025, em parceria com a Academia da Cachaça —",
                "A <strong>feijoada da Academia da Cachaça</strong> — vencedora da categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025 e servida aqui por meio de parceria formal —",
            ),
            (
                r"Feijoada premiada(?: da Academia da Cachaça)? Veja Rio Comer &amp; Beber 2025",
                "Feijoada da Academia da Cachaça · Melhor Feijoada · Veja Rio Comer &amp; Beber 2025",
            ),
            (
                r"Melhor Feijoada do Rio(?: de Janeiro)? — Veja Rio Comer &amp; Beber 2025",
                "Feijoada da Academia da Cachaça — Melhor Feijoada, Veja Rio Comer &amp; Beber 2025",
            ),
        ],
        "en": [
            (
                r"Embaixada Carioca was named by <strong>Veja Rio</strong> magazine as the restaurant with the best feijoada in Rio de Janeiro\.",
                "<strong>Academia da Cachaça</strong> won Veja Rio Comer &amp; Beber's Best Feijoada category in 2025, and Embaixada Carioca serves the same feijoada through a formal partnership.",
            ),
            (
                r"serves the Best Feijoada in Rio de Janeiro — Veja Rio Comer &amp; Beber 2025, in partnership with Academia da Cachaça",
                "serves Academia da Cachaça's feijoada — winner of Veja Rio Comer &amp; Beber's Best Feijoada category in 2025 — through a formal partnership",
            ),
            (
                r"the <strong>award-winning feijoada</strong> recognised as Best in Rio by Veja Rio Comer &amp; Beber 2025",
                "<strong>Academia da Cachaça's award-winning feijoada</strong>, winner of Veja Rio Comer &amp; Beber's Best Feijoada category in 2025",
            ),
            (
                r"the <strong>award-winning feijoada</strong> — recognised as the best in Brazil —",
                "<strong>Academia da Cachaça's award-winning feijoada</strong> — winner of Veja Rio Comer &amp; Beber's Best Feijoada category in 2025 and served here through a formal partnership —",
            ),
            (
                r"full feijoada elected Award-winning feijoada from Academia da Cachaça by Veja Rio Comer &amp; Beber 2025",
                "Academia da Cachaça's feijoada, winner of Veja Rio Comer &amp; Beber's Best Feijoada category in 2025 and served here through a formal partnership",
            ),
            (
                r"Award-winning Feijoada(?: \(Veja Rio Comer &amp; Beber 2025\)| Veja Rio Comer &amp; Beber 2025)",
                "Award-winning feijoada from Academia da Cachaça · Veja Rio Comer &amp; Beber 2025",
            ),
            (
                r"(?<!from Academia da Cachaça )award-winning feijoada(?! from Academia da Cachaça)",
                "award-winning feijoada from Academia da Cachaça",
            ),
        ],
        "es": [
            (
                r"sirve la Mejor Feijoada de Río de Janeiro — Veja Rio Comer &amp; Beber 2025, en colaboración con Academia da Cachaça",
                "sirve la feijoada de Academia da Cachaça — ganadora de la categoría Mejor Feijoada de Veja Rio Comer &amp; Beber 2025 — mediante una colaboración formal",
            ),
            (
                r"(?:Elegida|elegida) <strong>Mejor Feijoada de Río de Janeiro</strong> por Veja Rio Comer &amp; Beber 2025",
                "Feijoada de <strong>Academia da Cachaça</strong>, ganadora de la categoría Mejor Feijoada de Veja Rio Comer &amp; Beber 2025",
            ),
            (
                r"(?:Elegida|elegida) Mejor Feijoada de Río de Janeiro por Veja Rio Comer & Beber 2025",
                "Feijoada de Academia da Cachaça, ganadora de la categoría Mejor Feijoada de Veja Rio Comer & Beber 2025",
            ),
            (
                r"Feijoada premiada(?: de Academia da Cachaça)? Veja Rio Comer &amp; Beber 2025",
                "Feijoada de Academia da Cachaça · Mejor Feijoada · Veja Rio Comer &amp; Beber 2025",
            ),
            (
                r"Mejor Feijoada de Río(?: de Janeiro)? — Veja Rio Comer &amp; Beber 2025",
                "Feijoada de Academia da Cachaça — Mejor Feijoada, Veja Rio Comer &amp; Beber 2025",
            ),
        ],
    }
    for pattern, replacement in editorial_patterns[lang]:
        text, made = re.subn(pattern, replacement, text, flags=re.I)
        count += made

    # Remove duplicações deixadas por substituições históricas encadeadas.
    cleanup_patterns = [
        (r"servida na Embaixada Carioca por meio de parceria formal, servida na Embaixada Carioca", "servida na Embaixada Carioca por meio de parceria formal"),
        (r"served at Embaixada Carioca through a formal partnership, served at Embaixada Carioca", "served at Embaixada Carioca through a formal partnership"),
        (r"servida en Embaixada Carioca mediante una colaboración formal, servida en Embaixada Carioca", "servida en Embaixada Carioca mediante una colaboración formal"),
        (r"feijoada premiada de Academia da Cachaça</strong> de Academia da Cachaça", "feijoada premiada de Academia da Cachaça</strong>"),
        (r"por meio de parceria formal, servida há", "por meio de parceria formal há"),
        (r"a feijoada da Embaixada Carioca chega", "a feijoada da Academia da Cachaça servida na Embaixada Carioca chega"),
        (r"<p>a feijoada da Academia da Cachaça servida na Embaixada Carioca chega", "<p>A feijoada da Academia da Cachaça servida na Embaixada Carioca chega"),
        (r"Por que a feijoada da Embaixada Carioca é diferente", "Por que a feijoada servida na Embaixada Carioca é diferente"),
        (r"Feijoada de Academia da Cachaça — Mejor Feijoada de Río, Veja Rio Comer &amp; Beber 2025, en colaboración con Academia da Cachaça", "feijoada de Academia da Cachaça — ganadora de la categoría Mejor Feijoada de Veja Rio Comer &amp; Beber 2025 y servida mediante una colaboración formal"),
        (r"feijoada da <strong>Academia da Cachaça</strong>, vencedora da categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025, servida pela <strong>Embaixada Carioca</strong> por meio de parceria formal", "feijoada da Academia da Cachaça, vencedora da categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025, servida pela Embaixada Carioca por meio de parceria formal"),
        (r"A Embaixada Carioca serve a feijoada da <strong>Academia da Cachaça</strong>, vencedora da categoria <strong>Melhor Feijoada</strong> no <strong>Veja Rio Comer &amp; Beber 2025</strong>, por meio de parceria formal", "A Embaixada Carioca serve a feijoada da Academia da Cachaça, vencedora da categoria Melhor Feijoada no Veja Rio Comer &amp; Beber 2025, por meio de parceria formal"),
    ]
    for pattern, replacement in cleanup_patterns:
        text, made = re.subn(pattern, replacement, text, flags=re.I)
        count += made

    return text, count if text != original else 0


def type_set(node: dict) -> set[str]:
    value = node.get("@type", [])
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {item for item in value if isinstance(item, str)}
    return set()


def clean_schema(node: object, lang: str, stats: dict[str, int]) -> None:
    if isinstance(node, list):
        for item in node:
            clean_schema(item, lang, stats)
        return
    if not isinstance(node, dict):
        return

    types = type_set(node)
    award = node.get("award")
    if award is not None and types & ENTITY_TYPES:
        if isinstance(award, list):
            kept = [item for item in award if not (isinstance(item, str) and AWARD_SIGNAL.search(item))]
            if len(kept) != len(award):
                stats["entity_awards_removed"] += len(award) - len(kept)
                if kept:
                    node["award"] = kept
                else:
                    del node["award"]
        elif isinstance(award, str) and AWARD_SIGNAL.search(award):
            del node["award"]
            stats["entity_awards_removed"] += 1
    elif award is not None and types & DISH_TYPES:
        if isinstance(award, str) and AWARD_SIGNAL.search(award):
            node["award"] = JSON_CANONICAL[lang]
            stats["dish_awards_normalized"] += 1
        elif isinstance(award, list):
            node["award"] = [
                JSON_CANONICAL[lang] if isinstance(item, str) and AWARD_SIGNAL.search(item) else item
                for item in award
            ]
            stats["dish_awards_normalized"] += sum(
                1 for item in award if isinstance(item, str) and AWARD_SIGNAL.search(item)
            )

    for value in node.values():
        clean_schema(value, lang, stats)


def clean_json_ld(text: str, lang: str, stats: dict[str, object], rel: str) -> str:
    def transform(match: re.Match[str]) -> str:
        raw = match.group(2).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            stats["json_errors"] += 1
            stats["json_error_files"].append(rel)
            return match.group(0)
        before = json.dumps(data, ensure_ascii=False, sort_keys=True)
        clean_schema(data, lang, stats)
        after = json.dumps(data, ensure_ascii=False, sort_keys=True)
        if before == after:
            return match.group(0)
        stats["json_blocks_changed"] += 1
        return f"{match.group(1)}\n{json.dumps(data, ensure_ascii=False, indent=2)}\n{match.group(3)}"

    return JSON_LD_RE.sub(transform, text)


def residuals(text: str) -> list[str]:
    patterns = [
        r"Embaixada Carioca.{0,160}(?:foi eleit|vencedora do prêmio|was voted|fue elegida|ganadora del premio)",
        r"Embaixada Carioca's feijoada was voted",
        r"feijoada da Embaixada Carioca.{0,120}foi eleita",
        r"feijoada de Embaixada Carioca.{0,120}fue elegida",
        r"Premiada como premiada|eleita premiada|eleita a premiada",
        r"(?:Veja Rio|feijoada|Feijoada).{0,100}2025/2026",
        r"2025/2026.{0,100}(?:Veja Rio|feijoada|Feijoada)",
        r"feijoada premiada da Embaixada Carioca",
        r"Embaixada Carioca's feijoada.{0,100}(?:named|voted|award|Best)",
        r"feijoada de Embaixada Carioca.{0,100}(?:elegida|premiada|Mejor)",
        r"servida na Embaixada Carioca.{0,100}servida na Embaixada Carioca",
        r"served at Embaixada Carioca.{0,100}served at Embaixada Carioca",
        r"servida en Embaixada Carioca.{0,100}servida en Embaixada Carioca",
        r"Eleita <strong>Melhor Feijoada",
        r"feijoada premiada Veja Rio é exclusiva da Embaixada Carioca",
    ]
    return [pattern for pattern in patterns if re.search(pattern, text, re.I | re.S)]


def main() -> int:
    changed: list[str] = []
    replacements = 0
    stats = {
        "entity_awards_removed": 0,
        "dish_awards_normalized": 0,
        "json_blocks_changed": 0,
        "json_errors": 0,
        "json_error_files": [],
    }

    for path in html_files():
        original = path.read_text(encoding="utf-8")
        lang = language(path)
        text, made = replace_copy(original, lang)
        rel = path.relative_to(ROOT).as_posix()
        text = clean_json_ld(text, lang, stats, rel)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="")
            changed.append(path.relative_to(ROOT).as_posix())
            replacements += made

    remaining: dict[str, list[str]] = {}
    for path in html_files():
        found = residuals(path.read_text(encoding="utf-8"))
        if found:
            remaining[path.relative_to(ROOT).as_posix()] = found

    status = "PASS" if not remaining and stats["json_errors"] == 0 else "FAIL"
    lines = [
        "# Padronização factual do prêmio da feijoada",
        "",
        "Data: 2026-08-23",
        f"Status geral: **{status}**",
        "",
        "## Regra canônica",
        "",
        "- A feijoada da Academia da Cachaça foi eleita Melhor Feijoada do Brasil pela revista **Prazeres da Mesa em 2017**.",
        "- A vencedora da categoria Melhor Feijoada no Veja Rio Comer & Beber 2025 é a **Academia da Cachaça**.",
        "- A Embaixada Carioca serve essa feijoada no Morro da Urca por meio de **parceria formal**.",
        "- Estrutura societária e percentuais não são publicados.",
        "",
        "## Resultado",
        "",
        f"- Arquivos HTML alterados: **{len(changed)}**",
        f"- Substituições editoriais: **{replacements}**",
        f"- Awards indevidos removidos de Restaurant/LocalBusiness/Organization: **{stats['entity_awards_removed']}**",
        f"- Awards de Recipe/MenuItem/Product normalizados: **{stats['dish_awards_normalized']}**",
        f"- Blocos JSON-LD alterados: **{stats['json_blocks_changed']}**",
        f"- Erros de parse JSON-LD: **{stats['json_errors']}**",
        f"- Arquivos com erro de parse JSON-LD: **{', '.join(sorted(set(stats['json_error_files']))) or 'nenhum'}**",
        f"- Arquivos com alegações diretas residuais: **{len(remaining)}**",
        "",
        "## Arquivos alterados",
        "",
    ]
    lines.extend(f"- `{item}`" for item in changed)
    if remaining:
        lines.extend(["", "## Resíduos", ""])
        for rel, patterns in remaining.items():
            lines.append(f"- `{rel}`: {', '.join(f'`{pattern}`' for pattern in patterns)}")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
    print(f"Feijoada award attribution: {status} changed={len(changed)} residuals={len(remaining)}")
    print(f"Report: {REPORT}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
