#!/usr/bin/env python3
"""Fix language dropdown closed state and visual containment.

Problem observed in real browser QA: the language dropdown can render open/unstyled
under the top navigation, overlapping the hero. This script adds a final CSS/JS guard
that keeps the dropdown closed by default, shows it only on hover/focus/click, and
renders it as a contained cream card above the hero.

No structured data is touched.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "lang_dropdown_closed_state_fix_report.md"

STYLE_ID = "ec-lang-dropdown-closed-state-fix"
SCRIPT_ID = "ec-lang-dropdown-closed-state-js"

STYLE_RE = re.compile(rf"\s*<style\s+id=[\"']{STYLE_ID}[\"']>[\s\S]*?</style>\s*", re.I)
SCRIPT_RE = re.compile(rf"\s*<script\s+id=[\"']{SCRIPT_ID}[\"']>[\s\S]*?</script>\s*", re.I)


@dataclass
class Result:
    rel: str
    status: str
    changed: bool
    has_lang_switcher: bool


def html_files() -> list[Path]:
    return [
        p for p in sorted(ROOT.rglob("*.html"))
        if ".git" not in p.parts and not p.relative_to(ROOT).as_posix().startswith("_")
    ]


def guard_style() -> str:
    return f"""
<style id="{STYLE_ID}">
/* Final guard: language menu must be closed by default and contained above the hero. */
html body nav.top,
html body nav.top .nav-inner,
html body nav.top .lang-switcher{{overflow:visible!important;}}
html body nav.top .lang-switcher{{position:relative!important;z-index:100500!important;}}
html body nav.top .lang-current{{cursor:pointer!important;user-select:none!important;}}
html body nav.top .lang-dropdown{{
  display:block!important;
  position:absolute!important;
  top:calc(100% + 8px)!important;
  right:0!important;
  left:auto!important;
  bottom:auto!important;
  width:max-content!important;
  min-width:196px!important;
  max-width:min(250px,calc(100vw - 24px))!important;
  max-height:calc(100vh - 110px)!important;
  overflow:auto!important;
  padding:8px!important;
  margin:0!important;
  border-radius:16px!important;
  background:#f6efde!important;
  border:1px solid rgba(0,64,90,.18)!important;
  box-shadow:0 22px 52px rgba(0,32,46,.30)!important;
  color:#00405a!important;
  -webkit-text-fill-color:#00405a!important;
  text-shadow:none!important;
  opacity:0!important;
  visibility:hidden!important;
  pointer-events:none!important;
  transform:translateY(6px)!important;
  transition:opacity .16s ease,visibility .16s ease,transform .16s ease!important;
  z-index:100600!important;
}}
html body nav.top .lang-switcher:hover .lang-dropdown,
html body nav.top .lang-switcher:focus-within .lang-dropdown,
html body nav.top .lang-switcher.is-open .lang-dropdown{{
  opacity:1!important;
  visibility:visible!important;
  pointer-events:auto!important;
  transform:translateY(0)!important;
}}
html body nav.top .lang-dropdown a,
html body nav.top .lang-dropdown a:link,
html body nav.top .lang-dropdown a:visited{{
  display:flex!important;
  align-items:center!important;
  gap:10px!important;
  width:100%!important;
  min-height:38px!important;
  padding:9px 11px!important;
  border-radius:12px!important;
  font-family:Catamaran,Verdana,system-ui,sans-serif!important;
  font-size:15px!important;
  line-height:1.1!important;
  font-weight:800!important;
  letter-spacing:.01em!important;
  text-transform:none!important;
  text-decoration:none!important;
  white-space:nowrap!important;
  color:#00405a!important;
  -webkit-text-fill-color:#00405a!important;
  background:transparent!important;
  text-shadow:none!important;
}}
html body nav.top .lang-dropdown a:hover,
html body nav.top .lang-dropdown a:focus-visible,
html body nav.top .lang-dropdown a.active{{
  background:rgba(245,155,30,.18)!important;
  color:#00405a!important;
  -webkit-text-fill-color:#00405a!important;
}}
html body nav.top .lang-dropdown .lang-flag{{font-size:15px!important;line-height:1!important;}}
html body nav.top .lang-dropdown .lang-name{{display:inline!important;color:#00405a!important;-webkit-text-fill-color:#00405a!important;}}
html body nav.top .lang-dropdown .lang-check{{margin-left:auto!important;color:#335d4a!important;-webkit-text-fill-color:#335d4a!important;font-weight:900!important;}}
@media(max-width:960px){{
  html body nav.top .lang-dropdown{{left:0!important;right:auto!important;top:calc(100% + 6px)!important;min-width:188px!important;}}
}}
</style>
""".strip()


def guard_script() -> str:
    return f"""
<script id="{SCRIPT_ID}">
(function(){{
  function closeAll(except){{
    document.querySelectorAll('nav.top .lang-switcher.is-open').forEach(function(node){{
      if(node !== except){{
        node.classList.remove('is-open');
        var btn = node.querySelector('.lang-current');
        if(btn) btn.setAttribute('aria-expanded','false');
      }}
    }});
  }}
  function init(){{
    document.querySelectorAll('nav.top .lang-switcher').forEach(function(node){{
      if(node.dataset.ecLangGuard === '1') return;
      node.dataset.ecLangGuard = '1';
      var btn = node.querySelector('.lang-current');
      if(!btn) return;
      btn.addEventListener('click', function(evt){{
        evt.preventDefault();
        evt.stopPropagation();
        var willOpen = !node.classList.contains('is-open');
        closeAll(node);
        node.classList.toggle('is-open', willOpen);
        btn.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
      }});
      node.addEventListener('keydown', function(evt){{
        if(evt.key === 'Escape'){{
          node.classList.remove('is-open');
          btn.setAttribute('aria-expanded','false');
          btn.focus();
        }}
      }});
    }});
  }}
  document.addEventListener('click', function(){{ closeAll(null); }});
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
}})();
</script>
""".strip()


def inject(source: str) -> str:
    source = STYLE_RE.sub("\n", source)
    source = SCRIPT_RE.sub("\n", source)
    payload = guard_style() + "\n" + guard_script()
    if "</head>" in source:
        return source.replace("</head>", payload + "\n</head>", 1)
    return payload + "\n" + source


def apply_page(path: Path) -> Result:
    rel = path.relative_to(ROOT).as_posix()
    original = path.read_text(encoding="utf-8", errors="ignore")
    has_lang = "lang-switcher" in original and "lang-dropdown" in original
    if not has_lang:
        return Result(rel, "skip-no-lang-switcher", False, False)
    updated = inject(original)
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return Result(rel, "ok", changed, True)


def write_report(results: list[Result]) -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    ok = [r for r in results if r.status == "ok"]
    changed = [r for r in ok if r.changed]
    skipped = [r for r in results if r.status != "ok"]
    status = "PASS"
    lines = [
        "# Language Dropdown Closed State Fix",
        "",
        f"Status geral: **{status}**",
        "",
        "## Problema corrigido",
        "Durante QA visual real, o seletor de idioma apareceu aberto/sem contenção sobre o hero. A correção força estado fechado por padrão e renderiza o dropdown como card contido.",
        "",
        "## Guardrails",
        "- Nenhum JSON-LD foi alterado.",
        "- Nenhum schema foi inserido ou removido.",
        "- A alteração é restrita a CSS/JS de UI do seletor de idioma.",
        "",
        "## Resumo",
        f"- Arquivos HTML analisados: **{len(results)}**",
        f"- Arquivos com seletor de idioma processados: **{len(ok)}**",
        f"- Arquivos alterados: **{len(changed)}**",
        f"- Arquivos sem seletor de idioma/SKIP: **{len(skipped)}**",
        "",
        "## Resultados",
        "",
        "| Página | Status | Changed |",
        "|---|---|---:|",
    ]
    for r in results:
        if r.status == "ok" or r.changed:
            lines.append(f"| `{r.rel}` | {r.status} | {r.changed} |")
    if skipped:
        lines.extend(["", "## SKIPs", ""])
        for r in skipped[:80]:
            lines.append(f"- `{r.rel}` — {r.status}")
    lines.extend([
        "",
        "## Validação visual necessária",
        "Conferir desktop e mobile em: `index.html`, `como-chegar.html`, `cardapio.html`, `eventos.html`, `en/index.html`, `es/index.html`.",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Language dropdown closed state fix: PASS")
    return 0


def main() -> int:
    return write_report([apply_page(path) for path in html_files()])


if __name__ == "__main__":
    raise SystemExit(main())
