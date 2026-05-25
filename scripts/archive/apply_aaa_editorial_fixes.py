#!/usr/bin/env python3
"""
Segunda rodada AAA / 6 estrelas: polimento editorial humano.

Foco:
- reduzir superlativos genéricos;
- melhorar inglês/espanhol turístico;
- substituir expressões corretas, mas menos premium;
- preservar layout, CSS e estrutura HTML.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT: list[str] = []

REPLACEMENTS = {
    # English home / tourism positioning
    "A whole day <span class=\"serif\">high above</span> the city — the best restaurant at Sugarloaf Mountain — with a view of Rio de Janeiro.":
    "A whole day <span class=\"serif\">high above</span> the city — breakfast, Brazilian lunch and sunset drinks with a direct view of Sugarloaf Mountain.",

    "Embaixada Carioca is the <strong>Sugarloaf Cable Car restaurant</strong> — the only restaurant with a direct view of Sugarloaf Mountain, atop Urca Hill. It accompanies your entire day with Sugarloaf Mountain in the foreground, from sunrise to sunset. For those looking for <strong>where to eat in Rio de Janeiro</strong> with the best view of the city, this is the answer.":
    "Embaixada Carioca is located inside <strong>Bondinho Pão de Açúcar Park</strong>, at the first cable car stop on Urca Hill, with a direct view of Sugarloaf Mountain. From breakfast to sunset, it brings together Brazilian food, caipirinhas, cold draft beer and one of Rio’s most iconic views.",

    "The most special <strong>breakfast with Sugarloaf Mountain view</strong> in Rio de Janeiro — served every day from 8:30am to 11:30am at the top of Urca Hill. Artisan sourdough breads, seasonal tropical fruits, mini açaí, homemade cake of the day and specialty coffee from espresso to pour-over. A unique experience among the <strong>best breakfasts in Rio de Janeiro</strong>.":
    "A memorable <strong>breakfast with a Sugarloaf Mountain view</strong> in Rio de Janeiro — served every day from 8:30am to 11:30am at the top of Urca Hill. Artisan sourdough breads, seasonal tropical fruits, mini açaí, homemade cake of the day and specialty coffee from espresso to pour-over.",

    "One of the most special experiences in Rio · book in advance":
    "A scenic way to start the day · book in advance",

    "the only <strong>lunch inside Bondinho Pão de Açúcar Park</strong>":
    "a <strong>Brazilian lunch inside Bondinho Pão de Açúcar Park</strong>",

    "Among the <strong>best restaurants with a view in Rio de Janeiro</strong>, this is the only one at the top of Urca Hill.":
    "For those looking for a <strong>restaurant with a view in Rio de Janeiro</strong>, this is one of the most scenic choices on Urca Hill.",

    "Sugarloaf Cable Car restaurant": "restaurant inside Bondinho Pão de Açúcar Park",
    "best restaurant at Sugarloaf Mountain": "restaurant with a view of Sugarloaf Mountain",
    "The most special": "A memorable",
    "A unique experience": "A memorable experience",

    # Spanish home / tourism positioning
    "Un día entero <span class=\"serif\">en lo alto</span> de la ciudad — el mejor restaurante con vista en Río de Janeiro.":
    "Un día entero <span class=\"serif\">en lo alto</span> de la ciudad — desayuno, almuerzo brasileño y atardecer con vista directa al Pan de Azúcar.",

    "Embaixada Carioca es el <strong>restaurante del Teleférico Pan de Azúcar</strong> — el único restaurante con vista directa al Pan de Azúcar, en lo alto del Morro da Urca. Acompaña tu día entero con el Pan de Azúcar en primer plano, desde el amanecer hasta el atardecer. Para quienes buscan <strong>dónde comer en Río de Janeiro</strong> con la mejor vista de la ciudad, esta es la respuesta.":
    "Embaixada Carioca está dentro del <strong>Parque Bondinho Pão de Açúcar</strong>, en la primera parada del teleférico, en el Morro da Urca, con vista directa al Pan de Azúcar. Desde el desayuno hasta el atardecer, reúne gastronomía brasileña, caipirinhas, chopp helado y una de las vistas más icónicas de Río.",

    "El <strong>desayuno con vista al Pan de Azúcar</strong> más especial de Río de Janeiro — servido todos los días de 8:30 a 11:30 en lo alto del Morro da Urca. Panes artesanales de fermentación natural, frutas tropicales de temporada, mini açaí, bizcocho casero del día y café especial. Una experiencia única entre los <strong>mejores desayunos de Río de Janeiro</strong>.":
    "Un <strong>desayuno con vista al Pan de Azúcar</strong> memorable en Río de Janeiro — servido todos los días de 8:30 a 11:30 en lo alto del Morro da Urca. Panes artesanales de fermentación natural, frutas tropicales de temporada, mini açaí, bizcocho casero del día y café especial.",

    "Una de las experiencias más especiales de Río · reserva con anticipación":
    "Una forma panorámica de empezar el día · reserva con anticipación",

    "el único <strong>almuerzo dentro del Parque Bondinho Pão de Açúcar</strong>":
    "un <strong>almuerzo brasileño dentro del Parque Bondinho Pão de Açúcar</strong>",

    "Entre los <strong>mejores restaurantes con vista de Río de Janeiro</strong>, este es el único en lo alto del Morro da Urca.":
    "Para quienes buscan un <strong>restaurante con vista en Río de Janeiro</strong>, es una de las opciones más panorámicas del Morro da Urca.",

    "restaurante del Teleférico Pan de Azúcar": "restaurante dentro del Parque Bondinho Pão de Açúcar",
    "el mejor restaurante con vista": "un restaurante con vista directa",
    "experiencia única": "experiencia memorable",
    "ddónde": "dónde",

    # Portuguese premium tone
    "o melhor restaurante no Pão de Açúcar": "um restaurante no alto do Morro da Urca",
    "O programa romântico mais único da cidade": "Um dos programas românticos mais especiais da cidade",
    "mais único": "mais especial",
    "Uma experiência única entre os melhores cafés da manhã do Rio de Janeiro.": "Uma experiência memorável para começar o dia no alto do Morro da Urca.",
}

CRITICAL_TERMS = [
    "BondinhSugarloaf",
    "Bondinhel",
    "ddónde",
    "mais único",
    "most unique",
    "Capacity for capacity",
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
        REPORT.append(f"UPDATED: {path.relative_to(ROOT)} | editorial_replacements={count}")


def audit() -> list[str]:
    issues: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(ROOT)
        for term in CRITICAL_TERMS:
            if term in text:
                issues.append(f"{rel}: residual editorial/crítico: {term}")
    return issues


def main() -> int:
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" not in path.parts:
            process(path)

    issues = audit()
    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / "aaa_editorial_polish_report.md"
    report_path.write_text(
        "# Relatório de Polimento Editorial AAA\n\n"
        "## Alterações\n"
        + ("\n".join(f"- {line}" for line in REPORT) if REPORT else "- Nenhuma alteração editorial aplicada")
        + "\n\n## Pendências\n"
        + ("\n".join(f"- {issue}" for issue in issues) if issues else "- Nenhuma pendência editorial crítica detectada")
        + "\n",
        encoding="utf-8",
    )
    print(report_path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
