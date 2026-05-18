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

# 1. Correções de blocos em EN
en_blocks = {
    'Roteiros & grupos': 'Itineraries & Groups',
    'Venha nos visitar': 'Come visit us',
    'Endereço & Acesso': 'Address & Access',
    'Acesso via bondinho': 'Access via cable car',
    'Saiba mais': 'Learn more',
    'Fazer reserva': 'Make a reservation',
    'Fale conosco': 'Contact us',
    'Reservar mesa': 'Book a table',
    'Vista panorâmica': 'Panoramic view',
    'do Pão de Açúcar a partir da Embaixada Carioca no Morro da Urca': 'of Sugarloaf Mountain from Embaixada Carioca on Urca Hill',
    'do Pão de Açúcar': 'of Sugarloaf Mountain',
    'para o Pão de Açúcar': 'to Sugarloaf Mountain',
    'da montanha': 'of the mountain',
    'a montanha': 'the mountain',
    'o Pão de Açúcar': 'Sugarloaf Mountain',
    'Morro da Urca': 'Urca Hill',
    'Parque Bondinho': 'Cable Car Park',
    'Bondinho do Pão de Açúcar': 'Sugarloaf Cable Car',
}

for f in Path('en').glob('*.html'):
    replace_in_file(f, en_blocks)

# 2. Correções de blocos em ES
es_blocks = {
    'Roteiros & grupos': 'Itinerarios y Grupos',
    'Venha nos visitar': 'Ven a visitarnos',
    'Endereço & Acesso': 'Dirección y Acceso',
    'Acesso via bondinho': 'Acceso vía teleférico',
    'Saiba mais': 'Saber más',
    'Fazer reserva': 'Hacer reserva',
    'Fale conosco': 'Contáctenos',
    'Reservar mesa': 'Reservar mesa',
    'Vista panorâmica': 'Vista panorámica',
    'Panoramic view': 'Vista panorámica',
    'do Pão de Açúcar a partir da Embaixada Carioca no Morro da Urca': 'del Pan de Azúcar desde Embaixada Carioca en el Morro da Urca',
    'do Pão de Açúcar': 'del Pan de Azúcar',
    'para o Pão de Açúcar': 'al Pan de Azúcar',
    'da montanha': 'de la montaña',
    'a montanha': 'la montaña',
    'o Pão de Açúcar': 'el Pan de Azúcar',
    'Morro da Urca': 'Morro da Urca',
    'Parque Bondinho': 'Parque del Teleférico',
    'Bondinho do Pão de Açúcar': 'Teleférico del Pan de Azúcar',
}

for f in Path('es').glob('*.html'):
    replace_in_file(f, es_blocks)

