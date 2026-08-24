#!/usr/bin/env python3
"""Build a clean static output directory for Cloudflare Pages."""

from pathlib import Path
import json
import shutil


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site"

PUBLIC_ASSET_DIRECTORIES = ("assets", "img")
PUBLIC_ROOT_SUFFIXES = {
    ".html",
    ".css",
    ".js",
    ".xml",
    ".txt",
    ".ico",
    ".webmanifest",
}
PUBLIC_ROOT_FILES = {"_headers", "_redirects", "manifest.json", "version.json"}


def copy_public_site() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()

    html_store = OUTPUT / "_html"
    html_store.mkdir()

    for path in ROOT.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() == ".html":
            shutil.copy2(path, html_store / f"{path.name}.txt")
        elif path.name in PUBLIC_ROOT_FILES or path.suffix.lower() in PUBLIC_ROOT_SUFFIXES:
            shutil.copy2(path, OUTPUT / path.name)

    for directory_name in PUBLIC_ASSET_DIRECTORIES:
        source = ROOT / directory_name
        if source.exists():
            shutil.copytree(source, OUTPUT / directory_name)

    for language in ("en", "es"):
        source = ROOT / language
        html_destination = html_store / language
        public_destination = OUTPUT / language
        html_destination.mkdir()
        public_destination.mkdir()
        for path in source.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(source)
            if path.suffix.lower() == ".html":
                target = html_destination / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target.with_name(f"{target.name}.txt"))
            else:
                target = public_destination / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)

    routes = {
        "version": 1,
        "include": ["/*"],
        "exclude": [
            "/assets/*",
            "/img/*",
            "/*.css",
            "/*.js",
            "/*.json",
            "/*.xml",
            "/*.txt",
            "/*.ico",
        ],
    }
    (OUTPUT / "_routes.json").write_text(json.dumps(routes, indent=2) + "\n", encoding="utf-8")

    largest = max((p.stat().st_size for p in OUTPUT.rglob("*") if p.is_file()), default=0)
    if largest > 25 * 1024 * 1024:
        raise RuntimeError("Cloudflare Pages output contains a file larger than 25 MiB")

    if not (html_store / "index.html.txt").exists():
        raise RuntimeError("Cloudflare Pages output is missing the stored home page")

    file_count = sum(1 for p in OUTPUT.rglob("*") if p.is_file())
    print(f"Cloudflare Pages output ready: {file_count} files in {OUTPUT}")


if __name__ == "__main__":
    copy_public_site()
