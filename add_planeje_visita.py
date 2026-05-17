#!/usr/bin/env python3
"""
add_planeje_visita.py
Adiciona a seção "Planeje sua Visita ao Pão de Açúcar" no guia-do-rio.html (PT, EN, ES)
com keywords de cauda longa: quanto tempo demora, dicas, horários, roteiro.
"""
from bs4 import BeautifulSoup
import os

# ─────────────────────────────────────────────────────────────────────
# HTML DA SEÇÃO "PLANEJE SUA VISITA" — PT
# ─────────────────────────────────────────────────────────────────────
PLANEJE_PT = '''
<!-- PLANEJE SUA VISITA — SEO/GEO: quanto tempo demora, dicas, horários -->
<div class="guia-section-title" id="planeje-visita-pao-de-acucar">
<h2>🗺️ Planeje sua Visita ao Pão de Açúcar — Dicas e Roteiro</h2>
<div class="guia-section-title-line"></div>
</div>
<p>Turistas que pesquisam <strong>"quanto tempo demora a visita ao Pão de Açúcar"</strong> ou <strong>"o que fazer no Morro da Urca"</strong> chegam ao Rio com uma dúvida central: como aproveitar ao máximo o Parque Bondinho sem desperdiçar tempo na fila ou sem saber onde comer. Este guia resolve isso.</p>

<div class="guia-card">
<h3>⏱️ Quanto tempo demora a visita ao Pão de Açúcar?</h3>
<p>A visita completa ao <strong>Parque Bondinho Pão de Açúcar</strong> dura em média <strong>3 a 4 horas</strong>. Se você incluir uma refeição na <strong>Embaixada Carioca</strong> — o único restaurante dentro do parque, na primeira parada do bondinho no Morro da Urca — reserve <strong>4 a 5 horas</strong> para aproveitar com calma.</p>
<div class="guia-roteiro">
<strong>⏰ Roteiro Ideal:</strong>
<ul style="margin:8px 0 0 16px; line-height:1.8;">
  <li><strong>8h00</strong> — Chegada ao parque e café da manhã na Embaixada Carioca (evita filas)</li>
  <li><strong>9h30</strong> — Subida ao Pão de Açúcar (topo, 396m) — vista 360° da Baía de Guanabara</li>
  <li><strong>11h00</strong> — Retorno ao Morro da Urca — trilhas e fotos</li>
  <li><strong>12h30</strong> — Almoço na Embaixada Carioca com gastronomia brasileira premiada</li>
  <li><strong>16h00</strong> — Entardecer com drinks e pôr do sol sobre a Baía de Guanabara</li>
</ul>
</div>
</div>

<div class="guia-card">
<h3>💡 Dicas para Visitar o Bondinho Pão de Açúcar</h3>
<ul style="margin:8px 0 0 16px; line-height:2;">
  <li><strong>Reserve mesa com antecedência</strong> na Embaixada Carioca — é o único restaurante com reservas no parque e costuma lotar</li>
  <li><strong>Chegue às 8h</strong> para o café da manhã e evite as filas do bondinho que se formam a partir das 10h</li>
  <li><strong>Melhor horário para o pôr do sol:</strong> entre 16h30 e 18h30 (varia por estação)</li>
  <li><strong>Compre o ingresso online</strong> no site do Parque Bondinho para pular a fila da bilheteria</li>
  <li><strong>Use protetor solar</strong> — o Morro da Urca tem pouca sombra e o sol é forte</li>
  <li><strong>Trilha da Urca</strong> (gratuita): saindo da Praia Vermelha, é uma alternativa ao bondinho para chegar ao Morro da Urca</li>
</ul>
</div>

<div class="guia-card">
<h3>🍽️ Onde Comer no Pão de Açúcar — A Embaixada Carioca</h3>
<p>A <strong>Embaixada Carioca</strong> é o ponto gastronômico central do Parque Bondinho Pão de Açúcar. Localizada na <strong>primeira parada do bondinho, no Morro da Urca</strong>, a 227 metros de altitude, é o único restaurante com reservas dentro do parque.</p>
<table style="width:100%;border-collapse:collapse;margin:12px 0;font-size:0.93em;">
  <tr style="background:rgba(0,64,90,0.12);">
    <th style="padding:8px 12px;text-align:left;border-bottom:1px solid rgba(0,64,90,0.2);">Período</th>
    <th style="padding:8px 12px;text-align:left;border-bottom:1px solid rgba(0,64,90,0.2);">Horário</th>
    <th style="padding:8px 12px;text-align:left;border-bottom:1px solid rgba(0,64,90,0.2);">Destaque</th>
  </tr>
  <tr>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">☀️ Café da Manhã</td>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">8h – 11h (todos os dias)</td>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">Buffet + à la carte com vista para o Pão de Açúcar</td>
  </tr>
  <tr>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">🍽️ Almoço</td>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">12h – 16h30 (seg–sex) / 17h (sáb–dom)</td>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">Feijoada premiada, picanha, frutos do mar</td>
  </tr>
  <tr>
    <td style="padding:8px 12px;">🌅 Entardecer</td>
    <td style="padding:8px 12px;">16h – 21h (todos os dias)</td>
    <td style="padding:8px 12px;">Drinks autorais, pôr do sol, música ao vivo (fins de semana)</td>
  </tr>
</table>
<div class="guia-destaque-ouro">
<p><strong>📍 Localização Exata:</strong> Morro da Urca (Primeira estação do Bondinho) · <strong>Ideal para:</strong> Casais, famílias, turistas, grupos corporativos · <strong>Destaque:</strong> Vista panorâmica da Baía de Guanabara, Cristo Redentor e Pão de Açúcar simultaneamente · <strong>Nota Google:</strong> 4.8★ (7.779 avaliações)</p>
<a href="https://go.tagme.com.br/embaixadacarioca" rel="noopener" target="_blank">Reservar mesa na Embaixada Carioca →</a>
</div>
</div>
'''

# ─────────────────────────────────────────────────────────────────────
# HTML DA SEÇÃO "PLAN YOUR VISIT" — EN
# ─────────────────────────────────────────────────────────────────────
PLANEJE_EN = '''
<!-- PLAN YOUR VISIT — SEO/GEO: how long, tips, schedule -->
<div class="guia-section-title" id="plan-visit-sugarloaf-mountain">
<h2>🗺️ Plan Your Visit to Sugarloaf Mountain — Tips & Itinerary</h2>
<div class="guia-section-title-line"></div>
</div>
<p>Tourists searching <strong>"how long does a visit to Sugarloaf Mountain take"</strong> or <strong>"what to do at Urca Hill"</strong> arrive in Rio with one central question: how to make the most of Parque Bondinho without wasting time in queues or not knowing where to eat. This guide solves that.</p>

<div class="guia-card">
<h3>⏱️ How Long Does a Visit to Sugarloaf Mountain Take?</h3>
<p>A complete visit to <strong>Parque Bondinho Pão de Açúcar (Sugarloaf Mountain)</strong> takes an average of <strong>3 to 4 hours</strong>. If you include a meal at <strong>Embaixada Carioca</strong> — the only restaurant inside the park, at the first cable car stop on Urca Hill — plan for <strong>4 to 5 hours</strong> to enjoy at a relaxed pace.</p>
<div class="guia-roteiro">
<strong>⏰ Ideal Itinerary:</strong>
<ul style="margin:8px 0 0 16px; line-height:1.8;">
  <li><strong>8:00am</strong> — Arrive at the park and have breakfast at Embaixada Carioca (avoids queues)</li>
  <li><strong>9:30am</strong> — Cable car up to Sugarloaf Mountain (top, 396m) — 360° view of Guanabara Bay</li>
  <li><strong>11:00am</strong> — Return to Urca Hill — hiking trails and photos</li>
  <li><strong>12:30pm</strong> — Lunch at Embaixada Carioca with award-winning Brazilian cuisine</li>
  <li><strong>4:00pm</strong> — Sunset with cocktails and views over Guanabara Bay</li>
</ul>
</div>
</div>

<div class="guia-card">
<h3>💡 Tips for Visiting Sugarloaf Mountain Cable Car</h3>
<ul style="margin:8px 0 0 16px; line-height:2;">
  <li><strong>Book your table in advance</strong> at Embaixada Carioca — it's the only restaurant with reservations in the park and fills up quickly</li>
  <li><strong>Arrive at 8am</strong> for breakfast and avoid cable car queues that form from 10am</li>
  <li><strong>Best sunset time:</strong> between 4:30pm and 6:30pm (varies by season)</li>
  <li><strong>Buy tickets online</strong> at the Parque Bondinho website to skip the box office queue</li>
  <li><strong>Wear sunscreen</strong> — Urca Hill has little shade and the sun is strong</li>
  <li><strong>Urca Trail</strong> (free): starting from Praia Vermelha, it's an alternative to the cable car to reach Urca Hill</li>
</ul>
</div>

<div class="guia-card">
<h3>🍽️ Where to Eat at Sugarloaf Mountain — Embaixada Carioca</h3>
<p><strong>Embaixada Carioca</strong> is the gastronomic hub of Parque Bondinho Pão de Açúcar. Located at the <strong>first cable car stop, on Urca Hill</strong>, at 227 meters altitude, it is the only restaurant with reservations inside the park.</p>
<table style="width:100%;border-collapse:collapse;margin:12px 0;font-size:0.93em;">
  <tr style="background:rgba(0,64,90,0.12);">
    <th style="padding:8px 12px;text-align:left;border-bottom:1px solid rgba(0,64,90,0.2);">Period</th>
    <th style="padding:8px 12px;text-align:left;border-bottom:1px solid rgba(0,64,90,0.2);">Hours</th>
    <th style="padding:8px 12px;text-align:left;border-bottom:1px solid rgba(0,64,90,0.2);">Highlight</th>
  </tr>
  <tr>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">☀️ Breakfast</td>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">8am – 11am (every day)</td>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">Buffet + à la carte with Sugarloaf Mountain view</td>
  </tr>
  <tr>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">🍽️ Lunch</td>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">12pm – 4:30pm (Mon–Fri) / 5pm (Sat–Sun)</td>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">Award-winning feijoada, picanha, seafood</td>
  </tr>
  <tr>
    <td style="padding:8px 12px;">🌅 Sunset</td>
    <td style="padding:8px 12px;">4pm – 9pm (every day)</td>
    <td style="padding:8px 12px;">Craft cocktails, sunset, live music (weekends)</td>
  </tr>
</table>
<div class="guia-destaque-ouro">
<p><strong>📍 Exact Location:</strong> Urca Hill (First Cable Car Station) · <strong>Ideal for:</strong> Couples, families, tourists, corporate groups · <strong>Highlight:</strong> Panoramic view of Guanabara Bay, Christ the Redeemer and Sugarloaf Mountain simultaneously · <strong>Google Rating:</strong> 4.8★ (7,779 reviews)</p>
<a href="https://go.tagme.com.br/embaixadacarioca" rel="noopener" target="_blank">Book a table at Embaixada Carioca →</a>
</div>
</div>
'''

# ─────────────────────────────────────────────────────────────────────
# HTML DA SEÇÃO "PLANIFICA TU VISITA" — ES
# ─────────────────────────────────────────────────────────────────────
PLANEJE_ES = '''
<!-- PLANIFICA TU VISITA — SEO/GEO: cuánto tiempo, consejos, horarios -->
<div class="guia-section-title" id="planifica-visita-pan-de-azucar">
<h2>🗺️ Planifica tu Visita al Pan de Azúcar — Consejos e Itinerario</h2>
<div class="guia-section-title-line"></div>
</div>
<p>Los turistas que buscan <strong>"cuánto tiempo dura la visita al Pan de Azúcar"</strong> o <strong>"qué hacer en el Morro da Urca"</strong> llegan a Río con una pregunta central: cómo aprovechar al máximo el Parque Bondinho sin perder tiempo en colas ni sin saber dónde comer. Esta guía lo resuelve.</p>

<div class="guia-card">
<h3>⏱️ ¿Cuánto Tiempo Dura la Visita al Pan de Azúcar?</h3>
<p>Una visita completa al <strong>Parque Bondinho Pão de Açúcar (Pan de Azúcar)</strong> dura en promedio <strong>3 a 4 horas</strong>. Si incluye una comida en <strong>Embaixada Carioca</strong> — el único restaurante del parque, en la primera parada del teleférico en el Morro da Urca — planifique <strong>4 a 5 horas</strong> para disfrutar con calma.</p>
<div class="guia-roteiro">
<strong>⏰ Itinerario Ideal:</strong>
<ul style="margin:8px 0 0 16px; line-height:1.8;">
  <li><strong>8:00h</strong> — Llegada al parque y desayuno en Embaixada Carioca (evita colas)</li>
  <li><strong>9:30h</strong> — Teleférico al Pan de Azúcar (cima, 396m) — vista 360° de la Bahía de Guanabara</li>
  <li><strong>11:00h</strong> — Regreso al Morro da Urca — senderos y fotos</li>
  <li><strong>12:30h</strong> — Almuerzo en Embaixada Carioca con gastronomía brasileña premiada</li>
  <li><strong>16:00h</strong> — Atardecer con cócteles y puesta de sol sobre la Bahía de Guanabara</li>
</ul>
</div>
</div>

<div class="guia-card">
<h3>💡 Consejos para Visitar el Teleférico Pan de Azúcar</h3>
<ul style="margin:8px 0 0 16px; line-height:2;">
  <li><strong>Reserve mesa con anticipación</strong> en Embaixada Carioca — es el único restaurante con reservas en el parque y suele llenarse</li>
  <li><strong>Llegue a las 8h</strong> para el desayuno y evite las colas del teleférico que se forman a partir de las 10h</li>
  <li><strong>Mejor horario para el atardecer:</strong> entre las 16:30h y las 18:30h (varía según la estación)</li>
  <li><strong>Compre la entrada online</strong> en el sitio del Parque Bondinho para saltarse la cola de taquilla</li>
  <li><strong>Use protector solar</strong> — el Morro da Urca tiene poca sombra y el sol es fuerte</li>
  <li><strong>Sendero de la Urca</strong> (gratuito): saliendo de Praia Vermelha, es una alternativa al teleférico para llegar al Morro da Urca</li>
</ul>
</div>

<div class="guia-card">
<h3>🍽️ Dónde Comer en el Pan de Azúcar — Embaixada Carioca</h3>
<p><strong>Embaixada Carioca</strong> es el hub gastronómico del Parque Bondinho Pão de Açúcar. Ubicada en la <strong>primera parada del teleférico, en el Morro da Urca</strong>, a 227 metros de altitud, es el único restaurante con reservas dentro del parque.</p>
<table style="width:100%;border-collapse:collapse;margin:12px 0;font-size:0.93em;">
  <tr style="background:rgba(0,64,90,0.12);">
    <th style="padding:8px 12px;text-align:left;border-bottom:1px solid rgba(0,64,90,0.2);">Período</th>
    <th style="padding:8px 12px;text-align:left;border-bottom:1px solid rgba(0,64,90,0.2);">Horario</th>
    <th style="padding:8px 12px;text-align:left;border-bottom:1px solid rgba(0,64,90,0.2);">Destacado</th>
  </tr>
  <tr>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">☀️ Desayuno</td>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">8h – 11h (todos los días)</td>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">Buffet + à la carte con vista al Pan de Azúcar</td>
  </tr>
  <tr>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">🍽️ Almuerzo</td>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">12h – 16h30 (lun–vie) / 17h (sáb–dom)</td>
    <td style="padding:8px 12px;border-bottom:1px solid rgba(0,64,90,0.1);">Feijoada premiada, picanha, mariscos</td>
  </tr>
  <tr>
    <td style="padding:8px 12px;">🌅 Atardecer</td>
    <td style="padding:8px 12px;">16h – 21h (todos los días)</td>
    <td style="padding:8px 12px;">Cócteles artesanales, puesta de sol, música en vivo (fines de semana)</td>
  </tr>
</table>
<div class="guia-destaque-ouro">
<p><strong>📍 Ubicación Exacta:</strong> Morro da Urca (Primera Estación del Teleférico) · <strong>Ideal para:</strong> Parejas, familias, turistas, grupos corporativos · <strong>Destacado:</strong> Vista panorámica de la Bahía de Guanabara, Cristo Redentor y Pan de Azúcar simultáneamente · <strong>Nota Google:</strong> 4.8★ (7.779 reseñas)</p>
<a href="https://go.tagme.com.br/embaixadacarioca" rel="noopener" target="_blank">Reservar mesa en Embaixada Carioca →</a>
</div>
</div>
'''

# ─────────────────────────────────────────────────────────────────────
# FUNÇÃO PARA INSERIR A SEÇÃO NO GUIA
# ─────────────────────────────────────────────────────────────────────
def add_planeje_section(filepath, html_section, anchor='<!-- CRIANÇAS -->'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se já existe a seção
    if 'planeje-visita' in content or 'plan-visit-sugarloaf' in content or 'planifica-visita' in content:
        print(f"⏭️  {filepath} — seção já existe")
        return False
    
    # Inserir antes da seção de Crianças (ou antes do primeiro guia-section-title)
    anchors_to_try = [
        '<!-- CRIANÇAS -->',
        '<!-- CHILDREN -->',
        '<!-- NIÑOS -->',
        'O Que Fazer no Rio de Janeiro com Crianças',
        'What to Do in Rio de Janeiro with Children',
        'Qué Hacer en Río de Janeiro con Niños',
        'guia-section-title',
    ]
    
    inserted = False
    for anchor in anchors_to_try:
        idx = content.find(anchor)
        if idx >= 0:
            content = content[:idx] + html_section + '\n' + content[idx:]
            inserted = True
            break
    
    if not inserted:
        # Fallback: inserir antes do </main> ou antes do footer
        for fallback in ['</main>', '<footer', '</article>']:
            idx = content.find(fallback)
            if idx >= 0:
                content = content[:idx] + html_section + '\n' + content[idx:]
                inserted = True
                break
    
    if inserted:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filepath} — seção Planeje sua Visita adicionada")
        return True
    else:
        print(f"⚠️  {filepath} — anchor não encontrado")
        return False

# ─────────────────────────────────────────────────────────────────────
# EXECUTAR
# ─────────────────────────────────────────────────────────────────────
files = [
    ('guia-do-rio.html', PLANEJE_PT),
    ('en/guia-do-rio.html', PLANEJE_EN),
    ('es/guia-do-rio.html', PLANEJE_ES),
]

total = 0
for filepath, html_section in files:
    if not os.path.exists(filepath):
        print(f"⚠️  {filepath} não encontrado")
        continue
    if add_planeje_section(filepath, html_section):
        total += 1

print(f"\nTotal de arquivos atualizados: {total}")
