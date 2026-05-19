#!/usr/bin/env python3
"""
Final Subpage Home Header Override — Embaixada Carioca.

Objetivo:
- aplicar uma camada final de CSS depois de todos os outros ajustes;
- fazer as subpáginas seguirem o topo da home;
- corrigir cardápio e demais páginas em larguras intermediárias;
- manter a pedra do Pão de Açúcar sem texto por cima;
- eliminar moldura/overflow horizontal.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE_ID = "subpage-home-top-final-override"
STYLE_RE = re.compile(rf"\n*<style id=[\"']{STYLE_ID}[\"']>[\s\S]*?</style>\s*", re.IGNORECASE)
EYEBROW_RE = re.compile(r'(<div\s+class=["\']eyebrow hero-eyebrow["\'][^>]*>)([\s\S]*?)(</div>)', re.IGNORECASE)

EXCLUDED = {
    "index.html",
    "home-preview.html",
    "offline.html",
    "404.html",
}

FINAL_OVERRIDE = r'''
<style id="subpage-home-top-final-override">
/* FINAL OVERRIDE — subpáginas com topo da home e pedra livre */
html,body{margin:0!important;padding:0!important;overflow-x:hidden!important;background:#00202e!important;}
body[data-screen-label]{overflow-x:hidden!important;max-width:100vw!important;background:#00202e!important;}
body[data-screen-label] nav.top,
body[data-screen-label] header.page-hero,
body[data-screen-label] .page-hero{width:100%!important;max-width:100vw!important;margin:0!important;left:0!important;right:0!important;overflow:hidden!important;}
body[data-screen-label] nav.top,body[data-screen-label] nav.top *{box-sizing:border-box!important;}

@media (min-width:961px){
  body[data-screen-label] nav.top:not(.scrolled){
    height:112px!important;min-height:112px!important;
    background:linear-gradient(180deg,rgba(0,32,46,.40) 0%,rgba(0,32,46,.24) 58%,rgba(0,32,46,0) 100%)!important;
    border:0!important;box-shadow:none!important;backdrop-filter:none!important;-webkit-backdrop-filter:none!important;
  }
  body[data-screen-label] nav.top .nav-inner{
    width:100%!important;max-width:100%!important;height:82px!important;margin:0!important;
    padding:10px 70px 0!important;display:grid!important;
    grid-template-columns:140px minmax(0,1fr) 205px 94px 188px!important;
    column-gap:26px!important;align-items:center!important;justify-content:normal!important;color:var(--areia-pale,#f6efde)!important;
  }
  body[data-screen-label] nav.top .brand-mark{grid-column:1!important;width:140px!important;min-width:0!important;display:flex!important;align-items:center!important;justify-content:flex-start!important;gap:0!important;flex:initial!important;color:inherit!important;text-decoration:none!important;}
  body[data-screen-label] nav.top .brand-logo{width:68px!important;height:68px!important;object-fit:contain!important;}
  body[data-screen-label] nav.top .brand-logo.light{display:block!important;}body[data-screen-label] nav.top .brand-logo.dark{display:none!important;}body[data-screen-label] nav.top .brand-word{display:none!important;}

  body[data-screen-label] nav.top .nav-links{grid-column:2!important;display:flex!important;align-items:center!important;justify-content:flex-start!important;gap:30px!important;min-width:0!important;width:auto!important;margin:0!important;padding:0!important;list-style:none!important;overflow:hidden!important;}
  body[data-screen-label] nav.top .nav-links a,body[data-screen-label] nav.top .nav-links a:link,body[data-screen-label] nav.top .nav-links a:visited{
    font-family:"JetBrains Mono",ui-monospace,monospace!important;font-size:12px!important;line-height:1!important;letter-spacing:.145em!important;font-weight:800!important;text-transform:uppercase!important;color:rgba(246,239,222,.94)!important;opacity:1!important;text-decoration:none!important;white-space:nowrap!important;padding:6px 0!important;
  }
  body[data-screen-label] nav.top .nav-links a::after{bottom:-13px!important;height:2px!important;background:var(--amarelo,#f59b1e)!important;}
  body[data-screen-label] nav.top .nav-wa-btn{display:none!important;}

  body[data-screen-label] nav.top .nav-rating-badge,body[data-screen-label] nav.top .nav-rating-badge:link,body[data-screen-label] nav.top .nav-rating-badge:visited{
    grid-column:3!important;width:205px!important;min-width:0!important;height:35px!important;margin:0!important;padding:0 16px!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:7px!important;border-radius:999px!important;background:rgba(246,239,222,.14)!important;border:1px solid rgba(246,239,222,.30)!important;color:var(--areia-pale,#f6efde)!important;text-decoration:none!important;overflow:hidden!important;box-shadow:0 8px 22px rgba(0,32,46,.12)!important;
  }
  body[data-screen-label] nav.top .nav-rating-stars{color:var(--amarelo,#f59b1e)!important;font-size:15px!important;font-weight:900!important;letter-spacing:.01em!important;white-space:nowrap!important;}
  body[data-screen-label] nav.top .nav-rating-count{color:rgba(246,239,222,.78)!important;font-size:11px!important;font-weight:800!important;letter-spacing:.08em!important;white-space:nowrap!important;}
  body[data-screen-label] nav.top .lang-switcher{grid-column:4!important;width:94px!important;min-width:0!important;margin:0!important;display:block!important;flex:initial!important;}
  body[data-screen-label] nav.top .lang-current{width:94px!important;height:36px!important;padding:0 12px!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:6px!important;border-radius:12px!important;background:rgba(246,239,222,.14)!important;border:1px solid rgba(246,239,222,.30)!important;color:var(--areia-pale,#f6efde)!important;font-family:"JetBrains Mono",ui-monospace,monospace!important;font-size:12px!important;font-weight:900!important;letter-spacing:.06em!important;white-space:nowrap!important;}
  body[data-screen-label] nav.top .lang-current span{color:inherit!important;}
  body[data-screen-label] nav.top .btn,body[data-screen-label] nav.top .btn:link,body[data-screen-label] nav.top .btn:visited{grid-column:5!important;width:188px!important;min-width:0!important;height:60px!important;min-height:0!important;padding:0!important;margin:0!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;border-radius:999px!important;background:var(--amarelo,#f59b1e)!important;border:1px solid var(--amarelo,#f59b1e)!important;color:#fff!important;font-family:"JetBrains Mono",ui-monospace,monospace!important;font-size:14px!important;line-height:1!important;font-weight:900!important;letter-spacing:.16em!important;text-transform:uppercase!important;text-decoration:none!important;box-shadow:none!important;overflow:hidden!important;}
  body[data-screen-label] nav.top .nav-hamburger{display:none!important;}

  /* Herói das subpáginas: central livre para a pedra */
  body[data-screen-label] .page-hero{height:100svh!important;min-height:100svh!important;padding:0!important;display:block!important;position:relative!important;overflow:hidden!important;isolation:isolate!important;}
  body[data-screen-label] .page-hero-photo,body[data-screen-label] picture.page-hero-photo,body[data-screen-label] picture.page-hero-photo img{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;object-fit:cover!important;object-position:center 44%!important;z-index:-2!important;}
  body[data-screen-label] .page-hero-overlay{position:absolute!important;inset:0!important;z-index:-1!important;background:linear-gradient(90deg,rgba(0,32,46,.08) 0%,rgba(0,32,46,.10) 35%,rgba(0,32,46,.38) 57%,rgba(0,32,46,.82) 100%),linear-gradient(180deg,rgba(0,32,46,.10) 0%,rgba(0,32,46,.18) 45%,rgba(0,32,46,.78) 100%)!important;}
  body[data-screen-label] .page-hero-content{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;max-width:none!important;margin:0!important;padding:0!important;z-index:2!important;}
  body[data-screen-label] .page-hero-content .crumbs{display:none!important;}
  body[data-screen-label] .page-hero-content .eyebrow.hero-eyebrow{position:absolute!important;left:clamp(185px,11.8vw,215px)!important;top:calc(clamp(136px,16vh,172px) - 76px + 38px - 19px)!important;width:calc(100vw - clamp(185px,11.8vw,215px) - clamp(210px,16vw,300px))!important;max-width:none!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:clip!important;font-family:"JetBrains Mono",ui-monospace,monospace!important;font-size:9px!important;line-height:1!important;letter-spacing:.31em!important;font-weight:500!important;text-transform:uppercase!important;color:var(--amarelo,#f59b1e)!important;opacity:1!important;margin:0!important;text-shadow:0 2px 12px rgba(0,32,46,.66)!important;z-index:10!important;}
  body[data-screen-label] .page-hero-content .eyebrow.hero-eyebrow::before{width:32px!important;min-width:32px!important;height:1px!important;margin-right:18px!important;background:var(--amarelo,#f59b1e)!important;opacity:1!important;}
  body[data-screen-label] .page-hero-content h1{position:absolute!important;right:clamp(66px,5.5vw,126px)!important;top:calc(clamp(205px,23vh,270px) - 76px)!important;max-width:min(610px,39vw)!important;margin:0!important;font-family:"Catamaran",system-ui,sans-serif!important;font-size:clamp(38px,4.35vw,70px)!important;line-height:.98!important;letter-spacing:-.026em!important;font-weight:200!important;color:var(--areia-pale,#f6efde)!important;text-wrap:balance!important;z-index:7!important;}
  body[data-screen-label] .page-hero-content h1 .serif{font-family:"Cormorant Garamond",Georgia,serif!important;font-style:italic!important;font-weight:500!important;color:var(--amarelo,#f59b1e)!important;}
  body[data-screen-label] .page-hero-content .lede,body[data-screen-label] .page-hero-content p.lede{position:absolute!important;right:clamp(66px,5.5vw,126px)!important;top:calc(clamp(520px,58vh,625px) - 76px + 38px)!important;max-width:min(610px,40vw)!important;margin:0!important;font-size:clamp(15px,1vw,18px)!important;line-height:1.55!important;font-weight:400!important;color:rgba(246,239,222,.95)!important;text-shadow:0 2px 16px rgba(0,32,46,.55)!important;z-index:7!important;}
  body[data-screen-label] .page-hero-content .hero-chips{position:absolute!important;left:clamp(70px,5.5vw,118px)!important;bottom:calc(clamp(132px,15.8vh,172px) + 76px)!important;max-width:min(760px,56vw)!important;margin:0!important;gap:8px!important;display:flex!important;flex-wrap:wrap!important;align-items:center!important;z-index:8!important;}
  body[data-screen-label] .page-hero-content .hero-chips span{font-size:.82rem!important;padding:5px 13px!important;background:rgba(0,32,46,.42)!important;border:1px solid rgba(246,239,222,.28)!important;color:var(--areia-pale,#f6efde)!important;border-radius:999px!important;}
  body[data-screen-label] .page-hero-content .ctas,body[data-screen-label] .page-hero-content .hero-ctas{position:absolute!important;left:clamp(70px,5.5vw,118px)!important;bottom:calc(clamp(54px,7.2vh,82px) + 76px)!important;max-width:min(900px,62vw)!important;display:flex!important;flex-wrap:wrap!important;align-items:center!important;gap:12px!important;margin:0!important;z-index:8!important;}
}

/* Larguras intermediárias: caber tudo sem cortar rating/idioma/botão */
@media (min-width:961px) and (max-width:1180px){
  body[data-screen-label] nav.top .nav-inner{padding-left:18px!important;padding-right:18px!important;grid-template-columns:68px minmax(0,1fr) 132px 62px 124px!important;column-gap:8px!important;}
  body[data-screen-label] nav.top .brand-mark{width:68px!important;}
  body[data-screen-label] nav.top .brand-logo{width:54px!important;height:54px!important;}
  body[data-screen-label] nav.top .nav-links{gap:8px!important;overflow:hidden!important;}
  body[data-screen-label] nav.top .nav-links a{font-size:7.6px!important;letter-spacing:.035em!important;font-weight:900!important;}
  body[data-screen-label] nav.top .nav-rating-badge{width:132px!important;height:32px!important;padding:0 7px!important;gap:3px!important;}
  body[data-screen-label] nav.top .nav-rating-stars{font-size:11px!important;}
  body[data-screen-label] nav.top .nav-rating-count{font-size:7.6px!important;letter-spacing:.02em!important;}
  body[data-screen-label] nav.top .lang-switcher,body[data-screen-label] nav.top .lang-current{width:62px!important;}
  body[data-screen-label] nav.top .lang-current{height:32px!important;font-size:9px!important;padding:0 6px!important;gap:3px!important;}
  body[data-screen-label] nav.top .btn{width:124px!important;height:46px!important;font-size:9.3px!important;letter-spacing:.07em!important;}
  body[data-screen-label] .page-hero-content .eyebrow.hero-eyebrow{left:120px!important;right:150px!important;font-size:7.6px!important;letter-spacing:.18em!important;top:96px!important;}
  body[data-screen-label] .page-hero-content h1,body[data-screen-label] .page-hero-content .lede{display:none!important;}
}

@media (min-width:1181px) and (max-width:1460px){
  body[data-screen-label] nav.top .nav-inner{padding-left:34px!important;padding-right:34px!important;grid-template-columns:108px minmax(0,1fr) 188px 84px 174px!important;column-gap:18px!important;}
  body[data-screen-label] nav.top .brand-mark{width:108px!important;}body[data-screen-label] nav.top .brand-logo{width:62px!important;height:62px!important;}
  body[data-screen-label] nav.top .nav-links{gap:18px!important;}body[data-screen-label] nav.top .nav-links a{font-size:10.5px!important;letter-spacing:.115em!important;}
  body[data-screen-label] nav.top .nav-rating-badge{width:188px!important;height:38px!important;}body[data-screen-label] nav.top .nav-rating-stars{font-size:14px!important;}body[data-screen-label] nav.top .nav-rating-count{font-size:10px!important;letter-spacing:.06em!important;}
  body[data-screen-label] nav.top .lang-switcher,body[data-screen-label] nav.top .lang-current{width:84px!important;}body[data-screen-label] nav.top .btn{width:174px!important;height:58px!important;font-size:12.5px!important;letter-spacing:.14em!important;}
}

@media (max-width:960px){
  body[data-screen-label]{overflow-x:hidden!important;}
  body[data-screen-label] nav.top{max-width:100vw!important;}
}
</style>
'''

REPORT: list[str] = []
COUNTERS = {"scanned": 0, "updated": 0, "skipped": 0, "eyebrows_synced": 0}


def should_process(path: Path, text: str) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel in EXCLUDED or rel.startswith("_") or ".git" in path.parts:
        return False
    if not rel.endswith(".html"):
        return False
    return "class=\"top\"" in text or "class='top'" in text


def eyebrow_text(rel: str) -> str:
    if rel.startswith("en/"):
        return "Restaurant at the Cable Car · Morro da Urca · Sugarloaf Cable Car Park · Rio de Janeiro · Brazil"
    if rel.startswith("es/"):
        return "Restaurante del Bondinho · Morro da Urca · Parque Bondinho Pan de Azúcar · Río de Janeiro · Brasil"
    return "Restaurante do Bondinho · Morro da Urca · Parque Bondinho Pão de Açúcar · Rio de Janeiro · Brasil"


def process(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    COUNTERS["scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    if not should_process(path, original):
        COUNTERS["skipped"] += 1
        return

    text = STYLE_RE.sub("\n", original)

    def repl(match: re.Match[str]) -> str:
        COUNTERS["eyebrows_synced"] += 1
        return match.group(1) + eyebrow_text(rel) + match.group(3)

    text = EYEBROW_RE.sub(repl, text, count=1)
    if "</head>" in text:
        text = text.replace("</head>", FINAL_OVERRIDE + "\n</head>", 1)
    else:
        REPORT.append(f"WARN: sem </head> — {rel}")

    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["updated"] += 1
        REPORT.append(f"UPDATED: {rel}")


def write_report() -> None:
    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report = report_dir / "subpage_home_header_final_override_report.md"
    lines = [
        "# Final Subpage Home Header Override",
        "",
        "## Objetivo",
        "- Corrigir páginas que ainda não estavam iguais ao topo da home.",
        "- Garantir que avaliação, idioma e reserva não sejam cortados em largura intermediária.",
        "- Deixar a pedra do Pão de Açúcar sem textos sobrepostos.",
        "",
        "## Contadores",
    ]
    for key, value in COUNTERS.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Arquivos"])
    lines.extend(f"- {item}" for item in REPORT)
    lines.append("")
    report.write_text("\n".join(lines), encoding="utf-8")
    print(report.read_text(encoding="utf-8"))


def main() -> int:
    for path in sorted(ROOT.rglob("*.html")):
        process(path)
    write_report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
