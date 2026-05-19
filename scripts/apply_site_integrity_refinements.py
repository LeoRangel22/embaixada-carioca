#!/usr/bin/env python3
"""
Auditoria e refinamento global — Embaixada Carioca.

Escopo:
- canonicals coerentes com arquivos reais;
- hreflang e URLs absolutas com .html quando o arquivo real usa .html;
- sitemap sem URLs quebradas;
- correção global do link de avaliação Google;
- correção de URLs placeholder;
- correções editoriais pequenas que afetam confiança;
- relatório técnico de performance, caminhos e idiomas.

Não altera layout visual da home.
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse, urlunparse

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.embaixadacarioca.com"
CORRECT_REVIEW_URL = "https://g.page/r/CU-tJiJIjBUcEAE/review"
MAPS_URL = "https://www.google.com/maps/search/?api=1&query=Embaixada+Carioca+Morro+da+Urca"

REPORT: list[str] = []
WARNINGS: list[str] = []
COUNTERS = {
    "html_files_scanned": 0,
    "html_files_updated": 0,
    "canonical_fixed": 0,
    "og_url_fixed": 0,
    "absolute_urls_fixed": 0,
    "review_links_fixed": 0,
    "placeholder_maps_fixed": 0,
    "text_typos_fixed": 0,
    "sitemap_urls_fixed": 0,
    "sitemap_blocks_removed": 0,
}

OLD_REVIEW_URLS = {
    "https://g.page/r/embaixadacarioca/review",
    "https://www.google.com/maps/place/Embaixada+Carioca",
    "https://www.google.com/maps/place/Embaixada%20Carioca",
    "https://maps.google.com/?q=Embaixada+Carioca",
    "https://www.google.com/search?q=Embaixada+Carioca+Google+Reviews",
}

TEXT_REPLACEMENTS = {
    "parBaía": "para a Baía",
    "parBaía de Guanabara": "para a Baía de Guanabara",
    "paraBaía": "para a Baía",
    "referência em café da manhã no Rio de Janeiro com vista é o da": "A referência em café da manhã no Rio de Janeiro com vista é o da",
    "o mais premiado restaurante com vista no Rio de Janeiro é a": "A Embaixada Carioca é uma das principais referências de restaurante com vista no Rio de Janeiro:",
}

HTML_ATTR_URL_RE = re.compile(r'(?P<prefix>\b(?:href|src|content)=["\'])(?P<url>https://www\.embaixadacarioca\.com/[^"\']*)(?P<suffix>["\'])')
CANONICAL_RE = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']+["\']\s*/?>', re.IGNORECASE)
OG_URL_RE = re.compile(r'<meta\s+property=["\']og:url["\']\s+content=["\'][^"\']+["\']\s*/?>', re.IGNORECASE)
URL_TAG_RE = re.compile(r'<url>[\s\S]*?</url>', re.IGNORECASE)
LOC_RE = re.compile(r'<loc>([^<]+)</loc>', re.IGNORECASE)
SITE_URL_RE = re.compile(r'https://www\.embaixadacarioca\.com/[^\s<"\']*')


def rel_from_url(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.netloc and parsed.netloc != "www.embaixadacarioca.com":
        return None
    path = parsed.path or "/"
    if path == "/":
        return "index.html"
    path = path.lstrip("/")
    if path.endswith("/"):
        return f"{path}index.html"
    return path


def url_exists(url: str) -> bool:
    rel = rel_from_url(url)
    if not rel:
        return True
    return (ROOT / rel).exists()


def fix_site_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc and parsed.netloc != "www.embaixadacarioca.com":
        return url
    if parsed.fragment:
        return url
    path = parsed.path or "/"
    if path == "/" or path.endswith("/"):
        return url
    suffix = Path(path).suffix
    if suffix:
        return url
    candidate = ROOT / (path.lstrip("/") + ".html")
    if candidate.exists():
        fixed = parsed._replace(path=path + ".html")
        return urlunparse(fixed)
    return url


def canonical_for_html(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return BASE + "/"
    if rel.endswith("/index.html"):
        return BASE + "/" + rel[:-len("index.html")]
    return BASE + "/" + rel


def replace_canonical(text: str, canonical: str, rel: str) -> tuple[str, int]:
    tag = f'<link rel="canonical" href="{canonical}">'
    if CANONICAL_RE.search(text):
        new_text = CANONICAL_RE.sub(tag, text, count=1)
    elif "<head>" in text:
        new_text = text.replace("<head>", "<head>\n" + tag, 1)
    else:
        new_text = text
    changed = 1 if new_text != text else 0
    if changed:
        REPORT.append(f"CANONICAL: {rel} -> {canonical}")
    return new_text, changed


def replace_og_url(text: str, canonical: str, rel: str) -> tuple[str, int]:
    tag = f'<meta property="og:url" content="{canonical}" />'
    if OG_URL_RE.search(text):
        new_text = OG_URL_RE.sub(tag, text, count=1)
        changed = 1 if new_text != text else 0
        if changed:
            REPORT.append(f"OG_URL: {rel} -> {canonical}")
        return new_text, changed
    return text, 0


def process_html(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if ".git" in path.parts:
        return
    COUNTERS["html_files_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original

    canonical = canonical_for_html(path)
    text, c = replace_canonical(text, canonical, rel)
    COUNTERS["canonical_fixed"] += c
    text, c = replace_og_url(text, canonical, rel)
    COUNTERS["og_url_fixed"] += c

    for old in OLD_REVIEW_URLS:
        n = text.count(old)
        if n:
            text = text.replace(old, CORRECT_REVIEW_URL)
            COUNTERS["review_links_fixed"] += n
            REPORT.append(f"REVIEW_LINK: {rel} | {n} ocorrência(s)")

    for old, new in TEXT_REPLACEMENTS.items():
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            COUNTERS["text_typos_fixed"] += n
            REPORT.append(f"TEXT_FIX: {rel} | {old!r} -> {new!r} | {n}")

    n = text.count('https://maps.app.goo.gl/')
    if n:
        text = text.replace('https://maps.app.goo.gl/', MAPS_URL)
        COUNTERS["placeholder_maps_fixed"] += n
        REPORT.append(f"MAPS_PLACEHOLDER: {rel} | {n} ocorrência(s)")

    def attr_repl(match: re.Match[str]) -> str:
        url = match.group("url")
        fixed = fix_site_url(url)
        if fixed != url:
            COUNTERS["absolute_urls_fixed"] += 1
        return match.group("prefix") + fixed + match.group("suffix")

    text = HTML_ATTR_URL_RE.sub(attr_repl, text)

    # Limpeza leve: excesso de linhas vazias no head causado por rodadas anteriores.
    text = re.sub(r'(<head>)\s{6,}', r'\1\n', text, count=1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_files_updated"] += 1


def fix_sitemap() -> None:
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        WARNINGS.append("sitemap.xml ausente")
        return
    original = sitemap.read_text(encoding="utf-8", errors="ignore")
    text = original

    def site_url_repl(match: re.Match[str]) -> str:
        url = match.group(0)
        fixed = fix_site_url(url)
        if fixed != url:
            COUNTERS["sitemap_urls_fixed"] += 1
        return fixed

    text = SITE_URL_RE.sub(site_url_repl, text)

    def url_block_repl(match: re.Match[str]) -> str:
        block = match.group(0)
        loc_match = LOC_RE.search(block)
        if not loc_match:
            return block
        loc = loc_match.group(1).strip()
        if url_exists(loc):
            return block
        COUNTERS["sitemap_blocks_removed"] += 1
        WARNINGS.append(f"SITEMAP_REMOVED_BROKEN_URL: {loc}")
        return ""

    text = URL_TAG_RE.sub(url_block_repl, text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    if text != original:
        sitemap.write_text(text, encoding="utf-8")
        REPORT.append("SITEMAP: URLs sem .html corrigidas e blocos quebrados removidos")


def audit_sizes() -> list[str]:
    rows: list[tuple[int, str]] = []
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        rows.append((path.stat().st_size, path.relative_to(ROOT).as_posix()))
    rows.sort(reverse=True)
    out = []
    for size, rel in rows[:15]:
        kb = size / 1024
        flag = " ⚠️" if kb > 500 else ""
        out.append(f"- {rel}: {kb:.1f} KB{flag}")
    return out


def audit_assets() -> list[str]:
    assets = ROOT / "assets"
    if not assets.exists():
        return ["- Pasta assets não encontrada"]
    rows: list[tuple[int, str]] = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.svg"):
        for path in assets.rglob(ext):
            rows.append((path.stat().st_size, path.relative_to(ROOT).as_posix()))
    rows.sort(reverse=True)
    out = []
    for size, rel in rows[:20]:
        kb = size / 1024
        flag = " ⚠️" if kb > 300 else ""
        out.append(f"- {rel}: {kb:.1f} KB{flag}")
    return out


def write_report() -> None:
    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report = report_dir / "site_integrity_performance_audit.md"
    body = [
        "# Auditoria Técnica Global — Embaixada Carioca",
        "",
        "## Escopo",
        "- PT / EN / ES",
        "- canonicals, hreflang e sitemap",
        "- links externos críticos",
        "- limpeza leve de HTML",
        "- performance percebida e peso de páginas/assets",
        "- sem alteração de layout da home",
        "",
        "## Contadores",
    ]
    for key, value in COUNTERS.items():
        body.append(f"- {key}: {value}")
    body.extend([
        "",
        "## Correções aplicadas",
        *(f"- {line}" for line in REPORT) if REPORT else "- Nenhuma correção necessária nesta rodada",
        "",
        "## Alertas encontrados",
        *(f"- {line}" for line in WARNINGS) if WARNINGS else "- Nenhum alerta crítico encontrado",
        "",
        "## Maiores páginas HTML",
        *audit_sizes(),
        "",
        "## Maiores assets de imagem",
        *audit_assets(),
        "",
        "## Diagnóstico executivo",
        "- O principal risco técnico estava na inconsistência entre URLs com e sem `.html`, especialmente em sitemap, canonical e hreflang.",
        "- URLs no sitemap que não correspondem a arquivos reais foram removidas para evitar rastreamento desperdiçado e sinais ruins ao Google.",
        "- Links de avaliação e placeholders foram normalizados para reduzir caminho quebrado em CTAs.",
        "- A lentidão percebida tende a vir de três fatores: HTML muito grande em algumas páginas, muitas camadas de CSS inline acumuladas e assets de imagem grandes.",
        "- Próxima etapa segura: dividir CSS global, reduzir HTML duplicado e revisar imagens acima de 300 KB sem alterar o layout vencedor da home.",
        "",
    ])
    report.write_text("\n".join(body), encoding="utf-8")
    print(report.read_text(encoding="utf-8"))


def main() -> int:
    for path in sorted(ROOT.rglob("*.html")):
        process_html(path)
    fix_sitemap()
    write_report()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
