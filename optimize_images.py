#!/usr/bin/env python3
"""
Otimização de imagens para PageSpeed Insights:
1. Recomprime imagens WebP com qualidade 72 (era ~85)
2. Gera versões mobile (400px) para as imagens grandes sem versão mobile
3. Mantém backups das originais
"""
from PIL import Image
import os, shutil, glob

ASSETS = '/home/ubuntu/embaixada-deploy/assets'
BACKUP = '/home/ubuntu/embaixada-deploy/assets_backup_orig'

# Criar backup se não existir
if not os.path.exists(BACKUP):
    shutil.copytree(ASSETS, BACKUP)
    print(f"✅ Backup criado em {BACKUP}")

def recompress_webp(path, quality=72):
    """Recomprime um WebP com qualidade menor."""
    img = Image.open(path)
    orig_size = os.path.getsize(path)
    # Salvar com qualidade menor
    img.save(path, 'WEBP', quality=quality, method=6)
    new_size = os.path.getsize(path)
    saving = (orig_size - new_size) / orig_size * 100
    return orig_size, new_size, saving

def generate_mobile_version(path, max_width=400, quality=70):
    """Gera versão mobile de uma imagem."""
    img = Image.open(path)
    w, h = img.size
    if w <= max_width:
        return None
    # Calcular nova altura mantendo proporção
    new_h = int(h * max_width / w)
    img_resized = img.resize((max_width, new_h), Image.LANCZOS)
    # Gerar nome do arquivo mobile
    base = path.rsplit('.', 1)[0]
    mobile_path = f"{base}-mobile-opt.webp"
    img_resized.save(mobile_path, 'WEBP', quality=quality, method=6)
    return mobile_path

# ── 1. Recomprimir imagens grandes (>80KB) ──────────────────────────────────
print("\n=== Recomprimindo WebPs grandes ===")
total_saved = 0
webp_files = glob.glob(f'{ASSETS}/*.webp')
webp_files.sort(key=lambda x: os.path.getsize(x), reverse=True)

for path in webp_files:
    size = os.path.getsize(path)
    if size < 80 * 1024:  # Pular arquivos < 80KB
        continue
    fname = os.path.basename(path)
    # Pular arquivos que já são versões mobile/400w (já são pequenos)
    if any(s in fname for s in ['-mobile', '-400w', '-800w', 'logo', 'thumb']):
        continue
    
    orig, new, pct = recompress_webp(path, quality=72)
    total_saved += (orig - new)
    print(f"  {fname}: {orig//1024}KB → {new//1024}KB (-{pct:.0f}%)")

print(f"\n  Total economizado: {total_saved//1024}KB")

# ── 2. Recomprimir hero.jpg ──────────────────────────────────────────────────
print("\n=== Recomprimindo hero.jpg ===")
hero_jpg = f'{ASSETS}/hero.jpg'
if os.path.exists(hero_jpg):
    img = Image.open(hero_jpg)
    orig_size = os.path.getsize(hero_jpg)
    # Converter para WebP e salvar como hero.webp (já deve existir, mas recomprimir)
    hero_webp = f'{ASSETS}/hero.webp'
    if os.path.exists(hero_webp):
        orig_webp = os.path.getsize(hero_webp)
        img_hero = Image.open(hero_webp)
        img_hero.save(hero_webp, 'WEBP', quality=72, method=6)
        new_webp = os.path.getsize(hero_webp)
        print(f"  hero.webp: {orig_webp//1024}KB → {new_webp//1024}KB")
    # Recomprimir o JPG também
    img.save(hero_jpg, 'JPEG', quality=75, optimize=True)
    new_size = os.path.getsize(hero_jpg)
    print(f"  hero.jpg: {orig_size//1024}KB → {new_size//1024}KB")

# ── 3. Gerar versões 400w para imagens sem versão mobile ────────────────────
print("\n=== Gerando versões 400w para imagens sem versão mobile ===")

# Imagens que precisam de versão 400w mas não têm
needs_400w = [
    'fabio-almoco-salmao-pao-acucar.webp',  # 900x1350, 249KB — exibida em 318px no mobile
    'hero-800w.webp',  # já tem hero-400w.webp, pular
]

for fname in needs_400w:
    path = f'{ASSETS}/{fname}'
    if not os.path.exists(path):
        continue
    base = fname.rsplit('.', 1)[0]
    out_400 = f'{ASSETS}/{base}-400w.webp'
    if os.path.exists(out_400):
        print(f"  {fname}: já tem versão 400w ({os.path.getsize(out_400)//1024}KB)")
        continue
    
    img = Image.open(path)
    w, h = img.size
    new_h = int(h * 400 / w)
    img_400 = img.resize((400, new_h), Image.LANCZOS)
    img_400.save(out_400, 'WEBP', quality=70, method=6)
    print(f"  {fname} → {os.path.basename(out_400)}: {os.path.getsize(out_400)//1024}KB")

# ── 4. Verificar resultado final ─────────────────────────────────────────────
print("\n=== Resultado final das imagens problemáticas ===")
check = [
    'fabio-almoco-salmao-pao-acucar.webp',
    'hero.jpg',
    'hero-800w.webp',
    'cafe-manha-pao-acucar-frente.webp',
    'hero.webp',
]
for fname in check:
    path = f'{ASSETS}/{fname}'
    if os.path.exists(path):
        img = Image.open(path)
        size = os.path.getsize(path)
        print(f"  {fname}: {img.size[0]}x{img.size[1]} | {size//1024}KB")
