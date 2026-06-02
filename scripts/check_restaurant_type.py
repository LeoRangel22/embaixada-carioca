#!/usr/bin/env python3
"""Verifica o problema restaurant_type_array nas páginas."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_RE = re.compile(r'(<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)

pages = [
    'index.html', 'morro-da-urca.html', 'parque-bondinho.html',
    'en/index.html', 'nossa-visao.html', 'en/morro-da-urca.html',
    'en/parque-bondinho.html', 'es/index.html', 'es/morro-da-urca.html',
    'es/parque-bondinho.html', 'contato.html', 'en/contato.html',
    'es/contato.html', 'en/nossa-visao.html', 'es/nossa-visao.html',
    'caipirinha-com-vista-rio.html', 'en/caipirinha-com-vista-rio.html',
    'es/caipirinha-com-vista-rio.html',
]

def walk(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk(item)

for page in pages:
    path = ROOT / page
    if not path.exists():
        continue
    html = path.read_text(encoding='utf-8', errors='ignore')
    for i, m in enumerate(SCRIPT_RE.finditer(html)):
        raw = m.group(2).strip()
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        for node in walk(obj):
            if not isinstance(node, dict):
                continue
            t = node.get('@type', '')
            if isinstance(t, list) and 'Restaurant' in t:
                print(f'{page} bloco {i+1}: @type = {t}')
