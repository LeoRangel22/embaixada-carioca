#!/usr/bin/env python3
"""Audit and lightly stabilize existing page structure before new landing pages.

Scope:
- Existing public pages only.
- No new landing pages.
- Safe automatic fix: inject consolidated stabilization CSS link.
- Audit only: H1/H2 duplication, image alt quality, internal links, repeated content signals.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "existing_pages_content_structure_audit.md"
CSS_HREF = "/assets/css/ec-stabilization-base.css"
CSS_LINK = f'<link rel="stylesheet" href="{CSS_HREF}">'

PAGES = [
    "index.html",
    "cafe-da-manha.html",
    "almoco.html",
    "cardapio.html",
    "como-chegar.html",
    "eventos.html",
    "guia-do-rio.html",
]

EXPECTED_INTERNAL_LINKS = {
    "index.html": ["cafe-da-manha.html", "almoco.html", "cardapio.html", "eventos.html", "como-chegar.html"],
    "cafe-da-manha.html": ["index.html", "almoco.html", "cardapio.html", "como-chegar.html"],
    "almoco.html": ["index.html", "cardapio.html", "cafe-da-manha.html", "como-chegar.html"],
    "cardapio.html": ["index.html", "cafe-da-manha.html", "almoco.html", "eventos.html"],
    "como-chegar.html": ["index.html", "cafe-da-manha.html", "almoco.html", "cardapio.html"],
    "eventos.html": ["index.html", "cardapio.html", "como-chegar.html"],
    "guia-do-rio.html": ["index.html", "cafe-da-manha.html", "almoco.html", "eventos.html", "como-chegar.html"],
}

STRATEGIC_ALT_TERMS = [
    "Embaixada Carioca",
    "Morro da Urca",
    "Pão de Açúcar",
    "Bondinho",
    "Rio de Janeiro",
    "Urca",
    "vista",
]

GENERIC_ALT = {
    "foto", "imagem", "img", "banner", "hero", "restaurante", "café", "cafe", "mesa", "prato", "view", "image", "photo"
}

REPETITION_PHRASES = [
    "morro da urca",
    "pão de açúcar",
    "parque bondinho",
    "vista para o pão de açúcar",
    "café da manhã com vista",
    "restaurante no morro da urca",
    "rio de janeiro",
    "embaixada carioca",
]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.current_heading: str | None = None
        self.heading_buf: list[str] = []
        self.headings: list[tuple[str, str]] = []
        self.imgs: list[dict[str, str]] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k.lower(): v or "" for k, v in attrs}
        if tag.lower() in {"h1", "h2", "h3"}:
            self.current_heading = tag.lower()
            self.heading_buf = []
        if tag.lower() == "img":
            self.imgs.append({"src": attr.get("src", ""), "alt": attr.get("alt", "")})
        if tag.lower() == "a" and attr.get("href"):
            self.links.append(attr["href"])

    def handle_data(self, data: str) -> None:
        if self.current_heading:
            self.heading_buf.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.current_heading and tag.lower() == self.current_heading:
            text = " ".join("".join(self.heading_buf).split())
            self.headings.append((self.current_heading, text))
            self.current_heading = None
            self.heading_buf = []


def strip_scripts_and_styles(html: str) -> str:
    html = re.sub(r"<script\b.*?</script>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<style\b.*?</style>", " ", html, flags=re.I | re.S)
    return html


def visible_text(html: str) -> str:
    html = strip_scripts_and_styles(html)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def inject_css_if_missing(path: Path, html: str) -> tuple[str, bool]:
    if CSS_HREF in html:
        return html, False
    # Prefer after fonts.css if present, otherwise before </head>.
    font_link = re.search(r"<link[^>]+fonts\.css[^>]*>", html, flags=re.I)
    if font_link:
        pos = font_link.end()
        return html[:pos] + "\n" + CSS_LINK + html[pos:], True
    if "</head>" in html.lower():
        return re.sub(r"</head>", CSS_LINK + "\n</head>", html, count=1, flags=re.I), True
    return html, False


def alt_quality(alt: str) -> str:
    normalized = re.sub(r"\s+", " ", alt.strip())
    if not normalized:
        return "missing"
    if normalized.lower() in GENERIC_ALT or len(normalized) < 18:
        return "generic"
    if not any(term.lower() in normalized.lower() for term in STRATEGIC_ALT_TERMS):
        return "non-strategic"
    return "ok"


def href_matches(links: list[str], target: str) -> bool:
    clean = target.replace("index.html", "")
    for href in links:
        h = href.split("#", 1)[0].split("?", 1)[0]
        if h == target or h.endswith("/" + target) or (clean and h.endswith(clean)):
            return True
    return False


def audit_page(filename: str) -> dict[str, object]:
    path = ROOT / filename
    html = path.read_text(encoding="utf-8")
    new_html, css_injected = inject_css_if_missing(path, html)
    if css_injected:
        path.write_text(new_html, encoding="utf-8")
        html = new_html

    parser = PageParser()
    parser.feed(html)

    h1s = [text for tag, text in parser.headings if tag == "h1"]
    h2s = [text for tag, text in parser.headings if tag == "h2"]
    h2_dupes = [h for h, count in Counter(h2s).items() if count > 1 and h]

    imgs_by_quality = defaultdict(list)
    for img in parser.imgs:
        imgs_by_quality[alt_quality(img.get("alt", ""))].append(img)

    missing_links = [target for target in EXPECTED_INTERNAL_LINKS[filename] if not href_matches(parser.links, target)]

    text = visible_text(html).lower()
    word_count = len(text.split())
    repetition = []
    for phrase in REPETITION_PHRASES:
        count = text.count(phrase)
        if word_count and count >= 8:
            per_1000 = round(count / max(word_count, 1) * 1000, 2)
            repetition.append((phrase, count, per_1000))

    return {
        "css_injected": css_injected,
        "h1s": h1s,
        "h2_count": len(h2s),
        "h2_dupes": h2_dupes,
        "img_count": len(parser.imgs),
        "alt_missing": imgs_by_quality["missing"],
        "alt_generic": imgs_by_quality["generic"],
        "alt_non_strategic": imgs_by_quality["non-strategic"],
        "alt_ok": imgs_by_quality["ok"],
        "missing_links": missing_links,
        "word_count": word_count,
        "repetition": repetition,
    }


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# Existing Pages Content Structure Audit")
    lines.append("")
    lines.append("Scope: current pages only. No new landing pages were created.")
    lines.append("")

    total_issues = 0
    for filename in PAGES:
        path = ROOT / filename
        lines.append(f"## {filename}")
        if not path.exists():
            lines.append("- FAIL: file missing")
            total_issues += 1
            lines.append("")
            continue
        data = audit_page(filename)
        h1s = data["h1s"]
        h1_status = "PASS" if len(h1s) == 1 else "WARN"
        if h1_status == "WARN":
            total_issues += 1
        lines.append(f"- CSS consolidated link: {'ADDED' if data['css_injected'] else 'already present'}")
        lines.append(f"- H1 count: {len(h1s)} — {h1_status}")
        for h in h1s:
            lines.append(f"  - H1: {h}")
        lines.append(f"- H2 count: {data['h2_count']}")
        if data["h2_dupes"]:
            total_issues += len(data["h2_dupes"])
            lines.append("- WARN: duplicated H2 headings:")
            for h in data["h2_dupes"]:
                lines.append(f"  - {h}")
        else:
            lines.append("- H2 duplicates: PASS")

        alt_issue_count = len(data["alt_missing"]) + len(data["alt_generic"]) + len(data["alt_non_strategic"])
        total_issues += alt_issue_count
        lines.append(f"- Images: {data['img_count']}")
        lines.append(f"- Alt OK: {len(data['alt_ok'])}")
        lines.append(f"- Alt missing: {len(data['alt_missing'])}")
        lines.append(f"- Alt generic: {len(data['alt_generic'])}")
        lines.append(f"- Alt non-strategic: {len(data['alt_non_strategic'])}")
        for label, items in [("missing", data["alt_missing"]), ("generic", data["alt_generic"]), ("non-strategic", data["alt_non_strategic"] )]:
            for img in items[:8]:
                lines.append(f"  - {label}: src={img.get('src','')[:120]} alt={img.get('alt','')[:120]}")
            if len(items) > 8:
                lines.append(f"  - ... +{len(items)-8} more")

        if data["missing_links"]:
            total_issues += len(data["missing_links"])
            lines.append("- WARN: missing strategic internal links:")
            for link in data["missing_links"]:
                lines.append(f"  - {link}")
        else:
            lines.append("- Strategic internal links: PASS")

        if data["repetition"]:
            total_issues += len(data["repetition"])
            lines.append("- WARN: high repeated phrase signals:")
            for phrase, count, per_1000 in data["repetition"]:
                lines.append(f"  - {phrase}: {count} uses ({per_1000}/1k words)")
        else:
            lines.append("- Repetition signals: PASS")
        lines.append("")

    lines.append("## Summary")
    lines.append(f"- Total issues/signals: {total_issues}")
    lines.append("- Auto-fix applied: consolidated CSS link injection only.")
    lines.append("- Manual/next automated passes: headings normalization, alt text rewrite, internal link insertion, copy deduplication.")
    lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
