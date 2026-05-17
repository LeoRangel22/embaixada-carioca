#!/usr/bin/env python3
"""
fix_keywords_seo.py
Corrige titles, meta descriptions, H1 e alt texts de imagens-chave
em todas as páginas PT, EN e ES para atingir 6 estrelas nas keywords prioritárias.
"""
from bs4 import BeautifulSoup
import os, re, copy

# ─────────────────────────────────────────────────────────────────────
# MAPA DE CORREÇÕES POR PÁGINA
# ─────────────────────────────────────────────────────────────────────
FIXES = {
    # ── PT ──────────────────────────────────────────────────────────
    'index.html': {
        'title': 'Restaurante Morro da Urca com Vista para o Pão de Açúcar | Embaixada Carioca',
        'desc':  'Restaurante do Bondinho no Rio de Janeiro. Café da manhã, almoço e entardecer com vista 360° para o Pão de Açúcar, Baía de Guanabara e Cristo Redentor. Reserve agora.',
        'og_title': 'Restaurante Morro da Urca com Vista para o Pão de Açúcar | Embaixada Carioca',
        'og_desc':  'Restaurante do Bondinho no Rio de Janeiro. Café da manhã, almoço e entardecer com vista 360° para o Pão de Açúcar, Baía de Guanabara e Cristo Redentor.',
        'h1_old': None,  # não alterar H1 da home
        'h1_new': None,
        'alt_updates': {
            'hero': 'Vista do Pão de Açúcar a partir do salão da Embaixada Carioca, restaurante do Bondinho no Morro da Urca',
            'hero-800w': 'Vista do Pão de Açúcar a partir do salão da Embaixada Carioca, restaurante do Bondinho no Morro da Urca',
        }
    },
    'almoco.html': {
        'title': 'Almoço com Vista no Bondinho do Pão de Açúcar | Embaixada Carioca – Urca',
        'desc':  'Um dos restaurantes com melhor vista do Rio de Janeiro. Gastronomia brasileira premiada no Morro da Urca, dentro do Bondinho Pão de Açúcar. Seg–Sex 12h–16h, Sáb–Dom 12h–17h. Reservas online.',
        'og_title': 'Almoço com Vista no Bondinho do Pão de Açúcar | Embaixada Carioca',
        'og_desc':  'Gastronomia brasileira premiada no Morro da Urca. Almoço dentro do Bondinho Pão de Açúcar com vista 360°. Reservas online.',
        'h1_old': 'Almoço premiado no Pão de Açúcar',
        'h1_new': 'Almoço premiado no Bondinho do Pão de Açúcar',
        'alt_updates': {
            'fabio-almoco-salmao-pao-acucar': 'Salmão grelhado com arroz e suco de laranja, com o Pão de Açúcar e o Bondinho ao fundo – Embaixada Carioca, Morro da Urca',
        }
    },
    'cafe-da-manha.html': {
        'title': 'Café da Manhã com Vista para o Pão de Açúcar | Embaixada Carioca – Urca, RJ',
        'desc':  'Café da manhã com vista incrível no Morro da Urca, Rio de Janeiro. Buffet completo e à la carte com a melhor vista do Rio. Todos os dias das 8h às 11h. Reserve sua mesa.',
        'og_title': 'Café da Manhã com Vista para o Pão de Açúcar | Embaixada Carioca',
        'og_desc':  'O café da manhã mais bonito do Rio. Buffet completo com vista para o Pão de Açúcar no Morro da Urca. Todos os dias das 8h às 11h.',
        'h1_old': None,
        'h1_new': None,
        'alt_updates': {}
    },
    'entardecer.html': {
        'title': 'Restaurante Romântico no Rio de Janeiro | Entardecer com Vista – Embaixada Carioca',
        'desc':  'Drinks autorais, petiscos e pôr do sol sobre o Pão de Açúcar. O lugar mais romântico do Rio de Janeiro com música ao vivo no Morro da Urca. Reserve o seu horário.',
        'og_title': 'Entardecer Romântico no Rio | Drinks com Vista para o Pão de Açúcar',
        'og_desc':  'Drinks, petiscos e pôr do sol sobre o Pão de Açúcar. O entardecer mais romântico do Rio de Janeiro, com música ao vivo no Morro da Urca.',
        'h1_old': 'Entardecer no Morro da Urca',
        'h1_new': 'Entardecer Romântico no Morro da Urca',
        'alt_updates': {}
    },
    'eventos.html': {
        'title': 'Espaço para Eventos no Rio de Janeiro | Vista Panorâmica – Embaixada Carioca',
        'desc':  'Espaço para eventos corporativos, aniversários e experiências gastronômicas com vista 360° no Rio de Janeiro. Capacidade para 300+ convidados no Morro da Urca. Solicite orçamento.',
        'og_title': 'Espaço para Eventos com Vista Panorâmica | Rio de Janeiro – Embaixada Carioca',
        'og_desc':  'Eventos corporativos e festas com vista 360° para o Pão de Açúcar no Morro da Urca. Capacidade para 300+ convidados.',
        'h1_old': None,
        'h1_new': None,
        'alt_updates': {}
    },
    'feijoada.html': {
        'title': 'Feijoada Premiada no Morro da Urca | Embaixada Carioca – Rio de Janeiro',
        'desc':  'A feijoada eleita melhor do Brasil pela Revista Prazeres da Mesa. Todos os dias no Morro da Urca, dentro do Bondinho Pão de Açúcar, com vista panorâmica. Reserve sua mesa.',
        'og_title': 'Feijoada Premiada no Morro da Urca | Embaixada Carioca',
        'og_desc':  'A feijoada eleita melhor do Brasil. Todos os dias no Bondinho Pão de Açúcar, com vista para o Rio de Janeiro.',
        'h1_old': 'Feijoada premiada',
        'h1_new': 'Feijoada Premiada no Morro da Urca',
        'alt_updates': {}
    },
    'cardapio.html': {
        'title': 'Cardápio | Restaurante no Bondinho Pão de Açúcar – Embaixada Carioca, Urca',
        'desc':  'Picanha na chapa, feijoada premiada, escondidinho, frutos do mar e sobremesas autorais. Cardápio completo do restaurante do Bondinho Pão de Açúcar em Urca, Rio de Janeiro.',
        'og_title': 'Cardápio | Restaurante no Bondinho Pão de Açúcar – Embaixada Carioca',
        'og_desc':  'Picanha, feijoada premiada e gastronomia brasileira contemporânea. Cardápio completo do restaurante do Bondinho Pão de Açúcar na Urca.',
        'h1_old': 'Cardápio completo',
        'h1_new': 'Cardápio completo – Embaixada Carioca, Morro da Urca',
        'alt_updates': {}
    },
    'guia-do-rio.html': {
        'title': 'Onde Comer no Rio de Janeiro | Guia Completo de Restaurantes – Embaixada Carioca',
        'desc':  'Onde comer no Rio de Janeiro: os melhores restaurantes, praias, museus e o que fazer na cidade. Guia completo com dicas de quem vive no Morro da Urca.',
        'og_title': 'Onde Comer no Rio de Janeiro | Guia Completo – Embaixada Carioca',
        'og_desc':  'Guia completo do Rio de Janeiro: melhores restaurantes, praias, mirantes e dicas para turistas. Curadoria da Embaixada Carioca no Morro da Urca.',
        'h1_old': None,
        'h1_new': None,
        'alt_updates': {}
    },
    # ── EN ──────────────────────────────────────────────────────────
    'en/index.html': {
        'title': 'Restaurant at Sugarloaf Mountain Cable Car | Embaixada Carioca – Rio de Janeiro',
        'desc':  'The only restaurant inside Parque Bondinho Pão de Açúcar, at 227m altitude on Urca Hill. Breakfast, lunch and sunset drinks with 360° views. Book your table.',
        'og_title': 'Restaurant at Sugarloaf Mountain Cable Car | Embaixada Carioca',
        'og_desc':  'The only restaurant inside Parque Bondinho Pão de Açúcar. Breakfast, lunch and sunset with 360° views of Sugarloaf, Guanabara Bay and Christ the Redeemer.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    'en/almoco.html': {
        'title': 'Lunch with Sugarloaf Mountain View | Embaixada Carioca – Urca, Rio',
        'desc':  'Award-winning Brazilian cuisine at 227m altitude inside the Sugarloaf cable car park. Lunch with panoramic views Mon–Fri 12–4pm, Sat–Sun 12–5pm. Book online.',
        'og_title': 'Lunch at Sugarloaf Mountain Cable Car | Embaixada Carioca',
        'og_desc':  'Award-winning Brazilian cuisine inside Parque Bondinho Pão de Açúcar. Lunch with panoramic views of Sugarloaf Mountain.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    'en/cafe-da-manha.html': {
        'title': 'Breakfast with Sugarloaf Mountain View | Embaixada Carioca – Urca, Rio',
        'desc':  'The most beautiful breakfast in Rio de Janeiro. Full buffet and à la carte with a stunning view of Sugarloaf Mountain on Urca Hill. Every day from 8am to 11am.',
        'og_title': 'Breakfast with Sugarloaf Mountain View | Embaixada Carioca',
        'og_desc':  'The most beautiful breakfast in Rio. Full buffet with Sugarloaf Mountain view on Urca Hill. Every day from 8am to 11am.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    'en/entardecer.html': {
        'title': 'Romantic Restaurant Rio de Janeiro | Sunset Drinks – Embaixada Carioca',
        'desc':  'Craft cocktails, snacks and sunset over Sugarloaf Mountain. The most romantic spot in Rio de Janeiro with live music on Urca Hill. Book your table.',
        'og_title': 'Romantic Sunset at Sugarloaf Mountain | Embaixada Carioca Rio',
        'og_desc':  'Craft cocktails and sunset over Sugarloaf Mountain. The most romantic spot in Rio de Janeiro with live music on Urca Hill.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    'en/eventos.html': {
        'title': 'Event Venue Rio de Janeiro | Panoramic View – Embaixada Carioca',
        'desc':  'Corporate events, private parties and gastronomic experiences with 360° views in Rio de Janeiro. Capacity for 300+ guests on Urca Hill. Request a quote.',
        'og_title': 'Event Venue with Panoramic View | Rio de Janeiro – Embaixada Carioca',
        'og_desc':  'Corporate events and private parties with 360° views of Sugarloaf Mountain. Capacity for 300+ guests on Urca Hill.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    'en/feijoada.html': {
        'title': 'Best Feijoada in Rio de Janeiro | Sugarloaf Mountain – Embaixada Carioca',
        'desc':  'Award-winning feijoada, voted best in Brazil by Prazeres da Mesa magazine. Every day inside Parque Bondinho Pão de Açúcar with panoramic views. Book your table.',
        'og_title': 'Award-Winning Feijoada at Sugarloaf Mountain | Embaixada Carioca',
        'og_desc':  'The best feijoada in Brazil, every day inside Parque Bondinho Pão de Açúcar with panoramic views of Rio de Janeiro.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    'en/cardapio.html': {
        'title': 'Menu | Restaurant at Sugarloaf Cable Car – Embaixada Carioca, Urca',
        'desc':  'Grilled picanha, award-winning feijoada, seafood and signature desserts. Full menu of the restaurant inside Parque Bondinho Pão de Açúcar in Urca, Rio de Janeiro.',
        'og_title': 'Menu | Restaurant at Sugarloaf Cable Car – Embaixada Carioca',
        'og_desc':  'Grilled picanha, award-winning feijoada and Brazilian contemporary cuisine. Full menu of the restaurant inside Parque Bondinho Pão de Açúcar.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    'en/guia-do-rio.html': {
        'title': 'Best Restaurants in Rio de Janeiro | Complete Guide – Embaixada Carioca',
        'desc':  'Where to eat in Rio de Janeiro: the best restaurants, beaches, viewpoints and tips for tourists. Complete guide curated by Embaixada Carioca on Urca Hill.',
        'og_title': 'Best Restaurants in Rio de Janeiro | Complete Guide – Embaixada Carioca',
        'og_desc':  'Complete guide to Rio de Janeiro: best restaurants, beaches, viewpoints and tips for tourists. Curated by Embaixada Carioca on Urca Hill.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    # ── ES ──────────────────────────────────────────────────────────
    'es/index.html': {
        'title': 'Restaurante en el Teleférico Pan de Azúcar | Embaixada Carioca – Río de Janeiro',
        'desc':  'El único restaurante dentro del Parque Bondinho Pão de Açúcar, a 227m de altitud en el Morro da Urca. Desayuno, almuerzo y atardecer con vistas de 360°. Reserve su mesa.',
        'og_title': 'Restaurante en el Teleférico Pan de Azúcar | Embaixada Carioca',
        'og_desc':  'El único restaurante dentro del Parque Bondinho Pão de Açúcar. Desayuno, almuerzo y atardecer con vistas de 360° al Pan de Azúcar y la Bahía de Guanabara.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    'es/almoco.html': {
        'title': 'Almuerzo con Vista al Pan de Azúcar | Embaixada Carioca – Urca, Río',
        'desc':  'Gastronomía brasileña premiada a 227m de altitud dentro del teleférico Pan de Azúcar. Almuerzo con vistas panorámicas. Lun–Vie 12–16h, Sáb–Dom 12–17h. Reserve online.',
        'og_title': 'Almuerzo en el Teleférico Pan de Azúcar | Embaixada Carioca',
        'og_desc':  'Gastronomía brasileña premiada dentro del Parque Bondinho Pão de Açúcar. Almuerzo con vistas panorámicas al Pan de Azúcar.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    'es/cafe-da-manha.html': {
        'title': 'Desayuno con Vista al Pan de Azúcar | Embaixada Carioca – Urca, Río',
        'desc':  'El desayuno más bonito de Río de Janeiro. Buffet completo y à la carte con vistas al Pan de Azúcar en el Morro da Urca. Todos los días de 8h a 11h.',
        'og_title': 'Desayuno con Vista al Pan de Azúcar | Embaixada Carioca',
        'og_desc':  'El desayuno más bonito de Río. Buffet completo con vistas al Pan de Azúcar en el Morro da Urca. Todos los días de 8h a 11h.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    'es/entardecer.html': {
        'title': 'Restaurante Romántico Río de Janeiro | Atardecer con Vista – Embaixada Carioca',
        'desc':  'Cócteles artesanales, tapas y puesta de sol sobre el Pan de Azúcar. El lugar más romántico de Río de Janeiro con música en vivo en el Morro da Urca. Reserve su mesa.',
        'og_title': 'Atardecer Romántico en el Pan de Azúcar | Embaixada Carioca Río',
        'og_desc':  'Cócteles y puesta de sol sobre el Pan de Azúcar. El lugar más romántico de Río de Janeiro con música en vivo en el Morro da Urca.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    'es/eventos.html': {
        'title': 'Espacio para Eventos en Río de Janeiro | Vista Panorámica – Embaixada Carioca',
        'desc':  'Eventos corporativos, fiestas privadas y experiencias gastronómicas con vistas de 360° en Río de Janeiro. Capacidad para 300+ invitados en el Morro da Urca.',
        'og_title': 'Espacio para Eventos con Vista Panorámica | Río de Janeiro – Embaixada Carioca',
        'og_desc':  'Eventos corporativos y fiestas con vistas de 360° al Pan de Azúcar. Capacidad para 300+ invitados en el Morro da Urca.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    'es/feijoada.html': {
        'title': 'Mejor Feijoada de Río de Janeiro | Pan de Azúcar – Embaixada Carioca',
        'desc':  'Feijoada premiada, elegida la mejor de Brasil por la revista Prazeres da Mesa. Todos los días dentro del Parque Bondinho Pão de Açúcar con vistas panorámicas.',
        'og_title': 'Feijoada Premiada en el Pan de Azúcar | Embaixada Carioca',
        'og_desc':  'La mejor feijoada de Brasil, todos los días dentro del Parque Bondinho Pão de Açúcar con vistas panorámicas de Río de Janeiro.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    'es/cardapio.html': {
        'title': 'Carta | Restaurante en el Teleférico Pan de Azúcar – Embaixada Carioca, Urca',
        'desc':  'Picanha a la parrilla, feijoada premiada, mariscos y postres de autor. Carta completa del restaurante dentro del Parque Bondinho Pão de Açúcar en Urca, Río de Janeiro.',
        'og_title': 'Carta | Restaurante en el Teleférico Pan de Azúcar – Embaixada Carioca',
        'og_desc':  'Picanha a la parrilla, feijoada premiada y gastronomía brasileña contemporánea. Carta completa del restaurante dentro del Parque Bondinho Pão de Açúcar.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
    'es/guia-do-rio.html': {
        'title': 'Dónde Comer en Río de Janeiro | Guía Completa – Embaixada Carioca',
        'desc':  'Dónde comer en Río de Janeiro: los mejores restaurantes, playas, miradores y consejos para turistas. Guía completa elaborada por Embaixada Carioca en el Morro da Urca.',
        'og_title': 'Dónde Comer en Río de Janeiro | Guía Completa – Embaixada Carioca',
        'og_desc':  'Guía completa de Río de Janeiro: mejores restaurantes, playas, miradores y consejos para turistas. Elaborada por Embaixada Carioca en el Morro da Urca.',
        'h1_old': None, 'h1_new': None, 'alt_updates': {}
    },
}

# ─────────────────────────────────────────────────────────────────────
# PARQUE BONDINHO PAGE (PT, EN, ES)
# ─────────────────────────────────────────────────────────────────────
FIXES['parque-bondinho.html'] = {
    'title': 'Parque Bondinho Pão de Açúcar | Restaurante com Vista – Embaixada Carioca',
    'desc':  'Restaurante dentro do Parque Bondinho Pão de Açúcar no Morro da Urca. Café da manhã, almoço e entardecer com vista para o Pão de Açúcar. Única opção com reservas.',
    'og_title': 'Parque Bondinho Pão de Açúcar | Restaurante com Vista – Embaixada Carioca',
    'og_desc':  'O único restaurante com reservas dentro do Parque Bondinho Pão de Açúcar. Café da manhã, almoço e entardecer no Morro da Urca.',
    'h1_old': None, 'h1_new': None, 'alt_updates': {}
}
FIXES['en/parque-bondinho.html'] = {
    'title': 'Parque Bondinho Pão de Açúcar | Restaurant with View – Embaixada Carioca',
    'desc':  'The only restaurant with reservations inside Parque Bondinho Pão de Açúcar on Urca Hill. Breakfast, lunch and sunset drinks with Sugarloaf Mountain view.',
    'og_title': 'Parque Bondinho Pão de Açúcar | Restaurant with View – Embaixada Carioca',
    'og_desc':  'The only restaurant with reservations inside Parque Bondinho Pão de Açúcar. Breakfast, lunch and sunset on Urca Hill.',
    'h1_old': None, 'h1_new': None, 'alt_updates': {}
}
FIXES['es/parque-bondinho.html'] = {
    'title': 'Parque Bondinho Pão de Açúcar | Restaurante con Vista – Embaixada Carioca',
    'desc':  'El único restaurante con reservas dentro del Parque Bondinho Pão de Açúcar en el Morro da Urca. Desayuno, almuerzo y atardecer con vistas al Pan de Azúcar.',
    'og_title': 'Parque Bondinho Pão de Açúcar | Restaurante con Vista – Embaixada Carioca',
    'og_desc':  'El único restaurante con reservas dentro del Parque Bondinho Pão de Açúcar. Desayuno, almuerzo y atardecer en el Morro da Urca.',
    'h1_old': None, 'h1_new': None, 'alt_updates': {}
}

# ─────────────────────────────────────────────────────────────────────
# APLICAR CORREÇÕES
# ─────────────────────────────────────────────────────────────────────
fixed = 0
skipped = 0

for filepath, fix in FIXES.items():
    if not os.path.exists(filepath):
        skipped += 1
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    changed = False

    # 1. Title
    title_tag = soup.find('title')
    if title_tag and title_tag.text.strip() != fix['title']:
        title_tag.string = fix['title']
        changed = True

    # 2. Meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        if meta_desc.get('content', '') != fix['desc']:
            meta_desc['content'] = fix['desc']
            changed = True
    else:
        # Criar meta description se não existir
        new_meta = soup.new_tag('meta', attrs={'name': 'description', 'content': fix['desc']})
        if soup.head:
            soup.head.append(new_meta)
            changed = True

    # 3. OG title
    og_title = soup.find('meta', property='og:title')
    if og_title and fix.get('og_title'):
        if og_title.get('content', '') != fix['og_title']:
            og_title['content'] = fix['og_title']
            changed = True

    # 4. OG description
    og_desc = soup.find('meta', property='og:description')
    if og_desc and fix.get('og_desc'):
        if og_desc.get('content', '') != fix['og_desc']:
            og_desc['content'] = fix['og_desc']
            changed = True

    # 5. Twitter title
    tw_title = soup.find('meta', attrs={'name': 'twitter:title'})
    if tw_title and fix.get('og_title'):
        tw_title['content'] = fix['og_title']
        changed = True

    # 6. Twitter description
    tw_desc = soup.find('meta', attrs={'name': 'twitter:description'})
    if tw_desc and fix.get('og_desc'):
        tw_desc['content'] = fix['og_desc']
        changed = True

    # 7. H1 (se especificado)
    if fix.get('h1_old') and fix.get('h1_new'):
        for h1 in soup.find_all('h1'):
            h1_text = h1.get_text(strip=True)
            if fix['h1_old'].lower() in h1_text.lower():
                # Substituir apenas o texto, preservando tags internas
                new_text = h1_text.replace(fix['h1_old'], fix['h1_new'])
                # Se H1 tem apenas texto simples
                if len(h1.contents) == 1 and isinstance(h1.contents[0], str):
                    h1.string = fix['h1_new']
                    changed = True
                break

    # 8. Alt texts de imagens-chave
    if fix.get('alt_updates'):
        for img in soup.find_all('img'):
            src = img.get('src', '') + img.get('srcset', '')
            for key, new_alt in fix['alt_updates'].items():
                if key in src:
                    if img.get('alt', '') != new_alt:
                        img['alt'] = new_alt
                        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        fixed += 1
        print(f"✅ {filepath}")
    else:
        print(f"⏭️  {filepath} (sem alterações)")

print(f"\n{'='*50}")
print(f"Arquivos corrigidos: {fixed}")
print(f"Arquivos pulados:    {skipped}")
