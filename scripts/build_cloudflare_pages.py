#!/usr/bin/env python3
"""Build a clean static output directory for Cloudflare Pages."""

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site"

PUBLIC_DIRECTORIES = ("assets", "img", "en", "es")
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

    for path in ROOT.iterdir():
        if path.is_file() and (
            path.name in PUBLIC_ROOT_FILES or path.suffix.lower() in PUBLIC_ROOT_SUFFIXES
        ):
            shutil.copy2(path, OUTPUT / path.name)

    for directory_name in PUBLIC_DIRECTORIES:
        source = ROOT / directory_name
        if source.exists():
            shutil.copytree(source, OUTPUT / directory_name)

    largest = max((p.stat().st_size for p in OUTPUT.rglob("*") if p.is_file()), default=0)
    if largest > 25 * 1024 * 1024:
        raise RuntimeError("Cloudflare Pages output contains a file larger than 25 MiB")

    if not (OUTPUT / "index.html").exists():
        raise RuntimeError("Cloudflare Pages output is missing index.html")

    file_count = sum(1 for p in OUTPUT.rglob("*") if p.is_file())
    print(f"Cloudflare Pages output ready: {file_count} files in {OUTPUT}")


if __name__ == "__main__":
    copy_public_site()
