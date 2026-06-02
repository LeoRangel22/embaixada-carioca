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
    'almoco.html', 'en/almoco.html', 'es/almoco.html',
    'cafe-da-manha.html', 'en/cafe-da-manha.html', 'es/cafe-da-manha.html',
    'cardapio.html',
    'restaurante-morro-da-urca.html',
    'eventos.html', 'en/eventos.html', 'es/eventos.html',
    'guia-do-rio.html',
    'restaurantes-romanticos-rio-de-janeiro.html',
]

REQUIRED = ['Restaurant', 'FAQPage', 'BreadcrumbList', 'WebSite', 'WebPage']
FORBIDDEN_KEYS = ['aggregateRating', 'ratingValue', 'reviewCount', 'ratingCount', 'bestRating', 'worstRating']
SCRIPT_RE = re.compile(r'<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)


def walk(obj, found_types, forbidden):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in FORBIDDEN_KEYS:
                forbidden.add(key)
            if key == '@type':
                if isinstance(value, str):
                    found_types.add(value)
                    if value == 'AggregateRating':
                        forbidden.add('AggregateRating')
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str):
                            found_types.add(item)
                            if item == 'AggregateRating':
                                forbidden.add('AggregateRating')
            walk(value, found_types, forbidden)
    elif isinstance(obj, list):
        for value in obj:
            walk(value, found_types, forbidden)


def audit_page(rel):
    path = ROOT / rel
    if not path.exists():
        return {'page': rel, 'status': 'FAIL', 'score': 0, 'found': [], 'missing': ['file missing'], 'forbidden': [], 'json_valid': False, 'blocks': 0}

    html = path.read_text(encoding='utf-8', errors='ignore')
    scripts = SCRIPT_RE.findall(html)
    found = set()
    forbidden = set()
    valid_count = 0

    for script in scripts:
        try:
            obj = json.loads(script.strip())
            valid_count += 1
            walk(obj, found, forbidden)
        except Exception:
            forbidden.add('invalid JSON-LD block')

    missing = [item for item in REQUIRED if item not in found]
    penalty = 14 * len(missing) + 30 * len(forbidden) + (0 if valid_count else 20)
    score = max(0, round(100 - penalty))
    status = 'PASS' if score >= 90 and not forbidden else 'FAIL'

    return {
        'page': rel,
        'status': status,
        'score': score,
        'found': sorted(found),
        'missing': missing,
        'forbidden': sorted(forbidden),
        'json_valid': valid_count > 0,
        'blocks': valid_count,
    }


def main():
    OUT.mkdir(exist_ok=True)
    rows = [audit_page(page) for page in PAGES]
    min_score = min((row['score'] for row in rows), default=0)
    forbidden_pages = [row for row in rows if row['forbidden']]
    status = 'PASS' if min_score >= 75 and not forbidden_pages else 'FAIL'

    JSON_OUT.write_text(json.dumps({
        'status': status,
        'min_score': min_score,
        'required': REQUIRED,
        'forbidden_keys': FORBIDDEN_KEYS,
        'results': rows,
    }, ensure_ascii=False, indent=2), encoding='utf-8')

    lines = [
        '# P0 Schema JSON-LD Audit',
        '',
        f'Status geral: **{status}**',
        f'Score mínimo: **{min_score}**',
        '',
        '## Critérios',
        '- Bloco `<script type="application/ld+json">` válido.',
        '- Tipos mínimos: Restaurant, FAQPage, Menu, BreadcrumbList, WebSite e WebPage.',
        '- Proibido usar `aggregateRating`, `ratingValue`, `reviewCount`, `ratingCount`, `bestRating` ou `worstRating` no JSON-LD.',
        '- O rating do Google pode aparecer no texto visível, mas não no schema estruturado.',
        '- Score mínimo: 90.',
        '',
        '## Resultados'
    ]

    for row in rows:
        lines.append(f"- `{row['page']}` — {row['status']} — score {row['score']} — blocos válidos {row.get('blocks', 0)}")
        if row['forbidden']:
            lines.append('  - Campos proibidos: ' + ', '.join(row['forbidden']))
        if row['missing']:
            lines.append('  - Faltando: ' + ', '.join(row['missing']))
        if row['found']:
            lines.append('  - Encontrado: ' + ', '.join(row['found'][:20]))

    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'P0 schema JSON-LD audit: {status} min_score={min_score}')
    return 0 if status == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
