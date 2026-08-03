#!/usr/bin/env python3
"""
Otimização em massa das páginas existentes da Embaixada Carioca.
Aplica: 4,8★ no title, meta description otimizada, aggregateRating JSON-LD.
"""
import json
import re
from bs4 import BeautifulSoup

# ─── Mapa de páginas a otimizar ───────────────────────────────────────────────
PAGES = [
    # (path, lang, novo_title_suffix, nova_meta_desc)
    (
        "feijoada-morro-da-urca.html", "pt-BR",
        "4,8★",
        "A feijoada premiada do Rio de Janeiro, servida todos os dias no Morro da Urca com vista para o Pão de Açúcar. Academia da Cachaça · Veja Rio 2025/2026. Reserve sua mesa."
    ),
    (
        "en/feijoada.html", "en",
        "4.8★",
        "Award-winning feijoada at Urca Hill with a view of Sugarloaf Mountain. Served daily 12h–17h. Academia da Cachaça · Veja Rio 2025/2026. Book your table."
    ),
    (
        "es/feijoada.html", "es",
        "4,8★",
        "La feijoada premiada de Río de Janeiro, servida todos los días en el Morro da Urca con vista al Pan de Azúcar. Academia da Cachaça · Veja Rio 2025/2026. Reserve su mesa."
    ),
    (
        "restaurante-com-vista-rio-de-janeiro.html", "pt-BR",
        "4,8★",
        "O único restaurante dentro do Parque Bondinho Pão de Açúcar, a 227m de altitude com vista panorâmica para o Rio. Almoço, café da manhã e happy hour. Reserve sua mesa."
    ),
    (
        "en/restaurant-at-sugarloaf.html", "en",
        "4.8★",
        "The only restaurant inside Sugarloaf Mountain Park, 227m above sea level with panoramic views of Rio de Janeiro. Breakfast, lunch and happy hour. Book your table."
    ),
    (
        "es/restaurante-com-vista-rio-de-janeiro.html", "es",
        "4,8★",
        "El único restaurante dentro del Parque Bondinho Pan de Azúcar, a 227m de altitud con vista panorámica de Río. Desayuno, almuerzo y happy hour. Reserve su mesa."
    ),
    (
        "en/morro-da-urca.html", "en",
        "4.8★",
        "Complete guide to Urca Hill: cable car, free hiking trail and the best restaurant with a view of Sugarloaf Mountain. Book your table at Embaixada Carioca."
    ),
    (
        "cafe-da-manha-pao-de-acucar.html", "pt-BR",
        "4,8★",
        "Café da manhã com vista para o Pão de Açúcar no Morro da Urca. Embaixada Carioca serve das 8h30 dentro do Parque Bondinho. Reserve sua mesa."
    ),
    (
        "en/cafe-da-manha-pao-de-acucar.html", "en",
        "4.8★",
        "Breakfast with a view of Sugarloaf Mountain at Urca Hill. Embaixada Carioca serves from 8h30 inside Bondinho Park. Book your table."
    ),
    (
        "es/cafe-da-manha-pao-de-acucar.html", "es",
        "4,8★",
        "Desayuno con vista al Pan de Azúcar en el Morro da Urca. Embaixada Carioca sirve desde las 8h30 dentro del Parque Bondinho. Reserve su mesa."
    ),
    (
        "por-do-sol-morro-da-urca.html", "pt-BR",
        "4,8★",
        "O melhor pôr do sol do Rio de Janeiro com caipirinha e chopp gelado no Morro da Urca. Happy hour das 17h às 21h com vista direta para o Pão de Açúcar. Reserve sua mesa."
    ),
    (
        "en/sunset.html", "en",
        "4.8★",
        "The best sunset in Rio de Janeiro with craft cocktails and cold draft beer at Urca Hill. Happy hour 17h–21h with a direct view of Sugarloaf Mountain. Book your table."
    ),
    (
        "es/atardecer.html", "es",
        "4,8★",
        "El mejor atardecer de Río de Janeiro con caipirinhas y cerveza de barril en el Morro da Urca. Happy hour de 17h a 21h con vista directa al Pan de Azúcar. Reserve su mesa."
    ),
]

# ─── aggregateRating JSON-LD a inserir nas páginas sem ele ───────────────────
AGGREGATE_RATING_NODE = {
    "@context": "https://schema.org",
    "@type": "Restaurant",
    "@id": "https://www.embaixadacarioca.com/#restaurant",
    "name": "Embaixada Carioca",
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.8",
        "bestRating": "5",
        "worstRating": "1",
        "reviewCount": "8600"
    }
}

def has_aggregate_rating(soup):
    for s in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(s.string or '')
            if isinstance(data, dict):
                if data.get('aggregateRating'):
                    return True
                if isinstance(data.get('@graph'), list):
                    for node in data['@graph']:
                        if node.get('aggregateRating'):
                            return True
        except:
            pass
    return False

def add_rating_to_title(title_text, suffix):
    """Adiciona o sufixo de rating ao title se não existir."""
    if '4,8' in title_text or '4.8' in title_text:
        return title_text
    # Remove pipe final se existir e adiciona o rating
    title_text = title_text.strip()
    if title_text.endswith('|'):
        title_text = title_text[:-1].strip()
    # Inserir antes do último separador | ou no final
    if ' | ' in title_text:
        parts = title_text.rsplit(' | ', 1)
        return f"{parts[0]} {suffix} | {parts[1]}"
    elif ' — ' in title_text:
        parts = title_text.split(' — ', 1)
        return f"{parts[0]} {suffix} — {parts[1]}"
    else:
        return f"{title_text} {suffix}"

results = []
for path, lang, suffix, new_desc in PAGES:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        changed = []

        # 1. Atualizar title
        title_tag = soup.find('title')
        if title_tag:
            old_title = title_tag.string or ''
            if '4,8' not in old_title and '4.8' not in old_title:
                new_title = add_rating_to_title(old_title, suffix)
                title_tag.string = new_title
                changed.append(f"title: '{old_title[:50]}' → '{new_title[:50]}'")

        # 2. Atualizar og:title
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        if og_title and og_title.get('content'):
            old_og = og_title['content']
            if '4,8' not in old_og and '4.8' not in old_og:
                og_title['content'] = add_rating_to_title(old_og, suffix)
                changed.append("og:title atualizado")

        # 3. Atualizar meta description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            old_desc = desc_tag.get('content', '')
            if len(old_desc) > 160 or (suffix in new_desc and suffix not in old_desc):
                desc_tag['content'] = new_desc
                changed.append(f"meta desc: {len(old_desc)} → {len(new_desc)} chars")

        # 4. Atualizar og:description
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        if og_desc:
            og_desc['content'] = new_desc
            changed.append("og:description atualizado")

        # 5. Adicionar aggregateRating JSON-LD se ausente
        if not has_aggregate_rating(soup):
            new_script = soup.new_tag('script', type='application/ld+json')
            new_script.string = json.dumps(AGGREGATE_RATING_NODE, ensure_ascii=False, indent=2)
            # Inserir antes do </head>
            head = soup.find('head')
            if head:
                head.append(new_script)
                changed.append("aggregateRating JSON-LD adicionado")

        # Salvar
        with open(path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        status = "✓ " + " | ".join(changed) if changed else "— sem alterações"
        results.append(f"{path}: {status}")
        print(f"✓ {path}: {len(changed)} alterações")

    except FileNotFoundError:
        results.append(f"{path}: ❌ NÃO EXISTE")
        print(f"❌ {path}: arquivo não encontrado")

print(f"\n✅ {len([r for r in results if '✓' in r])} páginas otimizadas")
print(f"❌ {len([r for r in results if '❌' in r])} páginas não encontradas")
