#!/usr/bin/env python3
"""Visual Readability Reality Fix — Embaixada Carioca.

Correção motivada por validação visual real:
- Títulos dos pratos no cardápio estavam claros demais sobre fundo areia.
- Algumas páginas ainda tinham baixo contraste por herança de CSS e -webkit-text-fill-color.
- Havia declarações rgba inválidas geradas por substituições anteriores.

Este script injeta um CSS/JS final, no fim do body, para vencer a cascata.
"""
from __future__ import annotations

from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "visual_readability_reality_fix_report.md"
REPORT_CSV = REPORT_DIR / "visual_readability_reality_fix_details.csv"

START = "<!-- EC Visual Readability Reality Fix -->"
END = "<!-- /EC Visual Readability Reality Fix -->"
BLOCK_RE = re.compile(r"\n*<!-- EC Visual Readability Reality Fix -->[\s\S]*?<!-- /EC Visual Readability Reality Fix -->\s*", re.I)
BODY_RE = re.compile(r"</body>", re.I)
HEAD_RE = re.compile(r"</head>", re.I)
SKIP = {"404.html", "offline.html", "home-preview.html"}

INVALID_REPLACEMENTS = {
    "rgba(237.779,201,": "rgba(237,226,201,",
    "rgba(245,237.779,0.82)": "rgba(245,237,229,0.82)",
    "rgba(37.779,102,": "rgba(37,211,102,",
}

FIX_BLOCK = START + r'''
<style id="ec-visual-readability-reality-fix">
/* VISUAL REALITY FIX — correção final de contraste observada no navegador.
   Regra crítica: card claro = texto escuro. Cardápio = nome do prato em verde escuro. */
:root{--ec-vr-blue:#00405a;--ec-vr-green:#335d4a;--ec-vr-yellow:#f59b1e;--ec-vr-sand:#ede2c9;--ec-vr-paper:#f6efde;--ec-vr-gray:#485156;--ec-vr-gray2:#6b7377;--ec-vr-price:#9a6500;}

/* Reset seguro: impede texto fantasma causado por text-fill e sombras */
html body main :is(.menu-item,.menu-card,.dish-card,.card,.box,.guide-card,.place-card,.beach-card,.route-card,.access-card,.access-fact,.access-route,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details) *{text-shadow:none!important;opacity:1!important;-webkit-text-fill-color:currentColor!important;}

/* CARDÁPIO — prioridade máxima */
html body main .menu-section .menu-item,
html body main .menu-grid .menu-item,
html body main .menu-item{background:var(--ec-vr-sand)!important;color:var(--ec-vr-gray)!important;border-color:rgba(0,64,90,.16)!important;}
html body main .menu-section .menu-item :is(h1,h2,h3,h4,.menu-item-name,.item-name,.dish-name,.title,.card-title),
html body main .menu-grid .menu-item :is(h1,h2,h3,h4,.menu-item-name,.item-name,.dish-name,.title,.card-title),
html body main .menu-item :is(h1,h2,h3,h4,.menu-item-name,.item-name,.dish-name,.title,.card-title){color:var(--ec-vr-green)!important;-webkit-text-fill-color:var(--ec-vr-green)!important;font-weight:800!important;text-shadow:none!important;opacity:1!important;}
html body main .menu-section .menu-item.featured :is(h1,h2,h3,h4,.menu-item-name,.item-name,.dish-name,.title,.card-title),
html body main .menu-item.featured :is(h1,h2,h3,h4,.menu-item-name,.item-name,.dish-name,.title,.card-title){color:var(--ec-vr-green)!important;-webkit-text-fill-color:var(--ec-vr-green)!important;}
html body main .menu-section .menu-item :is(p,li,span,small,.menu-item-desc,.item-desc,.description,.copy),
html body main .menu-grid .menu-item :is(p,li,span,small,.menu-item-desc,.item-desc,.description,.copy),
html body main .menu-item :is(p,li,span,small,.menu-item-desc,.item-desc,.description,.copy){color:var(--ec-vr-gray)!important;-webkit-text-fill-color:var(--ec-vr-gray)!important;text-shadow:none!important;opacity:1!important;}
html body main .menu-section .menu-item :is(.price,.menu-item-price,.item-price),
html body main .menu-grid .menu-item :is(.price,.menu-item-price,.item-price),
html body main .menu-item :is(.price,.menu-item-price,.item-price){color:var(--ec-vr-price)!important;-webkit-text-fill-color:var(--ec-vr-price)!important;font-weight:900!important;}
html body main .menu-section .menu-item :is(.tag,.badge,.kicker),
html body main .menu-item :is(.tag,.badge,.kicker){color:var(--ec-vr-blue)!important;-webkit-text-fill-color:var(--ec-vr-blue)!important;text-shadow:none!important;}
html body main .menu-section .menu-item :is(.tag.win,.badge.win,.premiada,.premiado),
html body main .menu-item :is(.tag.win,.badge.win,.premiada,.premiado){background:var(--ec-vr-yellow)!important;color:var(--ec-vr-blue)!important;-webkit-text-fill-color:var(--ec-vr-blue)!important;}

/* Cards claros de conteúdo — leitura obrigatória */
html body main :is(.card,.box,.guide-card,.place-card,.beach-card,.route-card,.access-card,.access-fact,.access-route,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details){background-color:var(--ec-vr-paper)!important;color:var(--ec-vr-gray)!important;border-color:rgba(0,64,90,.14)!important;}
html body main :is(.card,.box,.guide-card,.place-card,.beach-card,.route-card,.access-card,.access-fact,.access-route,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details) :is(h1,h2,h3,h4,h5,h6,.title,.card-title){color:var(--ec-vr-blue)!important;-webkit-text-fill-color:var(--ec-vr-blue)!important;font-weight:800!important;}
html body main :is(.card,.box,.guide-card,.place-card,.beach-card,.route-card,.access-card,.access-fact,.access-route,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details) :is(p,li,span,small,dd,dt,summary,.copy,.description){color:var(--ec-vr-gray)!important;-webkit-text-fill-color:var(--ec-vr-gray)!important;}
html body main :is(.card,.box,.guide-card,.place-card,.beach-card,.route-card,.access-card,.access-fact,.access-route,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details) :is(strong,b){color:var(--ec-vr-green)!important;-webkit-text-fill-color:var(--ec-vr-green)!important;}
html body main :is(.card,.box,.guide-card,.place-card,.beach-card,.route-card,.access-card,.access-fact,.access-route,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details) a:not(.btn):not(.btn-secondary){color:#b76f00!important;-webkit-text-fill-color:#b76f00!important;}

/* Áreas escuras sem card: texto claro e sem opacidade baixa */
html body main section:not(.menu-section):not(.gallery-section):not(.light-section):not(.paper-section):not(.section-paper):not(.bg-paper):not(.ec-final-geo-answer) :is(p,li,span,small,dd,dt,.lede,.copy,.description){color:rgba(246,239,222,.88)!important;-webkit-text-fill-color:rgba(246,239,222,.88)!important;opacity:1!important;}
html body main section:not(.menu-section):not(.gallery-section):not(.light-section):not(.paper-section):not(.section-paper):not(.bg-paper):not(.ec-final-geo-answer) :is(h1,h2,h3,h4,h5,h6){color:var(--ec-vr-paper)!important;-webkit-text-fill-color:var(--ec-vr-paper)!important;opacity:1!important;}

/* Galerias/captions em fundo branco */
html body main .gallery-section :is(figure,figcaption,.caption){background:#fff!important;color:var(--ec-vr-gray)!important;-webkit-text-fill-color:var(--ec-vr-gray)!important;}

/* Botões mantêm hierarquia */
html body main a.btn[href*="tagme"],html body main a.btn[href*="reserv"],nav.top a.btn[href*="tagme"]{background:var(--ec-vr-yellow)!important;border-color:var(--ec-vr-yellow)!important;color:var(--ec-vr-blue)!important;-webkit-text-fill-color:var(--ec-vr-blue)!important;}
</style>
<script id="ec-visual-readability-reality-js">
(function(){
  function setImportant(el, prop, val){ if(el && el.style) el.style.setProperty(prop, val, 'important'); }
  function fixMenu(){
    document.querySelectorAll('main .menu-item h1, main .menu-item h2, main .menu-item h3, main .menu-item h4, main .menu-item .menu-item-name, main .menu-item .item-name, main .menu-item .dish-name, main .menu-item .title, main .menu-item .card-title').forEach(function(el){
      setImportant(el,'color','#335d4a');
      setImportant(el,'-webkit-text-fill-color','#335d4a');
      setImportant(el,'text-shadow','none');
      setImportant(el,'opacity','1');
      setImportant(el,'font-weight','800');
    });
    document.querySelectorAll('main .menu-item p, main .menu-item .menu-item-desc, main .menu-item .item-desc, main .menu-item .description, main .menu-item small').forEach(function(el){
      setImportant(el,'color','#485156');
      setImportant(el,'-webkit-text-fill-color','#485156');
      setImportant(el,'text-shadow','none');
      setImportant(el,'opacity','1');
    });
    document.querySelectorAll('main .menu-item .price, main .menu-item .menu-item-price, main .menu-item .item-price').forEach(function(el){
      setImportant(el,'color','#9a6500');
      setImportant(el,'-webkit-text-fill-color','#9a6500');
      setImportant(el,'font-weight','900');
    });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fixMenu, {once:true}); else fixMenu();
  window.addEventListener('load', fixMenu, {once:true});
})();
</script>
''' + END

COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "css_js_injected": 0,
    "invalid_rgba_fixed": 0,
    "audit_pass": 0,
    "audit_warn": 0,
}
DETAILS: list[dict[str, object]] = []


def is_html(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return path.suffix.lower() == ".html" and not rel.startswith("_") and ".git" not in path.parts and rel not in SKIP


def normalize_invalid_rgba(text: str, rel: str) -> str:
    total = 0
    for bad, good in INVALID_REPLACEMENTS.items():
        text, count = text.replace(bad, good), text.count(bad)
        total += count
    # Fallback para variações comuns com ponto indevido em rgba.
    text2 = re.sub(r"rgba\(237\.779,201,", "rgba(237,226,201,", text)
    if text2 != text:
        total += 1
        text = text2
    if total:
        COUNTERS["invalid_rgba_fixed"] += total
        DETAILS.append({"page": rel, "status": "FIXED", "action": "invalid_rgba_fixed", "count": total})
    return text


def inject_block(text: str, rel: str) -> str:
    before = text
    text = BLOCK_RE.sub("\n", text)
    if BODY_RE.search(text):
        text = BODY_RE.sub(FIX_BLOCK + "\n</body>", text, count=1)
    elif HEAD_RE.search(text):
        text = HEAD_RE.sub(FIX_BLOCK + "\n</head>", text, count=1)
    if text != before:
        COUNTERS["css_js_injected"] += 1
    return text


def process(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = normalize_invalid_rgba(original, rel)
    text = inject_block(text, rel)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1


def audit(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="ignore")
    compact = text.replace(" ", "").lower()
    is_menu = rel.endswith("cardapio.html") or rel.endswith("menu.html") or "cardapio" in rel or "menu" in rel
    checks = {
        "reality_fix_present": "ec-visual-readability-reality-fix" in text,
        "menu_titles_dark_green_rule": "color:var(--ec-vr-green)!important" in compact and "#335d4a" in compact,
        "menu_js_guard_present": "ec-visual-readability-reality-js" in text,
        "light_card_dark_text_rule": "--ec-vr-gray:#485156" in compact and "--ec-vr-blue:#00405a" in compact,
        "invalid_rgba_clean": ".779" not in text,
        "menu_page_guard": (not is_menu) or ("main .menu-item h1" in text and "#335d4a" in text),
    }
    status = "PASS" if all(checks.values()) else "WARN"
    COUNTERS["audit_pass" if status == "PASS" else "audit_warn"] += 1
    DETAILS.append({"page": rel, "status": status, **checks})


def write_reports() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    warn = [d for d in DETAILS if d.get("status") == "WARN"]
    lines = [
        "# Visual Readability Reality Fix",
        "",
        "## Objetivo",
        "Corrigir problemas visuais reais de contraste, especialmente o cardápio com títulos de pratos claros sobre fundo areia.",
        "",
        "## Decisão visual",
        "- Nome dos pratos no cardápio: verde escuro oficial `#335d4a`.",
        "- Descrição dos pratos e cards claros: cinza escuro `#485156`.",
        "- Preços: dourado escuro `#9a6500`.",
        "- Fundo escuro: texto areia claro com opacidade alta.",
        "",
        "## Veredito",
        f"- Páginas auditadas: {COUNTERS['html_scanned']}",
        f"- PASS: {COUNTERS['audit_pass']}",
        f"- WARN: {COUNTERS['audit_warn']}",
        f"- Status geral: {'PASS' if not warn else 'WARN'}",
        "",
        "## Contadores",
    ]
    lines.extend(f"- {k}: {v}" for k, v in COUNTERS.items())
    lines.extend(["", "## Páginas com WARN"])
    if warn:
        for d in warn:
            failed = [k for k, v in d.items() if isinstance(v, bool) and not v]
            lines.append(f"- {d['page']}: {', '.join(failed)}")
    else:
        lines.append("- Nenhuma.")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    with REPORT_CSV.open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(DETAILS[0].keys()) if DETAILS else ["page"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader(); writer.writerows(DETAILS)
    print(REPORT_MD.read_text(encoding="utf-8"))


def main() -> int:
    for p in sorted(ROOT.rglob("*.html")):
        if is_html(p):
            process(p)
    for p in sorted(ROOT.rglob("*.html")):
        if is_html(p):
            audit(p)
    write_reports()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
