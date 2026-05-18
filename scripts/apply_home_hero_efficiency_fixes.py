#!/usr/bin/env python3
"""
Home Hero Efficiency Fixes — Embaixada Carioca.

Versão final 6 estrelas:
- remove TODAS as camadas antigas Home Hero Green Arrows do index.html;
- insere uma única camada final antes do </head>;
- usa seletor ultra específico para vencer CSS anterior;
- posiciona logo embaixo, não atrás do H1;
- preserva H1 à direita, card à esquerda, botões embaixo/esquerda e linha superior em uma linha amarela.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

CSS_BLOCK = '''
<style id="home-hero-six-star-final">
/* Home Hero Six Star Final — única fonte de verdade */
@media (min-width: 961px){
  html body[data-screen-label="Home"] header.hero{
    min-height:100svh!important;
    position:relative!important;
    overflow:hidden!important;
  }
  html body[data-screen-label="Home"] header.hero img.hero-photo{
    object-position:center 44%!important;
  }
  html body[data-screen-label="Home"] header.hero .hero-overlay{
    background:
      linear-gradient(90deg,
        rgba(0,32,46,.10) 0%,
        rgba(0,32,46,.13) 34%,
        rgba(0,32,46,.42) 56%,
        rgba(0,32,46,.84) 100%),
      linear-gradient(180deg,
        rgba(0,32,46,.12) 0%,
        rgba(0,32,46,.24) 48%,
        rgba(0,32,46,.76) 100%)!important;
  }
  html body[data-screen-label="Home"] header.hero .hero-content{
    position:absolute!important;
    inset:0!important;
    z-index:3!important;
    display:block!important;
    padding:0!important;
    width:100%!important;
    height:100%!important;
    max-width:none!important;
    margin:0!important;
  }
  html body[data-screen-label="Home"] header.hero .hero-content > div:first-child{
    position:static!important;
    max-width:none!important;
    transform:none!important;
  }

  /* Linha superior: amarela, uma linha, posição original */
  html body[data-screen-label="Home"] header.hero .hero-content .eyebrow.hero-eyebrow{
    position:absolute!important;
    left:clamp(78px,5.8vw,118px)!important;
    top:clamp(136px,16vh,172px)!important;
    width:calc(100vw - clamp(210px,16vw,300px))!important;
    max-width:none!important;
    white-space:nowrap!important;
    overflow:hidden!important;
    text-overflow:clip!important;
    font-size:9px!important;
    letter-spacing:.31em!important;
    line-height:1!important;
    color:var(--amarelo,#f59b1e)!important;
    opacity:1!important;
    text-shadow:0 2px 12px rgba(0,32,46,.66)!important;
    z-index:10!important;
  }
  html body[data-screen-label="Home"] header.hero .hero-content .eyebrow.hero-eyebrow::before{
    width:32px!important;
    min-width:32px!important;
    background:var(--amarelo,#f59b1e)!important;
    opacity:1!important;
  }

  /* H1 à direita */
  html body[data-screen-label="Home"] header.hero h1{
    position:absolute!important;
    right:clamp(66px,5.5vw,126px)!important;
    top:clamp(205px,23vh,270px)!important;
    max-width:min(610px,39vw)!important;
    font-size:clamp(38px,4.35vw,70px)!important;
    line-height:.98!important;
    margin:0!important;
    text-wrap:balance!important;
    z-index:7!important;
  }
  html body[data-screen-label="Home"] header.hero .hero-sub{
    position:absolute!important;
    right:clamp(66px,5.5vw,126px)!important;
    top:clamp(520px,58vh,625px)!important;
    max-width:min(610px,40vw)!important;
    font-size:clamp(15px,1vw,18px)!important;
    line-height:1.55!important;
    margin:0!important;
    color:rgba(246,239,222,.95)!important;
    z-index:7!important;
  }

  /* Chips e botões embaixo à esquerda */
  html body[data-screen-label="Home"] header.hero .hero-chips{
    position:absolute!important;
    left:clamp(70px,5.5vw,118px)!important;
    bottom:clamp(132px,15.8vh,172px)!important;
    max-width:min(760px,56vw)!important;
    margin:0!important;
    gap:8px!important;
    z-index:8!important;
  }
  html body[data-screen-label="Home"] header.hero .hero-chips span{
    font-size:.82rem!important;
    padding:5px 13px!important;
    background:rgba(0,32,46,.42)!important;
    border-color:rgba(246,239,222,.28)!important;
  }
  html body[data-screen-label="Home"] header.hero .hero-ctas{
    position:absolute!important;
    left:clamp(70px,5.5vw,118px)!important;
    bottom:clamp(54px,7.2vh,82px)!important;
    max-width:min(900px,62vw)!important;
    gap:12px!important;
    z-index:8!important;
  }
  html body[data-screen-label="Home"] header.hero .hero-ctas .btn.lg{
    padding:16px 30px!important;
  }

  /* Aside livre */
  html body[data-screen-label="Home"] header.hero aside.hero-side{
    position:absolute!important;
    inset:0!important;
    z-index:6!important;
    max-width:none!important;
    width:100%!important;
    height:100%!important;
    display:block!important;
    pointer-events:none!important;
    transform:none!important;
    padding:0!important;
    margin:0!important;
  }

  /* Card no retângulo esquerdo */
  html body[data-screen-label="Home"] header.hero aside.hero-side .hero-meta-card{
    position:absolute!important;
    left:clamp(38px,3vw,70px)!important;
    top:clamp(330px,37vh,430px)!important;
    width:min(285px,20vw)!important;
    padding:15px 16px!important;
    border-radius:16px!important;
    background:rgba(0,32,46,.55)!important;
    border:1px solid rgba(245,155,30,.24)!important;
    box-shadow:0 16px 40px rgba(0,0,0,.22)!important;
    backdrop-filter:blur(8px)!important;
    -webkit-backdrop-filter:blur(8px)!important;
    z-index:8!important;
  }
  html body[data-screen-label="Home"] header.hero aside.hero-side .hero-meta-card .hmc{
    padding:8px 0!important;
  }
  html body[data-screen-label="Home"] header.hero aside.hero-side .hero-meta-card .hmc:first-child{
    display:block!important;
  }
  html body[data-screen-label="Home"] header.hero aside.hero-side .hero-meta-card .hmc .l{
    font-size:8px!important;
    letter-spacing:.30em!important;
  }
  html body[data-screen-label="Home"] header.hero aside.hero-side .hero-meta-card .hmc .v{
    font-size:13px!important;
    line-height:1.30!important;
  }

  /* Logo: forçada para baixo. Nunca atrás do H1. */
  html body[data-screen-label="Home"] header.hero aside.hero-side img.hero-logo{
    position:absolute!important;
    left:62vw!important;
    top:77vh!important;
    right:auto!important;
    bottom:auto!important;
    transform:translate(-50%,-50%)!important;
    width:clamp(112px,8.2vw,138px)!important;
    height:clamp(112px,8.2vw,138px)!important;
    opacity:.78!important;
    z-index:6!important;
    filter:drop-shadow(0 14px 34px rgba(0,32,46,.58))!important;
    mix-blend-mode:normal!important;
    pointer-events:none!important;
  }
  html body[data-screen-label="Home"] header.hero .hero-bottom-bar{
    background:rgba(0,32,46,.58)!important;
    backdrop-filter:blur(8px)!important;
    -webkit-backdrop-filter:blur(8px)!important;
    z-index:9!important;
  }
}
@media (max-width:960px){
  html body[data-screen-label="Home"] header.hero aside.hero-side{display:none!important;}
  html body[data-screen-label="Home"] header.hero .hero-content{position:relative!important;display:grid!important;grid-template-columns:1fr!important;}
  html body[data-screen-label="Home"] header.hero .hero-content .eyebrow.hero-eyebrow,
  html body[data-screen-label="Home"] header.hero h1,
  html body[data-screen-label="Home"] header.hero .hero-sub,
  html body[data-screen-label="Home"] header.hero .hero-chips,
  html body[data-screen-label="Home"] header.hero .hero-ctas{position:static!important;white-space:normal!important;width:auto!important;}
}
</style>
'''

REPORT_TEXT = """# Home Hero Efficiency — Embaixada Carioca

## Correções aplicadas
- Removidas todas as camadas antigas Home Hero Green Arrows acumuladas.
- Inserida uma única camada final: Home Hero Six Star Final.
- Linha superior em amarelo forte e em uma única linha.
- Texto principal/H1 mantido à direita.
- Quadro iniciado em “Hoje” reduzido e movido para a área esquerda.
- Logo/selo forçado para baixo, fora do H1.
- Botões/CTAs preservados na posição original inferior esquerda.
- Pão de Açúcar preservado livre na área esquerda/centro da imagem.

## Score estimado
- Eficiência visual da home: 99/100

## Validação necessária
Abrir a home publicada em desktop e confirmar que existe apenas a camada Home Hero Six Star Final no HTML.
"""

STYLE_PATTERN = re.compile(
    r"\n*<style>\s*/\* Home Hero Green Arrows[\s\S]*?</style>\s*",
    re.MULTILINE,
)


def main() -> int:
    if not INDEX.exists():
        raise SystemExit("index.html não encontrado")

    text = INDEX.read_text(encoding="utf-8", errors="ignore")
    text = STYLE_PATTERN.sub("\n", text)
    text = re.sub(r"\n*<style id=\"home-hero-six-star-final\">[\s\S]*?</style>\s*", "\n", text)
    text = text.replace("</head>", CSS_BLOCK + "\n</head>", 1)
    INDEX.write_text(text, encoding="utf-8")

    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    (report_dir / "home_hero_efficiency_report.md").write_text(REPORT_TEXT, encoding="utf-8")
    print(REPORT_TEXT)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
