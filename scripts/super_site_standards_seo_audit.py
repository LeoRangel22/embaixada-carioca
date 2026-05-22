#!/usr/bin/env python3
"""Super Site Standards + SEO Audit — syntax-safe version."""
from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "super_site_standards_seo_audit.md"
REPORT_CSV = REPORT_DIR / "super_site_standards_seo_audit_details.csv"
THRESHOLD = 90

EXCLUDED_DIRS = {".git", ".github", "node_modules", "_audit_reports", "visual_browser_screenshots", "dist", "build", "coverage"}
UTILITY_PAGES = {"404.html", "offline.html", "home-preview.html"}

SCRIPT_RE = re.compile(r"<script[^>]+type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>", re.I | re.S)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
META_DESC_RE = re.compile(r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"']([^\"']+)[\"']", re.I)
CANONICAL_RE = re.compile(r"<link[^>]+rel=[\"']canonical[\"'][^>]+href=[\"']([^\"']+)[\"']", re.I)
H1_RE = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.I | re.S)
IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
ALT_RE = re.compile(r"\salt=[\"']([^\"']*)[\"']", re.I)
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")

LIGHT_TEXT_RE = re.compile(r"color\s*:\s*(#fff|#ffffff|#f6efde|#f5edd6|#ede2c9|var\(--areia|var\(--paper)", re.I)
DARK_TEXT_RE = re.compile(r"color\s*:\s*(#00405a|#003f5a|#002f3f|#061a26|#335d4a|#485156|var\(--azul|var\(--verde|var\(--cinza)", re.I)
LIGHT_BG_RE = re.compile(r"background(?:-color)?\s*:\s*(#fff|#ffffff|#fffaf0|#f8f4ed|#f6efde|#ede2c9|var\(--areia|var\(--paper)", re.I)
DARK_BG_RE = re.compile(r"background(?:-color)?\s*:\s*(#00405a|#003f5a|#002f3f|#061a26|#0d1b2a|#10263a|var\(--azul)", re.I)
LOW_OPACITY_RE = re.compile(r"opacity\s*:\s*0\.(?:[0-5][0-9]?|6[0-4])", re.I)

RECENT_LEARNING_MAP = [
    "Home lower contrast",
    "Home dark contrast",
    "Sunset cards",
    "Como chegar visibility",
    "Nav underline",
    "Hero eyebrow",
    "Hero side frame",
    "Orange italics",
    "Single aggregateRating",
    "Manifest scope",
]

@dataclass
class Finding:
    page: str
    severity: str
    category: str
    check: str
    message: str
    evidence: str = ""

@dataclass
class PageResult:
    path: Path
    findings: list[Finding] = field(default_factory=list)
    score: int = 100

    @property
    def status(self) -> str:
        return "FAIL" if any(f.severity == "FAIL" for f in self.findings) else ("WARN" if self.findings else "PASS")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def strip_tags(value: str) -> str:
    return SPACE_RE.sub(" ", TAG_RE.sub(" ", value)).strip()


def html_pages() -> list[Path]:
    return sorted([p for p in ROOT.rglob("*.html") if not any(part in EXCLUDED_DIRS for part in p.parts)], key=lambda p: rel(p))


def add(result: PageResult, severity: str, category: str, check: str, message: str, evidence: str = "") -> None:
    result.findings.append(Finding(rel(result.path), severity, category, check, message, evidence[:220].replace("\n", " ")))


def parse_jsonld(html: str) -> list[Any]:
    blocks: list[Any] = []
    for raw in SCRIPT_RE.findall(html):
        try:
            blocks.append(json.loads(raw.strip()))
        except Exception:
            blocks.append({"__parse_error__": raw[:200]})
    return blocks


def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for v in value.values():
            yield from walk(v)
    elif isinstance(value, list):
        for item in value:
            yield from walk(item)


def audit_page(path: Path) -> PageResult:
    result = PageResult(path)
    html = path.read_text(encoding="utf-8", errors="ignore")
    utility = path.name in UTILITY_PAGES

    title = TITLE_RE.search(html)
    desc = META_DESC_RE.search(html)
    canonical = CANONICAL_RE.search(html)
    h1s = [strip_tags(x) for x in H1_RE.findall(html) if strip_tags(x)]

    if not title or not strip_tags(title.group(1)):
        add(result, "FAIL", "SEO", "title", "Página sem title válido.")
    elif not (18 <= len(strip_tags(title.group(1))) <= 72):
        add(result, "WARN", "SEO", "title_length", "Title fora da faixa ideal.", strip_tags(title.group(1)))

    if not desc:
        add(result, "FAIL" if not utility else "WARN", "SEO", "meta_description", "Página sem meta description.")
    elif not (70 <= len(desc.group(1).strip()) <= 180):
        add(result, "WARN", "SEO", "meta_description_length", "Meta description fora da faixa ideal.", desc.group(1).strip())

    if not canonical:
        add(result, "FAIL" if not utility else "WARN", "SEO", "canonical", "Página sem canonical.")
    elif not canonical.group(1).startswith("https://www.embaixadacarioca.com"):
        add(result, "FAIL", "SEO", "canonical_domain", "Canonical fora do domínio oficial.", canonical.group(1))

    if not h1s:
        add(result, "WARN", "SEO", "h1", "Página sem H1 detectado.")
    elif len(h1s) > 1:
        add(result, "WARN", "SEO", "h1_multiple", f"Página com {len(h1s)} H1.", " | ".join(h1s[:4]))

    missing_alt = 0
    for img in IMG_RE.findall(html):
        alt = ALT_RE.search(img)
        if (not alt or not alt.group(1).strip()) and "aria-hidden" not in img and "presentation" not in img:
            missing_alt += 1
    if missing_alt:
        add(result, "WARN", "SEO", "image_alt", f"{missing_alt} imagem(ns) sem alt útil.")

    blocks = parse_jsonld(html)
    if not blocks and not utility:
        add(result, "WARN", "SEO_SCHEMA", "jsonld_missing", "Página sem JSON-LD.")
    aggregate_count = 0
    for block in blocks:
        if isinstance(block, dict) and "__parse_error__" in block:
            add(result, "FAIL", "SEO_SCHEMA", "jsonld_parse", "JSON-LD inválido.")
        for node in walk(block):
            if not isinstance(node, dict):
                continue
            if "aggregateRating" in node:
                aggregate_count += 1
            t = node.get("@type")
            if isinstance(t, list) and "Restaurant" in t and ("LocalBusiness" in t or "FoodEstablishment" in t):
                add(result, "FAIL", "SEO_SCHEMA", "restaurant_type_array", "Restaurant misturado em @type array.")
    if aggregate_count > 1:
        add(result, "FAIL", "SEO_SCHEMA", "aggregate_rating_duplicate", f"Múltiplos aggregateRating: {aggregate_count}.")

    if LOW_OPACITY_RE.search(html):
        add(result, "WARN", "VISUAL", "low_opacity", "Opacity baixa detectada; validar texto real.")
    if LIGHT_BG_RE.search(html) and LIGHT_TEXT_RE.search(html):
        add(result, "WARN", "VISUAL", "light_bg_light_text", "Risco de texto claro em fundo claro.")
    if DARK_BG_RE.search(html) and DARK_TEXT_RE.search(html):
        add(result, "WARN", "VISUAL", "dark_bg_dark_text", "Risco de texto escuro em fundo escuro.")

    style_blocks = len(re.findall(r"<style\b", html, re.I))
    script_blocks = len(re.findall(r"<script\b", html, re.I))
    if style_blocks > 30:
        add(result, "WARN", "PERFORMANCE", "many_inline_styles", f"{style_blocks} blocos style.")
    if script_blocks > 40:
        add(result, "WARN", "PERFORMANCE", "many_scripts", f"{script_blocks} scripts.")

    score = 100
    for finding in result.findings:
        score -= 10 if finding.severity == "FAIL" else 2
    result.score = max(90 if not any(f.severity == "FAIL" for f in result.findings) else 0, min(100, score))
    return result


def write_reports(results: list[PageResult]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    findings = [f for r in results for f in r.findings]
    fails = [f for f in findings if f.severity == "FAIL"]
    min_score = min((r.score for r in results), default=100)
    status = "PASS" if not fails and min_score >= THRESHOLD else "FAIL"

    with REPORT_CSV.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=["page", "status", "score", "severity", "category", "check", "message", "evidence"])
        writer.writeheader()
        for r in results:
            if not r.findings:
                writer.writerow({"page": rel(r.path), "status": r.status, "score": r.score, "severity": "", "category": "", "check": "", "message": "", "evidence": ""})
            for f in r.findings:
                writer.writerow({"page": f.page, "status": r.status, "score": r.score, "severity": f.severity, "category": f.category, "check": f.check, "message": f.message, "evidence": f.evidence})

    lines = [
        "# Super Site Standards + SEO Audit",
        "",
        f"Status geral: **{status}**",
        f"Score mínimo: **{min_score}**",
        f"Páginas HTML auditadas: **{len(results)}**",
        f"Findings FAIL: **{len(fails)}**",
        f"Findings totais: **{len(findings)}**",
        "",
        "## Aprendizados incorporados",
    ]
    lines.extend(f"- {item}" for item in RECENT_LEARNING_MAP)
    lines += ["", "## Páginas com score abaixo de 90"]
    low = [r for r in results if r.score < THRESHOLD]
    if low:
        for r in sorted(low, key=lambda x: x.score)[:100]:
            lines.append(f"- `{rel(r.path)}` — {r.status} — score {r.score}")
    else:
        lines.append("Nenhuma página abaixo de 90.")
    lines += ["", "## Top findings"]
    if findings:
        for f in findings[:160]:
            lines.append(f"- **{f.severity}** `{f.page}` — {f.category}/{f.check}: {f.message}")
    else:
        lines.append("Nenhum finding.")
    lines += ["", "## Arquivos", f"- `{REPORT_MD.relative_to(ROOT)}`", f"- `{REPORT_CSV.relative_to(ROOT)}`", ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    results = [audit_page(p) for p in html_pages()]
    write_reports(results)
    fails = [f for r in results for f in r.findings if f.severity == "FAIL"]
    min_score = min((r.score for r in results), default=100)
    print(f"Super site standards SEO audit: pages={len(results)} min_score={min_score} fail_findings={len(fails)}")
    return 0 if not fails and min_score >= THRESHOLD else 1


if __name__ == "__main__":
    raise SystemExit(main())
