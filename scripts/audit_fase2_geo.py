#!/usr/bin/env python3
"""
audit_fase2_geo.py — Auditoria GEO Profunda
Embaixada Carioca — embaixadacarioca.com
Mapeia: NAP inconsistências, schema Restaurant, openingHours, aggregateRating,
        ambiguidade semântica Pão de Açúcar, keywords nas landing pages.
"""
from __future__ import annotations
import glob, json, re
from bs4 import BeautifulSoup
from collections import Counter

html_files = sorted(glob.glob('*.html') + glob.glob('en/*.html') + glob.glob('es/*.html'))
html_files = [f for f in html_files if f not in ('404.html','offline.html')]

print(f"Total de páginas: {len(html_files)}\n")

# ─────────────────────────────────────────────────────────────
# 1. NAP — Variações de endereço, telefone e nome
# ─────────────────────────────────────────────────────────────
print("="*60)
print("1. NAP — VARIAÇÕES DE ENDEREÇO, TELEFONE E NOME")
print("="*60)

address_variants = Counter()
phone_variants = Counter()
name_variants = Counter()

for page in html_files:
    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')

    # Extrair schemas JSON-LD
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string or '{}')
            schemas = data if isinstance(data, list) else [data]
            for s in schemas:
                if isinstance(s, dict):
                    addr = s.get('address', {})
                    if isinstance(addr, dict):
                        street = addr.get('streetAddress', '')
                        if street:
                            address_variants[street.strip()] += 1
                    tel = s.get('telephone', '')
                    if tel:
                        phone_variants[tel.strip()] += 1
                    nm = s.get('name', '')
                    if nm and ('Embaixada' in nm or 'Restaurant' in nm or 'Restaurante' in nm):
                        name_variants[nm.strip()] += 1
        except Exception:
            pass

print(f"\n  Variações de streetAddress encontradas: {len(address_variants)}")
for addr, count in address_variants.most_common():
    print(f"    [{count}x] \"{addr}\"")

print(f"\n  Variações de telefone encontradas: {len(phone_variants)}")
for tel, count in phone_variants.most_common():
    print(f"    [{count}x] \"{tel}\"")

print(f"\n  Variações de nome encontradas: {len(name_variants)}")
for nm, count in name_variants.most_common():
    print(f"    [{count}x] \"{nm}\"")

# ─────────────────────────────────────────────────────────────
# 2. SCHEMA RESTAURANT — openingHours e aggregateRating
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("2. SCHEMA RESTAURANT — openingHours e aggregateRating")
print("="*60)

pages_with_restaurant_schema = []
pages_missing_opening_hours = []
pages_missing_rating = []
pages_missing_price = []
pages_missing_cuisine = []
pages_missing_menu = []
pages_missing_reservation = []

for page in html_files:
    with open(page, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string or '{}')
            schemas = data if isinstance(data, list) else [data]
            for s in schemas:
                if not isinstance(s, dict):
                    continue
                stype = s.get('@type', '')
                if stype in ('Restaurant', 'FoodEstablishment') or \
                   (isinstance(stype, list) and any(t in ('Restaurant','FoodEstablishment') for t in stype)):
                    pages_with_restaurant_schema.append(page)
                    if not s.get('openingHours') and not s.get('openingHoursSpecification'):
                        pages_missing_opening_hours.append(page)
                    if not s.get('aggregateRating'):
                        pages_missing_rating.append(page)
                    if not s.get('priceRange'):
                        pages_missing_price.append(page)
                    if not s.get('servesCuisine'):
                        pages_missing_cuisine.append(page)
                    if not s.get('hasMenu') and not s.get('menu'):
                        pages_missing_menu.append(page)
                    if not s.get('acceptsReservations') and not s.get('reservations'):
                        pages_missing_reservation.append(page)
        except Exception:
            pass

print(f"\n  Páginas com schema Restaurant: {len(pages_with_restaurant_schema)}")
print(f"  Páginas SEM openingHours:      {len(pages_missing_opening_hours)}")
for p in pages_missing_opening_hours[:8]: print(f"    {p}")
print(f"  Páginas SEM aggregateRating:   {len(pages_missing_rating)}")
for p in pages_missing_rating[:8]: print(f"    {p}")
print(f"  Páginas SEM priceRange:        {len(pages_missing_price)}")
print(f"  Páginas SEM servesCuisine:     {len(pages_missing_cuisine)}")
print(f"  Páginas SEM hasMenu:           {len(pages_missing_menu)}")
print(f"  Páginas SEM acceptsReservations: {len(pages_missing_reservation)}")

# ─────────────────────────────────────────────────────────────
# 3. SCHEMA — Extrair um exemplo completo para referência
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("3. SCHEMA RESTAURANT — EXEMPLO ATUAL (index.html)")
print("="*60)

with open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

for script in soup.find_all('script', type='application/ld+json'):
    try:
        data = json.loads(script.string or '{}')
        schemas = data if isinstance(data, list) else [data]
        for s in schemas:
            if isinstance(s, dict) and s.get('@type') in ('Restaurant', 'FoodEstablishment'):
                print(json.dumps(s, ensure_ascii=False, indent=2)[:2000])
    except Exception:
        pass

# ─────────────────────────────────────────────────────────────
# 4. AMBIGUIDADE SEMÂNTICA — "Pão de Açúcar" nas landing pages
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("4. AMBIGUIDADE SEMÂNTICA — PAO DE ACUCAR NAS LANDING PAGES")
print("="*60)

TARGET_PAGES = [
    'restaurante-morro-da-urca.html',
    'almoco-morro-da-urca.html',
    'cafe-da-manha.html',
    'cafe-da-manha-pao-de-acucar.html',
    'parque-bondinho-pao-de-acucar.html',
    'parque-bondinho.html',
    'morro-da-urca.html',
]

KEYWORDS = [
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

for page in TARGET_PAGES:
    try:
        with open(page, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        text = soup.get_text(separator=' ').lower()
        text_norm = re.sub(r'[áàãâä]','a', re.sub(r'[éèê]','e', re.sub(r'[íì]','i',
                   re.sub(r'[óòõô]','o', re.sub(r'[úùü]','u', re.sub(r'[ç]','c', text))))))
        print(f"\n  {page}:")
        for kw in KEYWORDS:
            kw_norm = re.sub(r'[áàãâä]','a', re.sub(r'[éèê]','e', re.sub(r'[íì]','i',
                     re.sub(r'[óòõô]','o', re.sub(r'[úùü]','u', re.sub(r'[ç]','c', kw.lower()))))))
            count = text_norm.count(kw_norm)
            status = '✅' if count >= 2 else ('⚠️ 1x' if count == 1 else '❌ 0x')
            print(f"    {status}  \"{kw}\" ({count}x)")
    except FileNotFoundError:
        print(f"\n  {page}: NÃO ENCONTRADO")

# ─────────────────────────────────────────────────────────────
# 5. FAQ SCHEMA — Verificar presença nas landing pages
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("5. FAQ SCHEMA — PRESENÇA NAS LANDING PAGES")
print("="*60)

for page in TARGET_PAGES:
    try:
        with open(page, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        has_faq = False
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string or '{}')
                schemas = data if isinstance(data, list) else [data]
                for s in schemas:
                    if isinstance(s, dict) and s.get('@type') == 'FAQPage':
                        has_faq = True
            except Exception:
                pass
        print(f"  {'✅ FAQ' if has_faq else '❌ SEM FAQ'}  {page}")
    except FileNotFoundError:
        pass

# ─────────────────────────────────────────────────────────────
# 6. GEO — Verificar se há BreadcrumbList nas páginas internas
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("6. BREADCRUMB SCHEMA — PRESENÇA NAS LANDING PAGES")
print("="*60)

for page in TARGET_PAGES:
    try:
        with open(page, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        has_bc = False
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string or '{}')
                schemas = data if isinstance(data, list) else [data]
                for s in schemas:
                    if isinstance(s, dict) and s.get('@type') == 'BreadcrumbList':
                        has_bc = True
            except Exception:
                pass
        print(f"  {'✅ Breadcrumb' if has_bc else '❌ SEM Breadcrumb'}  {page}")
    except FileNotFoundError:
        pass
