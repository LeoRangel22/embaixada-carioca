#!/usr/bin/env python3
"""Fix Google Search Console Review snippets issue.

Problem exported from GSC: "A avaliação tem várias classificações agregadas".

Action:
- Scan every public HTML file.
- Sanitize JSON-LD blocks by removing Review Snippet rating structures:
  AggregateRating objects, aggregateRating keys and nested rating fields.
- Keep Restaurant, WebPage, FAQPage, BreadcrumbList, Menu and other schema intact.
- Write a compact audit report for Search Console follow-up.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "review_snippets_issue_fix_report.md"
SITE = "https://www.embaixadacarioca.com/"

JSONLD_RE = re.compile(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)

FORBIDDEN_TYPES = {"AggregateRating"}
FORBIDDEN_KEYS = {
    "aggregateRating",
    "ratingValue",
    "reviewCount",
    "ratingCount",
    "bestRating",
    "worstRating",
}

GSC_AFFECTED_URLS = [
    "https://www.embaixadacarioca.com/morro-da-urca.html",
    "https://www.embaixadacarioca.com/onde-comer-no-pao-de-acucar.html",
    "https://www.embaixadacarioca.com/restaurante-morro-da-urca.html",
    "https://www.embaixadacarioca.com/parque-bondinho.html",
    "https://www.embaixadacarioca.com/o-que-fazer-depois-do-bondinho-pao-de-acucar.html",
    "https://www.embaixadacarioca.com/roteiro-meio-dia-urca-pao-de-acucar.html",
    "https://www.embaixadacarioca.com/cafe-da-manha.html",
    "https://www.embaixadacarioca.com/entardecer.html",
]


@dataclass
class FileResult:
    rel: str
    jsonld_blocks: int
    removed_terms: int
    parse_errors: int
    changed: bool
    remaining_terms: list[str]


def rel_from_url(url: str) -> str:
    return url.replace(SITE, "")


def has_forbidden_type(value: Any) -> bool:
    if isinstance(value, str):
        return value in FORBIDDEN_TYPES
    if isinstance(value, list):
        return any(str(item) in FORBIDDEN_TYPES for item in value)
    return False


def clean_jsonld(obj: Any, counter: dict[str, int]) -> Any:
    if isinstance(obj, dict):
        if has_forbidden_type(obj.get("@type")):
            counter["removed"] += 1
            return None
        cleaned: dict[str, Any] = {}
        for key, value in obj.items():
            if key in FORBIDDEN_KEYS:
                counter["removed"] += 1
                continue
            next_value = clean_jsonld(value, counter)
            if next_value is None:
                continue
            if isinstance(next_value, list) and not next_value:
                continue
            cleaned[key] = next_value
        return cleaned
    if isinstance(obj, list):
        cleaned_list = []
        for item in obj:
            next_item = clean_jsonld(item, counter)
            if next_item is not None:
                cleaned_list.append(next_item)
        return cleaned_list
    return obj


def collect_forbidden(obj: Any, found: set[str]) -> None:
    if isinstance(obj, dict):
        typ = obj.get("@type")
        if isinstance(typ, str) and typ in FORBIDDEN_TYPES:
            found.add(typ)
        elif isinstance(typ, list):
            for item in typ:
                item_str = str(item)
                if item_str in FORBIDDEN_TYPES:
                    found.add(item_str)
        for key, value in obj.items():
            if key in FORBIDDEN_KEYS:
                found.add(key)
            collect_forbidden(value, found)
    elif isinstance(obj, list):
        for item in obj:
            collect_forbidden(item, found)


def sanitize_html(text: str) -> tuple[str, int, int, int, list[str]]:
    total_blocks = 0
    parse_errors = 0
    removed_total = 0
    remaining: set[str] = set()

    def repl(match: re.Match[str]) -> str:
        nonlocal total_blocks, parse_errors, removed_total
        opener, raw, closer = match.groups()
        total_blocks += 1
        try:
            obj = json.loads(html.unescape(raw.strip()))
        except Exception:
            parse_errors += 1
            return match.group(0)
        counter = {"removed": 0}
        cleaned = clean_jsonld(obj, counter)
        removed_total += counter["removed"]
        if cleaned is None:
            return ""
        collect_forbidden(cleaned, remaining)
        serialized = json.dumps(cleaned, ensure_ascii=False, separators=(",", ":"))
        return opener + serialized + closer

    updated = JSONLD_RE.sub(repl, text)
    return updated, total_blocks, removed_total, parse_errors, sorted(remaining)


def html_files() -> list[Path]:
    files = []
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if ".git" in path.parts or rel.startswith("_"):
            continue
        files.append(path)
    return files


def apply_file(path: Path) -> FileResult:
    rel = path.relative_to(ROOT).as_posix()
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated, blocks, removed, parse_errors, remaining = sanitize_html(original)
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return FileResult(rel, blocks, removed, parse_errors, changed, remaining)


def write_report(results: list[FileResult]) -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    changed = [r for r in results if r.changed]
    remaining = [r for r in results if r.remaining_terms]
    affected_rels = [rel_from_url(url) for url in GSC_AFFECTED_URLS]
    by_rel = {r.rel: r for r in results}
    status = "PASS" if not remaining else "FAIL"

    lines = [
        "# Review Snippets Issue Fix",
        "",
        f"Status geral: **{status}**",
        "",
        "## Problema do Google Search Console",
        "- A avaliação tem várias classificações agregadas.",
        "- Estratégia: remover AggregateRating e campos de rating do JSON-LD, preservando os demais schemas.",
        "",
        "## Resumo",
        f"- Arquivos HTML escaneados: {len(results)}",
        f"- Arquivos alterados: {len(changed)}",
        f"- Arquivos com termos proibidos remanescentes: {len(remaining)}",
        "",
        "## URLs afetadas no XLSX do Search Console",
        "",
        "| URL | Arquivo | Changed | Removidos | Remanescentes |",
        "|---|---|---:|---:|---|",
    ]
    for url in GSC_AFFECTED_URLS:
        rel = rel_from_url(url)
        r = by_rel.get(rel)
        if r is None:
            lines.append(f"| {url} | `{rel}` | n/a | n/a | arquivo não encontrado |")
        else:
            rem = ", ".join(r.remaining_terms) if r.remaining_terms else "—"
            lines.append(f"| {url} | `{rel}` | {r.changed} | {r.removed_terms} | {rem} |")

    lines.extend([
        "",
        "## Arquivos alterados",
        "",
    ])
    if changed:
        for r in changed:
            lines.append(f"- `{r.rel}` — removidos={r.removed_terms}, jsonld={r.jsonld_blocks}, parse_errors={r.parse_errors}")
    else:
        lines.append("- Nenhum arquivo precisou ser alterado.")

    if remaining:
        lines.extend(["", "## Pendências", ""])
        for r in remaining:
            lines.append(f"- `{r.rel}` — {', '.join(r.remaining_terms)}")

    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Review snippets issue fix: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    results = [apply_file(path) for path in html_files()]
    return write_report(results)


if __name__ == "__main__":
    raise SystemExit(main())
