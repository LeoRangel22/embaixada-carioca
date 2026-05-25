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
BASE_CSS = 'ec-stabilization-base.css'

STYLE_RE = re.compile(r'<style[^>]*>(.*?)</style>', re.I | re.S)
LINK_RE = re.compile(r'<link[^>]+href=["\']([^"\']+)["\'][^>]*>', re.I)
CLASS_RE = re.compile(r'class=["\'][^"\']*(?:green-section|section-green|ec-green-solid|bg-green|verde-section|cafe-green|breakfast-green|menu-green)[^"\']*["\']', re.I)
REAL_BACKGROUND_RE = re.compile(
    r'(?:background|background-color)\s*:\s*(?:var\(--verde\)|var\(--ec-green-solid\)|#152f22|#153022|#0f2b1f|#102f22|#0e2a20|#123321|linear-gradient\([^;{}]*(?:#152f22|#153022|var\(--verde\)|var\(--ec-green-solid\)))',
    re.I,
)


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


def stripped_css_declarations(html: str) -> str:
    parts = []
    for match in STYLE_RE.finditer(html):
        css = match.group(1)
        # Ignore custom property declarations in :root. They are color tokens, not actual green-background usage.
        css = re.sub(r':root\s*\{.*?\}', '', css, flags=re.I | re.S)
        parts.append(css)
    # Inline style attributes may contain real background declarations.
    parts.extend(re.findall(r'style=["\']([^"\']+)["\']', html, flags=re.I | re.S))
    return '\n'.join(parts)


def has_real_green_signal(html: str) -> tuple[bool, str]:
    css = stripped_css_declarations(html)
    if REAL_BACKGROUND_RE.search(css):
        return True, 'background declaration'
    if CLASS_RE.search(html):
        return True, 'semantic green class'
    return False, ''


def has_green_css(html: str) -> bool:
    return GREEN_CSS in html or 'ec-green-solid-palette.css' in html


def has_imported_base(html: str) -> bool:
    return BASE_CSS in html


def base_imports_green_palette() -> bool:
    base = ROOT / 'assets/css/ec-stabilization-base.css'
    if not base.exists():
        return False
    text = base.read_text(encoding='utf-8', errors='ignore')
    return 'ec-green-solid-palette.css' in text


def main() -> int:
    OUT.mkdir(exist_ok=True)
    files = html_files()
    base_has_green = base_imports_green_palette()
    results = []

    for path in files:
        html = path.read_text(encoding='utf-8', errors='ignore')
        green_signal, signal_source = has_real_green_signal(html)
        direct_green_css = has_green_css(html)
        base_css = has_imported_base(html)
        covered = direct_green_css or (base_css and base_has_green)
        status = 'OK'
        issues = []
        if green_signal and not covered:
            status = 'WARN'
            issues.append('Página tem fundo verde sólido real, mas não carrega o padrão verde sólido.')
        results.append({
            'file': rel(path),
            'status': status,
            'green_signal': green_signal,
            'signal_source': signal_source,
            'direct_green_css': direct_green_css,
            'base_css': base_css,
            'base_imports_green_palette': base_has_green,
            'covered': covered,
            'issues': issues,
        })

    warn = [r for r in results if r['status'] == 'WARN']
    status = 'PASS' if not warn else 'WARN'
    payload = {
        'status': status,
        'files_checked': len(results),
        'real_green_signal_pages': sum(1 for r in results if r['green_signal']),
        'pages_direct_green_css': sum(1 for r in results if r['direct_green_css']),
        'pages_with_base_css': sum(1 for r in results if r['base_css']),
        'base_imports_green_palette': base_has_green,
        'warnings': len(warn),
        'results': results,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

    lines = [
        '# Green Solid Palette Audit — Embaixada Carioca',
        '',
        f'Status: **{status}**',
        f'Arquivos HTML verificados: **{len(results)}**',
        f'Páginas com fundo verde sólido real: **{payload["real_green_signal_pages"]}**',
        f'Páginas com CSS verde importado diretamente: **{payload["pages_direct_green_css"]}**',
        f'Páginas com CSS base: **{payload["pages_with_base_css"]}**',
        f'CSS base importa padrão verde: **{base_has_green}**',
        f'Avisos: **{len(warn)}**',
        '',
        '## Critério eficiente',
        '- A auditoria ignora mera declaração de variável em `:root`, como `--verde`.',
        '- Só conta como sinal real: `background/background-color` verde aplicado ou classes semânticas de seção verde.',
        '- Página coberta = importa `ec-green-solid-palette.css` diretamente ou importa `ec-stabilization-base.css` quando este já importa o padrão verde.',
        '',
        '## Avisos',
    ]
    if warn:
        for row in warn:
            lines.append(f'- `{row["file"]}` — ' + '; '.join(row['issues']) + f' Fonte: {row["signal_source"]}.')
    else:
        lines.append('- Nenhum aviso.')
    lines += ['', '## Resumo por página']
    for row in results:
        lines.append(
            f"- `{row['file']}` — {row['status']} — green_signal={row['green_signal']} "
            f"source={row['signal_source'] or '-'} direct_green_css={row['direct_green_css']} base_css={row['base_css']} covered={row['covered']}"
        )
    REPORT_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(f'Green solid palette audit: {status} files={len(results)} warnings={len(warn)}')
    return 0 if not warn else 1


if __name__ == '__main__':
    raise SystemExit(main())
