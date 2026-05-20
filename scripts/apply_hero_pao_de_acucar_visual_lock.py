#!/usr/bin/env python3
"""
Hero Pão de Açúcar Visual Lock — Embaixada Carioca

Objetivo visual solicitado:
- remover molduras/bordas cinzas que aparecem em algumas páginas;
- manter o espaço central da hero sempre livre para a pedra do Pão de Açúcar;
- posicionar o texto grande à direita da pedra;
- levar o texto menor das páginas internas para o frame lateral que começa com HOJE na home;
- padronizar a linha laranja em todas as páginas.

O script não altera conteúdo SEO. Ele cria um lock visual final e, nas páginas internas,
duplica o resumo curto no frame lateral, ocultando o parágrafo menor da área central.
"""
from __future__ import annotations

from pathlib import Path
import re
import html
import csv

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "hero_pao_de_acucar_visual_lock_report.md"
REPORT_CSV = REPORT_DIR / "hero_pao_de_acucar_visual_lock_details.csv"

CSS_START = "<!-- EC Hero Pao de Acucar Visual Lock -->"
CSS_END = "<!-- /EC Hero Pao de Acucar Visual Lock -->"
CSS_RE = re.compile(r"\n*<!-- EC Hero Pao de Acucar Visual Lock -->[\s\S]*?<!-- /EC Hero Pao de Acucar Visual Lock -->\s*", re.I)
HEAD_CLOSE_RE = re.compile(r"</head>", re.I)
BODY_LANG_RE = re.compile(r"<html\b[^>]*lang=[\"']([^\"']+)[\"']", re.I)
HERO_RE = re.compile(r"<header\b(?=[^>]*class=[\"'][^\"']*\bhero\b[^\"']*[\"'])[^>]*>[\s\S]*?</header>", re.I)
HERO_SUB_RE = re.compile(r"<p\b(?=[^>]*class=[\"'][^\"']*\bhero-sub\b[^\"']*[\"'])[^>]*>([\s\S]*?)</p>", re.I)
META_CARD_RE = re.compile(r"(<div\s+class=[\"']hero-meta-card[\"'][^>]*>)([\s\S]*?)(</div>\s*</aside>)", re.I)
SUMMARY_RE = re.compile(r"\n*<!-- EC Hero Summary In Side Frame -->[\s\S]*?<!-- /EC Hero Summary In Side Frame -->\s*", re.I)
HERO_EYEBROW_RE = re.compile(r'(<div\s+class=["\']eyebrow hero-eyebrow["\'][^>]*>)([\s\S]*?)(</div>)', re.I)

SKIP = {"404.html", "offline.html", "home-preview.html"}

LABELS = {
    "pt-BR": {
        "summary_label": "Resumo",
        "eyebrow": "Restaurante do Bondinho · Morro da Urca · Parque Bondinho Pão de Açúcar · Rio de Janeiro · Brasil",
    },
    "en": {
        "summary_label": "Summary",
        "eyebrow": "Restaurant at the Cable Car · Morro da Urca · Sugarloaf Cable Car Park · Rio de Janeiro · Brazil",
    },
    "es": {
        "summary_label": "Resumen",
        "eyebrow": "Restaurante del Bondinho · Morro da Urca · Parque Bondinho Pan de Azúcar · Río de Janeiro · Brasil",
    },
}

CSS_BLOCK = f"""{CSS_START}
<style id="ec-hero-pao-de-acucar-visual-lock">
/* HERO VISUAL LOCK — pedra do Pão de Açúcar livre no centro */
html,body{{background:#00202e!important;overflow-x:hidden!important;}}
header.hero,.hero,.page-hero,.hero-photo,.hero-overlay,.hero-content{{border:0!important;outline:0!important;box-shadow:none!important;}}
header.hero::before,header.hero::after,.hero::before,.hero::after{{box-shadow:none!important;}}

@media (min-width:961px){{
  html body header.hero{{
    --ec-hero-up-2cm:76px;
    --ec-hero-down-1cm:38px;
    --ec-hero-up-05cm:19px;
    --ec-hero-down-subtitle:38px;
    --ec-hero-eyebrow-left:clamp(185px,11.8vw,215px);
    min-height:100svh!important;
    position:relative!important;
    overflow:hidden!important;
    isolation:isolate!important;
    background:#00202e!important;
  }}
  html body header.hero img.hero-photo,
  html body header.hero .hero-photo{{
    position:absolute!important;inset:0!important;width:100%!important;height:100%!important;
    object-fit:cover!important;object-position:center 44%!important;z-index:-2!important;
    border:0!important;outline:0!important;box-shadow:none!important;
  }}
  html body header.hero .hero-overlay{{
    position:absolute!important;inset:0!important;z-index:-1!important;
    background:
      linear-gradient(90deg,
        rgba(0,32,46,.06) 0%,
        rgba(0,32,46,.08) 32%,
        rgba(0,32,46,.24) 48%,
        rgba(0,32,46,.62) 70%,
        rgba(0,32,46,.88) 100%),
      linear-gradient(180deg,
        rgba(0,32,46,.14) 0%,
        rgba(0,32,46,.18) 46%,
        rgba(0,32,46,.76) 100%)!important;
  }}
  html body header.hero .hero-content{{
    position:absolute!important;inset:0!important;z-index:3!important;display:block!important;
    width:100%!important;height:100%!important;max-width:none!important;margin:0!important;padding:0!important;
  }}
  html body header.hero .hero-content>div:first-child{{position:static!important;max-width:none!important;transform:none!important;}}

  /* Linha laranja: uma única posição para home e internas */
  html body header.hero .hero-content .eyebrow.hero-eyebrow{{
    position:absolute!important;
    left:var(--ec-hero-eyebrow-left)!important;
    top:calc(clamp(136px,16vh,172px) - var(--ec-hero-up-2cm) + var(--ec-hero-down-1cm) - var(--ec-hero-up-05cm))!important;
    transform:translate(37px,-6px)!important;
    width:calc(100vw - var(--ec-hero-eyebrow-left) - clamp(210px,16vw,300px))!important;
    max-width:none!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:clip!important;
    font-size:9px!important;letter-spacing:.31em!important;line-height:1!important;color:var(--amarelo,#f59b1e)!important;
    opacity:1!important;text-shadow:0 2px 12px rgba(0,32,46,.66)!important;z-index:10!important;
    margin:0!important;border:0!important;outline:0!important;
  }}
  html body header.hero .hero-content .eyebrow.hero-eyebrow::before{{
    width:32px!important;min-width:32px!important;height:2px!important;background:var(--amarelo,#f59b1e)!important;opacity:1!important;
  }}

  /* Título sempre à direita da pedra */
  html body header.hero h1{{
    position:absolute!important;right:clamp(66px,5.5vw,126px)!important;
    top:calc(clamp(205px,23vh,270px) - var(--ec-hero-up-2cm))!important;
    max-width:min(610px,39vw)!important;font-size:clamp(38px,4.35vw,70px)!important;
    line-height:.98!important;margin:0!important;text-wrap:balance!important;z-index:7!important;
    border:0!important;outline:0!important;box-shadow:none!important;
  }}

  /* Nas páginas internas, o texto pequeno sai do centro e fica no frame lateral */
  html body:not([data-screen-label="Home"]) header.hero .hero-sub{{
    display:none!important;
  }}
  html body[data-screen-label="Home"] header.hero .hero-sub{{
    position:absolute!important;right:clamp(66px,5.5vw,126px)!important;
    top:calc(clamp(520px,58vh,625px) - var(--ec-hero-up-2cm) + var(--ec-hero-down-subtitle))!important;
    max-width:min(610px,40vw)!important;font-size:clamp(15px,1vw,18px)!important;line-height:1.55!important;margin:0!important;color:rgba(246,239,222,.95)!important;z-index:7!important;
  }}

  html body header.hero .hero-chips{{
    position:absolute!important;left:clamp(70px,5.5vw,118px)!important;
    bottom:calc(clamp(132px,15.8vh,172px) + var(--ec-hero-up-2cm))!important;
    max-width:min(760px,56vw)!important;margin:0!important;gap:8px!important;z-index:8!important;
    display:flex!important;flex-wrap:wrap!important;align-items:center!important;
  }}
  html body header.hero .hero-chips span{{font-size:.82rem!important;padding:5px 13px!important;background:rgba(0,32,46,.42)!important;border-color:rgba(246,239,222,.28)!important;}}
  html body header.hero .hero-ctas{{
    position:absolute!important;left:clamp(70px,5.5vw,118px)!important;
    bottom:calc(clamp(54px,7.2vh,82px) + var(--ec-hero-up-2cm))!important;
    max-width:min(900px,62vw)!important;gap:12px!important;z-index:8!important;
  }}

  html body header.hero aside.hero-side{{
    position:absolute!important;inset:0!important;z-index:6!important;max-width:none!important;width:100%!important;height:100%!important;
    display:block!important;pointer-events:none!important;transform:none!important;padding:0!important;margin:0!important;
  }}
  html body header.hero aside.hero-side .hero-meta-card{{
    position:absolute!important;left:clamp(38px,3vw,70px)!important;top:auto!important;
    bottom:calc(clamp(246px,28.5vh,315px) + var(--ec-hero-up-2cm))!important;
    width:min(214px,15vw)!important;min-height:clamp(310px,38vh,390px)!important;
    display:flex!important;flex-direction:column!important;justify-content:space-between!important;
    padding:18px 16px!important;border-radius:16px!important;background:rgba(0,32,46,.55)!important;
    border:1px solid rgba(245,155,30,.24)!important;box-shadow:0 16px 40px rgba(0,0,0,.22)!important;
    backdrop-filter:blur(8px)!important;-webkit-backdrop-filter:blur(8px)!important;z-index:8!important;overflow:hidden!important;
  }}
  html body header.hero aside.hero-side .hero-meta-card .hmc{{display:block!important;padding:8px 0!important;}}
  html body header.hero aside.hero-side .hero-meta-card .hmc .l{{display:block!important;width:100%!important;font-size:8px!important;letter-spacing:.30em!important;line-height:1!important;margin:0 0 10px!important;white-space:nowrap!important;color:var(--amarelo,#f59b1e)!important;}}
  html body header.hero aside.hero-side .hero-meta-card .hmc .v{{display:block!important;width:100%!important;font-size:13px!important;line-height:1.30!important;margin:0!important;white-space:normal!important;color:var(--areia-pale,#f6efde)!important;}}
  html body:not([data-screen-label="Home"]) header.hero aside.hero-side .hero-meta-card .hmc.hero-summary-card .v{{font-size:12.2px!important;line-height:1.26!important;}}

  html body header.hero aside.hero-side img.hero-logo{{
    position:absolute!important;left:72vw!important;top:auto!important;right:auto!important;
    bottom:calc(clamp(54px,7.2vh,82px) + var(--ec-hero-up-2cm) - 46px)!important;
    transform:translateX(-50%)!important;width:clamp(140px,10vw,166px)!important;height:clamp(140px,10vw,166px)!important;
    opacity:.80!important;z-index:6!important;filter:drop-shadow(0 14px 34px rgba(0,32,46,.58))!important;pointer-events:none!important;
  }}
  html body header.hero .hero-bottom-bar{{
    background:rgba(0,32,46,.58)!important;backdrop-filter:blur(8px)!important;-webkit-backdrop-filter:blur(8px)!important;z-index:9!important;
    border-top:1px solid rgba(245,155,30,.30)!important;box-shadow:none!important;outline:0!important;
  }}
}}

@media (max-width:960px){{
  html body header.hero{{border:0!important;outline:0!important;box-shadow:none!important;}}
  html body header.hero aside.hero-side{{display:none!important;}}
  html body header.hero .hero-content{{position:relative!important;display:grid!important;grid-template-columns:1fr!important;}}
  html body header.hero .hero-content .eyebrow.hero-eyebrow,
  html body header.hero h1,
  html body header.hero .hero-sub,
  html body header.hero .hero-chips,
  html body header.hero .hero-ctas{{position:static!important;white-space:normal!important;width:auto!important;}}
}}
</style>
{CSS_END}"""

COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "css_injected": 0,
    "eyebrow_synced": 0,
    "summary_cards_inserted": 0,
    "audit_pass": 0,
    "audit_warn": 0,
}
DETAILS: list[dict[str, object]] = []
ACTIONS: list[str] = []


def lang_for(rel: str, text: str) -> str:
    m = BODY_LANG_RE.search(text)
    if m:
        val = m.group(1).lower()
        if val.startswith("en"):
            return "en"
        if val.startswith("es"):
            return "es"
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt-BR"


def visible_text(raw: str) -> str:
    txt = re.sub(r"<[^>]+>", " ", raw)
    txt = html.unescape(txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt


def short_summary(text: str, max_chars: int = 170) -> str:
    text = visible_text(text)
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars].rsplit(" ", 1)[0].rstrip(".,;: ")
    return cut + "…"


def sync_eyebrow(text: str, lang: str) -> str:
    def repl(match: re.Match[str]) -> str:
        COUNTERS["eyebrow_synced"] += 1
        return match.group(1) + LABELS[lang]["eyebrow"] + match.group(3)
    return HERO_EYEBROW_RE.sub(repl, text, count=1)


def add_summary_to_side_frame(text: str, rel: str, lang: str) -> str:
    if rel == "index.html" or rel in {"en/index.html", "es/index.html"}:
        return text
    sub = HERO_SUB_RE.search(text)
    if not sub:
        return text
    summary = short_summary(sub.group(1))
    if not summary:
        return text
    text = SUMMARY_RE.sub("\n", text)
    block = f'''\n<!-- EC Hero Summary In Side Frame -->\n<div class="hmc hero-summary-card"><span class="l">{LABELS[lang]['summary_label']}</span><span class="v">{html.escape(summary)}</span></div>\n<!-- /EC Hero Summary In Side Frame -->\n'''

    def repl(match: re.Match[str]) -> str:
        COUNTERS["summary_cards_inserted"] += 1
        return match.group(1) + match.group(2).rstrip() + block + match.group(3)

    new_text, count = META_CARD_RE.subn(repl, text, count=1)
    if count:
        ACTIONS.append(f"SUMMARY_TO_SIDE_FRAME: {rel}")
        return new_text
    return text


def process(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix != ".html" or rel.startswith("_") or ".git" in path.parts or rel in SKIP:
        return
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    lang = lang_for(rel, original)
    text = original
    text = CSS_RE.sub("\n", text)
    if HEAD_CLOSE_RE.search(text):
        text = HEAD_CLOSE_RE.sub(CSS_BLOCK + "\n</head>", text, count=1)
        COUNTERS["css_injected"] += 1
    text = sync_eyebrow(text, lang)
    text = add_summary_to_side_frame(text, rel, lang)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1
        ACTIONS.append(f"UPDATED: {rel}")


def audit_page(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix != ".html" or rel.startswith("_") or ".git" in path.parts or rel in SKIP:
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    has_hero = bool(HERO_RE.search(text)) or "class=\"hero" in text or "class='hero" in text
    checks = {
        "hero_present": has_hero,
        "visual_lock_present": "ec-hero-pao-de-acucar-visual-lock" in text,
        "no_gray_frame_lock": "border:0!important;outline:0!important;box-shadow:none!important" in text.replace(" ", ""),
        "eyebrow_lock": "transform:translate(37px,-6px)" in text.replace(" ", ""),
        "title_right_lock": "right:clamp(66px,5.5vw,126px)" in text.replace(" ", ""),
        "internal_summary_side_frame": (rel in {"index.html","en/index.html","es/index.html"}) or ("hero-summary-card" in text) or (not has_hero),
    }
    status = "PASS" if all(checks.values()) else "WARN"
    COUNTERS["audit_pass" if status == "PASS" else "audit_warn"] += 1
    DETAILS.append({"page": rel, "status": status, **checks})


def write_reports() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    pages = len(DETAILS)
    pass_count = sum(1 for d in DETAILS if d["status"] == "PASS")
    warn_count = pages - pass_count
    lines = [
        "# Hero Pão de Açúcar Visual Lock",
        "",
        "## Objetivo",
        "Garantir que a pedra do Pão de Açúcar fique livre no espaço central da hero, com o texto grande à direita, o texto menor das páginas internas no frame lateral e a linha laranja igual em todas as páginas.",
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
    lines.extend(["", "## Páginas com WARN"])
    warns = [d for d in DETAILS if d["status"] != "PASS"]
    if warns:
        for d in warns:
            failed = [k for k, v in d.items() if isinstance(v, bool) and not v]
            lines.append(f"- {d['page']}: {', '.join(failed)}")
    else:
        lines.append("- Nenhuma.")
    lines.extend([
        "",
        "## Ações aplicadas",
    ])
    lines.extend(f"- {a}" for a in ACTIONS) if ACTIONS else lines.append("- Nenhuma alteração necessária.")
    lines.extend([
        "",
        "## Observação",
        "Esta auditoria garante o lock de CSS/estrutura no repositório. A validação final de pixel depende do navegador pós-deploy com cache limpo.",
        "",
    ])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    with REPORT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(DETAILS[0].keys()) if DETAILS else ["page"])
        writer.writeheader(); writer.writerows(DETAILS)
    print(REPORT_MD.read_text(encoding="utf-8"))


def main() -> int:
    for p in sorted(ROOT.rglob("*.html")):
        process(p)
    for p in sorted(ROOT.rglob("*.html")):
        audit_page(p)
    write_reports()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
