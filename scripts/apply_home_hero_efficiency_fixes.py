#!/usr/bin/env python3
"""
Home Hero Efficiency Fixes — Embaixada Carioca.

Versão setas verdes:
- mover o texto principal para a direita, sobre a área mais escura/teto;
- liberar a área esquerda/centro onde aparece o Pão de Açúcar;
- manter CTA e prova social sem cobrir a paisagem;
- reduzir ou deslocar o bloco lateral para não competir com a imagem.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

CSS_BLOCK = '''
<style>
/* Home Hero Green Arrows v2 — texto à direita, Pão de Açúcar livre */
@media (min-width: 961px){
  body[data-screen-label="Home"] .hero{
    min-height:100svh;
  }
  body[data-screen-label="Home"] .hero-photo{
    object-position:center 44%;
  }
  body[data-screen-label="Home"] .hero-overlay{
    background:
      linear-gradient(90deg,
        rgba(0,32,46,.18) 0%,
        rgba(0,32,46,.18) 32%,
        rgba(0,32,46,.48) 54%,
        rgba(0,32,46,.78) 100%),
      linear-gradient(180deg,
        rgba(0,32,46,.20) 0%,
        rgba(0,32,46,.30) 48%,
        rgba(0,32,46,.72) 100%);
  }
  body[data-screen-label="Home"] .hero-content{
    display:grid;
    grid-template-columns:minmax(45vw,1fr) minmax(500px,620px);
    gap:clamp(36px,5vw,88px);
    align-items:end;
    padding-top:128px;
    padding-bottom:92px;
  }
  body[data-screen-label="Home"] .hero-content > div:first-child{
    grid-column:2;
    justify-self:end;
    max-width:620px;
    text-align:left;
    transform:translateY(8px);
  }
  body[data-screen-label="Home"] .hero .eyebrow.hero-eyebrow{
    max-width:620px;
    font-size:10px;
    letter-spacing:.30em;
    opacity:.86;
  }
  body[data-screen-label="Home"] .hero h1{
    font-size:clamp(40px,4.55vw,74px);
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
    grid-column:2;
    justify-self:end;
    align-self:start;
    max-width:220px;
    margin-top:142px;
    transform:translateX(8px);
    gap:12px;
    opacity:.92;
    pointer-events:none;
  }
  body[data-screen-label="Home"] .hero-logo{
    width:112px;
    height:112px;
    margin-left:auto;
    opacity:.70;
    filter:drop-shadow(0 10px 28px rgba(0,32,46,.46));
  }
  body[data-screen-label="Home"] .hero-meta-card{
    width:220px;
    padding:13px 15px;
    border-radius:14px;
    background:rgba(0,32,46,.48);
    border:1px solid rgba(245,155,30,.24);
    backdrop-filter:blur(7px);
    -webkit-backdrop-filter:blur(7px);
  }
  body[data-screen-label="Home"] .hero-meta-card .hmc{
    padding:9px 0;
  }
  body[data-screen-label="Home"] .hero-meta-card .hmc:first-child{
    display:none;
  }
  body[data-screen-label="Home"] .hmc .l{
    font-size:9px;
    letter-spacing:.32em;
  }
  body[data-screen-label="Home"] .hmc .v{
    font-size:13px;
    line-height:1.32;
  }
  body[data-screen-label="Home"] .hero-bottom-bar{
    background:rgba(0,32,46,.58);
    backdrop-filter:blur(8px);
    -webkit-backdrop-filter:blur(8px);
  }
}
@media (min-width: 1280px){
  body[data-screen-label="Home"] .hero-content{
    grid-template-columns:minmax(50vw,1fr) minmax(520px,650px);
  }
  body[data-screen-label="Home"] .hero-content > div:first-child{
    transform:translate(8px,10px);
  }
}
@media (min-width: 1500px){
  body[data-screen-label="Home"] .hero-content{
    grid-template-columns:minmax(54vw,1fr) minmax(540px,660px);
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
- Bloco principal deslocado para a direita, seguindo as setas verdes.
- Área esquerda/central liberada para leitura do Pão de Açúcar.
- Overlay reforçado à direita e suavizado à esquerda.
- Headline reduzida e limitada em largura para não invadir a paisagem.
- Chips compactados.
- CTAs mantidos, mas com menor ocupação visual.
- Logo e card lateral reduzidos e reposicionados.
- Primeiro item do card lateral ocultado para diminuir ruído visual.
- Lateral oculto em tablet/mobile.

## Objetivo visual
Deixar o Pão de Açúcar livre na imagem e concentrar a mensagem comercial na área escura à direita, com maior eficiência e eficácia de conversão.

## Score estimado
- Eficiência visual da home: 95/100

## Validação necessária
Abrir a home publicada em desktop e confirmar se o Pão de Açúcar ficou livre à esquerda/centro conforme as setas verdes.
"""


def main() -> int:
    if not INDEX.exists():
        raise SystemExit("index.html não encontrado")
    text = INDEX.read_text(encoding="utf-8", errors="ignore")
    original = text

    if "Home Hero Green Arrows v2" not in text:
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
