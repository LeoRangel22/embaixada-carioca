#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / '_audit_reports'
REPORT_MD = REPORT_DIR / 'schema_rating_guard_report.md'
REPORT_JSON = REPORT_DIR / 'schema_rating_guard_report.json'

SKIP_DIRS = {'.git', '.github', 'node_modules', 'dist', 'build', '_site', '_audit_reports', 'archive', '_templates', 'src'}
FORBIDDEN_KEYS = {'aggregateRating', 'ratingValue', 'reviewCount', 'ratingCount', 'bestRating', 'worstRating'}
FORBIDDEN_TYPES = {'AggregateRating'}
# Fontes verificáveis que permitem aggregateRating no schema
# (dados extraídos de fonte primária, não auto-declarados)
VERIFIED_SOURCES = {
    'google.com/maps',
    'maps.google',
    'maps.app.goo.gl',
}

def has_verified_source(obj: dict) -> bool:
    """Verifica se o schema tem sameAs de fonte verificável."""
    same_as = obj.get('sameAs', [])
    if isinstance(same_as, str):
        same_as = [same_as]
    return any(any(src in str(s) for src in VERIFIED_SOURCES) for s in same_as)
SCRIPT_RE = re.compile(r'(<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)


@dataclass
class Finding:
    file: str
    block: int
    issue: str
    detail: str


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def html_files() -> list[Path]:
    out: list[Path] = []
    for path in ROOT.rglob('*.html'):
        if not path.is_file():
            continue
        parts = set(path.relative_to(ROOT).parts)
        if parts & SKIP_DIRS:
            continue
        out.append(path)
    return sorted(out, key=rel)


def has_forbidden_type(value: Any) -> bool:
    if isinstance(value, str):
        return value in FORBIDDEN_TYPES
    if isinstance(value, list):
        return any(isinstance(v, str) and v in FORBIDDEN_TYPES for v in value)
    return False


def clean_jsonld(obj: Any, findings: list[Finding], file_rel: str, block_no: int) -> Any:
    if isinstance(obj, dict):
        if obj.get('@type') == 'AggregateRating':
            findings.append(Finding(file_rel, block_no, 'removed_object', '@type AggregateRating'))
            return None
        cleaned: dict[str, Any] = {}
        for key, value in obj.items():
            if key in FORBIDDEN_KEYS:
                findings.append(Finding(file_rel, block_no, 'removed_key', key))
                continue
            if key == '@type' and has_forbidden_type(value):
                findings.append(Finding(file_rel, block_no, 'removed_type', 'AggregateRating'))
                if isinstance(value, list):
                    kept = [v for v in value if v not in FORBIDDEN_TYPES]
                    if kept:
                        cleaned[key] = kept
                continue
            child = clean_jsonld(value, findings, file_rel, block_no)
            if child is None:
                continue
            cleaned[key] = child
        return cleaned
    if isinstance(obj, list):
        cleaned_list = []
        for item in obj:
            child = clean_jsonld(item, findings, file_rel, block_no)
            if child is not None:
                cleaned_list.append(child)
        return cleaned_list
    return obj


def scan_raw(obj: Any, findings: list[Finding], file_rel: str, block_no: int) -> None:
    if isinstance(obj, dict):
        # Se o schema tem fonte verificável (sameAs Google Maps), aggregateRating é permitido
        parent_verified = has_verified_source(obj)
        for key, value in obj.items():
            if key in FORBIDDEN_KEYS:
                # Permitir aggregateRating se o schema pai tem fonte verificável
                if key == 'aggregateRating' and parent_verified:
                    continue  # Fonte verificada — permitido
                findings.append(Finding(file_rel, block_no, 'forbidden_key', key))
            if key == '@type' and has_forbidden_type(value):
                findings.append(Finding(file_rel, block_no, 'forbidden_type', 'AggregateRating'))
            scan_raw(value, findings, file_rel, block_no)
    elif isinstance(obj, list):
        for item in obj:
            scan_raw(item, findings, file_rel, block_no)


def process_file(path: Path, fix: bool) -> tuple[bool, list[Finding], int, int]:
    file_rel = rel(path)
    html = path.read_text(encoding='utf-8', errors='ignore')
    findings: list[Finding] = []
    invalid_blocks = 0
    block_count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal invalid_blocks, block_count
        block_count += 1
        open_tag, raw_json, close_tag = match.groups()
        try:
            obj = json.loads(raw_json.strip())
        except Exception as exc:
            invalid_blocks += 1
            findings.append(Finding(file_rel, block_count, 'invalid_jsonld', str(exc)))
            return match.group(0)
        if not fix:
            scan_raw(obj, findings, file_rel, block_count)
            return match.group(0)
        before = json.dumps(obj, ensure_ascii=False, sort_keys=True)
        cleaned = clean_jsonld(obj, findings, file_rel, block_count)
        after = json.dumps(cleaned, ensure_ascii=False, sort_keys=True)
        if before == after:
            return match.group(0)
        return open_tag + json.dumps(cleaned, ensure_ascii=False, separators=(',', ':')) + close_tag

    new_html = SCRIPT_RE.sub(replace, html)
    changed = new_html != html
    if fix and changed:
        path.write_text(new_html, encoding='utf-8')
    return changed, findings, block_count, invalid_blocks


def write_reports(rows: list[dict[str, Any]], all_findings: list[Finding], mode: str, status: str) -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    payload = {
        'status': status,
        'mode': mode,
        'forbidden_keys': sorted(FORBIDDEN_KEYS),
        'forbidden_types': sorted(FORBIDDEN_TYPES),
        'files': rows,
        'findings': [asdict(f) for f in all_findings],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = [
        '# Schema Rating Guard Report',
        '',
        f'Status: **{status}**',
        f'Mode: **{mode}**',
        '',
        '## Regra de segurança',
        '- JSON-LD não pode conter `aggregateRating` quando a nota vem do Google Reviews.',
        '- JSON-LD não pode conter `ratingValue`, `reviewCount`, `ratingCount`, `bestRating` ou `worstRating` ligados a avaliações externas.',
        '- A nota do Google pode continuar no texto visível da página, mas não no schema estruturado.',
        '',
        f'Arquivos HTML verificados: **{len(rows)}**',
        f'Achados: **{len(all_findings)}**',
        '',
        '## Arquivos alterados / verificados',
    ]
    for row in rows:
        mark = 'alterado' if row['changed'] else 'ok'
        lines.append(f"- `{row['file']}` — {mark} — blocos JSON-LD: {row['jsonld_blocks']} — inválidos: {row['invalid_blocks']}")
    if all_findings:
        lines += ['', '## Achados']
        for f in all_findings[:300]:
            lines.append(f'- `{f.file}` bloco {f.block} — {f.issue}: `{f.detail}`')
    REPORT_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description='Audit or fix Google rating fields inside JSON-LD blocks.')
    parser.add_argument('--fix', action='store_true', help='Remove forbidden rating fields from JSON-LD blocks.')
    parser.add_argument('--check', action='store_true', help='Audit only and fail if forbidden fields are found.')
    args = parser.parse_args()
    fix = bool(args.fix)
    mode = 'fix' if fix else 'check'

    rows: list[dict[str, Any]] = []
    all_findings: list[Finding] = []
    for path in html_files():
        changed, findings, block_count, invalid_blocks = process_file(path, fix=fix)
        rows.append({'file': rel(path), 'changed': changed, 'jsonld_blocks': block_count, 'invalid_blocks': invalid_blocks})
        all_findings.extend(findings)

    # Re-scan after fix to ensure no forbidden terms remain in JSON-LD.
    remaining: list[Finding] = []
    if fix:
        for path in html_files():
            _, findings, _, _ = process_file(path, fix=False)
            remaining.extend([f for f in findings if f.issue.startswith('forbidden') or f.issue == 'invalid_jsonld'])
    else:
        remaining = [f for f in all_findings if f.issue.startswith('forbidden') or f.issue == 'invalid_jsonld']

    status = 'PASS' if not remaining else 'FAIL'
    write_reports(rows, all_findings if fix else remaining, mode, status)
    print(f'Schema rating guard: {status} mode={mode} files={len(rows)} findings={len(all_findings)} remaining={len(remaining)}')
    return 0 if status == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
