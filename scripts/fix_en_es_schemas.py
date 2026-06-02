#!/usr/bin/env python3
"""
Fix GEO signals and missing schemas across high-value EN/ES landing pages.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCRIPT_RE = re.compile(
    r'(<script\s[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.I | re.S
)

CONTAINED_IN = {
    "@type": "TouristAttraction",
    "name": "Parque Bondinho Pão de Açúcar",
    "url": "https://bondinho.com.br/",
    "sameAs": "https://en.wikipedia.org/wiki/Sugarloaf_Mountain",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Praça General Tibúrcio, 68",
        "addressLocality": "Rio de Janeiro",
        "addressRegion": "RJ",
        "addressCountry": "BR"
    }
}

NEARBY_ATTRACTIONS = [
    {"@type": "TouristAttraction", "name": "Sugarloaf Mountain",
     "sameAs": "https://en.wikipedia.org/wiki/Sugarloaf_Mountain"},
    {"@type": "TouristAttraction", "name": "Urca Hill",
     "sameAs": "https://en.wikipedia.org/wiki/Urca_Hill"}
]

NEARBY_ATTRACTIONS_ES = [
    {"@type": "TouristAttraction", "name": "Pan de Azúcar",
     "sameAs": "https://en.wikipedia.org/wiki/Sugarloaf_Mountain"},
    {"@type": "TouristAttraction", "name": "Morro da Urca",
     "sameAs": "https://en.wikipedia.org/wiki/Urca_Hill"}
]


def add_geo_to_obj(obj, nearby):
    changed = False
    if isinstance(obj, dict):
        t = obj.get("@type", "")
        types = [t] if isinstance(t, str) else (t if isinstance(t, list) else [])
        if any(x in types for x in ("Restaurant", "FoodEstablishment", "LocalBusiness")):
            if "containedInPlace" not in obj:
                obj["containedInPlace"] = CONTAINED_IN
                changed = True
            if "nearbyAttraction" not in obj:
                obj["nearbyAttraction"] = nearby
                changed = True
        if "@graph" in obj:
            for item in obj["@graph"]:
                if add_geo_to_obj(item, nearby):
                    changed = True
    return changed


def update_geo(html, nearby):
    changed = False
    def replace(m):
        nonlocal changed
        try:
            obj = json.loads(m.group(2).strip())
        except Exception:
            return m.group(0)
        if add_geo_to_obj(obj, nearby):
            changed = True
            return m.group(1) + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + m.group(3)
        return m.group(0)
    new_html = SCRIPT_RE.sub(replace, html)
    return new_html, changed


def get_types(html):
    found = set()
    for m in SCRIPT_RE.finditer(html):
        try:
            obj = json.loads(m.group(2).strip())
        except Exception:
            continue
        def walk(o):
            if isinstance(o, dict):
                t = o.get("@type", "")
                ts = [t] if isinstance(t, str) else (t if isinstance(t, list) else [])
                found.update(ts)
                for v in o.values(): walk(v)
            elif isinstance(o, list):
                for v in o: walk(v)
        walk(obj)
    return found


def inject(html, schema):
    block = '\n<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False, separators=(",", ":")) + "</script>"
    if "</head>" in html:
        return html.replace("</head>", block + "\n</head>", 1), True
    return html, False


def fix_page(rel, webpage_schema, faq_schema=None, nearby=None):
    if nearby is None:
        nearby = NEARBY_ATTRACTIONS
    path = ROOT / rel
    if not path.exists():
        print("  MISSING " + rel)
        return
    html = path.read_text(encoding="utf-8")
    original = html
    changes = []

    html, ch = update_geo(html, nearby)
    if ch:
        changes.append("GEO signals")

    types = get_types(html)

    if "WebPage" not in types and webpage_schema:
        html, ok = inject(html, webpage_schema)
        if ok:
            changes.append("WebPage")

    if faq_schema and "FAQPage" not in get_types(html):
        html, ok = inject(html, faq_schema)
        if ok:
            changes.append("FAQPage")

    if html != original:
        path.write_text(html, encoding="utf-8")
        print("  " + rel + ": " + ", ".join(changes))
    else:
        print("  " + rel + ": no changes")


def main():
    print("Fixing EN/ES high-value pages...")

    # ── EN pages ──────────────────────────────────────────

    fix_page("en/sugarloaf-cable-car-restaurant.html",
        webpage_schema={
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Sugarloaf Cable Car Restaurant — Embaixada Carioca",
            "description": "The best restaurant at the Sugarloaf Cable Car Park: Embaixada Carioca at Morro da Urca, with panoramic views of Sugarloaf Mountain.",
            "url": "https://www.embaixadacarioca.com/en/sugarloaf-cable-car-restaurant.html",
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".hero-sub", ".faq-answer"]},
            "inLanguage": "en"
        }
    )

    fix_page("en/restaurants-near-sugarloaf-mountain.html",
        webpage_schema={
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Restaurants Near Sugarloaf Mountain — Embaixada Carioca",
            "description": "Looking for restaurants near Sugarloaf Mountain? Embaixada Carioca is the only restaurant inside Parque Bondinho, at Morro da Urca with views of Sugarloaf.",
            "url": "https://www.embaixadacarioca.com/en/restaurants-near-sugarloaf-mountain.html",
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".hero-sub", ".faq-answer"]},
            "inLanguage": "en"
        }
    )

    fix_page("en/where-to-eat-near-sugarloaf.html",
        webpage_schema={
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Where to Eat Near Sugarloaf Mountain — Embaixada Carioca",
            "description": "Where to eat near Sugarloaf Mountain in Rio de Janeiro: Embaixada Carioca at Morro da Urca offers breakfast, lunch and sundowners with Sugarloaf views.",
            "url": "https://www.embaixadacarioca.com/en/where-to-eat-near-sugarloaf.html",
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".hero-sub", ".faq-answer"]},
            "inLanguage": "en"
        }
    )

    fix_page("en/restaurant-at-urca-hill.html",
        webpage_schema={
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Restaurant at Urca Hill — Embaixada Carioca",
            "description": "Embaixada Carioca is the restaurant at Urca Hill (Morro da Urca), inside Sugarloaf Cable Car Park, with Brazilian cuisine and panoramic views.",
            "url": "https://www.embaixadacarioca.com/en/restaurant-at-urca-hill.html",
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".hero-sub", ".faq-answer"]},
            "inLanguage": "en"
        }
    )

    fix_page("en/morro-da-urca.html",
        webpage_schema={
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Morro da Urca Restaurant — Embaixada Carioca",
            "description": "Embaixada Carioca at Morro da Urca: the only restaurant on Urca Hill, inside the Sugarloaf Cable Car Park with 360° views of Rio de Janeiro.",
            "url": "https://www.embaixadacarioca.com/en/morro-da-urca.html",
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".hero-sub", ".faq-answer"]},
            "inLanguage": "en"
        }
    )

    fix_page("en/cafe-da-manha-pao-de-acucar.html",
        webpage_schema=None,
        faq_schema={
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "@id": "https://www.embaixadacarioca.com/en/cafe-da-manha-pao-de-acucar.html#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "Is there breakfast at Sugarloaf Mountain?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Yes! Embaixada Carioca serves breakfast at Morro da Urca, the first stop of the Sugarloaf cable car, with stunning views of Sugarloaf Mountain. Breakfast runs daily from 8:30 to 11:30."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Where to have breakfast near Sugarloaf?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Embaixada Carioca, inside Parque Bondinho Pão de Açúcar at Morro da Urca (227m altitude), is the best place for breakfast near Sugarloaf Mountain in Rio de Janeiro."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Do I need a cable car ticket to have breakfast at Sugarloaf?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Yes, entry to Parque Bondinho Pão de Açúcar is required. You can buy tickets at the park entrance (Praça General Tibúrcio, 68, Urca). The Embaixada Carioca restaurant is at the first stop (Morro da Urca)."
                    }
                }
            ]
        }
    )

    fix_page("en/almoco-morro-da-urca.html",
        webpage_schema=None,
        faq_schema={
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "@id": "https://www.embaixadacarioca.com/en/almoco-morro-da-urca.html#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "Where can I have lunch at Morro da Urca?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Embaixada Carioca is the restaurant at Morro da Urca, inside Parque Bondinho Pão de Açúcar. Lunch is served daily from 11:30 to 17:00 with views of Sugarloaf Mountain."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Do I need a reservation for lunch at Morro da Urca?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "We recommend booking in advance, especially on weekends. Reserve online via our website, WhatsApp (+55 21 96683-7556), or through Tagme."
                    }
                }
            ]
        }
    )

    # ── ES pages ──────────────────────────────────────────

    fix_page("es/restaurante-morro-da-urca.html",
        webpage_schema={
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Restaurante Morro da Urca — Embaixada Carioca",
            "description": "Embaixada Carioca es el restaurante en el Morro da Urca, dentro del Parque Bondinho Pan de Azúcar, con desayuno, almuerzo y vistas panorámicas.",
            "url": "https://www.embaixadacarioca.com/es/restaurante-morro-da-urca.html",
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".hero-sub", ".faq-answer"]},
            "inLanguage": "es"
        },
        nearby=NEARBY_ATTRACTIONS_ES
    )

    fix_page("es/donde-comer-cerca-del-pan-de-azucar.html",
        webpage_schema={
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Dónde Comer cerca del Pan de Azúcar — Embaixada Carioca",
            "description": "¿Dónde comer cerca del Pan de Azúcar en Río de Janeiro? La Embaixada Carioca en el Morro da Urca es el único restaurante dentro del Parque Bondinho.",
            "url": "https://www.embaixadacarioca.com/es/donde-comer-cerca-del-pan-de-azucar.html",
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".hero-sub", ".faq-answer"]},
            "inLanguage": "es"
        },
        nearby=NEARBY_ATTRACTIONS_ES
    )

    fix_page("es/restaurantes-cerca-del-pan-de-azucar.html",
        webpage_schema={
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Restaurantes cerca del Pan de Azúcar — Embaixada Carioca",
            "description": "La Embaixada Carioca es el mejor restaurante cerca del Pan de Azúcar: está dentro del Parque Bondinho en el Morro da Urca con vistas panorámicas.",
            "url": "https://www.embaixadacarioca.com/es/restaurantes-cerca-del-pan-de-azucar.html",
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".hero-sub", ".faq-answer"]},
            "inLanguage": "es"
        },
        nearby=NEARBY_ATTRACTIONS_ES
    )

    fix_page("es/almoco-morro-da-urca.html",
        webpage_schema=None,
        faq_schema={
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "@id": "https://www.embaixadacarioca.com/es/almoco-morro-da-urca.html#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "¿Dónde almorzar en el Morro da Urca?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Embaixada Carioca es el restaurante en el Morro da Urca, dentro del Parque Bondinho Pão de Açúcar, con almuerzo servido todos los días de 11:30 a 17:00 con vista al Pan de Azúcar."
                    }
                },
                {
                    "@type": "Question",
                    "name": "¿Necesito reservar para almorzar en el Morro da Urca?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Recomendamos reservar con anticipación, especialmente los fines de semana. Reserve por nuestro sitio web, WhatsApp (+55 21 96683-7556) o por Tagme."
                    }
                }
            ]
        },
        nearby=NEARBY_ATTRACTIONS_ES
    )

    fix_page("es/cafe-da-manha-pao-de-acucar.html",
        webpage_schema=None,
        faq_schema={
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "@id": "https://www.embaixadacarioca.com/es/cafe-da-manha-pao-de-acucar.html#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "¿Hay desayuno en el Pan de Azúcar?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Sí. La Embaixada Carioca sirve desayuno en el Morro da Urca, la primera parada del teleférico del Pan de Azúcar, con vistas panorámicas. El desayuno se sirve todos los días de 8:30 a 11:30."
                    }
                },
                {
                    "@type": "Question",
                    "name": "¿Necesito entrada al Parque Bondinho para desayunar?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Sí, se requiere entrada al Parque Bondinho Pão de Açúcar. Puedes comprar las entradas en la taquilla del parque (Praça General Tibúrcio, 68, Urca). El restaurante está en la primera parada: Morro da Urca."
                    }
                }
            ]
        },
        nearby=NEARBY_ATTRACTIONS_ES
    )

    # Also fix remaining EN/ES pages missing GEO
    for rel in [
        "en/almoco.html", "es/almoco.html",
        "en/cafe-da-manha.html", "es/cafe-da-manha.html",
        "cardapio.html", "en/cardapio.html", "es/cardapio.html",
    ]:
        nearby = NEARBY_ATTRACTIONS_ES if rel.startswith("es/") else NEARBY_ATTRACTIONS
        fix_page(rel, webpage_schema=None, faq_schema=None, nearby=nearby)

    print("Done.")


if __name__ == "__main__":
    main()
