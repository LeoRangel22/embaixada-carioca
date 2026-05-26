#!/usr/bin/env python3
"""Apply static Restaurant Schema and FAQPage blocks to priority product pages.

P1B objective:
- Guarantee that critical product/location pages expose JSON-LD in the static HTML.
- Avoid relying on runtime JavaScript injection for FAQPage or Restaurant schema.
- Add 8-question FAQPage blocks to pages that need AIO/GEO visibility.
- Keep Google-rating-derived fields out of JSON-LD.

This script is idempotent: it replaces only the block marked below and leaves other page content intact.
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
FORBIDDEN_TERMS = {"AggregateRating", "aggregateRating", "ratingValue", "reviewCount", "ratingCount", "bestRating", "worstRating"}
JSONLD_RE = re.compile(r'<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)

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

PAGES: dict[str, dict[str, Any]] = {
    "eventos.html": {"lang": "pt", "kind": "events", "restaurant": True, "faq": True, "url": SITE + "/eventos.html"},
    "cardapio.html": {"lang": "pt", "kind": "menu", "restaurant": True, "faq": True, "url": SITE + "/cardapio.html"},
    "almoco.html": {"lang": "pt", "kind": "lunch", "restaurant": True, "faq": True, "url": SITE + "/almoco.html"},
    "entardecer.html": {"lang": "pt", "kind": "sunset", "restaurant": True, "faq": True, "url": SITE + "/entardecer.html"},
    "feijoada.html": {"lang": "pt", "kind": "feijoada", "restaurant": True, "faq": True, "url": SITE + "/feijoada.html"},
    "cafe-da-manha.html": {"lang": "pt", "kind": "breakfast", "restaurant": True, "faq": True, "url": SITE + "/cafe-da-manha.html"},
    "morro-da-urca.html": {"lang": "pt", "kind": "morro", "restaurant": False, "faq": True, "url": SITE + "/morro-da-urca.html"},

    "en/sunset.html": {"lang": "en", "kind": "sunset", "restaurant": True, "faq": True, "url": SITE + "/en/sunset.html"},
    "en/cardapio.html": {"lang": "en", "kind": "menu", "restaurant": True, "faq": True, "url": SITE + "/en/cardapio.html"},
    "en/almoco.html": {"lang": "en", "kind": "lunch", "restaurant": True, "faq": True, "url": SITE + "/en/almoco.html"},
    "en/morro-da-urca.html": {"lang": "en", "kind": "morro", "restaurant": False, "faq": True, "url": SITE + "/en/morro-da-urca.html"},

    "es/atardecer.html": {"lang": "es", "kind": "sunset", "restaurant": True, "faq": True, "url": SITE + "/es/atardecer.html"},
    "es/cardapio.html": {"lang": "es", "kind": "menu", "restaurant": True, "faq": True, "url": SITE + "/es/cardapio.html"},
    "es/almoco.html": {"lang": "es", "kind": "lunch", "restaurant": True, "faq": True, "url": SITE + "/es/almoco.html"},
    "es/morro-da-urca.html": {"lang": "es", "kind": "morro", "restaurant": False, "faq": True, "url": SITE + "/es/morro-da-urca.html"},
}

FAQ_LIBRARY: dict[str, dict[str, list[tuple[str, str]]]] = {
    "pt": {
        "events": [
            ("A Embaixada Carioca realiza eventos no Morro da Urca?", "Sim. A casa recebe eventos corporativos, grupos, agências, celebrações e experiências gastronômicas dentro do Parque Bondinho Pão de Açúcar."),
            ("O evento precisa de ingresso do Bondinho?", "Sim. Como a Embaixada Carioca fica dentro do Parque Bondinho Pão de Açúcar, o acesso acontece pela operação do parque."),
            ("Quais tipos de evento podem ser feitos na Embaixada Carioca?", "A casa atende coquetéis, cafés da manhã, grupos turísticos, eventos corporativos, welcome drinks e celebrações com vista no Morro da Urca."),
            ("A Embaixada Carioca atende grupos de turismo?", "Sim. O restaurante é adequado para grupos que desejam uma experiência carioca durante a visita ao Pão de Açúcar."),
            ("É possível fazer café da manhã de evento?", "Sim. A Embaixada Carioca oferece café da manhã para grupos e eventos, com serviço organizado conforme o formato contratado."),
            ("O restaurante tem vista para eventos?", "Sim. A localização no Morro da Urca oferece uma experiência de evento associada ao cenário do Parque Bondinho."),
            ("Como solicitar orçamento de evento?", "O orçamento pode ser solicitado pelo e-mail de eventos ou pelo WhatsApp oficial da Embaixada Carioca."),
            ("A Embaixada Carioca oferece comida brasileira em eventos?", "Sim. A proposta gastronômica valoriza comida brasileira e carioca, além de bebidas como caipirinhas e chope."),
        ],
        "menu": [
            ("O que tem no cardápio da Embaixada Carioca?", "O cardápio reúne café da manhã, almoço brasileiro, pratos cariocas, petiscos, caipirinhas, chope e bebidas para a visita ao Morro da Urca."),
            ("A Embaixada Carioca serve café da manhã todos os dias?", "Sim. O café da manhã é servido todos os dias no Morro da Urca."),
            ("Quais são os pratos principais da casa?", "Entre os destaques estão picanha, feijoada, bobó de camarão, pratos brasileiros, petiscos e sobremesas."),
            ("A casa serve caipirinha?", "Sim. A caipirinha é uma das especialidades da Embaixada Carioca."),
            ("O cardápio tem opções para almoço?", "Sim. A casa serve almoço brasileiro no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar."),
            ("O restaurante serve chope?", "Sim. A Embaixada Carioca trabalha com chope Heineken e outras bebidas."),
            ("O cardápio é adequado para turistas?", "Sim. A proposta é apresentar uma experiência gastronômica carioca para visitantes do Pão de Açúcar."),
            ("Onde consultar o cardápio online?", "O cardápio online pode ser acessado pelo QR code e pelos canais oficiais da Embaixada Carioca."),
        ],
        "lunch": [
            ("Onde almoçar no Pão de Açúcar?", "A Embaixada Carioca fica no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, e serve almoço brasileiro."),
            ("O almoço fica na primeira parada do Bondinho?", "Sim. O restaurante fica no Morro da Urca, a primeira parada do bondinho."),
            ("Quais pratos são servidos no almoço?", "A casa serve pratos brasileiros e cariocas, como picanha, feijoada, bobó de camarão e opções de petiscos."),
            ("Preciso reservar para almoçar?", "A reserva é recomendada em períodos de maior movimento, especialmente fins de semana, feriados e grupos."),
            ("O restaurante é indicado para turistas?", "Sim. A proposta da Embaixada Carioca é oferecer uma experiência carioca autêntica durante o passeio ao Pão de Açúcar."),
            ("O almoço combina com visita ao Bondinho?", "Sim. A localização permite almoçar durante a visita ao Parque Bondinho, sem sair do passeio."),
            ("A casa serve bebidas no almoço?", "Sim. Há caipirinhas, chope, drinks, bebidas sem álcool e outras opções."),
            ("O almoço tem vista no Morro da Urca?", "Sim. A experiência de almoço acontece dentro do Parque Bondinho Pão de Açúcar, no Morro da Urca."),
        ],
        "sunset": [
            ("Onde ver o entardecer no Morro da Urca?", "A Embaixada Carioca oferece uma experiência gastronômica no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar."),
            ("A Embaixada Carioca é boa para o fim de tarde?", "Sim. A casa combina caipirinhas, chope, petiscos e ambiente carioca para o fim de tarde no Morro da Urca."),
            ("Preciso de ingresso do Bondinho para ir ao entardecer?", "Sim. O acesso ao restaurante acontece dentro da visita ao Parque Bondinho Pão de Açúcar."),
            ("O que pedir no entardecer?", "Caipirinhas, chope gelado, petiscos e pratos brasileiros são boas escolhas para a experiência."),
            ("O entardecer é indicado para turistas?", "Sim. É uma forma prática de unir o passeio ao Pão de Açúcar com gastronomia carioca."),
            ("A casa aceita grupos no entardecer?", "Sim. Grupos podem consultar disponibilidade e formatos pelo canal de eventos."),
            ("Tem comida no fim de tarde?", "Sim. O cardápio oferece petiscos, bebidas e opções gastronômicas conforme o horário da operação."),
            ("A experiência acontece no Morro da Urca?", "Sim. A Embaixada Carioca está localizada no Morro da Urca, primeira parada do bondinho."),
        ],
        "feijoada": [
            ("Tem feijoada na Embaixada Carioca?", "Sim. A feijoada é um dos pratos brasileiros associados à experiência gastronômica da casa."),
            ("A feijoada é servida no Morro da Urca?", "Sim. A Embaixada Carioca fica no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar."),
            ("A feijoada combina com o passeio ao Pão de Açúcar?", "Sim. É uma opção para quem deseja uma refeição brasileira durante a visita ao parque."),
            ("A feijoada serve mais de uma pessoa?", "A disponibilidade e o formato de serviço devem ser confirmados no cardápio do dia."),
            ("A casa também serve caipirinha?", "Sim. A caipirinha é uma das especialidades da Embaixada Carioca."),
            ("Preciso reservar para comer feijoada?", "A reserva é recomendada em dias de maior movimento ou para grupos."),
            ("A feijoada é indicada para turistas?", "Sim. É um prato brasileiro clássico para quem deseja experimentar a culinária carioca."),
            ("Onde fica o restaurante da feijoada?", "O restaurante fica no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar."),
        ],
        "breakfast": [
            ("Onde tomar café da manhã no Morro da Urca?", "A Embaixada Carioca serve café da manhã no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar."),
            ("O café da manhã é servido todos os dias?", "Sim. A Embaixada Carioca serve café da manhã todos os dias."),
            ("Preciso comprar ingresso do Bondinho para o café da manhã?", "Sim. O restaurante fica dentro do Parque Bondinho Pão de Açúcar."),
            ("O café da manhã é indicado para turistas?", "Sim. É uma forma prática de começar a visita ao Pão de Açúcar com uma experiência carioca."),
            ("O café da manhã aceita grupos?", "Sim. Grupos e eventos podem consultar condições e disponibilidade com a equipe de eventos."),
            ("O café da manhã tem vista?", "A experiência acontece no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar."),
            ("Posso reservar café da manhã?", "Sim. As reservas podem ser feitas pelos canais oficiais da Embaixada Carioca."),
            ("O café da manhã tem opções brasileiras?", "Sim. A proposta valoriza sabores brasileiros em uma experiência no Morro da Urca."),
        ],
        "morro": [
            ("Onde fica o Morro da Urca?", "O Morro da Urca é a primeira parada do Bondinho Pão de Açúcar, no Rio de Janeiro."),
            ("A Embaixada Carioca fica no Morro da Urca?", "Sim. A Embaixada Carioca fica dentro do Parque Bondinho Pão de Açúcar, no Morro da Urca."),
            ("Como chegar à Embaixada Carioca?", "O acesso acontece pela visita ao Parque Bondinho Pão de Açúcar, subindo até a primeira parada no Morro da Urca."),
            ("Preciso de ingresso para acessar o Morro da Urca pelo Bondinho?", "Sim. O acesso pelo bondinho faz parte da operação do Parque Bondinho Pão de Açúcar."),
            ("Tem restaurante no Morro da Urca?", "Sim. A Embaixada Carioca é uma opção gastronômica no Morro da Urca."),
            ("Dá para almoçar no Morro da Urca?", "Sim. A Embaixada Carioca serve almoço brasileiro no Morro da Urca."),
            ("Tem café da manhã no Morro da Urca?", "Sim. A Embaixada Carioca serve café da manhã todos os dias."),
            ("O Morro da Urca é bom para turistas?", "Sim. É uma das experiências mais conhecidas do Rio e permite combinar passeio, vista e gastronomia."),
        ],
    },
}

FAQ_LIBRARY["en"] = {
    "sunset": [("Where can I enjoy sunset at Morro da Urca?", "Embaixada Carioca offers a carioca food and drink experience inside Sugarloaf Cable Car Park, at Morro da Urca."), ("Is Embaixada Carioca good for late afternoon?", "Yes. The restaurant combines caipirinhas, draft beer, snacks and a Morro da Urca setting."), ("Do I need a cable car ticket?", "Yes. Access is through Parque Bondinho Pão de Açúcar."), ("What should I order at sunset?", "Caipirinhas, draft beer, snacks and Brazilian dishes are good choices."), ("Is the experience good for tourists?", "Yes. It combines the Sugarloaf visit with carioca gastronomy."), ("Can groups book this experience?", "Yes. Groups can check availability through the events channel."), ("Is food available in the late afternoon?", "Yes. Snacks, drinks and selected food options are available according to operating hours."), ("Is it located at Morro da Urca?", "Yes. Embaixada Carioca is at Morro da Urca, the first cable car stop.")],
    "menu": [("What is on the Embaixada Carioca menu?", "Breakfast, Brazilian lunch, carioca dishes, snacks, caipirinhas, draft beer and drinks."), ("Does the restaurant serve breakfast daily?", "Yes. Breakfast is served daily at Morro da Urca."), ("What are the main dishes?", "Highlights include picanha, feijoada, shrimp bobó, snacks and desserts."), ("Does the menu include caipirinhas?", "Yes. Caipirinha is one of the house specialties."), ("Does the menu include lunch?", "Yes. Brazilian lunch is served at Morro da Urca."), ("Does the restaurant serve draft beer?", "Yes. Embaixada Carioca serves Heineken draft beer and other drinks."), ("Is the menu suitable for tourists?", "Yes. It is designed for visitors looking for a carioca food experience."), ("Where can I view the online menu?", "The online menu is available through the official Embaixada Carioca channels and QR code.")],
    "lunch": [("Where can I have lunch at Sugarloaf?", "Embaixada Carioca is located at Morro da Urca inside Sugarloaf Cable Car Park and serves Brazilian lunch."), ("Is lunch served at the first cable car stop?", "Yes. The restaurant is located at Morro da Urca, the first stop."), ("What dishes are served for lunch?", "Brazilian and carioca dishes such as picanha, feijoada and shrimp bobó."), ("Should I book lunch?", "Booking is recommended on busy days and for groups."), ("Is the restaurant good for tourists?", "Yes. It offers an authentic carioca food experience during a Sugarloaf visit."), ("Does lunch fit into the cable car visit?", "Yes. You can eat during the park visit without leaving the attraction."), ("Are drinks available at lunch?", "Yes. Caipirinhas, draft beer, cocktails and soft drinks are available."), ("Is lunch served with a Morro da Urca setting?", "Yes. The experience takes place inside Parque Bondinho Pão de Açúcar at Morro da Urca.")],
    "morro": [("Where is Morro da Urca?", "Morro da Urca is the first stop of the Sugarloaf cable car in Rio de Janeiro."), ("Is Embaixada Carioca at Morro da Urca?", "Yes. It is inside Sugarloaf Cable Car Park at Morro da Urca."), ("How do I get to Embaixada Carioca?", "Access is through Parque Bondinho Pão de Açúcar, going up to the first stop."), ("Do I need a ticket?", "Yes. Access through the cable car is part of the park operation."), ("Is there a restaurant at Morro da Urca?", "Yes. Embaixada Carioca is a restaurant option at Morro da Urca."), ("Can I have lunch at Morro da Urca?", "Yes. Embaixada Carioca serves Brazilian lunch there."), ("Is breakfast available at Morro da Urca?", "Yes. Embaixada Carioca serves breakfast daily."), ("Is Morro da Urca good for tourists?", "Yes. It combines one of Rio's best-known attractions with views and gastronomy.")],
}
FAQ_LIBRARY["es"] = {
    "sunset": [("¿Dónde vivir el atardecer en Morro da Urca?", "Embaixada Carioca ofrece una experiencia carioca dentro del Parque Bondinho Pão de Açúcar, en Morro da Urca."), ("¿Embaixada Carioca es buena para la tarde?", "Sí. Combina caipirinhas, chope, petiscos y ambiente de Morro da Urca."), ("¿Necesito entrada del Bondinho?", "Sí. El acceso es por el Parque Bondinho Pão de Açúcar."), ("¿Qué pedir al atardecer?", "Caipirinhas, chope, petiscos y platos brasileños son buenas opciones."), ("¿Es recomendable para turistas?", "Sí. Une el paseo al Pão de Açúcar con gastronomía carioca."), ("¿Se pueden reservar grupos?", "Sí. Los grupos pueden consultar disponibilidad por el canal de eventos."), ("¿Hay comida por la tarde?", "Sí. Hay petiscos, bebidas y opciones según el horario de operación."), ("¿Está en Morro da Urca?", "Sí. Embaixada Carioca está en Morro da Urca, primera parada del teleférico.")],
    "menu": [("¿Qué hay en el menú de Embaixada Carioca?", "Desayuno, almuerzo brasileño, platos cariocas, petiscos, caipirinhas, chope y bebidas."), ("¿Sirve desayuno todos los días?", "Sí. El desayuno se sirve todos los días en Morro da Urca."), ("¿Cuáles son los platos principales?", "Destacan picanha, feijoada, bobó de camarón, petiscos y postres."), ("¿Hay caipirinhas?", "Sí. La caipirinha es una especialidad de la casa."), ("¿Hay opciones para almuerzo?", "Sí. Se sirve almuerzo brasileño en Morro da Urca."), ("¿Sirven chope?", "Sí. Embaixada Carioca sirve chope Heineken y otras bebidas."), ("¿El menú es adecuado para turistas?", "Sí. Fue pensado para visitantes que buscan una experiencia carioca."), ("¿Dónde ver el menú online?", "El menú online está disponible por QR code y canales oficiales.")],
    "lunch": [("¿Dónde almorzar en el Pão de Açúcar?", "Embaixada Carioca está en Morro da Urca, dentro del Parque Bondinho Pão de Açúcar, y sirve almuerzo brasileño."), ("¿El almuerzo es en la primera parada?", "Sí. El restaurante está en Morro da Urca, primera parada del teleférico."), ("¿Qué platos se sirven?", "Platos brasileños y cariocas como picanha, feijoada y bobó de camarón."), ("¿Conviene reservar?", "La reserva es recomendable en días de mucho movimiento y para grupos."), ("¿Es bueno para turistas?", "Sí. Ofrece una experiencia carioca durante el paseo al Pão de Açúcar."), ("¿El almuerzo combina con la visita?", "Sí. Se puede comer durante la visita al parque sin salir de la atracción."), ("¿Hay bebidas en el almuerzo?", "Sí. Hay caipirinhas, chope, cócteles y bebidas sin alcohol."), ("¿El almuerzo es en Morro da Urca?", "Sí. La experiencia ocurre dentro del Parque Bondinho, en Morro da Urca.")],
    "morro": [("¿Dónde está Morro da Urca?", "Morro da Urca es la primera parada del Bondinho Pão de Açúcar en Río de Janeiro."), ("¿Embaixada Carioca está en Morro da Urca?", "Sí. Está dentro del Parque Bondinho Pão de Açúcar, en Morro da Urca."), ("¿Cómo llegar a Embaixada Carioca?", "El acceso es por el Parque Bondinho Pão de Açúcar, subiendo hasta la primera parada."), ("¿Necesito entrada?", "Sí. El acceso por el teleférico forma parte de la operación del parque."), ("¿Hay restaurante en Morro da Urca?", "Sí. Embaixada Carioca es una opción gastronómica en Morro da Urca."), ("¿Puedo almorzar en Morro da Urca?", "Sí. Embaixada Carioca sirve almuerzo brasileño."), ("¿Hay desayuno en Morro da Urca?", "Sí. Embaixada Carioca sirve desayuno todos los días."), ("¿Morro da Urca es bueno para turistas?", "Sí. Combina paseo, vista y gastronomía.")],
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


def strip_old_block(source: str) -> str:
    return re.sub(re.escape(BLOCK_START) + r"[\s\S]*?" + re.escape(BLOCK_END) + r"\s*", "", source, flags=re.I)


def build_restaurant_schema(url: str) -> dict[str, Any]:
    schema = dict(RESTAURANT_BASE)
    schema["mainEntityOfPage"] = url
    return schema


def build_faq_schema(lang: str, kind: str, url: str) -> dict[str, Any]:
    faqs = FAQ_LIBRARY[lang][kind]
    return {
        "@type": "FAQPage",
        "@id": url.rstrip("/") + "#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs[:8]
        ],
    }


def build_block(config: dict[str, Any]) -> str:
    graph: list[dict[str, Any]] = []
    if config.get("restaurant"):
        graph.append(build_restaurant_schema(config["url"]))
    if config.get("faq"):
        graph.append(build_faq_schema(config["lang"], config["kind"], config["url"]))
    payload = {"@context": "https://schema.org", "@graph": graph}
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    leaked = sorted(term for term in FORBIDDEN_TERMS if term in serialized)
    if leaked:
        raise ValueError(f"Forbidden terms leaked into new schema: {leaked}")
    return f'{BLOCK_START}\n<script id="{SCRIPT_ID}" type="application/ld+json">{html.escape(serialized, quote=False)}</script>\n{BLOCK_END}\n'


def insert_before_head_close(source: str, block: str) -> str:
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
    forbidden = sorted(term for term in FORBIDDEN_TERMS if term in source)
    for raw in JSONLD_RE.findall(source):
        try:
            obj = json.loads(html.unescape(raw.strip()))
        except Exception:
            continue
        walk_schema(obj, types, faq_counts)
    return ("Restaurant" in types or "FoodEstablishment" in types), "FAQPage" in types, max(faq_counts or [0]), forbidden


def apply_page(page: str, config: dict[str, Any]) -> PageResult:
    path = ROOT / page
    if not path.exists():
        return PageResult(page, False, "SKIP", bool(config.get("restaurant")), False, bool(config.get("faq")), False, 0, [], False, ["file missing"])
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated = strip_old_block(original)
    updated = insert_before_head_close(updated, build_block(config))
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
        "- Nenhum campo de rating/review proibido no HTML.",
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
