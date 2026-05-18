"""
Otimização de fotos v2 — Embaixada Carioca
- Fotos de salão/banda: WebP quality=75 (melhor compressão, imperceptível visualmente)
- Foto de prato (bolinho): JPG otimizado quality=82 + ajustes (WebP ficou maior)
- Todos os ajustes de brilho/contraste/saturação/nitidez mantidos
"""
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

SRC_DIR = Path('assets/fotos')
DST_DIR = Path('assets/fotos')

# (arquivo, categoria, brilho, contraste, saturação, nitidez, formato_saida, quality)
PHOTO_CONFIGS = [
    # Salão/ambiente — dia, luz natural
    ('salao-almoco-01.jpg',      'salao',      1.05, 1.10, 1.15, 1.30, 'webp', 75),
    ('salao-almoco-02.jpg',      'salao',      1.05, 1.10, 1.15, 1.30, 'webp', 75),
    ('salao-almoco-03.jpg',      'salao',      1.05, 1.10, 1.15, 1.30, 'webp', 75),
    ('salao-pao-de-acucar.jpg',  'salao',      1.05, 1.12, 1.18, 1.30, 'webp', 75),
    # Entardecer — preservar dourado
    ('salao-entardecer-vista.jpg','entardecer', 1.02, 1.15, 1.22, 1.40, 'webp', 75),
    # Banda ao vivo — luz natural forte
    ('banda-pao-de-acucar-01.jpg','banda',      1.03, 1.15, 1.18, 1.40, 'webp', 75),
    ('banda-pao-de-acucar-02.jpg','banda',      1.03, 1.15, 1.18, 1.40, 'webp', 75),
    ('banda-pao-de-acucar-03.jpg','banda',      1.03, 1.15, 1.18, 1.40, 'webp', 75),
    ('banda-pao-de-acucar-04.jpg','banda',      1.03, 1.15, 1.18, 1.40, 'webp', 75),
    # Prato (bolinho) — close, fundo escuro: JPG é melhor aqui
    ('bolinho-bacalhau.jpg',     'prato',      1.08, 1.20, 1.25, 1.60, 'jpg',  82),
]

results = []

for filename, category, brightness, contrast, saturation, sharpness, fmt, quality in PHOTO_CONFIGS:
    src_path = SRC_DIR / filename
    if not src_path.exists():
        print(f"⚠️  Não encontrado: {src_path}")
        continue

    orig_size_kb = src_path.stat().st_size // 1024

    img = Image.open(src_path).convert('RGB')

    # Ajustes de imagem
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Color(img).enhance(saturation)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)

    # Nitidez extra para pratos
    if category == 'prato':
        img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=3))

    # Salvar no formato correto
    if fmt == 'webp':
        out_name = filename.replace('.jpg', '.webp').replace('.jpeg', '.webp')
        out_path = DST_DIR / out_name
        img.save(out_path, 'WEBP', quality=quality, method=6)
    else:
        out_name = filename  # mantém .jpg
        out_path = DST_DIR / out_name
        img.save(out_path, 'JPEG', quality=quality, optimize=True)

    new_size_kb = out_path.stat().st_size // 1024
    reduction = round((1 - new_size_kb / orig_size_kb) * 100, 1)

    results.append({
        'arquivo': filename,
        'saida': out_name,
        'categoria': category,
        'orig_kb': orig_size_kb,
        'new_kb': new_size_kb,
        'reducao': reduction,
    })

    arrow = "↓" if reduction > 0 else "↑"
    print(f"✅ {filename} → {out_name}")
    print(f"   {category:12} | {orig_size_kb}KB {arrow} {new_size_kb}KB ({abs(reduction)}% {'menor' if reduction > 0 else 'maior'})")

# Resumo
total_orig = sum(r['orig_kb'] for r in results)
total_new  = sum(r['new_kb']  for r in results)
total_red  = round((1 - total_new / total_orig) * 100, 1)

print(f"\n{'='*60}")
print(f"RESUMO: {len(results)} fotos otimizadas")
print(f"  Original total : {total_orig}KB ({total_orig//1024}MB)")
print(f"  Otimizado total: {total_new}KB ({total_new//1024}MB)")
print(f"  Redução total  : {total_red}%  (economia de {total_orig - total_new}KB)")
