#!/usr/bin/env python3
"""Phase 2 audit: performance, SEO structure and conversion readiness.

Scope: current public pages only. No new landing pages.
Checks:
- title / meta description / canonical
- CSS and JS payload signals
- image lazy/eager/preload signals
- hero image preload
- render-blocking density
- CTA/reservation presence
- JSON-LD presence
- internal links to key pages
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "phase2_performance_seo_audit.md"
PAGES = ["index.html", "cafe-da-manha.html", "almoco.html", "cardapio.html", "como-chegar.html", "eventos.html", "guia-do-rio.html"]
KEY_LINKS = ["cafe-da-manha.html", "almoco.html", "cardapio.html", "como-chegar.html", "eventos.html", "guia-do-rio.html"]

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.in_title = False
        self.meta = []
        self.links = []
        self.scripts = []
        self.styles = []
        self.imgs = []
        self.anchors = []
        self.jsonld = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): v or "" for k, v in attrs}
        t = tag.lower()
        if t == "title": self.in_title = True
        if t == "meta": self.meta.append(a)
        if t == "link": self.links.append(a)
        if t == "script":
            self.scripts.append(a)
            if a.get("type") == "application/ld+json": self.jsonld += 1
        if t == "style": self.styles.append(a)
        if t == "img": self.imgs.append(a)
        if t == "a": self.anchors.append(a.get("href", ""))

    def handle_data(self, data):
        if self.in_title: self.title += data

    def handle_endtag(self, tag):
        if tag.lower() == "title": self.in_title = False


def parse(path: Path) -> Parser:
    p = Parser()
    p.feed(path.read_text(encoding="utf-8"))
    return p


def meta_content(p: Parser, name: str) -> str:
    for m in p.meta:
        if m.get("name", "").lower() == name.lower():
            return m.get("content", "")
    return ""


def has_canonical(p: Parser) -> bool:
    return any(l.get("rel") == "canonical" and l.get("href") for l in p.links)


def has_preload_image(p: Parser) -> bool:
    return any(l.get("rel") == "preload" and l.get("as") == "image" for l in p.links)


def has_css(p: Parser, href: str) -> bool:
    return any(href in l.get("href", "") for l in p.links)


def score_page(filename: str, p: Parser, text: str) -> tuple[int, list[str]]:
    score = 100
    issues = []
    title = " ".join(p.title.split())
    desc = meta_content(p, "description")
    if not (35 <= len(title) <= 75):
        score -= 8; issues.append(f"title length suboptimal: {len(title)}")
    if not (110 <= len(desc) <= 170):
        score -= 8; issues.append(f"meta description length suboptimal: {len(desc)}")
    if not has_canonical(p):
        score -= 10; issues.append("missing canonical")
    if p.jsonld == 0:
        score -= 8; issues.append("missing JSON-LD")
    if not has_preload_image(p):
        score -= 8; issues.append("missing hero/image preload")
    if not has_css(p, "ec-stabilization-base.css"):
        score -= 8; issues.append("missing consolidated CSS")
    if len(p.styles) > 12:
        score -= min(15, len(p.styles) - 12); issues.append(f"high inline style blocks: {len(p.styles)}")
    if len(p.scripts) > 18:
        score -= min(10, len(p.scripts) - 18); issues.append(f"high script count: {len(p.scripts)}")
    imgs_without_lazy = [i for i in p.imgs if i.get("loading") not in {"lazy", "eager"}]
    if len(imgs_without_lazy) > 2:
        score -= min(10, len(imgs_without_lazy)); issues.append(f"images missing loading attr: {len(imgs_without_lazy)}")
    imgs_without_alt = [i for i in p.imgs if not i.get("alt", "").strip()]
    if imgs_without_alt:
        score -= min(10, len(imgs_without_alt)); issues.append(f"images missing alt: {len(imgs_without_alt)}")
    if "tagme" not in text.lower() and "reserv" not in text.lower():
        score -= 12; issues.append("reservation CTA not clearly present")
    missing_links = [x for x in KEY_LINKS if x != filename and x not in text]
    if len(missing_links) >= 3:
        score -= min(10, len(missing_links)); issues.append("weak internal link coverage: " + ", ".join(missing_links[:4]))
    return max(score, 0), issues


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Phase 2 Performance & SEO Audit", "", "Scope: existing public pages only. No new landing pages.", ""]
    total = 0
    for filename in PAGES:
        path = ROOT / filename
        lines.append(f"## {filename}")
        if not path.exists():
            lines.append("- FAIL: missing file")
            lines.append("")
            continue
        text = path.read_text(encoding="utf-8")
        p = parse(path)
        score, issues = score_page(filename, p, text)
        total += score
        lines.append(f"- Score: {score}/100")
        lines.append(f"- Title length: {len(' '.join(p.title.split()))}")
        lines.append(f"- Meta description length: {len(meta_content(p, 'description'))}")
        lines.append(f"- Inline style blocks: {len(p.styles)}")
        lines.append(f"- Script tags: {len(p.scripts)}")
        lines.append(f"- Images: {len(p.imgs)}")
        lines.append(f"- JSON-LD blocks: {p.jsonld}")
        if issues:
            lines.append("- Issues:")
            for i in issues: lines.append(f"  - {i}")
        else:
            lines.append("- Issues: none")
        lines.append("")
    avg = round(total / len(PAGES), 1)
    lines.append("## Summary")
    lines.append(f"- Average score: {avg}/100")
    lines.append("- Phase 2 next fixes: reduce inline style density, normalize image loading, preserve CTAs, keep JSON-LD, and prepare performance validation.")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
