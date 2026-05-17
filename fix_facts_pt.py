#!/usr/bin/env python3
"""
fix_facts_pt.py
Padroniza fatos oficiais e corrige textos quebrados em todos os arquivos HTML em Português.
"""
import os, re
from pathlib import Path

BASE = '/home/ubuntu/embaixada-deploy'

# Fatos oficiais
FACTS = {
    'avaliacoes': '7.779',
    'instagram': '100 mil',
    'horario_geral': '8h30 às 21h',
    'horario_cafe': '8h30 às 11h30',
    'horario_almoco': '11h30 às 17h',
    'premio_feijoada': 'Melhor Feijoada do Rio (Veja Rio 2025/2026)',
}

# Substituições regex
REPLACEMENTS = [
    # Avaliações
    (r'7[.,][0-9]{3}', '7.779'),
    
    # Instagram
    (r'84 mil|84[Kk]|100[Kk]', '100 mil'),
    
    # Horários de Almoço
    (r'12h às 17h|12h – 16h30|12h – 17h|12h – 15h30|12:00 às 17:00|12h às 15h30', '11h30 às 17h'),
    (r'12h – 16h30 \(seg–sex\) / 17h \(sáb–dom\)', '11h30 às 17h (todos os dias)'),
    
    # Horários de Café da Manhã
    (r'8h – 11h|8:00 às 11:00|8h às 11h', '8h30 às 11h30'),
    
    # Prêmios da Feijoada
    (r'[Mm]elhor [Ff]eijoada do Brasil pela Revista Prazeres da Mesa', 'Melhor Feijoada do Rio pela Veja Rio 2025/2026'),
    (r'[Mm]elhor [Ff]eijoada do Brasil', 'Melhor Feijoada do Rio'),
    (r'Prazeres da Mesa', 'Veja Rio 2025/2026'),
    
    # Textos Quebrados e Copydesk
    (r'[Bb]ondinho o monte', 'Bondinho do Pão de Açúcar'),
    (r'dentro do Parque Bondinho o Morro da Urca', 'dentro do Parque Bondinho, no Morro da Urca'),
    (r'vista direta para o a montanha', 'vista direta para a montanha'),
    (r'a Embaixada Carioca restaurante com vista', 'a Embaixada Carioca, restaurante com vista'),
    
    # Ingresso do bondinho (correção operacional)
    (r'não requer ingresso do bondinho para entrar', 'o acesso requer ingresso do Parque Bondinho ou via Trilha do Morro da Urca'),
]

# Coletar todos os HTMLs em PT (raiz)
html_files = sorted(Path(BASE).glob('*.html'))
html_files = [f for f in html_files if '.bak' not in str(f) and '__pycache__' not in str(f)]

total_files = 0
total_replacements = 0

for fpath in html_files:
    try:
        content = fpath.read_text(encoding='utf-8')
    except:
        continue
    
    original_content = content
    
    for pattern, replacement in REPLACEMENTS:
        content, count = re.subn(pattern, replacement, content)
        total_replacements += count
        
    if content != original_content:
        fpath.write_text(content, encoding='utf-8')
        total_files += 1
        print(f"✅ {fpath.name} atualizado")

print(f"\nTotal de arquivos PT atualizados: {total_files}")
print(f"Total de substituições feitas: {total_replacements}")
