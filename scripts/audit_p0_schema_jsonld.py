#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
REPORT = OUT / 'p0_schema_jsonld_audit.md'
JSON_OUT = OUT / 'p0_schema_jsonld_audit.json'

PAGES = [
    'index.html', 'en/index.html', 'es/index.html',
    'cafe-da-manha.html', 'en/cafe-da-manha.html', 'es/cafe-da-manha.html',
    'restaurante-morro-da-urca.html', 'eventos.html', 'en/eventos.html', 'es/eventos.html',
    'guia-do-rio.html', 'restaurantes-romanticos-rio-de-janeiro.html',
]
REQUIRED = ['Restaurant', 'FAQPage', 'Menu', 'BreadcrumbList', 'WebSite', 'WebPage']
SCRIPT_RE = re.compile(r'<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)


def extract_types(obj):
    found = set()
    def walk(x):
        if isinstance(x, dict):
            t = x.get('@type')
            if isinstance(t, str): found.add(t)
            if isinstance(t, list):
                for i in t:
                    if isinstance(i, str): found.add(i)
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(obj)
    return found


def audit_page(rel):
    path = ROOT / rel
    if not path.exists():
        return {'page': rel, 'status': 'FAIL', 'score': 0, 'found': [], 'missing': ['file missing'], 'json_valid': False}
    html = path.read_text(encoding='utf-8', errors='ignore')
    scripts = SCRIPT_RE.findall(html)
    found = set()
    valid_count = 0
    for s in scripts:
        try:
            obj = json.loads(s.strip())
            valid_count += 1
            found.update(extract_types(obj))
        except Exception:
            pass
    missing = [t for t in REQUIRED if t not in found]
    score = max(0, round(100 - 14 * len(missing) - (0 if valid_count else 20)))
    return {'page': rel, 'status': 'PASS' if score >= 90 else 'FAIL', 'score': score, 'found': sorted(found), 'missing': missing, 'json_valid': valid_count > 0, 'blocks': valid_count}


def main():
    OUT.mkdir(exist_ok=True)
    rows = [audit_page(p) for p in PAGES]
    min_score = min(r['score'] for r in rows) if rows else 0
    status = 'PASS' if min_score >= 90 else 'FAIL'
    JSON_OUT.write_text(json.dumps({'status': status, 'min_score': min_score, 'required': REQUIRED, 'results': rows}, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# P0 Schema JSON-LD Audit', '', f'Status geral: **{status}**', f'Score mínimo: **{min_score}**', '', '## Critério', '- Bloco `<script type="application/ld+json">` válido.', '- Tipos mínimos: Restaurant, FAQPage, Menu, BreadcrumbList, WebSite e WebPage.', '- Score mínimo: 90.', '', '## Resultados']
    for r in rows:
        lines.append(f"- `{r['page']}` — {r['status']} — score {r['score']} — blocos válidos {r.get('blocks',0)}")
        if r['missing']:
            lines.append('  - Faltando: ' + ', '.join(r['missing']))
        if r['found']:
            lines.append('  - Encontrado: ' + ', '.join(r['found'][:20]))
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'P0 schema JSON-LD audit: {status} min_score={min_score}')
    return 0 if min_score >= 90 else 1

if __name__ == '__main__':
    raise SystemExit(main())
