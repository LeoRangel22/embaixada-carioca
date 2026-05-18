import os
from pathlib import Path
from bs4 import BeautifulSoup
import re

# 1. Ler o arquivo PT
pt_content = Path('guia-do-rio.html').read_text(encoding='utf-8')
soup_pt = BeautifulSoup(pt_content, 'html.parser')
main_pt = soup_pt.find('main')
section_pt = main_pt.find('section')

# 2. Ler o arquivo ES atual
es_content = Path('es/guia-do-rio.html').read_text(encoding='utf-8')
soup_es = BeautifulSoup(es_content, 'html.parser')
main_es = soup_es.find('main')
section_es = main_es.find('section')

# 3. Dicionário de traduções para os blocos HTML
html_to_translate = str(section_pt)

translations = {
    # Títulos H2
    'Guia de onde comer e o que fazer no Rio de Janeiro — melhores restaurantes': 'Guía de dónde comer y qué hacer en Río de Janeiro — mejores restaurantes',
    '🏖️ Melhores Praias do Rio de Janeiro': '🏖️ Las Mejores Playas de Río de Janeiro',
    '⚽ Esportes, Eventos e Vida Noturna': '⚽ Deportes, Eventos y Vida Nocturna',
    '🗺️ Planeje sua Visita ao Pão de Açúcar — Dicas e Roteiro': '🗺️ Planea tu Visita al Pan de Azúcar — Consejos e Itinerario',
    '👨‍👩‍👧 O Que Fazer no Rio de Janeiro com Crianças': '👨‍👩‍👧 Qué Hacer en Río de Janeiro con Niños',
    '🏛️ Museus e Cultura Carioca': '🏛️ Museos y Cultura Carioca',
    '🛍️ Compras: Shoppings no Rio de Janeiro': '🛍️ Compras: Centros Comerciales en Río de Janeiro',
    '📸 Mirantes: As Melhores Vistas do Rio': '📸 Miradores: Las Mejores Vistas de Río',
    '🥘 Gastronomia Brasileira: Os Pratos Essenciais': '🥘 Gastronomía Brasileña: Los Platos Esenciales',
    '🍹 Bebidas Cariocas: Vinhos e Coquetelaria': '🍹 Bebidas Cariocas: Vinos y Cócteles',
    '🏆 Top Restaurantes Definitivos para o Seu Roteiro': '🏆 Top Restaurantes Definitivos para tu Itinerario',
    
    # Títulos H3
    '1. Praia de Ipanema, Leblon e Pedra do Arpoador': '1. Ipanema, Leblon y Pedra do Arpoador',
    '2. Prainha': '2. Prainha',
    '3. Praia de Copacabana': '3. Playa de Copacabana',
    '4. Praia da Barra da Tijuca': '4. Playa de Barra da Tijuca',
    '5. Praia Vermelha (Urca)': '5. Praia Vermelha (Urca)',
    '6. Praia do Flamengo': '6. Playa de Flamengo',
    '7. Praia da Joatinga': '7. Playa de Joatinga',
    
    '1. Maracanã — O Templo do Futebol': '1. Maracanã — El Templo del Fútbol',
    '2. Os Arcos e a Lapa': '2. Los Arcos y La Lapa',
    '3. Festivais e Megaeventos': '3. Festivales y Megaeventos',
    
    '⏱️ Quanto tempo demora a visita ao Pão de Açúcar?': '⏱️ ¿Cuánto tiempo dura la visita al Pan de Azúcar?',
    '💡 Dicas para Visitar o Bondinho Pão de Açúcar': '💡 Consejos para Visitar el Teleférico del Pan de Azúcar',
    '🍽️ Onde Comer no Pão de Açúcar — A Embaixada Carioca': '🍽️ Dónde Comer en el Pan de Azúcar — Embaixada Carioca',
    
    '1. Bondinho do Pão de Açúcar': '1. Teleférico del Pan de Azúcar',
    '2. Jardim Botânico & Parque Lage': '2. Jardín Botánico y Parque Lage',
    '3. AquaRio & BioParque': '3. AquaRio y BioParque',
    '4. Planetário da Gávea': '4. Planetario de Gávea',
    
    '1. Museu de Arte Moderna (MAM)': '1. Museo de Arte Moderno (MAM)',
    '2. Museu do Amanhã & MAR': '2. Museo del Mañana y MAR',
    '3. Museu do Cocuruto (Bondinho)': '3. Museo Cocuruto (Teleférico)',
    '4. Centro Cultural Banco do Brasil (CCBB) & Museu da República': '4. CCBB y Museo de la República',
    
    '1. Pão de Açúcar (Urca)': '1. Pan de Azúcar (Urca)',
    '2. Mureta da Urca': '2. Mureta da Urca',
    '3. Mirante Dona Marta': '3. Mirador Dona Marta',
    '4. Cristo Redentor (Trem do Corcovado)': '4. Cristo Redentor (Tren del Corcovado)',
    '5. Parque das Ruínas & Vista Chinesa': '5. Parque das Ruínas y Vista Chinesa',
    
    'Pronto para viver o melhor do Rio?': '¿Listo para vivir lo mejor de Río?',
    
    # Textos de parágrafos e listas (amostragem dos principais)
    'A Praia de Ipanema é o coração da cultura de praia carioca.': 'La Playa de Ipanema es el corazón de la cultura de playa carioca.',
    'A Praia de Copacabana é a mais famosa do mundo.': 'La Playa de Copacabana es la más famosa del mundo.',
    'O Maracanã é uma parada obrigatória para fãs de esportes.': 'El Maracanã es una parada obligatoria para los fanáticos de los deportes.',
    'A Lapa é o centro da vida noturna boêmia do Rio.': 'La Lapa es el centro de la vida nocturna bohemia de Río.',
    'O Bondinho do Pão de Açúcar é a atração mais icônica.': 'El Teleférico del Pan de Azúcar es la atracción más icónica.',
    'O Jardim Botânico é um oásis de tranquilidade.': 'El Jardín Botánico es un oasis de tranquilidad.',
    'O Museu do Amanhã é um marco arquitetônico.': 'El Museo del Mañana es un hito arquitectónico.',
    'O Cristo Redentor é uma das Sete Maravilhas do Mundo Moderno.': 'El Cristo Redentor es una de las Siete Maravillas del Mundo Moderno.',
    'A Feijoada é o prato nacional do Brasil.': 'La Feijoada es el plato nacional de Brasil.',
    'A Caipirinha é o coquetel mais famoso do Brasil.': 'La Caipirinha es el cóctel más famoso de Brasil.',
    'A Embaixada Carioca é o restaurante oficial do Bondinho.': 'Embaixada Carioca es el restaurante oficial del Teleférico.',
    
    # Links
    'href="/cafe-da-manha.html"': 'href="/es/cafe-da-manha.html"',
    'href="/almoco.html"': 'href="/es/almoco.html"',
    'href="/feijoada.html"': 'href="/es/feijoada.html"',
    'href="/entardecer.html"': 'href="/es/entardecer.html"',
    'href="/cardapio.html"': 'href="/es/cardapio.html"',
    'href="/eventos.html"': 'href="/es/eventos.html"',
    'href="/morro-da-urca.html"': 'href="/es/morro-da-urca.html"',
    'href="/parque-bondinho.html"': 'href="/es/parque-bondinho.html"',
    'href="/gastronomia-carioca.html"': 'href="/es/gastronomia-carioca.html"',
    'href="/guia-do-rio.html"': 'href="/es/guia-do-rio.html"',
    'href="/roteiro-meio-dia-urca-pao-de-acucar"': 'href="/es/roteiro-meio-dia-urca-pao-de-acucar"',
    'href="/o-que-fazer-depois-do-bondinho-pao-de-acucar"': 'href="/es/o-que-fazer-depois-do-bondinho-pao-de-acucar"',
    'href="/cafe-da-manha-pao-de-acucar"': 'href="/es/cafe-da-manha-pao-de-acucar"',
    'href="/almoco-morro-da-urca"': 'href="/es/almoco-morro-da-urca"',
    'href="/feijoada-com-vista-rio-de-janeiro"': 'href="/es/feijoada-com-vista-rio-de-janeiro"',
    'href="/caipirinha-com-vista-rio"': 'href="/es/caipirinha-com-vista-rio"',
    'href="/por-do-sol-morro-da-urca"': 'href="/es/por-do-sol-morro-da-urca"',
}

# Aplicar traduções
for pt, es in translations.items():
    html_to_translate = html_to_translate.replace(pt, es)

# Substituir a seção no arquivo ES
new_es_content = es_content.replace(str(section_es), html_to_translate)

# Salvar
Path('es/guia-do-rio.html').write_text(new_es_content, encoding='utf-8')
print("✅ es/guia-do-rio.html atualizado com a estrutura completa do PT")

# Verificar o tamanho novo
new_size = len(new_es_content)
print(f"Novo tamanho ES: {new_size} chars (era {len(es_content)})")
