#!/usr/bin/env python3
"""
Sprint 2 — Keyword Alignment + GEO Growth | Embaixada Carioca

Escopo:
1. Alinhar titles/metas com palavras que já provaram tráfego e conversão.
2. Inserir blocos GEO de resposta direta em páginas estratégicas.
3. Criar landing de café da manhã com vista como aposta orgânica em PT/EN/ES.
4. Reforçar Guia do Rio como hub de alto volume.
5. Adicionar interlinking entre Home, experiências e páginas de território.
6. Atualizar sitemap com novas landing pages.

Estratégia:
- Home: intenção local/conversão — restaurante Morro da Urca, Pão de Açúcar, Bondinho.
- Café da manhã: grande aposta orgânica — café da manhã com vista no Rio.
- Guia do Rio: alto volume — onde comer no Rio, restaurantes com vista.
- Território: capturar demanda do Parque Bondinho/Pão de Açúcar/Urca.
"""
from __future__ import annotations

from pathlib import Path
import html
import re
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.embaixadacarioca.com"
TAGME = "https://go.tagme.com.br/embaixadacarioca"
WHATSAPP = "https://wa.me/5521966837556"

REPORT: list[str] = []
COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "meta_updated": 0,
    "geo_blocks_inserted": 0,
    "geo_blocks_refreshed": 0,
    "landing_pages_created": 0,
    "sitemap_updated": 0,
}

CSS_MARKER_START = "<!-- EC Sprint 2 GEO Growth CSS -->"
CSS_MARKER_END = "<!-- /EC Sprint 2 GEO Growth CSS -->"
GEO_MARKER_START = "<!-- EC Sprint 2 GEO Direct Answer -->"
GEO_MARKER_END = "<!-- /EC Sprint 2 GEO Direct Answer -->"

HEAD_CLOSE_RE = re.compile(r"</head>", re.IGNORECASE)
BODY_CLOSE_RE = re.compile(r"</body>", re.IGNORECASE)
TITLE_RE = re.compile(r"<title>.*?</title>", re.IGNORECASE | re.DOTALL)
META_DESC_RE = re.compile(r'<meta\b(?=[^>]*\bname=["\']description["\'])(?=[^>]*\bcontent=["\'][^"\']*["\'])[^>]*>', re.IGNORECASE)
OG_TITLE_RE = re.compile(r'<meta\b(?=[^>]*\bproperty=["\']og:title["\'])(?=[^>]*\bcontent=["\'][^"\']*["\'])[^>]*>', re.IGNORECASE)
OG_DESC_RE = re.compile(r'<meta\b(?=[^>]*\bproperty=["\']og:description["\'])(?=[^>]*\bcontent=["\'][^"\']*["\'])[^>]*>', re.IGNORECASE)
TW_TITLE_RE = re.compile(r'<meta\b(?=[^>]*\bname=["\']twitter:title["\'])(?=[^>]*\bcontent=["\'][^"\']*["\'])[^>]*>', re.IGNORECASE)
TW_DESC_RE = re.compile(r'<meta\b(?=[^>]*\bname=["\']twitter:description["\'])(?=[^>]*\bcontent=["\'][^"\']*["\'])[^>]*>', re.IGNORECASE)
CSS_BLOCK_RE = re.compile(r"\n*<!-- EC Sprint 2 GEO Growth CSS -->[\s\S]*?<!-- /EC Sprint 2 GEO Growth CSS -->\s*", re.IGNORECASE)
GEO_BLOCK_RE = re.compile(r"\n*<!-- EC Sprint 2 GEO Direct Answer -->[\s\S]*?<!-- /EC Sprint 2 GEO Direct Answer -->\s*", re.IGNORECASE)

CSS_BLOCK = f"""{CSS_MARKER_START}
<style>
.ec-sprint2-geo{{background:#f6efde;color:#00405a;border-top:1px solid rgba(0,64,90,.10);border-bottom:1px solid rgba(0,64,90,.10);padding:48px 0;font-family:Catamaran,Verdana,system-ui,sans-serif}}
.ec-sprint2-geo .ec-wrap{{max-width:1180px;margin:0 auto;padding:0 24px}}
.ec-sprint2-geo .ec-kicker{{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#527f8f;margin-bottom:12px}}
.ec-sprint2-geo h2{{font-size:clamp(26px,3vw,42px);line-height:1.05;margin:0 0 14px;font-weight:700;letter-spacing:-.02em;color:#00405a}}
.ec-sprint2-geo p{{font-size:18px;line-height:1.55;max-width:860px;margin:0;color:#485156}}
.ec-sprint2-geo strong{{color:#00405a}}
.ec-sprint2-geo .ec-links{{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}}
.ec-sprint2-geo .ec-links a{{display:inline-flex;align-items:center;gap:8px;border:1px solid rgba(0,64,90,.18);border-radius:999px;padding:10px 15px;text-decoration:none;color:#00405a;background:rgba(255,255,255,.45);font-size:14px;font-weight:700}}
.ec-sprint2-geo .ec-links a:hover{{background:#f59b1e;color:#00405a;border-color:#f59b1e}}
@media(max-width:760px){{.ec-sprint2-geo{{padding:34px 0}}.ec-sprint2-geo p{{font-size:16px}}.ec-sprint2-geo .ec-links a{{width:100%;justify-content:center}}}}
</style>
{CSS_MARKER_END}"""

META = {
    "index.html": {
        "title": "Restaurante no Pão de Açúcar e Morro da Urca | Embaixada Carioca",
        "description": "Restaurante no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. Café da manhã, almoço brasileiro, caipirinhas e vista no Rio.",
        "geo_title": "Restaurante no Pão de Açúcar, Morro da Urca e Parque Bondinho",
        "answer": "Sim. A Embaixada Carioca é um restaurante no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, na primeira parada do teleférico. Serve café da manhã, almoço brasileiro, caipirinhas, chope e eventos com vista direta para o Pão de Açúcar.",
        "links": [
            ("Café da manhã com vista", "/cafe-da-manha-com-vista-rio-de-janeiro.html"),
            ("Almoço no Morro da Urca", "/almoco.html"),
            ("Onde comer no Pão de Açúcar", "/onde-comer-no-pao-de-acucar.html"),
            ("Restaurante Morro da Urca", "/restaurante-morro-da-urca.html"),
            ("Guia do Rio", "/guia-do-rio.html"),
        ],
    },
    "cafe-da-manha.html": {
        "title": "Café da Manhã com Vista no Rio | Pão de Açúcar",
        "description": "Café da manhã com vista no Rio, no Morro da Urca dentro do Parque Bondinho Pão de Açúcar. Aberto todos os dias a partir de 8h30.",
        "geo_title": "Café da manhã com vista no Rio de Janeiro, no Morro da Urca",
        "answer": "A Embaixada Carioca serve café da manhã todos os dias no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. É uma opção para quem busca café da manhã com vista no Rio de Janeiro, em ambiente ao ar livre e com vista direta para o Pão de Açúcar.",
        "links": [("Landing café com vista", "/cafe-da-manha-com-vista-rio-de-janeiro.html"), ("Reservar mesa", TAGME), ("Almoço brasileiro", "/almoco.html"), ("Como chegar", "/guia-do-rio.html")],
    },
    "cafe-da-manha-pao-de-acucar.html": {
        "title": "Café da Manhã no Pão de Açúcar | Embaixada Carioca",
        "description": "Café da manhã no Pão de Açúcar, na primeira parada do Bondinho. Vista para o Rio, pães, frutas, café e experiência carioca no Morro da Urca.",
        "geo_title": "Café da manhã no Pão de Açúcar: onde ir depois do Bondinho",
        "answer": "Para tomar café da manhã no Pão de Açúcar, a Embaixada Carioca fica dentro do Parque Bondinho, no Morro da Urca. O restaurante abre às 8h30 e oferece uma experiência de café da manhã com vista para quem visita o bondinho cedo.",
        "links": [("Café com vista no Rio", "/cafe-da-manha-com-vista-rio-de-janeiro.html"), ("Restaurante no Bondinho", "/restaurante-bondinho-pao-de-acucar.html"), ("Reservar", TAGME)],
    },
    "almoco.html": {
        "title": "Almoço no Morro da Urca | Restaurante Pão de Açúcar",
        "description": "Almoço brasileiro no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. Feijoada, picanha, caipirinhas e vista no Rio.",
        "geo_title": "Onde almoçar no Morro da Urca e no Pão de Açúcar",
        "answer": "A Embaixada Carioca é uma opção de almoço no Morro da Urca para quem visita o Parque Bondinho Pão de Açúcar. O cardápio destaca culinária brasileira, feijoada, picanha, caipirinhas e pratos para compartilhar com vista para o Rio.",
        "links": [("Cardápio", "/cardapio.html"), ("Feijoada com vista", "/feijoada-com-vista-rio-de-janeiro.html"), ("Onde comer no Pão de Açúcar", "/onde-comer-no-pao-de-acucar.html"), ("Reservar", TAGME)],
    },
    "entardecer.html": {
        "title": "Entardecer no Morro da Urca | Drinks com Vista no Rio",
        "description": "Entardecer no Morro da Urca com caipirinhas, chope e petiscos no Parque Bondinho Pão de Açúcar. Drinks com vista no Rio.",
        "geo_title": "Entardecer no Morro da Urca com caipirinhas e vista",
        "answer": "A Embaixada Carioca é uma opção para o entardecer no Morro da Urca, com caipirinhas, chope, petiscos e vista para o Pão de Açúcar. É indicada para quem quer estender o passeio no Parque Bondinho com uma experiência carioca ao fim da tarde.",
        "links": [("Caipirinha com vista", "/caipirinha-com-vista-rio.html"), ("Eventos", "/eventos.html"), ("Reservar", TAGME), ("Guia do Rio", "/guia-do-rio.html")],
    },
    "eventos.html": {
        "title": "Eventos no Morro da Urca | Vista para o Pão de Açúcar",
        "description": "Eventos corporativos e privados no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. Gastronomia brasileira e vista no Rio.",
        "geo_title": "Eventos no Morro da Urca dentro do Parque Bondinho",
        "answer": "A Embaixada Carioca recebe eventos no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. O espaço atende encontros corporativos, grupos, lançamentos, aniversários e experiências para agências, com gastronomia brasileira e vista para o Rio.",
        "links": [("Solicitar orçamento", "/eventos.html#orcamento"), ("Falar no WhatsApp", WHATSAPP), ("Cardápio", "/cardapio.html"), ("Como chegar", "/guia-do-rio.html")],
    },
    "cardapio.html": {
        "title": "Cardápio Embaixada Carioca | Restaurante no Pão de Açúcar",
        "description": "Cardápio da Embaixada Carioca: café da manhã, almoço brasileiro, feijoada, picanha, caipirinhas e chope no Morro da Urca.",
        "geo_title": "Cardápio do restaurante no Morro da Urca e Pão de Açúcar",
        "answer": "O cardápio da Embaixada Carioca reúne café da manhã, almoço brasileiro, feijoada, picanha, petiscos, caipirinhas e chope. O restaurante fica no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar.",
        "links": [("Café da manhã", "/cafe-da-manha.html"), ("Almoço", "/almoco.html"), ("Entardecer", "/entardecer.html"), ("Reservar", TAGME)],
    },
    "guia-do-rio.html": {
        "title": "Onde Comer no Rio de Janeiro com Vista | Guia da Embaixada",
        "description": "Guia para saber onde comer no Rio de Janeiro com vista: Morro da Urca, Pão de Açúcar, Urca, café da manhã, almoço e entardecer.",
        "geo_title": "Onde comer no Rio de Janeiro com vista: guia do Morro da Urca",
        "answer": "Para quem procura onde comer no Rio de Janeiro com vista, o Morro da Urca é uma das escolhas mais estratégicas. A Embaixada Carioca fica dentro do Parque Bondinho Pão de Açúcar e reúne café da manhã, almoço brasileiro, caipirinhas e entardecer com vista.",
        "links": [("Onde comer no Pão de Açúcar", "/onde-comer-no-pao-de-acucar.html"), ("Restaurantes perto do Pão de Açúcar", "/restaurantes-perto-do-pao-de-acucar.html"), ("Restaurante Morro da Urca", "/restaurante-morro-da-urca.html"), ("Café com vista", "/cafe-da-manha-com-vista-rio-de-janeiro.html")],
    },
    "restaurante-morro-da-urca.html": {
        "title": "Restaurante Morro da Urca | Embaixada Carioca",
        "description": "Restaurante no Morro da Urca com café da manhã, almoço, caipirinhas e vista para o Pão de Açúcar dentro do Parque Bondinho.",
        "geo_title": "Restaurante no Morro da Urca para café, almoço e vista",
        "answer": "A Embaixada Carioca é um restaurante no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. É indicada para café da manhã, almoço brasileiro, caipirinhas, chope e eventos com vista para o Rio.",
        "links": [("Home", "/"), ("Almoço", "/almoco.html"), ("Café com vista", "/cafe-da-manha-com-vista-rio-de-janeiro.html"), ("Onde comer no Pão de Açúcar", "/onde-comer-no-pao-de-acucar.html")],
    },
    "restaurante-bondinho-pao-de-acucar.html": {
        "title": "Restaurante do Bondinho Pão de Açúcar | Embaixada Carioca",
        "description": "Restaurante do Bondinho Pão de Açúcar, na primeira parada do teleférico. Café da manhã, almoço brasileiro, caipirinhas e vista.",
        "geo_title": "Restaurante do Bondinho Pão de Açúcar na primeira parada",
        "answer": "A Embaixada Carioca é o restaurante do Bondinho Pão de Açúcar no Morro da Urca, a primeira parada do teleférico. O restaurante funciona para café da manhã, almoço, drinks e eventos com vista.",
        "links": [("Reservar", TAGME), ("Café da manhã", "/cafe-da-manha.html"), ("Almoço", "/almoco.html"), ("Guia do Rio", "/guia-do-rio.html")],
    },
    "onde-comer-no-pao-de-acucar.html": {
        "title": "Onde Comer no Pão de Açúcar | Embaixada Carioca",
        "description": "Onde comer no Pão de Açúcar: Embaixada Carioca fica no Morro da Urca, dentro do Parque Bondinho, com café, almoço e caipirinhas.",
        "geo_title": "Onde comer no Pão de Açúcar durante o passeio de Bondinho",
        "answer": "Para comer no Pão de Açúcar durante o passeio, a Embaixada Carioca fica no Morro da Urca, dentro do Parque Bondinho. É uma opção para café da manhã, almoço brasileiro, caipirinhas e drinks com vista.",
        "links": [("Restaurante do Bondinho", "/restaurante-bondinho-pao-de-acucar.html"), ("Café da manhã", "/cafe-da-manha.html"), ("Almoço", "/almoco.html"), ("Reservar", TAGME)],
    },
    "restaurantes-perto-do-pao-de-acucar.html": {
        "title": "Restaurantes Perto do Pão de Açúcar | Onde Comer na Urca",
        "description": "Restaurantes perto do Pão de Açúcar: opção dentro do Parque Bondinho no Morro da Urca, com café, almoço, caipirinhas e vista.",
        "geo_title": "Restaurantes perto do Pão de Açúcar e da Urca",
        "answer": "Entre os restaurantes perto do Pão de Açúcar, a Embaixada Carioca tem o diferencial de estar dentro do próprio Parque Bondinho, no Morro da Urca. O restaurante atende café da manhã, almoço, drinks e eventos com vista.",
        "links": [("Onde comer no Pão de Açúcar", "/onde-comer-no-pao-de-acucar.html"), ("Restaurante Morro da Urca", "/restaurante-morro-da-urca.html"), ("Guia do Rio", "/guia-do-rio.html"), ("Reservar", TAGME)],
    },
}

META.update({
    "en/index.html": {
        "title": "Restaurant at Sugarloaf and Urca Hill | Embaixada Carioca",
        "description": "Brazilian restaurant at Urca Hill inside Sugarloaf Cable Car Park. Breakfast, lunch, caipirinhas and Rio views.",
        "geo_title": "Restaurant at Sugarloaf Cable Car Park and Urca Hill",
        "answer": "Embaixada Carioca is a Brazilian restaurant at Urca Hill, inside Sugarloaf Cable Car Park, on the first cable car stop. It serves breakfast, lunch, caipirinhas, draft beer and events with views of Sugarloaf Mountain and Rio.",
        "links": [("Breakfast with a view", "/en/breakfast-with-a-view-rio-de-janeiro.html"), ("Where to eat near Sugarloaf", "/en/where-to-eat-near-sugarloaf.html"), ("Restaurant at Urca Hill", "/en/restaurant-at-urca-hill.html"), ("Reserve", TAGME)],
    },
    "en/cafe-da-manha.html": {
        "title": "Breakfast with a View in Rio | Sugarloaf Cable Car Park",
        "description": "Breakfast with a view in Rio at Urca Hill, inside Sugarloaf Cable Car Park. Open daily from 8:30 am.",
        "geo_title": "Breakfast with a view in Rio de Janeiro at Urca Hill",
        "answer": "Embaixada Carioca serves breakfast with a view in Rio de Janeiro at Urca Hill, inside Sugarloaf Cable Car Park. It is a practical option for visitors going up the cable car early and looking for breakfast with a direct Sugarloaf view.",
        "links": [("Breakfast landing", "/en/breakfast-with-a-view-rio-de-janeiro.html"), ("Where to eat near Sugarloaf", "/en/where-to-eat-near-sugarloaf.html"), ("Reserve", TAGME)],
    },
    "en/guia-do-rio.html": {
        "title": "Where to Eat in Rio with a View | Embaixada Carioca Guide",
        "description": "Guide to where to eat in Rio with a view: Urca Hill, Sugarloaf, Brazilian lunch, breakfast, caipirinhas and sunset drinks.",
        "geo_title": "Where to eat in Rio de Janeiro with a view",
        "answer": "For visitors asking where to eat in Rio with a view, Urca Hill and Sugarloaf Cable Car Park are high-intent choices. Embaixada Carioca offers breakfast, Brazilian lunch, caipirinhas and sunset drinks inside the park.",
        "links": [("Where to eat near Sugarloaf", "/en/where-to-eat-near-sugarloaf.html"), ("Sugarloaf restaurant", "/en/sugarloaf-cable-car-restaurant.html"), ("Breakfast with a view", "/en/breakfast-with-a-view-rio-de-janeiro.html"), ("Reserve", TAGME)],
    },
    "es/index.html": {
        "title": "Restaurante en Pan de Azúcar y Morro da Urca | Embaixada",
        "description": "Restaurante brasileño en el Morro da Urca, dentro del Parque Bondinho Pan de Azúcar. Desayuno, almuerzo, caipirinhas y vista.",
        "geo_title": "Restaurante en el Pan de Azúcar, Morro da Urca y Parque Bondinho",
        "answer": "Embaixada Carioca es un restaurante brasileño en el Morro da Urca, dentro del Parque Bondinho Pan de Azúcar, en la primera parada del teleférico. Sirve desayuno, almuerzo, caipirinhas, cerveza de barril y eventos con vista.",
        "links": [("Desayuno con vista", "/es/desayuno-con-vista-rio-de-janeiro.html"), ("Dónde comer cerca del Pan de Azúcar", "/es/donde-comer-cerca-del-pan-de-azucar.html"), ("Restaurante Morro da Urca", "/es/restaurante-morro-da-urca.html"), ("Reservar", TAGME)],
    },
    "es/cafe-da-manha.html": {
        "title": "Desayuno con Vista en Río | Pan de Azúcar",
        "description": "Desayuno con vista en Río, en el Morro da Urca dentro del Parque Bondinho Pan de Azúcar. Abierto todos los días desde las 8:30.",
        "geo_title": "Desayuno con vista en Río de Janeiro, en el Morro da Urca",
        "answer": "Embaixada Carioca sirve desayuno con vista en Río de Janeiro, en el Morro da Urca, dentro del Parque Bondinho Pan de Azúcar. Es una opción para visitantes que suben temprano en el teleférico y quieren empezar el día con vista.",
        "links": [("Landing de desayuno", "/es/desayuno-con-vista-rio-de-janeiro.html"), ("Dónde comer cerca del Pan de Azúcar", "/es/donde-comer-cerca-del-pan-de-azucar.html"), ("Reservar", TAGME)],
    },
    "es/guia-do-rio.html": {
        "title": "Dónde Comer en Río con Vista | Guía Embaixada Carioca",
        "description": "Guía para saber dónde comer en Río con vista: Morro da Urca, Pan de Azúcar, desayuno, almuerzo brasileño y caipirinhas.",
        "geo_title": "Dónde comer en Río de Janeiro con vista",
        "answer": "Para quienes buscan dónde comer en Río con vista, el Morro da Urca y el Parque Bondinho Pan de Azúcar son opciones estratégicas. Embaixada Carioca reúne desayuno, almuerzo brasileño, caipirinhas y atardecer con vista.",
        "links": [("Dónde comer cerca del Pan de Azúcar", "/es/donde-comer-cerca-del-pan-de-azucar.html"), ("Restaurante en el Bondinho", "/es/restaurante-bondinho-pan-de-azucar.html"), ("Desayuno con vista", "/es/desayuno-con-vista-rio-de-janeiro.html"), ("Reservar", TAGME)],
    },
})

LANDINGS = {
    "cafe-da-manha-com-vista-rio-de-janeiro.html": {
        "lang": "pt-BR",
        "title": "Café da Manhã com Vista no Rio de Janeiro | Embaixada Carioca",
        "description": "Café da manhã com vista no Rio de Janeiro, no Morro da Urca dentro do Parque Bondinho Pão de Açúcar. Aberto todos os dias a partir de 8h30.",
        "h1": "Café da manhã com vista no Rio de Janeiro",
        "lead": "A Embaixada Carioca fica no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, e serve café da manhã todos os dias a partir das 8h30, com vista direta para o Pão de Açúcar.",
        "answer_title": "Qual o melhor café da manhã com vista no Rio?",
        "answer": "Para quem busca café da manhã com vista no Rio de Janeiro, a Embaixada Carioca combina localização turística, vista para o Pão de Açúcar e experiência brasileira no alto do Morro da Urca.",
        "cta": "Reservar mesa",
        "links": [("Café da manhã", "/cafe-da-manha.html"), ("Onde comer no Pão de Açúcar", "/onde-comer-no-pao-de-acucar.html"), ("Guia do Rio", "/guia-do-rio.html")],
    },
    "en/breakfast-with-a-view-rio-de-janeiro.html": {
        "lang": "en",
        "title": "Breakfast with a View in Rio de Janeiro | Embaixada Carioca",
        "description": "Breakfast with a view in Rio de Janeiro at Urca Hill, inside Sugarloaf Cable Car Park. Open daily from 8:30 am.",
        "h1": "Breakfast with a view in Rio de Janeiro",
        "lead": "Embaixada Carioca is located at Urca Hill, inside Sugarloaf Cable Car Park, and serves breakfast daily from 8:30 am with a direct view of Sugarloaf Mountain.",
        "answer_title": "Where to have breakfast with a view in Rio?",
        "answer": "For travelers looking for breakfast with a view in Rio de Janeiro, Embaixada Carioca combines a landmark location, Brazilian flavors and a direct Sugarloaf view inside the cable car park.",
        "cta": "Reserve a table",
        "links": [("Breakfast", "/en/cafe-da-manha.html"), ("Where to eat near Sugarloaf", "/en/where-to-eat-near-sugarloaf.html"), ("Rio guide", "/en/guia-do-rio.html")],
    },
    "es/desayuno-con-vista-rio-de-janeiro.html": {
        "lang": "es",
        "title": "Desayuno con Vista en Río de Janeiro | Embaixada Carioca",
        "description": "Desayuno con vista en Río de Janeiro, en el Morro da Urca dentro del Parque Bondinho Pan de Azúcar. Abierto todos los días desde las 8:30.",
        "h1": "Desayuno con vista en Río de Janeiro",
        "lead": "Embaixada Carioca está en el Morro da Urca, dentro del Parque Bondinho Pan de Azúcar, y sirve desayuno todos los días desde las 8:30 con vista directa al Pan de Azúcar.",
        "answer_title": "¿Dónde desayunar con vista en Río?",
        "answer": "Para quienes buscan desayuno con vista en Río de Janeiro, Embaixada Carioca combina una ubicación turística, sabores brasileños y vista directa al Pan de Azúcar dentro del parque del teleférico.",
        "cta": "Reservar mesa",
        "links": [("Desayuno", "/es/cafe-da-manha.html"), ("Dónde comer cerca del Pan de Azúcar", "/es/donde-comer-cerca-del-pan-de-azucar.html"), ("Guía de Río", "/es/guia-do-rio.html")],
    },
}


def replace_or_insert_meta(text: str, pattern: re.Pattern[str], replacement: str, fallback_before: str = "</head>") -> tuple[str, bool]:
    if pattern.search(text):
        new = pattern.sub(replacement, text, count=1)
        return new, new != text
    if fallback_before in text:
        return text.replace(fallback_before, replacement + "\n" + fallback_before, 1), True
    return text, False


def update_meta(text: str, rel: str, cfg: dict[str, object]) -> str:
    original = text
    title = html.escape(str(cfg["title"]), quote=False)
    desc = html.escape(str(cfg["description"]), quote=True)
    replacements = [
        (TITLE_RE, f"<title>{title}</title>"),
        (META_DESC_RE, f'<meta name="description" content="{desc}">'),
        (OG_TITLE_RE, f'<meta property="og:title" content="{title}">'),
        (OG_DESC_RE, f'<meta property="og:description" content="{desc}">'),
        (TW_TITLE_RE, f'<meta name="twitter:title" content="{title}">'),
        (TW_DESC_RE, f'<meta name="twitter:description" content="{desc}">'),
    ]
    for pattern, replacement in replacements:
        text, changed = replace_or_insert_meta(text, pattern, replacement)
        if changed:
            COUNTERS["meta_updated"] += 1
    if text != original:
        REPORT.append(f"META: {rel}")
    return text


def geo_block(cfg: dict[str, object]) -> str:
    links = "".join(f'<a href="{html.escape(url, quote=True)}">{html.escape(label)} →</a>' for label, url in cfg.get("links", []))
    return f"""
{GEO_MARKER_START}
<section class="ec-sprint2-geo" aria-label="Resposta direta para busca e IA">
  <div class="ec-wrap">
    <div class="ec-kicker">Resposta direta · SEO + GEO</div>
    <h2>{html.escape(str(cfg['geo_title']))}</h2>
    <p>{html.escape(str(cfg['answer']))}</p>
    <div class="ec-links">{links}</div>
  </div>
</section>
{GEO_MARKER_END}
""".strip()


def inject_css(text: str) -> str:
    text = CSS_BLOCK_RE.sub("\n", text)
    if HEAD_CLOSE_RE.search(text):
        return HEAD_CLOSE_RE.sub(CSS_BLOCK + "\n</head>", text, count=1)
    return text


def inject_geo(text: str, rel: str, cfg: dict[str, object]) -> str:
    had_block = bool(GEO_BLOCK_RE.search(text))
    text = GEO_BLOCK_RE.sub("\n", text)
    block = geo_block(cfg)
    if BODY_CLOSE_RE.search(text):
        text = BODY_CLOSE_RE.sub(block + "\n</body>", text, count=1)
        if had_block:
            COUNTERS["geo_blocks_refreshed"] += 1
        else:
            COUNTERS["geo_blocks_inserted"] += 1
        REPORT.append(f"GEO_BLOCK: {rel}")
    return text


def process_existing_pages() -> None:
    for rel, cfg in META.items():
        path = ROOT / rel
        if not path.exists():
            REPORT.append(f"SKIP_MISSING: {rel}")
            continue
        COUNTERS["html_scanned"] += 1
        original = path.read_text(encoding="utf-8", errors="ignore")
        text = update_meta(original, rel, cfg)
        text = inject_css(text)
        text = inject_geo(text, rel, cfg)
        if text != original:
            path.write_text(text, encoding="utf-8")
            COUNTERS["html_updated"] += 1
            REPORT.append(f"UPDATED: {rel}")


def landing_html(rel: str, cfg: dict[str, object]) -> str:
    lang = cfg["lang"]
    links = "".join(f'<a href="{html.escape(url, quote=True)}">{html.escape(label)} →</a>' for label, url in cfg["links"])
    canonical = f"{BASE}/{rel}" if not rel.endswith("index.html") else f"{BASE}/"
    return f"""<!DOCTYPE html>
<html lang="{html.escape(str(lang))}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(str(cfg['title']))}</title>
<meta name="description" content="{html.escape(str(cfg['description']), quote=True)}">
<link rel="canonical" href="{canonical}">
<link rel="preload" as="image" href="/assets/cafe-manha-pao-acucar-frente.webp" type="image/webp">
<link href="/assets/fonts/fonts.css" rel="stylesheet">
<style>
:root{{--azul:#00405a;--amarelo:#f59b1e;--areia:#f6efde;--verde:#335d4a;--cinza:#485156}}*{{box-sizing:border-box}}body{{margin:0;background:var(--areia);color:var(--azul);font-family:Catamaran,Verdana,system-ui,sans-serif;line-height:1.55}}a{{color:inherit}}.top{{position:fixed;top:0;left:0;right:0;z-index:5;display:flex;justify-content:space-between;gap:24px;align-items:center;padding:18px 32px;background:rgba(0,64,90,.72);backdrop-filter:blur(14px);color:white}}.brand{{font-weight:800;letter-spacing:.12em;text-transform:uppercase;text-decoration:none}}.nav{{display:flex;gap:18px;flex-wrap:wrap}}.nav a{{text-decoration:none;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.08em}}.hero{{min-height:82vh;display:grid;align-items:end;padding:140px 24px 64px;background:linear-gradient(180deg,rgba(0,32,46,.12),rgba(0,32,46,.86)),url('/assets/cafe-manha-pao-acucar-frente.webp') center/cover;color:white}}.wrap{{max-width:1120px;margin:0 auto;width:100%}}.kicker{{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--amarelo);margin-bottom:18px}}h1{{font-size:clamp(42px,7vw,86px);line-height:.95;margin:0 0 18px;letter-spacing:-.04em}}.lead{{font-size:clamp(18px,2.2vw,24px);max-width:760px;color:rgba(255,255,255,.9)}}.ctas{{display:flex;gap:14px;flex-wrap:wrap;margin-top:28px}}.btn{{display:inline-flex;border-radius:999px;padding:15px 24px;background:var(--amarelo);color:var(--azul);font-weight:800;text-decoration:none;text-transform:uppercase;letter-spacing:.08em}}.btn.ghost{{background:transparent;color:white;border:1px solid rgba(255,255,255,.7)}}section{{padding:72px 24px}}.card{{background:white;border:1px solid rgba(0,64,90,.12);border-radius:24px;padding:34px;box-shadow:0 18px 55px rgba(0,64,90,.08)}}h2{{font-size:clamp(30px,4vw,52px);line-height:1.05;margin:0 0 18px}}p{{font-size:18px;color:var(--cinza);max-width:820px}}.links{{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}}.links a{{border:1px solid rgba(0,64,90,.18);border-radius:999px;padding:10px 15px;text-decoration:none;font-weight:700}}footer{{padding:34px 24px;background:var(--azul);color:white;text-align:center}}@media(max-width:760px){{.top{{position:absolute;align-items:flex-start;flex-direction:column}}.nav{{gap:10px}}.hero{{padding-top:190px}}.btn,.links a{{width:100%;justify-content:center}}}}
</style>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Restaurant","name":"Embaixada Carioca","url":"{BASE}/","servesCuisine":["Brazilian","Carioca","Breakfast"],"hasMenu":"{BASE}/cardapio.html","acceptsReservations":true,"telephone":"+5521966837556","address":{{"@type":"PostalAddress","streetAddress":"Av. Pasteur, 520 — Morro da Urca","addressLocality":"Rio de Janeiro","addressRegion":"RJ","addressCountry":"BR"}}}}</script>
</head>
<body>
<header class="top"><a class="brand" href="/">Embaixada Carioca</a><nav class="nav"><a href="/cafe-da-manha.html">Café</a><a href="/almoco.html">Almoço</a><a href="/entardecer.html">Entardecer</a><a href="/cardapio.html">Cardápio</a></nav></header>
<main>
<section class="hero"><div class="wrap"><div class="kicker">Morro da Urca · Parque Bondinho Pão de Açúcar</div><h1>{html.escape(str(cfg['h1']))}</h1><p class="lead">{html.escape(str(cfg['lead']))}</p><div class="ctas"><a class="btn" href="{TAGME}">{html.escape(str(cfg['cta']))}</a><a class="btn ghost" href="/guia-do-rio.html">Como chegar</a></div></div></section>
<section><div class="wrap card"><div class="kicker">Resposta direta · SEO + GEO</div><h2>{html.escape(str(cfg['answer_title']))}</h2><p>{html.escape(str(cfg['answer']))}</p><div class="links">{links}</div></div></section>
<section><div class="wrap"><h2>Por que essa página existe?</h2><p>Esta landing foi criada para responder diretamente às buscas de alta intenção sobre café da manhã com vista, restaurantes no Morro da Urca e experiências dentro do Parque Bondinho Pão de Açúcar.</p></div></section>
</main>
<footer>Embaixada Carioca · Morro da Urca · Parque Bondinho Pão de Açúcar</footer>
</body>
</html>
"""


def create_landings() -> None:
    for rel, cfg in LANDINGS.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        original = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        text = landing_html(rel, cfg)
        if text != original:
            path.write_text(text, encoding="utf-8")
            COUNTERS["landing_pages_created"] += 1
            REPORT.append(f"LANDING: {rel}")


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text
    today = date.today().isoformat()
    entries = []
    for rel in LANDINGS:
        loc = f"{BASE}/{rel}"
        if loc not in text:
            entries.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.86</priority>\n  </url>")
    if entries:
        text = text.replace("</urlset>", "\n" + "\n".join(entries) + "\n</urlset>")
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["sitemap_updated"] += 1
        REPORT.append("SITEMAP: novas landings de café adicionadas")


def write_report() -> None:
    out = ROOT / "_audit_reports"
    out.mkdir(exist_ok=True)
    report = out / "sprint2_keyword_geo_growth_report.md"
    lines = [
        "# Sprint 2 — Keyword Alignment + GEO Growth",
        "",
        "## Objetivo",
        "Ocupar território de busca com base em palavras que já provaram tráfego e conversão: Morro da Urca, Pão de Açúcar, Bondinho, onde comer no Rio, restaurantes com vista e café da manhã com vista.",
        "",
        "## Entregas",
        "- Titles/metas orientados por intenção real.",
        "- Blocos GEO de resposta direta em páginas estratégicas.",
        "- Landing de café da manhã com vista em PT/EN/ES.",
        "- Guia do Rio reforçado como hub de alto volume.",
        "- Interlinking entre home, experiências e páginas de território.",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Ações aplicadas"])
    lines.extend(f"- {x}" for x in REPORT) if REPORT else lines.append("- Nenhuma ação necessária.")
    lines.append("")
    report.write_text("\n".join(lines), encoding="utf-8")
    print(report.read_text(encoding="utf-8"))


def main() -> int:
    process_existing_pages()
    create_landings()
    update_sitemap()
    write_report()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
