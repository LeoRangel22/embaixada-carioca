#!/usr/bin/env python3
"""
Auditoria e polimento de idiomas — meta acima de 9.

Foco:
- remover misturas PT/EN/ES;
- remover promessas factualmente incorretas, especialmente vista para o Cristo Redentor;
- ajustar a narrativa de entardecer/sunset à experiência real da Embaixada Carioca;
- priorizar subpáginas que aparecem na home: café, almoço, entardecer/sunset, eventos, cardápio e guia.

Preserva HTML, CSS e layout.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT: list[str] = []

REPLACEMENTS = {
    # =========================
    # FATO: SEM CRISTO REDENTOR
    # =========================
    "Pão de Açúcar, Baía de Guanabara e Cristo Redentor": "Pão de Açúcar e Baía de Guanabara",
    "Pão de Açúcar, a Baía de Guanabara e o Cristo Redentor": "Pão de Açúcar e a Baía de Guanabara",
    "Pão de Açúcar, la Bahía de Guanabara y el Cristo Redentor": "Pan de Azúcar y la Bahía de Guanabara",
    "Sugarloaf Mountain, Guanabara Bay and Christ the Redeemer": "Sugarloaf Mountain and Guanabara Bay",
    "Sugarloaf Mountain, a Baía de Guanabara e o Cristo Redentor": "Sugarloaf Mountain and Guanabara Bay",
    "a Baía de Guanabara e o Cristo Redentor": "a Baía de Guanabara",
    "la Bahía de Guanabara y el Cristo Redentor": "la Bahía de Guanabara",
    "Guanabara Bay and Christ the Redeemer": "Guanabara Bay",
    "e o Cristo Redentor": "",
    "y el Cristo Redentor": "",
    "and Christ the Redeemer": "",

    # =========================
    # ENTARDECER / SUNSET — EXPERIÊNCIA REAL
    # =========================
    "Drinks autorais e pôr do sol sobre o Pão de Açúcar. O lugar mais romântico do Rio de Janeiro no Morro da Urca. Reservas via Tagme.":
    "Entardecer no Morro da Urca com vista para o Pão de Açúcar, caipirinhas, drinks bem feitos, sanduíches e petiscos. Reservas via Tagme.",
    "Drinks, petiscos e pôr do sol sobre o Pão de Açúcar. O entardecer mais romântico do Rio de Janeiro, com música ao vivo no Morro da Urca.":
    "Caipirinhas, drinks bem feitos, sanduíches e petiscos no Morro da Urca, com o Pão de Açúcar em primeiro plano.",
    "Drinks, petiscos e pôr do sol sobre o Pão de Açúcar. O entardecer mais romântico do Rio de Janeiro, com música ao vivo no Morro da Urca.":
    "Caipirinhas, drinks bem feitos, sanduíches e petiscos no Morro da Urca, com o Pão de Açúcar em primeiro plano.",
    "Pôr do sol atrás do Pão de Açúcar visto da Embaixada Carioca, Morro da Urca":
    "Entardecer no Morro da Urca com o Pão de Açúcar em primeiro plano — Embaixada Carioca",
    "O pôr do sol atrás do Pão de Açúcar ocorre entre 17h30 e 18h30, dependendo da época do ano.":
    "O entardecer no Morro da Urca muda de horário ao longo do ano; a experiência combina a vista do Pão de Açúcar com sanduíches, petiscos, caipirinhas e drinks bem feitos.",
    "O entardecer da Embaixada Carioca é considerado um dos programas românticos más bonitos do Rio de Janeiro — pôr do sol sobre o Pão de Açúcar, drinks autorais e vista panorâmica frontal para o Pão de Açúcar da Baía de Guanabara.":
    "O entardecer da Embaixada Carioca é um programa especial no Morro da Urca, com o Pão de Açúcar em primeiro plano, sanduíches, petiscos, caipirinhas e drinks bem feitos.",
    "Caipirinha com cachaça Magnífica premiada, Bossa Sour, caipirinhas da estação, chope Heineken (2º melhor do Brasil), cervejas fluminenses, coquetelaria brasileira e água de coco in natura.":
    "Caipirinhas, Bossa Sour, drinks bem feitos, chope, cervejas, sanduíches, petiscos e água de coco in natura.",
    "Sunset with closed package of drinks &amp; snacks":
    "Sunset-style visit with sandwiches, snacks, caipirinhas and well-made drinks",
    "Sunset as premium itinerary":
    "Sunset-style stop on Urca Hill",
    "Sunset no Parque — DJ TOMMAX": "Entardecer no Morro da Urca",
    "SUNSET NO PARQUE — DJ TOMMAX": "ENTARDECER NO MORRO DA URCA",
    "Live jazz band on the terrace of Embaixada Carioca": "Terrace at Embaixada Carioca",
    "Banda de jazz en vivo en la terraza de Embaixada Carioca": "Terraza de Embaixada Carioca",

    # =========================
    # ACESSO — TEXTO CORRETO
    # =========================
    "O restaurante fica na primeira parada do teleférico — não é necessário comprar ingresso para o bondinho para acessar o restaurante.":
    "O restaurante fica na primeira parada do teleférico. O acesso pode ser feito pelo bondinho, com ingresso regular do Parque Bondinho Pão de Açúcar, ou pela trilha da Praia Vermelha, quando aberta, sem ingresso do bondinho. A reserva no restaurante garante a mesa, mas não inclui o ingresso do Parque.",
    "You do not need to buy a cable car ticket to access the restaurant. Access is via Av. Pasteur, 520, Urca, Rio de Janeiro. The cable car takes you to Urca Hill (1st stop), where Embaixada Carioca is located.":
    "Access is by cable car, with a regular Bondinho Pão de Açúcar Park ticket, or by the Praia Vermelha trail, when open, without a cable car ticket. A restaurant reservation guarantees your table, but does not include the park ticket.",
    "No necesitas comprar entrada del teleférico para acceder al restaurante. El acceso es por Av. Pasteur, 520, Urca, Río de Janeiro. El teleférico lleva al Morro da Urca, donde se encuentra Embaixada Carioca.":
    "El acceso es por teleférico, con entrada regular del Parque Bondinho Pão de Açúcar, o por el sendero de Praia Vermelha, cuando esté abierto, sin entrada del teleférico. La reserva en el restaurante garantiza la mesa, pero no incluye la entrada del Parque.",

    # =========================
    # EN EVENTOS — RESÍDUOS DE PORTUGUÊS
    # =========================
    "Parcerias com agências e operadoras para receber grupos de turistas,\n          delegações e clientes VIP em experiências autorais do Rio.":
    "Partnerships with travel agencies and tour operators to host tourist groups, delegations and VIP clients through curated Rio experiences.",
    "<div class=\"num\"><b>02</b> Estrutura &amp; capacidade</div>":
    "<div class=\"num\"><b>02</b> Structure &amp; capacity</div>",
    "Multiple halls and panoramic terraces at <strong>Urca Hill</strong>, with views to Sugarloaf Mountain, a Baía de Guanabara e o Cristo Redentor. Full catering infrastructure, A/V e equipe receptiva multilíngue. O <strong>lugar para comemorar aniversário no Rio de Janeiro</strong> mais especial da cidade — e um dos <strong>melhores espaços para corporate events no Rio de Janeiro</strong>.":
    "Multiple halls and panoramic terraces on <strong>Urca Hill</strong>, with views of Sugarloaf Mountain and Guanabara Bay. Full catering infrastructure, A/V support and a multilingual hospitality team. A scenic venue for private celebrations, corporate events and curated group experiences in Rio de Janeiro.",
    "<span class=\"d\">salão principal</span>": "<span class=\"d\">main dining room</span>",
    "<span class=\"l\">Salões</span>": "<span class=\"l\">Rooms</span>",
    "<span class=\"d\">+ terraços panorâmicos</span>": "<span class=\"d\">+ panoramic terraces</span>",
    "<span class=\"l\">Idiomas</span>": "<span class=\"l\">Languages</span>",
    "<span class=\"d\">equipe receptiva multilíngue</span>": "<span class=\"d\">multilingual hospitality team</span>",
    "300<sup>+</sup>": "Capacity varies",
    "standing guests": "by format and setup",

    # =========================
    # ES EVENTOS — RESÍDUOS DE PORTUGUÊS
    # =========================
    "<a href=\"../index.html\">Home</a>": "<a href=\"../index.html\">Inicio</a>",
    "Eventos no <span class=\"serif\">Morro da Urca</span><br/>": "Eventos en el <span class=\"serif\">Morro da Urca</span><br/>",
    "O <strong>espacio para eventos mais bonito do Río de Janeiro</strong> — no alto do Morro da Urca, a 227 metros, con vista panorámica al Pan de Azúcar, a Bahía de Guanabara e o Cristo Redentor. Reuniões executivas, almuerzos corporativos, lanzamientos, aniversarios e itinerarios para grupos internacionales — todos recebidos com a gastronomía brasileña premiada e a vista mais impressionante da cidade.":
    "Un <strong>espacio para eventos con vista panorámica en Río de Janeiro</strong>, en lo alto del Morro da Urca, a 227 metros, con vista al Pan de Azúcar y la Bahía de Guanabara. Reuniones ejecutivas, almuerzos corporativos, lanzamientos, aniversarios e itinerarios para grupos internacionales, con gastronomía brasileña y una de las vistas más icónicas de la ciudad.",
    "Fale com nossa equipe": "Hablar con nuestro equipo",
    "<div class=\"num\"><b>01</b> Para quem</div>": "<div class=\"num\"><b>01</b> Para quién</div>",
    "Dois universos, <span class=\"serif\">uma vista</span> — eventos en Morro da Urca para empresas y agencias.":
    "Dos universos, <span class=\"serif\">una vista</span> — eventos en el Morro da Urca para empresas y agencias.",
    "Do evento corporativo ao roteiro premium para grupos internacionais — recebemos cada formato com curadoria sob medida no <strong>espacio para eventos do Morro da Urca</strong>. Entre os <strong>lugares para comemorar no Río de Janeiro</strong>, este é o único con vista panorámica al Pan de Azúcar, a Bahía de Guanabara e o Cristo Redentor. A gastronomía brasileña premiada é o conteúdo.":
    "Del evento corporativo al itinerario premium para grupos internacionales, cada formato se recibe con curaduría a medida en un <strong>espacio para eventos en el Morro da Urca</strong>. Entre los lugares para celebrar en Río de Janeiro, se destaca por la vista panorámica al Pan de Azúcar y la Bahía de Guanabara, con gastronomía brasileña como parte central de la experiencia.",
    "Restaurante del Teleférico · Restaurante Carioca Tradicional de Calidad · Morro da Urca · Parque Bondinho · Río de Janeiro · Brasil":
    "Restaurante en el Parque Bondinho · Gastronomía carioca tradicional · Morro da Urca · Río de Janeiro · Brasil",
    "Espaço panorâmico para eventos en Embaixada Carioca": "Espacio panorámico para eventos en Embaixada Carioca",
    "al Pan de Azúcar, a Bahía de Guanabara e o Cristo Redentor": "al Pan de Azúcar y la Bahía de Guanabara",
    "a Bahía de Guanabara e o Cristo Redentor": "la Bahía de Guanabara",
    "no alto do Morro da Urca": "en lo alto del Morro da Urca",
    "do Morro da Urca": "del Morro da Urca",
    "mais bonito": "más bonito",
    "mais impressionante": "más impresionante",
    "recebidos com": "recibidos con",
    "Reuniões": "Reuniones",
    "reuniões": "reuniones",
    "ao roteiro": "al itinerario",
    "uma vista": "una vista",
    "este é": "este es",
    "os lugares": "los lugares",
    "nossa equipe": "nuestro equipo",
    "comemorar": "celebrar",

    # =========================
    # PRÊMIO DA FEIJOADA — ORIGEM CORRETA
    # =========================
    "🏆 Melhor Feijoada do Rio — Veja Rio 2025/2026": "🏆 Feijoada premiada da Academia da Cachaça — servida na Embaixada Carioca",
    "🏆 Best Feijoada in Rio — Veja Rio 2025/2026": "🏆 Award-winning feijoada from Academia da Cachaça — served at Embaixada Carioca",
    "🏆 Mejor Feijoada de Río — Veja Rio 2025/2026": "🏆 Feijoada premiada de Academia da Cachaça — servida en Embaixada Carioca",
    "a <strong>award-winning feijoada</strong>": "the <strong>award-winning feijoada from Academia da Cachaça</strong>",
    "la <strong>feijoada premiada</strong>": "la <strong>feijoada premiada de Academia da Cachaça</strong>",
    "<strong>feijoada premiada</strong> da Academia da Cachaça": "<strong>feijoada premiada da Academia da Cachaça</strong>",
    "Best Feijoada in Brazil": "Award-winning feijoada from Academia da Cachaça",
    "Mejor Feijoada de Brasil": "Feijoada premiada de Academia da Cachaça",

    # =========================
    # LIMPEZA DE IDIOMA SOLTA
    # =========================
    "en lo alto del Morro da Urca": "no alto do Morro da Urca",
    "más bonitos": "mais bonitos",
    "del Morro da Urca": "do Morro da Urca",
    "vista panorâmica del Morro da Urca": "vista panorâmica do Morro da Urca",
    "Rio de Janeiro": "Rio de Janeiro",
}

FORBIDDEN = [
    "Cristo Redentor",
    "Christ the Redeemer",
    "BondinhSugarloaf",
    "Bondinhel",
    "Quando Every day",
    "Harmonização",
    "Roteiros & grupos",
    "Eventos corporativos",
    "Fale com nossa equipe",
    "a Baía de Guanabara e o Cristo",
    "la Bahía de Guanabara y el Cristo",
    "A/V e equipe",
    "lugar para comemorar aniversário no Rio de Janeiro",
    "salão principal",
    "terraços panorâmicos",
    "equipe receptiva",
    "Eventos no <span",
    "O <strong>espacio",
    "Dois universos",
    "Do evento corporativo",
    "música ao vivo no Morro da Urca",
    "pôr do sol atrás do Pão de Açúcar",
    "pôr do sol sobre o Pão de Açúcar",
]

PRIORITY_FILES = {
    "index.html",
    "cafe-da-manha.html",
    "almoco.html",
    "entardecer.html",
    "eventos.html",
    "cardapio.html",
    "guia-do-rio.html",
    "en/index.html",
    "en/cafe-da-manha.html",
    "en/almoco.html",
    "en/entardecer.html",
    "en/sunset.html",
    "en/eventos.html",
    "en/cardapio.html",
    "en/guia-do-rio.html",
    "es/index.html",
    "es/cafe-da-manha.html",
    "es/almoco.html",
    "es/entardecer.html",
    "es/atardecer.html",
    "es/eventos.html",
    "es/cardapio.html",
    "es/guia-do-rio.html",
}


def process(path: Path) -> None:
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    count = 0
    for old, new in REPLACEMENTS.items():
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            count += c
    if text != original:
        path.write_text(text, encoding="utf-8")
        marker = "PRIORITY" if path.relative_to(ROOT).as_posix() in PRIORITY_FILES else "SECONDARY"
        REPORT.append(f"{marker}: UPDATED: {path.relative_to(ROOT)} | replacements={count}")


def audit() -> list[str]:
    issues: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        for term in FORBIDDEN:
            if term in text:
                issues.append(f"{rel}: residual: {term}")
    return issues


def main() -> int:
    html_files = sorted([p for p in ROOT.rglob("*.html") if ".git" not in p.parts])
    # Prioriza as subpáginas da home, depois aplica no restante.
    html_files.sort(key=lambda p: (p.relative_to(ROOT).as_posix() not in PRIORITY_FILES, p.relative_to(ROOT).as_posix()))
    for path in html_files:
        process(path)

    issues = audit()
    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report = report_dir / "language_score9_report.md"
    report.write_text(
        "# Auditoria de Idiomas — Meta > 9\n\n"
        "## Escopo prioritário\n"
        "- Home PT/EN/ES\n"
        "- Café da manhã\n"
        "- Almoço\n"
        "- Entardecer / Sunset / Atardecer\n"
        "- Eventos\n"
        "- Cardápio\n"
        "- Guia do Rio\n\n"
        "## Alterações aplicadas\n"
        + ("\n".join(f"- {line}" for line in REPORT) if REPORT else "- Nenhuma alteração aplicada")
        + "\n\n## Pendências críticas\n"
        + ("\n".join(f"- {issue}" for issue in issues) if issues else "- Nenhuma pendência crítica de idioma ou fato detectada")
        + "\n",
        encoding="utf-8",
    )
    print(report.read_text(encoding="utf-8"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
