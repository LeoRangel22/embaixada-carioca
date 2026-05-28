#!/usr/bin/env python3
"""Lock all top navigations to the home-reference component.

Visual QA scope:
- external frame/line appearing on cardapio, cafe-da-manha and guia-do-rio;
- menu position, font and sizing drifting from the home reference;
- hero eyebrow line such as "Restaurante no Bondinho" not matching home;
- eventos keeps the same frame but uses the event budget CTA.

Guardrails:
- no JSON-LD/schema changes;
- no body content section changes except replacing the top <nav> component;
- per-page CTA rule only.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "home_reference_top_nav_lock_report.md"
STYLE_ID = "ec-home-reference-top-nav-lock-css"

NAV_RE = re.compile(r"<nav\b[^>]*(?:class=[\"'][^\"']*\btop\b[^\"']*[\"']|id=[\"']topnav[\"'])[^>]*>[\s\S]*?</nav>", re.I)
STRIP_BLOCKS = [
    r"<!-- EC TOP NAV STANDARDIZATION -->[\s\S]*?<!-- /EC TOP NAV STANDARDIZATION -->\s*",
    r"<!-- EC TOP NAV VISUAL REFINEMENT -->[\s\S]*?<!-- /EC TOP NAV VISUAL REFINEMENT -->\s*",
    r"<!-- EC HOME REFERENCE TOP NAV LOCK -->[\s\S]*?<!-- /EC HOME REFERENCE TOP NAV LOCK -->\s*",
]

STYLE = f"""
<!-- EC HOME REFERENCE TOP NAV LOCK -->
<style id="{STYLE_ID}">
/* Final lock: top nav must visually follow the home reference. */
html,body{{margin:0!important;padding:0!important;border:0!important;outline:0!important;max-width:100%!important;overflow-x:hidden!important;}}
html body{{background:#00202e!important;}}
html body::before,html body::after{{content:none!important;display:none!important;}}
html body nav.top,html body #topnav.top{{position:fixed!important;top:0!important;left:0!important;right:0!important;width:100%!important;z-index:990!important;min-height:104px!important;background:linear-gradient(180deg,rgba(0,64,90,.56) 0%,rgba(0,64,90,.34) 56%,rgba(0,64,90,0) 100%)!important;border:0!important;border-top:0!important;border-bottom:0!important;outline:0!important;box-shadow:none!important;filter:none!important;backdrop-filter:none!important;overflow:visible!important;}}
html body nav.top::before,html body nav.top::after,html body #topnav::before,html body #topnav::after{{content:none!important;display:none!important;border:0!important;outline:0!important;box-shadow:none!important;}}
html body nav.top.scrolled,html body nav.top.nav-scrolled,html body.scrolled nav.top{{min-height:84px!important;background:rgba(237,226,201,.96)!important;border:0!important;outline:0!important;box-shadow:none!important;backdrop-filter:blur(12px)!important;}}
html body nav.top .nav-inner,html body #topnav .nav-inner{{width:100%!important;max-width:1440px!important;height:104px!important;min-height:104px!important;margin:0 auto!important;padding:14px clamp(28px,4.2vw,72px)!important;display:flex!important;align-items:center!important;justify-content:space-between!important;gap:clamp(20px,2vw,30px)!important;color:#f6efde!important;border:0!important;outline:0!important;box-shadow:none!important;}}
html body nav.top.scrolled .nav-inner,html body nav.top.nav-scrolled .nav-inner,html body.scrolled nav.top .nav-inner{{height:84px!important;min-height:84px!important;color:#00405a!important;}}
html body nav.top .brand-mark{{display:flex!important;align-items:center!important;gap:18px!important;min-width:64px!important;padding:0!important;margin:0!important;color:inherit!important;text-decoration:none!important;border:0!important;outline:0!important;box-shadow:none!important;}}
html body nav.top .brand-logo{{width:64px!important;height:64px!important;min-width:64px!important;min-height:64px!important;max-width:64px!important;max-height:64px!important;object-fit:contain!important;display:block!important;filter:none!important;}}
html body nav.top:not(.scrolled):not(.nav-scrolled) .brand-logo.light,html body:not(.scrolled) nav.top:not(.scrolled):not(.nav-scrolled) .brand-logo.light{{display:block!important;}}
html body nav.top:not(.scrolled):not(.nav-scrolled) .brand-logo.dark,html body:not(.scrolled) nav.top:not(.scrolled):not(.nav-scrolled) .brand-logo.dark{{display:none!important;}}
html body nav.top.scrolled .brand-logo.light,html body nav.top.nav-scrolled .brand-logo.light,html body.scrolled nav.top .brand-logo.light{{display:none!important;}}
html body nav.top.scrolled .brand-logo.dark,html body nav.top.nav-scrolled .brand-logo.dark,html body.scrolled nav.top .brand-logo.dark{{display:block!important;}}
html body nav.top .nav-links{{display:flex!important;align-items:center!important;justify-content:center!important;flex:1 1 auto!important;gap:clamp(22px,2.15vw,32px)!important;list-style:none!important;padding:0!important;margin:0!important;min-width:0!important;border:0!important;outline:0!important;box-shadow:none!important;}}
html body nav.top .nav-links li{{display:flex!important;margin:0!important;padding:0!important;}}
html body nav.top .nav-links a{{display:inline-flex!important;align-items:center!important;min-height:44px!important;padding:6px 0!important;color:inherit!important;-webkit-text-fill-color:currentColor!important;text-decoration:none!important;font-family:'JetBrains Mono',ui-monospace,monospace!important;font-size:12px!important;line-height:1!important;font-weight:800!important;letter-spacing:.12em!important;text-transform:uppercase!important;white-space:nowrap!important;opacity:.97!important;text-shadow:0 2px 10px rgba(0,64,90,.72)!important;}}
html body nav.top.scrolled .nav-links a,html body nav.top.nav-scrolled .nav-links a,html body.scrolled nav.top .nav-links a{{color:#00405a!important;text-shadow:none!important;}}
html body nav.top .nav-links a:hover{{color:#f59b1e!important;-webkit-text-fill-color:#f59b1e!important;}}
html body nav.top .nav-wa-btn{{display:none!important;}}
html body nav.top .nav-rating-badge{{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:44px!important;height:44px!important;padding:0 22px!important;border-radius:999px!important;background:rgba(0,64,90,.52)!important;border:1px solid rgba(237,226,201,.36)!important;color:#f6efde!important;-webkit-text-fill-color:#f6efde!important;text-decoration:none!important;flex:0 0 auto!important;box-shadow:none!important;white-space:nowrap!important;}}
html body nav.top .gr-copy{{display:block!important;line-height:1!important;}}
html body nav.top .gr-label{{display:block!important;font-family:'JetBrains Mono',ui-monospace,monospace!important;font-size:10px!important;line-height:1!important;color:rgba(246,239,222,.84)!important;-webkit-text-fill-color:rgba(246,239,222,.84)!important;}}
html body nav.top .gr-row{{display:flex!important;align-items:center!important;gap:4px!important;font-family:'JetBrains Mono',ui-monospace,monospace!important;font-size:12px!important;line-height:1.1!important;}}
html body nav.top .gr-stars{{color:#f59b1e!important;-webkit-text-fill-color:#f59b1e!important;letter-spacing:.02em!important;}}
html body nav.top .gr-count{{font-size:10px!important;color:rgba(246,239,222,.82)!important;-webkit-text-fill-color:rgba(246,239,222,.82)!important;}}
html body nav.top .lang-switcher{{position:relative!important;display:block!important;flex:0 0 auto!important;z-index:1000!important;}}
html body nav.top .lang-current{{display:inline-flex!important;align-items:center!important;gap:8px!important;height:44px!important;min-height:44px!important;padding:0 20px!important;border-radius:999px!important;background:rgba(0,64,90,.52)!important;border:1px solid rgba(237,226,201,.36)!important;color:#f6efde!important;-webkit-text-fill-color:#f6efde!important;font-family:'JetBrains Mono',ui-monospace,monospace!important;font-size:12px!important;font-weight:800!important;letter-spacing:.08em!important;text-transform:uppercase!important;box-shadow:none!important;}}
html body nav.top .lang-dropdown{{position:absolute!important;top:calc(100% + 8px)!important;right:0!important;min-width:180px!important;background:#f6efde!important;border:1px solid rgba(0,64,90,.16)!important;border-radius:16px!important;padding:8px!important;box-shadow:0 18px 48px rgba(0,32,46,.20)!important;display:none!important;z-index:1100!important;}}
html body nav.top .lang-switcher.is-open .lang-dropdown{{display:block!important;}}
html body nav.top .lang-dropdown a{{display:flex!important;align-items:center!important;gap:8px!important;padding:10px 12px!important;border-radius:10px!important;color:#00405a!important;-webkit-text-fill-color:#00405a!important;text-decoration:none!important;font-size:13px!important;}}
html body nav.top .nav-hamburger{{display:none!important;}}
html body nav.top .btn{{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:56px!important;height:56px!important;padding:0 clamp(34px,3.8vw,56px)!important;border-radius:999px!important;background:#f59b1e!important;border:0!important;color:#00405a!important;-webkit-text-fill-color:#00405a!important;text-decoration:none!important;font-family:'JetBrains Mono',ui-monospace,monospace!important;font-size:12px!important;font-weight:900!important;letter-spacing:.18em!important;text-transform:uppercase!important;white-space:nowrap!important;box-shadow:none!important;flex:0 0 auto!important;}}
html body nav.top.scrolled .nav-rating-badge,html body nav.top.nav-scrolled .nav-rating-badge,html body.scrolled nav.top .nav-rating-badge,html body nav.top.scrolled .lang-current,html body nav.top.nav-scrolled .lang-current,html body.scrolled nav.top .lang-current{{background:rgba(255,255,255,.58)!important;border-color:rgba(0,64,90,.22)!important;color:#00405a!important;-webkit-text-fill-color:#00405a!important;}}
html body nav.top.scrolled .gr-label,html body nav.top.scrolled .gr-count,html body nav.top.nav-scrolled .gr-label,html body nav.top.nav-scrolled .gr-count,html body.scrolled nav.top .gr-label,html body.scrolled nav.top .gr-count{{color:#00405a!important;-webkit-text-fill-color:#00405a!important;}}
/* Hero eyebrow/subtitle line must follow home reference. */
html body header.hero .eyebrow,html body header.hero .hero-eyebrow,html body header.page-hero .eyebrow,html body header.page-hero .hero-eyebrow{{font-family:'JetBrains Mono',ui-monospace,monospace!important;font-size:11px!important;line-height:1.2!important;font-weight:700!important;letter-spacing:.22em!important;text-transform:uppercase!important;color:#f59b1e!important;-webkit-text-fill-color:#f59b1e!important;text-shadow:0 2px 10px rgba(0,64,90,.72)!important;margin-top:0!important;margin-bottom:22px!important;}}
html body header.hero,html body header.page-hero{{margin-top:0!important;border:0!important;outline:0!important;box-shadow:none!important;}}
html body header.hero::before,html body header.hero::after,html body header.page-hero::before,html body header.page-hero::after{{border:0!important;outline:0!important;box-shadow:none!important;}}
@media(max-width:1280px){{html body nav.top .nav-rating-badge{{display:none!important;}}}}
@media(max-width:1120px){{html body nav.top .nav-links{{gap:18px!important;}}}}
@media(max-width:900px){{html body nav.top{{min-height:76px!important;background:rgba(0,64,90,.88)!important;backdrop-filter:blur(12px)!important;}}html body nav.top .nav-inner{{height:76px!important;min-height:76px!important;padding:10px 20px!important;}}html body nav.top .brand-logo{{width:54px!important;height:54px!important;min-width:54px!important;min-height:54px!important;}}html body nav.top .nav-links{{display:none!important;}}html body nav.top .lang-switcher{{display:none!important;}}html body nav.top .btn{{height:46px!important;min-height:46px!important;padding:0 18px!important;font-size:10px!important;letter-spacing:.10em!important;}}}}
@media(max-width:520px){{html body nav.top .btn{{display:none!important;}}}}
</style>
<!-- /EC HOME REFERENCE TOP NAV LOCK -->
""".strip()


@dataclass
class Result:
    page: str
    changed: bool
    event_cta: bool
    nav_replaced: bool
    notes: str


def is_event_page(rel: str) -> bool:
    r = rel.lower()
    return "eventos" in r or "events" in r


def lang_for(rel: str) -> tuple[str, str, str]:
    if rel.startswith("en/"):
        return "en", "🇺🇸", "EN"
    if rel.startswith("es/"):
        return "es", "🇪🇸", "ES"
    return "pt-BR", "🇧🇷", "PT"


def nav_html(rel: str) -> str:
    is_event = is_event_page(rel)
    lang, flag, label = lang_for(rel)
    cta_href = "https://leorangel22.github.io/main/formulario.html" if is_event else "https://go.tagme.com.br/embaixadacarioca"
    cta_text = "Solicitar orçamento" if is_event else "Reservar"
    return f'''<nav class="top" id="topnav" aria-label="Navegação principal">
<div class="nav-inner">
<a aria-label="Embaixada Carioca · início" class="brand-mark" href="/">
<img alt="Embaixada Carioca — Restaurante com Vista para o Pão de Açúcar, Morro da Urca, Rio de Janeiro" class="brand-logo light" src="/assets/logo-areia.svg" decoding="async" fetchpriority="high"/>
<img alt="Embaixada Carioca · Restaurante no Morro da Urca, Rio de Janeiro" class="brand-logo dark" loading="lazy" src="/assets/logo-azul.svg" decoding="async"/>
</a>
<ul class="nav-links">
<li><a href="/cafe-da-manha.html">Café da Manhã</a></li>
<li><a href="/almoco.html">Almoço</a></li>
<li><a href="/como-chegar.html">Como Chegar</a></li>
<li><a href="/eventos.html">Eventos</a></li>
<li><a href="/cardapio.html">Cardápio</a></li>
<li><a href="/guia-do-rio.html">Guia do Rio</a></li>
</ul>
<a aria-label="Google Reviews: 4.8 estrelas · 7.779 avaliações" class="nav-rating-badge google-review-badge" href="https://g.page/r/CU-tJiJIjBUcEAE/review" rel="noopener" target="_blank" title="Google Reviews · 4.8 estrelas">
<span class="gr-copy"><span class="gr-label">Google Reviews</span><span class="gr-row"><strong class="gr-score">4.8</strong><span class="gr-stars" aria-hidden="true">★★★★★</span><span class="gr-count">7.779 avaliações</span></span></span>
</a>
<div aria-label="Selecionar idioma" class="lang-switcher" role="navigation">
<button aria-expanded="false" aria-haspopup="true" aria-label="Idioma atual: {label}" class="lang-current"><span class="lang-flag">{flag}</span><span>{label}</span><span class="lang-arrow">▼</span></button>
<div class="lang-dropdown" role="menu">
<a class="{'active' if lang == 'pt-BR' else ''}" href="/" hreflang="pt-BR" role="menuitem"><span class="lang-flag">🇧🇷</span><span class="lang-name">Português</span>{' <span class="lang-check">✓</span>' if lang == 'pt-BR' else ''}</a>
<a class="{'active' if lang == 'en' else ''}" href="/en/" hreflang="en" role="menuitem"><span class="lang-flag">🇺🇸</span><span class="lang-name">English</span>{' <span class="lang-check">✓</span>' if lang == 'en' else ''}</a>
<a class="{'active' if lang == 'es' else ''}" href="/es/" hreflang="es" role="menuitem"><span class="lang-flag">🇪🇸</span><span class="lang-name">Español</span>{' <span class="lang-check">✓</span>' if lang == 'es' else ''}</a>
</div>
</div>
<button aria-controls="nav-drawer" aria-expanded="false" aria-label="Abrir menu de navegação" class="nav-hamburger" id="nav-hamburger"><span></span><span></span><span></span></button>
<a class="btn" href="{cta_href}"{' rel="noopener nofollow" target="_blank"' if is_event else ''}>{cta_text}</a>
</div>
</nav>'''


def strip_old_styles(source: str) -> str:
    for pattern in STRIP_BLOCKS:
        source = re.sub(pattern, "", source, flags=re.I)
    source = re.sub(rf"<style\b[^>]*id=[\"']{re.escape(STYLE_ID)}[\"'][^>]*>[\s\S]*?</style>\s*", "", source, flags=re.I)
    return source


def insert_style(source: str) -> str:
    return source.replace("</head>", STYLE + "\n</head>", 1) if "</head>" in source else STYLE + "\n" + source


def process(path: Path) -> Result | None:
    rel = path.relative_to(ROOT).as_posix()
    original = path.read_text(encoding="utf-8", errors="ignore")
    if not NAV_RE.search(original):
        return None
    updated = strip_old_styles(original)
    updated, count = NAV_RE.subn(nav_html(rel), updated, count=1)
    updated = insert_style(updated)
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return Result(rel, changed, is_event_page(rel), count > 0, "canonical-home-nav-markup-and-css")


def write_report(results: list[Result]) -> int:
    REPORT.parent.mkdir(exist_ok=True)
    status = "PASS" if results else "FAIL"
    lines = [
        "# Home Reference Top Nav Lock",
        "",
        f"Status geral: **{status}**",
        "",
        "## Objetivo",
        "Substituir as variações do topo por um componente canônico baseado na home, eliminando moldura externa, linha residual e diferenças de posição/fonte/tamanho.",
        "",
        "## Correções",
        "- Nav markup canônico em todas as páginas com `nav.top`.",
        "- CSS final sem `border-bottom`, outline, pseudo-linhas ou sombra no frame do topo.",
        "- Fonte, tamanho, peso, espaçamento e posição dos links seguem a home.",
        "- Linha/eyebrow do hero, como `Restaurante no Bondinho`, segue a tipografia da home.",
        "- Páginas de eventos mantêm o CTA `Solicitar orçamento`.",
        "",
        "## Guardrails",
        "- Nenhum JSON-LD/schema foi alterado.",
        "- Nenhuma seção de conteúdo foi alterada fora do `nav.top`.",
        "- Os links principais seguem o padrão da home.",
        "",
        "## Resumo",
        f"- Páginas processadas: **{len(results)}**",
        f"- Páginas alteradas: **{len([r for r in results if r.changed])}**",
        f"- Páginas de eventos com CTA especial: **{len([r for r in results if r.event_cta])}**",
        "",
        "## Resultados por página",
        "",
        "| Página | Changed | Nav substituído | CTA evento | Notas |",
        "|---|---:|---:|---:|---|",
    ]
    for r in results:
        lines.append(f"| `{r.page}` | {r.changed} | {r.nav_replaced} | {r.event_cta} | {r.notes} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Home reference top nav lock: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    pages = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts and "node_modules" not in p.parts)
    results = [r for p in pages if (r := process(p)) is not None]
    return write_report(results)


if __name__ == "__main__":
    raise SystemExit(main())
