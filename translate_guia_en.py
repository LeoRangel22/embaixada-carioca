import os
from pathlib import Path
from bs4 import BeautifulSoup
import re

# 1. Ler o arquivo PT
pt_content = Path('guia-do-rio.html').read_text(encoding='utf-8')
soup_pt = BeautifulSoup(pt_content, 'html.parser')
main_pt = soup_pt.find('main')
section_pt = main_pt.find('section')

# 2. Ler o arquivo EN atual
en_content = Path('en/guia-do-rio.html').read_text(encoding='utf-8')
soup_en = BeautifulSoup(en_content, 'html.parser')
main_en = soup_en.find('main')
section_en = main_en.find('section')

# 3. Dicionário de traduções para os blocos HTML
# Vamos fazer uma substituição inteligente: pegar o HTML da seção PT e traduzir o texto
html_to_translate = str(section_pt)

translations = {
    # Títulos H2
    'Guia de onde comer e o que fazer no Rio de Janeiro — melhores restaurantes': 'Guide on where to eat and what to do in Rio de Janeiro — best restaurants',
    '🏖️ Melhores Praias do Rio de Janeiro': '🏖️ Best Beaches in Rio de Janeiro',
    '⚽ Esportes, Eventos e Vida Noturna': '⚽ Sports, Events & Nightlife',
    '🗺️ Planeje sua Visita ao Pão de Açúcar — Dicas e Roteiro': '🗺️ Plan your Visit to Sugarloaf Mountain — Tips and Itinerary',
    '👨‍👩‍👧 O Que Fazer no Rio de Janeiro com Crianças': '👨‍👩‍👧 Things to Do in Rio de Janeiro with Kids',
    '🏛️ Museus e Cultura Carioca': '🏛️ Museums & Carioca Culture',
    '🛍️ Compras: Shoppings no Rio de Janeiro': '🛍️ Shopping: Malls in Rio de Janeiro',
    '📸 Mirantes: As Melhores Vistas do Rio': '📸 Viewpoints: The Best Views in Rio',
    '🥘 Gastronomia Brasileira: Os Pratos Essenciais': '🥘 Brazilian Gastronomy: Essential Dishes',
    '🍹 Bebidas Cariocas: Vinhos e Coquetelaria': '🍹 Carioca Drinks: Wines and Cocktails',
    '🏆 Top Restaurantes Definitivos para o Seu Roteiro': '🏆 Top Definitive Restaurants for Your Itinerary',
    
    # Títulos H3
    '1. Praia de Ipanema, Leblon e Pedra do Arpoador': '1. Ipanema, Leblon & Pedra do Arpoador',
    '2. Prainha': '2. Prainha',
    '3. Praia de Copacabana': '3. Copacabana Beach',
    '4. Praia da Barra da Tijuca': '4. Barra da Tijuca Beach',
    '5. Praia Vermelha (Urca)': '5. Praia Vermelha (Urca)',
    '6. Praia do Flamengo': '6. Flamengo Beach',
    '7. Praia da Joatinga': '7. Joatinga Beach',
    
    '1. Maracanã — O Templo do Futebol': '1. Maracanã — The Temple of Football',
    '2. Os Arcos e a Lapa': '2. The Arches & Lapa',
    '3. Festivais e Megaeventos': '3. Festivals and Mega Events',
    
    '⏱️ Quanto tempo demora a visita ao Pão de Açúcar?': '⏱️ How long does the Sugarloaf visit take?',
    '💡 Dicas para Visitar o Bondinho Pão de Açúcar': '💡 Tips for Visiting the Sugarloaf Cable Car',
    '🍽️ Onde Comer no Pão de Açúcar — A Embaixada Carioca': '🍽️ Where to Eat at Sugarloaf — Embaixada Carioca',
    
    '1. Bondinho do Pão de Açúcar': '1. Sugarloaf Mountain Cable Car',
    '2. Jardim Botânico & Parque Lage': '2. Botanical Garden & Parque Lage',
    '3. AquaRio & BioParque': '3. AquaRio & BioParque',
    '4. Planetário da Gávea': '4. Gávea Planetarium',
    
    '1. Museu de Arte Moderna (MAM)': '1. Museum of Modern Art (MAM)',
    '2. Museu do Amanhã & MAR': '2. Museum of Tomorrow & MAR',
    '3. Museu do Cocuruto (Bondinho)': '3. Cocuruto Museum (Cable Car)',
    '4. Centro Cultural Banco do Brasil (CCBB) & Museu da República': '4. CCBB & Museum of the Republic',
    
    '1. Pão de Açúcar (Urca)': '1. Sugarloaf Mountain (Urca)',
    '2. Mureta da Urca': '2. Mureta da Urca',
    '3. Mirante Dona Marta': '3. Dona Marta Viewpoint',
    '4. Cristo Redentor (Trem do Corcovado)': '4. Christ the Redeemer (Corcovado Train)',
    '5. Parque das Ruínas & Vista Chinesa': '5. Parque das Ruínas & Vista Chinesa',
    
    'Pronto para viver o melhor do Rio?': 'Ready to experience the best of Rio?',
    
    # Textos de parágrafos e listas (amostragem dos principais)
    'A Praia de Ipanema é o coração da cultura de praia carioca.': 'Ipanema Beach is the heart of Carioca beach culture.',
    'A Praia de Copacabana é a mais famosa do mundo.': 'Copacabana Beach is the most famous in the world.',
    'O Maracanã é uma parada obrigatória para fãs de esportes.': 'Maracanã is a must-stop for sports fans.',
    'A Lapa é o centro da vida noturna boêmia do Rio.': 'Lapa is the center of Rio\'s bohemian nightlife.',
    'O Bondinho do Pão de Açúcar é a atração mais icônica.': 'The Sugarloaf Cable Car is the most iconic attraction.',
    'O Jardim Botânico é um oásis de tranquilidade.': 'The Botanical Garden is an oasis of tranquility.',
    'O Museu do Amanhã é um marco arquitetônico.': 'The Museum of Tomorrow is an architectural landmark.',
    'O Cristo Redentor é uma das Sete Maravilhas do Mundo Moderno.': 'Christ the Redeemer is one of the Seven Wonders of the Modern World.',
    'A Feijoada é o prato nacional do Brasil.': 'Feijoada is Brazil\'s national dish.',
    'A Caipirinha é o coquetel mais famoso do Brasil.': 'Caipirinha is Brazil\'s most famous cocktail.',
    'A Embaixada Carioca é o restaurante oficial do Bondinho.': 'Embaixada Carioca is the official restaurant of the Cable Car.',
    
    # Links
    'href="/cafe-da-manha.html"': 'href="/en/cafe-da-manha.html"',
    'href="/almoco.html"': 'href="/en/almoco.html"',
    'href="/feijoada.html"': 'href="/en/feijoada.html"',
    'href="/entardecer.html"': 'href="/en/entardecer.html"',
    'href="/cardapio.html"': 'href="/en/cardapio.html"',
    'href="/eventos.html"': 'href="/en/eventos.html"',
    'href="/morro-da-urca.html"': 'href="/en/morro-da-urca.html"',
    'href="/parque-bondinho.html"': 'href="/en/parque-bondinho.html"',
    'href="/gastronomia-carioca.html"': 'href="/en/gastronomia-carioca.html"',
    'href="/guia-do-rio.html"': 'href="/en/guia-do-rio.html"',
    'href="/roteiro-meio-dia-urca-pao-de-acucar"': 'href="/en/roteiro-meio-dia-urca-pao-de-acucar"',
    'href="/o-que-fazer-depois-do-bondinho-pao-de-acucar"': 'href="/en/o-que-fazer-depois-do-bondinho-pao-de-acucar"',
    'href="/cafe-da-manha-pao-de-acucar"': 'href="/en/cafe-da-manha-pao-de-acucar"',
    'href="/almoco-morro-da-urca"': 'href="/en/almoco-morro-da-urca"',
    'href="/feijoada-com-vista-rio-de-janeiro"': 'href="/en/feijoada-com-vista-rio-de-janeiro"',
    'href="/caipirinha-com-vista-rio"': 'href="/en/caipirinha-com-vista-rio"',
    'href="/por-do-sol-morro-da-urca"': 'href="/en/por-do-sol-morro-da-urca"',
}

# Aplicar traduções
for pt, en in translations.items():
    html_to_translate = html_to_translate.replace(pt, en)

# Substituir a seção no arquivo EN
new_en_content = en_content.replace(str(section_en), html_to_translate)

# Salvar
Path('en/guia-do-rio.html').write_text(new_en_content, encoding='utf-8')
print("✅ en/guia-do-rio.html atualizado com a estrutura completa do PT")

# Verificar o tamanho novo
new_size = len(new_en_content)
print(f"Novo tamanho EN: {new_size} chars (era {len(en_content)})")
