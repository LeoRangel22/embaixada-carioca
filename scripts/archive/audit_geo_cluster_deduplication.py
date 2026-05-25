#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
MD = OUT / 'geo_cluster_deduplication_audit.md'
JSON_OUT = OUT / 'geo_cluster_deduplication_audit.json'

PAGES = [
    'restaurante-morro-da-urca.html',
    'restaurante-bondinho-pao-de-acucar.html',
    'onde-comer-no-pao-de-acucar.html',
    'cafe-da-manha.html',
    'cafe-da-manha-com-vista.html',
    'como-chegar.html',
    'guia-do-rio.html',
    'eventos.html',
    'restaurantes-romanticos-rio-de-janeiro.html',
]

SCRIPT_STYLE = re.compile(r'<script.*?</script>|<style.*?</style>', re.I | re.S)
TAG = re.compile(r'<[^>]+>')
SPACE = re.compile(r'\s+')
START = '<!-- EC GEO UNIQUE INTENT BLOCK -->'


def visible(path):
    html = path.read_text(encoding='utf-8', errors='ignore')
    text = TAG.sub(' ', SCRIPT_STYLE.sub(' ', html)).lower()
    return SPACE.sub(' ', text).strip()


def shingles(text, size=14):
    words = re.findall(r'[a-záàâãéêíóôõúçñü0-9]+', text.lower())
    if len(words) < size:
        return set(words)
    return {' '.join(words[i:i+size]) for i in range(len(words)-size+1)}


def similarity(a, b):
    sa, sb = shingles(a), shingles(b)
    if not sa or not sb:
        return 0
    return round(100 * len(sa & sb) / len(sa | sb))


def has_unique_block(path):
    return START in path.read_text(encoding='utf-8', errors='ignore')


def main():
    OUT.mkdir(exist_ok=True)
    existing = [p for p in PAGES if (ROOT / p).exists()]
    missing = [p for p in PAGES if not (ROOT / p).exists()]
    texts = {p: visible(ROOT / p) for p in existing}
    rows = []
    max_sim = 0
    for i, p1 in enumerate(existing):
        for p2 in existing[i+1:]:
            sim = similarity(texts[p1], texts[p2])
            max_sim = max(max_sim, sim)
            if sim >= 55:
                rows.append({'page_a': p1, 'page_b': p2, 'similarity': sim})
    unique_missing = [p for p in existing if not has_unique_block(ROOT / p)]
    status = 'PASS' if max_sim < 55 and not unique_missing else 'FAIL'
    result = {'status': status, 'max_similarity': max_sim, 'high_similarity_pairs': rows, 'unique_block_missing': unique_missing, 'missing_pages': missing}
    JSON_OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# GEO Cluster Deduplication Audit', '', f'Status geral: **{status}**', f'Maior similaridade detectada: **{max_sim}%**', '', '## Critérios', '- Similaridade entre páginas do cluster abaixo de 55%.', '- Bloco de intenção única presente nas páginas existentes.', '- Páginas ausentes listadas sem quebrar o ciclo.', '', '## Pares de alta similaridade']
    if rows:
        for r in rows:
            lines.append(f"- `{r['page_a']}` × `{r['page_b']}` — {r['similarity']}%")
    else:
        lines.append('- Nenhum par acima do limite.')
    if unique_missing:
        lines += ['', '## Sem bloco de intenção única']
        for p in unique_missing:
            lines.append(f'- `{p}`')
    if missing:
        lines += ['', '## Páginas ausentes']
        for p in missing:
            lines.append(f'- `{p}`')
    MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'GEO cluster dedup audit: {status} max_similarity={max_sim}')
    return 0 if status == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
