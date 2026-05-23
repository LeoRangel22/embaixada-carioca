#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re
import shutil
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / '_audit_reports'
LEGACY_ROOT = ROOT / 'archive' / 'legacy'
STAMP = datetime.now(timezone.utc).strftime('%Y%m%d')
LEGACY_DIR = LEGACY_ROOT / STAMP

REPORT_MD = REPORT_DIR / 'repo_hygiene_report.md'
REPORT_JSON = REPORT_DIR / 'repo_hygiene_report.json'

EXCLUDED_DIRS = {'.git', 'node_modules', 'dist', 'build', '_site', '.next', '.cache'}
CONFIG_DEAD_ON_GH_PAGES = {'.htaccess', '_headers'}
ONE_OFF_PATTERNS = [
    re.compile(r'(^|/)fix[_\-].*\.py$', re.I),
    re.compile(r'(^|/)patch[_\-].*\.py$', re.I),
    re.compile(r'(^|/)quick[_\-].*\.py$', re.I),
    re.compile(r'(^|/)tmp[_\-].*\.py$', re.I),
    re.compile(r'(^|/)temp[_\-].*\.py$', re.I),
    re.compile(r'(^|/)cleanup[_\-].*\.py$', re.I),
    re.compile(r'(^|/)repair[_\-].*\.py$', re.I),
]

ALWAYS_ACTIVE = {
    'scripts/apply_p0_schema_jsonld.py',
    'scripts/audit_p0_schema_jsonld.py',
    'scripts/apply_hreflang_pt_en_es.py',
    'scripts/audit_hreflang_pt_en_es.py',
    'scripts/apply_geo_cluster_deduplication.py',
    'scripts/audit_geo_cluster_deduplication.py',
    'scripts/apply_multilingual_continuous_optimization.py',
    'scripts/audit_multilingual_ai_search_score.py',
    'scripts/super_site_standards_seo_audit.py',
    'scripts/audit_language_quality_pt_en_es.py',
    'scripts/repo_hygiene_archive_legacy.py',
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def iter_files() -> list[Path]:
    files = []
    for p in ROOT.rglob('*'):
        if not p.is_file():
            continue
        parts = set(p.relative_to(ROOT).parts)
        if parts & EXCLUDED_DIRS:
            continue
        files.append(p)
    return sorted(files, key=lambda x: rel(x))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return ''


def workflow_references() -> set[str]:
    refs: set[str] = set()
    workflow_dir = ROOT / '.github' / 'workflows'
    if not workflow_dir.exists():
        return refs
    for wf in workflow_dir.glob('*.yml'):
        text = read_text(wf)
        for match in re.findall(r'scripts/[A-Za-z0-9_./\-]+\.py', text):
            refs.add(match.strip())
    for wf in workflow_dir.glob('*.yaml'):
        text = read_text(wf)
        for match in re.findall(r'scripts/[A-Za-z0-9_./\-]+\.py', text):
            refs.add(match.strip())
    return refs


def is_one_off(relpath: str) -> bool:
    return any(pattern.search(relpath) for pattern in ONE_OFF_PATTERNS)


def classify_file(path: Path, active_refs: set[str]) -> dict:
    rp = rel(path)
    name = path.name
    if rp in active_refs or rp in ALWAYS_ACTIVE:
        kind = 'active_script'
        reason = 'Referenced by workflow or active SEO/GEO/audit allowlist.'
    elif rp.startswith('scripts/') and name.startswith('audit_') and name.endswith('.py'):
        kind = 'audit_script'
        reason = 'Audit script not directly referenced by workflow; keep under scripts unless later archived manually.'
    elif rp.startswith('scripts/') and name.startswith('apply_') and name.endswith('.py'):
        kind = 'active_candidate'
        reason = 'Applicator script; review before archiving.'
    elif name in CONFIG_DEAD_ON_GH_PAGES and '/' not in rp:
        kind = 'dead_config'
        reason = 'Ignored by GitHub Pages static hosting in this setup.'
    elif is_one_off(rp):
        kind = 'obsolete_one_off_script'
        reason = 'One-off maintenance script pattern and not referenced by workflow.'
    elif rp.endswith('.py') and not rp.startswith('scripts/'):
        kind = 'python_outside_scripts'
        reason = 'Python script outside /scripts; move to scripts or archive after review.'
    else:
        kind = 'keep'
        reason = 'No cleanup rule matched.'
    return {'path': rp, 'kind': kind, 'reason': reason}


def target_for(src: Path) -> Path:
    rp = rel(src)
    return LEGACY_DIR / rp


def move_to_legacy(path: Path) -> str:
    dst = target_for(path)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        i = 1
        while True:
            candidate = dst.with_name(dst.stem + f'-{i}' + dst.suffix)
            if not candidate.exists():
                dst = candidate
                break
            i += 1
    shutil.move(str(path), str(dst))
    return rel(dst)


def main() -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    active_refs = workflow_references()
    files = iter_files()
    rows = [classify_file(p, active_refs) for p in files]
    moved = []
    for row in rows:
        if row['kind'] in {'dead_config', 'obsolete_one_off_script'}:
            src = ROOT / row['path']
            if src.exists():
                moved.append({'from': row['path'], 'to': move_to_legacy(src), 'kind': row['kind'], 'reason': row['reason']})
    # Reclassify after moves for final report.
    final_files = iter_files()
    final_rows = [classify_file(p, active_refs) for p in final_files]
    groups = {}
    for row in final_rows:
        groups.setdefault(row['kind'], []).append(row)
    payload = {'status': 'PASS', 'moved': moved, 'active_workflow_references': sorted(active_refs), 'groups': groups}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = [
        '# Repo Hygiene Report',
        '',
        'Status: **PASS**',
        '',
        '## O que foi feito',
        '- Listagem real dos arquivos do repositório no momento da execução.',
        '- Separação de scripts ativos, auditorias, candidatos ativos e scripts obsoletos.',
        '- Movidos para `archive/legacy/` apenas arquivos com regra segura: `.htaccess`, `_headers` e scripts one-off `fix_`, `patch_`, `quick_`, `tmp_`, `temp_`, `cleanup_`, `repair_` sem referência em workflow.',
        '- Nada referenciado por workflow foi movido.',
        '',
        f'Arquivos movidos: **{len(moved)}**',
        '',
        '## Movidos para archive/legacy',
    ]
    if moved:
        for item in moved:
            lines.append(f"- `{item['from']}` → `{item['to']}` — {item['kind']}")
    else:
        lines.append('- Nenhum arquivo morto seguro encontrado para mover.')
    lines += ['', '## Scripts ativos por workflow/allowlist']
    for item in groups.get('active_script', []):
        lines.append(f"- `{item['path']}` — {item['reason']}")
    lines += ['', '## Auditorias não referenciadas diretamente']
    for item in groups.get('audit_script', []):
        lines.append(f"- `{item['path']}` — {item['reason']}")
    lines += ['', '## Aplicadores candidatos ativos']
    for item in groups.get('active_candidate', []):
        lines.append(f"- `{item['path']}` — {item['reason']}")
    lines += ['', '## Python fora de /scripts']
    for item in groups.get('python_outside_scripts', []):
        lines.append(f"- `{item['path']}` — {item['reason']}")
    REPORT_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Repo hygiene completed. moved={len(moved)}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
