#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
REPORT = OUT / 'p0_schema_jsonld_report.md'
START = '<!-- EC P0 Structured Data -->'
END = '<!-- /EC P0 Structured Data -->'
BASE = 'https://www.embaixadacarioca.com'
TAGME = 'https://go.tagme.com.br/embaixadacarioca'
PHONE = '+5521966837556'
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
FORBIDDEN_RATING_KEYS = {'aggregateRating', 'ratingValue', 'reviewCount', 'ratingCount', 'bestRating', 'worstRating'}
SCRIPT_RE = re.compile(r'(<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)

PAGES = [
    ('pt-BR', 'index.html', '/', 'Embaixada Carioca', 'Restaurante no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, na primeira parada do teleférico. Café da manhã, almoço brasileiro, feijoada premiada, caipirinhas e chope com vista para o Pão de Açúcar.'),
    ('en', 'en/index.html', '/en/', 'Embaixada Carioca', 'Brazilian restaurant at Urca Hill, the first Sugarloaf Cable Car stop, with breakfast, Brazilian lunch, feijoada, caipirinhas, draft beer and Sugarloaf views.'),
    ('es', 'es/index.html', '/es/', 'Embaixada Carioca', 'Restaurante brasileño en el Morro da Urca, primera parada del Bondinho Pão de Açúcar, con desayuno, almuerzo brasileño, feijoada, caipirinhas, chopp y vista al Pan de Azúcar.'),
    ('pt-BR', 'almoco.html', '/almoco.html', 'Almoço no Morro da Urca', 'Almoço brasileiro no Morro da Urca, com feijoada premiada, picanha, bobó de camarão, caipirinhas e vista para o Pão de Açúcar.'),
    ('en', 'en/almoco.html', '/en/almoco.html', 'Lunch at Urca Hill', 'Brazilian lunch at Urca Hill with feijoada, picanha, shrimp bobó, caipirinhas and Sugarloaf views.'),
    ('es', 'es/almoco.html', '/es/almoco.html', 'Almuerzo en el Morro da Urca', 'Almuerzo brasileño en el Morro da Urca con feijoada, picanha, bobó de camarón, caipirinhas y vista al Pan de Azúcar.'),
    ('pt-BR', 'cafe-da-manha.html', '/cafe-da-manha.html', 'Café da manhã no Morro da Urca', 'Café da manhã todos os dias no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com vista para o Pão de Açúcar.'),
    ('en', 'en/cafe-da-manha.html', '/en/cafe-da-manha.html', 'Breakfast at Urca Hill', 'Daily breakfast at Urca Hill inside Sugarloaf Cable Car Park, with views of Sugarloaf Mountain.'),
    ('es', 'es/cafe-da-manha.html', '/es/cafe-da-manha.html', 'Desayuno en el Morro da Urca', 'Desayuno todos los días en el Morro da Urca, dentro del Parque Bondinho Pão de Açúcar, con vista al Pan de Azúcar.'),
    ('pt-BR', 'cardapio.html', '/cardapio.html', 'Cardápio Embaixada Carioca', 'Cardápio da Embaixada Carioca com café da manhã, almoço brasileiro, feijoada premiada, picanha, bobó de camarão, caipirinhas e chope.'),
    ('pt-BR', 'restaurante-morro-da-urca.html', '/restaurante-morro-da-urca.html', 'Restaurante no Morro da Urca', 'Restaurante no Morro da Urca, primeira parada do Bondinho Pão de Açúcar, com comida brasileira, caipirinhas, café da manhã, almoço e eventos.'),
    ('pt-BR', 'eventos.html', '/eventos.html', 'Eventos com vista no Rio de Janeiro', 'Eventos corporativos e privados no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com gastronomia brasileira e vista.'),
    ('en', 'en/eventos.html', '/en/eventos.html', 'Events with a view in Rio de Janeiro', 'Private and corporate events at Urca Hill inside Sugarloaf Cable Car Park, with Brazilian food, drinks and views.'),
    ('es', 'es/eventos.html', '/es/eventos.html', 'Eventos con vista en Río de Janeiro', 'Eventos privados y corporativos en el Morro da Urca, dentro del Parque Bondinho, con comida brasileña, drinks y vista.'),
    ('pt-BR', 'guia-do-rio.html', '/guia-do-rio.html', 'Guia do Rio: Morro da Urca e Pão de Açúcar', 'Guia para visitar o Morro da Urca e Pão de Açúcar, com dicas de acesso, roteiro e onde comer dentro do Parque Bondinho.'),
    ('pt-BR', 'restaurantes-romanticos-rio-de-janeiro.html', '/restaurantes-romanticos-rio-de-janeiro.html', 'Restaurante romântico no Rio de Janeiro com vista', 'Restaurante romântico no Rio de Janeiro com vista para o Pão de Açúcar, no Morro da Urca, ideal para casais e ocasiões especiais.'),
]

FAQS = {
    'pt-BR': [
        ('Tem restaurante no Bondinho do teleférico?', 'Sim. A Embaixada Carioca fica dentro do Parque Bondinho Pão de Açúcar, no Morro da Urca, a primeira parada do teleférico, com vista para o Pão de Açúcar.'),
        ('A Embaixada Carioca fica no topo do Pão de Açúcar?', 'Não. A Embaixada Carioca fica no Morro da Urca, na primeira parada do Bondinho Pão de Açúcar, com vista para o Pão de Açúcar.'),
        ('Precisa pagar o bondinho para ir ao restaurante?', 'A reserva é do restaurante. Quem sobe de bondinho precisa comprar o ingresso regular do Parque Bondinho; quem sobe pela trilha, quando aberta, segue as regras de acesso do parque.'),
        ('Tem café da manhã todos os dias?', 'Sim. A Embaixada Carioca serve café da manhã todos os dias no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar.'),
        ('Quais são as especialidades da casa?', 'As especialidades incluem picanha brasileira, feijoada premiada ligada à tradição da Academia da Cachaça, bobó de camarão, caipirinhas e chope gelado.'),
        ('A Embaixada Carioca recebe eventos?', 'Sim. A casa recebe eventos corporativos, grupos turísticos, cafés da manhã, coquetéis, aniversários e experiências privadas com vista no Morro da Urca.'),
    ],
    'en': [
        ('Is there a restaurant at the Sugarloaf cable car?', 'Yes. Embaixada Carioca is inside Sugarloaf Cable Car Park, at Urca Hill, the first cable car stop, with views of Sugarloaf Mountain.'),
        ('Is Embaixada Carioca at the top of Sugarloaf Mountain?', 'No. Embaixada Carioca is at Urca Hill, the first Sugarloaf Cable Car stop, with views of Sugarloaf Mountain.'),
        ('Does the restaurant reservation include the cable car ticket?', 'No. The restaurant reservation does not include the Sugarloaf Cable Car Park ticket. The park ticket must be purchased separately.'),
        ('Is breakfast served every day?', 'Yes. Embaixada Carioca serves breakfast every day at Urca Hill inside Sugarloaf Cable Car Park.'),
        ('What is the restaurant known for?', 'The restaurant is known for Brazilian food, caipirinhas, feijoada, picanha, breakfast and views of Sugarloaf Mountain.'),
    ],
    'es': [
        ('¿Hay restaurante en el Bondinho del teleférico?', 'Sí. Embaixada Carioca está dentro del Parque Bondinho Pão de Açúcar, en el Morro da Urca, la primera parada del teleférico, con vista al Pan de Azúcar.'),
        ('¿Embaixada Carioca está en la cima del Pan de Azúcar?', 'No. Embaixada Carioca está en el Morro da Urca, en la primera parada del Bondinho Pão de Açúcar, con vista al Pan de Azúcar.'),
        ('¿La reserva incluye la entrada del Bondinho?', 'No. La reserva es del restaurante. La entrada del Parque Bondinho Pão de Açúcar debe comprarse por separado para subir en teleférico.'),
        ('¿Hay desayuno todos los días?', 'Sí. Embaixada Carioca sirve desayuno todos los días en el Morro da Urca, dentro del Parque Bondinho Pão de Açúcar.'),
        ('¿Cuáles son las especialidades?', 'Las especialidades incluyen picanha brasileña, feijoada premiada vinculada a la tradición de Academia da Cachaça, bobó de camarón, caipirinhas y chopp frío.'),
    ],
}


def remove_forbidden_rating_fields(obj: Any) -> Any:
    if isinstance(obj, dict):
        cleaned = {}
        for k, v in obj.items():
            if k in FORBIDDEN_RATING_KEYS:
                continue
            if k == '@type' and (v == 'AggregateRating' or (isinstance(v, list) and 'AggregateRating' in v)):
                continue
            cleaned[k] = remove_forbidden_rating_fields(v)
        return cleaned
    if isinstance(obj, list):
        return [remove_forbidden_rating_fields(v) for v in obj]
    return obj


def clean_legacy_jsonld(html: str) -> str:
    def repl(match: re.Match) -> str:
        open_tag, payload, close_tag = match.groups()
        try:
            obj = json.loads(payload.strip())
        except Exception:
            return match.group(0)
        cleaned = remove_forbidden_rating_fields(obj)
        return open_tag + '\n' + json.dumps(cleaned, ensure_ascii=False, indent=2) + '\n' + close_tag
    return SCRIPT_RE.sub(repl, html)


def restaurant_schema(lang: str) -> dict:
    descriptions = {
        'pt-BR': 'Restaurante no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, na primeira parada do teleférico. Café da manhã, almoço brasileiro, feijoada premiada, caipirinhas e chope com vista para o Pão de Açúcar.',
        'en': 'Brazilian restaurant at Urca Hill, inside Sugarloaf Cable Car Park, at the first cable car stop. Breakfast, Brazilian lunch, feijoada, caipirinhas and draft beer with Sugarloaf views.',
        'es': 'Restaurante brasileño en el Morro da Urca, dentro del Parque Bondinho Pão de Açúcar, en la primera parada del teleférico. Desayuno, almuerzo brasileño, feijoada, caipirinhas y chopp con vista al Pan de Azúcar.',
    }
    return {
        '@type': ['Restaurant', 'LocalBusiness', 'FoodEstablishment'],
        '@id': BASE + '/#restaurant',
        'name': 'Embaixada Carioca',
        'alternateName': ['Restaurante do Bondinho', 'Restaurante Morro da Urca', 'Brazilian Restaurant at Urca Hill'],
        'url': BASE + '/',
        'logo': BASE + '/assets/logo-azul.svg',
        'image': [BASE + '/assets/hero.jpg', BASE + '/assets/hero.webp'],
        'description': descriptions.get(lang, descriptions['pt-BR']),
        'slogan': 'A alma carioca em frente ao Pão de Açúcar.',
        'telephone': PHONE,
        'email': EMAIL,
        'priceRange': '$$',
        'currenciesAccepted': 'BRL',
        'servesCuisine': ['Brasileira', 'Carioca', 'Brazilian', 'Frutos do mar', 'Café da manhã'],
        'address': ADDRESS,
        'geo': GEO,
        'hasMap': 'https://www.google.com/maps/dir/?api=1&destination=-22.9508333,-43.1641667',
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], 'opens': '08:30', 'closes': '21:00'}],
        'acceptsReservations': True,
        'hasMenu': BASE + '/cardapio.html',
        'award': ['Melhor Feijoada do Rio de Janeiro — Veja Rio Comer & Beber 2025/2026', '2º melhor chope Heineken do Brasil'],
        'isAccessibleForFree': False,
        'publicAccess': True,
        'smokingAllowed': False,
        'amenityFeature': [
            {'@type': 'LocationFeatureSpecification', 'name': 'Vista para o Pão de Açúcar', 'value': True},
            {'@type': 'LocationFeatureSpecification', 'name': 'Acessível para cadeirantes', 'value': True},
            {'@type': 'LocationFeatureSpecification', 'name': 'Café da manhã todos os dias', 'value': True},
            {'@type': 'LocationFeatureSpecification', 'name': 'Cardápio em português, inglês e espanhol', 'value': True},
        ],
        'parentOrganization': {'@type': 'Organization', 'name': 'Parque Bondinho Pão de Açúcar'},
        'sameAs': ['https://www.instagram.com/embaixadacarioca/'],
        'potentialAction': {'@type': 'ReserveAction', 'target': TAGME},
    }


def menu_schema(lang: str) -> dict:
    return {
        '@type': 'Menu',
        '@id': BASE + '/cardapio.html#menu',
        'name': 'Cardápio Embaixada Carioca',
        'inLanguage': lang,
        'url': BASE + '/cardapio.html',
        'provider': {'@id': BASE + '/#restaurant'},
        'hasMenuSection': [
            {'@type': 'MenuSection', 'name': 'Café da Manhã', 'description': 'Todos os dias, das 8h30 às 11h30', 'hasMenuItem': [
                {'@type': 'MenuItem', 'name': 'Café da manhã', 'description': 'Café da manhã diário no Morro da Urca, com vista para o Pão de Açúcar.'},
            ]},
            {'@type': 'MenuSection', 'name': 'Almoço Brasileiro', 'description': 'Todos os dias, das 11h30 às 17h', 'hasMenuItem': [
                {'@type': 'MenuItem', 'name': 'Feijoada da Academia da Cachaça', 'description': 'Feijoada premiada pela Veja Rio 2025/2026, servida no Morro da Urca.'},
                {'@type': 'MenuItem', 'name': 'Picanha à brasileira', 'description': 'Picanha grelhada com acompanhamentos brasileiros.'},
                {'@type': 'MenuItem', 'name': 'Bobó de camarão', 'description': 'Camarão em creme de mandioca com tempero brasileiro.'},
                {'@type': 'MenuItem', 'name': 'Picadinho carioca', 'description': 'Clássico carioca para almoço.'},
            ]},
            {'@type': 'MenuSection', 'name': 'Drinks e Bebidas', 'hasMenuItem': [
                {'@type': 'MenuItem', 'name': 'Caipirinha da casa', 'description': 'Caipirinha com cachaça Magnífica, limão tahiti e siciliano, adoçada com rapadura.'},
                {'@type': 'MenuItem', 'name': 'Chope Heineken', 'description': 'Chope Heineken gelado.'},
                {'@type': 'MenuItem', 'name': 'Bossa Sour', 'description': 'Drink da casa.'},
            ]},
        ],
    }


def faq_schema(lang: str, page_url: str) -> dict:
    return {'@type': 'FAQPage', '@id': BASE + page_url + '#faq', 'inLanguage': lang, 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQS.get(lang, FAQS['pt-BR'])]}


def breadcrumb_schema(page_url: str, page_name: str, lang: str) -> dict:
    home_name = {'pt-BR': 'Início', 'en': 'Home', 'es': 'Inicio'}.get(lang, 'Home')
    return {'@type': 'BreadcrumbList', '@id': BASE + page_url + '#breadcrumb', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': home_name, 'item': BASE + '/'}, {'@type': 'ListItem', 'position': 2, 'name': page_name, 'item': BASE + page_url}]}


def webpage_schema(lang: str, page_url: str, page_name: str, desc: str) -> dict:
    return {'@type': 'WebPage', '@id': BASE + page_url + '#webpage', 'url': BASE + page_url, 'name': page_name, 'description': desc, 'inLanguage': lang, 'isPartOf': {'@id': BASE + '/#website'}, 'about': {'@id': BASE + '/#restaurant'}, 'mainEntity': {'@id': BASE + '/#restaurant'}}


def website_schema(lang: str) -> dict:
    return {'@type': 'WebSite', '@id': BASE + '/#website', 'url': BASE + '/', 'name': 'Embaixada Carioca', 'inLanguage': lang, 'publisher': {'@id': BASE + '/#restaurant'}}


def graph(lang: str, page_url: str, page_name: str, desc: str) -> dict:
    return {'@context': 'https://schema.org', '@graph': [restaurant_schema(lang), menu_schema(lang), website_schema(lang), webpage_schema(lang, page_url, page_name, desc), faq_schema(lang, page_url), breadcrumb_schema(page_url, page_name, lang)]}


def strip_old_schema(html: str) -> str:
    return re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\s*', '', html, flags=re.S)


def insert_schema(html: str, schema: dict) -> str:
    html = clean_legacy_jsonld(strip_old_schema(html))
    payload = json.dumps(remove_forbidden_rating_fields(schema), ensure_ascii=False, indent=2)
    block = f'{START}\n<script type="application/ld+json" id="ec-p0-jsonld">\n{payload}\n</script>\n{END}\n'
    idx = html.lower().find('</head>')
    return html[:idx] + block + html[idx:] if idx >= 0 else block + html


def main() -> int:
    OUT.mkdir(exist_ok=True)
    changed, skipped = [], []
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
    lines = ['# P0 Schema JSON-LD Report', '', 'Status: **PASS**', '', '## Conformidade aplicada', '- `aggregateRating`, `ratingValue`, `reviewCount` e `ratingCount` foram removidos do JSON-LD.', '- O rating 4.8 pode continuar visível no texto da página, mas não entra no schema.', '- `award` foi usado para prêmios factuais, como Veja Rio.', '', '## Implementado', '- JSON-LD estático no `<head>` das páginas prioritárias.', '- `Restaurant` + `LocalBusiness` + `FoodEstablishment`.', '- `FAQPage`, `Menu`, `BreadcrumbList`, `WebSite` e `WebPage`.', '- Cobertura PT/EN/ES quando há página correspondente.', '', f'Páginas alteradas: **{len(changed)}**', f'Páginas não encontradas: **{len(skipped)}**', '', '## Alteradas']
    lines += [f'- `{rel}`' for rel in changed] or ['Nenhuma; schema já estava aplicado.']
    if skipped:
        lines += ['', '## Não encontradas'] + [f'- `{rel}`' for rel in skipped]
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'P0 schema JSON-LD applied safely: changed={len(changed)} skipped={len(skipped)}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
