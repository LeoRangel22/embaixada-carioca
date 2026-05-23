#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
MD = OUT / 'hreflang_pt_en_es_audit.md'
JSON_OUT = OUT / 'hreflang_pt_en_es_audit.json'

PAGES = [
    'index.html', 'almoco.html', 'cafe-da-manha.html', 'eventos.html', 'guia-do-rio.html',
    'restaurante-morro-da-urca.html', 'restaurantes-romanticos-rio-de-janeiro.html',
    'en/index.html', 'en/almoco.html', 'en/cafe-da-manha.html', 'en/eventos.html',
    'es/index.html', 'es/almoco.html', 'es/cafe-da-manha.html', 'es/eventos.html',
]
REQUIRED = ['pt-BR', 'en', 'es', 'x-default']
HREFLANG_RE = re.compile(r'<link\s+[^>]*rel=["\']alternate["\'][^>]*hreflang=["\']([^"\']+)["\'][^>]*>|<link\s+[^>]*hreflang=["\']([^"\']+)["\'][^>]*rel=["\']alternate["\'][^>]*>', re.I)
CANONICAL_RE = re.compile(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\'][^>]*>|<link\s+[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\'][^>]*>', re.I)


def head(html):
    m = re.search(r'<head[^>]*>(.*?)</head>', html, re.I | re.S)
    return m.group(1) if m else html[:3000]


def audit_page(rel):
    path = ROOT / rel
    if not path.exists():
        return {'page': rel, 'status': 'FAIL', 'score': 0, 'missing': ['file missing'], 'found': [], 'canonical': None}
    html = path.read_text(encoding='utf-8', errors='ignore')
    h = head(html)
    found = []
    for a, b in HREFLANG_RE.findall(h):
        found.append((a or b).strip())
    found_set = set(found)
    missing = [x for x in REQUIRED if x not in found_set]
    canonical_match = CANONICAL_RE.search(h)
    canonical = None
    if canonical_match:
        canonical = canonical_match.group(1) or canonical_match.group(2)
    if not canonical:
        missing.append('canonical')
    score = max(0, 100 - len(missing) * 18)
    return {'page': rel, 'status': 'PASS' if score >= 90 else 'FAIL', 'score': score, 'missing': missing, 'found': sorted(found_set), 'canonical': canonical}


def main():
    OUT.mkdir(exist_ok=True)
    rows = [audit_page(p) for p in PAGES]
    min_score = min(r['score'] for r in rows) if rows else 0
    status = 'PASS' if min_score >= 90 else 'FAIL'
    JSON_OUT.write_text(json.dumps({'status': status, 'min_score': min_score, 'required': REQUIRED, 'results': rows}, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Hreflang PT/EN/ES Audit', '', f'Status geral: **{status}**', f'Score mínimo: **{min_score}**', '', '## Critérios', '- `rel="alternate"` com `hreflang="pt-BR"`.', '- `rel="alternate"` com `hreflang="en"`.', '- `rel="alternate"` com `hreflang="es"`.', '- `rel="alternate"` com `hreflang="x-default"`.', '- `canonical` presente no `<head>`.', '', '## Resultados']
    for r in rows:
        lines.append(f"- `{r['page']}` — {r['status']} — score {r['score']}")
        lines.append('  - Found: ' + ', '.join(r['found']) if r['found'] else '  - Found: nenhum hreflang')
        if r['canonical']:
            lines.append('  - Canonical: ' + r['canonical'])
        if r['missing']:
            lines.append('  - Faltando: ' + ', '.join(r['missing']))
    MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Hreflang PT EN ES audit: {status} min_score={min_score}')
    return 0 if min_score >= 90 else 1

if __name__ == '__main__':
    raise SystemExit(main())
