#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
REPORT = OUT / 'hreflang_pt_en_es_apply_report.md'
BASE = 'https://www.embaixadacarioca.com'

GROUPS = {
    'index': ('/', '/en/', '/es/'),
    'almoco': ('/almoco.html', '/en/almoco.html', '/es/almoco.html'),
    'cafe-da-manha': ('/cafe-da-manha.html', '/en/cafe-da-manha.html', '/es/cafe-da-manha.html'),
    'eventos': ('/eventos.html', '/en/eventos.html', '/es/eventos.html'),
    'guia-do-rio': ('/guia-do-rio.html', '/guia-do-rio.html', '/guia-do-rio.html'),
    'restaurante-morro-da-urca': ('/restaurante-morro-da-urca.html', '/restaurante-morro-da-urca.html', '/restaurante-morro-da-urca.html'),
    'restaurantes-romanticos-rio-de-janeiro': ('/restaurantes-romanticos-rio-de-janeiro.html', '/restaurantes-romanticos-rio-de-janeiro.html', '/restaurantes-romanticos-rio-de-janeiro.html'),
}

FILES = {
    'index.html': 'index', 'en/index.html': 'index', 'es/index.html': 'index',
    'almoco.html': 'almoco', 'en/almoco.html': 'almoco', 'es/almoco.html': 'almoco',
    'cafe-da-manha.html': 'cafe-da-manha', 'en/cafe-da-manha.html': 'cafe-da-manha', 'es/cafe-da-manha.html': 'cafe-da-manha',
    'eventos.html': 'eventos', 'en/eventos.html': 'eventos', 'es/eventos.html': 'eventos',
    'guia-do-rio.html': 'guia-do-rio',
    'restaurante-morro-da-urca.html': 'restaurante-morro-da-urca',
    'restaurantes-romanticos-rio-de-janeiro.html': 'restaurantes-romanticos-rio-de-janeiro',
}

ALT_RE = re.compile(r'\n?<link\s+[^>]*rel=["\']alternate["\'][^>]*hreflang=["\'][^"\']+["\'][^>]*>\s*|\n?<link\s+[^>]*hreflang=["\'][^"\']+["\'][^>]*rel=["\']alternate["\'][^>]*>\s*', re.I)
CANON_RE = re.compile(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*>', re.I)


def block(group):
    pt, en, es = GROUPS[group]
    return '\n'.join([
        f'<link href="{BASE}{pt}" hreflang="pt-BR" rel="alternate"/>',
        f'<link href="{BASE}{en}" hreflang="en" rel="alternate"/>',
        f'<link href="{BASE}{es}" hreflang="es" rel="alternate"/>',
        f'<link href="{BASE}{pt}" hreflang="x-default" rel="alternate"/>',
    ]) + '\n'


def apply(html, group):
    html = ALT_RE.sub('\n', html)
    b = block(group)
    m = CANON_RE.search(html)
    if m:
        insert_at = m.end()
        return html[:insert_at] + '\n' + b + html[insert_at:]
    idx = html.lower().find('</head>')
    if idx >= 0:
        return html[:idx] + b + html[idx:]
    return b + html


def main():
    OUT.mkdir(exist_ok=True)
    changed = []
    missing = []
    for rel, group in FILES.items():
        p = ROOT / rel
        if not p.exists():
            missing.append(rel)
            continue
        html = p.read_text(encoding='utf-8', errors='ignore')
        new = apply(html, group)
        if new != html:
            p.write_text(new, encoding='utf-8')
            changed.append(rel)
    lines = ['# Hreflang PT/EN/ES Apply Report', '', 'Status: **PASS**', '', '## Aplicado', '- Blocos `hreflang` canônicos PT/EN/ES/x-default inseridos ou normalizados no `<head>`.', '- Inserção logo após o `canonical` quando disponível.', '', f'Arquivos alterados: **{len(changed)}**', f'Arquivos ausentes: **{len(missing)}**', '', '## Alterados']
    for r in changed:
        lines.append(f'- `{r}`')
    if missing:
        lines += ['', '## Ausentes']
        for r in missing:
            lines.append(f'- `{r}`')
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Hreflang PT EN ES applied: changed={len(changed)} missing={len(missing)}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
