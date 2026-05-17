#!/usr/bin/env python3
"""
audit_facts.py
Mapeia todas as inconsistências de fatos e textos quebrados em todos os arquivos HTML.
"""
import os, re
from bs4 import BeautifulSoup
from pathlib import Path

BASE = '/home/ubuntu/embaixada-deploy'

# Fatos a verificar
FACT_PATTERNS = {
    'avaliacoes_7779': r'7[.,]779',
    'avaliacoes_7752': r'7[.,]752',
    'avaliacoes_outros': r'7[.,][0-9]{3}',
    'instagram_100k': r'100[Kk]|100 mil',
    'instagram_84k': r'84 mil|84[Kk]',
    'horario_almoco_1530': r'15h30|15:30',
    'horario_almoco_17h': r'17h|17:00',
    'horario_almoco_1130': r'11h30|11:30',
    'horario_cafe_830': r'8h30|8:30',
    'horario_cafe_8h': r'\b8h\b',
    'horario_cafe_11h': r'\b11h\b',
    'horario_cafe_1130': r'11h30',
    'premio_melhor_rio': r'[Mm]elhor [Ff]eijoada do Rio',
    'premio_melhor_brasil': r'[Mm]elhor [Ff]eijoada do Brasil',
    'premio_veja_rio': r'Veja Rio',
    'premio_prazeres': r'Prazeres da Mesa',
    'texto_quebrado_monte': r'[Bb]ondinho o monte',
    'texto_quebrado_morro': r'dentro do Parque Bondinho o Morro',
    'texto_quebrado_vista': r'vista direta para o a montanha',
    'texto_vista_panoramica_en': r'Vista panor[aâ]mica',
}

# Coletar todos os HTMLs
html_files = sorted(Path(BASE).rglob('*.html'))
# Excluir arquivos de backup
html_files = [f for f in html_files if '.bak' not in str(f) and '__pycache__' not in str(f)]

print(f"Total de arquivos HTML: {len(html_files)}\n")

results = {}
for fpath in html_files:
    rel = str(fpath).replace(BASE+'/', '')
    try:
        content = fpath.read_text(encoding='utf-8')
    except:
        continue
    
    found = {}
    for key, pattern in FACT_PATTERNS.items():
        matches = re.findall(pattern, content)
        if matches:
            found[key] = list(set(matches))
    
    if found:
        results[rel] = found

# Imprimir resultados agrupados por tipo de problema
print("=" * 70)
print("INCONSISTÊNCIAS DE FATOS E TEXTOS QUEBRADOS")
print("=" * 70)

# Agrupar por tipo
by_type = {}
for filepath, facts in results.items():
    for key, vals in facts.items():
        if key not in by_type:
            by_type[key] = []
        by_type[key].append((filepath, vals))

for key in sorted(by_type.keys()):
    files = by_type[key]
    print(f"\n[{key}] — {len(files)} arquivo(s):")
    for filepath, vals in sorted(files):
        print(f"  • {filepath}: {vals}")

print("\n" + "=" * 70)
print(f"Total de tipos de inconsistências encontradas: {len(by_type)}")
