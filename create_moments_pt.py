import os
from pathlib import Path
import re

# Template base (usando o guia-do-rio como base estrutural)
template = Path('guia-do-rio.html').read_text(encoding='utf-8')

# Configurações das 5 novas páginas
pages = [
    {
        'filename': 'cafe-da-manha-pao-de-acucar.html',
        'title': 'Café da Manhã com Vista no Rio de Janeiro | Embaixada Carioca',
        'desc': 'Onde tomar café da manhã com vista no Rio de Janeiro? Descubra a Embaixada Carioca, no Morro da Urca, com vista frontal para o Pão de Açúcar.',
        'h1': 'Café da Manhã com Vista no Rio de Janeiro',
        'h2': 'A melhor forma de começar o dia no Pão de Açúcar',
        'hero_img': 'https://www.embaixadacarioca.com/assets/cafe-da-manha.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Resposta Rápida</div>
                <h2>Onde tomar café da manhã com vista no Rio?</h2>
                <p class="lede">A <strong>Embaixada Carioca</strong> é o único restaurante dentro do Parque Bondinho Pão de Açúcar que serve café da manhã completo com vista panorâmica frontal para o Pão de Açúcar e a Baía de Guanabara. Servido todos os dias, das 8h30 às 11h30.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Como encaixar no roteiro</div>
                <h2>Planejando sua manhã no Pão de Açúcar</h2>
                <p class="lede">A melhor estratégia para evitar filas e aproveitar a luz da manhã:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;"><strong>8h00:</strong> Chegue na bilheteria da Praia Vermelha (abertura).</li>
                    <li style="margin-bottom: 16px;"><strong>8h20:</strong> Pegue um dos primeiros bondinhos para o Morro da Urca.</li>
                    <li style="margin-bottom: 16px;"><strong>8h30 - 9h30:</strong> Tome seu café da manhã na Embaixada Carioca com o terraço ainda vazio.</li>
                    <li style="margin-bottom: 16px;"><strong>9h45:</strong> Pegue o segundo bondinho até o topo do Pão de Açúcar.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> O Cardápio</div>
                <h2>O que servimos</h2>
                <p class="lede">Nosso cardápio inclui opções à la carte e combos completos para 2 pessoas. Destaques: pães artesanais, ovos mexidos, frutas frescas, sucos naturais, bolos e o clássico pão de queijo.</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Reservar Mesa para Café da Manhã</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Perguntas Frequentes</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">Preciso pagar o bondinho para tomar café?</h3>
                        <p style="color: var(--cinza1);">Sim, o restaurante fica no Morro da Urca (1ª parada), então é necessário o ingresso do Parque Bondinho.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">Precisa de reserva?</h3>
                        <p style="color: var(--cinza1);">Recomendamos fortemente a reserva, especialmente aos finais de semana, para garantir as melhores mesas no terraço.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'Restaurant',
        'schema_name': 'Café da Manhã na Embaixada Carioca'
    },
    {
        'filename': 'almoco-morro-da-urca.html',
        'title': 'Onde Almoçar no Morro da Urca | Embaixada Carioca',
        'desc': 'Procurando onde almoçar no Morro da Urca? A Embaixada Carioca oferece a melhor gastronomia brasileira com vista para o Pão de Açúcar.',
        'h1': 'Onde Almoçar no Morro da Urca',
        'h2': 'Gastronomia brasileira com a melhor vista do Rio',
        'hero_img': 'https://www.embaixadacarioca.com/assets/almoco.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Resposta Rápida</div>
                <h2>Onde almoçar no Morro da Urca?</h2>
                <p class="lede">A <strong>Embaixada Carioca</strong> é o restaurante principal do Morro da Urca (1ª parada do bondinho). Oferecemos um cardápio completo de almoço com pratos clássicos brasileiros, carnes premium e frutos do mar, tudo com vista panorâmica para o Pão de Açúcar.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Como encaixar no roteiro</div>
                <h2>Almoço perfeito no seu passeio</h2>
                <p class="lede">Como organizar seu tempo para almoçar com tranquilidade:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;"><strong>10h30:</strong> Subida pelo bondinho.</li>
                    <li style="margin-bottom: 16px;"><strong>11h00:</strong> Visita ao topo do Pão de Açúcar (2ª parada).</li>
                    <li style="margin-bottom: 16px;"><strong>12h30:</strong> Descida de volta ao Morro da Urca.</li>
                    <li style="margin-bottom: 16px;"><strong>13h00:</strong> Almoço na Embaixada Carioca. Reserve este horário para garantir mesa sem fila.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> O Cardápio</div>
                <h2>Destaques do Almoço</h2>
                <p class="lede">Nossa especialidade é a autêntica gastronomia carioca. O prato mais pedido é a nossa Picanha Grelhada Premium, seguida pela nossa premiada Feijoada. Também oferecemos opções vegetarianas e menu kids.</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Reservar Mesa para Almoço</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Perguntas Frequentes</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">Qual o horário do almoço?</h3>
                        <p style="color: var(--cinza1);">Servimos almoço todos os dias, das 12h às 16h.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">Aceitam grupos grandes?</h3>
                        <p style="color: var(--cinza1);">Sim, temos estrutura para receber grupos, mas é imprescindível fazer reserva antecipada.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'Restaurant',
        'schema_name': 'Almoço na Embaixada Carioca'
    },
    {
        'filename': 'feijoada-com-vista-rio-de-janeiro.html',
        'title': 'Onde Comer Feijoada no Rio de Janeiro | Embaixada Carioca',
        'desc': 'Buscando onde comer feijoada no Rio de Janeiro? A Embaixada Carioca serve feijoada premiada todos os dias com vista para o Pão de Açúcar.',
        'h1': 'Onde Comer Feijoada no Rio de Janeiro',
        'h2': 'A feijoada mais famosa da Urca, servida todos os dias',
        'hero_img': 'https://www.embaixadacarioca.com/assets/feijoada.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Resposta Rápida</div>
                <h2>Onde comer feijoada no Rio?</h2>
                <p class="lede">A <strong>Embaixada Carioca</strong>, localizada no Morro da Urca, serve uma das feijoadas mais elogiadas do Rio de Janeiro. O grande diferencial: <strong>servimos feijoada todos os dias</strong>, não apenas aos finais de semana, sempre acompanhada da vista panorâmica para o Pão de Açúcar.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Como encaixar no roteiro</div>
                <h2>Feijoada no passeio do Bondinho</h2>
                <p class="lede">A combinação perfeita de turismo e gastronomia:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;">Faça o passeio completo do Bondinho pela manhã.</li>
                    <li style="margin-bottom: 16px;">Programe sua descida do topo para o Morro da Urca por volta das 13h.</li>
                    <li style="margin-bottom: 16px;">Sente-se no nosso terraço, peça uma Caipirinha Magnífica e aproveite a feijoada completa.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> Nossa Feijoada</div>
                <h2>O que acompanha</h2>
                <p class="lede">Nossa feijoada é servida em panela de barro, acompanhada de arroz branco soltinho, farofa crocante, couve à mineira, torresmo, laranja e carnes nobres selecionadas. É o nosso segundo prato mais vendido!</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Reservar Mesa para Feijoada</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Perguntas Frequentes</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">A feijoada é servida durante a semana?</h3>
                        <p style="color: var(--cinza1);">Sim! Diferente da maioria dos restaurantes no Rio, servimos nossa feijoada completa todos os dias da semana.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">Serve quantas pessoas?</h3>
                        <p style="color: var(--cinza1);">Temos opções individuais e para compartilhar (2 pessoas), sempre muito bem servidas.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'Restaurant',
        'schema_name': 'Feijoada na Embaixada Carioca'
    },
    {
        'filename': 'caipirinha-com-vista-rio.html',
        'title': 'Onde Tomar Caipirinha no Rio de Janeiro | Embaixada Carioca',
        'desc': 'Onde tomar a melhor caipirinha no Rio de Janeiro? Prove a Caipirinha Magnífica da Embaixada Carioca com vista para o Pão de Açúcar.',
        'h1': 'Onde Tomar Caipirinha no Rio de Janeiro',
        'h2': 'A autêntica caipirinha carioca com a melhor vista da cidade',
        'hero_img': 'https://www.embaixadacarioca.com/assets/drinks.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Resposta Rápida</div>
                <h2>Onde tomar caipirinha no Rio?</h2>
                <p class="lede">Para a experiência completa, a <strong>Embaixada Carioca</strong> no Morro da Urca oferece a premiada Caipirinha com Cachaça Magnífica. É a combinação perfeita: a bebida mais tradicional do Brasil com a vista mais icônica do Rio de Janeiro.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Como encaixar no roteiro</div>
                <h2>O momento perfeito para um drink</h2>
                <p class="lede">Dicas para aproveitar sua caipirinha:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;"><strong>Pausa no passeio:</strong> Entre a subida e a descida do bondinho, faça uma pausa no nosso terraço.</li>
                    <li style="margin-bottom: 16px;"><strong>Acompanhamento:</strong> Peça nossa caipirinha junto com a Feijoada ou com nossa famosa porção de Pastéis.</li>
                    <li style="margin-bottom: 16px;"><strong>Golden Hour:</strong> O melhor horário é a partir das 16h, para tomar seu drink assistindo ao pôr do sol.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> Nossos Drinks</div>
                <h2>Além da Caipirinha</h2>
                <p class="lede">Nossa Caipirinha com Cachaça Magnífica é a estrela, mas também servimos o Chopp Heineken (considerado o melhor da cidade), drinks autorais, caipivodkas de frutas da estação e coquetéis clássicos.</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Reservar Mesa no Terraço</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Perguntas Frequentes</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">Quais os sabores de caipirinha?</h3>
                        <p style="color: var(--cinza1);">Além do tradicional limão, temos maracujá, morango, abacaxi e frutas vermelhas, dependendo da estação.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">Posso ir só para beber?</h3>
                        <p style="color: var(--cinza1);">Sim! Nosso terraço é perfeito para quem quer apenas tomar bons drinks e comer petiscos apreciando a vista.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'BarOrPub',
        'schema_name': 'Drinks na Embaixada Carioca'
    },
    {
        'filename': 'por-do-sol-morro-da-urca.html',
        'title': 'Pôr do Sol no Pão de Açúcar e Morro da Urca | Embaixada Carioca',
        'desc': 'Onde ver o pôr do sol no Pão de Açúcar? O terraço da Embaixada Carioca no Morro da Urca oferece a melhor vista para o entardecer no Rio.',
        'h1': 'Pôr do Sol no Pão de Açúcar',
        'h2': 'O entardecer mais inesquecível do Rio de Janeiro',
        'hero_img': 'https://www.embaixadacarioca.com/assets/entardecer.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Resposta Rápida</div>
                <h2>Onde ver o pôr do sol no Pão de Açúcar?</h2>
                <p class="lede">O melhor lugar para assistir ao pôr do sol é no terraço da <strong>Embaixada Carioca</strong>, no Morro da Urca. Você tem vista frontal para o Pão de Açúcar de um lado, e para a Baía de Guanabara e Cristo Redentor do outro, onde o sol se põe, tudo isso com conforto, drinks e boa gastronomia.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Como encaixar no roteiro</div>
                <h2>Planejando seu entardecer</h2>
                <p class="lede">O roteiro perfeito para o fim de tarde:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;"><strong>15h30:</strong> Suba pelo bondinho e vá direto ao topo do Pão de Açúcar.</li>
                    <li style="margin-bottom: 16px;"><strong>16h30:</strong> Desça para o Morro da Urca.</li>
                    <li style="margin-bottom: 16px;"><strong>17h00:</strong> Sente-se na Embaixada Carioca, peça um Chopp Heineken gelado ou uma Caipirinha.</li>
                    <li style="margin-bottom: 16px;"><strong>17h30 - 18h30:</strong> Assista ao espetáculo do pôr do sol e o acender das luzes da cidade.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> O que pedir</div>
                <h2>Acompanhamentos para o pôr do sol</h2>
                <p class="lede">Para o entardecer, recomendamos nossa famosa porção de Bolinhos de Bacalhau, os Pastéis crocantes ou a tábua de Picanha fatiada, acompanhados do nosso Chopp Heineken, considerado o melhor da cidade.</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Reservar Mesa para o Entardecer</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Perguntas Frequentes</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">Que horas o sol se põe?</h3>
                        <p style="color: var(--cinza1);">Varia ao longo do ano, geralmente entre 17h15 (inverno) e 19h30 (verão). Recomendamos chegar ao restaurante 1 hora antes.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">É muito cheio neste horário?</h3>
                        <p style="color: var(--cinza1);">Sim, o entardecer é o horário mais disputado do Parque Bondinho. A reserva antecipada na Embaixada Carioca é essencial para garantir seu lugar sentado.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'Restaurant',
        'schema_name': 'Entardecer na Embaixada Carioca'
    }
]

for page in pages:
    # Substituir meta tags e título
    content = re.sub(r'<title>.*?</title>', f'<title>{page["title"]}</title>', template)
    content = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{page["desc"]}">', content)
    
    # Atualizar canonical e hreflang
    canonical_url = f'https://www.embaixadacarioca.com/{page["filename"].replace(".html", "")}'
    content = re.sub(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{canonical_url}" />', content)
    content = re.sub(r'<link rel="alternate" hreflang="pt-BR" href="[^"]*" />', f'<link rel="alternate" hreflang="pt-BR" href="{canonical_url}" />', content)
    content = re.sub(r'<link rel="alternate" hreflang="en" href="[^"]*" />', f'<link rel="alternate" hreflang="en" href="https://www.embaixadacarioca.com/en/{page["filename"].replace(".html", "")}" />', content)
    content = re.sub(r'<link rel="alternate" hreflang="es" href="[^"]*" />', f'<link rel="alternate" hreflang="es" href="https://www.embaixadacarioca.com/es/{page["filename"].replace(".html", "")}" />', content)
    content = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]*" />', f'<link rel="alternate" hreflang="x-default" href="{canonical_url}" />', content)
    
    # Substituir H1 e H2 do hero
    content = re.sub(r'<h1 class="hero-title">.*?</h1>', f'<h1 class="hero-title">{page["h1"]}</h1>', content, flags=re.DOTALL)
    content = re.sub(r'<p class="hero-subtitle">.*?</p>', f'<p class="hero-subtitle">{page["h2"]}</p>', content, flags=re.DOTALL)
    
    # Substituir imagem do hero
    content = re.sub(r'background-image:\s*url\([^)]+\)', f'background-image: url({page["hero_img"]})', content)
    
    # Substituir o conteúdo principal (tudo entre <main> e o footer/newsletter)
    main_start = content.find('<main>') + 6
    newsletter_start = content.find('<section class="newsletter">')
    if newsletter_start == -1:
        newsletter_start = content.find('<footer')
    
    content = content[:main_start] + f'\n<section class="content-section" style="padding: 80px 0;">\n{page["content"]}\n</section>\n' + content[newsletter_start:]
    
    # Atualizar Schema JSON-LD
    schema_pattern = r'<script type="application/ld\+json">.*?</script>'
    new_schema = f'''<script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "{page['schema_type']}",
      "name": "{page['schema_name']}",
      "image": "{page['hero_img']}",
      "description": "{page['desc']}",
      "url": "{canonical_url}",
      "telephone": "+5521966837556",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "Estrada Dona Castorina, 110 - Urca",
        "addressLocality": "Rio de Janeiro",
        "addressRegion": "RJ",
        "postalCode": "22290-240",
        "addressCountry": "BR"
      }}
    }}
    </script>'''
    content = re.sub(schema_pattern, new_schema, content, count=1, flags=re.DOTALL)
    
    # Salvar arquivo
    Path(page['filename']).write_text(content, encoding='utf-8')
    print(f"✅ Criada: {page['filename']}")

