#!/usr/bin/env python3
"""
update_css_references.py
Embaixada Carioca — CSS consolidation helper.

Para cada arquivo HTML que referenciar qualquer um dos CSS "patch" antigos,
insere links para ec-base.css e ec-theme.css caso ainda não estejam presentes.
NÃO remove as referências antigas — isso deve ser feito manualmente após validação.

Uso:
    python scripts/update_css_references.py [--dry-run]
"""

import argparse
import os
import re
import sys
from pathlib import Path

# CSS files that trigger injection (any of these = file qualifies)
OLD_CSS_PATTERNS = [
    "ec-stabilization-base",
    "ec-button-hover-standard",
    "ec-contrast-hotfix",
    "ec-green-solid-palette",
    "ec-home-final-visual-tuning",
    "ec-visible-text-lock",
    "superholistic_visual_readability_lock",
    "eventos-contrast-lock",
]

# New consolidated files to inject
NEW_CSS_BASE = "/assets/css/ec-base.css"
NEW_CSS_THEME = "/assets/css/ec-theme.css"

LINK_BASE = f'<link rel="stylesheet" href="{NEW_CSS_BASE}">'
LINK_THEME = f'<link rel="stylesheet" href="{NEW_CSS_THEME}">'

# Regex to match <link rel="stylesheet" ...> or </head>
RE_LINK_TAG = re.compile(r'<link\b[^>]+rel=["\']stylesheet["\'][^>]*>', re.IGNORECASE)
RE_END_HEAD = re.compile(r'</head>', re.IGNORECASE)


def find_html_files(root: Path):
    """Yield all .html files under root, skipping archive subdirs."""
    for path in sorted(root.rglob("*.html")):
        # Check only relative parts (from root) to avoid matching parent dirs
        try:
            rel_parts = path.relative_to(root).parts
        except ValueError:
            continue
        if "archive" in rel_parts:
            continue
        yield path


def has_old_css(content: str) -> bool:
    for pat in OLD_CSS_PATTERNS:
        if pat in content:
            return True
    return False


def needs_base(content: str) -> bool:
    return NEW_CSS_BASE not in content


def needs_theme(content: str) -> bool:
    return NEW_CSS_THEME not in content


def inject_links(content: str, add_base: bool, add_theme: bool) -> str:
    """Insert the new <link> tags before the first existing stylesheet link,
    or before </head> if no stylesheet link is found."""
    if not add_base and not add_theme:
        return content

    inject = ""
    if add_base:
        inject += LINK_BASE + "\n"
    if add_theme:
        inject += LINK_THEME + "\n"

    # Try to insert before first <link rel="stylesheet"> found in <head>
    match = RE_LINK_TAG.search(content)
    if match:
        pos = match.start()
        return content[:pos] + inject + content[pos:]

    # Fallback: insert before </head>
    match = RE_END_HEAD.search(content)
    if match:
        pos = match.start()
        return content[:pos] + inject + content[pos:]

    # Last resort: append to end (should never happen on valid HTML)
    return content + inject


def process(root: Path, dry_run: bool = False):
    updated = []
    skipped = []

    for html_file in find_html_files(root):
        content = html_file.read_text(encoding="utf-8", errors="replace")

        if not has_old_css(content):
            continue

        add_base = needs_base(content)
        add_theme = needs_theme(content)

        if not add_base and not add_theme:
            skipped.append(html_file)
            continue

        new_content = inject_links(content, add_base, add_theme)
        tags = []
        if add_base:
            tags.append("ec-base.css")
        if add_theme:
            tags.append("ec-theme.css")

        print(f"{'[DRY RUN] ' if dry_run else ''}Updated: {html_file.relative_to(root)}  (+{', '.join(tags)})")

        if not dry_run:
            html_file.write_text(new_content, encoding="utf-8")

        updated.append(html_file)

    print()
    print(f"Files updated : {len(updated)}")
    print(f"Already had both links: {len(skipped)}")


def main():
    parser = argparse.ArgumentParser(description="Inject ec-base.css and ec-theme.css links into qualifying HTML files.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files.")
    parser.add_argument("--root", default=None, help="Root directory (defaults to repo root based on script location).")
    args = parser.parse_args()

    # Resolve root: go up one level from scripts/
    script_dir = Path(__file__).resolve().parent
    root = Path(args.root).resolve() if args.root else script_dir.parent

    if not root.exists():
        print(f"ERROR: Root directory not found: {root}", file=sys.stderr)
        sys.exit(1)

    print(f"Root: {root}")
    print(f"Dry run: {args.dry_run}")
    print()

    process(root, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
