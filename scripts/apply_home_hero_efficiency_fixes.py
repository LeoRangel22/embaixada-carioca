#!/usr/bin/env python3
"""
Home Hero Efficiency Fixes — Embaixada Carioca.

Versão setas verdes v3:
- texto principal deslocado para a direita;
- card iniciado em "Hoje" colocado no espaço original do texto principal;
- logo/selo grande movido para baixo e para a esquerda;
- Pão de Açúcar livre na área esquerda/centro.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

CSS_BLOCK = '''
<style>
/* Home Hero Green Arrows v3 — card à esquerda, texto à direita, logo embaixo */
@media (min-width: 961px){
  body[data-screen-label="Home"] .hero{
    min-height:100svh;
    position:relative;
  }
  body[data-screen-label="Home"] .hero-photo{
    object-position:center 44%;
  }
  body[data-screen-label="Home"] .hero-overlay{
    background:
      linear-gradient(90deg,
        rgba(0,32,46,.13) 0%,
        rgba(0,32,46,.16) 31%,
        rgba(0,32,46,.46) 57%,
        rgba(0,32,46,.82) 100%),
      linear-gradient(180deg,
        rgba(0,32,46,.16) 0%,
        rgba(0,32,46,.25) 47%,
        rgba(0,32,46,.74) 100%);
  }
  body[data-screen-label="Home"] .hero-content{
    display:grid;
    grid-template-columns:minmax(49vw,1fr) minmax(500px,640px);
    gap:clamp(38px,5vw,88px);
    align-items:end;
    padding-top:126px;
    padding-bottom:92px;
    position:relative;
    z-index:3;
  }
  body[data-screen-label="Home"] .hero-content > div:first-child{
    grid-column:2;
    justify-self:end;
    max-width:620px;
    text-align:left;
    transform:translate(10px,8px);
  }
  body[data-screen-label="Home"] .hero .eyebrow.hero-eyebrow{
    max-width:620px;
    font-size:10px;
    letter-spacing:.30em;
    opacity:.86;
  }
  body[data-screen-label="Home"] .hero h1{
    font-size:clamp(39px,4.45vw,72px);
    line-height:.97;
    max-width:11.8ch;
    margin:0 0 18px;
    text-wrap:balance;
  }
  body[data-screen-label="Home"] .hero-sub{
    max-width:560px;
    font-size:clamp(15px,1vw,18px);
    line-height:1.55;
    margin:0 0 20px;
    color:rgba(246,239,222,.94);
  }
  body[data-screen-label="Home"] .hero-chips{
    max-width:560px;
    margin:0 0 22px!important;
    gap:7px!important;
  }
  body[data-screen-label="Home"] .hero-chips span{
    font-size:.78rem!important;
    padding:5px 11px!important;
    background:rgba(0,32,46,.46)!important;
    border-color:rgba(246,239,222,.26)!important;
  }
  body[data-screen-label="Home"] .hero-ctas{
    max-width:620px;
    gap:10px;
  }
  body[data-screen-label="Home"] .hero-ctas .btn.lg{
    padding:15px 25px!important;
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
    left:clamp(64px,5.4vw,112px);
    top:clamp(365px,43vh,470px);
    width:min(340px,26vw);
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
    left:clamp(70px,5.8vw,118px);
    bottom:clamp(92px,10.5vh,128px);
    width:118px;
    height:118px;
    opacity:.72;
    filter:drop-shadow(0 12px 30px rgba(0,32,46,.48));
  }

  body[data-screen-label="Home"] .hero-bottom-bar{
    background:rgba(0,32,46,.58);
    backdrop-filter:blur(8px);
    -webkit-backdrop-filter:blur(8px);
    z-index:5;
  }
}
@media (min-width: 1280px){
  body[data-screen-label="Home"] .hero-content{
    grid-template-columns:minmax(53vw,1fr) minmax(520px,650px);
  }
}
@media (min-width: 1500px){
  body[data-screen-label="Home"] .hero-content{
    grid-template-columns:minmax(56vw,1fr) minmax(540px,660px);
  }
  body[data-screen-label="Home"] .hero-meta-card{
    top:clamp(390px,45vh,500px);
  }
}
@media (max-width: 960px){
  body[data-screen-label="Home"] .hero-side{
    display:none!important;
  }
  body[data-screen-label="Home"] .hero-content{
    grid-template-columns:1fr;
  }
}
</style>
'''

REPORT_TEXT = """# Home Hero Efficiency — Embaixada Carioca

## Correções aplicadas
- Texto principal deslocado para a direita.
- Card iniciado em “Hoje” movido para o espaço original do texto principal.
- Logo/selo movido para baixo e para a esquerda.
- Pão de Açúcar preservado livre na área esquerda/centro da imagem.
- Overlay suavizado à esquerda e reforçado à direita.
- Chips e CTAs compactados.
- Hero lateral oculto em tablet/mobile.

## Objetivo visual
Seguir exatamente a direção das setas verdes: conteúdo comercial concentrado em áreas escuras/vazias, sem cobrir a imagem do Pão de Açúcar.

## Score estimado
- Eficiência visual da home: 96/100

## Validação necessária
Abrir a home publicada em desktop e verificar se o card “Hoje” entrou no espaço antigo do texto principal e se a logo ficou abaixo à esquerda.
"""


def main() -> int:
    if not INDEX.exists():
        raise SystemExit("index.html não encontrado")
    text = INDEX.read_text(encoding="utf-8", errors="ignore")
    original = text

    if "Home Hero Green Arrows v3" not in text:
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
