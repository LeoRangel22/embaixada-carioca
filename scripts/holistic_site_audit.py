#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
REPORT_MD = OUT / 'holistic_site_audit_report.md'
REPORT_JSON = OUT / 'holistic_site_audit_report.json'
BASE_HOSTS = {'www.embaixadacarioca.com', 'embaixadacarioca.com'}
SKIP_DIRS = {'.git', '.github', 'node_modules', 'dist', 'build', '_site', '_audit_reports', 'archive'}
FORBIDDEN_RATING_KEYS = {'aggregateRating', 'ratingValue', 'reviewCount', 'ratingCount', 'bestRating', 'worstRating'}
FORBIDDEN_RATING_TYPES = {'AggregateRating'}
JSONLD_RE = re.compile(r'<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
TAG_RE = re.compile(r'<(?P<tag>[a-zA-Z0-9]+)\b(?P<attrs>[^>]*)>', re.I | re.S)
ATTR_RE = re.compile(r'([a-zA-Z_:.-]+)\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+)')

P0_PAGES = {
    'index.html', 'en/index.html', 'es/index.html',
    'cardapio.html', 'en/cardapio.html', 'es/cardapio.html',
    'almoco.html', 'en/almoco.html', 'es/almoco.html',
    'cafe-da-manha.html', 'en/cafe-da-manha.html', 'es/cafe-da-manha.html',
    'eventos.html', 'en/eventos.html', 'es/eventos.html',
    'restaurante-morro-da-urca.html', 'es/restaurante-morro-da-urca.html',
    'guia-do-rio.html', 'en/guia-do-rio.html', 'es/guia-do-rio.html',
}

LANGUAGE_PATTERNS = [
    ('bad_english_do_breakfast', re.compile(r'\bDo breakfast\b', re.I), 'Use “Breakfast” or “Have breakfast”, not “Do breakfast”.'),
    ('wrong_location_top_sugarloaf_en', re.compile(r'\btop of Sugarloaf\b', re.I), 'Use Urca Hill / first cable car stop, not top of Sugarloaf.'),
    ('wrong_location_top_sugarloaf_pt', re.compile(r'\btopo do P[ãa]o de A[çc][úu]car\b', re.I), 'Use Morro da Urca / primeira parada do Bondinho.'),
    ('wrong_location_top_sugarloaf_es', re.compile(r'\bcima del Pan de Az[úu]car\b|\bcima do P[ãa]o de A[çc][úu]car\b', re.I), 'Use Morro da Urca / primera parada del Bondinho.'),
]


@dataclass
class Finding:
    severity: str
    file: str
    category: str
    detail: str


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


def attrs_to_dict(raw: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for key, val in ATTR_RE.findall(raw or ''):
        val = val.strip()
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]
        attrs[key.lower()] = val
    return attrs


def tags(html: str, name: str) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for match in TAG_RE.finditer(html):
        if match.group('tag').lower() == name.lower():
            out.append(attrs_to_dict(match.group('attrs')))
    return out


def title_text(html: str) -> str:
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''


def meta_content(html: str, name: str) -> str:
    for item in tags(html, 'meta'):
        if item.get('name', '').lower() == name.lower() or item.get('property', '').lower() == name.lower():
            return item.get('content', '').strip()
    return ''


def canonical_links(html: str) -> list[str]:
    links = []
    for item in tags(html, 'link'):
        rels = set(item.get('rel', '').lower().split())
        if 'canonical' in rels and item.get('href'):
            links.append(item['href'].strip())
    return links


def hreflang_links(html: str) -> list[tuple[str, str]]:
    out = []
    for item in tags(html, 'link'):
        rels = set(item.get('rel', '').lower().split())
        if 'alternate' in rels and item.get('hreflang') and item.get('href'):
            out.append((item['hreflang'].strip(), item['href'].strip()))
    return out


def scan_jsonld(obj: Any, file_rel: str, block_no: int, findings: list[Finding]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in FORBIDDEN_RATING_KEYS:
                findings.append(Finding('critical', file_rel, 'schema_rating_forbidden', f'JSON-LD block {block_no}: forbidden key {key}'))
            if key == '@type':
                if isinstance(value, str) and value in FORBIDDEN_RATING_TYPES:
                    findings.append(Finding('critical', file_rel, 'schema_rating_forbidden', f'JSON-LD block {block_no}: forbidden @type {value}'))
                if isinstance(value, list) and any(v in FORBIDDEN_RATING_TYPES for v in value if isinstance(v, str)):
                    findings.append(Finding('critical', file_rel, 'schema_rating_forbidden', f'JSON-LD block {block_no}: forbidden @type AggregateRating'))
            scan_jsonld(value, file_rel, block_no, findings)
    elif isinstance(obj, list):
        for item in obj:
            scan_jsonld(item, file_rel, block_no, findings)


def jsonld_summary(html: str, file_rel: str, findings: list[Finding]) -> tuple[int, int]:
    invalid = 0
    blocks = JSONLD_RE.findall(html)
    for idx, raw in enumerate(blocks, start=1):
        try:
            obj = json.loads(raw.strip())
            scan_jsonld(obj, file_rel, idx, findings)
        except Exception as exc:
            invalid += 1
            findings.append(Finding('critical', file_rel, 'invalid_jsonld', f'JSON-LD block {idx}: {exc}'))
    return len(blocks), invalid


def expected_internal_path(current_file: Path, href: str) -> str | None:
    href = href.strip()
    if not href or href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:') or href.startswith('javascript:') or href.startswith('whatsapp:'):
        return None
    parsed = urlparse(href)
    if parsed.scheme in {'http', 'https'}:
        if parsed.netloc not in BASE_HOSTS:
            return None
        path = parsed.path
    else:
        path = href.split('#', 1)[0].split('?', 1)[0]
    if not path:
        return None
    if path.startswith('/'):
        candidate = path.lstrip('/')
    else:
        candidate = (current_file.parent / path).relative_to(ROOT).as_posix() if current_file.is_absolute() else path
    candidate = candidate.split('#', 1)[0].split('?', 1)[0]
    if not candidate or candidate.endswith('/'):
        candidate = candidate.rstrip('/') + '/index.html' if candidate.strip('/') else 'index.html'
    suffix = Path(candidate).suffix.lower()
    if suffix and suffix not in {'.html', '.htm'}:
        return None
    if not suffix:
        candidate_html = candidate + '.html'
        if (ROOT / candidate_html).exists():
            return candidate_html
        candidate_index = candidate.rstrip('/') + '/index.html'
        if (ROOT / candidate_index).exists():
            return candidate_index
        return candidate_html
    return candidate


def audit_file(path: Path) -> dict[str, Any]:
    file_rel = rel(path)
    html = path.read_text(encoding='utf-8', errors='ignore')
    findings: list[Finding] = []
    title = title_text(html)
    desc = meta_content(html, 'description')
    canonicals = canonical_links(html)
    hreflangs = hreflang_links(html)
    jsonld_blocks, invalid_jsonld = jsonld_summary(html, file_rel, findings)
    h1_count = len(re.findall(r'<h1\b', html, re.I))
    img_tags = tags(html, 'img')
    missing_alt = sum(1 for img in img_tags if not img.get('alt', '').strip())

    is_p0 = file_rel in P0_PAGES
    if is_p0:
        if not title:
            findings.append(Finding('critical', file_rel, 'missing_title', 'P0 page has no <title>.'))
        if not desc:
            findings.append(Finding('critical', file_rel, 'missing_meta_description', 'P0 page has no meta description.'))
        if not canonicals:
            findings.append(Finding('critical', file_rel, 'missing_canonical', 'P0 page has no canonical link.'))
        if jsonld_blocks == 0:
            findings.append(Finding('critical', file_rel, 'missing_jsonld', 'P0 page has no JSON-LD block.'))
    if title and not (20 <= len(title) <= 75):
        findings.append(Finding('warning', file_rel, 'title_length', f'Title length {len(title)} outside 20–75 chars.'))
    if desc and not (70 <= len(desc) <= 180):
        findings.append(Finding('warning', file_rel, 'description_length', f'Meta description length {len(desc)} outside 70–180 chars.'))
    if len(canonicals) > 1:
        findings.append(Finding('warning', file_rel, 'multiple_canonicals', f'{len(canonicals)} canonical links found.'))
    if file_rel not in {'404.html', 'offline.html', 'home-preview.html'} and len(hreflangs) == 0:
        findings.append(Finding('warning', file_rel, 'missing_hreflang', 'No hreflang alternate links found.'))
    if h1_count == 0:
        findings.append(Finding('warning', file_rel, 'missing_h1', 'No H1 found.'))
    elif h1_count > 1:
        findings.append(Finding('warning', file_rel, 'multiple_h1', f'{h1_count} H1 tags found.'))
    if missing_alt:
        findings.append(Finding('warning', file_rel, 'image_alt', f'{missing_alt} image(s) without alt text.'))
    for code, pattern, suggestion in LANGUAGE_PATTERNS:
        if pattern.search(html):
            findings.append(Finding('warning', file_rel, code, suggestion))

    broken_links: list[str] = []
    for a in tags(html, 'a'):
        href = a.get('href', '')
        internal = expected_internal_path(path, href)
        if internal and not (ROOT / internal).exists():
            broken_links.append(href)
    if broken_links:
        sample = ', '.join(sorted(set(broken_links))[:8])
        findings.append(Finding('warning', file_rel, 'broken_internal_links', f'{len(set(broken_links))} possible broken internal HTML link(s): {sample}'))

    return {
        'file': file_rel,
        'is_p0': is_p0,
        'title_length': len(title),
        'description_length': len(desc),
        'canonical_count': len(canonicals),
        'hreflang_count': len(hreflangs),
        'jsonld_blocks': jsonld_blocks,
        'invalid_jsonld': invalid_jsonld,
        'h1_count': h1_count,
        'images': len(img_tags),
        'images_missing_alt': missing_alt,
        'findings': [asdict(f) for f in findings],
    }


def main() -> int:
    OUT.mkdir(exist_ok=True)
    rows = [audit_file(path) for path in html_files()]
    findings = [Finding(**f) for row in rows for f in row['findings']]
    critical = [f for f in findings if f.severity == 'critical']
    warnings = [f for f in findings if f.severity == 'warning']
    score = max(0, round(100 - len(critical) * 10 - min(35, len(warnings) * 0.4)))
    status = 'PASS' if not critical else 'FAIL'
    payload = {
        'status': status,
        'score': score,
        'files_checked': len(rows),
        'critical_count': len(critical),
        'warning_count': len(warnings),
        'p0_pages': sorted(P0_PAGES),
        'results': rows,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

    lines = [
        '# Holistic Site Audit — Embaixada Carioca',
        '',
        f'Status: **{status}**',
        f'Score técnico: **{score}/100**',
        f'Arquivos HTML verificados: **{len(rows)}**',
        f'Críticos: **{len(critical)}**',
        f'Avisos: **{len(warnings)}**',
        '',
        '## Critérios críticos',
        '- JSON-LD válido.',
        '- Ausência de `aggregateRating`, `ratingValue`, `reviewCount`, `ratingCount`, `bestRating`, `worstRating` e `AggregateRating` no JSON-LD.',
        '- Páginas P0 com title, meta description, canonical e JSON-LD.',
        '',
        '## Critérios de aviso',
        '- Tamanho de title e meta description.',
        '- Hreflang ausente.',
        '- H1 ausente ou múltiplo.',
        '- Imagens sem alt.',
        '- Termos problemáticos de tradução/localização.',
        '- Links internos HTML possivelmente quebrados.',
        '',
        '## Achados críticos',
    ]
    if critical:
        for f in critical:
            lines.append(f'- `{f.file}` — {f.category}: {f.detail}')
    else:
        lines.append('- Nenhum achado crítico.')
    lines += ['', '## Avisos principais']
    if warnings:
        for f in warnings[:150]:
            lines.append(f'- `{f.file}` — {f.category}: {f.detail}')
    else:
        lines.append('- Nenhum aviso.')
    lines += ['', '## Resumo por arquivo']
    for row in rows:
        crit = sum(1 for f in row['findings'] if f['severity'] == 'critical')
        warn = sum(1 for f in row['findings'] if f['severity'] == 'warning')
        lines.append(f"- `{row['file']}` — JSON-LD {row['jsonld_blocks']} / inválidos {row['invalid_jsonld']} / canonical {row['canonical_count']} / hreflang {row['hreflang_count']} / H1 {row['h1_count']} / críticos {crit} / avisos {warn}")
    REPORT_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Holistic site audit: {status} score={score} files={len(rows)} critical={len(critical)} warnings={len(warnings)}')
    return 0 if status == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
