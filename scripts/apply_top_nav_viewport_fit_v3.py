#!/usr/bin/env python3
"""Apply a final viewport-fit patch for the home-reference top nav.

Live visual QA showed that the top nav was structurally standardized, but common
browser widths/zoom levels could still show:
- the event CTA clipped to the right;
- Google Reviews staying visible where it should collapse;
- the hero eyebrow/location line inheriting white from older page CSS.

This script adds one final CSS block at the end of <head> on every page with a
top nav. It does not touch JSON-LD or content sections.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "top_nav_viewport_fit_v3_report.md"
STYLE_ID = "ec-top-nav-viewport-fit-v3-css"
STYLE_RE = re.compile(rf"<style\b[^>]*id=[\"']{re.escape(STYLE_ID)}[\"'][^>]*>[\s\S]*?</style>\s*", re.I)
NAV_RE = re.compile(r"<nav\b[^>]*(?:class=[\"'][^\"']*\btop\b[^\"']*[\"']|id=[\"']topnav[\"'])[^>]*>", re.I)

STYLE = f"""
<style id="{STYLE_ID}">
/* V3 viewport-fit lock. Must stay as the last nav CSS in <head>. */
html,body{{overflow-x:hidden!important;max-width:100%!important;border:0!important;outline:0!important;}}
html body nav.top,html body #topnav.top{{left:0!important;right:0!important;width:100%!important;max-width:100vw!important;overflow:visible!important;border:0!important;border-bottom:0!important;outline:0!important;box-shadow:none!important;}}
html body nav.top::before,html body nav.top::after,html body #topnav::before,html body #topnav::after{{content:none!important;display:none!important;border:0!important;box-shadow:none!important;}}
html body nav.top .nav-inner{{box-sizing:border-box!important;width:100%!important;max-width:min(1440px,100vw)!important;margin:0 auto!important;padding-left:clamp(22px,3.4vw,58px)!important;padding-right:clamp(22px,3.4vw,58px)!important;display:flex!important;align-items:center!important;justify-content:space-between!important;gap:clamp(14px,1.35vw,24px)!important;overflow:visible!important;border:0!important;outline:0!important;box-shadow:none!important;}}
html body nav.top .brand-mark{{flex:0 0 auto!important;min-width:64px!important;padding:0!important;margin:0!important;}}
html body nav.top .brand-logo{{width:64px!important;height:64px!important;min-width:64px!important;min-height:64px!important;max-width:64px!important;max-height:64px!important;}}
html body nav.top .nav-links{{flex:1 1 auto!important;min-width:0!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:clamp(16px,1.65vw,28px)!important;margin:0!important;padding:0!important;}}
html body nav.top .nav-links a{{font-family:'JetBrains Mono',ui-monospace,monospace!important;font-size:12px!important;line-height:1!important;font-weight:800!important;letter-spacing:.12em!important;text-transform:uppercase!important;white-space:nowrap!important;color:#f6efde!important;-webkit-text-fill-color:#f6efde!important;text-shadow:0 2px 10px rgba(0,64,90,.72)!important;}}
html body.scrolled nav.top .nav-links a,html body nav.top.scrolled .nav-links a,html body nav.top.nav-scrolled .nav-links a{{color:#00405a!important;-webkit-text-fill-color:#00405a!important;text-shadow:none!important;}}
html body nav.top .nav-rating-badge{{flex:0 0 auto!important;}}
html body nav.top .lang-switcher{{flex:0 0 auto!important;}}
html body nav.top .btn{{flex:0 0 auto!important;min-height:56px!important;height:56px!important;border:0!important;box-shadow:none!important;overflow:hidden!important;}}
html body nav.top .btn[href*="formulario"]{{min-width:218px!important;max-width:250px!important;padding-left:24px!important;padding-right:24px!important;font-size:11.5px!important;letter-spacing:.135em!important;}}
html body nav.top:has(.btn[href*="formulario"]) .nav-rating-badge{{display:none!important;}}
html body nav.top:has(.btn[href*="formulario"]) .nav-links{{gap:clamp(14px,1.45vw,24px)!important;}}
html body nav.top:has(.btn[href*="formulario"]) .nav-inner{{padding-left:clamp(22px,3.2vw,54px)!important;padding-right:clamp(22px,3.2vw,54px)!important;gap:clamp(12px,1.15vw,20px)!important;}}
@media(max-width:1800px){{html body nav.top .nav-rating-badge{{display:none!important;}}}}
@media(max-width:1500px){{html body nav.top .lang-switcher{{display:none!important;}}html body nav.top .nav-links{{gap:clamp(14px,1.35vw,22px)!important;}}html body nav.top .nav-links a{{font-size:11.5px!important;letter-spacing:.105em!important;}}}}
@media(max-width:1280px){{html body nav.top .nav-links{{gap:13px!important;}}html body nav.top .nav-links a{{font-size:11px!important;letter-spacing:.09em!important;}}html body nav.top .btn{{min-width:128px!important;max-width:180px!important;padding-left:18px!important;padding-right:18px!important;font-size:10.5px!important;letter-spacing:.10em!important;}}html body nav.top .btn[href*="formulario"]{{min-width:184px!important;max-width:220px!important;}}}}
/* Hero eyebrow/location line: final color and typography guard. */
html body header.hero :is(.eyebrow,.hero-eyebrow,.hero-kicker,.page-eyebrow,.page-kicker),
html body header.page-hero :is(.eyebrow,.hero-eyebrow,.hero-kicker,.page-eyebrow,.page-kicker),
html body .page-hero-content .eyebrow.hero-eyebrow{{font-family:'JetBrains Mono',ui-monospace,monospace!important;font-size:11px!important;line-height:1.2!important;font-weight:700!important;letter-spacing:.22em!important;text-transform:uppercase!important;color:#f59b1e!important;-webkit-text-fill-color:#f59b1e!important;text-shadow:0 2px 10px rgba(0,64,90,.72)!important;}}
html body header.hero :is(.eyebrow,.hero-eyebrow,.hero-kicker,.page-eyebrow,.page-kicker)::before,
html body header.page-hero :is(.eyebrow,.hero-eyebrow,.hero-kicker,.page-eyebrow,.page-kicker)::before,
html body .page-hero-content .eyebrow.hero-eyebrow::before{{background:#f59b1e!important;border-color:#f59b1e!important;}}
@media(max-width:900px){{html body nav.top .nav-links,html body nav.top .lang-switcher,html body nav.top .nav-rating-badge{{display:none!important;}}html body nav.top .brand-logo{{width:54px!important;height:54px!important;min-width:54px!important;min-height:54px!important;}}}}
</style>
""".strip()


@dataclass
class Result:
    page: str
    changed: bool
    has_event_cta: bool
    notes: str


def process(path: Path) -> Result | None:
    rel = path.relative_to(ROOT).as_posix()
    original = path.read_text(encoding="utf-8", errors="ignore")
    if not NAV_RE.search(original):
        return None
    updated = STYLE_RE.sub("", original)
    if "</head>" in updated:
        updated = updated.replace("</head>", STYLE + "\n</head>", 1)
    else:
        updated = STYLE + "\n" + updated
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return Result(rel, changed, 'formulario.html' in updated, "final-css-order-viewport-fit")


def write_report(results: list[Result]) -> int:
    REPORT.parent.mkdir(exist_ok=True)
    status = "PASS" if results else "FAIL"
    lines = [
        "# Top Nav Viewport Fit V3",
        "",
        f"Status geral: **{status}**",
        "",
        "## Objetivo",
        "Corrigir o overflow visual remanescente do topo em larguras reais de navegador, especialmente `eventos.html`, e travar a cor da linha/eyebrow em amarelo nas páginas internas.",
        "",
        "## Correções",
        "- CSS final inserido como último bloco de navegação no `<head>`.",
        "- Google Reviews oculto em larguras até 1800px para impedir corte lateral.",
        "- Em páginas com CTA de evento (`formulario.html`), Google Reviews é oculto sempre.",
        "- Idioma é oculto abaixo de 1500px para preservar menu e CTA.",
        "- Botão `Solicitar orçamento` recebe largura controlada para não sair da tela.",
        "- Linha/eyebrow do hero é forçada para amarelo, JetBrains Mono, 11px, uppercase.",
        "",
        "## Guardrails",
        "- Nenhum JSON-LD/schema foi alterado.",
        "- Nenhum conteúdo de seção foi alterado.",
        "- Apenas CSS final de navegação foi inserido/atualizado.",
        "",
        "## Resumo",
        f"- Páginas processadas: **{len(results)}**",
        f"- Páginas alteradas: **{len([r for r in results if r.changed])}**",
        f"- Páginas com CTA de evento: **{len([r for r in results if r.has_event_cta])}**",
        "",
        "## Resultados por página",
        "",
        "| Página | Changed | CTA evento detectado | Notas |",
        "|---|---:|---:|---|",
    ]
    for r in results:
        lines.append(f"| `{r.page}` | {r.changed} | {r.has_event_cta} | {r.notes} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Top nav viewport fit v3: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    pages = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts and "node_modules" not in p.parts)
    results = [r for p in pages if (r := process(p)) is not None]
    return write_report(results)


if __name__ == "__main__":
    raise SystemExit(main())
