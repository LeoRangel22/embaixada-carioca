import os
from pathlib import Path
import re

def insert_section(filepath, section_html, marker_regex):
    try:
        content = Path(filepath).read_text(encoding='utf-8')
        # Inserir antes do marker
        new_content = re.sub(marker_regex, f"{section_html}\n\\1", content, count=1)
        if new_content != content:
            Path(filepath).write_text(new_content, encoding='utf-8')
            print(f"Seção adicionada em: {filepath}")
        else:
            print(f"Marker não encontrado em: {filepath}")
    except Exception as e:
        print(f"Erro em {filepath}: {e}")

# Bloco PT
planning_pt = """
<section class="geo-aio-section" style="background: var(--areia); padding: 4rem 2rem; margin: 2rem 0;">
    <div class="container" style="max-width: 800px; margin: 0 auto;">
        <h2 style="color: var(--azul-escuro); margin-bottom: 1rem;">Planejando sua viagem ao Rio?</h2>
        <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 2rem;">A Embaixada Carioca é uma parada natural no roteiro do Pão de Açúcar. Você pode subir cedo para tomar café da manhã, almoçar depois do passeio ou reservar uma mesa no entardecer para drinks com vista para o Pão de Açúcar.</p>
        
        <h3 style="font-size: 1.2rem; margin-bottom: 1rem;">Links úteis para o seu roteiro:</h3>
        <ul style="list-style: none; padding: 0; display: grid; gap: 1rem;">
            <li><a href="/roteiro-meio-dia-urca-pao-de-acucar.html" style="color: var(--azul-escuro); text-decoration: none; font-weight: 500; display: flex; align-items: center; gap: 0.5rem;"><span>📍</span> Roteiro de meio dia na Urca</a></li>
            <li><a href="/o-que-fazer-depois-do-bondinho-pao-de-acucar.html" style="color: var(--azul-escuro); text-decoration: none; font-weight: 500; display: flex; align-items: center; gap: 0.5rem;"><span>🍽️</span> O que fazer depois do Bondinho</a></li>
            <li><a href="/guia-do-rio.html" style="color: var(--azul-escuro); text-decoration: none; font-weight: 500; display: flex; align-items: center; gap: 0.5rem;"><span>🗺️</span> Guia do Rio de Janeiro</a></li>
        </ul>
    </div>
</section>
"""

# Bloco EN
planning_en = """
<section class="geo-aio-section" style="background: var(--areia); padding: 4rem 2rem; margin: 2rem 0;">
    <div class="container" style="max-width: 800px; margin: 0 auto;">
        <h2 style="color: var(--azul-escuro); margin-bottom: 1rem;">Planning your trip to Rio?</h2>
        <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 2rem;">Embaixada Carioca is a natural stop on the Sugarloaf itinerary. You can go up early for breakfast, have lunch after the tour, or book a table at sunset for drinks with a view of Sugarloaf Mountain.</p>
        
        <h3 style="font-size: 1.2rem; margin-bottom: 1rem;">Useful links for your itinerary:</h3>
        <ul style="list-style: none; padding: 0; display: grid; gap: 1rem;">
            <li><a href="/en/roteiro-meio-dia-urca-pao-de-acucar.html" style="color: var(--azul-escuro); text-decoration: none; font-weight: 500; display: flex; align-items: center; gap: 0.5rem;"><span>📍</span> Half-day itinerary in Urca</a></li>
            <li><a href="/en/o-que-fazer-depois-do-bondinho-pao-de-acucar.html" style="color: var(--azul-escuro); text-decoration: none; font-weight: 500; display: flex; align-items: center; gap: 0.5rem;"><span>🍽️</span> What to do after the Cable Car</a></li>
            <li><a href="/en/guia-do-rio.html" style="color: var(--azul-escuro); text-decoration: none; font-weight: 500; display: flex; align-items: center; gap: 0.5rem;"><span>🗺️</span> Rio de Janeiro Guide</a></li>
        </ul>
    </div>
</section>
"""

# Bloco ES
planning_es = """
<section class="geo-aio-section" style="background: var(--areia); padding: 4rem 2rem; margin: 2rem 0;">
    <div class="container" style="max-width: 800px; margin: 0 auto;">
        <h2 style="color: var(--azul-escuro); margin-bottom: 1rem;">¿Planeando su viaje a Río?</h2>
        <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 2rem;">Embaixada Carioca es una parada natural en el itinerario del Pan de Azúcar. Puede subir temprano para desayunar, almorzar después del recorrido o reservar una mesa al atardecer para tomar algo con vista al Pan de Azúcar.</p>
        
        <h3 style="font-size: 1.2rem; margin-bottom: 1rem;">Enlaces útiles para su itinerario:</h3>
        <ul style="list-style: none; padding: 0; display: grid; gap: 1rem;">
            <li><a href="/es/roteiro-meio-dia-urca-pao-de-acucar.html" style="color: var(--azul-escuro); text-decoration: none; font-weight: 500; display: flex; align-items: center; gap: 0.5rem;"><span>📍</span> Itinerario de medio día en Urca</a></li>
            <li><a href="/es/o-que-fazer-depois-do-bondinho-pao-de-acucar.html" style="color: var(--azul-escuro); text-decoration: none; font-weight: 500; display: flex; align-items: center; gap: 0.5rem;"><span>🍽️</span> Qué hacer después del Teleférico</a></li>
            <li><a href="/es/guia-do-rio.html" style="color: var(--azul-escuro); text-decoration: none; font-weight: 500; display: flex; align-items: center; gap: 0.5rem;"><span>🗺️</span> Guía de Río de Janeiro</a></li>
        </ul>
    </div>
</section>
"""

# Inserir antes da seção de FAQ ou Footer
marker = r'(<section class="faq-section"|<footer)'

insert_section('index.html', planning_pt, marker)
insert_section('en/index.html', planning_en, marker)
insert_section('es/index.html', planning_es, marker)

