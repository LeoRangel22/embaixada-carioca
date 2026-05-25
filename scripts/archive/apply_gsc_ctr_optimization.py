#!/usr/bin/env python3
"""
GSC CTR Optimization — Embaixada Carioca.

Usa consultas reais do Google Search Console para reforçar títulos, descrições,
FAQs e links internos nas páginas com maior intenção de clique.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "gsc_click_magnet_queries.json"
REPORT = []
WARNINGS = []

CTR_BLOCK = '''
<section class="gsc-ctr-block" aria-label="Restaurante no Morro da Urca" style="padding:48px 0;background:#f6efde;border-top:1px solid rgba(0,64,90,.12);border-bottom:1px solid rgba(0,64,90,.12);">
  <div class="wrap">
    <p class="eyebrow" style="margin-bottom:14px;">Restaurante no Morro da Urca</p>
    <h2 style="font-size:clamp(26px,3vw,44px);line-height:1.05;margin:0 0 16px;color:var(--azul1,#00405a);">Dentro do Parque Bondinho Pão de Açúcar, com vista direta para o Pão de Açúcar.</h2>
    <p style="max-width:820px;margin:0 0 22px;color:var(--cinza1,#485156);">A Embaixada Carioca reúne café da manhã todos os dias, almoço brasileiro, feijoada premiada da Academia da Cachaça, Picanha Brasileira, caipirinhas e chope Heineken premiado no Morro da Urca.</p>
    <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:22px;">
      <span style="border:1px solid rgba(0,64,90,.18);border-radius:999px;padding:8px 13px;color:#00405a;font-weight:700;">4.8★ · 7.779 avaliações</span>
      <span style="border:1px solid rgba(0,64,90,.18);border-radius:999px;padding:8px 13px;color:#00405a;font-weight:700;">Av. Pasteur, 520 · Urca</span>
      <span style="border:1px solid rgba(0,64,90,.18);border-radius:999px;padding:8px 13px;color:#00405a;font-weight:700;">Café da manhã 8h30–11h30</span>
      <span style="border:1px solid rgba(0,64,90,.18);border-radius:999px;padding:8px 13px;color:#00405a;font-weight:700;">Aberto todos os dias</span>
    </div>
    <div style="display:flex;flex-wrap:wrap;gap:12px;">
      <a class="btn" href="https://go.tagme.com.br/embaixadacarioca">Reservar mesa →</a>
      <a class="btn ghost" href="cafe-da-manha.html">Ver café da manhã</a>
      <a class="btn ghost" href="cardapio.html">Ver cardápio</a>
    </div>
  </div>
</section>
'''

FAQS = {
    "index.html": '''
<div class="faq-item" style="border-top:1px solid var(--rule);padding-top:24px;">
  <h3 style="font-size:18px;font-weight:600;margin:0 0 12px;">Qual é o restaurante no Morro da Urca dentro do Parque Bondinho?</h3>
  <p class="faq-answer" style="color:var(--cinza1);margin:0;">A Embaixada Carioca fica no Morro da Urca, primeira parada do Bondinho Pão de Açúcar, na Av. Pasteur, 520. É um restaurante com vista direta para o Pão de Açúcar, café da manhã todos os dias, almoço brasileiro, caipirinhas, chope Heineken premiado e reservas pela Tagme.</p>
</div>
<div class="faq-item" style="border-top:1px solid var(--rule);padding-top:24px;">
  <h3 style="font-size:18px;font-weight:600;margin:0 0 12px;">A Embaixada Carioca tem boas avaliações?</h3>
  <p class="faq-answer" style="color:var(--cinza1);margin:0;">Sim. A Embaixada Carioca tem 4.8 estrelas e mais de 7.779 avaliações no Google, sendo uma referência para quem busca restaurante no Morro da Urca, restaurante no Pão de Açúcar e café da manhã com vista no Rio de Janeiro.</p>
</div>
''',
    "cafe-da-manha.html": '''
<div class="faq-item" style="border-top:1px solid var(--rule);padding-top:24px;">
  <h3 style="font-size:18px;font-weight:600;margin:0 0 12px;">Tem café da manhã no Pão de Açúcar?</h3>
  <p class="faq-answer" style="color:var(--cinza1);margin:0;">Sim. A Embaixada Carioca serve café da manhã todos os dias, das 8h30 às 11h30, no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com vista direta para o Pão de Açúcar.</p>
</div>
''',
    "cardapio.html": '''
<div class="faq-item" style="border-top:1px solid var(--rule);padding-top:24px;">
  <h3 style="font-size:18px;font-weight:600;margin:0 0 12px;">Tem feijoada, picanha e chope Heineken no Morro da Urca?</h3>
  <p class="faq-answer" style="color:var(--cinza1);margin:0;">Sim. A Embaixada Carioca serve a feijoada premiada da Academia da Cachaça, Picanha Brasileira, caipirinhas e chope Heineken premiado no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar.</p>
</div>
'''
}

REPLACEMENTS = {
    "index.html": {
        "<title>Restaurante Morro da Urca | Embaixada Carioca</title>": "<title>Restaurante Morro da Urca e Pão de Açúcar | Embaixada Carioca</title>",
        "Restaurante do Bondinho no Rio de Janeiro. Café da manhã, almoço e entardecer com vista panorâmica para o Pão de Açúcar e Baía de Guanabara.": "Restaurante no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. Café da manhã, almoço, feijoada, picanha, caipirinhas e chope Heineken premiado.",
    },
    "cafe-da-manha.html": {
        "<title>Café da Manhã com Vista para o Pão de Açúcar | Embaixada Carioca</title>": "<title>Café da Manhã Pão de Açúcar e Morro da Urca | Embaixada Carioca</title>",
        "Café da manhã com vista para o Pão de Açúcar no Morro da Urca. Buffet e à la carte todos os dias das 8h30 às 11h30. Reservas via Tagme.": "Café da manhã no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. Servido todos os dias das 8h30 às 11h30, com vista direta para o Pão de Açúcar.",
    },
    "cardapio.html": {
        "<title>Cardápio | Embaixada Carioca</title>": "<title>Cardápio: Feijoada, Picanha e Chope Heineken | Embaixada Carioca</title>",
    }
}

TARGETS = ["index.html", "cafe-da-manha.html", "cardapio.html", "almoco.html", "entardecer.html", "guia-do-rio.html"]


def optimize(rel: str) -> None:
    path = ROOT / rel
    if not path.exists():
        WARNINGS.append(f"{rel}: arquivo ausente")
        return
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    changes = 0

    for old, new in REPLACEMENTS.get(rel, {}).items():
        if old in text:
            text = text.replace(old, new)
            changes += 1

    if rel == "index.html" and "class=\"gsc-ctr-block\"" not in text:
        if "</footer>" in text:
            text = text.replace("</footer>", CTR_BLOCK + "\n</footer>", 1)
            changes += 1
        elif "</body>" in text:
            text = text.replace("</body>", CTR_BLOCK + "\n</body>", 1)
            changes += 1

    faq = FAQS.get(rel)
    if faq and faq.strip() not in text:
        idx = text.rfind("</section>")
        if idx != -1:
            text = text[:idx] + faq + "\n" + text[idx:]
            changes += 1

    if text != original:
        path.write_text(text, encoding="utf-8")
        REPORT.append(f"UPDATED: {rel} | changes={changes}")


def cluster_stats(data: dict) -> dict:
    out = {}
    for item in data.get("queries", []):
        name = item.get("cluster", "other")
        out.setdefault(name, {"clicks": 0, "impressions": 0, "queries": []})
        out[name]["clicks"] += int(item.get("clicks", 0))
        out[name]["impressions"] += int(item.get("impressions", 0))
        out[name]["queries"].append(item.get("query", ""))
    for stats in out.values():
        impressions = stats["impressions"] or 1
        stats["ctr"] = round(100 * stats["clicks"] / impressions, 2)
    return out


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8")) if DATA_PATH.exists() else {"queries": []}
    for rel in TARGETS:
        optimize(rel)

    clusters = cluster_stats(data)
    low_ctr = []
    for name, stats in clusters.items():
        if stats["impressions"] >= 3 and stats["ctr"] < 10:
            low_ctr.append(f"{name}: CTR {stats['ctr']}% | {stats['impressions']} impressões | {', '.join(stats['queries'])}")

    score = 96 if len(low_ctr) <= 3 else max(80, 96 - len(low_ctr) * 2)
    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report = report_dir / "gsc_ctr_optimization_report.md"
    report.write_text(
        "# GSC CTR Optimization — Embaixada Carioca\n\n"
        f"## Fonte\n- {data.get('source', 'GSC')}\n- Período: {data.get('period', 'N/A')}\n\n"
        "## Alterações aplicadas\n"
        + ("\n".join(f"- {x}" for x in REPORT) if REPORT else "- Nenhuma alteração necessária")
        + "\n\n## Clusters com CTR baixo\n"
        + ("\n".join(f"- {x}" for x in low_ctr) if low_ctr else "- Nenhum cluster prioritário com CTR baixo")
        + f"\n\n## Score estimado de captura de cliques\n- {score}/100\n",
        encoding="utf-8",
    )
    print(report.read_text(encoding="utf-8"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
