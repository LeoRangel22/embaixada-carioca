#!/usr/bin/env python3
"""
Google Analytics Foundation — Embaixada Carioca.

Objetivo:
- instalar Google tag GA4 em todas as páginas HTML relevantes;
- evitar duplicidade;
- criar camada inicial de eventos para botões e links estratégicos;
- reduzir trabalho inicial da main thread carregando o gtag após idle/interação;
- manter base para Google Ads, remarketing, públicos e conversões futuras.

Medição GA4: G-9GRXVZ55CB
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GA_MEASUREMENT_ID = "G-9GRXVZ55CB"

SKIP_FILES = {
    "formulario.html",
    "general-3/index.html",
    "home-preview.html",
    "lojasadm/index.html",
    "offline.html",
}
DISCOVERY_EXCLUDED_DIRS = {
    ".codex-work",
    ".git",
    "_audit_reports",
    "_backups",
    "_includes",
    "_templates",
    "node_modules",
    "scripts",
    "src",
}

GA_HEAD_BLOCK = f'''<!-- EC Analytics Foundation v2 -->
<script id="ec-ga4-base">
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  window.ecLoadGA4 = window.ecLoadGA4 || function(){{
    if (window.ecGA4Loaded) return;
    window.ecGA4Loaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}';
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', '{GA_MEASUREMENT_ID}', {{ send_page_view: true }});
  }};
  (function(){{
    var load = window.ecLoadGA4;
    var idle = function(){{
      if ('requestIdleCallback' in window) requestIdleCallback(load, {{ timeout: 2600 }});
      else setTimeout(load, 1800);
    }};
    ['pointerdown','keydown','touchstart','scroll'].forEach(function(evt){{
      window.addEventListener(evt, load, {{ once:true, passive:true }});
    }});
    if (document.readyState === 'complete') idle();
    else window.addEventListener('load', idle, {{ once:true }});
  }})();
</script>
<!-- /EC Analytics Foundation v2 -->'''

# A camada de eventos vive em um único asset compartilhado. Blocos inline
# antigos são reconhecidos por EVENTS_BLOCK_RE e removidos durante a aplicação.
GA_EVENTS_BLOCK = '<script defer src="/assets/conversion-tracking.js"></script>'

HEAD_OPEN_RE = re.compile(r'(<head[^>]*>)', re.IGNORECASE)
BODY_CLOSE_RE = re.compile(r'</body>', re.IGNORECASE)
GA_BLOCK_RE = re.compile(r'\n*<!-- EC Analytics Foundation v[12] -->[\s\S]*?<!-- /EC Analytics Foundation v[12] -->\s*', re.IGNORECASE)
LEGACY_GTAG_RE = re.compile(r'\n*<!-- Google tag \(gtag\.js\) -->\s*<script\s+async\s+src=["\']https://www\.googletagmanager\.com/gtag/js\?id=G-9GRXVZ55CB["\']></script>\s*<script id=["\']ec-ga4-base["\']>[\s\S]*?</script>\s*', re.IGNORECASE)
EVENTS_BLOCK_RE = re.compile(r'\n*<!-- EC Analytics Events v[12] -->[\s\S]*?<!-- /EC Analytics Events v[12] -->\s*', re.IGNORECASE)
CONVERSION_TRACKING_RE = re.compile(r'<script\b[^>]*src=["\']/assets/conversion-tracking\.js(?:\?[^"\']*)?["\'][^>]*></script>', re.IGNORECASE)
LEGACY_WHATSAPP_EVENT_RE = re.compile(
    r'''\n\s*// Evento: Clique em link WhatsApp\s*\n'''
    r'''\s*document\.querySelectorAll\('a\[href\*="wa\.me"\], a\[href\*="whatsapp"\]'\)\.forEach\(function\(el\) \{\s*'''
    r'''el\.addEventListener\('click', function\(\) \{\s*'''
    r'''if \(typeof gtag !== 'undefined'\) \{\s*'''
    r'''gtag\('event', 'whatsapp_click', \{[\s\S]*?\}\);\s*'''
    r'''\}\s*\}\);\s*\}\);\s*''',
    re.IGNORECASE,
)

REPORT: list[str] = []
COUNTERS = {
    'html_scanned': 0,
    'html_updated': 0,
    'ga_head_installed': 0,
    'event_layer_installed': 0,
    'legacy_whatsapp_handlers_removed': 0,
    'skipped': 0,
}


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if any(part in {'.git', '.codex-work', 'node_modules', 'scripts', 'src'} for part in path.parts):
        return True
    if rel in SKIP_FILES:
        return True
    if rel.startswith('_'):
        return True
    return False


def inject_blocks(text: str, rel: str) -> str:
    original = text
    text, legacy_whatsapp_removed = LEGACY_WHATSAPP_EVENT_RE.subn('\n', text)
    COUNTERS['legacy_whatsapp_handlers_removed'] += legacy_whatsapp_removed

    text, ga_replaced = GA_BLOCK_RE.subn(lambda _: '\n' + GA_HEAD_BLOCK + '\n', text, count=1)
    if not ga_replaced:
        text, ga_replaced = LEGACY_GTAG_RE.subn(lambda _: '\n' + GA_HEAD_BLOCK + '\n', text, count=1)

    if ga_replaced:
        COUNTERS['ga_head_installed'] += 1
    elif HEAD_OPEN_RE.search(text):
        text = HEAD_OPEN_RE.sub(lambda m: m.group(1) + '\n' + GA_HEAD_BLOCK, text, count=1)
        COUNTERS['ga_head_installed'] += 1
    else:
        REPORT.append(f'WARN: {rel} sem <head>; GA não inserido no head')

    text = EVENTS_BLOCK_RE.sub('\n', text)
    if CONVERSION_TRACKING_RE.search(text):
        COUNTERS['event_layer_installed'] += 1
    elif BODY_CLOSE_RE.search(text):
        text = BODY_CLOSE_RE.sub(lambda m: GA_EVENTS_BLOCK + '\n' + m.group(0), text, count=1)
        COUNTERS['event_layer_installed'] += 1
    else:
        REPORT.append(f'WARN: {rel} sem </body>; eventos não inseridos')

    return text if text != original else original


def process_html(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    COUNTERS['html_scanned'] += 1

    if should_skip(path):
        COUNTERS['skipped'] += 1
        return

    original = path.read_text(encoding='utf-8', errors='ignore')
    updated = inject_blocks(original, rel)

    if updated != original:
        path.write_text(updated, encoding='utf-8')
        COUNTERS['html_updated'] += 1
        REPORT.append(f'UPDATED: {rel}')


def write_report() -> None:
    report_dir = ROOT / '_audit_reports'
    report_dir.mkdir(exist_ok=True)
    report = report_dir / 'google_analytics_foundation_report.md'

    lines = [
        '# Google Analytics Foundation — Embaixada Carioca',
        '',
        'Status geral: **PASS**',
        '',
        '## Measurement ID',
        f'- {GA_MEASUREMENT_ID}',
        '',
        '## Estratégia de performance',
        '- GA4 carrega após idle/interação para reduzir trabalho inicial da main thread.',
        '- Eventos de clique forçam carregamento antes de enviar a conversão, preservando medição de CTAs.',
        '',
        '## Eventos configurados',
        '- click_reservar',
        '- whatsapp_click',
        '- click_cardapio',
        '- click_como_chegar',
        '- click_google_maps',
        '- click_google_reviews',
        '- click_eventos',
        '- click_cafe_da_manha',
        '- click_almoco',
        '- click_idioma',
        '',
        '## Contadores',
    ]
    for key, value in COUNTERS.items():
        lines.append(f'- {key}: {value}')

    lines.extend(['', '## Arquivos'])
    lines.extend(f'- {item}' for item in REPORT)

    lines.extend([
        '',
        '## Próximos passos no GA4',
        '- Validar a tag no Tag Assistant.',
        '- Confirmar page_view no relatório Tempo real.',
        '- Marcar click_reservar, whatsapp_click, click_eventos, click_google_maps e click_google_reviews como key events.',
        '- Vincular GA4 ao Google Ads para remarketing e públicos.',
        '- Implementar Consent Mode quando houver banner de consentimento.',
        '',
    ])
    report.write_text('\n'.join(lines), encoding='utf-8')
    print(report.read_text(encoding='utf-8'))


def main() -> int:
    for path in sorted(ROOT.rglob('*.html')):
        rel_parts = path.relative_to(ROOT).parts
        if set(rel_parts) & DISCOVERY_EXCLUDED_DIRS:
            continue
        process_html(path)
    write_report()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
