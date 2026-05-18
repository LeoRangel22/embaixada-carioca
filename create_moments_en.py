import os
from pathlib import Path
import re

# Template base (usando o guia-do-rio EN como base estrutural)
template = Path('en/guia-do-rio.html').read_text(encoding='utf-8')

# Configurações das 5 novas páginas EN
pages = [
    {
        'filename': 'en/cafe-da-manha-pao-de-acucar.html',
        'title': 'Breakfast with a View in Rio de Janeiro | Embaixada Carioca',
        'desc': 'Where to have breakfast with a view in Rio de Janeiro? Discover Embaixada Carioca on Urca Hill, with a frontal view of Sugarloaf Mountain.',
        'h1': 'Breakfast with a View in Rio de Janeiro',
        'h2': 'The best way to start your day at Sugarloaf Mountain',
        'hero_img': 'https://www.embaixadacarioca.com/assets/cafe-da-manha.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Quick Answer</div>
                <h2>Where to have breakfast with a view in Rio?</h2>
                <p class="lede"><strong>Embaixada Carioca</strong> is the only restaurant inside the Sugarloaf Cable Car Park that serves a full breakfast with a frontal panoramic view of Sugarloaf Mountain and Guanabara Bay. Served every day, from 8:30am to 11:30am.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Itinerary Integration</div>
                <h2>Planning your morning at Sugarloaf</h2>
                <p class="lede">The best strategy to avoid lines and enjoy the morning light:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;"><strong>8:00am:</strong> Arrive at Praia Vermelha ticket office (opening time).</li>
                    <li style="margin-bottom: 16px;"><strong>8:20am:</strong> Take one of the first cable cars to Urca Hill.</li>
                    <li style="margin-bottom: 16px;"><strong>8:30am - 9:30am:</strong> Have your breakfast at Embaixada Carioca while the terrace is still empty.</li>
                    <li style="margin-bottom: 16px;"><strong>9:45am:</strong> Take the second cable car to the top of Sugarloaf Mountain.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> The Menu</div>
                <h2>What we serve</h2>
                <p class="lede">Our menu includes à la carte options and full combos for 2 people. Highlights: artisanal breads, scrambled eggs, fresh fruits, natural juices, cakes, and the classic Brazilian cheese bread (pão de queijo).</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Book a Table for Breakfast</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Frequently Asked Questions</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">Do I need to pay for the cable car to have breakfast?</h3>
                        <p style="color: var(--cinza1);">Yes, the restaurant is located on Urca Hill (1st stop), so a Cable Car Park ticket is required.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">Do I need a reservation?</h3>
                        <p style="color: var(--cinza1);">We highly recommend booking in advance, especially on weekends, to secure the best tables on the terrace.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'Restaurant',
        'schema_name': 'Breakfast at Embaixada Carioca'
    },
    {
        'filename': 'en/almoco-morro-da-urca.html',
        'title': 'Where to Lunch on Urca Hill | Embaixada Carioca',
        'desc': 'Looking for where to lunch on Urca Hill? Embaixada Carioca offers the best Brazilian gastronomy with a view of Sugarloaf Mountain.',
        'h1': 'Where to Lunch on Urca Hill',
        'h2': 'Brazilian gastronomy with the best view in Rio',
        'hero_img': 'https://www.embaixadacarioca.com/assets/almoco.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Quick Answer</div>
                <h2>Where to lunch on Urca Hill?</h2>
                <p class="lede"><strong>Embaixada Carioca</strong> is the main restaurant on Urca Hill (1st cable car stop). We offer a full lunch menu with classic Brazilian dishes, premium meats, and seafood, all with a panoramic view of Sugarloaf Mountain.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Itinerary Integration</div>
                <h2>Perfect lunch during your tour</h2>
                <p class="lede">How to organize your time for a relaxed lunch:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;"><strong>10:30am:</strong> Go up via cable car.</li>
                    <li style="margin-bottom: 16px;"><strong>11:00am:</strong> Visit the top of Sugarloaf Mountain (2nd stop).</li>
                    <li style="margin-bottom: 16px;"><strong>12:30pm:</strong> Go back down to Urca Hill.</li>
                    <li style="margin-bottom: 16px;"><strong>1:00pm:</strong> Lunch at Embaixada Carioca. Book this time to secure a table without waiting.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> The Menu</div>
                <h2>Lunch Highlights</h2>
                <p class="lede">Our specialty is authentic Carioca gastronomy. The most ordered dish is our Premium Grilled Picanha, followed by our award-winning Feijoada. We also offer vegetarian options and a kids menu.</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Book a Table for Lunch</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Frequently Asked Questions</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">What are the lunch hours?</h3>
                        <p style="color: var(--cinza1);">We serve lunch every day, from 12:00pm to 4:00pm.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">Do you accept large groups?</h3>
                        <p style="color: var(--cinza1);">Yes, we have the structure to host groups, but advance booking is essential.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'Restaurant',
        'schema_name': 'Lunch at Embaixada Carioca'
    },
    {
        'filename': 'en/feijoada-com-vista-rio-de-janeiro.html',
        'title': 'Where to Eat Feijoada in Rio de Janeiro | Embaixada Carioca',
        'desc': 'Looking for where to eat feijoada in Rio de Janeiro? Embaixada Carioca serves award-winning feijoada every day with a view of Sugarloaf Mountain.',
        'h1': 'Where to Eat Feijoada in Rio de Janeiro',
        'h2': 'The most famous feijoada in Urca, served every day',
        'hero_img': 'https://www.embaixadacarioca.com/assets/feijoada.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Quick Answer</div>
                <h2>Where to eat feijoada in Rio?</h2>
                <p class="lede"><strong>Embaixada Carioca</strong>, located on Urca Hill, serves one of the most highly praised feijoadas in Rio de Janeiro. The big difference: <strong>we serve feijoada every day</strong>, not just on weekends, always accompanied by a panoramic view of Sugarloaf Mountain.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Itinerary Integration</div>
                <h2>Feijoada during your Cable Car tour</h2>
                <p class="lede">The perfect combination of tourism and gastronomy:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;">Do the full Cable Car tour in the morning.</li>
                    <li style="margin-bottom: 16px;">Plan your descent from the top to Urca Hill around 1:00pm.</li>
                    <li style="margin-bottom: 16px;">Sit on our terrace, order a Magnífica Caipirinha, and enjoy the complete feijoada.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> Our Feijoada</div>
                <h2>What it includes</h2>
                <p class="lede">Our feijoada is served in a clay pot, accompanied by fluffy white rice, crispy farofa, mineira-style collard greens, pork rinds (torresmo), orange slices, and selected premium meats. It is our second best-selling dish!</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Book a Table for Feijoada</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Frequently Asked Questions</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">Is feijoada served during the week?</h3>
                        <p style="color: var(--cinza1);">Yes! Unlike most restaurants in Rio, we serve our complete feijoada every day of the week.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">How many people does it serve?</h3>
                        <p style="color: var(--cinza1);">We have individual options and portions to share (2 people), always very well served.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'Restaurant',
        'schema_name': 'Feijoada at Embaixada Carioca'
    },
    {
        'filename': 'en/caipirinha-com-vista-rio.html',
        'title': 'Where to Drink Caipirinha in Rio de Janeiro | Embaixada Carioca',
        'desc': 'Where to drink the best caipirinha in Rio de Janeiro? Try the Magnífica Caipirinha at Embaixada Carioca with a view of Sugarloaf Mountain.',
        'h1': 'Where to Drink Caipirinha in Rio de Janeiro',
        'h2': 'The authentic Carioca caipirinha with the best view in the city',
        'hero_img': 'https://www.embaixadacarioca.com/assets/drinks.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Quick Answer</div>
                <h2>Where to drink caipirinha in Rio?</h2>
                <p class="lede">For the complete experience, <strong>Embaixada Carioca</strong> on Urca Hill offers the award-winning Caipirinha with Magnífica Cachaça. It is the perfect combination: Brazil's most traditional drink with the most iconic view of Rio de Janeiro.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Itinerary Integration</div>
                <h2>The perfect moment for a drink</h2>
                <p class="lede">Tips to enjoy your caipirinha:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;"><strong>Tour break:</strong> Between going up and down the cable car, take a break on our terrace.</li>
                    <li style="margin-bottom: 16px;"><strong>Pairing:</strong> Order our caipirinha along with Feijoada or our famous portion of Pastéis (crispy pastries).</li>
                    <li style="margin-bottom: 16px;"><strong>Golden Hour:</strong> The best time is from 4:00pm onwards, to have your drink while watching the sunset.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> Our Drinks</div>
                <h2>Beyond Caipirinha</h2>
                <p class="lede">Our Caipirinha with Magnífica Cachaça is the star, but we also serve Heineken Draft Beer (considered the best in the city), signature drinks, seasonal fruit caipivodkas, and classic cocktails.</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Book a Table on the Terrace</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Frequently Asked Questions</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">What caipirinha flavors do you have?</h3>
                        <p style="color: var(--cinza1);">Besides the traditional lime, we have passion fruit, strawberry, pineapple, and red berries, depending on the season.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">Can I go just for drinks?</h3>
                        <p style="color: var(--cinza1);">Yes! Our terrace is perfect for those who just want to have good drinks and snacks while enjoying the view.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'BarOrPub',
        'schema_name': 'Drinks at Embaixada Carioca'
    },
    {
        'filename': 'en/por-do-sol-morro-da-urca.html',
        'title': 'Sunset at Sugarloaf Mountain and Urca Hill | Embaixada Carioca',
        'desc': 'Where to watch the sunset at Sugarloaf Mountain? Embaixada Carioca\'s terrace on Urca Hill offers the best view for the sunset in Rio.',
        'h1': 'Sunset at Sugarloaf Mountain',
        'h2': 'The most unforgettable sunset in Rio de Janeiro',
        'hero_img': 'https://www.embaixadacarioca.com/assets/entardecer.jpg',
        'content': '''
        <div class="wrap">
            <div class="sec-head">
                <div class="num"><b>01</b> Quick Answer</div>
                <h2>Where to watch the sunset at Sugarloaf?</h2>
                <p class="lede">The best place to watch the sunset is on the terrace of <strong>Embaixada Carioca</strong>, on Urca Hill. You have a frontal view of Sugarloaf Mountain on one side, and Guanabara Bay and Christ the Redeemer on the other, where the sun sets, all with comfort, drinks, and good gastronomy.</p>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>02</b> Itinerary Integration</div>
                <h2>Planning your sunset</h2>
                <p class="lede">The perfect itinerary for the late afternoon:</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-top: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 16px;"><strong>3:30pm:</strong> Go up via cable car straight to the top of Sugarloaf Mountain.</li>
                    <li style="margin-bottom: 16px;"><strong>4:30pm:</strong> Go down to Urca Hill.</li>
                    <li style="margin-bottom: 16px;"><strong>5:00pm:</strong> Sit at Embaixada Carioca, order a cold Heineken Draft Beer or a Caipirinha.</li>
                    <li style="margin-bottom: 16px;"><strong>5:30pm - 6:30pm:</strong> Watch the sunset spectacle and the city lights turning on.</li>
                </ul>
            </div>

            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>03</b> What to order</div>
                <h2>Pairings for the sunset</h2>
                <p class="lede">For the sunset, we recommend our famous portion of Cod Fritters (Bolinhos de Bacalhau), crispy Pastéis, or the sliced Picanha board, accompanied by our Heineken Draft Beer, considered the best in the city.</p>
                <div style="margin-top: 32px;">
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">Book a Table for Sunset</a>
                </div>
            </div>
            
            <div class="sec-head" style="margin-top: 64px;">
                <div class="num"><b>04</b> FAQ</div>
                <h2>Frequently Asked Questions</h2>
                <div class="faq-grid" style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-top: 32px;">
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">What time does the sun set?</h3>
                        <p style="color: var(--cinza1);">It varies throughout the year, usually between 5:15pm (winter) and 7:30pm (summer). We recommend arriving at the restaurant 1 hour before.</p>
                    </div>
                    <div style="border-top: 1px solid var(--rule); padding-top: 16px;">
                        <h3 style="font-size: 18px; margin-bottom: 8px;">Is it very crowded at this time?</h3>
                        <p style="color: var(--cinza1);">Yes, sunset is the most sought-after time at the Cable Car Park. Advance booking at Embaixada Carioca is essential to secure your seat.</p>
                    </div>
                </div>
            </div>
        </div>
        ''',
        'schema_type': 'Restaurant',
        'schema_name': 'Sunset at Embaixada Carioca'
    }
]

for page in pages:
    # Substituir meta tags e título
    content = re.sub(r'<title>.*?</title>', f'<title>{page["title"]}</title>', template)
    content = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{page["desc"]}">', content)
    
    # Atualizar canonical e hreflang
    canonical_url = f'https://www.embaixadacarioca.com/{page["filename"].replace(".html", "")}'
    pt_url = f'https://www.embaixadacarioca.com/{page["filename"].replace("en/", "").replace(".html", "")}'
    es_url = f'https://www.embaixadacarioca.com/es/{page["filename"].replace("en/", "").replace(".html", "")}'
    
    content = re.sub(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{canonical_url}" />', content)
    content = re.sub(r'<link rel="alternate" hreflang="pt-BR" href="[^"]*" />', f'<link rel="alternate" hreflang="pt-BR" href="{pt_url}" />', content)
    content = re.sub(r'<link rel="alternate" hreflang="en" href="[^"]*" />', f'<link rel="alternate" hreflang="en" href="{canonical_url}" />', content)
    content = re.sub(r'<link rel="alternate" hreflang="es" href="[^"]*" />', f'<link rel="alternate" hreflang="es" href="{es_url}" />', content)
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

