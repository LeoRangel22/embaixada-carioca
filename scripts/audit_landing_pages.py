#!/usr/bin/env python3
"""
audit_landing_pages.py — Auditoria profunda das 7 landing pages estratégicas
=============================================================================
Analisa estrutura de conteúdo, densidade de keywords, CTAs, FAQ, schema,
imagens, links internos e oportunidades de otimização.

Autor: Manus AI — 03/06/2026
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent

# 12 keywords alvo e suas landing pages primárias
LANDING_PAGES = {
    'index.html': {
        'primary_kws': ['restaurante morro da urca', 'restaurante pão de açúcar', 'restaurante embaixada carioca'],
        'secondary_kws': ['onde comer morro da urca', 'almoço morro da urca'],
        'intent': 'navegacional + informacional',
        'persona': 'turista pesquisando antes da visita',
    },
    'almoco.html': {
        'primary_kws': ['almoço morro da urca', 'almoço pão de açúcar', 'almoço embaixada carioca'],
        'secondary_kws': ['restaurante morro da urca', 'onde comer morro da urca'],
        'intent': 'transacional',
        'persona': 'turista no bondinho decidindo onde almoçar',
    },
    'almoco-morro-da-urca.html': {
        'primary_kws': ['almoço morro da urca', 'restaurante morro da urca'],
        'secondary_kws': ['almoço pão de açúcar', 'onde comer morro da urca'],
        'intent': 'transacional',
        'persona': 'turista buscando opção de almoço específica',
    },
    'restaurante-morro-da-urca.html': {
        'primary_kws': ['restaurante morro da urca', 'restaurante pão de açúcar'],
        'secondary_kws': ['onde comer morro da urca', 'restaurante embaixada carioca'],
        'intent': 'informacional + transacional',
        'persona': 'turista pesquisando restaurantes no Morro da Urca',
    },
    'onde-comer-no-pao-de-acucar.html': {
        'primary_kws': ['onde comer pão de açúcar', 'onde comer morro da urca'],
        'secondary_kws': ['restaurante pão de açúcar', 'restaurante morro da urca'],
        'intent': 'informacional',
        'persona': 'turista pesquisando opções de alimentação no Pão de Açúcar',
    },
    'cafe-da-manha.html': {
        'primary_kws': ['café da manhã morro da urca', 'café da manhã pão de açúcar', 'café da manhã embaixada carioca'],
        'secondary_kws': ['restaurante morro da urca', 'onde comer morro da urca'],
        'intent': 'transacional',
        'persona': 'turista buscando café da manhã com vista',
    },
    'parque-bondinho-pao-de-acucar.html': {
        'primary_kws': ['restaurante pão de açúcar', 'onde comer pão de açúcar'],
        'secondary_kws': ['restaurante morro da urca', 'almoço pão de açúcar'],
        'intent': 'informacional',
        'persona': 'turista pesquisando sobre o Parque Bondinho e alimentação',
    },
}


def analyze_page(page_name: str, config: dict) -> dict:
    path = ROOT / page_name
    if not path.exists():
        return {'error': 'Página não encontrada'}

    html = path.read_text(encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    html_lower = html.lower()
    text_content = soup.get_text(separator=' ', strip=True).lower()

    result = {
        'page': page_name,
        'size_kb': round(len(html) / 1024, 1),
        'intent': config['intent'],
        'persona': config['persona'],
        'keywords': {},
        'structure': {},
        'ctas': {},
        'faq': {},
        'schema': {},
        'images': {},
        'internal_links': {},
        'opportunities': [],
        'score': 0,
    }

    # ── 1. Densidade de Keywords ──────────────────────────────────────────────
    all_kws = config['primary_kws'] + config['secondary_kws']
    kw_data = {}
    for kw in all_kws:
        # Buscar variações com/sem artigo
        variations = [kw]
        if 'pão de açúcar' in kw:
            variations.append(kw.replace('pão de açúcar', 'no pão de açúcar'))
            variations.append(kw.replace('pão de açúcar', 'do pão de açúcar'))
        if 'morro da urca' in kw:
            variations.append(kw.replace('morro da urca', 'no morro da urca'))
            variations.append(kw.replace('morro da urca', 'do morro da urca'))

        total_count = 0
        for v in variations:
            total_count += html_lower.count(v.lower())
            total_count += text_content.count(v.lower())

        kw_data[kw] = {
            'count': total_count,
            'status': '✅' if total_count >= 4 else ('⚠️' if total_count >= 2 else '❌'),
            'is_primary': kw in config['primary_kws'],
        }
    result['keywords'] = kw_data

    # ── 2. Estrutura de Conteúdo ──────────────────────────────────────────────
    h1_tags = soup.find_all('h1')
    h2_tags = soup.find_all('h2')
    h3_tags = soup.find_all('h3')
    paragraphs = soup.find_all('p')
    main_tag = soup.find('main')
    article_tag = soup.find('article')

    # Verificar se tem seção de hero
    hero = soup.find(class_=re.compile(r'hero', re.I))
    # Verificar se tem seção de destaques/pratos
    pratos_section = soup.find(class_=re.compile(r'prat|menu|cardapio|dish|food', re.I))
    # Verificar se tem seção de avaliações/reviews
    reviews_section = soup.find(class_=re.compile(r'review|avalia|rating|star', re.I))
    # Verificar se tem seção de localização/mapa
    map_section = soup.find(class_=re.compile(r'map|mapa|local|location', re.I))
    # Verificar se tem seção de horários
    hours_section = soup.find(class_=re.compile(r'hour|horario|opening|schedule', re.I))

    result['structure'] = {
        'h1_count': len(h1_tags),
        'h1_texts': [h.get_text(strip=True)[:80] for h in h1_tags[:3]],
        'h2_count': len(h2_tags),
        'h3_count': len(h3_tags),
        'paragraph_count': len(paragraphs),
        'has_main': bool(main_tag),
        'has_hero': bool(hero),
        'has_pratos_section': bool(pratos_section),
        'has_reviews_section': bool(reviews_section),
        'has_map_section': bool(map_section),
        'has_hours_section': bool(hours_section),
        'word_count': len(text_content.split()),
    }

    # ── 3. CTAs ───────────────────────────────────────────────────────────────
    all_links = soup.find_all('a', href=True)
    cta_links = []
    whatsapp_links = []
    reservation_links = []
    phone_links = []

    for link in all_links:
        href = link.get('href', '').lower()
        text = link.get_text(strip=True).lower()
        if 'whatsapp' in href or 'wa.me' in href:
            whatsapp_links.append(link.get_text(strip=True)[:50])
        if 'formulario' in href or 'reserva' in href or 'booking' in href:
            reservation_links.append(link.get_text(strip=True)[:50])
        if 'tel:' in href:
            phone_links.append(href)
        if any(w in text for w in ['reservar', 'reserve', 'agendar', 'visitar', 'ver cardápio', 'cardapio', 'menu']):
            cta_links.append(link.get_text(strip=True)[:50])

    result['ctas'] = {
        'whatsapp_count': len(whatsapp_links),
        'whatsapp_texts': whatsapp_links[:3],
        'reservation_count': len(reservation_links),
        'phone_count': len(phone_links),
        'cta_links': list(set(cta_links))[:5],
        'has_floating_cta': bool(soup.find(class_=re.compile(r'float|sticky|fixed|fab', re.I))),
    }

    # ── 4. FAQ ────────────────────────────────────────────────────────────────
    faq_section = soup.find(class_=re.compile(r'faq|pergunta|question', re.I))
    details_tags = soup.find_all('details')
    faq_schema = None

    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string or '{}')
            if isinstance(data, dict) and data.get('@type') == 'FAQPage':
                faq_schema = data
            elif isinstance(data, dict) and data.get('@graph'):
                for item in data['@graph']:
                    if isinstance(item, dict) and item.get('@type') == 'FAQPage':
                        faq_schema = item
        except Exception:
            pass

    result['faq'] = {
        'has_faq_section': bool(faq_section) or len(details_tags) > 0,
        'faq_items_count': len(details_tags),
        'has_faq_schema': bool(faq_schema),
        'faq_questions': [d.find('summary').get_text(strip=True)[:80] if d.find('summary') else '' for d in details_tags[:5]],
    }

    # ── 5. Schema JSON-LD ─────────────────────────────────────────────────────
    schemas = []
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string or '{}')
            if isinstance(data, dict):
                if data.get('@graph'):
                    for item in data['@graph']:
                        if isinstance(item, dict):
                            schemas.append(item.get('@type', '?'))
                else:
                    schemas.append(data.get('@type', '?'))
        except Exception:
            pass

    has_restaurant = 'Restaurant' in schemas
    has_faq_schema = 'FAQPage' in schemas
    has_breadcrumb = 'BreadcrumbList' in schemas
    has_local_business = 'LocalBusiness' in schemas or has_restaurant

    result['schema'] = {
        'types': schemas,
        'has_restaurant': has_restaurant,
        'has_faq': has_faq_schema,
        'has_breadcrumb': has_breadcrumb,
        'has_local_business': has_local_business,
        'schema_count': len(schemas),
    }

    # ── 6. Imagens ────────────────────────────────────────────────────────────
    images = soup.find_all('img')
    imgs_without_alt = [img.get('src', '')[:60] for img in images if not img.get('alt')]
    imgs_without_srcset = [img.get('src', '')[:60] for img in images if not img.get('srcset') and img.get('src', '').endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    imgs_with_loading_lazy = [img for img in images if img.get('loading') == 'lazy']

    result['images'] = {
        'total': len(images),
        'without_alt': len(imgs_without_alt),
        'without_srcset': len(imgs_without_srcset),
        'with_lazy': len(imgs_with_loading_lazy),
        'alt_coverage': round((len(images) - len(imgs_without_alt)) / max(len(images), 1) * 100, 0),
    }

    # ── 7. Links Internos ─────────────────────────────────────────────────────
    internal_links = [a.get('href', '') for a in all_links if a.get('href', '').startswith('/') or (not a.get('href', '').startswith('http') and not a.get('href', '').startswith('#') and not a.get('href', '').startswith('mailto') and not a.get('href', '').startswith('tel'))]
    result['internal_links'] = {
        'count': len(internal_links),
        'sample': list(set(internal_links))[:8],
    }

    # ── 8. Score e Oportunidades ──────────────────────────────────────────────
    score = 0
    opportunities = []

    # Keywords primárias
    primary_ok = sum(1 for kw in config['primary_kws'] if kw_data.get(kw, {}).get('count', 0) >= 4)
    score += primary_ok * 15
    if primary_ok < len(config['primary_kws']):
        opportunities.append(f"🔴 P0: {len(config['primary_kws']) - primary_ok} keywords primárias com densidade < 4x")

    # FAQ
    if result['faq']['has_faq_schema']:
        score += 15
    else:
        opportunities.append("🔴 P0: FAQ Schema (FAQPage JSON-LD) ausente — bloqueia Rich Snippets")

    if result['faq']['faq_items_count'] >= 3:
        score += 10
    else:
        opportunities.append(f"🟡 P1: FAQ com apenas {result['faq']['faq_items_count']} perguntas — ideal ≥ 5 para AIO")

    # CTAs
    if result['ctas']['whatsapp_count'] >= 1:
        score += 10
    else:
        opportunities.append("🔴 P0: Botão WhatsApp ausente — principal canal de conversão")

    if result['ctas']['reservation_count'] >= 1:
        score += 5
    else:
        opportunities.append("🟡 P1: Link de reserva ausente")

    # Schema
    if result['schema']['has_restaurant']:
        score += 10
    else:
        opportunities.append("🔴 P0: Schema Restaurant ausente")

    if result['schema']['has_breadcrumb']:
        score += 5
    else:
        opportunities.append("🟡 P1: BreadcrumbList ausente — perde trilha na SERP")

    # Estrutura
    if result['structure']['h1_count'] == 1:
        score += 5
    elif result['structure']['h1_count'] == 0:
        opportunities.append("🔴 P0: Sem H1 — crítico para SEO")
    elif result['structure']['h1_count'] > 1:
        opportunities.append(f"🟡 P1: {result['structure']['h1_count']} H1 na página — ideal é 1")

    if result['structure']['word_count'] >= 800:
        score += 5
    else:
        opportunities.append(f"🟡 P1: Conteúdo com {result['structure']['word_count']} palavras — ideal ≥ 800 para autoridade")

    if result['structure']['has_hero']:
        score += 5
    else:
        opportunities.append("🟡 P1: Seção Hero ausente — impacto na conversão")

    # Imagens
    if result['images']['alt_coverage'] >= 95:
        score += 5
    else:
        opportunities.append(f"🟡 P1: {result['images']['without_alt']} imagens sem alt text")

    result['score'] = min(score, 100)
    result['opportunities'] = opportunities

    return result


def main():
    print("=" * 70)
    print("  AUDITORIA PROFUNDA — 7 LANDING PAGES ESTRATÉGICAS")
    print("=" * 70)

    all_results = {}

    for page_name, config in LANDING_PAGES.items():
        print(f"\n{'─' * 70}")
        print(f"  📄 {page_name}")
        print(f"{'─' * 70}")

        result = analyze_page(page_name, config)
        all_results[page_name] = result

        if 'error' in result:
            print(f"  ❌ {result['error']}")
            continue

        print(f"  Tamanho: {result['size_kb']}KB | Palavras: {result['structure']['word_count']} | Score: {result['score']}/100")
        print(f"  Intent: {result['intent']}")
        print(f"  Persona: {result['persona']}")

        print(f"\n  KEYWORDS:")
        for kw, data in result['keywords'].items():
            tag = '[PRI]' if data['is_primary'] else '[SEC]'
            print(f"    {data['status']} {tag} '{kw}': {data['count']}x")

        print(f"\n  ESTRUTURA:")
        s = result['structure']
        print(f"    H1: {s['h1_count']} | H2: {s['h2_count']} | H3: {s['h3_count']} | Parágrafos: {s['paragraph_count']}")
        print(f"    <main>: {'✅' if s['has_main'] else '❌'} | Hero: {'✅' if s['has_hero'] else '❌'} | Pratos: {'✅' if s['has_pratos_section'] else '❌'} | Mapa: {'✅' if s['has_map_section'] else '❌'}")

        print(f"\n  CTAs:")
        c = result['ctas']
        print(f"    WhatsApp: {c['whatsapp_count']}x | Reserva: {c['reservation_count']}x | Telefone: {c['phone_count']}x | Float CTA: {'✅' if c['has_floating_cta'] else '❌'}")

        print(f"\n  FAQ:")
        f = result['faq']
        print(f"    Seção FAQ: {'✅' if f['has_faq_section'] else '❌'} | Itens: {f['faq_items_count']} | FAQPage Schema: {'✅' if f['has_faq_schema'] else '❌'}")

        print(f"\n  SCHEMA:")
        sc = result['schema']
        print(f"    Tipos: {sc['types']}")
        print(f"    Restaurant: {'✅' if sc['has_restaurant'] else '❌'} | FAQ: {'✅' if sc['has_faq'] else '❌'} | Breadcrumb: {'✅' if sc['has_breadcrumb'] else '❌'}")

        print(f"\n  IMAGENS:")
        img = result['images']
        print(f"    Total: {img['total']} | Alt coverage: {img['alt_coverage']}% | Sem srcset: {img['without_srcset']}")

        if result['opportunities']:
            print(f"\n  OPORTUNIDADES ({len(result['opportunities'])}):")
            for opp in result['opportunities']:
                print(f"    {opp}")

    # Salvar resultados em JSON
    output_path = ROOT / '_audit_reports' / 'landing_pages_audit.json'
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n\n{'=' * 70}")
    print(f"  RESUMO GERAL")
    print(f"{'=' * 70}")
    for page, result in all_results.items():
        if 'error' not in result:
            score = result['score']
            opps = len(result['opportunities'])
            bar = '█' * (score // 10) + '░' * (10 - score // 10)
            print(f"  {bar} {score:3d}/100  {page} ({opps} oportunidades)")

    print(f"\n📄 Relatório JSON: {output_path}")


if __name__ == "__main__":
    main()
