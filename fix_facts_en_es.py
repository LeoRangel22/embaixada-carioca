#!/usr/bin/env python3
"""
fix_facts_en_es.py
Padroniza fatos oficiais e corrige textos quebrados em todos os arquivos HTML em Inglês e Espanhol.
"""
import os, re
from pathlib import Path

BASE = '/home/ubuntu/embaixada-deploy'

# Substituições regex para EN e ES
REPLACEMENTS = [
    # Avaliações
    (r'7[.,][0-9]{3}', '7.779'),
    
    # Instagram
    (r'84 mil|84[Kk]|100[Kk]', '100K'),
    
    # Horários de Almoço EN
    (r'12pm – 4:30pm|12pm – 5pm|12:00pm to 5:00pm|12:00pm to 4:30pm', '11:30am to 5:00pm'),
    (r'12pm – 4:30pm \(Mon–Fri\) / 5pm \(Sat–Sun\)', '11:30am to 5:00pm (every day)'),
    
    # Horários de Almoço ES
    (r'12h – 16h30|12h – 17h|12h – 15h30|12:00 a 17:00|12:00 a 16:30', '11:30 a 17:00'),
    (r'12h – 16h30 \(lun–vie\) / 17h \(sáb–dom\)', '11:30 a 17:00 (todos los días)'),
    
    # Horários de Café da Manhã EN
    (r'8am – 11am|8:00am to 11:00am', '8:30am to 11:30am'),
    
    # Horários de Café da Manhã ES
    (r'8h – 11h|8:00 a 11:00', '8:30 a 11:30'),
    
    # Prêmios da Feijoada EN
    (r'[Bb]est [Ff]eijoada in Brazil by Prazeres da Mesa', 'Best Feijoada in Rio by Veja Rio 2025/2026'),
    (r'[Bb]est [Ff]eijoada in Brazil', 'Best Feijoada in Rio'),
    (r'Prazeres da Mesa', 'Veja Rio 2025/2026'),
    
    # Prêmios da Feijoada ES
    (r'[Mm]ejor [Ff]eijoada de Brasil por Prazeres da Mesa', 'Mejor Feijoada de Río por Veja Rio 2025/2026'),
    (r'[Mm]ejor [Ff]eijoada de Brasil', 'Mejor Feijoada de Río'),
    
    # Textos Quebrados e Copydesk EN
    (r'Vista panor[aâ]mica', 'Panoramic view'),
    (r'does not require a cable car ticket to enter', 'access requires a Parque Bondinho ticket or via the Urca Hill Trail'),
    
    # Textos Quebrados e Copydesk ES
    (r'Vista panor[aâ]mica', 'Vista panorámica'),
    (r'no requiere boleto de teleférico para entrar', 'el acceso requiere boleto del Parque Bondinho o vía el Sendero del Morro da Urca'),
]

# Coletar todos os HTMLs em EN e ES
html_files = []
for lang in ['en', 'es']:
    files = sorted(Path(BASE).glob(f'{lang}/*.html'))
    html_files.extend([f for f in files if '.bak' not in str(f) and '__pycache__' not in str(f)])

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

print(f"\nTotal de arquivos EN/ES atualizados: {total_files}")
print(f"Total de substituições feitas: {total_replacements}")
