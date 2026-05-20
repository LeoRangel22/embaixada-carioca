#!/usr/bin/env python3
"""
Sprint 4 — R2D2 + AIO/SAI + Conversion Hardening | Embaixada Carioca

Usa os relatórios recentes como backlog de correção:
- thin content em páginas EN/ES de captação;
- FAQs curtas/ausentes em produto e eventos;
- ausência de listas ordenadas para snippets;
- sitemap incompleto;
- links âncora quebrados;
- telefone/coordinates inconsistentes;
- botão Reservar do topo com seta/largura/efeito fora do padrão.

Rodar no final dos ajustes visuais, antes da auditoria estrutural final.
"""
from __future__ import annotations

from pathlib import Path
import html
import json
import re
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.embaixadacarioca.com"
TAGME = "https://go.tagme.com.br/embaixadacarioca"
PHONE_DISPLAY = "+55 21 96683-7556"
PHONE_COMPACT = "+5521966837556"
LAT = "-22.9508333"
LON = "-43.1641667"
TODAY = date.today().isoformat()

REPORT: list[str] = []
WARNINGS: list[str] = []
COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "coordinates_fixed": 0,
    "phones_fixed": 0,
    "reserve_buttons_fixed": 0,
    "css_injected": 0,
    "anchors_fixed": 0,
    "r2d2_blocks_added": 0,
    "faq_blocks_added": 0,
    "schema_blocks_added": 0,
    "ordered_lists_added": 0,
    "sitemap_urls_added": 0,
    "warnings": 0,
}

# ---------- CSS / visual ----------
CSS_START = "<!-- EC Sprint 4 R2D2 AIO Conversion CSS -->"
CSS_END = "<!-- /EC Sprint 4 R2D2 AIO Conversion CSS -->"
CSS_RE = re.compile(r"\n*<!-- EC Sprint 4 R2D2 AIO Conversion CSS -->[\s\S]*?<!-- /EC Sprint 4 R2D2 AIO Conversion CSS -->\s*", re.IGNORECASE)
HEAD_CLOSE_RE = re.compile(r"</head>", re.IGNORECASE)
BODY_CLOSE_RE = re.compile(r"</body>", re.IGNORECASE)
MAIN_CLOSE_RE = re.compile(r"</main>", re.IGNORECASE)

CSS_BLOCK = f"""{CSS_START}
<style id="ec-sprint4-r2d2-aio-conversion-css">
/* Topo: botão Reservar com efeito do CTA principal, sem seta e menor */
nav.top .btn,
nav.top .nav-inner > .btn{{
  min-width:148px!important;
  width:auto!important;
  max-width:164px!important;
  justify-content:center!important;
  text-align:center!important;
  padding-left:22px!important;
  padding-right:22px!important;
  gap:0!important;
  box-shadow:0 9px 0 rgba(0,64,90,.22),0 16px 30px rgba(0,32,46,.22)!important;
}}
nav.top .btn::after,
nav.top .nav-inner > .btn::after{{content:none!important;display:none!important}}
@media(max-width:1180px) and (min-width:961px){{
  nav.top .nav-inner{{grid-template-columns:68px minmax(0,1fr) 136px 62px 148px!important}}
  nav.top .btn,nav.top .nav-inner > .btn{{min-width:118px!important;max-width:148px!important;padding-left:14px!important;padding-right:14px!important}}
}}
/* Âncoras: evitam links quebrados e compensam header fixo */
.ec-anchor-target{{display:block;position:relative;top:-118px;visibility:hidden;height:0;width:0;overflow:hidden}}
/* Blocos R2D2/AIO */
.ec-r2d2-depth,.ec-sprint4-faq,.ec-sprint4-steps{{background:#f6efde;color:#00405a;padding:64px 0;border-top:1px solid rgba(0,64,90,.10)}}
.ec-r2d2-depth .wrap,.ec-sprint4-faq .wrap,.ec-sprint4-steps .wrap{{max-width:1120px;margin:0 auto;padding:0 24px}}
.ec-r2d2-depth h2,.ec-sprint4-faq h2,.ec-sprint4-steps h2{{font-size:clamp(30px,3.6vw,50px);line-height:1.05;margin:0 0 20px;color:#00405a}}
.ec-r2d2-depth h3{{font-size:24px;line-height:1.15;margin:28px 0 8px;color:#00405a}}
.ec-r2d2-depth p,.ec-sprint4-faq p,.ec-sprint4-steps li{{font-size:17px;line-height:1.62;color:#485156}}
.ec-r2d2-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin:28px 0}}
.ec-r2d2-card,.ec-sprint4-faq details{{background:#fff;border:1px solid rgba(0,64,90,.12);border-radius:20px;padding:22px}}
.ec-r2d2-card strong{{display:block;color:#00405a;margin-bottom:6px}}
.ec-r2d2-depth table{{width:100%;border-collapse:collapse;margin:28px 0;background:#fff;border-radius:18px;overflow:hidden}}
.ec-r2d2-depth th,.ec-r2d2-depth td{{padding:14px 16px;border-bottom:1px solid rgba(0,64,90,.10);text-align:left;vertical-align:top}}
.ec-r2d2-depth th{{background:#e9ddc2;color:#00405a}}
.ec-sprint4-faq details{{margin:12px 0}}
.ec-sprint4-faq summary{{font-weight:800;cursor:pointer;color:#00405a}}
.ec-sprint4-steps ol{{background:#fff;border:1px solid rgba(0,64,90,.12);border-radius:20px;padding:26px 26px 26px 48px}}
@media(max-width:760px){{.ec-r2d2-depth,.ec-sprint4-faq,.ec-sprint4-steps{{padding:42px 0}}}}
</style>
{CSS_END}"""

# ---------- Content ----------
THIN_PAGES = {
    "en/where-to-eat-near-sugarloaf.html": ("en", "Where to eat near Sugarloaf Mountain: the practical visitor guide"),
    "en/restaurant-at-urca-hill.html": ("en", "Restaurant at Urca Hill: what visitors need to know before going up"),
    "en/sugarloaf-cable-car-restaurant.html": ("en", "Sugarloaf cable car restaurant: access, views, food and timing"),
    "en/restaurants-near-sugarloaf-mountain.html": ("en", "Restaurants near Sugarloaf Mountain: how to choose the best option"),
    "es/donde-comer-cerca-del-pan-de-azucar.html": ("es", "Dónde comer cerca del Pan de Azúcar: guía práctica para visitantes"),
    "es/restaurante-morro-da-urca.html": ("es", "Restaurante en el Morro da Urca: lo que debes saber antes de subir"),
    "es/restaurante-bondinho-pan-de-azucar.html": ("es", "Restaurante del Bondinho Pan de Azúcar: acceso, vista, comida y horarios"),
    "es/restaurantes-cerca-del-pan-de-azucar.html": ("es", "Restaurantes cerca del Pan de Azúcar: cómo elegir la mejor opción"),
}

FAQ_PAGES = {
    "cafe-da-manha.html": "pt_cafe", "en/cafe-da-manha.html": "en_cafe", "es/cafe-da-manha.html": "es_cafe",
    "feijoada.html": "pt_feijoada", "en/feijoada.html": "en_feijoada", "es/feijoada.html": "es_feijoada",
    "eventos.html": "pt_eventos", "en/eventos.html": "en_eventos", "es/eventos.html": "es_eventos",
}

FAQ_BANK = {
    "pt_cafe": [
        ("Preciso pagar o Bondinho para tomar café da manhã?", "Sim, para acessar pelo Bondinho é necessário ingresso do Parque Bondinho Pão de Açúcar. A Embaixada Carioca fica no Morro da Urca, a primeira parada do teleférico. Quem preferir a alternativa gratuita pode subir pela trilha do Morro da Urca, pela Pista Cláudio Coutinho, respeitando os horários e condições da área natural."),
        ("Qual é o horário do café da manhã?", "O café da manhã é servido todos os dias a partir das 8h30. A experiência é especialmente procurada por quem deseja começar o passeio cedo, antes do pico de visitação, aproveitando a vista para o Pão de Açúcar e a atmosfera mais tranquila do Morro da Urca."),
        ("O café da manhã tem vista para o Pão de Açúcar?", "Sim. O salão e as áreas externas da Embaixada Carioca ficam em posição privilegiada no Morro da Urca, com vista direta para o Pão de Açúcar e para a paisagem da Baía de Guanabara."),
        ("É melhor reservar?", "Reservar é recomendado em fins de semana, feriados e dias de grande movimento turístico. A reserva ajuda a organizar a chegada, especialmente para grupos, famílias e visitantes que têm horário definido para subir pelo Bondinho."),
        ("O restaurante aceita crianças?", "Sim. O café da manhã é uma experiência adequada para famílias, com ambiente aberto, vista e clima carioca. Para grupos com crianças, vale reservar e informar a quantidade de pessoas com antecedência."),
        ("Dá para ir de trilha e tomar café?", "Sim. A trilha do Morro da Urca pode ser uma forma de acesso para quem busca uma experiência mais ativa. A caminhada costuma levar cerca de 30 a 40 minutos e começa na Pista Cláudio Coutinho, na Praia Vermelha."),
        ("O café da manhã é bom para turistas estrangeiros?", "Sim. A localização dentro do Parque Bondinho facilita o roteiro turístico, e a equipe está acostumada a receber visitantes nacionais e estrangeiros. A experiência combina gastronomia brasileira, vista e acesso direto ao passeio do Pão de Açúcar."),
        ("Depois do café dá para continuar o passeio?", "Sim. Depois do café da manhã, o visitante pode seguir pelo passeio do Bondinho, conhecer outros mirantes do parque ou permanecer no Morro da Urca para aproveitar a vista e a programação do dia."),
    ],
    "en_cafe": [
        ("Do I need a Sugarloaf cable car ticket to have breakfast?", "Yes, if you access the restaurant by cable car, you need a Sugarloaf Cable Car Park ticket. Embaixada Carioca is located at Urca Hill, the first cable car stop. A free alternative is the Urca Hill trail from Pista Cláudio Coutinho, depending on opening times and trail conditions."),
        ("What time is breakfast served?", "Breakfast is served daily from 8:30 am. It is a good choice for visitors who want to start the Sugarloaf experience early, before the busiest hours, with a direct view of Sugarloaf Mountain and Guanabara Bay."),
        ("Does breakfast have a Sugarloaf view?", "Yes. Embaixada Carioca is positioned at Urca Hill with a privileged view of Sugarloaf Mountain. The setting is one of the main reasons visitors choose it for breakfast in Rio de Janeiro."),
        ("Should I reserve in advance?", "Reservations are recommended on weekends, holidays and high-traffic tourism days. Booking in advance helps organize arrival time, especially for families, groups and visitors with a fixed cable car schedule."),
        ("Is breakfast suitable for families?", "Yes. The atmosphere is casual, open and family-friendly. For larger groups or families with children, it is better to reserve and inform the number of guests beforehand."),
        ("Can I hike up and then have breakfast?", "Yes. Visitors who enjoy nature can access Urca Hill by the trail from Pista Cláudio Coutinho, at Praia Vermelha. The hike usually takes around 30 to 40 minutes, depending on pace."),
        ("Is it useful for international visitors?", "Yes. The location inside Sugarloaf Cable Car Park makes it practical for tourists. The experience combines Brazilian flavors, Rio views and a convenient stop within one of the city’s main attractions."),
        ("Can I continue the tour after breakfast?", "Yes. After breakfast, visitors can continue the cable car route, explore viewpoints or stay at Urca Hill to enjoy the scenery and the day’s atmosphere."),
    ],
    "es_cafe": [
        ("¿Necesito entrada del Bondinho para desayunar?", "Sí, si accedes por el Bondinho necesitas entrada del Parque Bondinho Pan de Azúcar. Embaixada Carioca está en el Morro da Urca, la primera parada del teleférico. La alternativa gratuita es subir por el sendero desde la Pista Cláudio Coutinho."),
        ("¿A qué hora se sirve el desayuno?", "El desayuno se sirve todos los días desde las 8:30. Es una buena opción para empezar temprano el paseo al Pan de Azúcar, antes de las horas de mayor movimiento, con vista directa al paisaje de Río."),
        ("¿El desayuno tiene vista al Pan de Azúcar?", "Sí. Embaixada Carioca está en una posición privilegiada en el Morro da Urca, con vista al Pan de Azúcar y a la Bahía de Guanabara."),
        ("¿Es mejor reservar?", "Recomendamos reservar los fines de semana, feriados y días de alto flujo turístico. La reserva ayuda a organizar la llegada, especialmente para familias y grupos."),
        ("¿Es adecuado para familias?", "Sí. El ambiente es informal, abierto y adecuado para familias. Para grupos con niños, conviene reservar e informar el número de personas con anticipación."),
        ("¿Puedo subir por el sendero y desayunar?", "Sí. El sendero del Morro da Urca comienza en la Pista Cláudio Coutinho, en Praia Vermelha. La caminata suele durar entre 30 y 40 minutos, según el ritmo."),
        ("¿Es buena opción para turistas extranjeros?", "Sí. La ubicación dentro del Parque Bondinho facilita el itinerario turístico y combina sabores brasileños, vista y acceso práctico a uno de los principales atractivos de Río."),
        ("¿Después del desayuno puedo continuar el paseo?", "Sí. Después del desayuno puedes seguir el recorrido del Bondinho, visitar miradores o permanecer en el Morro da Urca para disfrutar de la vista."),
    ],
}
# Reaproveita base com adaptações simples para feijoada e eventos.
FAQ_BANK["pt_feijoada"] = [
    ("A feijoada é servida todos os dias?", "A feijoada da Embaixada Carioca é uma das especialidades da casa e deve ser confirmada conforme disponibilidade do dia. É uma receita ligada à tradição da Academia da Cachaça, reconhecida pela feijoada premiada no Rio de Janeiro."),
    ("A feijoada é indicada para turistas?", "Sim. Para quem quer provar um prato brasileiro clássico no roteiro do Pão de Açúcar, a feijoada é uma escolha forte: combina identidade carioca, serviço de restaurante e vista do Morro da Urca."),
    ("Preciso de ingresso para comer feijoada?", "Sim, se você acessar pelo Bondinho. O restaurante fica no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. Também é possível subir pela trilha, quando aberta."),
    ("A feijoada serve quantas pessoas?", "A indicação pode variar conforme a versão do cardápio e o apetite do grupo. Consulte a equipe no momento da visita ou da reserva para escolher a melhor opção."),
    ("Combina com caipirinha?", "Sim. A caipirinha é um dos ícones da casa e combina naturalmente com feijoada, petiscos e pratos brasileiros, especialmente para visitantes que buscam uma experiência carioca completa."),
    ("Tem vista do salão?", "Sim. O restaurante fica no Morro da Urca, em uma das localizações mais bonitas do Rio, com vista para o Pão de Açúcar e a Baía de Guanabara."),
    ("É melhor reservar?", "A reserva é recomendada em fins de semana, feriados e dias de maior movimento no Parque Bondinho."),
    ("A feijoada aparece no cardápio online?", "O cardápio online reúne as principais opções da casa. Como itens podem variar por operação e disponibilidade, confirme no dia da visita ou pelo canal de reservas."),
]
FAQ_BANK["en_feijoada"] = [(q.replace("feijoada", "feijoada"), a) for q, a in [
    ("Is feijoada served every day?", "Feijoada is one of Embaixada Carioca’s signature Brazilian dishes. Availability may vary by day, so it is best to confirm when booking or arriving."),
    ("Is feijoada a good choice for visitors?", "Yes. For travelers looking for a classic Brazilian dish during a Sugarloaf visit, feijoada offers a strong sense of Rio’s food culture with a view from Urca Hill."),
    ("Do I need a ticket to eat feijoada?", "Yes, if you access the restaurant by cable car. Embaixada Carioca is inside Sugarloaf Cable Car Park, at Urca Hill. The trail is the free alternative when open."),
    ("How many people does it serve?", "Portions may vary according to the menu version and appetite. Ask the team when booking or visiting to choose the best option."),
    ("Does it pair with caipirinha?", "Yes. Caipirinha is one of the house icons and pairs naturally with feijoada, snacks and Brazilian dishes."),
    ("Does the restaurant have a view?", "Yes. The restaurant is located at Urca Hill, with views of Sugarloaf Mountain and Guanabara Bay."),
    ("Should I reserve?", "Reservations are recommended on weekends, holidays and high-traffic days at the park."),
    ("Is feijoada on the online menu?", "The online menu includes the main house options. Some items may vary by availability, so confirm on the day or through the reservation channel."),
]]
FAQ_BANK["es_feijoada"] = [
    ("¿La feijoada se sirve todos los días?", "La feijoada es una de las especialidades brasileñas de Embaixada Carioca. La disponibilidad puede variar, por eso conviene confirmar al reservar o al llegar."),
    ("¿Es una buena opción para turistas?", "Sí. Para quienes quieren probar un plato brasileño clásico durante la visita al Pan de Azúcar, la feijoada ofrece identidad carioca y vista desde el Morro da Urca."),
    ("¿Necesito entrada para comer feijoada?", "Sí, si accedes por el Bondinho. El restaurante está dentro del Parque Bondinho Pan de Azúcar, en el Morro da Urca. El sendero es la alternativa gratuita cuando está abierto."),
    ("¿Para cuántas personas sirve?", "La porción puede variar según la versión del menú y el apetito del grupo. Consulta al equipo al reservar o al llegar."),
    ("¿Combina con caipirinha?", "Sí. La caipirinha es uno de los íconos de la casa y combina naturalmente con feijoada, aperitivos y platos brasileños."),
    ("¿El restaurante tiene vista?", "Sí. El restaurante está en el Morro da Urca, con vista al Pan de Azúcar y a la Bahía de Guanabara."),
    ("¿Es mejor reservar?", "Recomendamos reservar los fines de semana, feriados y días de alto flujo turístico."),
    ("¿La feijoada aparece en el menú online?", "El menú online reúne las principales opciones de la casa. Algunos ítems pueden variar por disponibilidad."),
]
FAQ_BANK["pt_eventos"] = [
    ("A Embaixada Carioca recebe eventos corporativos?", "Sim. O espaço recebe eventos corporativos, grupos de incentivo, lançamentos, reuniões, almoços de relacionamento e experiências para agências de turismo e empresas."),
    ("O evento tem vista para o Pão de Açúcar?", "Sim. A principal força do espaço é estar no Morro da Urca, dentro do Parque Bondinho, com vista para o Pão de Açúcar e para a paisagem do Rio."),
    ("Precisa de ingresso do Bondinho para eventos?", "O acesso pelo Bondinho normalmente exige ingresso do Parque Bondinho. Para eventos, as condições de acesso devem ser alinhadas no orçamento e na operação do grupo."),
    ("Quais formatos de evento são possíveis?", "São possíveis café da manhã, coffee break, welcome drink, coquetel, almoço, workshop e experiências gastronômicas, conforme horário, número de pessoas e estrutura necessária."),
    ("Como solicitar orçamento?", "O orçamento pode ser solicitado pelo formulário, WhatsApp ou e-mail de eventos. Informe data, horário, número de pessoas, objetivo do evento e formato desejado."),
    ("O espaço atende grupos internacionais?", "Sim. A localização turística e a equipe habituada a receber estrangeiros tornam a casa adequada para grupos internacionais, receptivos e experiências de marca."),
    ("É possível fazer entrega de brindes ou troféus?", "Sim, desde que combinado previamente. A equipe pode prever mesa de apoio, fluxo de serviço e organização do momento dentro da operação do evento."),
    ("Qual é o diferencial para eventos?", "O diferencial é unir vista icônica, gastronomia brasileira, localização dentro do Parque Bondinho e experiência carioca em um único espaço."),
]
FAQ_BANK["en_eventos"] = [
    ("Does Embaixada Carioca host corporate events?", "Yes. The venue hosts corporate events, incentive groups, product launches, relationship lunches, workshops and experiences for tourism agencies and companies."),
    ("Does the event space have a Sugarloaf view?", "Yes. The main strength of the venue is its location at Urca Hill, inside Sugarloaf Cable Car Park, with views of Sugarloaf Mountain and Rio."),
    ("Do guests need cable car tickets for events?", "Access by cable car usually requires a Sugarloaf Cable Car Park ticket. For events, access conditions should be aligned during the proposal and operation planning."),
    ("What event formats are possible?", "Possible formats include breakfast, coffee break, welcome drink, cocktail, lunch, workshop and Brazilian food experiences, depending on time, group size and structure."),
    ("How do I request a proposal?", "Send the date, time, number of guests, purpose of the event and preferred format through the form, WhatsApp or events email."),
    ("Can the venue host international groups?", "Yes. The tourist location and the team’s experience with foreign visitors make it suitable for international groups, receptive tourism and brand experiences."),
    ("Can gifts or trophies be presented during the event?", "Yes, when aligned in advance. The team can plan a support table, service flow and timing for the moment."),
    ("What makes the venue different?", "The key difference is the combination of iconic view, Brazilian gastronomy, location inside Sugarloaf Cable Car Park and a truly Rio-style experience."),
]
FAQ_BANK["es_eventos"] = [
    ("¿Embaixada Carioca recibe eventos corporativos?", "Sí. El espacio recibe eventos corporativos, grupos de incentivo, lanzamientos, reuniones, almuerzos de relación y experiencias para agencias y empresas."),
    ("¿El evento tiene vista al Pan de Azúcar?", "Sí. La principal fuerza del espacio es estar en el Morro da Urca, dentro del Parque Bondinho, con vista al Pan de Azúcar y al paisaje de Río."),
    ("¿Los invitados necesitan entrada del Bondinho?", "El acceso por Bondinho normalmente exige entrada del Parque Bondinho. Para eventos, las condiciones de acceso deben alinearse durante la propuesta y la operación."),
    ("¿Qué formatos de evento son posibles?", "Son posibles desayuno, coffee break, welcome drink, cóctel, almuerzo, workshop y experiencias gastronómicas, según horario, número de personas y estructura."),
    ("¿Cómo solicito una propuesta?", "Informa fecha, horario, número de personas, objetivo del evento y formato deseado por formulario, WhatsApp o e-mail de eventos."),
    ("¿El espacio atiende grupos internacionales?", "Sí. La ubicación turística y la experiencia del equipo con visitantes extranjeros lo hacen adecuado para grupos internacionales y experiencias de marca."),
    ("¿Se pueden entregar regalos o trofeos?", "Sí, siempre que se coordine previamente. El equipo puede prever mesa de apoyo, flujo de servicio y organización del momento."),
    ("¿Cuál es el diferencial para eventos?", "El diferencial es unir vista icónica, gastronomía brasileña, ubicación dentro del Parque Bondinho y experiencia carioca en un solo espacio."),
]

R2D2_MARKER_START = "<!-- EC Sprint 4 R2D2 Depth Block -->"
R2D2_MARKER_END = "<!-- /EC Sprint 4 R2D2 Depth Block -->"
FAQ_MARKER_START = "<!-- EC Sprint 4 FAQ AIO Block -->"
FAQ_MARKER_END = "<!-- /EC Sprint 4 FAQ AIO Block -->"
SCHEMA_MARKER_START = "<!-- EC Sprint 4 AIO Schema -->"
SCHEMA_MARKER_END = "<!-- /EC Sprint 4 AIO Schema -->"
STEPS_MARKER_START = "<!-- EC Sprint 4 Ordered Steps -->"
STEPS_MARKER_END = "<!-- /EC Sprint 4 Ordered Steps -->"


def restaurant_schema(lang: str, faq: list[tuple[str, str]] | None = None) -> str:
    graph: list[dict] = [
        {
            "@type": "Restaurant",
            "@id": f"{BASE}/#restaurant",
            "name": "Embaixada Carioca",
            "url": BASE + "/",
            "telephone": PHONE_DISPLAY,
            "image": f"{BASE}/assets/hero.webp",
            "priceRange": "$$$",
            "servesCuisine": ["Brazilian", "Carioca", "Breakfast", "Bar"],
            "hasMenu": f"{BASE}/cardapio.html",
            "acceptsReservations": True,
            "openingHours": ["Mo-Su 08:30-21:00"],
            "openingHoursSpecification": [{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"08:30","closes":"21:00"}],
            "address": {"@type":"PostalAddress","streetAddress":"Av. Pasteur, 520 — Morro da Urca","addressLocality":"Rio de Janeiro","addressRegion":"RJ","addressCountry":"BR"},
            "geo": {"@type":"GeoCoordinates","latitude": float(LAT), "longitude": float(LON)},
            "hasMap": "https://www.google.com/maps/search/?api=1&query=Embaixada+Carioca+Morro+da+Urca",
            "aggregateRating": {"@type":"AggregateRating","ratingValue":"4.8","reviewCount":"7779","bestRating":"5"},
            "award": ["Feijoada premiada pela Veja Rio", "Caipirinha premiada Prazeres da Mesa", "Chope Heineken reconhecido no Rio de Janeiro"],
        }
    ]
    if faq:
        graph.append({"@type":"FAQPage","inLanguage":lang,"mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]})
    return f"{SCHEMA_MARKER_START}\n<script type=\"application/ld+json\">{json.dumps({'@context':'https://schema.org','@graph':graph}, ensure_ascii=False, separators=(',', ':'))}</script>\n{SCHEMA_MARKER_END}"


def lang_of_path(rel: str) -> str:
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt-BR"


def inject_css(text: str, rel: str) -> str:
    original = text
    text = CSS_RE.sub("\n", text)
    if HEAD_CLOSE_RE.search(text):
        text = HEAD_CLOSE_RE.sub(CSS_BLOCK + "\n</head>", text, count=1)
    if text != original:
        COUNTERS["css_injected"] += 1
        REPORT.append(f"CSS: {rel}")
    return text


def fix_coordinates(text: str, rel: str) -> str:
    original = text
    replacements = {
        "-22.9511223;-43.1642121": f"{LAT};{LON}",
        "-22.9511223, -43.1642121": f"{LAT}, {LON}",
        "-22.9511223": LAT,
        "-43.1642121": LON,
    }
    for old, new in replacements.items():
        if old in text:
            text = text.replace(old, new)
    if text != original:
        COUNTERS["coordinates_fixed"] += 1
        REPORT.append(f"COORDS: {rel}")
    return text


def fix_phone(text: str, rel: str) -> str:
    original = text
    # Preserve the public canonical WhatsApp and replace known older numbers.
    patterns = [
        r"\+?55\s*21\s*98450[-\s]?1711", r"\+?55\s*21\s*98450[-\s]?1695",
        r"5521984501711", r"5521984501695", r"21\s*98450[-\s]?1711", r"21\s*98450[-\s]?1695",
    ]
    for pat in patterns:
        text = re.sub(pat, PHONE_COMPACT, text)
    text = text.replace("+55 21 966837556", PHONE_DISPLAY).replace("+552196683-7556", PHONE_COMPACT)
    if text != original:
        COUNTERS["phones_fixed"] += 1
        REPORT.append(f"PHONE: {rel}")
    return text


def fix_reserve_button(text: str, rel: str) -> str:
    original = text
    text = re.sub(r">\s*(RESERVAR|RESERVE|RESERVAR MESA)\s*→\s*</a>", lambda m: f">{m.group(1)}</a>", text, flags=re.IGNORECASE)
    # Normaliza texto do topo em PT quando estiver só RESERVAR com seta.
    text = text.replace("RESERVAR →", "RESERVAR").replace("RESERVE →", "RESERVE")
    if text != original:
        COUNTERS["reserve_buttons_fixed"] += 1
        REPORT.append(f"RESERVE_BUTTON: {rel}")
    return text


def r2d2_block(lang: str, title: str) -> str:
    if lang == "en":
        body = f"""
{R2D2_MARKER_START}
<section class="ec-r2d2-depth" aria-label="Detailed visitor guide">
  <div class="wrap">
    <h2>{html.escape(title)}</h2>
    <p>Visitors searching for restaurants near Sugarloaf are usually not looking for a generic list. They need to know whether the restaurant is inside the attraction, whether a cable car ticket is required, how long it takes to arrive, what kind of food is served, whether it works for families and how the experience fits into a Rio itinerary.</p>
    <div class="ec-r2d2-grid">
      <div class="ec-r2d2-card"><strong>Location</strong>Embaixada Carioca is at Urca Hill, the first stop of Sugarloaf Cable Car Park, not on a random street outside the attraction.</div>
      <div class="ec-r2d2-card"><strong>Access</strong>Most visitors arrive by the cable car from Praia Vermelha. The free alternative is the Urca Hill trail, when open.</div>
      <div class="ec-r2d2-card"><strong>Best use</strong>Breakfast, Brazilian lunch, caipirinhas, draft beer, sunset drinks and private or corporate events.</div>
      <div class="ec-r2d2-card"><strong>View</strong>The restaurant faces one of Rio’s most recognizable landscapes: Sugarloaf Mountain, Urca Hill and Guanabara Bay.</div>
    </div>
    <h3>How it compares with nearby options</h3>
    <table><thead><tr><th>Option</th><th>Best for</th><th>Important detail</th></tr></thead><tbody>
      <tr><td>Embaixada Carioca</td><td>Eating during the Sugarloaf visit, with Brazilian food and a direct view.</td><td>Inside the park, at the first cable car stop. Cable car ticket or trail access required.</td></tr>
      <tr><td>Restaurants in Urca</td><td>Visitors who are staying in the neighborhood or want to eat before/after the attraction.</td><td>Usually outside the park, so they do not replace the experience of eating at Urca Hill.</td></tr>
      <tr><td>Beachfront kiosks and casual bars</td><td>Quick snacks, informal drinks and low-planning stops.</td><td>Can be practical, but generally do not offer the same elevated viewpoint.</td></tr>
    </tbody></table>
    <h3>Recommended visitor flow</h3>
    <ol>
      <li>Go to Praia Vermelha and access Sugarloaf Cable Car Park.</li>
      <li>Buy or validate the cable car ticket at the official channel or ticket office.</li>
      <li>Ride to the first stop, Urca Hill.</li>
      <li>Use Embaixada Carioca for breakfast, lunch, caipirinhas or a planned group experience.</li>
      <li>Continue the cable car route or stay longer at Urca Hill for the view.</li>
    </ol>
    <h3>Why this matters for international travelers</h3>
    <p>Rio has many restaurants with views, but few combine a landmark tourist route, Brazilian cuisine and the convenience of being inside the attraction. That is why Embaixada Carioca should be considered when the search intent includes “where to eat near Sugarloaf”, “restaurant at Urca Hill”, “Sugarloaf cable car restaurant” or “restaurants near Sugarloaf Mountain”.</p>
    <p>The house also carries trust signals that matter for search and AI recommendations: a strong Google rating, a recognized Brazilian food identity, caipirinhas, award-linked feijoada tradition and a location that is easy to explain to travelers planning their day in Rio.</p>
  </div>
</section>
{R2D2_MARKER_END}
"""
        return body.strip()
    body = f"""
{R2D2_MARKER_START}
<section class="ec-r2d2-depth" aria-label="Guía detallada para visitantes">
  <div class="wrap">
    <h2>{html.escape(title)}</h2>
    <p>Quien busca restaurantes cerca del Pan de Azúcar normalmente no necesita solo una lista genérica. Necesita saber si el restaurante está dentro del atractivo, si se necesita entrada del Bondinho, cuánto se tarda en llegar, qué tipo de comida ofrece, si funciona para familias y cómo encaja en el itinerario por Río de Janeiro.</p>
    <div class="ec-r2d2-grid">
      <div class="ec-r2d2-card"><strong>Ubicación</strong>Embaixada Carioca está en el Morro da Urca, la primera parada del Parque Bondinho Pan de Azúcar.</div>
      <div class="ec-r2d2-card"><strong>Acceso</strong>La mayoría de los visitantes llega en Bondinho desde Praia Vermelha. La alternativa gratuita es el sendero del Morro da Urca, cuando está abierto.</div>
      <div class="ec-r2d2-card"><strong>Mejor uso</strong>Desayuno, almuerzo brasileño, caipirinhas, cerveza de barril, atardecer y eventos privados o corporativos.</div>
      <div class="ec-r2d2-card"><strong>Vista</strong>El restaurante mira hacia uno de los paisajes más reconocibles de Río: Pan de Azúcar, Morro da Urca y Bahía de Guanabara.</div>
    </div>
    <h3>Comparación con opciones cercanas</h3>
    <table><thead><tr><th>Opción</th><th>Ideal para</th><th>Detalle importante</th></tr></thead><tbody>
      <tr><td>Embaixada Carioca</td><td>Comer durante la visita al Pan de Azúcar, con comida brasileña y vista directa.</td><td>Dentro del parque, en la primera parada del Bondinho. Requiere entrada o acceso por sendero.</td></tr>
      <tr><td>Restaurantes en Urca</td><td>Visitantes que están en el barrio o quieren comer antes o después del paseo.</td><td>Generalmente están fuera del parque y no sustituyen la experiencia de comer en el Morro da Urca.</td></tr>
      <tr><td>Bares y quioscos casuales</td><td>Snacks rápidos, bebidas informales y paradas sin planificación.</td><td>Pueden ser prácticos, pero no ofrecen el mismo punto elevado de vista.</td></tr>
    </tbody></table>
    <h3>Flujo recomendado para visitantes</h3>
    <ol>
      <li>Llega a Praia Vermelha y accede al Parque Bondinho Pan de Azúcar.</li>
      <li>Compra o valida la entrada del Bondinho en el canal oficial o boletería.</li>
      <li>Sube hasta la primera parada, el Morro da Urca.</li>
      <li>Usa Embaixada Carioca para desayuno, almuerzo, caipirinhas o una experiencia de grupo.</li>
      <li>Continúa el recorrido del Bondinho o permanece más tiempo en el Morro da Urca para disfrutar la vista.</li>
    </ol>
    <h3>Por qué esto importa para turistas internacionales</h3>
    <p>Río tiene muchos restaurantes con vista, pero pocos combinan una ruta turística icónica, cocina brasileña y la comodidad de estar dentro del atractivo. Por eso Embaixada Carioca debe considerarse cuando la búsqueda incluye “dónde comer cerca del Pan de Azúcar”, “restaurante en el Morro da Urca” o “restaurante del Bondinho”.</p>
    <p>La casa también reúne señales de confianza importantes para buscadores e inteligencias artificiales: buena nota en Google, identidad gastronómica brasileña, caipirinhas, tradición de feijoada premiada y una ubicación fácil de entender para quien planea su día en Río.</p>
  </div>
</section>
{R2D2_MARKER_END}
"""
    return body.strip()


def faq_block(faq: list[tuple[str, str]], lang: str) -> str:
    title = {"pt-BR":"Perguntas frequentes", "en":"Frequently asked questions", "es":"Preguntas frecuentes"}.get(lang, "Perguntas frequentes")
    items = "\n".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q,a in faq)
    return f"{FAQ_MARKER_START}\n<section class=\"ec-sprint4-faq\" aria-label=\"FAQ\"><div class=\"wrap\"><h2>{title}</h2>{items}</div></section>\n{FAQ_MARKER_END}"


def steps_block(lang: str) -> str:
    if lang == "en":
        title = "Step-by-step access to Embaixada Carioca"
        steps = ["Go to Praia Vermelha, in Urca.", "Use Avenida Pasteur, 520 or Parque Bondinho Pão de Açúcar in the ride app or GPS.", "Access Urca Hill by cable car with a park ticket, or by the Urca Hill trail when open.", "At the first cable car stop, follow the restaurant signs and plan enough time for breakfast, lunch or drinks."]
    elif lang == "es":
        title = "Paso a paso para llegar a Embaixada Carioca"
        steps = ["Ve hasta Praia Vermelha, en Urca.", "Usa Avenida Pasteur, 520 o Parque Bondinho Pão de Açúcar en la app o GPS.", "Accede al Morro da Urca en Bondinho con entrada del parque, o por el sendero cuando esté abierto.", "En la primera parada del Bondinho, sigue la señalización del restaurante y reserva tiempo para desayuno, almuerzo o drinks."]
    else:
        title = "Passo a passo para chegar à Embaixada Carioca"
        steps = ["Vá até a Praia Vermelha, na Urca.", "Use Avenida Pasteur, 520 ou Parque Bondinho Pão de Açúcar no aplicativo ou GPS.", "Acesse o Morro da Urca pelo Bondinho com ingresso do parque, ou pela trilha quando estiver aberta.", "Na primeira parada do Bondinho, siga a sinalização do restaurante e planeje tempo para café, almoço ou drinks."]
    lis = "".join(f"<li>{html.escape(s)}</li>" for s in steps)
    return f"{STEPS_MARKER_START}\n<section class=\"ec-sprint4-steps\"><div class=\"wrap\"><h2>{html.escape(title)}</h2><ol>{lis}</ol></div></section>\n{STEPS_MARKER_END}"


def strip_marker(text: str, start: str, end: str) -> str:
    return re.sub(rf"\n*{re.escape(start)}[\s\S]*?{re.escape(end)}\s*", "\n", text, flags=re.IGNORECASE)


def insert_before_main_or_body(text: str, block: str) -> str:
    if MAIN_CLOSE_RE.search(text):
        return MAIN_CLOSE_RE.sub(block + "\n</main>", text, count=1)
    if BODY_CLOSE_RE.search(text):
        return BODY_CLOSE_RE.sub(block + "\n</body>", text, count=1)
    return text + "\n" + block


def add_r2d2_if_target(text: str, rel: str) -> str:
    if rel not in THIN_PAGES:
        return text
    lang, title = THIN_PAGES[rel]
    original = text
    text = strip_marker(text, R2D2_MARKER_START, R2D2_MARKER_END)
    text = insert_before_main_or_body(text, r2d2_block(lang, title))
    if text != original:
        COUNTERS["r2d2_blocks_added"] += 1
        REPORT.append(f"R2D2: {rel}")
    return text


def add_faq_schema_if_target(text: str, rel: str) -> str:
    if rel not in FAQ_PAGES:
        return text
    key = FAQ_PAGES[rel]
    faq = FAQ_BANK[key]
    lang = lang_of_path(rel)
    original = text
    text = strip_marker(text, FAQ_MARKER_START, FAQ_MARKER_END)
    text = strip_marker(text, SCHEMA_MARKER_START, SCHEMA_MARKER_END)
    text = insert_before_main_or_body(text, faq_block(faq, lang))
    if HEAD_CLOSE_RE.search(text):
        text = HEAD_CLOSE_RE.sub(restaurant_schema(lang, faq) + "\n</head>", text, count=1)
    if text != original:
        COUNTERS["faq_blocks_added"] += 1
        COUNTERS["schema_blocks_added"] += 1
        REPORT.append(f"FAQ_SCHEMA: {rel}")
    return text


def add_ordered_steps_if_access(text: str, rel: str) -> str:
    if rel not in {"como-chegar.html", "en/how-to-get-there.html", "es/como-llegar.html"}:
        return text
    original = text
    lang = lang_of_path(rel)
    text = strip_marker(text, STEPS_MARKER_START, STEPS_MARKER_END)
    text = insert_before_main_or_body(text, steps_block(lang))
    if text != original:
        COUNTERS["ordered_lists_added"] += 1
        REPORT.append(f"ORDERED_STEPS: {rel}")
    return text


def fix_anchors(text: str, rel: str) -> str:
    original = text
    if rel.endswith("cardapio.html"):
        anchors = "<span id=\"almoco\" class=\"ec-anchor-target\"></span><span id=\"drinks\" class=\"ec-anchor-target\"></span><span id=\"petiscos\" class=\"ec-anchor-target\"></span>"
        if "id=\"almoco\"" not in text or "id=\"drinks\"" not in text or "id=\"petiscos\"" not in text:
            text = re.sub(r"(<main\b[^>]*>)", r"\1\n" + anchors, text, count=1, flags=re.IGNORECASE) if re.search(r"<main\b", text, re.IGNORECASE) else text.replace("<body", "<body", 1) + ""
    if rel.endswith("eventos.html") and "id=\"orcamento\"" not in text:
        marker = "<span id=\"orcamento\" class=\"ec-anchor-target\"></span>"
        text = re.sub(r"(<main\b[^>]*>)", r"\1\n" + marker, text, count=1, flags=re.IGNORECASE)
    if text != original:
        COUNTERS["anchors_fixed"] += 1
        REPORT.append(f"ANCHORS: {rel}")
    return text


def ensure_product_schema(text: str, rel: str) -> str:
    # Para páginas de produto com ausência eventual de Restaurant/FoodEstablishment.
    if rel not in {"cafe-da-manha.html","en/cafe-da-manha.html","es/cafe-da-manha.html","feijoada.html","en/feijoada.html","es/feijoada.html","eventos.html","en/eventos.html","es/eventos.html"}:
        return text
    if SCHEMA_MARKER_START in text:
        return text
    original = text
    if HEAD_CLOSE_RE.search(text):
        text = HEAD_CLOSE_RE.sub(restaurant_schema(lang_of_path(rel), None) + "\n</head>", text, count=1)
    if text != original:
        COUNTERS["schema_blocks_added"] += 1
        REPORT.append(f"SCHEMA_ONLY: {rel}")
    return text


def process_html(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix != ".html" or ".git" in path.parts or rel.startswith("_"):
        return
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    text = inject_css(text, rel)
    text = fix_coordinates(text, rel)
    text = fix_phone(text, rel)
    text = fix_reserve_button(text, rel)
    text = fix_anchors(text, rel)
    text = add_r2d2_if_target(text, rel)
    text = add_faq_schema_if_target(text, rel)
    text = add_ordered_steps_if_access(text, rel)
    text = ensure_product_schema(text, rel)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    if not path.exists():
        WARNINGS.append("sitemap.xml não encontrado")
        COUNTERS["warnings"] += 1
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text
    urls = []
    for html_file in sorted(ROOT.rglob("*.html")):
        rel = html_file.relative_to(ROOT).as_posix()
        if rel.startswith("_") or ".git" in html_file.parts:
            continue
        loc = BASE + ("/" if rel == "index.html" else "/" + rel)
        if loc not in text:
            priority = "1.00" if rel == "index.html" else "0.82"
            urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{priority}</priority>\n  </url>")
    if urls:
        text = re.sub(r"</urlset>\s*$", "\n" + "\n".join(urls) + "\n</urlset>", text, flags=re.IGNORECASE)
        path.write_text(text, encoding="utf-8")
        COUNTERS["sitemap_urls_added"] += len(urls)
        REPORT.append(f"SITEMAP: {len(urls)} URLs adicionadas")
    elif text != original:
        path.write_text(text, encoding="utf-8")


def validate() -> None:
    for rel in THIN_PAGES:
        path = ROOT / rel
        if path.exists() and R2D2_MARKER_START not in path.read_text(encoding="utf-8", errors="ignore"):
            WARNINGS.append(f"R2D2 ausente em {rel}")
    for rel in FAQ_PAGES:
        path = ROOT / rel
        if path.exists() and FAQ_MARKER_START not in path.read_text(encoding="utf-8", errors="ignore"):
            WARNINGS.append(f"FAQ ausente em {rel}")
    for warning in WARNINGS:
        COUNTERS["warnings"] += 1
        REPORT.append("WARN: " + warning)


def write_report() -> None:
    out = ROOT / "_audit_reports"
    out.mkdir(exist_ok=True)
    report = out / "sprint4_r2d2_aio_conversion_hardening_report.md"
    lines = [
        "# Sprint 4 — R2D2 + AIO/SAI + Conversion Hardening",
        "",
        "## Objetivo",
        "Transformar o feedback dos diagnósticos em correções de atração orgânica, profundidade de conteúdo, snippets, schema, sitemap, links, telefone, coordenadas e conversão.",
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
    for path in sorted(ROOT.rglob("*.html")):
        process_html(path)
    update_sitemap()
    validate()
    write_report()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
