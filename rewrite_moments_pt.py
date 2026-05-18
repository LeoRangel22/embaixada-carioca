import os
from pathlib import Path
from bs4 import BeautifulSoup

# As páginas atuais foram geradas de forma muito básica.
# Vamos reescrevê-las com o conteúdo rico sugerido pelo usuário:
# H1 específico, resposta rápida, bloco de roteiro, fotos reais, CTA, FAQ curto, schema.

pages_data = {
    'cafe-da-manha-pao-de-acucar.html': {
        'title': 'Café da Manhã com Vista no Rio de Janeiro | Embaixada Carioca',
        'desc': 'Onde tomar café da manhã com vista no Rio? A Embaixada Carioca serve café da manhã todos os dias no Morro da Urca, com vista para o Pão de Açúcar.',
        'h1': 'Café da Manhã com Vista no Rio de Janeiro',
        'h1_sub': 'A melhor forma de começar o dia no Pão de Açúcar.',
        'resposta': 'A <strong>Embaixada Carioca</strong> é o único restaurante dentro do Parque Bondinho Pão de Açúcar que serve café da manhã completo com vista panorâmica frontal para o Pão de Açúcar e a Baía de Guanabara. Servido <strong>todos os dias</strong>, das 8h30 às 11h30.',
        'roteiro_title': 'Como encaixar no seu roteiro',
        'roteiro': [
            ('8h00', 'Chegue na bilheteria da Praia Vermelha logo na abertura para evitar filas.'),
            ('8h20', 'Pegue um dos primeiros bondinhos para o Morro da Urca (primeira parada).'),
            ('8h30 - 9h30', 'Tome seu café da manhã na Embaixada Carioca com o terraço ainda vazio e a melhor luz para fotos.'),
            ('9h45', 'Pegue o segundo bondinho até o topo do Pão de Açúcar com energia recarregada.')
        ],
        'cardapio_title': 'O que pedir no Café da Manhã',
        'cardapio_desc': 'Nosso cardápio inclui opções à la carte e combos completos para 2 pessoas. Destaques:',
        'cardapio_items': ['Pães artesanais de fermentação natural', 'Ovos mexidos cremosos', 'Frutas tropicais frescas', 'Sucos naturais e café especial', 'O clássico pão de queijo quentinho'],
        'faq': [
            ('Preciso pagar o bondinho para tomar café?', 'Sim, o restaurante fica no Morro da Urca (1ª parada), então é necessário o ingresso do Parque Bondinho.'),
            ('Precisa de reserva?', 'Recomendamos fortemente a reserva, especialmente aos finais de semana, para garantir as melhores mesas no terraço com vista.')
        ],
        'schema_type': 'Restaurant',
        'schema_name': 'Café da Manhã na Embaixada Carioca'
    },
    'almoco-morro-da-urca.html': {
        'title': 'Onde Almoçar no Morro da Urca e Pão de Açúcar | Embaixada Carioca',
        'desc': 'Procurando onde almoçar no Morro da Urca? A Embaixada Carioca oferece a melhor gastronomia brasileira com vista panorâmica no Pão de Açúcar.',
        'h1': 'Onde Almoçar no Morro da Urca',
        'h1_sub': 'Gastronomia brasileira com a melhor vista do Rio.',
        'resposta': 'A <strong>Embaixada Carioca</strong> é a principal escolha para almoçar no Morro da Urca. Localizada na primeira parada do bondinho, oferece pratos clássicos brasileiros, como a famosa Picanha Grelhada e a Feijoada Premiada, com vista panorâmica para a Baía de Guanabara.',
        'roteiro_title': 'Como encaixar o almoço no seu passeio',
        'roteiro': [
            ('10h00', 'Suba o primeiro bondinho até o Morro da Urca e explore a área.'),
            ('11h00', 'Pegue o segundo bondinho até o topo do Pão de Açúcar.'),
            ('12h30', 'Desça de volta ao Morro da Urca.'),
            ('13h00', 'Almoce na Embaixada Carioca com tranquilidade antes de descer para a Praia Vermelha.')
        ],
        'cardapio_title': 'Destaques do Almoço',
        'cardapio_desc': 'Nossa especialidade é a autêntica culinária carioca e brasileira. Os pratos mais pedidos:',
        'cardapio_items': ['Picanha Grelhada (nosso prato mais vendido)', 'Feijoada Premiada (servida todos os dias)', 'Picadinho Carioca', 'Bolinho de Bacalhau autêntico', 'Chopp Heineken (eleito o 2º melhor do Brasil)'],
        'faq': [
            ('Qual o horário do almoço?', 'Servimos almoço todos os dias, das 11h30 às 16h00. Após esse horário, o cardápio de petiscos e jantar continua disponível.'),
            ('Aceitam grupos grandes?', 'Sim! Temos infraestrutura para receber grupos de turismo e famílias grandes. Recomendamos reserva antecipada.')
        ],
        'schema_type': 'Restaurant',
        'schema_name': 'Almoço na Embaixada Carioca'
    },
    'feijoada-com-vista-rio-de-janeiro.html': {
        'title': 'Onde Comer Feijoada no Rio de Janeiro com Vista | Embaixada Carioca',
        'desc': 'A melhor feijoada do Rio de Janeiro com vista para o Pão de Açúcar. Servida todos os dias na Embaixada Carioca, no Morro da Urca.',
        'h1': 'Onde Comer Feijoada no Rio de Janeiro',
        'h1_sub': 'A autêntica feijoada carioca servida todos os dias.',
        'resposta': 'Se você busca onde comer feijoada no Rio, a <strong>Embaixada Carioca</strong> serve sua Feijoada Premiada <strong>todos os dias da semana</strong>. Eleita pela Veja Rio Comer & Beber como uma das melhores da cidade, você degusta este clássico com vista frontal para o Pão de Açúcar.',
        'roteiro_title': 'A experiência completa da Feijoada',
        'roteiro': [
            ('12h00', 'Chegue à Embaixada Carioca no Morro da Urca.'),
            ('12h15', 'Comece com nossa Caipirinha de Cachaça Magnífica premiada e um caldinho de feijão.'),
            ('12h45', 'Aproveite a Feijoada completa, servida em panelinhas de ferro tradicionais.'),
            ('14h30', 'Finalize com uma sobremesa típica brasileira e um café expresso.')
        ],
        'cardapio_title': 'O que acompanha nossa Feijoada',
        'cardapio_desc': 'Nossa feijoada é preparada com carnes nobres selecionadas e acompanha todos os clássicos:',
        'cardapio_items': ['Arroz branco soltinho', 'Farofa crocante', 'Couve mineira refogada', 'Torresmo', 'Laranja fresca em fatias'],
        'faq': [
            ('A feijoada é servida durante a semana?', 'Sim! Diferente da maioria dos restaurantes no Rio que servem apenas às sextas e sábados, nós servimos nossa feijoada todos os dias.'),
            ('Serve quantas pessoas?', 'Temos opções individuais bem servidas e opções para compartilhar (2 pessoas).')
        ],
        'schema_type': 'Restaurant',
        'schema_name': 'Feijoada na Embaixada Carioca'
    },
    'caipirinha-com-vista-rio.html': {
        'title': 'Onde Tomar Caipirinha no Rio com Vista | Embaixada Carioca',
        'desc': 'A melhor caipirinha do Rio de Janeiro com vista para o Pão de Açúcar. Cachaça Magnífica premiada e frutas frescas no Morro da Urca.',
        'h1': 'Onde Tomar Caipirinha no Rio de Janeiro',
        'h1_sub': 'O drink nacional com a vista mais icônica do Brasil.',
        'resposta': 'Para tomar a autêntica caipirinha no Rio com uma vista inesquecível, o terraço da <strong>Embaixada Carioca</strong> no Morro da Urca é o local perfeito. Nossa caipirinha é preparada com a premiada Cachaça Magnífica e frutas frescas selecionadas.',
        'roteiro_title': 'O momento perfeito para um drink',
        'roteiro': [
            ('16h00', 'Após visitar o topo do Pão de Açúcar, desça para o Morro da Urca.'),
            ('16h15', 'Garanta uma mesa na varanda da Embaixada Carioca.'),
            ('16h30', 'Peça nossa Caipirinha Magnífica acompanhada de Pastéis ou Bolinhos de Bacalhau.'),
            ('17h30', 'Aproveite seu drink enquanto assiste ao pôr do sol sobre a Baía de Guanabara.')
        ],
        'cardapio_title': 'Nossas Caipirinhas e Petiscos',
        'cardapio_desc': 'Além da clássica caipirinha de limão, oferecemos variações e os melhores acompanhamentos:',
        'cardapio_items': ['Caipirinha Clássica de Limão com Cachaça Magnífica', 'Caipivodka de frutas da estação (Maracujá, Morango, Kiwi)', 'Pastel de Queijo e Carne', 'Bolinho de Bacalhau', 'Espetinhos variados'],
        'faq': [
            ('Quais os sabores de caipirinha?', 'Além do tradicional limão, temos maracujá, morango, abacaxi e kiwi, dependendo da estação. Podem ser feitas com cachaça, vodka ou saquê.'),
            ('Posso ir só para beber?', 'Claro! Nosso terraço é perfeito para um happy hour descontraído após o passeio.')
        ],
        'schema_type': 'BarOrPub',
        'schema_name': 'Caipirinha e Drinks na Embaixada Carioca'
    },
    'por-do-sol-morro-da-urca.html': {
        'title': 'Pôr do Sol no Pão de Açúcar e Morro da Urca | Embaixada Carioca',
        'desc': 'Onde ver o pôr do sol no Pão de Açúcar? A Embaixada Carioca no Morro da Urca oferece a melhor vista para o entardecer no Rio de Janeiro.',
        'h1': 'Pôr do Sol no Pão de Açúcar',
        'h1_sub': 'O entardecer mais espetacular do Rio de Janeiro.',
        'resposta': 'O melhor lugar para ver o pôr do sol no complexo do Pão de Açúcar é no terraço da <strong>Embaixada Carioca</strong>, localizado no Morro da Urca. Você assiste ao sol se pondo atrás do Cristo Redentor e da Baía de Guanabara com conforto, drinks e boa gastronomia.',
        'roteiro_title': 'Planejando seu entardecer',
        'roteiro': [
            ('15h30', 'Suba pelo bondinho para aproveitar a luz da tarde.'),
            ('16h30', 'Chegue à Embaixada Carioca no Morro da Urca e escolha uma mesa na varanda.'),
            ('17h00', 'Peça o Chopp Heineken (eleito o 2º melhor do Brasil) ou uma Caipirinha.'),
            ('17h30 - 18h00', 'Aprecie o espetáculo do pôr do sol (o horário exato varia conforme a estação do ano).')
        ],
        'cardapio_title': 'Acompanhamentos para o Pôr do Sol',
        'cardapio_desc': 'O happy hour perfeito pede os melhores petiscos cariocas:',
        'cardapio_items': ['Chopp Heineken estupidamente gelado', 'Caipirinhas com Cachaça Magnífica', 'Tábua de petiscos mistos', 'Empadas artesanais', 'Sanduíches especiais'],
        'faq': [
            ('Que horas o sol se põe?', 'Varia ao longo do ano. No verão (dez-fev) por volta das 19h30. No inverno (jun-ago) por volta das 17h15. Recomendamos chegar 1 hora antes.'),
            ('É muito cheio neste horário?', 'O pôr do sol é o horário de pico do Parque Bondinho. Ter uma reserva na Embaixada Carioca garante seu conforto longe das multidões.')
        ],
        'schema_type': 'Restaurant',
        'schema_name': 'Pôr do Sol na Embaixada Carioca'
    }
}

# Template base para as páginas
template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="stylesheet" href="assets/style.css">
    <link rel="stylesheet" href="assets/fonts/fonts.css">
    <link rel="canonical" href="https://www.embaixadacarioca.com/{slug}">
    <link rel="alternate" hreflang="pt-BR" href="https://www.embaixadacarioca.com/{slug}">
    <link rel="alternate" hreflang="en" href="https://www.embaixadacarioca.com/en/{slug}">
    <link rel="alternate" hreflang="es" href="https://www.embaixadacarioca.com/es/{slug}">
    <link rel="alternate" hreflang="x-default" href="https://www.embaixadacarioca.com/{slug}">
    <style>
        .page-hero-content .eyebrow.hero-eyebrow {{
            color: rgba(246, 239, 222, 0.75);
            margin-bottom: 20px;
            font-size: 10px;
            letter-spacing: 0.22em;
        }}
        .page-hero-content .eyebrow.hero-eyebrow::before {{
            background: var(--amarelo, #d4a017);
        }}
    </style>
</head>
<body>
    <a href="#conteudo-principal" class="skip-nav">Pular para o conteúdo principal</a>
    
    <nav class="top" id="topnav">
        <div class="nav-inner">
            <a href="index.html" class="brand-mark" aria-label="Embaixada Carioca · início">
                <img src="assets/logo-areia.svg" alt="Embaixada Carioca" class="brand-logo light" loading="lazy">
                <img src="assets/logo-azul.svg" alt="Embaixada Carioca" class="brand-logo dark" loading="lazy">
            </a>
            <ul class="nav-links">
                <li><a href="cafe-da-manha.html">Café da Manhã</a></li>
                <li><a href="almoco.html">Almoço</a></li>
                <li><a href="entardecer.html">Entardecer</a></li>
                <li><a href="eventos.html">Eventos</a></li>
                <li><a href="cardapio.html">Cardápio</a></li>
                <li><a href="guia-do-rio.html">Guia do Rio</a></li>
            </ul>
            <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Reservar →</a>
        </div>
    </nav>

    <header class="page-hero">
        <picture>
            <source media="(max-width: 720px)" srcset="assets/hero-mobile.webp" type="image/webp">
            <source srcset="assets/hero.jpg" type="image/jpg">
            <img src="assets/hero.webp" alt="{h1}" class="page-hero-photo" loading="eager" decoding="async">
        </picture>
        <div class="page-hero-overlay" aria-hidden="true"></div>
        <div class="page-hero-content">
            <div class="eyebrow hero-eyebrow">Restaurante Brasileiro do Bondinho · Restaurante Carioca Tradicional de Qualidade · Morro da Urca · Parque Bondinho Pão de Açúcar · Rio de Janeiro · Brasil</div>
            <div class="crumbs">
                <a href="index.html">Home</a> <span class="sep">/</span> <span class="here">{h1}</span>
            </div>
            <h1>{h1}</h1>
            <p class="lede">{h1_sub}</p>
        </div>
    </header>

    <main id="conteudo-principal">
        <section style="padding: 4rem 0; background: var(--areia-pale);">
            <div class="wrap" style="max-width: 800px; margin: 0 auto;">
                <div style="background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 3rem;">
                    <h2 style="color: var(--azul-escuro); margin-bottom: 1rem; font-size: 1.8rem;">A Resposta Rápida</h2>
                    <p style="font-size: 1.2rem; line-height: 1.6; color: var(--cinza1);">{resposta}</p>
                </div>

                <h2 style="color: var(--azul-escuro); margin-bottom: 1.5rem; font-size: 2rem;">{roteiro_title}</h2>
                <div style="margin-bottom: 3rem;">
                    {roteiro_html}
                </div>

                <h2 style="color: var(--azul-escuro); margin-bottom: 1.5rem; font-size: 2rem;">{cardapio_title}</h2>
                <p style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-bottom: 1rem;">{cardapio_desc}</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-bottom: 3rem; padding-left: 20px;">
                    {cardapio_items_html}
                </ul>

                <div style="text-align: center; margin: 4rem 0; padding: 3rem; background: var(--azul-escuro); border-radius: 8px; color: white;">
                    <h3 style="font-size: 1.8rem; margin-bottom: 1rem; color: white;">Garanta sua mesa com vista</h3>
                    <p style="font-size: 1.1rem; margin-bottom: 2rem; opacity: 0.9;">Recomendamos reserva antecipada para garantir os melhores lugares no terraço.</p>
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn" style="background: var(--amarelo); color: var(--azul-escuro); font-size: 1.2rem; padding: 1rem 2rem;">Reservar Mesa Agora</a>
                </div>

                <h2 style="color: var(--azul-escuro); margin-bottom: 1.5rem; font-size: 2rem;">Perguntas Frequentes</h2>
                <div style="display: grid; gap: 1.5rem;">
                    {faq_html}
                </div>
            </div>
        </section>
    </main>

    <footer class="foot">
        <div class="wrap">
            <div class="foot-top">
                <div class="foot-brand">
                    <p class="big">Embaixada<br><span class="serif">Carioca.</span></p>
                    <p class="tagline">O consulado da gastronomia e da cultura brasileira para o mundo — no alto do Morro da Urca, Rio de Janeiro.</p>
                </div>
            </div>
            <div class="foot-bottom">
                <div>Parque Bondinho Pão de Açúcar · Rio de Janeiro</div>
                <div>© 2026 · Todos os direitos reservados</div>
            </div>
        </div>
    </footer>

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "{schema_type}",
      "name": "{schema_name}",
      "image": "https://www.embaixadacarioca.com/assets/hero.jpg",
      "url": "https://www.embaixadacarioca.com/{slug}",
      "telephone": "+5521966837556",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "Av. Pasteur, 520 - Morro da Urca",
        "addressLocality": "Rio de Janeiro",
        "addressRegion": "RJ",
        "postalCode": "22290-240",
        "addressCountry": "BR"
      }}
    }}
    </script>
</body>
</html>"""

for filename, data in pages_data.items():
    slug = filename
    
    # Gerar HTML do roteiro
    roteiro_html = ""
    for time, desc in data['roteiro']:
        roteiro_html += f'<div style="display: flex; gap: 1rem; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(0,0,0,0.1);"><div style="font-weight: bold; color: var(--verde); min-width: 100px;">{time}</div><div style="color: var(--cinza1); line-height: 1.5;">{desc}</div></div>\n'
        
    # Gerar HTML dos itens do cardápio
    cardapio_items_html = ""
    for item in data['cardapio_items']:
        cardapio_items_html += f'<li style="margin-bottom: 0.5rem;">{item}</li>\n'
        
    # Gerar HTML do FAQ
    faq_html = ""
    for q, a in data['faq']:
        faq_html += f'<div style="background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);"><h3 style="font-size: 1.2rem; margin-bottom: 0.5rem; color: var(--azul-escuro);">{q}</h3><p style="color: var(--cinza1); line-height: 1.5;">{a}</p></div>\n'
        
    # Preencher template
    html = template.format(
        slug=slug,
        title=data['title'],
        desc=data['desc'],
        h1=data['h1'],
        h1_sub=data['h1_sub'],
        resposta=data['resposta'],
        roteiro_title=data['roteiro_title'],
        roteiro_html=roteiro_html,
        cardapio_title=data['cardapio_title'],
        cardapio_desc=data['cardapio_desc'],
        cardapio_items_html=cardapio_items_html,
        faq_html=faq_html,
        schema_type=data['schema_type'],
        schema_name=data['schema_name']
    )
    
    Path(filename).write_text(html, encoding='utf-8')
    print(f"✅ Recriada: {filename}")

