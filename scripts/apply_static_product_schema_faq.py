#!/usr/bin/env python3
"""Apply and audit static Restaurant Schema + FAQPage on priority pages.

P1B objective:
- Guarantee static JSON-LD in HTML, not runtime-only injection.
- Add Restaurant schema where required.
- Add FAQPage with 8 questions where required.
- Remove legacy rating/review fields from all JSON-LD blocks on audited pages.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "static_schema_product_pages_audit.md"
REPORT_JSON = REPORT_DIR / "static_schema_product_pages_audit.json"
SITE = "https://www.embaixadacarioca.com"
BLOCK_START = "<!-- EC STATIC PRODUCT SCHEMA FAQ FIX -->"
BLOCK_END = "<!-- /EC STATIC PRODUCT SCHEMA FAQ FIX -->"
SCRIPT_ID = "ec-static-product-schema-faq"
FORBIDDEN_KEYS = {"aggregateRating", "ratingValue", "reviewCount", "ratingCount", "bestRating", "worstRating"}
FORBIDDEN_TYPES = {"AggregateRating"}
FORBIDDEN_TERMS = {"AggregateRating", *FORBIDDEN_KEYS}
JSONLD_RE = re.compile(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)

PAGES: dict[str, dict[str, Any]] = {
    "eventos.html": {"lang": "pt", "topic": "eventos no Morro da Urca", "restaurant": True, "faq": True, "url": SITE + "/eventos.html"},
    "cardapio.html": {"lang": "pt", "topic": "cardápio da Embaixada Carioca", "restaurant": True, "faq": True, "url": SITE + "/cardapio.html"},
    "almoco.html": {"lang": "pt", "topic": "almoço no Pão de Açúcar", "restaurant": True, "faq": True, "url": SITE + "/almoco.html"},
    "entardecer.html": {"lang": "pt", "topic": "entardecer no Morro da Urca", "restaurant": True, "faq": True, "url": SITE + "/entardecer.html"},
    "feijoada.html": {"lang": "pt", "topic": "feijoada no Morro da Urca", "restaurant": True, "faq": True, "url": SITE + "/feijoada.html"},
    "cafe-da-manha.html": {"lang": "pt", "topic": "café da manhã no Morro da Urca", "restaurant": True, "faq": True, "url": SITE + "/cafe-da-manha.html"},
    "morro-da-urca.html": {"lang": "pt", "topic": "Morro da Urca", "restaurant": False, "faq": True, "url": SITE + "/morro-da-urca.html"},
    "en/sunset.html": {"lang": "en", "topic": "sunset at Morro da Urca", "restaurant": True, "faq": True, "url": SITE + "/en/sunset.html"},
    "en/cardapio.html": {"lang": "en", "topic": "Embaixada Carioca menu", "restaurant": True, "faq": True, "url": SITE + "/en/cardapio.html"},
    "en/almoco.html": {"lang": "en", "topic": "Brazilian lunch at Sugarloaf", "restaurant": True, "faq": True, "url": SITE + "/en/almoco.html"},
    "en/morro-da-urca.html": {"lang": "en", "topic": "Morro da Urca", "restaurant": False, "faq": True, "url": SITE + "/en/morro-da-urca.html"},
    "es/atardecer.html": {"lang": "es", "topic": "atardecer en Morro da Urca", "restaurant": True, "faq": True, "url": SITE + "/es/atardecer.html"},
    "es/cardapio.html": {"lang": "es", "topic": "menú de Embaixada Carioca", "restaurant": True, "faq": True, "url": SITE + "/es/cardapio.html"},
    "es/almoco.html": {"lang": "es", "topic": "almuerzo brasileño en Pão de Açúcar", "restaurant": True, "faq": True, "url": SITE + "/es/almoco.html"},
    "es/morro-da-urca.html": {"lang": "es", "topic": "Morro da Urca", "restaurant": False, "faq": True, "url": SITE + "/es/morro-da-urca.html"},
}

RESTAURANT_BASE: dict[str, Any] = {
    "@type": "Restaurant",
    "@id": f"{SITE}/#restaurant",
    "name": "Embaixada Carioca",
    "url": SITE + "/",
    "telephone": "+55 21 96683-7556",
    "email": "eventos@embaixadacarioca.com.br",
    "servesCuisine": ["Brazilian", "Carioca", "Brazilian breakfast", "Brazilian lunch"],
    "priceRange": "R$R$",
    "acceptsReservations": True,
    "hasMenu": SITE + "/cardapio.html",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Parque Bondinho Pão de Açúcar, Morro da Urca",
        "addressLocality": "Rio de Janeiro",
        "addressRegion": "RJ",
        "addressCountry": "BR",
    },
    "amenityFeature": [
        {"@type": "LocationFeatureSpecification", "name": "Dentro do Parque Bondinho Pão de Açúcar", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Vista no Morro da Urca", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Experiência gastronômica carioca", "value": True},
    ],
    "potentialAction": {"@type": "ReserveAction", "target": "https://go.tagme.com.br/embaixadacarioca"},
    "sameAs": ["https://www.instagram.com/embaixadacarioca/"],
}

@dataclass
class PageResult:
    page: str
    exists: bool
    status: str
    restaurant_required: bool
    restaurant_found: bool
    faq_required: bool
    faq_found: bool
    faq_questions: int
    forbidden_terms: list[str]
    changed: bool
    warnings: list[str]


def faq_items(lang: str, topic: str) -> list[tuple[str, str]]:
    if lang == "en":
        return [
            (f"What is {topic}?", "It is part of the Embaixada Carioca experience at Morro da Urca, inside Sugarloaf Cable Car Park."),
            ("Where is Embaixada Carioca located?", "Embaixada Carioca is located at Morro da Urca, inside Parque Bondinho Pão de Açúcar, at the first cable car stop."),
            ("Do I need a cable car ticket?", "Yes. Access to the restaurant is through Parque Bondinho Pão de Açúcar."),
            ("Does the restaurant serve Brazilian food?", "Yes. The restaurant serves Brazilian and carioca food, including breakfast, lunch, snacks and drinks."),
            ("Can I make a reservation?", "Yes. Reservations can be made through the official Embaixada Carioca booking link."),
            ("Is it suitable for tourists?", "Yes. The restaurant is designed for visitors who want a carioca food experience during a Sugarloaf visit."),
            ("Does Embaixada Carioca host groups and events?", "Yes. The venue hosts groups, corporate events, agencies and celebrations."),
            ("What is Embaixada Carioca known for?", "It is known for caipirinhas, draft beer, Brazilian food and its Morro da Urca location."),
        ]
    if lang == "es":
        return [
            (f"¿Qué es {topic}?", "Forma parte de la experiencia de Embaixada Carioca en Morro da Urca, dentro del Parque Bondinho Pão de Açúcar."),
            ("¿Dónde está Embaixada Carioca?", "Embaixada Carioca está en Morro da Urca, dentro del Parque Bondinho Pão de Açúcar, en la primera parada del teleférico."),
            ("¿Necesito entrada del Bondinho?", "Sí. El acceso al restaurante ocurre dentro del Parque Bondinho Pão de Açúcar."),
            ("¿El restaurante sirve comida brasileña?", "Sí. El restaurante sirve comida brasileña y carioca, con desayuno, almuerzo, petiscos y bebidas."),
            ("¿Puedo hacer una reserva?", "Sí. Las reservas se pueden hacer por el enlace oficial de Embaixada Carioca."),
            ("¿Es recomendable para turistas?", "Sí. La casa fue pensada para visitantes que quieren una experiencia carioca durante el paseo al Pão de Açúcar."),
            ("¿Embaixada Carioca recibe grupos y eventos?", "Sí. La casa recibe grupos, eventos corporativos, agencias y celebraciones."),
            ("¿Cuál es la especialidad de Embaixada Carioca?", "La casa es conocida por caipirinhas, chope, comida brasileña y su ubicación en Morro da Urca."),
        ]
    return [
        (f"O que é {topic}?", "É uma experiência da Embaixada Carioca no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar."),
        ("Onde fica a Embaixada Carioca?", "A Embaixada Carioca fica no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, na primeira parada do bondinho."),
        ("Preciso comprar ingresso do Bondinho?", "Sim. O acesso ao restaurante acontece dentro da visita ao Parque Bondinho Pão de Açúcar."),
        ("A Embaixada Carioca serve comida brasileira?", "Sim. A casa serve comida brasileira e carioca, incluindo café da manhã, almoço, petiscos e bebidas."),
        ("Posso fazer reserva?", "Sim. As reservas podem ser feitas pelo link oficial da Embaixada Carioca."),
        ("É indicado para turistas?", "Sim. A proposta é oferecer uma experiência carioca durante a visita ao Pão de Açúcar."),
        ("A Embaixada Carioca recebe grupos e eventos?", "Sim. A casa recebe grupos, eventos corporativos, agências e celebrações."),
        ("Qual é a especialidade da Embaixada Carioca?", "A casa é conhecida por caipirinhas, chope, comida brasileira e localização no Morro da Urca."),
    ]


def strip_old_block(source: str) -> str:
    return re.sub(re.escape(BLOCK_START) + r"[\s\S]*?" + re.escape(BLOCK_END) + r"\s*", "", source, flags=re.I)


def remove_forbidden_jsonld(obj: Any) -> Any:
    if isinstance(obj, dict):
        typ = obj.get("@type")
        if typ in FORBIDDEN_TYPES or (isinstance(typ, list) and any(t in FORBIDDEN_TYPES for t in typ)):
            return None
        cleaned: dict[str, Any] = {}
        for key, value in obj.items():
            if key in FORBIDDEN_KEYS:
                continue
            next_value = remove_forbidden_jsonld(value)
            if next_value is None:
                continue
            if isinstance(next_value, list) and not next_value:
                continue
            cleaned[key] = next_value
        return cleaned
    if isinstance(obj, list):
        return [item for item in (remove_forbidden_jsonld(v) for v in obj) if item is not None]
    return obj


def sanitize_jsonld(source: str) -> str:
    def repl(match: re.Match[str]) -> str:
        opener, raw, closer = match.groups()
        try:
            obj = json.loads(html.unescape(raw.strip()))
        except Exception:
            return match.group(0)
        cleaned = remove_forbidden_jsonld(obj)
        if cleaned is None:
            return ""
        serialized = json.dumps(cleaned, ensure_ascii=False, separators=(",", ":"))
        if any(term in serialized for term in FORBIDDEN_TERMS):
            raise ValueError("Forbidden rating/review term remains after JSON-LD sanitization")
        return opener + serialized + closer
    return JSONLD_RE.sub(repl, source)


def schema_block(config: dict[str, Any]) -> str:
    graph: list[dict[str, Any]] = []
    if config.get("restaurant"):
        schema = dict(RESTAURANT_BASE)
        schema["mainEntityOfPage"] = config["url"]
        graph.append(schema)
    if config.get("faq"):
        graph.append({
            "@type": "FAQPage",
            "@id": config["url"].rstrip("/") + "#faq",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faq_items(config["lang"], config["topic"])
            ],
        })
    payload = {"@context": "https://schema.org", "@graph": graph}
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    if any(term in serialized for term in FORBIDDEN_TERMS):
        raise ValueError("Forbidden rating/review term leaked into new static schema")
    return f'{BLOCK_START}\n<script id="{SCRIPT_ID}" type="application/ld+json">{serialized}</script>\n{BLOCK_END}\n'


def insert_block(source: str, block: str) -> str:
    if "</head>" in source:
        return source.replace("</head>", block + "</head>", 1)
    return block + source


def walk_schema(obj: Any, types: list[str], faq_counts: list[int]) -> None:
    if isinstance(obj, dict):
        typ = obj.get("@type")
        if isinstance(typ, str):
            types.append(typ)
        elif isinstance(typ, list):
            types.extend(str(t) for t in typ)
        if typ == "FAQPage" and isinstance(obj.get("mainEntity"), list):
            faq_counts.append(len(obj["mainEntity"]))
        for value in obj.values():
            walk_schema(value, types, faq_counts)
    elif isinstance(obj, list):
        for item in obj:
            walk_schema(item, types, faq_counts)


def audit_html(source: str) -> tuple[bool, bool, int, list[str]]:
    types: list[str] = []
    faq_counts: list[int] = []
    forbidden: set[str] = set()
    for _, raw, _ in JSONLD_RE.findall(source):
        if any(term in raw for term in FORBIDDEN_TERMS):
            forbidden.update(term for term in FORBIDDEN_TERMS if term in raw)
        try:
            obj = json.loads(html.unescape(raw.strip()))
        except Exception:
            continue
        walk_schema(obj, types, faq_counts)
    return ("Restaurant" in types or "FoodEstablishment" in types), "FAQPage" in types, max(faq_counts or [0]), sorted(forbidden)


def apply_page(page: str, config: dict[str, Any]) -> PageResult:
    path = ROOT / page
    if not path.exists():
        return PageResult(page, False, "SKIP", bool(config.get("restaurant")), False, bool(config.get("faq")), False, 0, [], False, ["file missing"])
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated = strip_old_block(original)
    updated = sanitize_jsonld(updated)
    updated = insert_block(updated, schema_block(config))
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    restaurant_found, faq_found, faq_questions, forbidden = audit_html(updated)
    warnings: list[str] = []
    if config.get("restaurant") and not restaurant_found:
        warnings.append("Restaurant schema missing")
    if config.get("faq") and (not faq_found or faq_questions < 8):
        warnings.append("FAQPage missing or below 8 questions")
    if forbidden:
        warnings.append("forbidden rating/review terms found")
    status = "PASS" if not warnings else "FAIL"
    return PageResult(page, True, status, bool(config.get("restaurant")), restaurant_found, bool(config.get("faq")), faq_found, faq_questions, forbidden, changed, warnings)


def write_reports(results: list[PageResult]) -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    status = "PASS" if all(r.status in {"PASS", "SKIP"} for r in results) else "FAIL"
    payload = {"status": status, "results": [asdict(r) for r in results]}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Static Schema Product Pages Audit",
        "",
        f"Status geral: **{status}**",
        "",
        "## Critérios",
        "- Restaurant Schema estático no HTML das páginas de produto críticas.",
        "- FAQPage estático com 8 perguntas nas páginas configuradas.",
        "- Nenhum campo de rating/review proibido no JSON-LD.",
        "- Páginas inexistentes são marcadas como SKIP, não como FAIL.",
        "",
        "## Resultados por página",
    ]
    for r in results:
        lines.append(f"- `{r.page}` — **{r.status}** — Restaurant={r.restaurant_found} — FAQ={r.faq_found} ({r.faq_questions}) — changed={r.changed}")
        if r.forbidden_terms:
            lines.append("  - forbidden: " + ", ".join(r.forbidden_terms))
        for warning in r.warnings:
            lines.append(f"  - {warning}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Static product schema/FAQ audit: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    results = [apply_page(page, cfg) for page, cfg in PAGES.items()]
    return write_reports(results)


if __name__ == "__main__":
    raise SystemExit(main())
