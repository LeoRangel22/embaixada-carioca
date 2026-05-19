#!/usr/bin/env python3
"""
Search Territory Phase 1 — Embaixada Carioca.

Cria páginas SEO/GEO em PT, EN e ES para ocupar o território central:
- Parque Bondinho Pão de Açúcar
- Restaurante no Bondinho
- Onde comer no Pão de Açúcar
- Restaurante no Morro da Urca
- Restaurantes perto do Pão de Açúcar

Regra: todo tema criado em português é criado também em inglês e espanhol.
"""
from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.embaixadacarioca.com"
HERO = "/assets/hero.jpg"
RESERVE_URL = "https://go.tagme.com.br/embaixadacarioca"
REVIEW_URL = "https://g.page/r/CU-tJiJIjBUcEAE/review"

LANG = {
    "pt": {
        "html": "pt-BR", "hreflang": "pt-BR", "prefix": "", "locale": "pt_BR",
        "reserve": "Reservar mesa", "menu": "Ver cardápio",
        "eyebrow": "Restaurante do Bondinho · Morro da Urca · Parque Bondinho Pão de Açúcar · Rio de Janeiro · Brasil",
        "direct": "Resposta direta", "why": "Por que essa busca importa", "choose": "Quando escolher a Embaixada Carioca", "compare": "Opções da região e como decidir", "faq": "Perguntas frequentes", "links": "Continue explorando",
        "disclaimer": "Guia editorial. As marcas citadas pertencem aos seus respectivos titulares.",
        "nav": [("Café da manhã","/cafe-da-manha.html"),("Almoço","/almoco.html"),("Entardecer","/entardecer.html"),("Eventos","/eventos.html"),("Cardápio","/cardapio.html"),("Guia do Rio","/guia-do-rio.html")],
    },
    "en": {
        "html": "en", "hreflang": "en", "prefix": "en/", "locale": "en_US",
        "reserve": "Reserve a table", "menu": "See menu",
        "eyebrow": "Restaurant at the Cable Car · Urca Hill · Sugarloaf Cable Car Park · Rio de Janeiro · Brazil",
        "direct": "Direct answer", "why": "Why this search matters", "choose": "When to choose Embaixada Carioca", "compare": "Nearby options and how to decide", "faq": "Frequently asked questions", "links": "Keep exploring",
        "disclaimer": "Editorial guide. Mentioned brands belong to their respective owners.",
        "nav": [("Breakfast","/en/cafe-da-manha.html"),("Lunch","/en/almoco.html"),("Sunset","/en/entardecer.html"),("Events","/en/eventos.html"),("Menu","/en/cardapio.html"),("Rio Guide","/en/guia-do-rio.html")],
    },
    "es": {
        "html": "es", "hreflang": "es", "prefix": "es/", "locale": "es_ES",
        "reserve": "Reservar mesa", "menu": "Ver menú",
        "eyebrow": "Restaurante del Bondinho · Morro da Urca · Parque Bondinho Pan de Azúcar · Río de Janeiro · Brasil",
        "direct": "Respuesta directa", "why": "Por qué importa esta búsqueda", "choose": "Cuándo elegir Embaixada Carioca", "compare": "Opciones cercanas y cómo decidir", "faq": "Preguntas frecuentes", "links": "Seguir explorando",
        "disclaimer": "Guía editorial. Las marcas mencionadas pertenecen a sus respectivos titulares.",
        "nav": [("Desayuno","/es/cafe-da-manha.html"),("Almuerzo","/es/almoco.html"),("Atardecer","/es/entardecer.html"),("Eventos","/es/eventos.html"),("Menú","/es/cardapio.html"),("Guía de Río","/es/guia-do-rio.html")],
    },
}

PAGES = [
    {
        "key": "parque-bondinho",
        "pt": {"slug":"parque-bondinho-pao-de-acucar.html","title":"Parque Bondinho Pão de Açúcar: onde comer no Morro da Urca","description":"Guia para comer no Parque Bondinho Pão de Açúcar: café da manhã, almoço brasileiro, caipirinhas e vista direta para o Pão de Açúcar.","h1":"Onde comer no Parque Bondinho Pão de Açúcar","lede":"A Embaixada Carioca fica no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, na primeira parada do bondinho.","answer":"Sim. Existe uma experiência gastronômica completa no Parque Bondinho Pão de Açúcar: a Embaixada Carioca, no Morro da Urca, com café da manhã, almoço brasileiro, caipirinhas, chope gelado e eventos com vista direta para o Pão de Açúcar."},
        "en": {"slug":"en/sugarloaf-cable-car-park.html","title":"Sugarloaf Cable Car Park: where to eat at Urca Hill","description":"Where to eat inside Sugarloaf Cable Car Park: breakfast, Brazilian lunch, caipirinhas and a direct Sugarloaf Mountain view at Urca Hill.","h1":"Where to eat at Sugarloaf Cable Car Park","lede":"Embaixada Carioca is located at Urca Hill, inside Sugarloaf Cable Car Park, at the first cable car stop.","answer":"Yes. Embaixada Carioca is a restaurant experience inside Sugarloaf Cable Car Park, at Urca Hill, serving breakfast, Brazilian lunch, caipirinhas, draft beer and events with a direct view of Sugarloaf Mountain."},
        "es": {"slug":"es/parque-bondinho-pan-de-azucar.html","title":"Parque Bondinho Pan de Azúcar: dónde comer en el Morro da Urca","description":"Dónde comer dentro del Parque Bondinho Pan de Azúcar: desayuno, almuerzo brasileño, caipirinhas y vista directa al Pan de Azúcar.","h1":"Dónde comer en el Parque Bondinho Pan de Azúcar","lede":"Embaixada Carioca está en el Morro da Urca, dentro del Parque Bondinho Pan de Azúcar, en la primera parada del teleférico.","answer":"Sí. Embaixada Carioca es una experiencia gastronómica dentro del Parque Bondinho Pan de Azúcar, en el Morro da Urca, con desayuno, almuerzo brasileño, caipirinhas, cerveza de barril y eventos con vista directa al Pan de Azúcar."}
    },
    {
        "key": "restaurante-bondinho",
        "pt": {"slug":"restaurante-bondinho-pao-de-acucar.html","title":"Restaurante no Bondinho Pão de Açúcar | Embaixada Carioca","description":"Restaurante no Bondinho Pão de Açúcar, na primeira parada do teleférico, com café da manhã, almoço, caipirinhas e vista.","h1":"Restaurante no Bondinho Pão de Açúcar","lede":"Para quem procura restaurante no Bondinho, a Embaixada Carioca é a opção no Morro da Urca, dentro do parque.","answer":"Sim. A Embaixada Carioca fica dentro do Parque Bondinho Pão de Açúcar, no Morro da Urca, e funciona como restaurante para quem busca onde comer no percurso do bondinho."},
        "en": {"slug":"en/sugarloaf-cable-car-restaurant.html","title":"Sugarloaf Cable Car Restaurant | Embaixada Carioca","description":"Restaurant inside Sugarloaf Cable Car Park, at the first cable car stop, with breakfast, Brazilian lunch, caipirinhas and views.","h1":"Sugarloaf Cable Car restaurant","lede":"For visitors looking for a restaurant at the Sugarloaf Cable Car, Embaixada Carioca is located at Urca Hill inside the park.","answer":"Yes. Embaixada Carioca is located inside Sugarloaf Cable Car Park, at Urca Hill, and serves visitors looking for where to eat on the cable car route."},
        "es": {"slug":"es/restaurante-bondinho-pan-de-azucar.html","title":"Restaurante en el Bondinho Pan de Azúcar | Embaixada Carioca","description":"Restaurante dentro del Parque Bondinho Pan de Azúcar, en la primera parada del teleférico, con desayuno, almuerzo y vista.","h1":"Restaurante en el Bondinho Pan de Azúcar","lede":"Para quien busca restaurante en el Bondinho, Embaixada Carioca está en el Morro da Urca, dentro del parque.","answer":"Sí. Embaixada Carioca está dentro del Parque Bondinho Pan de Azúcar, en el Morro da Urca, para quienes buscan dónde comer en el recorrido del teleférico."}
    },
    {
        "key": "onde-comer-pao",
        "pt": {"slug":"onde-comer-no-pao-de-acucar.html","title":"Onde comer no Pão de Açúcar | Guia Embaixada Carioca","description":"Onde comer no Pão de Açúcar: restaurante no Morro da Urca com café da manhã, almoço brasileiro, caipirinhas, chope e vista.","h1":"Onde comer no Pão de Açúcar","lede":"Um guia direto para quem está visitando o Pão de Açúcar e quer decidir onde comer com vista.","answer":"Para comer no Pão de Açúcar, a Embaixada Carioca é a opção no Morro da Urca, dentro do Parque Bondinho, com café da manhã, almoço, drinks e vista direta."},
        "en": {"slug":"en/where-to-eat-near-sugarloaf.html","title":"Where to eat near Sugarloaf Mountain | Embaixada Carioca","description":"Where to eat near Sugarloaf Mountain in Rio: restaurant at Urca Hill with breakfast, Brazilian lunch, caipirinhas and direct views.","h1":"Where to eat near Sugarloaf Mountain","lede":"A practical guide for visitors deciding where to eat before, during or after Sugarloaf Mountain.","answer":"For visitors looking for where to eat near Sugarloaf Mountain, Embaixada Carioca is located at Urca Hill inside Sugarloaf Cable Car Park."},
        "es": {"slug":"es/donde-comer-cerca-del-pan-de-azucar.html","title":"Dónde comer cerca del Pan de Azúcar | Embaixada Carioca","description":"Dónde comer cerca del Pan de Azúcar en Río: restaurante en el Morro da Urca con desayuno, almuerzo brasileño y vista directa.","h1":"Dónde comer cerca del Pan de Azúcar","lede":"Una guía directa para quien visita el Pan de Azúcar y quiere decidir dónde comer con vista.","answer":"Para quienes buscan dónde comer cerca del Pan de Azúcar, Embaixada Carioca está en el Morro da Urca, dentro del Parque Bondinho."}
    },
    {
        "key": "restaurante-morro-urca",
        "pt": {"slug":"restaurante-morro-da-urca.html","title":"Restaurante Morro da Urca com vista para o Pão de Açúcar","description":"Restaurante no Morro da Urca, dentro do Parque Bondinho, com café da manhã, almoço brasileiro e vista direta para o Pão de Açúcar.","h1":"Restaurante no Morro da Urca","lede":"A busca por restaurante no Morro da Urca aponta diretamente para a experiência gastronômica no alto do Bondinho.","answer":"A Embaixada Carioca é um restaurante no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com café da manhã, almoço brasileiro, caipirinhas e vista."},
        "en": {"slug":"en/restaurant-at-urca-hill.html","title":"Restaurant at Urca Hill with Sugarloaf Mountain view","description":"Restaurant at Urca Hill inside Sugarloaf Cable Car Park, serving breakfast, Brazilian lunch and drinks with direct Sugarloaf views.","h1":"Restaurant at Urca Hill","lede":"Searches for a restaurant at Urca Hill usually point to visitors already planning the Sugarloaf Cable Car route.","answer":"Embaixada Carioca is a restaurant at Urca Hill, inside Sugarloaf Cable Car Park, serving breakfast, Brazilian lunch and drinks with a direct view."},
        "es": {"slug":"es/restaurante-morro-da-urca.html","title":"Restaurante en el Morro da Urca con vista al Pan de Azúcar","description":"Restaurante en el Morro da Urca, dentro del Parque Bondinho, con desayuno, almuerzo brasileño y vista directa al Pan de Azúcar.","h1":"Restaurante en el Morro da Urca","lede":"La búsqueda por restaurante en el Morro da Urca apunta a visitantes que están organizando el recorrido del Bondinho.","answer":"Embaixada Carioca es un restaurante en el Morro da Urca, dentro del Parque Bondinho Pan de Azúcar, con desayuno, almuerzo brasileño y vista."}
    },
    {
        "key": "restaurantes-perto",
        "pt": {"slug":"restaurantes-perto-do-pao-de-acucar.html","title":"Restaurantes perto do Pão de Açúcar | Guia local","description":"Restaurantes perto do Pão de Açúcar: opções na Urca, Praia Vermelha e Morro da Urca para café, almoço, drinks e vista.","h1":"Restaurantes perto do Pão de Açúcar","lede":"Uma página para capturar quem compara Araá, Clássico Sunset Club, Terra Brasilis, Bar Urca, Flutuante, Fogo de Chão, Assador e opções do Parque Bondinho.","answer":"Quem procura restaurantes perto do Pão de Açúcar pode comparar opções na Praia Vermelha, Urca, Botafogo e Morro da Urca. A Embaixada Carioca se posiciona como a opção dentro do Parque Bondinho, no Morro da Urca."},
        "en": {"slug":"en/restaurants-near-sugarloaf-mountain.html","title":"Restaurants near Sugarloaf Mountain | Local guide","description":"Restaurants near Sugarloaf Mountain: options around Urca, Praia Vermelha and Urca Hill for breakfast, lunch, drinks and views.","h1":"Restaurants near Sugarloaf Mountain","lede":"A guide for searches comparing Araá, Clássico Sunset Club, Terra Brasilis, Bar Urca, Flutuante, Fogo de Chão, Assador and options inside the Cable Car Park.","answer":"Visitors searching for restaurants near Sugarloaf Mountain can compare Urca, Praia Vermelha, Botafogo and Urca Hill. Embaixada Carioca is positioned as the option inside Sugarloaf Cable Car Park."},
        "es": {"slug":"es/restaurantes-cerca-del-pan-de-azucar.html","title":"Restaurantes cerca del Pan de Azúcar | Guía local","description":"Restaurantes cerca del Pan de Azúcar: opciones en Urca, Praia Vermelha y Morro da Urca para desayuno, almuerzo, drinks y vista.","h1":"Restaurantes cerca del Pan de Azúcar","lede":"Una guía para búsquedas que comparan Araá, Clássico Sunset Club, Terra Brasilis, Bar Urca, Flutuante, Fogo de Chão, Assador y opciones del Parque Bondinho.","answer":"Quien busca restaurantes cerca del Pan de Azúcar puede comparar Urca, Praia Vermelha, Botafogo y Morro da Urca. Embaixada Carioca se posiciona como la opción dentro del Parque Bondinho."}
    }
]

COMPARE = {
    "pt": [("Araá", "Busca relacionada ao ecossistema gastronômico do Bondinho."), ("Clássico Sunset Club", "Busca associada a sunset e experiências no alto."), ("Terra Brasilis", "Opção pesquisada por quem está na Praia Vermelha e Urca."), ("Bar Urca", "Referência pesquisada por quem busca tradição na Urca."), ("Flutuante", "Busca ligada a vista e Baía de Guanabara."), ("Fogo de Chão e Assador", "Buscas comuns para quem pesquisa carne, grupos e vista no Rio."), ("Embaixada Carioca", "Opção no Morro da Urca, dentro do Parque Bondinho, com café da manhã, almoço, drinks e eventos.")],
    "en": [("Araá", "Search related to the Cable Car food ecosystem."), ("Clássico Sunset Club", "Search related to sunset and hilltop experiences."), ("Terra Brasilis", "An option searched by people around Praia Vermelha and Urca."), ("Bar Urca", "A reference searched by people looking for tradition in Urca."), ("Flutuante", "Search linked to views and Guanabara Bay."), ("Fogo de Chão and Assador", "Common searches for meat-focused restaurants, groups and views in Rio."), ("Embaixada Carioca", "Option at Urca Hill, inside Sugarloaf Cable Car Park, with breakfast, lunch, drinks and events.")],
    "es": [("Araá", "Búsqueda relacionada con el ecosistema gastronómico del Bondinho."), ("Clássico Sunset Club", "Búsqueda asociada al atardecer y experiencias en el alto."), ("Terra Brasilis", "Opción buscada por quienes están en Praia Vermelha y Urca."), ("Bar Urca", "Referencia buscada por quienes buscan tradición en Urca."), ("Flutuante", "Búsqueda vinculada a vista y Bahía de Guanabara."), ("Fogo de Chão y Assador", "Búsquedas comunes para carne, grupos y vista en Río."), ("Embaixada Carioca", "Opción en el Morro da Urca, dentro del Parque Bondinho, con desayuno, almuerzo, drinks y eventos.")]
}

FAQ = {
    "pt": [("A Embaixada Carioca fica dentro do Parque Bondinho?", "Sim. Fica no Morro da Urca, na primeira parada do bondinho."), ("Precisa comprar ingresso do Bondinho?", "Sim. O acesso ao Morro da Urca é feito pelo Parque Bondinho."), ("Serve café da manhã e almoço?", "Sim. A casa serve café da manhã, almoço brasileiro, caipirinhas, chope e eventos."), ("Esta página é uma comparação oficial com concorrentes?", "Não. É um guia editorial para ajudar o visitante a decidir onde comer na região.")],
    "en": [("Is Embaixada Carioca inside Sugarloaf Cable Car Park?", "Yes. It is at Urca Hill, at the first cable car stop."), ("Do I need a cable car ticket?", "Yes. Access to Urca Hill is through Sugarloaf Cable Car Park."), ("Does it serve breakfast and lunch?", "Yes. The restaurant serves breakfast, Brazilian lunch, caipirinhas, draft beer and events."), ("Is this an official comparison with competitors?", "No. This is an editorial guide to help visitors decide where to eat in the area.")],
    "es": [("¿Embaixada Carioca está dentro del Parque Bondinho?", "Sí. Está en el Morro da Urca, en la primera parada del teleférico."), ("¿Hay que comprar entrada del Bondinho?", "Sí. El acceso al Morro da Urca se realiza por el Parque Bondinho."), ("¿Sirve desayuno y almuerzo?", "Sí. La casa ofrece desayuno, almuerzo brasileño, caipirinhas, cerveza de barril y eventos."), ("¿Esta página es una comparación oficial con competidores?", "No. Es una guía editorial para ayudar al visitante a decidir dónde comer en la región.")]
}

WHY = {
    "pt": ["A busca local tem alta intenção: a pessoa está planejando o passeio, já está na região ou comparando onde comer.", "O objetivo é responder de forma clara e mostrar quando a Embaixada Carioca é a opção mais natural: dentro do Parque Bondinho, no alto do Morro da Urca, com vista direta para o Pão de Açúcar."],
    "en": ["Local search has strong intent: the visitor is planning the attraction, is already nearby or is comparing where to eat.", "The goal is to answer clearly and show when Embaixada Carioca is the natural option: inside the Cable Car Park, at Urca Hill, with a direct Sugarloaf view."],
    "es": ["La búsqueda local tiene alta intención: la persona está planificando el paseo, ya está en la región o comparando dónde comer.", "El objetivo es responder claramente y mostrar cuándo Embaixada Carioca es la opción natural: dentro del Parque Bondinho, en el Morro da Urca, con vista directa al Pan de Azúcar."]
}

CHOOSE = {
    "pt": ["Quando quiser comer dentro do circuito do Bondinho.", "Quando a vista para o Pão de Açúcar for parte da experiência.", "Quando quiser café da manhã, almoço brasileiro, caipirinha, chope ou evento no Morro da Urca."],
    "en": ["When you want to eat inside the Cable Car circuit.", "When the Sugarloaf view is part of the experience.", "When you want breakfast, Brazilian lunch, caipirinhas, draft beer or events at Urca Hill."],
    "es": ["Cuando quieres comer dentro del circuito del Bondinho.", "Cuando la vista al Pan de Azúcar es parte de la experiencia.", "Cuando quieres desayuno, almuerzo brasileño, caipirinha, cerveza de barril o evento en el Morro da Urca."]
}

CSS = """
<style>
:root{--azul:#00202e;--azul1:#00405a;--amarelo:#f59b1e;--areia:#f6efde}*{box-sizing:border-box}html,body{margin:0;padding:0;overflow-x:hidden}body{font-family:Catamaran,system-ui,sans-serif;background:var(--areia);color:var(--azul1);font-size:17px;line-height:1.6}.mono{font-family:'JetBrains Mono',monospace}a{color:inherit}nav.top{position:fixed;top:0;left:0;right:0;z-index:50}.nav-inner{display:flex;gap:26px;align-items:center;justify-content:space-between;padding:14px 64px;color:var(--areia)}.brand-logo{width:60px;height:60px}.brand-logo.dark,.brand-word,.nav-wa-btn{display:none}.nav-links{display:flex;gap:26px}.nav-links a,.btn{font-family:'JetBrains Mono',monospace;text-decoration:none;text-transform:uppercase;letter-spacing:.1em;font-size:12px;font-weight:800;white-space:nowrap}.btn{background:var(--amarelo);color:#fff;border-radius:999px;padding:15px 28px}.btn.ghost{background:transparent;border:1px solid var(--areia);color:var(--areia)}.nav-rating-badge{border:1px solid rgba(246,239,222,.3);border-radius:999px;padding:8px 16px;text-decoration:none;background:rgba(246,239,222,.12);font-family:'JetBrains Mono',monospace;font-size:11px}.nav-rating-stars{color:var(--amarelo);font-weight:900}.lang-current{border:1px solid rgba(246,239,222,.3);background:rgba(246,239,222,.12);color:#fff;border-radius:12px;height:36px;padding:0 12px;font-weight:800}.page-hero{height:100svh;min-height:720px;position:relative;overflow:hidden;color:var(--areia);isolation:isolate}.page-hero-photo{position:absolute;inset:0;z-index:-3}.page-hero-photo img{width:100%;height:100%;object-fit:cover;object-position:center 44%}.page-hero-overlay{position:absolute;inset:0;z-index:-2;background:linear-gradient(90deg,rgba(0,32,46,.08),rgba(0,32,46,.12) 35%,rgba(0,32,46,.5) 62%,rgba(0,32,46,.86)),linear-gradient(180deg,rgba(0,32,46,.18),rgba(0,32,46,.78))}.page-hero-content{position:absolute;inset:0;padding:140px 70px 90px}.eyebrow{font-family:'JetBrains Mono',monospace;color:var(--amarelo);text-transform:uppercase;letter-spacing:.28em;font-size:10px}.page-hero h1{position:absolute;right:7vw;top:22vh;max-width:620px;font-size:clamp(42px,5vw,78px);line-height:.95;font-weight:200;letter-spacing:-.03em;margin:0}.lede{position:absolute;right:7vw;top:54vh;max-width:580px;font-size:18px;color:rgba(246,239,222,.94)}.hero-chips{position:absolute;left:70px;bottom:175px;display:flex;gap:8px;flex-wrap:wrap}.hero-chips span{border:1px solid rgba(246,239,222,.28);background:rgba(0,32,46,.42);border-radius:999px;padding:6px 13px}.ctas{position:absolute;left:70px;bottom:88px;display:flex;gap:14px;flex-wrap:wrap}.wrap{max-width:1180px;margin:0 auto;padding:0 32px}.section{padding:82px 0;border-bottom:1px solid rgba(0,64,90,.12)}.section h2{font-size:clamp(32px,4vw,56px);line-height:1.04;margin:0 0 24px;font-weight:300}.direct-answer{background:white;border-left:5px solid var(--amarelo);padding:28px 32px;margin-top:-70px;position:relative;z-index:3;box-shadow:0 18px 60px rgba(0,32,46,.14)}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.card{background:white;border:1px solid rgba(0,64,90,.1);padding:24px}.faq details{background:white;margin-bottom:10px;padding:18px 22px}.territory-links{display:flex;flex-wrap:wrap;gap:10px}.territory-link{background:white;border:1px solid rgba(0,64,90,.18);border-radius:999px;padding:9px 14px;text-decoration:none}.footer{background:var(--azul);color:var(--areia);padding:42px 32px;text-align:center}@media(max-width:960px){.nav-links,.nav-rating-badge,.lang-switcher{display:none}.nav-inner{padding:10px 22px}.page-hero h1,.lede{position:static}.page-hero-content{padding:120px 24px}.hero-chips,.ctas{position:static;margin-top:24px}.grid{grid-template-columns:1fr}.direct-answer{margin-top:0}}
</style>
"""

def canon(slug: str) -> str:
    return f"{BASE}/{slug}"

def nav(lang: str) -> str:
    links = "".join(f'<a href="{href}">{escape(label)}</a>' for label, href in LANG[lang]["nav"])
    return f'<nav class="top"><div class="nav-inner"><a class="brand-mark" href="/"><img class="brand-logo light" src="/assets/logo-branco.svg" alt="Embaixada Carioca"><img class="brand-logo dark" src="/assets/logo-branco.svg" alt=""></a><div class="nav-links">{links}</div><a class="nav-rating-badge" href="{REVIEW_URL}"><span class="nav-rating-stars">4.8★</span> <span class="nav-rating-count">7.779 avaliações</span></a><div class="lang-switcher"><button class="lang-current" type="button">BR&nbsp;PT</button></div><a class="btn" href="{RESERVE_URL}">Reservar →</a></div></nav>'

def alternates(page: dict) -> str:
    out = []
    for l, cfg in LANG.items():
        out.append(f'<link rel="alternate" hreflang="{cfg["hreflang"]}" href="{canon(page[l]["slug"])}">')
    out.append(f'<link rel="alternate" hreflang="x-default" href="{canon(page["pt"]["slug"])}">')
    return "\n".join(out)

def schema(page: dict, lang: str) -> str:
    data = page[lang]
    faq_schema = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ[lang]]}
    restaurant = {"@context":"https://schema.org","@type":"Restaurant","@id":f"{BASE}/#restaurant","name":"Embaixada Carioca","url":BASE,"image":f"{BASE}{HERO}","telephone":"+55-21-96683-7556","priceRange":"$$$","servesCuisine":["Brasileira","Carioca","Breakfast","Bar"],"address":{"@type":"PostalAddress","streetAddress":"Av. Pasteur, 520 — Morro da Urca","addressLocality":"Urca","addressRegion":"RJ","addressCountry":"BR"},"geo":{"@type":"GeoCoordinates","latitude":-22.9511223,"longitude":-43.1642121},"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.8","reviewCount":"7779"}}
    breadcrumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Embaixada Carioca","item":BASE+"/"},{"@type":"ListItem","position":2,"name":data["h1"],"item":canon(data["slug"])}]}
    itemlist = {"@context":"https://schema.org","@type":"ItemList","name":data["h1"],"itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"description":d} for i,(n,d) in enumerate(COMPARE[lang])]}
    return "\n".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False,separators=(",",":"))}</script>' for x in [restaurant, faq_schema, breadcrumb, itemlist])

def territory_links(lang: str, current: str) -> str:
    links = []
    for p in PAGES:
        if p["key"] != current:
            links.append(f'<a class="territory-link" href="/{p[lang]["slug"]}">{escape(p[lang]["h1"])}</a>')
    return "".join(links)

def page_html(page: dict, lang: str) -> str:
    cfg, data = LANG[lang], page[lang]
    why = "".join(f"<p>{escape(x)}</p>" for x in WHY[lang])
    choose = "".join(f"<li>{escape(x)}</li>" for x in CHOOSE[lang])
    compare = "".join(f"<article class='card'><h3>{escape(n)}</h3><p>{escape(d)}</p></article>" for n,d in COMPARE[lang])
    faq = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q,a in FAQ[lang])
    chips = "".join(f"<span>{escape(x)}</span>" for x in ["4.8★ · 7.779 avaliações","Parque Bondinho","Morro da Urca","Pão de Açúcar"])
    return f'''<!DOCTYPE html>
<html lang="{cfg["html"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="canonical" href="{canon(data["slug"])}">
{alternates(page)}
<title>{escape(data["title"])}</title>
<meta name="description" content="{escape(data["description"])}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:locale" content="{cfg["locale"]}"><meta property="og:url" content="{canon(data["slug"])}"><meta property="og:title" content="{escape(data["title"])}"><meta property="og:description" content="{escape(data["description"])}"><meta property="og:image" content="{BASE}{HERO}"><meta property="og:site_name" content="Embaixada Carioca">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(data["title"])}"><meta name="twitter:description" content="{escape(data["description"])}"><meta name="twitter:image" content="{BASE}{HERO}">
<link rel="preload" as="image" href="{HERO}"><link rel="stylesheet" href="/assets/fonts/fonts.css">
{schema(page, lang)}
{CSS}
</head>
<body data-screen-label="Territory">
{nav(lang)}
<header class="page-hero"><picture class="page-hero-photo"><img src="{HERO}" alt="{escape(data["h1"])} — Embaixada Carioca"></picture><div class="page-hero-overlay"></div><div class="page-hero-content"><div class="eyebrow hero-eyebrow">{escape(cfg["eyebrow"])}</div><h1>{escape(data["h1"])}</h1><p class="lede">{escape(data["lede"])}</p><div class="hero-chips">{chips}</div><div class="ctas"><a class="btn" href="{RESERVE_URL}">{escape(cfg["reserve"])} →</a><a class="btn ghost" href="/cardapio.html">{escape(cfg["menu"])}</a></div></div></header>
<main><div class="wrap"><section class="direct-answer"><strong class="mono">{escape(cfg["direct"])}</strong><p>{escape(data["answer"])}</p></section><section class="section"><h2>{escape(cfg["why"])}</h2>{why}</section><section class="section"><h2>{escape(cfg["choose"])}</h2><ul>{choose}</ul></section><section class="section"><h2>{escape(cfg["compare"])}</h2><div class="grid">{compare}</div><p><small>{escape(cfg["disclaimer"])}</small></p></section><section class="section faq"><h2>{escape(cfg["faq"])}</h2>{faq}</section><section class="section"><h2>{escape(cfg["links"])}</h2><div class="territory-links">{territory_links(lang, page["key"])}</div></section></div></main>
<footer class="footer"><p>Embaixada Carioca · Morro da Urca · Parque Bondinho Pão de Açúcar</p><p><a class="btn" href="{RESERVE_URL}">{escape(cfg["reserve"])} →</a></p></footer>
</body></html>'''

def write_pages() -> list[str]:
    written = []
    for p in PAGES:
        for lang in LANG:
            slug = p[lang]["slug"]
            path = ROOT / slug
            path.parent.mkdir(parents=True, exist_ok=True)
            html = page_html(p, lang)
            old = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
            if html != old:
                path.write_text(html, encoding="utf-8")
                written.append(slug)
    return written

def update_sitemap() -> int:
    sitemap = ROOT / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8", errors="ignore") if sitemap.exists() else '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n'
    inserts, added = [], 0
    for p in PAGES:
        for lang in LANG:
            url = canon(p[lang]["slug"])
            if f"<loc>{url}</loc>" not in text:
                inserts.append(f"  <url>\n    <loc>{url}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.90</priority>\n  </url>")
                added += 1
    if inserts:
        text = text.replace("</urlset>", "\n" + "\n".join(inserts) + "\n</urlset>")
        sitemap.write_text(text, encoding="utf-8")
    return added

def report(written: list[str], added: int) -> None:
    d = ROOT / "_audit_reports"
    d.mkdir(exist_ok=True)
    f = d / "search_territory_phase1_report.md"
    lines = ["# Search Territory Phase 1", "", "## Regra", "- Todo tema criado em português foi criado também em inglês e espanhol.", "", "## Páginas geradas/atualizadas", *[f"- {x}" for x in written], "", f"## URLs adicionadas ao sitemap: {added}", "", "## Território", "- Parque Bondinho Pão de Açúcar", "- Restaurante no Bondinho", "- Onde comer no Pão de Açúcar", "- Restaurante Morro da Urca", "- Restaurantes perto do Pão de Açúcar", "- Araá, Clássico Sunset Club, Terra Brasilis, Bar Urca, Flutuante, Fogo de Chão e Assador citados apenas em contexto editorial seguro."]
    f.write_text("\n".join(lines), encoding="utf-8")
    print(f.read_text(encoding="utf-8"))

def main() -> int:
    written = write_pages()
    added = update_sitemap()
    report(written, added)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
