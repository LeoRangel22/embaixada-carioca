#!/usr/bin/env python3
"""
Correções AAA / 6 estrelas para o site estático da Embaixada Carioca.

Objetivo: aplicar correções editoriais, técnicas e multilíngues nos HTMLs sem alterar layout/CSS.
A saída gera um relatório em _audit_reports/aaa_6_estrelas_fixes_report.md.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.embaixadacarioca.com"
REVIEW_COUNT = "7779"

REPORT: list[str] = []

SLUGS = {
    "index": {"pt": "", "en": "en/", "es": "es/"},
    "cafe-da-manha": {"pt": "cafe-da-manha", "en": "en/cafe-da-manha", "es": "es/cafe-da-manha"},
    "almoco": {"pt": "almoco", "en": "en/almoco", "es": "es/almoco"},
    "entardecer": {"pt": "entardecer", "en": "en/sunset", "es": "es/atardecer"},
    "sunset": {"pt": "entardecer", "en": "en/sunset", "es": "es/atardecer"},
    "atardecer": {"pt": "entardecer", "en": "en/sunset", "es": "es/atardecer"},
    "eventos": {"pt": "eventos", "en": "en/eventos", "es": "es/eventos"},
    "cardapio": {"pt": "cardapio", "en": "en/cardapio", "es": "es/cardapio"},
    "guia-do-rio": {"pt": "guia-do-rio", "en": "en/guia-do-rio", "es": "es/guia-do-rio"},
    "contato": {"pt": "contato", "en": "en/contato", "es": "es/contato"},
    "nossa-visao": {"pt": "nossa-visao", "en": "en/nossa-visao", "es": "es/nossa-visao"},
}

GLOBAL_REPLACEMENTS = {
    "Parque BondinhSugarloaf Mountain": "Bondinho Pão de Açúcar Park",
    "BondinhSugarloaf Mountain": "Bondinho Pão de Açúcar",
    "Parque Bondinhel Pan de Azúcar": "Parque Bondinho Pão de Açúcar",
    "Parque Bondinhel Pan de Azúcar®": "Parque Bondinho Pão de Açúcar®",
    "Bondinhel Pan de Azúcar": "Parque Bondinho Pão de Açúcar",
    "vista para o o Bondinho": "vista para o Pão de Açúcar",
    "vista direta para o Bondinho": "vista direta para o Pão de Açúcar",
    "vista frontal para o Bondinho": "vista frontal para o Pão de Açúcar",
    "vista para o Bondinho": "vista para o Pão de Açúcar",
    "Vista direta para o Bondinho": "Vista direta para o Pão de Açúcar",
    "Vista panorâmica para o Bondinho": "Vista panorâmica para o Pão de Açúcar",
    "Morro da Urca e Morro da Urca": "Morro da Urca e no Parque Bondinho Pão de Açúcar",
    "Morro da Urca, dentro do Parque Bondinho, no Morro da Urca": "Morro da Urca, dentro do Parque Bondinho Pão de Açúcar",
    "Pão de Açúcar para o Pão de Açúcar": "Pão de Açúcar",
    "para o o Pão de Açúcar": "para o Pão de Açúcar",
    "referência em do Rio": "referência no Rio",
    "Embaixada Carioca restaurante": "Embaixada Carioca",
    "restaurante café da manhã": "café da manhã",
    "Embaixada Carioca aberto": "Embaixada Carioca abre",
    "Capacidade para 300+ convidados": "Capacidade variável conforme formato, montagem e áreas utilizadas",
    "capacidade para 300+ convidados": "capacidade variável conforme formato, montagem e áreas utilizadas",
    "300+ convidados": "capacidade conforme formato",
    "300+ guests": "capacity varies by format",
    "300+ invitados": "capacidad según montaje",
    "até 300 pax": "capacidade conforme montagem",
    "up to 300 pax": "capacity varies by format",
    "hasta 300 pax": "capacidad según montaje",
    "Capacity for capacity varies by format and setup": "Capacity varies by format and setup",
    "capacity for capacity varies by format and setup": "capacity varies by format and setup",
}

EN_REPLACEMENTS = {
    "Inauguração": "Opening",
    "Altura": "Altitude",
    "227 metros · sobre a Baía": "227 meters · above the bay",
    "sobre a Baía": "above the bay",
    "★ best feijoada ★ PRÊMIO": "★ award-winning feijoada ★",
    "PRÊMIO": "award",
    "Quando Every day": "Served every day",
    "Harmonização Selected cachaças and wines": "Pairing: selected cachaças and wines",
    "Harmonização": "Pairing:",
    "Eventos corporativos.": "Corporate events",
    "Roteiros & grupos.": "Travel groups & curated itineraries",
    "Roteiros & grupos": "Travel groups & curated itineraries",
    "Restaurante Urca Hill": "Embaixada Carioca",
    "The most unique romantic experience": "One of the most memorable romantic experiences",
    "most unique": "most memorable",
    "11h30 – 17h": "11:30 AM – 5:00 PM",
    "11h30–17h": "11:30 AM–5:00 PM",
    "17h – 21h": "5:00 PM – 9:00 PM",
    "8h30": "8:30 AM",
    "12 PM – 5 PM": "11:30 AM – 5:00 PM",
    "12–5 PM": "11:30 AM–5:00 PM",
    "12pm to 5pm": "11:30 AM to 5:00 PM",
    "Mon–Fri 12–4pm, Sat–Sun 12–5pm": "every day from 11:30 AM to 5:00 PM",
    "Parque Sugarloaf Mountain": "Bondinho Pão de Açúcar Park",
    "Sugarloaf Mountain Cable Car Park": "Bondinho Pão de Açúcar Park",
    "Sugarloaf cable car park": "Bondinho Pão de Açúcar Park",
    "restaurant inside Sugarloaf cable car park": "restaurant inside Bondinho Pão de Açúcar Park",
    "free to access for dining": "accessible depending on how you arrive",
    "No cable car ticket is required to access the restaurant.": "If you take the cable car, a regular Bondinho Pão de Açúcar Park ticket is required. If you hike up via the Praia Vermelha trail, when open, no cable car ticket is needed.",
    "No cable car ticket is required": "A cable car ticket is not required only if you hike up via the Praia Vermelha trail, when open",
    "by car or Uber to Av. Pasteur, 520": "by car or Uber to the Bondinho Pão de Açúcar Park entrance at Av. Pasteur, 520; from there, access to Urca Hill is by cable car or by the Praia Vermelha trail, when open",
    "Gastronomia italiana e brasileira no coração do Museu de Arte Moderna do Rio de Janeiro, com vista para a Baía de Guanabara e Sugarloaf Mountain.": "Italian and Brazilian cuisine in the heart of Rio de Janeiro’s Museum of Modern Art, with views of Guanabara Bay and Sugarloaf Mountain.",
    "A vista mais bonita do Rio de Janeiro": "One of Rio’s most beautiful views",
    "Drinks com vista para a Baía de Guanabara": "Drinks with a view of Guanabara Bay",
    "Gastronomia brasileira com Sugarloaf Mountain ao fundo": "Brazilian cuisine with Sugarloaf Mountain in the background",
    "Pôr do sol atrás of Sugarloaf Mountain visto da Embaixada Carioca, Urca Hill": "Sunset behind Sugarloaf Mountain seen from Embaixada Carioca, Urca Hill",
    "Breakfast na Embaixada Carioca": "Breakfast at Embaixada Carioca",
    "Menu da Embaixada Carioca": "Embaixada Carioca menu",
    "Restaurant no Urca Hill": "restaurant on Urca Hill",
    "lunch com vista": "lunch with a view",
    "restaurante brasileiro": "Brazilian restaurant",
    "best feijoada do Brasil": "best feijoada in Brazil",
    "roteiro Rio de Janeiro": "Rio de Janeiro itinerary",
    "o que fazer no Rio de Janeiro": "what to do in Rio de Janeiro",
    "onde comer no Rio de Janeiro": "where to eat in Rio de Janeiro",
    "melhores praias Rio de Janeiro": "best beaches Rio de Janeiro",
    "restaurantes com vista Rio de Janeiro": "restaurants with a view Rio de Janeiro",
    "Roteiro Rio de Janeiro: O Guia Definitivo do que Fazer, Onde Ir e Onde Comer": "Rio de Janeiro Guide: What to Do, Where to Go and Where to Eat",
    "Guia completo de onde comer in Rio de Janeiro com vista. Os melhores restaurantes with a view of Sugarloaf Mountain, Cristo Redentor e Baía de Guanabara.": "Complete guide to where to eat in Rio de Janeiro with a view, including restaurants overlooking Sugarloaf Mountain, Christ the Redeemer and Guanabara Bay.",
    "Panoramic view of Sugarloaf Mountain from Morro da Urca from Urca Hill": "Panoramic view of Sugarloaf Mountain from Urca Hill",
}

ES_REPLACEMENTS = {
    "Inauguração": "Inauguración",
    "Altura": "Altitud",
    "227 metros · sobre a Baía": "227 metros · sobre la bahía",
    "sobre a Baía": "sobre la bahía",
    "★ melhor feijoada ★ PRÊMIO": "★ mejor feijoada ★ premio",
    "melhor feijoada": "mejor feijoada",
    "PRÊMIO": "premio",
    "Quando Todos los días": "Servida todos los días",
    "Harmonização Cachaças y vinos seleccionados": "Maridaje: cachaças y vinos seleccionados",
    "Harmonização": "Maridaje:",
    "Roteiros & grupos.": "Itinerarios y grupos",
    "Roteiros & grupos": "Itinerarios y grupos",
    "Venha nos visitar.": "Planifique su visita.",
    "Endereço & Acesso": "Dirección y acceso",
    "Acceso vía teleférico (teleférico) ou a pé pela Praia Vermelha": "Acceso en teleférico, con entrada regular del Parque Bondinho Pão de Açúcar, o a pie por el sendero de Praia Vermelha, cuando esté abierto",
    "ou a pé pela Praia Vermelha": "o a pie por el sendero de Praia Vermelha",
    "8h30": "8:30",
    "11h30": "11:30",
    "17h": "17:00",
    "21h": "21:00",
    "12h–17:00": "11:30–17:00",
    "12h a 17:00": "11:30 a 17:00",
    "el Pão de Açúcar": "el Pan de Azúcar",
    "al Pão de Açúcar": "al Pan de Azúcar",
    "del Pão de Açúcar": "del Pan de Azúcar",
    "Vista panorámica del Pão de Açúcar": "Vista panorámica al Pan de Azúcar",
    "Pan de Açúcar": "Pan de Azúcar",
    "Parque del Teleférico Pan de Azúcar": "Parque Bondinho Pão de Açúcar",
    "2ª mejor cerveza Heineken de Brasil": "2º mejor chopp Heineken de Brasil",
    "2ª mejor cerveza de Brasil": "2º mejor chopp Heineken de Brasil",
    "Mejor cerveza Heineken de barril de Río": "Mejor chopp Heineken de Río de Janeiro",
    "la experiencia romántica más única": "una de las experiencias románticas más especiales",
    "La experiencia romántica más única": "Una de las experiencias románticas más especiales",
    "desayuno com vista": "desayuno con vista",
    "melhor desayuno": "mejor desayuno",
    "brunch com vista": "brunch con vista",
    "almuerzo com vista": "almuerzo con vista",
    "eventos com vista": "eventos con vista",
    "restaurante brasileiro": "restaurante brasileño",
    "aluguel espaço festas": "alquiler de espacio para fiestas",
    "Gastronomia italiana e brasileira": "Gastronomía italiana y brasileña",
    "Gastronomia brasileira": "Gastronomía brasileña",
    "Gastronomia": "Gastronomía",
    "com vista": "con vista",
    "na Embaixada Carioca": "en Embaixada Carioca",
    "Espaço para eventos": "Espacio para eventos",
    "aniversários": "aniversarios",
    "lançamentos": "lanzamientos",
    "roteiros": "itinerarios",
    "Recebemos grupos de agências": "Recibimos grupos de agencias",
    "Sim.": "Sí.",
    "Oferecemos": "Ofrecemos",
    "acesso preferencial": "acceso preferencial",
    "Best restaurant in Rio de Janeiro with an incredible view of Sugarloaf Mountain. The caipirinhas and sunset experience are magic.": "El mejor restaurante de Río de Janeiro, con una vista increíble al Pan de Azúcar. Las caipirinhas y la experiencia del atardecer son mágicas.",
    "Chef Walace — a alma da Embaixada Carioca": "Chef Walace — el alma de Embaixada Carioca",
    "Menú da Embaixada Carioca": "Menú de Embaixada Carioca",
    "Rio de Janeiro": "Río de Janeiro",
    "roteiro Rio de Janeiro": "itinerario Río de Janeiro",
    "o que fazer no Rio de Janeiro": "qué hacer en Río de Janeiro",
    "dónde comer no Rio de Janeiro": "dónde comer en Río de Janeiro",
    "melhores praias Rio de Janeiro": "mejores playas Río de Janeiro",
    "restaurantes com vista Rio de Janeiro": "restaurantes con vista Río de Janeiro",
    "Roteiro Rio de Janeiro: O Guia Definitivo do que Fazer, Dónde Ir e Dónde Comer": "Guía de Río de Janeiro: qué hacer, dónde ir y dónde comer",
    "Guia completo de dónde comer en Río de Janeiro com vista. Os melhores restaurantes com vista al Pan de Azúcar, Cristo Redentor e Bahía de Guanabara.": "Guía completa sobre dónde comer en Río de Janeiro con vista, incluyendo restaurantes con vista al Pan de Azúcar, el Cristo Redentor y la Bahía de Guanabara.",
    "Pôr do sol atrás del Pan de Azúcar visto da Embaixada Carioca, Morro da Urca": "Puesta de sol detrás del Pan de Azúcar vista desde Embaixada Carioca, Morro da Urca",
    "No es necesario comprar entrada del bondinho": "Si sube en teleférico, debe comprar la entrada regular del Parque Bondinho Pão de Açúcar. Si sube por el sendero de Praia Vermelha, cuando esté abierto, no necesita entrada del teleférico",
    "2º mejor chopp Heineken de Brasil y el mejor de Río de Janeiro y la mejor de Río de Janeiro": "2º mejor chopp Heineken de Brasil y el mejor de Río de Janeiro",
}

META_REPLACEMENTS = {
    "The most beautiful breakfast in Rio de Janeiro. Full buffet and à la carte with a stunning view of Sugarloaf Mountain on Urca Hill. Every day from 8am to 11am.": "Breakfast with a view of Sugarloaf Mountain on Urca Hill, served daily from 8:30 AM to 11:30 AM at Embaixada Carioca.",
    "El desayuno más bonito de Río de Janeiro. Buffet completo y à la carte con vistas al Pan de Azúcar en el Morro da Urca. Todos los días de 8h a 11h.": "Desayuno con vista al Pan de Azúcar en el Morro da Urca, servido todos los días de 8:30 a 11:30 en Embaixada Carioca.",
    "Award-winning Brazilian cuisine at 227m altitude inside Bondinho Pão de Açúcar Park. Lunch with panoramic views Mon–Fri 12–4pm, Sat–Sun 12–5pm. Book online.": "Award-winning Brazilian cuisine at 227 meters, inside Bondinho Pão de Açúcar Park. Lunch with a view of Sugarloaf Mountain every day from 11:30 AM to 5:00 PM.",
    "Corporate events, private parties and gastronomic experiences with 360° views in Rio de Janeiro. Capacity for capacity varies by format and setup on Urca Hill. Request a quote.": "Corporate events, private parties and gastronomic experiences with panoramic views in Rio de Janeiro. Capacity varies by format, setup and areas used on Urca Hill.",
}

PROHIBITED = ["BondinhSugarloaf", "Bondinhel", "vista para o o Bondinho", "Pão de Açúcar para o Pão de Açúcar", "Capacity for capacity", "Urca Hill (Urca Hill)"]


def lang_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt"


def canonical_for(path: Path) -> str:
    lang = lang_for(path)
    key = path.stem.lower()
    if key in SLUGS:
        slug = SLUGS[key][lang]
    else:
        slug = path.relative_to(ROOT).with_suffix("").as_posix()
    return f"{BASE_URL}/{slug}" if slug else f"{BASE_URL}/"


def replace_all(text: str, mapping: dict[str, str]) -> tuple[str, int]:
    total = 0
    for old, new in mapping.items():
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            total += count
    return text, total


def normalize_canonical(text: str, path: Path) -> str:
    url = canonical_for(path)
    text = re.sub(r"\n?<link\s+[^>]*rel=[\"']canonical[\"'][^>]*>\s*", "\n", text, flags=re.I)
    text = re.sub(r"(<head>\s*)", f"\\1\n<link rel=\"canonical\" href=\"{url}\">\n", text, count=1, flags=re.I)
    text = re.sub(r"<meta\s+content=\"[^\"]*\"\s+property=\"og:url\"\s*/?>", f"<meta content=\"{url}\" property=\"og:url\"/>", text, flags=re.I)
    text = re.sub(r"\"mainEntityOfPage\"\s*:\s*\"https://www\.embaixadacarioca\.com/[^\"]*\"", f"\"mainEntityOfPage\": \"{url}\"", text)
    return text


def normalize_hreflang(text: str, path: Path) -> str:
    key = path.stem.lower()
    if key not in SLUGS:
        return text
    def u(lang: str) -> str:
        slug = SLUGS[key][lang]
        return f"{BASE_URL}/{slug}" if slug else f"{BASE_URL}/"
    block = "\n".join([
        f'<link href="{u("pt")}" hreflang="pt-BR" rel="alternate"/>',
        f'<link href="{u("en")}" hreflang="en" rel="alternate"/>',
        f'<link href="{u("es")}" hreflang="es" rel="alternate"/>',
        f'<link href="{u("pt")}" hreflang="x-default" rel="alternate"/>',
    ])
    text = re.sub(r"(?:\n?<link\s+href=\"https://www\.embaixadacarioca\.com[^\"]*\"\s+hreflang=\"(?:pt-BR|en|es|x-default)\"\s+rel=\"alternate\"/?\s*>\s*)+", "\n" + block + "\n", text)
    return text


def normalize_schema(text: str, lang: str) -> str:
    text = text.replace('"reviewCount":"7752"', f'"reviewCount":"{REVIEW_COUNT}"')
    text = text.replace('"reviewCount": "7752"', f'"reviewCount": "{REVIEW_COUNT}"')
    text = text.replace('"opens": "12:00"', '"opens": "11:30"')
    text = text.replace('"opens":"12:00"', '"opens":"11:30"')
    text = re.sub(r"\n\s*\"maximumAttendeeCapacity\"\s*:\s*300,?", "", text)
    if lang == "en":
        text = re.sub(r'"inLanguage"\s*:\s*"pt-BR"', '"inLanguage": "en"', text)
    elif lang == "es":
        text = re.sub(r'"inLanguage"\s*:\s*"pt-BR"', '"inLanguage": "es"', text)
    return text


def copy_sunset_aliases() -> None:
    pairs = [
        (ROOT / "en" / "entardecer.html", ROOT / "en" / "sunset.html"),
        (ROOT / "es" / "entardecer.html", ROOT / "es" / "atardecer.html"),
    ]
    for src, dst in pairs:
        if src.exists() and not dst.exists():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            REPORT.append(f"CREATED_ALIAS: {dst.relative_to(ROOT)}")


def process(path: Path) -> None:
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    lang = lang_for(path)
    rel = path.relative_to(ROOT).as_posix()

    text, c1 = replace_all(text, GLOBAL_REPLACEMENTS)
    text, c2 = replace_all(text, META_REPLACEMENTS)
    if lang == "en":
        text, c3 = replace_all(text, EN_REPLACEMENTS)
    elif lang == "es":
        text, c3 = replace_all(text, ES_REPLACEMENTS)
    else:
        c3 = 0

    text = normalize_schema(text, lang)
    text = normalize_canonical(text, path)
    text = normalize_hreflang(text, path)

    # Access rules, high-risk commercial wording.
    text = text.replace("Acesso via bondinho (teleférico) ou a pé pela Praia Vermelha", "Acesso pelo bondinho, com ingresso regular do Parque Bondinho Pão de Açúcar, ou pela trilha da Praia Vermelha, quando aberta, sem necessidade de ingresso do bondinho")
    text = text.replace("Access via cable car (Bondinho) or on foot via Praia Vermelha trail", "Access by cable car, with a regular Bondinho Pão de Açúcar Park ticket, or by the Praia Vermelha trail, when open, without a cable car ticket")
    text = text.replace("El restaurante del Morro da Urca — Embaixada Carioca — el acceso depende de cómo llegue", "El acceso depende de cómo llegue. Si sube en teleférico, debe comprar la entrada regular del Parque Bondinho Pão de Açúcar. Si sube por el sendero de Praia Vermelha, cuando esté abierto, no necesita entrada del teleférico. La reserva en el restaurante garantiza la mesa, pero no incluye la entrada al Parque")

    if text != original:
        path.write_text(text, encoding="utf-8")
        REPORT.append(f"UPDATED: {rel} | replacements={c1+c2+c3}")


def audit() -> list[str]:
    issues: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        for term in PROHIBITED:
            if term in text:
                issues.append(f"{rel}: residual crítico: {term}")
        canonical_count = len(re.findall(r"rel=[\"']canonical[\"']", text, flags=re.I))
        if canonical_count > 1:
            issues.append(f"{rel}: canonical duplicado ({canonical_count})")
        if '"opens": "12:00"' in text or "12 PM – 5 PM" in text:
            issues.append(f"{rel}: horário antigo de almoço")
    return issues


def main() -> int:
    copy_sunset_aliases()
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" not in path.parts:
            process(path)
    issues = audit()
    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / "aaa_6_estrelas_fixes_report.md"
    report_path.write_text(
        "# Relatório de Correções AAA / 6 Estrelas\n\n"
        "## Alterações\n"
        + ("\n".join(f"- {line}" for line in REPORT) if REPORT else "- Nenhuma alteração aplicada")
        + "\n\n## Pendências automatizadas\n"
        + ("\n".join(f"- {issue}" for issue in issues) if issues else "- Nenhuma pendência crítica detectada")
        + "\n",
        encoding="utf-8",
    )
    print(report_path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
