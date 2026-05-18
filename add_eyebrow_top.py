from pathlib import Path
from bs4 import BeautifulSoup

# Páginas alvo
PT_PAGES = [
    'cafe-da-manha.html',
    'almoco.html',
    'entardecer.html',
    'eventos.html',
    'cardapio.html',
    'guia-do-rio.html',
]

# Textos por idioma
EYEBROW = {
    'pt': 'Restaurante do Bondinho · Restaurante Carioca Tradicional de Qualidade · Morro da Urca · Parque Bondinho Pão de Açúcar · Rio de Janeiro · Brasil',
    'en': 'Cable Car Restaurant · Traditional Carioca Restaurant · Morro da Urca · Parque Bondinho Sugarloaf Mountain · Rio de Janeiro · Brazil',
    'es': 'Restaurante del Teleférico · Restaurante Carioca Tradicional de Calidad · Morro da Urca · Parque Bondinho Pan de Azúcar · Río de Janeiro · Brasil',
}

def add_eyebrow(filepath, lang):
    content = Path(filepath).read_text(encoding='utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    
    page_hero_content = soup.find('div', class_='page-hero-content')
    if not page_hero_content:
        print(f"  ⚠️  Sem page-hero-content em {filepath}")
        return False
    
    # Verificar se já existe o eyebrow
    existing = page_hero_content.find('div', class_='eyebrow')
    if existing and 'hero-eyebrow' in existing.get('class', []):
        print(f"  ⏭️  Eyebrow já existe em {filepath}")
        return False
    
    # Criar o novo eyebrow
    eyebrow_html = f'<div class="eyebrow hero-eyebrow">{EYEBROW[lang]}</div>'
    
    # Inserir como primeiro filho do page-hero-content (antes do crumbs/h1)
    # Usar substituição de string para preservar formatação
    insert_marker = '<div class="page-hero-content">'
    new_content = content.replace(
        insert_marker,
        insert_marker + '\n' + eyebrow_html,
        1  # apenas primeira ocorrência
    )
    
    if new_content != content:
        Path(filepath).write_text(new_content, encoding='utf-8')
        print(f"  ✅ Eyebrow adicionado em {filepath}")
        return True
    else:
        print(f"  ⚠️  Não foi possível inserir em {filepath}")
        return False

# Processar PT
print("=== PT ===")
for page in PT_PAGES:
    add_eyebrow(page, 'pt')

# Processar EN
print("\n=== EN ===")
for page in PT_PAGES:
    en_path = f'en/{page}'
    if Path(en_path).exists():
        add_eyebrow(en_path, 'en')
    else:
        print(f"  ⚠️  Não encontrado: {en_path}")

# Processar ES
print("\n=== ES ===")
for page in PT_PAGES:
    es_path = f'es/{page}'
    if Path(es_path).exists():
        add_eyebrow(es_path, 'es')
    else:
        print(f"  ⚠️  Não encontrado: {es_path}")

print("\n✅ Concluído!")
