#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
REPORT_MD = OUT / 'schema_jsonld_duplicate_key_report.md'
REPORT_JSON = OUT / 'schema_jsonld_duplicate_key_report.json'

SKIP_DIRS = {'.git', '.github', 'node_modules', 'dist', 'build', '_site', '_audit_reports', 'archive'}
SCRIPT_RE = re.compile(r'(<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)


@dataclass
class Finding:
    file: str
    block: int
    key: str
    count: int


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def html_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob('*.html'):
        if not path.is_file():
            continue
        parts = set(path.relative_to(ROOT).parts)
        if parts & SKIP_DIRS:
            continue
        files.append(path)
    return sorted(files, key=rel)


def duplicate_tracking_hook(file_rel: str, block_no: int, findings: list[Finding]):
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        counts: dict[str, int] = {}
        out: dict[str, Any] = {}
        for key, value in pairs:
            counts[key] = counts.get(key, 0) + 1
            out[key] = value
        for key, count in counts.items():
            if count > 1:
                findings.append(Finding(file_rel, block_no, key, count))
        return out
    return hook


def process_file(path: Path, fix: bool) -> tuple[bool, list[Finding], int, int]:
    file_rel = rel(path)
    html = path.read_text(encoding='utf-8', errors='ignore')
    findings: list[Finding] = []
    invalid = 0
    block_count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal invalid, block_count
        block_count += 1
        open_tag, raw_json, close_tag = match.groups()
        local_findings: list[Finding] = []
        try:
            obj = json.loads(raw_json.strip(), object_pairs_hook=duplicate_tracking_hook(file_rel, block_count, local_findings))
        except Exception:
            invalid += 1
            return match.group(0)
        findings.extend(local_findings)
        if fix and local_findings:
            return open_tag + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + close_tag
        return match.group(0)

    new_html = SCRIPT_RE.sub(repl, html)
    changed = fix and new_html != html
    if changed:
        path.write_text(new_html, encoding='utf-8')
    return changed, findings, block_count, invalid


def write_reports(rows: list[dict[str, Any]], findings: list[Finding], mode: str, status: str) -> None:
    OUT.mkdir(exist_ok=True)
    REPORT_JSON.write_text(json.dumps({
        'status': status,
        'mode': mode,
        'files_checked': len(rows),
        'findings_count': len(findings),
        'files': rows,
        'findings': [asdict(f) for f in findings],
    }, ensure_ascii=False, indent=2), encoding='utf-8')

    lines = [
        '# JSON-LD Duplicate Key Guard Report',
        '',
        f'Status: **{status}**',
        f'Mode: **{mode}**',
        f'Arquivos HTML verificados: **{len(rows)}**',
        f'Achados: **{len(findings)}**',
        '',
        '## Regra',
        '- Nenhum objeto JSON-LD deve repetir a mesma chave dentro do mesmo objeto.',
        '- Exemplo de alerta do Google: `O campo url está duplicado (opcional)`.',
        '- Em modo `fix`, o JSON-LD é reserializado e a última ocorrência da chave é preservada.',
        '',
        '## Achados',
    ]
    if findings:
        for f in findings[:300]:
            lines.append(f'- `{f.file}` bloco {f.block} — chave duplicada `{f.key}` apareceu {f.count} vezes')
    else:
        lines.append('- Nenhum campo duplicado encontrado.')
    lines += ['', '## Arquivos']
    for row in rows:
        mark = 'alterado' if row['changed'] else 'ok'
        lines.append(f"- `{row['file']}` — {mark} — blocos JSON-LD: {row['jsonld_blocks']} — inválidos: {row['invalid_blocks']}")
    REPORT_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description='Audit/fix duplicate keys inside JSON-LD blocks.')
    parser.add_argument('--fix', action='store_true', help='Normalize JSON-LD blocks with duplicate keys.')
    parser.add_argument('--check', action='store_true', help='Audit only and fail if duplicate keys are found.')
    args = parser.parse_args()
    fix = bool(args.fix)
    mode = 'fix' if fix else 'check'

    rows: list[dict[str, Any]] = []
    findings: list[Finding] = []
    for path in html_files():
        changed, file_findings, block_count, invalid = process_file(path, fix=fix)
        rows.append({'file': rel(path), 'changed': changed, 'jsonld_blocks': block_count, 'invalid_blocks': invalid})
        findings.extend(file_findings)

    remaining: list[Finding] = []
    if fix:
        for path in html_files():
            _, file_findings, _, _ = process_file(path, fix=False)
            remaining.extend(file_findings)
    else:
        remaining = findings

    status = 'PASS' if not remaining else 'FAIL'
    write_reports(rows, findings, mode, status)
    print(f'JSON-LD duplicate key guard: {status} mode={mode} files={len(rows)} findings={len(findings)} remaining={len(remaining)}')
    return 0 if status == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
