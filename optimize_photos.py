"""
Otimização de fotos reais — Embaixada Carioca
Aplica ajustes de brilho, contraste, saturação e nitidez por categoria,
converte para WebP e gera relatório de ganho de tamanho.
"""
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import shutil

SRC_DIR = Path('assets/fotos')
DST_DIR = Path('assets/fotos')  # sobrescreve no mesmo diretório

# Parâmetros por categoria
# Cada entrada: (arquivo, categoria, brilho, contraste, saturação, nitidez)
# brilho: 1.0 = original, 1.1 = +10%
# contraste: 1.0 = original, 1.15 = +15%
# saturação (color): 1.0 = original, 1.2 = +20%
# nitidez (sharpness): 1.0 = original, 1.5 = +50%

PHOTO_CONFIGS = {
    # Fotos de salão/ambiente — dia, luz natural
    # Objetivo: mais brilho (+5%), contraste (+10%), saturação (+15%), nitidez (+30%)
    'salao-almoco-01.jpg': ('salao', 1.05, 1.10, 1.15, 1.30),
    'salao-almoco-02.jpg': ('salao', 1.05, 1.10, 1.15, 1.30),
    'salao-almoco-03.jpg': ('salao', 1.05, 1.10, 1.15, 1.30),
    'salao-pao-de-acucar.jpg': ('salao', 1.05, 1.12, 1.18, 1.30),

    # Foto de salão ao entardecer — luz dourada já presente
    # Objetivo: preservar o dourado (+saturação +20%), contraste (+15%), nitidez (+40%)
    'salao-entardecer-vista.jpg': ('entardecer', 1.02, 1.15, 1.20, 1.40),

    # Fotos de banda ao vivo — luz natural forte, Pão de Açúcar ao fundo
    # Objetivo: contraste (+15%), saturação (+18%), nitidez (+40%), brilho neutro
    'banda-pao-de-acucar-01.jpg': ('banda', 1.03, 1.15, 1.18, 1.40),
    'banda-pao-de-acucar-02.jpg': ('banda', 1.03, 1.15, 1.18, 1.40),
    'banda-pao-de-acucar-03.jpg': ('banda', 1.03, 1.15, 1.18, 1.40),
    'banda-pao-de-acucar-04.jpg': ('banda', 1.03, 1.15, 1.18, 1.40),

    # Foto de prato (bolinho de bacalhau) — close, fundo escuro
    # Objetivo: brilho (+8%), contraste (+20%), saturação (+25%), nitidez máxima (+60%)
    'bolinho-bacalhau.jpg': ('prato', 1.08, 1.20, 1.25, 1.60),
}

results = []

for filename, (category, brightness, contrast, saturation, sharpness) in PHOTO_CONFIGS.items():
    src_path = SRC_DIR / filename
    if not src_path.exists():
        print(f"⚠️  Não encontrado: {src_path}")
        continue

    # Tamanho original
    orig_size_kb = src_path.stat().st_size // 1024

    # Abrir imagem
    img = Image.open(src_path).convert('RGB')

    # Aplicar ajustes em sequência
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Color(img).enhance(saturation)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)

    # Aplicar leve filtro de nitidez adicional para pratos
    if category == 'prato':
        img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=3))

    # Salvar como WebP (qualidade 82 — ótimo equilíbrio visual/tamanho)
    webp_name = filename.replace('.jpg', '.webp').replace('.jpeg', '.webp')
    webp_path = DST_DIR / webp_name
    img.save(webp_path, 'WEBP', quality=82, method=6)

    new_size_kb = webp_path.stat().st_size // 1024
    reduction = round((1 - new_size_kb / orig_size_kb) * 100, 1)

    results.append({
        'arquivo': filename,
        'webp': webp_name,
        'categoria': category,
        'orig_kb': orig_size_kb,
        'new_kb': new_size_kb,
        'reducao': reduction,
        'brilho': brightness,
        'contraste': contrast,
        'saturacao': saturation,
        'nitidez': sharpness,
    })

    print(f"✅ {filename} → {webp_name}")
    print(f"   Categoria: {category} | {orig_size_kb}KB → {new_size_kb}KB ({reduction}% menor)")
    print(f"   Ajustes: brilho={brightness} contraste={contrast} saturação={saturation} nitidez={sharpness}")

# Resumo
total_orig = sum(r['orig_kb'] for r in results)
total_new = sum(r['new_kb'] for r in results)
total_reduction = round((1 - total_new / total_orig) * 100, 1)

print(f"\n{'='*60}")
print(f"RESUMO: {len(results)} fotos otimizadas")
print(f"Tamanho original total: {total_orig}KB")
print(f"Tamanho otimizado total: {total_new}KB")
print(f"Redução total: {total_reduction}%")
print(f"Economia: {total_orig - total_new}KB")
