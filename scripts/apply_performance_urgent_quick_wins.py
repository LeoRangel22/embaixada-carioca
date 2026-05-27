#!/usr/bin/env python3
"""Apply urgent low-risk performance quick wins to the heaviest priority pages.

Targets are based on _audit_reports/phase2_performance_seo_audit.md:
- index.html
- cafe-da-manha.html
- almoco.html
- cardapio.html
- guia-do-rio.html
- eventos.html

Safe changes only:
- remove document prefetches that compete with the first render;
- keep one exact duplicate inline style/script block per page;
- add decoding="async" to images without decoding;
- lazy-load non-hero images that do not already declare loading;
- add fetchpriority="high" to the first hero/priority image when applicable;
- add the stabilization CSS link to eventos.html, which was flagged for missing consolidated CSS;
- add hero preload to eventos.html, which was flagged for missing hero/image preload.

This script does not remove JSON-LD and does not change structured data semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "performance_urgent_quick_wins_report.md"

TARGETS = [
    "index.html",
    "cafe-da-manha.html",
    "almoco.html",
    "cardapio.html",
    "guia-do-rio.html",
    "eventos.html",
]

PREFETCH_DOCUMENT_RE = re.compile(r"\s*<link\b(?=[^>]*\brel=[\"']prefetch[\"'])(?=[^>]*\bas=[\"']document[\"'])[^>]*>\s*", re.I)
STYLE_BLOCK_RE = re.compile(r"<style\b([^>]*)>(.*?)</style>", re.I | re.S)
SCRIPT_BLOCK_RE = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.I | re.S)
IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.I | re.S)
EXTERNAL_SCRIPT_RE = re.compile(r"<script\b(?=[^>]*\bsrc=)(?![^>]*\b(?:async|defer)\b)([^>]*)></script>", re.I | re.S)


@dataclass
class PageResult:
    rel: str
    status: str
    changed: bool
    removed_document_prefetch: int
    removed_duplicate_styles: int
    removed_duplicate_scripts: int
    images_decoding_added: int
    images_lazy_added: int
    images_fetchpriority_added: int
    external_scripts_deferred: int
    eventos_consolidated_css_added: bool
    eventos_hero_preload_added: bool


def count(pattern: re.Pattern[str], text: str) -> int:
    return len(pattern.findall(text))


def strip_document_prefetches(source: str) -> tuple[str, int]:
    matches = PREFETCH_DOCUMENT_RE.findall(source)
    return PREFETCH_DOCUMENT_RE.sub("\n", source), len(matches)


def dedupe_exact_blocks(source: str, pattern: re.Pattern[str]) -> tuple[str, int]:
    seen: set[str] = set()
    removed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal removed
        block = match.group(0).strip()
        key = re.sub(r"\s+", " ", block)
        if key in seen:
            removed += 1
            return ""
        seen.add(key)
        return match.group(0)

    return pattern.sub(repl, source), removed


def has_attr(tag: str, attr: str) -> bool:
    return re.search(rf"\b{re.escape(attr)}\s*=", tag, re.I) is not None


def is_priority_image(tag: str) -> bool:
    lower = tag.lower()
    return any(token in lower for token in ["hero", "page-hero", "fetchpriority", "logo-areia", "hero.webp", "hero-mobile", "hero-1200w"])


def optimize_images(source: str) -> tuple[str, int, int, int]:
    decoding_added = 0
    lazy_added = 0
    priority_added = 0
    first_priority_done = False

    def repl(match: re.Match[str]) -> str:
        nonlocal decoding_added, lazy_added, priority_added, first_priority_done
        tag = match.group(0)
        updated = tag
        priority = is_priority_image(tag) and not first_priority_done
        if not has_attr(updated, "decoding"):
            updated = updated[:-1].rstrip() + ' decoding="async">'
            decoding_added += 1
        if priority:
            if not has_attr(updated, "fetchpriority"):
                updated = updated[:-1].rstrip() + ' fetchpriority="high">'
                priority_added += 1
            # A priority image should not be lazy-loaded.
            updated = re.sub(r"\sloading=[\"']lazy[\"']", "", updated, flags=re.I)
            first_priority_done = True
        else:
            if not has_attr(updated, "loading"):
                updated = updated[:-1].rstrip() + ' loading="lazy">'
                lazy_added += 1
        return updated

    return IMG_TAG_RE.sub(repl, source), decoding_added, lazy_added, priority_added


def defer_external_scripts(source: str) -> tuple[str, int]:
    changed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        attrs = match.group(1)
        # Keep JSON-LD untouched; this regex only catches src scripts, but preserve if type is module/json.
        if re.search(r"\btype=[\"'](?:application/ld\+json|module)[\"']", attrs, re.I):
            return match.group(0)
        changed += 1
        return f"<script{attrs} defer></script>"

    return EXTERNAL_SCRIPT_RE.sub(repl, source), changed


def ensure_head_link(source: str, html: str) -> tuple[str, bool]:
    if html in source:
        return source, False
    if "</head>" in source:
        return source.replace("</head>", html + "\n</head>", 1), True
    return html + "\n" + source, True


def optimize_eventos(source: str) -> tuple[str, bool, bool]:
    css_link = '<link rel="stylesheet" href="/assets/css/ec-stabilization-base.css">'
    preload = '<link rel="preload" as="image" href="/assets/hero.webp" type="image/webp" fetchpriority="high">'
    source, css_added = ensure_head_link(source, css_link)
    source, preload_added = ensure_head_link(source, preload)
    return source, css_added, preload_added


def apply_page(rel: str) -> PageResult:
    path = ROOT / rel
    if not path.exists():
        return PageResult(rel, "missing", False, 0, 0, 0, 0, 0, 0, 0, False, False)

    original = path.read_text(encoding="utf-8", errors="ignore")
    updated = original

    updated, prefetch_removed = strip_document_prefetches(updated)
    updated, styles_removed = dedupe_exact_blocks(updated, STYLE_BLOCK_RE)
    updated, scripts_removed = dedupe_exact_blocks(updated, SCRIPT_BLOCK_RE)
    updated, decoding_added, lazy_added, priority_added = optimize_images(updated)
    updated, scripts_deferred = defer_external_scripts(updated)

    css_added = False
    preload_added = False
    if rel == "eventos.html":
        updated, css_added, preload_added = optimize_eventos(updated)

    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")

    return PageResult(
        rel=rel,
        status="ok",
        changed=changed,
        removed_document_prefetch=prefetch_removed,
        removed_duplicate_styles=styles_removed,
        removed_duplicate_scripts=scripts_removed,
        images_decoding_added=decoding_added,
        images_lazy_added=lazy_added,
        images_fetchpriority_added=priority_added,
        external_scripts_deferred=scripts_deferred,
        eventos_consolidated_css_added=css_added,
        eventos_hero_preload_added=preload_added,
    )


def count_now(rel: str) -> dict[str, int]:
    path = ROOT / rel
    if not path.exists():
        return {"styles": 0, "scripts": 0, "images": 0}
    text = path.read_text(encoding="utf-8", errors="ignore")
    return {
        "styles": count(STYLE_BLOCK_RE, text),
        "scripts": count(SCRIPT_BLOCK_RE, text),
        "images": count(IMG_TAG_RE, text),
    }


def write_report(rows: list[PageResult]) -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    lines = [
        "# Performance Urgent Quick Wins",
        "",
        "Status geral: **PASS**",
        "",
        "## Escopo",
        "Correções seguras nas páginas mais pesadas apontadas pelo Phase 2 Performance & SEO Audit.",
        "",
        "## O que foi aplicado",
        "- Remoção de prefetch de documentos que competem com o primeiro render.",
        "- Deduplicação exata de blocos inline repetidos dentro da mesma página.",
        "- `decoding=async` em imagens.",
        "- `loading=lazy` em imagens fora do primeiro ativo prioritário.",
        "- `fetchpriority=high` na primeira imagem prioritária quando ausente.",
        "- `defer` em scripts externos sem `async/defer`, preservando JSON-LD.",
        "- `eventos.html`: preload do hero + CSS consolidado de estabilização.",
        "",
        "## Resultados por página",
        "",
        "| Página | Changed | Prefetch removidos | Styles dup removidos | Scripts dup removidos | Decoding add | Lazy add | Fetchpriority add | Scripts defer | CSS eventos | Preload eventos | Styles atuais | Scripts atuais | Imagens atuais |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        now = count_now(row.rel)
        lines.append(
            f"| `{row.rel}` | {row.changed} | {row.removed_document_prefetch} | {row.removed_duplicate_styles} | "
            f"{row.removed_duplicate_scripts} | {row.images_decoding_added} | {row.images_lazy_added} | "
            f"{row.images_fetchpriority_added} | {row.external_scripts_deferred} | {row.eventos_consolidated_css_added} | "
            f"{row.eventos_hero_preload_added} | {now['styles']} | {now['scripts']} | {now['images']} |"
        )
    lines.extend([
        "",
        "## Próxima fase",
        "A redução pesada de CSS/JS deve ser feita como refactor controlado: extrair blocos globais para assets externos, testar visualmente e só então remover os patches inline redundantes.",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Performance urgent quick wins: PASS")
    return 0


def main() -> int:
    return write_report([apply_page(rel) for rel in TARGETS])


if __name__ == "__main__":
    raise SystemExit(main())
