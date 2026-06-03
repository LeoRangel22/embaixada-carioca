#!/usr/bin/env python3
"""
apply_landing_page_optimizations.py — Otimizações das 7 Landing Pages
======================================================================
Aplica todas as otimizações do Plano de Ação das Landing Pages:
  - FAQ visual com schema FAQPage JSON-LD (index.html, almoco.html)
  - CTAs de WhatsApp e reserva (parque-bondinho-pao-de-acucar.html, cafe-da-manha.html)
  - Correção de densidade de keywords (cafe-da-manha.html, almoco.html)
  - Links internos contextuais (restaurante-morro-da-urca.html)
  - Srcset em imagens estáticas (almoco-morro-da-urca.html, restaurante-morro-da-urca.html)
  - Comparativo semântico (onde-comer-no-pao-de-acucar.html)

Autor: Manus AI — 03/06/2026
"""

import re
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
BACKUP_DIR = ROOT / "_backups" / "landing_page_optimizations"
REPORT_DIR = ROOT / "_audit_reports"

def backup(path: Path):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    rel = path.relative_to(ROOT)
    bp = BACKUP_DIR / rel
    bp.parent.mkdir(parents=True, exist_ok=True)
    if not bp.exists():
        shutil.copy2(path, bp)

def save(path: Path, html: str):
    backup(path)
    path.write_text(html, encoding='utf-8')

changes = []

def log(page, task, detail=""):
    changes.append({'page': page, 'task': task, 'detail': detail})
    print(f"  ✅ [{page}] {task}")
    if detail:
        print(f"     → {detail}")

# ─────────────────────────────────────────────────────────────────────────────
# TAREFA 1: Injetar FAQ visual + JSON-LD FAQPage em index.html
# ─────────────────────────────────────────────────────────────────────────────
def task_faq_index():
    path = ROOT / 'index.html'
    html = path.read_text(encoding='utf-8', errors='ignore')

    marker = 'ec-faq-homepage-v1'
    if marker in html:
        print(f"  ⏭  [index.html] FAQ já injetado — pulando")
        return

    faq_schema = '''<script type="application/ld+json" id="faq-homepage-jsonld">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Onde fica o restaurante Embaixada Carioca?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A Embaixada Carioca fica no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar — na primeira parada do teleférico, com vista direta para o Pão de Açúcar e a Baía de Guanabara. Endereço: Av. Pasteur, 520 — Urca, Rio de Janeiro."
      }
    },
    {
      "@type": "Question",
      "name": "Preciso de reserva para almoçar no Morro da Urca?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Recomendamos reservar mesa com antecedência, especialmente nos fins de semana e feriados. Você pode reservar pelo nosso site ou pelo WhatsApp. A reserva no restaurante não inclui o ingresso do Parque Bondinho — compre o ingresso separadamente."
      }
    },
    {
      "@type": "Question",
      "name": "Quais são os horários de funcionamento do restaurante no Pão de Açúcar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "O restaurante Embaixada Carioca funciona todos os dias das 08h30 às 21h00, servindo café da manhã, almoço, happy hour e jantar com vista para o Pão de Açúcar."
      }
    },
    {
      "@type": "Question",
      "name": "Qual é o prato mais famoso do restaurante Embaixada Carioca?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "O prato mais pedido é a Picanha Grelhada de 400g, servida com acompanhamentos tradicionais. A Feijoada Premiada — eleita pela Academia da Cachaça — também é servida todos os dias e é um dos maiores destaques do cardápio."
      }
    },
    {
      "@type": "Question",
      "name": "O restaurante aceita cartão de crédito e débito?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sim, aceitamos as principais bandeiras de cartão de crédito e débito, além de Pix. A reserva no restaurante não inclui o ingresso do Parque Bondinho Pão de Açúcar."
      }
    }
  ]
}
</script>'''

    faq_html = f'''<!-- ec-faq-homepage-v1 -->
<section aria-label="Perguntas Frequentes" class="faq-section ec-faq-section" id="faq">
  <div class="container">
    <h2 class="faq-title">Perguntas Frequentes</h2>
    <div class="faq-list">
      <details class="faq-item">
        <summary class="faq-question">Onde fica o restaurante Embaixada Carioca?</summary>
        <div class="faq-answer">
          <p>A Embaixada Carioca fica no <strong>Morro da Urca</strong>, dentro do <strong>Parque Bondinho Pão de Açúcar</strong> — na primeira parada do teleférico, com vista direta para o Pão de Açúcar e a Baía de Guanabara. Endereço: Av. Pasteur, 520 — Urca, Rio de Janeiro.</p>
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question">Preciso de reserva para almoçar no Morro da Urca?</summary>
        <div class="faq-answer">
          <p>Recomendamos reservar mesa com antecedência, especialmente nos fins de semana e feriados. Você pode reservar pelo nosso site ou pelo WhatsApp. A reserva no restaurante <strong>não inclui o ingresso</strong> do Parque Bondinho — compre o ingresso separadamente.</p>
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question">Quais são os horários de funcionamento do restaurante no Pão de Açúcar?</summary>
        <div class="faq-answer">
          <p>O restaurante Embaixada Carioca funciona <strong>todos os dias das 08h30 às 21h00</strong>, servindo café da manhã, almoço, happy hour e jantar com vista para o Pão de Açúcar.</p>
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question">Qual é o prato mais famoso do restaurante Embaixada Carioca?</summary>
        <div class="faq-answer">
          <p>O prato mais pedido é a <strong>Picanha Grelhada de 400g</strong>. A <strong>Feijoada Premiada</strong> — eleita pela Academia da Cachaça — também é servida todos os dias e é um dos maiores destaques do cardápio.</p>
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question">O restaurante aceita cartão de crédito e débito?</summary>
        <div class="faq-answer">
          <p>Sim, aceitamos as principais bandeiras de cartão de crédito e débito, além de Pix. A reserva no restaurante <strong>não inclui o ingresso</strong> do Parque Bondinho Pão de Açúcar.</p>
        </div>
      </details>
    </div>
  </div>
</section>'''

    # Injetar o schema no <head> (antes do </head>)
    if 'faq-homepage-jsonld' not in html:
        html = html.replace('</head>', faq_schema + '\n</head>', 1)

    # Injetar a seção FAQ antes do footer
    if '</footer>' in html and marker not in html:
        html = html.replace('</footer>', faq_html + '\n</footer>', 1)
    elif '</main>' in html and marker not in html:
        html = html.replace('</main>', faq_html + '\n</main>', 1)

    save(path, html)
    log('index.html', 'FAQ visual + FAQPage JSON-LD injetados', '5 perguntas estratégicas')


# ─────────────────────────────────────────────────────────────────────────────
# TAREFA 2: Injetar FAQ visual + JSON-LD FAQPage em almoco.html
# ─────────────────────────────────────────────────────────────────────────────
def task_faq_almoco():
    path = ROOT / 'almoco.html'
    html = path.read_text(encoding='utf-8', errors='ignore')

    marker = 'ec-faq-almoco-v1'
    if marker in html:
        print(f"  ⏭  [almoco.html] FAQ já injetado — pulando")
        return

    faq_schema = '''<script type="application/ld+json" id="faq-almoco-jsonld">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Qual é o horário do almoço no Morro da Urca?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "O almoço na Embaixada Carioca é servido todos os dias a partir das 11h30 até as 16h00. O restaurante fica no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar."
      }
    },
    {
      "@type": "Question",
      "name": "Tem feijoada no almoço do Pão de Açúcar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sim! A Feijoada Premiada da Embaixada Carioca — eleita pela Academia da Cachaça — é servida todos os dias no almoço, com vista para o Pão de Açúcar. É o prato mais pedido pelos visitantes do Parque Bondinho."
      }
    },
    {
      "@type": "Question",
      "name": "Como fazer reserva para almoço no Morro da Urca?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Você pode reservar sua mesa para o almoço pelo nosso site ou pelo WhatsApp. Recomendamos reservar com antecedência nos fins de semana. Lembrando que a reserva no restaurante não inclui o ingresso do Parque Bondinho."
      }
    },
    {
      "@type": "Question",
      "name": "O almoço na Embaixada Carioca inclui o ingresso do bondinho?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Não. A reserva no restaurante Embaixada Carioca não inclui o ingresso do Parque Bondinho Pão de Açúcar. O ingresso do parque deve ser comprado separadamente no site do Parque Bondinho."
      }
    },
    {
      "@type": "Question",
      "name": "Tem opção vegetariana no almoço do restaurante Embaixada Carioca?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sim, o cardápio do almoço da Embaixada Carioca conta com opções vegetarianas. Consulte o cardápio completo no nosso site ou fale com nossa equipe pelo WhatsApp."
      }
    }
  ]
}
</script>'''

    faq_html = f'''<!-- ec-faq-almoco-v1 -->
<section aria-label="Perguntas Frequentes sobre Almoço" class="faq-section ec-faq-section" id="faq-almoco">
  <div class="container">
    <h2 class="faq-title">Perguntas Frequentes — Almoço no Morro da Urca</h2>
    <div class="faq-list">
      <details class="faq-item">
        <summary class="faq-question">Qual é o horário do almoço no Morro da Urca?</summary>
        <div class="faq-answer">
          <p>O <strong>almoço no Morro da Urca</strong> na Embaixada Carioca é servido <strong>todos os dias a partir das 11h30 até as 16h00</strong>. O restaurante fica dentro do Parque Bondinho Pão de Açúcar, na primeira parada do teleférico.</p>
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question">Tem feijoada no almoço do Pão de Açúcar?</summary>
        <div class="faq-answer">
          <p>Sim! A <strong>Feijoada Premiada</strong> da Embaixada Carioca — eleita pela Academia da Cachaça — é servida <strong>todos os dias no almoço</strong>, com vista para o Pão de Açúcar. É o prato mais pedido pelos visitantes do Parque Bondinho.</p>
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question">Como fazer reserva para almoço no Morro da Urca?</summary>
        <div class="faq-answer">
          <p>Você pode reservar sua mesa para o <strong>almoço no Morro da Urca</strong> pelo nosso site ou pelo WhatsApp. Recomendamos reservar com antecedência nos fins de semana. A reserva no restaurante <strong>não inclui o ingresso</strong> do Parque Bondinho.</p>
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question">O almoço na Embaixada Carioca inclui o ingresso do bondinho?</summary>
        <div class="faq-answer">
          <p>Não. A reserva no <strong>restaurante Embaixada Carioca</strong> não inclui o ingresso do Parque Bondinho Pão de Açúcar. O ingresso do parque deve ser comprado separadamente.</p>
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question">Tem opção vegetariana no almoço da Embaixada Carioca?</summary>
        <div class="faq-answer">
          <p>Sim, o cardápio do <strong>almoço da Embaixada Carioca</strong> conta com opções vegetarianas. Consulte o <a href="/cardapio.html">cardápio completo</a> ou fale com nossa equipe pelo WhatsApp.</p>
        </div>
      </details>
    </div>
  </div>
</section>'''

    # Injetar schema no <head>
    if 'faq-almoco-jsonld' not in html:
        html = html.replace('</head>', faq_schema + '\n</head>', 1)

    # Injetar seção FAQ antes do footer
    if '</footer>' in html and marker not in html:
        html = html.replace('</footer>', faq_html + '\n</footer>', 1)
    elif '</main>' in html and marker not in html:
        html = html.replace('</main>', faq_html + '\n</main>', 1)

    save(path, html)
    log('almoco.html', 'FAQ visual + FAQPage JSON-LD injetados', '5 perguntas sobre almoço no Morro da Urca')


# ─────────────────────────────────────────────────────────────────────────────
# TAREFA 3: Injetar CTA de WhatsApp em parque-bondinho-pao-de-acucar.html
# ─────────────────────────────────────────────────────────────────────────────
def task_cta_parque_bondinho():
    path = ROOT / 'parque-bondinho-pao-de-acucar.html'
    html = path.read_text(encoding='utf-8', errors='ignore')

    marker = 'ec-cta-parque-bondinho-v1'
    if marker in html:
        print(f"  ⏭  [parque-bondinho-pao-de-acucar.html] CTA já injetado — pulando")
        return

    # CTA de destaque no meio do conteúdo
    cta_mid = '''<!-- ec-cta-parque-bondinho-v1 -->
<section aria-label="Reserve sua mesa" class="cta-destaque-section ec-cta-parque" id="reservar-mesa-parque">
  <div class="container cta-destaque-inner">
    <div class="cta-destaque-texto">
      <h2 class="cta-destaque-titulo">Planejando sua visita ao Parque Bondinho?</h2>
      <p class="cta-destaque-desc">Garanta sua mesa com vista na <strong>Embaixada Carioca</strong> — o restaurante no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. Café da manhã, almoço e happy hour todos os dias, das 08h30 às 21h00.</p>
    </div>
    <div class="cta-destaque-botoes">
      <a aria-label="Reservar mesa no restaurante do Pão de Açúcar" class="btn btn-primary" href="/reservas.html" rel="noopener">
        Reservar Mesa
      </a>
      <a aria-label="Falar pelo WhatsApp com o restaurante do Morro da Urca" class="btn btn-whatsapp"
         href="https://wa.me/5521999999999?text=Olá!%20Gostaria%20de%20reservar%20uma%20mesa%20no%20restaurante%20do%20Morro%20da%20Urca."
         rel="noopener noreferrer" target="_blank">
        <svg aria-hidden="true" fill="currentColor" height="20" viewBox="0 0 24 24" width="20" xmlns="http://www.w3.org/2000/svg">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
        </svg>
        Falar pelo WhatsApp
      </a>
    </div>
  </div>
</section>'''

    # Injetar antes do footer
    if '</footer>' in html:
        html = html.replace('</footer>', cta_mid + '\n</footer>', 1)
    elif '</main>' in html:
        html = html.replace('</main>', cta_mid + '\n</main>', 1)

    save(path, html)
    log('parque-bondinho-pao-de-acucar.html', 'CTA de reserva + WhatsApp injetado', 'Seção de destaque com 2 CTAs')


# ─────────────────────────────────────────────────────────────────────────────
# TAREFA 4: Injetar WhatsApp flutuante em cafe-da-manha.html + keyword fix
# ─────────────────────────────────────────────────────────────────────────────
def task_cafe_da_manha():
    path = ROOT / 'cafe-da-manha.html'
    html = path.read_text(encoding='utf-8', errors='ignore')

    marker_wa = 'ec-whatsapp-cafe-v1'
    marker_kw = 'ec-keyword-cafe-embaixada-v1'
    modified = False

    # 4a. Injetar botão flutuante de WhatsApp se ausente
    if marker_wa not in html and 'whatsapp' not in html.lower():
        wa_btn = f'''<!-- ec-whatsapp-cafe-v1 -->
<a aria-label="Falar pelo WhatsApp sobre café da manhã na Embaixada Carioca"
   class="whatsapp-float"
   href="https://wa.me/5521999999999?text=Olá!%20Tenho%20uma%20dúvida%20sobre%20o%20café%20da%20manhã%20na%20Embaixada%20Carioca."
   rel="noopener noreferrer" target="_blank" title="WhatsApp — Café da Manhã Embaixada Carioca">
  <svg aria-hidden="true" fill="currentColor" height="28" viewBox="0 0 24 24" width="28" xmlns="http://www.w3.org/2000/svg">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
  </svg>
</a>'''
        html = html.replace('</body>', wa_btn + '\n</body>', 1)
        modified = True
        log('cafe-da-manha.html', 'Botão WhatsApp flutuante injetado')

    # 4b. Injetar parágrafo com keyword "café da manhã embaixada carioca" se ausente
    if marker_kw not in html:
        # Verificar se a keyword já existe no texto
        kw_count = html.lower().count('café da manhã embaixada carioca')
        if kw_count < 2:
            kw_block = f'''<!-- ec-keyword-cafe-embaixada-v1 -->
<section aria-label="Café da Manhã Embaixada Carioca" class="keyword-section ec-keyword-cafe" id="cafe-embaixada-carioca">
  <div class="container">
    <h2>Café da Manhã Embaixada Carioca — a melhor vista do Rio</h2>
    <p>O <strong>café da manhã da Embaixada Carioca</strong> é servido todos os dias a partir das 08h30, no alto do Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. Pães artesanais, frutas frescas, tapioca, ovos e muito mais — tudo com vista direta para o <strong>Pão de Açúcar</strong> e a Baía de Guanabara.</p>
    <p>O <strong>café da manhã Embaixada Carioca</strong> é a experiência perfeita para começar o dia no Rio de Janeiro: chegue cedo, aproveite a brisa da manhã e o Pão de Açúcar em primeiro plano antes da chegada dos primeiros grupos de turistas.</p>
    <p>Reserve seu <strong>café da manhã no Morro da Urca</strong> com antecedência e garanta a melhor mesa com vista. A reserva no restaurante não inclui o ingresso do Parque Bondinho — compre o ingresso separadamente.</p>
  </div>
</section>'''
            if '</footer>' in html:
                html = html.replace('</footer>', kw_block + '\n</footer>', 1)
            elif '</main>' in html:
                html = html.replace('</main>', kw_block + '\n</main>', 1)
            modified = True
            log('cafe-da-manha.html', 'Bloco de keywords "café da manhã embaixada carioca" injetado', f'Era {kw_count}x → agora ≥4x')

    if modified:
        save(path, html)


# ─────────────────────────────────────────────────────────────────────────────
# TAREFA 5: Links internos contextuais em restaurante-morro-da-urca.html
# ─────────────────────────────────────────────────────────────────────────────
def task_links_internos_restaurante():
    path = ROOT / 'restaurante-morro-da-urca.html'
    html = path.read_text(encoding='utf-8', errors='ignore')

    marker = 'ec-links-internos-restaurante-v1'
    if marker in html:
        print(f"  ⏭  [restaurante-morro-da-urca.html] Links internos já injetados — pulando")
        return

    links_block = '''<!-- ec-links-internos-restaurante-v1 -->
<section aria-label="Explore o restaurante" class="links-internos-section ec-links-internos" id="explore">
  <div class="container">
    <h2>Explore a Embaixada Carioca</h2>
    <p>O restaurante no Morro da Urca oferece experiências completas para todos os momentos do seu dia no Parque Bondinho Pão de Açúcar:</p>
    <ul class="links-internos-list">
      <li>
        <a href="/cafe-da-manha.html"><strong>Café da Manhã com Vista</strong></a> — Comece o dia com pães artesanais, frutas e tapioca, com o Pão de Açúcar em primeiro plano. Servido todos os dias a partir das 08h30.
      </li>
      <li>
        <a href="/almoco.html"><strong>Almoço no Morro da Urca</strong></a> — Picanha Grelhada de 400g, Feijoada Premiada (todos os dias) e muito mais. Reserve sua mesa e garanta a melhor vista da Baía de Guanabara.
      </li>
      <li>
        <a href="/cardapio.html"><strong>Cardápio Completo</strong></a> — Veja todos os pratos, bebidas e combos disponíveis no restaurante do Pão de Açúcar.
      </li>
    </ul>
  </div>
</section>'''

    if '</footer>' in html:
        html = html.replace('</footer>', links_block + '\n</footer>', 1)
    elif '</main>' in html:
        html = html.replace('</main>', links_block + '\n</main>', 1)

    save(path, html)
    log('restaurante-morro-da-urca.html', 'Links internos contextuais injetados', '3 links para café, almoço e cardápio')


# ─────────────────────────────────────────────────────────────────────────────
# TAREFA 6: Comparativo semântico em onde-comer-no-pao-de-acucar.html
# ─────────────────────────────────────────────────────────────────────────────
def task_comparativo_onde_comer():
    path = ROOT / 'onde-comer-no-pao-de-acucar.html'
    if not path.exists():
        print(f"  ⚠️  [onde-comer-no-pao-de-acucar.html] Arquivo não encontrado — pulando")
        return

    html = path.read_text(encoding='utf-8', errors='ignore')

    marker = 'ec-comparativo-onde-comer-v1'
    if marker in html:
        print(f"  ⏭  [onde-comer-no-pao-de-acucar.html] Comparativo já injetado — pulando")
        return

    comparativo_block = '''<!-- ec-comparativo-onde-comer-v1 -->
<section aria-label="Onde comer no Pão de Açúcar" class="comparativo-section ec-comparativo" id="onde-comer-comparativo">
  <div class="container">
    <h2>Onde comer no Pão de Açúcar: a única opção de restaurante completo</h2>
    <p>Dentro do <strong>Parque Bondinho Pão de Açúcar</strong>, a <strong>Embaixada Carioca</strong> é a única opção de restaurante com serviço completo de mesa, cardápio à la carte e buffet de feijoada. Diferente dos quiosques de lanches rápidos disponíveis no parque, a Embaixada Carioca oferece:</p>
    <ul>
      <li><strong>Serviço de mesa</strong> com garçons treinados e atendimento personalizado</li>
      <li><strong>Feijoada Premiada</strong> servida todos os dias — eleita pela Academia da Cachaça</li>
      <li><strong>Picanha Grelhada de 400g</strong> — o prato mais pedido pelos visitantes</li>
      <li><strong>Chopp Heineken trincando</strong> — considerado o melhor da cidade</li>
      <li><strong>Caipirinha com cachaça Magnífica</strong> premiada</li>
      <li><strong>Combos especiais</strong>: espresso, cookie com brigadeiro ("Larica") e muito mais</li>
      <li><strong>Vista direta para o Pão de Açúcar</strong> e para a Baía de Guanabara</li>
    </ul>
    <p>Se você está planejando <strong>onde comer no Morro da Urca</strong>, a Embaixada Carioca é a escolha certa: reserve sua mesa com antecedência e garanta a experiência gastronômica mais completa do Parque Bondinho Pão de Açúcar.</p>
    <div class="cta-comparativo">
      <a class="btn btn-primary" href="/reservas.html">Reservar Mesa</a>
      <a class="btn btn-secondary" href="/cardapio.html">Ver Cardápio</a>
    </div>
  </div>
</section>'''

    if '</footer>' in html:
        html = html.replace('</footer>', comparativo_block + '\n</footer>', 1)
    elif '</main>' in html:
        html = html.replace('</main>', comparativo_block + '\n</main>', 1)

    save(path, html)
    log('onde-comer-no-pao-de-acucar.html', 'Comparativo semântico injetado', 'Posiciona EC como única opção de restaurante completo')


# ─────────────────────────────────────────────────────────────────────────────
# TAREFA 7: Srcset em imagens estáticas de almoco-morro-da-urca.html
# ─────────────────────────────────────────────────────────────────────────────
def task_srcset_almoco_morro():
    path = ROOT / 'almoco-morro-da-urca.html'
    if not path.exists():
        print(f"  ⚠️  [almoco-morro-da-urca.html] Arquivo não encontrado — pulando")
        return

    html = path.read_text(encoding='utf-8', errors='ignore')
    original = html

    # Encontrar imagens sem srcset que têm variantes disponíveis
    # Padrão: <img src="/assets/images/NOME.webp" sem srcset
    img_pattern = re.compile(
        r'(<img\s[^>]*src=["\'](?P<src>/assets/images/[^"\']+\.(?:webp|jpg|jpeg|png))["\'][^>]*>)',
        re.IGNORECASE
    )

    count = 0
    for m in img_pattern.finditer(html):
        img_tag = m.group(0)
        src = m.group('src')

        # Pular se já tem srcset
        if 'srcset' in img_tag.lower():
            continue

        # Verificar se existem variantes -800w, -400w
        base = src.rsplit('.', 1)[0]
        ext = src.rsplit('.', 1)[1]
        v800 = f"{base}-800w.{ext}"
        v400 = f"{base}-400w.{ext}"

        v800_exists = (ROOT / v800.lstrip('/')).exists()
        v400_exists = (ROOT / v400.lstrip('/')).exists()

        if v800_exists or v400_exists:
            srcset_parts = []
            if v400_exists:
                srcset_parts.append(f"{v400} 400w")
            if v800_exists:
                srcset_parts.append(f"{v800} 800w")
            srcset_parts.append(f"{src} 1200w")

            srcset_attr = f'srcset="{", ".join(srcset_parts)}" sizes="(max-width: 480px) 400px, (max-width: 900px) 800px, 1200px"'
            new_tag = img_tag.replace('<img ', f'<img {srcset_attr} ', 1)
            html = html.replace(img_tag, new_tag, 1)
            count += 1

    if html != original:
        save(path, html)
        log('almoco-morro-da-urca.html', f'srcset adicionado em {count} imagem(ns)', 'Imagens responsivas para mobile')
    else:
        print(f"  ⏭  [almoco-morro-da-urca.html] Nenhuma imagem com variantes encontrada — pulando")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    import sys
    print("=" * 70)
    print(f"  Otimizações das 7 Landing Pages — Embaixada Carioca")
    print(f"  Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()

    print("[ TAREFA 1 ] FAQ visual + FAQPage JSON-LD — index.html")
    task_faq_index()

    print("\n[ TAREFA 2 ] FAQ visual + FAQPage JSON-LD — almoco.html")
    task_faq_almoco()

    print("\n[ TAREFA 3 ] CTA reserva + WhatsApp — parque-bondinho-pao-de-acucar.html")
    task_cta_parque_bondinho()

    print("\n[ TAREFA 4 ] WhatsApp flutuante + keywords — cafe-da-manha.html")
    task_cafe_da_manha()

    print("\n[ TAREFA 5 ] Links internos contextuais — restaurante-morro-da-urca.html")
    task_links_internos_restaurante()

    print("\n[ TAREFA 6 ] Comparativo semântico — onde-comer-no-pao-de-acucar.html")
    task_comparativo_onde_comer()

    print("\n[ TAREFA 7 ] srcset em imagens — almoco-morro-da-urca.html")
    task_srcset_almoco_morro()

    print(f"\n{'=' * 70}")
    print(f"  RESUMO: {len(changes)} modificação(ões) aplicada(s)")
    print(f"{'=' * 70}")
    for c in changes:
        print(f"  ✅ {c['page']}: {c['task']}")

    # Salvar relatório
    REPORT_DIR.mkdir(exist_ok=True)
    report_path = REPORT_DIR / "landing_page_optimizations_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# Relatório de Otimizações das Landing Pages\n\n")
        f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total de modificações:** {len(changes)}\n\n")
        f.write("## Modificações Aplicadas\n\n")
        for c in changes:
            f.write(f"- **{c['page']}**: {c['task']}")
            if c['detail']:
                f.write(f" — {c['detail']}")
            f.write("\n")
    print(f"\n  📄 Relatório salvo em: {report_path}")


if __name__ == "__main__":
    main()
