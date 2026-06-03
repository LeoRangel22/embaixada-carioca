"""
Auditoria Profunda - Fase 1: Higiene de Código
Embaixada Carioca — embaixadacarioca.com
"""
from bs4 import BeautifulSoup
import glob, re, os
from collections import defaultdict, Counter

html_files = sorted(glob.glob('*.html'))
print(f"Total de páginas HTML: {len(html_files)}\n")

# ============================================================
# 1. DUPLICAÇÕES DE CSS E JS
# ============================================================
print("=" * 60)
print("1. DUPLICAÇÕES DE CSS E JS")
print("=" * 60)

for page in html_files:
    with open(page, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # CSS duplicados
    css_links = [tag.get('href', '') for tag in soup.find_all('link', rel='stylesheet')]
    css_counts = Counter(css_links)
    for href, count in css_counts.items():
        if count > 1 and href:
            print(f"  [CSS DUPLICADO] {page}: '{href}' carregado {count}x")

    # JS duplicados
    js_srcs = [tag.get('src', '') for tag in soup.find_all('script', src=True)]
    js_counts = Counter(js_srcs)
    for src, count in js_counts.items():
        if count > 1 and src:
            print(f"  [JS DUPLICADO]  {page}: '{src}' carregado {count}x")

# ============================================================
# 2. PROBLEMAS DE HEADINGS (H1)
# ============================================================
print()
print("=" * 60)
print("2. PROBLEMAS DE HEADINGS (H1 MÚLTIPLOS / AUSENTES)")
print("=" * 60)

h1_issues = []
for page in html_files:
    with open(page, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    h1s = soup.find_all('h1')
    if len(h1s) == 0:
        h1_issues.append((page, 'AUSENTE', []))
    elif len(h1s) > 1:
        texts = [h.get_text(strip=True)[:60] for h in h1s]
        h1_issues.append((page, f'MÚLTIPLOS ({len(h1s)})', texts))

for page, status, texts in h1_issues:
    print(f"  [{status}] {page}")
    for t in texts:
        print(f"    → \"{t}\"")

# ============================================================
# 3. TITLE E META DESCRIPTION (TAMANHO)
# ============================================================
print()
print("=" * 60)
print("3. TITLE E META DESCRIPTION — TAMANHO FORA DO PADRÃO")
print("=" * 60)

title_issues = []
desc_issues = []
for page in html_files:
    with open(page, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    title = soup.title.string.strip() if soup.title and soup.title.string else ''
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    desc = desc_tag.get('content', '').strip() if desc_tag else ''

    if len(title) == 0:
        title_issues.append((page, len(title), 'AUSENTE', title))
    elif len(title) > 60:
        title_issues.append((page, len(title), 'LONGO', title))
    elif len(title) < 30:
        title_issues.append((page, len(title), 'CURTO', title))

    if len(desc) == 0:
        desc_issues.append((page, len(desc), 'AUSENTE', desc))
    elif len(desc) > 160:
        desc_issues.append((page, len(desc), 'LONGA', desc[:80] + '...'))
    elif len(desc) < 70:
        desc_issues.append((page, len(desc), 'CURTA', desc))

print(f"\n  Títulos com problemas: {len(title_issues)}")
for page, length, status, text in sorted(title_issues, key=lambda x: -x[1]):
    print(f"  [{status} — {length} chars] {page}")
    print(f"    \"{text[:80]}\"")

print(f"\n  Descrições com problemas: {len(desc_issues)}")
for page, length, status, text in sorted(desc_issues, key=lambda x: -x[1]):
    print(f"  [{status} — {length} chars] {page}")
    print(f"    \"{text[:100]}\"")

# ============================================================
# 4. HREFLANG AUSENTE
# ============================================================
print()
print("=" * 60)
print("4. HREFLANG AUSENTE OU INCOMPLETO")
print("=" * 60)

for page in html_files:
    with open(page, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    hreflangs = soup.find_all('link', attrs={'rel': 'alternate', 'hreflang': True})
    langs = [h.get('hreflang', '') for h in hreflangs]
    if not hreflangs:
        print(f"  [SEM HREFLANG] {page}")
    elif 'x-default' not in langs:
        print(f"  [SEM x-default] {page}: {langs}")
    elif 'en' not in langs:
        print(f"  [SEM en] {page}: {langs}")

# ============================================================
# 5. IMAGENS SEM SRCSET (RESPONSIVE IMAGES)
# ============================================================
print()
print("=" * 60)
print("5. IMAGENS SEM SRCSET — RESPONSIVE IMAGES")
print("=" * 60)

srcset_summary = {}
for page in html_files:
    with open(page, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    imgs = soup.find_all('img')
    no_srcset = [img for img in imgs if not img.get('srcset') and img.get('src', '').startswith('/assets/')]
    if no_srcset:
        srcset_summary[page] = [(img.get('src', ''), img.get('width', '?'), img.get('height', '?')) for img in no_srcset]

total_missing = sum(len(v) for v in srcset_summary.values())
print(f"  Total de imagens sem srcset (assets locais): {total_missing}")
for page, imgs in list(srcset_summary.items())[:10]:
    print(f"\n  {page}: {len(imgs)} imagens sem srcset")
    for src, w, h in imgs[:5]:
        print(f"    {src} ({w}x{h})")

# ============================================================
# 6. IMAGENS SEM loading=lazy OU SEM fetchpriority=high (HERO)
# ============================================================
print()
print("=" * 60)
print("6. IMAGENS — LOADING E FETCHPRIORITY")
print("=" * 60)

for page in html_files[:5]:
    with open(page, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    imgs = soup.find_all('img')
    for img in imgs:
        src = img.get('src', '')
        loading = img.get('loading', 'AUSENTE')
        fetchpriority = img.get('fetchpriority', '')
        if loading == 'AUSENTE' and '/assets/' in src:
            print(f"  [SEM loading] {page}: {src}")
        if 'hero' in src.lower() and not fetchpriority:
            print(f"  [HERO SEM fetchpriority=high] {page}: {src}")

# ============================================================
# 7. CANONICAL TAGS
# ============================================================
print()
print("=" * 60)
print("7. CANONICAL TAGS — AUSENTES OU INCONSISTENTES")
print("=" * 60)

canonical_issues = []
for page in html_files:
    with open(page, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if not canonical:
        canonical_issues.append((page, 'AUSENTE', ''))
    else:
        href = canonical.get('href', '')
        if not href.startswith('https://www.embaixadacarioca.com'):
            canonical_issues.append((page, 'URL INCORRETA', href))

print(f"  Páginas com problema de canonical: {len(canonical_issues)}")
for page, status, href in canonical_issues[:15]:
    print(f"  [{status}] {page}: {href}")

# ============================================================
# 8. INLINE STYLES EXCESSIVOS
# ============================================================
print()
print("=" * 60)
print("8. INLINE STYLES EXCESSIVOS (style= em elementos)")
print("=" * 60)

for page in html_files:
    with open(page, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    inline = soup.find_all(style=True)
    if len(inline) > 100:
        print(f"  [CRÍTICO — {len(inline)} elementos] {page}")
    elif len(inline) > 50:
        print(f"  [ALTO — {len(inline)} elementos] {page}")

# ============================================================
# 9. SITEMAP — URLs SEM LASTMOD
# ============================================================
print()
print("=" * 60)
print("9. SITEMAP — URLs SEM LASTMOD")
print("=" * 60)

import xml.etree.ElementTree as ET
tree = ET.parse('sitemap.xml')
root = tree.getroot()
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
no_lastmod = []
for url in root.findall('sm:url', ns):
    loc = url.find('sm:loc', ns)
    lastmod = url.find('sm:lastmod', ns)
    if lastmod is None and loc is not None:
        no_lastmod.append(loc.text)

print(f"  URLs sem lastmod: {len(no_lastmod)}")
for url in no_lastmod[:10]:
    print(f"  {url}")
if len(no_lastmod) > 10:
    print(f"  ... e mais {len(no_lastmod) - 10} URLs")

# ============================================================
# 10. ROBOTS.TXT E ARQUIVOS DE CONFIGURAÇÃO
# ============================================================
print()
print("=" * 60)
print("10. ROBOTS.TXT E CONFIGURAÇÃO")
print("=" * 60)

try:
    with open('robots.txt', 'r') as f:
        robots = f.read()
    print("  robots.txt:")
    print(robots[:500])
except:
    print("  robots.txt: NÃO ENCONTRADO")

print()
print("=" * 60)
print("RESUMO EXECUTIVO")
print("=" * 60)
print(f"  Total páginas HTML: {len(html_files)}")
print(f"  Páginas com H1 múltiplo ou ausente: {len(h1_issues)}")
print(f"  Páginas com title fora do padrão: {len(title_issues)}")
print(f"  Páginas com description fora do padrão: {len(desc_issues)}")
print(f"  Imagens sem srcset: {total_missing}")
print(f"  URLs no sitemap sem lastmod: {len(no_lastmod)}")
print(f"  Páginas sem canonical: {len([x for x in canonical_issues if x[1]=='AUSENTE'])}")
