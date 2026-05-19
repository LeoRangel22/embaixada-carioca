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
- padronização do topo das principais subpáginas com o topo vencedor da home;
- relatório técnico de performance, caminhos e idiomas.

Não altera a composição principal da home.
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
    "subpage_top_synced": 0,
}

OLD_REVIEW_URLS = {
    "https://g.page/r/embaixadacarioca/review",
    "https://www.google.com/maps/place/Embaixada+Carioca",
    "https://www.google.com/maps/place/Embaixada%20Carioca",
    "https://maps.google.com/?q=Embaixada+Carioca",
    "https://www.google.com/search?q=Embaixada+Carioca+Google+Reviews",
}

TEXT_REPLACEMENTS = {
    "parBaía de Guanabara": "para a Baía de Guanabara",
    "parBaía": "para a Baía",
    "paraBaía": "para a Baía",
    "referência em café da manhã no Rio de Janeiro com vista é o da": "A referência em café da manhã no Rio de Janeiro com vista é o da",
    "o mais premiado restaurante com vista no Rio de Janeiro é a": "A Embaixada Carioca é uma das principais referências de restaurante com vista no Rio de Janeiro:",
}

TARGET_TOP_SYNC_PAGES = {
    "cafe-da-manha.html",
    "almoco.html",
    "entardecer.html",
    "eventos.html",
    "cardapio.html",
    "guia-do-rio.html",
    "en/cafe-da-manha.html",
    "en/almoco.html",
    "en/entardecer.html",
    "en/eventos.html",
    "en/cardapio.html",
    "en/guia-do-rio.html",
    "es/cafe-da-manha.html",
    "es/almoco.html",
    "es/entardecer.html",
    "es/eventos.html",
    "es/cardapio.html",
    "es/guia-do-rio.html",
}

SUBPAGE_HOME_TOP_CSS = r'''
<style id="subpage-home-top-sync">
/* Topo das subpáginas sincronizado com o topo vencedor da home */
@media (min-width:901px){
  body[data-screen-label] nav.top:not(.scrolled){
    min-height:82px!important;
    background:linear-gradient(180deg,rgba(0,32,46,.58) 0%,rgba(0,32,46,.32) 58%,rgba(0,32,46,0) 100%)!important;
    border-bottom:0!important;
    box-shadow:none!important;
    backdrop-filter:none!important;
    -webkit-backdrop-filter:none!important;
  }
  body[data-screen-label] nav.top .nav-inner{
    height:82px!important;
    max-width:none!important;
    margin:0!important;
    padding:10px clamp(48px,3.9vw,76px) 0!important;
    gap:clamp(22px,2vw,36px)!important;
    color:var(--areia-pale,#f6efde)!important;
    align-items:center!important;
  }
  body[data-screen-label] nav.top .brand-mark{
    min-width:138px!important;
    gap:0!important;
    flex:0 0 138px!important;
  }
  body[data-screen-label] nav.top .brand-logo{
    width:62px!important;
    height:62px!important;
    object-fit:contain!important;
  }
  body[data-screen-label] nav.top .brand-logo.light{display:block!important;}
  body[data-screen-label] nav.top .brand-logo.dark{display:none!important;}
  body[data-screen-label] nav.top .brand-word{display:none!important;}
  body[data-screen-label] nav.top .nav-links{
    display:flex!important;
    align-items:center!important;
    gap:clamp(22px,2.05vw,38px)!important;
    margin:0!important;
    padding:0!important;
    flex:0 1 auto!important;
  }
  body[data-screen-label] nav.top .nav-links a,
  body[data-screen-label] nav.top .nav-links a:visited{
    font-family:"JetBrains Mono",ui-monospace,monospace!important;
    font-size:12px!important;
    line-height:1!important;
    letter-spacing:.18em!important;
    font-weight:700!important;
    text-transform:uppercase!important;
    color:rgba(246,239,222,.94)!important;
    opacity:1!important;
    text-decoration:none!important;
  }
  body[data-screen-label] nav.top .nav-links a::after{bottom:-13px!important;height:2px!important;background:var(--amarelo,#f59b1e)!important;}
  body[data-screen-label] nav.top .nav-wa-btn{display:none!important;}
  body[data-screen-label] nav.top .nav-rating-badge,
  body[data-screen-label] nav.top .nav-rating-badge:visited{
    display:flex!important;
    align-items:center!important;
    justify-content:center!important;
    gap:7px!important;
    height:35px!important;
    min-width:205px!important;
    margin-left:auto!important;
    padding:0 18px!important;
    border-radius:999px!important;
    background:rgba(246,239,222,.14)!important;
    border:1px solid rgba(246,239,222,.30)!important;
    color:var(--areia-pale,#f6efde)!important;
    text-decoration:none!important;
    box-shadow:0 8px 22px rgba(0,32,46,.12)!important;
  }
  body[data-screen-label] nav.top .nav-rating-stars{
    color:var(--amarelo,#f59b1e)!important;
    font-size:15px!important;
    font-weight:900!important;
    letter-spacing:.01em!important;
  }
  body[data-screen-label] nav.top .nav-rating-count{
    color:rgba(246,239,222,.78)!important;
    font-size:11px!important;
    font-weight:700!important;
    letter-spacing:.10em!important;
  }
  body[data-screen-label] nav.top .lang-switcher{
    margin:0!important;
    flex:0 0 auto!important;
  }
  body[data-screen-label] nav.top .lang-current{
    height:36px!important;
    padding:0 13px!important;
    border-radius:12px!important;
    background:rgba(246,239,222,.14)!important;
    border:1px solid rgba(246,239,222,.30)!important;
    color:var(--areia-pale,#f6efde)!important;
    font-family:"JetBrains Mono",ui-monospace,monospace!important;
    font-size:12px!important;
    font-weight:800!important;
    letter-spacing:.08em!important;
  }
  body[data-screen-label] nav.top .lang-current span{color:inherit!important;}
  body[data-screen-label] nav.top .btn,
  body[data-screen-label] nav.top .btn:visited{
    height:60px!important;
    min-width:188px!important;
    padding:0 31px!important;
    border-radius:999px!important;
    background:var(--amarelo,#f59b1e)!important;
    border:1px solid var(--amarelo,#f59b1e)!important;
    color:#fff!important;
    font-family:"JetBrains Mono",ui-monospace,monospace!important;
    font-size:14px!important;
    font-weight:900!important;
    letter-spacing:.18em!important;
    text-transform:uppercase!important;
    box-shadow:none!important;
  }
  body[data-screen-label] nav.top .btn:hover{background:var(--amarelo,#f59b1e)!important;color:#fff!important;filter:brightness(1.04)!important;}
  body[data-screen-label] nav.top .nav-hamburger{display:none!important;}
  body[data-screen-label] .page-hero-content .eyebrow.hero-eyebrow{
    position:absolute!important;
    top:95px!important;
    left:clamp(260px,14.2vw,300px)!important;
    right:clamp(220px,14vw,320px)!important;
    width:auto!important;
    max-width:none!important;
    margin:0!important;
    white-space:nowrap!important;
    overflow:hidden!important;
    text-overflow:clip!important;
    font-family:"JetBrains Mono",ui-monospace,monospace!important;
    font-size:10px!important;
    line-height:1!important;
    letter-spacing:.34em!important;
    font-weight:500!important;
    color:var(--amarelo,#f59b1e)!important;
    opacity:1!important;
    text-shadow:0 2px 12px rgba(0,32,46,.66)!important;
    z-index:8!important;
  }
  body[data-screen-label] .page-hero-content .eyebrow.hero-eyebrow::before{
    width:34px!important;
    min-width:34px!important;
    height:1px!important;
    background:var(--amarelo,#f59b1e)!important;
    opacity:1!important;
  }
  body[data-screen-label] .page-hero-content{padding-top:168px!important;}
}
@media (min-width:901px) and (max-width:1240px){
  body[data-screen-label] nav.top .nav-inner{padding-left:34px!important;padding-right:34px!important;gap:16px!important;}
  body[data-screen-label] nav.top .brand-mark{min-width:96px!important;flex-basis:96px!important;}
  body[data-screen-label] nav.top .nav-links{gap:18px!important;}
  body[data-screen-label] nav.top .nav-links a{font-size:10.5px!important;letter-spacing:.13em!important;}
  body[data-screen-label] nav.top .nav-rating-badge{min-width:178px!important;padding:0 12px!important;}
  body[data-screen-label] nav.top .btn{min-width:154px!important;padding:0 22px!important;font-size:12px!important;}
}
</style>
'''

HTML_ATTR_URL_RE = re.compile(r'(?P<prefix>\b(?:href|src|content)=["\'])(?P<url>https://www\.embaixadacarioca\.com/[^"\']*)(?P<suffix>["\'])')
CANONICAL_RE = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']+["\']\s*/?>', re.IGNORECASE)
OG_URL_RE = re.compile(r'<meta\s+property=["\']og:url["\']\s+content=["\'][^"\']+["\']\s*/?>', re.IGNORECASE)
URL_TAG_RE = re.compile(r'<url>[\s\S]*?</url>', re.IGNORECASE)
LOC_RE = re.compile(r'<loc>([^<]+)</loc>', re.IGNORECASE)
SITE_URL_RE = re.compile(r'https://www\.embaixadacarioca\.com/[^\s<"\']*')
TOP_SYNC_RE = re.compile(r'\n*<style id=["\']subpage-home-top-sync["\']>[\s\S]*?</style>\s*', re.IGNORECASE)


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


def sync_subpage_top(text: str, rel: str) -> str:
    if rel not in TARGET_TOP_SYNC_PAGES:
        return text
    cleaned = TOP_SYNC_RE.sub("\n", text)
    if "</head>" not in cleaned:
        WARNINGS.append(f"TOP_SYNC_SKIPPED_NO_HEAD: {rel}")
        return cleaned
    updated = cleaned.replace("</head>", SUBPAGE_HOME_TOP_CSS + "\n</head>", 1)
    COUNTERS["subpage_top_synced"] += 1
    REPORT.append(f"TOP_SYNC: {rel} | topo sincronizado com a home")
    return updated


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

    n = text.count("https://maps.app.goo.gl/")
    if n:
        text = text.replace("https://maps.app.goo.gl/", MAPS_URL)
        COUNTERS["placeholder_maps_fixed"] += n
        REPORT.append(f"MAPS_PLACEHOLDER: {rel} | {n} ocorrência(s)")

    def attr_repl(match: re.Match[str]) -> str:
        url = match.group("url")
        fixed = fix_site_url(url)
        if fixed != url:
            COUNTERS["absolute_urls_fixed"] += 1
        return match.group("prefix") + fixed + match.group("suffix")

    text = HTML_ATTR_URL_RE.sub(attr_repl, text)
    text = re.sub(r'(<head>)\s{6,}', r'\1\n', text, count=1)
    text = sync_subpage_top(text, rel)

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
        flag = " [ACIMA DE 500 KB]" if kb > 500 else ""
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
        flag = " [ACIMA DE 300 KB]" if kb > 300 else ""
        out.append(f"- {rel}: {kb:.1f} KB{flag}")
    return out


def write_report() -> None:
    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report = report_dir / "site_integrity_performance_audit.md"

    body: list[str] = [
        "# Auditoria Técnica Global — Embaixada Carioca",
        "",
        "## Escopo",
        "- PT / EN / ES",
        "- canonicals, hreflang e sitemap",
        "- links externos críticos",
        "- limpeza leve de HTML",
        "- sincronização do topo das principais subpáginas com a home",
        "- performance percebida e peso de páginas/assets",
        "- sem alteração da composição principal da home",
        "",
        "## Contadores",
    ]

    for key, value in COUNTERS.items():
        body.append(f"- {key}: {value}")

    body.extend(["", "## Correções aplicadas"])
    if REPORT:
        body.extend(f"- {line}" for line in REPORT)
    else:
        body.append("- Nenhuma correção necessária nesta rodada")

    body.extend(["", "## Alertas encontrados"])
    if WARNINGS:
        body.extend(f"- {line}" for line in WARNINGS)
    else:
        body.append("- Nenhum alerta crítico encontrado")

    body.extend(["", "## Maiores páginas HTML"])
    body.extend(audit_sizes())

    body.extend(["", "## Maiores assets de imagem"])
    body.extend(audit_assets())

    body.extend([
        "",
        "## Diagnóstico executivo",
        "- O principal risco técnico estava na inconsistência entre URLs com e sem `.html`, especialmente em sitemap, canonical e hreflang.",
        "- URLs no sitemap que não correspondem a arquivos reais foram removidas para evitar rastreamento desperdiçado e sinais ruins ao Google.",
        "- Links de avaliação e placeholders foram normalizados para reduzir caminhos quebrados em CTAs.",
        "- O topo das páginas principais foi sincronizado visualmente com a home, mantendo a estrutura de navegação, avaliação, idioma e botão de reserva.",
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
