#!/usr/bin/env python3
"""
apply_partials.py — Aplica partials de nav e footer a todas as páginas HTML.

Uso:
  python3 scripts/apply_partials.py              # aplica todos os partials
  python3 scripts/apply_partials.py --dry-run    # mostra o que seria alterado
  python3 scripts/apply_partials.py --partial nav # aplica só o nav
  python3 scripts/apply_partials.py --partial footer

Partials ficam em:
  src/partials/pt/nav.html     → páginas em /
  src/partials/en/nav.html     → páginas em /en/
  src/partials/es/nav.html     → páginas em /es/
  src/partials/pt/footer.html  → (idem)
  ...

Para atualizar o nav em todas as páginas:
  1. Edite src/partials/pt/nav.html
  2. python3 scripts/apply_partials.py --partial nav
  3. git diff para revisar
  4. git commit
"""

import argparse
import glob
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LANGS = {
    'pt': {'pages': f'{BASE}/*.html',    'partials': f'{BASE}/src/partials/pt'},
    'en': {'pages': f'{BASE}/en/*.html', 'partials': f'{BASE}/src/partials/en'},
    'es': {'pages': f'{BASE}/es/*.html', 'partials': f'{BASE}/src/partials/es'},
}

SKIP_PAGES = {'offline.html', '404.html', 'home-preview.html'}


def load_partial(lang, name):
    path = os.path.join(LANGS[lang]['partials'], f'{name}.html')
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return f.read().strip()


def apply_nav(content, partial):
    new, n = re.subn(
        r'<nav class="top".*?</nav>',
        partial,
        content,
        count=1,
        flags=re.DOTALL,
    )
    return new, n > 0


def apply_footer(content, partial):
    new, n = re.subn(
        r'<footer[\s\S]*?</footer>',
        partial,
        content,
        count=1,
        flags=re.DOTALL,
    )
    return new, n > 0


APPLIERS = {
    'nav': apply_nav,
    'footer': apply_footer,
}


def main():
    parser = argparse.ArgumentParser(description='Apply HTML partials to all pages')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without writing')
    parser.add_argument('--partial', choices=['nav', 'footer', 'all'], default='all')
    args = parser.parse_args()

    partials_to_apply = ['nav', 'footer'] if args.partial == 'all' else [args.partial]

    total_changed = 0
    total_skipped = 0

    for lang, cfg in LANGS.items():
        pages = sorted(glob.glob(cfg['pages']))
        for partial_name in partials_to_apply:
            partial_content = load_partial(lang, partial_name)
            if partial_content is None:
                print(f'[SKIP] No partial: src/partials/{lang}/{partial_name}.html')
                continue

            applier = APPLIERS[partial_name]

            for page_path in pages:
                filename = os.path.basename(page_path)
                if filename in SKIP_PAGES:
                    continue

                with open(page_path) as f:
                    original = f.read()

                updated, changed = applier(original, partial_content)

                if not changed:
                    total_skipped += 1
                    continue

                if updated == original:
                    continue

                total_changed += 1
                rel = page_path.replace(BASE + '/', '')
                if args.dry_run:
                    print(f'[DRY] Would update {partial_name} in {rel}')
                else:
                    with open(page_path, 'w') as f:
                        f.write(updated)
                    print(f'[OK]  Updated {partial_name} in {rel}')

    print(f'\nDone: {total_changed} pages updated, {total_skipped} unchanged/skipped')
    if args.dry_run:
        print('(dry-run — no files written)')


if __name__ == '__main__':
    main()
