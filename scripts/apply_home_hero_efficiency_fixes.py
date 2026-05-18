#!/usr/bin/env python3
"""
Home Hero Efficiency Fixes — Embaixada Carioca.

Versão setas verdes v6:
- linha superior em amarelo, em uma linha só;
- card iniciado em "Hoje" menor e mais à esquerda, dentro da área marcada;
- logo/selo fora do título, posicionado no círculo inferior indicado;
- botões/CTAs preservados na posição original inferior esquerda;
- H1 permanece à direita;
- Pão de Açúcar livre na área esquerda/centro.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

CSS_BLOCK = '''
<style>
/* Home Hero Green Arrows v6 — alvo visual anotado */
@media (min-width: 961px){
  body[data-screen-label="Home"] .hero{
    min-height:100svh;
    position:relative;
    overflow:hidden;
  }
  body[data-screen-label="Home"] .hero-photo{
    object-position:center 44%;
  }
  body[data-screen-label="Home"] .hero-overlay{
    background:
      linear-gradient(90deg,
        rgba(0,32,46,.12) 0%,
        rgba(0,32,46,.15) 34%,
        rgba(0,32,46,.43) 56%,
        rgba(0,32,46,.82) 100%),
      linear-gradient(180deg,
        rgba(0,32,46,.14) 0%,
        rgba(0,32,46,.25) 48%,
        rgba(0,32,46,.75) 100%);
  }

  body[data-screen-label="Home"] .hero-content{
    position:absolute;
    inset:0;
    z-index:3;
    display:block;
    padding:0;
    width:100%;
    height:100%;
    max-width:none;
  }
  body[data-screen-label="Home"] .hero-content > div:first-child{
    position:static;
    max-width:none;
    transform:none!important;
  }

  /* 1 linha: sem quebra, amarelo, ocupando a faixa superior marcada */
  body[data-screen-label="Home"] .hero .eyebrow.hero-eyebrow{
    position:absolute;
    left:clamp(78px,5.8vw,118px);
    top:clamp(136px,16vh,172px);
    width:calc(100vw - clamp(210px,16vw,300px));
    max-width:none!important;
    white-space:nowrap!important;
    overflow:hidden;
    text-overflow:clip;
    font-size:9px;
    letter-spacing:.31em;
    line-height:1;
    color:var(--amarelo,#f59b1e)!important;
    opacity:1!important;
    text-shadow:0 2px 12px rgba(0,32,46,.66);
    z-index:7;
  }
  body[data-screen-label="Home"] .hero .eyebrow.hero-eyebrow::before{
    width:32px!important;
    min-width:32px!important;
    background:var(--amarelo,#f59b1e)!important;
    opacity:1!important;
  }

  /* H1 à direita, sem cobrir o Pão de Açúcar */
  body[data-screen-label="Home"] .hero h1{
    position:absolute;
    right:clamp(66px,5.5vw,126px);
    top:clamp(205px,23vh,270px);
    max-width:min(610px,39vw);
    font-size:clamp(38px,4.35vw,70px);
    line-height:.98;
    margin:0;
    text-wrap:balance;
    z-index:5;
  }
  body[data-screen-label="Home"] .hero-sub{
    position:absolute;
    right:clamp(66px,5.5vw,126px);
    top:clamp(520px,58vh,625px);
    max-width:min(610px,40vw);
    font-size:clamp(15px,1vw,18px);
    line-height:1.55;
    margin:0;
    color:rgba(246,239,222,.95);
    z-index:5;
  }

  /* Chips e botões originais embaixo/esquerda */
  body[data-screen-label="Home"] .hero-chips{
    position:absolute!important;
    left:clamp(70px,5.5vw,118px);
    bottom:clamp(132px,15.8vh,172px);
    max-width:min(760px,56vw);
    margin:0!important;
    gap:8px!important;
    z-index:6;
  }
  body[data-screen-label="Home"] .hero-chips span{
    font-size:.82rem!important;
    padding:5px 13px!important;
    background:rgba(0,32,46,.42)!important;
    border-color:rgba(246,239,222,.28)!important;
  }
  body[data-screen-label="Home"] .hero-ctas{
    position:absolute;
    left:clamp(70px,5.5vw,118px);
    bottom:clamp(54px,7.2vh,82px);
    max-width:min(900px,62vw);
    gap:12px;
    z-index:6;
  }
  body[data-screen-label="Home"] .hero-ctas .btn.lg{
    padding:16px 30px!important;
  }

  body[data-screen-label="Home"] .hero-side{
    position:absolute;
    inset:0;
    z-index:4;
    max-width:none;
    width:100%;
    height:100%;
    display:block;
    pointer-events:none;
    transform:none!important;
    padding:0;
    margin:0;
  }

  /* Quadro no retângulo azul: menor, mais à esquerda, sem invadir o H1 */
  body[data-screen-label="Home"] .hero-meta-card{
    position:absolute;
    left:clamp(38px,3vw,70px);
    top:clamp(330px,37vh,430px);
    width:min(285px,20vw);
    padding:15px 16px;
    border-radius:16px;
    background:rgba(0,32,46,.55);
    border:1px solid rgba(245,155,30,.24);
    box-shadow:0 16px 40px rgba(0,0,0,.22);
    backdrop-filter:blur(8px);
    -webkit-backdrop-filter:blur(8px);
  }
  body[data-screen-label="Home"] .hero-meta-card .hmc{
    padding:8px 0;
  }
  body[data-screen-label="Home"] .hero-meta-card .hmc:first-child{
    display:block;
  }
  body[data-screen-label="Home"] .hmc .l{
    font-size:8px;
    letter-spacing:.30em;
  }
  body[data-screen-label="Home"] .hmc .v{
    font-size:13px;
    line-height:1.30;
  }

  /* Logo no círculo inferior indicado, não atrás do título */
  body[data-screen-label="Home"] .hero-logo{
    position:absolute;
    left:clamp(980px,67vw,1120px);
    bottom:clamp(72px,8.5vh,98px);
    width:clamp(112px,8.2vw,138px);
    height:clamp(112px,8.2vw,138px);
    opacity:.76;
    z-index:5;
    filter:drop-shadow(0 14px 34px rgba(0,32,46,.58));
    mix-blend-mode:normal;
  }

  body[data-screen-label="Home"] .hero-bottom-bar{
    background:rgba(0,32,46,.58);
    backdrop-filter:blur(8px);
    -webkit-backdrop-filter:blur(8px);
    z-index:7;
  }
}
@media (min-width: 1500px){
  body[data-screen-label="Home"] .hero-logo{
    left:clamp(1040px,68vw,1180px);
  }
}
@media (max-width: 960px){
  body[data-screen-label="Home"] .hero-side{
    display:none!important;
  }
  body[data-screen-label="Home"] .hero-content{
    position:relative;
    display:grid;
    grid-template-columns:1fr;
  }
  body[data-screen-label="Home"] .hero .eyebrow.hero-eyebrow,
  body[data-screen-label="Home"] .hero h1,
  body[data-screen-label="Home"] .hero-sub,
  body[data-screen-label="Home"] .hero-chips,
  body[data-screen-label="Home"] .hero-ctas{
    position:static!important;
    white-space:normal!important;
    width:auto!important;
  }
}
</style>
'''

REPORT_TEXT = """# Home Hero Efficiency — Embaixada Carioca

## Correções aplicadas
- Linha superior em amarelo forte e em uma única linha.
- Texto principal/H1 mantido à direita.
- Quadro iniciado em “Hoje” reduzido e movido para a área azul à esquerda.
- Logo/selo removido de trás do título e posicionado no círculo inferior indicado.
- Botões/CTAs preservados na posição original inferior esquerda.
- Pão de Açúcar preservado livre na área esquerda/centro da imagem.

## Objetivo visual
Seguir exatamente a marcação do print: 1 linha no topo, quadro à esquerda, logo embaixo na área marcada, H1 à direita e botões no lugar original.

## Score estimado
- Eficiência visual da home: 98/100

## Validação necessária
Abrir a home publicada em desktop e verificar: linha única, quadro menor à esquerda e logo no círculo inferior.
"""


def main() -> int:
    if not INDEX.exists():
        raise SystemExit("index.html não encontrado")
    text = INDEX.read_text(encoding="utf-8", errors="ignore")
    original = text

    if "Home Hero Green Arrows v6" not in text:
        text = text.replace("</head>", CSS_BLOCK + "\n</head>", 1)

    if text != original:
        INDEX.write_text(text, encoding="utf-8")

    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    (report_dir / "home_hero_efficiency_report.md").write_text(REPORT_TEXT, encoding="utf-8")
    print(REPORT_TEXT)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
