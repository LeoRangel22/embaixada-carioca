#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / '_audit_reports'
REPORT = REPORT_DIR / 'multilingual_continuous_optimization_report.md'
EXCLUDE = {'.git', '.github', 'node_modules', '_audit_reports', 'dist', 'build', 'coverage'}

ASSETS = [
    '<script defer src="/assets/conversion-tracking.js"></script>',
    '<script defer src="/assets/r2d2-dynamic-banner.js"></script>',
    '<script defer src="/assets/bondinho-ticket-notice.js"></script>',
    '<script defer src="/assets/menuitem-schema-enhancer.js"></script>',
    '<script defer src="/assets/internal-page-contrast-rescue.js"></script>',
    '<script defer src="/assets/dossie-content-enhancer.js"></script>',
]

PAGE_META = {
    'index.html': {
        'pt': ('Restaurante no Morro da Urca com Vista para o Pão de Açúcar | Embaixada Carioca', 'Restaurante brasileiro no Morro da Urca, primeira parada do Bondinho Pão de Açúcar. Café da manhã, almoço, caipirinhas, feijoada e eventos com vista no Rio.'),
        'en': ('Brazilian Restaurant at Urca Hill with Sugarloaf View | Embaixada Carioca', 'Brazilian restaurant at Urca Hill, first Sugarloaf Cable Car stop. Daily breakfast, Brazilian lunch, caipirinhas, feijoada, events and Rio views.'),
        'es': ('Restaurante Brasileño en el Morro da Urca con Vista al Pan de Azúcar | Embaixada Carioca', 'Restaurante brasileño en el Morro da Urca, primera parada del Bondinho Pão de Açúcar. Desayuno, almuerzo, caipirinhas, feijoada, eventos y vista en Río.'),
    },
    'cafe-da-manha.html': {
        'pt': ('Café da Manhã na Urca com Vista para o Pão de Açúcar | Embaixada Carioca', 'Café da manhã todos os dias no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com vista para o Pão de Açúcar e reserva online.'),
        'en': ('Breakfast at Urca Hill with Sugarloaf View | Embaixada Carioca', 'Daily breakfast at Urca Hill inside Sugarloaf Cable Car Park, with views of Sugarloaf Mountain and online reservation.'),
        'es': ('Desayuno en el Morro da Urca con Vista al Pan de Azúcar | Embaixada Carioca', 'Desayuno todos los días en el Morro da Urca, dentro del Parque Bondinho Pão de Açúcar, con vista al Pan de Azúcar y reserva online.'),
    },
    'restaurante-morro-da-urca.html': {
        'pt': ('Restaurante no Morro da Urca | Vista para o Pão de Açúcar | Embaixada Carioca', 'Restaurante no Morro da Urca, primeira parada do Bondinho Pão de Açúcar. Comida brasileira, caipirinhas, café da manhã, almoço e eventos com vista.'),
        'en': ('Restaurant at Urca Hill with Sugarloaf View | Embaixada Carioca', 'Restaurant at Urca Hill, first Sugarloaf Cable Car stop. Brazilian food, caipirinhas, breakfast, lunch and events with Rio views.'),
        'es': ('Restaurante en el Morro da Urca con Vista al Pan de Azúcar | Embaixada Carioca', 'Restaurante en el Morro da Urca, primera parada del Bondinho Pão de Açúcar. Comida brasileña, caipirinhas, desayuno, almuerzo y eventos con vista.'),
    },
    'eventos.html': {
        'pt': ('Eventos com Vista no Rio de Janeiro | Embaixada Carioca Morro da Urca', 'Espaço para eventos no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com vista para o Pão de Açúcar, gastronomia brasileira e estrutura para grupos.'),
        'en': ('Events with a View in Rio de Janeiro | Embaixada Carioca Urca Hill', 'Private and corporate events at Urca Hill inside Sugarloaf Cable Car Park, with Brazilian food, drinks and views of Sugarloaf.'),
        'es': ('Eventos con Vista en Río de Janeiro | Embaixada Carioca Morro da Urca', 'Eventos privados y corporativos en el Morro da Urca, dentro del Parque Bondinho, con comida brasileña, drinks y vista al Pan de Azúcar.'),
    },
    'guia-do-rio.html': {
        'pt': ('Guia do Rio: Morro da Urca, Pão de Açúcar e Onde Comer | Embaixada Carioca', 'Guia para planejar a visita ao Morro da Urca e Pão de Açúcar, com roteiro, dicas de acesso e onde comer dentro do Parque Bondinho.'),
        'en': ('Rio Guide: Urca Hill, Sugarloaf and Where to Eat | Embaixada Carioca', 'Guide to planning your visit to Urca Hill and Sugarloaf, with itinerary tips, access information and where to eat inside the park.'),
        'es': ('Guía de Río: Morro da Urca, Pan de Azúcar y Dónde Comer | Embaixada Carioca', 'Guía para planificar su visita al Morro da Urca y Pan de Azúcar, con roteiro, acceso y dónde comer dentro del parque.'),
    },
    'restaurantes-romanticos-rio-de-janeiro.html': {
        'pt': ('Restaurante Romântico no Rio de Janeiro com Vista | Embaixada Carioca', 'Restaurante romântico no Rio de Janeiro com vista para o Pão de Açúcar, no Morro da Urca. Drinks, almoço, pedidos especiais e eventos íntimos.'),
        'en': ('Romantic Restaurant in Rio with Sugarloaf View | Embaixada Carioca', 'Romantic restaurant in Rio de Janeiro with Sugarloaf views at Urca Hill. Drinks, Brazilian lunch, special occasions and private events.'),
        'es': ('Restaurante Romántico en Río con Vista al Pan de Azúcar | Embaixada Carioca', 'Restaurante romántico en Río de Janeiro con vista al Pan de Azúcar, en el Morro da Urca. Drinks, almuerzo, ocasiones especiales y eventos privados.'),
    },
}

REPLACEMENTS = {
    'pt': [
        ('No topo do Pão de Açúcar', 'No Morro da Urca'),
        ('no topo do Pão de Açúcar', 'no Morro da Urca'),
        ('Restaurante no Topo', 'Restaurante com vista para o Pão de Açúcar'),
        ('restaurante no topo', 'restaurante com vista para o Pão de Açúcar'),
        ('topo do Pão de Açúcar', 'Morro da Urca'),
        ('vista do Pão de Açúcar', 'vista para o Pão de Açúcar'),
    ],
    'en': [
        ('on top of Sugarloaf Mountain', 'at Urca Hill, the first Sugarloaf Cable Car stop'),
        ('at the top of Sugarloaf Mountain', 'at Urca Hill, the first Sugarloaf Cable Car stop'),
        ('top of Sugarloaf', 'Urca Hill'),
        ('RESERVAR', 'Reserve'),
        ('Reservar mesa', 'Reserve a table'),
        ('avaliações', 'reviews'),
    ],
    'es': [
        ('en la cima del Pan de Azúcar', 'en el Morro da Urca, primera parada del Bondinho'),
        ('cima del Pan de Azúcar', 'Morro da Urca'),
        ('topo do Pão de Açúcar', 'Morro da Urca'),
        ('avaliações', 'reseñas'),
        ('Reserva tu mesa', 'Reserve su mesa'),
        ('tu visita', 'su visita'),
        ('tu mesa', 'su mesa'),
    ],
}


def html_pages():
    return sorted([p for p in ROOT.rglob('*.html') if not any(part in EXCLUDE for part in p.parts)], key=lambda p: p.relative_to(ROOT).as_posix())


def language_for(rel):
    if rel.startswith('en/'):
        return 'en'
    if rel.startswith('es/'):
        return 'es'
    return 'pt'


def basename_for(rel):
    parts = rel.split('/')
    return parts[-1]


def before_body(html, snippet):
    if snippet in html:
        return html, False
    idx = html.lower().rfind('</body>')
    if idx < 0:
        return html + '\n' + snippet + '\n', True
    return html[:idx] + snippet + '\n' + html[idx:], True


def update_meta(html, title, desc):
    changed = False
    if '<title>' in html:
        html2 = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', html, count=1, flags=re.I|re.S)
        changed = changed or html2 != html
        html = html2
    if 'name="description"' in html:
        html2 = re.sub(r'<meta\s+name="description"\s+content="[^"]*"\s*/?>', f'<meta name="description" content="{desc}">', html, count=1, flags=re.I)
        changed = changed or html2 != html
        html = html2
    if 'property="og:title"' in html:
        html = re.sub(r'<meta\s+property="og:title"\s+content="[^"]*"\s*/?>', f'<meta property="og:title" content="{title}">', html, count=1, flags=re.I)
    if 'property="og:description"' in html:
        html = re.sub(r'<meta\s+property="og:description"\s+content="[^"]*"\s*/?>', f'<meta property="og:description" content="{desc}">', html, count=1, flags=re.I)
    if 'name="twitter:title"' in html:
        html = re.sub(r'<meta\s+name="twitter:title"\s+content="[^"]*"\s*/?>', f'<meta name="twitter:title" content="{title}">', html, count=1, flags=re.I)
    if 'name="twitter:description"' in html:
        html = re.sub(r'<meta\s+name="twitter:description"\s+content="[^"]*"\s*/?>', f'<meta name="twitter:description" content="{desc}">', html, count=1, flags=re.I)
    return html, changed


def main():
    REPORT_DIR.mkdir(exist_ok=True)
    changes = []
    for path in html_pages():
        rel = path.relative_to(ROOT).as_posix()
        lang = language_for(rel)
        base = basename_for(rel)
        html = path.read_text(encoding='utf-8', errors='ignore')
        original = html
        file_actions = []

        for before, after in REPLACEMENTS.get(lang, []):
            if before in html:
                html = html.replace(before, after)
                file_actions.append(f'replace {before} -> {after}')

        if base in PAGE_META and lang in PAGE_META[base]:
            title, desc = PAGE_META[base][lang]
            html, meta_changed = update_meta(html, title, desc)
            if meta_changed:
                file_actions.append('updated multilingual title/meta')

        for asset in ASSETS:
            html, added = before_body(html, asset)
            if added:
                file_actions.append('injected asset ' + asset.split('/assets/')[-1].split('.js')[0])

        if html != original:
            path.write_text(html, encoding='utf-8')
            changes.append((rel, file_actions))

    lines = [
        '# Multilingual Continuous Optimization Report', '', 'Status: **PASS**', '',
        '## Regra operacional',
        'Toda melhoria crítica do site deve ter cobertura em português, inglês e espanhol sempre que existir página equivalente.', '',
        '## Otimizações aplicadas',
        '- Titles e meta descriptions PT/EN/ES para páginas prioritárias.',
        '- Correção de geografia: Morro da Urca / primeira parada do Bondinho / vista para o Pão de Açúcar.',
        '- Correção de CTAs e reviews/reseñas nas versões EN/ES.',
        '- Injeção de conversão, R2D2, aviso de ingresso, schema MenuItem, contraste e dossiê nas páginas HTML.', '',
        f'Arquivos alterados: **{len(changes)}**', '', '## Detalhe'
    ]
    if changes:
        for rel, actions in changes:
            lines.append(f'- `{rel}` — ' + '; '.join(actions[:8]))
    else:
        lines.append('Nenhuma alteração pendente; padrões multilíngues já estavam aplicados.')
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Multilingual continuous optimization: files={len(changes)}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
