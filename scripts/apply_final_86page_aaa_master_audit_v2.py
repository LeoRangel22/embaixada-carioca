#!/usr/bin/env python3
"""Final Site AAA Master Audit V2 — Embaixada Carioca.

Recalibragem da auditoria mestre para refletir a realidade visual pós-correções:
- não confunde chaves de CSS/JS com template quebrado;
- aceita o closeout design lock e o visual readability reality fix como locks válidos;
- trata páginas utilitárias como utilitárias, sem exigir navegação/CTA comercial;
- usa o sitemap como fonte de verdade para a contagem das páginas públicas.
"""
from __future__ import annotations

from pathlib import Path
import csv
import json
import re
import urllib.parse
import xml.etree.ElementTree as ET
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "final_86page_aaa_master_audit_report.md"
REPORT_CSV = REPORT_DIR / "final_86page_aaa_master_audit_details.csv"

UTILITY_PAGES = {"404.html", "offline.html", "home-preview.html"}
EVENT_FORM_URL = "https://leorangel22.github.io/main/formulario.html"
CORRECT_EVENT_EMAIL = "eventos@embaixadacarioca.com.br"
WRONG_EMAIL_RE = re.compile(r"eventos@embaixadacarioca\.com(?!\.br)", re.I)

HTML_TAG_RE = re.compile(r"<html\b[^>]*lang=[\"']([^\"']+)[\"']", re.I)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
DESC_RE = re.compile(r"<meta\b(?=[^>]*name=[\"']description[\"'])(?=[^>]*content=[\"']([^\"']+)[\"'])[^>]*>", re.I | re.S)
CANONICAL_RE = re.compile(r"<link\b(?=[^>]*rel=[\"']canonical[\"'])(?=[^>]*href=[\"']([^\"']+)[\"'])[^>]*>", re.I | re.S)
H1_RE = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.I | re.S)
IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
ALT_RE = re.compile(r"\balt=[\"'][^\"']*[\"']", re.I)
JSONLD_RE = re.compile(r"<script\b[^>]*type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>", re.I | re.S)
ANCHOR_RE = re.compile(r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", re.I | re.S)
STYLE_RE = re.compile(r"<style\b[^>]*>.*?</style>", re.I | re.S)
SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.I | re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

DESIGN_LOCK_MARKERS = (
    "ec-final-design-consistency-lock",
    "EC AAA Closeout Design Lock",
    "ec-aaa-closeout-design-lock",
    "ec-visual-readability-reality-fix",
)
BRAND_MARKERS = (
    "ec-brand-manual-alignment",
    "#00405a",
    "#f59b1e",
    "#ede2c9",
)
CONTRAST_MARKERS = (
    "ec-visual-readability-reality-fix",
    "ec-lunch-photos-global-readability-hardfix",
    "ec-aaa-readability-emergency-fix",
    "ec-legibility-contrast-lock",
)
GEO_MARKERS = (
    "application/ld+json",
    "FAQPage",
    "Restaurant",
    "LocalBusiness",
    "Resposta direta",
    "Direct answer",
    "Respuesta directa",
    "ec-final-geo-answer",
    "ec-sprint2-geo",
)


def strip_tags(raw: str) -> str:
    raw = SCRIPT_RE.sub(" ", raw)
    raw = STYLE_RE.sub(" ", raw)
    raw = COMMENT_RE.sub(" ", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = unescape(raw)
    return re.sub(r"\s+", " ", raw).strip()


def content_for_integrity(raw: str) -> str:
    raw = SCRIPT_RE.sub(" ", raw)
    raw = STYLE_RE.sub(" ", raw)
    raw = COMMENT_RE.sub(" ", raw)
    raw = unescape(raw)
    return raw


def score(checks: dict[str, bool]) -> float:
    if not checks:
        return 10.0
    return round(10 * sum(1 for v in checks.values() if v) / len(checks), 1)


def expected_lang(rel: str) -> str:
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt"


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


def title(text: str) -> str:
    m = TITLE_RE.search(text)
    return strip_tags(m.group(1)) if m else ""


def description(text: str) -> str:
    m = DESC_RE.search(text)
    return unescape(m.group(1)).strip() if m else ""


def h1_count(text: str) -> int:
    return len(H1_RE.findall(text))


def schema_types(text: str) -> set[str]:
    out: set[str] = set()
    def add_type(v):
        if isinstance(v, str):
            out.add(v)
        elif isinstance(v, list):
            for x in v:
                add_type(x)
    for m in JSONLD_RE.finditer(text):
        try:
            data = json.loads(m.group(1).strip())
        except Exception:
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if isinstance(item, dict):
                add_type(item.get("@type"))
                graph = item.get("@graph")
                if isinstance(graph, list):
                    for g in graph:
                        if isinstance(g, dict):
                            add_type(g.get("@type"))
    return out


def audit_language(rel: str, text: str, kind: str):
    lang = expected_lang(rel)
    html_lang_match = HTML_TAG_RE.search(text)
    html_lang = html_lang_match.group(1).lower() if html_lang_match else ""
    visible = strip_tags(text).lower()
    checks = {
        "html_lang_present": bool(html_lang),
        "html_lang_matches_path": html_lang.startswith(lang),
        "visible_copy_present": len(visible) > (20 if kind == "utility" else 120),
        "event_email_domain_ok": not WRONG_EMAIL_RE.search(text),
    }
    if kind != "utility":
        if lang == "pt":
            checks["pt_no_major_foreign_cta_leak"] = "request a quote" not in visible and "solicitar cotización" not in visible
        elif lang == "en":
            checks["en_marker_present"] = any(x in visible for x in ["rio", "restaurant", "sugarloaf", "breakfast", "lunch", "quote"])
        else:
            checks["es_marker_present"] = any(x in visible for x in ["río", "azúcar", "restaurante", "desayuno", "almuerzo", "cotización"])
    return score(checks), checks


def audit_seo(rel: str, text: str, kind: str):
    t = title(text)
    d = description(text)
    h1 = h1_count(text)
    checks = {
        "title_present": bool(t),
        "title_length_ok": kind == "utility" or 25 <= len(t) <= 95,
        "description_present": bool(d),
        "description_length_ok": kind == "utility" or 45 <= len(d) <= 190,
        "viewport_present": "name=\"viewport\"" in text.lower() or "name='viewport'" in text.lower(),
        "canonical_or_utility": kind == "utility" or bool(CANONICAL_RE.search(text)),
        "h1_or_utility": kind == "utility" or h1 >= 1,
        "h1_not_excessive": h1 <= 3,
    }
    return score(checks), checks


def audit_geo(rel: str, text: str, kind: str):
    low = text.lower()
    types = schema_types(text)
    checks = {
        "jsonld_or_utility": kind == "utility" or "application/ld+json" in low,
        "schema_types_or_utility": kind == "utility" or bool(types),
        "restaurant_local_or_web_schema": kind == "utility" or bool(types & {"Restaurant", "LocalBusiness", "FoodEstablishment", "WebPage", "FAQPage"}),
        "geo_or_direct_answer_marker": kind == "utility" or any(m.lower() in low for m in GEO_MARKERS),
        "entity_terms_present": kind == "utility" or any(x in low for x in ["morro da urca", "pão de açúcar", "pao de acucar", "sugarloaf", "pan de azúcar", "bondinho"]),
        "address_or_map_present": kind == "utility" or any(x in low for x in ["av. pasteur", "avenida pasteur", "hasmap", "22°", "morro da urca"]),
    }
    return score(checks), checks


def audit_ux(rel: str, text: str, kind: str):
    low = text.lower()
    anchors = [m.group(1).lower() for m in ANCHOR_RE.finditer(text)]
    checks = {
        "top_nav_or_utility": kind == "utility" or ("<nav" in low and "class=\"top" in low),
        "reservation_cta_or_utility": kind == "utility" or any("tagme" in a or "reserv" in a for a in anchors),
        "content_cta_present_or_utility": kind == "utility" or any(x in low for x in ["cardápio", "cardapio", "menu", "como chegar", "how to get", "cómo llegar", "cotação", "quote", "cotización"]),
        "language_switcher_or_utility": kind == "utility" or "lang-current" in text,
        "reviews_or_utility": kind == "utility" or "google reviews" in low or "7.779" in low,
        "event_quote_form_ok": kind != "events" or EVENT_FORM_URL in text,
        "event_email_ok": kind != "events" or CORRECT_EVENT_EMAIL in text,
    }
    return score(checks), checks


def audit_design(rel: str, text: str, kind: str):
    low = text.lower()
    checks = {
        "brand_system_or_utility": kind == "utility" or any(m.lower() in low for m in [x.lower() for x in BRAND_MARKERS]),
        "design_lock_or_closeout_or_utility": kind == "utility" or any(m.lower() in low for m in [x.lower() for x in DESIGN_LOCK_MARKERS]),
        "palette_present_or_utility": kind == "utility" or all(x in low for x in ["#00405a", "#f59b1e"]),
        "typography_or_utility": kind == "utility" or ("catamaran" in low and "verdana" in low),
        "logo_or_utility": kind == "utility" or "logo" in low,
        "button_hierarchy_or_utility": kind == "utility" or any(x in low for x in ["somente reserva / tagme", "reserva / tagme", "ec-vr-yellow", "ec-aaa-closeout-design-lock"]),
    }
    return score(checks), checks


def audit_contrast(rel: str, text: str, kind: str):
    low = text.lower().replace(" ", "")
    checks = {
        "contrast_lock_or_utility": kind == "utility" or any(m.lower().replace(" ", "") in low for m in CONTRAST_MARKERS),
        "visual_reality_fix_or_utility": kind == "utility" or "ec-visual-readability-reality-fix" in low,
        "webkit_reset_or_utility": kind == "utility" or "-webkit-text-fill-color:currentcolor!important" in low,
        "dark_text_light_rule_or_utility": kind == "utility" or "rgba(246,239,222,.90)!important" in low or "rgba(246,239,222,.88)!important" in low,
        "light_card_dark_text_rule_or_utility": kind == "utility" or "--ec-vr-gray:#485156" in low or "--ec-gray:#485156" in low,
        "menu_green_title_rule_or_utility": kind == "utility" or kind != "menu" or "#335d4a" in low,
    }
    return score(checks), checks


def audit_images(rel: str, text: str, kind: str):
    imgs = IMG_RE.findall(text)
    checks = {
        "alt_ok_or_no_images": all(ALT_RE.search(img) for img in imgs) if imgs else True,
        "lazy_or_priority_or_no_images": "loading=\"lazy\"" in text.lower() or "fetchpriority" in text.lower() or not imgs,
        "webp_or_utility": kind == "utility" or ".webp" in text.lower(),
        "lunch_photos_or_not_lunch": kind != "lunch" or all(x in text for x in ["fabio-almoco-mesa-completa.webp", "bobo-camarao-real.webp", "fabio-almoco-salmao-pao-acucar.webp"]),
    }
    return score(checks), checks


def audit_integrity(rel: str, text: str, kind: str):
    visible = content_for_integrity(text)
    # Evita falso positivo por chaves legítimas de CSS/JS removidas acima. Só marca tokens visíveis típicos de template quebrado.
    broken_template = bool(re.search(r"\{\{\s*[A-Za-z0-9_.-]+\s*\}\}", visible))
    checks = {
        "no_old_event_email": not WRONG_EMAIL_RE.search(text),
        "no_visible_broken_template_tokens": not broken_template and "[object Object]" not in visible and "Lorem ipsum" not in visible,
        "no_visible_undefined": "undefined" not in strip_tags(text).lower(),
        "has_closing_body": "</body>" in text.lower(),
        "has_closing_html": "</html>" in text.lower(),
        "not_empty": len(text) > (200 if kind == "utility" else 900),
        "no_standalone_button_arrows": not re.search(r">\s*(?:→|↗|›|»|➜|➔|➡)\s*</a>", text),
    }
    return score(checks), checks


def html_files() -> list[Path]:
    """Return only indexable sitemap pages plus intentional utility pages.

    The old recursive scan included Playwright dependencies, generated test
    reports and source partials whenever those folders existed locally. That
    inflated the audit and produced false WARN results unrelated to the site.
    """
    sitemap = ROOT / "sitemap.xml"
    out: dict[str, Path] = {}
    if sitemap.exists():
        tree = ET.parse(sitemap)
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for node in tree.findall("s:url/s:loc", ns):
            if not node.text:
                continue
            url_path = urllib.parse.unquote(urllib.parse.urlparse(node.text).path)
            rel = "index.html" if url_path in {"", "/"} else url_path.lstrip("/")
            page = ROOT / rel
            if page.is_file() and page.suffix.lower() == ".html":
                out[rel] = page
    for rel in sorted(UTILITY_PAGES):
        page = ROOT / rel
        if page.is_file():
            out.setdefault(rel, page)
    return [out[rel] for rel in sorted(out)]


def audit_page(path: Path) -> dict[str, object]:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="ignore")
    kind = classify_page(rel)
    audits = {
        "language": audit_language(rel, text, kind),
        "seo": audit_seo(rel, text, kind),
        "geo_aio_sai": audit_geo(rel, text, kind),
        "ux_conversion": audit_ux(rel, text, kind),
        "design_brand": audit_design(rel, text, kind),
        "contrast_readability": audit_contrast(rel, text, kind),
        "images_performance": audit_images(rel, text, kind),
        "technical_integrity": audit_integrity(rel, text, kind),
    }
    scores = {k: v[0] for k, v in audits.items()}
    overall = round(sum(scores.values()) / len(scores), 1)
    status = "PASS" if overall >= 9.5 and all(v >= 9.0 for v in scores.values()) else "WARN"
    failures = []
    for category, (_s, checks) in audits.items():
        failed = [k for k, ok in checks.items() if not ok]
        if failed:
            failures.append(f"{category}:" + ";".join(failed))
    return {"page": rel, "kind": kind, "status": status, "overall_score": overall, **{f"score_{k}": v for k, v in scores.items()}, "failures": " | ".join(failures)}


def write_reports(rows: list[dict[str, object]]):
    REPORT_DIR.mkdir(exist_ok=True)
    total = len(rows)
    commercial = [r for r in rows if r["kind"] != "utility"]
    utility = [r for r in rows if r["kind"] == "utility"]
    warn = [r for r in rows if r["status"] != "PASS"]
    avg = round(sum(float(r["overall_score"]) for r in rows) / total, 1) if rows else 0
    categories = ["language", "seo", "geo_aio_sai", "ux_conversion", "design_brand", "contrast_readability", "images_performance", "technical_integrity"]
    cat_avgs = {cat: round(sum(float(r[f"score_{cat}"]) for r in rows) / total, 1) for cat in categories}
    lines = [
        "# Final Site AAA Master Audit",
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
        lines.append(f"- {cat.replace('_', ' ').upper()}: {val}/10")
    lines += ["", "## Páginas com WARN"]
    if warn:
        for r in warn:
            lines.append(f"- {r['page']} — {r['overall_score']}/10 — {r['failures']}")
    else:
        lines.append("- Nenhuma.")
    lines += ["", "## Leitura crítica", "- Auditoria V2 recalibrada para não confundir CSS/JS legítimo com template quebrado.", "- O visual readability reality fix é considerado lock válido de contraste real.", "- Páginas utilitárias são auditadas, mas com critérios compatíveis com função utilitária.", ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    with REPORT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(rows[0].keys()) if rows else ["page"],
            lineterminator="\n",
        )
        writer.writeheader(); writer.writerows(rows)
    print(REPORT_MD.read_text(encoding="utf-8"))


def main() -> int:
    rows = [audit_page(p) for p in html_files()]
    write_reports(rows)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
