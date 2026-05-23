#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
MD = OUT / 'multilingual_ai_search_score_audit.md'
CSV = OUT / 'multilingual_ai_search_score_audit.csv'
JSON = OUT / 'multilingual_ai_search_score_audit.json'
THRESHOLD = 90

PAGES = [
    ('pt', 'index.html'), ('en', 'en/index.html'), ('es', 'es/index.html'),
    ('pt', 'cafe-da-manha.html'), ('en', 'en/cafe-da-manha.html'), ('es', 'es/cafe-da-manha.html'),
    ('pt', 'eventos.html'), ('en', 'en/eventos.html'), ('es', 'es/eventos.html'),
    ('pt', 'restaurante-morro-da-urca.html'), ('pt', 'guia-do-rio.html'),
    ('pt', 'restaurantes-romanticos-rio-de-janeiro.html'),
]

TERMS = {
    'pt': ['Morro da Urca', 'Pão de Açúcar', 'Bondinho', 'restaurante', 'café da manhã', 'caipirinha', 'feijoada', 'vista', 'reserva', 'ingresso'],
    'en': ['Urca Hill', 'Sugarloaf', 'Cable Car', 'restaurant', 'breakfast', 'caipirinha', 'feijoada', 'view', 'reserve', 'ticket'],
    'es': ['Morro da Urca', 'Pan de Azúcar', 'Bondinho', 'restaurante', 'desayuno', 'caipirinha', 'feijoada', 'vista', 'reservar', 'entrada'],
}

REQUIRED_ASSETS = [
    'conversion-tracking.js', 'r2d2-dynamic-banner.js', 'bondinho-ticket-notice.js',
    'menuitem-schema-enhancer.js', 'dossie-content-enhancer.js'
]

BAD_PATTERNS = {
    'pt': ['topo do Pão de Açúcar', 'No topo do Pão de Açúcar', 'Restaurante no Topo'],
    'en': ['RESERVAR', 'avaliações', 'on top of Sugarloaf Mountain'],
    'es': ['avaliações', 'Reserva tu mesa', 'tu visita', 'tu mesa', 'cima del Pan de Azúcar'],
}

TAG = re.compile(r'<[^>]+>')
SCRIPT = re.compile(r'<script.*?</script>|<style.*?</style>', re.I|re.S)
SPACE = re.compile(r'\s+')


def visible(html):
    return SPACE.sub(' ', TAG.sub(' ', SCRIPT.sub(' ', html))).strip()


def has_meta(html, name):
    return bool(re.search(r'<meta\s+[^>]*(name|property)=["\']'+re.escape(name)+r'["\'][^>]*content=["\'][^"\']{30,}["\']', html, re.I))


def score_page(lang, rel):
    path = ROOT / rel
    if not path.exists():
        return {'lang': lang, 'page': rel, 'score': 0, 'status': 'FAIL', 'missing': ['file missing'], 'bad': []}
    html = path.read_text(encoding='utf-8', errors='ignore')
    text = visible(html).lower()
    missing = []
    bad = []
    score = 100

    if not re.search(r'<title>[^<]{35,}</title>', html, re.I|re.S):
        missing.append('strong title')
        score -= 8
    if not has_meta(html, 'description'):
        missing.append('meta description')
        score -= 8
    if not has_meta(html, 'og:title'):
        missing.append('og:title')
        score -= 4
    if not has_meta(html, 'og:description'):
        missing.append('og:description')
        score -= 4

    terms = TERMS[lang]
    present_terms = [t for t in terms if t.lower() in text]
    term_score = round(100 * len(present_terms) / len(terms))
    if term_score < 80:
        score -= (80 - term_score) * 0.35
        missing.append('semantic terms below 80%')

    for asset in REQUIRED_ASSETS:
        if asset not in html:
            missing.append('asset ' + asset)
            score -= 3

    for pattern in BAD_PATTERNS.get(lang, []):
        if pattern.lower() in text or pattern in html:
            bad.append(pattern)
            score -= 8

    if 'pergunta' not in text and 'where to eat' not in text and 'dónde comer' not in text and 'onde comer' not in text:
        missing.append('AI direct-answer/Q&A block')
        score -= 5

    score = max(0, min(100, round(score)))
    return {'lang': lang, 'page': rel, 'score': score, 'status': 'PASS' if score >= THRESHOLD else 'FAIL', 'missing': missing, 'bad': bad}


def main():
    OUT.mkdir(exist_ok=True)
    rows = [score_page(lang, rel) for lang, rel in PAGES]
    min_score = min(r['score'] for r in rows) if rows else 0
    status = 'PASS' if min_score >= THRESHOLD else 'FAIL'

    JSON.write_text(json.dumps({'status': status, 'threshold': THRESHOLD, 'min_score': min_score, 'results': rows}, ensure_ascii=False, indent=2), encoding='utf-8')
    with CSV.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['lang','page','status','score','missing','bad'])
        w.writeheader()
        for r in rows:
            w.writerow({**r, 'missing': ' | '.join(r['missing']), 'bad': ' | '.join(r['bad'])})

    lines = ['# Multilingual AI Search Score Audit', '', f'Status geral: **{status}**', f'Score mínimo: **{min_score}**', f'Threshold: **{THRESHOLD}**', '', '## Critérios', '- PT/EN/ES sempre que houver página equivalente.', '- Title/meta/OG fortes.', '- Termos semânticos de busca e IA.', '- Assets de conversão, R2D2, ingresso, schema e dossiê.', '- Ausência de erros geográficos ou idioma errado.', '', '## Resultados']
    for r in rows:
        lines.append(f"- `{r['page']}` [{r['lang']}] — {r['status']} — score {r['score']}")
        if r['missing']:
            lines.append('  - Faltando: ' + ', '.join(r['missing']))
        if r['bad']:
            lines.append('  - Padrões ruins: ' + ', '.join(r['bad']))
    MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Multilingual AI search audit: {status} min_score={min_score}')
    return 0 if min_score >= THRESHOLD else 1

if __name__ == '__main__':
    raise SystemExit(main())
