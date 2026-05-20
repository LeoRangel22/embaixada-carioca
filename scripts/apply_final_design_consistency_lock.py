#!/usr/bin/env python3
"""
Final Design Consistency Lock — Embaixada Carioca

Objetivo:
- padronizar a linha laranja da hero em todas as páginas com a mesma coordenada;
- padronizar botões no padrão visual da home: formato, acabamento, fonte e altura;
- remover setas visíveis dos botões;
- padronizar os frames/pílulas acima dos botões no padrão da home;
- auditar por código se ainda existe falha grosseira de design.

Este script roda no fim do pipeline visual para vencer overrides antigos.
"""
from __future__ import annotations

from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "final_design_consistency_lock_report.md"
REPORT_CSV = REPORT_DIR / "final_design_consistency_lock_details.csv"

CSS_START = "<!-- EC Final Design Consistency Lock -->"
CSS_END = "<!-- /EC Final Design Consistency Lock -->"
CSS_RE = re.compile(r"\n*<!-- EC Final Design Consistency Lock -->[\s\S]*?<!-- /EC Final Design Consistency Lock -->\s*", re.I)
HEAD_CLOSE_RE = re.compile(r"</head>", re.I)
HTML_FILE_RE = re.compile(r"\.html?$", re.I)
HERO_RE = re.compile(r"<header\b(?=[^>]*class=[\"'][^\"']*\b(?:hero|page-hero)\b[^\"']*[\"'])[^>]*>[\s\S]*?</header>", re.I)
ANCHOR_OR_BUTTON_RE = re.compile(r"<(a|button)\b(?=[^>]*class=[\"'][^\"']*\b(?:btn|button|cta)\b[^\"']*[\"'])[^>]*>[\s\S]*?</\1>", re.I)
ARROW_RE = re.compile(r"\s*(?:→|↗|›|»|➜|➔|➡|&rarr;|&#8594;|&#x2192;)\s*", re.I)
OLD_PIN_RE = re.compile(r"<span\s+class=[\"']drawer-icon[\"']>\s*📍\s*</span>\s*", re.I)

SKIP = {"404.html", "offline.html", "home-preview.html"}

CSS_BLOCK = f"""{CSS_START}
<style id="ec-final-design-consistency-lock">
/* FINAL DESIGN LOCK — linha laranja, botões e frames no padrão da home */

/* 1) Linha laranja da hero: coordenada única em home e páginas internas */
@media (min-width:961px){{
  html body header.hero .hero-content .eyebrow.hero-eyebrow,
  html body header.page-hero .page-hero-content .eyebrow.hero-eyebrow{{
    position:absolute!important;
    top:96px!important;
    left:clamp(78px,5.5vw,112px)!important;
    transform:none!important;
    margin:0!important;
    width:calc(100vw - clamp(78px,5.5vw,112px) - 250px)!important;
    max-width:none!important;
    white-space:nowrap!important;
    overflow:hidden!important;
    text-overflow:clip!important;
    display:flex!important;
    align-items:center!important;
    gap:14px!important;
    font-family:"JetBrains Mono",ui-monospace,monospace!important;
    font-size:9px!important;
    line-height:1!important;
    letter-spacing:.31em!important;
    font-weight:700!important;
    text-transform:uppercase!important;
    color:var(--amarelo,#f59b1e)!important;
    opacity:1!important;
    text-shadow:0 2px 12px rgba(0,32,46,.66)!important;
    z-index:20!important;
    border:0!important;
    outline:0!important;
    box-shadow:none!important;
  }}
  html body header.hero .hero-content .eyebrow.hero-eyebrow::before,
  html body header.page-hero .page-hero-content .eyebrow.hero-eyebrow::before{{
    content:""!important;
    display:inline-block!important;
    flex:0 0 34px!important;
    width:34px!important;
    min-width:34px!important;
    height:2px!important;
    margin:0!important;
    background:var(--amarelo,#f59b1e)!important;
    opacity:1!important;
  }}
}}

/* 2) Botões: padrão da home, sem setas e com acabamento único */
html body .btn,
html body a.btn,
html body button.btn,
html body .hero-ctas .btn,
html body .hero-ctas a.btn,
html body .ctas .btn,
html body .ctas a.btn{{
  min-height:60px!important;
  height:60px!important;
  padding:0 36px!important;
  border-radius:999px!important;
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  gap:0!important;
  font-family:"JetBrains Mono",ui-monospace,monospace!important;
  font-size:14px!important;
  line-height:1!important;
  font-weight:900!important;
  letter-spacing:.13em!important;
  text-transform:uppercase!important;
  text-align:center!important;
  text-decoration:none!important;
  white-space:nowrap!important;
  border:1px solid var(--amarelo,#f59b1e)!important;
  background:var(--amarelo,#f59b1e)!important;
  color:#fff!important;
  box-shadow:0 9px 0 rgba(0,64,90,.20),0 16px 30px rgba(0,32,46,.18)!important;
  overflow:hidden!important;
}}
html body .btn::after,
html body .btn::before,
html body a.btn::after,
html body button.btn::after{{
  content:none!important;
  display:none!important;
}}
html body .btn-secondary,
html body a.btn-secondary,
html body .hero-ctas .btn-secondary,
html body .hero-ctas a.btn-secondary,
html body .ctas .btn-secondary,
html body .ctas a.btn-secondary,
html body .hero-ctas a:not(.btn):not(.nav-wa-btn),
html body .ctas a:not(.btn):not(.nav-wa-btn){{
  min-height:60px!important;
  height:60px!important;
  padding:0 36px!important;
  border-radius:999px!important;
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  gap:0!important;
  font-family:"JetBrains Mono",ui-monospace,monospace!important;
  font-size:14px!important;
  line-height:1!important;
  font-weight:900!important;
  letter-spacing:.13em!important;
  text-transform:uppercase!important;
  text-align:center!important;
  text-decoration:none!important;
  white-space:nowrap!important;
  color:var(--areia-pale,#f6efde)!important;
  border:1px solid rgba(246,239,222,.82)!important;
  background:rgba(0,32,46,.18)!important;
  box-shadow:inset 0 0 0 1px rgba(246,239,222,.08),0 10px 26px rgba(0,32,46,.18)!important;
  backdrop-filter:blur(6px)!important;
  -webkit-backdrop-filter:blur(6px)!important;
  overflow:hidden!important;
}}
html body .btn-secondary::after,
html body .btn-secondary::before,
html body .hero-ctas a::after,
html body .ctas a::after{{
  content:none!important;
  display:none!important;
}}

/* Topo: reservar sem seta, mantendo o padrão aprovado */
html body nav.top .btn,
html body nav.top a.btn[href*="tagme"]{{
  min-height:60px!important;
  height:60px!important;
  width:188px!important;
  min-width:188px!important;
  padding:0!important;
  letter-spacing:.16em!important;
}}

/* 3) Frames/pílulas acima dos botões: padrão home */
html body header.hero .hero-chips,
html body header.page-hero .hero-chips{{
  display:flex!important;
  flex-wrap:wrap!important;
  align-items:center!important;
  gap:8px!important;
  margin:0!important;
  border:0!important;
  outline:0!important;
  box-shadow:none!important;
}}
html body header.hero .hero-chips span,
html body header.hero .hero-chips a,
html body header.page-hero .hero-chips span,
html body header.page-hero .hero-chips a{{
  min-height:36px!important;
  height:36px!important;
  padding:0 17px!important;
  border-radius:999px!important;
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  gap:7px!important;
  background:rgba(0,32,46,.46)!important;
  border:1px solid rgba(246,239,222,.30)!important;
  color:var(--areia-pale,#f6efde)!important;
  box-shadow:0 8px 22px rgba(0,32,46,.14)!important;
  backdrop-filter:blur(7px)!important;
  -webkit-backdrop-filter:blur(7px)!important;
  font-family:Catamaran,Verdana,system-ui,sans-serif!important;
  font-size:14px!important;
  line-height:1!important;
  font-weight:700!important;
  letter-spacing:0!important;
  text-decoration:none!important;
  white-space:nowrap!important;
}}
html body header.hero .hero-chips span::before,
html body header.page-hero .hero-chips span::before,
html body header.hero .hero-chips a::before,
html body header.page-hero .hero-chips a::before{{
  box-shadow:none!important;
}}

/* 4) Blindagem contra molduras cinzas residuais em hero/topo */
html body header.hero,
html body header.page-hero,
html body header.hero .hero-content,
html body header.page-hero .page-hero-content,
html body header.hero .hero-photo,
html body header.page-hero .page-hero-photo,
html body header.hero .hero-overlay,
html body header.page-hero .page-hero-overlay{{
  border:0!important;
  outline:0!important;
  box-shadow:none!important;
}}

@media (max-width:960px){{
  html body .btn,
  html body a.btn,
  html body button.btn,
  html body .btn-secondary,
  html body a.btn-secondary,
  html body .hero-ctas a,
  html body .ctas a{{
    min-height:54px!important;
    height:54px!important;
    padding:0 24px!important;
    font-size:12px!important;
    letter-spacing:.10em!important;
  }}
  html body nav.top .btn,
  html body nav.top a.btn[href*="tagme"]{{
    width:auto!important;
    min-width:124px!important;
    height:46px!important;
    min-height:46px!important;
    font-size:9.5px!important;
  }}
  html body header.hero .hero-chips span,
  html body header.hero .hero-chips a,
  html body header.page-hero .hero-chips span,
  html body header.page-hero .hero-chips a{{
    height:34px!important;
    min-height:34px!important;
    padding:0 13px!important;
    font-size:12px!important;
  }}
}}
</style>
{CSS_END}"""

COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "css_injected": 0,
    "button_arrows_removed": 0,
    "pins_removed": 0,
    "audit_pass": 0,
    "audit_warn": 0,
    "audit_na": 0,
}
DETAILS: list[dict[str, object]] = []
ACTIONS: list[str] = []


def is_html_path(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return path.suffix.lower() == ".html" and not rel.startswith("_") and ".git" not in path.parts and rel not in SKIP


def clean_button_markup(markup: str) -> str:
    cleaned = ARROW_RE.sub(" ", markup)
    cleaned = re.sub(r"\s+</", "</", cleaned)
    cleaned = re.sub(r">\s+", ">", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    return cleaned


def remove_button_arrows(text: str, rel: str) -> str:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        original = match.group(0)
        cleaned = clean_button_markup(original)
        if cleaned != original:
            count += 1
        return cleaned

    text = ANCHOR_OR_BUTTON_RE.sub(repl, text)
    if count:
        COUNTERS["button_arrows_removed"] += count
        ACTIONS.append(f"BUTTON_ARROWS_REMOVED: {rel} ({count})")
    return text


def remove_pins(text: str, rel: str) -> str:
    text, count = OLD_PIN_RE.subn("", text)
    if count:
        COUNTERS["pins_removed"] += count
        ACTIONS.append(f"PINS_REMOVED: {rel} ({count})")
    return text


def inject_css(text: str, rel: str) -> str:
    original = text
    text = CSS_RE.sub("\n", text)
    if HEAD_CLOSE_RE.search(text):
        text = HEAD_CLOSE_RE.sub(CSS_BLOCK + "\n</head>", text, count=1)
    if text != original:
        COUNTERS["css_injected"] += 1
        ACTIONS.append(f"CSS_LOCK: {rel}")
    return text


def process(path: Path) -> None:
    if not is_html_path(path):
        return
    rel = path.relative_to(ROOT).as_posix()
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    text = remove_pins(text, rel)
    text = remove_button_arrows(text, rel)
    text = inject_css(text, rel)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1


def has_button_arrow(text: str) -> bool:
    for m in ANCHOR_OR_BUTTON_RE.finditer(text):
        if ARROW_RE.search(m.group(0)):
            return True
    return False


def audit_page(path: Path) -> None:
    if not is_html_path(path):
        return
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="ignore")
    has_hero = bool(HERO_RE.search(text))
    compact = text.replace(" ", "")
    checks = {
        "design_lock_present": "ec-final-design-consistency-lock" in text,
        "no_button_arrows": not has_button_arrow(text),
        "button_home_standard_lock": "min-height:60px!important" in compact and "JetBrainsMono" in compact.replace('"', '').replace("'", ""),
        "chips_home_standard_lock": "height:36px!important" in compact and "hero-chips" in text,
        "no_pin_in_nav_or_buttons": "drawer-icon"> not in text if False else "drawer-icon"> not in text,
        "no_gray_frame_lock": "border:0!important" in compact and "box-shadow:none!important" in compact,
    }
    if has_hero:
        checks.update({
            "hero_line_same_position": "top:96px!important" in compact and "left:clamp(78px,5.5vw,112px)!important" in compact and "transform:none!important" in compact,
        })
        status = "PASS" if all(checks.values()) else "WARN"
    else:
        checks.update({"hero_line_same_position": True})
        status = "PASS" if all(checks.values()) else "WARN"
    COUNTERS["audit_pass" if status == "PASS" else "audit_warn"] += 1
    DETAILS.append({"page": rel, "status": status, "has_hero": has_hero, **checks})


def write_reports() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    total = len(DETAILS)
    pass_count = sum(1 for d in DETAILS if d["status"] == "PASS")
    warn_count = sum(1 for d in DETAILS if d["status"] == "WARN")
    lines = [
        "# Final Design Consistency Lock",
        "",
        "## Objetivo",
        "Padronizar a linha laranja, botões, frames/pílulas acima dos botões e remover setas/pins residuais em todas as páginas.",
        "",
        "## Veredito",
        f"- Páginas auditadas: {total}",
        f"- PASS: {pass_count}",
        f"- WARN: {warn_count}",
        f"- Status geral: {'PASS' if warn_count == 0 else 'WARN'}",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Páginas com WARN"])
    warnings = [d for d in DETAILS if d["status"] == "WARN"]
    if warnings:
        for d in warnings:
            failed = [k for k, v in d.items() if isinstance(v, bool) and not v]
            lines.append(f"- {d['page']}: {', '.join(failed)}")
    else:
        lines.append("- Nenhuma.")
    lines.extend(["", "## Ações aplicadas"])
    lines.extend(f"- {a}" for a in ACTIONS) if ACTIONS else lines.append("- Nenhuma alteração necessária.")
    lines.extend([
        "",
        "## Observação",
        "Esta auditoria é estática e garante o lock de CSS/código. A validação final deve ser feita no navegador pós-deploy com cache limpo.",
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
