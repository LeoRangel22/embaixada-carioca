#!/usr/bin/env python3
"""
Build script: gera páginas HTML finais a partir de templates Jinja2.
Uso: python build.py [--page index] [--all] [--check]

Flags:
  --all         Gera todas as páginas definidas em _data/pages.json
  --page SLUG   Gera apenas a página com o slug especificado
  --check       Modo verificação: compara o HTML gerado com os arquivos existentes
                e retorna exit code 1 se houver diferenças (não escreve em disco)
"""

import argparse
import difflib
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def load_jinja_env():
    try:
        from jinja2 import Environment, FileSystemLoader, select_autoescape
    except ImportError:
        print("ERROR: Jinja2 não instalado. Execute: pip install jinja2", file=sys.stderr)
        sys.exit(1)

    env = Environment(
        loader=FileSystemLoader(ROOT),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env


def load_pages():
    data_path = os.path.join(ROOT, "_data", "pages.json")
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    return data["pages"]


def render_page(env, page):
    """Renderiza uma página usando o template base e os dados da página."""
    template = env.get_template("_templates/base.html")
    context = {
        "lang": {"pt": "pt-BR", "en": "en", "es": "es"}.get(page["lang"], page["lang"]),
        "title": page["title"],
        "description": page["description"],
        "canonical": page["canonical"],
        "hreflang": page.get("hreflang", {}),
    }
    return template.render(**context)


def generate_page(env, page, check=False):
    """
    Gera ou verifica uma página.
    Em modo --check, compara o HTML gerado com o existente.
    Em modo normal, escreve o arquivo gerado no destino.
    """
    output_path = os.path.join(ROOT, page["output"])
    rendered = render_page(env, page)

    if check:
        if not os.path.exists(output_path):
            print(f"  MISSING  {page['output']}")
            return False
        with open(output_path, encoding="utf-8") as f:
            existing = f.read()
        if rendered == existing:
            print(f"  OK       {page['output']}")
            return True
        diff = list(
            difflib.unified_diff(
                existing.splitlines(keepends=True),
                rendered.splitlines(keepends=True),
                fromfile=f"existing/{page['output']}",
                tofile=f"generated/{page['output']}",
                n=3,
            )
        )
        print(f"  DIFF     {page['output']} ({len(diff)} lines changed)")
        for line in diff[:40]:
            print("    " + line, end="")
        if len(diff) > 40:
            print(f"    ... ({len(diff) - 40} more lines)")
        return False
    else:
        os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"  WROTE    {page['output']}")
        return True


def main():
    parser = argparse.ArgumentParser(description="Embaixada Carioca — build estático Jinja2")
    parser.add_argument("--all", dest="all_pages", action="store_true", help="Gera todas as páginas")
    parser.add_argument("--page", dest="page_slug", default=None, help="Gera apenas o slug especificado")
    parser.add_argument("--check", dest="check", action="store_true",
                        help="Verifica se os HTMLs gerados batem com os existentes (não escreve)")
    args = parser.parse_args()

    if not args.all_pages and not args.page_slug:
        parser.print_help()
        sys.exit(0)

    env = load_jinja_env()
    pages = load_pages()

    if args.page_slug:
        pages = [p for p in pages if p["slug"] == args.page_slug]
        if not pages:
            print(f"ERROR: Nenhuma página encontrada com slug '{args.page_slug}'", file=sys.stderr)
            sys.exit(1)

    mode = "CHECK" if args.check else "BUILD"
    print(f"\n[{mode}] {len(pages)} página(s)\n")

    results = []
    for page in pages:
        ok = generate_page(env, page, check=args.check)
        results.append(ok)

    success = sum(results)
    failed = len(results) - success
    print(f"\nResultado: {success} OK, {failed} com diferença/erro")

    if failed > 0 and args.check:
        sys.exit(1)


if __name__ == "__main__":
    main()
