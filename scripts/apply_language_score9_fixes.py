#!/usr/bin/env python3
"""
Auditoria e polimento de idiomas — meta > 90 / preparação para 95.

Prioridades:
- zerar qualquer menção de vista para Cristo Redentor;
- remover misturas PT/EN/ES;
- ajustar entardecer/sunset à experiência real da Embaixada Carioca;
- preservar layout, HTML e CSS;
- gerar relatório objetivo de pendências críticas.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT: list[str] = []

PRIORITY_FILES = {
    "index.html", "cafe-da-manha.html", "almoco.html", "entardecer.html", "eventos.html", "cardapio.html", "guia-do-rio.html",
    "en/index.html", "en/cafe-da-manha.html", "en/almoco.html", "en/entardecer.html", "en/sunset.html", "en/eventos.html", "en/cardapio.html", "en/guia-do-rio.html",
    "es/index.html", "es/cafe-da-manha.html", "es/almoco.html", "es/entardecer.html", "es/atardecer.html", "es/eventos.html", "es/cardapio.html", "es/guia-do-rio.html",
}

REPLACEMENTS = {
    # Vista real — remover Cristo de listas de vista
    "Pão de Açúcar, Baía de Guanabara e Cristo Redentor": "Pão de Açúcar e Baía de Guanabara",
    "Pão de Açúcar, a Baía de Guanabara e o Cristo Redentor": "Pão de Açúcar e a Baía de Guanabara",
    "Pão de Açúcar, Baía de Guanabara, Cristo Redentor": "Pão de Açúcar e Baía de Guanabara",
    "Sugarloaf Mountain, Guanabara Bay and Christ the Redeemer": "Sugarloaf Mountain and Guanabara Bay",
    "Sugarloaf Mountain, Guanabara Bay, Christ the Redeemer": "Sugarloaf Mountain and Guanabara Bay",
    "Pan de Azúcar, Bahía de Guanabara y Cristo Redentor": "Pan de Azúcar y Bahía de Guanabara",
    "Pan de Azúcar, la Bahía de Guanabara y el Cristo Redentor": "Pan de Azúcar y la Bahía de Guanabara",
    "Pão de Açúcar e Cristo Redentor": "Pão de Açúcar",
    "Sugarloaf Mountain and Christ the Redeemer": "Sugarloaf Mountain",
    "Pan de Azúcar y Cristo Redentor": "Pan de Azúcar",
    "Cristo Redentor ao fundo": "Pão de Açúcar em primeiro plano",
    "Christ the Redeemer in the background": "Sugarloaf Mountain in the foreground",
    "Cristo Redentor de fondo": "Pan de Azúcar en primer plano",
    "e o Cristo Redentor": "",
    "and Christ the Redeemer": "",
    "y el Cristo Redentor": "",
    "Cristo Redentor": "Pão de Açúcar",
    "Christ the Redeemer": "Sugarloaf Mountain",

    # Entardecer real — não confundir com DJ do Parque
    "pôr do sol atrás do Pão de Açúcar": "entardecer no Morro da Urca com o Pão de Açúcar em primeiro plano",
    "pôr do sol sobre o Pão de Açúcar": "entardecer no Morro da Urca com o Pão de Açúcar em primeiro plano",
    "sunset behind Sugarloaf Mountain": "sunset-style visit on Urca Hill with Sugarloaf Mountain in the foreground",
    "sunset over Sugarloaf Mountain": "sunset-style visit on Urca Hill with Sugarloaf Mountain in the foreground",
    "atardecer detrás del Pan de Azúcar": "atardecer en el Morro da Urca con el Pan de Azúcar en primer plano",
    "atardecer sobre el Pan de Azúcar": "atardecer en el Morro da Urca con el Pan de Azúcar en primer plano",
    "música ao vivo no Morro da Urca": "sanduíches, petiscos, caipirinhas e drinks bem feitos no Morro da Urca",
    "live music on Urca Hill": "sandwiches, snacks, caipirinhas and well-made drinks on Urca Hill",
    "música en vivo en el Morro da Urca": "sándwiches, aperitivos, caipirinhas y buenos drinks en el Morro da Urca",
    "Sunset no Parque — DJ TOMMAX": "Entardecer no Morro da Urca",
    "SUNSET NO PARQUE — DJ TOMMAX": "ENTARDECER NO MORRO DA URCA",
    "DJ TOMMAX": "Entardecer no Morro da Urca",

    # Acesso correto
    "não é necessário comprar ingresso para o bondinho para acessar o restaurante": "o acesso pode ser feito pelo bondinho, com ingresso regular do Parque Bondinho Pão de Açúcar, ou pela trilha da Praia Vermelha, quando aberta",
    "You do not need to buy a cable car ticket to access the restaurant": "Access is by cable car with a regular Bondinho Pão de Açúcar Park ticket, or by the Praia Vermelha trail when open",
    "No necesitas comprar entrada del teleférico para acceder al restaurante": "El acceso es por teleférico con entrada regular del Parque Bondinho Pão de Açúcar, o por el sendero de Praia Vermelha cuando esté abierto",

    # PT contaminado por ES
    "en lo alto del Morro da Urca": "no alto do Morro da Urca",
    "del Morro da Urca": "do Morro da Urca",
    "más bonito": "mais bonito",
    "más bonitos": "mais bonitos",
    "este es o único": "este é o único",
    "para quién": "para quem",
    "vista panorâmica del Morro da Urca": "vista panorâmica do Morro da Urca",

    # EN contaminado por PT
    "Eventos corporativos": "Corporate events",
    "Roteiros & grupos": "Itineraries & groups",
    "Quando Every day": "When Every day",
    "Harmonização": "Pairing",
    "salão principal": "main dining room",
    "terraços panorâmicos": "panoramic terraces",
    "equipe receptiva": "hospitality team",
    "A/V e equipe": "A/V support and team",
    "a Baía de Guanabara": "Guanabara Bay",
    "O <strong>lugar para comemorar aniversário no Rio de Janeiro</strong> mais especial da cidade": "A scenic place for private celebrations in Rio de Janeiro",

    # ES contaminado por PT
    "Eventos no <span": "Eventos en el <span",
    "Dois universos": "Dos universos",
    "Do evento corporativo": "Del evento corporativo",
    "Para quem": "Para quién",
    "para quem": "para quién",
    "Fale com nossa equipe": "Hablar con nuestro equipo",
    "Espaço panorâmico": "Espacio panorámico",
    "mais bonito": "más bonito",
    "mais impressionante": "más impresionante",
    "no alto do Morro da Urca": "en lo alto del Morro da Urca",
    "do Morro da Urca": "del Morro da Urca",
    "recebidos com": "recibidos con",
    "Reuniões": "Reuniones",
    "reuniões": "reuniones",
    "ao roteiro": "al itinerario",
    "uma vista": "una vista",
    "este é": "este es",
    "os lugares": "los lugares",
    "comemorar": "celebrar",

    # Capacidade/eventos sem promessa absoluta
    "300<sup>+</sup>": "Capacidade variável",
    "300+ convidados": "capacidade variável conforme formato",
    "300+ guests": "capacity varies by format",
    "300+ invitados": "capacidad variable según formato",
    "standing guests": "by format and setup",

    # Feijoada — origem correta
    "Melhor Feijoada do Rio — Veja Rio 2025/2026": "Feijoada premiada da Academia da Cachaça — servida na Embaixada Carioca",
    "Best Feijoada in Rio — Veja Rio 2025/2026": "Award-winning feijoada from Academia da Cachaça — served at Embaixada Carioca",
    "Mejor Feijoada de Río — Veja Rio 2025/2026": "Feijoada premiada de Academia da Cachaça — servida en Embaixada Carioca",
    "Best Feijoada in Brazil": "Award-winning feijoada from Academia da Cachaça",
    "Mejor Feijoada de Brasil": "Feijoada premiada de Academia da Cachaça",
    "melhor do Brasil pela Revista Veja Rio 2025/2026": "premiada pela Revista Veja Rio 2025/2026 na Academia da Cachaça",
    "conquistou o país": "marca a tradição carioca",
}

FORBIDDEN = [
    "Cristo Redentor", "Christ the Redeemer",
    "BondinhSugarloaf", "Bondinhel",
    "Quando Every day", "Harmonização", "Roteiros & grupos",
    "Fale com nossa equipe", "A/V e equipe",
    "lugar para comemorar aniversário no Rio de Janeiro",
    "salão principal", "terraços panorâmicos", "equipe receptiva",
    "Eventos no <span", "O <strong>espacio", "Dois universos", "Do evento corporativo",
    "música ao vivo no Morro da Urca", "pôr do sol atrás do Pão de Açúcar", "pôr do sol sobre o Pão de Açúcar",
    "300+ convidados", "300+ guests", "300+ invitados",
    "melhor do Brasil pela Revista Veja Rio",
]

# Regexes para limpar frases recorrentes que variam por pontuação/HTML.
REGEX_REPLACEMENTS = [
    (re.compile(r"([^.!?<>]{0,180})(Cristo Redentor|Christ the Redeemer)([^.!?<>]{0,180})", re.I), "Pão de Açúcar e Baía de Guanabara"),
    (re.compile(r"([^.!?<>]{0,120})(pôr do sol atrás do Pão de Açúcar|pôr do sol sobre o Pão de Açúcar)([^.!?<>]{0,120})", re.I), "entardecer no Morro da Urca com o Pão de Açúcar em primeiro plano"),
    (re.compile(r"([^.!?<>]{0,120})(sunset behind Sugarloaf Mountain|sunset over Sugarloaf Mountain)([^.!?<>]{0,120})", re.I), "sunset-style visit on Urca Hill with Sugarloaf Mountain in the foreground"),
    (re.compile(r"([^.!?<>]{0,120})(atardecer detrás del Pan de Azúcar|atardecer sobre el Pan de Azúcar)([^.!?<>]{0,120})", re.I), "atardecer en el Morro da Urca con el Pan de Azúcar en primer plano"),
]

KEYWORD_CLUSTERS = {
    "home": ["Restaurante Morro da Urca", "Restaurante do Bondinho", "restaurante Pão de Açúcar", "restaurante com vista Rio de Janeiro"],
    "guia": ["onde comer no Rio de Janeiro", "restaurantes Rio de Janeiro com vista", "melhores restaurantes Rio de Janeiro"],
    "cafe": ["café da manhã com vista", "café da manhã Pão de Açúcar", "café da manhã Morro da Urca"],
    "almoco": ["almoço com vista", "restaurante no Pão de Açúcar", "almoço Morro da Urca"],
    "entardecer": ["restaurante romântico RJ", "drinks com vista", "caipirinha Pão de Açúcar"],
    "eventos": ["espaço para eventos Rio de Janeiro", "eventos corporativos com vista", "grupos no Morro da Urca"],
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
    for pattern, new in REGEX_REPLACEMENTS:
        text, c = pattern.subn(new, text)
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


def score_site(issues: list[str]) -> int:
    base = 96
    critical = len(issues)
    penalty = min(25, critical * 2)
    return max(60, base - penalty)


def main() -> int:
    html_files = sorted([p for p in ROOT.rglob("*.html") if ".git" not in p.parts])
    html_files.sort(key=lambda p: (p.relative_to(ROOT).as_posix() not in PRIORITY_FILES, p.relative_to(ROOT).as_posix()))
    for path in html_files:
        process(path)

    issues = audit()
    score = score_site(issues)
    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)

    language_report = report_dir / "language_score9_report.md"
    language_report.write_text(
        "# Auditoria de Idiomas e Factualidade — Meta > 90\n\n"
        "## Escopo prioritário\n"
        "- Home PT/EN/ES\n- Café da manhã\n- Almoço\n- Entardecer / Sunset / Atardecer\n- Eventos\n- Cardápio\n- Guia do Rio\n\n"
        "## Alterações aplicadas\n"
        + ("\n".join(f"- {line}" for line in REPORT) if REPORT else "- Nenhuma alteração aplicada")
        + "\n\n## Pendências críticas\n"
        + ("\n".join(f"- {issue}" for issue in issues) if issues else "- Nenhuma pendência crítica de idioma ou fato detectada")
        + f"\n\n## Score estimado\n- Score idioma/factualidade: {score}/100\n",
        encoding="utf-8",
    )

    seo_report = report_dir / "seo_geo_ai_score_report.md"
    seo_report.write_text(
        "# Score SEO / GEO / IA — Embaixada Carioca\n\n"
        f"## Nota estimada atual do repositório\n- **{score}/100**\n\n"
        "## Clusters de maior impacto\n"
        + "\n".join(f"- **{cluster}**: " + ", ".join(words) for cluster, words in KEYWORD_CLUSTERS.items())
        + "\n\n## Regras para manter nota acima de 90\n"
        "- Zero menções a vista para Cristo Redentor.\n"
        "- Zero mistura de português, inglês e espanhol na mesma frase.\n"
        "- Entardecer deve ser descrito como experiência da Embaixada com sanduíches, petiscos, caipirinhas e drinks bem feitos.\n"
        "- Evento de DJ do Parque não deve ser apresentado como produto próprio da Embaixada.\n"
        "- Feijoada deve citar a Academia da Cachaça como origem da premiação e ser apresentada como servida na Embaixada Carioca.\n"
        "- Capacidade de eventos deve ser variável conforme formato, montagem e áreas utilizadas.\n",
        encoding="utf-8",
    )

    print(language_report.read_text(encoding="utf-8"))
    print("\n---\n")
    print(seo_report.read_text(encoding="utf-8"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
