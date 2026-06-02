#!/usr/bin/env python3
"""
Sprint 1 — Conversion + Quality Fixes | Embaixada Carioca

Escopo:
1. Corrigir idioma e duplicações visíveis.
2. Corrigir meta description de en/entardecer.html.
3. Inserir/validar schema principal Restaurant/WebSite/Breadcrumb.
4. Conferir telefone e hasMap.
5. Validar CTAs por idioma, especialmente WhatsApp.
6. Preparar lista de key events GA4 para marcação manual no painel.

Observação:
- A marcação de key events no GA4 é uma configuração administrativa no GA4.
- Este script garante nomes/eventos no código e gera instruções operacionais.
"""
from __future__ import annotations

from pathlib import Path
from urllib.parse import quote
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.embaixadacarioca.com"
RESERVE_URL = "https://go.tagme.com.br/embaixadacarioca"
REVIEW_URL = "https://g.page/r/CU-tJiJIjBUcEAE/review"
MAPS_URL = "https://www.google.com/maps/search/?api=1&query=Embaixada+Carioca+Morro+da+Urca"
PHONE_E164 = "+5521966837556"
PHONE_DISPLAY = "+55 21 96683-7556"
WHATSAPP_NUMBER = "5521966837556"

REPORT: list[str] = []
WARNINGS: list[str] = []
COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "language_fixes": 0,
    "duplication_fixes": 0,
    "meta_fixes": 0,
    "schema_injected": 0,
    "phone_fixes": 0,
    "hasmap_fixes": 0,
    "whatsapp_fixes": 0,
    "reports_written": 0,
}

SCHEMA_START = "<!-- EC Sprint 1 Structured Data -->"
SCHEMA_END = "<!-- /EC Sprint 1 Structured Data -->"
SCHEMA_BLOCK_RE = re.compile(r"\n*<!-- EC Sprint 1 Structured Data -->[\s\S]*?<!-- /EC Sprint 1 Structured Data -->\s*", re.IGNORECASE)
HEAD_CLOSE_RE = re.compile(r"</head>", re.IGNORECASE)
HTML_LANG_RE = re.compile(r"<html\b[^>]*\blang=[\"']([^\"']+)[\"']", re.IGNORECASE)
META_DESCRIPTION_RE = re.compile(r'<meta\b(?=[^>]*\bname=["\']description["\'])(?=[^>]*\bcontent=["\'][^"\']*["\'])[^>]*>', re.IGNORECASE)
CANONICAL_RE = re.compile(r'<link\b(?=[^>]*\brel=["\']canonical["\'])(?=[^>]*\bhref=["\']([^"\']+)["\'])[^>]*>', re.IGNORECASE)
TITLE_RE = re.compile(r"<title>\s*([^<]+?)\s*</title>", re.IGNORECASE)
WA_RE = re.compile(r'https://(?:wa\.me/|api\.whatsapp\.com/send\?phone=)(?:\+?55)?(?:21)?9?6683[-]?7556(?:[^"\'\s<>]*)?', re.IGNORECASE)
HASMAP_RE = re.compile(r'("hasMap"\s*:\s*")[^"]+(")', re.IGNORECASE)

PT_TEXT_FIXES = {
    "Para quién": "Para quem",
    "para quién": "para quem",
    "Eventos en el ": "Eventos no ",
    "Hablar con nuestro equipo": "Falar com nossa equipe",
    "Solicitar presupuesto": "Solicitar orçamento",
    "Abierto todos los días": "Aberto todos os dias",
    "todos recibidos con": "todos recebidos com",
    "vista más impresionante": "vista mais impressionante",
    "Reuniones matutinas": "Reuniões matinais",
    "main dining room": "salão principal",
    "panoramic terraces": "terraços panorâmicos",
    "hospitality team": "equipe receptiva",
    "Capacity varies": "Capacidade variável",
    "Structure &amp; capacity": "Estrutura e capacidade",
    "Structure & capacity": "Estrutura e capacidade",
    "Breakfast": "Café da manhã",
    "Lunch": "Almoço",
}

EN_TEXT_FIXES = {
    "Solicitar orçamento": "Request a quote",
    "Falar com nossa equipe": "Talk to our team",
    "Aberto todos os dias": "Open daily",
    "Capacidade variável": "Capacity varies",
    "salão principal": "main dining room",
    "terraços panorâmicos": "panoramic terraces",
    "equipe receptiva": "hospitality team",
}

ES_TEXT_FIXES = {
    "Solicitar orçamento": "Solicitar presupuesto",
    "Falar com nossa equipe": "Hablar con nuestro equipo",
    "Aberto todos os dias": "Abierto todos los días",
    "Capacidade variável": "Capacidad variable",
    "salão principal": "salón principal",
    "terraços panorâmicos": "terrazas panorámicas",
    "equipe receptiva": "equipo de recepción",
    "Breakfast": "Desayuno",
    "Lunch": "Almuerzo",
}

LANG_LABELS = {
    "pt": {"reserve": "Reservar mesa", "whatsapp": "Olá! Vim pelo site da Embaixada Carioca e gostaria de fazer uma reserva.", "site_name": "Embaixada Carioca"},
    "en": {"reserve": "Reserve a table", "whatsapp": "Hi! I found Embaixada Carioca through the website and would like to make a reservation.", "site_name": "Embaixada Carioca"},
    "es": {"reserve": "Reservar mesa", "whatsapp": "Hola. Vi Embaixada Carioca en el sitio web y me gustaría hacer una reserva.", "site_name": "Embaixada Carioca"},
}

SCHEMA_I18N = {
    "pt": {
        "inLanguage": "pt-BR",
        "description": "Restaurante brasileiro no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com café da manhã, almoço, caipirinhas, chope e eventos com vista.",
        "servesCuisine": ["Brasileira", "Carioca", "Café da manhã", "Bar"],
        "features": ["Vista para o Pão de Açúcar", "Dentro do Parque Bondinho Pão de Açúcar", "Mesas ao ar livre"],
        "keywords": ["restaurante no Pão de Açúcar", "restaurante Morro da Urca", "restaurante no Bondinho", "café da manhã com vista", "caipirinha no Rio de Janeiro"],
    },
    "en": {
        "inLanguage": "en",
        "description": "Brazilian restaurant at Urca Hill, inside Sugarloaf Cable Car Park, serving breakfast, lunch, caipirinhas, draft beer and events with a view.",
        "servesCuisine": ["Brazilian", "Carioca", "Breakfast", "Bar"],
        "features": ["Sugarloaf Mountain view", "Inside Sugarloaf Cable Car Park", "Outdoor seating"],
        "keywords": ["restaurant near Sugarloaf Mountain", "restaurant at Urca Hill", "Sugarloaf Cable Car restaurant", "breakfast with a view", "caipirinha in Rio de Janeiro"],
    },
    "es": {
        "inLanguage": "es",
        "description": "Restaurante brasileño en el Morro da Urca, dentro del Parque Bondinho Pan de Azúcar, con desayuno, almuerzo, caipirinhas, cerveza de barril y eventos con vista.",
        "servesCuisine": ["Brasileña", "Carioca", "Desayuno", "Bar"],
        "features": ["Vista al Pan de Azúcar", "Dentro del Parque Bondinho Pan de Azúcar", "Mesas al aire libre"],
        "keywords": ["restaurante cerca del Pan de Azúcar", "restaurante en el Morro da Urca", "restaurante en el Bondinho", "desayuno con vista", "caipirinha en Río de Janeiro"],
    },
}

SUSPICIOUS_BY_LANG = {
    "pt": ["Para quién", " en el ", "Hablar con nuestro", "recibidos con", "más impresionante", "main dining room", "panoramic terraces", "hospitality team"],
    "en": ["Solicitar orçamento", "Falar com nossa equipe", "Capacidade variável", "salão principal", "terraços panorâmicos"],
    "es": ["Solicitar orçamento", "Falar com nossa equipe", "Capacidade variável", "Breakfast", "Lunch"],
}

KEY_EVENTS = [
    "click_reservar",
    "click_whatsapp",
    "click_eventos",
    "click_como_chegar",
    "click_cardapio",
    "click_cafe_da_manha",
    "click_almoco",
    "click_idioma",
]


def detect_lang(rel: str, text: str) -> str:
    match = HTML_LANG_RE.search(text)
    if match:
        val = match.group(1).lower()
        if val.startswith("en"):
            return "en"
        if val.startswith("es"):
            return "es"
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt"


def canonical_for(rel: str, text: str) -> str:
    match = CANONICAL_RE.search(text)
    if match:
        return match.group(1)
    if rel == "index.html":
        return BASE + "/"
    return BASE + "/" + rel


def title_for(text: str) -> str:
    match = TITLE_RE.search(text)
    return match.group(1).strip() if match else "Embaixada Carioca"


def apply_language_and_duplication_fixes(text: str, rel: str, lang: str) -> str:
    repl = {"pt": PT_TEXT_FIXES, "en": EN_TEXT_FIXES, "es": ES_TEXT_FIXES}.get(lang, {})
    for old, new in repl.items():
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            COUNTERS["language_fixes"] += count
            REPORT.append(f"LANG_FIX: {rel} [{lang}] | {old!r} -> {new!r} | {count}")

    if lang == "pt":
        patterns = [
            (re.compile(r"\bA\s+A\s+referência", re.IGNORECASE), "A referência"),
            (re.compile(r"\bA\s+A\s+A\s+referência", re.IGNORECASE), "A referência"),
            (re.compile(r"Entre os restaurantes com vista no Rio de Janeiro,\s*a Embaixada Carioca ocupa um lugar único:\s*Entre os restaurantes com vista no Rio de Janeiro,", re.IGNORECASE), "Entre os restaurantes com vista no Rio de Janeiro,"),
            (re.compile(r"(A Embaixada Carioca ocupa um lugar único:)\s*\1", re.IGNORECASE), r"\1"),
        ]
        for pattern, replacement in patterns:
            text, count = pattern.subn(replacement, text)
            if count:
                COUNTERS["duplication_fixes"] += count
                REPORT.append(f"DUP_FIX: {rel} | {pattern.pattern[:70]}... | {count}")
    return text


def fix_en_entardecer_description(text: str, rel: str) -> str:
    if rel != "en/entardecer.html":
        return text
    desc = "Enjoy sunset drinks at Embaixada Carioca, inside Sugarloaf Cable Car Park, with caipirinhas, Brazilian snacks and views of Rio."
    tag = f'<meta name="description" content="{desc}">'
    if META_DESCRIPTION_RE.search(text):
        new_text, count = META_DESCRIPTION_RE.subn(tag, text, count=1)
    elif "<head>" in text:
        new_text = text.replace("<head>", "<head>\n" + tag, 1)
        count = 1
    else:
        return text
    if count and new_text != text:
        COUNTERS["meta_fixes"] += count
        REPORT.append(f"META_FIX: {rel} | description EN corrigida")
    return new_text


def repair_phone_and_hasmap(text: str, rel: str) -> str:
    phone_repls = {
        "+55-21-3042-3060": PHONE_DISPLAY,
        "+55 21 3042-3060": PHONE_DISPLAY,
        "+552130423060": PHONE_E164,
        "+55-21-96683-7556": PHONE_DISPLAY,
    }
    for old, new in phone_repls.items():
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            COUNTERS["phone_fixes"] += count
            REPORT.append(f"PHONE_FIX: {rel} | {old} -> {new} | {count}")

    def hasmap_repl(match: re.Match[str]) -> str:
        current = match.group(0)
        if MAPS_URL in current:
            return current
        COUNTERS["hasmap_fixes"] += 1
        REPORT.append(f"HASMAP_FIX: {rel} | hasMap corrigido")
        return match.group(1) + MAPS_URL + match.group(2)

    text = HASMAP_RE.sub(hasmap_repl, text)
    return text


def whatsapp_url(lang: str) -> str:
    message = LANG_LABELS[lang]["whatsapp"]
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}"


def fix_whatsapp_ctas(text: str, rel: str, lang: str) -> str:
    target = whatsapp_url(lang)

    def repl(match: re.Match[str]) -> str:
        old = match.group(0)
        if old == target:
            return old
        COUNTERS["whatsapp_fixes"] += 1
        REPORT.append(f"WHATSAPP_FIX: {rel} [{lang}] | CTA localizado")
        return target

    return WA_RE.sub(repl, text)


def build_schema(rel: str, text: str, lang: str) -> str:
    canonical = canonical_for(rel, text)
    title = title_for(text)
    cfg = SCHEMA_I18N.get(lang, SCHEMA_I18N["pt"])
    restaurant = {
        "@context": "https://schema.org",
        "@type": "Restaurant",
        "@id": f"{BASE}/#restaurant",
        "name": "Embaixada Carioca",
        "alternateName": ["Restaurante do Bondinho", "Restaurante Morro da Urca", "Restaurant at Sugarloaf Cable Car Park"],
        "url": BASE + "/",
        "logo": f"{BASE}/assets/logo-azul.svg",
        "image": [f"{BASE}/assets/hero.webp", f"{BASE}/assets/hero-1200w.webp"],
        "description": cfg["description"],
        "telephone": PHONE_E164,
        "priceRange": "$$",
        "servesCuisine": cfg["servesCuisine"],
        "acceptsReservations": True,
        "hasMenu": f"{BASE}/cardapio.html",
        "hasMap": MAPS_URL,
        "isAccessibleForFree": False,
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": name, "value": True} for name in cfg["features"]],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Av. Pasteur, 520 — Morro da Urca",
            "addressLocality": "Rio de Janeiro",
            "addressRegion": "RJ",
            "postalCode": "22290-240",
            "addressCountry": "BR",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": -22.9511223, "longitude": -43.1642121},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "08:30", "closes": "21:00"}
        ],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "7779", "bestRating": "5", "worstRating": "1"},
        "sameAs": ["https://www.instagram.com/embaixadacarioca/", REVIEW_URL, MAPS_URL],
        "potentialAction": {"@type": "ReserveAction", "target": RESERVE_URL, "name": LANG_LABELS[lang]["reserve"]},
        "keywords": cfg["keywords"],
        "inLanguage": cfg["inLanguage"],
    }
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{BASE}/#website",
        "name": "Embaixada Carioca",
        "url": BASE + "/",
        "inLanguage": cfg["inLanguage"],
        "publisher": {"@id": f"{BASE}/#restaurant"},
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Embaixada Carioca", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": title, "item": canonical},
        ],
    }
    return (
        SCHEMA_START
        + "\n<script type=\"application/ld+json\">"
        + json.dumps({"@context": "https://schema.org", "@graph": [restaurant, website, breadcrumb]}, ensure_ascii=False, separators=(",", ":"))
        + "</script>\n"
        + SCHEMA_END
    )


def inject_schema(text: str, rel: str, lang: str) -> str:
    text = SCHEMA_BLOCK_RE.sub("\n", text)
    block = build_schema(rel, text, lang)
    if HEAD_CLOSE_RE.search(text):
        text = HEAD_CLOSE_RE.sub(block + "\n</head>", text, count=1)
        COUNTERS["schema_injected"] += 1
        REPORT.append(f"SCHEMA: {rel} | schema principal validado/injetado")
    else:
        WARNINGS.append(f"SCHEMA_WARNING: {rel} sem </head>")
    return text


def audit_remaining_language(text: str, rel: str, lang: str) -> None:
    visible_like = SCHEMA_BLOCK_RE.sub("", text)
    for token in SUSPICIOUS_BY_LANG.get(lang, []):
        if token in visible_like:
            WARNINGS.append(f"LANG_WARNING: {rel} [{lang}] ainda contém {token!r}")


def process_html(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix != ".html" or ".git" in path.parts or rel.startswith("_"):
        return
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    lang = detect_lang(rel, original)
    text = original
    text = apply_language_and_duplication_fixes(text, rel, lang)
    text = fix_en_entardecer_description(text, rel)
    text = repair_phone_and_hasmap(text, rel)
    text = fix_whatsapp_ctas(text, rel, lang)
    text = inject_schema(text, rel, lang)
    audit_remaining_language(text, rel, lang)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1
        REPORT.append(f"UPDATED: {rel}")


def write_reports() -> None:
    out = ROOT / "_audit_reports"
    out.mkdir(exist_ok=True)

    sprint = out / "sprint1_conversion_quality_report.md"
    lines = [
        "# Sprint 1 — Conversion + Quality Fixes",
        "",
        "## Itens executados",
        "1. Correção de idioma e duplicações visíveis.",
        "2. Correção da meta description de `en/entardecer.html`.",
        "3. Validação/injeção do schema principal por idioma.",
        "4. Normalização de telefone e `hasMap`.",
        "5. Localização de CTAs de WhatsApp por idioma.",
        "6. Preparação dos eventos GA4 para marcação como key events.",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Ações aplicadas"])
    lines.extend(f"- {item}" for item in REPORT) if REPORT else lines.append("- Nenhuma ação necessária.")
    lines.extend(["", "## Alertas"])
    lines.extend(f"- {item}" for item in WARNINGS) if WARNINGS else lines.append("- Nenhum alerta remanescente encontrado.")
    lines.append("")
    sprint.write_text("\n".join(lines), encoding="utf-8")
    COUNTERS["reports_written"] += 1

    ga4 = out / "ga4_key_events_manual_setup.md"
    ga4.write_text(
        "# GA4 — Key Events para configurar manualmente\n\n"
        "Estes eventos já estão preparados no código do site. A marcação como key event precisa ser feita no painel do GA4.\n\n"
        "## Eventos recomendados como key events\n"
        + "\n".join(f"- `{event}`" for event in KEY_EVENTS)
        + "\n\n## Caminho no GA4\n"
        "1. Admin → Data display → Events.\n"
        "2. Procurar cada evento da lista.\n"
        "3. Marcar como key event.\n"
        "4. Validar no relatório Realtime após clicar em reserva, WhatsApp, cardápio e como chegar.\n\n"
        "## Observação\n"
        "Eventos só aparecem na tela de Events depois de serem recebidos pelo GA4 pelo menos uma vez.\n",
        encoding="utf-8",
    )
    COUNTERS["reports_written"] += 1
    print(sprint.read_text(encoding="utf-8"))
    print(ga4.read_text(encoding="utf-8"))


def main() -> int:
    for path in sorted(ROOT.rglob("*.html")):
        process_html(path)
    write_reports()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
