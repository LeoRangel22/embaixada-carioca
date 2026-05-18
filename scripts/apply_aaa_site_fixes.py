#!/usr/bin/env python3
"""
Apply AAA / 6-star editorial, multilingual, SEO and local-business fixes
for Embaixada Carioca static HTML pages.

Scope:
- PT / EN / ES home and subpages
- visible copy residues
- meta descriptions / OG / Twitter language residues
- JSON-LD hours, review count, inLanguage
- canonical / og:url consistency
- dangerous/over-specific event capacity claims

This script is intentionally conservative: it preserves layout/CSS/HTML structure
and applies text + metadata replacements only.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.embaixadacarioca.com"
REVIEW_COUNT = "7779"

HTML_FILES = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts]
REPORT_LINES: list[str] = []

# Slug mapping for canonical/og:url. Keep current public slugs unless clearly localized.
LOCALIZED_SLUGS = {
    "index": {"pt": "", "en": "en/", "es": "es/"},
    "cafe-da-manha": {"pt": "cafe-da-manha", "en": "en/cafe-da-manha", "es": "es/cafe-da-manha"},
    "almoco": {"pt": "almoco", "en": "en/almoco", "es": "es/almoco"},
    "entardecer": {"pt": "entardecer", "en": "en/sunset", "es": "es/atardecer"},
    "sunset": {"pt": "entardecer", "en": "en/sunset", "es": "es/atardecer"},
    "atardecer": {"pt": "entardecer", "en": "en/sunset", "es": "es/atardecer"},
    "eventos": {"pt": "eventos", "en": "en/eventos", "es": "es/eventos"},
    "cardapio": {"pt": "cardapio", "en": "en/cardapio", "es": "es/cardapio"},
    "guia-do-rio": {"pt": "guia-do-rio", "en": "en/guia-do-rio", "es": "es/guia-do-rio"},
    "contato": {"pt": "contato", "en": "en/contato", "es": "es/contato"},
    "nossa-visao": {"pt": "nossa-visao", "en": "en/nossa-visao", "es": "es/nossa-visao"},
}

# Files that should not be indexed if legacy/duplicates exist.
LEGACY_PATTERNS = [
    re.compile(r"home\s*v\d+", re.I),
    re.compile(r"home[-_ ]?v\d+", re.I),
]

GLOBAL_REPLACEMENTS = {
    "Parque BondinhSugarloaf Mountain": "Bondinho Pão de Açúcar Park",
    "BondinhSugarloaf Mountain": "Bondinho Pão de Açúcar",
    "Parque Bondinhel Pan de Azúcar": "Parque Bondinho Pão de Açúcar",
    "Parque Bondinhel Pan de Azúcar®": "Parque Bondinho Pão de Açúcar®",
    "Bondinhel Pan de Azúcar": "Parque Bondinho Pão de Açúcar",
    "vista para o o Bondinho": "vista para o Pão de Açúcar",
    "vista direta para o Bondinho": "vista direta para o Pão de Açúcar",
    "vista frontal para o Bondinho": "vista frontal para o Pão de Açúcar",
    "vista para o Bondinho": "vista para o Pão de Açúcar",
    "Vista direta para o Bondinho": "Vista direta para o Pão de Açúcar",
    "Vista panorâmica para o Bondinho": "Vista panorâmica para o Pão de Açúcar",
    "Morro da Urca e Morro da Urca": "Morro da Urca e no Parque Bondinho Pão de Açúcar",
    "Morro da Urca, dentro do Parque Bondinho, no Morro da Urca": "Morro da Urca, dentro do Parque Bondinho Pão de Açúcar",
    "Pão de Açúcar para o Pão de Açúcar": "Pão de Açúcar",
    "para o o Pão de Açúcar": "para o Pão de Açúcar",
    "referência em do Rio": "referência no Rio",
    "Embaixada Carioca restaurante": "Embaixada Carioca",
    "restaurante café da manhã": "café da manhã",
    "Embaixada Carioca aberto": "Embaixada Carioca abre",
    "Capacidade para 300+ convidados": "Capacidade variável conforme formato, montagem e áreas utilizadas",
    "capacidade para 300+ convidados": "capacidade variável conforme formato, montagem e áreas utilizadas",
    "Até 300 convidados": "Capacidade conforme formato",
    "até 300 convidados": "capacidade conforme formato",
    "até 300 pessoas": "capacidade conforme formato",
    "300+ convidados": "capacidade conforme formato",
    "300+ guests": "capacity varies by format",
    "300+ invitados": "capacidad según montaje",
    "até 300 pax": "capacidade conforme montagem",
    "up to 300 pax": "capacity varies by format",
    "hasta 300 pax": "capacidad según montaje",
    "maximumAttendeeCapacity": "_maximumAttendeeCapacity_removed",
}

EN_REPLACEMENTS = {
    "Inauguração": "Opening",
    "Altura": "Altitude",
    "227 metros · sobre a Baía": "227 meters · above the bay",
    "sobre a Baía": "above the bay",
    "★ best feijoada ★ PRÊMIO": "★ award-winning feijoada ★",
    "PRÊMIO": "award",
    "Quando Every day": "Served every day",
    "Quando": "When",
    "Harmonização Selected cachaças and wines": "Pairing: selected cachaças and wines",
    "Harmonização": "Pairing:",
    "Eventos corporativos.": "Corporate events",
    "Roteiros & grupos.": "Travel groups & curated itineraries",
    "Roteiros & grupos": "Travel groups & curated itineraries",
    "Restaurante Urca Hill": "Embaixada Carioca",
    "The most unique romantic experience": "One of the most memorable romantic experiences",
    "most unique": "most memorable",
    "11h30 – 17h": "11:30 AM – 5:00 PM",
    "11h30–17h": "11:30 AM–5:00 PM",
    "17h – 21h": "5:00 PM – 9:00 PM",
    "8h30": "8:30 AM",
    "12 PM – 5 PM": "11:30 AM – 5:00 PM",
    "12–5 PM": "11:30 AM–5:00 PM",
    "12pm to 5pm": "11:30 AM to 5:00 PM",
    "12pm": "11:30 AM",
    "Mon–Fri 12–4pm, Sat–Sun 12–5pm": "every day from 11:30 AM to 5:00 PM",
    "Parque Sugarloaf Mountain": "Bondinho Pão de Açúcar Park",
    "Sugarloaf Mountain Cable Car Park": "Bondinho Pão de Açúcar Park",
    "Sugarloaf cable car park": "Bondinho Pão de Açúcar Park",
    "restaurant inside Sugarloaf cable car park": "restaurant inside Bondinho Pão de Açúcar Park",
    "free to access for dining": "accessible depending on how you arrive",
    "No cable car ticket is required to access the restaurant.": "If you take the cable car, a regular Bondinho Pão de Açúcar Park ticket is required. If you hike up via the Praia Vermelha trail, when open, no cable car ticket is needed.",
    "No cable car ticket is required": "A cable car ticket is not required only if you hike up via the Praia Vermelha trail, when open",
    "by car or Uber to Av. Pasteur, 520": "by car or Uber to the Bondinho Pão de Açúcar Park entrance at Av. Pasteur, 520; from there, access to Urca Hill is by cable car or by the Praia Vermelha trail, when open",
    "Gastronomia italiana e brasileira no coração do Museu de Arte Moderna do Rio de Janeiro, com vista para a Baía de Guanabara e Sugarloaf Mountain.": "Italian and Brazilian cuisine in the heart of Rio de Janeiro’s Museum of Modern Art, with views of Guanabara Bay and Sugarloaf Mountain.",
    "Gastronomia italiana e brasileira no coração do Museu de Arte Moderna": "Italian and Brazilian cuisine in the heart of Rio de Janeiro’s Museum of Modern Art",
    "A vista mais bonita do Rio de Janeiro": "One of Rio’s most beautiful views",
    "Drinks com vista para a Baía de Guanabara": "Drinks with a view of Guanabara Bay",
    "Gastronomia brasileira com Sugarloaf Mountain ao fundo": "Brazilian cuisine with Sugarloaf Mountain in the background",
    "Pôr do sol atrás of Sugarloaf Mountain visto da Embaixada Carioca, Urca Hill": "Sunset behind Sugarloaf Mountain seen from Embaixada Carioca, Urca Hill",
    "Breakfast na Embaixada Carioca": "Breakfast at Embaixada Carioca",
    "Menu da Embaixada Carioca": "Embaixada Carioca menu",
    "Restaurant no Urca Hill": "restaurant on Urca Hill",
    "lunch com vista": "lunch with a view",
    "restaurante brasileiro": "Brazilian restaurant",
    "best feijoada do Brasil": "best feijoada in Brazil",
    "roteiro Rio de Janeiro": "Rio de Janeiro itinerary",
    "o que fazer no Rio de Janeiro": "what to do in Rio de Janeiro",
    "onde comer no Rio de Janeiro": "where to eat in Rio de Janeiro",
    "melhores praias Rio de Janeiro": "best beaches Rio de Janeiro",
    "restaurantes com vista Rio de Janeiro": "restaurants with a view Rio de Janeiro",
    "Roteiro Rio de Janeiro: O Guia Definitivo do que Fazer, Onde Ir e Onde Comer": "Rio de Janeiro Guide: What to Do, Where to Go and Where to Eat",
    "Guia completo de onde comer in Rio de Janeiro com vista. Os melhores restaurantes with a view of Sugarloaf Mountain, Cristo Redentor e Baía de Guanabara.": "Complete guide to where to eat in Rio de Janeiro with a view, including restaurants overlooking Sugarloaf Mountain, Christ the Redeemer and Guanabara Bay.",
    "Vista panorâmica do Pão de Açúcar a partir do Morro da Urca a partir do Morro da Urca": "Panoramic view of Sugarloaf Mountain from Urca Hill",
    "Panoramic view of Sugarloaf Mountain from Morro da Urca from Urca Hill": "Panoramic view of Sugarloaf Mountain from Urca Hill",
    "Capacity for capacity varies by format and setup": "Capacity varies by format and setup",
    "capacity for capacity varies by format and setup": "capacity varies by format and setup",
}

ES_REPLACEMENTS = {
    "Inauguração": "Inauguración",
    "Altura": "Altitud",
    "227 metros · sobre a Baía": "227 metros · sobre la bahía",
    "sobre a Baía": "sobre la bahía",
    "★ melhor feijoada ★ PRÊMIO": "★ mejor feijoada ★ premio",
    "melhor feijoada": "mejor feijoada",
    "PRÊMIO": "premio",
    "prazeres da mesa": "Prazeres da Mesa",
    "Quando Todos los días": "Servida todos los días",
    "Quando": "Cuándo",
    "Harmonização Cachaças y vinos seleccionados": "Maridaje: cachaças y vinos seleccionados",
    "Harmonização": "Maridaje:",
    "Roteiros & grupos.": "Itinerarios y grupos",
    "Roteiros & grupos": "Itinerarios y grupos",
    "O Morro da Urca é o seu evento — o espaço mais bonito do Rio de Janeiro.": "El Morro da Urca puede ser el escenario de su evento — un espacio panorámico inolvidable en Río de Janeiro.",
    "Confraternizaciones": "Celebraciones corporativas",
    "Capacitaciones & workshops": "Capacitaciones y talleres",
    "bebidas & snacks": "bebidas y aperitivos",
    "Venha nos visitar.": "Planifique su visita.",
    "Endereço & Acesso": "Dirección y acceso",
    "Acceso vía teleférico (teleférico) ou a pé pela Praia Vermelha": "Acceso en teleférico, con entrada regular del Parque Bondinho Pão de Açúcar, o a pie por el sendero de Praia Vermelha, cuando esté abierto",
    "Acceso vía teleférico": "Acceso en teleférico",
    "ou a pé pela Praia Vermelha": "o a pie por el sendero de Praia Vermelha",
    "8h30": "8:30",
    "11h30": "11:30",
    "17h": "17:00",
    "21h": "21:00",
    "12h–17:00": "11:30–17:00",
    "12h a 17:00": "11:30 a 17:00",
    "12h": "11:30",
    "el Pão de Açúcar": "el Pan de Azúcar",
    "al Pão de Açúcar": "al Pan de Azúcar",
    "del Pão de Açúcar": "del Pan de Azúcar",
    "Vista panorámica del Pão de Açúcar": "Vista panorámica al Pan de Azúcar",
    "Pan de Açúcar": "Pan de Azúcar",
    "Pão de Açúcar como telón": "Pan de Azúcar como telón",
    "Parque del Teleférico Pan de Azúcar": "Parque Bondinho Pão de Açúcar",
    "2ª mejor cerveza Heineken de Brasil": "2º mejor chopp Heineken de Brasil",
    "2ª mejor cerveza de Brasil": "2º mejor chopp Heineken de Brasil",
    "2ª Mejor Cerveza de Barril Heineken de Brasil": "2º mejor chopp Heineken de Brasil",
    "Mejor cerveza Heineken de barril de Río": "Mejor chopp Heineken de Río de Janeiro",
    "cerveza artesanal premiada": "chopp Heineken premiado",
    "la experiencia romántica más única": "una de las experiencias románticas más especiales",
    "La experiencia romántica más única": "Una de las experiencias románticas más especiales",
    "desayuno com vista": "desayuno con vista",
    "melhor desayuno": "mejor desayuno",
    "brunch com vista": "brunch con vista",
    "almuerzo com vista": "almuerzo con vista",
    "eventos com vista": "eventos con vista",
    "restaurante brasileiro": "restaurante brasileño",
    "aluguel espaço festas": "alquiler de espacio para fiestas",
    "Gastronomia italiana e brasileira": "Gastronomía italiana y brasileña",
    "Gastronomia brasileira": "Gastronomía brasileña",
    "Gastronomia": "Gastronomía",
    "com vista": "con vista",
    "na Embaixada Carioca": "en Embaixada Carioca",
    "Espaço para eventos": "Espacio para eventos",
    "aniversários": "aniversarios",
    "lançamentos": "lanzamientos",
    "roteiros": "itinerarios",
    "Recebemos grupos de agências": "Recibimos grupos de agencias",
    "Sim.": "Sí.",
    "Oferecemos": "Ofrecemos",
    "acesso preferencial": "acceso preferencial",
    "A vista mais bonita do Rio de Janeiro": "La vista más bonita de Río de Janeiro",
    "Drinks com vista para a Baía de Guanabara": "Bebidas con vista a la Bahía de Guanabara",
    "Gastronomia brasileira com el Pan de Azúcar ao fundo": "Gastronomía brasileña con el Pan de Azúcar al fondo",
    "Best restaurant in Rio de Janeiro with an incredible view of Sugarloaf Mountain. The caipirinhas and sunset experience are magic.": "El mejor restaurante de Río de Janeiro, con una vista increíble al Pan de Azúcar. Las caipirinhas y la experiencia del atardecer son mágicas.",
    "Chef Walace — a alma da Embaixada Carioca": "Chef Walace — el alma de Embaixada Carioca",
    "Menú da Embaixada Carioca": "Menú de Embaixada Carioca",
    "com vista al": "con vista al",
    "Rio de Janeiro": "Río de Janeiro",
    "roteiro Rio de Janeiro": "itinerario Río de Janeiro",
    "o que fazer no Rio de Janeiro": "qué hacer en Río de Janeiro",
    "dónde comer no Rio de Janeiro": "dónde comer en Río de Janeiro",
    "melhores praias Rio de Janeiro": "mejores playas Río de Janeiro",
    "restaurantes com vista Rio de Janeiro": "restaurantes con vista Río de Janeiro",
    "Roteiro Rio de Janeiro: O Guia Definitivo do que Fazer, Dónde Ir e Dónde Comer": "Guía de Río de Janeiro: qué hacer, dónde ir y dónde comer",
    "Guia completo de dónde comer en Río de Janeiro com vista. Os melhores restaurantes com vista al Pan de Azúcar, Cristo Redentor e Bahía de Guanabara.": "Guía completa sobre dónde comer en Río de Janeiro con vista, incluyendo restaurantes con vista al Pan de Azúcar, el Cristo Redentor y la Bahía de Guanabara.",
    "Vista panorámica del Pan de Azúcar desde el Morro da Urca desde el Morro da Urca": "Vista panorámica del Pan de Azúcar desde el Morro da Urca",
    "Pôr do sol atrás del Pan de Azúcar visto da Embaixada Carioca, Morro da Urca": "Puesta de sol detrás del Pan de Azúcar vista desde Embaixada Carioca, Morro da Urca",
    "tiene acceso gratuito para comer": "el acceso depende de cómo llegue",
    "No es necesario comprar entrada del bondinho": "Si sube en teleférico, debe comprar la entrada regular del Parque Bondinho Pão de Açúcar. Si sube por el sendero de Praia Vermelha, cuando esté abierto, no necesita entrada del teleférico",
    "Menú bilíngue": "Menú bilingüe",
    "bilíngue": "bilingüe",
    "2º mejor chopp Heineken de Brasil y el mejor de Río de Janeiro y la mejor de Río de Janeiro": "2º mejor chopp Heineken de Brasil y el mejor de Río de Janeiro",
}

META_REPLACEMENTS_BY_FILE = {
    "en/cafe-da-manha.html": {
        "The most beautiful breakfast in Rio de Janeiro. Full buffet and à la carte with a stunning view of Sugarloaf Mountain on Urca Hill. Every day from 8am to 11am.":
        "Breakfast with a view of Sugarloaf Mountain on Urca Hill, served daily from 8:30 AM to 11:30 AM at Embaixada Carioca.",
        "breakfast com vista Rio de Janeiro, breakfast Urca, melhor breakfast Rio de Janeiro, brunch com vista Rio, breakfast Pão de Açúcar":
        "breakfast with a view Rio de Janeiro, breakfast Urca Hill, best breakfast Rio de Janeiro, Sugarloaf Mountain breakfast, Embaixada Carioca breakfast",
    },
    "es/cafe-da-manha.html": {
        "El desayuno más bonito de Río de Janeiro. Buffet completo y à la carte con vistas al Pan de Azúcar en el Morro da Urca. Todos los días de 8h a 11h.":
        "Desayuno con vista al Pan de Azúcar en el Morro da Urca, servido todos los días de 8:30 a 11:30 en Embaixada Carioca.",
        "desayuno com vista Rio de Janeiro, desayuno Urca, melhor desayuno Rio de Janeiro, brunch com vista Rio, desayuno Pan de Azúcar":
        "desayuno con vista Río de Janeiro, desayuno Morro da Urca, mejor desayuno Río de Janeiro, desayuno Pan de Azúcar, Embaixada Carioca desayuno",
    },
    "en/almoco.html": {
        "Award-winning Brazilian cuisine at 227m altitude inside Bondinho Pão de Açúcar Park. Lunch with panoramic views Mon–Fri 12–4pm, Sat–Sun 12–5pm. Book online.":
        "Award-winning Brazilian cuisine at 227 meters, inside Bondinho Pão de Açúcar Park. Lunch with a view of Sugarloaf Mountain every day from 11:30 AM to 5:00 PM.",
        "lunch com vista Rio de Janeiro, restaurante Urca Hill, feijoada Urca Rio de Janeiro, picanha Rio de Janeiro restaurante, lunch Urca, restaurante brasileiro Urca, best feijoada do Brasil":
        "lunch with a view Rio de Janeiro, Urca Hill restaurant, feijoada Rio de Janeiro, picanha restaurant Rio de Janeiro, Brazilian restaurant Urca Hill, Embaixada Carioca lunch",
    },
    "es/almoco.html": {
        "almuerzo com vista Rio de Janeiro, restaurante Morro da Urca, feijoada Urca Rio de Janeiro, picanha Rio de Janeiro restaurante, almuerzo Urca, restaurante brasileiro Urca, mejor feijoada de Brasil":
        "almuerzo con vista Río de Janeiro, restaurante Morro da Urca, feijoada Río de Janeiro, picanha Río de Janeiro, restaurante brasileño Morro da Urca, Embaixada Carioca almuerzo",
    },
    "en/eventos.html": {
        "Corporate events, private parties and gastronomic experiences with 360° views in Rio de Janeiro. Capacity for capacity varies by format and setup on Urca Hill. Request a quote.":
        "Corporate events, private parties and gastronomic experiences with panoramic views in Rio de Janeiro. Capacity varies by format, setup and areas used on Urca Hill.",
    },
    "es/eventos.html": {
        "espacio para eventos Río de Janeiro con vista, eventos corporativos Rio de Janeiro, aluguel espaço festas Rio de Janeiro, desayuno para grupos Río, agencias de viajes del Pan de Azúcar, eventos com vista panorámica":
        "espacio para eventos Río de Janeiro con vista, eventos corporativos Río de Janeiro, alquiler de espacio para fiestas Río de Janeiro, desayuno para grupos Río, agencias de viajes Pan de Azúcar, eventos con vista panorámica",
    },
    "en/cardapio.html": {
        "Grilled picanha, award-winning feijoada, seafood and signature desserts. Full menu of the restaurant inside Parque Sugarloaf Mountain in Urca, Rio de Janeiro.":
        "Grilled picanha, award-winning feijoada, seafood and signature desserts. Full menu of Embaixada Carioca, inside Bondinho Pão de Açúcar Park, on Urca Hill.",
        "menu restaurante Urca Hill, menu Embaixada Carioca, feijoada Rio de Janeiro, caipirinha Rio de Janeiro, menu restaurante com vista Rio":
        "menu Urca Hill restaurant, Embaixada Carioca menu, feijoada Rio de Janeiro, caipirinha Rio de Janeiro, restaurant with a view Rio",
    },
    "es/cardapio.html": {
        "menú restaurante Morro da Urca, menú Embaixada Carioca, feijoada Rio de Janeiro, caipirinha Rio de Janeiro, menú restaurante com vista Rio":
        "menú restaurante Morro da Urca, menú Embaixada Carioca, feijoada Río de Janeiro, caipirinha Río de Janeiro, restaurante con vista Río",
    },
    "en/guia-do-rio.html": {
        "roteiro Rio de Janeiro, o que fazer no Rio de Janeiro, onde comer no Rio de Janeiro, melhores praias Rio de Janeiro, restaurantes com vista Rio de Janeiro":
        "Rio de Janeiro itinerary, what to do in Rio de Janeiro, where to eat in Rio de Janeiro, best beaches Rio de Janeiro, restaurants with a view Rio de Janeiro",
    },
    "es/guia-do-rio.html": {
        "roteiro Rio de Janeiro, o que fazer no Rio de Janeiro, dónde comer no Rio de Janeiro, melhores praias Rio de Janeiro, restaurantes com vista Rio de Janeiro":
        "itinerario Río de Janeiro, qué hacer en Río de Janeiro, dónde comer en Río de Janeiro, mejores playas Río de Janeiro, restaurantes con vista Río de Janeiro",
    },
}

PROHIBITED = [
    "BondinhSugarloaf",
    "Bondinhel",
    "Parque Bondinh",
    "Parque Bondinhel",
    "vista para o o Bondinho",
    "Pão de Açúcar para o Pão de Açúcar",
    "referência em do Rio",
    "Morro da Urca e Morro da Urca",
    "Embaixada Carioca restaurante",
    "restaurante café da manhã",
    "Capacity for capacity",
    "Urca Hill (Urca Hill)",
    "Urca Hill hill",
]

EN_FORBIDDEN = [
    "Inauguração", "Altura", "sobre a Baía", "Quando Every day", "Harmonização", "Eventos corporativos", "Roteiros & grupos",
    "Pôr do sol", " visto da ", " na Embaixada", "Menu da", " com vista", "restaurante brasileiro", "melhor breakfast",
]
ES_FORBIDDEN = [
    "Inauguração", "Altura", "sobre a Baía", "Quando", "Harmonização", "Roteiros & grupos", "Venha nos visitar",
    "Endereço & Acesso", " ou a pé", " com vista", "Espaço para eventos", "Gastronomia italiana e brasileira",
    "roteiro Rio", "o que fazer", "melhores praias", "PRÊMIO", "melhor feijoada",
]


def language_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt"


def slug_key(path: Path) -> str:
    return path.stem.lower()


def clean_url_for(path: Path) -> str:
    lang = language_for(path)
    key = slug_key(path)
    if key in LOCALIZED_SLUGS:
        slug = LOCALIZED_SLUGS[key][lang]
    else:
        rel = path.relative_to(ROOT).with_suffix("").as_posix()
        slug = rel
    if slug == "":
        return BASE_URL + "/"
    if slug.endswith("/"):
        return f"{BASE_URL}/{slug}"
    return f"{BASE_URL}/{slug}"


def set_canonical_and_og(text: str, path: Path) -> str:
    canonical = clean_url_for(path)
    # remove every canonical link, then add one right after <head>
    text = re.sub(r"\n?<link\s+[^>]*rel=[\"']canonical[\"'][^>]*>\s*", "\n", text, flags=re.I)
    text = re.sub(r"(<head>\s*)", rf"\1\n<link rel=\"canonical\" href=\"{canonical}\">\n", text, count=1, flags=re.I)
    # normalize OG URL
    text = re.sub(r'<meta\s+content="[^"]*"\s+property="og:url"\s*/?>', f'<meta content="{canonical}" property="og:url"/>', text, flags=re.I)
    # mainEntityOfPage and @id for Article pages should match language URL
    text = re.sub(r'"mainEntityOfPage"\s*:\s*"https://www\.embaixadacarioca\.com/[^"]*"', f'"mainEntityOfPage": "{canonical}"', text)
    return text


def fix_hreflang(text: str, path: Path) -> str:
    key = slug_key(path)
    if key not in LOCALIZED_SLUGS:
        return text
    urls = {
        "pt-BR": BASE_URL + "/" + LOCALIZED_SLUGS[key]["pt"].strip("/"),
        "en": BASE_URL + "/" + LOCALIZED_SLUGS[key]["en"].strip("/"),
        "es": BASE_URL + "/" + LOCALIZED_SLUGS[key]["es"].strip("/"),
        "x-default": BASE_URL + "/" + LOCALIZED_SLUGS[key]["pt"].strip("/"),
    }
    for k, v in list(urls.items()):
        if v == BASE_URL + "/":
            urls[k] = v
    block = "\n".join([f'<link href="{u}" hreflang="{h}" rel="alternate"/>' for h, u in urls.items()])
    # Replace an existing group of hreflang links if present.
    text = re.sub(r'(?:\n?<link\s+href="https://www\.embaixadacarioca\.com[^"]*"\s+hreflang="(?:pt-BR|en|es|x-default)"\s+rel="alternate"/?\s*>\s*)+', "\n" + block + "\n", text)
    return text


def apply_replacements(text: str, replacements: dict[str, str]) -> tuple[str, int]:
    count = 0
    for old, new in replacements.items():
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            count += c
    return text, count


def fix_schema_and_hours(text: str, lang: str, path: Path) -> str:
    # Global hours and ratings
    text = text.replace('"reviewCount":"7752"', f'"reviewCount":"{REVIEW_COUNT}"')
    text = text.replace('"reviewCount": "7752"', f'"reviewCount": "{REVIEW_COUNT}"')
    text = text.replace('"opens": "12:00"', '"opens": "11:30"')
    text = text.replace('"opens":"12:00"', '"opens":"11:30"')
    # Remove unsafe hard capacity field when present.
    text = re.sub(r'\n\s*"_maximumAttendeeCapacity_removed"\s*:\s*300,?', '', text)
    text = re.sub(r'\n\s*"maximumAttendeeCapacity"\s*:\s*300,?', '', text)
    # Correct inLanguage for language-specific pages.
    if lang == "en":
        text = re.sub(r'"inLanguage"\s*:\s*"pt-BR"', '"inLanguage": "en"', text)
    elif lang == "es":
        text = re.sub(r'"inLanguage"\s*:\s*"pt-BR"', '"inLanguage": "es"', text)
    return text


def noindex_legacy(text: str, path: Path) -> str:
    name = path.name
    if any(p.search(name) for p in LEGACY_PATTERNS):
        if 'name="robots"' in text:
            text = re.sub(r'<meta\s+content="[^"]*"\s+name="robots"\s*/?>', '<meta content="noindex, nofollow" name="robots"/>', text, flags=re.I)
        else:
            text = re.sub(r"(<head>\s*)", r'\1\n<meta content="noindex, nofollow" name="robots"/>\n', text, count=1, flags=re.I)
    return text


def rename_localized_sunset_files() -> None:
    renames = [
        (ROOT / "en" / "entardecer.html", ROOT / "en" / "sunset.html"),
        (ROOT / "es" / "entardecer.html", ROOT / "es" / "atardecer.html"),
    ]
    for src, dst in renames:
        if src.exists() and not dst.exists():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            src.unlink()
            REPORT_LINES.append(f"RENAMED: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def process_file(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    lang = language_for(path)
    original = path.read_text(encoding="utf-8")
    text = original

    text, c_global = apply_replacements(text, GLOBAL_REPLACEMENTS)
    c_lang = 0
    if lang == "en":
        text, c_lang = apply_replacements(text, EN_REPLACEMENTS)
    elif lang == "es":
        text, c_lang = apply_replacements(text, ES_REPLACEMENTS)

    text, c_meta = apply_replacements(text, META_REPLACEMENTS_BY_FILE.get(rel, {}))
    text = fix_schema_and_hours(text, lang, path)
    text = set_canonical_and_og(text, path)
    text = fix_hreflang(text, path)
    text = noindex_legacy(text, path)

    # Specific high-value copy fixes.
    text = text.replace(
        "Acesso via bondinho (teleférico) ou a pé pela Praia Vermelha",
        "Acesso pelo bondinho, com ingresso regular do Parque Bondinho Pão de Açúcar, ou pela trilha da Praia Vermelha, quando aberta, sem necessidade de ingresso do bondinho",
    )
    text = text.replace(
        "Access via cable car (Bondinho) or on foot via Praia Vermelha trail",
        "Access by cable car, with a regular Bondinho Pão de Açúcar Park ticket, or by the Praia Vermelha trail, when open, without a cable car ticket",
    )
    text = text.replace(
        "The Urca Hill restaurant — Embaixada Carioca — is accessible depending on how you arrive",
        "Access depends on how you arrive. If you take the cable car, a regular Bondinho Pão de Açúcar Park ticket is required. If you hike up via the Praia Vermelha trail, when open, no cable car ticket is needed. A restaurant reservation guarantees your table, but does not include the park ticket",
    )
    text = text.replace(
        "El restaurante del Morro da Urca — Embaixada Carioca — el acceso depende de cómo llegue",
        "El acceso depende de cómo llegue. Si sube en teleférico, debe comprar la entrada regular del Parque Bondinho Pão de Açúcar. Si sube por el sendero de Praia Vermelha, cuando esté abierto, no necesita entrada del teleférico. La reserva en el restaurante garantiza la mesa, pero no incluye la entrada al Parque",
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        REPORT_LINES.append(f"UPDATED: {rel} | replacements: global={c_global}, lang={c_lang}, meta={c_meta}")


def audit_remaining() -> list[str]:
    issues: list[str] = []
    for path in sorted([p for p in ROOT.rglob("*.html") if ".git" not in p.parts]):
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        lang = language_for(path)
        for term in PROHIBITED:
            if term in text:
                issues.append(f"{rel}: prohibited term still present: {term}")
        if lang == "en":
            for term in EN_FORBIDDEN:
                if term in text:
                    issues.append(f"{rel}: EN residual term: {term}")
        if lang == "es":
            for term in ES_FORBIDDEN:
                if term in text:
                    issues.append(f"{rel}: ES residual term: {term}")
        # Multiple canonicals are a technical error.
        if len(re.findall(r'rel=[\"']canonical[\"']', text, flags=re.I)) > 1:
            issues.append(f"{rel}: multiple canonical tags")
        # Old lunch hour in schema/text.
        if '"opens": "12:00"' in text or '12 PM – 5 PM' in text or '12h–17' in text:
            issues.append(f"{rel}: old lunch hour pattern remains")
    return issues


def main() -> int:
    rename_localized_sunset_files()
    for path in sorted([p for p in ROOT.rglob("*.html") if ".git" not in p.parts]):
        process_file(path)

    issues = audit_remaining()
    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report = report_dir / "aaa_6_estrelas_fixes_report.md"
    report.write_text(
        "# Relatório de Correções AAA / 6 Estrelas\n\n"
        "## Arquivos alterados\n"
        + ("\n".join(f"- {line}" for line in REPORT_LINES) if REPORT_LINES else "- Nenhuma alteração necessária")
        + "\n\n## Pendências detectadas após script\n"
        + ("\n".join(f"- {issue}" for issue in issues) if issues else "- Nenhuma pendência crítica detectada pelos padrões automatizados")
        + "\n",
        encoding="utf-8",
    )
    print(report.read_text(encoding="utf-8"))
    # Do not fail the workflow for editorial residues; the report is the source of truth.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
