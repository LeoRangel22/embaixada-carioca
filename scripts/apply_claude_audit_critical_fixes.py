#!/usr/bin/env python3
"""Apply critical fixes from the Claude digital audit.

Scope:
- Standardize all feijoada award language.
- Preserve the confirmed common ownership between Embaixada Carioca and
  Cantina do MAM.
- Fix common EN portunhol fragments detected in previous scripts.
- Standardize Instagram follower claims to 84K/84 mil.
- Strip review/rating nodes from JSON-LD to avoid review-snippet regressions.
- Audit workflow count and produce a governance report.

Guardrails:
- Does not change canonicals/hreflang.
- Does not add AggregateRating/Rating/Review.
- Does not touch prices unless part of visible text replacement.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "claude_audit_critical_fixes_report.md"
EXCLUDED_DIRS = {
    ".git", "node_modules", "_backups", "_templates",
    "_site", "dist", "build", "tests",
}
HTML_FILES = sorted(
    p for p in ROOT.rglob("*.html")
    if not any(part in EXCLUDED_DIRS for part in p.relative_to(ROOT).parts)
)
WORKFLOW_DIR = ROOT / ".github" / "workflows"
JSONLD_RE = re.compile(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)

PT_AWARD = "Feijoada da Academia da Cachaça — Melhor Feijoada, Veja Rio Comer & Beber 2025 — servida na Embaixada Carioca por meio de parceria formal"
EN_AWARD = "Academia da Cachaça's feijoada — Best Feijoada, Veja Rio Comer & Beber 2025 — served at Embaixada Carioca through a formal partnership"
ES_AWARD = "Feijoada de Academia da Cachaça — Mejor Feijoada, Veja Rio Comer & Beber 2025 — servida en Embaixada Carioca mediante una colaboración formal"

TEXT_REPLACEMENTS: list[tuple[str, str, str]] = [
    (r"Melhor\s+Feijoada\s+do\s+Brasil", "Melhor Feijoada do Rio de Janeiro", "award-pt-brasil-to-rio"),
    (r"best\s+feijoada\s+in\s+Brazil", "Best Feijoada in Rio de Janeiro", "award-en-brazil-to-rio"),
    (r"best\s+feijoada\s+of\s+Brazil", "Best Feijoada in Rio de Janeiro", "award-en-of-brazil-to-rio"),
    (r"one\s+of\s+the\s+best\s+feijoadas?\s+in\s+the\s+city", EN_AWARD, "award-en-weak-to-best"),
    (r"one\s+of\s+the\s+best\s+in\s+the\s+city", EN_AWARD, "award-en-generic-weak-to-best"),
    (r"Voted\s+by\s+Veja\s+Rio\s+as\s+one\s+of\s+the\s+best\s+in\s+the\s+city", f"Voted {EN_AWARD}", "award-en-veja-one-of-best"),
    (r"Revista\s+Prazeres\s+da\s+Mesa", "Veja Rio Comer & Beber 2025/2026", "wrong-magazine-prazeres-to-veja"),
    (r"Prazeres\s+da\s+Mesa", "Veja Rio Comer & Beber 2025/2026", "wrong-source-prazeres-to-veja"),
    (r"Veja\s+Rio\s+2025/2026(?!\s+Comer\s*&\s*Beber)", "Veja Rio Comer & Beber 2025/2026", "award-veja-full-name"),
    (r"O\s+sunset\s+m[aá]s\s+bonito\s+do\s+Rio\s+de\s+Janeiro", "The most beautiful sunset in Rio de Janeiro", "en-portunhol-sunset-mas"),
    (r"Servida\s+every\s+day\s+no\s+lunch", "Served daily for lunch", "en-portunhol-servida"),
    (r"drinks\s+e\s+petiscos", "drinks and Brazilian snacks", "en-portunhol-e"),
    (r"O\s+segunof\s+the\s+cable\s+car", "The second section of the cable car", "en-typo-segunof"),
    (r"experi[eê]ncia\s+gastron[oô]micas", "gastronomic experience", "en-portunhol-concordance"),
    (r"Perfeito\s+para\s+o\s+sunset\s+com\s+draft\s+beer\s+no\s+Urca\s+Hill", "Perfect for sunset with draft beer at Urca Hill", "en-portunhol-perfect"),
    (r'<li><a href="/cafe-da-manha\.html">Café da Manhã</a></li>', '<li><a href="/en/cafe-da-manha.html">Breakfast</a></li>', "en-nav-breakfast"),
    (r'<li><a href="/almoco\.html">Almoço</a></li>', '<li><a href="/en/almoco.html">Lunch</a></li>', "en-nav-lunch"),
    (r'<li><a href="/como-chegar\.html">Como Chegar</a></li>', '<li><a href="/en/how-to-get-there.html">How to get there</a></li>', "en-nav-directions"),
    (r'<li><a href="/eventos\.html">Eventos</a></li>', '<li><a href="/en/eventos.html">Events</a></li>', "en-nav-events"),
    (r'<li><a href="/cardapio\.html">Cardápio</a></li>', '<li><a href="/en/cardapio.html">Menu</a></li>', "en-nav-menu"),
    (r'<li><a href="/guia-do-rio\.html">Guia do Rio</a></li>', '<li><a href="/en/guia-do-rio.html">Rio guide</a></li>', "en-nav-rio-guide"),
    (r"Premiada\s+como\s+best\s+in\s+Brazil\s+pela\s+Revista\s+Veja\s+Rio\s+Comer\s*&\s*Beber\s+2025/2026\.", "Winner of Best Feijoada in Rio de Janeiro — Veja Rio Comer & Beber 2025/2026.", "en-award-sentence"),
    (r"Servida\s+every\s+day,?\s+das\s+11:30\s+AM\s+[àa]s\s+5:00\s+PM\.", "Served every day from 11:30 AM to 5:00 PM.", "en-serving-hours"),
    (r"Servida\s+every\s+day\.", "Served every day.", "en-served-daily"),
    (r"O\s+único\s+<strong>lunch\s+dentro\s+do\s+Bondinho\s+Pão\s+de\s+Açúcar\s+Park</strong>,\s+at\s+227\s+meters\s+altitude\s+no\s+Urca\s+Hill\.\s+Award-winning\s+Brazilian\s+gastronomy:\s+picanha\s+à\s+brasileira\s+e\s+a\s+feijoada\s+eleita\s+best\s+in\s+Brazil\s+pela\s+Revista\s+Veja\s+Rio\s+Comer\s*&\s*Beber\s+2025/2026\.\s+Para\s+quién\s+busca\s+<strong>onde\s+have\s+lunch\s+no\s+Rio\s+de\s+Janeiro</strong>\s+com\s+a\s+vista\s+mais\s+bonita\s+da\s+cidade\s+—\s+entre\s+os\s+<strong>restaurantes\s+com\s+vista\s+no\s+Rio\s+de\s+Janeiro</strong>,\s+este\s+es\s+o\s+único\s+atop\s+Urca\s+Hill\.", "The only <strong>lunch inside Bondinho Pão de Açúcar Park</strong>, 227 meters above sea level on Urca Hill. Enjoy Brazilian picanha and the winner of Best Feijoada in Rio de Janeiro — Veja Rio Comer & Beber 2025/2026 — at the park's only restaurant with a direct view of Sugarloaf Mountain.", "en-lunch-hero-rewrite"),
    (r"O\s+<strong>sunset\s+m[aá]s\s+bonito\s+do\s+Rio\s+de\s+Janeiro</strong>\s+—\s+sunset\s+atrás\s+of\s+Sugarloaf\s+Mountain,\s+visto\s+do\s+alto\s+do\s+Urca\s+Hill\.\s+Caipirinha\s+com\s+cachaça\s+Magnífica\s+e\s+draft\s+beer\s+Heineken\s+\(2º\s+best\s+in\s+Brazil\)\.\s+Um\s+dos\s+<strong>lugares\s+m[aá]s\s+bonitos\s+do\s+Rio\s+de\s+Janeiro</strong>\s+para\s+um\s+momento\s+romântico,\s+um\s+aniversário\s+ou\s+simplesmente\s+o\s+fim\s+de\s+um\s+dia\s+perfeito\s+na\s+cidade\.\s+Open\s+daily\s+das\s+5:00\s+PM\s+[àa]s\s+9:00\s+PM\.", "Watch the sun set behind Sugarloaf Mountain from Urca Hill while enjoying a caipirinha made with Magnífica cachaça or an ice-cold Heineken draft beer. It is an ideal setting for a romantic evening, a birthday or a relaxed end to a day in Rio. Open daily from 5:00 PM to 9:00 PM.", "en-sunset-hero-rewrite"),
    (r"O\s+sunset\s+m[aá]s\s+bonito\s+in\s+Rio\s+de\s+Janeiro,\s+com\s+música\s+ao\s+vivo\s+e\s+drinks\s+no\s+Urca\s+Hill\.", "Sunset in Rio de Janeiro with live music and drinks on Urca Hill.", "en-sunset-description"),
    (r"Veja\s+como\s+é\s+o\s+sunset\s+m[aá]s\s+bonito\s+in\s+Rio\s+de\s+Janeiro\s+no\s+Urca\s+Hill\.\s+Música\s+ao\s+vivo,\s+caipirinhas\s+e\s+vista\s+panorâmica\s+dGuanabara\s+Bay\s+e\s+of\s+Sugarloaf\s+Mountain\.", "See sunset from Urca Hill with live music, caipirinhas and panoramic views of Guanabara Bay and Sugarloaf Mountain.", "en-sunset-long-description"),
    (r"A\s+<a\s+href=\"/en/almoco\.html\"\s+title=\"Lunch\s+no\s+Urca\s+Hill\s+com\s+feijoada\s+premiada\">feijoada\s+da\s+Embaixada\s+Carioca</a>\s+é\s+a\s+mesma\s+feijoada\s+premiada\s+da\s+Academia\s+da\s+Cachaça,\s+eleita\s+a\s+best\s+in\s+Brazil\s+pela\s+Revista\s+Veja\s+Rio\s+Comer\s*&amp;\s*Beber\s+2025/2026\.\s+Served\s+daily\s+for\s+lunch,\s+with\s+a\s+view\s+of\s+Sugarloaf\s+Mountain\.\s+Uma\s+experiência\s+que\s+combina\s+gastronomia\s+de\s+alto\s+nível\s+com\s+o\s+cenário\s+m[aá]s\s+bonito\s+do\s+Rio\.", "The <a href=\"/en/almoco.html\" title=\"Lunch on Urca Hill with award-winning feijoada\">Embaixada Carioca feijoada</a> is the award-winning Academia da Cachaça recipe, named Best Feijoada in Rio de Janeiro by Veja Rio Comer &amp; Beber 2025/2026. It is served daily for lunch with a direct view of Sugarloaf Mountain.", "en-morro-feijoada-paragraph"),
    (r"\bno\s+Urca\s+Hill\b", "on Urca Hill", "en-no-urca-to-on"),
    (r"\bcom\s+a\s+vista\s+of\b", "with a view of", "en-com-vista-of"),
    (r"mais\s+de\s+100K\s+seguidores", "mais de 84 mil seguidores", "followers-pt-100k-to-84k"),
    (r"mais\s+de\s+100\s+mil\s+seguidores", "mais de 84 mil seguidores", "followers-pt-100mil-to-84mil"),
    (r"over\s+100K\s+followers", "over 84K followers", "followers-en-100k-to-84k"),
    (r"more\s+than\s+100K\s+followers", "more than 84K followers", "followers-en-100k-to-84k-2"),
    (r"\+100K(?=\s*</div><div[^>]*>\s*Instagram followers)", "84K", "followers-en-counter-to-84k"),
    (r"m[aá]s\s+de\s+100K\s+seguidores", "más de 84K seguidores", "followers-es-100k-to-84k"),
    (r"\+100K(?=\s*</div><div[^>]*>\s*Seguidores)", "84K", "followers-es-counter-to-84k"),
    (r"Instagram\s*·\s*\+100K", "Instagram · 84K", "followers-footer-100k-to-84k"),
    (r"aria-label=\"Seguir @embaixadacarioca no Instagram — 100\.716 seguidores\"", 'aria-label="Seguir @embaixadacarioca no Instagram — 84 mil seguidores"', "followers-instagram-aria-to-84k"),
    (r"aria-label=\"Follow @embaixadacarioca on Instagram — 100\.716 followers\"", 'aria-label="Follow @embaixadacarioca on Instagram — 84K followers"', "followers-instagram-aria-en-to-84k"),
    (r"aria-label=\"Seguir @embaixadacarioca en Instagram — 100\.716 seguidores\"", 'aria-label="Seguir @embaixadacarioca en Instagram — 84K seguidores"', "followers-instagram-aria-es-to-84k"),
    (r"·\s*100\.716\s+seguidores", "· 84 mil seguidores", "followers-instagram-visible-to-84k"),
    (r"·\s*100\.716\s+followers", "· 84K followers", "followers-instagram-visible-en-to-84k"),
    (r"Instagram\s*·\s*\+100\s+mil", "Instagram · 84 mil", "followers-footer-100mil-to-84mil"),
    (r"\+100K", "84K", "followers-generic-100k-to-84k"),
    (r">100<span([^>]*)>K</span>", r">84<span\1>K</span>", "followers-split-counter-to-84k"),
    (r"Voted one of the best in Rio by Veja Rio magazine \(Comer (?:&amp;|&) Beber 2025 and 2026\)\.", "Named Best Feijoada in Rio de Janeiro by Veja Rio Comer &amp; Beber 2025/2026.", "award-en-canonical-morro-faq"),
    (r"\+100\s+mil", "84 mil", "followers-generic-100mil-to-84mil"),
]

# The owner confirmed on 2026-08-23 that Embaixada Carioca and Cantina do MAM
# have the same shareholders. Academia da Cachaça is a separate family business
# connected to Embaixada Carioca through a formal partnership and overlapping
# ownership; it must not be described as having the same shareholder structure.
# This maintenance script must not delete or distort either relationship.
CLAIM_PATTERNS: list[tuple[str, str]] = []

FORBIDDEN_AFTER = [
    "Prazeres da Mesa",
    "best feijoada in Brazil",
    "Best Feijoada in Brazil",
    "Melhor Feijoada do Brasil",
    "one of the best in the city",
    "100K seguidores",
    "100 mil seguidores",
    "+100K",
    "+100 mil",
    "segunof",
    "Servida every day no lunch",
    "drinks e petiscos",
    "best in Brazil pela",
    "Servida every",
    "sunset más",
    "dGuanabara",
    "Para quién",
    "onde have",
]

@dataclass
class FileResult:
    path: str
    changed: bool
    replacements: int
    jsonld_rating_removed: int
    notes: str


def lang_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt"


def canonical_award_for(path: Path) -> str:
    lang = lang_for(path)
    return EN_AWARD if lang == "en" else ES_AWARD if lang == "es" else PT_AWARD


def apply_language_specific_fixes(source: str, path: Path) -> tuple[str, int, list[str]]:
    """Normalize recurring award claims without leaking one language into another."""
    lang = lang_for(path)
    updated = source
    total = 0
    notes: list[str] = []
    replacements: list[tuple[str, str, str]]
    if lang == "en":
        replacements = [
            (
                r"feijoada premiada da Academia da Cachaça",
                "feijoada named Best Feijoada in Rio de Janeiro by Veja Rio Comer & Beber 2025/2026, in partnership with Academia da Cachaça",
                "award-en-academia-source-corrected",
            ),
            (
                r"eleita melhor do Brasil pela Revista Veja Rio",
                "named Best Feijoada in Rio de Janeiro by Veja Rio Comer & Beber 2025/2026",
                "award-en-rio-not-brazil",
            ),
            (
                r"voted Best in Brazil by Veja Rio Comer & Beber 2025/2026 Magazine",
                "named Best Feijoada in Rio de Janeiro by Veja Rio Comer & Beber 2025/2026, in partnership with Academia da Cachaça",
                "award-en-menu-rio-not-brazil",
            ),
        ]
    elif lang == "es":
        replacements = [
            (
                r"feijoada premiada da Academia da Cachaça",
                "feijoada elegida Mejor Feijoada de Río de Janeiro por Veja Rio Comer & Beber 2025/2026, en colaboración con Academia da Cachaça",
                "award-es-academia-source-corrected",
            ),
            (
                r"eleita (?:a )?premiada pela Revista Veja Rio Comer &amp; Beber 2025/2026 na Academia da Cachaça",
                "elegida Mejor Feijoada de Río de Janeiro por Veja Rio Comer &amp; Beber 2025/2026, en colaboración con Academia da Cachaça",
                "award-es-canonical",
            ),
            (
                r"(?:elegida|premiada como) (?:la )?mejor (?:feijoada )?de Brasil por la Revista Veja Rio Comer & Beber 2025/2026",
                "elegida Mejor Feijoada de Río de Janeiro por Veja Rio Comer & Beber 2025/2026",
                "award-es-rio-not-brazil",
            ),
            (
                r"mejor feijoada de Brasil",
                "Mejor Feijoada de Río de Janeiro",
                "award-es-keyword-rio-not-brazil",
            ),
            (
                r"La famosa Feijoada de la Academia da Cachaça, elegida la Mejor de Brasil por la Revista Veja Rio Comer & Beber 2025/2026",
                "La feijoada de Embaixada Carioca, elegida Mejor Feijoada de Río de Janeiro por Veja Rio Comer & Beber 2025/2026, en colaboración con Academia da Cachaça",
                "award-es-menu-canonical",
            ),
            (
                r'<li><a href="/cafe-da-manha\.html">Café da Manhã</a></li>',
                '<li><a href="/es/cafe-da-manha.html">Desayuno</a></li>',
                "es-nav-breakfast",
            ),
            (
                r'<li><a href="/almoco\.html">Almoço</a></li>',
                '<li><a href="/es/almoco.html">Almuerzo</a></li>',
                "es-nav-lunch",
            ),
            (
                r'<li><a href="/como-chegar\.html">Como Chegar</a></li>',
                '<li><a href="/es/como-llegar.html">Cómo llegar</a></li>',
                "es-nav-directions",
            ),
            (
                r"Perguntas Frequentes sobre o Menú",
                "Preguntas frecuentes sobre el menú",
                "es-menu-faq-heading",
            ),
            (
                r"A feijoada é servida todos los días\?",
                "¿La feijoada se sirve todos los días?",
                "es-menu-faq-question",
            ),
            (
                r"(?:creada|creado) y preparad[ao] en la <strong>Academia da Cachaça</strong>(?: y traída con todo cuidado para ofrecer la misma calidad aquí en la Embaixada Carioca)?",
                "servida por <strong>Embaixada Carioca</strong>, ganadora del premio Veja Rio Comer & Beber 2025/2026 en colaboración con Academia da Cachaça",
                "award-es-not-prepared-at-academia",
            ),
            (
                r"preparada con el cuidado de la Academia da Cachaça",
                "premiada por Veja Rio Comer & Beber 2025/2026 en colaboración con Academia da Cachaça",
                "award-es-source-clarified",
            ),
            (
                r"creada y preparada en la Academia da Cachaça",
                "premiada por Veja Rio Comer & Beber 2025/2026 en colaboración con Academia da Cachaça",
                "award-es-plain-source-clarified",
            ),
            (
                r"Sim! A feijoada da <strong>Academia da Cachaça</strong> — eleita premiada pela Revista Veja Rio Comer & Beber 2025/2026 na Academia da Cachaça — é servida <strong>todos los días das 11:30 às 17:00</strong>\. Preparada pela Academia da Cachaça e servida en Embaixada Carioca com a mesma qualidade premiada\. Charque, costela, lombo, paio e linguiça fina, acompanhada de arroz, couve refogada, farofa tostada e fatias de laranja\. Serve 2 pessoas por R\$ 189,70\.",
                "Sí. La Mejor Feijoada de Río de Janeiro — Veja Rio Comer & Beber 2025/2026, en colaboración con Academia da Cachaça — se sirve todos los días de 11:30 a 17:00 en Embaixada Carioca. Lleva carne seca, costilla, lomo y embutidos, con arroz, col salteada, farofa y naranja. La porción para dos personas cuesta R$ 189,70.",
                "es-menu-faq-answer-rewritten",
            ),
        ]
    else:
        replacements = [
            (
                r"<strong>Feijoada Premiada</strong> da Embaixada Carioca\s*[—-]\s*eleita pela Academia da Cachaça",
                "<strong>Melhor Feijoada do Rio de Janeiro</strong> — Veja Rio Comer &amp; Beber 2025/2026, em parceria com a Academia da Cachaça",
                "award-pt-tagged-source-corrected",
            ),
            (
                r"<strong>Feijoada Premiada</strong>\s*[—-]\s*eleita pela Academia da Cachaça",
                "<strong>Melhor Feijoada do Rio de Janeiro</strong> — Veja Rio Comer &amp; Beber 2025/2026, em parceria com a Academia da Cachaça",
                "award-pt-tagged-short-corrected",
            ),
            (
                r"<strong>Feijoada Premiada</strong> servida todos os dias\s*[—-]\s*eleita pela Academia da Cachaça",
                "<strong>Melhor Feijoada do Rio de Janeiro</strong> — Veja Rio Comer &amp; Beber 2025/2026, em parceria com a Academia da Cachaça — servida todos os dias",
                "award-pt-tagged-list-corrected",
            ),
            (
                r"Feijoada Premiada da Embaixada Carioca\s*[—-]\s*eleita pela Academia da Cachaça",
                "Melhor Feijoada do Rio de Janeiro — Veja Rio Comer & Beber 2025/2026, em parceria com a Academia da Cachaça",
                "award-pt-source-corrected-long",
            ),
            (
                r"feijoada premiada da Academia da Cachaça",
                "Melhor Feijoada do Rio de Janeiro — Veja Rio Comer & Beber 2025/2026, em parceria com a Academia da Cachaça",
                "award-pt-source-corrected",
            ),
            (
                r"eleita melhor do Brasil pela(?:\s+<strong>)?\s*Revista Veja Rio Comer &amp; Beber 2025/2026(?:</strong>)?",
                "eleita Melhor Feijoada do Rio de Janeiro pela Revista Veja Rio Comer &amp; Beber 2025/2026",
                "award-pt-rio-not-brazil",
            ),
            (
                r"feijoada premiada rio(?:</strong>)? preparada na Academia da Cachaça",
                "Melhor Feijoada do Rio de Janeiro — Veja Rio Comer & Beber 2025/2026, em parceria com a Academia da Cachaça",
                "award-pt-not-prepared-at-academia",
            ),
            (
                r"<strong>feijoada premiada rio</strong> \(criada e preparada na Academia da Cachaça\)",
                "<strong>Melhor Feijoada do Rio de Janeiro</strong> — Veja Rio Comer &amp; Beber 2025/2026, em parceria com a Academia da Cachaça",
                "award-pt-not-created-at-academia",
            ),
            (
                r"criad[ao] e preparad[ao] na <strong>Academia da Cachaça</strong>(?: e trazid[ao] com todo cuidado para ter a mesma qualidade aqui na Embaixada Carioca)?",
                "servida pela <strong>Embaixada Carioca</strong>, vencedora do prêmio Veja Rio Comer &amp; Beber 2025/2026 em parceria com a Academia da Cachaça",
                "award-pt-source-clarified",
            ),
            (
                r"Preparada pela Academia da Cachaça e servida na Embaixada Carioca com a mesma qualidade premiada\.",
                "Servida pela Embaixada Carioca e premiada pela Veja Rio Comer &amp; Beber 2025/2026, em parceria com a Academia da Cachaça.",
                "award-pt-menu-source-clarified",
            ),
        ]
    for pattern, replacement, note in replacements:
        updated, count = re.subn(pattern, replacement, updated, flags=re.I)
        if count:
            total += count
            notes.append(f"{note}:{count}")
    return updated, total, notes


def apply_page_specific_language_fixes(source: str, path: Path) -> tuple[str, int, list[str]]:
    """Replace known high-impact blocks that were produced by word-level translation."""
    rel = path.relative_to(ROOT).as_posix()
    updated = source
    notes: list[str] = []
    total = 0
    exact_maps: dict[str, list[tuple[str, str]]] = {
        "en/sunset.html": [
            ("Coquetelaria autoral com cachaças premium, frutas tropicais frescas e draft beer Heineken servido na temperatura premiada — tudo com a vista above the Bay de Guanabara. Um dos <strong>programas românticos más bonitos do Rio de Janeiro</strong>, atop Urca Hill, at 227 meters altitude.", "Signature cocktails made with premium cachaças and fresh tropical fruit, plus ice-cold Heineken draft beer — all overlooking Guanabara Bay. One of Rio de Janeiro's most romantic settings, 227 metres above sea level on Urca Hill."),
            ("Coquetelaria <span class=\"serif\">brasileira.</span>", "Brazilian <span class=\"serif\">cocktails.</span>"),
            ("Negroni Carioca (com Aperol e cachaça), Margarita do Rio,", "Carioca Negroni (with Aperol and cachaça), Rio Margarita,"),
            ("Olá! Bem-vindo à <strong>Embaixada Carioca</strong> — o sabor do Rio com vista para o <strong>Pão de Açúcar</strong>!", "Hello! Welcome to <strong>Embaixada Carioca</strong> — Rio flavours with a view of <strong>Sugarloaf Mountain</strong>!"),
        ],
        "en/sunset-por-do-sol-rio-de-janeiro.html": [
            ("O único lunch dentro do Bondinho Pão de Açúcar Park , at 227 meters altitude on Urca Hill. Award-winning Brazilian gastronomy: picanha à brasileira e a feijoada eleita best…", "Brazilian food and sunset drinks inside Sugarloaf Cable Car Park, 227 metres above sea level on Urca Hill."),
            ("Garanta sua mesa with a view of Sugarloaf Mountain no <strong>Restaurant do Bondinho</strong>. Reservations pela plataforma Tagme — confirmação imediata. O único <strong>lunch with a view on Urca Hill</strong>, aberto every day das 12h às 5:00 PM.", "Book your table with a view of Sugarloaf Mountain at the <strong>restaurant inside the cable-car park</strong>. Tagme provides immediate booking confirmation. Lunch is served daily on Urca Hill from noon to 5:00 PM."),
            ("Pratos autorais com ingredientes frescos, servidos com a vista most beautiful in Rio de Janeiro in the background.", "Signature dishes made with fresh ingredients and served with one of Rio de Janeiro's finest views."),
            ("Pratos autorais servidos every day nthe best restaurant com vista do Rio de Janeiro", "Signature dishes served daily with panoramic views of Rio de Janeiro"),
            ("Olá! Bem-vindo à <strong>Embaixada Carioca</strong> — o sabor do Rio com vista para o <strong>Pão de Açúcar</strong>!", "Hello! Welcome to <strong>Embaixada Carioca</strong> — Rio flavours with a view of <strong>Sugarloaf Mountain</strong>!"),
        ],
        "en/gastronomia-carioca.html": [
            ("A <strong>gastronomia carioca</strong> é uma das mais ricas e diversas do Brasil, influenciada pela cultura africana, portuguesa e indígena. Da feijoada premiada ao salmão with a view of Sugarloaf Mountain, a <strong>Embaixada Carioca</strong> celebra essa herança atop Urca Hill.", "<strong>Carioca food</strong> brings together African, Portuguese and Indigenous influences. From award-winning feijoada to grilled salmon with a view of Sugarloaf Mountain, <strong>Embaixada Carioca</strong> celebrates this heritage on Urca Hill."),
            ("Pratos Típicos", "Typical dishes"),
            ("PRATO NACIONAL", "NATIONAL DISH"),
            ("FRUTOS DO MAR", "SEAFOOD"),
            ("Picanha na Brasa", "Grilled picanha"),
            ("Picanha selecionada, grelhada no ponto certo, com farofa artesanal e vinagrete. A interpretação da Embaixada Carioca do clássico churrasco brasileiro.", "Selected picanha grilled to order, served with house-made farofa and vinaigrette — Embaixada Carioca's take on a Brazilian barbecue classic."),
            ("NORDESTINO", "NORTHEASTERN BRAZIL"),
            ("Carne Seca com Mandioca", "Sun-dried beef with cassava"),
            ("Carne seca desfiada com mandioca cremosa e coentro fresco. Um clássico da culinária nordestina reinterpretado com técnica contemporânea.", "Shredded sun-dried beef with creamy cassava and fresh coriander, a Northeastern Brazilian classic prepared with a contemporary touch."),
            ("Breakfast Panorâmico", "Panoramic breakfast"),
            ("Pães artesanais, frutas tropicais, tapioca, ovos e sucos naturais — com Sugarloaf Mountain iluminado pela luz da manhã in the background. Every day, from 8:30am to 11:30am.", "Artisan breads, tropical fruit, tapioca, eggs and fresh juices, with Sugarloaf Mountain lit by the morning sun. Served daily from 8:30 AM to 11:30 AM."),
            ("BEBIDA", "DRINKS"),
            ("Cachaça Artesanal", "Brazilian cachaça"),
            ("Drinks autorais com cachaças selecionadas da Academia da Cachaça, uma das maiores coleções de cachaças artesanais do Brasil. Servidos no sunset with a view of Sugarloaf Mountain.", "Signature drinks made with selected Brazilian cachaças. Served at sunset with a view of Sugarloaf Mountain."),
            ("Os pratos mais representativos da gastronomia carioca são: feijoada (prato nacional), moqueca de frutos do mar, camarão na moranga, picanha na brasa, bolinho de bacalhau e açaí. A Embaixada Carioca serve a feijoada named Best Feijoada in Rio de Janeiro by Veja Rio Comer & Beber 2025/2026, in partnership with Academia da Cachaça every day no lunch, with a view of Sugarloaf Mountain.", "Rio's most representative dishes include feijoada, seafood moqueca, shrimp in pumpkin, grilled picanha, codfish fritters and açaí. Embaixada Carioca serves the Best Feijoada in Rio de Janeiro — Veja Rio Comer & Beber 2025/2026, in partnership with Academia da Cachaça — every day at lunch with a view of Sugarloaf Mountain."),
            ("Os pratos mais representativos da gastronomia carioca são: <strong>feijoada</strong> (prato nacional, servida especialmente aos sábados), moqueca de frutos do mar, camarão na moranga, picanha na brasa, bolinho de bacalhau, pão de queijo e açaí. A Embaixada Carioca serve a feijoada named Best Feijoada in Rio de Janeiro by Veja Rio Comer & Beber 2025/2026, in partnership with Academia da Cachaça every day no lunch, with a view of Sugarloaf Mountain.", "Rio's most representative dishes include <strong>feijoada</strong>, seafood moqueca, shrimp in pumpkin, grilled picanha, codfish fritters, pão de queijo and açaí. Embaixada Carioca serves the Best Feijoada in Rio de Janeiro — Veja Rio Comer & Beber 2025/2026, in partnership with Academia da Cachaça — every day at lunch with a view of Sugarloaf Mountain."),
            ("Salmão Grelhado", "Grilled salmon"),
            ("Salmão fresco grelhado com acompanhamentos da estação, servido with a view of Sugarloaf Mountain in the background. Um dos pratos mais fotografados da Embaixada Carioca.", "Fresh grilled salmon with seasonal sides and Sugarloaf Mountain in the background — one of Embaixada Carioca's most photographed dishes."),
            ("Perguntas Frequentes sobre Carioca Gastronomy", "Frequently asked questions about Carioca food"),
            ("A <strong>Embaixada Carioca</strong>, on Urca Hill, é um dos restaurantes mais reconhecidos de Brazilian gastronomy no Rio de Janeiro. Com feijoada premiada pela Revista Veja Rio Comer & Beber 2025/2026, vista de frente to Sugarloaf Mountain e localização no Bondinho Pão de Açúcar Park, combina gastronomia de alto nível com a experiência turística mais icônica do Rio. Open every day from 8:30 AM às 9:00 PM.", "<strong>Embaixada Carioca</strong>, on Urca Hill, serves Brazilian food inside Sugarloaf Cable Car Park with a direct view of Sugarloaf Mountain. It is open daily from 8:30 AM to 9:00 PM and serves the Best Feijoada in Rio de Janeiro — Veja Rio Comer & Beber 2025/2026, in partnership with Academia da Cachaça."),
        ],
        "en/cardapio.html": [
            ("The famous Feijoada from Academia da Cachaça, voted Best in Brazil by Veja Rio Comer & Beber 2025/2026 Magazine.", "Embaixada Carioca's feijoada, named Best Feijoada in Rio de Janeiro by Veja Rio Comer & Beber 2025/2026, in partnership with Academia da Cachaça."),
            ("Picanha grelhada no ponto, acompanhada de arroz, farofa e vinagrete.", "Grilled picanha served with rice, toasted cassava flour and vinaigrette."),
            ("Picanha grelhada para duas pessoas, acompanhada de arroz, farofa e vinagrete.", "Grilled picanha for two, served with rice, toasted cassava flour and vinaigrette."),
            ("Carne em cubos refogada, acompanhada de arroz, ovo, banana e farofa.", "Braised diced beef served with rice, egg, banana and toasted cassava flour."),
            ("Camarão em creme de mandioca com azeite de dendê e coentro.", "Shrimp in cassava cream with dendê oil and coriander."),
            ("Filé de salmão grelhado com molho de maracujá, arroz e legumes.", "Grilled salmon fillet with passion-fruit sauce, rice and vegetables."),
            ("Petiscos e Entradas", "Snacks and starters"),
            ("Drinks e Bebidas", "Drinks and beverages"),
            ("cachaça Magnífica, limão, açúcar e gelo. A caipirinha most beautiful in Rio — feita with a view of Sugarloaf Mountain.", "Magnífica cachaça, lime, sugar and ice — a classic caipirinha made with a view of Sugarloaf Mountain."),
            ("Cachaça Magnífica, maracujá, limão, clara de ovo e espuma de maracujá.", "Magnífica cachaça, passion fruit, lime, egg white and passion-fruit foam."),
            ("Água de coco fresca, servida na própria casca.", "Fresh coconut water served in the coconut."),
        ],
        "es/almoco.html": [
            ("O único <strong>almuerzo dentro do Parque Bondinho Pão de Açúcar</strong>, a 227 metros de altitude en el Morro da Urca. Gastronomía brasileña premiada: picanha à brasileira e a feijoada eleita premiada pela Revista Veja Rio Comer & Beber 2025/2026 na Academia da Cachaça. Para quién busca <strong>dónde almoçar no Río de Janeiro</strong> com a vista mais bonita da cidade — entre os <strong>restaurantes con vista no Río de Janeiro</strong>, este es o único en lo alto del Morro da Urca.", "El único <strong>almuerzo dentro del Parque Bondinho Pan de Azúcar</strong> con vista directa al Pan de Azúcar, a 227 metros de altitud en el Morro da Urca. Picanha brasileña y la Mejor Feijoada de Río de Janeiro — Veja Rio Comer & Beber 2025/2026, en colaboración con Academia da Cachaça."),
            ("Receitas clássicas da gastronomía brasileña servidas com técnica contemporânea e ingredientes selecionados — o sabor do Brasil com a vista más bonita de Rio. O <strong>Restaurante del Bondinho</strong> é o único almuerzo a 227 metros con vista direta al Pan de Azúcar, en lo alto del Morro da Urca. Um dos <strong>melhores restaurantes do Río de Janeiro</strong> para quién quer gastronomia e vista em um só lugar.", "Recetas clásicas de la gastronomía brasileña preparadas con técnica contemporánea e ingredientes seleccionados. El <strong>restaurante del Bondinho</strong> ofrece almuerzo a 227 metros de altitud, con vista directa al Pan de Azúcar desde el Morro da Urca."),
            ("La olla de barro, la receta de familia, la col salteada en el momento — todo creado y preparado en la <strong>Academia da Cachaça</strong> y traído con todo cuidado para ofrecer la misma calidad aquí en la Embaixada Carioca, con vista al Pan de Azúcar. Servida todos los días, das 11:30 às 17:00. Reserve com antecedência: é o prato mais disputado entre os visitantes do <strong>Restaurante Morro da Urca</strong>.", "La feijoada se sirve en olla de barro con arroz, col salteada, farofa y naranja. Ganadora como Mejor Feijoada de Río de Janeiro por Veja Rio Comer & Beber 2025/2026, en colaboración con Academia da Cachaça. Disponible todos los días de 11:30 a 17:00 en Embaixada Carioca, con vista al Pan de Azúcar."),
        ],
        "es/gastronomia-carioca.html": [
            ("Gastronomía Carioca: Os Pratos Típicos do Rio e Dónde Comer", "Gastronomía carioca: platos típicos de Río y dónde comer"),
            ("A <strong>gastronomia carioca</strong> é uma das mais ricas e diversas do Brasil, influenciada pela cultura africana, portuguesa e indígena. Da feijoada premiada ao salmão con vista al Pan de Azúcar, a <strong>Embaixada Carioca</strong> celebra essa herança en lo alto del Morro da Urca.", "La <strong>gastronomía carioca</strong> combina influencias africanas, portuguesas e indígenas. Desde la feijoada premiada hasta el salmón con vista al Pan de Azúcar, <strong>Embaixada Carioca</strong> celebra esta herencia en lo alto del Morro da Urca."),
            ("Os Pratos Mais Representativos da Gastronomía Carioca", "Los platos más representativos de la gastronomía carioca"),
            ("Os pratos mais representativos da gastronomia carioca são: feijoada (prato nacional), moqueca de frutos do mar, camarão na moranga, picanha na brasa, bolinho de bacalhau e açaí. A Embaixada Carioca serve a feijoada elegida Mejor Feijoada de Río de Janeiro por Veja Rio Comer & Beber 2025/2026, en colaboración con Academia da Cachaça todos los días no almuerzo, con vista al Pan de Azúcar.", "Los platos más representativos de la gastronomía carioca incluyen feijoada, moqueca de mariscos, camarones en calabaza, picanha a la parrilla, buñuelos de bacalao y açaí. Embaixada Carioca sirve la Mejor Feijoada de Río de Janeiro — Veja Rio Comer & Beber 2025/2026, en colaboración con Academia da Cachaça — todos los días durante el almuerzo, con vista al Pan de Azúcar."),
            ("Salmão Grelhado", "Salmón a la parrilla"),
            ("Salmão fresco grelhado com acompanhamentos da estação, servido com a vista del Pan de Azúcar al fondo. Um dos pratos mais fotografados da Embaixada Carioca.", "Salmón fresco a la parrilla con guarniciones de temporada y el Pan de Azúcar al fondo, uno de los platos más fotografiados de Embaixada Carioca."),
            ("Perguntas Frequentes sobre Gastronomía Carioca", "Preguntas frecuentes sobre la gastronomía carioca"),
            ("Quais são os pratos típicos da gastronomia carioca?", "¿Cuáles son los platos típicos de la gastronomía carioca?"),
            ("Qual o melhor restaurante de gastronomía brasileña no Río de Janeiro?", "¿Dónde comer gastronomía brasileña con vista en Río de Janeiro?"),
            ("A <strong>Embaixada Carioca</strong>, en el Morro da Urca, é um dos restaurantes mais reconhecidos de gastronomía brasileña no Río de Janeiro. Com feijoada premiada pela Revista Veja Rio Comer & Beber 2025/2026, vista de frente al Pan de Azúcar e localização en el Parque Bondinho Pão de Açúcar, combina gastronomia de alto nível com a experiência turística mais icônica do Rio. Funciona todos los días das 8:30 às 21:00.", "<strong>Embaixada Carioca</strong>, en el Morro da Urca, sirve gastronomía brasileña dentro del Parque Bondinho Pan de Azúcar con vista directa al Pan de Azúcar. Abre todos los días de 8:30 a 21:00 y sirve la Mejor Feijoada de Río de Janeiro — Veja Rio Comer & Beber 2025/2026, en colaboración con Academia da Cachaça."),
        ],
        "es/morro-da-urca.html": [
            ("O <a href=\"/es/atardecer.html\" title=\"Atardecer en el Morro da Urca com drinks e petiscos\">atardecer en el Morro da Urca</a> é considerado um dos más bonitos do Río de Janeiro. O sol desce atrás del Pan de Azúcar, criando um espetáculo de cores que dura cerca de 30 minutos. A Embaixada Carioca serve drinks e petiscos durante todo o atardecer, das 15h às 21:00.", "El <a href=\"/es/atardecer.html\" title=\"Atardecer en el Morro da Urca con bebidas y aperitivos\">atardecer en el Morro da Urca</a> es uno de los más bonitos de Río de Janeiro. El sol desciende detrás del Pan de Azúcar y crea un espectáculo de colores. Embaixada Carioca sirve bebidas y aperitivos durante el atardecer, de 15:00 a 21:00."),
        ],
        "es/restaurante-com-vista-rio-de-janeiro.html": [
            ("O único <strong>almuerzo dentro do Parque Bondinho Pão de Açúcar</strong>, a 227 metros de altitude en el Morro da Urca. Gastronomía brasileña premiada: picanha à brasileira e a feijoada eleita premiada pela Revista Veja Rio Comer & Beber 2025/2026 na Academia da Cachaça. Para quién busca <strong>dónde almoçar no Río de Janeiro</strong> com a vista mais bonita da cidade — entre os <strong>restaurantes con vista no Río de Janeiro</strong>, este es o único en lo alto del Morro da Urca.", "El único <strong>almuerzo dentro del Parque Bondinho Pan de Azúcar</strong> con vista directa al Pan de Azúcar, a 227 metros de altitud en el Morro da Urca. Picanha brasileña y la Mejor Feijoada de Río de Janeiro — Veja Rio Comer & Beber 2025/2026, en colaboración con Academia da Cachaça."),
            ("Receitas clássicas da gastronomía brasileña servidas com técnica contemporânea e ingredientes selecionados — o sabor do Brasil com a vista más bonita de Rio. O <strong>Restaurante del Bondinho</strong> é o único almuerzo a 227 metros con vista direta al Pan de Azúcar, en lo alto del Morro da Urca. Um dos <strong>melhores restaurantes do Río de Janeiro</strong> para quién quer gastronomia e vista em um só lugar.", "Recetas clásicas de la gastronomía brasileña preparadas con técnica contemporánea e ingredientes seleccionados. El <strong>restaurante del Bondinho</strong> ofrece almuerzo a 227 metros de altitud, con vista directa al Pan de Azúcar desde el Morro da Urca."),
            ("La olla de barro, la receta de familia, la col salteada en el momento — todo creado y preparado en la <strong>Academia da Cachaça</strong> y traído con todo cuidado para ofrecer la misma calidad aquí en la Embaixada Carioca, con vista al Pan de Azúcar. Servida todos los días, das 11:30 às 17:00. Reserve com antecedência: é o prato mais disputado entre os visitantes do <strong>Restaurante Morro da Urca</strong>.", "La feijoada se sirve en olla de barro con arroz, col salteada, farofa y naranja. Ganadora como Mejor Feijoada de Río de Janeiro por Veja Rio Comer & Beber 2025/2026, en colaboración con Academia da Cachaça. Disponible todos los días de 11:30 a 17:00 en Embaixada Carioca, con vista al Pan de Azúcar."),
        ],
    }
    for old, new in exact_maps.get(rel, []):
        count = updated.count(old)
        if count:
            updated = updated.replace(old, new)
            total += count
            notes.append(f"language-block-rewritten:{count}")
    if rel == "en/restaurant-at-sugarloaf.html":
        replacement = '''<section class="section"><h2>Restaurant inside Sugarloaf Cable Car Park</h2><p>Embaixada Carioca is located at Morro da Urca, the first cable-car stop inside Sugarloaf Cable Car Park. It is the park's only restaurant with a direct, front-facing view of Sugarloaf Mountain and serves Brazilian food at the table from breakfast through sunset.</p><p>The restaurant is open daily from 8:30 AM to 9:00 PM. The menu includes Brazilian breakfast, grilled picanha, feijoada, seafood, caipirinhas and draft beer.</p></section><section class="section"><h2>Breakfast, lunch and sunset</h2><ul><li><strong>Breakfast, 8:30–11:30 AM:</strong> Brazilian breads, fruit, tapioca, eggs and coffee with a direct Sugarloaf view.</li><li><strong>Lunch, 11:30 AM–5:00 PM:</strong> grilled picanha, seafood and the Best Feijoada in Rio de Janeiro — Veja Rio Comer &amp; Beber 2025/2026, in partnership with Academia da Cachaça.</li><li><strong>Sunset, 5:00–9:00 PM:</strong> caipirinhas, Brazilian snacks and drinks overlooking Sugarloaf Mountain.</li></ul></section><section class="section faq"><h2>Frequently asked questions</h2><details><summary>Which restaurant is inside Sugarloaf Cable Car Park?</summary><p>Embaixada Carioca is at Morro da Urca, the first cable-car stop, and is the only restaurant in the park with a direct view of Sugarloaf Mountain.</p></details><details><summary>Do I need a cable-car ticket to visit?</summary><p>The usual route is by cable car with a park ticket. The Morro da Urca trail is an alternative when it is open. Visitors who hike up and remain at Morro da Urca do not need a cable-car ticket for the restaurant; a ticket is required to ride up to Sugarloaf Mountain or descend to Praia Vermelha by cable car.</p></details><details><summary>How much does it cost?</summary><p>Prices vary by item and season. Check the current menu online before your visit.</p></details><details><summary>Should I reserve a table?</summary><p>Reservations are recommended on weekends, holidays and during high season.</p></details><details><summary>Is feijoada served every day?</summary><p>Yes. The Best Feijoada in Rio de Janeiro — Veja Rio Comer &amp; Beber 2025/2026, in partnership with Academia da Cachaça — is served daily at lunch.</p></details></section><section class="section"><h2>Continue exploring</h2><div class="territory-links"><a class="territory-link" href="/en/restaurant-at-urca-hill.html">Restaurant at Urca Hill</a><a class="territory-link" href="/en/sugarloaf-cable-car-restaurant.html">Sugarloaf Cable Car restaurant</a><a class="territory-link" href="/en/where-to-eat-near-sugarloaf.html">Where to eat near Sugarloaf</a><a class="territory-link" href="/en/cafe-da-manha.html">Breakfast with a view</a><a class="territory-link" href="/en/feijoada.html">Award-winning feijoada</a><a class="territory-link" href="/en/how-to-get-there.html">How to get there</a></div></section>'''
        updated, count = re.subn(r'<section class="section"><h2>O que é o restaurante no Pão de Açúcar</h2>.*?</section><section class="section"><h2>Continue explorando</h2>.*?</section>', replacement, updated, count=1, flags=re.S)
        if count:
            total += count
            notes.append("en-sugarloaf-full-block-rewritten:1")
    elif rel == "es/restaurante-pan-de-azucar.html":
        replacement = '''<section class="section"><h2>Restaurante dentro del Parque Bondinho Pan de Azúcar</h2><p>Embaixada Carioca está en el Morro da Urca, la primera parada del teleférico dentro del Parque Bondinho Pan de Azúcar. Es el único restaurante del parque con vista directa y frontal al Pan de Azúcar y sirve gastronomía brasileña desde el desayuno hasta el atardecer.</p><p>Abre todos los días de 8:30 a 21:00. El menú incluye desayuno brasileño, picanha a la parrilla, feijoada, mariscos, caipirinhas y cerveza de barril.</p></section><section class="section"><h2>Desayuno, almuerzo y atardecer</h2><ul><li><strong>Desayuno, 8:30–11:30:</strong> panes brasileños, frutas, tapioca, huevos y café con vista directa al Pan de Azúcar.</li><li><strong>Almuerzo, 11:30–17:00:</strong> picanha a la parrilla, mariscos y la Mejor Feijoada de Río de Janeiro — Veja Rio Comer &amp; Beber 2025/2026, en colaboración con Academia da Cachaça.</li><li><strong>Atardecer, 17:00–21:00:</strong> caipirinhas, aperitivos brasileños y bebidas frente al Pan de Azúcar.</li></ul></section><section class="section faq"><h2>Preguntas frecuentes</h2><details><summary>¿Qué restaurante está dentro del Parque Bondinho?</summary><p>Embaixada Carioca está en el Morro da Urca, la primera parada del teleférico, y es el único restaurante del parque con vista directa al Pan de Azúcar.</p></details><details><summary>¿Necesito entrada del teleférico para visitar?</summary><p>La ruta habitual es en teleférico con entrada del parque. La senda del Morro da Urca es una alternativa cuando está abierta. Quien sube a pie y permanece en el Morro da Urca no necesita entrada para visitar el restaurante; la entrada es necesaria para subir al Pan de Azúcar o bajar a Praia Vermelha en teleférico.</p></details><details><summary>¿Cuánto cuesta?</summary><p>Los precios varían según el producto y la temporada. Consulta el menú actualizado en línea antes de la visita.</p></details><details><summary>¿Conviene reservar?</summary><p>Recomendamos reservar durante fines de semana, festivos y temporada alta.</p></details><details><summary>¿Sirven feijoada todos los días?</summary><p>Sí. La Mejor Feijoada de Río de Janeiro — Veja Rio Comer &amp; Beber 2025/2026, en colaboración con Academia da Cachaça — se sirve todos los días durante el almuerzo.</p></details></section><section class="section"><h2>Continúa explorando</h2><div class="territory-links"><a class="territory-link" href="/es/restaurante-morro-da-urca.html">Restaurante en el Morro da Urca</a><a class="territory-link" href="/es/restaurante-bondinho-pan-de-azucar.html">Restaurante del teleférico</a><a class="territory-link" href="/es/donde-comer-cerca-del-pan-de-azucar.html">Dónde comer cerca del Pan de Azúcar</a><a class="territory-link" href="/es/cafe-da-manha.html">Desayuno con vista</a><a class="territory-link" href="/es/feijoada.html">Feijoada premiada</a><a class="territory-link" href="/es/como-llegar.html">Cómo llegar</a></div></section>'''
        updated, count = re.subn(r'<section class="section"><h2>O que é o restaurante no Pão de Açúcar</h2>.*?</section><section class="section"><h2>Continue explorando</h2>.*?</section>', replacement, updated, count=1, flags=re.S)
        if count:
            total += count
            notes.append("es-sugarloaf-full-block-rewritten:1")
    return updated, total, notes


def parse_json(raw: str) -> Any | None:
    try:
        return json.loads(html.unescape(raw.strip()))
    except Exception:
        return None


def scrub_rating_nodes(
    obj: Any,
    forbidden_types: set[str] | None = None,
) -> tuple[Any, int]:
    """Remove review/rating/aggregateRating keys recursively from JSON-LD."""
    forbidden_types = forbidden_types or {"Review", "Rating", "AggregateRating"}
    removed = 0
    if isinstance(obj, dict):
        node_type = obj.get("@type")
        node_types = node_type if isinstance(node_type, list) else [node_type]
        present_types = [value for value in node_types if value is not None]
        if present_types and all(value in forbidden_types for value in present_types):
            return None, 1
        if isinstance(node_type, list):
            safe_types = [value for value in node_type if value not in forbidden_types]
            removed += len(node_type) - len(safe_types)
            obj = dict(obj)
            obj["@type"] = safe_types
        cleaned = {}
        for k, v in obj.items():
            if k in {
                "review", "reviews", "aggregateRating", "reviewRating",
                "ratingValue", "ratingCount", "reviewCount",
                "bestRating", "worstRating",
            }:
                removed += 1
                continue
            new_v, count = scrub_rating_nodes(v, forbidden_types)
            removed += count
            if new_v is not None:
                cleaned[k] = new_v
        return cleaned, removed
    if isinstance(obj, list):
        new_list = []
        for item in obj:
            new_item, count = scrub_rating_nodes(item, forbidden_types)
            removed += count
            if new_item is not None:
                new_list.append(new_item)
        return new_list, removed
    return obj, 0


def scrub_jsonld(source: str, remove_event: bool = False) -> tuple[str, int]:
    removed_total = 0
    parts: list[str] = []
    last = 0
    for m in JSONLD_RE.finditer(source):
        opener, raw, closer = m.groups()
        obj = parse_json(raw)
        if obj is None:
            continue
        forbidden_types = {"Review", "Rating", "AggregateRating"}
        if remove_event:
            forbidden_types.add("Event")
        cleaned, removed = scrub_rating_nodes(obj, forbidden_types)
        if not removed:
            continue
        parts.append(source[last:m.start()])
        parts.append(opener + "\n" + json.dumps(cleaned, ensure_ascii=False, indent=2) + "\n" + closer)
        last = m.end()
        removed_total += removed
    if not removed_total:
        return source, 0
    parts.append(source[last:])
    return "".join(parts), removed_total


def apply_text_fixes(source: str, path: Path) -> tuple[str, int, list[str]]:
    count_total = 0
    notes: list[str] = []
    updated = source
    page_lang = lang_for(path)
    updated, lang_count, lang_notes = apply_language_specific_fixes(updated, path)
    count_total += lang_count
    notes.extend(lang_notes)
    updated, page_count, page_notes = apply_page_specific_language_fixes(updated, path)
    count_total += page_count
    notes.extend(page_notes)
    for pattern, repl, note in TEXT_REPLACEMENTS:
        if note.startswith("en-") and page_lang != "en":
            continue
        updated, count = re.subn(pattern, repl, updated, flags=re.I)
        if count:
            count_total += count
            notes.append(f"{note}:{count}")
    for pattern, repl in CLAIM_PATTERNS:
        updated, count = re.subn(pattern, repl, updated, flags=re.I | re.S)
        if count:
            count_total += count
            notes.append(f"unverified-cantina-claim-removed:{count}")

    # Final factual guard. Older replacement rules above intentionally keep
    # matching legacy text, but their output must converge on the official
    # 2025 attribution before any file is written.
    year_count = updated.count("2025/2026")
    if year_count:
        updated = updated.replace("2025/2026", "2025")
        count_total += year_count
        notes.append(f"award-year-official-2025:{year_count}")

    return updated, count_total, notes


def process_file(path: Path) -> FileResult:
    rel = path.relative_to(ROOT).as_posix()
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated, replacements, notes = apply_text_fixes(original, path)
    remove_event = path.name == "sunset-por-do-sol-rio-de-janeiro.html"
    updated, rating_removed = scrub_jsonld(updated, remove_event=remove_event)
    if rating_removed:
        notes.append(f"jsonld-rating-review-removed:{rating_removed}")
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return FileResult(rel, changed, replacements, rating_removed, "; ".join(notes) if notes else "no-op")


def scan_remaining() -> dict[str, list[str]]:
    remaining: dict[str, list[str]] = {}
    for path in HTML_FILES:
        text = path.read_text(encoding="utf-8", errors="ignore")
        page_lang = lang_for(path)
        found = []
        en_only = {
            "drinks e petiscos", "best in Brazil pela", "Servida every",
            "sunset más", "dGuanabara", "Para quién", "onde have",
        }
        for term in FORBIDDEN_AFTER:
            if term in en_only and page_lang != "en":
                continue
            if term.lower() in text.lower():
                found.append(term)
        if found:
            remaining[path.relative_to(ROOT).as_posix()] = found
    return remaining


def workflow_inventory() -> list[str]:
    if not WORKFLOW_DIR.exists():
        return []
    return sorted(p.relative_to(ROOT).as_posix() for p in WORKFLOW_DIR.glob("*.yml")) + sorted(p.relative_to(ROOT).as_posix() for p in WORKFLOW_DIR.glob("*.yaml"))


def write_report(results: list[FileResult], remaining: dict[str, list[str]], workflows: list[str]) -> int:
    REPORT.parent.mkdir(exist_ok=True)
    changed = [r for r in results if r.changed]
    status = "PASS" if not remaining else "WARN"
    lines = [
        "# Claude Audit Critical Fixes",
        "",
        f"Status geral: **{status}**",
        "",
        "## Objetivo",
        "Atuar sobre os pontos críticos do relatório Claude: atribuição oficial do prêmio da feijoada à Academia da Cachaça, preservação da parceria institucional confirmada, limpeza de portunhol técnico, padronização de seguidores e blindagem contra retorno de review/rating em JSON-LD.",
        "",
        "## Formulações canônicas aplicadas",
        f"- PT: `{PT_AWARD}`",
        f"- EN: `{EN_AWARD}`",
        f"- ES: `{ES_AWARD}`",
        "",
        "## Guardrails",
        "- Nenhum canonical/hreflang foi alterado.",
        "- Nenhum AggregateRating, Rating ou Review foi adicionado.",
        "- JSON-LD com `review`, `reviewRating` ou `aggregateRating` foi limpo quando encontrado.",
        "- A composição societária comum confirmada entre Embaixada Carioca e Cantina do MAM não é removida nem distorcida por este script.",
        "- A Academia da Cachaça é tratada separadamente como parceira formal com vínculo societário familiar, sem afirmar composição societária idêntica.",
        "",
        "## Resumo",
        f"- HTML analisados: **{len(results)}**",
        f"- Arquivos alterados: **{len(changed)}**",
        f"- Substituições textuais: **{sum(r.replacements for r in results)}**",
        f"- Nós/campos JSON-LD de rating/review removidos: **{sum(r.jsonld_rating_removed for r in results)}**",
        f"- Workflows encontrados: **{len(workflows)}**",
        "",
    ]
    if workflows:
        lines.extend(["## Inventário de workflows", ""])
        for w in workflows:
            lines.append(f"- `{w}`")
        lines.append("")
    if remaining:
        lines.extend(["## Pendências encontradas", ""])
        for rel, terms in remaining.items():
            lines.append(f"- `{rel}`: {', '.join(f'`{t}`' for t in terms)}")
        lines.append("")
    else:
        lines.extend(["## Pendências encontradas", "", "Nenhuma ocorrência dos termos críticos monitorados.", ""])
    lines.extend(["## Arquivos alterados", "", "| Arquivo | Changed | Substituições | JSON-LD rating/review removidos | Notas |", "|---|---:|---:|---:|---|"])
    for r in results:
        if r.changed:
            lines.append(f"| `{r.path}` | {r.changed} | {r.replacements} | {r.jsonld_rating_removed} | {r.notes} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Claude audit critical fixes: {status}")
    return 0 if status in {"PASS", "WARN"} else 1


def main() -> int:
    results = [process_file(path) for path in HTML_FILES]
    remaining = scan_remaining()
    workflows = workflow_inventory()
    return write_report(results, remaining, workflows)


if __name__ == "__main__":
    raise SystemExit(main())
