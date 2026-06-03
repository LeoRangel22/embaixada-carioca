from bs4 import BeautifulSoup
import json, glob
from collections import Counter

print("=== AUDITORIA COMPLETA DE SCHEMAS EM TODAS AS PÁGINAS ===")
html_files = sorted(glob.glob('*.html'))

schema_issues = []
for page in html_files:
    with open(page, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    scripts = soup.find_all('script', type='application/ld+json')
    page_schemas = []
    page_issues = []
    
    for script in scripts:
        try:
            data = json.loads(script.string)
            stype = data.get('@type', '?')
            # Convert list to string for hashing
            if isinstance(stype, list):
                stype = str(stype)
            page_schemas.append(stype)
            
            # Verificar Restaurant schema
            if data.get('@type') == 'Restaurant':
                if not data.get('openingHours'):
                    page_issues.append('Restaurant: MISSING openingHours')
                if not data.get('aggregateRating'):
                    page_issues.append('Restaurant: MISSING aggregateRating')
                if not data.get('geo'):
                    page_issues.append('Restaurant: MISSING geo')
                if not data.get('image'):
                    page_issues.append('Restaurant: MISSING image')
                if not data.get('menu') and not data.get('hasMenu'):
                    page_issues.append('Restaurant: MISSING menu/hasMenu')
                    
            # Verificar @graph
            if isinstance(data.get('@graph'), list):
                for item in data['@graph']:
                    if item.get('@type') == 'Restaurant':
                        if not item.get('openingHours'):
                            page_issues.append('@graph Restaurant: MISSING openingHours')
                        if not item.get('aggregateRating'):
                            page_issues.append('@graph Restaurant: MISSING aggregateRating')
        except Exception as e:
            page_issues.append(f'JSON-LD PARSE ERROR: {e}')
    
    # Contar schemas duplicados
    schema_counts = Counter(page_schemas)
    for stype, count in schema_counts.items():
        if count > 1 and stype not in ['?']:
            page_issues.append(f'DUPLICATE SCHEMA: {stype} x{count}')
    
    if page_issues:
        schema_issues.append((page, page_issues))

print(f"Páginas com problemas de schema: {len(schema_issues)}")
for page, issues in schema_issues[:20]:
    print(f"\n  {page}:")
    for issue in issues:
        print(f"    - {issue}")

# Verificar hreflang em TODAS as páginas
print("\n=== PÁGINAS SEM HREFLANG ===")
no_hreflang = []
for page in html_files:
    with open(page, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    hreflangs = soup.find_all('link', attrs={'rel': 'alternate', 'hreflang': True})
    if not hreflangs:
        no_hreflang.append(page)
print(f"Total sem hreflang: {len(no_hreflang)}")
for p in no_hreflang:
    print(f"  {p}")

# Verificar imagens sem alt
print("\n=== IMAGENS SEM ALT (todas as páginas) ===")
total_imgs = 0
total_no_alt = 0
for page in html_files:
    with open(page, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    imgs = soup.find_all('img')
    no_alt = [img for img in imgs if not img.get('alt')]
    total_imgs += len(imgs)
    total_no_alt += len(no_alt)
    if no_alt:
        print(f"  {page}: {len(no_alt)}/{len(imgs)} sem alt")
print(f"TOTAL: {total_no_alt}/{total_imgs} imagens sem alt")

# Verificar links internos quebrados
print("\n=== LINKS INTERNOS (verificar existência) ===")
broken = []
for page in html_files:
    with open(page, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/') and not href.startswith('//') and not href.startswith('/#'):
            # Remove query string and anchor
            clean = href.split('?')[0].split('#')[0].lstrip('/')
            if clean and clean.endswith('.html'):
                import os
                if not os.path.exists(clean):
                    broken.append((page, href))

print(f"Links internos potencialmente quebrados: {len(broken)}")
for page, href in broken[:20]:
    print(f"  {page} -> {href}")
