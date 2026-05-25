#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
REPORT = OUT / 'eventos_page_polish_report.md'
TARGETS = [ROOT / 'eventos.html']

TEXT_REPLACEMENTS = [
    ('Corporate events e privados', 'Eventos corporativos e privados'),
    ('Dos universos, una vista', 'Dois universos, uma vista'),
    ('Del evento corporativo al itinerario premium', 'Do evento corporativo ao roteiro premium'),
    ('Nossa equipo responde', 'Nossa equipe responde'),
    ('nossa equipo responde', 'nossa equipe responde'),
    ('equipo de bar', 'equipe de bar'),
    ('Rooms 3 + terraços panorâmicos', 'Ambientes 3 + terraços panorâmicos'),
    ('Languages PT ESP·EN multilingual equipe receptiva', 'Idiomas PT · ES · EN equipe receptiva multilíngue'),
    ('Hoje Por do sol', 'Hoje Pôr do sol'),
    (' no alto do Morro da Urca, a 227 metros,', ' no Morro da Urca, a 227 metros,'),
    (' — no alto do Morro da Urca, com vista', ' — no Morro da Urca, com vista'),
    (' — no alto do Morro da Urca, Rio de Janeiro.', ' — no Morro da Urca, Rio de Janeiro.'),
]

URL_REPLACEMENTS = [
    ('https://www.embaixadacarioca.com/eventos#venue', 'https://www.embaixadacarioca.com/eventos.html#venue'),
    ('https://www.embaixadacarioca.com/eventos"', 'https://www.embaixadacarioca.com/eventos.html"'),
    ('https://www.embaixadacarioca.com/eventos<', 'https://www.embaixadacarioca.com/eventos.html<'),
]

JSONLD_RE = re.compile(r'(<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)


def normalize_jsonld(html: str, changes: list[str]) -> str:
    def repl(match: re.Match[str]) -> str:
        open_tag, raw, close_tag = match.groups()
        try:
            obj = json.loads(raw.strip())
        except Exception:
            return match.group(0)
        before = json.dumps(obj, ensure_ascii=False, sort_keys=True)
        def walk(value):
            if isinstance(value, dict):
                for key, child in list(value.items()):
                    if key in {'@id', 'url', 'item'} and child == 'https://www.embaixadacarioca.com/eventos':
                        value[key] = 'https://www.embaixadacarioca.com/eventos.html'
                    elif key == '@id' and child == 'https://www.embaixadacarioca.com/eventos#venue':
                        value[key] = 'https://www.embaixadacarioca.com/eventos.html#venue'
                    elif isinstance(child, str):
                        fixed = child
                        for old, new in TEXT_REPLACEMENTS:
                            fixed = fixed.replace(old, new)
                        if fixed != child:
                            value[key] = fixed
                    else:
                        walk(child)
            elif isinstance(value, list):
                for item in value:
                    walk(item)
        walk(obj)
        after = json.dumps(obj, ensure_ascii=False, sort_keys=True)
        if before != after:
            changes.append('JSON-LD normalizado: textos mistos e URLs /eventos → /eventos.html')
            return open_tag + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + close_tag
        return match.group(0)
    return JSONLD_RE.sub(repl, html)


def polish_file(path: Path) -> list[str]:
    html = path.read_text(encoding='utf-8', errors='ignore')
    changes: list[str] = []
    updated = html
    for old, new in TEXT_REPLACEMENTS + URL_REPLACEMENTS:
        if old in updated:
            updated = updated.replace(old, new)
            changes.append(f'Trocado: {old} → {new}')
    updated = normalize_jsonld(updated, changes)
    if updated != html:
        path.write_text(updated, encoding='utf-8')
    return changes


def main() -> int:
    OUT.mkdir(exist_ok=True)
    lines = ['# Eventos Page Polish Report', '']
    total = 0
    for path in TARGETS:
        if not path.exists():
            lines.append(f'- `{path.relative_to(ROOT)}` — arquivo não encontrado')
            continue
        changes = polish_file(path)
        total += len(changes)
        lines.append(f'## `{path.relative_to(ROOT)}`')
        if changes:
            for change in changes:
                lines.append(f'- {change}')
        else:
            lines.append('- Nenhuma alteração necessária.')
        lines.append('')
    lines.insert(1, f'Total de ajustes aplicados: **{total}**')
    REPORT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Eventos page polish completed: changes={total}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
