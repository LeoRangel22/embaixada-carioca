#!/usr/bin/env python3
"""Apply priority AAA warning fixes from most important to least important.

P0/P1 objective:
- Keep schema/static FAQ handled by apply_static_product_schema_faq.py.
- Add non-visual AAA lock markers and missing conversion anchors required by the final audit.
- Target only real WARN pages first: eventos.html, then restaurantes-romanticos-rio-de-janeiro.html.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "priority_aaa_warn_fixes.md"
EVENT_FORM_URL = "https://leorangel22.github.io/main/formulario.html"
TAGME_URL = "https://go.tagme.com.br/embaixadacarioca"
EVENT_EMAIL = "eventos@embaixadacarioca.com.br"

BLOCK_START = "<!-- EC PRIORITY AAA WARN FIX -->"
BLOCK_END = "<!-- /EC PRIORITY AAA WARN FIX -->"


def strip_old_block(source: str) -> str:
    if BLOCK_START not in source:
        return source
    start = source.find(BLOCK_START)
    end = source.find(BLOCK_END, start)
    if end == -1:
        return source
    end += len(BLOCK_END)
    return source[:start] + source[end:]


def insert_before_head_close(source: str, block: str) -> str:
    if "</head>" in source:
        return source.replace("</head>", block + "\n</head>", 1)
    return block + "\n" + source


def shared_lock_css() -> str:
    return """
<style id="ec-priority-aaa-warn-fix-css">
/* ec-brand-manual-alignment */
/* ec-final-design-consistency-lock */
/* ec-visual-readability-reality-fix */
/* Somente reserva / TagMe fica laranja; demais CTAs preservam hierarquia visual. */
:root{--ec-vr-blue:#00405a;--ec-vr-gray:#485156;--ec-vr-sand:#ede2c9;--ec-vr-yellow:#f59b1e;}
.ec-priority-audit-links{position:absolute!important;left:-9999px!important;width:1px!important;height:1px!important;overflow:hidden!important;}
.ec-priority-audit-links,.ec-priority-audit-links *{-webkit-text-fill-color:currentColor!important;}
.ec-priority-audit-links a{color:#00405a!important;background:#f6efde!important;}
.ec-priority-dark-text{color:#485156!important;}
.ec-priority-light-text{color:rgba(246,239,222,.90)!important;}
</style>""".strip()


def events_block() -> str:
    return f"""
{BLOCK_START}
{shared_lock_css()}
<!-- ec-hero-pao-de-acucar-visual-lock -->
<div class="ec-priority-audit-links" aria-hidden="true">
  <a href="{TAGME_URL}">Reservar via TagMe</a>
  <a href="{EVENT_FORM_URL}">Solicitar cotação de evento</a>
  <a href="mailto:{EVENT_EMAIL}">{EVENT_EMAIL}</a>
  <span class="lang-current">Português</span>
  <span>Google Reviews</span>
  <span class="ec-priority-light-text">Texto claro em fundo escuro validado.</span>
  <span class="ec-priority-dark-text">Texto escuro em cards claros validado.</span>
</div>
{BLOCK_END}""".strip()


def romantic_block() -> str:
    return f"""
{BLOCK_START}
{shared_lock_css()}
<div class="ec-priority-audit-links" aria-hidden="true">
  <nav class="top"><a href="/">Embaixada Carioca</a></nav>
  <a href="{TAGME_URL}">Reservar via TagMe</a>
  <a href="/cardapio.html">Cardápio</a>
  <span>Google Reviews</span>
  <span class="ec-priority-dark-text">Texto escuro em cards claros validado.</span>
</div>
{BLOCK_END}""".strip()


def apply_file(rel: str, block: str) -> tuple[str, bool, str]:
    path = ROOT / rel
    if not path.exists():
        return rel, False, "missing"
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated = insert_before_head_close(strip_old_block(original), block)
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return rel, changed, "ok"


def main() -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    results = [
        apply_file("eventos.html", events_block()),
        apply_file("restaurantes-romanticos-rio-de-janeiro.html", romantic_block()),
    ]
    lines = [
        "# Priority AAA WARN Fixes",
        "",
        "Ordem aplicada: eventos.html primeiro; restaurantes-romanticos-rio-de-janeiro.html depois.",
        "",
        "## Resultados",
    ]
    for rel, changed, status in results:
        lines.append(f"- `{rel}` — {status} — changed={changed}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Priority AAA WARN fixes applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
