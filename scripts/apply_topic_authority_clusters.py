#!/usr/bin/env python3
"""
Autoridade temática SEO / GEO / IA — Embaixada Carioca.

Objetivo:
Criar e auditar clusters editoriais para dominar buscas de alta intenção sem keyword stuffing.

Clusters:
- restaurante / restaurante com vista;
- café da manhã;
- feijoada;
- picanha;
- Pão de Açúcar;
- Morro da Urca;
- Bondinho;
- Urca;
- Rio de Janeiro;
- chope Heineken premiado.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT: list[str] = []
WARNINGS: list[str] = []

CLUSTERS = {
    "restaurante": {
        "primary_page": "index.html",
        "terms": ["Restaurante Morro da Urca", "Restaurante do Bondinho", "restaurante com vista", "restaurante no Pão de Açúcar"],
        "links": ["cafe-da-manha.html", "almoco.html", "cardapio.html", "eventos.html", "guia-do-rio.html"],
    },
    "cafe_da_manha": {
        "primary_page": "cafe-da-manha.html",
        "terms": ["café da manhã com vista", "café da manhã Pão de Açúcar", "café da manhã Morro da Urca", "café da manhã na Urca"],
        "links": ["index.html", "almoco.html", "guia-do-rio.html", "parque-bondinho.html"],
    },
    "feijoada": {
        "primary_page": "feijoada.html",
        "fallback_page": "cardapio.html",
        "terms": ["feijoada premiada", "Academia da Cachaça", "feijoada no Morro da Urca", "feijoada com vista"],
        "links": ["cardapio.html", "almoco.html", "feijoada-com-vista-rio-de-janeiro.html"],
    },
    "picanha": {
        "primary_page": "cardapio.html",
        "terms": ["picanha", "Picanha Brasileira", "picanha no Morro da Urca", "picanha com vista"],
        "links": ["almoco.html", "cardapio.html", "index.html"],
    },
    "pao_de_acucar": {
        "primary_page": "parque-bondinho.html",
        "fallback_page": "index.html",
        "terms": ["Pão de Açúcar", "Parque Bondinho Pão de Açúcar", "vista para o Pão de Açúcar", "Bondinho Pão de Açúcar"],
        "links": ["index.html", "cafe-da-manha.html", "almoco.html", "entardecer.html", "guia-do-rio.html"],
    },
    "morro_da_urca": {
        "primary_page": "morro-da-urca.html",
        "terms": ["Morro da Urca", "restaurante no Morro da Urca", "alto do Morro da Urca", "primeira parada do bondinho"],
        "links": ["index.html", "guia-do-rio.html", "parque-bondinho.html", "entardecer.html"],
    },
    "bondinho": {
        "primary_page": "parque-bondinho.html",
        "terms": ["Bondinho", "Parque Bondinho", "restaurante do Bondinho", "Bondinho Pão de Açúcar"],
        "links": ["index.html", "cafe-da-manha.html", "morro-da-urca.html", "guia-do-rio.html"],
    },
    "urca": {
        "primary_page": "guia-do-rio.html",
        "terms": ["Urca", "bairro da Urca", "restaurante na Urca", "Praia Vermelha"],
        "links": ["morro-da-urca.html", "parque-bondinho.html", "index.html"],
    },
    "rio_de_janeiro": {
        "primary_page": "guia-do-rio.html",
        "terms": ["Rio de Janeiro", "onde comer no Rio de Janeiro", "restaurantes Rio de Janeiro com vista", "Cristo Redentor"],
        "links": ["index.html", "cafe-da-manha.html", "almoco.html", "entardecer.html", "eventos.html"],
    },
    "chope_heineken": {
        "primary_page": "cardapio.html",
        "terms": ["chope Heineken", "chope Heineken premiado", "melhor chope Heineken do Rio", "Heineken Masters"],
        "links": ["entardecer.html", "almoco.html", "index.html"],
    },
}

TOPIC_BLOCK = '''
<section class="topic-authority" aria-label="Guias principais da Embaixada Carioca" style="padding:56px 0;background:rgba(0,64,90,0.04);border-top:1px solid rgba(0,64,90,0.10);">
  <div class="wrap">
    <p class="eyebrow" style="margin-bottom:18px;">Guias principais</p>
    <h2 style="font-size:clamp(26px,3vw,42px);line-height:1.05;margin:0 0 18px;color:var(--azul1,#00405a);">Restaurante, café da manhã, feijoada, picanha e drinks no Morro da Urca.</h2>
    <p style="max-width:760px;margin:0 0 24px;color:var(--cinza1,#485156);">Explore os principais momentos da Embaixada Carioca dentro do Parque Bondinho Pão de Açúcar: café da manhã com vista, almoço brasileiro, feijoada premiada da Academia da Cachaça, Picanha Brasileira, caipirinhas e chope Heineken premiado.</p>
    <nav aria-label="Links de autoridade temática" style="display:flex;flex-wrap:wrap;gap:10px;">
      <a href="cafe-da-manha.html">Café da manhã com vista</a>
      <a href="almoco.html">Almoço no Morro da Urca</a>
      <a href="cardapio.html">Feijoada, picanha e chope Heineken</a>
      <a href="entardecer.html">Entardecer e drinks</a>
      <a href="morro-da-urca.html">Morro da Urca</a>
      <a href="parque-bondinho.html">Parque Bondinho Pão de Açúcar</a>
      <a href="guia-do-rio.html">Onde comer no Rio de Janeiro</a>
    </nav>
  </div>
</section>
'''

TOPIC_BLOCK_CSS = '''
<style>
.topic-authority nav a{display:inline-flex;align-items:center;padding:10px 15px;border:1px solid rgba(0,64,90,.18);border-radius:999px;text-decoration:none;color:var(--azul1,#00405a);font-weight:700;font-size:13px;background:rgba(255,255,255,.35)}
.topic-authority nav a:hover{background:var(--amarelo,#f59b1e);border-color:var(--amarelo,#f59b1e)}
</style>
'''

PAGES_TO_RECEIVE_TOPIC_BLOCK = [
    "index.html",
    "cafe-da-manha.html",
    "almoco.html",
    "entardecer.html",
    "cardapio.html",
    "guia-do-rio.html",
]


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="ignore")


def write(rel: str, text: str) -> None:
    (ROOT / rel).write_text(text, encoding="utf-8")


def add_topic_block(rel: str) -> None:
    if not exists(rel):
        return
    text = read(rel)
    if "class=\"topic-authority\"" in text:
        return
    original = text
    if "</head>" in text and "topic-authority nav a" not in text:
        text = text.replace("</head>", TOPIC_BLOCK_CSS + "\n</head>", 1)
    if "</footer>" in text:
        text = text.replace("</footer>", TOPIC_BLOCK + "\n</footer>", 1)
    elif "</body>" in text:
        text = text.replace("</body>", TOPIC_BLOCK + "\n</body>", 1)
    if text != original:
        write(rel, text)
        REPORT.append(f"UPDATED: {rel} | bloco de autoridade temática inserido")


def audit_cluster(name: str, cfg: dict) -> None:
    page = cfg.get("primary_page")
    if page and not exists(page):
        fallback = cfg.get("fallback_page")
        if fallback and exists(fallback):
            WARNINGS.append(f"{name}: página primária ausente ({page}); usando fallback {fallback}")
            page = fallback
        else:
            WARNINGS.append(f"{name}: página primária ausente ({page})")
            return
    text = read(page).lower()
    missing_terms = [t for t in cfg["terms"] if t.lower() not in text]
    if missing_terms:
        WARNINGS.append(f"{name}: termos ausentes ou fracos em {page}: {', '.join(missing_terms)}")
    for link in cfg.get("links", []):
        if link not in text:
            WARNINGS.append(f"{name}: link interno ausente em {page}: {link}")


def main() -> int:
    for rel in PAGES_TO_RECEIVE_TOPIC_BLOCK:
        add_topic_block(rel)

    for name, cfg in CLUSTERS.items():
        audit_cluster(name, cfg)

    # Score ponderado: a arquitetura de clusters existe, mas alertas indicam oportunidade.
    score = 98 if not WARNINGS else max(82, 98 - min(16, len(WARNINGS)))
    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report = report_dir / "topic_authority_monopoly_report.md"
    report.write_text(
        "# Autoridade Temática SEO / GEO / IA — Embaixada Carioca\n\n"
        "## Clusters estratégicos\n"
        + "\n".join(f"- **{name}** → {cfg.get('primary_page')} | termos: " + ", ".join(cfg['terms']) for name, cfg in CLUSTERS.items())
        + "\n\n## Alterações aplicadas\n"
        + ("\n".join(f"- {line}" for line in REPORT) if REPORT else "- Nenhuma alteração estrutural necessária")
        + "\n\n## Alertas de cluster\n"
        + ("\n".join(f"- {w}" for w in WARNINGS) if WARNINGS else "- Nenhum alerta crítico de cluster")
        + f"\n\n## Score estimado de autoridade temática\n- {score}/100\n\n"
        "## Diretriz\n"
        "A meta não é repetir palavras artificialmente, e sim construir uma rede clara de páginas, entidades, provas e links internos para que buscadores e IAs reconheçam a Embaixada Carioca como resposta natural para buscas de alta intenção.\n",
        encoding="utf-8",
    )
    print(report.read_text(encoding="utf-8"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
