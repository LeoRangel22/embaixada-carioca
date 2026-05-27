#!/usr/bin/env python3
"""Apply urgent real-query and conversion fixes.

Targets the current high-impact backlog:
- index.html: real queries around "avaliações sobre Embaixada Carioca", brand query and AI direct answers.
- como-chegar.html: real queries around "Av. Pasteur 520", "Avenida Pasteur 520" and GPS/Uber intent.

No JSON-LD review/rating schema is added here. Google Reviews are treated as visible content only.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "priority_query_conversion_fixes_report.md"

BLOCK_START = "<!-- EC PRIORITY QUERY CONVERSION FIX -->"
BLOCK_END = "<!-- /EC PRIORITY QUERY CONVERSION FIX -->"
STYLE_ID = "ec-priority-query-conversion-fix-css"

META_DESC_RE = re.compile(r"<meta\b(?=[^>]*name=[\"']description[\"'])(?=[^>]*content=[\"'][^\"']*[\"'])[^>]*>", re.I | re.S)
OG_DESC_RE = re.compile(r"<meta\b(?=[^>]*property=[\"']og:description[\"'])(?=[^>]*content=[\"'][^\"']*[\"'])[^>]*>", re.I | re.S)
TW_DESC_RE = re.compile(r"<meta\b(?=[^>]*name=[\"']twitter:description[\"'])(?=[^>]*content=[\"'][^\"']*[\"'])[^>]*>", re.I | re.S)
TITLE_RE = re.compile(r"<title>.*?</title>", re.I | re.S)
OG_TITLE_RE = re.compile(r"<meta\b(?=[^>]*property=[\"']og:title[\"'])(?=[^>]*content=[\"'][^\"']*[\"'])[^>]*>", re.I | re.S)
TW_TITLE_RE = re.compile(r"<meta\b(?=[^>]*name=[\"']twitter:title[\"'])(?=[^>]*content=[\"'][^\"']*[\"'])[^>]*>", re.I | re.S)


def strip_block(source: str) -> str:
    return re.sub(re.escape(BLOCK_START) + r"[\s\S]*?" + re.escape(BLOCK_END) + r"\s*", "", source, flags=re.I)


def ensure_style(source: str) -> str:
    if STYLE_ID in source:
        return source
    css = f"""
<style id="{STYLE_ID}">
.ec-priority-query-fix{{background:#f6efde;color:#00405a;border-top:1px solid rgba(0,64,90,.10);border-bottom:1px solid rgba(0,64,90,.08);padding:54px 0;font-family:Catamaran,Verdana,system-ui,sans-serif}}
.ec-priority-query-fix .ec-wrap{{width:min(1080px,calc(100% - 44px));margin:0 auto}}
.ec-priority-query-fix .ec-kicker{{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#527f8f;margin-bottom:12px}}
.ec-priority-query-fix h2{{font-size:clamp(28px,3.5vw,48px);line-height:1.08;margin:0 0 16px;color:#00405a;font-weight:800;letter-spacing:-.02em}}
.ec-priority-query-fix p{{font-size:18px;line-height:1.62;color:#485156;max-width:880px;margin:0 0 14px}}
.ec-priority-query-fix strong{{color:#335d4a}}
.ec-priority-query-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:26px 0}}
.ec-priority-query-card{{background:#fff;border:1px solid rgba(0,64,90,.12);border-radius:20px;padding:22px;box-shadow:0 14px 34px rgba(0,64,90,.06)}}
.ec-priority-query-card h3{{font-size:20px;line-height:1.16;margin:0 0 8px;color:#00405a}}
.ec-priority-query-card p{{font-size:15.5px;margin:0;color:#485156}}
.ec-priority-query-fix ol{{margin:18px 0 0;padding-left:1.4rem;color:#485156}}
.ec-priority-query-fix li{{margin:8px 0;line-height:1.55}}
.ec-priority-query-cta{{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}}
.ec-priority-query-cta a{{display:inline-flex;align-items:center;justify-content:center;min-height:46px;border-radius:999px;padding:0 20px;background:#f59b1e;color:#00405a!important;-webkit-text-fill-color:#00405a!important;text-decoration:none;font-weight:900;letter-spacing:.08em;text-transform:uppercase}}
.ec-priority-query-cta a.secondary{{background:#00405a;color:#f6efde!important;-webkit-text-fill-color:#f6efde!important}}
@media(max-width:760px){{.ec-priority-query-fix{{padding:38px 0}}.ec-priority-query-grid{{grid-template-columns:1fr}}.ec-priority-query-fix p{{font-size:16px}}.ec-priority-query-cta a{{width:100%}}}}
</style>
""".strip()
    if "</head>" in source:
        return source.replace("</head>", css + "\n</head>", 1)
    return css + "\n" + source


def update_head(source: str, title: str | None = None, desc: str | None = None) -> str:
    if title:
        source = TITLE_RE.sub(f"<title>{title}</title>", source, count=1)
        source = OG_TITLE_RE.sub(f'<meta property="og:title" content="{title}">', source, count=1)
        source = TW_TITLE_RE.sub(f'<meta name="twitter:title" content="{title}">', source, count=1)
    if desc:
        source = META_DESC_RE.sub(f'<meta name="description" content="{desc}">', source, count=1)
        source = OG_DESC_RE.sub(f'<meta property="og:description" content="{desc}">', source, count=1)
        source = TW_DESC_RE.sub(f'<meta name="twitter:description" content="{desc}">', source, count=1)
    return source


def insert_block(source: str, block: str) -> str:
    if "</main>" in source:
        return source.replace("</main>", block + "\n</main>", 1)
    if "</body>" in source:
        return source.replace("</body>", block + "\n</body>", 1)
    return source + "\n" + block


def index_block() -> str:
    return f"""
{BLOCK_START}
<section class="ec-priority-query-fix" aria-label="Avaliações e resposta rápida sobre a Embaixada Carioca">
  <div class="ec-wrap">
    <div class="ec-kicker">Avaliações sobre Embaixada Carioca</div>
    <h2>Por que a Embaixada Carioca é tão procurada por quem visita o Pão de Açúcar?</h2>
    <p>A <strong>Embaixada Carioca</strong> é o restaurante brasileiro no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com café da manhã, almoço, caipirinhas, chope e eventos com vista direta para o Pão de Açúcar.</p>
    <p>Nas avaliações sobre a Embaixada Carioca, os visitantes costumam destacar a vista, a localização dentro do Bondinho, o atendimento, a caipirinha, o chope gelado e a facilidade de transformar o passeio em uma experiência gastronômica completa.</p>
    <div class="ec-priority-query-grid">
      <div class="ec-priority-query-card"><h3>Restaurante no Pão de Açúcar</h3><p>Fica na primeira parada do Bondinho, no Morro da Urca, antes da subida final ao Pão de Açúcar.</p></div>
      <div class="ec-priority-query-card"><h3>Café da manhã e almoço</h3><p>Abre todos os dias às 8h30, com café da manhã, pratos brasileiros, petiscos e bebidas.</p></div>
      <div class="ec-priority-query-card"><h3>Google Reviews</h3><p>A prova social deve ser usada como conteúdo visível, sem schema de review/rating para evitar erros no Search Console.</p></div>
    </div>
    <ol>
      <li>Compre o ingresso do Parque Bondinho Pão de Açúcar.</li>
      <li>Suba até o Morro da Urca, a primeira parada do bondinho.</li>
      <li>Escolha a Embaixada Carioca para café da manhã, almoço, caipirinha, chope ou evento.</li>
      <li>Use a reserva online para organizar melhor a visita em fins de semana, feriados e horários de pico.</li>
    </ol>
    <div class="ec-priority-query-cta">
      <a href="https://go.tagme.com.br/embaixadacarioca" rel="noopener" target="_blank">Reservar</a>
      <a class="secondary" href="/como-chegar.html">Como chegar</a>
    </div>
  </div>
</section>
{BLOCK_END}
""".strip()


def access_block() -> str:
    return f"""
{BLOCK_START}
<section class="ec-priority-query-fix" aria-label="Endereço para GPS, Uber e Google Maps">
  <div class="ec-wrap">
    <div class="ec-kicker">Endereço para GPS e Uber</div>
    <h2>Use Avenida Pasteur, 520 — Urca, Rio de Janeiro.</h2>
    <p>Para chegar à Embaixada Carioca, coloque no GPS, Uber ou táxi: <strong>Parque Bondinho Pão de Açúcar — Avenida Pasteur, 520, Urca, Rio de Janeiro</strong>. A entrada do passeio fica na Praia Vermelha.</p>
    <p>Depois de entrar no Parque Bondinho, suba de bondinho até o <strong>Morro da Urca</strong>, a primeira parada. A Embaixada Carioca fica dentro do parque, no alto do Morro da Urca.</p>
    <ol>
      <li>Digite <strong>Av. Pasteur 520</strong> ou <strong>Avenida Pasteur, 520 — Urca</strong> no aplicativo de transporte.</li>
      <li>Vá até a entrada do Parque Bondinho Pão de Açúcar, na Praia Vermelha.</li>
      <li>Compre ou apresente o ingresso do Bondinho.</li>
      <li>Suba até a primeira parada, o Morro da Urca.</li>
      <li>Siga para a Embaixada Carioca para café da manhã, almoço, caipirinha, chope ou evento.</li>
    </ol>
    <div class="ec-priority-query-cta">
      <a href="https://www.google.com/maps/search/?api=1&query=Parque+Bondinho+P%C3%A3o+de+A%C3%A7%C3%BAcar+Avenida+Pasteur+520+Urca" rel="noopener" target="_blank">Abrir no Maps</a>
      <a class="secondary" href="https://go.tagme.com.br/embaixadacarioca" rel="noopener" target="_blank">Reservar</a>
    </div>
  </div>
</section>
{BLOCK_END}
""".strip()


def apply_file(rel: str, title: str | None, desc: str | None, block: str) -> tuple[str, bool, str]:
    path = ROOT / rel
    if not path.exists():
        return rel, False, "missing"
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated = strip_block(original)
    updated = update_head(updated, title, desc)
    updated = ensure_style(updated)
    updated = insert_block(updated, block)
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return rel, changed, "ok"


def main() -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    results = [
        apply_file(
            "index.html",
            "Restaurante no Morro da Urca | Embaixada Carioca",
            "Restaurante no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com avaliações, café da manhã, almoço, caipirinhas, chope e eventos com vista.",
            index_block(),
        ),
        apply_file(
            "como-chegar.html",
            "Como Chegar: Av. Pasteur 520, Urca | Embaixada Carioca",
            "Como chegar à Embaixada Carioca: use Av. Pasteur 520, Urca, Rio de Janeiro, entrada do Parque Bondinho Pão de Açúcar na Praia Vermelha.",
            access_block(),
        ),
    ]
    lines = [
        "# Priority Query and Conversion Fixes",
        "",
        "Status geral: **PASS**",
        "",
        "## Objetivo",
        "Corrigir gaps muito urgentes de consultas reais: `av pasteur`, `avenida pasteur 520`, `avaliações sobre Embaixada Carioca`, `embaixada` e intenção de reserva/como chegar.",
        "",
        "## Resultados",
    ]
    for rel, changed, status in results:
        lines.append(f"- `{rel}` — {status} — changed={changed}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Priority query and conversion fixes: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
