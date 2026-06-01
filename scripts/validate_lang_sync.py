#!/usr/bin/env python3
"""
validate_lang_sync.py — Valida sincronização de páginas PT/EN/ES.

Verifica:
1. Quais páginas PT não têm equivalente EN ou ES
2. Quais páginas EN/ES não têm equivalente PT (páginas órfãs)
3. Hreflang de cada página aponta para URLs que realmente existem
4. Título e meta description estão presentes em todos os idiomas

Uso:
  python3 scripts/validate_lang_sync.py
  python3 scripts/validate_lang_sync.py --fix-report   # salva CSV com gaps

Saída: relatório no terminal + opcionalmente _audit_reports/lang_sync_YYYY-MM-DD.csv
"""

import argparse
import csv
import glob
import os
import re
import sys
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP = {'404.html', 'offline.html', 'home-preview.html', 'llms.txt'}

EN_EQUIVALENTS = {
    'como-chegar.html': 'how-to-get-there.html',
    'nossa-visao.html': 'nossa-visao.html',
}


def pages_in(folder):
    pattern = os.path.join(BASE, folder, '*.html')
    return {os.path.basename(p) for p in glob.glob(pattern)} - SKIP


def extract_meta(filepath, tag, attr='name'):
    with open(filepath, errors='replace') as f:
        content = f.read()
    m = re.search(
        rf'<meta\s+{attr}=["\']{tag}["\']\s+content=["\']([^"\']*)["\']',
        content, re.IGNORECASE
    )
    if not m:
        m = re.search(
            rf'<meta\s+content=["\']([^"\']*)["\'][^>]*{attr}=["\']{tag}["\']',
            content, re.IGNORECASE
        )
    return m.group(1).strip() if m else ''


def extract_title(filepath):
    with open(filepath, errors='replace') as f:
        content = f.read()
    m = re.search(r'<title>([^<]+)</title>', content)
    return m.group(1).strip() if m else ''


def extract_hreflang(filepath):
    with open(filepath, errors='replace') as f:
        content = f.read()
    return re.findall(r'hreflang=["\']([^"\']+)["\'][^>]+href=["\']([^"\']+)["\']|href=["\']([^"\']+)["\'][^>]+hreflang=["\']([^"\']+)["\']', content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fix-report', action='store_true')
    args = parser.parse_args()

    pt_pages = pages_in('')
    en_pages = pages_in('en')
    es_pages = pages_in('es')

    issues = []
    warnings = []

    print(f"Pages: PT={len(pt_pages)}  EN={len(en_pages)}  ES={len(es_pages)}")
    print()

    # 1. PT pages missing EN or ES equivalent
    missing_en = []
    missing_es = []
    for page in sorted(pt_pages):
        en_name = EN_EQUIVALENTS.get(page, page)
        if en_name not in en_pages:
            missing_en.append(page)
        if page not in es_pages:
            missing_es.append(page)

    if missing_en:
        print(f"❌ PT pages missing EN equivalent ({len(missing_en)}):")
        for p in missing_en:
            print(f"   {p}")
            issues.append(('MISSING_EN', p, '', ''))
        print()

    if missing_es:
        print(f"❌ PT pages missing ES equivalent ({len(missing_es)}):")
        for p in missing_es:
            print(f"   {p}")
            issues.append(('MISSING_ES', p, '', ''))
        print()

    # 2. EN/ES orphans (no PT equivalent)
    en_orphans = en_pages - pt_pages - set(EN_EQUIVALENTS.values())
    es_orphans = es_pages - pt_pages

    if en_orphans:
        print(f"⚠️  EN pages without PT equivalent ({len(en_orphans)}):")
        for p in sorted(en_orphans):
            print(f"   en/{p}")
            warnings.append(('EN_ORPHAN', f'en/{p}', '', ''))
        print()

    if es_orphans:
        print(f"⚠️  ES pages without PT equivalent ({len(es_orphans)}):")
        for p in sorted(es_orphans):
            print(f"   es/{p}")
            warnings.append(('ES_ORPHAN', f'es/{p}', '', ''))
        print()

    # 3. Hreflang pointing to non-existent pages
    all_pages = (
        [(p, os.path.join(BASE, p)) for p in sorted(pt_pages)] +
        [(f'en/{p}', os.path.join(BASE, 'en', p)) for p in sorted(en_pages)] +
        [(f'es/{p}', os.path.join(BASE, 'es', p)) for p in sorted(es_pages)]
    )

    hreflang_broken = []
    for rel_path, full_path in all_pages:
        refs = extract_hreflang(full_path)
        for ref in refs:
            lang = ref[0] or ref[3]
            url = ref[1] or ref[2]
            # Extract path from URL
            m = re.search(r'embaixadacarioca\.com(/[^"\']*)', url)
            if not m:
                continue
            path = m.group(1).lstrip('/')
            if not path or path.endswith('/'):
                path = path + 'index.html'
            local = os.path.join(BASE, path)
            if not os.path.exists(local):
                hreflang_broken.append((rel_path, lang, url))
                issues.append(('HREFLANG_404', rel_path, lang, url))

    if hreflang_broken:
        print(f"❌ Hreflang pointing to missing pages ({len(hreflang_broken)}):")
        for page, lang, url in hreflang_broken[:20]:
            print(f"   {page} → [{lang}] {url}")
        if len(hreflang_broken) > 20:
            print(f"   ... and {len(hreflang_broken)-20} more")
        print()

    # 4. Missing title/description
    no_title = []
    no_desc = []
    for rel_path, full_path in all_pages:
        title = extract_title(full_path)
        desc = extract_meta(full_path, 'description')
        if not title:
            no_title.append(rel_path)
            issues.append(('NO_TITLE', rel_path, '', ''))
        if not desc:
            no_desc.append(rel_path)
            issues.append(('NO_DESC', rel_path, '', ''))

    if no_title:
        print(f"❌ Pages missing <title> ({len(no_title)}): {no_title[:5]}")
    if no_desc:
        print(f"⚠️  Pages missing meta description ({len(no_desc)}): {no_desc[:5]}")

    # Summary
    print()
    print('=' * 60)
    print(f"ERRORS:   {len(issues)}")
    print(f"WARNINGS: {len(warnings)}")

    if not issues and not warnings:
        print("✅ All language pages in sync!")

    if args.fix_report and (issues or warnings):
        out_dir = os.path.join(BASE, '_audit_reports')
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, f'lang_sync_{date.today()}.csv')
        with open(out_file, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['type', 'page', 'lang', 'url'])
            w.writerows(issues + warnings)
        print(f"\nReport saved: {out_file}")

    sys.exit(1 if issues else 0)


if __name__ == '__main__':
    main()
