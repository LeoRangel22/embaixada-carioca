#!/usr/bin/env python3
"""Add visible ordered lists for featured-snippet/AIO coverage.

This script intentionally does NOT touch JSON-LD. It only adds visible <ol>
sections to priority commercial pages, avoiding duplicate FAQPage/Restaurant schema
and preserving the GSC structured-data fixes.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "featured_snippet_ordered_lists_report.md"

BLOCK_START = "<!-- EC FEATURED SNIPPET ORDERED LISTS -->"
BLOCK_END = "<!-- /EC FEATURED SNIPPET ORDERED LISTS -->"
STYLE_ID = "ec-featured-snippet-ordered-lists-css"

PRODUCT_PAGES = [
    "index.html",
    "cafe-da-manha.html",
    "almoco.html",
    "cardapio.html",
    "entardecer.html",
    "eventos.html",
    "feijoada.html",
    "como-chegar.html",
    "guia-do-rio.html",
    "restaurante-morro-da-urca.html",
    "morro-da-urca.html",
    "en/index.html",
    "en/cafe-da-manha.html",
    "en/almoco.html",
    "en/cardapio.html",
    "en/sunset.html",
    "en/eventos.html",
    "en/feijoada.html",
    "en/how-to-get-there.html",
    "en/morro-da-urca.html",
    "es/index.html",
    "es/cafe-da-manha.html",
    "es/almoco.html",
    "es/cardapio.html",
    "es/atardecer.html",
    "es/eventos.html",
    "es/feijoada.html",
    "es/como-llegar.html",
    "es/morro-da-urca.html",
]


@dataclass
class Result:
    rel: str
    status: str
    changed: bool
    ol_count_after: int


def language_for(rel: str) -> str:
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt"


def page_kind(rel: str) -> str:
    stem = Path(rel).stem.lower()
    if "cafe" in stem:
        return "breakfast"
    if "almoco" in stem:
        return "lunch"
    if "cardapio" in stem:
        return "menu"
    if "entardecer" in stem or "sunset" in stem or "atardecer" in stem:
        return "sunset"
    if "evento" in stem:
        return "events"
    if "feijoada" in stem:
        return "feijoada"
    if "como-chegar" in stem or "how-to-get-there" in stem or "como-llegar" in stem:
        return "access"
    if "guia" in stem:
        return "guide"
    if "morro" in stem or "restaurante-morro" in stem:
        return "morro"
    return "home"


def strip_existing(source: str) -> str:
    return re.sub(re.escape(BLOCK_START) + r"[\s\S]*?" + re.escape(BLOCK_END) + r"\s*", "", source, flags=re.I)


def ensure_style(source: str) -> str:
    if STYLE_ID in source:
        return source
    css = f"""
<style id="{STYLE_ID}">
.ec-featured-snippet-ol{{background:#fff8ea;color:#00405a;border-top:1px solid rgba(0,64,90,.10);border-bottom:1px solid rgba(0,64,90,.08);padding:56px 0;font-family:Catamaran,Verdana,system-ui,sans-serif}}
.ec-featured-snippet-ol .ec-fs-wrap{{width:min(1080px,calc(100% - 44px));margin:0 auto}}
.ec-featured-snippet-ol .ec-fs-kicker{{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#527f8f;margin-bottom:12px}}
.ec-featured-snippet-ol h2{{font-size:clamp(28px,3.4vw,48px);line-height:1.08;margin:0 0 16px;color:#00405a;font-weight:800;letter-spacing:-.02em}}
.ec-featured-snippet-ol p{{font-size:18px;line-height:1.62;color:#485156;max-width:880px;margin:0 0 18px}}
.ec-featured-snippet-ol ol{{counter-reset:item;margin:20px 0 0;padding:0;display:grid;gap:12px;list-style:none}}
.ec-featured-snippet-ol li{{display:grid;grid-template-columns:42px 1fr;gap:14px;align-items:start;background:#fff;border:1px solid rgba(0,64,90,.12);border-radius:18px;padding:18px;line-height:1.5;color:#485156;box-shadow:0 12px 32px rgba(0,64,90,.05)}}
.ec-featured-snippet-ol li::before{{counter-increment:item;content:counter(item);display:grid;place-items:center;width:34px;height:34px;border-radius:999px;background:#f59b1e;color:#00405a;font-weight:900;font-family:'JetBrains Mono',ui-monospace,monospace}}
.ec-featured-snippet-ol strong{{color:#335d4a}}
@media(max-width:760px){{.ec-featured-snippet-ol{{padding:40px 0}}.ec-featured-snippet-ol p{{font-size:16px}}.ec-featured-snippet-ol li{{grid-template-columns:36px 1fr;padding:15px}}}}
</style>
""".strip()
    if "</head>" in source:
        return source.replace("</head>", css + "\n</head>", 1)
    return css + "\n" + source


def block(rel: str) -> str:
    lang = language_for(rel)
    kind = page_kind(rel)

    content = {
        "pt": {
            "home": ("Como aproveitar a Embaixada Carioca no Pão de Açúcar", "Use este roteiro simples para transformar a visita ao Bondinho em uma experiência gastronômica completa.", ["Compre ou apresente o ingresso do <strong>Parque Bondinho Pão de Açúcar</strong>.", "Suba até o <strong>Morro da Urca</strong>, a primeira parada do bondinho.", "Escolha café da manhã, almoço, caipirinha, chope ou petiscos conforme o horário da visita.", "Faça reserva online em fins de semana, feriados e horários de maior movimento."]),
            "breakfast": ("Como tomar café da manhã com vista no Morro da Urca", "Passo a passo para organizar o café da manhã na Embaixada Carioca.", ["Chegue cedo ao Parque Bondinho, na Av. Pasteur, 520 — Urca.", "Suba no primeiro trecho do bondinho até o Morro da Urca.", "Siga para a Embaixada Carioca e peça o café da manhã servido todos os dias.", "Reserve antes em fins de semana e feriados para reduzir espera."]),
            "lunch": ("Como almoçar na Embaixada Carioca", "O almoço funciona melhor quando a visita é planejada junto com o passeio pelo Pão de Açúcar.", ["Suba ao Morro da Urca pelo Bondinho Pão de Açúcar.", "Planeje o almoço entre o fim da manhã e o meio da tarde.", "Peça pratos brasileiros, como picanha, feijoada, bobó, petiscos e caipirinhas.", "Use a reserva online para grupos, famílias e horários de pico."]),
            "menu": ("Como escolher no cardápio", "Uma forma direta de decidir o pedido de acordo com o momento da visita.", ["Comece pela <strong>caipirinha da casa</strong> ou pelo chope gelado.", "Para compartilhar, escolha petiscos brasileiros e entradas clássicas.", "Para prato principal, priorize picanha, feijoada, bobó ou pratos do dia.", "Finalize com café ou sobremesa antes de seguir o passeio pelo parque."]),
            "sunset": ("Como aproveitar o entardecer no Morro da Urca", "O entardecer combina melhor com bebida, petiscos e tempo livre para apreciar a vista.", ["Chegue ao Morro da Urca no meio da tarde.", "Escolha uma mesa com vista e peça caipirinha, chope ou drink do dia.", "Combine com petiscos para compartilhar.", "Fique atento ao horário do último bondinho e ao funcionamento do parque."]),
            "events": ("Como solicitar um evento no Morro da Urca", "O orçamento fica mais preciso quando as informações essenciais chegam completas.", ["Informe data, horário e número estimado de convidados.", "Escolha o formato: café da manhã, almoço, welcome drink, coquetel, workshop ou experiência.", "Envie necessidades especiais de montagem, audiovisual, troféus, brindes ou roteiro do grupo.", "Aguarde a proposta e confirme o evento com pagamento do sinal."]),
            "feijoada": ("Como pedir feijoada no Morro da Urca", "A feijoada é uma escolha forte para quem quer uma refeição brasileira clássica durante o passeio.", ["Suba ao Morro da Urca pelo Parque Bondinho.", "Confirme a disponibilidade da feijoada do dia com a equipe.", "Peça acompanhamentos e bebidas brasileiras, como caipirinha ou chope.", "Reserve antes para grupos e horários de maior movimento."]),
            "access": ("Como chegar à Embaixada Carioca", "Use este passo a passo para evitar erro no GPS e chegar diretamente ao Parque Bondinho.", ["Digite <strong>Av. Pasteur, 520 — Urca, Rio de Janeiro</strong> no GPS ou aplicativo de transporte.", "Vá até a entrada do Parque Bondinho Pão de Açúcar, na Praia Vermelha.", "Compre ou apresente o ingresso do Bondinho.", "Suba até o Morro da Urca, a primeira parada, onde fica a Embaixada Carioca."]),
            "guide": ("Como encaixar a Embaixada Carioca no roteiro do Rio", "A visita funciona bem como pausa gastronômica dentro de um roteiro pela Urca e pelo Pão de Açúcar.", ["Comece pela Praia Vermelha ou pela chegada ao Parque Bondinho.", "Suba ao Morro da Urca e pare para café da manhã, almoço ou drinks.", "Continue o passeio até o Pão de Açúcar.", "Depois, siga para outros pontos próximos da Urca ou Botafogo."]),
            "morro": ("Como visitar o restaurante no Morro da Urca", "O acesso depende do Parque Bondinho, por isso o planejamento do ingresso é essencial.", ["Vá até a Av. Pasteur, 520, na Urca.", "Entre no Parque Bondinho Pão de Açúcar.", "Suba até a primeira parada, o Morro da Urca.", "Procure a Embaixada Carioca para comer, beber ou realizar eventos com vista."]),
        },
        "en": {
            "home": ("How to visit Embaixada Carioca at Sugarloaf", "Use this quick route to combine the cable car visit with a Brazilian food experience.", ["Buy or present your ticket to <strong>Sugarloaf Cable Car Park</strong>.", "Ride to <strong>Morro da Urca</strong>, the first cable car stop.", "Choose breakfast, lunch, caipirinhas, draft beer or snacks depending on your schedule.", "Book online on weekends, holidays and peak hours."]),
            "breakfast": ("How to have breakfast with a view at Morro da Urca", "A simple plan for breakfast at Embaixada Carioca.", ["Arrive early at Sugarloaf Cable Car Park, Av. Pasteur, 520 — Urca.", "Take the first cable car section to Morro da Urca.", "Go to Embaixada Carioca and order breakfast, served every day.", "Book ahead on weekends and holidays to reduce waiting time."]),
            "lunch": ("How to have lunch at Embaixada Carioca", "Lunch works best when planned together with the Sugarloaf visit.", ["Take the cable car to Morro da Urca.", "Plan lunch from late morning to mid-afternoon.", "Order Brazilian dishes such as steak, feijoada, shrimp stew, snacks and caipirinhas.", "Use online booking for groups, families and peak hours."]),
            "menu": ("How to choose from the menu", "A direct way to order according to the moment of your visit.", ["Start with the house caipirinha or a cold draft beer.", "For sharing, choose Brazilian snacks and classic starters.", "For the main course, prioritize steak, feijoada, shrimp stew or daily specials.", "Finish with coffee or dessert before continuing through the park."]),
            "sunset": ("How to enjoy sunset at Morro da Urca", "Sunset works best with drinks, snacks and time to enjoy the view.", ["Arrive at Morro da Urca in the afternoon.", "Choose a table with a view and order a caipirinha, draft beer or cocktail.", "Pair it with snacks to share.", "Check the last cable car time and park schedule."]),
            "events": ("How to request an event at Morro da Urca", "The proposal is more accurate when the essential information is complete.", ["Send date, time and estimated number of guests.", "Choose the format: breakfast, lunch, welcome drink, cocktail, workshop or experience.", "Share setup, audiovisual, awards, gifts or group schedule needs.", "Review the proposal and confirm the event with the deposit."]),
            "feijoada": ("How to order feijoada at Morro da Urca", "Feijoada is a strong choice for a classic Brazilian meal during the visit.", ["Take the cable car to Morro da Urca.", "Check the day's feijoada availability with the team.", "Order Brazilian drinks such as caipirinha or draft beer.", "Book ahead for groups and peak hours."]),
            "access": ("How to get to Embaixada Carioca", "Use this route to avoid GPS mistakes and arrive at Sugarloaf Cable Car Park.", ["Enter <strong>Av. Pasteur, 520 — Urca, Rio de Janeiro</strong> in your GPS or ride app.", "Go to the Sugarloaf Cable Car Park entrance at Praia Vermelha.", "Buy or present your cable car ticket.", "Ride to Morro da Urca, the first stop, where Embaixada Carioca is located."]),
            "morro": ("How to visit the restaurant at Morro da Urca", "Access is through the Sugarloaf Cable Car Park, so ticket planning is essential.", ["Go to Av. Pasteur, 520, in Urca.", "Enter Sugarloaf Cable Car Park.", "Ride to the first stop, Morro da Urca.", "Find Embaixada Carioca for food, drinks or private events with a view."]),
        },
        "es": {
            "home": ("Cómo visitar Embaixada Carioca en el Pan de Azúcar", "Use esta ruta simple para combinar el paseo en bondinho con una experiencia gastronómica brasileña.", ["Compre o presente su entrada al <strong>Parque Bondinho Pão de Açúcar</strong>.", "Suba hasta el <strong>Morro da Urca</strong>, la primera parada del bondinho.", "Elija desayuno, almuerzo, caipirinhas, chopp o aperitivos según el horario de la visita.", "Reserve online en fines de semana, feriados y horarios de mayor movimiento."]),
            "breakfast": ("Cómo desayunar con vista en el Morro da Urca", "Un plan simple para desayunar en Embaixada Carioca.", ["Llegue temprano al Parque Bondinho, Av. Pasteur, 520 — Urca.", "Suba en el primer tramo del bondinho hasta el Morro da Urca.", "Vaya a Embaixada Carioca y pida el desayuno, servido todos los días.", "Reserve antes en fines de semana y feriados para reducir la espera."]),
            "lunch": ("Cómo almorzar en Embaixada Carioca", "El almuerzo funciona mejor cuando se planifica junto con la visita al Pan de Azúcar.", ["Suba al Morro da Urca por el Bondinho Pão de Açúcar.", "Planifique el almuerzo entre el final de la mañana y la media tarde.", "Pida platos brasileños como picanha, feijoada, bobó, aperitivos y caipirinhas.", "Use la reserva online para grupos, familias y horarios de pico."]),
            "menu": ("Cómo elegir en el menú", "Una forma directa de decidir el pedido según el momento de la visita.", ["Empiece con la caipirinha de la casa o un chopp frío.", "Para compartir, elija aperitivos brasileños y entradas clásicas.", "Como plato principal, priorice picanha, feijoada, bobó o platos del día.", "Termine con café o postre antes de seguir el paseo por el parque."]),
            "sunset": ("Cómo disfrutar el atardecer en el Morro da Urca", "El atardecer combina mejor con bebidas, aperitivos y tiempo para disfrutar la vista.", ["Llegue al Morro da Urca por la tarde.", "Elija una mesa con vista y pida caipirinha, chopp o un cóctel.", "Combine con aperitivos para compartir.", "Verifique el horario del último bondinho y el funcionamiento del parque."]),
            "events": ("Cómo solicitar un evento en el Morro da Urca", "El presupuesto queda más preciso cuando la información esencial llega completa.", ["Informe fecha, horario y número estimado de invitados.", "Elija el formato: desayuno, almuerzo, welcome drink, cóctel, workshop o experiencia.", "Envíe necesidades de montaje, audiovisual, trofeos, regalos o agenda del grupo.", "Revise la propuesta y confirme el evento con el pago de la señal."]),
            "feijoada": ("Cómo pedir feijoada en el Morro da Urca", "La feijoada es una buena opción para una comida brasileña clásica durante el paseo.", ["Suba al Morro da Urca por el Parque Bondinho.", "Confirme la disponibilidad de la feijoada del día con el equipo.", "Pida bebidas brasileñas, como caipirinha o chopp.", "Reserve antes para grupos y horarios de mayor movimiento."]),
            "access": ("Cómo llegar a Embaixada Carioca", "Use este paso a paso para evitar errores en el GPS y llegar directamente al Parque Bondinho.", ["Digite <strong>Av. Pasteur, 520 — Urca, Rio de Janeiro</strong> en el GPS o aplicación de transporte.", "Vaya a la entrada del Parque Bondinho Pão de Açúcar, en Praia Vermelha.", "Compre o presente su entrada del Bondinho.", "Suba hasta Morro da Urca, la primera parada, donde está Embaixada Carioca."]),
            "morro": ("Cómo visitar el restaurante en Morro da Urca", "El acceso depende del Parque Bondinho, por eso planificar la entrada es esencial.", ["Vaya a Av. Pasteur, 520, en Urca.", "Entre al Parque Bondinho Pão de Açúcar.", "Suba hasta la primera parada, Morro da Urca.", "Busque Embaixada Carioca para comer, beber o realizar eventos con vista."]),
        },
    }
    lang_content = content[lang]
    title, lede, items = lang_content.get(kind, lang_content.get("home"))
    li = "\n".join(f"      <li>{item}</li>" for item in items)
    kicker = {"pt": "Passo a passo", "en": "Step by step", "es": "Paso a paso"}[lang]
    return f"""
{BLOCK_START}
<section class="ec-featured-snippet-ol" aria-label="{title}">
  <div class="ec-fs-wrap">
    <div class="ec-fs-kicker">{kicker}</div>
    <h2>{title}</h2>
    <p>{lede}</p>
    <ol>
{li}
    </ol>
  </div>
</section>
{BLOCK_END}
""".strip()


def insert_before_close(source: str, html: str) -> str:
    if "</main>" in source:
        return source.replace("</main>", html + "\n</main>", 1)
    if "</body>" in source:
        return source.replace("</body>", html + "\n</body>", 1)
    return source + "\n" + html


def count_ol(source: str) -> int:
    return len(re.findall(r"<ol\b", source, flags=re.I))


def apply_page(rel: str) -> Result:
    path = ROOT / rel
    if not path.exists():
        return Result(rel, "missing", False, 0)
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated = strip_existing(original)
    updated = ensure_style(updated)
    updated = insert_before_close(updated, block(rel))
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return Result(rel, "ok", changed, count_ol(updated))


def write_report(results: list[Result]) -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    ok = [r for r in results if r.status == "ok"]
    missing = [r for r in results if r.status != "ok"]
    changed = [r for r in ok if r.changed]
    without_ol = [r for r in ok if r.ol_count_after < 1]
    status = "PASS" if not without_ol else "FAIL"
    lines = [
        "# Featured Snippet Ordered Lists",
        "",
        f"Status geral: **{status}**",
        "",
        "## Objetivo",
        "Adicionar listas ordenadas visíveis (`<ol>`) em páginas comerciais prioritárias para Featured Snippets, AIO/GEO e respostas diretas, sem alterar JSON-LD.",
        "",
        "## Guardrails",
        "- Nenhum FAQPage ou Restaurant schema foi inserido por este script.",
        "- Nenhum AggregateRating, Rating ou Review foi inserido.",
        "- A melhoria é apenas conteúdo visível no corpo da página.",
        "",
        "## Resumo",
        f"- Páginas configuradas: **{len(results)}**",
        f"- Páginas existentes processadas: **{len(ok)}**",
        f"- Páginas alteradas: **{len(changed)}**",
        f"- Páginas inexistentes/SKIP: **{len(missing)}**",
        f"- Páginas processadas sem `<ol>` após execução: **{len(without_ol)}**",
        "",
        "## Resultados por página",
        "",
        "| Página | Status | Changed | OL após execução |",
        "|---|---|---:|---:|",
    ]
    for r in results:
        lines.append(f"| `{r.rel}` | {r.status} | {r.changed} | {r.ol_count_after} |")
    if missing:
        lines.extend(["", "## SKIPs", ""])
        for r in missing:
            lines.append(f"- `{r.rel}` — {r.status}")
    lines.extend([
        "",
        "## Próxima validação",
        "Rodar o Final 86-page AAA master audit e conferir visualmente as páginas principais antes de avançar para extração de CSS/JS.",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Featured snippet ordered lists: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    return write_report([apply_page(rel) for rel in PRODUCT_PAGES])


if __name__ == "__main__":
    raise SystemExit(main())
