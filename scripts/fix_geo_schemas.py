#!/usr/bin/env python3
"""
Fix GEO signals and missing schema types across key pages.
- Add containedInPlace + nearbyAttraction to Restaurant schemas
- Add missing WebPage, BreadcrumbList, WebSite, FAQPage schemas
- Add SpeakableSpecification where missing
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCRIPT_RE = re.compile(
    r'(<script\s[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.I | re.S
)

# GEO entities for containedInPlace and nearbyAttraction
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
    {
        "@type": "TouristAttraction",
        "name": "Pão de Açúcar",
        "sameAs": "https://en.wikipedia.org/wiki/Sugarloaf_Mountain"
    },
    {
        "@type": "TouristAttraction",
        "name": "Morro da Urca",
        "sameAs": "https://en.wikipedia.org/wiki/Urca_Hill"
    }
]


def add_geo_to_restaurant_in_obj(obj):
    """Recursively find Restaurant nodes and add containedInPlace/nearbyAttraction."""
    changed = False
    if isinstance(obj, dict):
        t = obj.get("@type", "")
        types = [t] if isinstance(t, str) else (t if isinstance(t, list) else [])
        if any(x in types for x in ("Restaurant", "FoodEstablishment", "LocalBusiness")):
            if "containedInPlace" not in obj:
                obj["containedInPlace"] = CONTAINED_IN
                changed = True
            if "nearbyAttraction" not in obj:
                obj["nearbyAttraction"] = NEARBY_ATTRACTIONS
                changed = True
        if "@graph" in obj:
            for item in obj["@graph"]:
                if add_geo_to_restaurant_in_obj(item):
                    changed = True
    return changed


def update_restaurant_blocks(html):
    """Update all Restaurant JSON-LD blocks to add GEO signals."""
    changed = False

    def replace_match(m):
        nonlocal changed
        open_tag, content, close_tag = m.group(1), m.group(2), m.group(3)
        try:
            obj = json.loads(content.strip())
        except Exception:
            return m.group(0)

        if add_geo_to_restaurant_in_obj(obj):
            changed = True
            new_content = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
            return f"{open_tag}{new_content}{close_tag}"
        return m.group(0)

    new_html = SCRIPT_RE.sub(replace_match, html)
    return new_html, changed


def inject_schema_before_head_close(html, schema_obj):
    """Inject a JSON-LD block just before </head>."""
    block = (
        '\n<script type="application/ld+json">'
        + json.dumps(schema_obj, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
    )
    if "</head>" in html:
        return html.replace("</head>", block + "\n</head>", 1), True
    return html, False


def has_type(html, *types):
    """Check if any of the given schema types exist in the page."""
    found = set()
    for s in SCRIPT_RE.findall(html):
        content = s[1] if isinstance(s, tuple) else s
        try:
            obj = json.loads(content.strip()) if isinstance(s, tuple) else json.loads(s.strip())
        except Exception:
            continue
        def walk(o):
            if isinstance(o, dict):
                t = o.get("@type", "")
                ts = [t] if isinstance(t, str) else (t if isinstance(t, list) else [])
                found.update(ts)
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(obj)
    return {t for t in types if t in found}


# Script RE returns full match as group(0); need to search by content
def get_types_in_html(html):
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


# ──────────────────────────────────────────────
# Page-specific fix functions
# ──────────────────────────────────────────────

def fix_restaurante_morro_da_urca():
    path = ROOT / "restaurante-morro-da-urca.html"
    html = path.read_text(encoding="utf-8")
    original = html
    changes = []

    html, ch = update_restaurant_blocks(html)
    if ch:
        changes.append("added containedInPlace + nearbyAttraction")

    types = get_types_in_html(html)

    if "WebPage" not in types:
        schema = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Restaurante Morro da Urca — Embaixada Carioca",
            "description": "Restaurante no Morro da Urca com vista panorâmica para o Pão de Açúcar. Café da manhã, almoço e eventos no Parque Bondinho.",
            "url": "https://www.embaixadacarioca.com/restaurante-morro-da-urca.html",
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": ["h1", ".hero-sub", ".intro-text", ".faq-answer"]
            },
            "inLanguage": "pt-BR"
        }
        html, ok = inject_schema_before_head_close(html, schema)
        if ok:
            changes.append("added WebPage + SpeakableSpecification")

    if html != original:
        path.write_text(html, encoding="utf-8")
        print(f"  restaurante-morro-da-urca.html: {', '.join(changes)}")
    else:
        print("  restaurante-morro-da-urca.html: no changes needed")


def fix_onde_comer_no_pao_de_acucar():
    path = ROOT / "onde-comer-no-pao-de-acucar.html"
    html = path.read_text(encoding="utf-8")
    original = html
    changes = []

    html, ch = update_restaurant_blocks(html)
    if ch:
        changes.append("added containedInPlace + nearbyAttraction")

    types = get_types_in_html(html)

    if "WebPage" not in types:
        schema = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Onde Comer no Pão de Açúcar — Embaixada Carioca",
            "description": "Descubra onde comer no Pão de Açúcar com o melhor restaurante do Parque Bondinho: a Embaixada Carioca no Morro da Urca.",
            "url": "https://www.embaixadacarioca.com/onde-comer-no-pao-de-acucar.html",
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": ["h1", ".hero-sub", ".intro-text", ".faq-answer"]
            },
            "inLanguage": "pt-BR"
        }
        html, ok = inject_schema_before_head_close(html, schema)
        if ok:
            changes.append("added WebPage + SpeakableSpecification")

    if html != original:
        path.write_text(html, encoding="utf-8")
        print(f"  onde-comer-no-pao-de-acucar.html: {', '.join(changes)}")
    else:
        print("  onde-comer-no-pao-de-acucar.html: no changes needed")


def fix_cafe_da_manha_com_vista():
    path = ROOT / "cafe-da-manha-com-vista-rio-de-janeiro.html"
    html = path.read_text(encoding="utf-8")
    original = html
    changes = []

    html, ch = update_restaurant_blocks(html)
    if ch:
        changes.append("added containedInPlace + nearbyAttraction")

    types = get_types_in_html(html)

    if "WebSite" not in types:
        schema = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "@id": "https://www.embaixadacarioca.com/#website",
            "name": "Embaixada Carioca",
            "url": "https://www.embaixadacarioca.com/",
            "inLanguage": "pt-BR",
            "publisher": {
                "@type": "Organization",
                "name": "Embaixada Carioca",
                "url": "https://www.embaixadacarioca.com/"
            }
        }
        html, ok = inject_schema_before_head_close(html, schema)
        if ok:
            changes.append("added WebSite")

    types = get_types_in_html(html)

    if "BreadcrumbList" not in types:
        schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Início",
                 "item": "https://www.embaixadacarioca.com/"},
                {"@type": "ListItem", "position": 2,
                 "name": "Café da Manhã com Vista no Rio de Janeiro",
                 "item": "https://www.embaixadacarioca.com/cafe-da-manha-com-vista-rio-de-janeiro.html"}
            ]
        }
        html, ok = inject_schema_before_head_close(html, schema)
        if ok:
            changes.append("added BreadcrumbList")

    if html != original:
        path.write_text(html, encoding="utf-8")
        print(f"  cafe-da-manha-com-vista-rio-de-janeiro.html: {', '.join(changes)}")
    else:
        print("  cafe-da-manha-com-vista-rio-de-janeiro.html: no changes needed")


def fix_almoco_morro_da_urca():
    path = ROOT / "almoco-morro-da-urca.html"
    html = path.read_text(encoding="utf-8")
    original = html
    changes = []

    html, ch = update_restaurant_blocks(html)
    if ch:
        changes.append("added containedInPlace + nearbyAttraction")

    types = get_types_in_html(html)

    if "FAQPage" not in types:
        schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "@id": "https://www.embaixadacarioca.com/almoco-morro-da-urca.html#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "Como chegar ao Restaurante Morro da Urca para almoçar?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Para almoçar no Morro da Urca, você acessa o Parque Bondinho Pão de Açúcar (Praça General Tibúrcio, 68) e sobe de bonde até o Morro da Urca, onde fica a Embaixada Carioca."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Qual o horário do almoço no Morro da Urca?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "O almoço é servido todos os dias das 11h30 às 17h no restaurante Embaixada Carioca, no Morro da Urca."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Precisa de reserva para almoçar no Morro da Urca?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Recomendamos reservar com antecedência, especialmente nos fins de semana. Reserve pelo site, WhatsApp ou Tagme."
                    }
                }
            ]
        }
        html, ok = inject_schema_before_head_close(html, schema)
        if ok:
            changes.append("added FAQPage")

    if html != original:
        path.write_text(html, encoding="utf-8")
        print(f"  almoco-morro-da-urca.html: {', '.join(changes)}")
    else:
        print("  almoco-morro-da-urca.html: no changes needed")


def fix_almoco():
    path = ROOT / "almoco.html"
    html = path.read_text(encoding="utf-8")
    original = html
    changes = []

    html, ch = update_restaurant_blocks(html)
    if ch:
        changes.append("added containedInPlace + nearbyAttraction")

    if html != original:
        path.write_text(html, encoding="utf-8")
        print(f"  almoco.html: {', '.join(changes)}")
    else:
        print("  almoco.html: no changes needed")


def fix_cafe_da_manha():
    path = ROOT / "cafe-da-manha.html"
    html = path.read_text(encoding="utf-8")
    original = html
    changes = []

    html, ch = update_restaurant_blocks(html)
    if ch:
        changes.append("added containedInPlace + nearbyAttraction")

    if html != original:
        path.write_text(html, encoding="utf-8")
        print(f"  cafe-da-manha.html: {', '.join(changes)}")
    else:
        print("  cafe-da-manha.html: no changes needed")


def fix_index():
    path = ROOT / "index.html"
    html = path.read_text(encoding="utf-8")
    original = html
    changes = []

    # nearbyAttraction missing (containedInPlace already present)
    html, ch = update_restaurant_blocks(html)
    if ch:
        changes.append("added nearbyAttraction to Restaurant")

    types = get_types_in_html(html)

    if "WebPage" not in types:
        schema = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Embaixada Carioca — Restaurante no Morro da Urca, Pão de Açúcar",
            "description": "Restaurante premiado no Morro da Urca com vista para o Pão de Açúcar. Café da manhã, almoço e eventos no Parque Bondinho.",
            "url": "https://www.embaixadacarioca.com/",
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": ["h1", ".hero-sub", ".section-intro", ".faq-answer"]
            },
            "inLanguage": "pt-BR"
        }
        html, ok = inject_schema_before_head_close(html, schema)
        if ok:
            changes.append("added WebPage + SpeakableSpecification")

    if html != original:
        path.write_text(html, encoding="utf-8")
        print(f"  index.html: {', '.join(changes)}")
    else:
        print("  index.html: no changes needed")


def fix_en_index():
    path = ROOT / "en" / "index.html"
    html = path.read_text(encoding="utf-8")
    original = html
    changes = []

    html, ch = update_restaurant_blocks(html)
    if ch:
        changes.append("added containedInPlace + nearbyAttraction")

    types = get_types_in_html(html)

    if "WebPage" not in types:
        schema = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Embaixada Carioca — Restaurant at Sugarloaf, Morro da Urca",
            "description": "Award-winning restaurant at Morro da Urca with panoramic views of Sugarloaf Mountain. Breakfast, lunch and events at Parque Bondinho.",
            "url": "https://www.embaixadacarioca.com/en/",
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": ["h1", ".hero-sub", ".section-intro", ".faq-answer"]
            },
            "inLanguage": "en"
        }
        html, ok = inject_schema_before_head_close(html, schema)
        if ok:
            changes.append("added WebPage + SpeakableSpecification")

    if html != original:
        path.write_text(html, encoding="utf-8")
        print(f"  en/index.html: {', '.join(changes)}")
    else:
        print("  en/index.html: no changes needed")


def fix_es_index():
    path = ROOT / "es" / "index.html"
    html = path.read_text(encoding="utf-8")
    original = html
    changes = []

    html, ch = update_restaurant_blocks(html)
    if ch:
        changes.append("added containedInPlace + nearbyAttraction")

    types = get_types_in_html(html)

    if "WebPage" not in types:
        schema = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Embaixada Carioca — Restaurante en el Morro da Urca, Pão de Açúcar",
            "description": "Restaurante premiado en el Morro da Urca con vista panorámica al Pan de Azúcar. Desayuno, almuerzo y eventos en el Parque Bondinho.",
            "url": "https://www.embaixadacarioca.com/es/",
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": ["h1", ".hero-sub", ".section-intro", ".faq-answer"]
            },
            "inLanguage": "es"
        }
        html, ok = inject_schema_before_head_close(html, schema)
        if ok:
            changes.append("added WebPage + SpeakableSpecification")

    if html != original:
        path.write_text(html, encoding="utf-8")
        print(f"  es/index.html: {', '.join(changes)}")
    else:
        print("  es/index.html: no changes needed")


def fix_internal_links_almoco():
    """Add link from almoco.html to almoco-morro-da-urca.html."""
    path = ROOT / "almoco.html"
    html = path.read_text(encoding="utf-8")

    if "almoco-morro-da-urca" in html:
        print("  almoco.html internal link: already present")
        return

    # Find a suitable place to add the link — look for the related links section
    # or add near the end of the main content, before scripts
    link_html = (
        '\n<div class="related-link" style="margin:1.5rem 0;padding:1rem;'
        'background:#f0f7ff;border-radius:8px;border-left:4px solid #1d4ed8">'
        '<p style="margin:0">Prefere uma experiência completa no Morro da Urca? '
        '<a href="/almoco-morro-da-urca.html" style="color:#1d4ed8;font-weight:600">'
        'Veja o almoço especial no Morro da Urca &rarr;</a></p></div>\n'
    )

    # Insert before the first </section> or </main> or before footer
    for marker in ["</main>", "</article>", '<footer', '<section id="faq']:
        if marker in html:
            html = html.replace(marker, link_html + marker, 1)
            path.write_text(html, encoding="utf-8")
            print(f"  almoco.html: added internal link to almoco-morro-da-urca.html (before {marker})")
            return

    print("  almoco.html: could not find suitable insertion point for internal link")


def main():
    print("Fixing GEO signals and missing schemas...")
    fix_restaurante_morro_da_urca()
    fix_onde_comer_no_pao_de_acucar()
    fix_cafe_da_manha_com_vista()
    fix_almoco_morro_da_urca()
    fix_almoco()
    fix_cafe_da_manha()
    fix_index()
    fix_en_index()
    fix_es_index()
    fix_internal_links_almoco()
    print("Done.")


if __name__ == "__main__":
    main()
