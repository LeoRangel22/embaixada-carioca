#!/usr/bin/env python3
"""
Ação 1: Otimizar title, meta description e FAQ schema de morro-da-urca.html (PT, EN, ES)
Objetivo: Aumentar CTR da query "morro da urca" (3.256 impressões, CTR 0,34%, posição 8,28)
"""
import json
from bs4 import BeautifulSoup

# ============================================================
# CONFIGURAÇÕES POR IDIOMA
# ============================================================
CONFIGS = {
    'morro-da-urca.html': {
        'title': 'Morro da Urca: Guia Completo 2026 — Bondinho, Trilha e Restaurante 4,8★',
        'description': 'O único restaurante dentro do Parque Bondinho Pão de Açúcar. Almoço, feijoada premiada e happy hour com vista para o Pão de Açúcar. 4,8★ com 8.600+ avaliações. Reserve agora.',
        'og_title': 'Morro da Urca: Guia Completo 2026 | Restaurante 4,8★ no Bondinho',
        'og_description': 'O único restaurante dentro do Parque Bondinho. Feijoada premiada da Academia da Cachaça, almoço e happy hour com vista para o Pão de Açúcar. Reserve sua mesa.',
        'new_faqs': [
            {
                '@type': 'Question',
                'name': 'Qual o horário do Parque Bondinho Pão de Açúcar?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'O Parque Bondinho Pão de Açúcar funciona todos os dias das 8h às 21h, com última subida às 20h. O restaurante Embaixada Carioca, localizado no Morro da Urca dentro do parque, atende das 12h às 21h.'
                }
            },
            {
                '@type': 'Question',
                'name': 'O que fazer no Morro da Urca além do bondinho?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'No Morro da Urca você pode: fazer a trilha gratuita pelo Caminho da Costa (sem pagar ingresso), almoçar no restaurante Embaixada Carioca com vista para o Pão de Açúcar, curtir o happy hour ao entardecer com caipirinha e chopp gelado, e assistir a shows e eventos na arena ao ar livre.'
                }
            },
            {
                '@type': 'Question',
                'name': 'Qual o melhor restaurante no Morro da Urca?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'A Embaixada Carioca é o único restaurante localizado dentro do Parque Bondinho Pão de Açúcar, no Morro da Urca. Com 4,8 estrelas e mais de 8.600 avaliações no Google, serve café da manhã, almoço com feijoada premiada da Academia da Cachaça e happy hour com vista panorâmica para o Pão de Açúcar.'
                }
            },
            {
                '@type': 'Question',
                'name': 'Tem como subir o Morro da Urca de graça?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'Sim! É possível subir o Morro da Urca gratuitamente pela trilha do Caminho da Costa, sem pagar ingresso do bondinho. A trilha tem cerca de 1,5 km e nível moderado. Ao chegar no topo, você pode almoçar ou tomar uma caipirinha na Embaixada Carioca com vista para o Pão de Açúcar.'
                }
            },
            {
                '@type': 'Question',
                'name': 'Como chegar ao Morro da Urca?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'O Morro da Urca fica na Praia Vermelha, Urca, Rio de Janeiro. Você pode chegar de bondinho pelo Parque Bondinho Pão de Açúcar (Av. Pasteur, 520), de Uber/táxi, ou de ônibus pelas linhas 107, 511 e 512. A trilha gratuita também parte da Praia Vermelha.'
                }
            },
            {
                '@type': 'Question',
                'name': 'Tem feijoada no Morro da Urca?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'Sim! A Embaixada Carioca serve a feijoada premiada da Academia da Cachaça todos os dias no almoço, das 12h às 17h. É a única feijoada servida a 227 metros de altitude, com vista direta para o Pão de Açúcar. Eleita uma das melhores do Rio pela revista Veja Rio (Comer & Beber 2025 e 2026).'
                }
            }
        ]
    },
    'en/morro-da-urca.html': {
        'title': 'Urca Hill (Morro da Urca): Complete Guide 2026 — Cable Car, Trail & Restaurant 4.8★',
        'description': 'The only restaurant inside Sugarloaf Mountain Park. Lunch, award-winning feijoada and happy hour with a panoramic view. 4.8★ with 8,600+ reviews. Book your table now.',
        'og_title': 'Urca Hill: Complete Guide 2026 | Restaurant 4.8★ at Sugarloaf',
        'og_description': 'The only restaurant inside Sugarloaf Mountain Park. Award-winning feijoada, lunch and happy hour with a panoramic view of Sugarloaf. Book your table.',
        'new_faqs': [
            {
                '@type': 'Question',
                'name': 'What are the opening hours of Sugarloaf Mountain Park (Parque Bondinho)?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'Sugarloaf Mountain Park (Parque Bondinho Pão de Açúcar) is open every day from 8am to 9pm, with the last cable car ride at 8pm. The Embaixada Carioca restaurant, located at Urca Hill inside the park, is open from 12pm to 9pm.'
                }
            },
            {
                '@type': 'Question',
                'name': 'What is the best restaurant at Urca Hill (Morro da Urca)?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'Embaixada Carioca is the only restaurant located inside Sugarloaf Mountain Park, at Urca Hill. Rated 4.8 stars with over 8,600 Google reviews, it serves breakfast, lunch with award-winning feijoada from Academia da Cachaça, and happy hour with a panoramic view of Sugarloaf Mountain.'
                }
            },
            {
                '@type': 'Question',
                'name': 'Can you hike to Urca Hill for free?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'Yes! You can hike to Urca Hill for free via the Caminho da Costa trail, without paying for the cable car ticket. The trail is about 1.5 km and moderate difficulty. Once at the top, you can have lunch or enjoy a caipirinha at Embaixada Carioca with a view of Sugarloaf Mountain.'
                }
            },
            {
                '@type': 'Question',
                'name': 'Is there feijoada at Urca Hill?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'Yes! Embaixada Carioca serves the award-winning feijoada from Academia da Cachaça every day at lunch, from 12pm to 5pm. It\'s the only feijoada served at 227 meters altitude, with a direct view of Sugarloaf Mountain. Voted one of the best in Rio by Veja Rio magazine (Comer & Beber 2025 and 2026).'
                }
            },
            {
                '@type': 'Question',
                'name': 'How to get to Urca Hill (Morro da Urca)?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'Urca Hill is located at Praia Vermelha, Urca neighborhood, Rio de Janeiro. You can get there by cable car through Sugarloaf Mountain Park (Av. Pasteur, 520), by Uber/taxi, or by bus lines 107, 511 and 512. The free hiking trail also starts from Praia Vermelha beach.'
                }
            },
            {
                '@type': 'Question',
                'name': 'What is there to do at Urca Hill besides the cable car?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'At Urca Hill you can: hike the free Caminho da Costa trail (no ticket needed), have lunch at Embaixada Carioca restaurant with a view of Sugarloaf, enjoy happy hour at sunset with caipirinha and cold draft beer, and watch shows and events at the open-air arena.'
                }
            }
        ]
    },
    'es/morro-da-urca.html': {
        'title': 'Morro da Urca: Guía Completa 2026 — Teleférico, Sendero y Restaurante 4,8★',
        'description': 'El único restaurante dentro del Parque Bondinho Pan de Azúcar. Almuerzo, feijoada premiada y happy hour con vista panorámica. 4,8★ con 8.600+ reseñas. Reserve su mesa ahora.',
        'og_title': 'Morro da Urca: Guía Completa 2026 | Restaurante 4,8★ en el Teleférico',
        'og_description': 'El único restaurante dentro del Parque Bondinho. Feijoada premiada, almuerzo y happy hour con vista al Pan de Azúcar. Reserve su mesa.',
        'new_faqs': [
            {
                '@type': 'Question',
                'name': '¿Cuál es el horario del Parque Bondinho Pan de Azúcar?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'El Parque Bondinho Pan de Azúcar abre todos los días de 8h a 21h, con el último teleférico a las 20h. El restaurante Embaixada Carioca, ubicado en el Morro da Urca dentro del parque, atiende de 12h a 21h.'
                }
            },
            {
                '@type': 'Question',
                'name': '¿Cuál es el mejor restaurante en el Morro da Urca?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'La Embaixada Carioca es el único restaurante ubicado dentro del Parque Bondinho Pan de Azúcar, en el Morro da Urca. Con 4,8 estrellas y más de 8.600 reseñas en Google, sirve desayuno, almuerzo con feijoada premiada de la Academia da Cachaça y happy hour con vista panorámica al Pan de Azúcar.'
                }
            },
            {
                '@type': 'Question',
                'name': '¿Se puede subir al Morro da Urca gratis?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': '¡Sí! Es posible subir al Morro da Urca gratuitamente por el sendero Caminho da Costa, sin pagar la entrada del teleférico. El sendero tiene aproximadamente 1,5 km y nivel moderado. Al llegar a la cima, puede almorzar o tomar una caipirinha en la Embaixada Carioca con vista al Pan de Azúcar.'
                }
            },
            {
                '@type': 'Question',
                'name': '¿Hay feijoada en el Morro da Urca?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': '¡Sí! La Embaixada Carioca sirve la feijoada premiada de la Academia da Cachaça todos los días en el almuerzo, de 12h a 17h. Es la única feijoada servida a 227 metros de altitud, con vista directa al Pan de Azúcar. Elegida una de las mejores de Río por la revista Veja Rio (Comer & Beber 2025 y 2026).'
                }
            },
            {
                '@type': 'Question',
                'name': '¿Cómo llegar al Morro da Urca?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'El Morro da Urca está en la Praia Vermelha, barrio de Urca, Río de Janeiro. Puede llegar en teleférico por el Parque Bondinho Pan de Azúcar (Av. Pasteur, 520), en Uber/taxi, o en autobús por las líneas 107, 511 y 512. El sendero gratuito también parte de la Praia Vermelha.'
                }
            },
            {
                '@type': 'Question',
                'name': '¿Qué hacer en el Morro da Urca además del teleférico?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'En el Morro da Urca puede: hacer el sendero gratuito Caminho da Costa (sin pagar entrada), almorzar en el restaurante Embaixada Carioca con vista al Pan de Azúcar, disfrutar del happy hour al atardecer con caipirinha y chopp frío, y ver shows y eventos en el anfiteatro al aire libre.'
                }
            }
        ]
    }
}

def optimize_page(filepath, config):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 1. Atualizar title
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = config['title']
    
    # 2. Atualizar meta description
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    if desc_tag:
        desc_tag['content'] = config['description']
    
    # 3. Atualizar OG title
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    if og_title:
        og_title['content'] = config['og_title']
    
    # 4. Atualizar OG description
    og_desc = soup.find('meta', attrs={'property': 'og:description'})
    if og_desc:
        og_desc['content'] = config['og_description']
    
    # 5. Atualizar Twitter title e description
    tw_title = soup.find('meta', attrs={'name': 'twitter:title'})
    if tw_title:
        tw_title['content'] = config['og_title']
    tw_desc = soup.find('meta', attrs={'name': 'twitter:description'})
    if tw_desc:
        tw_desc['content'] = config['og_description']
    
    # 6. Adicionar novas FAQs ao JSON-LD FAQPage
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            graph = data.get('@graph', [])
            for node in graph:
                if node.get('@type') == 'FAQPage':
                    existing_questions = {q['name'] for q in node.get('mainEntity', [])}
                    added = 0
                    for faq in config['new_faqs']:
                        if faq['name'] not in existing_questions:
                            node['mainEntity'].append(faq)
                            added += 1
                    if added > 0:
                        script.string = json.dumps(data, ensure_ascii=False, indent=2)
                        print(f"  + {added} FAQs adicionadas ao JSON-LD")
                    break
        except Exception as e:
            pass
    
    # 7. Adicionar FAQs visíveis na seção de FAQ (details/summary)
    # Encontrar o último details na seção de FAQ
    all_details = soup.find_all('details')
    if all_details:
        last_details = all_details[-1]
        lang = 'pt' if 'morro-da-urca.html' == filepath.split('/')[-1] and 'en/' not in filepath and 'es/' not in filepath else ('en' if 'en/' in filepath else 'es')
        
        added_visible = 0
        for faq in config['new_faqs']:
            # Verificar se já existe
            question_text = faq['name']
            already_exists = any(
                d.find('summary') and question_text.lower() in d.find('summary').text.lower()
                for d in all_details
            )
            if not already_exists:
                new_details = soup.new_tag('details')
                new_details['class'] = 'faq-item'
                new_summary = soup.new_tag('summary')
                new_summary.string = question_text
                new_p = soup.new_tag('p')
                new_p.string = faq['acceptedAnswer']['text']
                new_details.append(new_summary)
                new_details.append(new_p)
                last_details.insert_after(new_details)
                last_details = new_details
                added_visible += 1
        
        if added_visible > 0:
            print(f"  + {added_visible} FAQs visíveis adicionadas")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"✓ {filepath} otimizado")
    print(f"  Title: {config['title'][:70]}...")
    print(f"  Desc: {config['description'][:80]}...")

# Executar para as 3 versões
for filepath, config in CONFIGS.items():
    print(f"\nOtimizando {filepath}...")
    optimize_page(filepath, config)

print("\n✅ Ação 1 concluída!")
