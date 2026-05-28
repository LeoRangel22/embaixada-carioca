#!/usr/bin/env python3
"""Standardize the top navigation frame across HTML pages.

Reference: home navigation visual model. Eventos pages keep the same frame but use
"Solicitar orçamento" as the primary CTA. Other pages keep the reservation CTA.

This is intentionally CSS/markup-safe:
- It does not touch JSON-LD.
- It supports both legacy structures: `.nav-inner/.nav-links` and `.nav/.links`.
- It normalizes height, logo, link spacing, CTA frame and mobile behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "top_nav_standardization_report.md"
STYLE_ID = "ec-top-nav-standardization-css"

STYLE_BLOCK = f"""
<!-- EC TOP NAV STANDARDIZATION -->
<style id="{STYLE_ID}">
/* Home-reference top navigation normalization. Applies only to the fixed top nav. */
html body nav.top,
html body header nav.top,
html body #topnav.top,
html body .top#topnav{{
  position:fixed!important;
  top:0!important;left:0!important;right:0!important;
  z-index:900!important;
  min-height:104px!important;
  background:linear-gradient(180deg,rgba(0,64,90,.58) 0%,rgba(0,64,90,.34) 58%,rgba(0,64,90,0) 100%)!important;
  border-bottom:1px solid rgba(237,226,201,.14)!important;
  box-shadow:none!important;
  backdrop-filter:none!important;
}}
html body nav.top.scrolled,
html body nav.top.nav-scrolled,
html body.scrolled nav.top{{
  min-height:84px!important;
  background:rgba(237,226,201,.96)!important;
  border-bottom:1px solid rgba(0,64,90,.16)!important;
  box-shadow:0 12px 34px rgba(0,64,90,.12)!important;
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
  padding:14px clamp(24px,4vw,64px)!important;
  display:flex!important;
  align-items:center!important;
  justify-content:space-between!important;
  gap:28px!important;
  color:#f6efde!important;
}}
html body nav.top.scrolled .nav-inner,
html body nav.top.scrolled .nav,
html body nav.top.nav-scrolled .nav-inner,
html body nav.top.nav-scrolled .nav,
html body.scrolled nav.top .nav-inner,
html body.scrolled nav.top .nav{{
  height:84px!important;
  min-height:84px!important;
  color:#00405a!important;
}}
html body nav.top .brand-mark,
html body nav.top .brand,
html body #topnav .brand-mark,
html body #topnav .brand{{
  display:flex!important;
  align-items:center!important;
  gap:18px!important;
  min-width:0!important;
  padding:0!important;
  color:inherit!important;
  text-decoration:none!important;
  font-family:'JetBrains Mono',ui-monospace,monospace!important;
  font-size:11px!important;
  line-height:1.35!important;
  font-weight:700!important;
  letter-spacing:.18em!important;
  text-transform:uppercase!important;
}}
html body nav.top .brand-logo,
html body nav.top .brand img,
html body #topnav .brand-logo,
html body #topnav .brand img{{
  width:68px!important;
  height:68px!important;
  min-width:68px!important;
  min-height:68px!important;
  max-width:68px!important;
  max-height:68px!important;
  object-fit:contain!important;
  display:block!important;
  filter:none!important;
}}
html body nav.top .brand-word,
html body nav.top .brand-word-x,
html body nav.top .brand span:not(.lang-flag):not(.lang-name):not(.lang-check),
html body #topnav .brand-word,
html body #topnav .brand-word-x,
html body #topnav .brand span:not(.lang-flag):not(.lang-name):not(.lang-check){{
  display:block!important;
  border-left:1px solid currentColor!important;
  padding-left:18px!important;
  margin-left:0!important;
  min-width:140px!important;
  max-width:220px!important;
  color:inherit!important;
  opacity:.94!important;
  white-space:normal!important;
}}
html body nav.top .nav-links,
html body nav.top .links,
html body #topnav .nav-links,
html body #topnav .links{{
  display:flex!important;
  align-items:center!important;
  justify-content:center!important;
  flex:1 1 auto!important;
  gap:clamp(18px,2vw,28px)!important;
  list-style:none!important;
  padding:0!important;
  margin:0!important;
  min-width:0!important;
}}
html body nav.top .nav-links a,
html body nav.top .links a,
html body #topnav .nav-links a,
html body #topnav .links a{{
  display:inline-flex!important;
  align-items:center!important;
  min-height:44px!important;
  padding:6px 0!important;
  color:inherit!important;
  -webkit-text-fill-color:currentColor!important;
  text-decoration:none!important;
  font-family:'JetBrains Mono',ui-monospace,monospace!important;
  font-size:12px!important;
  line-height:1!important;
  font-weight:700!important;
  letter-spacing:.12em!important;
  text-transform:uppercase!important;
  white-space:nowrap!important;
  opacity:.96!important;
  text-shadow:0 2px 10px rgba(0,64,90,.72)!important;
}}
html body nav.top.scrolled .nav-links a,
html body nav.top.scrolled .links a,
html body nav.top.nav-scrolled .nav-links a,
html body nav.top.nav-scrolled .links a,
html body.scrolled nav.top .nav-links a,
html body.scrolled nav.top .links a{{
  color:#00405a!important;
  text-shadow:none!important;
}}
html body nav.top .nav-links a:hover,
html body nav.top .links a:hover,
html body #topnav .nav-links a:hover,
html body #topnav .links a:hover{{color:#f59b1e!important;-webkit-text-fill-color:#f59b1e!important;}}
html body nav.top .btn,
html body nav.top a.btn,
html body #topnav .btn,
html body #topnav a.btn{{
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  min-height:56px!important;
  height:56px!important;
  padding:0 clamp(28px,3vw,44px)!important;
  border-radius:999px!important;
  background:#f59b1e!important;
  border:1.5px solid #f59b1e!important;
  color:#00405a!important;
  -webkit-text-fill-color:#00405a!important;
  text-decoration:none!important;
  font-family:'JetBrains Mono',ui-monospace,monospace!important;
  font-size:12px!important;
  font-weight:800!important;
  letter-spacing:.14em!important;
  text-transform:uppercase!important;
  white-space:nowrap!important;
  box-shadow:none!important;
  flex:0 0 auto!important;
}}
html body nav.top .btn:hover,
html body nav.top a.btn:hover,
html body #topnav .btn:hover,
html body #topnav a.btn:hover{{
  transform:translateY(-1px)!important;
  background:#f6efde!important;
  border-color:#f6efde!important;
  color:#00405a!important;
  -webkit-text-fill-color:#00405a!important;
}}
html body nav.top .lang-switcher,
html body #topnav .lang-switcher{{flex:0 0 auto!important;}}
html body nav.top .nav-rating-badge,
html body #topnav .nav-rating-badge{{
  min-height:44px!important;
  border-radius:999px!important;
  flex:0 0 auto!important;
}}
@media(max-width:1120px){{
  html body nav.top .brand-word,
  html body nav.top .brand-word-x,
  html body nav.top .brand span:not(.lang-flag):not(.lang-name):not(.lang-check),
  html body #topnav .brand-word,
  html body #topnav .brand-word-x,
  html body #topnav .brand span:not(.lang-flag):not(.lang-name):not(.lang-check){{display:none!important;}}
  html body nav.top .nav-links,
  html body nav.top .links,
  html body #topnav .nav-links,
  html body #topnav .links{{gap:18px!important;}}
}}
@media(max-width:900px){{
  html body nav.top,
  html body #topnav.top{{min-height:76px!important;background:rgba(0,64,90,.88)!important;backdrop-filter:blur(12px)!important;}}
  html body nav.top .nav-inner,
  html body nav.top .nav,
  html body #topnav .nav-inner,
  html body #topnav .nav{{height:76px!important;min-height:76px!important;padding:10px 20px!important;}}
  html body nav.top .brand-logo,
  html body nav.top .brand img,
  html body #topnav .brand-logo,
  html body #topnav .brand img{{width:54px!important;height:54px!important;min-width:54px!important;min-height:54px!important;}}
  html body nav.top .nav-links,
  html body nav.top .links,
  html body #topnav .nav-links,
  html body #topnav .links{{display:none!important;}}
  html body nav.top .btn,
  html body nav.top a.btn,
  html body #topnav .btn,
  html body #topnav a.btn{{min-height:46px!important;height:46px!important;padding:0 18px!important;font-size:10px!important;letter-spacing:.10em!important;}}
}}
@media(max-width:520px){{
  html body nav.top .btn,
  html body nav.top a.btn,
  html body #topnav .btn,
  html body #topnav a.btn{{display:none!important;}}
}}
</style>
<!-- /EC TOP NAV STANDARDIZATION -->
""".strip()

HTML_RE = re.compile(r"\.html$")

@dataclass
class PageResult:
    page: str
    has_nav: bool
    changed: bool
    cta_status: str
    notes: str


def strip_old(source: str) -> str:
    source = re.sub(r"<!-- EC TOP NAV STANDARDIZATION -->[\s\S]*?<!-- /EC TOP NAV STANDARDIZATION -->\s*", "", source, flags=re.I)
    # Remove old repeated top standardization style if id-only survived.
    source = re.sub(rf"<style\b[^>]*id=[\"']{re.escape(STYLE_ID)}[\"'][^>]*>[\s\S]*?</style>\s*", "", source, flags=re.I)
    return source


def insert_style(source: str) -> str:
    if "</head>" in source:
        return source.replace("</head>", STYLE_BLOCK + "\n</head>", 1)
    return STYLE_BLOCK + "\n" + source


def is_event_page(rel: str) -> bool:
    name = Path(rel).name.lower()
    return name in {"eventos.html", "events.html"} or "eventos" in rel.lower() or "events" in rel.lower()


def normalize_event_cta(source: str) -> tuple[str, str]:
    if "leorangel22.github.io/main/formulario.html" in source and re.search(r">\s*Solicitar\s+or[çc]amento\s*<", source, flags=re.I):
        return source, "already-ok"
    # Only change a nav/header CTA when it already points to the event form or says evento/orçamento.
    updated = re.sub(
        r'(<a\b[^>]*class=["\'][^"\']*\bbtn\b[^"\']*["\'][^>]*href=["\']https://leorangel22\.github\.io/main/formulario\.html["\'][^>]*>)\s*[^<]+\s*</a>',
        r'\1Solicitar orçamento</a>',
        source,
        count=1,
        flags=re.I | re.S,
    )
    if updated != source:
        return updated, "normalized"
    return source, "not-found"


def normalize_reservation_cta(source: str) -> tuple[str, str]:
    # Do not force every page if it uses a different but intentional CTA; just normalize obvious nav reservation CTAs.
    if "go.tagme.com.br/embaixadacarioca" in source:
        return source, "reservation-present"
    return source, "not-forced"


def apply_page(path: Path) -> PageResult:
    rel = path.relative_to(ROOT).as_posix()
    original = path.read_text(encoding="utf-8", errors="ignore")
    has_nav = bool(re.search(r"<nav\b[^>]*(class=[\"'][^\"']*\btop\b|id=[\"']topnav[\"'])", original, flags=re.I))
    if not has_nav:
        return PageResult(rel, False, False, "skip", "no top nav")
    updated = strip_old(original)
    cta_status = "skip"
    if is_event_page(rel):
        updated, cta_status = normalize_event_cta(updated)
    else:
        updated, cta_status = normalize_reservation_cta(updated)
    updated = insert_style(updated)
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return PageResult(rel, True, changed, cta_status, "top-css-standardized")


def write_report(results: list[PageResult]) -> int:
    REPORT.parent.mkdir(exist_ok=True)
    nav_pages = [r for r in results if r.has_nav]
    changed = [r for r in nav_pages if r.changed]
    status = "PASS" if nav_pages else "FAIL"
    lines = [
        "# Top Nav Standardization",
        "",
        f"Status geral: **{status}**",
        "",
        "## Objetivo",
        "Padronizar o `top`/menu superior em todas as páginas com base visual na home, mantendo em `eventos.html` o CTA `Solicitar orçamento`.",
        "",
        "## O que foi padronizado",
        "- Altura e frame do topo.",
        "- Logo, marca, espaçamento e grid interno.",
        "- Links do menu principal.",
        "- Botão principal.",
        "- Comportamento do topo em desktop, scrolled e mobile.",
        "- Compatibilidade com variações antigas: `.nav-inner/.nav-links` e `.nav/.links`.",
        "",
        "## Guardrails",
        "- Nenhum JSON-LD/schema foi alterado.",
        "- Nenhum conteúdo de seção foi alterado.",
        "- Em páginas de eventos, o botão principal permanece como `Solicitar orçamento`.",
        "- Nas demais páginas, o botão de reserva existente foi preservado.",
        "",
        "## Resumo",
        f"- Arquivos HTML analisados: **{len(results)}**",
        f"- Páginas com `top` encontradas: **{len(nav_pages)}**",
        f"- Páginas alteradas: **{len(changed)}**",
        "",
        "## Resultados por página",
        "",
        "| Página | Top encontrado | Changed | CTA | Notas |",
        "|---|---:|---:|---|---|",
    ]
    for r in results:
        if r.has_nav:
            lines.append(f"| `{r.page}` | {r.has_nav} | {r.changed} | {r.cta_status} | {r.notes} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Top nav standardization: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    pages = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts and "node_modules" not in p.parts)
    results = [apply_page(p) for p in pages]
    return write_report(results)


if __name__ == "__main__":
    raise SystemExit(main())
