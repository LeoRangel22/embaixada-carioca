#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / '_audit_reports'
REPORT = REPORT_DIR / 'tracking_and_r2d2_assets_report.md'
EXCLUDE = {'.git', '.github', 'node_modules', '_audit_reports', 'dist', 'build', 'coverage'}
CONVERSION = '<script defer src="/assets/conversion-tracking.js"></script>'
R2D2 = '<script defer src="/assets/r2d2-dynamic-banner.js"></script>'
TICKET = '<script defer src="/assets/bondinho-ticket-notice.js"></script>'
MENU_SCHEMA = '<script defer src="/assets/menuitem-schema-enhancer.js"></script>'
INTERNAL_CONTRAST = '<script defer src="/assets/internal-page-contrast-rescue.js"></script>'


def html_pages():
    return sorted(p for p in ROOT.rglob('*.html') if not any(part in EXCLUDE for part in p.parts))


def before_body(html, snippet):
    if snippet in html:
        return html, False
    idx = html.lower().rfind('</body>')
    if idx < 0:
        return html + '\n' + snippet + '\n', True
    return html[:idx] + snippet + '\n' + html[idx:], True


def main():
    REPORT_DIR.mkdir(exist_ok=True)
    rows = []
    for path in html_pages():
        rel = path.relative_to(ROOT).as_posix()
        html = path.read_text(encoding='utf-8', errors='ignore')
        original = html
        html, c1 = before_body(html, CONVERSION)
        html, c2 = before_body(html, R2D2)
        html, c3 = before_body(html, TICKET)
        html, c4 = before_body(html, MENU_SCHEMA)
        html, c5 = before_body(html, INTERNAL_CONTRAST)
        if html != original:
            path.write_text(html, encoding='utf-8')
        if c1 or c2 or c3 or c4 or c5:
            rows.append((rel, c1, c2, c3, c4, c5))
    lines = [
        '# Tracking, R2D2, Ticket Notice, Menu Schema and Contrast Rescue Assets Report',
        '',
        'Status: **PASS**',
        '',
        '## Implementado',
        '- GA4/outbound conversion tracking para cliques em TagMe, WhatsApp, email e telefone.',
        '- Banner contextual por horário do dia para café, almoço, entardecer e reserva.',
        '- Aviso próximo aos CTAs: reserva não inclui ingresso do Parque Bondinho.',
        '- Schema MenuItem ampliado com picanha, feijoada, bobó, caipirinha, chope e café da manhã.',
        '- Resgate de contraste para páginas internas, H3 claros e cards em fundo escuro.',
        '',
        f'Arquivos alterados: **{len(rows)}**',
        '',
        '## Detalhe',
    ]
    for rel, c1, c2, c3, c4, c5 in rows:
        items = []
        if c1: items.append('conversion-tracking.js')
        if c2: items.append('r2d2-dynamic-banner.js')
        if c3: items.append('bondinho-ticket-notice.js')
        if c4: items.append('menuitem-schema-enhancer.js')
        if c5: items.append('internal-page-contrast-rescue.js')
        lines.append(f'- `{rel}` — ' + ', '.join(items))
    if not rows:
        lines.append('Nenhuma página pendente; scripts já estavam aplicados.')
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Tracking/R2D2/ticket/schema/contrast injected into {len(rows)} pages')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
