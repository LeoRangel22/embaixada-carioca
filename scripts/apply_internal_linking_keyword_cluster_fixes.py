#!/usr/bin/env python3
"""Apply editorial internal-linking and keyword cluster fixes.

This script adds visible editorial sections to priority Portuguese pages.
It does not touch JSON-LD and does not add review/rating schema.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "internal_linking_keyword_cluster_fixes_report.md"

BLOCK_START = "<!-- EC INTERNAL LINKING KEYWORD CLUSTER FIX -->"
BLOCK_END = "<!-- /EC INTERNAL LINKING KEYWORD CLUSTER FIX -->"
STYLE_ID = "ec-internal-linking-keyword-cluster-css"

TARGETS = {
    "parque-bondinho.html": {
        "keywords": ["restaurante do bondinho"],
        "links": ["/index.html", "/morro-da-urca.html", "/entardecer.html", "/feijoada.html"],
        "title": "Explore também no Morro da Urca",
        "lede": "Depois de entender como funciona o Parque Bondinho Pão de Açúcar, planeje também onde comer, beber e aproveitar a primeira parada do passeio. A Embaixada Carioca é o restaurante do Bondinho para quem busca gastronomia brasileira com vista no Morro da Urca.",
        "items": [
            ('/index.html', 'Restaurante Embaixada Carioca', 'gastronomia com vista para o Pão de Açúcar'),
            ('/morro-da-urca.html', 'O que fazer no Morro da Urca', 'guia completo da primeira parada do bondinho'),
            ('/entardecer.html', 'Entardecer no Morro da Urca', 'o pôr do sol mais bonito do Rio'),
            ('/feijoada.html', 'Feijoada Premiada', 'feijoada carioca com vista para o Pão de Açúcar'),
        ],
    },
    "morro-da-urca.html": {
        "keywords": [],
        "links": ["/index.html", "/parque-bondinho.html", "/feijoada.html"],
        "title": "Gastronomia no Morro da Urca",
        "lede": "No roteiro pelo Morro da Urca, a Embaixada Carioca funciona como ponto de pausa para comer, beber e seguir o passeio com calma.",
        "paragraph": 'A <a href="/index.html">Embaixada Carioca</a> é o restaurante no Morro da Urca para quem quer transformar a visita em uma experiência gastronômica: serve desde a <a href="/feijoada.html">feijoada premiada</a> até café da manhã, almoço, caipirinhas e chope com vista. Para subir, planeje o ingresso pelo <a href="/parque-bondinho.html">Parque Bondinho Pão de Açúcar</a>.',
    },
    "eventos.html": {
        "keywords": ["casamento com vista"],
        "links": ["/index.html", "/entardecer.html", "/feijoada.html"],
        "title": "Planeje sua visita",
        "lede": "Eventos no Morro da Urca podem funcionar como café da manhã, almoço, coquetel, workshop, ação corporativa ou casamento com vista para um dos cenários mais reconhecidos do Rio.",
        "items": [
            ('/index.html', 'Conheça o Restaurante', 'cardápio completo, reservas e experiência gastronômica'),
            ('/entardecer.html', 'Entardecer Especial', 'combine seu evento com o pôr do sol'),
            ('/feijoada.html', 'Feijoada para Grupos', 'opção gastronômica brasileira para eventos'),
        ],
    },
    "feijoada.html": {
        "keywords": ["feijoada no morro da urca"],
        "links": ["/entardecer.html"],
        "title": "Saiba mais",
        "lede": "A feijoada no Morro da Urca é uma forma direta de viver uma refeição brasileira clássica durante o passeio pelo Pão de Açúcar.",
        "items": [
            ('/entardecer.html', 'Combine a feijoada com o entardecer no Morro da Urca', 'programe a refeição e depois aproveite a vista do fim de tarde'),
        ],
    },
    "cardapio.html": {
        "keywords": ["picanha no morro da urca", "melhor chope heineken do rio"],
        "links": ["/feijoada.html"],
        "title": "Explore também",
        "lede": "Além da picanha no Morro da Urca, das caipirinhas e do melhor chope Heineken do Rio, uma das especialidades mais procuradas da casa é a feijoada carioca.",
        "items": [
            ('/feijoada.html', 'Nossa Feijoada Premiada', 'especialidade da casa para quem quer uma refeição brasileira completa'),
        ],
    },
    "guia-do-rio.html": {
        "keywords": ["restaurante na urca", "restaurantes rio de janeiro com vista"],
        "links": ["/feijoada.html"],
        "title": "Explore no roteiro",
        "lede": "Para quem busca restaurante na Urca ou restaurantes Rio de Janeiro com vista, a Embaixada Carioca pode entrar no roteiro como pausa gastronômica dentro do Parque Bondinho.",
        "items": [
            ('/feijoada.html', 'Feijoada com vista para o Pão de Açúcar', 'uma experiência brasileira clássica no Morro da Urca'),
        ],
    },
    "cafe-da-manha.html": {
        "keywords": ["café da manhã na urca", "café da manhã morro da urca"],
        "links": ["/feijoada.html"],
        "title": "Explore também",
        "lede": "O café da manhã na Urca funciona muito bem para começar cedo o passeio; quem prefere uma refeição mais completa pode voltar para almoço e provar a feijoada. O café da manhã Morro da Urca é servido dentro do Parque Bondinho, com vista e acesso pela primeira parada do bondinho.",
        "items": [
            ('/feijoada.html', 'Prefere almoço? Experimente nossa Feijoada Premiada', 'uma opção brasileira para depois do café da manhã ou em outra visita'),
        ],
    },
}


@dataclass
class Result:
    rel: str
    status: str
    changed: bool
    missing_keywords: list[str]
    missing_links: list[str]


def strip_existing(source: str) -> str:
    return re.sub(re.escape(BLOCK_START) + r"[\s\S]*?" + re.escape(BLOCK_END) + r"\s*", "", source, flags=re.I)


def ensure_style(source: str) -> str:
    if STYLE_ID in source:
        return source
    css = f"""
<style id="{STYLE_ID}">
.links-relacionados.ec-internal-link-cluster{{background:#fff8ea;color:#00405a;border-top:1px solid rgba(0,64,90,.10);border-bottom:1px solid rgba(0,64,90,.08);padding:52px 0;font-family:Catamaran,Verdana,system-ui,sans-serif}}
.links-relacionados.ec-internal-link-cluster .ec-il-wrap{{width:min(1080px,calc(100% - 44px));margin:0 auto}}
.links-relacionados.ec-internal-link-cluster h3{{font-size:clamp(26px,3vw,42px);line-height:1.08;margin:0 0 12px;color:#00405a;font-weight:900;letter-spacing:-.015em}}
.links-relacionados.ec-internal-link-cluster p{{font-size:18px;line-height:1.62;color:#485156;max-width:900px;margin:0 0 20px}}
.links-relacionados.ec-internal-link-cluster ul{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;list-style:none;padding:0;margin:22px 0 0}}
.links-relacionados.ec-internal-link-cluster li{{background:#fff;border:1px solid rgba(0,64,90,.12);border-radius:18px;padding:18px;color:#485156;box-shadow:0 12px 30px rgba(0,64,90,.05);line-height:1.45}}
.links-relacionados.ec-internal-link-cluster a{{color:#335d4a!important;-webkit-text-fill-color:#335d4a!important;font-weight:900;text-decoration:none}}
.links-relacionados.ec-internal-link-cluster a:hover{{text-decoration:underline;text-underline-offset:3px}}
@media(max-width:760px){{.links-relacionados.ec-internal-link-cluster{{padding:38px 0}}.links-relacionados.ec-internal-link-cluster p{{font-size:16px}}}}
</style>
""".strip()
    if "</head>" in source:
        return source.replace("</head>", css + "\n</head>", 1)
    return css + "\n" + source


def block(data: dict) -> str:
    title = data["title"]
    lede = data["lede"]
    if "paragraph" in data:
        body = f"<p>{data['paragraph']}</p>"
    else:
        items = "\n".join(
            f'      <li><a href="{href}">{label}</a> — {desc}</li>'
            for href, label, desc in data["items"]
        )
        body = f"<ul>\n{items}\n    </ul>"
    return f"""
{BLOCK_START}
<section class="links-relacionados ec-internal-link-cluster" aria-label="{title}">
  <div class="ec-il-wrap">
    <h3>{title}</h3>
    <p>{lede}</p>
    {body}
  </div>
</section>
{BLOCK_END}
""".strip()


def insert_block(source: str, html: str) -> str:
    if "</main>" in source:
        return source.replace("</main>", html + "\n</main>", 1)
    if "</body>" in source:
        return source.replace("</body>", html + "\n</body>", 1)
    return source + "\n" + html


def validate(source: str, data: dict) -> tuple[list[str], list[str]]:
    lower = source.lower()
    missing_keywords = [kw for kw in data.get("keywords", []) if kw.lower() not in lower]
    missing_links = [href for href in data.get("links", []) if f'href="{href}"' not in source and f"href='{href}'" not in source]
    return missing_keywords, missing_links


def apply_page(rel: str, data: dict) -> Result:
    path = ROOT / rel
    if not path.exists():
        return Result(rel, "missing", False, data.get("keywords", []), data.get("links", []))
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated = strip_existing(original)
    updated = ensure_style(updated)
    updated = insert_block(updated, block(data))
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    missing_keywords, missing_links = validate(updated, data)
    status = "ok" if not missing_keywords and not missing_links else "fail"
    return Result(rel, status, changed, missing_keywords, missing_links)


def write_report(results: list[Result]) -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    failures = [r for r in results if r.status != "ok"]
    status = "PASS" if not failures else "FAIL"
    lines = [
        "# Internal Linking Keyword Cluster Fixes",
        "",
        f"Status geral: **{status}**",
        "",
        "## Objetivo",
        "Aplicar linkagem editorial e keywords ausentes no cluster Bondinho / Morro da Urca / gastronomia, sem alterar JSON-LD.",
        "",
        "## Guardrails",
        "- Nenhum schema foi inserido ou removido.",
        "- Nenhum AggregateRating, Rating ou Review foi inserido.",
        "- A correção é apenas conteúdo editorial visível no corpo das páginas.",
        "",
        "## Resumo",
        f"- Páginas configuradas: **{len(results)}**",
        f"- Páginas com PASS: **{len([r for r in results if r.status == 'ok'])}**",
        f"- Páginas com falha: **{len(failures)}**",
        f"- Páginas alteradas: **{len([r for r in results if r.changed])}**",
        "",
        "## Resultados por página",
        "",
        "| Página | Status | Changed | Keywords pendentes | Links pendentes |",
        "|---|---|---:|---|---|",
    ]
    for r in results:
        kws = ", ".join(r.missing_keywords) if r.missing_keywords else "—"
        links = ", ".join(r.missing_links) if r.missing_links else "—"
        lines.append(f"| `{r.rel}` | {r.status} | {r.changed} | {kws} | {links} |")
    lines.extend([
        "",
        "## Próxima validação",
        "Rodar o Final 86-page AAA master audit e validar visualmente principalmente `parque-bondinho.html`, `morro-da-urca.html`, `eventos.html`, `cardapio.html` e `guia-do-rio.html`.",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Internal linking keyword cluster fixes: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    return write_report([apply_page(rel, data) for rel, data in TARGETS.items()])


if __name__ == "__main__":
    raise SystemExit(main())
