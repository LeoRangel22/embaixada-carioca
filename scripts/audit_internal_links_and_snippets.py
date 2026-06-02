#!/usr/bin/env python3
"""Audit internal links and featured-snippet readiness for Embaixada Carioca.

Sprint 2 scope:
- Verify priority internal links across PT/EN/ES pages.
- Detect broken internal href targets in local static HTML files.
- Check whether strategic pages contain ordered lists (<ol>) suitable for Featured Snippets.
- Generate Markdown and JSON reports in _audit_reports/.

This script is read-only for site pages. It only writes audit reports.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from html import unescape
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse
import json
import posixpath
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "internal_links_and_snippets_audit.md"
REPORT_JSON = REPORT_DIR / "internal_links_and_snippets_audit.json"
SITE_HOSTS = {"www.embaixadacarioca.com", "embaixadacarioca.com", "embaixadacarioca.com.br", "www.embaixadacarioca.com.br"}

PRIORITY_PAGES: dict[str, dict[str, str]] = {
    "index.html": {
        "lang": "pt",
        "snippet_topic": "Como chegar à Embaixada Carioca no Morro da Urca",
        "required_links": "cafe-da-manha.html,almoco.html,entardecer.html,eventos.html,cardapio.html",
    },
    "en/index.html": {
        "lang": "en",
        "snippet_topic": "How to get to Embaixada Carioca at Morro da Urca",
        "required_links": "en/cafe-da-manha.html,en/almoco.html,en/sunset.html,en/eventos.html",
    },
    "es/index.html": {
        "lang": "es",
        "snippet_topic": "Cómo llegar a Embaixada Carioca en Morro da Urca",
        "required_links": "es/cafe-da-manha.html,es/almoco.html,es/atardecer.html,es/eventos.html",
    },
    "cafe-da-manha.html": {
        "lang": "pt",
        "snippet_topic": "Como tomar café da manhã no Morro da Urca",
        "required_links": "index.html,almoco.html,cardapio.html,eventos.html",
    },
    "almoco.html": {
        "lang": "pt",
        "snippet_topic": "Como almoçar no Pão de Açúcar",
        "required_links": "index.html,cafe-da-manha.html,cardapio.html,eventos.html",
    },
    "eventos.html": {
        "lang": "pt",
        "snippet_topic": "Como fazer um evento no Morro da Urca",
        "required_links": "index.html,cardapio.html,cafe-da-manha.html,almoco.html",
    },
    "entardecer.html": {
        "lang": "pt",
        "snippet_topic": "Como viver o entardecer no Morro da Urca",
        "required_links": "index.html,cardapio.html,eventos.html",
    },
    "cardapio.html": {
        "lang": "pt",
        "snippet_topic": "Como escolher o que comer na Embaixada Carioca",
        "required_links": "index.html,cafe-da-manha.html,almoco.html,eventos.html,entardecer.html",
    },
    "en/cafe-da-manha.html": {
        "lang": "en",
        "snippet_topic": "How to have breakfast at Morro da Urca",
        "required_links": "en/index.html,en/almoco.html,en/eventos.html",
    },
    "en/almoco.html": {
        "lang": "en",
        "snippet_topic": "How to have lunch at Sugarloaf Cable Car Park",
        "required_links": "en/index.html,en/cafe-da-manha.html,en/eventos.html",
    },
    "en/eventos.html": {
        "lang": "en",
        "snippet_topic": "How to host an event at Morro da Urca",
        "required_links": "en/index.html,en/cafe-da-manha.html,en/almoco.html",
    },
    "en/sunset.html": {
        "lang": "en",
        "snippet_topic": "How to enjoy sunset at Morro da Urca",
        "required_links": "en/index.html,en/eventos.html",
    },
    "es/cafe-da-manha.html": {
        "lang": "es",
        "snippet_topic": "Cómo desayunar en Morro da Urca",
        "required_links": "es/index.html,es/almoco.html,es/eventos.html",
    },
    "es/almoco.html": {
        "lang": "es",
        "snippet_topic": "Cómo almorzar en el Parque Bondinho Pão de Açúcar",
        "required_links": "es/index.html,es/cafe-da-manha.html,es/eventos.html",
    },
    "es/eventos.html": {
        "lang": "es",
        "snippet_topic": "Cómo hacer un evento en Morro da Urca",
        "required_links": "es/index.html,es/cafe-da-manha.html,es/almoco.html",
    },
    "es/atardecer.html": {
        "lang": "es",
        "snippet_topic": "Cómo vivir el atardecer en Morro da Urca",
        "required_links": "es/index.html,es/eventos.html",
    },
}

SKIP_SCHEMES = {"mailto", "tel", "sms", "whatsapp", "javascript", "data"}
NON_HTML_EXTS = frozenset({
    '.css', '.js', '.webp', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
    '.xml', '.json', '.pdf', '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.webm', '.txt',
})
HREF_RE = re.compile(r'\s(?:href|src)=["\']([^"\']+)["\']', re.I)
ID_RE = re.compile(r'\s(?:id|name)=["\']([^"\']+)["\']', re.I)
OL_RE = re.compile(r'<ol\b[\s\S]*?</ol>', re.I)
LI_RE = re.compile(r'<li\b[\s\S]*?</li>', re.I)
TAG_RE = re.compile(r'<[^>]+>')
HEADING_RE = re.compile(r'<h[1-6][^>]*>([\s\S]*?)</h[1-6]>', re.I)


@dataclass
class LinkIssue:
    page: str
    href: str
    reason: str
    resolved_target: str | None = None


@dataclass
class PageAudit:
    page: str
    exists: bool
    lang: str
    status: str
    internal_links: int
    broken_links: int
    required_links_total: int
    required_links_found: int
    missing_required_links: list[str]
    ol_count: int
    max_ol_items: int
    has_featured_snippet_ol: bool
    snippet_topic: str
    headings_match_topic: bool
    warnings: list[str]


def strip_tags(value: str) -> str:
    return unescape(TAG_RE.sub(" ", value)).strip()


def page_url_for(rel: str) -> str:
    if rel == "index.html":
        return "https://www.embaixadacarioca.com/"
    if rel.endswith("/index.html"):
        return "https://www.embaixadacarioca.com/" + rel[: -len("index.html")]
    return "https://www.embaixadacarioca.com/" + rel


def html_file_for_path(path: str) -> str:
    clean = path.strip("/")
    if not clean:
        return "index.html"
    if clean.endswith("/"):
        return clean + "index.html"
    if clean.endswith(".html"):
        return clean
    candidate_html = clean + ".html"
    if (ROOT / candidate_html).exists():
        return candidate_html
    candidate_index = clean + "/index.html"
    if (ROOT / candidate_index).exists():
        return candidate_index
    return candidate_html


def resolve_internal_target(current_page: str, href: str) -> tuple[str | None, str | None]:
    href = unescape(href).strip()
    if not href or href.startswith("#"):
        return current_page, href[1:] if href.startswith("#") else None

    parsed = urlparse(href)
    if parsed.scheme and parsed.scheme.lower() in SKIP_SCHEMES:
        return None, None
    # Skip non-HTML resources (CSS, JS, images, fonts, etc.)
    path_ext = Path(parsed.path).suffix.lower() if parsed.path else ''
    if path_ext in NON_HTML_EXTS:
        return None, None
    if parsed.netloc and parsed.netloc not in SITE_HOSTS:
        return None, None

    if parsed.netloc in {"embaixadacarioca.com.br", "www.embaixadacarioca.com.br"}:
        # Canonical consolidation should avoid internal .com.br links.
        path = html_file_for_path(parsed.path)
        return path, parsed.fragment or None

    raw_path = parsed.path
    if not parsed.netloc and not raw_path.startswith("/"):
        base_dir = posixpath.dirname(current_page)
        raw_path = posixpath.normpath(posixpath.join(base_dir, raw_path))
    target = html_file_for_path(raw_path)
    return target, parsed.fragment or None


def existing_anchors(html: str) -> set[str]:
    return {unescape(m.group(1)).strip() for m in ID_RE.finditer(html) if m.group(1).strip()}


def audit_links(page: str, html: str) -> tuple[int, list[LinkIssue], set[str]]:
    issues: list[LinkIssue] = []
    seen_targets: set[str] = set()
    internal_count = 0
    cache_html: dict[str, str] = {page: html}
    for href in HREF_RE.findall(html):
        target, fragment = resolve_internal_target(page, href)
        if target is None:
            continue
        internal_count += 1
        seen_targets.add(target)
        target_path = ROOT / target
        if not target_path.exists():
            issues.append(LinkIssue(page=page, href=href, reason="target file missing", resolved_target=target))
            continue
        if fragment:
            if target not in cache_html:
                cache_html[target] = target_path.read_text(encoding="utf-8", errors="ignore")
            anchors = existing_anchors(cache_html[target])
            if fragment not in anchors:
                issues.append(LinkIssue(page=page, href=href, reason="target anchor missing", resolved_target=f"{target}#{fragment}"))
    return internal_count, issues, seen_targets


def audit_snippets(html: str, topic: str) -> tuple[int, int, bool, bool]:
    ol_blocks = OL_RE.findall(html)
    ol_count = len(ol_blocks)
    max_items = 0
    for block in ol_blocks:
        max_items = max(max_items, len(LI_RE.findall(block)))
    has_snippet_ol = ol_count > 0 and max_items >= 3
    topic_words = [w.lower() for w in re.findall(r'[\wÀ-ÿ]+', topic) if len(w) > 3]
    heading_text = " ".join(strip_tags(m.group(1)).lower() for m in HEADING_RE.finditer(html))
    headings_match = any(word in heading_text for word in topic_words[:4]) if topic_words else False
    return ol_count, max_items, has_snippet_ol, headings_match


def audit_page(page: str, cfg: dict[str, str]) -> tuple[PageAudit, list[LinkIssue]]:
    path = ROOT / page
    if not path.exists():
        return PageAudit(
            page=page,
            exists=False,
            lang=cfg.get("lang", ""),
            status="FAIL",
            internal_links=0,
            broken_links=0,
            required_links_total=len(cfg.get("required_links", "").split(",")) if cfg.get("required_links") else 0,
            required_links_found=0,
            missing_required_links=[x for x in cfg.get("required_links", "").split(",") if x],
            ol_count=0,
            max_ol_items=0,
            has_featured_snippet_ol=False,
            snippet_topic=cfg.get("snippet_topic", ""),
            headings_match_topic=False,
            warnings=["file missing"],
        ), []

    html = path.read_text(encoding="utf-8", errors="ignore")
    internal_count, link_issues, seen_targets = audit_links(page, html)
    required = [x.strip() for x in cfg.get("required_links", "").split(",") if x.strip()]
    missing_required = [target for target in required if target not in seen_targets]
    ol_count, max_items, has_snippet_ol, headings_match = audit_snippets(html, cfg.get("snippet_topic", ""))

    warnings: list[str] = []
    if link_issues:
        warnings.append(f"{len(link_issues)} broken internal link(s)")
    if missing_required:
        warnings.append("missing required cross-links: " + ", ".join(missing_required))
    if not has_snippet_ol:
        warnings.append("missing featured-snippet-ready ordered list with at least 3 items")
    if not headings_match:
        warnings.append("no heading appears to match the target snippet topic")

    status = "PASS" if not link_issues and not missing_required and has_snippet_ol else "FAIL"
    return PageAudit(
        page=page,
        exists=True,
        lang=cfg.get("lang", ""),
        status=status,
        internal_links=internal_count,
        broken_links=len(link_issues),
        required_links_total=len(required),
        required_links_found=len(required) - len(missing_required),
        missing_required_links=missing_required,
        ol_count=ol_count,
        max_ol_items=max_items,
        has_featured_snippet_ol=has_snippet_ol,
        snippet_topic=cfg.get("snippet_topic", ""),
        headings_match_topic=headings_match,
        warnings=warnings,
    ), link_issues


def write_reports(rows: list[PageAudit], link_issues: list[LinkIssue]) -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    status = "PASS" if all(row.status == "PASS" for row in rows) else "FAIL"
    total_pages = len(rows)
    pass_pages = sum(1 for row in rows if row.status == "PASS")
    total_broken = sum(row.broken_links for row in rows)
    total_missing_crosslinks = sum(len(row.missing_required_links) for row in rows)
    snippet_ready = sum(1 for row in rows if row.has_featured_snippet_ol)

    payload: dict[str, Any] = {
        "status": status,
        "summary": {
            "total_pages": total_pages,
            "pass_pages": pass_pages,
            "fail_pages": total_pages - pass_pages,
            "broken_internal_links": total_broken,
            "missing_required_crosslinks": total_missing_crosslinks,
            "featured_snippet_ready_pages": snippet_ready,
        },
        "results": [asdict(row) for row in rows],
        "link_issues": [asdict(issue) for issue in link_issues],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Internal Links + Featured Snippets Audit",
        "",
        f"Status geral: **{status}**",
        "",
        "## Critérios",
        "- Nenhum link interno quebrado nas páginas prioritárias.",
        "- Cross-links obrigatórios presentes entre Home, Café da Manhã, Almoço, Entardecer/Sunset/Atardecer, Eventos e Cardápio.",
        "- Cada página prioritária deve ter pelo menos uma lista ordenada `<ol>` com 3 ou mais itens para Featured Snippets.",
        "- Cada página deve ter um tópico claro de snippet associado ao objetivo de busca.",
        "",
        "## Resumo executivo",
        f"- Páginas auditadas: **{total_pages}**",
        f"- Páginas PASS: **{pass_pages}**",
        f"- Páginas FAIL: **{total_pages - pass_pages}**",
        f"- Links internos quebrados: **{total_broken}**",
        f"- Cross-links obrigatórios ausentes: **{total_missing_crosslinks}**",
        f"- Páginas prontas para Featured Snippets por `<ol>`: **{snippet_ready}/{total_pages}**",
        "",
        "## Resultados por página",
    ]
    for row in rows:
        lines.append(
            f"- `{row.page}` — **{row.status}** — links internos={row.internal_links} — quebrados={row.broken_links} — "
            f"cross-links={row.required_links_found}/{row.required_links_total} — `<ol>`={row.ol_count} — max itens={row.max_ol_items} — tópico: {row.snippet_topic}"
        )
        for warning in row.warnings:
            lines.append(f"  - {warning}")

    if link_issues:
        lines.extend(["", "## Links internos quebrados"])
        for issue in link_issues:
            lines.append(f"- `{issue.page}` → `{issue.href}` — {issue.reason} — resolved: `{issue.resolved_target}`")

    lines.extend([
        "",
        "## Próxima ação recomendada",
        "1. Corrigir links internos quebrados primeiro.",
        "2. Inserir blocos `<ol>` editoriais nas páginas FAIL, com texto visível e natural para o usuário.",
        "3. Reexecutar este script até `Status geral: PASS`.",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Internal links/snippets audit: {status}")
    print(f"Pages: {pass_pages}/{total_pages} PASS")
    print(f"Broken internal links: {total_broken}")
    print(f"Missing required cross-links: {total_missing_crosslinks}")
    print(f"Featured snippet ready pages: {snippet_ready}/{total_pages}")
    return 0 if status == "PASS" else 1


def main() -> int:
    rows: list[PageAudit] = []
    issues: list[LinkIssue] = []
    for page, cfg in PRIORITY_PAGES.items():
        row, page_issues = audit_page(page, cfg)
        rows.append(row)
        issues.extend(page_issues)
    return write_reports(rows, issues)


if __name__ == "__main__":
    raise SystemExit(main())
