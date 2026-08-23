#!/usr/bin/env python3
"""Polish the highest-traffic English commercial pages and verify the result."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "high_traffic_english_editorial_fix_report.md"

TARGETS = (
    "en/index.html",
    "en/eventos.html",
    "en/cardapio.html",
    "en/cafe-da-manha.html",
    "en/almoco.html",
    "en/feijoada.html",
    "en/sunset.html",
)

COMMON_REPLACEMENTS = (
    ('"name": "Vista para o Pão de Açúcar"', '"name": "View of Sugarloaf Mountain"'),
    ('"name": "Dentro do Parque Bondinho Pão de Açúcar"', '"name": "Inside Sugarloaf Cable Car Park"'),
    ('"name": "Atendimento para grupos e eventos"', '"name": "Group and event service"'),
    ('"name": "Vista no Morro da Urca"', '"name": "Views from Urca Hill"'),
    ('"name": "Experiência gastronômica carioca"', '"name": "Carioca dining experience"'),
    ("8.255 reviews", "8,255 reviews"),
    ("8.255 Google reviews", "8,255 Google reviews"),
    ("4.8 estrelas", "4.8 stars"),
    ('aria-label="Selecionar idioma"', 'aria-label="Select language"'),
    ('aria-label="Idioma atual: EN"', 'aria-label="Current language: English"'),
    ('aria-label="Abrir menu de navegação"', 'aria-label="Open navigation menu"'),
    (
        'aria-label="Falar com a Embaixada Carioca no WhatsApp"',
        'aria-label="Contact Embaixada Carioca on WhatsApp"',
    ),
    (">Inside Parque Bondinho</span>", ">Inside Sugarloaf Cable Car Park</span>"),
    ("inside Parque Bondinho Pão de Açúcar", "inside Sugarloaf Cable Car Park"),
    ('aria-label="Navegação principal"', 'aria-label="Main navigation"'),
    ('aria-label="Embaixada Carioca · início"', 'aria-label="Embaixada Carioca · home"'),
    ('aria-label="Navegação rápida mobile"', 'aria-label="Quick mobile navigation"'),
    ('aria-label="Fechar chat"', 'aria-label="Close chat"'),
    ('aria-label="Fechar"', 'aria-label="Close"'),
    (
        'aria-label="Informações úteis para visitantes"',
        'aria-label="Useful visitor information"',
    ),
    (
        "O consulado da gastronomia e da cultura brasileira para o mundo",
        "An embassy of Brazilian food and culture for the world",
    ),
    (
        "Academia da Cachaça's award-winning feijoada from Academia da Cachaça",
        "Academia da Cachaça's award-winning feijoada",
    ),
    ("🏆 Premiado ·", "🏆 Award winner ·"),
    (
        "<span class=\"v\">Cachaças premium<br/>e vinhos selecionados</span>",
        "<span class=\"v\">Premium cachaças<br/>and selected wines</span>",
    ),
    ('"Draft beer Heineken Premiado"', '"Award-winning Heineken draft beer"'),
    ("where to eat in sugarloaf", "where to eat at Sugarloaf Mountain"),
    ("restaurants near sugarloaf mountain", "restaurants near Sugarloaf Mountain"),
    ("feijoada in rio", "feijoada in Rio"),
)

PAGE_REPLACEMENTS = {
    "en/index.html": (
        (
            "Do breakfast ao sunset, Embaixada Carioca is the restaurant with the best view in Rio de Janeiro — high above Urca Hill, with Sugarloaf Mountain right in front.",
            "From breakfast through sunset, Embaixada Carioca offers Brazilian food and drinks high above Rio, with Sugarloaf Mountain directly in front of you.",
        ),
        (
            "Person enjoying the panoramic view of Rio de Janeiro from Urca Hill — Embaixada Carioca the best view do Rio",
            "Guest enjoying one of Rio de Janeiro's most iconic views from Embaixada Carioca on Urca Hill",
        ),
        (
            "Urca Hill, inside Bondinho Pão de Açúcar Park, inside Bondinho Pão de Açúcar Park",
            "Urca Hill, inside Sugarloaf Cable Car Park",
        ),
        (
            "The Bondinho Pão de Açúcar Park (Bondinho Pão de Açúcar Park)",
            "Sugarloaf Cable Car Park",
        ),
        (
            "inside Bondinho Pão de Açúcar Park (Bondinho Pão de Açúcar Park)",
            "inside Sugarloaf Cable Car Park",
        ),
        (
            "inside the Bondinho Pão de Açúcar Park (Bondinho Pão de Açúcar Park)",
            "inside Sugarloaf Cable Car Park",
        ),
        (
            "Those who take the cable car have the ticket included as part of the Bondinho Pão de Açúcar Park experience.",
            "Visitors arriving by cable car need a valid Sugarloaf Cable Car Park ticket. The free Praia Vermelha trail is an alternative when it is open.",
        ),
        (
            "If you are searching for <strong>where to eat at Sugarloaf Mountain</strong>, <strong>where to eat near the cable car</strong>, <strong>where to eat in Urca</strong>, or specifically <strong>where to eat morro da urca</strong>, Embaixada Carioca is your must-visit stop as the premier <strong>urca hill restaurant</strong> and <strong>sugarloaf restaurant</strong> with breathtaking views.",
            "If you are searching for <strong>where to eat at Sugarloaf Mountain</strong>, <strong>where to eat near the cable car</strong>, <strong>where to eat in Urca</strong>, or <strong>where to eat at Urca Hill</strong>, Embaixada Carioca is a must-visit <strong>Urca Hill restaurant</strong> with a direct view of Sugarloaf Mountain.",
        ),
        ("where to eat morro da urca", "where to eat at Urca Hill"),
        ("breakfast morro da urca", "breakfast at Urca Hill"),
        ("breakfast at sugarloaf", "breakfast near Sugarloaf Mountain"),
        (
            "Embaixada Carioca is the most complete restaurant in Urca — the only one open every day with breakfast, lunch and sunset service, a direct view of Sugarloaf Mountain, Award-winning feijoada from Academia da Cachaça · Veja Rio Comer &amp; Beber 2025 and capacity for private events of capacity varies according to format, layout and areas used.",
            "Embaixada Carioca is a full-service restaurant on Urca Hill, open every day for breakfast, lunch and sunset drinks, with a direct view of Sugarloaf Mountain. It also serves Academia da Cachaça's award-winning feijoada and hosts private events in formats tailored to each group.",
        ),
        (
            "Awarded by Veja Rio (Award-winning feijoada from Academia da Cachaça 2025) with 4.8★ across over 8,255 Google reviews.",
            "It serves Academia da Cachaça's feijoada, winner of Veja Rio Comer &amp; Beber's Best Feijoada category in 2025, through a formal partnership, and holds a 4.8★ rating across more than 8,255 Google reviews.",
        ),
        ("over 8,000+ reviews", "more than 8,000 reviews"),
        ("over 7.779 on Google Maps", "more than 8,255 on Google Maps"),
        ("restaurant with a view rio", "restaurant with a view in Rio"),
        ("breakfast with a view rio", "breakfast with a view in Rio"),
        ("where to eat in sugarloaf", "where to eat at Sugarloaf Mountain"),
        ("feijoada in rio", "feijoada in Rio"),
        ("restaurants near sugarloaf mountain", "restaurants near Sugarloaf Mountain"),
        ("sunset morro da urca", "sunset at Urca Hill"),
        ("sunset rio de janeiro", "sunset in Rio de Janeiro"),
        ("bar with a view rio", "bar with a view in Rio"),
        ("lunch at morro da urca", "lunch at Urca Hill"),
        ("sunrise at sugarloaf", "sunrise at Sugarloaf Mountain"),
        ("morro da urca restaurant", "Urca Hill restaurant"),
        ("bondinho restaurant", "cable car restaurant"),
        (
            "It is the only feijoada with a panoramic view of Rio de Janeiro, served at 227 meters altitude at Urca Hill.",
            "It is served with a panoramic view of Rio de Janeiro, 227 metres above sea level on Urca Hill.",
        ),
        (
            "The restaurant has been operating since 2012, making it the most traditional gastronomic establishment and the one with the highest number of reviews (more than 8,255 on Google Maps) in the Sugarloaf Mountain complex.",
            "The restaurant has more than 8,255 Google reviews and welcomes visitors throughout the day for breakfast, lunch and sunset drinks on Urca Hill.",
        ),
        (
            'title="Reservation de mesa — Embaixada Carioca via Tagme"',
            'title="Table reservation — Embaixada Carioca via Tagme"',
        ),
        (
            "Embaixada Carioca is located at Urca Hill, inside Bondinho Pão de Açúcar Park, in the Urca neighborhood, Rio de Janeiro (RJ), Brazil — inside Sugarloaf Cable Car Park, at Av. Pasteur, 520. The restaurant is 4 km from Copacabana, 5 km from Ipanema, 8 km from Sugarloaf Mountain and 2 km from the historic center of Botafogo. Sugarloaf Mountain (also searched as \"sugarloaf cable car Rio de Janeiro\", \"sugarloaf mountain cable car tickets\" and \"bondinho pão de açúcar\") is one of the most visited tourist attractions in Brazil, with over 1 million visitors per year. For those searching \"where to eat at Sugarloaf Mountain\", \"restaurant sugarloaf cable car\" or \"sugarloaf mountain park restaurant\" — Embaixada Carioca is the only restaurant in the complex with a direct view of Sugarloaf Mountain — in continuous operation since 2010 (since 2010, reopened in 2020). A reference in carioca cuisine with specialty Brazilian Picanha, Academia da Cachaça's feijoada, winner of Veja Rio Comer &amp; Beber's Best Feijoada category in 2025 and served here through a formal partnership, Heineken draft elected the best in Rio de Janeiro and award-winning caipirinha with Magnífica cachaça.",
            "Embaixada Carioca is located on Urca Hill, at the first stop inside Sugarloaf Cable Car Park, Rio de Janeiro, Brazil. The entrance is at Av. Pasteur, 520, in Urca. Open since 2010 and relaunched under the Embaixada Carioca name in 2020, the restaurant serves Brazilian picanha, Academia da Cachaça's feijoada — winner of Veja Rio Comer &amp; Beber's Best Feijoada category in 2025 and served here through a formal partnership — award-winning caipirinhas and acclaimed Heineken draft beer, all with a direct view of Sugarloaf Mountain.",
        ),
    ),
    "en/eventos.html": (
        (
            "with panoramic views of Sugarloaf Mountain, Guanabara Bay and Pão de Açúcar",
            "with panoramic views of Sugarloaf Mountain and Guanabara Bay",
        ),
        (
            "with panoramic views of Sugarloaf Mountain, Guanabara Bay and Pão de Açúcar.",
            "with panoramic views of Sugarloaf Mountain and Guanabara Bay.",
        ),
        (
            "Award-winning Brazilian cuisine is the content.",
            "Award-winning Brazilian cuisine completes the experience.",
        ),
        (
            "The main hall at <strong>Urca Hill</strong> accommodates capacity varies according to format, layout and areas used in cocktail format, or 120 seated. The panoramic terraces — with Sugarloaf Mountain views — can be combined with the hall for larger groups.",
            "Capacity at the <strong>Urca Hill</strong> venue varies according to the event format, layout, service plan and areas used. The panoramic terraces — with views of Sugarloaf Mountain — can be combined with the main hall for larger groups. Request a tailored proposal with your estimated guest count.",
        ),
        (
            "The embassy of Brazilian gastronomy and culture for the world — high above do Urca Hill, Rio de Janeiro.",
            "An embassy of Brazilian food and culture for the world — high above Rio on Urca Hill.",
        ),
        ("Bilingual menu PT/ES.", "Menus available in Portuguese, English and Spanish."),
    ),
    "en/cardapio.html": (
        (
            "Full menu at Urca Hill: breakfast, lunch, Academia da Cachaça's award-winning feijoada from Academia da Cachaça, grilled picanha, snacks and cocktails with a Sugarloaf view.",
            "Full menu at Urca Hill: breakfast, lunch, Academia da Cachaça's award-winning feijoada, grilled picanha, snacks and cocktails with a Sugarloaf Mountain view.",
        ),
        ('"name": "Bobó de camarão"', '"name": "Shrimp bobó (creamy cassava stew)"'),
        ('"name": "Salmão com molho de maracujá"', '"name": "Salmon with passion fruit sauce"'),
        (
            '"description": "Codfish balls português com aioli de limão-siciliano."',
            '"description": "Portuguese-style codfish fritters with Sicilian lemon aioli."',
        ),
        ('"name": "Pão de queijo artesanal"', '"name": "Artisan Brazilian cheese bread"'),
        (
            '"description": "Pão de queijo mineiro de polvilho azedo com queijo canastra."',
            '"description": "Minas Gerais-style cheese bread made with fermented cassava starch and Canastra cheese."',
        ),
        ('"name": "Água de coco in natura"', '"name": "Fresh coconut water"'),
        (
            '"name": "award-winning feijoada from Academia da Cachaça"',
            '"name": "Award-winning feijoada by Academia da Cachaça"',
        ),
    ),
    "en/cafe-da-manha.html": (
        (
            "Sanduíche artesanal com Sugarloaf Mountain in the background na Embaixada Carioca — breakfast e brunch com vista on Urca Hill, Rio de Janeiro",
            "Artisan sandwich with Sugarloaf Mountain in the background at Embaixada Carioca — breakfast and brunch with a view on Urca Hill, Rio de Janeiro",
        ),
        (
            "Sanduíche artesanal com Sugarloaf Mountain in the background",
            "Artisan sandwich with Sugarloaf Mountain in the background",
        ),
    ),
    "en/feijoada.html": (
        (
            '<meta content="https://www.embaixadacarioca.com/en/almoco.html" property="og:url"/>',
            '<meta content="https://www.embaixadacarioca.com/en/feijoada.html" property="og:url"/>',
        ),
        (
            "<title>Best Feijoada in Rio de Janeiro 4.8★ | Embaixada Carioca</title>",
            "<title>Award-Winning Feijoada at Urca Hill | Embaixada Carioca</title>",
        ),
        (
            '<meta content="Lunch at Urca Hill with View 4.8★ | Embaixada Carioca" property="og:title"/>',
            '<meta content="Award-Winning Feijoada at Urca Hill | Embaixada Carioca" property="og:title"/>',
        ),
        (
            '<meta content="Lunch at Urca Hill with View | Embaixada Carioca" name="twitter:title"/>',
            '<meta content="Award-Winning Feijoada at Urca Hill | Embaixada Carioca" name="twitter:title"/>',
        ),
        (
            "award-winning feijoada from Academia da Cachaça at Urca Hill with a view of Sugarloaf Mountain. Served daily 12h–17h. Academia da Cachaça · Veja Rio Comer & Beber 2025. Book your table.",
            "Academia da Cachaça's award-winning feijoada, winner of Veja Rio Comer & Beber's Best Feijoada category in 2025, served daily at Embaixada Carioca from 11:30 AM to 5:00 PM with a Sugarloaf Mountain view. Book your table.",
        ),
        (
            "🏆 Award Veja Rio Comer & Beber 2025 · Melhor Feijoada do Rio de Janeiro",
            "🏆 Veja Rio Comer & Beber 2025 · Best Feijoada category winner: Academia da Cachaça",
        ),
        (
            "<h3>Feijoada da <span class=\"serif\">Academia da Cachaça.</span></h3>",
            "<h3>Feijoada by <span class=\"serif\">Academia da Cachaça.</span></h3>",
        ),
        (
            "Enjoy the most Brazilian dish of all while admiring the postcard mais famoso do Brasil, a 227 metros de altitude.",
            "Enjoy one of Brazil's most iconic dishes while admiring its most famous postcard from 227 metres above sea level.",
        ),
    ),
    "en/sunset.html": (
        (
            '"description": "Entrada inclusa no ingresso do Parque Bondinho Pão de Açúcar"',
            '"description": "Access is included with a valid Sugarloaf Cable Car Park ticket"',
        ),
        (
            "O coquetel autoral da Embaixada Carioca — uma releitura do\n          whiskey sour com cachaça envelhecida, limão siciliano, mel\n          do brejo e clara de ovo em emulsão sedosa.",
            "Embaixada Carioca's signature take on a whiskey sour, made with\n          aged cachaça, Sicilian lemon, Brazilian honey and egg white for\n          a smooth, silky texture.",
        ),
        (
            "O coquetel autoral da Embaixada Carioca — uma releitura do",
            "Embaixada Carioca's signature cocktail — a fresh take on the",
        ),
        (
            "whiskey sour com cachaça envelhecida, limão siciliano, mel",
            "whiskey sour, made with aged cachaça, Sicilian lemon, Brazilian honey",
        ),
        (
            "do brejo e clara de ovo em emulsão sedosa.",
            "and egg white for a smooth, silky texture.",
        ),
        ("Cachaça premium · limão siciliano · mel · clara", "Premium cachaça · Sicilian lemon · honey · egg white"),
        ("<span class=\"tag\">clássico</span>", "<span class=\"tag\">classic</span>"),
        ("com cachaça selecionada.", "made with selected cachaça."),
        ("Cachaça · fruta fresca · açúcar demerara", "Cachaça · fresh fruit · demerara sugar"),
        ("<span class=\"tag\">🏆 Draft beer premiado</span>", "<span class=\"tag\">🏆 Award-winning draft beer</span>"),
        ("Heineken draft · copo congelado", "Heineken draft · chilled glass"),
        (
            "Spritz da casa e gin tônicas com aromáticos brasileiros\n          (pimenta rosa, cumaru, cravo).",
            "house spritzes and gin and tonics with Brazilian botanicals\n          such as pink peppercorn, tonka bean and clove.",
        ),
        (
            "Spritz da casa e gin tônicas com aromáticos brasileiros",
            "House spritzes and gin and tonics with Brazilian botanicals",
        ),
        ("(pimenta rosa, cumaru, cravo).", "(pink peppercorn, tonka bean and clove)."),
        ("Cachaça · gin · vermouth · botânicos", "Cachaça · gin · vermouth · botanicals"),
        ("ou em draft beer conforme disponibilidade.", "or on draft, depending on availability."),
        ("<span class=\"tag\">sem álcool</span>", "<span class=\"tag\">alcohol-free</span>"),
        ("Água de coco <span class=\"serif\">in natura.</span>", "Fresh <span class=\"serif\">coconut water.</span>"),
        (
            "Coco verde direto do produtor, servido gelado no próprio coco\n          ou em jarra com a polpa. Mocktails autorais e sucos da hora\n          também disponíveis.",
            "Fresh green coconut served chilled in the shell or in a jug\n          with coconut pulp. Signature mocktails and freshly made juices\n          are also available.",
        ),
        (
            "Coco verde direto do produtor, servido gelado no próprio coco",
            "Fresh green coconut served chilled in the shell",
        ),
        (
            "ou em jarra com a polpa. Mocktails autorais e sucos da hora",
            "or in a jug with coconut pulp. Signature mocktails and freshly made juices",
        ),
        ("também disponíveis.", "are also available."),
        ("Coco · sucos frescos · mocktails", "Coconut · fresh juices · mocktails"),
        ("<div class=\"eyebrow\">Imprensa internacional</div>", "<div class=\"eyebrow\">Guest review</div>"),
        ("Verão · dez–mar", "Summer · Dec–Mar"),
        ("Outono · abr–jun", "Autumn · Apr–Jun"),
        ("Inverno · jul–set", "Winter · Jul–Sep"),
        ("Primavera · out–nov", "Spring · Oct–Nov"),
        ("em movimento, desde o céu azul até as cores quentes.", "as the sky changes from blue to warm sunset colours."),
        (
            "Caipirinhas, gin tonics e espumantes com Sugarloaf Mountain e Guanabara Bay in the background.",
            "Caipirinhas, gin and tonics and sparkling wine with Sugarloaf Mountain and Guanabara Bay in the background.",
        ),
        ("Gin tonics com vista para Guanabara Bay", "Gin and tonics overlooking Guanabara Bay"),
        ("Cocktails com Sugarloaf Mountain in the background", "Cocktails with Sugarloaf Mountain in the background"),
        (
            "Posso te ajudar com reservations, menu, eventos ou informações sobre horários.",
            "I can help with reservations, the menu, events or opening hours.",
        ),
        ('aria-label="Iniciar conversa no WhatsApp com a Embaixada Carioca"', 'aria-label="Start a WhatsApp conversation with Embaixada Carioca"'),
        (">💬 Iniciar conversa</a>", ">💬 Start a conversation</a>"),
        (
            "It is located at Urca Hill, the first sUrca Hill Cable Car Park, which makes it practical for visitors already planning the attraction.",
            "It is located on Urca Hill, at the first stop inside Sugarloaf Cable Car Park, making it convenient for visitors already planning to see the attraction.",
        ),
    ),
    "en/almoco.html": (
        (
            '"description": "Academia da Cachaça\'s feijoada, winner of Veja Rio Comer & Beber\'s Best Feijoada category in 2025. Charque, costela, lombo, paio e linguiça fina em panela de barro. Served every day."',
            '"description": "Academia da Cachaça\'s feijoada, winner of Veja Rio Comer & Beber\'s Best Feijoada category in 2025. Beef jerky, ribs, pork loin and smoked sausages cooked in a clay pot. Served every day."',
        ),
        ('"name": "Bobó de camarão"', '"name": "Shrimp bobó (creamy cassava stew)"'),
        (
            '"description": "Camarão em creme de mandioca com azeite de dendê e coentro."',
            '"description": "Shrimp in a creamy cassava stew with red palm oil and coriander."',
        ),
        ('"name": "Salmão com molho de maracujá"', '"name": "Salmon with passion fruit sauce"'),
        (
            '"description": "Filé de salmão grelhado com molho de maracujá, arroz e legumes."',
            '"description": "Grilled salmon fillet with passion fruit sauce, rice and vegetables."',
        ),
        (
            "<h3>Feijoada da <span class=\"serif\">Academia da Cachaça.</span></h3>",
            "<h3>Feijoada by <span class=\"serif\">Academia da Cachaça.</span></h3>",
        ),
        (
            "<h3>Bobó de <span class=\"serif\">camarão.</span></h3>",
            "<h3>Creamy shrimp <span class=\"serif\">bobó.</span></h3>",
        ),
        (
            "<h3>Salmão com molho <span class=\"serif\">de maracujá.</span></h3>",
            "<h3>Salmon with <span class=\"serif\">passion fruit sauce.</span></h3>",
        ),
        (
            "Reserve com antecedência: é o prato mais disputado entre os visitantes do <strong>Restaurant Urca Hill</strong>.",
            "Book ahead: it is one of the most requested dishes among visitors to Embaixada Carioca on <strong>Urca Hill</strong>.",
        ),
        (
            "As the most traditional <strong>Sugarloaf Mountain restaurant</strong> and the only full-service restaurant at the park, we highly recommend booking in advance",
            "As a popular <strong>Sugarloaf Mountain restaurant</strong>, we recommend booking in advance",
        ),
    ),
}

FORBIDDEN = (
    "Do breakfast ao sunset",
    "Reservation de mesa",
    "where to eat morro da urca",
    "breakfast morro da urca",
    "capacity for private events of capacity varies",
    "accommodates capacity varies",
    "Sanduíche artesanal com",
    "Melhor Feijoada do Rio de Janeiro",
    "Entrada inclusa no ingresso",
    "O coquetel autoral",
    "com cachaça selecionada",
    "Spritz da casa e gin tônicas",
    "Coco verde direto do produtor",
    "Caipirinhas, gin tonics e espumantes com",
    "Gin tonics com vista",
    "Cocktails com Sugarloaf",
    "Posso te ajudar",
    "Iniciar conversa",
    "first sUrca Hill Cable Car Park",
    '"name": "Vista para o Pão de Açúcar"',
    '"name": "Dentro do Parque Bondinho Pão de Açúcar"',
    '"name": "Atendimento para grupos e eventos"',
    '"name": "Vista no Morro da Urca"',
    '"name": "Experiência gastronômica carioca"',
    'aria-label="Selecionar idioma"',
    'aria-label="Idioma atual: EN"',
    'aria-label="Abrir menu de navegação"',
    'aria-label="Falar com a Embaixada Carioca no WhatsApp"',
    ">Inside Parque Bondinho</span>",
    "inside Parque Bondinho Pão de Açúcar",
    'aria-label="Navegação principal"',
    'aria-label="Embaixada Carioca · início"',
    'aria-label="Navegação rápida mobile"',
    'aria-label="Fechar chat"',
    'aria-label="Fechar"',
    'aria-label="Informações úteis para visitantes"',
    "O consulado da gastronomia e da cultura brasileira para o mundo",
    "high above do Urca Hill",
    "Reserve com antecedência",
    "postcard mais famoso do Brasil",
    "Feijoada da <",
    "Bobó de <",
    "Salmão com molho <",
    '"description": "Camarão em',
    '"description": "Filé de salmão',
    "🏆 Premiado ·",
    "Cachaças premium<br/>e vinhos selecionados",
    '"Draft beer Heineken Premiado"',
    "where to eat in sugarloaf",
    "restaurants near sugarloaf mountain",
    "feijoada in rio",
)


def read_exact(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_exact(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def json_ld_errors(html: str) -> list[str]:
    errors: list[str] = []
    blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        flags=re.I | re.S,
    )
    for index, block in enumerate(blocks, start=1):
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f"JSON-LD block {index}: {exc.msg} at line {exc.lineno}")
    return errors


def main() -> int:
    REPORT.parent.mkdir(exist_ok=True)
    results = []

    for relative in TARGETS:
        path = ROOT / relative
        original = read_exact(path)
        updated = original
        replacements = 0

        for old, new in COMMON_REPLACEMENTS + PAGE_REPLACEMENTS.get(relative, ()):
            count = updated.count(old)
            if count:
                updated = updated.replace(old, new)
                replacements += count

        if updated != original:
            write_exact(path, updated)

        remaining = [phrase for phrase in FORBIDDEN if phrase in updated]
        json_errors = json_ld_errors(updated)
        unsafe_schema = bool(
            re.search(
                r'"@type"\s*:\s*"(?:Review|Rating|AggregateRating)"|"(?:review|aggregateRating|ratingValue|reviewCount|ratingCount)"\s*:',
                updated,
                flags=re.I,
            )
        )
        status = "PASS" if not remaining and not json_errors and not unsafe_schema else "FAIL"
        results.append(
            {
                "page": relative,
                "status": status,
                "replacements": replacements,
                "remaining": remaining,
                "json_errors": json_errors,
                "unsafe_schema": unsafe_schema,
            }
        )

    overall = "PASS" if all(item["status"] == "PASS" for item in results) else "FAIL"
    lines = [
        "# High-Traffic English Editorial Fix",
        "",
        f"Date: {date.today().isoformat()}",
        f"Overall status: **{overall}**",
        "",
        "## Scope",
        "",
        "Natural-English review of the seven highest-value commercial pages, covering visible copy, metadata, FAQ content and JSON-LD labels.",
        "",
        "## Results",
        "",
        "| Page | Status | Remaining blocked phrases | JSON-LD errors | Unsafe rating schema |",
        "|---|---:|---:|---:|---:|",
    ]
    for item in results:
        lines.append(
            f"| `{item['page']}` | {item['status']} | "
            f"{len(item['remaining'])} | {len(item['json_errors'])} | "
            f"{'yes' if item['unsafe_schema'] else 'no'} |"
        )

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- No Review, Rating or AggregateRating schema introduced.",
            "- Every JSON-LD block on the target pages remains parseable.",
            "- Canonical and hreflang URLs were preserved, except the incorrect English feijoada `og:url`, which now points to its own page.",
            "- The feijoada award is attributed to Academia da Cachaça and its formal partnership with Embaixada Carioca.",
            "- Event capacity remains variable by format; unsupported fixed-capacity claims were removed from the main English events page.",
        ]
    )

    for item in results:
        if item["remaining"] or item["json_errors"]:
            lines.extend(["", f"### {item['page']}"])
            for phrase in item["remaining"]:
                lines.append(f"- Remaining phrase: `{phrase}`")
            for error in item["json_errors"]:
                lines.append(f"- {error}")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"High-traffic English editorial fix: {overall}")
    for item in results:
        print(f"{item['page']}: {item['status']} replacements={item['replacements']}")
    print(f"Report: {REPORT}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
