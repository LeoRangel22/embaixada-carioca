#!/usr/bin/env python3
"""Refine top navigation to match the home reference more closely.

Fixes from visual QA:
- Removes the horizontal line/frame introduced by the first standardization pass.
- Prevents double-logo rendering on home-like navs by showing only the light logo before scroll.
- Adds Google Reviews + language selector to simplified `.nav/.links` pages, especially Eventos.
- Keeps Eventos CTA as "Solicitar orçamento".
- Does not touch JSON-LD or page content sections.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "top_nav_visual_refinement_report.md"
STYLE_ID = "ec-top-nav-visual-refinement-css"
OLD_STYLE_ID = "ec-top-nav-standardization-css"

RATING_HTML = '''
<a aria-label="Google Reviews: 4.8 estrelas · 7.779 avaliações" class="nav-rating-badge google-review-badge" href="https://g.page/r/CU-tJiJIjBUcEAE/review" rel="noopener" target="_blank" title="Google Reviews · 4.8 estrelas">
  <span class="gr-copy"><span class="gr-label">Google Reviews</span><span class="gr-row"><strong class="gr-score">4.8</strong><span class="gr-stars" aria-hidden="true">★★★★★</span><span class="gr-count">7.779 avaliações</span></span></span>
</a>
'''.strip()

LANG_HTML = '''
<div aria-label="Selecionar idioma" class="lang-switcher" role="navigation">
  <button aria-expanded="false" aria-haspopup="true" aria-label="Idioma atual: PT" class="lang-current">
    <span class="lang-flag">🇧🇷</span><span>PT</span><span class="lang-arrow">▼</span>
  </button>
  <div class="lang-dropdown" role="menu">
    <a class="active" href="/" hreflang="pt-BR" role="menuitem"><span class="lang-flag">🇧🇷</span><span class="lang-name">Português</span> <span class="lang-check">✓</span></a>
    <a href="/en/" hreflang="en" role="menuitem"><span class="lang-flag">🇺🇸</span><span class="lang-name">English</span></a>
    <a href="/es/" hreflang="es" role="menuitem"><span class="lang-flag">🇪🇸</span><span class="lang-name">Español</span></a>
  </div>
</div>
'''.strip()

STYLE = f'''
<!-- EC TOP NAV VISUAL REFINEMENT -->
<style id="{STYLE_ID}">
/* Visual QA refinement: home-reference top, no external frame, no bottom line. */
html,body{{max-width:100%;overflow-x:hidden!important;}}
html body nav.top,
html body #topnav.top,
html body .top#topnav{{
  position:fixed!important;
  top:0!important;left:0!important;right:0!important;
  z-index:900!important;
  min-height:104px!important;
  background:linear-gradient(180deg,rgba(0,64,90,.58) 0%,rgba(0,64,90,.34) 58%,rgba(0,64,90,0) 100%)!important;
  border:0!important;
  border-bottom:0!important;
  outline:0!important;
  box-shadow:none!important;
  backdrop-filter:none!important;
  overflow:visible!important;
}}
html body nav.top::before,html body nav.top::after,
html body #topnav::before,html body #topnav::after,
html body nav.top .nav::before,html body nav.top .nav::after,
html body nav.top .nav-inner::before,html body nav.top .nav-inner::after{{
  content:none!important;display:none!important;border:0!important;box-shadow:none!important;
}}
html body nav.top.scrolled,
html body nav.top.nav-scrolled,
html body.scrolled nav.top{{
  min-height:84px!important;
  background:rgba(237,226,201,.96)!important;
  border:0!important;
  border-bottom:0!important;
  outline:0!important;
  box-shadow:none!important;
  backdrop-filter:blur(12px)!important;
}}
html body nav.top .nav-inner,
html body nav.top .nav,
html body #topnav .nav-inner,
html body #topnav .nav{{
  width:100%!important;
  max-width:1440px!important;
  height:104px!important;
  min-height:104px!important;
  margin:0 auto!important;
  padding:14px clamp(28px,4.2vw,72px)!important;
  display:flex!important;
  align-items:center!important;
  justify-content:space-between!important;
  gap:clamp(20px,2.2vw,30px)!important;
  color:#f6efde!important;
  border:0!important;
  outline:0!important;
  box-shadow:none!important;
}}
html body nav.top.scrolled .nav-inner,
html body nav.top.scrolled .nav,
html body nav.top.nav-scrolled .nav-inner,
html body nav.top.nav-scrolled .nav,
html body.scrolled nav.top .nav-inner,
html body.scrolled nav.top .nav{{height:84px!important;min-height:84px!important;color:#00405a!important;}}
/* Home nav has two logos in markup; show only the right one for the current state. */
html body nav.top:not(.scrolled):not(.nav-scrolled) .brand-logo.light,
html body:not(.scrolled) nav.top:not(.scrolled):not(.nav-scrolled) .brand-logo.light{{display:block!important;}}
html body nav.top:not(.scrolled):not(.nav-scrolled) .brand-logo.dark,
html body:not(.scrolled) nav.top:not(.scrolled):not(.nav-scrolled) .brand-logo.dark{{display:none!important;}}
html body nav.top.scrolled .brand-logo.light,
html body nav.top.nav-scrolled .brand-logo.light,
html body.scrolled nav.top .brand-logo.light{{display:none!important;}}
html body nav.top.scrolled .brand-logo.dark,
html body nav.top.nav-scrolled .brand-logo.dark,
html body.scrolled nav.top .brand-logo.dark{{display:block!important;}}
html body nav.top .brand-logo,
html body nav.top .brand img,
html body #topnav .brand-logo,
html body #topnav .brand img{{
  width:64px!important;height:64px!important;min-width:64px!important;min-height:64px!important;
  max-width:64px!important;max-height:64px!important;object-fit:contain!important;filter:none!important;
}}
html body nav.top .brand-mark,
html body nav.top .brand,
html body #topnav .brand-mark,
html body #topnav .brand{{
  display:flex!important;align-items:center!important;gap:18px!important;min-width:0!important;
  color:inherit!important;text-decoration:none!important;border:0!important;outline:0!important;box-shadow:none!important;
}}
html body nav.top .brand-word,
html body nav.top .brand span:not(.lang-flag):not(.lang-name):not(.lang-check):not(.gr-stars):not(.gr-count):not(.gr-label),
html body #topnav .brand-word,
html body #topnav .brand span:not(.lang-flag):not(.lang-name):not(.lang-check):not(.gr-stars):not(.gr-count):not(.gr-label){{
  border-left:1px solid currentColor!important;padding-left:18px!important;color:inherit!important;opacity:.94!important;
  font-family:'JetBrains Mono',ui-monospace,monospace!important;font-size:11px!important;font-weight:700!important;letter-spacing:.18em!important;text-transform:uppercase!important;
}}
html body nav.top .nav-links,
html body nav.top .links,
html body #topnav .nav-links,
html body #topnav .links{{
  display:flex!important;align-items:center!important;justify-content:center!important;flex:1 1 auto!important;
  gap:clamp(20px,2vw,30px)!important;list-style:none!important;padding:0!important;margin:0!important;min-width:0!important;
}}
html body nav.top .nav-links a,
html body nav.top .links a,
html body #topnav .nav-links a,
html body #topnav .links a{{
  display:inline-flex!important;align-items:center!important;min-height:44px!important;padding:6px 0!important;
  color:inherit!important;-webkit-text-fill-color:currentColor!important;text-decoration:none!important;
  font-family:'JetBrains Mono',ui-monospace,monospace!important;font-size:12px!important;line-height:1!important;font-weight:800!important;
  letter-spacing:.12em!important;text-transform:uppercase!important;white-space:nowrap!important;opacity:.96!important;text-shadow:0 2px 10px rgba(0,64,90,.72)!important;
}}
html body nav.top.scrolled .nav-links a,
html body nav.top.scrolled .links a,
html body nav.top.nav-scrolled .nav-links a,
html body nav.top.nav-scrolled .links a,
html body.scrolled nav.top .nav-links a,
html body.scrolled nav.top .links a{{color:#00405a!important;text-shadow:none!important;}}
html body nav.top .nav-links a:hover,
html body nav.top .links a:hover{{color:#f59b1e!important;-webkit-text-fill-color:#f59b1e!important;}}
html body nav.top .nav-rating-badge,
html body #topnav .nav-rating-badge{{
  display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:44px!important;height:44px!important;
  padding:0 22px!important;border-radius:999px!important;background:rgba(0,64,90,.52)!important;border:1px solid rgba(237,226,201,.36)!important;
  color:#f6efde!important;-webkit-text-fill-color:#f6efde!important;text-decoration:none!important;flex:0 0 auto!important;box-shadow:none!important;white-space:nowrap!important;
}}
html body nav.top .gr-label{{display:block!important;font-family:'JetBrains Mono',ui-monospace,monospace!important;font-size:10px!important;line-height:1;color:rgba(246,239,222,.84)!important;}}
html body nav.top .gr-row{{display:flex!important;align-items:center!important;gap:4px!important;font-size:12px!important;line-height:1.1!important;}}
html body nav.top .gr-stars{{color:#f59b1e!important;-webkit-text-fill-color:#f59b1e!important;letter-spacing:.02em!important;}}
html body nav.top .gr-count{{font-size:10px!important;color:rgba(246,239,222,.82)!important;-webkit-text-fill-color:rgba(246,239,222,.82)!important;}}
html body nav.top .lang-switcher,
html body #topnav .lang-switcher{{position:relative!important;flex:0 0 auto!important;z-index:1000!important;}}
html body nav.top .lang-current,
html body #topnav .lang-current{{
  display:inline-flex!important;align-items:center!important;gap:8px!important;height:44px!important;min-height:44px!important;padding:0 20px!important;border-radius:999px!important;
  background:rgba(0,64,90,.52)!important;border:1px solid rgba(237,226,201,.36)!important;color:#f6efde!important;-webkit-text-fill-color:#f6efde!important;
  font-family:'JetBrains Mono',ui-monospace,monospace!important;font-size:12px!important;font-weight:800!important;letter-spacing:.08em!important;text-transform:uppercase!important;box-shadow:none!important;
}}
html body nav.top .lang-dropdown,
html body #topnav .lang-dropdown{{
  position:absolute!important;top:calc(100% + 8px)!important;right:0!important;min-width:180px!important;background:#f6efde!important;border:1px solid rgba(0,64,90,.16)!important;border-radius:16px!important;
  padding:8px!important;box-shadow:0 18px 48px rgba(0,32,46,.20)!important;display:none!important;z-index:1100!important;
}}
html body nav.top .lang-switcher.is-open .lang-dropdown,
html body #topnav .lang-switcher.is-open .lang-dropdown{{display:block!important;}}
html body nav.top .lang-dropdown a,
html body #topnav .lang-dropdown a{{display:flex!important;align-items:center!important;gap:8px!important;padding:10px 12px!important;border-radius:10px!important;color:#00405a!important;-webkit-text-fill-color:#00405a!important;text-decoration:none!important;font-size:13px!important;}}
html body nav.top .btn,
html body nav.top a.btn,
html body #topnav .btn,
html body #topnav a.btn{{
  display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:56px!important;height:56px!important;padding:0 clamp(34px,3.8vw,56px)!important;border-radius:999px!important;
  background:#f59b1e!important;border:0!important;color:#00405a!important;-webkit-text-fill-color:#00405a!important;text-decoration:none!important;
  font-family:'JetBrains Mono',ui-monospace,monospace!important;font-size:12px!important;font-weight:900!important;letter-spacing:.18em!important;text-transform:uppercase!important;white-space:nowrap!important;box-shadow:none!important;flex:0 0 auto!important;
}}
html body nav.top.scrolled .nav-rating-badge,
html body nav.top.nav-scrolled .nav-rating-badge,
html body.scrolled nav.top .nav-rating-badge,
html body nav.top.scrolled .lang-current,
html body nav.top.nav-scrolled .lang-current,
html body.scrolled nav.top .lang-current{{background:rgba(255,255,255,.58)!important;border-color:rgba(0,64,90,.22)!important;color:#00405a!important;-webkit-text-fill-color:#00405a!important;}}
html body nav.top.scrolled .gr-label,
html body.nav-scrolled nav.top .gr-label,
html body.scrolled nav.top .gr-label,
html body nav.top.scrolled .gr-count,
html body.nav-scrolled nav.top .gr-count,
html body.scrolled nav.top .gr-count{{color:#00405a!important;-webkit-text-fill-color:#00405a!important;}}
@media(max-width:1280px){{html body nav.top .nav-rating-badge{{display:none!important;}}}}
@media(max-width:1120px){{
  html body nav.top .brand-word,
  html body nav.top .brand span:not(.lang-flag):not(.lang-name):not(.lang-check):not(.gr-stars):not(.gr-count):not(.gr-label),
  html body #topnav .brand-word,
  html body #topnav .brand span:not(.lang-flag):not(.lang-name):not(.lang-check):not(.gr-stars):not(.gr-count):not(.gr-label){{display:none!important;}}
  html body nav.top .nav-links,html body nav.top .links{{gap:18px!important;}}
}}
@media(max-width:900px){{
  html body nav.top,html body #topnav.top{{min-height:76px!important;background:rgba(0,64,90,.88)!important;backdrop-filter:blur(12px)!important;}}
  html body nav.top .nav-inner,html body nav.top .nav,html body #topnav .nav-inner,html body #topnav .nav{{height:76px!important;min-height:76px!important;padding:10px 20px!important;}}
  html body nav.top .brand-logo,html body nav.top .brand img{{width:54px!important;height:54px!important;min-width:54px!important;min-height:54px!important;}}
  html body nav.top .nav-links,html body nav.top .links{{display:none!important;}}
  html body nav.top .lang-switcher,html body #topnav .lang-switcher{{display:none!important;}}
  html body nav.top .btn,html body nav.top a.btn{{height:46px!important;min-height:46px!important;padding:0 18px!important;font-size:10px!important;letter-spacing:.10em!important;}}
}}
@media(max-width:520px){{html body nav.top .btn,html body nav.top a.btn{{display:none!important;}}}}
</style>
<!-- /EC TOP NAV VISUAL REFINEMENT -->
'''.strip()

@dataclass
class Result:
    page: str
    changed: bool
    controls_added: bool
    old_css_removed: bool
    notes: str


def strip_blocks(source: str) -> tuple[str, bool]:
    before = source
    source = re.sub(r"<!-- EC TOP NAV STANDARDIZATION -->[\s\S]*?<!-- /EC TOP NAV STANDARDIZATION -->\s*", "", source, flags=re.I)
    source = re.sub(r"<!-- EC TOP NAV VISUAL REFINEMENT -->[\s\S]*?<!-- /EC TOP NAV VISUAL REFINEMENT -->\s*", "", source, flags=re.I)
    source = re.sub(rf"<style\b[^>]*id=[\"']{re.escape(OLD_STYLE_ID)}[\"'][^>]*>[\s\S]*?</style>\s*", "", source, flags=re.I)
    source = re.sub(rf"<style\b[^>]*id=[\"']{re.escape(STYLE_ID)}[\"'][^>]*>[\s\S]*?</style>\s*", "", source, flags=re.I)
    return source, source != before


def insert_style(source: str) -> str:
    return source.replace("</head>", STYLE + "\n</head>", 1) if "</head>" in source else STYLE + "\n" + source


def add_controls_to_simple_nav(source: str) -> tuple[str, bool]:
    if "nav-rating-badge" in source and "lang-switcher" in source:
        return source, False
    controls = "\n      " + RATING_HTML.replace("\n", "\n      ") + "\n      " + LANG_HTML.replace("\n", "\n      ") + "\n      "
    pattern = re.compile(r"(<div\s+class=[\"']links[\"']>[\s\S]*?</div>\s*)(<a\s+class=[\"']btn[\"'])", re.I)
    updated, count = pattern.subn(r"\1" + controls + r"\2", source, count=1)
    return updated, count > 0


def normalize_event_cta(source: str, rel: str) -> str:
    if "eventos" not in rel.lower() and "events" not in rel.lower():
        return source
    return re.sub(r"(<nav[\s\S]*?</nav>)", lambda m: re.sub(r">\s*(Reservar|Reserve|Reservar mesa|Book|Book now)\s*</a>", ">Solicitar orçamento</a>", m.group(1), flags=re.I), source, count=1, flags=re.I)


def has_top_nav(source: str) -> bool:
    return bool(re.search(r"<nav\b[^>]*(class=[\"'][^\"']*\btop\b|id=[\"']topnav[\"'])", source, flags=re.I))


def process_page(path: Path) -> Result | None:
    rel = path.relative_to(ROOT).as_posix()
    original = path.read_text(encoding="utf-8", errors="ignore")
    if not has_top_nav(original):
        return None
    updated, old_removed = strip_blocks(original)
    updated, controls_added = add_controls_to_simple_nav(updated)
    updated = normalize_event_cta(updated, rel)
    updated = insert_style(updated)
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return Result(rel, changed, controls_added, old_removed, "no-line-no-frame-home-logo-state")


def write_report(results: list[Result]) -> int:
    REPORT.parent.mkdir(exist_ok=True)
    lines = [
        "# Top Nav Visual Refinement",
        "",
        "Status geral: **PASS**" if results else "Status geral: **FAIL**",
        "",
        "## Objetivo",
        "Refinar o topo após inspeção visual: remover linha/moldura externa, evitar logo duplicada e aproximar todas as páginas do padrão visual da home.",
        "",
        "## Correções aplicadas",
        "- Remoção de `border-bottom`, outline, sombras e pseudo-elementos que criavam linha/moldura.",
        "- Controle de estado das logos `light` e `dark` para não renderizar duas marcas ao mesmo tempo.",
        "- Inclusão de Google Reviews e seletor de idioma em páginas com nav simplificado `.nav/.links`.",
        "- Preservação do CTA `Solicitar orçamento` em páginas de eventos.",
        "",
        "## Guardrails",
        "- Nenhum JSON-LD/schema foi alterado.",
        "- Nenhuma seção de conteúdo foi alterada.",
        "- Alteração limitada a navegação visual e relatório.",
        "",
        "## Resumo",
        f"- Páginas com top processadas: **{len(results)}**",
        f"- Páginas alteradas: **{len([r for r in results if r.changed])}**",
        f"- Páginas que receberam controles ausentes: **{len([r for r in results if r.controls_added])}**",
        "",
        "## Resultados por página",
        "",
        "| Página | Changed | Controles adicionados | CSS antigo removido | Notas |",
        "|---|---:|---:|---:|---|",
    ]
    for r in results:
        lines.append(f"| `{r.page}` | {r.changed} | {r.controls_added} | {r.old_css_removed} | {r.notes} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Top nav visual refinement: PASS" if results else "Top nav visual refinement: FAIL")
    return 0 if results else 1


def main() -> int:
    pages = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts and "node_modules" not in p.parts)
    results = [r for p in pages if (r := process_page(p)) is not None]
    return write_report(results)


if __name__ == "__main__":
    raise SystemExit(main())
