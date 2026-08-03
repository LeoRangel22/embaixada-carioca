#!/usr/bin/env python3
"""
Ação 3: Adicionar bloco de resposta direta de horários do Pão de Açúcar
Objetivo: Capturar query "pão de açúcar horário" (870 impressões, CTR 0,11%, posição 7,83)
Estratégia: Inserir bloco visível com horários formatados para featured snippet + OpeningHoursSpecification no JSON-LD
"""
import json
from bs4 import BeautifulSoup

CONFIGS = {
    'morro-da-urca.html': {
        'block_html': '''
<section class="horarios-box" id="horarios-pao-de-acucar" aria-label="Horários do Parque Bondinho Pão de Açúcar">
  <h2>Horário do Parque Bondinho Pão de Açúcar</h2>
  <p>O Parque Bondinho Pão de Açúcar funciona <strong>todos os dias das 8h às 21h</strong>, com última subida às 20h. A Embaixada Carioca, o restaurante dentro do parque no Morro da Urca, atende das <strong>12h às 21h</strong>.</p>
  <table class="horarios-table">
    <thead>
      <tr><th>Local</th><th>Horário de funcionamento</th></tr>
    </thead>
    <tbody>
      <tr><td>Parque Bondinho Pão de Açúcar</td><td>Todos os dias · 8h às 21h (última subida 20h)</td></tr>
      <tr><td>Embaixada Carioca (restaurante)</td><td>Todos os dias · 12h às 21h</td></tr>
      <tr><td>Café da manhã</td><td>Todos os dias · 8h30 às 11h30</td></tr>
      <tr><td>Almoço e feijoada</td><td>Todos os dias · 12h às 17h</td></tr>
      <tr><td>Happy hour / entardecer</td><td>Todos os dias · 17h às 21h</td></tr>
    </tbody>
  </table>
  <p><small>Horários sujeitos a alteração em feriados e eventos especiais. Consulte o <a href="https://bondinho.com.br" rel="noopener noreferrer" target="_blank">site oficial do Bondinho</a> para confirmar.</small></p>
</section>
<style>
.horarios-box { background: #f8f9fa; border-left: 4px solid #c8a96e; border-radius: 8px; padding: 28px 32px; margin: 40px 0; }
.horarios-box h2 { font-size: 1.4rem; margin-bottom: 12px; color: #1a1a2e; }
.horarios-table { width: 100%; border-collapse: collapse; margin: 16px 0; }
.horarios-table th { background: #1a1a2e; color: #fff; padding: 10px 14px; text-align: left; font-size: 0.9rem; }
.horarios-table td { padding: 10px 14px; border-bottom: 1px solid #e0e0e0; font-size: 0.95rem; }
.horarios-table tr:last-child td { border-bottom: none; }
</style>''',
        'opening_hours': [
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], 'opens': '12:00', 'closes': '21:00'}
        ],
        'speakable_selectors': ['h1', '.hero-sub', '.faq-answer', '#horarios-pao-de-acucar', '.horarios-box']
    },
    'en/morro-da-urca.html': {
        'block_html': '''
<section class="horarios-box" id="sugarloaf-opening-hours" aria-label="Sugarloaf Mountain Park Opening Hours">
  <h2>Sugarloaf Mountain Park Opening Hours</h2>
  <p>Sugarloaf Mountain Park (Parque Bondinho Pão de Açúcar) is open <strong>every day from 8am to 9pm</strong>, with the last cable car at 8pm. Embaixada Carioca, the restaurant inside the park at Urca Hill, is open from <strong>12pm to 9pm</strong>.</p>
  <table class="horarios-table">
    <thead>
      <tr><th>Location</th><th>Opening hours</th></tr>
    </thead>
    <tbody>
      <tr><td>Sugarloaf Mountain Park (Parque Bondinho)</td><td>Every day · 8am to 9pm (last cable car 8pm)</td></tr>
      <tr><td>Embaixada Carioca (restaurant)</td><td>Every day · 12pm to 9pm</td></tr>
      <tr><td>Breakfast</td><td>Every day · 8:30am to 11:30am</td></tr>
      <tr><td>Lunch and feijoada</td><td>Every day · 12pm to 5pm</td></tr>
      <tr><td>Happy hour / sunset</td><td>Every day · 5pm to 9pm</td></tr>
    </tbody>
  </table>
  <p><small>Hours subject to change on holidays and special events. Check the <a href="https://bondinho.com.br" rel="noopener noreferrer" target="_blank">official Bondinho website</a> to confirm.</small></p>
</section>
<style>
.horarios-box { background: #f8f9fa; border-left: 4px solid #c8a96e; border-radius: 8px; padding: 28px 32px; margin: 40px 0; }
.horarios-box h2 { font-size: 1.4rem; margin-bottom: 12px; color: #1a1a2e; }
.horarios-table { width: 100%; border-collapse: collapse; margin: 16px 0; }
.horarios-table th { background: #1a1a2e; color: #fff; padding: 10px 14px; text-align: left; font-size: 0.9rem; }
.horarios-table td { padding: 10px 14px; border-bottom: 1px solid #e0e0e0; font-size: 0.95rem; }
.horarios-table tr:last-child td { border-bottom: none; }
</style>''',
        'opening_hours': [
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], 'opens': '12:00', 'closes': '21:00'}
        ],
        'speakable_selectors': ['h1', '.hero-sub', '.faq-answer', '#sugarloaf-opening-hours', '.horarios-box']
    },
    'es/morro-da-urca.html': {
        'block_html': '''
<section class="horarios-box" id="horarios-pan-de-azucar" aria-label="Horarios del Parque Bondinho Pan de Azúcar">
  <h2>Horario del Parque Bondinho Pan de Azúcar</h2>
  <p>El Parque Bondinho Pan de Azúcar abre <strong>todos los días de 8h a 21h</strong>, con el último teleférico a las 20h. La Embaixada Carioca, el restaurante dentro del parque en el Morro da Urca, atiende de <strong>12h a 21h</strong>.</p>
  <table class="horarios-table">
    <thead>
      <tr><th>Lugar</th><th>Horario de atención</th></tr>
    </thead>
    <tbody>
      <tr><td>Parque Bondinho Pan de Azúcar</td><td>Todos los días · 8h a 21h (último teleférico 20h)</td></tr>
      <tr><td>Embaixada Carioca (restaurante)</td><td>Todos los días · 12h a 21h</td></tr>
      <tr><td>Desayuno</td><td>Todos los días · 8h30 a 11h30</td></tr>
      <tr><td>Almuerzo y feijoada</td><td>Todos los días · 12h a 17h</td></tr>
      <tr><td>Happy hour / atardecer</td><td>Todos los días · 17h a 21h</td></tr>
    </tbody>
  </table>
  <p><small>Horarios sujetos a cambios en feriados y eventos especiales. Consulte el <a href="https://bondinho.com.br" rel="noopener noreferrer" target="_blank">sitio oficial del Bondinho</a> para confirmar.</small></p>
</section>
<style>
.horarios-box { background: #f8f9fa; border-left: 4px solid #c8a96e; border-radius: 8px; padding: 28px 32px; margin: 40px 0; }
.horarios-box h2 { font-size: 1.4rem; margin-bottom: 12px; color: #1a1a2e; }
.horarios-table { width: 100%; border-collapse: collapse; margin: 16px 0; }
.horarios-table th { background: #1a1a2e; color: #fff; padding: 10px 14px; text-align: left; font-size: 0.9rem; }
.horarios-table td { padding: 10px 14px; border-bottom: 1px solid #e0e0e0; font-size: 0.95rem; }
.horarios-table tr:last-child td { border-bottom: none; }
</style>''',
        'opening_hours': [
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], 'opens': '12:00', 'closes': '21:00'}
        ],
        'speakable_selectors': ['h1', '.hero-sub', '.faq-answer', '#horarios-pan-de-azucar', '.horarios-box']
    }
}

def apply_horarios(filepath, config):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 1. Inserir bloco de horários antes da seção de FAQ ou antes do footer
    # Procurar a seção de FAQ visível
    faq_section = None
    for tag in soup.find_all(['section', 'div']):
        if tag.get('id') in ['faq', 'perguntas', 'questions', 'preguntas']:
            faq_section = tag
            break
    
    # Se não encontrou por ID, procurar por conteúdo
    if not faq_section:
        for tag in soup.find_all(['h2', 'h3']):
            text = tag.get_text().lower()
            if any(kw in text for kw in ['perguntas', 'faq', 'questions', 'preguntas']):
                faq_section = tag.parent
                break
    
    # Inserir o bloco de horários
    block_soup = BeautifulSoup(config['block_html'], 'html.parser')
    
    if faq_section:
        faq_section.insert_before(block_soup)
        print(f"  + Bloco de horários inserido antes da seção FAQ")
    else:
        # Inserir antes do footer
        footer = soup.find('footer')
        if footer:
            footer.insert_before(block_soup)
            print(f"  + Bloco de horários inserido antes do footer")
    
    # 2. Atualizar OpeningHoursSpecification no JSON-LD do Restaurant
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            graph = data.get('@graph', [])
            for node in graph:
                if node.get('@type') in ['Restaurant', 'LocalBusiness'] or (
                    isinstance(node.get('@type'), list) and 'Restaurant' in node.get('@type', [])
                ):
                    node['openingHoursSpecification'] = config['opening_hours']
                    print(f"  + OpeningHoursSpecification adicionado ao nó {node.get('@type')}")
                    break
            script.string = json.dumps(data, ensure_ascii=False, indent=2)
        except Exception as e:
            pass
    
    # 3. Atualizar speakable cssSelector
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            graph = data.get('@graph', [])
            for node in graph:
                if node.get('@type') == 'WebPage':
                    if 'speakable' in node:
                        node['speakable']['cssSelector'] = config['speakable_selectors']
                        print(f"  + Speakable cssSelector atualizado com {len(config['speakable_selectors'])} seletores")
                    break
            script.string = json.dumps(data, ensure_ascii=False, indent=2)
        except Exception as e:
            pass
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"✓ {filepath} atualizado")

# Executar para as 3 versões
for filepath, config in CONFIGS.items():
    print(f"\nAplicando Ação 3 em {filepath}...")
    apply_horarios(filepath, config)

print("\n✅ Ação 3 concluída!")
