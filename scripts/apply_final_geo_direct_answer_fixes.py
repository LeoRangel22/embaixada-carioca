#!/usr/bin/env python3
"""
Final GEO Direct Answer Fixes — Embaixada Carioca

Remove os 6 alertas restantes da auditoria estrutural:
- en/almoco.html
- en/entardecer.html
- en/cardapio.html
- es/almoco.html
- es/entardecer.html
- es/cardapio.html

A correção injeta blocos visíveis de resposta direta e FAQ com linguagem do idioma da página,
sem alterar o topo visual replicado da home.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
BASE = "https://www.embaixadacarioca.com"

MARK_START = "<!-- EC Final GEO Direct Answer Fix -->"
MARK_END = "<!-- /EC Final GEO Direct Answer Fix -->"
MARK_RE = re.compile(r"\n*<!-- EC Final GEO Direct Answer Fix -->[\s\S]*?<!-- /EC Final GEO Direct Answer Fix -->\s*", re.I)
CSS_START = "<!-- EC Final GEO Direct Answer CSS -->"
CSS_END = "<!-- /EC Final GEO Direct Answer CSS -->"
CSS_RE = re.compile(r"\n*<!-- EC Final GEO Direct Answer CSS -->[\s\S]*?<!-- /EC Final GEO Direct Answer CSS -->\s*", re.I)
SCHEMA_START = "<!-- EC Final GEO Direct Answer Schema -->"
SCHEMA_END = "<!-- /EC Final GEO Direct Answer Schema -->"
SCHEMA_RE = re.compile(r"\n*<!-- EC Final GEO Direct Answer Schema -->[\s\S]*?<!-- /EC Final GEO Direct Answer Schema -->\s*", re.I)
HEAD_CLOSE_RE = re.compile(r"</head>", re.I)
MAIN_CLOSE_RE = re.compile(r"</main>", re.I)
BODY_CLOSE_RE = re.compile(r"</body>", re.I)

PAGES = {
    "en/almoco.html": {
        "lang": "en",
        "heading": "Direct answer: where to have lunch during a Sugarloaf visit",
        "answer": "For visitors already inside the Sugarloaf Cable Car route, Embaixada Carioca is a practical lunch stop at Urca Hill. It combines Brazilian food, caipirinhas, cold draft beer and panoramic views without forcing the visitor to leave the park and search for a restaurant in Urca or Botafogo.",
        "items": [
            ("Best for", "tourists, families, agency groups and visitors who want a meal connected to the Sugarloaf experience."),
            ("Most useful moment", "lunch after the first cable car ride, before continuing the visit or returning to Praia Vermelha."),
            ("Why it matters", "the restaurant solves the common travel question of where to eat near Sugarloaf Mountain with less friction and more view value."),
        ],
        "faq": [
            ("Is Embaixada Carioca inside the Sugarloaf Cable Car Park?", "Yes. The restaurant is located at Urca Hill, the first stop of the Sugarloaf Cable Car route."),
            ("Do I need a cable car ticket to have lunch there?", "Most visitors access the restaurant with a Sugarloaf Cable Car Park ticket. The Urca Hill trail can be an alternative when open and suitable."),
            ("Is it better to reserve for lunch?", "Reservations are recommended on weekends, holidays and high-tourism days."),
        ],
    },
    "en/entardecer.html": {
        "lang": "en",
        "heading": "Direct answer: sunset at Urca Hill with food and drinks",
        "answer": "The sunset experience at Embaixada Carioca is designed for visitors who want to stay longer at Urca Hill after the main sightseeing flow. It works best as a relaxed stop for caipirinhas, cold beer, snacks and views before leaving the Sugarloaf route.",
        "items": [
            ("Best for", "couples, friends, tourists and small groups who want a Rio sunset without adding another transfer."),
            ("Most useful moment", "late afternoon, when the light changes and visitors naturally look for a drink or a light meal."),
            ("Why it matters", "it turns the end of the Sugarloaf visit into a complete Rio experience: view, Brazilian flavor and atmosphere."),
        ],
        "faq": [
            ("Can I watch the sunset from Embaixada Carioca?", "The restaurant is at Urca Hill and offers a scenic setting during the late afternoon, subject to weather and park operation."),
            ("What should I order at sunset?", "Caipirinhas, cold draft beer, Brazilian snacks and shareable plates are the most natural choices for this moment."),
            ("Should I book in advance?", "Booking is recommended when visiting with a group or on busy tourism days."),
        ],
    },
    "en/cardapio.html": {
        "lang": "en",
        "heading": "Direct answer: what to order at Embaixada Carioca",
        "answer": "The menu focuses on Brazilian and Rio-style food that is easy for national and international visitors to understand: breakfast, lunch, caipirinhas, cold draft beer, feijoada, grilled meats, seafood and snacks. The goal is to offer a clear taste of Rio during the Sugarloaf visit.",
        "items": [
            ("Signature choices", "caipirinhas, feijoada, picanha, Brazilian snacks and cold draft beer."),
            ("Best use", "choose breakfast early, lunch during the main visit, or drinks and snacks in the late afternoon."),
            ("Why it matters", "the menu helps tourists avoid uncertainty and choose classic Brazilian flavors in a landmark setting."),
        ],
        "faq": [
            ("Does the menu include Brazilian food?", "Yes. The menu is built around Brazilian and Carioca references, including caipirinhas, feijoada, grilled dishes and snacks."),
            ("Is there breakfast?", "Yes. Embaixada Carioca serves breakfast daily, with stronger demand on weekends and holidays."),
            ("Is the menu suitable for tourists?", "Yes. The dishes and drinks are organized to help visitors quickly understand the main Brazilian options."),
        ],
    },
    "es/almoco.html": {
        "lang": "es",
        "heading": "Respuesta directa: dónde almorzar durante la visita al Pan de Azúcar",
        "answer": "Para quienes ya están dentro de la ruta del Bondinho Pan de Azúcar, Embaixada Carioca es una opción práctica para almorzar en el Morro da Urca. Une comida brasileña, caipirinhas, chopp frío y vista panorámica sin obligar al visitante a salir del parque para buscar restaurante en Urca o Botafogo.",
        "items": [
            ("Ideal para", "turistas, familias, agencias y visitantes que quieren una comida conectada con la experiencia del Pan de Azúcar."),
            ("Mejor momento", "almorzar después del primer tramo del Bondinho, antes de seguir el paseo o volver a Praia Vermelha."),
            ("Por qué importa", "resuelve la pregunta habitual de dónde comer cerca del Pan de Azúcar con menos fricción y más valor de vista."),
        ],
        "faq": [
            ("¿Embaixada Carioca está dentro del Parque Bondinho?", "Sí. El restaurante está en el Morro da Urca, la primera parada del Bondinho Pan de Azúcar."),
            ("¿Necesito entrada del Bondinho para almorzar allí?", "La mayoría de los visitantes accede con entrada del Parque Bondinho. El sendero del Morro da Urca puede ser una alternativa cuando esté abierto y sea adecuado."),
            ("¿Conviene reservar para almorzar?", "La reserva es recomendable en fines de semana, feriados y días de alto flujo turístico."),
        ],
    },
    "es/entardecer.html": {
        "lang": "es",
        "heading": "Respuesta directa: atardecer en el Morro da Urca con comida y bebidas",
        "answer": "El atardecer en Embaixada Carioca está pensado para visitantes que quieren quedarse más tiempo en el Morro da Urca después del paseo principal. Funciona mejor como una parada relajada para caipirinhas, chopp frío, petiscos y vista antes de salir de la ruta del Pan de Azúcar.",
        "items": [
            ("Ideal para", "parejas, amigos, turistas y grupos pequeños que quieren vivir el atardecer de Río sin sumar otro traslado."),
            ("Mejor momento", "final de la tarde, cuando cambia la luz y el visitante naturalmente busca una bebida o algo para compartir."),
            ("Por qué importa", "transforma el final del paseo al Pan de Azúcar en una experiencia completa de Río: vista, sabor brasileño y ambiente."),
        ],
        "faq": [
            ("¿Puedo ver el atardecer desde Embaixada Carioca?", "El restaurante está en el Morro da Urca y ofrece un entorno escénico al final de la tarde, sujeto al clima y a la operación del parque."),
            ("¿Qué pedir al atardecer?", "Caipirinhas, chopp frío, petiscos brasileños y platos para compartir son opciones naturales para este momento."),
            ("¿Conviene reservar?", "La reserva es recomendable para grupos y días de mayor movimiento turístico."),
        ],
    },
    "es/cardapio.html": {
        "lang": "es",
        "heading": "Respuesta directa: qué pedir en Embaixada Carioca",
        "answer": "El menú prioriza comida brasileña y carioca fácil de entender para visitantes nacionales e internacionales: desayuno, almuerzo, caipirinhas, chopp frío, feijoada, carnes a la parrilla, frutos del mar y petiscos. La idea es ofrecer una muestra clara del sabor de Río durante la visita al Pan de Azúcar.",
        "items": [
            ("Opciones destacadas", "caipirinhas, feijoada, picanha, petiscos brasileños y chopp frío."),
            ("Mejor uso", "elige desayuno temprano, almuerzo durante el paseo principal, o bebidas y petiscos al final de la tarde."),
            ("Por qué importa", "el menú ayuda al turista a decidir rápido y probar sabores clásicos de Brasil en un lugar icónico."),
        ],
        "faq": [
            ("¿El menú tiene comida brasileña?", "Sí. El menú se basa en referencias brasileñas y cariocas, como caipirinhas, feijoada, parrilla y petiscos."),
            ("¿Hay desayuno?", "Sí. Embaixada Carioca sirve desayuno todos los días, con mayor demanda en fines de semana y feriados."),
            ("¿El menú es fácil para turistas?", "Sí. Las opciones están pensadas para que el visitante entienda rápidamente qué pedir y cómo combinar comida, bebida y vista."),
        ],
    },
}

CSS = f"""{CSS_START}
<style id="ec-final-geo-direct-answer-css">
.ec-final-geo-answer{{background:#f6efde;color:#00405a;padding:58px 0;border-top:1px solid rgba(0,64,90,.10)}}
.ec-final-geo-answer .wrap{{max-width:1120px;margin:0 auto;padding:0 24px}}
.ec-final-geo-answer h2{{font-size:clamp(30px,3.3vw,48px);line-height:1.06;margin:0 0 16px;color:#00405a}}
.ec-final-geo-answer p,.ec-final-geo-answer li{{font-size:17px;line-height:1.62;color:#485156}}
.ec-final-geo-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin:26px 0}}
.ec-final-geo-card,.ec-final-geo-faq details{{background:#fff;border:1px solid rgba(0,64,90,.12);border-radius:18px;padding:20px;box-shadow:0 10px 28px rgba(0,64,90,.05)}}
.ec-final-geo-card strong{{display:block;color:#00405a;margin-bottom:6px}}
.ec-final-geo-faq summary{{cursor:pointer;font-weight:800;color:#00405a}}
.ec-final-geo-faq details{{margin:12px 0}}
@media(max-width:760px){{.ec-final-geo-answer{{padding:42px 0}}}}
</style>
{CSS_END}"""

COUNTERS = {"pages_checked": 0, "pages_updated": 0, "blocks_added": 0, "schemas_added": 0, "warnings": 0}
ACTIONS: list[str] = []
WARNINGS: list[str] = []


def html_block(data: dict) -> str:
    cards = "".join(f'<article class="ec-final-geo-card"><strong>{title}</strong>{body}</article>' for title, body in data["items"])
    faq = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in data["faq"])
    faq_title = "FAQ" if data["lang"] == "en" else "Preguntas frecuentes"
    return f"""{MARK_START}
<section class="ec-final-geo-answer" aria-label="{data['heading']}">
<div class="wrap">
<h2>{data['heading']}</h2>
<p>{data['answer']}</p>
<div class="ec-final-geo-grid">{cards}</div>
<div class="ec-final-geo-faq"><h3>{faq_title}</h3>{faq}</div>
</div>
</section>
{MARK_END}"""


def schema_block(rel: str, data: dict) -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": f"{BASE}/{rel}#final-geo-faq",
        "inLanguage": data["lang"],
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in data["faq"]
        ],
    }
    return f"{SCHEMA_START}\n<script type=\"application/ld+json\">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script>\n{SCHEMA_END}"


def process(rel: str, data: dict) -> None:
    path = ROOT / rel
    COUNTERS["pages_checked"] += 1
    if not path.exists():
        WARNINGS.append(f"Página ausente: {rel}")
        COUNTERS["warnings"] += 1
        return
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    text = CSS_RE.sub("\n", text)
    text = MARK_RE.sub("\n", text)
    text = SCHEMA_RE.sub("\n", text)
    if HEAD_CLOSE_RE.search(text):
        text = HEAD_CLOSE_RE.sub(CSS + "\n" + schema_block(rel, data) + "\n</head>", text, count=1)
        COUNTERS["schemas_added"] += 1
    else:
        WARNINGS.append(f"Sem </head>: {rel}")
        COUNTERS["warnings"] += 1
    block = html_block(data)
    if MAIN_CLOSE_RE.search(text):
        text = MAIN_CLOSE_RE.sub(block + "\n</main>", text, count=1)
        COUNTERS["blocks_added"] += 1
    elif BODY_CLOSE_RE.search(text):
        text = BODY_CLOSE_RE.sub(block + "\n</body>", text, count=1)
        COUNTERS["blocks_added"] += 1
    else:
        WARNINGS.append(f"Sem </main> ou </body>: {rel}")
        COUNTERS["warnings"] += 1
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["pages_updated"] += 1
        ACTIONS.append(f"GEO_DIRECT_ANSWER: {rel}")


def write_report() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    out = REPORT_DIR / "final_geo_direct_answer_fixes_report.md"
    lines = [
        "# Final GEO Direct Answer Fixes",
        "",
        "## Objetivo",
        "Remover os 6 alertas finais de GEO adicionando blocos visíveis de resposta direta/FAQ em inglês e espanhol.",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Ações"])
    lines.extend(f"- {a}" for a in ACTIONS) if ACTIONS else lines.append("- Nenhuma ação necessária.")
    lines.extend(["", "## Warnings"])
    lines.extend(f"- {w}" for w in WARNINGS) if WARNINGS else lines.append("- Nenhum warning.")
    lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


def main() -> int:
    for rel, data in PAGES.items():
        process(rel, data)
    write_report()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
