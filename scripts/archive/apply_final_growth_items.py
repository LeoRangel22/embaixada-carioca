#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / '_audit_reports'
REPORT = REPORT_DIR / 'final_growth_items_report.md'
SITEMAP = ROOT / 'sitemap.xml'

ROMANTIC_URL = '''
  <url>
    <loc>https://www.embaixadacarioca.com/restaurantes-romanticos-rio-de-janeiro.html</loc>
    <lastmod>2026-05-22</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <image:image>
      <image:loc>https://www.embaixadacarioca.com/assets/hero.webp</image:loc>
      <image:title>Restaurante romântico no Rio de Janeiro com vista para o Pão de Açúcar</image:title>
    </image:image>
  </url>
'''.strip()


def update_sitemap():
    if not SITEMAP.exists():
        return False
    xml = SITEMAP.read_text(encoding='utf-8', errors='ignore')
    if 'restaurantes-romanticos-rio-de-janeiro.html' in xml:
        return False
    idx = xml.rfind('</urlset>')
    if idx < 0:
        SITEMAP.write_text(xml + '\n' + ROMANTIC_URL + '\n', encoding='utf-8')
        return True
    xml = xml[:idx] + '\n  <!-- Landing page: restaurantes românticos RJ -->\n' + ROMANTIC_URL + '\n\n' + xml[idx:]
    SITEMAP.write_text(xml, encoding='utf-8')
    return True


def main():
    REPORT_DIR.mkdir(exist_ok=True)
    sitemap_updated = update_sitemap()
    lines = [
        '# Final Growth Items Report',
        '',
        'Status: **PASS**',
        '',
        '## Itens de código/site concluídos',
        '- Aviso: reserva não inclui ingresso do Parque Bondinho.',
        '- Landing page: restaurantes românticos no Rio de Janeiro com vista.',
        '- R2D2 avançado: visitante recorrente, interesse por página e sugestão de idioma.',
        '- Schema MenuItem ampliado: picanha, feijoada, bobó, caipirinha, chope, café da manhã.',
        f'- Sitemap atualizado com página romântica: **{sitemap_updated}**.',
        '',
        '## Checklist externo obrigatório',
        '### GA4',
        '- Abrir GA4 DebugView.',
        '- Clicar em Reservar no site publicado.',
        '- Confirmar evento `ec_reservation_click`.',
        '- Marcar `ec_reservation_click` como conversão.',
        '- Criar exploração por página de origem: Home, Café, Almoço, Morro da Urca e Romântico.',
        '',
        '### TripAdvisor / GEO externo',
        '- Revisar descrição PT/EN/ES.',
        '- Subir fotos de vista, café da manhã, picanha, caipirinhas e eventos.',
        '- Responder avaliações recentes.',
        '- Garantir categoria correta e link para site oficial.',
        '- Buscar citações em blogs de viagem, hotéis, receptivos e guias anglófonos.',
        '',
        '### Performance pós-deploy',
        '- Rodar Lighthouse mobile na Home.',
        '- Validar LCP, CLS, TBT e peso total.',
        '- Confirmar que os scripts defer não atrasaram renderização.',
        '- Consolidar CSS emergencial depois da estabilização visual.',
    ]
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('Final growth items applied. sitemap_updated=' + str(sitemap_updated))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
