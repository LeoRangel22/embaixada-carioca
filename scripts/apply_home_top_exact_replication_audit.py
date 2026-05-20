#!/usr/bin/env python3
"""
Home Top Exact Replication + Audit — Embaixada Carioca

Objetivo:
- usar a home como padrão visual do topo;
- replicar a mesma estrutura de topo em todas as páginas HTML;
- remover overrides antigos de subpágina que podiam deixar menu/logo/review/idioma/reserva em posições diferentes;
- travar por CSS a posição dos elementos críticos;
- gerar auditoria estática de código + fingerprint visual do topo.

Elementos auditados:
logo, menu, linha laranja/hero-eyebrow, Google Reviews, seletor de idioma e botão Reservar.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import csv

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "home_top_exact_replication_visual_audit_report.md"
REPORT_CSV = REPORT_DIR / "home_top_exact_replication_visual_audit_details.csv"

NAV_RE = re.compile(r"<nav\b(?=[^>]*class=[\"'][^\"']*\btop\b[^\"']*[\"'])[^>]*>[\s\S]*?</nav>", re.IGNORECASE)
HEAD_CLOSE_RE = re.compile(r"</head>", re.IGNORECASE)
HTML_LANG_RE = re.compile(r"<html\b[^>]*lang=[\"']([^\"']+)[\"']", re.IGNORECASE)
BODY_RE = re.compile(r"<body\b([^>]*)>", re.IGNORECASE)
CSS_RE = re.compile(r"\n*<!-- EC Home Top Exact Replication Lock -->[\s\S]*?<!-- /EC Home Top Exact Replication Lock -->\s*", re.IGNORECASE)
OLD_STYLE_RE = re.compile(
    r"\n*<style\s+id=[\"'](?:subpage-home-top-sync|subpage-home-top-final-override)[\"']>[\s\S]*?</style>\s*",
    re.IGNORECASE,
)
EYEBROW_RE = re.compile(r'(<div\s+class=["\']eyebrow hero-eyebrow["\'][^>]*>)([\s\S]*?)(</div>)', re.IGNORECASE)

SKIP = {"404.html", "offline.html", "home-preview.html"}

COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "nav_replaced": 0,
    "old_overrides_removed": 0,
    "css_lock_injected": 0,
    "eyebrow_synced": 0,
    "audit_pass": 0,
    "audit_warn": 0,
}
DETAILS: list[dict[str, object]] = []
ACTIONS: list[str] = []

CSS_LOCK = """<!-- EC Home Top Exact Replication Lock -->
<style id="ec-home-top-exact-replication-lock">
/* Home top exact replication lock — mesma base visual em home e subpáginas */
html,body{overflow-x:hidden!important;}
nav.top,nav.top *{box-sizing:border-box!important;}
@media (min-width:961px){
  nav.top:not(.scrolled){
    position:fixed!important;
    top:0!important;left:0!important;right:0!important;
    z-index:50!important;
    background:linear-gradient(180deg,rgba(0,32,46,.40) 0%,rgba(0,32,46,.24) 58%,rgba(0,32,46,0) 100%)!important;
    border:0!important;box-shadow:none!important;
    backdrop-filter:none!important;-webkit-backdrop-filter:none!important;
  }
  nav.top .nav-inner{
    width:100%!important;max-width:100%!important;margin:0!important;
    padding:14px var(--gutter,64px)!important;
    display:flex!important;align-items:center!important;justify-content:space-between!important;
    gap:32px!important;color:var(--areia-pale,#f6efde)!important;
  }
  nav.top .brand-mark{display:flex!important;align-items:center!important;justify-content:flex-start!important;gap:18px!important;flex:0 0 auto!important;text-decoration:none!important;color:inherit!important;}
  nav.top .brand-logo{width:68px!important;height:68px!important;object-fit:contain!important;display:block!important;}
  nav.top .brand-logo.light{display:block!important;}nav.top .brand-logo.dark{display:none!important;}nav.top .brand-word{display:none!important;}
  nav.top .nav-links{display:flex!important;align-items:center!important;justify-content:flex-start!important;gap:28px!important;margin:0!important;padding:0!important;list-style:none!important;min-width:0!important;overflow:visible!important;}
  nav.top .nav-links a,nav.top .nav-links a:link,nav.top .nav-links a:visited{
    font-family:"JetBrains Mono",ui-monospace,monospace!important;font-size:12px!important;line-height:1!important;letter-spacing:.145em!important;font-weight:800!important;text-transform:uppercase!important;color:rgba(246,239,222,.94)!important;opacity:1!important;text-decoration:none!important;white-space:nowrap!important;padding:6px 0!important;
  }
  nav.top .nav-links a::after{bottom:-13px!important;height:2px!important;background:var(--amarelo,#f59b1e)!important;}
  nav.top .nav-wa-btn{display:none!important;}
  nav.top .nav-rating-badge.google-review-badge,nav.top .nav-rating-badge.google-review-badge:link,nav.top .nav-rating-badge.google-review-badge:visited{
    flex:0 0 170px!important;width:170px!important;min-width:170px!important;height:36px!important;min-height:36px!important;max-height:36px!important;
    margin-left:auto!important;margin-right:0!important;padding:4px 10px!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;gap:0!important;
    border-radius:12px!important;background:rgba(246,239,222,.13)!important;border:1px solid rgba(246,239,222,.30)!important;color:rgba(246,239,222,.94)!important;text-decoration:none!important;
    backdrop-filter:blur(9px)!important;-webkit-backdrop-filter:blur(9px)!important;transform:translateX(28px)!important;box-shadow:0 8px 22px rgba(0,32,46,.12)!important;
  }
  nav.top .lang-switcher{position:relative!important;z-index:4000!important;flex:0 0 94px!important;width:94px!important;min-width:94px!important;margin:0!important;transform:translateX(16px)!important;}
  nav.top .lang-current{width:94px!important;height:36px!important;min-height:36px!important;padding:0 12px!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:6px!important;border-radius:12px!important;background:rgba(246,239,222,.14)!important;border:1px solid rgba(246,239,222,.30)!important;color:var(--areia-pale,#f6efde)!important;font-family:"JetBrains Mono",ui-monospace,monospace!important;font-size:12px!important;font-weight:900!important;letter-spacing:.06em!important;white-space:nowrap!important;}
  nav.top .lang-dropdown{position:absolute!important;top:calc(100% + 8px)!important;bottom:auto!important;right:0!important;left:auto!important;transform:none!important;z-index:99999!important;}
  nav.top .nav-hamburger{display:none!important;}
  nav.top .btn,nav.top .btn:link,nav.top .btn:visited,nav.top a.btn[href*="tagme"]{
    flex:0 0 188px!important;width:188px!important;min-width:188px!important;height:60px!important;min-height:60px!important;margin:0!important;padding:0!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;gap:0!important;border-radius:999px!important;background:var(--amarelo,#f59b1e)!important;border:1px solid var(--amarelo,#f59b1e)!important;color:#fff!important;font-family:"JetBrains Mono",ui-monospace,monospace!important;font-size:14px!important;line-height:1!important;font-weight:900!important;letter-spacing:.16em!important;text-transform:uppercase!important;text-decoration:none!important;overflow:hidden!important;position:relative!important;animation:ecTopReservePulse 2.8s ease-in-out infinite!important;
  }
  .hero .hero-eyebrow,.page-hero .hero-eyebrow{position:relative!important;transform:translate(37px,-6px)!important;will-change:transform!important;}
}
@media (min-width:961px) and (max-width:1180px){
  nav.top .nav-inner{padding-left:18px!important;padding-right:18px!important;gap:10px!important;}
  nav.top .brand-logo{width:54px!important;height:54px!important;}
  nav.top .nav-links{gap:12px!important;overflow:hidden!important;}
  nav.top .nav-links a{font-size:8px!important;letter-spacing:.04em!important;}
  nav.top .nav-rating-badge.google-review-badge{flex-basis:72px!important;width:72px!important;min-width:72px!important;transform:none!important;}
  nav.top .lang-switcher,nav.top .lang-current{width:62px!important;min-width:62px!important;flex-basis:62px!important;transform:none!important;}
  nav.top .btn,nav.top a.btn[href*="tagme"]{flex-basis:124px!important;width:124px!important;min-width:124px!important;height:46px!important;min-height:46px!important;font-size:9.3px!important;letter-spacing:.07em!important;}
}
@media (max-width:960px){nav.top .nav-rating-badge.google-review-badge{display:none!important;}}
</style>
<!-- /EC Home Top Exact Replication Lock -->"""

LABELS = {
    "pt-BR": {
        "aria_home": "Embaixada Carioca · início",
        "logo_alt_light": "Embaixada Carioca — Restaurante com Vista para o Pão de Açúcar, Morro da Urca, Rio de Janeiro",
        "logo_alt_dark": "Embaixada Carioca · Restaurante no Morro da Urca, Rio de Janeiro",
        "menu": [("/cafe-da-manha.html", "Café da Manhã"), ("/almoco.html", "Almoço"), ("/como-chegar.html", "COMO CHEGAR"), ("/eventos.html", "Eventos"), ("/cardapio.html", "Cardápio"), ("/guia-do-rio.html", "Guia do Rio")],
        "wa_text": "Ol%C3%A1%21%20Vim%20pelo%20site%20da%20Embaixada%20Carioca%20e%20gostaria%20de%20fazer%20uma%20reserva.",
        "current": "PT", "flag": "🇧🇷", "active": "pt", "reserve": "Reservar",
        "eyebrow": "Restaurante do Bondinho · Morro da Urca · Parque Bondinho Pão de Açúcar · Rio de Janeiro · Brasil",
    },
    "en": {
        "aria_home": "Embaixada Carioca · home",
        "logo_alt_light": "Embaixada Carioca — Restaurant with a view of Sugarloaf Mountain, Urca Hill, Rio de Janeiro",
        "logo_alt_dark": "Embaixada Carioca · Restaurant at Urca Hill, Rio de Janeiro",
        "menu": [("/en/cafe-da-manha.html", "Breakfast"), ("/en/almoco.html", "Lunch"), ("/en/how-to-get-there.html", "HOW TO GET THERE"), ("/en/eventos.html", "Events"), ("/en/cardapio.html", "Menu"), ("/en/guia-do-rio.html", "Rio Guide")],
        "wa_text": "Hi%21%20I%20found%20Embaixada%20Carioca%20through%20the%20website%20and%20would%20like%20to%20make%20a%20reservation.",
        "current": "EN", "flag": "🇺🇸", "active": "en", "reserve": "Reservar",
        "eyebrow": "Restaurant at the Cable Car · Morro da Urca · Sugarloaf Cable Car Park · Rio de Janeiro · Brazil",
    },
    "es": {
        "aria_home": "Embaixada Carioca · inicio",
        "logo_alt_light": "Embaixada Carioca — Restaurante con vista al Pan de Azúcar, Morro da Urca, Río de Janeiro",
        "logo_alt_dark": "Embaixada Carioca · Restaurante en el Morro da Urca, Río de Janeiro",
        "menu": [("/es/cafe-da-manha.html", "Desayuno"), ("/es/almoco.html", "Almuerzo"), ("/es/como-llegar.html", "CÓMO LLEGAR"), ("/es/eventos.html", "Eventos"), ("/es/cardapio.html", "Menú"), ("/es/guia-do-rio.html", "Guía de Río")],
        "wa_text": "Hola%21%20Vi%20Embaixada%20Carioca%20en%20el%20sitio%20web%20y%20me%20gustar%C3%ADa%20hacer%20una%20reserva.",
        "current": "ES", "flag": "🇪🇸", "active": "es", "reserve": "Reservar",
        "eyebrow": "Restaurante del Bondinho · Morro da Urca · Parque Bondinho Pan de Azúcar · Río de Janeiro · Brasil",
    },
}

WA_SVG = '<svg viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M17.779 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.779-.767.779-.94 1.164-.173.199-.347.779-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.779-.52.149-.174.198-.298.298-.497.779-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.779.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.779h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"></path></svg>'


def lang_for(rel: str, text: str) -> str:
    m = HTML_LANG_RE.search(text)
    if m:
        value = m.group(1).lower()
        if value.startswith("en"):
            return "en"
        if value.startswith("es"):
            return "es"
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt-BR"


def nav_html(lang: str) -> str:
    cfg = LABELS[lang]
    links = "\n".join(f'<li><a href="{href}">{label}</a></li>' for href, label in cfg["menu"])
    active = cfg["active"]
    def lang_link(key: str, href: str, flag: str, name: str, hreflang: str) -> str:
        cls = "active" if active == key else ""
        check = ' <span class="lang-check">✓</span>' if active == key else ""
        return f'''<a class="{cls}" href="{href}" hreflang="{hreflang}" role="menuitem">
<span class="lang-flag">{flag}</span>
<span class="lang-name">{name}</span>{check}
</a>'''
    dropdown = "\n".join([
        lang_link("pt", "/", "🇧🇷", "Português", "pt-BR"),
        lang_link("en", "/en/", "🇺🇸", "English", "en"),
        lang_link("es", "/es/", "🇪🇸", "Español", "es"),
    ])
    return f'''<!-- NAV -->
<nav class="top" id="topnav">
<div class="nav-inner">
<a aria-label="{cfg['aria_home']}" class="brand-mark" href="/">
<img alt="{cfg['logo_alt_light']}" class="brand-logo light" loading="lazy" src="/assets/logo-areia.svg" decoding="async"/>
<img alt="{cfg['logo_alt_dark']}" class="brand-logo dark" loading="lazy" src="/assets/logo-azul.svg" decoding="async"/>
</a>
<ul class="nav-links">
{links}
</ul>
<a aria-label="WhatsApp Embaixada Carioca" class="nav-wa-btn" href="https://wa.me/5521966837556?text={cfg['wa_text']}" rel="noopener" target="_blank" title="WhatsApp · +55 21 96683-7556">
{WA_SVG}
</a>
<a aria-label="Google Reviews: 4.8 estrelas · 7.779 avaliações" class="nav-rating-badge google-review-badge" href="https://g.page/r/CU-tJiJIjBUcEAE/review" rel="noopener" target="_blank" title="Google Reviews · 4.8 estrelas">
<span class="gr-copy"><span class="gr-label">Google Reviews</span><span class="gr-row"><strong class="gr-score">4.8</strong><span class="gr-stars" aria-hidden="true">★★★★★</span><span class="gr-count">7.779 avaliações</span></span></span>
</a>
<div aria-label="Selecionar idioma" class="lang-switcher" role="navigation">
<button aria-expanded="false" aria-haspopup="true" aria-label="Idioma atual: {cfg['current']}" class="lang-current">
<span class="lang-flag">{cfg['flag']}</span>
<span>{cfg['current']}</span>
<span class="lang-arrow">▼</span>
</button>
<div class="lang-dropdown" role="menu">
{dropdown}
</div>
</div>
<button aria-controls="nav-drawer" aria-expanded="false" aria-label="Abrir menu de navegação" class="nav-hamburger" id="nav-hamburger">
<span></span>
<span></span>
<span></span>
</button>
<a class="btn" href="https://go.tagme.com.br/embaixadacarioca">{cfg['reserve']}</a>
</div>
</nav>'''


def normalize_nav_for_fingerprint(nav: str) -> str:
    nav = re.sub(r">[^<>]+<", "><", nav)
    nav = re.sub(r"href=\"[^\"]*\"", "href=\"#\"", nav)
    nav = re.sub(r"alt=\"[^\"]*\"", "alt=\"\"", nav)
    nav = re.sub(r"aria-label=\"[^\"]*\"", "aria-label=\"\"", nav)
    nav = re.sub(r"\s+", " ", nav)
    return nav.strip()


def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def process(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix != ".html" or rel.startswith("_") or ".git" in path.parts or rel in SKIP:
        return
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    lang = lang_for(rel, original)
    text = original

    text, removed = OLD_STYLE_RE.subn("\n", text)
    if removed:
        COUNTERS["old_overrides_removed"] += removed
        ACTIONS.append(f"OLD_OVERRIDE_REMOVED: {rel} ({removed})")

    new_nav = nav_html(lang)
    if NAV_RE.search(text):
        text = NAV_RE.sub(new_nav, text, count=1)
        COUNTERS["nav_replaced"] += 1
        ACTIONS.append(f"NAV_REPLACED: {rel}")
    else:
        ACTIONS.append(f"WARN_NO_NAV: {rel}")

    text = CSS_RE.sub("\n", text)
    if HEAD_CLOSE_RE.search(text):
        text = HEAD_CLOSE_RE.sub(CSS_LOCK + "\n</head>", text, count=1)
        COUNTERS["css_lock_injected"] += 1
    else:
        ACTIONS.append(f"WARN_NO_HEAD_CLOSE: {rel}")

    def eyebrow_repl(match: re.Match[str]) -> str:
        COUNTERS["eyebrow_synced"] += 1
        return match.group(1) + LABELS[lang]["eyebrow"] + match.group(3)
    text = EYEBROW_RE.sub(eyebrow_repl, text, count=1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1


def audit_page(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix != ".html" or rel.startswith("_") or ".git" in path.parts or rel in SKIP:
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    lang = lang_for(rel, text)
    nav_match = NAV_RE.search(text)
    nav = nav_match.group(0) if nav_match else ""
    expected = nav_html(lang)
    nav_fp = fingerprint(normalize_nav_for_fingerprint(nav)) if nav else "missing"
    expected_fp = fingerprint(normalize_nav_for_fingerprint(expected))
    checks = {
        "nav_exists": bool(nav),
        "nav_structure_matches": nav_fp == expected_fp,
        "css_lock_present": "ec-home-top-exact-replication-lock" in text,
        "old_override_absent": "subpage-home-top-sync" not in text and "subpage-home-top-final-override" not in text,
        "logo_present": "brand-logo light" in nav and "brand-logo dark" in nav,
        "menu_present": "nav-links" in nav and LABELS[lang]["menu"][2][1] in nav,
        "review_present": "google-review-badge" in nav and "Google Reviews" in nav,
        "language_present": "lang-switcher" in nav and f">{LABELS[lang]['current']}<" in nav,
        "reserve_present": "go.tagme.com.br/embaixadacarioca" in nav and ">Reservar<" in nav,
        "eyebrow_position_lock": "transform:translate(37px,-6px)" in text.replace(" ", ""),
    }
    status = "PASS" if all(checks.values()) else "WARN"
    if status == "PASS":
        COUNTERS["audit_pass"] += 1
    else:
        COUNTERS["audit_warn"] += 1
    DETAILS.append({
        "page": rel,
        "lang": lang,
        "status": status,
        "nav_fingerprint": nav_fp,
        "expected_fingerprint": expected_fp,
        **checks,
    })


def write_reports() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    pages = len(DETAILS)
    pass_count = sum(1 for d in DETAILS if d["status"] == "PASS")
    warn_count = pages - pass_count
    lines = [
        "# Home Top Exact Replication + Visual Audit",
        "",
        "## Objetivo",
        "Replicar o topo da home em todas as páginas e auditar por código/fingerprint visual estático os elementos: logo, menu, linha laranja, Google Reviews, idioma e botão Reservar.",
        "",
        "## Veredito",
        f"- Páginas auditadas: {pages}",
        f"- PASS: {pass_count}",
        f"- WARN: {warn_count}",
        f"- Status geral: {'PASS' if warn_count == 0 else 'WARN'}",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend([
        "",
        "## Critérios auditados",
        "- NAV estrutural igual ao padrão da home, com variação apenas de idioma/links.",
        "- Logo light/dark presente e com a mesma classe.",
        "- Menu principal com a mesma ordem visual.",
        "- Badge Google Reviews presente na mesma posição lógica.",
        "- Seletor de idioma presente após reviews e antes do Reservar.",
        "- Botão Reservar presente no final do topo.",
        "- Linha laranja travada em transform: translate(37px, -6px).",
        "- Overrides antigos de subpágina removidos.",
        "",
        "## Páginas com WARN",
    ])
    warnings = [d for d in DETAILS if d["status"] != "PASS"]
    if warnings:
        for d in warnings:
            failed = [k for k, v in d.items() if isinstance(v, bool) and not v]
            lines.append(f"- {d['page']} [{d['lang']}]: {', '.join(failed)}")
    else:
        lines.append("- Nenhuma.")
    lines.extend(["", "## Ações aplicadas"])
    lines.extend(f"- {a}" for a in ACTIONS) if ACTIONS else lines.append("- Nenhuma alteração necessária.")
    lines.extend([
        "",
        "## Observação sobre auditoria visual",
        "Esta auditoria garante igualdade estrutural e de CSS/fingerprint no repositório. A conferência final de pixels deve ser feita no navegador após o deploy, com cache limpo, porque PageSpeed/Chrome podem usar cache e largura de viewport diferentes.",
        "",
    ])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    with REPORT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(DETAILS[0].keys()) if DETAILS else ["page"])
        writer.writeheader()
        writer.writerows(DETAILS)
    print(REPORT_MD.read_text(encoding="utf-8"))


def main() -> int:
    for path in sorted(ROOT.rglob("*.html")):
        process(path)
    for path in sorted(ROOT.rglob("*.html")):
        audit_page(path)
    write_reports()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
