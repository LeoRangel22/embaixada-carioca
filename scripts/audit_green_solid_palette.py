#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
REPORT_MD = OUT / 'green_solid_palette_audit_report.md'
REPORT_JSON = OUT / 'green_solid_palette_audit_report.json'
SKIP_DIRS = {'.git', '.github', '_audit_reports', 'archive', 'node_modules', 'dist', 'build'}
GREEN_CSS = '/assets/css/ec-green-solid-palette.css'
GREEN_SIGNALS = [
    'var(--verde)',
    'background:#152f22',
    'background: #152f22',
    'background-color:#152f22',
    'background-color: #152f22',
    'background:#153022',
    'background: #153022',
    'green-section',
    'section-green',
    'ec-green-solid',
    'bg-green',
    'verde-section',
    'cafe-green',
    'breakfast-green',
    'menu-green',
    'feijoada',
    'reservas',
]

STYLE_RE = re.compile(r'<style[^>]*>(.*?)</style>', re.I | re.S)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def html_files() -> list[Path]:
    files = []
    for path in ROOT.rglob('*.html'):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files, key=rel)


def has_green_signal(html: str) -> bool:
    normalized = html.replace(' ', '').lower()
    for signal in GREEN_SIGNALS:
        if signal.replace(' ', '').lower() in normalized:
            return True
    return False


def has_green_css(html: str) -> bool:
    return GREEN_CSS in html or 'ec-green-solid-palette.css' in html


def has_imported_base(html: str) -> bool:
    return 'ec-stabilization-base.css' in html


def inline_palette_rules(html: str) -> bool:
    return 'Green Solid Palette Standard' in html or 'ec-green-solid' in html


def inject_green_css(html: str) -> tuple[str, bool]:
    if has_green_css(html):
        return html, False
    link = f'<link rel="stylesheet" href="{GREEN_CSS}">\n'
    if '</head>' in html:
        return html.replace('</head>', link + '</head>', 1), True
    return html, False


def main() -> int:
    OUT.mkdir(exist_ok=True)
    files = html_files()
    results = []
    for path in files:
        html = path.read_text(encoding='utf-8', errors='ignore')
        green_signal = has_green_signal(html)
        green_css = has_green_css(html)
        base_css = has_imported_base(html)
        inline_rules = inline_palette_rules(html)
        status = 'OK'
        issues = []
        if green_signal and not (green_css or base_css or inline_rules):
            status = 'WARN'
            issues.append('Página tem sinal de fundo verde, mas não carrega o padrão verde sólido.')
        results.append({
            'file': rel(path),
            'status': status,
            'green_signal': green_signal,
            'green_css': green_css,
            'base_css': base_css,
            'inline_rules': inline_rules,
            'issues': issues,
        })

    warn = [r for r in results if r['status'] == 'WARN']
    status = 'PASS' if not warn else 'WARN'
    payload = {
        'status': status,
        'files_checked': len(results),
        'green_signal_pages': sum(1 for r in results if r['green_signal']),
        'pages_with_green_css': sum(1 for r in results if r['green_css']),
        'pages_with_base_css': sum(1 for r in results if r['base_css']),
        'warnings': len(warn),
        'results': results,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

    lines = [
        '# Green Solid Palette Audit — Embaixada Carioca',
        '',
        f'Status: **{status}**',
        f'Arquivos HTML verificados: **{len(results)}**',
        f'Páginas com sinal de fundo verde: **{payload["green_signal_pages"]}**',
        f'Páginas com CSS verde importado diretamente: **{payload["pages_with_green_css"]}**',
        f'Páginas com CSS base: **{payload["pages_with_base_css"]}**',
        f'Avisos: **{len(warn)}**',
        '',
        '## Regra',
        '- Toda página com fundo verde sólido deve carregar o padrão `ec-green-solid-palette.css` direta ou indiretamente.',
        '- O padrão define fundo verde escuro, texto creme, destaques amarelos, cards internos verde mais claro e divisórias suaves.',
        '',
        '## Avisos',
    ]
    if warn:
        for row in warn:
            lines.append(f'- `{row["file"]}` — ' + '; '.join(row['issues']))
    else:
        lines.append('- Nenhum aviso.')
    lines += ['', '## Resumo por página']
    for row in results:
        lines.append(f"- `{row['file']}` — {row['status']} — green_signal={row['green_signal']} green_css={row['green_css']} base_css={row['base_css']}")
    REPORT_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(f'Green solid palette audit: {status} files={len(results)} warnings={len(warn)}')
    return 0 if not warn else 1


if __name__ == '__main__':
    raise SystemExit(main())
