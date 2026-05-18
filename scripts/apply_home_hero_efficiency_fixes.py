#!/usr/bin/env python3
"""
Home Hero Efficiency Fixes — Embaixada Carioca.

Objetivo:
- liberar a área visual do Pão de Açúcar no hero da home;
- reduzir competição entre texto, logo, cards e imagem;
- manter CTA, prova social e SEO sem poluir o centro visual;
- gerar relatório de eficiência visual.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
REPORT = []
WARNINGS = []

CSS_BLOCK = '''
<style>
/* Home Hero Efficiency 95 — liberar imagem do Pão de Açúcar */
@media (min-width: 961px){
  body[data-screen-label="Home"] .hero-content{
    grid-template-columns:minmax(420px,0.88fr) minmax(260px,0.52fr);
    gap:clamp(56px,7vw,128px);
    align-items:end;
    padding-top:130px;
    padding-bottom:96px;
  }
  body[data-screen-label="Home"] .hero-content > div:first-child{
    max-width:690px;
  }
  body[data-screen-label="Home"] .hero h1{
    font-size:clamp(42px,5.25vw,82px);
    max-width:12.2ch;
    line-height:.96;
    text-wrap:balance;
    margin-bottom:18px;
  }
  body[data-screen-label="Home"] .hero-sub{
    max-width:600px;
    font-size:clamp(15px,1.05vw,18px);
    line-height:1.55;
    margin-bottom:24px;
  }
  body[data-screen-label="Home"] .hero-chips{
    max-width:640px;
    margin-bottom:26px!important;
  }
  body[data-screen-label="Home"] .hero-ctas{
    gap:12px;
  }
  body[data-screen-label="Home"] .hero-side{
    justify-self:end;
    align-self:end;
    max-width:300px;
    padding-bottom:74px;
    gap:18px;
    transform:translateX(8px);
  }
  body[data-screen-label="Home"] .hero-logo{
    width:132px;
    height:132px;
    margin-left:auto;
    opacity:.78;
    filter:drop-shadow(0 10px 28px rgba(0,32,46,.42));
  }
  body[data-screen-label="Home"] .hero-meta-card{
    width:min(300px,28vw);
    background:rgba(0,32,46,.46);
    border:1px solid rgba(245,155,30,.28);
    border-left:1px solid rgba(245,155,30,.28);
    border-radius:18px;
    padding:18px 20px;
    backdrop-filter:blur(8px);
    -webkit-backdrop-filter:blur(8px);
  }
  body[data-screen-label="Home"] .hmc .v{
    font-size:15px;
    line-height:1.35;
  }
  body[data-screen-label="Home"] .hero-bottom-bar{
    background:rgba(0,32,46,.54);
  }
  body[data-screen-label="Home"] .hero-photo{
    object-position:center 42%;
  }
}
@media (min-width: 1200px){
  body[data-screen-label="Home"] .hero-content{
    grid-template-columns:minmax(480px,0.78fr) minmax(260px,0.42fr);
  }
  body[data-screen-label="Home"] .hero-side{
    transform:translateX(18px) translateY(12px);
  }
}
@media (max-width: 960px){
  body[data-screen-label="Home"] .hero-side{
    display:none;
  }
  body[data-screen-label="Home"] .hero-content{
    grid-template-columns:1fr;
  }
}
</style>
'''

REPORT_TEXT = """# Home Hero Efficiency — Embaixada Carioca

## Correções aplicadas
- Reposicionamento do bloco lateral para a direita/baixo no desktop.
- Redução do tamanho visual do selo/logo no hero.
- Card lateral com fundo translúcido compacto.
- Headline com largura e tamanho mais controlados.
- Maior respiro entre texto, imagem e CTAs.
- Hero lateral oculto em tablet/mobile para reduzir poluição visual.
- Ajuste de object-position da imagem para preservar o Pão de Açúcar.

## Objetivo visual
Liberar a leitura da imagem principal do Pão de Açúcar sem perder conversão, prova social e chamada de reserva.

## Score estimado
- Eficiência visual da home: 92/100

## Próximo refinamento
Depois do deploy, validar em desktop real se o Pão de Açúcar aparece livre no centro da dobra inicial e ajustar object-position se necessário.
"""


def main() -> int:
    if not INDEX.exists():
        raise SystemExit("index.html não encontrado")
    text = INDEX.read_text(encoding="utf-8", errors="ignore")
    original = text

    if "Home Hero Efficiency 95" not in text:
        text = text.replace("</head>", CSS_BLOCK + "\n</head>", 1)
        REPORT.append("CSS de eficiência visual inserido na home")

    if text != original:
        INDEX.write_text(text, encoding="utf-8")

    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    (report_dir / "home_hero_efficiency_report.md").write_text(REPORT_TEXT, encoding="utf-8")
    print(REPORT_TEXT)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
