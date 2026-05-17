#!/usr/bin/env python3
"""Auditoria completa do site embaixadacarioca.com"""
import os, re, json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_URL = "https://www.embaixadacarioca.com/"
DEPLOY_DIR = "/home/ubuntu/embaixada-deploy"

# Páginas principais a auditar (excluir versões antigas e offline)
SKIP = {'Home v1.html', 'Home v2.html', 'offline.html', '404.html'}

issues = []

def add_issue(file, severity, category, description):
    issues.append({
        'file': file,
        'severity': severity,  # CRÍTICO / AVISO / INFO
        'category': category,
        'description': description
    })

# Coletar todos os arquivos HTML válidos
html_files = []
for root, dirs, files in os.walk(DEPLOY_DIR):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules']]
    for f in files:
        if f.endswith('.html') and f not in SKIP:
            rel = os.path.relpath(os.path.join(root, f), DEPLOY_DIR)
            html_files.append(rel)
html_files.sort()

# Assets existentes
assets = set()
for root, dirs, files in os.walk(DEPLOY_DIR):
    dirs[:] = [d for d in dirs if d not in ['.git']]
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), DEPLOY_DIR)
        assets.add(rel)

def resolve_asset(href, file_path):
    """Resolve um href relativo para caminho no deploy dir"""
    if href.startswith('http') or href.startswith('//') or href.startswith('mailto:') or href.startswith('tel:') or href.startswith('#') or href.startswith('javascript:'):
        return None
    file_dir = os.path.dirname(file_path)
    resolved = os.path.normpath(os.path.join(file_dir, href))
    return resolved

# Páginas internas válidas
internal_pages = set(html_files)

for rel_path in html_files:
    full_path = os.path.join(DEPLOY_DIR, rel_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    # ── 1. META TAGS ──────────────────────────────────────────────
    title = soup.find('title')
    if not title or not title.text.strip():
        add_issue(rel_path, 'CRÍTICO', 'SEO', 'Title tag ausente ou vazia')
    elif len(title.text.strip()) < 30:
        add_issue(rel_path, 'AVISO', 'SEO', f'Title muito curto: "{title.text.strip()}"')
    elif len(title.text.strip()) > 70:
        add_issue(rel_path, 'AVISO', 'SEO', f'Title muito longo ({len(title.text.strip())} chars)')
    
    desc = soup.find('meta', attrs={'name': 'description'})
    if not desc or not desc.get('content', '').strip():
        add_issue(rel_path, 'CRÍTICO', 'SEO', 'Meta description ausente')
    elif len(desc.get('content', '')) < 100:
        add_issue(rel_path, 'AVISO', 'SEO', f'Meta description curta ({len(desc.get("content",""))} chars)')
    
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if not canonical:
        add_issue(rel_path, 'AVISO', 'SEO', 'Link canonical ausente')
    
    # ── 2. H1 ──────────────────────────────────────────────────────
    h1s = soup.find_all('h1')
    if len(h1s) == 0:
        add_issue(rel_path, 'CRÍTICO', 'SEO', 'H1 ausente')
    elif len(h1s) > 1:
        add_issue(rel_path, 'AVISO', 'SEO', f'Múltiplos H1 ({len(h1s)})')
    
    # ── 3. OG TAGS ─────────────────────────────────────────────────
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    og_image = soup.find('meta', attrs={'property': 'og:image'})
    og_desc = soup.find('meta', attrs={'property': 'og:description'})
    if not og_title:
        add_issue(rel_path, 'AVISO', 'SEO', 'og:title ausente')
    if not og_image:
        add_issue(rel_path, 'AVISO', 'SEO', 'og:image ausente')
    if not og_desc:
        add_issue(rel_path, 'AVISO', 'SEO', 'og:description ausente')
    
    # ── 4. LINKS INTERNOS ──────────────────────────────────────────
    for a in soup.find_all('a', href=True):
        href = a['href'].strip()
        if href.startswith('#') or href.startswith('javascript:') or href.startswith('mailto:') or href.startswith('tel:') or href.startswith('http') or href.startswith('//'):
            continue
        # Link interno relativo
        resolved = resolve_asset(href.split('?')[0].split('#')[0], rel_path)
        if resolved and not os.path.exists(os.path.join(DEPLOY_DIR, resolved)):
            add_issue(rel_path, 'CRÍTICO', 'Links', f'Link quebrado: {href} → {resolved}')
    
    # ── 5. IMAGENS ─────────────────────────────────────────────────
    for img in soup.find_all('img'):
        src = img.get('src', '').strip()
        if not src or src.startswith('data:') or src.startswith('http'):
            pass
        else:
            resolved = resolve_asset(src.split('?')[0], rel_path)
            if resolved and not os.path.exists(os.path.join(DEPLOY_DIR, resolved)):
                add_issue(rel_path, 'CRÍTICO', 'Imagens', f'Imagem quebrada: {src}')
        
        # Alt text
        if not img.get('alt'):
            add_issue(rel_path, 'AVISO', 'Acessibilidade', f'Imagem sem alt: {src[:60]}')
    
    # ── 6. SCHEMA JSON-LD ──────────────────────────────────────────
    schemas = soup.find_all('script', attrs={'type': 'application/ld+json'})
    for s in schemas:
        try:
            data = json.loads(s.string or '{}')
        except json.JSONDecodeError as e:
            add_issue(rel_path, 'CRÍTICO', 'Schema', f'JSON-LD inválido: {e}')
    
    # ── 7. VIEWPORT META ───────────────────────────────────────────
    viewport = soup.find('meta', attrs={'name': 'viewport'})
    if not viewport:
        add_issue(rel_path, 'CRÍTICO', 'Mobile', 'Meta viewport ausente')
    
    # ── 8. LANG ────────────────────────────────────────────────────
    html_tag = soup.find('html')
    if html_tag and not html_tag.get('lang'):
        add_issue(rel_path, 'AVISO', 'Acessibilidade', 'Atributo lang ausente no <html>')
    
    # ── 9. HREFLANG ────────────────────────────────────────────────
    hreflangs = soup.find_all('link', attrs={'rel': 'alternate', 'hreflang': True})
    if not hreflangs and rel_path not in ['404.html', 'offline.html']:
        add_issue(rel_path, 'AVISO', 'SEO', 'hreflang ausente')
    
    # ── 10. SCRIPTS E CSS EXTERNOS ────────────────────────────────
    for script in soup.find_all('script', src=True):
        src = script['src'].strip()
        if src.startswith('http') or src.startswith('//'):
            continue
        resolved = resolve_asset(src.split('?')[0], rel_path)
        if resolved and not os.path.exists(os.path.join(DEPLOY_DIR, resolved)):
            add_issue(rel_path, 'CRÍTICO', 'Scripts', f'Script quebrado: {src}')
    
    for link in soup.find_all('link', rel=True):
        if 'stylesheet' in link.get('rel', []):
            href = link.get('href', '').strip()
            if href.startswith('http') or href.startswith('//') or not href:
                continue
            resolved = resolve_asset(href.split('?')[0], rel_path)
            if resolved and not os.path.exists(os.path.join(DEPLOY_DIR, resolved)):
                add_issue(rel_path, 'CRÍTICO', 'CSS', f'Stylesheet quebrado: {href}')

# ── RELATÓRIO ──────────────────────────────────────────────────────
print(f"\n{'='*70}")
print(f"AUDITORIA COMPLETA — {len(html_files)} páginas auditadas")
print(f"{'='*70}")

criticos = [i for i in issues if i['severity'] == 'CRÍTICO']
avisos = [i for i in issues if i['severity'] == 'AVISO']

print(f"\nRESUMO: {len(criticos)} CRÍTICOS | {len(avisos)} AVISOS\n")

if criticos:
    print("── CRÍTICOS ──────────────────────────────────────────────────")
    for i in criticos:
        print(f"  [{i['category']}] {i['file']}")
        print(f"    → {i['description']}")

if avisos:
    print("\n── AVISOS ────────────────────────────────────────────────────")
    # Agrupar por categoria
    from collections import defaultdict
    by_cat = defaultdict(list)
    for i in avisos:
        by_cat[i['category']].append(i)
    for cat, items in sorted(by_cat.items()):
        print(f"\n  [{cat}] ({len(items)} ocorrências)")
        for i in items[:5]:  # Mostrar até 5 por categoria
            print(f"    {i['file']}: {i['description']}")
        if len(items) > 5:
            print(f"    ... e mais {len(items)-5} ocorrências")

print(f"\n{'='*70}")
