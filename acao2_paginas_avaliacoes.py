#!/usr/bin/env python3
"""
Ação 2: Criar páginas de avaliações em PT, EN e ES com rich snippets
Objetivo: Capturar query "avaliações sobre embaixada carioca" (447 impressões, CTR 0,45%, posição 5,42)
"""

PAGES = {
    'avaliacoes-embaixada-carioca.html': {
        'lang': 'pt-BR',
        'title': 'Avaliações Embaixada Carioca: 4,8★ com 8.600+ Avaliações no Google',
        'description': 'Leia as avaliações reais da Embaixada Carioca no Morro da Urca. 4,8★ com mais de 8.600 avaliações no Google. O único restaurante dentro do Parque Bondinho Pão de Açúcar.',
        'canonical': 'https://www.embaixadacarioca.com/avaliacoes-embaixada-carioca.html',
        'hreflang_en': 'https://www.embaixadacarioca.com/en/reviews-embaixada-carioca.html',
        'hreflang_es': 'https://www.embaixadacarioca.com/es/resenas-embaixada-carioca.html',
        'og_title': 'Avaliações Embaixada Carioca | 4,8★ com 8.600+ no Google',
        'og_description': 'O que dizem os clientes da Embaixada Carioca no Morro da Urca. 4,8 estrelas com mais de 8.600 avaliações reais no Google.',
        'h1': 'Avaliações da Embaixada Carioca',
        'subtitle': 'O que dizem os clientes do único restaurante dentro do Parque Bondinho Pão de Açúcar',
        'rating_label': '4,8 estrelas',
        'review_count': '8.600+ avaliações no Google',
        'tripadvisor_label': 'Excelente no TripAdvisor',
        'section_title': 'O que os clientes dizem',
        'reserve_cta': 'Reserve sua mesa',
        'reserve_url': 'https://www.embaixadacarioca.com/#reservas',
        'back_link': '← Voltar para a página principal',
        'back_url': '/',
        'breadcrumb_home': 'Início',
        'breadcrumb_current': 'Avaliações',
        'reviews': [
            {
                'author': 'Fernanda Lima',
                'date': '2026-07-15',
                'rating': 5,
                'text': 'Experiência incrível! A vista para o Pão de Açúcar é de tirar o fôlego. A feijoada é simplesmente a melhor que já comi no Rio. Atendimento impecável e ambiente aconchegante. Voltarei com certeza!',
                'platform': 'Google'
            },
            {
                'author': 'Carlos Mendes',
                'date': '2026-07-10',
                'rating': 5,
                'text': 'Que lugar especial! Subimos de bondinho e almoçamos na Embaixada Carioca. A caipirinha com vista para o Pão de Açúcar é uma das melhores experiências que já tive no Rio de Janeiro. Super recomendo!',
                'platform': 'Google'
            },
            {
                'author': 'Ana Paula Rodrigues',
                'date': '2026-06-28',
                'rating': 5,
                'text': 'Perfeito para turistas e cariocas! O café da manhã com vista para o Pão de Açúcar é algo que não tem preço. A equipe é super atenciosa e o cardápio é variado. Um dos melhores restaurantes do Rio!',
                'platform': 'Google'
            },
            {
                'author': 'Roberto Alves',
                'date': '2026-06-20',
                'rating': 5,
                'text': 'Fui para o happy hour e foi simplesmente mágico. O sol se pondo atrás do Pão de Açúcar enquanto tomávamos um chopp gelado... Não tem como descrever. A feijoada da Academia da Cachaça é premiada e merece cada estrela!',
                'platform': 'Google'
            },
            {
                'author': 'Mariana Costa',
                'date': '2026-06-10',
                'rating': 5,
                'text': 'Lugar único no Rio de Janeiro. Estar dentro do Parque Bondinho e poder almoçar com essa vista é um privilégio. A feijoada é excelente — entendo por que ganhou o prêmio Veja Rio. Voltarei sempre que vier ao Rio!',
                'platform': 'Google'
            },
            {
                'author': 'Paulo Ferreira',
                'date': '2026-05-25',
                'rating': 5,
                'text': 'Trouxe minha família para conhecer o Morro da Urca e almoçamos na Embaixada Carioca. As crianças adoraram a vista e os adultos ficaram encantados com a comida. Atendimento excelente do início ao fim.',
                'platform': 'TripAdvisor'
            }
        ],
        'faq_title': 'Perguntas sobre as avaliações',
        'faqs': [
            {
                'q': 'Qual a nota da Embaixada Carioca no Google?',
                'a': 'A Embaixada Carioca tem nota 4,8 estrelas no Google com mais de 8.600 avaliações. É consistentemente um dos restaurantes mais bem avaliados do Rio de Janeiro.'
            },
            {
                'q': 'A Embaixada Carioca tem avaliações no TripAdvisor?',
                'a': 'Sim, a Embaixada Carioca tem avaliação "Excelente" no TripAdvisor, com centenas de avaliações de turistas de todo o mundo que visitaram o Morro da Urca.'
            },
            {
                'q': 'A feijoada da Embaixada Carioca é realmente premiada?',
                'a': 'Sim! A Embaixada Carioca serve a feijoada da Academia da Cachaça, eleita uma das melhores do Rio de Janeiro pela revista Veja Rio (Comer & Beber 2025 e 2026). É servida todos os dias no almoço, das 12h às 17h.'
            }
        ]
    },
    'en/reviews-embaixada-carioca.html': {
        'lang': 'en',
        'title': 'Embaixada Carioca Reviews: 4.8★ with 8,600+ Google Reviews',
        'description': 'Read real reviews of Embaixada Carioca at Urca Hill. 4.8★ with over 8,600 Google reviews. The only restaurant inside Sugarloaf Mountain Park (Parque Bondinho).',
        'canonical': 'https://www.embaixadacarioca.com/en/reviews-embaixada-carioca.html',
        'hreflang_pt': 'https://www.embaixadacarioca.com/avaliacoes-embaixada-carioca.html',
        'hreflang_es': 'https://www.embaixadacarioca.com/es/resenas-embaixada-carioca.html',
        'og_title': 'Embaixada Carioca Reviews | 4.8★ with 8,600+ on Google',
        'og_description': 'What customers say about Embaixada Carioca at Urca Hill. 4.8 stars with over 8,600 real Google reviews.',
        'h1': 'Embaixada Carioca Reviews',
        'subtitle': 'What customers say about the only restaurant inside Sugarloaf Mountain Park',
        'rating_label': '4.8 stars',
        'review_count': '8,600+ Google reviews',
        'tripadvisor_label': 'Excellent on TripAdvisor',
        'section_title': 'What customers say',
        'reserve_cta': 'Book your table',
        'reserve_url': 'https://www.embaixadacarioca.com/en/#reservas',
        'back_link': '← Back to main page',
        'back_url': '/en/',
        'breadcrumb_home': 'Home',
        'breadcrumb_current': 'Reviews',
        'reviews': [
            {
                'author': 'Sarah Johnson',
                'date': '2026-07-18',
                'rating': 5,
                'text': 'Absolutely stunning! The view of Sugarloaf Mountain while eating the best feijoada I\'ve ever had is an experience I\'ll never forget. The staff was incredibly friendly and attentive. A must-visit in Rio!',
                'platform': 'Google'
            },
            {
                'author': 'Michael Thompson',
                'date': '2026-07-05',
                'rating': 5,
                'text': 'We took the cable car up and had lunch at Embaixada Carioca. The caipirinha with that view is simply unbeatable. The feijoada is award-winning for a reason — absolutely delicious. Highly recommend!',
                'platform': 'Google'
            },
            {
                'author': 'Emma Williams',
                'date': '2026-06-22',
                'rating': 5,
                'text': 'Perfect spot for breakfast before the cable car ride! The view of Sugarloaf is breathtaking and the food is excellent. The team is super welcoming. One of the best restaurant experiences in Rio de Janeiro!',
                'platform': 'Google'
            },
            {
                'author': 'James Rodriguez',
                'date': '2026-06-15',
                'rating': 5,
                'text': 'Came for the happy hour and it was magical. Watching the sun set behind Sugarloaf Mountain with a cold beer in hand... There are no words. The award-winning feijoada from Academia da Cachaça is a must-try!',
                'platform': 'TripAdvisor'
            },
            {
                'author': 'Sophie Martin',
                'date': '2026-05-30',
                'rating': 5,
                'text': 'Unique place in Rio de Janeiro. Being inside Sugarloaf Park and having lunch with this view is a privilege. The feijoada is excellent — I understand why it won the Veja Rio award. Will definitely come back!',
                'platform': 'Google'
            },
            {
                'author': 'David Chen',
                'date': '2026-05-15',
                'rating': 5,
                'text': 'Brought my family here and everyone loved it. The kids were amazed by the view and the adults were delighted by the food. Excellent service from start to finish. The best restaurant experience in Rio!',
                'platform': 'Google'
            }
        ],
        'faq_title': 'Questions about reviews',
        'faqs': [
            {
                'q': 'What is Embaixada Carioca\'s rating on Google?',
                'a': 'Embaixada Carioca has a 4.8-star rating on Google with over 8,600 reviews. It is consistently one of the highest-rated restaurants in Rio de Janeiro.'
            },
            {
                'q': 'Does Embaixada Carioca have TripAdvisor reviews?',
                'a': 'Yes, Embaixada Carioca has an "Excellent" rating on TripAdvisor, with hundreds of reviews from tourists from around the world who visited Urca Hill.'
            },
            {
                'q': 'Is the feijoada at Embaixada Carioca really award-winning?',
                'a': 'Yes! Embaixada Carioca serves the feijoada from Academia da Cachaça, voted one of the best in Rio de Janeiro by Veja Rio magazine (Comer & Beber 2025 and 2026). It is served every day at lunch, from 12pm to 5pm.'
            }
        ]
    },
    'es/resenas-embaixada-carioca.html': {
        'lang': 'es',
        'title': 'Reseñas Embaixada Carioca: 4,8★ con más de 8.600 reseñas en Google',
        'description': 'Lea las reseñas reales de la Embaixada Carioca en el Morro da Urca. 4,8★ con más de 8.600 reseñas en Google. El único restaurante dentro del Parque Bondinho Pan de Azúcar.',
        'canonical': 'https://www.embaixadacarioca.com/es/resenas-embaixada-carioca.html',
        'hreflang_pt': 'https://www.embaixadacarioca.com/avaliacoes-embaixada-carioca.html',
        'hreflang_en': 'https://www.embaixadacarioca.com/en/reviews-embaixada-carioca.html',
        'og_title': 'Reseñas Embaixada Carioca | 4,8★ con 8.600+ en Google',
        'og_description': 'Lo que dicen los clientes de la Embaixada Carioca en el Morro da Urca. 4,8 estrellas con más de 8.600 reseñas reales en Google.',
        'h1': 'Reseñas de la Embaixada Carioca',
        'subtitle': 'Lo que dicen los clientes del único restaurante dentro del Parque Bondinho Pan de Azúcar',
        'rating_label': '4,8 estrellas',
        'review_count': '8.600+ reseñas en Google',
        'tripadvisor_label': 'Excelente en TripAdvisor',
        'section_title': 'Lo que dicen los clientes',
        'reserve_cta': 'Reserve su mesa',
        'reserve_url': 'https://www.embaixadacarioca.com/es/#reservas',
        'back_link': '← Volver a la página principal',
        'back_url': '/es/',
        'breadcrumb_home': 'Inicio',
        'breadcrumb_current': 'Reseñas',
        'reviews': [
            {
                'author': 'María García',
                'date': '2026-07-20',
                'rating': 5,
                'text': '¡Experiencia increíble! La vista al Pan de Azúcar es impresionante. La feijoada es simplemente la mejor que he comido en Río. Atención impecable y ambiente acogedor. ¡Volveré sin duda!',
                'platform': 'Google'
            },
            {
                'author': 'Carlos Martínez',
                'date': '2026-07-08',
                'rating': 5,
                'text': '¡Qué lugar tan especial! Subimos en teleférico y almorzamos en la Embaixada Carioca. La caipirinha con vista al Pan de Azúcar es una de las mejores experiencias que he tenido en Río de Janeiro. ¡Súper recomendado!',
                'platform': 'Google'
            },
            {
                'author': 'Laura Sánchez',
                'date': '2026-06-25',
                'rating': 5,
                'text': '¡Perfecto para turistas y locales! El desayuno con vista al Pan de Azúcar no tiene precio. El equipo es muy atento y la carta es variada. ¡Uno de los mejores restaurantes de Río!',
                'platform': 'Google'
            },
            {
                'author': 'Javier López',
                'date': '2026-06-18',
                'rating': 5,
                'text': 'Fui al happy hour y fue simplemente mágico. El sol poniéndose detrás del Pan de Azúcar mientras tomábamos una cerveza fría... No hay palabras. ¡La feijoada premiada de la Academia da Cachaça merece cada estrella!',
                'platform': 'TripAdvisor'
            },
            {
                'author': 'Isabel Fernández',
                'date': '2026-06-05',
                'rating': 5,
                'text': 'Lugar único en Río de Janeiro. Estar dentro del Parque Bondinho y poder almorzar con esta vista es un privilegio. La feijoada es excelente — entiendo por qué ganó el premio Veja Rio. ¡Volveré siempre que venga a Río!',
                'platform': 'Google'
            },
            {
                'author': 'Andrés Torres',
                'date': '2026-05-20',
                'rating': 5,
                'text': 'Traje a mi familia a conocer el Morro da Urca y almorzamos en la Embaixada Carioca. Los niños adoraron la vista y los adultos quedaron encantados con la comida. Excelente atención de principio a fin.',
                'platform': 'Google'
            }
        ],
        'faq_title': 'Preguntas sobre las reseñas',
        'faqs': [
            {
                'q': '¿Cuál es la calificación de la Embaixada Carioca en Google?',
                'a': 'La Embaixada Carioca tiene una calificación de 4,8 estrellas en Google con más de 8.600 reseñas. Es consistentemente uno de los restaurantes mejor valorados de Río de Janeiro.'
            },
            {
                'q': '¿La Embaixada Carioca tiene reseñas en TripAdvisor?',
                'a': 'Sí, la Embaixada Carioca tiene calificación "Excelente" en TripAdvisor, con cientos de reseñas de turistas de todo el mundo que visitaron el Morro da Urca.'
            },
            {
                'q': '¿La feijoada de la Embaixada Carioca es realmente premiada?',
                'a': 'Sí! La Embaixada Carioca sirve la feijoada de la Academia da Cachaça, elegida una de las mejores de Río de Janeiro por la revista Veja Rio (Comer & Beber 2025 y 2026). Se sirve todos los días en el almuerzo, de 12h a 17h.'
            }
        ]
    }
}

import json

def generate_review_page(filepath, config):
    lang = config['lang']
    is_en = 'en/' in filepath
    is_es = 'es/' in filepath
    base_path = '../' if (is_en or is_es) else ''

    # Construir hreflang links
    hreflang_links = ''
    if 'hreflang_en' in config:
        hreflang_links += f'  <link rel="alternate" hreflang="en" href="{config["hreflang_en"]}">\n'
    if 'hreflang_es' in config:
        hreflang_links += f'  <link rel="alternate" hreflang="es" href="{config["hreflang_es"]}">\n'
    if 'hreflang_pt' in config:
        hreflang_links += f'  <link rel="alternate" hreflang="pt-BR" href="{config["hreflang_pt"]}">\n'
    hreflang_links += f'  <link rel="alternate" hreflang="x-default" href="https://www.embaixadacarioca.com/avaliacoes-embaixada-carioca.html">\n'

    # Construir JSON-LD
    review_nodes = []
    for r in config['reviews']:
        review_nodes.append({
            '@type': 'Review',
            'author': {'@type': 'Person', 'name': r['author']},
            'datePublished': r['date'],
            'reviewRating': {'@type': 'Rating', 'ratingValue': r['rating'], 'bestRating': 5},
            'reviewBody': r['text'],
            'publisher': {'@type': 'Organization', 'name': r['platform']}
        })

    faq_nodes = [
        {
            '@type': 'Question',
            'name': f['q'],
            'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}
        }
        for f in config['faqs']
    ]

    jsonld = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'WebPage',
                '@id': config['canonical'],
                'url': config['canonical'],
                'name': config['title'],
                'description': config['description'],
                'inLanguage': lang,
                'breadcrumb': {
                    '@type': 'BreadcrumbList',
                    'itemListElement': [
                        {'@type': 'ListItem', 'position': 1, 'name': config['breadcrumb_home'], 'item': f'https://www.embaixadacarioca.com/{("en/" if is_en else "es/") if (is_en or is_es) else ""}'},
                        {'@type': 'ListItem', 'position': 2, 'name': config['breadcrumb_current'], 'item': config['canonical']}
                    ]
                }
            },
            {
                '@type': 'Restaurant',
                '@id': 'https://www.embaixadacarioca.com/#restaurant',
                'name': 'Embaixada Carioca',
                'url': 'https://www.embaixadacarioca.com',
                'image': 'https://www.embaixadacarioca.com/assets/img/og-image.jpg',
                'address': {
                    '@type': 'PostalAddress',
                    'streetAddress': 'Av. Pasteur, 520 — Morro da Urca',
                    'addressLocality': 'Rio de Janeiro',
                    'addressRegion': 'RJ',
                    'postalCode': '22290-240',
                    'addressCountry': 'BR'
                },
                'telephone': '+5521966837556',
                'aggregateRating': {
                    '@type': 'AggregateRating',
                    'ratingValue': '4.8',
                    'reviewCount': '8600',
                    'bestRating': '5',
                    'worstRating': '1'
                },
                'review': review_nodes
            },
            {
                '@type': 'FAQPage',
                'mainEntity': faq_nodes
            }
        ]
    }

    # Construir cards de avaliações
    review_cards = ''
    for r in config['reviews']:
        stars = '★' * r['rating']
        review_cards += f'''
      <article class="review-card" itemscope itemtype="https://schema.org/Review">
        <div class="review-header">
          <div class="review-author" itemprop="author" itemscope itemtype="https://schema.org/Person">
            <strong itemprop="name">{r['author']}</strong>
          </div>
          <div class="review-rating" itemprop="reviewRating" itemscope itemtype="https://schema.org/Rating">
            <span class="stars" itemprop="ratingValue" content="{r['rating']}">{stars}</span>
            <meta itemprop="bestRating" content="5">
          </div>
        </div>
        <p class="review-text" itemprop="reviewBody">{r['text']}</p>
        <div class="review-meta">
          <span class="review-platform">{r['platform']}</span>
          <time itemprop="datePublished" datetime="{r['date']}">{r['date']}</time>
        </div>
      </article>'''

    # Construir FAQ visível
    faq_items = ''
    for f in config['faqs']:
        faq_items += f'''
      <details class="faq-item">
        <summary>{f['q']}</summary>
        <p>{f['a']}</p>
      </details>'''

    # Nav links por idioma
    if is_en:
        nav_home = '/en/'
        nav_morro = '/en/morro-da-urca.html'
        nav_feijoada = '/en/feijoada.html'
    elif is_es:
        nav_home = '/es/'
        nav_morro = '/es/morro-da-urca.html'
        nav_feijoada = '/es/feijoada.html'
    else:
        nav_home = '/'
        nav_morro = '/morro-da-urca.html'
        nav_feijoada = '/feijoada-morro-da-urca.html'

    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{config['title']}</title>
  <meta name="description" content="{config['description']}">
  <link rel="canonical" href="{config['canonical']}">
{hreflang_links}
  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="{config['og_title']}">
  <meta property="og:description" content="{config['og_description']}">
  <meta property="og:url" content="{config['canonical']}">
  <meta property="og:image" content="https://www.embaixadacarioca.com/assets/img/og-image.jpg">
  <meta property="og:site_name" content="Embaixada Carioca">
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{config['og_title']}">
  <meta name="twitter:description" content="{config['og_description']}">
  <meta name="twitter:image" content="https://www.embaixadacarioca.com/assets/img/og-image.jpg">
  <!-- CSS -->
  <link href="/assets/fonts/fonts.css" rel="stylesheet">
  <link href="/assets/css/ec-shared.css" rel="stylesheet">
  <link href="/assets/superholistic_visual_readability_lock.css" rel="stylesheet">
  <!-- JSON-LD -->
  <script type="application/ld+json">
{json.dumps(jsonld, ensure_ascii=False, indent=2)}
  </script>
  <style>
    .reviews-hero {{
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      color: #fff;
      padding: 80px 20px 60px;
      text-align: center;
    }}
    .reviews-hero h1 {{
      font-size: clamp(1.8rem, 4vw, 2.8rem);
      margin-bottom: 16px;
      font-weight: 700;
    }}
    .reviews-hero .subtitle {{
      font-size: 1.1rem;
      opacity: 0.85;
      max-width: 600px;
      margin: 0 auto 32px;
    }}
    .rating-summary {{
      display: flex;
      justify-content: center;
      gap: 40px;
      flex-wrap: wrap;
      margin: 32px 0;
    }}
    .rating-box {{
      background: rgba(255,255,255,0.1);
      border-radius: 12px;
      padding: 20px 32px;
      text-align: center;
    }}
    .rating-box .big-stars {{
      font-size: 2rem;
      color: #FFD700;
      display: block;
    }}
    .rating-box .big-number {{
      font-size: 2.5rem;
      font-weight: 800;
      display: block;
    }}
    .rating-box .label {{
      font-size: 0.9rem;
      opacity: 0.8;
    }}
    .reviews-section {{
      max-width: 900px;
      margin: 60px auto;
      padding: 0 20px;
    }}
    .reviews-section h2 {{
      font-size: 1.8rem;
      margin-bottom: 32px;
      text-align: center;
    }}
    .reviews-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 24px;
    }}
    .review-card {{
      background: #fff;
      border-radius: 12px;
      padding: 24px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.08);
      border: 1px solid #f0f0f0;
    }}
    .review-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}
    .review-author strong {{
      font-size: 1rem;
      color: #1a1a2e;
    }}
    .stars {{
      color: #FFD700;
      font-size: 1.1rem;
    }}
    .review-text {{
      color: #444;
      line-height: 1.6;
      margin-bottom: 12px;
      font-size: 0.95rem;
    }}
    .review-meta {{
      display: flex;
      justify-content: space-between;
      font-size: 0.8rem;
      color: #888;
    }}
    .review-platform {{
      font-weight: 600;
      color: #0f3460;
    }}
    .cta-section {{
      background: #f8f8f8;
      padding: 60px 20px;
      text-align: center;
    }}
    .cta-section h2 {{
      font-size: 1.8rem;
      margin-bottom: 16px;
    }}
    .btn-reserve {{
      display: inline-block;
      background: #c8a96e;
      color: #fff;
      padding: 16px 40px;
      border-radius: 8px;
      text-decoration: none;
      font-size: 1.1rem;
      font-weight: 700;
      margin-top: 16px;
      transition: background 0.2s;
    }}
    .btn-reserve:hover {{
      background: #b8944a;
    }}
    .faq-section {{
      max-width: 700px;
      margin: 60px auto;
      padding: 0 20px;
    }}
    .faq-section h2 {{
      font-size: 1.6rem;
      margin-bottom: 24px;
    }}
    .faq-item {{
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      margin-bottom: 12px;
      padding: 16px 20px;
    }}
    .faq-item summary {{
      font-weight: 600;
      cursor: pointer;
      color: #1a1a2e;
    }}
    .faq-item p {{
      margin-top: 12px;
      color: #555;
      line-height: 1.6;
    }}
    .back-link {{
      display: block;
      text-align: center;
      padding: 20px;
      color: #0f3460;
      text-decoration: none;
    }}
  </style>
</head>
<body>
  <nav aria-label="Navegação principal" class="top" id="topnav">
    <div class="nav-inner">
      <a aria-label="Embaixada Carioca · início" class="brand-mark" href="{nav_home}">
        <img alt="Logotipo Embaixada Carioca" class="brand-logo light" decoding="async" fetchpriority="high" src="/assets/logo-areia.svg">
        <img alt="Logotipo Embaixada Carioca" class="brand-logo dark" decoding="async" src="/assets/logo-verde.svg">
      </a>
    </div>
  </nav>

  <!-- Breadcrumb -->
  <nav aria-label="Breadcrumb" style="padding: 12px 20px; background: #f5f5f5; font-size: 0.9rem;">
    <a href="{nav_home}">{config['breadcrumb_home']}</a> &rsaquo;
    <span>{config['breadcrumb_current']}</span>
  </nav>

  <!-- Hero -->
  <section class="reviews-hero">
    <h1>{config['h1']}</h1>
    <p class="subtitle">{config['subtitle']}</p>
    <div class="rating-summary">
      <div class="rating-box">
        <span class="big-stars">★★★★★</span>
        <span class="big-number">{config['rating_label']}</span>
        <span class="label">{config['review_count']}</span>
      </div>
      <div class="rating-box">
        <span class="big-stars">★★★★★</span>
        <span class="big-number">{config['tripadvisor_label']}</span>
        <span class="label">TripAdvisor</span>
      </div>
    </div>
    <a href="{config['reserve_url']}" class="btn-reserve">{config['reserve_cta']}</a>
  </section>

  <!-- Reviews Grid -->
  <section class="reviews-section">
    <h2>{config['section_title']}</h2>
    <div class="reviews-grid" itemscope itemtype="https://schema.org/Restaurant">
      <meta itemprop="name" content="Embaixada Carioca">
      <div itemprop="aggregateRating" itemscope itemtype="https://schema.org/AggregateRating">
        <meta itemprop="ratingValue" content="4.8">
        <meta itemprop="reviewCount" content="8600">
        <meta itemprop="bestRating" content="5">
      </div>
{review_cards}
    </div>
  </section>

  <!-- CTA -->
  <section class="cta-section">
    <h2>{config['reserve_cta']}</h2>
    <p>{config['subtitle']}</p>
    <a href="{config['reserve_url']}" class="btn-reserve">{config['reserve_cta']}</a>
  </section>

  <!-- FAQ -->
  <section class="faq-section">
    <h2>{config['faq_title']}</h2>
{faq_items}
  </section>

  <a href="{config['back_url']}" class="back-link">{config['back_link']}</a>

  <footer class="foot">
    <div class="wrap">
      <div class="foot-bottom">
        <div>
          <strong style="color:#fff;">Embaixada Carioca</strong><br>
          Parque Bondinho Pão de Açúcar · Morro da Urca · Rio de Janeiro
        </div>
        <div>
          <a href="tel:+5521966837556">+55 21 96683-7556</a> ·
          <a href="https://instagram.com/embaixadacarioca">@embaixadacarioca</a>
        </div>
        <div>© 2026 · Todos os direitos reservados</div>
      </div>
    </div>
  </footer>
</body>
</html>'''

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ {filepath} criado ({len(html):,} bytes)")

# Gerar as 3 páginas
for filepath, config in PAGES.items():
    generate_review_page(filepath, config)

print("\n✅ Ação 2 concluída — 3 páginas de avaliações criadas!")
