#!/usr/bin/env python3
"""
Auditoria profunda de conteúdo para a Fase 4: Conteúdo Campeão.
Analisa: densidade de keywords, estrutura de conteúdo, CTAs, mídia, FAQ, E-E-A-T.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]

# 12 keywords alvo agrupadas por landing page
KEYWORD_GROUPS = {
    'restaurante-morro-da-urca.html': [
        'restaurante morro da urca',
        'almoço morro da urca',
        'onde comer morro da urca',
        'café da manhã morro da urca',
    ],
    'almoco-morro-da-urca.html': [
        'almoço morro da urca',
        'restaurante morro da urca',
        'onde comer morro da urca',
    ],
    'cafe-da-manha.html': [
        'café da manhã morro da urca',
        'café da manhã pão de açúcar',
    ],
    'onde-comer-no-pao-de-acucar.html': [
        'onde comer pão de açúcar',
        'restaurante pão de açúcar',
        'onde comer morro da urca',
    ],
    'restaurante-bondinho-pao-de-acucar.html': [
        'restaurante pão de açúcar',
        'almoço pão de açúcar',
        'onde comer pão de açúcar',
    ],
    'almoco.html': [
        'almoço morro da urca',
        'almoço pão de açúcar',
        'restaurante embaixada carioca',
    ],
    'index.html': [
        'restaurante embaixada carioca',
        'restaurante morro da urca',
        'restaurante pão de açúcar',
    ],
}

# Todas as 12 keywords
ALL_KEYWORDS = [
    'restaurante morro da urca',
    'almoço morro da urca',
    'café da manhã morro da urca',
    'onde comer morro da urca',
    'restaurante pão de açúcar',
    'almoço pão de açúcar',
    'café da manhã pão de açúcar',
    'onde comer pão de açúcar',
    'restaurante embaixada carioca',
    'almoço embaixada carioca',
    'café da manhã embaixada carioca',
    'onde comer embaixada carioca',
]

# CTAs de alta conversão esperados
HIGH_CONV_CTAS = [
    'reservar', 'reserve', 'reservation',
    'whatsapp', 'zap', 'wa.me',
    'cardápio', 'cardapio', 'menu',
    'ver cardápio', 'ver menu',
    'fazer reserva', 'agendar',
    'ligar', 'tel:', 'telefone',
]

# Elementos de E-E-A-T
EEAT_SIGNALS = [
    'premiado', 'premiada', 'award', 'prêmio',
    'anos de', 'fundado', 'desde',
    'chef', 'gastrônomo', 'especialista',
    'avaliação', 'nota', 'estrelas',
    'tripadvisor', 'google',
    'imprensa', 'mídia', 'reportagem',
]

# Elementos de FAQ / featured snippet
FAQ_SIGNALS = [
    'faq', 'perguntas', 'frequentes',
    'como chegar', 'horário', 'horario',
    'quanto custa', 'preço', 'preco',
    'aceita reserva', 'tem estacionamento',
]

SCRIPT_RE = re.compile(r'<script[^>]*>(.*?)</script>', re.I | re.S)
IMG_RE = re.compile(r'<img[^>]*>', re.I)
CTA_BTN_RE = re.compile(r'<(?:a|button)[^>]*(?:href|onclick)[^>]*>(.*?)</(?:a|button)>', re.I | re.S)
H_RE = re.compile(r'<h([1-6])[^>]*>(.*?)</h[1-6]>', re.I | re.S)
WORD_COUNT_RE = re.compile(r'\b\w+\b')
TAG_RE = re.compile(r'<[^>]+>')


def strip_tags(html: str) -> str:
    # Remove scripts e styles
    html = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.I | re.S)
    html = re.sub(r'<style[^>]*>.*?</style>', ' ', html, flags=re.I | re.S)
    return TAG_RE.sub(' ', html).lower()


def count_keyword(text: str, keyword: str) -> int:
    """Conta ocorrências de keyword no texto (case insensitive)."""
    kw = keyword.lower()
    # Normalizar acentos para busca
    replacements = {'ã': '[aã]', 'á': '[aá]', 'â': '[aâ]', 'à': '[aà]',
                    'é': '[eé]', 'ê': '[eê]', 'í': '[ií]', 'ó': '[oó]',
                    'ô': '[oô]', 'ú': '[uú]', 'ç': '[cç]', 'ã': '[aã]'}
    pattern = kw
    for char, repl in replacements.items():
        pattern = pattern.replace(char, repl)
    try:
        return len(re.findall(pattern, text, re.I))
    except Exception:
        return text.count(kw)


def audit_page(page_rel: str, keywords: list[str]) -> dict:
    path = ROOT / page_rel
    if not path.exists():
        return {'page': page_rel, 'exists': False}

    html = path.read_text(encoding='utf-8', errors='ignore')
    text = strip_tags(html)
    words = WORD_COUNT_RE.findall(text)
    word_count = len(words)

    # Keyword density
    kw_counts = {}
    for kw in keywords:
        count = count_keyword(text, kw)
        density = round(count / max(word_count, 1) * 100, 2)
        kw_counts[kw] = {'count': count, 'density': density}

    # Headings
    headings = [(int(m.group(1)), strip_tags(m.group(2)).strip()) for m in H_RE.finditer(html)]
    h1_list = [h for level, h in headings if level == 1]
    h2_list = [h for level, h in headings if level == 2]

    # Imagens
    imgs = IMG_RE.findall(html)
    imgs_with_alt = sum(1 for img in imgs if 'alt=' in img.lower() and 'alt=""' not in img.lower())
    imgs_with_srcset = sum(1 for img in imgs if 'srcset=' in img.lower())
    imgs_webp = sum(1 for img in imgs if '.webp' in img.lower())
    total_imgs = len(imgs)

    # CTAs
    cta_matches = CTA_BTN_RE.findall(html)
    cta_texts = [strip_tags(c).strip() for c in cta_matches]
    has_whatsapp = any('whatsapp' in c.lower() or 'wa.me' in c.lower() or 'zap' in c.lower()
                       for c in html.lower().split())
    has_reservation = any(word in text for word in ['reservar', 'reserve', 'reserva', 'reservation'])
    has_menu_cta = any(word in text for word in ['ver cardápio', 'ver menu', 'cardápio completo'])
    has_tel = 'tel:' in html.lower() or '+55' in html

    # E-E-A-T
    eeat_found = [s for s in EEAT_SIGNALS if s in text]

    # FAQ
    faq_found = [s for s in FAQ_SIGNALS if s in text]
    has_faq_schema = '"FAQPage"' in html or "'FAQPage'" in html

    # Schema types
    schema_types = set()
    for m in re.finditer(r'"@type"\s*:\s*"([^"]+)"', html):
        schema_types.add(m.group(1))

    # OpenGraph
    has_og_image = 'og:image' in html
    has_og_description = 'og:description' in html

    # Vídeo
    has_video = '<video' in html.lower() or 'youtube.com' in html.lower() or 'youtu.be' in html.lower()

    # Preço visível
    has_price = any(p in text for p in ['r$', 'reais', 'preço', 'preco', 'a partir de', 'cardápio a partir'])

    # Score de conteúdo (0-100)
    score = 0
    score_details = []

    # Keywords (40 pontos)
    kw_with_2plus = sum(1 for v in kw_counts.values() if v['count'] >= 2)
    kw_score = min(40, kw_with_2plus * 10)
    score += kw_score
    score_details.append(f'Keywords ≥2x: {kw_with_2plus}/{len(keywords)} (+{kw_score}pts)')

    # Estrutura (20 pontos)
    struct_score = 0
    if h1_list: struct_score += 5
    if len(h2_list) >= 3: struct_score += 5
    if word_count >= 500: struct_score += 5
    if has_faq_schema: struct_score += 5
    score += struct_score
    score_details.append(f'Estrutura: H1={len(h1_list)}, H2={len(h2_list)}, words={word_count} (+{struct_score}pts)')

    # CTAs (20 pontos)
    cta_score = 0
    if has_whatsapp: cta_score += 7
    if has_reservation: cta_score += 7
    if has_tel: cta_score += 3
    if has_menu_cta: cta_score += 3
    score += cta_score
    score_details.append(f'CTAs: WA={has_whatsapp}, Reserva={has_reservation}, Tel={has_tel} (+{cta_score}pts)')

    # Mídia (20 pontos)
    media_score = 0
    if total_imgs >= 3: media_score += 5
    if imgs_with_srcset >= 2: media_score += 5
    if imgs_webp >= 1: media_score += 5
    if has_video: media_score += 5
    score += media_score
    score_details.append(f'Mídia: imgs={total_imgs}, srcset={imgs_with_srcset}, webp={imgs_webp}, video={has_video} (+{media_score}pts)')

    return {
        'page': page_rel,
        'exists': True,
        'word_count': word_count,
        'score': score,
        'score_details': score_details,
        'keywords': kw_counts,
        'h1': h1_list,
        'h2_count': len(h2_list),
        'h2_list': h2_list[:5],
        'images': {
            'total': total_imgs,
            'with_alt': imgs_with_alt,
            'with_srcset': imgs_with_srcset,
            'webp': imgs_webp,
        },
        'ctas': {
            'whatsapp': has_whatsapp,
            'reservation': has_reservation,
            'menu': has_menu_cta,
            'tel': has_tel,
        },
        'eeat': eeat_found,
        'faq': faq_found,
        'has_faq_schema': has_faq_schema,
        'schema_types': sorted(schema_types),
        'has_og_image': has_og_image,
        'has_price': has_price,
        'has_video': has_video,
    }


def main():
    print('=' * 70)
    print('  Auditoria de Conteúdo — Fase 4: Conteúdo Campeão')
    print('=' * 70)

    all_results = {}

    for page, keywords in KEYWORD_GROUPS.items():
        result = audit_page(page, keywords)
        all_results[page] = result

        print(f'\n{"─"*60}')
        print(f'📄 {page}')
        if not result['exists']:
            print('  ❌ Arquivo não encontrado')
            continue

        print(f'  Score de Conteúdo: {result["score"]}/100')
        print(f'  Palavras: {result["word_count"]}')
        print(f'  H1: {result["h1"][:1]}')
        print(f'  H2s ({result["h2_count"]}): {result["h2_list"][:3]}')
        print()

        print('  📊 Densidade de Keywords:')
        for kw, data in result['keywords'].items():
            status = '✅' if data['count'] >= 2 else ('⚠️ ' if data['count'] == 1 else '❌')
            print(f'    {status} "{kw}": {data["count"]}x ({data["density"]}%)')

        print()
        print('  🖼️  Mídia:')
        imgs = result['images']
        print(f'    Imagens: {imgs["total"]} total | {imgs["with_alt"]} com alt | {imgs["with_srcset"]} srcset | {imgs["webp"]} WebP')
        print(f'    Vídeo: {"✅" if result["has_video"] else "❌"}')

        print()
        print('  🔘 CTAs:')
        ctas = result['ctas']
        print(f'    WhatsApp: {"✅" if ctas["whatsapp"] else "❌"}')
        print(f'    Reserva: {"✅" if ctas["reservation"] else "❌"}')
        print(f'    Cardápio: {"✅" if ctas["menu"] else "❌"}')
        print(f'    Telefone: {"✅" if ctas["tel"] else "❌"}')

        print()
        print(f'  🏆 E-E-A-T ({len(result["eeat"])} sinais): {result["eeat"][:5]}')
        print(f'  ❓ FAQ ({len(result["faq"])} sinais): {result["faq"][:5]}')
        print(f'  📋 Schema FAQ: {"✅" if result["has_faq_schema"] else "❌"}')
        print(f'  💰 Preço visível: {"✅" if result["has_price"] else "❌"}')

    # Verificar também as páginas EN/ES das principais
    print('\n' + '=' * 70)
    print('  Cobertura EN/ES das páginas principais')
    print('=' * 70)
    en_es_pages = [
        ('en/restaurant-at-urca-hill.html', ['restaurant urca hill', 'restaurant sugarloaf', 'where to eat sugarloaf']),
        ('en/where-to-eat-near-sugarloaf.html', ['where to eat sugarloaf', 'restaurant near sugarloaf', 'sugarloaf restaurant']),
        ('es/restaurante-morro-da-urca.html', ['restaurante morro da urca', 'restaurante pan de azucar', 'donde comer pan de azucar']),
    ]
    for page, keywords in en_es_pages:
        result = audit_page(page, keywords)
        if result.get('exists'):
            print(f'\n📄 {page} — Score: {result["score"]}/100 | Words: {result["word_count"]}')
            for kw, data in result['keywords'].items():
                status = '✅' if data['count'] >= 2 else ('⚠️ ' if data['count'] == 1 else '❌')
                print(f'    {status} "{kw}": {data["count"]}x')

    # Salvar JSON
    output_path = ROOT / '_audit_reports' / 'fase4_conteudo_audit.json'
    output_path.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\n✅ Relatório JSON salvo em: _audit_reports/fase4_conteudo_audit.json')


if __name__ == '__main__':
    main()
