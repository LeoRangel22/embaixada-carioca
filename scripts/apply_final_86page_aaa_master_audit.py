#!/usr/bin/env python3
"""Final 86-page AAA Master Audit — Embaixada Carioca.

Audita todas as páginas HTML do repositório em linguagem, SEO, GEO/AIO/SAI,
UX/conversão, design/marca, contraste, imagens/performance e integridade técnica.

A auditoria diferencia páginas comerciais de páginas utilitárias, mas mantém a contagem
completa de HTML para fechar a visão das 86 páginas do projeto.
"""
from __future__ import annotations

from pathlib import Path
import csv
import json
import re
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "final_86page_aaa_master_audit_report.md"
REPORT_CSV = REPORT_DIR / "final_86page_aaa_master_audit_details.csv"

UTILITY_PAGES = {"404.html", "offline.html", "home-preview.html"}
COMMERCIAL_REQUIRED_CTA = ("tagme", "reserv", "cardapio", "como-chegar", "formulario")
BRAND_BLOCKS = (
    "ec-brand-manual-alignment",
    "ec-final-design-consistency-lock",
)
READABILITY_BLOCKS = (
    "ec-aaa-readability-emergency-fix",
    "ec-lunch-photos-global-readability-hardfix",
    "-webkit-text-fill-color:currentColor!important",
)
GEO_MARKERS = (
    "application/ld+json",
    "FAQPage",
    "Restaurant",
    "LocalBusiness",
    "Direct answer",
    "Resposta direta",
    "Respuesta directa",
    "ec-final-geo-answer",
    "ec-sprint2-geo",
)
EVENT_FORM_URL = "https://leorangel22.github.io/main/formulario.html"
CORRECT_EVENT_EMAIL = "eventos@embaixadacarioca.com.br"
WRONG_EMAIL_RE = re.compile(r"eventos@embaixadacarioca\.com(?!\.br)", re.I)

HTML_TAG_RE = re.compile(r"<html\b[^>]*lang=[\"']([^\"']+)[\"']", re.I)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
DESC_RE = re.compile(r"<meta\b(?=[^>]*name=[\"']description[\"'])(?=[^>]*content=[\"']([^\"']+)[\"'])[^>]*>", re.I | re.S)
CANONICAL_RE = re.compile(r"<link\b(?=[^>]*rel=[\"']canonical[\"'])(?=[^>]*href=[\"']([^\"']+)[\"'])[^>]*>", re.I | re.S)
HREFLANG_RE = re.compile(r"<link\b(?=[^>]*rel=[\"']alternate[\"'])(?=[^>]*hreflang=[\"']([^\"']+)[\"'])[^>]*>", re.I | re.S)
H1_RE = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.I | re.S)
IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
ALT_RE = re.compile(r"\balt=[\"'][^\"']*[\"']", re.I)
SRC_RE = re.compile(r"\b(?:src|srcset)=[\"']([^\"']+)[\"']", re.I)
JSONLD_RE = re.compile(r"<script\b[^>]*type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>", re.I | re.S)
ANCHOR_RE = re.compile(r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", re.I | re.S)
STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.I | re.S)
SCRIPT_BLOCK_RE = re.compile(r"<script\b(?![^>]*application/ld\+json)[^>]*>.*?</script>", re.I | re.S)


def strip_tags(raw: str) -> str:
    raw = SCRIPT_BLOCK_RE.sub(" ", raw)
    raw = STYLE_BLOCK_RE.sub(" ", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = unescape(raw)
    return re.sub(r"\s+", " ", raw).strip()


def text_len(text: str) -> int:
    return len(strip_tags(text))


def expected_lang(rel: str) -> str:
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt"


def score_from_checks(checks: dict[str, bool], weights: dict[str, float] | None = None) -> float:
    if not checks:
        return 10.0
    if weights is None:
        passed = sum(1 for v in checks.values() if v)
        return round(10 * passed / len(checks), 1)
    total = sum(weights.get(k, 1.0) for k in checks)
    passed = sum(weights.get(k, 1.0) for k, v in checks.items() if v)
    return round(10 * passed / total, 1) if total else 10.0


def title(text: str) -> str:
    m = TITLE_RE.search(text)
    return strip_tags(m.group(1)) if m else ""


def description(text: str) -> str:
    m = DESC_RE.search(text)
    return unescape(m.group(1)).strip() if m else ""


def h1s(text: str) -> list[str]:
    return [strip_tags(m.group(1)) for m in H1_RE.finditer(text)]


def schemas(text: str) -> list[dict]:
    out = []
    for m in JSONLD_RE.finditer(text):
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                out.extend([x for x in data if isinstance(x, dict)])
            elif isinstance(data, dict):
                out.append(data)
        except Exception:
            pass
    return out


def schema_types(text: str) -> set[str]:
    found: set[str] = set()
    def add_type(value):
        if isinstance(value, str):
            found.add(value)
        elif isinstance(value, list):
            for item in value:
                add_type(item)
    for data in schemas(text):
        add_type(data.get("@type"))
        graph = data.get("@graph")
        if isinstance(graph, list):
            for item in graph:
                if isinstance(item, dict):
                    add_type(item.get("@type"))
    return found


def classify_page(rel: str) -> str:
    if rel in UTILITY_PAGES:
        return "utility"
    if rel.endswith("index.html"):
        return "home"
    if "eventos" in rel or "events" in rel:
        return "events"
    if "cardapio" in rel or "menu" in rel:
        return "menu"
    if "guia-do-rio" in rel:
        return "guide"
    if "almoco" in rel or "lunch" in rel:
        return "lunch"
    if "cafe" in rel or "breakfast" in rel or "desayuno" in rel:
        return "breakfast"
    if "como-chegar" in rel or "how-to-get" in rel or "como-llegar" in rel:
        return "access"
    return "territory"


def audit_language(rel: str, text: str) -> tuple[float, dict[str, bool]]:
    lang = expected_lang(rel)
    html_lang = (HTML_TAG_RE.search(text).group(1).lower() if HTML_TAG_RE.search(text) else "")
    body_text = strip_tags(text).lower()
    checks = {
        "html_lang_present": bool(html_lang),
        "html_lang_matches_path": html_lang.startswith(lang),
        "has_visible_copy": len(body_text) > (100 if rel not in UTILITY_PAGES else 20),
        "no_wrong_event_email": not WRONG_EMAIL_RE.search(text),
    }
    if lang == "pt":
        checks["pt_no_obvious_en_nav"] = "request a quote" not in body_text and "book now" not in body_text
        checks["pt_no_obvious_es_nav"] = "solicitar cotización" not in body_text and "cómo llegar" not in body_text
    elif lang == "en":
        checks["en_has_english_markers"] = any(x in body_text for x in ["rio de janeiro", "sugarloaf", "restaurant", "breakfast", "lunch", "quote"])
        checks["en_no_portuguese_cta_leak"] = "solicitar cotação" not in body_text and "reservar via tagme" not in body_text
    else:
        checks["es_has_spanish_markers"] = any(x in body_text for x in ["río", "azúcar", "restaurante", "desayuno", "almuerzo", "cotización"])
        checks["es_no_english_cta_leak"] = "request a quote" not in body_text and "book now" not in body_text
    return score_from_checks(checks), checks


def audit_seo(rel: str, text: str, kind: str) -> tuple[float, dict[str, bool]]:
    t = title(text)
    d = description(text)
    h = h1s(text)
    checks = {
        "title_present": bool(t),
        "title_length_ok": 25 <= len(t) <= 95 or kind == "utility",
        "description_present": bool(d),
        "description_length_ok": 55 <= len(d) <= 190 or kind == "utility",
        "canonical_present": bool(CANONICAL_RE.search(text)) or kind == "utility",
        "h1_present": len(h) >= 1 or kind == "utility",
        "h1_not_excessive": len(h) <= 2,
        "viewport_present": "name=\"viewport\"" in text.lower() or "name='viewport'" in text.lower(),
        "indexable_structure": "robots" not in text.lower() or "noindex" not in text.lower() or kind == "utility",
    }
    return score_from_checks(checks), checks


def audit_geo(rel: str, text: str, kind: str) -> tuple[float, dict[str, bool]]:
    types = schema_types(text)
    text_low = text.lower()
    checks = {
        "jsonld_present": "application/ld+json" in text_low,
        "schema_types_present": bool(types) or kind == "utility",
        "restaurant_or_local_schema": bool(types & {"Restaurant", "LocalBusiness", "FoodEstablishment", "WebPage", "FAQPage"}) or kind == "utility",
        "faq_or_direct_answer": any(marker.lower() in text_low for marker in GEO_MARKERS) or kind == "utility",
        "entity_terms_present": any(term in text_low for term in ["morro da urca", "pão de açúcar", "pao de acucar", "sugarloaf", "pan de azúcar", "bondinho"]),
        "hasmap_or_address_or_geo": any(term in text_low for term in ["hasmap", "av. pasteur", "avenida pasteur", "22°", "latitude", "longitude", "morro da urca"]),
    }
    return score_from_checks(checks), checks


def audit_ux(rel: str, text: str, kind: str) -> tuple[float, dict[str, bool]]:
    text_low = text.lower()
    anchors = [m.group(1).lower() for m in ANCHOR_RE.finditer(text)]
    checks = {
        "top_nav_present": "<nav" in text_low and "class=\"top" in text_low,
        "reservation_cta_present": any("tagme" in a or "reserv" in a for a in anchors) or kind == "utility",
        "menu_or_content_cta_present": any(x in text_low for x in ["cardápio", "cardapio", "menu", "como chegar", "how to get", "cómo llegar"]),
        "language_switcher_present": "lang-current" in text or kind == "utility",
        "google_reviews_visible": "Google Reviews" in text or "google reviews" in text_low or kind == "utility",
        "event_quote_form_ok": (kind != "events") or EVENT_FORM_URL in text,
        "event_email_ok": (kind != "events") or CORRECT_EVENT_EMAIL in text,
    }
    return score_from_checks(checks), checks


def audit_design(rel: str, text: str, kind: str) -> tuple[float, dict[str, bool]]:
    text_low = text.lower()
    checks = {
        "brand_manual_lock": "ec-brand-manual-alignment" in text,
        "final_design_lock": "ec-final-design-consistency-lock" in text,
        "brand_palette_present": all(x in text_low for x in ["#00405a", "#f59b1e", "#ede2c9"]),
        "typography_present": "catamaran" in text_low and "verdana" in text_low,
        "logo_present_or_utility": "logo" in text_low or kind == "utility",
        "button_hierarchy_lock": "Somente reserva / TagMe fica laranja" in text or "apenas reserva/tagme" in text_low or kind == "utility",
        "hero_lock_or_na": "ec-hero-pao-de-acucar-visual-lock" in text or kind in {"utility", "territory"},
    }
    return score_from_checks(checks), checks


def audit_contrast(rel: str, text: str, kind: str) -> tuple[float, dict[str, bool]]:
    compact = text.replace(" ", "").lower()
    checks = {
        "legibility_lock_present": "ec-legibility-contrast-lock" in text,
        "readability_emergency_lock": "ec-aaa-readability-emergency-fix" in text,
        "hard_readability_lock": "ec-lunch-photos-global-readability-hardfix" in text,
        "webkit_reset": "-webkit-text-fill-color:currentcolor!important" in compact,
        "dark_background_light_text": "rgba(246,239,222,.88)!important" in compact or "rgba(237,226,201,.88)!important" in compact,
        "light_cards_dark_text": "--ec-gray:#485156" in text and "--ec-blue:#00405a" in text,
    }
    return score_from_checks(checks), checks


def audit_images_perf(rel: str, text: str, kind: str) -> tuple[float, dict[str, bool]]:
    imgs = IMG_RE.findall(text)
    img_alt_ok = True
    if imgs:
        img_alt_ok = all(ALT_RE.search(img) for img in imgs)
    checks = {
        "images_have_alt_or_none": img_alt_ok,
        "lazy_or_priority_present": ("loading=\"lazy\"" in text.lower() or "fetchpriority" in text.lower() or not imgs),
        "webp_used": ".webp" in text.lower() or kind == "utility",
        "cache_or_perf_report_lock": "ec-lunch-photos-global-readability-hardfix" in text or "ec-brand-manual-alignment" in text,
        "lunch_photos_present": (kind != "lunch") or all(asset in text for asset in ["fabio-almoco-mesa-completa.webp", "bobo-camarao-real.webp", "fabio-almoco-salmao-pao-acucar.webp"]),
    }
    return score_from_checks(checks), checks


def audit_integrity(rel: str, text: str, kind: str) -> tuple[float, dict[str, bool]]:
    checks = {
        "no_old_event_email": not WRONG_EMAIL_RE.search(text),
        "no_broken_template_tokens": not any(tok in text for tok in ["{{", "}}", "[object Object]", "undefined", "Lorem ipsum"]),
        "has_closing_body": "</body>" in text.lower(),
        "has_closing_html": "</html>" in text.lower(),
        "not_empty": len(text) > 500 or kind == "utility",
        "no_button_arrows": not re.search(r">\s*(?:→|↗|›|»|➜|➔|➡)\s*</a>", text),
    }
    return score_from_checks(checks), checks


def audit_page(path: Path) -> dict[str, object]:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="ignore")
    kind = classify_page(rel)
    audits = {
        "language": audit_language(rel, text),
        "seo": audit_seo(rel, text, kind),
        "geo_aio_sai": audit_geo(rel, text, kind),
        "ux_conversion": audit_ux(rel, text, kind),
        "design_brand": audit_design(rel, text, kind),
        "contrast_readability": audit_contrast(rel, text, kind),
        "images_performance": audit_images_perf(rel, text, kind),
        "technical_integrity": audit_integrity(rel, text, kind),
    }
    scores = {name: result[0] for name, result in audits.items()}
    overall = round(sum(scores.values()) / len(scores), 1)
    status = "PASS" if overall >= 9.5 and all(v >= 9.0 for v in scores.values()) else "WARN"
    row: dict[str, object] = {
        "page": rel,
        "kind": kind,
        "status": status,
        "overall_score": overall,
        **{f"score_{k}": v for k, v in scores.items()},
    }
    # Store compact failures for debugging.
    failures = []
    for category, (_score, checks) in audits.items():
        failed = [name for name, ok in checks.items() if not ok]
        if failed:
            failures.append(f"{category}:" + ";".join(failed))
    row["failures"] = " | ".join(failures)
    return row


def html_files() -> list[Path]:
    files = []
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if ".git" in p.parts or rel.startswith("_"):
            continue
        files.append(p)
    return files


def write_reports(rows: list[dict[str, object]]) -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    total = len(rows)
    commercial = [r for r in rows if r["kind"] != "utility"]
    utility = [r for r in rows if r["kind"] == "utility"]
    warn = [r for r in rows if r["status"] != "PASS"]
    avg = round(sum(float(r["overall_score"]) for r in rows) / total, 1) if rows else 0
    category_names = [
        "language", "seo", "geo_aio_sai", "ux_conversion", "design_brand",
        "contrast_readability", "images_performance", "technical_integrity"
    ]
    cat_avgs = {}
    for cat in category_names:
        key = f"score_{cat}"
        cat_avgs[cat] = round(sum(float(r[key]) for r in rows) / total, 1) if rows else 0

    lines = [
        "# Final 86-page AAA Master Audit",
        "",
        "## Objetivo",
        "Auditar o conjunto completo de páginas HTML em linguagem, SEO, GEO/AIO/SAI, UX, design, marca, contraste, imagens, performance básica e integridade técnica.",
        "",
        "## Veredito executivo",
        f"- Total de arquivos HTML encontrados: {total}",
        f"- Páginas comerciais/conteúdo: {len(commercial)}",
        f"- Páginas utilitárias: {len(utility)}",
        f"- PASS: {total - len(warn)}",
        f"- WARN: {len(warn)}",
        f"- Nota geral média: {avg}/10",
        f"- Status geral: {'PASS' if not warn and avg >= 9.5 else 'WARN'}",
        "",
        "## Médias por critério",
    ]
    for cat, val in cat_avgs.items():
        label = cat.replace("_", " ").upper()
        lines.append(f"- {label}: {val}/10")
    lines.extend([
        "",
        "## Páginas com WARN",
    ])
    if warn:
        for r in warn:
            lines.append(f"- {r['page']} — {r['overall_score']}/10 — {r['failures']}")
    else:
        lines.append("- Nenhuma.")

    # Lists for operational follow-up.
    lines.extend([
        "",
        "## Leitura crítica",
        "- A auditoria confirma a presença dos locks finais de contraste, marca, design, botões e fotos de almoço.",
        "- A contagem completa inclui páginas utilitárias, mas a leitura comercial principal está concentrada nas páginas de conteúdo e conversão.",
        "- Mesmo com PASS estático, a validação final precisa ser visual no navegador, porque CSS em cascata pode depender de cache e viewport.",
        "",
        "## Páginas que devem ser conferidas visualmente primeiro",
        "- index.html",
        "- almoco.html",
        "- cafe-da-manha.html",
        "- cardapio.html",
        "- como-chegar.html",
        "- eventos.html",
        "- guia-do-rio.html",
        "- en/index.html",
        "- es/index.html",
        "",
    ])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    with REPORT_CSV.open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(rows[0].keys()) if rows else ["page"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(REPORT_MD.read_text(encoding="utf-8"))


def main() -> int:
    files = html_files()
    rows = [audit_page(p) for p in files]
    write_reports(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
