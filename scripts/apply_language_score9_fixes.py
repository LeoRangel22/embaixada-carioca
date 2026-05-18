#!/usr/bin/env python3
"""
Polimento de idiomas para elevar a nota PT/EN/ES acima de 9.
Foco: remover resíduos de português em EN/ES, textos híbridos e claims de capacidade/premiação mal formulados.
Preserva HTML, CSS e layout.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT: list[str] = []

REPLACEMENTS = {
    # EN eventos — residues and hybrid copy
    "Parcerias com agências e operadoras para receber grupos de turistas,\n          delegações e clientes VIP em experiências autorais do Rio.":
    "Partnerships with travel agencies and tour operators to host tourist groups, delegations and VIP clients through curated Rio experiences.",

    "<div class=\"num\"><b>02</b> Estrutura &amp; capacidade</div>":
    "<div class=\"num\"><b>02</b> Structure &amp; capacity</div>",

    "Multiple halls and panoramic terraces at <strong>Urca Hill</strong>, with views to Sugarloaf Mountain, a Baía de Guanabara e o Cristo Redentor. Full catering infrastructure, A/V e equipe receptiva multilíngue. O <strong>lugar para comemorar aniversário no Rio de Janeiro</strong> mais especial da cidade — e um dos <strong>melhores espaços para corporate events no Rio de Janeiro</strong>.":
    "Multiple halls and panoramic terraces on <strong>Urca Hill</strong>, with views of Sugarloaf Mountain, Guanabara Bay and Christ the Redeemer. Full catering infrastructure, A/V support and a multilingual hospitality team. A scenic venue for private celebrations, corporate events and curated group experiences in Rio de Janeiro.",

    "<span class=\"d\">salão principal</span>":
    "<span class=\"d\">main dining room</span>",
    "<span class=\"l\">Salões</span>":
    "<span class=\"l\">Rooms</span>",
    "<span class=\"d\">+ terraços panorâmicos</span>":
    "<span class=\"d\">+ panoramic terraces</span>",
    "<span class=\"l\">Idiomas</span>":
    "<span class=\"l\">Languages</span>",
    "<span class=\"d\">equipe receptiva multilíngue</span>":
    "<span class=\"d\">multilingual hospitality team</span>",
    "300<sup>+</sup>": "Capacity varies",
    "standing guests": "by format and setup",

    # ES eventos — severe hybrid text
    "<a href=\"../index.html\">Home</a>":
    "<a href=\"../index.html\">Inicio</a>",
    "Eventos no <span class=\"serif\">Morro da Urca</span><br/>":
    "Eventos en el <span class=\"serif\">Morro da Urca</span><br/>",
    "O <strong>espacio para eventos mais bonito do Río de Janeiro</strong> — no alto do Morro da Urca, a 227 metros, con vista panorámica al Pan de Azúcar, a Bahía de Guanabara e o Cristo Redentor. Reuniões executivas, almuerzos corporativos, lanzamientos, aniversarios e itinerarios para grupos internacionales — todos recebidos com a gastronomía brasileña premiada e a vista mais impressionante da cidade.":
    "Un <strong>espacio para eventos con vista panorámica en Río de Janeiro</strong>, en lo alto del Morro da Urca, a 227 metros, con vista al Pan de Azúcar, la Bahía de Guanabara y el Cristo Redentor. Reuniones ejecutivas, almuerzos corporativos, lanzamientos, aniversarios e itinerarios para grupos internacionales, con gastronomía brasileña y una de las vistas más icónicas de la ciudad.",
    "Fale com nossa equipe": "Hablar con nuestro equipo",
    "<div class=\"num\"><b>01</b> Para quem</div>":
    "<div class=\"num\"><b>01</b> Para quién</div>",
    "Dois universos, <span class=\"serif\">uma vista</span> — eventos en Morro da Urca para empresas y agencias.":
    "Dos universos, <span class=\"serif\">una vista</span> — eventos en el Morro da Urca para empresas y agencias.",
    "Do evento corporativo ao roteiro premium para grupos internacionais — recebemos cada formato com curadoria sob medida no <strong>espacio para eventos do Morro da Urca</strong>. Entre os <strong>lugares para comemorar no Río de Janeiro</strong>, este é o único con vista panorámica al Pan de Azúcar, a Bahía de Guanabara e o Cristo Redentor. A gastronomía brasileña premiada é o conteúdo.":
    "Del evento corporativo al itinerario premium para grupos internacionales, cada formato se recibe con curaduría a medida en un <strong>espacio para eventos en el Morro da Urca</strong>. Entre los lugares para celebrar en Río de Janeiro, se destaca por la vista panorámica al Pan de Azúcar, la Bahía de Guanabara y el Cristo Redentor, con gastronomía brasileña como parte central de la experiencia.",
    "Restaurante del Teleférico · Restaurante Carioca Tradicional de Calidad · Morro da Urca · Parque Bondinho · Río de Janeiro · Brasil":
    "Restaurante en el Parque Bondinho · Gastronomía carioca tradicional · Morro da Urca · Río de Janeiro · Brasil",
    "Espaço panorâmico para eventos en Embaixada Carioca":
    "Espacio panorámico para eventos en Embaixada Carioca",
    "al Pan de Azúcar, a Bahía de Guanabara e o Cristo Redentor":
    "al Pan de Azúcar, la Bahía de Guanabara y el Cristo Redentor",
    "a Bahía de Guanabara e o Cristo Redentor":
    "la Bahía de Guanabara y el Cristo Redentor",
    "no alto do Morro da Urca": "en lo alto del Morro da Urca",
    "do Morro da Urca": "del Morro da Urca",
    "mais bonito": "más bonito",
    "mais impressionante": "más impresionante",
    "recebidos com": "recibidos con",
    "reuniões": "reuniones",
    "Reuniões": "Reuniones",
    "ao roteiro": "al itinerario",
    "para quem": "para quién",
    "uma vista": "una vista",
    "este é": "este es",
    "os lugares": "los lugares",
    "equipe": "equipo",
    "nossa equipe": "nuestro equipo",
    "comemorar": "celebrar",

    # Awards — Academia da Cachaça origin, neutral and factual
    "🏆 Best Feijoada in Rio — Veja Rio 2025/2026":
    "🏆 Award-winning feijoada from Academia da Cachaca — served at Embaixada Carioca",
    "🏆 Mejor Feijoada de Río — Veja Rio 2025/2026":
    "🏆 Feijoada premiada de Academia da Cachaca — servida en Embaixada Carioca",
    "Best Feijoada in Rio": "Award-winning feijoada from Academia da Cachaca",
    "Mejor Feijoada de Río": "Feijoada premiada de Academia da Cachaca",

    # Global spelling/consistency in schema-generated pages
    "Pao de Acucar": "Pão de Açúcar",
    "Pan de Azucar": "Pan de Azúcar",
    "Cachaca": "Cachaça",
    "brasileno": "brasileño",
    "Rio — Veja Rio": "Río — Veja Rio",
}

FORBIDDEN = [
    "BondinhSugarloaf",
    "Bondinhel",
    "Quando Every day",
    "Harmonização",
    "Roteiros & grupos",
    "Eventos corporativos",
    "Fale com nossa equipe",
    "a Baía de Guanabara e o Cristo Redentor",
    "A/V e equipe",
    "lugar para comemorar aniversário no Rio de Janeiro",
    "salão principal",
    "terraços panorâmicos",
    "equipe receptiva",
    "Eventos no <span",
    "O <strong>espacio",
    "Dois universos",
    "Do evento corporativo",
]


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
        REPORT.append(f"UPDATED: {path.relative_to(ROOT)} | replacements={count}")


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
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" not in path.parts:
            process(path)
    issues = audit()
    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report = report_dir / "language_score9_report.md"
    report.write_text(
        "# Auditoria de Idiomas — Meta > 9\n\n"
        "## Alterações aplicadas\n"
        + ("\n".join(f"- {line}" for line in REPORT) if REPORT else "- Nenhuma alteração aplicada")
        + "\n\n## Pendências críticas\n"
        + ("\n".join(f"- {issue}" for issue in issues) if issues else "- Nenhuma pendência crítica de idioma detectada")
        + "\n",
        encoding="utf-8",
    )
    print(report.read_text(encoding="utf-8"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
