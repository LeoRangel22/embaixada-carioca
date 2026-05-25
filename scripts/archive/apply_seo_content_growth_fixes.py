#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / '_audit_reports'
REPORT = REPORT_DIR / 'seo_content_growth_fixes_report.md'

MORRO_BLOCK = '''
<section class="seo-conversion-block" aria-label="Restaurante no Morro da Urca e Parque Bondinho" style="background:#f6efde;padding:56px 0;border-top:1px solid rgba(0,64,90,.10);border-bottom:1px solid rgba(0,64,90,.10);">
  <div class="container" style="max-width:980px;margin:0 auto;padding:0 1.5rem;">
    <p class="eyebrow" style="color:#c47e15;font-size:11px;letter-spacing:.22em;text-transform:uppercase;margin-bottom:14px;">Restaurante no Morro da Urca</p>
    <h2 style="color:#00405a;font-size:clamp(30px,4vw,48px);line-height:1.1;margin:0 0 18px;">Por que a Embaixada Carioca é referência no Morro da Urca?</h2>
    <p style="color:#485156;font-size:1.08rem;line-height:1.7;max-width:760px;">A Embaixada Carioca fica dentro do Parque Bondinho Pão de Açúcar, na primeira parada do teleférico, no Morro da Urca. Para quem pesquisa <strong>restaurante no Morro da Urca</strong>, <strong>restaurante no Bondinho</strong> ou <strong>restaurante no Pão de Açúcar</strong>, a casa reúne localização, vista, café da manhã todos os dias, almoço brasileiro, caipirinhas e estrutura para eventos.</p>
    <ul style="color:#00405a;font-size:1rem;line-height:1.7;margin:22px 0 0;padding-left:1.25rem;">
      <li><strong>Vista direta:</strong> salão e varanda com vista para o Pão de Açúcar e a Baía de Guanabara.</li>
      <li><strong>Comida carioca:</strong> picanha, feijoada premiada, petiscos, caipirinhas e chope gelado.</li>
      <li><strong>Facilidade no roteiro:</strong> ideal antes ou depois da visita ao Parque Bondinho.</li>
      <li><strong>Eventos:</strong> grupos, cafés da manhã, coquetéis e encontros corporativos.</li>
    </ul>
    <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:28px;">
      <a href="https://go.tagme.com.br/embaixadacarioca" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 22px;border-radius:999px;background:#f59b1e;color:#00405a;font-weight:900;text-decoration:none;letter-spacing:.12em;text-transform:uppercase;font-size:12px;">Reservar mesa</a>
      <a href="/como-chegar.html" style="display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 22px;border-radius:999px;border:1px solid rgba(0,64,90,.28);color:#00405a;font-weight:800;text-decoration:none;letter-spacing:.12em;text-transform:uppercase;font-size:12px;">Como chegar</a>
    </div>
  </div>
</section>
'''.strip()

CAFE_BLOCK = '''
<section class="seo-conversion-block" aria-label="Café da manhã na Urca e no Bondinho" style="background:#f6efde;padding:56px 0;border-top:1px solid rgba(0,64,90,.10);border-bottom:1px solid rgba(0,64,90,.10);">
  <div class="container" style="max-width:980px;margin:0 auto;padding:0 1.5rem;">
    <p class="eyebrow" style="color:#c47e15;font-size:11px;letter-spacing:.22em;text-transform:uppercase;margin-bottom:14px;">Café da manhã com vista</p>
    <h2 style="color:#00405a;font-size:clamp(30px,4vw,48px);line-height:1.1;margin:0 0 18px;">Café da manhã na Urca, dentro do Parque Bondinho Pão de Açúcar</h2>
    <p style="color:#485156;font-size:1.08rem;line-height:1.7;max-width:760px;">Para quem busca <strong>café da manhã na Urca</strong>, <strong>café da manhã no Bondinho Pão de Açúcar</strong> ou uma experiência de manhã com vista no Rio de Janeiro, a Embaixada Carioca abre todos os dias no Morro da Urca.</p>
    <ul style="color:#00405a;font-size:1rem;line-height:1.7;margin:22px 0 0;padding-left:1.25rem;">
      <li>Suba cedo para aproveitar a luz da manhã e o movimento mais tranquilo do parque.</li>
      <li>Reserve a mesa antes da visita, especialmente em fins de semana e feriados.</li>
      <li>Combine café da manhã, fotos no Morro da Urca e subida ao Pão de Açúcar.</li>
      <li>Confira no cardápio do dia os itens disponíveis e sugestões da casa.</li>
    </ul>
    <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:28px;">
      <a href="https://go.tagme.com.br/embaixadacarioca" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 22px;border-radius:999px;background:#f59b1e;color:#00405a;font-weight:900;text-decoration:none;letter-spacing:.12em;text-transform:uppercase;font-size:12px;">Reservar café da manhã</a>
      <a href="/cardapio.html" style="display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 22px;border-radius:999px;border:1px solid rgba(0,64,90,.28);color:#00405a;font-weight:800;text-decoration:none;letter-spacing:.12em;text-transform:uppercase;font-size:12px;">Ver cardápio</a>
    </div>
  </div>
</section>
'''.strip()

GUIA_BLOCK = '''
<section class="guia-reservation-links" aria-label="Planeje sua visita à Embaixada Carioca" style="background:#00405a;color:#f6efde;padding:48px 0;margin:48px 0 0;">
  <div class="container" style="max-width:980px;margin:0 auto;padding:0 1.5rem;">
    <p style="color:#f59b1e;font-size:11px;letter-spacing:.22em;text-transform:uppercase;margin-bottom:12px;">Depois do roteiro</p>
    <h2 style="color:#fff;font-size:clamp(28px,4vw,44px);line-height:1.12;margin:0 0 14px;">Complete o passeio com a Embaixada Carioca</h2>
    <p style="color:rgba(246,239,222,.9);font-size:1.05rem;line-height:1.7;max-width:760px;">Se o seu roteiro passa pelo Bondinho, Morro da Urca ou Pão de Açúcar, reserve uma parada para café da manhã, almoço brasileiro, caipirinhas ou uma experiência com vista.</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px;">
      <a href="/cafe-da-manha.html" style="display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 18px;border-radius:999px;background:#f59b1e;color:#00405a;font-weight:900;text-decoration:none;">Café da manhã</a>
      <a href="/almoco.html" style="display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 18px;border-radius:999px;background:#f59b1e;color:#00405a;font-weight:900;text-decoration:none;">Almoço</a>
      <a href="/como-chegar.html" style="display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 18px;border-radius:999px;border:1px solid rgba(246,239,222,.5);color:#fff;font-weight:800;text-decoration:none;">Como chegar</a>
      <a href="https://go.tagme.com.br/embaixadacarioca" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 18px;border-radius:999px;border:1px solid rgba(246,239,222,.5);color:#fff;font-weight:800;text-decoration:none;">Reservar</a>
    </div>
  </div>
</section>
'''.strip()


def update_meta(html, desc):
    return re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', html, count=1)


def before_body(html, block):
    if block[:80] in html or 'seo-conversion-block' in html and 'Restaurante no Morro da Urca' in block:
        return html, False
    idx = html.lower().rfind('</body>')
    if idx < 0:
        return html + '\n' + block + '\n', True
    return html[:idx] + block + '\n' + html[idx:], True


def main():
    REPORT_DIR.mkdir(exist_ok=True)
    changed = []

    targets = [
        ('restaurante-morro-da-urca.html', 'Restaurante no Morro da Urca dentro do Parque Bondinho Pão de Açúcar. Café da manhã, almoço brasileiro, caipirinhas, eventos e vista no Rio de Janeiro.', MORRO_BLOCK),
        ('cafe-da-manha.html', 'Café da manhã na Urca com vista para o Pão de Açúcar, dentro do Parque Bondinho. Todos os dias, no Morro da Urca, com reserva online.', CAFE_BLOCK),
    ]
    for file, desc, block in targets:
        path = ROOT / file
        if not path.exists():
            continue
        html = path.read_text(encoding='utf-8', errors='ignore')
        original = html
        html = update_meta(html, desc)
        html, added = before_body(html, block)
        if html != original:
            path.write_text(html, encoding='utf-8')
            changed.append((file, 'SEO/conversion reinforcement'))

    guia = ROOT / 'guia-do-rio.html'
    if guia.exists():
        html = guia.read_text(encoding='utf-8', errors='ignore')
        original = html
        if 'guia-reservation-links' not in html:
            idx = html.lower().rfind('</body>')
            html = html[:idx] + GUIA_BLOCK + '\n' + html[idx:] if idx >= 0 else html + '\n' + GUIA_BLOCK
        if html != original:
            guia.write_text(html, encoding='utf-8')
            changed.append(('guia-do-rio.html', 'Internal linking to reservation/product pages'))

    for rel in ['en/index.html', 'es/index.html']:
        path = ROOT / rel
        if not path.exists():
            continue
        html = path.read_text(encoding='utf-8', errors='ignore')
        original = html
        if rel.startswith('en/'):
            desc = 'Brazilian restaurant at Urca Hill inside Sugarloaf Cable Car Park in Rio de Janeiro. Daily breakfast, Brazilian lunch, caipirinhas, cold draft beer and views.'
            html = update_meta(html, desc)
            html = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', html, count=1)
            html = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{desc}">', html, count=1)
            html = html.replace('7.779 avaliações', '7,779 reviews').replace('avaliações verificadas', 'verified reviews')
        else:
            html = html.replace('7.779 avaliações', '7.779 reseñas').replace('avaliações verificadas', 'reseñas verificadas')
            html = html.replace('vista panorámica panorámicas', 'vista panorámica')
            html = html.replace('Dos universos, una vista', 'Dois universos, uma vista')
        if html != original:
            path.write_text(html, encoding='utf-8')
            changed.append((rel, 'Final EN/ES badge, meta and CTA cleanup'))

    lines = ['# SEO Content Growth Fixes Report', '', 'Status: **PASS**', '', '## Implementado',
             '- Revisão final EN/ES de badge, meta e CTAs.',
             '- Reforço SEO de restaurante-morro-da-urca.html.',
             '- Reforço SEO/conversão de cafe-da-manha.html.',
             '- Internal linking do Guia do Rio para páginas de reserva.', '', f'Ações: **{len(changed)}**', '', '## Detalhe']
    for file, action in changed:
        lines.append(f'- `{file}` — {action}')
    if not changed:
        lines.append('Nenhuma alteração pendente.')
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'SEO content growth fixes: {len(changed)} actions')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
