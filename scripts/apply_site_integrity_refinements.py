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
- padronização rígida do topo das subpáginas com o topo vencedor da home;
- remoção de overflow/moldura lateral em desktop;
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
    "subpage_eyebrow_synced": 0,
}

EXCLUDED_TOP_SYNC = {
    "index.html",
    "home-preview.html",
    "offline.html",
    "404.html",
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

SUBPAGE_HOME_TOP_CSS = r'''
<style id="subpage-home-top-sync">
/* Topo das subpáginas — clone visual da home vencedora */
html,body{
  margin:0!important;
  padding:0!important;
  overflow-x:hidden!important;
}
body[data-screen-label]{
  max-width:100vw!important;
  overflow-x:hidden!important;
  background:#00202e!important;
}
body[data-screen-label] nav.top,
body[data-screen-label] .page-hero,
body[data-screen-label] header.page-hero{
  width:100%!important;
  max-width:100%!important;
  margin-left:0!important;
  margin-right:0!important;
}
body[data-screen-label] nav.top,
body[data-screen-label] nav.top *{
  box-sizing:border-box!important;
}
@media (min-width:901px){
  body[data-screen-label] nav.top:not(.scrolled){
    height:112px!important;
    min-height:112px!important;
    background:linear-gradient(180deg,rgba(0,32,46,.42) 0%,rgba(0,32,46,.30) 54%,rgba(0,32,46,0) 100%)!important;
    border:0!important;
    box-shadow:none!important;
    backdrop-filter:none!important;
    -webkit-backdrop-filter:none!important;
  }
  body[data-screen-label] nav.top .nav-inner{
    width:100%!important;
    max-width:100%!important;
    height:82px!important;
    margin:0!important;
    padding:10px clamp(54px,3.7vw,70px) 0!important;
    display:grid!important;
    grid-template-columns:140px minmax(650px,1fr) 205px 94px 190px!important;
    column-gap:26px!important;
    align-items:center!important;
    justify-content:normal!important;
    color:var(--areia-pale,#f6efde)!important;
  }
  body[data-screen-label] nav.top .brand-mark{
    grid-column:1!important;
    display:flex!important;
    align-items:center!important;
    justify-content:flex-start!important;
    width:140px!important;
    min-width:0!important;
    flex:initial!important;
    gap:0!important;
    color:inherit!important;
    text-decoration:none!important;
  }
  body[data-screen-label] nav.top .brand-logo{
    width:68px!important;
    height:68px!important;
    object-fit:contain!important;
    display:block!important;
  }
  body[data-screen-label] nav.top .brand-logo.light{display:block!important;}
  body[data-screen-label] nav.top .brand-logo.dark{display:none!important;}
  body[data-screen-label] nav.top .brand-word{display:none!important;}
  body[data-screen-label] nav.top .nav-links{
    grid-column:2!important;
    display:flex!important;
    align-items:center!important;
    justify-content:flex-start!important;
    gap:clamp(24px,2vw,36px)!important;
    min-width:0!important;
    width:auto!important;
    margin:0!important;
    padding:0!important;
    list-style:none!important;
    overflow:visible!important;
  }
  body[data-screen-label] nav.top .nav-links a,
  body[data-screen-label] nav.top .nav-links a:link,
  body[data-screen-label] nav.top .nav-links a:visited{
    font-family:"JetBrains Mono",ui-monospace,monospace!important;
    font-size:12px!important;
    line-height:1!important;
    letter-spacing:.145em!important;
    font-weight:800!important;
    text-transform:uppercase!important;
    color:rgba(246,239,222,.94)!important;
    opacity:1!important;
    text-decoration:none!important;
    white-space:nowrap!important;
    padding:6px 0!important;
  }
  body[data-screen-label] nav.top .nav-links a::after{
    bottom:-13px!important;
    height:2px!important;
    background:var(--amarelo,#f59b1e)!important;
  }
  body[data-screen-label] nav.top .nav-wa-btn{display:none!important;}
  body[data-screen-label] nav.top .nav-rating-badge,
  body[data-screen-label] nav.top .nav-rating-badge:link,
  body[data-screen-label] nav.top .nav-rating-badge:visited{
    grid-column:3!important;
    width:205px!important;
    min-width:0!important;
    height:39px!important;
    margin:0!important;
    padding:0 16px!important;
    display:flex!important;
    align-items:center!important;
    justify-content:center!important;
    gap:7px!important;
    border-radius:999px!important;
    background:rgba(246,239,222,.14)!important;
    border:1px solid rgba(246,239,222,.30)!important;
    color:var(--areia-pale,#f6efde)!important;
    text-decoration:none!important;
    box-shadow:0 8px 22px rgba(0,32,46,.12)!important;
    overflow:hidden!important;
  }
  body[data-screen-label] nav.top .nav-rating-stars{
    color:var(--amarelo,#f59b1e)!important;
    font-size:15px!important;
    font-weight:900!important;
    letter-spacing:.01em!important;
    white-space:nowrap!important;
  }
  body[data-screen-label] nav.top .nav-rating-count{
    color:rgba(246,239,222,.78)!important;
    font-size:11px!important;
    font-weight:800!important;
    letter-spacing:.08em!important;
    white-space:nowrap!important;
  }
  body[data-screen-label] nav.top .lang-switcher{
    grid-column:4!important;
    width:94px!important;
    min-width:0!important;
    margin:0!important;
    display:block!important;
    flex:initial!important;
  }
  body[data-screen-label] nav.top .lang-current{
    width:94px!important;
    height:36px!important;
    padding:0 12px!important;
    display:flex!important;
    align-items:center!important;
    justify-content:center!important;
    gap:6px!important;
    border-radius:12px!important;
    background:rgba(246,239,222,.14)!important;
    border:1px solid rgba(246,239,222,.30)!important;
    color:var(--areia-pale,#f6efde)!important;
    font-family:"JetBrains Mono",ui-monospace,monospace!important;
    font-size:12px!important;
    font-weight:900!important;
    letter-spacing:.06em!important;
    white-space:nowrap!important;
  }
  body[data-screen-label] nav.top .lang-current span{color:inherit!important;}
  body[data-screen-label] nav.top .btn,
  body[data-screen-label] nav.top .btn:link,
  body[data-screen-label] nav.top .btn:visited{
    grid-column:5!important;
    width:190px!important;
    min-width:0!important;
    height:60px!important;
    min-height:0!important;
    padding:0!important;
    margin:0!important;
    display:inline-flex!important;
    align-items:center!important;
    justify-content:center!important;
    border-radius:999px!important;
    background:var(--amarelo,#f59b1e)!important;
    border:1px solid var(--amarelo,#f59b1e)!important;
    color:#fff!important;
    font-family:"JetBrains Mono",ui-monospace,monospace!important;
    font-size:14px!important;
    line-height:1!important;
    font-weight:900!important;
    letter-spacing:.16em!important;
    text-transform:uppercase!important;
    text-decoration:none!important;
    box-shadow:none!important;
    overflow:hidden!important;
    box-sizing:border-box!important;
  }
  body[data-screen-label] nav.top .btn:hover{
    background:var(--amarelo,#f59b1e)!important;
    color:#fff!important;
    filter:brightness(1.04)!important;
  }
  body[data-screen-label] nav.top .nav-hamburger{display:none!important;}

  /* Linha institucional exatamente abaixo do menu, como na home */
  body[data-screen-label] .page-hero-content .eyebrow.hero-eyebrow{
    position:absolute!important;
    top:98px!important;
    left:clamp(214px,11.7vw,244px)!important;
    right:clamp(320px,23vw,430px)!important;
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
    text-transform:uppercase!important;
    color:var(--amarelo,#f59b1e)!important;
    opacity:1!important;
    text-shadow:0 2px 12px rgba(0,32,46,.66)!important;
    z-index:8!important;
  }
  body[data-screen-label] .page-hero-content .eyebrow.hero-eyebrow::before{
    width:34px!important;
    min-width:34px!important;
    height:1px!important;
    margin-right:18px!important;
    background:var(--amarelo,#f59b1e)!important;
    opacity:1!important;
  }
  body[data-screen-label] .page-hero-content{padding-top:168px!important;}
}
@media (min-width:901px) and (max-width:1460px){
  body[data-screen-label] nav.top .nav-inner{
    padding-left:34px!important;
    padding-right:34px!important;
    grid-template-columns:108px minmax(520px,1fr) 188px 84px 174px!important;
    column-gap:18px!important;
  }
  body[data-screen-label] nav.top .brand-mark{width:108px!important;}
  body[data-screen-label] nav.top .brand-logo{width:62px!important;height:62px!important;}
  body[data-screen-label] nav.top .nav-links{gap:18px!important;}
  body[data-screen-label] nav.top .nav-links a{font-size:10.5px!important;letter-spacing:.115em!important;}
  body[data-screen-label] nav.top .nav-rating-badge{width:188px!important;height:38px!important;}
  body[data-screen-label] nav.top .nav-rating-stars{font-size:14px!important;}
  body[data-screen-label] nav.top .nav-rating-count{font-size:10px!important;letter-spacing:.06em!important;}
  body[data-screen-label] nav.top .lang-switcher,
  body[data-screen-label] nav.top .lang-current{width:84px!important;}
  body[data-screen-label] nav.top .btn{width:174px!important;height:58px!important;font-size:12.5px!important;letter-spacing:.14em!important;}
  body[data-screen-label] .page-hero-content .eyebrow.hero-eyebrow{left:214px!important;right:280px!important;font-size:9.5px!important;letter-spacing:.30em!important;}
}
@media (min-width:901px) and (max-width:1180px){
  body[data-screen-label] nav.top .nav-inner{
    grid-template-columns:88px minmax(380px,1fr) 154px 74px 142px!important;
    column-gap:12px!important;
    padding-left:24px!important;
    padding-right:24px!important;
  }
  body[data-screen-label] nav.top .brand-mark{width:88px!important;}
  body[data-screen-label] nav.top .brand-logo{width:56px!important;height:56px!important;}
  body[data-screen-label] nav.top .nav-links{gap:12px!important;}
  body[data-screen-label] nav.top .nav-links a{font-size:9.2px!important;letter-spacing:.08em!important;}
  body[data-screen-label] nav.top .nav-rating-badge{width:154px!important;padding:0 8px!important;}
  body[data-screen-label] nav.top .nav-rating-count{font-size:9px!important;}
  body[data-screen-label] nav.top .lang-switcher,
  body[data-screen-label] nav.top .lang-current{width:74px!important;}
  body[data-screen-label] nav.top .btn{width:142px!important;height:54px!important;font-size:11px!important;letter-spacing:.10em!important;}
}
@media (max-width:900px){
  body[data-screen-label]{overflow-x:hidden!important;}
  body[data-screen-label] nav.top{max-width:100vw!important;}
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
EYEBROW_RE = re.compile(r'(<div\s+class=["\']eyebrow hero-eyebrow["\'][^>]*>)([\s\S]*?)(</div>)', re.IGNORECASE)


def should_sync_top(rel: str, text: str) -> bool:
    if rel in EXCLUDED_TOP_SYNC:
        return False
    if rel.startswith("_"):
        return False
    if not rel.endswith(".html"):
        return False
    return "nav" in text and "class=\"top\"" in text


def eyebrow_text_for(rel: str) -> str:
    if rel.startswith("en/"):
        return "Restaurant at the Cable Car · Morro da Urca · Sugarloaf Cable Car Park · Rio de Janeiro · Brazil"
    if rel.startswith("es/"):
        return "Restaurante del Bondinho · Morro da Urca · Parque Bondinho Pan de Azúcar · Río de Janeiro · Brasil"
    return "Restaurante do Bondinho · Morro da Urca · Parque Bondinho Pão de Açúcar · Rio de Janeiro · Brasil"


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
    if not should_sync_top(rel, text):
        return text

    cleaned = TOP_SYNC_RE.sub("\n", text)

    def eyebrow_repl(match: re.Match[str]) -> str:
        COUNTERS["subpage_eyebrow_synced"] += 1
        return match.group(1) + eyebrow_text_for(rel) + match.group(3)

    cleaned = EYEBROW_RE.sub(eyebrow_repl, cleaned, count=1)

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
        "- sincronização do topo das subpáginas com a home",
        "- remoção de overflow/moldura lateral em desktop",
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
        "- O topo das subpáginas foi forçado a seguir o grid visual da home: logo, menu, avaliações, idioma e botão de reserva.",
        "- O botão de reserva passou a usar largura fechada e box-sizing border-box para não estourar a lateral direita.",
        "- O body e o hero receberam bloqueio de overflow horizontal para eliminar moldura cinza e scroll lateral indesejado.",
        "- O principal risco técnico segue sendo HTML grande, CSS inline acumulado e imagens acima de 300 KB.",
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
