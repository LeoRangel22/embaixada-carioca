import os
from pathlib import Path
import re

def replace_in_file(filepath, replacements):
    try:
        content = Path(filepath).read_text(encoding='utf-8')
        original = content
        for old, new in replacements.items():
            content = content.replace(old, new)
        if content != original:
            Path(filepath).write_text(content, encoding='utf-8')
            print(f"Atualizado: {filepath}")
    except Exception as e:
        print(f"Erro em {filepath}: {e}")

# Correções de textos quebrados em PT
pt_replacements = {
    'do o monte': 'do Pão de Açúcar',
    'para o o monte': 'para o Pão de Açúcar',
    'de o monte': 'do Pão de Açúcar',
    'o o monte': 'o Pão de Açúcar',
    'para o a montanha': 'para a montanha',
    'para a a montanha': 'para a montanha',
    'de o a montanha': 'da montanha',
    'O a montanha icônica': 'A montanha icônica',
    'o restaurante espaço para eventos': 'o espaço para eventos',
    'do Morro da Urca e do o monte': 'do Morro da Urca e do Pão de Açúcar',
    'Vista panorâmica</span> <span class="fato-label-hero">Mais bonita do mundo': 'Vista panorâmica</span> <span class="fato-label-hero">Frontal para o Pão de Açúcar',
    'vista panorâmica mais bonita do mundo': 'vista panorâmica frontal para o Pão de Açúcar',
    'a vista panorâmica mais bonita do mundo': 'a vista panorâmica frontal para o Pão de Açúcar',
    'Panoramic view': 'Vista panorâmica',
    'Panoramic': 'Panorâmica'
}

# Aplicar em todos os arquivos PT
for f in Path('.').glob('*.html'):
    if f.name not in ['404.html', 'offline.html', 'Home v1.html', 'Home v2.html']:
        replace_in_file(f, pt_replacements)

