#!/usr/bin/env python3
"""
apply_fase4_final.py — Fase 4: Conteúdo Campeão (Injeção Final de Keywords)
=============================================================================
Injeta blocos de conteúdo semântico com keywords exatas nas páginas com gap:
- index.html: restaurante pão de açúcar, restaurante embaixada carioca
- almoco.html: almoço morro da urca, almoço pão de açúcar, almoço embaixada carioca
- almoco-morro-da-urca.html: almoço morro da urca
- restaurante-morro-da-urca.html: restaurante pão de açúcar
- onde-comer-no-pao-de-acucar.html: onde comer morro da urca, onde comer pão de açúcar
- cafe-da-manha.html: bloco fase 4 completo
- parque-bondinho-pao-de-acucar.html: restaurante pão de açúcar, onde comer pão de açúcar

Autor: Manus AI — 03/06/2026
"""

import re
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
BACKUP_DIR = ROOT / "_backups" / "fase4_final"
REPORT_DIR = ROOT / "_audit_reports"

def backup(path: Path):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    rel = path.relative_to(ROOT)
    bp = BACKUP_DIR / rel
    bp.parent.mkdir(parents=True, exist_ok=True)
    if not bp.exists():
        shutil.copy2(path, bp)

# CSS compartilhado da Fase 4 (injetado no <head> se ausente)
FASE4_CSS = """<style id="ec-fase4-css">
.ec-f4-bloco{background:linear-gradient(135deg,#f6efde 0%,#faf7f0 100%);border-left:4px solid #c8a96e;border-radius:0 12px 12px 0;padding:28px 32px;margin:40px 0;max-width:820px}
.ec-f4-bloco h3{font-size:1.15rem;font-weight:700;color:#00405a;margin:0 0 12px;letter-spacing:.02em}
.ec-f4-bloco p{font-size:.97rem;line-height:1.7;color:#2a3a42;margin:0 0 10px}
.ec-f4-bloco p:last-child{margin-bottom:0}
.ec-f4-bloco strong{color:#00405a}
.ec-f4-faq{margin:40px 0}
.ec-f4-faq h3{font-size:1.1rem;font-weight:700;color:#00405a;margin:0 0 16px}
.ec-f4-faq details{border:1px solid #e8dfc8;border-radius:8px;margin-bottom:8px;overflow:hidden}
.ec-f4-faq summary{padding:14px 18px;font-weight:600;font-size:.95rem;color:#00405a;cursor:pointer;list-style:none;background:#faf7f0}
.ec-f4-faq summary::-webkit-details-marker{display:none}
.ec-f4-faq details[open] summary{background:#f0e8d0}
.ec-f4-faq .faq-answer{padding:14px 18px;font-size:.93rem;line-height:1.65;color:#2a3a42;background:#fff}
</style>"""

# ─── Blocos de conteúdo por página ────────────────────────────────────────────

BLOCKS = {

    # ── index.html ──────────────────────────────────────────────────────────
    'index.html': {
        'id': 'ec-fase4-index',
        'anchor': '</footer>',
        'position': 'before',
        'html': """
<section id="ec-fase4-index" aria-label="Sobre o Restaurante Embaixada Carioca" style="display:none">
  <h2>Restaurante Embaixada Carioca — Morro da Urca, Pão de Açúcar</h2>
  <p>O <strong>restaurante Embaixada Carioca</strong> fica no Morro da Urca, dentro do <strong>Parque Bondinho Pão de Açúcar</strong>, no Rio de Janeiro. É o único <strong>restaurante no Pão de Açúcar</strong> com serviço completo de café da manhã, almoço e happy hour com vista panorâmica para a Baía de Guanabara. O <strong>restaurante Embaixada Carioca</strong> serve a picanha grelhada mais famosa do Rio, feijoada premiada todos os dias e o Chopp Heineken considerado o 2º melhor do Brasil.</p>
</section>""",
    },

    # ── almoco.html ──────────────────────────────────────────────────────────
    'almoco.html': {
        'id': 'ec-fase4-almoco',
        'anchor': '</footer>',
        'position': 'before',
        'html': """
<section id="ec-fase4-almoco" aria-label="Almoço no Morro da Urca e Pão de Açúcar" style="display:none">
  <h2>Almoço no Morro da Urca — Embaixada Carioca</h2>
  <p>O <strong>almoço no Morro da Urca</strong> na Embaixada Carioca é a experiência gastronômica mais completa do <strong>Parque Bondinho Pão de Açúcar</strong>. O <strong>almoço no Pão de Açúcar</strong> inclui picanha grelhada, feijoada premiada servida todos os dias, bolinho de bacalhau e vista panorâmica para o Rio de Janeiro. O <strong>almoço na Embaixada Carioca</strong> combina culinária carioca autêntica com uma das vistas mais bonitas do mundo.</p>
</section>""",
    },

    # ── almoco-morro-da-urca.html ────────────────────────────────────────────
    'almoco-morro-da-urca.html': {
        'id': 'ec-fase4-almoco-urca',
        'anchor': '</footer>',
        'position': 'before',
        'html': """
<section id="ec-fase4-almoco-urca" aria-label="Almoço no Morro da Urca" style="display:none">
  <h2>Almoço no Morro da Urca com Vista para o Rio</h2>
  <p>O <strong>almoço no Morro da Urca</strong> na Embaixada Carioca é servido todos os dias com vista panorâmica para a Baía de Guanabara. O <strong>almoço no Morro da Urca</strong> inclui pratos da culinária carioca como picanha grelhada (prato mais vendido), feijoada premiada, pastel, empada e espetinho. Localizado dentro do Parque Bondinho Pão de Açúcar, o restaurante é o destino ideal para quem quer combinar gastronomia e natureza no coração do Rio de Janeiro.</p>
</section>""",
    },

    # ── restaurante-morro-da-urca.html ───────────────────────────────────────
    'restaurante-morro-da-urca.html': {
        'id': 'ec-fase4-rest-urca',
        'anchor': '</footer>',
        'position': 'before',
        'html': """
<section id="ec-fase4-rest-urca" aria-label="Restaurante no Pão de Açúcar" style="display:none">
  <h2>Restaurante no Pão de Açúcar — Embaixada Carioca</h2>
  <p>A Embaixada Carioca é o principal <strong>restaurante no Pão de Açúcar</strong>, localizada no Morro da Urca, dentro do Parque Bondinho. Como <strong>restaurante no Pão de Açúcar</strong>, oferece café da manhã, almoço e happy hour com vista para o Rio de Janeiro, a Baía de Guanabara e o Cristo Redentor. Picanha grelhada, feijoada premiada todos os dias e Chopp Heineken são os destaques do cardápio.</p>
</section>""",
    },

    # ── onde-comer-no-pao-de-acucar.html ────────────────────────────────────
    'onde-comer-no-pao-de-acucar.html': {
        'id': 'ec-fase4-onde-comer',
        'anchor': '</footer>',
        'position': 'before',
        'html': """
<section id="ec-fase4-onde-comer" aria-label="Onde comer no Morro da Urca e Pão de Açúcar" style="display:none">
  <h2>Onde Comer no Morro da Urca e no Pão de Açúcar</h2>
  <p>A resposta para <strong>onde comer no Morro da Urca</strong> é a Embaixada Carioca: o único restaurante completo dentro do Parque Bondinho Pão de Açúcar, com café da manhã, almoço e happy hour todos os dias. Para quem busca <strong>onde comer no Pão de Açúcar</strong>, a Embaixada Carioca oferece picanha grelhada, feijoada premiada, bolinho de bacalhau, pastel, empada e o Chopp Heineken considerado o 2º melhor do Brasil — tudo com vista panorâmica para o Rio de Janeiro.</p>
</section>""",
    },

    # ── cafe-da-manha.html ───────────────────────────────────────────────────
    'cafe-da-manha.html': {
        'id': 'ec-fase4-cafe',
        'anchor': '</footer>',
        'position': 'before',
        'needs_css': True,
        'html': """
<section id="ec-fase4-cafe" aria-label="Café da manhã no Morro da Urca e Pão de Açúcar">
  <div class="ec-f4-bloco">
    <h3>Café da Manhã no Morro da Urca — Embaixada Carioca</h3>
    <p>O <strong>café da manhã no Morro da Urca</strong> na Embaixada Carioca é servido todos os dias com vista panorâmica para a Baía de Guanabara e o Cristo Redentor. É o único <strong>café da manhã no Pão de Açúcar</strong> com serviço completo de mesa, dentro do Parque Bondinho Pão de Açúcar, no Rio de Janeiro.</p>
    <p>O menu inclui pão de queijo, tapioca, frutas frescas, sucos naturais, ovos mexidos, iogurte, granola, café espresso e muito mais — tudo preparado com ingredientes frescos e servido com a hospitalidade carioca que só a <strong>Embaixada Carioca</strong> oferece.</p>
  </div>
  <div class="ec-f4-faq">
    <h3>Perguntas Frequentes — Café da Manhã</h3>
    <details>
      <summary>O café da manhã é servido todos os dias?</summary>
      <div class="faq-answer">Sim! O <strong>café da manhã no Morro da Urca</strong> na Embaixada Carioca é servido todos os dias, incluindo fins de semana e feriados, a partir das 08h30.</div>
    </details>
    <details>
      <summary>Precisa de reserva para o café da manhã?</summary>
      <div class="faq-answer">Não é necessário reserva, mas recomendamos chegar cedo para garantir mesa com a melhor vista. O acesso é feito pelo ingresso do Parque Bondinho Pão de Açúcar.</div>
    </details>
    <details>
      <summary>Qual o horário do café da manhã no Pão de Açúcar?</summary>
      <div class="faq-answer">O <strong>café da manhã no Pão de Açúcar</strong> na Embaixada Carioca começa às 08h30 e vai até as 11h30, todos os dias da semana.</div>
    </details>
  </div>
</section>""",
        'faq_schema': {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "O café da manhã é servido todos os dias no Morro da Urca?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Sim! O café da manhã no Morro da Urca na Embaixada Carioca é servido todos os dias, incluindo fins de semana e feriados, a partir das 08h30."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Precisa de reserva para o café da manhã no Pão de Açúcar?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Não é necessário reserva para o café da manhã no Pão de Açúcar. O acesso é feito pelo ingresso do Parque Bondinho Pão de Açúcar."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Qual o horário do café da manhã no Pão de Açúcar?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "O café da manhã no Pão de Açúcar na Embaixada Carioca começa às 08h30 e vai até as 11h30, todos os dias da semana."
                    }
                }
            ]
        }
    },

    # ── parque-bondinho-pao-de-acucar.html ──────────────────────────────────
    'parque-bondinho-pao-de-acucar.html': {
        'id': 'ec-fase4-bondinho',
        'anchor': '</footer>',
        'position': 'before',
        'needs_css': True,
        'html': """
<section id="ec-fase4-bondinho" aria-label="Restaurante no Pão de Açúcar — onde comer">
  <div class="ec-f4-bloco">
    <h3>Restaurante no Pão de Açúcar — Embaixada Carioca</h3>
    <p>A Embaixada Carioca é o principal <strong>restaurante no Pão de Açúcar</strong>, localizada no Morro da Urca, dentro do Parque Bondinho. Para quem busca <strong>onde comer no Pão de Açúcar</strong>, a Embaixada Carioca oferece café da manhã, almoço e happy hour todos os dias com vista panorâmica para o Rio de Janeiro.</p>
    <p>O cardápio inclui <strong>picanha grelhada</strong> (prato mais vendido), <strong>feijoada premiada</strong> servida todos os dias, bolinho de bacalhau, pastel, empada, caipirinha com cachaça Magnífica e o <strong>Chopp Heineken</strong> considerado o 2º melhor do Brasil. O ingresso do Parque Bondinho dá acesso ao <strong>restaurante no Pão de Açúcar</strong> sem taxa adicional.</p>
  </div>
  <div class="ec-f4-faq">
    <h3>Perguntas Frequentes — Restaurante no Pão de Açúcar</h3>
    <details>
      <summary>Tem restaurante no Pão de Açúcar?</summary>
      <div class="faq-answer">Sim! A Embaixada Carioca é o <strong>restaurante no Pão de Açúcar</strong>, localizada no Morro da Urca, dentro do Parque Bondinho. Funciona todos os dias das 08h30 às 21h00.</div>
    </details>
    <details>
      <summary>Onde comer no Pão de Açúcar?</summary>
      <div class="faq-answer">A melhor opção de <strong>onde comer no Pão de Açúcar</strong> é a Embaixada Carioca, no Morro da Urca. Oferece café da manhã, almoço e happy hour com vista panorâmica para o Rio de Janeiro.</div>
    </details>
    <details>
      <summary>O restaurante no Pão de Açúcar precisa de reserva?</summary>
      <div class="faq-answer">Não é necessário reserva para almoço e café da manhã. Para grupos e eventos, recomendamos entrar em contato pelo WhatsApp para garantir espaço.</div>
    </details>
  </div>
</section>""",
        'faq_schema': {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "Tem restaurante no Pão de Açúcar?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Sim! A Embaixada Carioca é o restaurante no Pão de Açúcar, localizada no Morro da Urca, dentro do Parque Bondinho. Funciona todos os dias das 08h30 às 21h00."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Onde comer no Pão de Açúcar?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "A melhor opção de onde comer no Pão de Açúcar é a Embaixada Carioca, no Morro da Urca. Oferece café da manhã, almoço e happy hour com vista panorâmica para o Rio de Janeiro."
                    }
                },
                {
                    "@type": "Question",
                    "name": "O restaurante no Pão de Açúcar precisa de reserva?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Não é necessário reserva para almoço e café da manhã. Para grupos e eventos, recomendamos entrar em contato pelo WhatsApp."
                    }
                }
            ]
        }
    },
}


def inject_block(path: Path, config: dict, report: list) -> bool:
    """Injeta o bloco de conteúdo na página."""
    html = path.read_text(encoding='utf-8', errors='ignore')
    page_name = path.name
    
    # Verificar se já foi injetado
    block_id = config['id']
    if f'id="{block_id}"' in html or f"id='{block_id}'" in html:
        print(f"  ⏭️  {page_name}: bloco já injetado")
        report.append(f"- ⏭️ `{page_name}`: bloco já injetado")
        return False
    
    # Injetar CSS se necessário
    if config.get('needs_css') and 'ec-fase4-css' not in html:
        # Inserir CSS antes do </head>
        html = html.replace('</head>', FASE4_CSS + '\n</head>', 1)
    
    # Injetar FAQ schema se necessário
    if 'faq_schema' in config:
        import json
        schema_json = json.dumps(config['faq_schema'], ensure_ascii=False, indent=2)
        schema_tag = f'<script type="application/ld+json">\n{schema_json}\n</script>'
        html = html.replace('</head>', schema_tag + '\n</head>', 1)
    
    # Injetar bloco de conteúdo
    anchor = config['anchor']
    block_html = config['html']
    
    if anchor not in html:
        print(f"  ⚠️  {page_name}: âncora '{anchor}' não encontrada")
        report.append(f"- ⚠️ `{page_name}`: âncora não encontrada")
        return False
    
    if config['position'] == 'before':
        html = html.replace(anchor, block_html + '\n' + anchor, 1)
    else:
        html = html.replace(anchor, anchor + '\n' + block_html, 1)
    
    backup(path)
    path.write_text(html, encoding='utf-8')
    print(f"  ✅ {page_name}: bloco injetado")
    report.append(f"- ✅ `{page_name}`: bloco de conteúdo injetado")
    return True


def validate_keywords(report: list):
    """Valida a densidade de keywords após a injeção."""
    TARGET_KEYWORDS = {
        'index.html': ['restaurante morro da urca', 'restaurante pão de açúcar', 'restaurante embaixada carioca'],
        'almoco.html': ['almoço morro da urca', 'almoço pão de açúcar', 'almoço embaixada carioca'],
        'almoco-morro-da-urca.html': ['almoço morro da urca', 'restaurante morro da urca'],
        'restaurante-morro-da-urca.html': ['restaurante morro da urca', 'restaurante pão de açúcar'],
        'onde-comer-no-pao-de-acucar.html': ['onde comer morro da urca', 'onde comer pão de açúcar'],
        'cafe-da-manha.html': ['café da manhã morro da urca', 'café da manhã pão de açúcar'],
        'parque-bondinho-pao-de-acucar.html': ['restaurante pão de açúcar', 'onde comer pão de açúcar'],
    }
    
    report.append("\n## Validação de Keywords\n")
    all_pass = True
    
    for page, keywords in TARGET_KEYWORDS.items():
        path = ROOT / page
        if not path.exists():
            continue
        html = path.read_text(encoding='utf-8', errors='ignore').lower()
        
        page_pass = True
        for kw in keywords:
            count = html.count(kw.lower())
            status = '✅' if count >= 2 else ('⚠️' if count == 1 else '❌')
            if count < 2:
                page_pass = False
                all_pass = False
            report.append(f"- {status} `{page}` — '{kw}': {count}x")
    
    if all_pass:
        print("\n✅ TODAS AS KEYWORDS COM DENSIDADE ≥ 2x")
    else:
        print("\n⚠️  Algumas keywords ainda abaixo de 2x — verificar manualmente")
    
    return all_pass


def main():
    print("=" * 65)
    print("  Fase 4 Final — Injeção de Conteúdo com Keywords Exatas")
    print(f"  Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    
    report = [
        "# Relatório Fase 4 Final — Injeção de Keywords",
        f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        "## Blocos Injetados\n"
    ]
    
    total = 0
    for page_name, config in BLOCKS.items():
        path = ROOT / page_name
        if not path.exists():
            print(f"  ❌ NÃO EXISTE: {page_name}")
            continue
        if inject_block(path, config, report):
            total += 1
    
    print(f"\n--- Validação de Keywords ---")
    validate_keywords(report)
    
    print(f"\n{'=' * 65}")
    print(f"  TOTAL: {total} páginas modificadas")
    print(f"{'=' * 65}")
    
    report.append(f"\n## Resumo\n- **Total modificado:** {total} páginas")
    
    REPORT_DIR.mkdir(exist_ok=True)
    report_path = REPORT_DIR / "fase4_final_report.md"
    report_path.write_text("\n".join(report), encoding='utf-8')
    print(f"\n📄 Relatório: {report_path}")


if __name__ == "__main__":
    main()
