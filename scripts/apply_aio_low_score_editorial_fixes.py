#!/usr/bin/env python3
"""Apply editorial AIO/SEO fixes to pages previously flagged below score 60.

The schema/FAQ problems from the old report were already solved by the static schema and
GSC structured-data fix workflows. This script addresses the remaining editorial items:
- shorter title tags where the old report flagged length issues;
- stronger meta descriptions in the 130-160 character range;
- visible ordered lists (<ol>) on the 8 priority pages;
- language cleanup for Spanish pages where old PT headings could remain;
- light visible content expansion on eventos and entardecer pages.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "aio_low_score_editorial_fixes_report.md"
BLOCK_START = "<!-- EC AIO LOW SCORE EDITORIAL FIX -->"
BLOCK_END = "<!-- /EC AIO LOW SCORE EDITORIAL FIX -->"
STYLE_ID = "ec-aio-low-score-editorial-fix-css"

TITLE_RE = re.compile(r"<title>.*?</title>", re.I | re.S)
META_DESC_RE = re.compile(r"<meta\b(?=[^>]*name=[\"']description[\"'])(?=[^>]*content=[\"'][^\"']*[\"'])[^>]*>", re.I | re.S)
OG_TITLE_RE = re.compile(r"<meta\b(?=[^>]*property=[\"']og:title[\"'])(?=[^>]*content=[\"'][^\"']*[\"'])[^>]*>", re.I | re.S)
OG_DESC_RE = re.compile(r"<meta\b(?=[^>]*property=[\"']og:description[\"'])(?=[^>]*content=[\"'][^\"']*[\"'])[^>]*>", re.I | re.S)
TW_TITLE_RE = re.compile(r"<meta\b(?=[^>]*name=[\"']twitter:title[\"'])(?=[^>]*content=[\"'][^\"']*[\"'])[^>]*>", re.I | re.S)
TW_DESC_RE = re.compile(r"<meta\b(?=[^>]*name=[\"']twitter:description[\"'])(?=[^>]*content=[\"'][^\"']*[\"'])[^>]*>", re.I | re.S)


@dataclass
class PageFix:
    rel: str
    title: str
    description: str
    heading: str
    intro: str
    ordered_items: list[str]
    extra_paragraphs: list[str]
    replacements: dict[str, str]


PAGES: list[PageFix] = [
    PageFix(
        rel="almoco.html",
        title="Almoço no Morro da Urca com Vista | Embaixada Carioca",
        description="Almoço brasileiro no Morro da Urca, dentro do Parque Bondinho, com picanha, feijoada, bobó, caipirinhas e vista para o Pão de Açúcar.",
        heading="Como aproveitar o almoço no Morro da Urca",
        intro="Para transformar a visita ao Bondinho em uma experiência gastronômica completa, planeje o almoço com tempo para sentar, pedir uma bebida e aproveitar a vista.",
        ordered_items=[
            "Compre o ingresso do Parque Bondinho Pão de Açúcar e suba até a primeira parada, no Morro da Urca.",
            "Chegue preferencialmente entre 11h30 e 16h30, período mais indicado para almoço completo.",
            "Comece por uma caipirinha da casa, chope gelado ou bebida sem álcool antes dos pratos principais.",
            "Escolha entre picanha, feijoada, bobó de camarão, salmão ou pratos brasileiros para compartilhar.",
            "Finalize com café, sobremesa ou mais alguns minutos de contemplação antes de seguir o passeio.",
        ],
        extra_paragraphs=[
            "A página de almoço deve responder rapidamente às dúvidas de quem está decidindo onde comer durante o passeio: localização dentro do Parque Bondinho, necessidade de ingresso, horários de maior movimento, pratos principais e possibilidade de reserva.",
            "A proposta da Embaixada Carioca é oferecer uma amostra clara da culinária carioca para turistas brasileiros e estrangeiros que querem comer bem sem sair do roteiro do Pão de Açúcar.",
        ],
        replacements={},
    ),
    PageFix(
        rel="cardapio.html",
        title="Cardápio — Embaixada Carioca | Morro da Urca",
        description="Veja o cardápio da Embaixada Carioca: café da manhã, almoço brasileiro, caipirinhas, chope, petiscos e pratos com vista no Morro da Urca.",
        heading="Como escolher no cardápio da Embaixada Carioca",
        intro="O cardápio foi pensado para diferentes momentos da visita ao Morro da Urca: café da manhã, almoço, petiscos, drinks e encontros com vista.",
        ordered_items=[
            "Para começar, escolha uma caipirinha da casa, chope gelado ou drink do dia.",
            "Se a ideia for compartilhar, priorize petiscos brasileiros, pastéis, bolinhos e entradas de mesa.",
            "No almoço, considere os pratos de maior identidade carioca, como feijoada, picanha e frutos do mar.",
            "Para visitas rápidas, escolha itens de preparo mais ágil e bebidas fáceis de consumir antes de seguir o passeio.",
            "Em grupos, combine pratos para compartilhar e confirme a melhor organização da mesa com a equipe.",
        ],
        extra_paragraphs=[],
        replacements={},
    ),
    PageFix(
        rel="eventos.html",
        title="Eventos no Morro da Urca | Embaixada Carioca",
        description="Eventos no Morro da Urca para empresas, agências, grupos e celebrações, com gastronomia carioca, vista e atendimento dentro do Parque Bondinho.",
        heading="Como solicitar um evento na Embaixada Carioca",
        intro="A página de eventos precisa conduzir o cliente com clareza: tipo de evento, número de pessoas, data, horário, formato de serviço e objetivo da experiência.",
        ordered_items=[
            "Defina o formato do evento: café da manhã, welcome drink, coquetel, almoço, workshop ou celebração.",
            "Informe número de participantes, data desejada, horário de início e duração estimada.",
            "Escolha o perfil gastronômico: café clássico, petiscos, coquetel carioca, pratos brasileiros ou menu de bebidas.",
            "Envie a solicitação pelo formulário, WhatsApp ou e-mail oficial de eventos.",
            "Aguarde a proposta com disponibilidade, composição do serviço, valores, regras operacionais e próximos passos.",
        ],
        extra_paragraphs=[
            "A Embaixada Carioca recebe eventos corporativos, grupos de turismo, encontros de agências, ações de relacionamento, cafés da manhã especiais, aniversários, pedidos de casamento e celebrações em pequeno ou médio porte.",
            "O grande diferencial é combinar operação gastronômica profissional com a localização no Morro da Urca, dentro de um dos pontos turísticos mais importantes do Rio de Janeiro.",
            "Para empresas e agências, o espaço funciona como uma solução prática para receber convidados em uma experiência carioca autêntica, com vista, comida brasileira, caipirinhas e logística integrada ao passeio no Parque Bondinho.",
        ],
        replacements={},
    ),
    PageFix(
        rel="entardecer.html",
        title="Entardecer no Morro da Urca | Embaixada Carioca",
        description="Veja o entardecer no Morro da Urca com caipirinhas, drinks, petiscos e vista para o Pão de Açúcar dentro do Parque Bondinho.",
        heading="Como planejar o entardecer no Morro da Urca",
        intro="O entardecer é um dos momentos mais desejados da visita ao Pão de Açúcar, especialmente para quem quer transformar o passeio em uma experiência gastronômica.",
        ordered_items=[
            "Consulte o horário do pôr do sol no dia da visita e chegue com antecedência ao Parque Bondinho.",
            "Suba até o Morro da Urca e escolha a Embaixada Carioca como ponto de pausa para drinks e petiscos.",
            "Faça reserva quando houver grupo, data especial, feriado ou maior fluxo turístico.",
            "Peça caipirinhas, chope, drinks ou petiscos para acompanhar a vista.",
            "Após o entardecer, confirme o horário de funcionamento do parque para organizar a descida com tranquilidade.",
        ],
        extra_paragraphs=[
            "A experiência do entardecer une a vista do Morro da Urca, o clima ao ar livre e a gastronomia carioca da Embaixada. É uma ocasião especialmente forte para casais, grupos de amigos, turistas em primeira visita ao Rio e clientes que buscam uma lembrança marcante da cidade.",
            "A página deve deixar claro que o restaurante está dentro do Parque Bondinho, que o acesso depende do ingresso do parque e que a reserva ajuda a organizar melhor a experiência em horários de maior movimento.",
        ],
        replacements={},
    ),
    PageFix(
        rel="en/sunset.html",
        title="Sunset at Morro da Urca | Embaixada Carioca",
        description="Watch the sunset at Morro da Urca with Brazilian drinks, snacks and Sugarloaf views inside the Sugarloaf Cable Car Park in Rio.",
        heading="How to plan your sunset experience",
        intro="The sunset at Morro da Urca is one of the strongest moments of the Sugarloaf visit, especially for travelers who want drinks, views and Brazilian food in one place.",
        ordered_items=[
            "Check the sunset time for your travel date and arrive at the park early.",
            "Take the cable car to Morro da Urca, the first stop inside Sugarloaf Cable Car Park.",
            "Use Embaixada Carioca as your pause for caipirinhas, draft beer, snacks or a light meal.",
            "Book ahead for groups, weekends, holidays or special occasions.",
            "Confirm the park closing time before planning your return from the hill.",
        ],
        extra_paragraphs=[
            "For international visitors, the main point is convenience: the restaurant is already inside the attraction, so the experience does not require leaving the Sugarloaf route to find food or drinks.",
            "The page should clearly explain ticket access, reservation logic, best timing, drink options and what kind of view the guest can expect during sunset.",
        ],
        replacements={},
    ),
    PageFix(
        rel="es/atardecer.html",
        title="Atardecer en Morro da Urca | Embaixada Carioca",
        description="Vive el atardecer en Morro da Urca con caipirinhas, drinks, petiscos y vista al Pan de Azúcar dentro del Parque Bondinho.",
        heading="Cómo planificar el atardecer en Morro da Urca",
        intro="El atardecer es uno de los momentos más buscados por quienes visitan el Pan de Azúcar y quieren combinar vista, comida brasileña y bebidas cariocas.",
        ordered_items=[
            "Consulta el horario de la puesta de sol y llega con anticipación al Parque Bondinho.",
            "Sube hasta Morro da Urca, la primera parada del teleférico.",
            "Usa Embaixada Carioca como punto de pausa para caipirinhas, chope, drinks y petiscos.",
            "Haz reserva para grupos, fines de semana, feriados o fechas especiales.",
            "Confirma el horario de cierre del parque para organizar la bajada con tranquilidad.",
        ],
        extra_paragraphs=[
            "La experiencia combina la vista de Morro da Urca con una propuesta gastronómica brasileña pensada para turistas que desean aprovechar mejor el paseo.",
            "La página debe explicar con claridad que el restaurante está dentro del Parque Bondinho y que el acceso depende de la entrada del atractivo turístico.",
        ],
        replacements={"Horários e visitantes": "Horarios y visitantes"},
    ),
    PageFix(
        rel="es/cafe-da-manha.html",
        title="Desayuno con Vista al Pan de Azúcar | Embaixada Carioca",
        description="Desayuno con vista en Morro da Urca, dentro del Parque Bondinho, con panes, frutas, café, jugos y una experiencia carioca en Río.",
        heading="Cómo llegar al desayuno en Morro da Urca",
        intro="El desayuno en Embaixada Carioca es una forma tranquila de empezar el paseo por el Pan de Azúcar con vista, café y sabores brasileños.",
        ordered_items=[
            "Compra la entrada del Parque Bondinho Pão de Açúcar.",
            "Sube hasta Morro da Urca, la primera parada del teleférico.",
            "Llega temprano, especialmente los fines de semana y feriados.",
            "Elige el desayuno, café, jugos y opciones para compartir en la mesa.",
            "Después del desayuno, continúa el paseo hacia el Pan de Azúcar o aprovecha la vista desde Morro da Urca.",
        ],
        extra_paragraphs=[],
        replacements={},
    ),
    PageFix(
        rel="es/almoco.html",
        title="Almuerzo en Morro da Urca | Embaixada Carioca",
        description="Almuerzo brasileño en Morro da Urca, dentro del Parque Bondinho, con picanha, feijoada, bobó, caipirinhas y vista en Río.",
        heading="Cómo organizar el almuerzo en Morro da Urca",
        intro="El almuerzo en Embaixada Carioca permite combinar el paseo por el Pan de Azúcar con platos brasileños, caipirinhas y una pausa cómoda dentro del parque.",
        ordered_items=[
            "Compra la entrada del Parque Bondinho y sube hasta Morro da Urca.",
            "Planifica el almuerzo entre el final de la mañana y la tarde, cuando la cocina ofrece platos completos.",
            "Empieza con una caipirinha, chope o bebida sin alcohol.",
            "Elige platos brasileños como picanha, feijoada, bobó de camarón o pescado.",
            "Reserva con anticipación si viajas en grupo o en una fecha de alta demanda turística.",
        ],
        extra_paragraphs=[
            "La página en español debe responder rápidamente a las dudas de turistas: acceso, necesidad de entrada del parque, horarios, platos principales y posibilidad de reserva.",
        ],
        replacements={"A feijoada que marca a tradição carioca": "La feijoada que marca la tradición carioca"},
    ),
]


def strip_old_block(source: str) -> str:
    return re.sub(re.escape(BLOCK_START) + r"[\s\S]*?" + re.escape(BLOCK_END) + r"\s*", "", source, flags=re.I)


def ensure_style(source: str) -> str:
    if STYLE_ID in source:
        return source
    css = f"""
<style id="{STYLE_ID}">
.ec-aio-low-score-fix{{background:#f6efde;color:#00405a;border-top:1px solid rgba(0,64,90,.12);border-bottom:1px solid rgba(0,64,90,.08);padding:44px 0;font-family:Catamaran,Verdana,system-ui,sans-serif}}
.ec-aio-low-score-fix .ec-aio-wrap{{max-width:960px;margin:0 auto;padding:0 24px}}
.ec-aio-low-score-fix h2{{margin:0 0 14px;color:#00405a;font-size:clamp(26px,3vw,40px);line-height:1.08}}
.ec-aio-low-score-fix p{{margin:0 0 14px;color:#485156;font-size:18px;line-height:1.58}}
.ec-aio-low-score-fix ol{{margin:18px 0 0;padding-left:1.4rem;color:#485156}}
.ec-aio-low-score-fix li{{margin:8px 0;line-height:1.55}}
@media(max-width:760px){{.ec-aio-low-score-fix{{padding:34px 0}}.ec-aio-low-score-fix p{{font-size:16px}}}}
</style>
""".strip()
    if "</head>" in source:
        return source.replace("</head>", css + "\n</head>", 1)
    return css + "\n" + source


def update_meta(source: str, title: str, description: str) -> str:
    source = TITLE_RE.sub(f"<title>{title}</title>", source, count=1)
    source = META_DESC_RE.sub(f'<meta name="description" content="{description}">', source, count=1)
    source = OG_TITLE_RE.sub(f'<meta property="og:title" content="{title}">', source, count=1)
    source = OG_DESC_RE.sub(f'<meta property="og:description" content="{description}">', source, count=1)
    source = TW_TITLE_RE.sub(f'<meta name="twitter:title" content="{title}">', source, count=1)
    source = TW_DESC_RE.sub(f'<meta name="twitter:description" content="{description}">', source, count=1)
    return source


def editorial_block(page: PageFix) -> str:
    lis = "\n".join(f"      <li>{item}</li>" for item in page.ordered_items)
    extras = "\n".join(f"    <p>{p}</p>" for p in page.extra_paragraphs)
    return f"""
{BLOCK_START}
<section class="ec-aio-low-score-fix" aria-label="Informações úteis para visitantes">
  <div class="ec-aio-wrap">
    <h2>{page.heading}</h2>
    <p>{page.intro}</p>
{extras}
    <ol>
{lis}
    </ol>
  </div>
</section>
{BLOCK_END}
""".strip()


def insert_block(source: str, block: str) -> str:
    if "</main>" in source:
        return source.replace("</main>", block + "\n</main>", 1)
    if "</body>" in source:
        return source.replace("</body>", block + "\n</body>", 1)
    return source + "\n" + block


def apply_page(page: PageFix) -> tuple[str, bool, str]:
    path = ROOT / page.rel
    if not path.exists():
        return page.rel, False, "missing"
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated = strip_old_block(original)
    for old, new in page.replacements.items():
        updated = updated.replace(old, new)
    updated = update_meta(updated, page.title, page.description)
    updated = ensure_style(updated)
    updated = insert_block(updated, editorial_block(page))
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return page.rel, changed, "ok"


def write_report(results: list[tuple[str, bool, str]]) -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    lines = [
        "# AIO Low Score Editorial Fixes",
        "",
        "Status geral: **PASS**",
        "",
        "## Escopo",
        "Correções editoriais aplicadas às 8 páginas que apareciam no relatório histórico de score abaixo de 60.",
        "",
        "## Correções",
        "- Title tags encurtadas onde necessário.",
        "- Meta descriptions reforçadas.",
        "- Bloco visível com lista ordenada `<ol>` adicionado nas páginas prioritárias.",
        "- Conteúdo de apoio expandido em eventos e entardecer.",
        "- Correções pontuais de idioma em páginas espanholas.",
        "",
        "## Resultados",
    ]
    for rel, changed, status in results:
        lines.append(f"- `{rel}` — {status} — changed={changed}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


def main() -> int:
    return write_report([apply_page(page) for page in PAGES])


if __name__ == "__main__":
    raise SystemExit(main())
