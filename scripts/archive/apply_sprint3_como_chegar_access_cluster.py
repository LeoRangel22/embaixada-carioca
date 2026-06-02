#!/usr/bin/env python3
"""
Sprint 3 — Como Chegar / Access Cluster | Embaixada Carioca

Objetivo:
- trocar o destaque do menu principal de Entardecer para Como Chegar;
- preservar a página Entardecer sem apagar;
- criar páginas Como Chegar em PT/EN/ES com SEO/GEO forte;
- atacar buscas de alta intenção sobre Bondinho, ingresso/ticket, acesso ao Pão de Açúcar,
  teleférico, Morro da Urca, Praia Vermelha, metrô, ônibus, Uber/táxi, carro, estacionamento,
  bicicleta e trilha do Morro da Urca;
- atualizar sitemap e gerar relatório.
"""
from __future__ import annotations

from pathlib import Path
from datetime import date
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.embaixadacarioca.com"
TAGME = "https://go.tagme.com.br/embaixadacarioca"
BONDINHO_URL = "https://bondinho.com.br"
MAPS_URL = "https://www.google.com/maps/search/?api=1&query=Parque+Bondinho+P%C3%A3o+de+A%C3%A7%C3%BAcar+Avenida+Pasteur+520+Urca"
PHONE = "+5521966837556"
ADDRESS = "Av. Pasteur, 520 – Urca – Rio de Janeiro – RJ"
TODAY = date.today().isoformat()

REPORT: list[str] = []
COUNTERS = {
    "html_scanned": 0,
    "nav_updated": 0,
    "pages_created": 0,
    "sitemap_updated": 0,
}

HTML_LANG_RE = re.compile(r"<html\b[^>]*\blang=[\"']([^\"']+)[\"']", re.IGNORECASE)
NAV_RE = re.compile(r"<nav\b[\s\S]*?</nav>", re.IGNORECASE)
ENTARDECER_ANCHOR_RE = re.compile(r"<a\b(?=[^>]*href=[\"'][^\"']*(?:entardecer|sunset|atardecer)\.html[\"'])[^>]*>[\s\S]*?</a>", re.IGNORECASE)
SITEMAP_URLSET_END_RE = re.compile(r"</urlset>\s*$", re.IGNORECASE)

NAV_TARGETS = {
    "pt": ("/como-chegar.html", "COMO CHEGAR"),
    "en": ("/en/how-to-get-there.html", "HOW TO GET THERE"),
    "es": ("/es/como-llegar.html", "CÓMO LLEGAR"),
}

PAGES = {
    "pt": {
        "rel": "como-chegar.html",
        "lang": "pt-BR",
        "title": "Como Chegar ao Pão de Açúcar e Morro da Urca | Embaixada Carioca",
        "description": "Como chegar à Embaixada Carioca no Morro da Urca: Bondinho, ingresso, trilha, metrô, ônibus, Uber, carro, estacionamento e bicicleta.",
        "nav": {"cafe": "CAFÉ DA MANHÃ", "almoco": "ALMOÇO", "como": "COMO CHEGAR", "eventos": "EVENTOS", "cardapio": "CARDÁPIO", "guia": "GUIA DO RIO", "base": ""},
        "h1": "Como chegar à Embaixada Carioca no Morro da Urca",
        "eyebrow": "Acesso ao Pão de Açúcar · Bondinho · Trilha · Urca",
        "lead": "Estamos no Morro da Urca, a primeira parada do Parque Bondinho Pão de Açúcar. O endereço de acesso é Avenida Pasteur, 520, Urca, Rio de Janeiro.",
        "direct_title": "Como acessar a Embaixada Carioca?",
        "direct_answer": "Para chegar à Embaixada Carioca, vá até a Praia Vermelha, na Urca, e acesse o Morro da Urca de Bondinho ou pela trilha. Pelo Bondinho, é necessário adquirir ingresso do Parque Bondinho Pão de Açúcar. Pela trilha, o acesso gratuito começa na Pista Cláudio Coutinho, ao lado da Praia Vermelha.",
        "quick": [
            ("📍 Localização", "Morro da Urca, primeira parada do Bondinho do Pão de Açúcar."),
            ("🗺️ Endereço", ADDRESS),
            ("🚠 Acesso principal", "Bondinho do Pão de Açúcar, com ingresso do parque."),
            ("🥾 Alternativa gratuita", "Trilha do Morro da Urca pela Pista Cláudio Coutinho, em média 30 a 40 minutos."),
        ],
        "sections": [
            ("1. Como acessar o Morro da Urca", [
                ("🚠 De Bondinho — acesso mais popular", "A forma mais tradicional e rápida é subir pelo Bondinho do Pão de Açúcar. O primeiro trecho liga a Praia Vermelha ao Morro da Urca, onde fica a Embaixada Carioca. Para acessar o restaurante por esse caminho, é necessário adquirir o ingresso do Parque Bondinho. Recomendamos comprar antecipadamente pelo site oficial do Bondinho."),
                ("🥾 Pela trilha — acesso gratuito e aventureiro", "Também é possível subir pela trilha do Morro da Urca, que começa na Pista Cláudio Coutinho, com entrada pela Praia Vermelha. A caminhada costuma levar cerca de 30 a 40 minutos, dependendo do ritmo. Vá com calçado confortável, água e atenção ao horário de funcionamento da área natural."),
            ]),
            ("2. Como chegar até a Urca e a Praia Vermelha", [
                ("🚕 Táxi, Uber ou 99", "É a opção mais direta. No aplicativo, use como destino Parque Bondinho Pão de Açúcar ou Avenida Pasteur, 520. O carro deixa você próximo à bilheteria e à entrada do parque."),
                ("🚇 Metrô + ônibus ou app", "A estação de metrô mais usada é Botafogo. De lá, siga de táxi, Uber/99 ou ônibus até a Urca/Praia Vermelha. A linha 513 costuma ser usada como conexão Botafogo–Urca, mas recomendamos conferir a rota em tempo real no app antes de sair."),
                ("🚌 Ônibus para a Urca", "Linhas comumente consultadas para Urca/Praia Vermelha incluem 107, 167, 513, 518 e 519. Como rotas e horários podem mudar, confirme o melhor trajeto no aplicativo de transporte no dia da visita."),
                ("🚗 De carro e estacionamento", "O Parque Bondinho não possui estacionamento próprio e as vagas públicas na Urca são limitadas. Alternativas próximas são estacionamentos em Botafogo, como Botafogo Praia Shopping, Shopping Rio Sul e Casa & Gourmet. A partir deles, avalie caminhar ou seguir de táxi/Uber conforme disposição, temperatura e tempo disponível."),
                ("🚲 Bicicleta e bikes compartilhadas", "A região da Praia Vermelha costuma ter estações de bicicleta compartilhada e é agradável para chegar pedalando pela orla. O parque não deve ser tratado como bicicletário interno; leve cadeado e prenda a bicicleta em local apropriado fora da área de acesso."),
                ("🚶 Caminhando de Botafogo", "De pontos como Shopping Rio Sul ou Casa & Gourmet, algumas pessoas optam por caminhar até a Praia Vermelha. É uma caminhada urbana curta a moderada, mas deve ser avaliada conforme calor, chuva, bagagem e disposição."),
            ]),
            ("3. Depois de chegar", [
                ("🍽️ Reserve e planeje o horário", "Depois de chegar ao Morro da Urca, você encontra a Embaixada Carioca na área da primeira parada do Bondinho. Para café da manhã, almoço, caipirinhas ou eventos, reserve com antecedência quando possível."),
                ("🌅 Entardecer sem destaque no menu", "A experiência de entardecer continua existindo, mas o menu principal passa a priorizar Como Chegar porque acesso, ingresso, Bondinho, trilha e estacionamento são dúvidas decisivas para quem visita o Pão de Açúcar."),
            ]),
        ],
        "faq": [
            ("Precisa comprar ingresso para chegar à Embaixada Carioca?", "Sim, se você acessar pelo Bondinho do Pão de Açúcar. O restaurante fica no Morro da Urca, dentro do Parque Bondinho. A alternativa gratuita é subir pela trilha do Morro da Urca, pela Pista Cláudio Coutinho."),
            ("Onde compro o ticket do Bondinho?", "O recomendado é comprar pelo site oficial bondinho.com.br ou pela bilheteria do parque, conforme disponibilidade."),
            ("Qual é o endereço para colocar no Uber ou GPS?", "Use Parque Bondinho Pão de Açúcar ou Avenida Pasteur, 520 – Urca – Rio de Janeiro – RJ."),
            ("Tem estacionamento no Parque Bondinho?", "Não há estacionamento próprio do parque. As vagas na Urca são limitadas; alternativas incluem estacionamentos em Botafogo, como Botafogo Praia Shopping, Shopping Rio Sul e Casa & Gourmet."),
            ("Dá para subir de graça?", "Sim, pela trilha do Morro da Urca, com acesso pela Pista Cláudio Coutinho, na Praia Vermelha. O percurso costuma levar cerca de 30 a 40 minutos."),
        ],
        "cta_primary": "Reservar mesa",
        "cta_secondary": "Comprar ingresso do Bondinho",
        "map_cta": "Abrir rota no Google Maps",
    },
    "en": {
        "rel": "en/how-to-get-there.html",
        "lang": "en",
        "title": "How to Get to Sugarloaf Cable Car Park and Urca Hill | Embaixada Carioca",
        "description": "How to get to Embaixada Carioca at Urca Hill: Sugarloaf cable car tickets, trail, metro, bus, Uber, car, parking and bike options.",
        "nav": {"cafe": "BREAKFAST", "almoco": "LUNCH", "como": "HOW TO GET THERE", "eventos": "EVENTS", "cardapio": "MENU", "guia": "RIO GUIDE", "base": "/en"},
        "h1": "How to get to Embaixada Carioca at Urca Hill",
        "eyebrow": "Sugarloaf access · Cable car · Trail · Urca",
        "lead": "We are located at Urca Hill, the first stop of Sugarloaf Cable Car Park. The access address is Avenida Pasteur, 520, Urca, Rio de Janeiro.",
        "direct_title": "How do I access Embaixada Carioca?",
        "direct_answer": "To reach Embaixada Carioca, go to Praia Vermelha in Urca and access Urca Hill by the Sugarloaf cable car or by the hiking trail. By cable car, visitors need a Sugarloaf Cable Car Park ticket. The free trail starts at Pista Cláudio Coutinho, next to Praia Vermelha.",
        "quick": [
            ("📍 Location", "Urca Hill, first stop of the Sugarloaf cable car."),
            ("🗺️ Address", ADDRESS),
            ("🚠 Main access", "Sugarloaf cable car, with a park ticket."),
            ("🥾 Free alternative", "Urca Hill trail from Pista Cláudio Coutinho, usually around 30 to 40 minutes."),
        ],
        "sections": [
            ("1. How to access Urca Hill", [
                ("🚠 By cable car — the most popular access", "The classic and fastest way is to take the Sugarloaf cable car. The first ride connects Praia Vermelha to Urca Hill, where Embaixada Carioca is located. To access the restaurant this way, visitors need a Sugarloaf Cable Car Park ticket. We recommend buying it in advance through the official Bondinho website."),
                ("🥾 By trail — free and adventurous", "You can also hike up the Urca Hill trail, which starts at Pista Cláudio Coutinho, with access from Praia Vermelha. The walk usually takes around 30 to 40 minutes, depending on pace. Wear comfortable shoes, bring water and check local opening times for the natural area."),
            ]),
            ("2. How to get to Urca and Praia Vermelha", [
                ("🚕 Taxi, Uber or 99", "This is the most direct option. In the app, use Parque Bondinho Pão de Açúcar or Avenida Pasteur, 520 as the destination. The car can drop you near the ticket office and park entrance."),
                ("🚇 Metro + bus or ride app", "Botafogo is the closest metro station commonly used by visitors. From there, continue by taxi, Uber/99 or bus to Urca/Praia Vermelha. Route 513 is often used for the Botafogo–Urca connection, but check real-time routing before leaving."),
                ("🚌 Bus to Urca", "Bus lines commonly checked for Urca/Praia Vermelha include 107, 167, 513, 518 and 519. Routes and schedules may change, so confirm the best itinerary in a transport app on the day of your visit."),
                ("🚗 By car and parking", "Sugarloaf Cable Car Park does not have its own parking lot and public parking in Urca is limited. Nearby alternatives include parking in Botafogo, such as Botafogo Praia Shopping, Shopping Rio Sul and Casa & Gourmet. From there, decide between walking or taking a ride app depending on weather, luggage and timing."),
                ("🚲 By bike", "Praia Vermelha often has shared-bike stations nearby and the area is pleasant for cycling. The park should not be treated as an internal bike parking area; bring a lock and use appropriate spots outside the access area."),
                ("🚶 Walking from Botafogo", "From Shopping Rio Sul or Casa & Gourmet, some visitors choose to walk to Praia Vermelha. It is a short to moderate urban walk, but heat, rain, luggage and available time should be considered."),
            ]),
            ("3. After you arrive", [
                ("🍽️ Reserve and plan your time", "Once you reach Urca Hill, Embaixada Carioca is located at the first cable car stop. For breakfast, lunch, caipirinhas or events, book in advance whenever possible."),
                ("🌅 Sunset is still available", "The sunset experience remains part of the restaurant, but the main menu now prioritizes access because directions, tickets, cable car, trail and parking are decisive questions for Sugarloaf visitors."),
            ]),
        ],
        "faq": [
            ("Do I need a ticket to reach Embaixada Carioca?", "Yes, if you access it by the Sugarloaf cable car. The restaurant is located at Urca Hill, inside Sugarloaf Cable Car Park. The free alternative is the Urca Hill trail via Pista Cláudio Coutinho."),
            ("Where do I buy Sugarloaf cable car tickets?", "We recommend buying tickets through the official website bondinho.com.br or at the park ticket office, depending on availability."),
            ("What should I type in Uber or GPS?", "Use Parque Bondinho Pão de Açúcar or Avenida Pasteur, 520 – Urca – Rio de Janeiro – RJ."),
            ("Is there parking at the park?", "The park does not have its own parking lot. Street parking in Urca is limited; alternatives include parking in Botafogo at Botafogo Praia Shopping, Shopping Rio Sul and Casa & Gourmet."),
            ("Can I go up for free?", "Yes. The Urca Hill trail starts at Pista Cláudio Coutinho, by Praia Vermelha, and usually takes around 30 to 40 minutes."),
        ],
        "cta_primary": "Reserve a table",
        "cta_secondary": "Buy cable car tickets",
        "map_cta": "Open route on Google Maps",
    },
    "es": {
        "rel": "es/como-llegar.html",
        "lang": "es",
        "title": "Cómo Llegar al Pan de Azúcar y Morro da Urca | Embaixada Carioca",
        "description": "Cómo llegar a Embaixada Carioca en el Morro da Urca: entradas del Bondinho, sendero, metro, autobús, Uber, coche, estacionamiento y bici.",
        "nav": {"cafe": "DESAYUNO", "almoco": "ALMUERZO", "como": "CÓMO LLEGAR", "eventos": "EVENTOS", "cardapio": "MENÚ", "guia": "GUÍA DE RÍO", "base": "/es"},
        "h1": "Cómo llegar a Embaixada Carioca en el Morro da Urca",
        "eyebrow": "Acceso al Pan de Azúcar · Bondinho · Sendero · Urca",
        "lead": "Estamos en el Morro da Urca, la primera parada del Parque Bondinho Pan de Azúcar. La dirección de acceso es Avenida Pasteur, 520, Urca, Río de Janeiro.",
        "direct_title": "¿Cómo acceder a Embaixada Carioca?",
        "direct_answer": "Para llegar a Embaixada Carioca, ve hasta Praia Vermelha, en Urca, y accede al Morro da Urca en Bondinho o por el sendero. En Bondinho, es necesario comprar entrada del Parque Bondinho Pan de Azúcar. El sendero gratuito comienza en la Pista Cláudio Coutinho, junto a Praia Vermelha.",
        "quick": [
            ("📍 Ubicación", "Morro da Urca, primera parada del Bondinho del Pan de Azúcar."),
            ("🗺️ Dirección", ADDRESS),
            ("🚠 Acceso principal", "Bondinho del Pan de Azúcar, con entrada del parque."),
            ("🥾 Alternativa gratuita", "Sendero del Morro da Urca por la Pista Cláudio Coutinho, normalmente 30 a 40 minutos."),
        ],
        "sections": [
            ("1. Cómo acceder al Morro da Urca", [
                ("🚠 En Bondinho — acceso más popular", "La forma más tradicional y rápida es subir en el Bondinho del Pan de Azúcar. El primer tramo conecta Praia Vermelha con el Morro da Urca, donde está Embaixada Carioca. Para acceder al restaurante por este camino, es necesario comprar la entrada del Parque Bondinho. Recomendamos comprarla con anticipación en el sitio oficial del Bondinho."),
                ("🥾 Por el sendero — acceso gratuito y aventurero", "También es posible subir por el sendero del Morro da Urca, que comienza en la Pista Cláudio Coutinho, con entrada por Praia Vermelha. La caminata suele durar entre 30 y 40 minutos, según el ritmo. Usa calzado cómodo, lleva agua y verifica los horarios del área natural."),
            ]),
            ("2. Cómo llegar a Urca y Praia Vermelha", [
                ("🚕 Taxi, Uber o 99", "Es la opción más directa. En la aplicación, usa Parque Bondinho Pão de Açúcar o Avenida Pasteur, 520 como destino. El coche te deja cerca de la boletería y la entrada del parque."),
                ("🚇 Metro + autobús o app", "La estación de metro más utilizada es Botafogo. Desde allí, sigue en taxi, Uber/99 o autobús hasta Urca/Praia Vermelha. La línea 513 suele usarse como conexión Botafogo–Urca, pero recomendamos confirmar la ruta en tiempo real antes de salir."),
                ("🚌 Autobús a Urca", "Líneas comúnmente consultadas para Urca/Praia Vermelha incluyen 107, 167, 513, 518 y 519. Como rutas y horarios pueden cambiar, confirma el mejor trayecto en una aplicación de transporte el día de la visita."),
                ("🚗 En coche y estacionamiento", "El Parque Bondinho no tiene estacionamiento propio y las plazas públicas en Urca son limitadas. Alternativas cercanas incluyen estacionamientos en Botafogo, como Botafogo Praia Shopping, Shopping Rio Sul y Casa & Gourmet. Desde allí, evalúa caminar o seguir en taxi/Uber según clima, equipaje y tiempo."),
                ("🚲 En bicicleta", "La zona de Praia Vermelha suele tener estaciones de bicicletas compartidas y es agradable para llegar pedaleando. El parque no debe considerarse bicicletario interno; lleva candado y usa lugares apropiados fuera del área de acceso."),
                ("🚶 Caminando desde Botafogo", "Desde Shopping Rio Sul o Casa & Gourmet, algunas personas optan por caminar hasta Praia Vermelha. Es una caminata urbana corta a moderada, pero conviene considerar calor, lluvia, equipaje y tiempo disponible."),
            ]),
            ("3. Después de llegar", [
                ("🍽️ Reserva y planifica el horario", "Después de llegar al Morro da Urca, encontrarás Embaixada Carioca en el área de la primera parada del Bondinho. Para desayuno, almuerzo, caipirinhas o eventos, reserva con anticipación cuando sea posible."),
                ("🌅 El atardecer sigue disponible", "La experiencia de atardecer continúa existiendo, pero el menú principal ahora prioriza Cómo llegar porque acceso, entradas, Bondinho, sendero y estacionamiento son dudas decisivas para quienes visitan el Pan de Azúcar."),
            ]),
        ],
        "faq": [
            ("¿Necesito comprar entrada para llegar a Embaixada Carioca?", "Sí, si accedes por el Bondinho del Pan de Azúcar. El restaurante está en el Morro da Urca, dentro del Parque Bondinho. La alternativa gratuita es subir por el sendero del Morro da Urca, por la Pista Cláudio Coutinho."),
            ("¿Dónde compro las entradas del Bondinho?", "Lo recomendado es comprar en el sitio oficial bondinho.com.br o en la boletería del parque, según disponibilidad."),
            ("¿Qué dirección pongo en Uber o GPS?", "Usa Parque Bondinho Pão de Açúcar o Avenida Pasteur, 520 – Urca – Rio de Janeiro – RJ."),
            ("¿Hay estacionamiento en el parque?", "El parque no tiene estacionamiento propio. Las plazas en Urca son limitadas; alternativas incluyen estacionamientos en Botafogo como Botafogo Praia Shopping, Shopping Rio Sul y Casa & Gourmet."),
            ("¿Se puede subir gratis?", "Sí. El sendero del Morro da Urca comienza en la Pista Cláudio Coutinho, junto a Praia Vermelha, y normalmente toma entre 30 y 40 minutos."),
        ],
        "cta_primary": "Reservar mesa",
        "cta_secondary": "Comprar entradas del Bondinho",
        "map_cta": "Abrir ruta en Google Maps",
    },
}


def detect_lang(rel: str, text: str) -> str:
    match = HTML_LANG_RE.search(text)
    if match:
        value = match.group(1).lower()
        if value.startswith("en"):
            return "en"
        if value.startswith("es"):
            return "es"
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt"


def update_anchor(anchor: str, href: str, label: str) -> str:
    if "href=" in anchor:
        anchor = re.sub(r"href=([\"']).*?\1", f'href="{href}"', anchor, count=1, flags=re.IGNORECASE)
    else:
        anchor = anchor.replace("<a", f'<a href="{href}"', 1)
    anchor = re.sub(r">[\s\S]*?</a>", f">{label}</a>", anchor, count=1, flags=re.IGNORECASE)
    return anchor


def update_navs(text: str, rel: str) -> str:
    lang = detect_lang(rel, text)
    href, label = NAV_TARGETS[lang]

    def nav_repl(match: re.Match[str]) -> str:
        nav = match.group(0)
        new_nav = ENTARDECER_ANCHOR_RE.sub(lambda a: update_anchor(a.group(0), href, label), nav)
        if new_nav != nav:
            COUNTERS["nav_updated"] += 1
            REPORT.append(f"NAV: {rel} -> {label}")
        return new_nav

    return NAV_RE.sub(nav_repl, text)


def html_page(data: dict[str, object]) -> str:
    nav = data["nav"]
    base = nav["base"]
    cards = "\n".join(f"<article class='fact'><h3>{html.escape(title)}</h3><p>{html.escape(body)}</p></article>" for title, body in data["quick"])
    section_html = []
    for title, items in data["sections"]:
        rows = "\n".join(f"<div class='route'><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>" for h, p in items)
        section_html.append(f"<section class='block'><div class='wrap'><h2>{html.escape(title)}</h2>{rows}</div></section>")
    faqs = "\n".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in data["faq"])
    faq_schema = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in data["faq"]]
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type":"Restaurant","@id":f"{BASE}/#restaurant","name":"Embaixada Carioca","url":f"{BASE}/","telephone":PHONE,"address":{"@type":"PostalAddress","streetAddress":"Av. Pasteur, 520 — Morro da Urca","addressLocality":"Rio de Janeiro","addressRegion":"RJ","addressCountry":"BR"},"hasMap":MAPS_URL,"acceptsReservations":True},
            {"@type":"WebPage","name":data["title"],"url":f"{BASE}/{data['rel']}","description":data["description"],"inLanguage":data["lang"],"about":["Parque Bondinho Pão de Açúcar","Morro da Urca","Praia Vermelha","Sugarloaf cable car","Urca Hill trail"]},
            {"@type":"FAQPage","mainEntity":faq_schema},
        ]
    }
    return f"""<!doctype html>
<html lang="{html.escape(str(data['lang']))}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(str(data['title']))}</title>
<meta name="description" content="{html.escape(str(data['description']), quote=True)}">
<link rel="canonical" href="{BASE}/{data['rel']}">
<link rel="preload" href="/assets/hero.webp" as="image" type="image/webp">
<link href="/assets/fonts/fonts.css" rel="stylesheet">
<meta property="og:title" content="{html.escape(str(data['title']), quote=True)}">
<meta property="og:description" content="{html.escape(str(data['description']), quote=True)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}/{data['rel']}">
<meta property="og:image" content="{BASE}/assets/hero.webp">
<style>
:root{{--azul:#00405a;--amarelo:#f59b1e;--areia:#f6efde;--cinza:#485156;--branco:#fff}}*{{box-sizing:border-box}}body{{margin:0;background:var(--areia);color:var(--azul);font-family:Catamaran,Verdana,system-ui,sans-serif;line-height:1.55}}a{{color:inherit}}.top{{position:fixed;top:0;left:0;right:0;z-index:10;display:flex;align-items:center;justify-content:space-between;gap:28px;padding:18px 34px;background:rgba(0,42,58,.72);backdrop-filter:blur(14px);color:#fff}}.brand{{font-weight:900;letter-spacing:.14em;text-transform:uppercase;text-decoration:none}}nav{{display:flex;gap:18px;align-items:center;flex-wrap:wrap}}nav a{{text-decoration:none;font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;opacity:.96}}.reserve{{background:var(--amarelo);color:var(--azul);border-radius:999px;padding:11px 18px}}.hero{{min-height:86vh;display:grid;align-items:end;color:#fff;padding:150px 24px 70px;background:linear-gradient(180deg,rgba(0,36,51,.22),rgba(0,36,51,.88)),url('/assets/hero.webp') center/cover}}.wrap{{width:min(1180px,calc(100% - 44px));margin:0 auto}}.eyebrow{{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--amarelo);margin-bottom:18px}}h1{{font-size:clamp(42px,7vw,92px);line-height:.93;margin:0 0 20px;letter-spacing:-.045em}}.lead{{max-width:840px;font-size:clamp(18px,2.2vw,25px);color:rgba(255,255,255,.92)}}.ctas{{display:flex;gap:14px;flex-wrap:wrap;margin-top:28px}}.btn{{display:inline-flex;align-items:center;justify-content:center;border-radius:999px;padding:15px 22px;background:var(--amarelo);color:var(--azul);text-decoration:none;font-weight:900;text-transform:uppercase;letter-spacing:.09em}}.btn.secondary{{background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.75);color:white}}.direct,.block,.faq{{padding:66px 0}}.direct{{background:#fff}}.direct .box{{border-left:6px solid var(--amarelo);padding:26px 30px;background:#f9f5ec;border-radius:22px}}h2{{font-size:clamp(28px,4vw,54px);line-height:1.05;margin:0 0 24px;color:var(--azul)}}.direct p,.route p,.fact p,details p{{font-size:18px;color:var(--cinza);max-width:900px}}.facts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px;margin-top:28px}}.fact,.route,details{{background:#fff;border:1px solid rgba(0,64,90,.12);border-radius:22px;padding:24px;box-shadow:0 12px 40px rgba(0,64,90,.06)}}.route{{margin:16px 0}}.route h3,.fact h3{{font-size:22px;margin:0 0 8px}}.block:nth-child(even){{background:#fff8ea}}details{{margin:14px 0}}summary{{cursor:pointer;font-weight:900;font-size:19px}}.footer{{padding:42px 24px;background:#00384f;color:white;text-align:center}}@media(max-width:850px){{.top{{position:absolute;align-items:flex-start;flex-direction:column;padding:18px 22px}}nav{{gap:10px}}nav a{{font-size:11px}}.hero{{padding-top:230px}}.btn{{width:100%}}.wrap{{width:min(100% - 28px,1180px)}}}}
</style>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script>
</head>
<body>
<header class="top"><a class="brand" href="{base or '/'}">Embaixada Carioca</a><nav aria-label="Main navigation"><a href="{base}/cafe-da-manha.html">{nav['cafe']}</a><a href="{base}/almoco.html">{nav['almoco']}</a><a href="{base}/como-chegar.html">{nav['como']}</a><a href="{base}/eventos.html">{nav['eventos']}</a><a href="{base}/cardapio.html">{nav['cardapio']}</a><a href="{base}/guia-do-rio.html">{nav['guia']}</a><a class="reserve" href="{TAGME}">{data['cta_primary']}</a></nav></header>
<main>
<section class="hero"><div class="wrap"><div class="eyebrow">{html.escape(str(data['eyebrow']))}</div><h1>{html.escape(str(data['h1']))}</h1><p class="lead">{html.escape(str(data['lead']))}</p><div class="ctas"><a class="btn" href="{MAPS_URL}">{html.escape(str(data['map_cta']))}</a><a class="btn secondary" href="{BONDINHO_URL}" rel="noopener">{html.escape(str(data['cta_secondary']))}</a><a class="btn secondary" href="{TAGME}">{html.escape(str(data['cta_primary']))}</a></div></div></section>
<section class="direct"><div class="wrap"><div class="box"><div class="eyebrow">SEO + GEO · Direct answer</div><h2>{html.escape(str(data['direct_title']))}</h2><p>{html.escape(str(data['direct_answer']))}</p><div class="facts">{cards}</div></div></div></section>
{''.join(section_html)}
<section class="faq"><div class="wrap"><div class="eyebrow">FAQ</div><h2>FAQ</h2>{faqs}</div></section>
</main>
<footer class="footer">Embaixada Carioca · Morro da Urca · Parque Bondinho Pão de Açúcar · {html.escape(ADDRESS)}</footer>
</body>
</html>"""


def create_pages() -> None:
    for lang, data in PAGES.items():
        path = ROOT / str(data["rel"])
        path.parent.mkdir(parents=True, exist_ok=True)
        original = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        text = html_page(data)
        if text != original:
            path.write_text(text, encoding="utf-8")
            COUNTERS["pages_created"] += 1
            REPORT.append(f"PAGE: {data['rel']}")


def update_existing_navs() -> None:
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts or path.relative_to(ROOT).as_posix().startswith("_"):
            continue
        rel = path.relative_to(ROOT).as_posix()
        COUNTERS["html_scanned"] += 1
        original = path.read_text(encoding="utf-8", errors="ignore")
        text = update_navs(original, rel)
        if text != original:
            path.write_text(text, encoding="utf-8")


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text
    locs = {str(data["rel"]): f"{BASE}/{data['rel']}" for data in PAGES.values()}
    entries = []
    for lang, data in PAGES.items():
        loc = f"{BASE}/{data['rel']}"
        if loc in text:
            continue
        if lang == "pt":
            hreflang = """
    <xhtml:link rel="alternate" hreflang="pt-BR" href="https://www.embaixadacarioca.com/como-chegar.html"/>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.embaixadacarioca.com/en/how-to-get-there.html"/>
    <xhtml:link rel="alternate" hreflang="es" href="https://www.embaixadacarioca.com/es/como-llegar.html"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://www.embaixadacarioca.com/como-chegar.html"/>"""
        else:
            hreflang = ""
        entries.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.92</priority>{hreflang}\n  </url>")
    if entries:
        text = SITEMAP_URLSET_END_RE.sub("\n" + "\n".join(entries) + "\n</urlset>", text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["sitemap_updated"] += 1
        REPORT.append("SITEMAP: como chegar PT/EN/ES adicionado")


def write_report() -> None:
    out = ROOT / "_audit_reports"
    out.mkdir(exist_ok=True)
    report = out / "sprint3_como_chegar_access_cluster_report.md"
    lines = [
        "# Sprint 3 — Como Chegar / Access Cluster",
        "",
        "## Objetivo",
        "Trocar o destaque do menu principal de Entardecer para Como Chegar e criar páginas PT/EN/ES para capturar buscas sobre Bondinho, ingressos, tickets, acesso ao Pão de Açúcar, teleférico, Morro da Urca, trilha, transporte e estacionamento.",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Ações"])
    lines.extend(f"- {x}" for x in REPORT) if REPORT else lines.append("- Nenhuma ação necessária.")
    lines.append("")
    report.write_text("\n".join(lines), encoding="utf-8")
    print(report.read_text(encoding="utf-8"))


def main() -> int:
    create_pages()
    update_existing_navs()
    update_sitemap()
    write_report()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
