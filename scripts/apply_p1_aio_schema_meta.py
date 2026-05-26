#!/usr/bin/env python3
"""Apply P1 AIO/SEO fixes for Embaixada Carioca.

Scope:
- FAQPage schema on PT/EN/ES home pages.
- Restaurant schema on critical conversion/product pages.
- Meta description normalization on the same priority pages.

Rules:
- Do not add aggregateRating, reviewCount, ratingValue, or Google review-derived ratings.
- Keep changes idempotent through a named HTML block.
"""
from __future__ import annotations

from pathlib import Path
import html
import json
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BLOCK_START = "<!-- EC P1 AIO Schema + Meta Fix -->"
BLOCK_END = "<!-- /EC P1 AIO Schema + Meta Fix -->"
SITE = "https://www.embaixadacarioca.com"

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
        {"@type": "LocationFeatureSpecification", "name": "Vista para o Pão de Açúcar", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Dentro do Parque Bondinho Pão de Açúcar", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Atendimento para grupos e eventos", "value": True},
    ],
    "sameAs": [
        "https://www.instagram.com/embaixadacarioca/",
        "https://www.wikidata.org/wiki/Q8678",
    ],
    "potentialAction": {
        "@type": "ReserveAction",
        "target": "https://go.tagme.com.br/embaixadacarioca",
    },
}

FAQS = {
    "pt": [
        ("Onde fica a Embaixada Carioca?", "A Embaixada Carioca fica no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, na primeira parada do bondinho."),
        ("Preciso comprar ingresso do Bondinho para ir ao restaurante?", "Sim. O restaurante fica dentro do Parque Bondinho Pão de Açúcar, portanto o acesso ocorre pela visita ao parque."),
        ("A Embaixada Carioca serve café da manhã?", "Sim. A Embaixada Carioca serve café da manhã todos os dias, com opções brasileiras e vista para o Morro da Urca."),
        ("O restaurante serve almoço no Morro da Urca?", "Sim. A casa serve almoço com comida brasileira e carioca, incluindo pratos como picanha, feijoada e bobó de camarão."),
        ("A Embaixada Carioca aceita reservas?", "Sim. As reservas podem ser feitas pelo link oficial de reservas da Embaixada Carioca."),
        ("A Embaixada Carioca é boa para turistas?", "Sim. A proposta da casa é apresentar uma experiência carioca autêntica para visitantes que desejam comer bem durante o passeio ao Pão de Açúcar."),
        ("A Embaixada Carioca realiza eventos?", "Sim. A casa recebe eventos corporativos, grupos, agências, celebrações e experiências gastronômicas com vista no Morro da Urca."),
        ("Qual é a especialidade da Embaixada Carioca?", "A casa é reconhecida por caipirinhas, chope Heineken, comida carioca tradicional e experiências com vista dentro do Parque Bondinho."),
    ],
    "en": [
        ("Where is Embaixada Carioca located?", "Embaixada Carioca is located on Morro da Urca, inside Parque Bondinho Pão de Açúcar, at the first cable car stop."),
        ("Do I need a Sugarloaf cable car ticket to visit the restaurant?", "Yes. The restaurant is inside Parque Bondinho Pão de Açúcar, so access is part of the park visit."),
        ("Does Embaixada Carioca serve breakfast?", "Yes. Embaixada Carioca serves breakfast daily with Brazilian options and a Morro da Urca setting."),
        ("Can I have lunch at Embaixada Carioca?", "Yes. The restaurant serves Brazilian and carioca food, including picanha, feijoada and shrimp bobó."),
        ("Does Embaixada Carioca take reservations?", "Yes. Reservations can be made through the official Embaixada Carioca booking link."),
        ("Is Embaixada Carioca good for tourists?", "Yes. The restaurant is designed for visitors who want an authentic carioca food experience during a Sugarloaf visit."),
        ("Does Embaixada Carioca host events?", "Yes. The venue hosts corporate events, groups, agencies, celebrations and gastronomic experiences with views from Morro da Urca."),
        ("What is Embaixada Carioca known for?", "It is known for caipirinhas, Heineken draft beer, traditional carioca food and a privileged location inside Parque Bondinho."),
    ],
    "es": [
        ("¿Dónde está Embaixada Carioca?", "Embaixada Carioca está en el Morro da Urca, dentro del Parque Bondinho Pão de Açúcar, en la primera parada del teleférico."),
        ("¿Necesito entrada del Bondinho para ir al restaurante?", "Sí. El restaurante está dentro del Parque Bondinho Pão de Açúcar, por lo que el acceso forma parte de la visita al parque."),
        ("¿Embaixada Carioca sirve desayuno?", "Sí. Embaixada Carioca sirve desayuno todos los días con opciones brasileñas y ambiente del Morro da Urca."),
        ("¿Puedo almorzar en Embaixada Carioca?", "Sí. El restaurante sirve comida brasileña y carioca, con platos como picanha, feijoada y bobó de camarón."),
        ("¿Embaixada Carioca acepta reservas?", "Sí. Las reservas se pueden hacer por el enlace oficial de reservas de Embaixada Carioca."),
        ("¿Embaixada Carioca es recomendable para turistas?", "Sí. La casa fue pensada para visitantes que quieren una experiencia carioca auténtica durante el paseo al Pão de Açúcar."),
        ("¿Embaixada Carioca realiza eventos?", "Sí. La casa recibe eventos corporativos, grupos, agencias, celebraciones y experiencias gastronómicas con vista desde el Morro da Urca."),
        ("¿Cuál es la especialidad de Embaixada Carioca?", "La casa es conocida por caipirinhas, chope Heineken, comida carioca tradicional y ubicación dentro del Parque Bondinho."),
    ],
}

PAGES: dict[str, dict[str, Any]] = {
    "index.html": {
        "lang": "pt",
        "meta": "Restaurante no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com café da manhã, almoço, caipirinhas, chope e eventos com vista.",
        "faq": True,
        "restaurant": True,
        "url": SITE + "/",
    },
    "en/index.html": {
        "lang": "en",
        "meta": "Restaurant on Morro da Urca inside Sugarloaf Cable Car Park, serving breakfast, lunch, caipirinhas, draft beer and events with a view.",
        "faq": True,
        "restaurant": True,
        "url": SITE + "/en/",
    },
    "es/index.html": {
        "lang": "es",
        "meta": "Restaurante en Morro da Urca dentro del Parque Bondinho Pão de Açúcar, con desayuno, almuerzo, caipirinhas y eventos con vista.",
        "faq": True,
        "restaurant": True,
        "url": SITE + "/es/",
    },
    "eventos.html": {
        "lang": "pt",
        "meta": "Eventos corporativos, grupos e celebrações no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com gastronomia carioca e vista.",
        "restaurant": True,
        "url": SITE + "/eventos.html",
    },
    "cardapio.html": {
        "lang": "pt",
        "meta": "Cardápio da Embaixada Carioca no Morro da Urca: café da manhã, almoço, pratos brasileiros, caipirinhas, chope e petiscos.",
        "restaurant": True,
        "url": SITE + "/cardapio.html",
    },
    "almoco.html": {
        "lang": "pt",
        "meta": "Almoço brasileiro no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com picanha, feijoada, bobó, caipirinhas e vista.",
        "restaurant": True,
        "url": SITE + "/almoco.html",
    },
    "cafe-da-manha.html": {
        "lang": "pt",
        "meta": "Café da manhã no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com experiência carioca, pães, frutas, bebidas e vista.",
        "restaurant": True,
        "url": SITE + "/cafe-da-manha.html",
    },
    "entardecer.html": {
        "lang": "pt",
        "meta": "Entardecer no Morro da Urca com caipirinhas, chope, petiscos e vista no Parque Bondinho Pão de Açúcar.",
        "restaurant": True,
        "url": SITE + "/entardecer.html",
    },
    "en/eventos.html": {
        "lang": "en",
        "meta": "Corporate events, groups and celebrations at Morro da Urca inside Sugarloaf Cable Car Park, with Brazilian food and views.",
        "restaurant": True,
        "url": SITE + "/en/eventos.html",
    },
    "en/almoco.html": {
        "lang": "en",
        "meta": "Brazilian lunch on Morro da Urca inside Sugarloaf Cable Car Park, with picanha, feijoada, shrimp bobó, caipirinhas and views.",
        "restaurant": True,
        "url": SITE + "/en/almoco.html",
    },
    "en/cafe-da-manha.html": {
        "lang": "en",
        "meta": "Breakfast on Morro da Urca inside Sugarloaf Cable Car Park, with Brazilian flavors, fruit, breads, hot drinks and views.",
        "restaurant": True,
        "url": SITE + "/en/cafe-da-manha.html",
    },
    "en/sunset.html": {
        "lang": "en",
        "meta": "Sunset at Morro da Urca with caipirinhas, draft beer, snacks and views inside Sugarloaf Cable Car Park.",
        "restaurant": True,
        "url": SITE + "/en/sunset.html",
    },
    "es/eventos.html": {
        "lang": "es",
        "meta": "Eventos corporativos, grupos y celebraciones en Morro da Urca, dentro del Parque Bondinho Pão de Açúcar, con gastronomía y vista.",
        "restaurant": True,
        "url": SITE + "/es/eventos.html",
    },
    "es/almoco.html": {
        "lang": "es",
        "meta": "Almuerzo brasileño en Morro da Urca, dentro del Parque Bondinho Pão de Açúcar, con picanha, feijoada, bobó, caipirinhas y vista.",
        "restaurant": True,
        "url": SITE + "/es/almoco.html",
    },
    "es/cafe-da-manha.html": {
        "lang": "es",
        "meta": "Desayuno en Morro da Urca, dentro del Parque Bondinho Pão de Açúcar, con sabores brasileños, frutas, panes, bebidas y vista.",
        "restaurant": True,
        "url": SITE + "/es/cafe-da-manha.html",
    },
    "es/atardecer.html": {
        "lang": "es",
        "meta": "Atardecer en Morro da Urca con caipirinhas, chope, petiscos y vista dentro del Parque Bondinho Pão de Açúcar.",
        "restaurant": True,
        "url": SITE + "/es/atardecer.html",
    },
}

FORBIDDEN_RATING_TERMS = ("aggregateRating", "ratingValue", "reviewCount", "ratingCount", "bestRating", "worstRating")


def strip_old_block(source: str) -> str:
    pattern = re.compile(re.escape(BLOCK_START) + r"[\s\S]*?" + re.escape(BLOCK_END) + r"\s*", re.I)
    return pattern.sub("", source)


def update_meta_description(source: str, description: str) -> str:
    meta = f'<meta name="description" content="{html.escape(description, quote=True)}">'
    pattern = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']*["\']\s*/?>', re.I)
    if pattern.search(source):
        return pattern.sub(meta, source, count=1)
    title_match = re.search(r'</title>', source, re.I)
    if title_match:
        return source[: title_match.end()] + "\n  " + meta + source[title_match.end():]
    return source.replace("</head>", "  " + meta + "\n</head>", 1)


def faq_schema(lang: str, url: str) -> dict[str, Any]:
    return {
        "@type": "FAQPage",
        "@id": url.rstrip("/") + "#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in FAQS[lang]
        ],
    }


def restaurant_schema(url: str) -> dict[str, Any]:
    data = dict(RESTAURANT_BASE)
    data["mainEntityOfPage"] = url
    return data


def schema_block(config: dict[str, Any]) -> str:
    graph: list[dict[str, Any]] = []
    if config.get("restaurant"):
        graph.append(restaurant_schema(config["url"]))
    if config.get("faq"):
        graph.append(faq_schema(config["lang"], config["url"]))
    if not graph:
        return ""
    payload = {"@context": "https://schema.org", "@graph": graph}
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    for term in FORBIDDEN_RATING_TERMS:
        if term in serialized:
            raise ValueError(f"Forbidden rating term leaked into schema: {term}")
    return f'{BLOCK_START}\n<script id="ec-p1-aio-schema-meta" type="application/ld+json">{serialized}</script>\n{BLOCK_END}\n'


def insert_schema_block(source: str, block: str) -> str:
    if not block:
        return source
    if "</head>" in source:
        return source.replace("</head>", block + "</head>", 1)
    return source + "\n" + block


def apply_page(path: Path, config: dict[str, Any]) -> bool:
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated = strip_old_block(original)
    updated = update_meta_description(updated, config["meta"])
    updated = insert_schema_block(updated, schema_block(config))
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed: list[str] = []
    missing: list[str] = []
    for rel, config in PAGES.items():
        path = ROOT / rel
        if not path.exists():
            missing.append(rel)
            continue
        if apply_page(path, config):
            changed.append(rel)

    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report = [
        "# P1 AIO Schema + Meta Report",
        "",
        "## Scope",
        "- FAQPage schema on PT/EN/ES home pages.",
        "- Restaurant schema on critical conversion/product pages.",
        "- Meta description normalization on priority pages.",
        "- No aggregateRating, ratingValue, reviewCount or Google-review-derived rating fields.",
        "",
        "## Changed files",
    ]
    report.extend([f"- `{item}`" for item in changed] or ["- none"])
    report.extend(["", "## Missing/skipped files"])
    report.extend([f"- `{item}`" for item in missing] or ["- none"])
    report_path = report_dir / "p1_aio_schema_meta_report.md"
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")

    print("P1 AIO schema/meta changed:", len(changed))
    for item in changed:
        print("-", item)
    if missing:
        print("P1 AIO schema/meta skipped missing:")
        for item in missing:
            print("-", item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
