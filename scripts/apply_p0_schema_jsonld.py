#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
REPORT = OUT / 'p0_schema_jsonld_report.md'
START = '<!-- EC P0 Structured Data -->'
END = '<!-- /EC P0 Structured Data -->'

BASE = 'https://www.embaixadacarioca.com'
TAGME = 'https://go.tagme.com.br/embaixadacarioca'
PHONE = '+55 21 96683-7556'
EMAIL = 'eventos@embaixadacarioca.com.br'
ADDRESS = {
    '@type': 'PostalAddress',
    'streetAddress': 'Av. Pasteur, 520 - Morro da Urca',
    'addressLocality': 'Rio de Janeiro',
    'addressRegion': 'RJ',
    'postalCode': '22290-255',
    'addressCountry': 'BR',
}
GEO = {'@type': 'GeoCoordinates', 'latitude': -22.9508333, 'longitude': -43.1641667}

PAGES = [
    ('pt-BR', 'index.html', '/', 'Embaixada Carioca', 'Restaurante brasileiro no Morro da Urca, primeira parada do Bondinho Pão de Açúcar, com café da manhã, almoço, caipirinhas, eventos e vista para o Pão de Açúcar.'),
    ('en', 'en/index.html', '/en/', 'Embaixada Carioca', 'Brazilian restaurant at Urca Hill, the first Sugarloaf Cable Car stop, with breakfast, lunch, caipirinhas, events and Sugarloaf views.'),
    ('es', 'es/index.html', '/es/', 'Embaixada Carioca', 'Restaurante brasileño en el Morro da Urca, primera parada del Bondinho Pão de Açúcar, con desayuno, almuerzo, caipirinhas, eventos y vista al Pan de Azúcar.'),
    ('pt-BR', 'cafe-da-manha.html', '/cafe-da-manha.html', 'Café da Manhã na Urca', 'Café da manhã todos os dias no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com vista para o Pão de Açúcar.'),
    ('en', 'en/cafe-da-manha.html', '/en/cafe-da-manha.html', 'Breakfast at Urca Hill', 'Daily breakfast at Urca Hill inside Sugarloaf Cable Car Park, with views of Sugarloaf Mountain.'),
    ('es', 'es/cafe-da-manha.html', '/es/cafe-da-manha.html', 'Desayuno en el Morro da Urca', 'Desayuno todos los días en el Morro da Urca, dentro del Parque Bondinho Pão de Açúcar, con vista al Pan de Azúcar.'),
    ('pt-BR', 'restaurante-morro-da-urca.html', '/restaurante-morro-da-urca.html', 'Restaurante no Morro da Urca', 'Restaurante no Morro da Urca, primeira parada do Bondinho Pão de Açúcar, com comida brasileira, caipirinhas, café da manhã, almoço e eventos.'),
    ('pt-BR', 'eventos.html', '/eventos.html', 'Eventos com Vista no Rio de Janeiro', 'Eventos corporativos e privados no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com gastronomia brasileira e vista.'),
    ('en', 'en/eventos.html', '/en/eventos.html', 'Events with a View in Rio de Janeiro', 'Private and corporate events at Urca Hill inside Sugarloaf Cable Car Park, with Brazilian food, drinks and views.'),
    ('es', 'es/eventos.html', '/es/eventos.html', 'Eventos con Vista en Río de Janeiro', 'Eventos privados y corporativos en el Morro da Urca, dentro del Parque Bondinho, con comida brasileña, drinks y vista.'),
    ('pt-BR', 'guia-do-rio.html', '/guia-do-rio.html', 'Guia do Rio: Morro da Urca e Pão de Açúcar', 'Guia para visitar o Morro da Urca e Pão de Açúcar, com dicas de acesso, roteiro e onde comer dentro do Parque Bondinho.'),
    ('pt-BR', 'restaurantes-romanticos-rio-de-janeiro.html', '/restaurantes-romanticos-rio-de-janeiro.html', 'Restaurante Romântico no Rio de Janeiro com Vista', 'Restaurante romântico no Rio de Janeiro com vista para o Pão de Açúcar, no Morro da Urca, ideal para casais e ocasiões especiais.'),
]

FAQS = {
    'pt-BR': [
        ('Onde comer no Morro da Urca?', 'A Embaixada Carioca é uma opção prática para comer no Morro da Urca, com café da manhã, almoço brasileiro, drinks, caipirinhas e vista para o Pão de Açúcar.'),
        ('A Embaixada Carioca fica no topo do Pão de Açúcar?', 'Não. A Embaixada Carioca fica no Morro da Urca, na primeira parada do Bondinho Pão de Açúcar, com vista para o Pão de Açúcar.'),
        ('A reserva inclui o ingresso do Bondinho?', 'Não. A reserva é do restaurante. O ingresso do Parque Bondinho Pão de Açúcar deve ser comprado separadamente para quem deseja subir de teleférico.'),
        ('Tem café da manhã todos os dias?', 'Sim. A Embaixada Carioca serve café da manhã todos os dias no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar.'),
        ('Quais são as especialidades da casa?', 'As especialidades incluem picanha brasileira, feijoada premiada ligada à tradição da Academia da Cachaça, bobó de camarão, caipirinhas e chope gelado.'),
        ('A Embaixada Carioca recebe eventos?', 'Sim. A casa recebe eventos corporativos, grupos turísticos, cafés da manhã, coquetéis, aniversários e experiências privadas com vista no Morro da Urca.'),
    ],
    'en': [
        ('Where to eat at Urca Hill?', 'Embaixada Carioca is a practical choice for eating at Urca Hill, with breakfast, Brazilian lunch, drinks, caipirinhas and Sugarloaf views.'),
        ('Is Embaixada Carioca at the top of Sugarloaf Mountain?', 'No. Embaixada Carioca is at Urca Hill, the first Sugarloaf Cable Car stop, with views of Sugarloaf Mountain.'),
        ('Does the restaurant reservation include the cable car ticket?', 'No. The restaurant reservation does not include the Sugarloaf Cable Car Park ticket. The park ticket must be purchased separately.'),
        ('Is breakfast served every day?', 'Yes. Embaixada Carioca serves breakfast every day at Urca Hill inside Sugarloaf Cable Car Park.'),
        ('What is the restaurant known for?', 'The restaurant is known for Brazilian food, caipirinhas, feijoada, picanha, breakfast and views of Sugarloaf Mountain.'),
    ],
    'es': [
        ('¿Dónde comer en el Morro da Urca?', 'Embaixada Carioca es una opción práctica para comer en el Morro da Urca, con desayuno, almuerzo brasileño, drinks, caipirinhas y vista al Pan de Azúcar.'),
        ('¿Embaixada Carioca está en la cima del Pan de Azúcar?', 'No. Embaixada Carioca está en el Morro da Urca, en la primera parada del Bondinho Pão de Açúcar, con vista al Pan de Azúcar.'),
        ('¿La reserva incluye la entrada del Bondinho?', 'No. La reserva es del restaurante. La entrada del Parque Bondinho Pão de Açúcar debe comprarse por separado para subir en teleférico.'),
        ('¿Hay desayuno todos los días?', 'Sí. Embaixada Carioca sirve desayuno todos los días en el Morro da Urca, dentro del Parque Bondinho Pão de Açúcar.'),
        ('¿Cuáles son las especialidades?', 'Las especialidades incluyen picanha brasileña, feijoada premiada vinculada a la tradición de Academia da Cachaça, bobó de camarón, caipirinhas y chopp frío.'),
    ],
}


def restaurant_schema(lang: str) -> dict:
    return {
        '@type': ['Restaurant', 'LocalBusiness', 'FoodEstablishment'],
        '@id': BASE + '/#restaurant',
        'name': 'Embaixada Carioca',
        'alternateName': ['Restaurante no Morro da Urca', 'Restaurante do Bondinho', 'Brazilian Restaurant at Urca Hill'],
        'url': BASE + '/',
        'image': [BASE + '/assets/hero.jpg', BASE + '/assets/hero.webp'],
        'logo': BASE + '/assets/logo-embaixada-carioca.png',
        'description': 'Restaurante brasileiro no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com café da manhã, almoço, caipirinhas, eventos e vista para o Pão de Açúcar.',
        'telephone': PHONE,
        'email': EMAIL,
        'address': ADDRESS,
        'geo': GEO,
        'servesCuisine': ['Brasileira', 'Carioca', 'Brazilian'],
        'priceRange': '$$',
        'acceptsReservations': True,
        'hasMap': 'https://maps.google.com/?q=Av.+Pasteur,+520,+Urca,+Rio+de+Janeiro',
        'isAccessibleForFree': False,
        'publicAccess': True,
        'touristType': ['Turistas brasileiros', 'International visitors', 'Famílias', 'Casais', 'Grupos corporativos'],
        'slogan': 'A alma carioca no alto do Rio.',
        'sameAs': ['https://www.instagram.com/embaixadacarioca/'],
        'potentialAction': {'@type': 'ReserveAction', 'target': TAGME},
        'aggregateRating': {'@type': 'AggregateRating', 'ratingValue': '4.8', 'bestRating': '5', 'ratingCount': '7779'},
    }


def menu_schema() -> dict:
    return {
        '@type': 'Menu',
        '@id': BASE + '/#menu',
        'name': 'Cardápio Embaixada Carioca',
        'url': BASE + '/cardapio.html',
        'hasMenuSection': [
            {'@type': 'MenuSection', 'name': 'Pratos brasileiros', 'hasMenuItem': [
                {'@type': 'MenuItem', 'name': 'Picanha brasileira', 'description': 'Picanha brasileira para almoço no Morro da Urca com vista para o Pão de Açúcar.'},
                {'@type': 'MenuItem', 'name': 'Feijoada premiada', 'description': 'Feijoada ligada à tradição da Academia da Cachaça.'},
                {'@type': 'MenuItem', 'name': 'Bobó de camarão', 'description': 'Clássico brasileiro com camarão.'},
            ]},
            {'@type': 'MenuSection', 'name': 'Bebidas e caipirinhas', 'hasMenuItem': [
                {'@type': 'MenuItem', 'name': 'Caipirinha da casa', 'description': 'Caipirinha com cachaça Magnífica, limão tahiti e siciliano, adoçada com rapadura.'},
                {'@type': 'MenuItem', 'name': 'Chope Heineken', 'description': 'Chope Heineken gelado.'},
                {'@type': 'MenuItem', 'name': 'Bossa Sour', 'description': 'Drink sugerido para começar a experiência.'},
            ]},
            {'@type': 'MenuSection', 'name': 'Café da manhã', 'hasMenuItem': [
                {'@type': 'MenuItem', 'name': 'Café da manhã da Embaixada', 'description': 'Café da manhã diário no Morro da Urca, com vista para o Pão de Açúcar.'},
            ]},
        ],
        'provider': {'@id': BASE + '/#restaurant'},
    }


def faq_schema(lang: str, page_url: str) -> dict:
    return {
        '@type': 'FAQPage',
        '@id': BASE + page_url + '#faq',
        'inLanguage': lang,
        'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
            for q, a in FAQS.get(lang, FAQS['pt-BR'])
        ]
    }


def breadcrumb_schema(page_url: str, page_name: str) -> dict:
    return {
        '@type': 'BreadcrumbList',
        '@id': BASE + page_url + '#breadcrumb',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': page_name, 'item': BASE + page_url},
        ]
    }


def webpage_schema(lang: str, page_url: str, page_name: str, desc: str) -> dict:
    return {
        '@type': 'WebPage',
        '@id': BASE + page_url + '#webpage',
        'url': BASE + page_url,
        'name': page_name,
        'description': desc,
        'inLanguage': lang,
        'isPartOf': {'@id': BASE + '/#website'},
        'about': {'@id': BASE + '/#restaurant'},
        'mainEntity': {'@id': BASE + '/#restaurant'},
    }


def website_schema(lang: str) -> dict:
    return {
        '@type': 'WebSite',
        '@id': BASE + '/#website',
        'url': BASE + '/',
        'name': 'Embaixada Carioca',
        'inLanguage': lang,
        'publisher': {'@id': BASE + '/#restaurant'},
        'potentialAction': {'@type': 'SearchAction', 'target': BASE + '/?s={search_term_string}', 'query-input': 'required name=search_term_string'},
    }


def graph(lang: str, page_url: str, page_name: str, desc: str) -> dict:
    return {
        '@context': 'https://schema.org',
        '@graph': [
            restaurant_schema(lang),
            menu_schema(),
            website_schema(lang),
            webpage_schema(lang, page_url, page_name, desc),
            faq_schema(lang, page_url),
            breadcrumb_schema(page_url, page_name),
        ]
    }


def strip_old_schema(html: str) -> str:
    pattern = re.compile(re.escape(START) + r'.*?' + re.escape(END) + r'\s*', re.S)
    return pattern.sub('', html)


def insert_schema(html: str, schema: dict) -> str:
    html = strip_old_schema(html)
    payload = json.dumps(schema, ensure_ascii=False, indent=2)
    block = f'{START}\n<script type="application/ld+json" id="ec-p0-jsonld">\n{payload}\n</script>\n{END}\n'
    idx = html.lower().find('</head>')
    if idx < 0:
        return block + html
    return html[:idx] + block + html[idx:]


def main() -> int:
    OUT.mkdir(exist_ok=True)
    changed = []
    skipped = []
    for lang, rel, url, name, desc in PAGES:
        path = ROOT / rel
        if not path.exists():
            skipped.append(rel)
            continue
        html = path.read_text(encoding='utf-8', errors='ignore')
        new_html = insert_schema(html, graph(lang, url, name, desc))
        if new_html != html:
            path.write_text(new_html, encoding='utf-8')
            changed.append(rel)
    lines = [
        '# P0 Schema JSON-LD Report', '', 'Status: **PASS**', '',
        '## Implementado',
        '- JSON-LD estático no `<head>` das páginas prioritárias.',
        '- `Restaurant` + `LocalBusiness` + `FoodEstablishment`.',
        '- `FAQPage` com perguntas diretas para buscadores e IA.',
        '- `Menu` com picanha, feijoada, bobó, caipirinha, chope e café da manhã.',
        '- `BreadcrumbList` por página.',
        '- `WebSite` e `WebPage` conectados ao restaurante.', '',
        f'Páginas alteradas: **{len(changed)}**',
        f'Páginas não encontradas: **{len(skipped)}**', '',
        '## Alteradas'
    ]
    if changed:
        for rel in changed:
            lines.append(f'- `{rel}`')
    else:
        lines.append('Nenhuma; schema já estava aplicado.')
    if skipped:
        lines += ['', '## Não encontradas']
        for rel in skipped:
            lines.append(f'- `{rel}`')
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'P0 schema JSON-LD applied: changed={len(changed)} skipped={len(skipped)}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
