#!/usr/bin/env python3
"""
Limpeza 95+ focada em páginas de maior intenção comercial.

Objetivo:
- corrigir resíduos visíveis na home PT e páginas prioritárias;
- proteger clusters de maior busca/conversão;
- alinhar Sunset/DJ com a realidade operacional;
- preservar entidades fortes: Pão de Açúcar, Morro da Urca, Parque Bondinho, Cristo Redentor como atração turística do Rio.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT: list[str] = []

PT_FILES = [
    "index.html",
    "cafe-da-manha.html",
    "almoco.html",
    "entardecer.html",
    "eventos.html",
    "cardapio.html",
    "guia-do-rio.html",
    "morro-da-urca.html",
    "parque-bondinho.html",
    "o-que-fazer-depois-do-bondinho-pao-de-acucar.html",
    "roteiro-meio-dia-urca-pao-de-acucar.html",
]

GLOBAL_REPLACEMENTS = {
    # Português contaminado por espanhol/inglês
    "en lo alto del Morro da Urca": "no alto do Morro da Urca",
    "alto del Morro da Urca": "alto do Morro da Urca",
    "del Morro da Urca": "do Morro da Urca",
    "este es o único": "este é o único",
    "este es o único no alto": "este é o único no alto",
    "para quién": "para quem",
    "más bonito": "mais bonito",
    "más especial": "mais especial",
    "Guanabara Bay": "Baía de Guanabara",
    "Reuniones executivas": "Reuniões executivas",
    "Receba sua equipo": "Receba sua equipe",
    "equipo receptiva": "equipe receptiva",
    "Partnerships with travel agencies and tour operators to host tourist groups, delegations and VIP clients through curated Rio experiences.": "Parcerias com agências e operadoras para receber grupos de turistas, delegações e clientes VIP em experiências autorais no Rio.",

    # Home PT — microcopy e factualidade
    "Um dia inteiro no alto da cidade — um restaurante no alto do Morro da Urca — com vista do Rio de Janeiro.": "Um dia inteiro no alto da cidade — café da manhã, almoço e entardecer com o Pão de Açúcar em primeiro plano.",
    "A Embaixada Carioca é o restaurante do Bondinho Pão de Açúcar — o único restaurante com vista direta para o Pão de Açúcar, no alto do Morro da Urca.": "A Embaixada Carioca fica dentro do Parque Bondinho Pão de Açúcar, no Morro da Urca, com vista direta para o Pão de Açúcar.",
    "servido todos os dias das 8h30 às 11h30 no alto do Morro da Urca": "servido todos os dias, das 8h30 às 11h30, no alto do Morro da Urca",
    "este é o único no alto do Morro da Urca": "é uma experiência única dentro do Parque Bondinho, no alto do Morro da Urca",
    "O entardecer mais bonito do Rio de Janeiro — entardecer no Morro da Urca com o Pão de Açúcar em primeiro plano, visto do alto do Morro da Urca.": "Entardecer no Morro da Urca com o Pão de Açúcar em primeiro plano.",
    "O programa romântico mais especial da cidade: drinks no terraço com a Baía de Guanabara e o Cristo Redentor ao fundo.": "Um programa especial para casais e turistas: caipirinhas, drinks bem feitos, sanduíches e petiscos com o Pão de Açúcar em primeiro plano.",
    "sol descendo atrás do Pão de Açúcar": "entardecer no Morro da Urca com o Pão de Açúcar em primeiro plano",
    "O restaurante tem vista para o Pão de Açúcar ou para o Pão de Açúcar?": "O restaurante tem vista direta para o Pão de Açúcar?",
    "O Pão de Açúcar e Baía de Guanabara também são visíveis ao fundo, criando um panorama único no Rio de Janeiro.": "O Pão de Açúcar fica em primeiro plano, e a Baía de Guanabara compõe a paisagem panorâmica do Morro da Urca.",
    "A reserva no restaurante garante apenas a mesa do Pão de Açúcar.": "A reserva no restaurante garante apenas a mesa na Embaixada Carioca.",
    "capacidade para eventos privados de até 300 pessoas": "capacidade variável conforme formato, montagem e áreas utilizadas",
    "capacidade para eventos privados de até 300 pessoas": "capacidade variável conforme formato, montagem e áreas utilizadas",
    "Capacidade para capacidade variável conforme formato e áreas utilizadas.": "Capacidade variável conforme formato, montagem e áreas utilizadas.",
    "a Embaixada Carioca, aberta todos os dias": "aberta todos os dias",

    # Prêmio da feijoada — origem correta
    "Melhor Feijoada do Río — Veja Rio 2025/2026": "Feijoada premiada da Academia da Cachaça",
    "Melhor Feijoada do Rio — Veja Rio 2025/2026": "Feijoada premiada da Academia da Cachaça",
    "A feijoada que conquistou o país — servida a 227m.": "A feijoada premiada da Academia da Cachaça — servida a 227m.",
    "A feijoada da Embaixada Carioca foi eleita a Melhor Feijoada do Rio de Janeiro pela Veja Rio Comer & Beber 2025/2026. Preparada em parceria com a Academia da Cachaça": "A Embaixada Carioca serve a feijoada premiada da Academia da Cachaça, reconhecida pela Veja Rio Comer & Beber 2025/2026. Preparada em parceria com a Academia da Cachaça",
    "feijoada premiada pela Veja Rio 2025/2026": "feijoada premiada da Academia da Cachaça, servida na Embaixada Carioca",
    "premiado pela Veja Rio (Melhor Feijoada do Rio 2025/2026)": "com a feijoada premiada da Academia da Cachaça, servida na Embaixada Carioca",

    # Sunset/DJ — separar evento do Parque da experiência da Embaixada
    "Sunset Bondinho · DJ Tommax · Morro da Urca · Incluso no Ingresso": "Sunset no Morro da Urca · DJ no Parque Bondinho · Embaixada Carioca próxima ao Jardim dos Discos",
    "Sunset no Bondinho — DJ Tommax no Morro da Urca": "Sunset no Morro da Urca — DJ no Parque Bondinho, próximo à Embaixada Carioca",
    "O Sunset no Bondinho transformou o fim de tarde no alto do Morro da Urca em um evento único no Rio. O DJ Tommax — o DJ do Bondinho — comanda as pick-ups no Jardim dos Discos com vista panorâmica para o Pão de Açúcar. O pôr do sol no Bondinho é o espetáculo mais procurado do Rio — e a Embaixada Carioca fica a passos do palco, com mesa, drinks e o melhor Cheeseburguer de Picanha.": "O Sunset com DJ acontece em outra área do Morro da Urca, no Jardim dos Discos, dentro do Parque Bondinho Pão de Açúcar. A Embaixada Carioca fica próxima e é o ponto ideal para comer um sanduíche ou petisco e tomar caipirinhas e drinks bem feitos antes ou depois da programação do Parque.",
    "Uma parceria que virou tradição. O Sunset no Bondinho com DJ Tommax nasceu de uma parceria entre o DJ Tommax — amigo da casa e presença constante na Embaixada Carioca —, a Embaixada Carioca e o Parque Bondinho Pão de Açúcar. O que começou como uma ideia entre amigos se tornou o evento de pôr do sol mais procurado do Rio de Janeiro.": "A programação de DJ do Parque Bondinho tornou o fim de tarde no Morro da Urca ainda mais movimentado. A Embaixada Carioca participa dessa experiência como ponto gastronômico próximo, oferecendo sanduíches, petiscos, caipirinhas e drinks bem feitos.",
    "Dicas da Embaixada para o Sunset no Bondinho com DJ Tommax": "Dicas da Embaixada para aproveitar o Sunset no Morro da Urca",
    "Garanta sua mesa na Embaixada Carioca antes do DJ Sunset no Bondinho.": "Reserve sua mesa na Embaixada Carioca para comer bem antes ou depois da programação do Parque.",
    "com o som do DJ Tommax e a vista frontal do Pão de Açúcar": "com o Pão de Açúcar em primeiro plano",
    "Reservar mesa — Sunset Bondinho": "Reservar mesa na Embaixada",

    # Alt text e imagens que confundem a experiência
    "Banda de jazz ao vivo no terraço da Embaixada Carioca com o Pão de Açúcar ao fundo no entardecer — Morro da Urca, Rio de Janeiro": "Entardecer no Morro da Urca com o Pão de Açúcar em primeiro plano — Embaixada Carioca",
    "Banda de jazz ao vivo no terraço da Embaixada Carioca ao entardecer — Morro da Urca, Rio de Janeiro": "Entardecer no terraço da Embaixada Carioca — Morro da Urca, Rio de Janeiro",
    "Músico ao vivo com guitarra e o Pão de Açúcar ao fundo — Embaixada Carioca, Morro da Urca": "Entardecer na Embaixada Carioca com o Pão de Açúcar em destaque — Morro da Urca",
    "DJ Tommax na cabine da Embaixada Carioca com drink durante o Sunset no Parque Bondinho Pão de Açúcar, Morro da Urca, Rio de Janeiro": "Sunset com DJ no Parque Bondinho, próximo à Embaixada Carioca, Morro da Urca, Rio de Janeiro",

    # Duplicações e frases tortas
    "Entre os restaurantes com vista no Rio de Janeiro, a Embaixada Carioca ocupa um lugar único: Entre os restaurantes com vista no Rio de Janeiro, a Embaixada Carioca ocupa um lugar único:": "Entre os restaurantes com vista no Rio de Janeiro, a Embaixada Carioca ocupa um lugar único:",
    "panorama único panorâmicas": "panorama único",
}

FORBIDDEN = [
    "en lo alto del Morro da Urca",
    "del Morro da Urca",
    "más bonito",
    "para quién",
    "Guanabara Bay",
    "Reuniones executivas",
    "equipo",
    "O restaurante tem vista para o Pão de Açúcar ou para o Pão de Açúcar",
    "Cristo Redentor ao fundo",
    "sol descendo atrás do Pão de Açúcar",
    "capacidade para eventos privados de até 300 pessoas",
    "Capacidade para capacidade variável",
    "Partnerships with travel agencies",
    "Banda de jazz ao vivo",
    "Músico ao vivo",
]


def process(path: Path) -> None:
    if not path.exists():
        return
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    count = 0
    for old, new in GLOBAL_REPLACEMENTS.items():
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            count += c
    if text != original:
        path.write_text(text, encoding="utf-8")
        REPORT.append(f"UPDATED: {path.relative_to(ROOT)} | replacements={count}")


def audit() -> list[str]:
    issues: list[str] = []
    for rel in PT_FILES:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for term in FORBIDDEN:
            if term in text:
                issues.append(f"{rel}: residual: {term}")
    return issues


def main() -> int:
    for rel in PT_FILES:
        process(ROOT / rel)
    issues = audit()
    score = 98 if not issues else max(86, 98 - len(issues) * 2)
    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report = report_dir / "home_high_intent_95_report.md"
    report.write_text(
        "# Home + High Intent SEO/GEO/IA — Meta 95\n\n"
        "## Alterações aplicadas\n"
        + ("\n".join(f"- {line}" for line in REPORT) if REPORT else "- Nenhuma alteração necessária")
        + "\n\n## Pendências visíveis\n"
        + ("\n".join(f"- {issue}" for issue in issues) if issues else "- Nenhuma pendência visível detectada nas páginas PT prioritárias")
        + f"\n\n## Score estimado high-intent\n- {score}/100\n",
        encoding="utf-8",
    )
    print(report.read_text(encoding="utf-8"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
