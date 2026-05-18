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

# 1. Correções do FAQ na home EN
en_faq_replacements = {
    'As perguntas mais comuns de quem busca <strong>onde comer no Rio de Janeiro</strong>': 'The most common questions from those looking for <strong>where to eat in Rio de Janeiro</strong>',
    'com vista para o Pão de Açúcar.': 'with a view of Sugarloaf Mountain.',
    'Tem restaurante no Bondinho do Pão de Açúcar?': 'Is there a restaurant at the Sugarloaf Cable Car?',
    'Sim! A Embaixada Carioca é o <strong>restaurante oficial do Bondinho Pão de Açúcar</strong>, localizado no <strong>Morro da Urca</strong> — a 1ª parada do teleférico, a 227 metros de altitude. Panoramic view de frente para o Pão de Açúcar, Baía de Guanabara e Cristo Redentor. Breakfast, lunch and sunset every day.': 'Yes! Embaixada Carioca is the <strong>official restaurant of the Sugarloaf Cable Car</strong>, located on <strong>Urca Hill</strong> — the 1st cable car stop, at 227 meters altitude. Frontal panoramic view of Sugarloaf Mountain, Guanabara Bay, and Christ the Redeemer. Breakfast, lunch, and sunset every day.',
    'Qual o melhor lugar para comer no Rio de Janeiro com vista?': 'What is the best place to eat in Rio de Janeiro with a view?',
    'Entre os <strong>restaurantes com vista no Rio de Janeiro</strong>, a Embaixada Carioca é o único dentro do Parque Bondinho, com vista panorâmica mais bonita do mundo para o Pão de Açúcar, Baía de Guanabara e Cristo Redentor — avaliação 4,8 ★ no Google. Open daily para café da manhã, almoço e entardecer.': 'Among the <strong>restaurants with a view in Rio de Janeiro</strong>, Embaixada Carioca is the main one inside the Cable Car Park, with a frontal panoramic view of Sugarloaf Mountain, Guanabara Bay, and Christ the Redeemer — rated 4.8 ★ on Google. Open daily for breakfast, lunch, and sunset.',
    'O <strong>breakfast at Morro da Urca</strong> is served <strong>every day</strong>, from 8:30am to 11:30am, with a panoramic view of Sugarloaf Mountain. It is one of the most unique <strong>breakfast with a view experiences in Rio de Janeiro</strong> — with no direct competitor in the city.': '<strong>Breakfast at Urca Hill</strong> is served <strong>every day</strong>, from 8:30am to 11:30am, with a panoramic view of Sugarloaf Mountain. It is one of the most unique <strong>breakfast with a view experiences in Rio de Janeiro</strong> — with no direct competitor in the city.',
    'Tem restaurante no Morro da Urca?': 'Is there a restaurant on Urca Hill?',
    'Tem restaurante no Parque Bondinho Pão de Açúcar?': 'Is there a restaurant at the Sugarloaf Cable Car Park?',
    'Panoramic view': 'Panoramic view', # Manter em EN, mas corrigir em ES
}

replace_in_file('en/index.html', en_faq_replacements)
replace_in_file('en/morro-da-urca.html', en_faq_replacements)
replace_in_file('en/parque-bondinho.html', en_faq_replacements)

# 2. Correções do FAQ na home ES
es_faq_replacements = {
    'As perguntas mais comuns de quem busca <strong>onde comer no Rio de Janeiro</strong>': 'Las preguntas más comunes de quienes buscan <strong>dónde comer en Río de Janeiro</strong>',
    'com vista para o Pão de Açúcar.': 'con vista al Pan de Azúcar.',
    'Tem restaurante no Bondinho do Pão de Açúcar?': '¿Hay restaurante en el Teleférico del Pan de Azúcar?',
    'Sim! A Embaixada Carioca é o <strong>restaurante oficial do Bondinho Pão de Açúcar</strong>, localizado no <strong>Morro da Urca</strong> — a 1ª parada do teleférico, a 227 metros de altitude. Panoramic view de frente para o Pão de Açúcar, Baía de Guanabara e Cristo Redentor. Desayuno, almuerzo y atardecer todos los días.': '¡Sí! Embaixada Carioca es el <strong>restaurante oficial del Teleférico del Pan de Azúcar</strong>, ubicado en el <strong>Morro da Urca</strong> — la 1ª parada del teleférico, a 227 metros de altitud. Vista panorámica frontal al Pan de Azúcar, Bahía de Guanabara y Cristo Redentor. Desayuno, almuerzo y atardecer todos los días.',
    'Qual o melhor lugar para comer no Rio de Janeiro com vista?': '¿Cuál es el mejor lugar para comer en Río de Janeiro con vista?',
    'Entre os <strong>restaurantes com vista no Rio de Janeiro</strong>, a Embaixada Carioca é o único dentro do Parque Bondinho, com vista panorâmica mais bonita do mundo para o Pão de Açúcar, Baía de Guanabara e Cristo Redentor — avaliação 4,8 ★ no Google. Abierto todos los días para café da manhã, almoço e entardecer.': 'Entre los <strong>restaurantes con vista en Río de Janeiro</strong>, Embaixada Carioca es el principal dentro del Parque del Teleférico, con vista panorámica frontal al Pan de Azúcar, Bahía de Guanabara y Cristo Redentor — calificación 4,8 ★ en Google. Abierto todos los días para desayuno, almuerzo y atardecer.',
    'O <strong>desayuno en el Morro da Urca</strong> se sirve <strong>todos los días</strong>, de 8:30 a 11:30, con vista panorámica al Pan de Azúcar. Es unaas experiências de <strong>café da manhã com vista no Rio de Janeiro</strong> más únicas — sin competidor directo en la ciudad.': 'El <strong>desayuno en el Morro da Urca</strong> se sirve <strong>todos los días</strong>, de 8:30 a 11:30, con vista panorámica al Pan de Azúcar. Es una de las experiencias de <strong>desayuno con vista en Río de Janeiro</strong> más únicas — sin competidor directo en la ciudad.',
    'Tem restaurante no Morro da Urca?': '¿Hay restaurante en el Morro da Urca?',
    'Tem restaurante no Parque Bondinho Pão de Açúcar?': '¿Hay restaurante en el Parque del Teleférico del Pan de Azúcar?',
    'Panoramic view': 'Vista panorámica',
}

replace_in_file('es/index.html', es_faq_replacements)
replace_in_file('es/morro-da-urca.html', es_faq_replacements)
replace_in_file('es/parque-bondinho.html', es_faq_replacements)

