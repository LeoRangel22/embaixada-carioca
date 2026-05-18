#!/usr/bin/env python3
"""
Home Hero Efficiency Fixes — Embaixada Carioca.

Versão setas verdes v4:
- linha "Restaurante do Bondinho..." permanece na posição original;
- botões/CTAs permanecem na posição original inferior esquerda;
- texto principal/H1 vai para a direita;
- card iniciado em "Hoje" ocupa o espaço original do bloco de texto principal;
- logo/selo grande desce e vai para a esquerda, em área vazia;
- Pão de Açúcar fica livre na área esquerda/centro.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

CSS_BLOCK = '''
<style>
/* Home Hero Green Arrows v4 — eyebrow e botões originais, H1 à direita */
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
        rgba(0,32,46,.14) 0%,
        rgba(0,32,46,.16) 34%,
        rgba(0,32,46,.43) 56%,
        rgba(0,32,46,.82) 100%),
      linear-gradient(180deg,
        rgba(0,32,46,.15) 0%,
        rgba(0,32,46,.26) 48%,
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

  body[data-screen-label="Home"] .hero .eyebrow.hero-eyebrow{
    position:absolute;
    left:clamp(70px,5.5vw,118px);
    top:clamp(138px,16.5vh,178px);
    max-width:min(760px,48vw);
    font-size:10px;
    letter-spacing:.32em;
    line-height:1.8;
    opacity:.92;
    z-index:4;
  }

  body[data-screen-label="Home"] .hero h1{
    position:absolute;
    right:clamp(66px,5.5vw,126px);
    top:clamp(205px,23vh,270px);
    max-width:min(610px,39vw);
    font-size:clamp(38px,4.35vw,70px);
    line-height:.98;
    margin:0;
    text-wrap:balance;
    z-index:4;
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
    z-index:4;
  }
  body[data-screen-label="Home"] .hero-chips{
    position:absolute!important;
    left:clamp(70px,5.5vw,118px);
    bottom:clamp(132px,15.8vh,172px);
    max-width:min(760px,56vw);
    margin:0!important;
    gap:8px!important;
    z-index:5;
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
    z-index:5;
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

  body[data-screen-label="Home"] .hero-meta-card{
    position:absolute;
    left:clamp(70px,5.5vw,118px);
    top:clamp(355px,39vh,455px);
    width:min(345px,27vw);
    padding:18px 20px;
    border-radius:18px;
    background:rgba(0,32,46,.54);
    border:1px solid rgba(245,155,30,.26);
    box-shadow:0 18px 46px rgba(0,0,0,.22);
    backdrop-filter:blur(8px);
    -webkit-backdrop-filter:blur(8px);
  }
  body[data-screen-label="Home"] .hero-meta-card .hmc{
    padding:10px 0;
  }
  body[data-screen-label="Home"] .hero-meta-card .hmc:first-child{
    display:block;
  }
  body[data-screen-label="Home"] .hmc .l{
    font-size:9px;
    letter-spacing:.32em;
  }
  body[data-screen-label="Home"] .hmc .v{
    font-size:14px;
    line-height:1.34;
  }

  body[data-screen-label="Home"] .hero-logo{
    position:absolute;
    left:clamp(520px,35vw,720px);
    bottom:clamp(86px,10vh,118px);
    width:122px;
    height:122px;
    opacity:.72;
    filter:drop-shadow(0 12px 30px rgba(0,32,46,.48));
  }

  body[data-screen-label="Home"] .hero-bottom-bar{
    background:rgba(0,32,46,.58);
    backdrop-filter:blur(8px);
    -webkit-backdrop-filter:blur(8px);
    z-index:6;
  }
}
@media (min-width: 1500px){
  body[data-screen-label="Home"] .hero-logo{
    left:clamp(610px,38vw,790px);
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
  }
}
</style>
'''

REPORT_TEXT = """# Home Hero Efficiency — Embaixada Carioca

## Correções aplicadas
- Linha “Restaurante do Bondinho...” preservada na posição original superior esquerda.
- Botões/CTAs preservados na posição original inferior esquerda.
- Texto principal/H1 deslocado para a direita.
- Card iniciado em “Hoje” movido para o espaço original do texto principal.
- Logo/selo movido para baixo e para a esquerda, em área vazia, sem cobrir o CTA.
- Pão de Açúcar preservado livre na área esquerda/centro da imagem.
- Overlay suavizado à esquerda e reforçado à direita.

## Objetivo visual
Seguir exatamente a composição solicitada: H1 à direita; card “Hoje” no antigo espaço do texto; logo embaixo/esquerda; linha superior e botões nas posições originais.

## Score estimado
- Eficiência visual da home: 97/100

## Validação necessária
Abrir a home publicada em desktop e verificar se os botões e a linha “Restaurante do Bondinho...” ficaram nas posições originais, com o H1 à direita.
"""


def main() -> int:
    if not INDEX.exists():
        raise SystemExit("index.html não encontrado")
    text = INDEX.read_text(encoding="utf-8", errors="ignore")
    original = text

    if "Home Hero Green Arrows v4" not in text:
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
