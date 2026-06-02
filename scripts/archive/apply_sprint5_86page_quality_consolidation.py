#!/usr/bin/env python3
"""
Sprint 5 — 86-Page Quality Consolidation | Embaixada Carioca

Objetivo:
- Auditar todas as páginas HTML existentes, não criar novas páginas.
- Medir qualidade por página: word count, idioma dominante, vazamento de idioma,
  title/meta/H1/canonical/schema/FAQ/CTA/sitemap/âncoras.
- Consolidar qualidade em páginas rasas com blocos editoriais úteis, sem mudar o layout do topo.
- Gerar relatório mestre e CSV para orientar próximos ajustes humanos.

Importante:
Este script é propositalmente conservador: só acrescenta conteúdo em páginas de conteúdo
existentes com baixa profundidade. 404/offline/home-preview não recebem expansão editorial.
"""
from __future__ import annotations

from pathlib import Path
import csv
import html
import json
import re
from datetime import date
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.embaixadacarioca.com"
TODAY = date.today().isoformat()

REPORT: list[str] = []
DETAILS: list[dict[str, object]] = []
COUNTERS = {
    "html_scanned": 0,
    "content_pages": 0,
    "utility_pages": 0,
    "pages_updated": 0,
    "thin_before": 0,
    "thin_after_estimated": 0,
    "consolidation_blocks_added": 0,
    "faq_blocks_added": 0,
    "schema_blocks_added": 0,
    "language_fixes_applied": 0,
    "anchor_targets_added": 0,
    "sitemap_missing": 0,
    "pages_score_80_plus_estimated": 0,
    "warnings": 0,
}

UTILITY_FILES = {"404.html", "offline.html", "home-preview.html"}
UTILITY_PREFIXES = {"_audit_reports/"}
CONTENT_MIN_WORDS = 900
THIN_LIMIT = 650

CSS_START = "<!-- EC Sprint 5 Quality Consolidation CSS -->"
CSS_END = "<!-- /EC Sprint 5 Quality Consolidation CSS -->"
BLOCK_START = "<!-- EC Sprint 5 Quality Consolidation Block -->"
BLOCK_END = "<!-- /EC Sprint 5 Quality Consolidation Block -->"
FAQ_START = "<!-- EC Sprint 5 Quality FAQ -->"
FAQ_END = "<!-- /EC Sprint 5 Quality FAQ -->"
SCHEMA_START = "<!-- EC Sprint 5 Quality Schema -->"
SCHEMA_END = "<!-- /EC Sprint 5 Quality Schema -->"

CSS_RE = re.compile(r"\n*<!-- EC Sprint 5 Quality Consolidation CSS -->[\s\S]*?<!-- /EC Sprint 5 Quality Consolidation CSS -->\s*", re.I)
BLOCK_RE = re.compile(r"\n*<!-- EC Sprint 5 Quality Consolidation Block -->[\s\S]*?<!-- /EC Sprint 5 Quality Consolidation Block -->\s*", re.I)
FAQ_RE = re.compile(r"\n*<!-- EC Sprint 5 Quality FAQ -->[\s\S]*?<!-- /EC Sprint 5 Quality FAQ -->\s*", re.I)
SCHEMA_RE = re.compile(r"\n*<!-- EC Sprint 5 Quality Schema -->[\s\S]*?<!-- /EC Sprint 5 Quality Schema -->\s*", re.I)
HEAD_CLOSE_RE = re.compile(r"</head>", re.I)
MAIN_CLOSE_RE = re.compile(r"</main>", re.I)
BODY_CLOSE_RE = re.compile(r"</body>", re.I)
TITLE_RE = re.compile(r"<title[^>]*>([\s\S]*?)</title>", re.I)
META_DESC_RE = re.compile(r"<meta\s+[^>]*name=[\"']description[\"'][^>]*content=[\"']([^\"']*)[\"'][^>]*>", re.I)
H1_RE = re.compile(r"<h1\b[^>]*>([\s\S]*?)</h1>", re.I)
CANONICAL_RE = re.compile(r"<link\s+[^>]*rel=[\"']canonical[\"'][^>]*href=[\"']([^\"']+)[\"'][^>]*>", re.I)
HTML_LANG_RE = re.compile(r"<html\b[^>]*lang=[\"']([^\"']+)[\"']", re.I)
INTERNAL_HREF_RE = re.compile(r"href=[\"'](/[^\"'#?]+(?:\.html)?)(#[^\"']+)?[\"']", re.I)
ID_RE = re.compile(r"\bid=[\"']([^\"']+)[\"']", re.I)

CSS_BLOCK = f"""{CSS_START}
<style id="ec-sprint5-quality-consolidation-css">
.ec-sprint5-quality,.ec-sprint5-faq{{background:#f6efde;color:#00405a;padding:62px 0;border-top:1px solid rgba(0,64,90,.10)}}
.ec-sprint5-quality .wrap,.ec-sprint5-faq .wrap{{max-width:1120px;margin:0 auto;padding:0 24px}}
.ec-sprint5-quality h2,.ec-sprint5-faq h2{{font-size:clamp(30px,3.4vw,48px);line-height:1.06;margin:0 0 18px;color:#00405a}}
.ec-sprint5-quality h3{{font-size:22px;line-height:1.18;margin:24px 0 8px;color:#00405a}}
.ec-sprint5-quality p,.ec-sprint5-quality li,.ec-sprint5-faq p{{font-size:17px;line-height:1.62;color:#485156}}
.ec-sprint5-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin:26px 0}}
.ec-sprint5-card,.ec-sprint5-faq details{{background:#fff;border:1px solid rgba(0,64,90,.12);border-radius:20px;padding:22px;box-shadow:0 12px 32px rgba(0,64,90,.05)}}
.ec-sprint5-card strong{{display:block;color:#00405a;margin-bottom:6px}}
.ec-sprint5-quality ol{{background:#fff;border:1px solid rgba(0,64,90,.12);border-radius:20px;padding:24px 24px 24px 46px}}
.ec-sprint5-faq details{{margin:12px 0}}
.ec-sprint5-faq summary{{font-weight:800;cursor:pointer;color:#00405a}}
@media(max-width:760px){{.ec-sprint5-quality,.ec-sprint5-faq{{padding:42px 0}}}}
</style>
{CSS_END}"""

LANG_FIXES = {
    "en": {
        "Café da Manhã": "Breakfast",
        "Almoço": "Lunch",
        "Cardápio": "Menu",
        "Como Chegar": "How to Get There",
        "Guia do Rio": "Rio Guide",
        "Restaurante do Bondinho": "Cable Car Restaurant",
        "Restaurante no Morro da Urca": "Restaurant at Urca Hill",
    },
    "es": {
        "Café da Manhã": "Desayuno",
        "Almoço": "Almuerzo",
        "Cardápio": "Menú",
        "Como Chegar": "Cómo Llegar",
        "Guia do Rio": "Guía de Río",
        "Restaurante do Bondinho": "Restaurante del Bondinho",
        "Restaurante no Morro da Urca": "Restaurante en el Morro da Urca",
    },
}

LEAK_TOKENS = {
    "pt-BR": ["breakfast with", "where to eat", "restaurant at", "sugarloaf cable car", "cómo llegar", "dónde comer", "desayuno con"],
    "en": ["resposta direta", "como chegar", "por que essa página", "solicitar orçamento", "falar com", "café da manhã", "almoço", "cardápio"],
    "es": ["resposta direta", "como chegar", "por que essa página", "breakfast with", "where to eat", "reserve a table", "café da manhã", "almoço", "cardápio"],
}

CATEGORY_KEYWORDS = {
    "breakfast": ["cafe-da-manha", "breakfast", "desayuno"],
    "feijoada": ["feijoada"],
    "events": ["eventos", "events"],
    "access": ["como-chegar", "how-to-get-there", "como-llegar"],
    "guide": ["guia", "guide", "roteiro", "rio", "o-que-fazer"],
    "local_restaurant": ["restaurante", "restaurant", "restaurantes", "where-to-eat", "donde-comer", "onde-comer"],
    "drinks": ["caipirinha", "por-do-sol", "sunset", "entardecer", "atardecer"],
    "park": ["parque-bondinho", "sugarloaf", "pan-de-azucar", "pao-de-acucar", "morro-da-urca"],
    "menu": ["cardapio", "menu", "almoco", "lunch", "almuerzo"],
}


def is_utility(rel: str) -> bool:
    return rel in UTILITY_FILES or any(rel.startswith(p) for p in UTILITY_PREFIXES)


def strip_tags(text: str) -> str:
    text = re.sub(r"<script\b[\s\S]*?</script>|<style\b[\s\S]*?</style>|<!--[^>]*-->", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def word_count(visible: str) -> int:
    return len(re.findall(r"[A-Za-zÀ-ÿ0-9][A-Za-zÀ-ÿ0-9'’\-]{1,}", visible))


def lang_for(rel: str, source: str) -> str:
    m = HTML_LANG_RE.search(source)
    if m:
        value = m.group(1).lower()
        if value.startswith("en"):
            return "en"
        if value.startswith("es"):
            return "es"
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt-BR"


def category_for(rel: str) -> str:
    low = rel.lower()
    for category, keys in CATEGORY_KEYWORDS.items():
        if any(k in low for k in keys):
            return category
    return "generic"


def get_first(pattern: re.Pattern[str], text: str) -> str:
    m = pattern.search(text)
    return strip_tags(m.group(1)) if m else ""


def schema_types(source: str) -> list[str]:
    types: set[str] = set()
    for m in re.finditer(r"<script[^>]*type=[\"']application/ld\+json[\"'][^>]*>([\s\S]*?)</script>", source, re.I):
        raw = html.unescape(m.group(1).strip())
        try:
            data = json.loads(raw)
        except Exception:
            continue
        stack = [data]
        while stack:
            item = stack.pop()
            if isinstance(item, dict):
                t = item.get("@type")
                if isinstance(t, str):
                    types.add(t)
                elif isinstance(t, list):
                    types.update(str(x) for x in t)
                stack.extend(item.values())
            elif isinstance(item, list):
                stack.extend(item)
    return sorted(types)


def sitemap_locs() -> set[str]:
    path = ROOT / "sitemap.xml"
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8", errors="ignore")
    return set(re.findall(r"<loc>(.*?)</loc>", text, flags=re.I))


def href_to_rel(href: str) -> str:
    href = href.strip("/")
    if not href:
        return "index.html"
    if href.endswith("/"):
        href += "index.html"
    if "." not in Path(href).name:
        href += ".html"
    return href


def broken_anchor_count(source: str) -> int:
    ids = set(ID_RE.findall(source))
    count = 0
    for _href, anchor in INTERNAL_HREF_RE.findall(source):
        if anchor:
            name = anchor[1:]
            if name and name not in ids:
                count += 1
    return count


def language_leaks(visible: str, lang: str) -> list[str]:
    low = visible.lower()
    leaks = [token for token in LEAK_TOKENS.get(lang, []) if token in low]
    return leaks


def safe_language_fixes(source: str, lang: str, rel: str) -> str:
    fixes = LANG_FIXES.get(lang, {})
    original = source
    # Apply only visible/menu label style tokens, not proper nouns like Pão de Açúcar.
    for old, new in fixes.items():
        source = source.replace(old, new)
    if source != original:
        COUNTERS["language_fixes_applied"] += 1
        REPORT.append(f"LANG_FIX: {rel}")
    return source


def consolidation_copy(lang: str, category: str, rel: str) -> tuple[str, list[tuple[str, str]], str]:
    if lang == "en":
        title = "Practical guide for planning this visit"
        intro = "This page is designed to answer the questions visitors usually have before deciding where to eat during a Sugarloaf visit: access, timing, food style, view, reservation and how the stop fits into the day. Embaixada Carioca is not positioned as a generic restaurant in Rio; it is a Brazilian restaurant inside the Sugarloaf Cable Car Park route, at Urca Hill, with breakfast, lunch, caipirinhas, draft beer and event options."
        cards = [
            ("Why it matters", "The location reduces friction for travelers who are already visiting Sugarloaf and want a reliable place to eat without leaving the attraction."),
            ("Best timing", "Morning works well for breakfast with a view; lunch is ideal for Brazilian dishes; late afternoon is useful for drinks and a slower Rio-style pause."),
            ("Access logic", "Most visitors reach the restaurant by cable car from Praia Vermelha. The Urca Hill trail can be an alternative when open."),
            ("Decision factor", "Choose this stop when the goal is to combine a landmark view, Brazilian food and a practical route inside the tourist attraction."),
        ]
        steps_title = "How to use this page"
        steps = ["Confirm whether your visit will be by cable car or trail.", "Check the best meal moment for your itinerary: breakfast, lunch, drinks or event.", "Use the reservation link when visiting on weekends, holidays or with a group.", "Continue exploring Urca Hill or the next cable car stage after the meal."]
    elif lang == "es":
        title = "Guía práctica para planificar la visita"
        intro = "Esta página responde a las dudas que suelen aparecer antes de decidir dónde comer durante una visita al Pan de Azúcar: acceso, horarios, tipo de comida, vista, reserva y cómo encaja la parada en el itinerario. Embaixada Carioca no es un restaurante genérico de Río; está dentro de la ruta del Parque Bondinho, en el Morro da Urca, con desayuno, almuerzo, caipirinhas, cerveza de barril y opciones para eventos."
        cards = [
            ("Por qué importa", "La ubicación reduce fricción para quienes ya visitan el Pan de Azúcar y quieren comer sin salir del atractivo."),
            ("Mejor horario", "La mañana funciona para desayuno con vista; el almuerzo para platos brasileños; la tarde para drinks y una pausa carioca."),
            ("Lógica de acceso", "La mayoría llega en Bondinho desde Praia Vermelha. El sendero del Morro da Urca puede ser alternativa cuando está abierto."),
            ("Factor de decisión", "Elige esta parada si quieres unir vista icónica, comida brasileña y una ruta práctica dentro del atractivo turístico."),
        ]
        steps_title = "Cómo usar esta página"
        steps = ["Confirma si tu acceso será por Bondinho o sendero.", "Elige el mejor momento: desayuno, almuerzo, drinks o evento.", "Usa la reserva en fines de semana, feriados o grupos.", "Después de comer, continúa por el Morro da Urca o por el siguiente tramo del Bondinho."]
    else:
        title = "Guia prático para planejar a visita"
        intro = "Esta página foi consolidada para responder às dúvidas que realmente influenciam a decisão do visitante: acesso, horário, tipo de experiência, vista, reserva e encaixe no roteiro do Pão de Açúcar. A Embaixada Carioca não é um restaurante genérico no Rio; é um restaurante brasileiro dentro da rota do Parque Bondinho, no Morro da Urca, com café da manhã, almoço, caipirinhas, chope e eventos."
        cards = [
            ("Por que importa", "A localização reduz atrito para quem já está visitando o Pão de Açúcar e quer comer bem sem sair do atrativo."),
            ("Melhor horário", "A manhã funciona para café com vista; o almoço para pratos brasileiros; o fim da tarde para drinks e uma pausa carioca."),
            ("Lógica de acesso", "A maioria chega de Bondinho pela Praia Vermelha. A trilha do Morro da Urca pode ser alternativa quando aberta."),
            ("Fator de decisão", "Escolha essa parada quando quiser unir vista icônica, comida brasileira e rota prática dentro do ponto turístico."),
        ]
        steps_title = "Como usar esta página"
        steps = ["Confirme se o acesso será pelo Bondinho ou pela trilha.", "Escolha o melhor momento: café, almoço, drinks ou evento.", "Use a reserva em fins de semana, feriados ou grupos.", "Depois da refeição, continue pelo Morro da Urca ou pelo próximo trecho do Bondinho."]
    if category == "feijoada":
        if lang == "en":
            intro += " For feijoada searches, the key value is cultural relevance: a classic Brazilian dish linked to Rio hospitality, caipirinha and a memorable view."
        elif lang == "es":
            intro += " Para búsquedas sobre feijoada, el valor central es cultural: un plato brasileño clásico, unido a hospitalidad carioca, caipirinha y vista memorable."
        else:
            intro += " Para buscas sobre feijoada, o valor central é cultural: um prato brasileiro clássico, ligado à hospitalidade carioca, caipirinha e vista memorável."
    elif category == "events":
        if lang == "en":
            intro += " For events, the page should clarify format, access, group flow, timing and why the location creates a stronger guest memory."
        elif lang == "es":
            intro += " Para eventos, la página debe aclarar formato, acceso, flujo del grupo, horarios y por qué la ubicación crea una memoria más fuerte para los invitados."
        else:
            intro += " Para eventos, a página deve esclarecer formato, acesso, fluxo do grupo, horários e por que a localização cria uma memória mais forte para os convidados."
    cards_html = "".join(f"<article class=\"ec-sprint5-card\"><strong>{html.escape(t)}</strong>{html.escape(b)}</article>" for t,b in cards)
    steps_html = "".join(f"<li>{html.escape(s)}</li>" for s in steps)
    block = f"{BLOCK_START}\n<section class=\"ec-sprint5-quality\" aria-label=\"Quality guide\"><div class=\"wrap\"><h2>{html.escape(title)}</h2><p>{html.escape(intro)}</p><div class=\"ec-sprint5-grid\">{cards_html}</div><h3>{html.escape(steps_title)}</h3><ol>{steps_html}</ol></div></section>\n{BLOCK_END}"
    faq = qa_for(lang, category)
    return block, faq, title


def qa_for(lang: str, category: str) -> list[tuple[str, str]]:
    if lang == "en":
        return [
            ("Is Embaixada Carioca inside Sugarloaf Cable Car Park?", "Yes. It is located at Urca Hill, the first stop of Sugarloaf Cable Car Park, which makes it practical for visitors already planning the attraction."),
            ("Do I need to plan access before visiting?", "Yes. Most visitors arrive by cable car with a park ticket. The Urca Hill trail can be a free alternative when open and suitable for the visitor."),
            ("Is it better for breakfast, lunch or drinks?", "It works for all three moments. Breakfast is best for an early scenic start, lunch for Brazilian food and afternoon for caipirinhas, draft beer and a slower view experience."),
            ("Should groups reserve?", "Yes. Reservations are recommended for groups, weekends, holidays and high-traffic tourism days to reduce waiting time and organize the visit."),
        ]
    if lang == "es":
        return [
            ("¿Embaixada Carioca está dentro del Parque Bondinho?", "Sí. Está en el Morro da Urca, la primera parada del Parque Bondinho Pan de Azúcar, lo que facilita la visita para quienes ya harán el paseo."),
            ("¿Debo planificar el acceso antes de ir?", "Sí. La mayoría llega en Bondinho con entrada del parque. El sendero del Morro da Urca puede ser una alternativa gratuita cuando está abierto y es adecuado para el visitante."),
            ("¿Es mejor para desayuno, almuerzo o drinks?", "Funciona para los tres momentos. El desayuno es ideal para empezar temprano con vista, el almuerzo para comida brasileña y la tarde para caipirinhas, cerveza y una pausa con vista."),
            ("¿Los grupos deben reservar?", "Sí. Recomendamos reservar para grupos, fines de semana, feriados y días de alto flujo turístico para organizar mejor la visita."),
        ]
    return [
        ("A Embaixada Carioca fica dentro do Parque Bondinho?", "Sim. Ela fica no Morro da Urca, a primeira parada do Parque Bondinho Pão de Açúcar, o que torna a visita prática para quem já está planejando o passeio."),
        ("Preciso planejar o acesso antes de ir?", "Sim. A maioria dos visitantes chega pelo Bondinho com ingresso do parque. A trilha do Morro da Urca pode ser alternativa gratuita quando aberta e adequada ao visitante."),
        ("É melhor para café, almoço ou drinks?", "Funciona nos três momentos. O café é ideal para começar cedo com vista, o almoço para comida brasileira e a tarde para caipirinhas, chope e uma pausa com vista."),
        ("Grupos devem reservar?", "Sim. A reserva é recomendada para grupos, fins de semana, feriados e dias de alto fluxo turístico para organizar melhor a visita."),
    ]


def faq_html(faq: list[tuple[str, str]], lang: str) -> str:
    title = {"en":"Useful questions before visiting", "es":"Preguntas útiles antes de visitar"}.get(lang, "Perguntas úteis antes da visita")
    items = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q,a in faq)
    return f"{FAQ_START}\n<section class=\"ec-sprint5-faq\"><div class=\"wrap\"><h2>{html.escape(title)}</h2>{items}</div></section>\n{FAQ_END}"


def schema_html(rel: str, lang: str, faq: list[tuple[str, str]]) -> str:
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type":"WebPage","@id":f"{BASE}/{rel}#webpage","url":f"{BASE}/{rel if rel != 'index.html' else ''}","name":"Embaixada Carioca","inLanguage":lang,"isPartOf":{"@id":f"{BASE}/#website"}},
            {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]},
        ],
    }
    return f"{SCHEMA_START}\n<script type=\"application/ld+json\">{json.dumps(data, ensure_ascii=False, separators=(',', ':'))}</script>\n{SCHEMA_END}"


def insert_before_end(source: str, block: str) -> str:
    if MAIN_CLOSE_RE.search(source):
        return MAIN_CLOSE_RE.sub(block + "\n</main>", source, count=1)
    if BODY_CLOSE_RE.search(source):
        return BODY_CLOSE_RE.sub(block + "\n</body>", source, count=1)
    return source + "\n" + block


def inject_css(source: str) -> str:
    source = CSS_RE.sub("\n", source)
    if HEAD_CLOSE_RE.search(source):
        return HEAD_CLOSE_RE.sub(CSS_BLOCK + "\n</head>", source, count=1)
    return source


def consolidate_if_needed(source: str, rel: str, lang: str, wc: int, category: str) -> str:
    if is_utility(rel):
        return source
    if wc >= CONTENT_MIN_WORDS and FAQ_START in source:
        return source
    original = source
    source = CSS_RE.sub("\n", source)
    source = BLOCK_RE.sub("\n", source)
    # Do not strip Sprint4 FAQ. Add Sprint5 FAQ only if page is still thin or has no FAQPage.
    should_add_block = wc < CONTENT_MIN_WORDS
    should_add_faq = (wc < CONTENT_MIN_WORDS) and ("FAQPage" not in source and FAQ_START not in source)
    if should_add_block:
        source = inject_css(source)
        block, faq, _title = consolidation_copy(lang, category, rel)
        source = insert_before_end(source, block)
        COUNTERS["consolidation_blocks_added"] += 1
        REPORT.append(f"CONSOLIDATION_BLOCK: {rel} ({wc} words before)")
        if should_add_faq:
            source = insert_before_end(source, faq_html(faq, lang))
            if HEAD_CLOSE_RE.search(source):
                source = SCHEMA_RE.sub("\n", source)
                source = HEAD_CLOSE_RE.sub(schema_html(rel, lang, faq) + "\n</head>", source, count=1)
            COUNTERS["faq_blocks_added"] += 1
            COUNTERS["schema_blocks_added"] += 1
            REPORT.append(f"SPRINT5_FAQ_SCHEMA: {rel}")
    return source if source != original else original


def score_page(metrics: dict[str, object]) -> int:
    score = 100
    if not metrics["title"]:
        score -= 10
    if not metrics["meta_description"]:
        score -= 10
    if not metrics["h1"]:
        score -= 8
    if not metrics["canonical"]:
        score -= 6
    wc = int(metrics["word_count"])
    utility = bool(metrics["utility"])
    if not utility:
        if wc < 400:
            score -= 24
        elif wc < 650:
            score -= 16
        elif wc < 900:
            score -= 8
    if int(metrics["language_leak_count"]) > 0:
        score -= min(18, int(metrics["language_leak_count"]) * 5)
    if not metrics["has_restaurant_schema"] and not utility:
        score -= 6
    if not metrics["has_opening_hours"] and not utility:
        score -= 5
    if not metrics["has_cta"] and not utility:
        score -= 6
    if not metrics["in_sitemap"] and not utility:
        score -= 7
    if int(metrics["broken_anchor_count"]) > 0:
        score -= min(12, int(metrics["broken_anchor_count"]) * 3)
    return max(0, min(100, score))


def page_metrics(path: Path, source: str, sitemap: set[str]) -> dict[str, object]:
    rel = path.relative_to(ROOT).as_posix()
    lang = lang_for(rel, source)
    visible = strip_tags(source)
    wc = word_count(visible)
    types = schema_types(source)
    leaks = language_leaks(visible, lang)
    url = BASE + ("/" if rel == "index.html" else "/" + rel)
    metrics: dict[str, object] = {
        "page": rel,
        "lang": lang,
        "utility": is_utility(rel),
        "category": category_for(rel),
        "word_count": wc,
        "title": get_first(TITLE_RE, source),
        "meta_description": get_first(META_DESC_RE, source),
        "h1": get_first(H1_RE, source),
        "canonical": get_first(CANONICAL_RE, source),
        "schema_types": ",".join(types),
        "has_restaurant_schema": "Restaurant" in types or "FoodEstablishment" in types or "LocalBusiness" in types,
        "has_faq_schema": "FAQPage" in types or "FAQPage" in source,
        "has_opening_hours": "openingHours" in source or "openingHoursSpecification" in source,
        "has_cta": "go.tagme.com.br/embaixadacarioca" in source or "reserv" in visible.lower(),
        "in_sitemap": url in sitemap,
        "language_leak_count": len(leaks),
        "language_leaks": "; ".join(leaks),
        "broken_anchor_count": broken_anchor_count(source),
        "html_kb": round(len(source.encode("utf-8")) / 1024, 1),
        "inline_style_count": len(re.findall(r"\sstyle=", source, flags=re.I)),
    }
    metrics["score"] = score_page(metrics)
    return metrics


def process_html(path: Path, sitemap: set[str]) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix != ".html" or ".git" in path.parts or rel.startswith("_"):
        return
    COUNTERS["html_scanned"] += 1
    if is_utility(rel):
        COUNTERS["utility_pages"] += 1
    else:
        COUNTERS["content_pages"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    lang = lang_for(rel, original)
    source = safe_language_fixes(original, lang, rel)
    before = page_metrics(path, source, sitemap)
    if int(before["word_count"]) < THIN_LIMIT and not bool(before["utility"]):
        COUNTERS["thin_before"] += 1
    source = consolidate_if_needed(source, rel, lang, int(before["word_count"]), str(before["category"]))
    if source != original:
        path.write_text(source, encoding="utf-8")
        COUNTERS["pages_updated"] += 1
    after = page_metrics(path, source, sitemap)
    if int(after["word_count"]) < THIN_LIMIT and not bool(after["utility"]):
        COUNTERS["thin_after_estimated"] += 1
    if not after["in_sitemap"] and not bool(after["utility"]):
        COUNTERS["sitemap_missing"] += 1
    if int(after["score"]) >= 80:
        COUNTERS["pages_score_80_plus_estimated"] += 1
    DETAILS.append(after)


def add_missing_anchor_targets() -> None:
    # Safety net for the most important anchors called out in prior audits.
    targets = {
        "cardapio.html": ["almoco", "drinks", "petiscos"],
        "en/cardapio.html": ["almoco", "drinks", "petiscos"],
        "es/cardapio.html": ["almoco", "drinks", "petiscos"],
        "eventos.html": ["orcamento"],
        "en/eventos.html": ["orcamento"],
        "es/eventos.html": ["orcamento"],
    }
    for rel, ids in targets.items():
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        existing = set(ID_RE.findall(text))
        missing = [i for i in ids if i not in existing]
        if missing:
            anchors = "".join(f"<span id=\"{i}\" class=\"ec-anchor-target\"></span>" for i in missing)
            if MAIN_CLOSE_RE.search(text):
                text = MAIN_CLOSE_RE.sub(anchors + "\n</main>", text, count=1)
            elif BODY_CLOSE_RE.search(text):
                text = BODY_CLOSE_RE.sub(anchors + "\n</body>", text, count=1)
            if text != original:
                path.write_text(text, encoding="utf-8")
                COUNTERS["anchor_targets_added"] += len(missing)
                REPORT.append(f"ANCHOR_TARGETS: {rel} -> {', '.join(missing)}")


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text
    additions = []
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith("_") or ".git" in p.parts:
            continue
        loc = BASE + ("/" if rel == "index.html" else "/" + rel)
        if loc not in text:
            additions.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{'1.00' if rel == 'index.html' else '0.80'}</priority>\n  </url>")
    if additions:
        text = re.sub(r"</urlset>\s*$", "\n" + "\n".join(additions) + "\n</urlset>", text, flags=re.I)
    if text != original:
        path.write_text(text, encoding="utf-8")
        REPORT.append(f"SITEMAP_CONSOLIDATED: {len(additions)} URLs")


def write_reports() -> None:
    out = ROOT / "_audit_reports"
    out.mkdir(exist_ok=True)
    md = out / "sprint5_86page_quality_consolidation_report.md"
    csv_path = out / "sprint5_86page_quality_details.csv"

    details_sorted = sorted(DETAILS, key=lambda x: (int(x["score"]), int(x["word_count"])))
    thin_pages = [d for d in details_sorted if not d["utility"] and int(d["word_count"]) < THIN_LIMIT]
    leak_pages = [d for d in details_sorted if int(d["language_leak_count"]) > 0]
    low_score = [d for d in details_sorted if int(d["score"]) < 80]
    largest = sorted(DETAILS, key=lambda x: float(x["html_kb"]), reverse=True)[:15]

    lines = [
        "# Sprint 5 — Auditoria e Consolidação das 86 páginas",
        "",
        "## Objetivo",
        "Auditar e consolidar a qualidade das páginas existentes, sem criar novas páginas, com foco em conteúdo útil, idioma, schema, sitemap, CTAs, âncoras, profundidade e preparação para SEO/AIO/GEO.",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend([
        "",
        "## Veredito técnico estimado",
        f"- Páginas auditadas: {COUNTERS['html_scanned']}",
        f"- Páginas de conteúdo: {COUNTERS['content_pages']}",
        f"- Páginas utilitárias: {COUNTERS['utility_pages']}",
        f"- Páginas estimadas com score ≥ 80: {COUNTERS['pages_score_80_plus_estimated']}/{COUNTERS['html_scanned']}",
        f"- Páginas ainda abaixo de 650 palavras: {len(thin_pages)}",
        f"- Páginas com possível vazamento de idioma: {len(leak_pages)}",
        f"- Páginas abaixo de score 80 estimado: {len(low_score)}",
        "",
        "## Piores páginas por score estimado",
        "| Página | Idioma | Score | Palavras | Vazamentos | Sitemap | Schema | FAQ | KB |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for d in details_sorted[:25]:
        lines.append(f"| {d['page']} | {d['lang']} | {d['score']} | {d['word_count']} | {d['language_leak_count']} | {d['in_sitemap']} | {d['has_restaurant_schema']} | {d['has_faq_schema']} | {d['html_kb']} |")
    lines.extend(["", "## Páginas ainda rasas após consolidação estimada"])
    if thin_pages:
        for d in thin_pages[:40]:
            lines.append(f"- {d['page']} — {d['word_count']} palavras — score {d['score']}")
    else:
        lines.append("- Nenhuma página de conteúdo abaixo de 650 palavras.")
    lines.extend(["", "## Possíveis vazamentos de idioma remanescentes"])
    if leak_pages:
        for d in leak_pages[:40]:
            lines.append(f"- {d['page']} [{d['lang']}]: {d['language_leaks']}")
    else:
        lines.append("- Nenhum vazamento de idioma detectado pelos tokens críticos.")
    lines.extend(["", "## Maiores páginas HTML"])
    for d in largest:
        lines.append(f"- {d['page']}: {d['html_kb']} KB, {d['inline_style_count']} estilos inline")
    lines.extend(["", "## Ações aplicadas"])
    lines.extend(f"- {item}" for item in REPORT) if REPORT else lines.append("- Nenhuma alteração aplicada.")
    lines.extend(["", "## Próxima ação recomendada", "- Separar CSS global em arquivo externo e reduzir peso da home/guia/café quando a validação visual estiver estável.", "- Revisar manualmente as páginas listadas com vazamento de idioma, pois detecção automática pode gerar falso positivo quando termos próprios aparecem em outro idioma.", ""])
    md.write_text("\n".join(lines), encoding="utf-8")

    fieldnames = list(DETAILS[0].keys()) if DETAILS else []
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted(DETAILS, key=lambda x: x["page"]):
            writer.writerow(row)
    print(md.read_text(encoding="utf-8"))


def main() -> int:
    update_sitemap()
    sitemap = sitemap_locs()
    for path in sorted(ROOT.rglob("*.html")):
        process_html(path, sitemap)
    add_missing_anchor_targets()
    # Recompute after anchor/sitemap safety net for final report consistency.
    DETAILS.clear()
    sitemap = sitemap_locs()
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix == ".html" and ".git" not in path.parts and not rel.startswith("_"):
            DETAILS.append(page_metrics(path, path.read_text(encoding="utf-8", errors="ignore"), sitemap))
    # Refresh counters derived from final pass.
    COUNTERS["pages_score_80_plus_estimated"] = sum(1 for d in DETAILS if int(d["score"]) >= 80)
    COUNTERS["thin_after_estimated"] = sum(1 for d in DETAILS if not d["utility"] and int(d["word_count"]) < THIN_LIMIT)
    COUNTERS["sitemap_missing"] = sum(1 for d in DETAILS if not d["utility"] and not d["in_sitemap"])
    write_reports()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
