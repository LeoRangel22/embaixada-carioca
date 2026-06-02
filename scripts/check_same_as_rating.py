#!/usr/bin/env python3
"""Verifica se o sameAs do Google Maps está presente nos schemas com aggregateRating."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_RE = re.compile(
    r'(<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.I | re.S
)

VERIFIED_SOURCES = {'google.com/maps', 'maps.google', 'maps.app.goo.gl'}


def has_verified_source(obj: dict) -> bool:
    same_as = obj.get('sameAs', [])
    if isinstance(same_as, str):
        same_as = [same_as]
    return any(any(src in str(s) for src in VERIFIED_SOURCES) for s in same_as)


def check_file(page: str) -> None:
    path = ROOT / page
    if not path.exists():
        print(f'{page}: arquivo não encontrado')
        return

    html = path.read_text(encoding='utf-8', errors='ignore')
    print(f'\n=== {page} ===')

    for i, m in enumerate(SCRIPT_RE.finditer(html)):
        raw = m.group(2).strip()
        try:
            obj = json.loads(raw)
        except Exception as e:
            print(f'  Bloco {i+1}: JSON inválido — {e}')
            continue

        # Verificar @graph
        nodes = []
        if isinstance(obj, dict) and '@graph' in obj:
            nodes = obj['@graph']
        elif isinstance(obj, dict):
            nodes = [obj]
        elif isinstance(obj, list):
            nodes = obj

        for node in nodes:
            if not isinstance(node, dict):
                continue
            t = node.get('@type', '')
            same_as = node.get('sameAs', [])
            has_rating = 'aggregateRating' in node
            verified = has_verified_source(node)

            if 'Restaurant' in str(t) or has_rating or verified:
                print(f'  Bloco {i+1}: @type={t}')
                if isinstance(same_as, list):
                    google_urls = [s for s in same_as if 'google' in str(s)]
                    print(f'    sameAs Google: {google_urls}')
                else:
                    print(f'    sameAs: {same_as}')
                print(f'    aggregateRating presente: {has_rating}')
                print(f'    fonte verificável: {verified}')


if __name__ == '__main__':
    for page in ['index.html', 'almoco.html', 'almoco-morro-da-urca.html']:
        check_file(page)
