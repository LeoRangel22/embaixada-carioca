import os
from pathlib import Path
import re

# Template base (usando o guia-do-rio ES como base estrutural)
template = Path('es/guia-do-rio.html').read_text(encoding='utf-8')

# Configurações das 5 novas páginas ES
pages = [
    {
        'filename': 'es/cafe-da-manha-pao-de-acucar.html',
        'title': 'Desayuno con Vista en Río de Janeiro | Embaixada Carioca',
        'desc': '¿Dónde desayunar con vista en Río de Janeiro? Descubre Embaixada Carioca en el Morro da Urca, con vista frontal al Pan de Azúcar.',
        'h1': 'Desayuno con Vista en Río de Janeiro',
        'h2': 'La mejor manera de empezar tu día en el Pan de Azúcar',
        'hero_img': 'https://www.embaixadacarioca.com/assets/cafe-da-manha.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Respuesta Rápida</div>
                <h2>¿Dónde desayunar con vista en Río?</h2>
                <p class="lede"><strong>Embaixada Carioca</strong> es el único restaurante dentro del Parque del Teleférico del Pan de Azúcar que sirve un desayuno completo con vista panorámica frontal al Pan de Azúcar y la Bahía de Guanabara. Servido todos los días, de 8:30 a 11:30.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Integración en el Itinerario</div>
                <h2>Planeando tu mañana en el Pan de Azúcar</h2>
                <p class="lede">La mejor estrategia para evitar filas y disfrutar de la luz de la mañana:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;"><strong>8:00:</strong> Llega a la taquilla de Praia Vermelha (hora de apertura).</li>
                    <li style="margin-bottom: 16px;"><strong>8:20:</strong> Toma uno de los primeros teleféricos hacia el Morro da Urca.</li>
                    <li style="margin-bottom: 16px;"><strong>8:30 - 9:30:</strong> Desayuna en Embaixada Carioca mientras la terraza aún está vacía.</li>
                    <li style="margin-bottom: 16px;"><strong>9:45:</strong> Toma el segundo teleférico hasta la cima del Pan de Azúcar.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> El Menú</div>
                <h2>Lo que servimos</h2>
                <p class="lede">Nuestro menú incluye opciones a la carta y combos completos para 2 personas. Destacados: panes artesanales, huevos revueltos, frutas frescas, jugos naturales, pasteles y el clásico pan de queso brasileño (pão de queijo).</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Reservar Mesa para Desayuno</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Preguntas Frecuentes</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">¿Necesito pagar el teleférico para desayunar?</h3>
                        <p style="color: var(--cinza1);">Sí, el restaurante está ubicado en el Morro da Urca (1ª parada), por lo que se requiere un boleto del Parque del Teleférico.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">¿Necesito hacer reserva?</h3>
                        <p style="color: var(--cinza1);">Recomendamos encarecidamente reservar con anticipación, especialmente los fines de semana, para asegurar las mejores mesas en la terraza.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'Restaurant',
        'schema_name': 'Desayuno en Embaixada Carioca'
    },
    {
        'filename': 'es/almoco-morro-da-urca.html',
        'title': 'Dónde Almorzar en el Morro da Urca | Embaixada Carioca',
        'desc': '¿Buscas dónde almorzar en el Morro da Urca? Embaixada Carioca ofrece la mejor gastronomía brasileña con vista al Pan de Azúcar.',
        'h1': 'Dónde Almorzar en el Morro da Urca',
        'h2': 'Gastronomía brasileña con la mejor vista de Río',
        'hero_img': 'https://www.embaixadacarioca.com/assets/almoco.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Respuesta Rápida</div>
                <h2>¿Dónde almorzar en el Morro da Urca?</h2>
                <p class="lede"><strong>Embaixada Carioca</strong> es el restaurante principal en el Morro da Urca (1ª parada del teleférico). Ofrecemos un menú de almuerzo completo con platos clásicos brasileños, carnes premium y mariscos, todo con vista panorámica al Pan de Azúcar.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Integración en el Itinerario</div>
                <h2>Almuerzo perfecto durante tu tour</h2>
                <p class="lede">Cómo organizar tu tiempo para un almuerzo relajado:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;"><strong>10:30:</strong> Sube en el teleférico.</li>
                    <li style="margin-bottom: 16px;"><strong>11:00:</strong> Visita la cima del Pan de Azúcar (2ª parada).</li>
                    <li style="margin-bottom: 16px;"><strong>12:30:</strong> Baja de regreso al Morro da Urca.</li>
                    <li style="margin-bottom: 16px;"><strong>13:00:</strong> Almuerzo en Embaixada Carioca. Reserva a esta hora para asegurar una mesa sin esperas.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> El Menú</div>
                <h2>Destacados del Almuerzo</h2>
                <p class="lede">Nuestra especialidad es la auténtica gastronomía carioca. El plato más pedido es nuestra Picanha a la Parrilla Premium, seguida de nuestra galardonada Feijoada. También ofrecemos opciones vegetarianas y menú infantil.</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Reservar Mesa para Almuerzo</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Preguntas Frecuentes</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">¿Cuál es el horario de almuerzo?</h3>
                        <p style="color: var(--cinza1);">Servimos almuerzo todos los días, de 12:00 a 16:00.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">¿Aceptan grupos grandes?</h3>
                        <p style="color: var(--cinza1);">Sí, tenemos la estructura para recibir grupos, pero es imprescindible reservar con anticipación.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'Restaurant',
        'schema_name': 'Almuerzo en Embaixada Carioca'
    },
    {
        'filename': 'es/feijoada-com-vista-rio-de-janeiro.html',
        'title': 'Dónde Comer Feijoada en Río de Janeiro | Embaixada Carioca',
        'desc': '¿Buscas dónde comer feijoada en Río de Janeiro? Embaixada Carioca sirve feijoada galardonada todos los días con vista al Pan de Azúcar.',
        'h1': 'Dónde Comer Feijoada en Río de Janeiro',
        'h2': 'La feijoada más famosa de Urca, servida todos los días',
        'hero_img': 'https://www.embaixadacarioca.com/assets/feijoada.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Respuesta Rápida</div>
                <h2>¿Dónde comer feijoada en Río?</h2>
                <p class="lede"><strong>Embaixada Carioca</strong>, ubicada en el Morro da Urca, sirve una de las feijoadas más elogiadas de Río de Janeiro. La gran diferencia: <strong>servimos feijoada todos los días</strong>, no solo los fines de semana, siempre acompañada de una vista panorámica al Pan de Azúcar.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Integración en el Itinerario</div>
                <h2>Feijoada durante tu tour en Teleférico</h2>
                <p class="lede">La combinación perfecta de turismo y gastronomía:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;">Haz el tour completo del Teleférico por la mañana.</li>
                    <li style="margin-bottom: 16px;">Planea tu descenso desde la cima hasta el Morro da Urca alrededor de las 13:00.</li>
                    <li style="margin-bottom: 16px;">Siéntate en nuestra terraza, pide una Caipirinha Magnífica y disfruta de la feijoada completa.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> Nuestra Feijoada</div>
                <h2>Qué incluye</h2>
                <p class="lede">Nuestra feijoada se sirve en una olla de barro, acompañada de arroz blanco suelto, farofa crujiente, col rizada estilo mineira, chicharrones (torresmo), rodajas de naranja y carnes premium seleccionadas. ¡Es nuestro segundo plato más vendido!</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Reservar Mesa para Feijoada</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Preguntas Frecuentes</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">¿Se sirve feijoada durante la semana?</h3>
                        <p style="color: var(--cinza1);">¡Sí! A diferencia de la mayoría de los restaurantes en Río, servimos nuestra feijoada completa todos los días de la semana.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">¿Para cuántas personas es?</h3>
                        <p style="color: var(--cinza1);">Tenemos opciones individuales y porciones para compartir (2 personas), siempre muy bien servidas.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'Restaurant',
        'schema_name': 'Feijoada en Embaixada Carioca'
    },
    {
        'filename': 'es/caipirinha-com-vista-rio.html',
        'title': 'Dónde Tomar Caipirinha en Río de Janeiro | Embaixada Carioca',
        'desc': '¿Dónde tomar la mejor caipirinha en Río de Janeiro? Prueba la Caipirinha Magnífica en Embaixada Carioca con vista al Pan de Azúcar.',
        'h1': 'Dónde Tomar Caipirinha en Río de Janeiro',
        'h2': 'La auténtica caipirinha carioca con la mejor vista de la ciudad',
        'hero_img': 'https://www.embaixadacarioca.com/assets/drinks.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Respuesta Rápida</div>
                <h2>¿Dónde tomar caipirinha en Río?</h2>
                <p class="lede">Para la experiencia completa, <strong>Embaixada Carioca</strong> en el Morro da Urca ofrece la galardonada Caipirinha con Cachaça Magnífica. Es la combinación perfecta: la bebida más tradicional de Brasil con la vista más icónica de Río de Janeiro.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Integración en el Itinerario</div>
                <h2>El momento perfecto para un trago</h2>
                <p class="lede">Consejos para disfrutar tu caipirinha:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;"><strong>Pausa en el tour:</strong> Entre la subida y la bajada del teleférico, haz una pausa en nuestra terraza.</li>
                    <li style="margin-bottom: 16px;"><strong>Acompañamiento:</strong> Pide nuestra caipirinha junto con Feijoada o nuestra famosa porción de Pastéis (empanadas crujientes).</li>
                    <li style="margin-bottom: 16px;"><strong>Golden Hour:</strong> El mejor momento es a partir de las 16:00, para tomar tu trago mientras ves el atardecer.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> Nuestros Tragos</div>
                <h2>Más allá de la Caipirinha</h2>
                <p class="lede">Nuestra Caipirinha con Cachaça Magnífica es la estrella, pero también servimos Cerveza de Barril Heineken (considerada la mejor de la ciudad), tragos de autor, caipivodkas de frutas de temporada y cócteles clásicos.</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Reservar Mesa en la Terraza</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Preguntas Frecuentes</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">¿Qué sabores de caipirinha tienen?</h3>
                        <p style="color: var(--cinza1);">Además del tradicional limón, tenemos maracuyá, fresa, piña y frutos rojos, dependiendo de la temporada.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">¿Puedo ir solo a beber?</h3>
                        <p style="color: var(--cinza1);">¡Sí! Nuestra terraza es perfecta para quienes solo quieren tomar buenos tragos y comer bocadillos mientras disfrutan de la vista.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'BarOrPub',
        'schema_name': 'Tragos en Embaixada Carioca'
    },
    {
        'filename': 'es/por-do-sol-morro-da-urca.html',
        'title': 'Atardecer en el Pan de Azúcar y Morro da Urca | Embaixada Carioca',
        'desc': '¿Dónde ver el atardecer en el Pan de Azúcar? La terraza de Embaixada Carioca en el Morro da Urca ofrece la mejor vista para el atardecer en Río.',
        'h1': 'Atardecer en el Pan de Azúcar',
        'h2': 'El atardecer más inolvidable de Río de Janeiro',
        'hero_img': 'https://www.embaixadacarioca.com/assets/entardecer.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Respuesta Rápida</div>
                <h2>¿Dónde ver el atardecer en el Pan de Azúcar?</h2>
                <p class="lede">El mejor lugar para ver el atardecer es en la terraza de <strong>Embaixada Carioca</strong>, en el Morro da Urca. Tienes una vista frontal al Pan de Azúcar por un lado, y a la Bahía de Guanabara y el Cristo Redentor por el otro, donde se pone el sol, todo con comodidad, tragos y buena gastronomía.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Integración en el Itinerario</div>
                <h2>Planeando tu atardecer</h2>
                <p class="lede">El itinerario perfecto para el final de la tarde:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;"><strong>15:30:</strong> Sube en el teleférico directo a la cima del Pan de Azúcar.</li>
                    <li style="margin-bottom: 16px;"><strong>16:30:</strong> Baja al Morro da Urca.</li>
                    <li style="margin-bottom: 16px;"><strong>17:00:</strong> Siéntate en Embaixada Carioca, pide una Cerveza de Barril Heineken fría o una Caipirinha.</li>
                    <li style="margin-bottom: 16px;"><strong>17:30 - 18:30:</strong> Observa el espectáculo del atardecer y las luces de la ciudad encendiéndose.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> Qué pedir</div>
                <h2>Acompañamientos para el atardecer</h2>
                <p class="lede">Para el atardecer, recomendamos nuestra famosa porción de Buñuelos de Bacalao (Bolinhos de Bacalhau), Pastéis crujientes o la tabla de Picanha en rodajas, acompañados de nuestra Cerveza de Barril Heineken, considerada la mejor de la ciudad.</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Reservar Mesa para el Atardecer</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Preguntas Frecuentes</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">¿A qué hora se pone el sol?</h3>
                        <p style="color: var(--cinza1);">Varía a lo largo del año, generalmente entre las 17:15 (invierno) y las 19:30 (verano). Recomendamos llegar al restaurante 1 hora antes.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">¿Está muy lleno a esta hora?</h3>
                        <p style="color: var(--cinza1);">Sí, el atardecer es el momento más solicitado en el Parque del Teleférico. Reservar con anticipación en Embaixada Carioca es esencial para asegurar tu asiento.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'Restaurant',
        'schema_name': 'Atardecer en Embaixada Carioca'
    }
]

for page in pages:
    # Substituir meta tags e título
    content = re.sub(r'<title>.*?</title>', f'<title>{page["title"]}</title>', template)
    content = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{page["desc"]}">', content)
    
    # Atualizar canonical e hreflang
    canonical_url = f'https://www.embaixadacarioca.com/{page["filename"].replace(".html", "")}'
    pt_url = f'https://www.embaixadacarioca.com/{page["filename"].replace("es/", "").replace(".html", "")}'
    en_url = f'https://www.embaixadacarioca.com/en/{page["filename"].replace("es/", "").replace(".html", "")}'
    
    content = re.sub(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{canonical_url}" />', content)
    content = re.sub(r'<link rel="alternate" hreflang="pt-BR" href="[^"]*" />', f'<link rel="alternate" hreflang="pt-BR" href="{pt_url}" />', content)
    content = re.sub(r'<link rel="alternate" hreflang="en" href="[^"]*" />', f'<link rel="alternate" hreflang="en" href="{en_url}" />', content)
    content = re.sub(r'<link rel="alternate" hreflang="es" href="[^"]*" />', f'<link rel="alternate" hreflang="es" href="{canonical_url}" />', content)
    content = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]*" />', f'<link rel="alternate" hreflang="x-default" href="{pt_url}" />', content)
    
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

