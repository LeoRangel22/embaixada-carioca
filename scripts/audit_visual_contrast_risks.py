#!/usr/bin/env python3
"""Audit visual contrast risks in current public pages.

This static guardrail detects patterns that previously created visual regressions.
It now classifies findings as:
- PASS/COVERED: pattern is covered by the global contrast hotfix CSS.
- OPEN: pattern still needs a code/CSS fix.
- VISUAL_CHECK: covered or ambiguous pattern that must still be confirmed in browser screenshots.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "visual_contrast_risk_audit.md"
HOTFIX = ROOT / "assets" / "css" / "ec-contrast-hotfix.css"

PAGES = [
    "index.html",
    "cafe-da-manha.html",
    "almoco.html",
    "cardapio.html",
    "como-chegar.html",
    "eventos.html",
    "guia-do-rio.html",
]

LOW_CONTRAST_LIGHT_TEXT = ["#ede2c9", "#f6efde", "rgba(237,226,201", "rgba(246,239,222", "rgb(237,226,201", "rgb(246,239,222"]
LOW_CONTRAST_DARK_TEXT = ["#00405a", "#00202e", "#335d4a", "#485156", "rgba(0,64,90", "rgba(0,32,46", "rgba(72,81,86"]
LIGHT_BACKGROUND_HINTS = ["#fff", "white", "#f6efde", "#ede2c9", "246,239,222", "237,226,201"]
DARK_BACKGROUND_HINTS = ["#00202e", "#00405a", "0,32,46", "0,64,90"]
IMPORTANT_TEXT_CLASSES = ["lede", "copy", "description", "sec-head", "card", "box", "guide-card", "place-card", "beach-card", "experience-card", "route-card", "faq-answer"]

HOTFIX_COVERAGE_MARKERS = [
    "FINAL DARK SECTION LOCK",
    "Final light card paragraph lock",
    "body main :is(.card,.box,.card-light",
    "body main section:not(.light-section)",
    "ec-hotfix-gray",
    "ec-hotfix-green",
]


class ContrastParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[dict[str, str]] = []
        self.findings: list[dict[str, str]] = []
        self.current_text_tag: dict[str, str] | None = None
        self.text_buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k.lower(): v or "" for k, v in attrs}
        node = {"tag": tag.lower(), "class": attr.get("class", ""), "style": attr.get("style", ""), "id": attr.get("id", "")}
        self.stack.append(node)
        if tag.lower() in {"h1", "h2", "h3", "h4", "p", "li", "span", "small", "summary"}:
            self.current_text_tag = node
            self.text_buffer = []

    def handle_data(self, data: str) -> None:
        if self.current_text_tag is not None:
            self.text_buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.current_text_tag is not None and tag.lower() == self.current_text_tag.get("tag"):
            text = " ".join("".join(self.text_buffer).split())
            if len(text) >= 28:
                self.inspect_text_node(self.current_text_tag, text)
            self.current_text_tag = None
            self.text_buffer = []
        if self.stack:
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i].get("tag") == tag.lower():
                    del self.stack[i:]
                    break

    def ancestors(self) -> list[dict[str, str]]:
        return self.stack[:-1]

    def inspect_text_node(self, node: dict[str, str], text: str) -> None:
        style_context = " ".join(item.get("style", "") for item in self.ancestors() + [node]).lower()
        class_context = " ".join(item.get("class", "") for item in self.ancestors() + [node]).lower()
        is_important = any(c in class_context for c in IMPORTANT_TEXT_CLASSES) or node.get("tag") in {"h1", "h2", "h3", "p"}
        if not is_important:
            return

        has_light_bg = any(h in style_context for h in LIGHT_BACKGROUND_HINTS) or any(k in class_context for k in ["card", "box", "paper", "light"])
        has_dark_bg = any(h in style_context for h in DARK_BACKGROUND_HINTS) or any(k in class_context for k in ["hero", "dark", "navy"])
        has_light_text = any(c in style_context for c in LOW_CONTRAST_LIGHT_TEXT)
        has_dark_text = any(c in style_context for c in LOW_CONTRAST_DARK_TEXT)

        if has_light_bg and has_light_text:
            self.findings.append({"type": "light-text-on-light-bg", "tag": node.get("tag", ""), "class": node.get("class", ""), "coverage": "covered-by-light-card-lock", "text": text[:160]})
        if has_dark_bg and has_dark_text:
            self.findings.append({"type": "dark-text-on-dark-bg", "tag": node.get("tag", ""), "class": node.get("class", ""), "coverage": "covered-by-dark-section-lock", "text": text[:160]})
        if "sec-head" in class_context and "lede" in class_context and not has_light_bg:
            self.findings.append({"type": "dark-section-lede-needs-visual-check", "tag": node.get("tag", ""), "class": node.get("class", ""), "coverage": "covered-by-final-dark-section-lock", "text": text[:160]})


def hotfix_has_expected_coverage() -> bool:
    if not HOTFIX.exists():
        return False
    css = HOTFIX.read_text(encoding="utf-8")
    return all(marker in css for marker in HOTFIX_COVERAGE_MARKERS)


def audit_page(path: Path) -> list[dict[str, str]]:
    parser = ContrastParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.findings


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    hotfix_ok = hotfix_has_expected_coverage()
    lines = ["# Visual Contrast Risk Audit", "", "Static guardrail for visual contrast regressions in current pages.", "", f"- Global contrast hotfix coverage: {'PASS' if hotfix_ok else 'FAIL'}", ""]
    total_findings = 0
    total_open = 0
    total_visual_check = 0

    for filename in PAGES:
        path = ROOT / filename
        lines.append(f"## {filename}")
        if not path.exists():
            lines.append("- FAIL: file missing")
            lines.append("")
            total_open += 1
            continue
        findings = audit_page(path)
        total_findings += len(findings)
        if not findings:
            lines.append("- PASS: no static contrast risk patterns found")
        elif hotfix_ok:
            total_visual_check += len(findings)
            lines.append(f"- VISUAL_CHECK: {len(findings)} pattern(s) detected but covered by global contrast hotfix")
            for item in findings[:20]:
                lines.append(f"  - {item['coverage']} | {item['type']} | <{item['tag']}> class='{item['class']}' | {item['text']}")
            if len(findings) > 20:
                lines.append(f"  - ... +{len(findings) - 20} more")
        else:
            total_open += len(findings)
            lines.append(f"- OPEN: {len(findings)} uncovered static risk(s)")
            for item in findings[:30]:
                lines.append(f"  - {item['type']} | <{item['tag']}> class='{item['class']}' | {item['text']}")
            if len(findings) > 30:
                lines.append(f"  - ... +{len(findings) - 30} more")
        lines.append("")

    lines.append("## Summary")
    lines.append(f"- Total static patterns detected: {total_findings}")
    lines.append(f"- Open contrast risks: {total_open}")
    lines.append(f"- Covered patterns requiring browser visual check: {total_visual_check}")
    lines.append("- Required next validation: browser screenshots for cafe-da-manha.html, guia-do-rio.html, index.html, almoco.html, cardapio.html and eventos.html after deployment.")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
