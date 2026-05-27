#!/usr/bin/env python3
"""Apply exact fixes from the page scorecard gap review.

Targets from visual scorecard:
- Home PT: FAQ has 6; enforce 8 FAQ entities.
- Eventos PT: FAQ has 3 + thin content; enforce 8 FAQ entities and add visible depth block.
- Cardapio EN: FAQ has 3; enforce 8 FAQ entities.
- Almoco EN: FAQ has 3; enforce 8 FAQ entities.
- Parque Bondinho PT: no FAQ/no OL; enforce 8 FAQ entities and add visible ordered-list block.

Guardrails:
- Replaces FAQPage JSON-LD on the target page instead of adding duplicates.
- Does not add AggregateRating/Rating/Review.
- Does not touch Restaurant schema except preserving existing non-FAQ JSON-LD.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import html
import json
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "scorecard_gap_fixes_report.md"

STYLE_ID = "ec-scorecard-gap-fixes-css"
SCRIPT_MARKER = "EC Scorecard Gap FAQ"
BLOCK_START = "<!-- EC SCORECARD GAP VISIBLE FIX -->"
BLOCK_END = "<!-- /EC SCORECARD GAP VISIBLE FIX -->"

SCRIPT_RE = re.compile(r"<script\b([^>]*)>([\s\S]*?)</script>", re.I)

FAQS: dict[str, list[tuple[str, str]]] = {
    "index.html": [
        ("Tem restaurante no Bondinho do Pão de Açúcar?", "Sim. A Embaixada Carioca fica no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com café da manhã, almoço, caipirinhas, chope e vista para o Rio."),
        ("Onde fica a Embaixada Carioca?", "A Embaixada Carioca fica no Morro da Urca, primeira parada do Bondinho Pão de Açúcar, com acesso pela Av. Pasteur, 520, Urca, Rio de Janeiro."),
        ("Precisa reservar mesa?", "A reserva é recomendada para fins de semana, feriados, grupos, café da manhã e horários de maior movimento, mas o atendimento também pode ocorrer por ordem de chegada conforme disponibilidade."),
        ("Tem café da manhã todos os dias?", "Sim. A Embaixada Carioca serve café da manhã todos os dias, ideal para quem sobe cedo ao Morro da Urca e quer começar o passeio com vista."),
        ("A Embaixada Carioca serve almoço?", "Sim. O restaurante serve almoço com pratos brasileiros e cariocas, como picanha, feijoada, bobó, petiscos, caipirinhas e chope gelado."),
        ("A feijoada é servida todos os dias?", "Sim. A feijoada da Embaixada Carioca é uma das especialidades da casa e pode ser pedida todos os dias, conforme disponibilidade operacional."),
        ("Dá para fazer eventos na Embaixada Carioca?", "Sim. A casa recebe eventos corporativos, grupos de turismo, celebrações, welcome drinks, cafés da manhã, almoços e formatos especiais no Morro da Urca."),
        ("Qual é a especialidade da Embaixada Carioca?", "A proposta é reunir gastronomia carioca, caipirinhas, chope bem tirado, pratos brasileiros e uma experiência com vista no Morro da Urca."),
    ],
    "eventos.html": [
        ("Quais eventos podem ser feitos na Embaixada Carioca?", "A casa recebe cafés da manhã, almoços, welcome drinks, coquetéis, workshops, ações corporativas, grupos de turismo, celebrações e eventos sociais com vista no Morro da Urca."),
        ("A Embaixada Carioca faz casamento com vista?", "Sim. A Embaixada Carioca pode receber casamento com vista, mini weddings, pedidos de casamento, noivados e celebrações intimistas no Morro da Urca, conforme disponibilidade e formato do evento."),
        ("Quantas pessoas cabem em um evento?", "A capacidade depende do formato, montagem, horário e operação do parque. Para eventos sentados, coquetéis e grupos, a equipe monta a proposta conforme número de convidados e necessidade de serviço."),
        ("Dá para fazer evento corporativo no Morro da Urca?", "Sim. A localização dentro do Parque Bondinho Pão de Açúcar é adequada para ações corporativas, receptivos, lançamentos, workshops e experiências para clientes ou equipes."),
        ("Quais formatos gastronômicos estão disponíveis?", "Os formatos incluem café da manhã servido, almoço, welcome drink, coquetel com bebidas, petiscos, feijoada para grupos e experiências personalizadas de acordo com o horário."),
        ("Como solicitar orçamento de evento?", "O orçamento deve informar data, horário, número de convidados, tipo de evento, necessidade de montagem, audiovisual, brindes, troféus, menu desejado e contato do responsável."),
        ("É possível combinar evento com o entardecer?", "Sim. Eventos no fim da tarde podem ser planejados para aproveitar a vista e o clima do entardecer no Morro da Urca, respeitando horários do parque e disponibilidade."),
        ("Como confirmar o evento?", "A confirmação ocorre após alinhamento da proposta, aceite das condições comerciais e pagamento do sinal, conforme regras enviadas pela equipe de eventos."),
    ],
    "en/cardapio.html": [
        ("What kind of food does Embaixada Carioca serve?", "Embaixada Carioca serves Brazilian and Carioca food at Morro da Urca, including grilled steak, feijoada, seafood dishes, snacks, caipirinhas and cold draft beer."),
        ("Is there a full menu at Sugarloaf Cable Car Park?", "Yes. The restaurant offers breakfast, lunch, snacks, drinks and Brazilian dishes inside Sugarloaf Cable Car Park, at the Morro da Urca stop."),
        ("What are the house specialties?", "The most requested items include grilled steak, feijoada, shrimp dishes, Brazilian snacks, the house caipirinha and cold draft beer."),
        ("Can I have lunch before visiting Sugarloaf Mountain?", "Yes. Many guests stop at Morro da Urca for lunch before continuing to Sugarloaf Mountain or after returning from the second cable car section."),
        ("Does the menu include drinks?", "Yes. The menu includes caipirinhas, cocktails, beer, draft beer, non-alcoholic options, coffee and drinks for different moments of the visit."),
        ("Is the restaurant good for families?", "Yes. The restaurant works well for families visiting the park, with table service, Brazilian dishes, snacks and a comfortable stop during the tour."),
        ("Do I need a reservation?", "Reservations are recommended for weekends, holidays, groups and peak hours, although tables may also be available on arrival."),
        ("Where is the restaurant located?", "It is located at Morro da Urca, the first stop of the Sugarloaf Cable Car, inside Sugarloaf Cable Car Park in Rio de Janeiro."),
    ],
    "en/almoco.html": [
        ("Can I have lunch at Morro da Urca?", "Yes. Embaixada Carioca serves lunch at Morro da Urca, inside Sugarloaf Cable Car Park, with Brazilian dishes and a view of Rio de Janeiro."),
        ("What should I order for lunch?", "Popular lunch choices include grilled steak, feijoada, seafood dishes, Brazilian snacks, caipirinhas and cold draft beer."),
        ("Is lunch served every day?", "Lunch is available daily according to the restaurant operation and park schedule. It is best to plan the meal between late morning and afternoon."),
        ("Is the restaurant inside Sugarloaf Cable Car Park?", "Yes. The restaurant is at Morro da Urca, the first cable car stop, inside Sugarloaf Cable Car Park."),
        ("Do I need to buy a cable car ticket?", "The usual access is through Sugarloaf Cable Car Park. Visitors who arrive at Morro da Urca by trail only need a ticket if they use the cable car to continue or go down."),
        ("Is lunch good for groups?", "Yes. Groups, families and corporate visitors can request reservations or event proposals depending on date, time and number of guests."),
        ("Can I combine lunch with sunset?", "Yes. Many guests plan lunch or a late afternoon visit and then stay at Morro da Urca to enjoy the view and sunset atmosphere."),
        ("How do I book a table?", "Reservations can be made through the online booking link or by contacting the restaurant through WhatsApp."),
    ],
    "parque-bondinho.html": [
        ("A Embaixada Carioca fica dentro do Parque Bondinho?", "Sim. A Embaixada Carioca fica no Morro da Urca, primeira parada do Parque Bondinho Pão de Açúcar."),
        ("Precisa pagar ingresso para ir à Embaixada Carioca?", "O acesso usual é pelo ingresso do Bondinho até o Morro da Urca. Quem sobe pela trilha, quando aberta, não precisa pagar ingresso se permanecer no Morro da Urca."),
        ("Quando o ingresso do Bondinho é necessário?", "O ingresso é necessário para usar o teleférico, seja para subir ao Pão de Açúcar ou para descer do Morro da Urca até a Praia Vermelha."),
        ("Existe acesso pela trilha do Morro da Urca?", "Sim. A trilha pela Pista Cláudio Coutinho é uma alternativa quando estiver aberta e liberada, respeitando horários e regras do parque."),
        ("Onde fica a entrada do Parque Bondinho?", "A entrada principal do Parque Bondinho fica na Av. Pasteur, 520, na Urca, Rio de Janeiro, junto à Praia Vermelha."),
        ("O que comer no Morro da Urca?", "Na Embaixada Carioca há café da manhã, almoço, feijoada, picanha, petiscos, caipirinhas, chope e bebidas para diferentes momentos do passeio."),
        ("Dá para reservar mesa no Parque Bondinho?", "Sim. A Embaixada Carioca aceita reservas online, especialmente úteis para fins de semana, feriados, grupos e horários de maior movimento."),
        ("Dá para fazer eventos no Parque Bondinho?", "Sim. A Embaixada Carioca recebe eventos corporativos, grupos de turismo, celebrações, welcome drinks, cafés da manhã e almoços no Morro da Urca."),
    ],
}

VISIBLE_BLOCKS = {
    "eventos.html": {
        "title": "Eventos no Morro da Urca: formatos e momentos ideais",
        "intro": "A Embaixada Carioca funciona como ponto de encontro para eventos no Morro da Urca, unindo vista, gastronomia brasileira, serviço de salão e o fluxo turístico do Parque Bondinho Pão de Açúcar.",
        "paragraphs": [
            "Para empresas, o espaço pode receber ações de relacionamento, lançamentos, workshops, cafés da manhã executivos, almoços de incentivo e experiências para clientes ou equipes. A localização ajuda a transformar o evento em memória de marca, porque o deslocamento pelo Bondinho já faz parte da experiência.",
            "Para grupos de turismo e receptivo, o restaurante permite organizar uma pausa gastronômica com vista durante o roteiro do Pão de Açúcar. O formato pode ser ajustado para café da manhã, almoço, welcome drink, coquetel ou menu definido, conforme horário, duração e número de convidados.",
            "Para celebrações sociais, a casa pode receber aniversário, noivado, pedido de casamento e casamento com vista em formato intimista. A proposta deve considerar horário do parque, operação do bondinho, necessidade de montagem, música, fotografia, troféus, brindes e cronograma do grupo.",
            "O melhor orçamento nasce quando o pedido chega com data, horário, número de convidados, tipo de serviço, expectativa de menu, necessidade de bebidas, tempo de permanência e contexto do evento. Com essas informações, a equipe consegue sugerir o formato mais eficiente e evitar excesso de estrutura.",
        ],
        "ol_title": "Como solicitar um evento",
        "steps": [
            "Informe data, horário e número estimado de convidados.",
            "Escolha o formato: café da manhã, almoço, welcome drink, coquetel, workshop ou experiência.",
            "Explique o objetivo do evento, como ação corporativa, grupo de turismo, celebração ou casamento com vista.",
            "Envie necessidades de montagem, audiovisual, troféus, brindes, música, fotografia ou roteiro do grupo.",
            "Aguarde a proposta e confirme a reserva do evento com o pagamento do sinal.",
        ],
    },
    "parque-bondinho.html": {
        "title": "Como planejar a visita ao Parque Bondinho com pausa na Embaixada Carioca",
        "intro": "O Parque Bondinho Pão de Açúcar é um dos roteiros mais conhecidos do Rio. A Embaixada Carioca fica no Morro da Urca, o que permite encaixar café da manhã, almoço, feijoada, drinks ou eventos no meio do passeio.",
        "paragraphs": [
            "O acesso usual ao Morro da Urca é pelo ingresso do Bondinho. A alternativa é subir pela trilha do Morro da Urca quando ela estiver aberta; nesse caso, quem permanece apenas no Morro da Urca não precisa pagar ingresso do Bondinho para visitar a Embaixada Carioca.",
            "O ingresso passa a ser necessário quando o visitante decide usar o teleférico, seja para seguir até o Pão de Açúcar ou para descer do Morro da Urca até a Praia Vermelha. Por isso, o planejamento depende de como a pessoa pretende subir, circular e sair do parque.",
        ],
        "ol_title": "Passo a passo recomendado",
        "steps": [
            "Defina se você vai subir pelo Bondinho ou pela trilha do Morro da Urca, quando aberta.",
            "Se usar o Bondinho, compre ou apresente o ingresso na entrada da Av. Pasteur, 520, Urca.",
            "Desembarque no Morro da Urca, primeira parada do teleférico.",
            "Faça uma pausa na Embaixada Carioca para café da manhã, almoço, feijoada, caipirinhas ou chope.",
            "Use o ingresso do teleférico se quiser subir ao Pão de Açúcar ou descer para a Praia Vermelha pelo Bondinho.",
        ],
    },
}


@dataclass
class Result:
    rel: str
    status: str
    changed: bool
    faq_count: int
    ol_count: int
    word_count: int
    notes: str


def parse_json_ld(text: str) -> Any | None:
    try:
        raw = html.unescape(text.strip())
        if not raw:
            return None
        return json.loads(raw)
    except Exception:
        return None


def type_matches(value: Any, target: str) -> bool:
    if isinstance(value, str):
        return value.lower() == target.lower()
    if isinstance(value, list):
        return any(type_matches(v, target) for v in value)
    return False


def is_faq_json_ld(data: Any) -> bool:
    if isinstance(data, dict):
        if type_matches(data.get("@type"), "FAQPage"):
            return True
        graph = data.get("@graph")
        if isinstance(graph, list):
            return any(is_faq_json_ld(item) for item in graph)
    return False


def remove_faq_json_ld(source: str) -> tuple[str, int]:
    removed = 0
    parts: list[str] = []
    last = 0
    for match in SCRIPT_RE.finditer(source):
        attrs = match.group(1) or ""
        body = match.group(2) or ""
        if "application/ld+json" not in attrs.lower():
            continue
        data = parse_json_ld(body)
        if is_faq_json_ld(data):
            parts.append(source[last:match.start()])
            last = match.end()
            removed += 1
    if removed:
        parts.append(source[last:])
        return "".join(parts), removed
    return source, 0


def faq_json(rel: str) -> str:
    entities = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in FAQS[rel]
    ]
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": f"https://www.embaixadacarioca.com/{'' if rel == 'index.html' else rel}#faq",
        "mainEntity": entities,
    }
    return f"<!-- {SCRIPT_MARKER}: {rel} -->\n<script type=\"application/ld+json\">{json.dumps(data, ensure_ascii=False, separators=(',', ':'))}</script>\n<!-- /{SCRIPT_MARKER}: {rel} -->"


def insert_before_head_close(source: str, payload: str) -> str:
    if "</head>" in source:
        return source.replace("</head>", payload + "\n</head>", 1)
    return payload + "\n" + source


def strip_visible(source: str) -> str:
    return re.sub(re.escape(BLOCK_START) + r"[\s\S]*?" + re.escape(BLOCK_END) + r"\s*", "", source, flags=re.I)


def ensure_style(source: str) -> str:
    if STYLE_ID in source:
        return source
    css = f"""
<style id="{STYLE_ID}">
.ec-scorecard-gap{{background:#fff8ea;color:#00405a;border-top:1px solid rgba(0,64,90,.10);border-bottom:1px solid rgba(0,64,90,.08);padding:56px 0;font-family:Catamaran,Verdana,system-ui,sans-serif}}
.ec-scorecard-gap .ec-wrap{{width:min(1080px,calc(100% - 44px));margin:0 auto}}
.ec-scorecard-gap .ec-kicker{{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#527f8f;margin-bottom:12px}}
.ec-scorecard-gap h2{{font-size:clamp(28px,3.4vw,48px);line-height:1.08;margin:0 0 16px;color:#00405a;font-weight:900;letter-spacing:-.02em}}
.ec-scorecard-gap h3{{font-size:24px;line-height:1.18;margin:28px 0 12px;color:#335d4a}}
.ec-scorecard-gap p{{font-size:18px;line-height:1.66;color:#485156;max-width:920px;margin:0 0 16px}}
.ec-scorecard-gap ol{{margin:18px 0 0;padding-left:1.4rem;color:#485156;background:#fff;border:1px solid rgba(0,64,90,.12);border-radius:18px;padding:22px 24px 22px 46px;box-shadow:0 12px 30px rgba(0,64,90,.05)}}
.ec-scorecard-gap li{{margin:8px 0;line-height:1.54;color:#485156}}
.ec-scorecard-gap strong{{color:#335d4a}}
@media(max-width:760px){{.ec-scorecard-gap{{padding:40px 0}}.ec-scorecard-gap p{{font-size:16px}}}}
</style>
""".strip()
    return insert_before_head_close(source, css)


def visible_block(rel: str) -> str:
    data = VISIBLE_BLOCKS[rel]
    paragraphs = "\n".join(f"    <p>{p}</p>" for p in data["paragraphs"])
    steps = "\n".join(f"      <li>{step}</li>" for step in data["steps"])
    return f"""
{BLOCK_START}
<section class="ec-scorecard-gap" aria-label="{data['title']}">
  <div class="ec-wrap">
    <div class="ec-kicker">Guia rápido</div>
    <h2>{data['title']}</h2>
    <p>{data['intro']}</p>
{paragraphs}
    <h3>{data['ol_title']}</h3>
    <ol>
{steps}
    </ol>
  </div>
</section>
{BLOCK_END}
""".strip()


def insert_visible(source: str, payload: str) -> str:
    if "</main>" in source:
        return source.replace("</main>", payload + "\n</main>", 1)
    if "</body>" in source:
        return source.replace("</body>", payload + "\n</body>", 1)
    return source + "\n" + payload


def faq_count(source: str) -> int:
    total = 0
    for match in SCRIPT_RE.finditer(source):
        attrs = match.group(1) or ""
        body = match.group(2) or ""
        if "application/ld+json" not in attrs.lower():
            continue
        data = parse_json_ld(body)
        if isinstance(data, dict) and type_matches(data.get("@type"), "FAQPage"):
            items = data.get("mainEntity")
            if isinstance(items, list):
                total += len(items)
        elif isinstance(data, dict) and isinstance(data.get("@graph"), list):
            for node in data["@graph"]:
                if isinstance(node, dict) and type_matches(node.get("@type"), "FAQPage"):
                    items = node.get("mainEntity")
                    if isinstance(items, list):
                        total += len(items)
    return total


def count_ol(source: str) -> int:
    return len(re.findall(r"<ol\b", source, flags=re.I))


def count_words(source: str) -> int:
    text = re.sub(r"<script[\s\S]*?</script>", " ", source, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"\b[\wÀ-ÿ]{2,}\b", html.unescape(text)))


def apply_page(rel: str) -> Result:
    path = ROOT / rel
    if not path.exists():
        return Result(rel, "missing", False, 0, 0, 0, "file not found")
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated, removed = remove_faq_json_ld(original)
    updated = insert_before_head_close(updated, faq_json(rel))
    notes = [f"faq_json_ld_removed={removed}"]
    if rel in VISIBLE_BLOCKS:
        updated = strip_visible(updated)
        updated = ensure_style(updated)
        updated = insert_visible(updated, visible_block(rel))
        notes.append("visible_depth_block=True")
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    fc = faq_count(updated)
    oc = count_ol(updated)
    wc = count_words(updated)
    status = "ok" if fc >= 8 and (rel != "parque-bondinho.html" or oc >= 1) and (rel != "eventos.html" or wc >= 1200) else "fail"
    return Result(rel, status, changed, fc, oc, wc, "; ".join(notes))


def write_report(results: list[Result]) -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    failures = [r for r in results if r.status != "ok"]
    status = "PASS" if not failures else "FAIL"
    lines = [
        "# Scorecard Gap Fixes",
        "",
        f"Status geral: **{status}**",
        "",
        "## Objetivo",
        "Corrigir os gaps apontados no scorecard visual: FAQ incompleto, `parque-bondinho.html` sem FAQ/OL e conteúdo fino em `eventos.html`.",
        "",
        "## Guardrails",
        "- FAQPage existente nas páginas-alvo foi substituído por um único FAQPage com 8 perguntas para evitar duplicidade.",
        "- Nenhum AggregateRating, Rating ou Review foi inserido.",
        "- Nenhum Restaurant schema foi removido.",
        "- Alterações visíveis foram aplicadas apenas em `eventos.html` e `parque-bondinho.html`.",
        "",
        "## Resumo",
        f"- Páginas configuradas: **{len(results)}**",
        f"- Páginas com PASS: **{len([r for r in results if r.status == 'ok'])}**",
        f"- Páginas com falha: **{len(failures)}**",
        f"- Páginas alteradas: **{len([r for r in results if r.changed])}**",
        "",
        "## Resultados por página",
        "",
        "| Página | Status | Changed | FAQ | OL | Palavras | Notas |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for r in results:
        lines.append(f"| `{r.rel}` | {r.status} | {r.changed} | {r.faq_count} | {r.ol_count} | {r.word_count} | {r.notes} |")
    lines.extend([
        "",
        "## Próxima validação",
        "Rodar o Final 86-page AAA master audit e a validação GSC pós-fix para confirmar que não houve duplicidade de FAQPage.",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Scorecard gap fixes: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    targets = ["index.html", "eventos.html", "en/cardapio.html", "en/almoco.html", "parque-bondinho.html"]
    return write_report([apply_page(rel) for rel in targets])


if __name__ == "__main__":
    raise SystemExit(main())
