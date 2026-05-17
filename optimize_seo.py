#!/usr/bin/env python3
"""
optimize_seo.py
Otimiza as páginas-chave para SEO (notas 95+) com base na análise de concorrência e cooperação.
"""
import os
import re

def optimize_index():
    path = 'index.html'
    if not os.path.exists(path): return
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Otimizar Título (era 107 chars, muito longo)
    # Antes: Embaixada Carioca | Restaurante no Morro da Urca — Restaurante do Bondinho Pão de Açúcar, Rio de Janeiro RJ
    # Depois: Restaurante no Morro da Urca | Embaixada Carioca (50 chars)
    content = re.sub(
        r'<title>.*?</title>',
        '<title>Restaurante no Morro da Urca | Embaixada Carioca</title>',
        content
    )
    
    # 2. Adicionar seção de diferenciais competitivos (vs Araá e Clássico)
    if '<!-- Diferenciais -->' not in content and '<section class="section-below-fold">' in content:
        diferenciais_html = """
<section class="section-below-fold" style="background: var(--areia-pale); padding: 80px 0;">
  <div class="wrap">
    <div class="sec-head" style="text-align: center; margin-bottom: 3rem;">
      <h2 style="font-family: var(--serif); font-size: clamp(2rem, 4vw, 2.8rem); color: var(--azul1); margin-bottom: 1rem;">Por que escolher a Embaixada Carioca?</h2>
      <p style="color: var(--cinza1); max-width: 700px; margin: 0 auto; font-size: 1.1rem;">O único restaurante completo dentro do Parque Bondinho Pão de Açúcar que oferece reservas, café da manhã diário e a feijoada mais premiada do Rio.</p>
    </div>
    
    <div class="grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px;">
      <div class="card" style="background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); text-align: center;">
        <div style="font-size: 2.5rem; margin-bottom: 15px;">🏆</div>
        <h3 style="color: var(--azul1); font-size: 1.3rem; margin-bottom: 10px;">Feijoada Premiada</h3>
        <p style="color: var(--cinza2); font-size: 0.95rem;">Eleita a melhor do Brasil pela Prazeres da Mesa. Servida todos os dias, não apenas aos finais de semana.</p>
      </div>
      
      <div class="card" style="background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); text-align: center;">
        <div style="font-size: 2.5rem; margin-bottom: 15px;">📅</div>
        <h3 style="color: var(--azul1); font-size: 1.3rem; margin-bottom: 10px;">Reservas Garantidas</h3>
        <p style="color: var(--cinza2); font-size: 0.95rem;">Diferente de outras opções no Pão de Açúcar, aceitamos reservas para garantir sua mesa com a melhor vista.</p>
      </div>
      
      <div class="card" style="background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); text-align: center;">
        <div style="font-size: 2.5rem; margin-bottom: 15px;">☕</div>
        <h3 style="color: var(--azul1); font-size: 1.3rem; margin-bottom: 10px;">Café da Manhã Diário</h3>
        <p style="color: var(--cinza2); font-size: 0.95rem;">O único café da manhã com vista panorâmica servido todos os dias da semana no Morro da Urca.</p>
      </div>
    </div>
  </div>
</section>
<!-- Diferenciais -->
"""
        content = content.replace('<section class="section-below-fold">', diferenciais_html + '\n<section class="section-below-fold">', 1)
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {path} otimizado")

def optimize_parque_bondinho():
    path = 'parque-bondinho.html'
    if not os.path.exists(path): return
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Adicionar conteúdo sobre o ecossistema gastronômico (cooperação/concorrência)
    if 'Onde comer no Parque Bondinho' not in content:
        gastronomia_html = """
<h2 style="font-family: var(--serif); font-size: 2.2rem; color: var(--azul1); margin-top: 3rem; margin-bottom: 1.5rem;">Onde comer no Parque Bondinho Pão de Açúcar?</h2>
<p style="margin-bottom: 1.5rem; line-height: 1.8; color: var(--cinza1);">O complexo turístico oferece diversas opções gastronômicas. A <strong>Embaixada Carioca</strong> destaca-se como o restaurante mais completo do Morro da Urca, oferecendo desde café da manhã até jantar, com a vantagem exclusiva de aceitar reservas.</p>

<p style="margin-bottom: 1.5rem; line-height: 1.8; color: var(--cinza1);">Recentemente, o parque ganhou novas opções como o restaurante Araá, focado em ingredientes nativos, ampliando o polo gastronômico local. No Pão de Açúcar (segundo morro), encontra-se o Clássico Sunset Club, que opera por ordem de chegada (sem reservas). Para quem busca lanches rápidos, o complexo conta com parceiros como Brewteco, Bonde Bar Heineken e diversas lanchonetes.</p>

<p style="margin-bottom: 1.5rem; line-height: 1.8; color: var(--cinza1);"><strong>Dica de ouro:</strong> Se você planeja almoçar ou jantar com vista, <a href="/almoco.html" style="color: var(--amarelo-deep); font-weight: 600;">reservar sua mesa na Embaixada Carioca</a> garante seu lugar sem filas, permitindo que você aproveite o passeio de bondinho com total tranquilidade.</p>
"""
        # Inserir antes do FAQ
        content = content.replace('<h2 style="font-family: var(--serif);', gastronomia_html + '\n<h2 style="font-family: var(--serif);', 1)
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {path} otimizado")

def optimize_almoco():
    path = 'almoco.html'
    if not os.path.exists(path): return
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Adicionar conteúdo sobre o processo decisório do cliente
    if 'roteiro perfeito' not in content.lower():
        roteiro_html = """
<div style="background: rgba(0,64,90,0.03); padding: 40px; border-radius: 12px; margin: 3rem 0; border-left: 4px solid var(--amarelo);">
  <h3 style="font-family: var(--serif); font-size: 1.8rem; color: var(--azul1); margin-bottom: 1rem;">O roteiro perfeito: Bondinho + Almoço</h3>
  <p style="margin-bottom: 1rem; line-height: 1.7; color: var(--cinza1);">Para otimizar seu tempo e orçamento no Rio de Janeiro, recomendamos combinar a visita ao Parque Bondinho com seu almoço. Ao invés de procurar restaurantes na Urca após descer, almoçar no Morro da Urca transforma uma simples refeição em uma experiência panorâmica inesquecível.</p>
  <p style="margin-bottom: 0; line-height: 1.7; color: var(--cinza1);">Nossa <strong>picanha grelhada</strong> (prato mais vendido) e o <strong>Chopp Heineken</strong> (eleito o melhor da cidade) são as escolhas favoritas de quem busca a autêntica alma carioca após o passeio de teleférico.</p>
</div>
"""
        # Inserir após o primeiro parágrafo longo
        content = re.sub(r'(<p[^>]*>.*?</p>\s*<p[^>]*>.*?</p>)', r'\1\n' + roteiro_html, content, count=1)
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {path} otimizado")

# Executar otimizações
optimize_index()
optimize_parque_bondinho()
optimize_almoco()
print("Otimizações de conteúdo concluídas.")
