#!/usr/bin/env python3
"""
Google Analytics Foundation — Embaixada Carioca.

Objetivo:
- instalar Google tag GA4 em todas as páginas HTML relevantes;
- evitar duplicidade;
- criar uma camada inicial de eventos para botões e links estratégicos;
- deixar base limpa para Google Ads, remarketing, públicos e conversões futuras.

Medição GA4: G-9GRXVZ55CB
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GA_MEASUREMENT_ID = "G-9GRXVZ55CB"

SKIP_FILES = {
    "home-preview.html",
    "offline.html",
}

GA_HEAD_BLOCK = f'''<!-- EC Analytics Foundation v1 -->
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script id="ec-ga4-base">
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_MEASUREMENT_ID}', {{
    send_page_view: true
  }});
</script>
<!-- /EC Analytics Foundation v1 -->'''

GA_EVENTS_BLOCK = '''<!-- EC Analytics Events v1 -->
<script id="ec-ga4-events">
(function(){
  'use strict';

  var EVENT_VERSION = '2026-05-19.1';

  function textOf(el){
    if (!el) return '';
    return String(
      el.innerText ||
      el.getAttribute('aria-label') ||
      el.getAttribute('title') ||
      el.getAttribute('data-analytics-label') ||
      ''
    ).replace(/\s+/g, ' ').trim().slice(0, 140);
  }

  function cleanUrl(url){
    if (!url) return '';
    try {
      var u = new URL(url, window.location.href);
      var host = u.hostname.toLowerCase();
      if (host.indexOf('wa.me') >= 0 || host.indexOf('whatsapp') >= 0) {
        return u.origin + u.pathname;
      }
      return u.href.slice(0, 500);
    } catch(e) {
      return String(url).slice(0, 500);
    }
  }

  function eventNameFor(el){
    var href = String(el.href || el.getAttribute('href') || '');
    var label = textOf(el);
    var classes = String(el.className || '');
    var aria = String(el.getAttribute('aria-label') || '');
    var haystack = (href + ' ' + label + ' ' + classes + ' ' + aria).toLowerCase();

    if (haystack.indexOf('go.tagme.com.br') >= 0 || haystack.indexOf('reservar') >= 0 || haystack.indexOf('reserva') >= 0) return 'click_reservar';
    if (haystack.indexOf('wa.me') >= 0 || haystack.indexOf('whatsapp') >= 0) return 'click_whatsapp';
    if (haystack.indexOf('google.com/maps') >= 0 || haystack.indexOf('maps.app.goo') >= 0 || haystack.indexOf('como chegar') >= 0 || haystack.indexOf('directions') >= 0) return 'click_como_chegar';
    if (haystack.indexOf('cardapio') >= 0 || haystack.indexOf('cardápio') >= 0 || haystack.indexOf('menu') >= 0) return 'click_cardapio';
    if (haystack.indexOf('eventos') >= 0 || haystack.indexOf('events') >= 0 || haystack.indexOf('eventos corporativos') >= 0) return 'click_eventos';
    if (haystack.indexOf('cafe-da-manha') >= 0 || haystack.indexOf('café da manhã') >= 0 || haystack.indexOf('breakfast') >= 0 || haystack.indexOf('desayuno') >= 0) return 'click_cafe_da_manha';
    if (haystack.indexOf('almoco') >= 0 || haystack.indexOf('almoço') >= 0 || haystack.indexOf('lunch') >= 0 || haystack.indexOf('almuerzo') >= 0) return 'click_almoco';
    if (haystack.indexOf('lang-') >= 0 || haystack.indexOf('hreflang') >= 0 || el.closest('.lang-switcher')) return 'click_idioma';

    return '';
  }

  function sendAnalyticsEvent(name, el){
    if (!name || typeof window.gtag !== 'function') return;

    var href = String(el.href || el.getAttribute('href') || '');
    var label = textOf(el);

    window.gtag('event', name, {
      event_category: 'site_interaction',
      event_label: label || cleanUrl(href),
      link_url: cleanUrl(href),
      link_text: label,
      page_path: window.location.pathname,
      page_location_clean: window.location.origin + window.location.pathname,
      page_language: document.documentElement.lang || '',
      analytics_version: EVENT_VERSION
    });
  }

  document.addEventListener('click', function(event){
    var target = event.target;
    if (!target || !target.closest) return;

    var el = target.closest('a, button, [role="button"]');
    if (!el) return;

    var name = eventNameFor(el);
    if (!name) return;

    sendAnalyticsEvent(name, el);
  }, true);
})();
</script>
<!-- /EC Analytics Events v1 -->'''

HEAD_OPEN_RE = re.compile(r'(<head[^>]*>)', re.IGNORECASE)
BODY_CLOSE_RE = re.compile(r'</body>', re.IGNORECASE)
GA_BLOCK_RE = re.compile(r'\n*<!-- EC Analytics Foundation v1 -->[\s\S]*?<!-- /EC Analytics Foundation v1 -->\s*', re.IGNORECASE)
EVENTS_BLOCK_RE = re.compile(r'\n*<!-- EC Analytics Events v1 -->[\s\S]*?<!-- /EC Analytics Events v1 -->\s*', re.IGNORECASE)

REPORT: list[str] = []
COUNTERS = {
    'html_scanned': 0,
    'html_updated': 0,
    'ga_head_installed': 0,
    'event_layer_installed': 0,
    'skipped': 0,
}


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel in SKIP_FILES:
        return True
    if rel.startswith('_'):
        return True
    return False


def inject_blocks(text: str, rel: str) -> str:
    original = text
    text = GA_BLOCK_RE.sub('\n', text)
    text = EVENTS_BLOCK_RE.sub('\n', text)

    if HEAD_OPEN_RE.search(text):
        text = HEAD_OPEN_RE.sub(r'\1\n' + GA_HEAD_BLOCK, text, count=1)
        COUNTERS['ga_head_installed'] += 1
    else:
        REPORT.append(f'WARN: {rel} sem <head>; GA não inserido no head')

    if BODY_CLOSE_RE.search(text):
        text = BODY_CLOSE_RE.sub(GA_EVENTS_BLOCK + '\n</body>', text, count=1)
        COUNTERS['event_layer_installed'] += 1
    else:
        REPORT.append(f'WARN: {rel} sem </body>; eventos não inseridos')

    return text if text != original else original


def process_html(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    COUNTERS['html_scanned'] += 1

    if should_skip(path):
        COUNTERS['skipped'] += 1
        REPORT.append(f'SKIP: {rel}')
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
        f'## Measurement ID',
        f'- {GA_MEASUREMENT_ID}',
        '',
        '## Eventos configurados',
        '- click_reservar',
        '- click_whatsapp',
        '- click_cardapio',
        '- click_como_chegar',
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
        '- Marcar click_reservar, click_whatsapp, click_eventos e click_como_chegar como key events.',
        '- Vincular GA4 ao Google Ads para remarketing e públicos.',
        '- Implementar Consent Mode quando houver banner de consentimento.',
        '',
    ])
    report.write_text('\n'.join(lines), encoding='utf-8')
    print(report.read_text(encoding='utf-8'))


def main() -> int:
    for path in sorted(ROOT.rglob('*.html')):
        if '.git' not in path.parts:
            process_html(path)
    write_report()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
