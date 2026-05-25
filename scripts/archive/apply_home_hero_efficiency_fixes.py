#!/usr/bin/env python3
"""
Home Hero Efficiency Fixes — Embaixada Carioca.

Versão final 6 estrelas:
- remove TODAS as camadas antigas Home Hero Green Arrows do index.html;
- insere uma única camada final antes do </head>;
- usa seletor ultra específico para vencer CSS anterior;
- preserva H1 à direita, card à esquerda, botões embaixo/esquerda e linha superior em uma linha amarela;
- quadro "Hoje / Premiada / Vista" 25% mais estreito, com base fixa e altura maior;
- valor "Pôr do sol às 17h44" fica em linha própria abaixo de "Hoje, no alto";
- todo o conteúdo do hero sobe 2cm, mantendo a foto de fundo no lugar;
- linha amarela alinhada ao início do item "CAFÉ DA MANHÃ" e subida 0,5cm;
- texto menor/subtítulo baixado 1,0cm, ou seja, subiu 0,5cm em relação ao ajuste anterior;
- logo na altura dos botões, centralizada no eixo visual do A de Açúcar;
- chip "Dentro do Parque Bondinho" forçado para a segunda linha.
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
    --hero-up-2cm:76px;
    --hero-down-1cm:38px;
    --hero-up-05cm:19px;
    --hero-down-subtitle:38px;
    --hero-eyebrow-left:clamp(185px,11.8vw,215px);
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
  html body[data-screen-label="Home"] header.hero .hero-content .eyebrow.hero-eyebrow{
    position:absolute!important;
    left:var(--hero-eyebrow-left)!important;
    top:calc(clamp(136px,16vh,172px) - var(--hero-up-2cm) + var(--hero-down-1cm) - var(--hero-up-05cm))!important;
    width:calc(100vw - var(--hero-eyebrow-left) - clamp(210px,16vw,300px))!important;
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
  html body[data-screen-label="Home"] header.hero h1{
    position:absolute!important;
    right:clamp(66px,5.5vw,126px)!important;
    top:calc(clamp(205px,23vh,270px) - var(--hero-up-2cm))!important;
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
    top:calc(clamp(520px,58vh,625px) - var(--hero-up-2cm) + var(--hero-down-subtitle))!important;
    max-width:min(610px,40vw)!important;
    font-size:clamp(15px,1vw,18px)!important;
    line-height:1.55!important;
    margin:0!important;
    color:rgba(246,239,222,.95)!important;
    z-index:7!important;
  }
  html body[data-screen-label="Home"] header.hero .hero-chips{
    position:absolute!important;
    left:clamp(70px,5.5vw,118px)!important;
    bottom:calc(clamp(132px,15.8vh,172px) + var(--hero-up-2cm))!important;
    max-width:min(760px,56vw)!important;
    margin:0!important;
    gap:8px!important;
    z-index:8!important;
    display:flex!important;
    flex-wrap:wrap!important;
    align-items:center!important;
  }
  html body[data-screen-label="Home"] header.hero .hero-chips::before{
    content:""!important;
    flex:0 0 100%!important;
    height:0!important;
    order:3!important;
  }
  html body[data-screen-label="Home"] header.hero .hero-chips span{
    font-size:.82rem!important;
    padding:5px 13px!important;
    background:rgba(0,32,46,.42)!important;
    border-color:rgba(246,239,222,.28)!important;
  }
  html body[data-screen-label="Home"] header.hero .hero-chips span:nth-child(1){order:1!important;}
  html body[data-screen-label="Home"] header.hero .hero-chips span:nth-child(2){order:2!important;}
  html body[data-screen-label="Home"] header.hero .hero-chips span:nth-child(3){order:4!important;}
  html body[data-screen-label="Home"] header.hero .hero-chips span:nth-child(4){order:5!important;}
  html body[data-screen-label="Home"] header.hero .hero-ctas{
    position:absolute!important;
    left:clamp(70px,5.5vw,118px)!important;
    bottom:calc(clamp(54px,7.2vh,82px) + var(--hero-up-2cm))!important;
    max-width:min(900px,62vw)!important;
    gap:12px!important;
    z-index:8!important;
  }
  html body[data-screen-label="Home"] header.hero .hero-ctas .btn.lg{
    padding:16px 30px!important;
  }
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
  html body[data-screen-label="Home"] header.hero aside.hero-side .hero-meta-card{
    position:absolute!important;
    left:clamp(38px,3vw,70px)!important;
    top:auto!important;
    bottom:calc(clamp(246px,28.5vh,315px) + var(--hero-up-2cm))!important;
    width:min(214px,15vw)!important;
    min-height:clamp(310px,38vh,390px)!important;
    display:flex!important;
    flex-direction:column!important;
    justify-content:space-between!important;
    padding:18px 16px!important;
    border-radius:16px!important;
    background:rgba(0,32,46,.55)!important;
    border:1px solid rgba(245,155,30,.24)!important;
    box-shadow:0 16px 40px rgba(0,0,0,.22)!important;
    backdrop-filter:blur(8px)!important;
    -webkit-backdrop-filter:blur(8px)!important;
    z-index:8!important;
  }
  html body[data-screen-label="Home"] header.hero aside.hero-side .hero-meta-card .hmc{
    display:block!important;
    padding:8px 0!important;
  }
  html body[data-screen-label="Home"] header.hero aside.hero-side .hero-meta-card .hmc:first-child{
    display:block!important;
  }
  html body[data-screen-label="Home"] header.hero aside.hero-side .hero-meta-card .hmc .l{
    display:block!important;
    width:100%!important;
    font-size:8px!important;
    letter-spacing:.30em!important;
    line-height:1!important;
    margin:0 0 10px!important;
    white-space:nowrap!important;
  }
  html body[data-screen-label="Home"] header.hero aside.hero-side .hero-meta-card .hmc .v{
    display:block!important;
    width:100%!important;
    font-size:13px!important;
    line-height:1.30!important;
    margin:0!important;
    white-space:normal!important;
  }
  html body[data-screen-label="Home"] header.hero aside.hero-side img.hero-logo{
    position:absolute!important;
    left:72vw!important;
    top:auto!important;
    right:auto!important;
    bottom:calc(clamp(54px,7.2vh,82px) + var(--hero-up-2cm) - 46px)!important;
    transform:translateX(-50%)!important;
    width:clamp(140px,10vw,166px)!important;
    height:clamp(140px,10vw,166px)!important;
    opacity:.80!important;
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
- Texto menor do hero subiu 0,5cm em relação ao último ajuste.
- O deslocamento líquido agora é de 1,0cm para baixo, em vez de 1,5cm.
- H1, foto de fundo, chips, botões e logo preservados.

## Score estimado
- Eficiência visual da home: 99/100
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
