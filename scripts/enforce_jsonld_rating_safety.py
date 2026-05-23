#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
REPORT = OUT / 'jsonld_rating_safety_report.md'
REPORT_JSON = OUT / 'jsonld_rating_safety_report.json'

SCRIPT_RE = re.compile(r'(<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)
FORBIDDEN_KEYS = {'aggregateRating', 'ratingValue', 'reviewCount', 'ratingCount', 'bestRating', 'worstRating'}
FORBIDDEN_TYPES = {'AggregateRating'}
SKIP_DIRS = {'.git', 'node_modules', 'dist', 'build', '_audit_reports', 'archive'}


def html_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob('*.html'):
        rel_parts = set(path.relative_to(ROOT).parts)
        if rel_parts & SKIP_DIRS:
            continue
        files.append(path)
    return sorted(files)


def clean_obj(obj: Any, removed: list[str]) -> Any:
    if isinstance(obj, dict):
        cleaned: dict[str, Any] = {}
        for key, value in obj.items():
            if key in FORBIDDEN_KEYS:
                removed.append(key)
                continue
            if key == '@type':
                if isinstance(value, str) and value in FORBIDDEN_TYPES:
                    removed.append(value)
                    continue
                if isinstance(value, list):
                    new_types = [v for v in value if v not in FORBIDDEN_TYPES]
                    if len(new_types) != len(value):
                        removed.append('AggregateRating')
                    if not new_types:
                        continue
                    cleaned[key] = new_types
                    continue
            cleaned[key] = clean_obj(value, removed)
        return cleaned
    if isinstance(obj, list):
        return [clean_obj(item, removed) for item in obj]
    return obj


def clean_html(path: Path) -> dict[str, Any]:
    html = path.read_text(encoding='utf-8', errors='ignore')
    removed: list[str] = []
    invalid = 0
    blocks = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal invalid, blocks
        open_tag, payload, close_tag = match.groups()
        try:
            data = json.loads(payload.strip())
        except Exception:
            invalid += 1
            return match.group(0)
        blocks += 1
        cleaned = clean_obj(data, removed)
        return open_tag + '\n' + json.dumps(cleaned, ensure_ascii=False, indent=2) + '\n' + close_tag

    new_html = SCRIPT_RE.sub(repl, html)
    changed = new_html != html
    if changed:
        path.write_text(new_html, encoding='utf-8')
    return {
        'path': path.relative_to(ROOT).as_posix(),
        'changed': changed,
        'blocks': blocks,
        'invalid_blocks': invalid,
        'removed': sorted(set(removed)),
    }


def main() -> int:
    OUT.mkdir(exist_ok=True)
    rows = [clean_html(path) for path in html_files()]
    changed = [row for row in rows if row['changed']]
    with_remaining: list[str] = []
    forbidden_pattern = re.compile(r'aggregateRating|ratingValue|reviewCount|ratingCount|bestRating|worstRating|AggregateRating')
    for path in html_files():
        text = path.read_text(encoding='utf-8', errors='ignore')
        if forbidden_pattern.search(text):
            with_remaining.append(path.relative_to(ROOT).as_posix())
    status = 'PASS' if not with_remaining else 'FAIL'
    REPORT_JSON.write_text(json.dumps({'status': status, 'changed': changed, 'remaining': with_remaining, 'results': rows}, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = [
        '# JSON-LD Rating Safety Report',
        '',
        f'Status: **{status}**',
        '',
        '## Regra aplicada',
        '- Remover `aggregateRating` do JSON-LD quando a nota vem de Google Reviews.',
        '- Remover também `ratingValue`, `reviewCount`, `ratingCount`, `bestRating`, `worstRating` e `AggregateRating`.',
        '- A nota pode permanecer no texto visível da página, mas não no schema.',
        '',
        f'Arquivos HTML alterados: **{len(changed)}**',
        '',
        '## Alterados',
    ]
    if changed:
        for row in changed:
            lines.append(f"- `{row['path']}` — removido: {', '.join(row['removed']) or 'campos de rating'}")
    else:
        lines.append('- Nenhum arquivo precisou de alteração.')
    if with_remaining:
        lines += ['', '## Ainda com campos proibidos']
        lines += [f'- `{path}`' for path in with_remaining]
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'JSON-LD rating safety: {status} changed={len(changed)} remaining={len(with_remaining)}')
    return 0 if status == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
