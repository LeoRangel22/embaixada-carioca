#!/usr/bin/env python3
"""
Sprint 3 Design Consistency Gate — Embaixada Carioca

Objetivo:
- corrigir bugs de links criados no Sprint 3;
- garantir que as páginas Como Chegar PT/EN/ES usem o mesmo sistema visual da home;
- manter Entardecer existente, mas retirar o destaque principal do menu;
- reforçar layout em 3 partes: topo/nav, hero com imagem livre, barra/chips/CTAs;
- gerar relatório para auditoria antes de avançar.
"""
from __future__ import annotations

from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.embaixadacarioca.com"
TAGME = "https://go.tagme.com.br/embaixadacarioca"
BONDINHO_URL = "https://bondinho.com.br"
MAPS_URL = "https://www.google.com/maps/search/?api=1&query=Parque+Bondinho+P%C3%A3o+de+A%C3%A7%C3%BAcar+Avenida+Pasteur+520+Urca"
ADDRESS = "Av. Pasteur, 520 – Urca – Rio de Janeiro – RJ"
PHONE = "+5521966837556"
LOGO = "/assets/logo-azul.svg"
HERO = "/assets/hero.webp"

REPORT: list[str] = []
COUNTERS = {
    "html_scanned": 0,
    "broken_links_fixed": 0,
    "pages_rebuilt": 0,
    "drawer_fixed": 0,
    "warnings": 0,
}

BROKEN_LINK_REPAIRS = {
    'href="/en/como-chegar.html"': 'href="/en/how-to-get-there.html"',
    "href='/en/como-chegar.html'": "href='/en/how-to-get-there.html'",
    'href="/es/como-chegar.html"': 'href="/es/como-llegar.html"',
    "href='/es/como-chegar.html'": "href='/es/como-llegar.html'",
}

DRAWER_REPAIRS = {
    '<li><a href="/como-chegar.html">COMO CHEGAR</a></li>': '<li><a href="/como-chegar.html"><span class="drawer-icon">📍</span>Como Chegar</a></li>',
    '<li><a href="/en/how-to-get-there.html">HOW TO GET THERE</a></li>': '<li><a href="/en/how-to-get-there.html"><span class="drawer-icon">📍</span>How to Get There</a></li>',
    '<li><a href="/es/como-llegar.html">CÓMO LLEGAR</a></li>': '<li><a href="/es/como-llegar.html"><span class="drawer-icon">📍</span>Cómo Llegar</a></li>',
}

DATA = {
    "pt": {
        "rel": "como-chegar.html",
        "lang": "pt-BR",
        "body_label": "Como Chegar",
        "title": "Como Chegar ao Pão de Açúcar e Morro da Urca | Embaixada Carioca",
        "description": "Como chegar à Embaixada Carioca no Morro da Urca: Bondinho, ingresso, trilha, metrô, ônibus, Uber, carro, estacionamento e bicicleta.",
        "nav": [
            ("/cafe-da-manha.html", "CAFÉ DA MANHÃ"),
            ("/almoco.html", "ALMOÇO"),
            ("/como-chegar.html", "COMO CHEGAR"),
            ("/eventos.html", "EVENTOS"),
            ("/cardapio.html", "CARDÁPIO"),
            ("/guia-do-rio.html", "GUIA DO RIO"),
        ],
        "lang_label": "BR PT",
        "eyebrow": "Restaurante do Bondinho · Morro da Urca · Parque Bondinho Pão de Açúcar · Rio de Janeiro · Brasil",
        "h1": "Como chegar à Embaixada Carioca no Morro da Urca",
        "lede": "Estamos no Morro da Urca, a primeira parada do Parque Bondinho Pão de Açúcar. O acesso é pela Praia Vermelha, na Avenida Pasteur, 520, Urca.",
        "chips": ["Primeira parada do Bondinho", "Ingressos no bondinho.com.br", "Trilha gratuita pela Pista Cláudio Coutinho", "Uber, metrô, ônibus, carro e bicicleta"],
        "cta_map": "COMO CHEGAR",
        "cta_ticket": "INGRESSOS DO BONDINHO",
        "cta_reserve": "RESERVAR MESA",
        "direct_kicker": "Resposta direta · SEO + GEO",
        "direct_title": "Como acessar o restaurante no Morro da Urca?",
        "direct_answer": "Para chegar à Embaixada Carioca, vá até a Praia Vermelha, na Urca, e acesse o Morro da Urca de Bondinho ou pela trilha. Pelo Bondinho, é necessário adquirir ingresso do Parque Bondinho Pão de Açúcar. Pela trilha, o acesso gratuito começa na Pista Cláudio Coutinho, ao lado da Praia Vermelha.",
        "quick": [
            ("📍 Localização", "Morro da Urca, primeira parada do Bondinho do Pão de Açúcar."),
            ("🗺️ Endereço", ADDRESS),
            ("🚠 Acesso principal", "Bondinho do Pão de Açúcar, com ingresso do parque."),
            ("🥾 Acesso alternativo", "Trilha do Morro da Urca pela Pista Cláudio Coutinho, cerca de 30 a 40 minutos."),
        ],
        "sections": [
            ("1. Como acessar o Morro da Urca", [
                ("🚠 De Bondinho — acesso mais popular", "A forma mais tradicional, rápida e turística é subir pelo Bondinho do Pão de Açúcar. O primeiro trecho liga a Praia Vermelha ao Morro da Urca, onde fica a Embaixada Carioca. Para acessar o restaurante por esse caminho, é necessário adquirir o ingresso do Parque Bondinho. Recomendamos a compra antecipada pelo site oficial bondinho.com.br."),
                ("🥾 Pela trilha — acesso gratuito e aventureiro", "A trilha do Morro da Urca começa na Pista Cláudio Coutinho, com entrada pela Praia Vermelha. A caminhada leva cerca de 30 a 40 minutos, dependendo do ritmo, e é uma opção gratuita para quem gosta de natureza. Vá com calçado confortável, água e atenção ao horário da área natural."),
            ]),
            ("2. Como chegar até a Urca e a Praia Vermelha", [
                ("🚕 Táxi, Uber ou 99", "É a forma mais prática. No aplicativo, use Parque Bondinho Pão de Açúcar ou Avenida Pasteur, 520. O carro deixa você próximo à bilheteria e à entrada do parque."),
                ("🚇 Metrô + ônibus ou app", "A estação de metrô mais usada é Botafogo. De lá, siga de táxi, Uber/99 ou ônibus até a Urca/Praia Vermelha. A linha 513 costuma ser usada na conexão Botafogo–Urca, mas confirme a rota em tempo real no app antes de sair."),
                ("🚌 Ônibus para a Urca", "Linhas comumente consultadas para Urca/Praia Vermelha incluem 107, 167, 513, 518 e 519. Como rotas e horários podem mudar, confirme no aplicativo de transporte no dia da visita."),
                ("🚗 De carro e estacionamento", "O Parque Bondinho não possui estacionamento próprio e as vagas na Urca são limitadas. Alternativas próximas ficam em Botafogo, como Botafogo Praia Shopping, Shopping Rio Sul e Casa & Gourmet. A partir deles, avalie seguir a pé ou de táxi/Uber conforme disposição, temperatura e tempo disponível."),
                ("🚲 Bicicleta e aluguel", "A região da Praia Vermelha costuma ter estações de bicicletas compartilhadas e acesso agradável por ciclovia. O parque não deve ser tratado como bicicletário interno; leve cadeado e use locais apropriados fora da área de acesso."),
                ("🚶 Caminhando de Botafogo", "De pontos como Shopping Rio Sul ou Casa & Gourmet, algumas pessoas caminham até a Praia Vermelha. É uma caminhada urbana curta a moderada, mas deve ser avaliada conforme calor, chuva, bagagem e tempo disponível."),
            ]),
        ],
        "faq_title": "Perguntas frequentes sobre acesso, ingresso e chegada",
        "faq": [
            ("Precisa comprar ingresso para chegar à Embaixada Carioca?", "Sim, se você acessar pelo Bondinho do Pão de Açúcar. A alternativa gratuita é subir pela trilha do Morro da Urca, pela Pista Cláudio Coutinho."),
            ("Onde compro o ticket do Bondinho?", "O recomendado é comprar pelo site oficial bondinho.com.br ou pela bilheteria do parque, conforme disponibilidade."),
            ("Qual endereço devo colocar no Uber ou GPS?", "Use Parque Bondinho Pão de Açúcar ou Avenida Pasteur, 520 – Urca – Rio de Janeiro – RJ."),
            ("Tem estacionamento no Parque Bondinho?", "Não há estacionamento próprio do parque. As vagas na Urca são limitadas; alternativas incluem Botafogo Praia Shopping, Shopping Rio Sul e Casa & Gourmet."),
        ],
        "footer": "Embaixada Carioca · Morro da Urca · Parque Bondinho Pão de Açúcar",
    },
    "en": {
        "rel": "en/how-to-get-there.html",
        "lang": "en",
        "body_label": "How to Get There",
        "title": "How to Get to Sugarloaf Cable Car Park and Urca Hill | Embaixada Carioca",
        "description": "How to get to Embaixada Carioca at Urca Hill: Sugarloaf cable car tickets, trail, metro, bus, Uber, car, parking and bike options.",
        "nav": [("/en/cafe-da-manha.html", "BREAKFAST"), ("/en/almoco.html", "LUNCH"), ("/en/how-to-get-there.html", "HOW TO GET THERE"), ("/en/eventos.html", "EVENTS"), ("/en/cardapio.html", "MENU"), ("/en/guia-do-rio.html", "RIO GUIDE")],
        "lang_label": "EN",
        "eyebrow": "Restaurant at the Cable Car · Urca Hill · Sugarloaf Cable Car Park · Rio de Janeiro · Brazil",
        "h1": "How to get to Embaixada Carioca at Urca Hill",
        "lede": "We are located at Urca Hill, the first stop of Sugarloaf Cable Car Park. Access starts at Praia Vermelha, Avenida Pasteur, 520, Urca.",
        "chips": ["First cable car stop", "Tickets at bondinho.com.br", "Free trail from Pista Cláudio Coutinho", "Uber, metro, bus, car and bike"],
        "cta_map": "HOW TO GET THERE",
        "cta_ticket": "CABLE CAR TICKETS",
        "cta_reserve": "RESERVE A TABLE",
        "direct_kicker": "Direct answer · SEO + GEO",
        "direct_title": "How do I access the restaurant at Urca Hill?",
        "direct_answer": "To reach Embaixada Carioca, go to Praia Vermelha in Urca and access Urca Hill by the Sugarloaf cable car or by the trail. By cable car, visitors need a Sugarloaf Cable Car Park ticket. The free trail starts at Pista Cláudio Coutinho, next to Praia Vermelha.",
        "quick": [("📍 Location", "Urca Hill, first stop of the Sugarloaf cable car."), ("🗺️ Address", ADDRESS), ("🚠 Main access", "Sugarloaf cable car, with park ticket."), ("🥾 Free option", "Urca Hill trail from Pista Cláudio Coutinho, around 30 to 40 minutes.")],
        "sections": [("1. How to access Urca Hill", [("🚠 By cable car — the most popular access", "The classic and fastest way is to take the Sugarloaf cable car. The first ride connects Praia Vermelha to Urca Hill, where Embaixada Carioca is located. Visitors need a Sugarloaf Cable Car Park ticket; we recommend buying it in advance through the official Bondinho website."), ("🥾 By trail — free and adventurous", "The Urca Hill trail starts at Pista Cláudio Coutinho, with access from Praia Vermelha. The walk usually takes around 30 to 40 minutes. Wear comfortable shoes, bring water and check local opening times for the natural area.")]), ("2. How to get to Urca and Praia Vermelha", [("🚕 Taxi, Uber or 99", "Use Parque Bondinho Pão de Açúcar or Avenida Pasteur, 520 as the destination. The car can drop you near the ticket office and park entrance."), ("🚇 Metro + bus or ride app", "Botafogo is the closest metro station commonly used by visitors. From there, continue by taxi, Uber/99 or bus to Urca/Praia Vermelha. Route 513 is often used, but check real-time routing before leaving."), ("🚌 Bus to Urca", "Bus lines commonly checked for Urca/Praia Vermelha include 107, 167, 513, 518 and 519. Routes and schedules may change, so confirm in a transport app on the day of your visit."), ("🚗 By car and parking", "Sugarloaf Cable Car Park does not have its own parking lot and public parking in Urca is limited. Nearby alternatives include Botafogo Praia Shopping, Shopping Rio Sul and Casa & Gourmet. From there, choose walking or a ride app depending on weather, luggage and time."), ("🚲 By bike", "Praia Vermelha often has shared-bike stations nearby and the area is pleasant for cycling. Bring a lock and use appropriate spots outside the access area."), ("🚶 Walking from Botafogo", "From Shopping Rio Sul or Casa & Gourmet, some visitors walk to Praia Vermelha. Consider heat, rain, luggage and available time.")])],
        "faq_title": "FAQ about access, tickets and arrival",
        "faq": [("Do I need a ticket to reach Embaixada Carioca?", "Yes, if you access it by the Sugarloaf cable car. The free alternative is the Urca Hill trail via Pista Cláudio Coutinho."), ("Where do I buy Sugarloaf cable car tickets?", "We recommend buying tickets through the official website bondinho.com.br or at the park ticket office, depending on availability."), ("What should I type in Uber or GPS?", "Use Parque Bondinho Pão de Açúcar or Avenida Pasteur, 520 – Urca – Rio de Janeiro – RJ."), ("Is there parking at the park?", "The park does not have its own parking lot. Street parking in Urca is limited; alternatives include parking in Botafogo at Botafogo Praia Shopping, Shopping Rio Sul and Casa & Gourmet.")],
        "footer": "Embaixada Carioca · Urca Hill · Sugarloaf Cable Car Park",
    },
    "es": {
        "rel": "es/como-llegar.html",
        "lang": "es",
        "body_label": "Cómo Llegar",
        "title": "Cómo Llegar al Pan de Azúcar y Morro da Urca | Embaixada Carioca",
        "description": "Cómo llegar a Embaixada Carioca en el Morro da Urca: entradas del Bondinho, sendero, metro, autobús, Uber, coche, estacionamiento y bici.",
        "nav": [("/es/cafe-da-manha.html", "DESAYUNO"), ("/es/almoco.html", "ALMUERZO"), ("/es/como-llegar.html", "CÓMO LLEGAR"), ("/es/eventos.html", "EVENTOS"), ("/es/cardapio.html", "MENÚ"), ("/es/guia-do-rio.html", "GUÍA DE RÍO")],
        "lang_label": "ES",
        "eyebrow": "Restaurante del Bondinho · Morro da Urca · Parque Bondinho Pan de Azúcar · Río de Janeiro · Brasil",
        "h1": "Cómo llegar a Embaixada Carioca en el Morro da Urca",
        "lede": "Estamos en el Morro da Urca, la primera parada del Parque Bondinho Pan de Azúcar. El acceso comienza en Praia Vermelha, Avenida Pasteur, 520, Urca.",
        "chips": ["Primera parada del Bondinho", "Entradas en bondinho.com.br", "Sendero gratuito por la Pista Cláudio Coutinho", "Uber, metro, autobús, coche y bicicleta"],
        "cta_map": "CÓMO LLEGAR",
        "cta_ticket": "ENTRADAS DEL BONDINHO",
        "cta_reserve": "RESERVAR MESA",
        "direct_kicker": "Respuesta directa · SEO + GEO",
        "direct_title": "¿Cómo acceder al restaurante en el Morro da Urca?",
        "direct_answer": "Para llegar a Embaixada Carioca, ve hasta Praia Vermelha, en Urca, y accede al Morro da Urca en Bondinho o por el sendero. En Bondinho, es necesario comprar entrada del Parque Bondinho Pan de Azúcar. El sendero gratuito comienza en la Pista Cláudio Coutinho, junto a Praia Vermelha.",
        "quick": [("📍 Ubicación", "Morro da Urca, primera parada del Bondinho del Pan de Azúcar."), ("🗺️ Dirección", ADDRESS), ("🚠 Acceso principal", "Bondinho del Pan de Azúcar, con entrada del parque."), ("🥾 Opción gratuita", "Sendero del Morro da Urca por la Pista Cláudio Coutinho, normalmente 30 a 40 minutos.")],
        "sections": [("1. Cómo acceder al Morro da Urca", [("🚠 En Bondinho — acceso más popular", "La forma más tradicional y rápida es subir en el Bondinho del Pan de Azúcar. El primer tramo conecta Praia Vermelha con el Morro da Urca, donde está Embaixada Carioca. Es necesario comprar la entrada del Parque Bondinho; recomendamos hacerlo con anticipación en el sitio oficial."), ("🥾 Por el sendero — acceso gratuito y aventurero", "El sendero del Morro da Urca comienza en la Pista Cláudio Coutinho, con entrada por Praia Vermelha. La caminata suele durar entre 30 y 40 minutos. Usa calzado cómodo, lleva agua y verifica los horarios del área natural.")]), ("2. Cómo llegar a Urca y Praia Vermelha", [("🚕 Taxi, Uber o 99", "Usa Parque Bondinho Pão de Açúcar o Avenida Pasteur, 520 como destino. El coche te deja cerca de la boletería y la entrada del parque."), ("🚇 Metro + autobús o app", "La estación de metro más utilizada es Botafogo. Desde allí, sigue en taxi, Uber/99 o autobús hasta Urca/Praia Vermelha. La línea 513 suele usarse, pero confirma la ruta en tiempo real antes de salir."), ("🚌 Autobús a Urca", "Líneas comúnmente consultadas para Urca/Praia Vermelha incluyen 107, 167, 513, 518 y 519. Como rutas y horarios pueden cambiar, confirma en una aplicación de transporte el día de la visita."), ("🚗 En coche y estacionamiento", "El Parque Bondinho no tiene estacionamiento propio y las plazas en Urca son limitadas. Alternativas cercanas incluyen Botafogo Praia Shopping, Shopping Rio Sul y Casa & Gourmet. Desde allí, evalúa caminar o seguir en taxi/Uber según clima, equipaje y tiempo."), ("🚲 En bicicleta", "La zona de Praia Vermelha suele tener estaciones de bicicletas compartidas y es agradable para llegar pedaleando. Lleva candado y usa lugares apropiados fuera del área de acceso."), ("🚶 Caminando desde Botafogo", "Desde Shopping Rio Sul o Casa & Gourmet, algunas personas caminan hasta Praia Vermelha. Considera calor, lluvia, equipaje y tiempo disponible.")])],
        "faq_title": "FAQ sobre acceso, entradas y llegada",
        "faq": [("¿Necesito comprar entrada para llegar a Embaixada Carioca?", "Sí, si accedes por el Bondinho del Pan de Azúcar. La alternativa gratuita es subir por el sendero del Morro da Urca, por la Pista Cláudio Coutinho."), ("¿Dónde compro las entradas del Bondinho?", "Lo recomendado es comprar en el sitio oficial bondinho.com.br o en la boletería del parque, según disponibilidad."), ("¿Qué dirección pongo en Uber o GPS?", "Usa Parque Bondinho Pão de Açúcar o Avenida Pasteur, 520 – Urca – Rio de Janeiro – RJ."), ("¿Hay estacionamiento en el parque?", "El parque no tiene estacionamiento propio. Las plazas en Urca son limitadas; alternativas incluyen Botafogo Praia Shopping, Shopping Rio Sul y Casa & Gourmet.")],
        "footer": "Embaixada Carioca · Morro da Urca · Parque Bondinho Pan de Azúcar",
    },
}


def nav_markup(items: list[tuple[str, str]]) -> str:
    return "\n".join(f'<li><a href="{href}">{html.escape(label)}</a></li>' for href, label in items)


def jsonld(data: dict[str, object]) -> str:
    faq = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in data["faq"]]
    graph = [
        {"@type": "Restaurant", "@id": f"{BASE}/#restaurant", "name": "Embaixada Carioca", "url": BASE + "/", "telephone": PHONE, "address": {"@type": "PostalAddress", "streetAddress": "Av. Pasteur, 520 — Morro da Urca", "addressLocality": "Rio de Janeiro", "addressRegion": "RJ", "addressCountry": "BR"}, "hasMap": MAPS_URL, "acceptsReservations": True},
        {"@type": "WebPage", "name": data["title"], "url": f"{BASE}/{data['rel']}", "description": data["description"], "inLanguage": data["lang"], "about": ["Parque Bondinho Pão de Açúcar", "Morro da Urca", "Praia Vermelha", "Sugarloaf cable car", "Urca Hill trail"]},
        {"@type": "FAQPage", "mainEntity": faq},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def page_html(data: dict[str, object]) -> str:
    chips = "".join(f"<span>{html.escape(c)}</span>" for c in data["chips"])
    quick = "".join(f"<article class=\"access-fact\"><h3>{html.escape(t)}</h3><p>{html.escape(b)}</p></article>" for t, b in data["quick"])
    sections = []
    for title, items in data["sections"]:
        rows = "".join(f"<article class=\"access-route\"><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></article>" for h, p in items)
        sections.append(f"<section class=\"access-section\"><div class=\"wrap\"><h2>{html.escape(title)}</h2><div class=\"route-grid\">{rows}</div></div></section>")
    faq = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in data["faq"])
    return f"""<!doctype html>
<html lang=\"{html.escape(str(data['lang']))}\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">
<title>{html.escape(str(data['title']))}</title>
<meta name=\"description\" content=\"{html.escape(str(data['description']), quote=True)}\">
<link rel=\"canonical\" href=\"{BASE}/{data['rel']}\">
<link rel=\"alternate\" hreflang=\"pt-BR\" href=\"{BASE}/como-chegar.html\">
<link rel=\"alternate\" hreflang=\"en\" href=\"{BASE}/en/how-to-get-there.html\">
<link rel=\"alternate\" hreflang=\"es\" href=\"{BASE}/es/como-llegar.html\">
<link rel=\"alternate\" hreflang=\"x-default\" href=\"{BASE}/como-chegar.html\">
<link rel=\"preload\" href=\"{HERO}\" as=\"image\" type=\"image/webp\">
<link href=\"/assets/fonts/fonts.css\" rel=\"stylesheet\">
<meta property=\"og:title\" content=\"{html.escape(str(data['title']), quote=True)}\">
<meta property=\"og:description\" content=\"{html.escape(str(data['description']), quote=True)}\">
<meta property=\"og:type\" content=\"website\">
<meta property=\"og:url\" content=\"{BASE}/{data['rel']}\">
<meta property=\"og:image\" content=\"{BASE}{HERO}\">
<script type=\"application/ld+json\">{jsonld(data)}</script>
<style id=\"sprint3-access-page-base\">
html,body{{margin:0;padding:0;background:#f6efde;color:#00405a;font-family:Catamaran,Verdana,system-ui,sans-serif;overflow-x:hidden}}*{{box-sizing:border-box}}a{{color:inherit}}.wrap{{width:min(1180px,calc(100% - 44px));margin:0 auto}}.top{{position:fixed;inset:0 0 auto 0;z-index:50;color:#f6efde}}.nav-inner{{width:100%;height:112px;display:grid;grid-template-columns:140px minmax(0,1fr) 205px 94px 188px;gap:26px;align-items:center;padding:10px 70px 0;background:linear-gradient(180deg,rgba(0,32,46,.40),rgba(0,32,46,.08),rgba(0,32,46,0))}}.brand-mark{{display:flex;align-items:center;text-decoration:none}}.brand-logo{{width:68px;height:68px;object-fit:contain}}.brand-word{{display:none}}.nav-links{{list-style:none;display:flex;align-items:center;gap:30px;margin:0;padding:0;overflow:hidden}}.nav-links a,.btn{{font-family:'JetBrains Mono',ui-monospace,monospace;text-transform:uppercase;text-decoration:none;font-weight:900;letter-spacing:.14em;white-space:nowrap}}.nav-links a{{font-size:12px;color:rgba(246,239,222,.94)}}.nav-rating-badge{{height:35px;border-radius:999px;background:rgba(246,239,222,.14);border:1px solid rgba(246,239,222,.30);display:flex;align-items:center;justify-content:center;gap:7px;text-decoration:none}}.nav-rating-stars{{color:#f59b1e;font-weight:900}}.nav-rating-count{{font-size:11px;color:rgba(246,239,222,.78);font-weight:800;letter-spacing:.08em}}.lang-current{{height:36px;border-radius:12px;background:rgba(246,239,222,.14);border:1px solid rgba(246,239,222,.30);display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:900}}.top .btn{{height:60px;border-radius:999px;background:#f59b1e;color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px}}.page-hero{{height:100svh;min-height:100svh;position:relative;overflow:hidden;isolation:isolate;background:#00202e}}.page-hero-photo,.page-hero-photo img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 44%;z-index:-2}}.page-hero-overlay{{position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(0,32,46,.08),rgba(0,32,46,.12) 36%,rgba(0,32,46,.40) 58%,rgba(0,32,46,.84)),linear-gradient(180deg,rgba(0,32,46,.10),rgba(0,32,46,.20) 45%,rgba(0,32,46,.80))}}.page-hero-content{{position:absolute;inset:0}}.hero-eyebrow{{position:absolute;left:clamp(185px,11.8vw,215px);top:118px;width:calc(100vw - 520px);white-space:nowrap;overflow:hidden;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.31em;text-transform:uppercase;color:#f59b1e;text-shadow:0 2px 12px rgba(0,32,46,.66)}}.page-hero h1{{position:absolute;right:clamp(66px,5.5vw,126px);top:clamp(160px,22vh,260px);max-width:min(610px,39vw);font-size:clamp(38px,4.35vw,70px);line-height:.98;font-weight:250;letter-spacing:-.026em;color:#f6efde;margin:0}}.lede{{position:absolute;right:clamp(66px,5.5vw,126px);top:clamp(430px,57vh,620px);max-width:min(610px,40vw);font-size:clamp(15px,1vw,18px);line-height:1.55;color:rgba(246,239,222,.95);text-shadow:0 2px 16px rgba(0,32,46,.55);margin:0}}.hero-chips{{position:absolute;left:clamp(70px,5.5vw,118px);bottom:clamp(138px,15vh,178px);max-width:min(760px,56vw);display:flex;gap:8px;flex-wrap:wrap}}.hero-chips span{{font-size:.82rem;padding:5px 13px;background:rgba(0,32,46,.42);border:1px solid rgba(246,239,222,.28);color:#f6efde;border-radius:999px}}.hero-ctas{{position:absolute;left:clamp(70px,5.5vw,118px);bottom:clamp(58px,7.2vh,88px);display:flex;gap:12px;flex-wrap:wrap}}.hero-ctas a{{border-radius:999px;padding:15px 28px;text-decoration:none;font-family:'JetBrains Mono',monospace;font-weight:900;letter-spacing:.12em;text-transform:uppercase;background:#f59b1e;color:#00405a}}.hero-ctas a.secondary{{background:rgba(0,32,46,.38);border:1px solid rgba(246,239,222,.65);color:#f6efde}}.access-direct,.access-section,.access-faq{{padding:72px 0;background:#f6efde}}.access-section:nth-child(even){{background:#fff8ea}}.box{{background:#fff;border:1px solid rgba(0,64,90,.12);border-radius:24px;padding:34px;box-shadow:0 18px 55px rgba(0,64,90,.08)}}.kicker{{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#527f8f;margin-bottom:12px}}h2{{font-size:clamp(30px,4vw,54px);line-height:1.05;margin:0 0 20px}}.box p,.access-route p,.access-fact p,details p{{font-size:18px;color:#485156;line-height:1.6}}.facts,.route-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px;margin-top:24px}}.access-fact,.access-route,details{{background:#fff;border:1px solid rgba(0,64,90,.12);border-radius:20px;padding:24px}}.access-route h3,.access-fact h3{{font-size:22px;margin:0 0 8px}}details{{margin:14px 0}}summary{{cursor:pointer;font-weight:900;font-size:19px}}.footer{{padding:42px 24px;background:#00384f;color:#fff;text-align:center}}@media(max-width:1180px) and (min-width:961px){{.nav-inner{{padding-left:18px;padding-right:18px;grid-template-columns:68px minmax(0,1fr) 132px 62px 124px;gap:8px}}.brand-logo{{width:54px;height:54px}}.nav-links{{gap:8px}}.nav-links a{{font-size:7.6px;letter-spacing:.035em}}.nav-rating-badge{{width:132px}}.nav-rating-stars{{font-size:11px}}.nav-rating-count{{font-size:7.6px}}.lang-current{{font-size:9px}}.top .btn{{height:46px;font-size:9.3px;letter-spacing:.07em}}.page-hero h1,.lede{{display:none}}}}@media(max-width:960px){{.top{{position:absolute;background:rgba(0,32,46,.88)}}.nav-inner{{height:auto;display:flex;flex-wrap:wrap;padding:14px 18px;gap:12px}}.brand-logo{{width:58px;height:58px}}.nav-links{{width:100%;gap:12px;flex-wrap:wrap}}.nav-links a{{font-size:10px}}.nav-rating-badge,.lang-current{{height:32px;padding:0 12px}}.top .btn{{height:42px;padding:0 18px}}.page-hero{{height:auto;min-height:760px}}.hero-eyebrow{{left:24px;right:24px;top:150px;width:auto;font-size:8px;letter-spacing:.17em}}.page-hero h1{{left:24px;right:24px;top:210px;max-width:none;font-size:44px}}.lede{{left:24px;right:24px;top:410px;max-width:none;font-size:17px}}.hero-chips{{left:24px;right:24px;bottom:170px;max-width:none}}.hero-ctas{{left:24px;right:24px;bottom:38px}}.hero-ctas a{{width:100%;text-align:center;justify-content:center}}.wrap{{width:calc(100% - 28px)}}}}
</style>
</head>
<body data-screen-label=\"{html.escape(str(data['body_label']))}\">
<nav class=\"top\" aria-label=\"Main navigation\"><div class=\"nav-inner\"><a class=\"brand-mark\" href=\"/\"><img class=\"brand-logo light\" src=\"{LOGO}\" alt=\"Embaixada Carioca\"><span class=\"brand-word\">Embaixada Carioca</span></a><ul class=\"nav-links\">{nav_markup(data['nav'])}</ul><a class=\"nav-rating-badge\" href=\"https://www.google.com/search?q=Embaixada+Carioca+reviews\"><span class=\"nav-rating-stars\">4.8★</span><span class=\"nav-rating-count\">7.779 avaliações</span></a><div class=\"lang-switcher\"><div class=\"lang-current\"><span>{html.escape(str(data['lang_label']))}</span></div></div><a class=\"btn\" href=\"{TAGME}\">RESERVAR →</a></div></nav>
<header class=\"page-hero\"><picture class=\"page-hero-photo\"><img src=\"{HERO}\" alt=\"Pão de Açúcar visto do Morro da Urca\" width=\"1920\" height=\"1280\"></picture><div class=\"page-hero-overlay\"></div><div class=\"page-hero-content\"><div class=\"eyebrow hero-eyebrow\">{html.escape(str(data['eyebrow']))}</div><h1>{html.escape(str(data['h1']))}</h1><p class=\"lede\">{html.escape(str(data['lede']))}</p><div class=\"hero-chips\">{chips}</div><div class=\"hero-ctas\"><a href=\"{MAPS_URL}\">{html.escape(str(data['cta_map']))}</a><a class=\"secondary\" href=\"{BONDINHO_URL}\">{html.escape(str(data['cta_ticket']))}</a><a class=\"secondary\" href=\"{TAGME}\">{html.escape(str(data['cta_reserve']))}</a></div></div></header>
<main><section class=\"access-direct\"><div class=\"wrap\"><div class=\"box\"><div class=\"kicker\">{html.escape(str(data['direct_kicker']))}</div><h2>{html.escape(str(data['direct_title']))}</h2><p>{html.escape(str(data['direct_answer']))}</p><div class=\"facts\">{quick}</div></div></div></section>{''.join(sections)}<section class=\"access-faq\"><div class=\"wrap\"><div class=\"kicker\">FAQ</div><h2>{html.escape(str(data['faq_title']))}</h2>{faq}</div></section></main><footer class=\"footer\">{html.escape(str(data['footer']))} · {html.escape(ADDRESS)}</footer>
</body>
</html>"""


def rebuild_pages() -> None:
    for data in DATA.values():
        path = ROOT / str(data["rel"])
        path.parent.mkdir(parents=True, exist_ok=True)
        original = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        text = page_html(data)
        if text != original:
            path.write_text(text, encoding="utf-8")
            COUNTERS["pages_rebuilt"] += 1
            REPORT.append(f"REBUILT: {data['rel']}")


def fix_links_everywhere() -> None:
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts or path.relative_to(ROOT).as_posix().startswith("_"):
            continue
        COUNTERS["html_scanned"] += 1
        original = path.read_text(encoding="utf-8", errors="ignore")
        text = original
        for old, new in BROKEN_LINK_REPAIRS.items():
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                COUNTERS["broken_links_fixed"] += count
                REPORT.append(f"LINK: {path.relative_to(ROOT).as_posix()} | {old} -> {new} | {count}")
        for old, new in DRAWER_REPAIRS.items():
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                COUNTERS["drawer_fixed"] += count
                REPORT.append(f"DRAWER: {path.relative_to(ROOT).as_posix()} | {count}")
        if text != original:
            path.write_text(text, encoding="utf-8")


def verify() -> None:
    for rel in ["como-chegar.html", "en/how-to-get-there.html", "es/como-llegar.html"]:
        path = ROOT / rel
        if not path.exists():
            COUNTERS["warnings"] += 1
            REPORT.append(f"WARN: missing {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        required = ["class=\"top\"", "class=\"nav-inner\"", "class=\"page-hero\"", "class=\"page-hero-photo\"", "class=\"hero-chips\"", "class=\"hero-ctas\"", "data-screen-label"]
        for token in required:
            if token not in text:
                COUNTERS["warnings"] += 1
                REPORT.append(f"WARN: {rel} missing {token}")
        if rel.startswith("en/") and "/en/como-chegar.html" in text:
            COUNTERS["warnings"] += 1
            REPORT.append(f"WARN: {rel} still has broken EN como-chegar link")
        if rel.startswith("es/") and "/es/como-chegar.html" in text:
            COUNTERS["warnings"] += 1
            REPORT.append(f"WARN: {rel} still has broken ES como-chegar link")


def write_report() -> None:
    out = ROOT / "_audit_reports"
    out.mkdir(exist_ok=True)
    report = out / "sprint3_design_consistency_gate_report.md"
    lines = ["# Sprint 3 Design Consistency Gate", "", "## Objetivo", "Garantir que Como Chegar PT/EN/ES siga o padrão visual da home e corrigir links quebrados do Sprint 3.", "", "## Contadores"]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Ações"])
    lines.extend(f"- {item}" for item in REPORT) if REPORT else lines.append("- Nenhuma ação necessária.")
    lines.append("")
    report.write_text("\n".join(lines), encoding="utf-8")
    print(report.read_text(encoding="utf-8"))


def main() -> int:
    fix_links_everywhere()
    rebuild_pages()
    verify()
    write_report()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
