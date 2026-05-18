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

# 1. Correções de textos PT em ES
es_replacements = {
    'Entardecer como roteiro premium': 'Atardecer como itinerario premium',
    'Pôr do sol com pacote fechado de drinks &amp; petiscos': 'Puesta de sol con paquete cerrado de bebidas &amp; snacks',
    'Experiência VIP exclusiva': 'Experiencia VIP exclusiva',
    'Acesso reservado, hostess bilíngue, traslados': 'Acceso reservado, anfitriona bilingüe, traslados',
    'Feijoada premiada para grupos': 'Feijoada premiada para grupos',
    'Almuerzo auténtico los fines de semana': 'Almuerzo auténtico los fines de semana',
    'Acesso via bondinho': 'Acceso vía teleférico',
    'Reservar mesa': 'Reservar mesa', # Mantendo, mas vamos ajustar o footer
    'Fale conosco': 'Contáctenos',
    'Nosso endereço': 'Nuestra dirección',
    'Como chegar': 'Cómo llegar',
    'Ver cardápio': 'Ver menú',
    'Saiba mais': 'Saber más'
}

for f in Path('es').glob('*.html'):
    replace_in_file(f, es_replacements)

# 2. Correções de textos PT em EN
en_replacements = {
    'Entardecer como roteiro premium': 'Sunset as premium itinerary',
    'Pôr do sol com pacote fechado de drinks &amp; petiscos': 'Sunset with closed package of drinks &amp; snacks',
    'Experiência VIP exclusiva': 'Exclusive VIP experience',
    'Acesso reservado, hostess bilíngue, traslados': 'Reserved access, bilingual hostess, transfers',
    'Feijoada premiada para grupos': 'Award-winning feijoada for groups',
    'Reservar mesa': 'Book a table',
    'Fale conosco': 'Contact us',
    'Nosso endereço': 'Our address',
    'Como chegar': 'How to get there',
    'Ver cardápio': 'View menu',
    'Saiba mais': 'Learn more'
}

for f in Path('en').glob('*.html'):
    replace_in_file(f, en_replacements)

# 3. Correções de claims absolutos na Home PT
pt_claims = {
    'é o único restaurante dentro do Parque Bondinho': 'é o restaurante principal dentro do Parque Bondinho',
    'a única opção completa do complexo': 'a opção mais completa do complexo',
    'a maior base de avaliações e a maior nota entre os restaurantes': 'mais de 7.700 avaliações e nota 4,8★ entre os restaurantes',
    'Vista panorâmica</span> <span class="fato-label-hero">Mais bonita do mundo': 'Vista panorâmica</span> <span class="fato-label-hero">Frontal para o Pão de Açúcar',
    'o espaço mais bonito do Rio de Janeiro': 'um espaço panorâmico inesquecível no Rio de Janeiro',
    'O melhor restaurante com vista do Rio': 'Uma das experiências gastronômicas com vista mais marcantes do Rio'
}
replace_in_file('index.html', pt_claims)

# 4. Correções de claims absolutos na Home EN
en_claims = {
    'The only restaurant inside Parque Bondinho': 'The main restaurant inside Parque Bondinho',
    'the only complete option in the complex': 'the most complete option in the complex',
    'the largest review base and the highest rating': 'over 7,700 reviews and a 4.8★ rating',
    'most beautiful sunset in Rio de Janeiro': 'unforgettable sunset in Rio de Janeiro',
    'best view in the world': 'frontal view of Sugarloaf Mountain',
    'best restaurant Rio de Janeiro view': 'top restaurant Rio de Janeiro view'
}
replace_in_file('en/index.html', en_claims)

# 5. Criar redirects 301 para páginas antigas
redirect_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url={url}">
    <link rel="canonical" href="https://www.embaixadacarioca.com{url}">
    <title>Redirecionando...</title>
</head>
<body>
    <p>Redirecionando para <a href="{url}">a nova página</a>...</p>
</body>
</html>"""

redirects = {
    'café-da-manhã-com-a-melhor-vista-do-rio.html': '/cafe-da-manha.html',
    'caf%C3%A9-da-manh%C3%A3-com-a-melhor-vista-do-rio.html': '/cafe-da-manha.html',
    'contato.html': '/#visitar',
    'nossa-visao.html': '/#sobre',
    'Home v1.html': '/',
    'Home v2.html': '/'
}

for old_file, new_url in redirects.items():
    Path(old_file).write_text(redirect_template.format(url=new_url), encoding='utf-8')
    print(f"Criado redirect: {old_file} -> {new_url}")

# 6. Atualizar a página antiga cafe-da-manha-com-vista-rio.html para redirecionar
Path('cafe-da-manha-com-vista-rio.html').write_text(redirect_template.format(url='/cafe-da-manha.html'), encoding='utf-8')
print("Atualizado cafe-da-manha-com-vista-rio.html para redirect")

