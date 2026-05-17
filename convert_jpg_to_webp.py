#!/usr/bin/env python3
"""
1. Converte JPGs sem versão WebP para WebP (qualidade 72)
2. Atualiza src nos HTMLs para usar WebP com fallback
3. Atualiza imagens que têm WebP mas ainda usam JPG no src
"""
import os, glob, re
from PIL import Image

DEPLOY = '/home/ubuntu/embaixada-deploy'

def jpg_to_webp(jpg_path, quality=72):
    """Converte JPG para WebP."""
    webp_path = jpg_path.rsplit('.', 1)[0] + '.webp'
    img = Image.open(jpg_path)
    img.save(webp_path, 'WEBP', quality=quality, method=6)
    jpg_size = os.path.getsize(jpg_path)
    webp_size = os.path.getsize(webp_path)
    return webp_path, jpg_size, webp_size

# ── 1. Converter JPGs sem WebP ───────────────────────────────────────────────
print("=== Convertendo JPGs para WebP ===")
total_saved = 0

# cafe/ directory
cafe_jpgs = glob.glob(f'{DEPLOY}/assets/cafe/*.jpg')
# academia/ directory
academia_jpgs = glob.glob(f'{DEPLOY}/assets/academia/*.jpg')
# root assets JPGs que têm WebP mas ainda são referenciados como JPG
root_jpgs_with_webp = [
    f'{DEPLOY}/assets/hero.jpg',
    f'{DEPLOY}/assets/carne-seca-mandioca.jpg',
    f'{DEPLOY}/assets/bobo-camarao-real.jpg',
    f'{DEPLOY}/assets/fabio-almoco-mesa-completa.jpg',
    f'{DEPLOY}/assets/fabio-almoco-salmao-maracuja.jpg',
    f'{DEPLOY}/assets/fabio-almoco-picanha-fritas.jpg',
    f'{DEPLOY}/assets/fabio-feijoada-caldeiron.jpg',
    f'{DEPLOY}/assets/fabio-chef-wallace-sorrindo.jpg',
    f'{DEPLOY}/assets/gin-tonic-vista.jpg',
    f'{DEPLOY}/assets/cocktails-vista.jpg',
    f'{DEPLOY}/assets/entardecer-banda-opt.jpg',
    f'{DEPLOY}/assets/sanduiche-vista.jpg',
    f'{DEPLOY}/assets/casal-romantico-opt.jpg',
    f'{DEPLOY}/assets/cafe-da-manha-mesa-opt.jpg',
]

all_jpgs_to_convert = cafe_jpgs + academia_jpgs

for jpg_path in sorted(all_jpgs_to_convert):
    fname = os.path.basename(jpg_path)
    webp_path = jpg_path.rsplit('.', 1)[0] + '.webp'
    if os.path.exists(webp_path):
        print(f"  SKIP {fname} (WebP já existe)")
        continue
    webp_path, jpg_size, webp_size = jpg_to_webp(jpg_path)
    saved = jpg_size - webp_size
    total_saved += saved
    print(f"  {fname}: {jpg_size//1024}KB → {webp_size//1024}KB (-{saved//1024}KB)")

print(f"\n  Total economizado: {total_saved//1024}KB")

# ── 2. Atualizar src nos HTMLs para usar WebP ────────────────────────────────
print("\n=== Atualizando src nos HTMLs para WebP ===")

html_files = glob.glob(f'{DEPLOY}/**/*.html', recursive=True)
html_files += glob.glob(f'{DEPLOY}/*.html')
html_files = list(set(html_files))

# Padrões de substituição: src="...jpg" → src="...webp"
# Para imagens que TÊM versão WebP disponível
def update_html_img_src(content, base_path=''):
    """Substitui src de JPGs por WebP quando o WebP existe."""
    changes = 0
    
    def replace_jpg_src(match):
        nonlocal changes
        full_match = match.group(0)
        src_val = match.group(1)
        
        # Calcular caminho absoluto do WebP
        if src_val.startswith('/assets/'):
            webp_src = src_val.rsplit('.', 1)[0] + '.webp'
            webp_abs = f'{DEPLOY}{webp_src}'
        elif src_val.startswith('assets/'):
            webp_src = src_val.rsplit('.', 1)[0] + '.webp'
            webp_abs = f'{DEPLOY}/{webp_src}'
        elif src_val.startswith('../assets/'):
            webp_src = src_val.rsplit('.', 1)[0] + '.webp'
            webp_abs = f'{DEPLOY}/{webp_src.replace("../", "")}'
        else:
            return full_match
        
        if os.path.exists(webp_abs):
            changes += 1
            return full_match.replace(src_val, webp_src)
        return full_match
    
    # Substituir src="...jpg" → src="...webp"
    new_content = re.sub(
        r'src=["\']([^"\']+\.jpg)["\']',
        replace_jpg_src,
        content
    )
    return new_content, changes

total_html_changes = 0
for html_path in sorted(html_files):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    content, changes = update_html_img_src(content)
    
    if changes > 0:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        total_html_changes += changes
        rel = os.path.relpath(html_path, DEPLOY)
        print(f"  ✅ {rel}: {changes} imagens atualizadas")

print(f"\n  Total de substituições: {total_html_changes}")

# ── 3. Verificação final ─────────────────────────────────────────────────────
print("\n=== Verificação final ===")
pages_check = ['almoco.html', 'index.html', 'cafe-da-manha.html', 'feijoada.html']
for page in pages_check:
    path = f'{DEPLOY}/{page}'
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    remaining_jpgs = re.findall(r'src=["\']([^"\']+\.jpg)["\']', content)
    heavy = [j for j in remaining_jpgs if 'hero' not in j]
    if heavy:
        print(f"  {page}: {len(heavy)} JPGs restantes: {heavy[:3]}")
    else:
        print(f"  ✅ {page}: sem JPGs pesados")
