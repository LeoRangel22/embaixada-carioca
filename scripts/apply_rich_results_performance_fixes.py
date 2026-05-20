#!/usr/bin/env python3
"""
Rich Results + Performance Hardening — Embaixada Carioca

Responde aos problemas vistos no Search Console/PageSpeed:
- FAQPage duplicado;
- author/datePublished/uploadDate inválidos ou ausentes;
- Review/AggregateRating duplicado ou aninhado incorretamente;
- Event/Offer sem performer/price/priceCurrency/validFrom;
- parent_node inválido;
- imagens sem prioridade/decoding/loading adequados;
- cache TTL limitado por hospedagem: adiciona service worker e arquivo _headers para CDN compatível.

Observação: GitHub Pages não permite controlar headers finos de Cache-Control pelo repositório.
O _headers fica pronto para eventual Cloudflare Pages/Netlify ou regra equivalente em CDN.
"""
from __future__ import annotations

from pathlib import Path
import datetime as dt
import html
import json
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
BASE = "https://www.embaixadacarioca.com"
TODAY = dt.date.today().isoformat()
DEFAULT_DT = f"{TODAY}T08:30:00-03:00"
DEFAULT_IMAGE = f"{BASE}/assets/hero.webp"
ORG = {
    "@type": "Organization",
    "@id": f"{BASE}/#organization",
    "name": "Embaixada Carioca",
    "url": BASE + "/",
    "logo": f"{BASE}/assets/logo-areia.svg",
}

LD_RE = re.compile(r"<script\b(?=[^>]*type=[\"']application/ld\+json[\"'])[^>]*>[\s\S]*?</script>", re.I)
LD_CONTENT_RE = re.compile(r"<script\b(?=[^>]*type=[\"']application/ld\+json[\"'])[^>]*>([\s\S]*?)</script>", re.I)
HEAD_CLOSE_RE = re.compile(r"</head>", re.I)
BODY_CLOSE_RE = re.compile(r"</body>", re.I)
TITLE_RE = re.compile(r"<title[^>]*>([\s\S]*?)</title>", re.I)
META_DESC_RE = re.compile(r"<meta\s+[^>]*name=[\"']description[\"'][^>]*content=[\"']([^\"']*)[\"'][^>]*>", re.I)
H1_RE = re.compile(r"<h1\b[^>]*>([\s\S]*?)</h1>", re.I)
IMG_RE = re.compile(r"<img\b[^>]*>", re.I)

FAQ_MARK_START = "<!-- EC Rich Results Consolidated FAQ -->"
FAQ_MARK_END = "<!-- /EC Rich Results Consolidated FAQ -->"
FAQ_MARK_RE = re.compile(r"\n*<!-- EC Rich Results Consolidated FAQ -->[\s\S]*?<!-- /EC Rich Results Consolidated FAQ -->\s*", re.I)
SW_MARK_START = "<!-- EC Performance Service Worker -->"
SW_MARK_END = "<!-- /EC Performance Service Worker -->"
SW_MARK_RE = re.compile(r"\n*<!-- EC Performance Service Worker -->[\s\S]*?<!-- /EC Performance Service Worker -->\s*", re.I)

COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "jsonld_scripts_parsed": 0,
    "jsonld_scripts_rewritten": 0,
    "jsonld_scripts_removed": 0,
    "faq_pages_consolidated": 0,
    "faq_entities_merged": 0,
    "articles_fixed": 0,
    "dates_fixed": 0,
    "offers_fixed_or_removed": 0,
    "events_converted_to_services": 0,
    "reviews_removed": 0,
    "parent_node_removed": 0,
    "images_hardened": 0,
    "service_worker_registered": 0,
    "files_written": 0,
    "remaining_warnings": 0,
}
ACTIONS: list[str] = []
WARNINGS: list[str] = []


def strip_tags(text: str) -> str:
    text = re.sub(r"<script\b[\s\S]*?</script>|<style\b[\s\S]*?</style>|<!--[^>]*-->", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def page_title(source: str, rel: str) -> str:
    for rx in (H1_RE, TITLE_RE):
        m = rx.search(source)
        if m:
            t = strip_tags(m.group(1))
            if t:
                return t[:110]
    return "Embaixada Carioca"


def page_description(source: str) -> str:
    m = META_DESC_RE.search(source)
    if m and m.group(1).strip():
        return html.unescape(m.group(1)).strip()[:260]
    return "Restaurante brasileiro no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com vista, café da manhã, almoço, caipirinhas e eventos."


def page_url(rel: str) -> str:
    return BASE + ("/" if rel == "index.html" else "/" + rel)


def as_types(value: Any) -> set[str]:
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {str(x) for x in value}
    return set()


def has_type(node: Any, typename: str) -> bool:
    return isinstance(node, dict) and typename in as_types(node.get("@type"))


def ensure_iso_datetime(value: Any) -> str:
    global COUNTERS
    if not isinstance(value, str) or not value.strip():
        COUNTERS["dates_fixed"] += 1
        return DEFAULT_DT
    v = value.strip()
    # yyyy-mm-dd -> full datetime with Brazilian timezone.
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
        COUNTERS["dates_fixed"] += 1
        return f"{v}T08:30:00-03:00"
    # Missing timezone.
    if "T" in v and not re.search(r"(Z|[+-]\d{2}:?\d{2})$", v):
        COUNTERS["dates_fixed"] += 1
        return v + "-03:00"
    # Invalid-looking datetime -> default.
    if not re.match(r"^\d{4}-\d{2}-\d{2}T", v):
        COUNTERS["dates_fixed"] += 1
        return DEFAULT_DT
    return v


def normalize_author(node: dict[str, Any]) -> None:
    author = node.get("author")
    valid = isinstance(author, dict) and author.get("@type") in {"Person", "Organization"} and author.get("name")
    if not valid:
        node["author"] = ORG


def normalize_article(node: dict[str, Any], rel: str, source: str) -> None:
    node.setdefault("headline", page_title(source, rel))
    node.setdefault("description", page_description(source))
    node.setdefault("image", [DEFAULT_IMAGE])
    node.setdefault("mainEntityOfPage", {"@type": "WebPage", "@id": page_url(rel)})
    normalize_author(node)
    node["publisher"] = ORG
    node["datePublished"] = ensure_iso_datetime(node.get("datePublished"))
    node["dateModified"] = ensure_iso_datetime(node.get("dateModified", node["datePublished"]))
    COUNTERS["articles_fixed"] += 1


def normalize_media(node: dict[str, Any], rel: str, source: str) -> None:
    types = as_types(node.get("@type"))
    if "VideoObject" in types:
        node.setdefault("name", page_title(source, rel))
        node.setdefault("description", page_description(source))
        node.setdefault("thumbnailUrl", [DEFAULT_IMAGE])
        node["uploadDate"] = ensure_iso_datetime(node.get("uploadDate"))
        node.setdefault("url", page_url(rel))
    if "ImageObject" in types:
        node.setdefault("url", node.get("contentUrl") or DEFAULT_IMAGE)
        node.setdefault("contentUrl", node.get("url") or DEFAULT_IMAGE)
        node.setdefault("caption", page_title(source, rel))


def normalize_offer(offer: Any, rel: str) -> Any:
    # GSC reclama quando Offer existe sem price/priceCurrency/validFrom/url.
    # Se não há preço real, remove o Offer em vez de publicar preço falso.
    if isinstance(offer, list):
        fixed = [normalize_offer(x, rel) for x in offer]
        fixed = [x for x in fixed if x is not None]
        return fixed or None
    if not isinstance(offer, dict):
        return None
    if not offer.get("price"):
        COUNTERS["offers_fixed_or_removed"] += 1
        return None
    offer.setdefault("@type", "Offer")
    offer.setdefault("priceCurrency", "BRL")
    offer.setdefault("url", page_url(rel))
    offer["validFrom"] = ensure_iso_datetime(offer.get("validFrom"))
    return offer


def sanitize_node(node: Any, rel: str, source: str, faq_entities: list[dict[str, Any]]) -> Any:
    if isinstance(node, list):
        out = []
        for item in node:
            clean = sanitize_node(item, rel, source, faq_entities)
            if clean is not None:
                out.append(clean)
        return out
    if not isinstance(node, dict):
        return node

    if "parent_node" in node:
        node.pop("parent_node", None)
        COUNTERS["parent_node_removed"] += 1

    types = as_types(node.get("@type"))

    # Consolidar FAQPage em script único por página.
    if "FAQPage" in types:
        entities = node.get("mainEntity") or []
        if isinstance(entities, dict):
            entities = [entities]
        for q in entities:
            if isinstance(q, dict) and q.get("name"):
                faq_entities.append(q)
        COUNTERS["faq_pages_consolidated"] += 1
        return None

    # Reviews são a origem mais comum de erros de aggregateRating/parent_node.
    # Mantemos aggregateRating apenas no Restaurant/LocalBusiness.
    if "Review" in types:
        COUNTERS["reviews_removed"] += 1
        return None
    if "review" in node:
        node.pop("review", None)
        COUNTERS["reviews_removed"] += 1

    # Eventos privados/corporativos sob orçamento não são ticketed Event no Google.
    # Convertendo para Service, removemos performer/offers inválidos sem criar preço falso.
    if "Event" in types:
        node["@type"] = "Service"
        node.setdefault("serviceType", "Eventos e experiências gastronômicas no Morro da Urca")
        node.pop("performer", None)
        node.pop("startDate", None)
        node.pop("endDate", None)
        node.pop("eventAttendanceMode", None)
        node.pop("eventStatus", None)
        node.pop("offers", None)
        COUNTERS["events_converted_to_services"] += 1

    if {"Article", "BlogPosting", "NewsArticle"} & types:
        normalize_article(node, rel, source)

    normalize_media(node, rel, source)

    # Datas genéricas com fuso horário.
    for key in ("datePublished", "dateModified", "uploadDate", "validFrom"):
        if key in node:
            node[key] = ensure_iso_datetime(node.get(key))

    # Author válido para CreativeWork-like.
    if types & {"Article", "BlogPosting", "NewsArticle", "CreativeWork"}:
        normalize_author(node)

    # Offer: remover se incompleto, normalizar se tiver preço real.
    if "offers" in node:
        fixed = normalize_offer(node.get("offers"), rel)
        if fixed is None:
            node.pop("offers", None)
        else:
            node["offers"] = fixed

    # aggregateRating só fica onde faz sentido.
    if "aggregateRating" in node and not (types & {"Restaurant", "LocalBusiness", "FoodEstablishment", "Product"}):
        node.pop("aggregateRating", None)

    # url padrão quando Google pede url em objetos criativos/ofertas.
    if (types & {"Article", "BlogPosting", "NewsArticle", "CreativeWork", "ImageObject", "VideoObject", "Service", "Product"}) and not node.get("url"):
        node["url"] = page_url(rel)

    # Recursão final.
    for key, value in list(node.items()):
        clean = sanitize_node(value, rel, source, faq_entities)
        if clean is None:
            node.pop(key, None)
        else:
            node[key] = clean

    if "@graph" in node and isinstance(node["@graph"], list):
        node["@graph"] = [x for x in node["@graph"] if x]
        if not node["@graph"] and set(node.keys()) <= {"@context", "@graph"}:
            return None
    return node


def consolidated_faq_script(faq_entities: list[dict[str, Any]], rel: str) -> str:
    seen: set[str] = set()
    clean: list[dict[str, Any]] = []
    for q in faq_entities:
        name = strip_tags(str(q.get("name", ""))).strip()
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())
        ans = q.get("acceptedAnswer") or {}
        text = ""
        if isinstance(ans, dict):
            text = strip_tags(str(ans.get("text", ""))).strip()
        if not text:
            continue
        clean.append({"@type": "Question", "name": name, "acceptedAnswer": {"@type": "Answer", "text": text}})
    if not clean:
        return ""
    COUNTERS["faq_entities_merged"] += len(clean)
    data = {"@context": "https://schema.org", "@type": "FAQPage", "@id": page_url(rel) + "#faq", "mainEntity": clean}
    return f"{FAQ_MARK_START}\n<script type=\"application/ld+json\">{json.dumps(data, ensure_ascii=False, separators=(',', ':'))}</script>\n{FAQ_MARK_END}"


def process_jsonld(text: str, rel: str) -> str:
    original = text
    text = FAQ_MARK_RE.sub("\n", text)
    matches = list(LD_RE.finditer(text))
    if not matches:
        return text

    faq_entities: list[dict[str, Any]] = []
    replacements: list[tuple[tuple[int, int], str]] = []

    for m in matches:
        raw_script = m.group(0)
        cm = LD_CONTENT_RE.search(raw_script)
        if not cm:
            continue
        raw_json = html.unescape(cm.group(1).strip())
        try:
            data = json.loads(raw_json)
        except Exception:
            continue
        COUNTERS["jsonld_scripts_parsed"] += 1
        clean = sanitize_node(data, rel, text, faq_entities)
        if clean is None or clean == {}:
            replacements.append((m.span(), ""))
            COUNTERS["jsonld_scripts_removed"] += 1
        else:
            new_script = f'<script type="application/ld+json">{json.dumps(clean, ensure_ascii=False, separators=(",", ":"))}</script>'
            if new_script != raw_script:
                COUNTERS["jsonld_scripts_rewritten"] += 1
            replacements.append((m.span(), new_script))

    # Apply replacements backwards.
    for (start, end), repl in reversed(replacements):
        text = text[:start] + repl + text[end:]

    faq_script = consolidated_faq_script(faq_entities, rel)
    if faq_script and HEAD_CLOSE_RE.search(text):
        text = HEAD_CLOSE_RE.sub(faq_script + "\n</head>", text, count=1)

    if text != original:
        ACTIONS.append(f"RICH_RESULTS: {rel}")
    return text


def harden_images(text: str, rel: str) -> str:
    original = text
    seen_hero = False

    def repl(match: re.Match[str]) -> str:
        nonlocal seen_hero
        tag = match.group(0)
        low = tag.lower()
        new = tag
        if "<img" not in low:
            return tag
        is_hero = "hero-photo" in low or (not seen_hero and "loading=\"eager\"" in low)
        if is_hero:
            seen_hero = True
            if "fetchpriority=" not in low:
                new = new[:-1] + ' fetchpriority="high">'
            if "loading=\"lazy\"" in new.lower():
                new = re.sub(r'\sloading=["\']lazy["\']', ' loading="eager"', new, flags=re.I)
        else:
            if "loading=" not in low:
                new = new[:-1] + ' loading="lazy">'
        if "decoding=" not in new.lower():
            new = new[:-1] + ' decoding="async">'
        if new != tag:
            COUNTERS["images_hardened"] += 1
        return new

    text = IMG_RE.sub(repl, text)
    if text != original:
        ACTIONS.append(f"IMAGES: {rel}")
    return text


def service_worker_snippet() -> str:
    return f"""{SW_MARK_START}
<script>
(function(){{
  if(!('serviceWorker' in navigator) || location.protocol !== 'https:') return;
  var run=function(){{navigator.serviceWorker.register('/sw.js').catch(function(){{}});}};
  if('requestIdleCallback' in window) requestIdleCallback(run, {{timeout: 3500}}); else window.addEventListener('load', run);
}})();
</script>
{SW_MARK_END}"""


def register_service_worker(text: str, rel: str) -> str:
    original = text
    text = SW_MARK_RE.sub("\n", text)
    if BODY_CLOSE_RE.search(text):
        text = BODY_CLOSE_RE.sub(service_worker_snippet() + "\n</body>", text, count=1)
    if text != original:
        COUNTERS["service_worker_registered"] += 1
        ACTIONS.append(f"SERVICE_WORKER: {rel}")
    return text


def process_html(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix != ".html" or rel.startswith("_") or ".git" in path.parts:
        return
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    text = process_jsonld(text, rel)
    text = harden_images(text, rel)
    text = register_service_worker(text, rel)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1


def write_sw_and_headers() -> None:
    sw = """const CACHE_VERSION = 'ec-assets-v2026-05-20';
const ASSET_PATTERNS = [/^\/assets\//, /^\/fonts\//];
self.addEventListener('install', event => { self.skipWaiting(); });
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (url.origin !== location.origin || event.request.method !== 'GET') return;
  if (!ASSET_PATTERNS.some(rx => rx.test(url.pathname))) return;
  event.respondWith(caches.open(CACHE_VERSION).then(cache => cache.match(event.request).then(cached => {
    const network = fetch(event.request).then(response => { if (response && response.ok) cache.put(event.request, response.clone()); return response; }).catch(() => cached);
    return cached || network;
  })));
});
"""
    headers = """# Cache headers for CDN platforms that support _headers (Cloudflare Pages/Netlify).
# GitHub Pages ignores this file; use Cloudflare cache rules if staying on GitHub Pages origin.
/assets/*
  Cache-Control: public, max-age=31536000, immutable
/fonts/*
  Cache-Control: public, max-age=31536000, immutable
/sw.js
  Cache-Control: no-cache
/*.html
  Cache-Control: public, max-age=300, must-revalidate
"""
    (ROOT / "sw.js").write_text(sw, encoding="utf-8")
    (ROOT / "_headers").write_text(headers, encoding="utf-8")
    COUNTERS["files_written"] += 2
    ACTIONS.append("FILES: sw.js + _headers")


def audit_remaining() -> None:
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("_") or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        faq_count = text.count('"@type":"FAQPage"') + text.count('"@type": "FAQPage"')
        if faq_count > 1:
            WARNINGS.append(f"{rel}: FAQPage duplicado ({faq_count})")
        if "parent_node" in text:
            WARNINGS.append(f"{rel}: parent_node remanescente")
        if '"@type":"Review"' in text or '"@type": "Review"' in text:
            WARNINGS.append(f"{rel}: Review remanescente")
        if '"@type":"Event"' in text or '"@type": "Event"' in text:
            WARNINGS.append(f"{rel}: Event remanescente")
    COUNTERS["remaining_warnings"] = len(WARNINGS)


def write_report() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    out = REPORT_DIR / "rich_results_performance_fix_report.md"
    lines = [
        "# Rich Results + Performance Hardening",
        "",
        "## Objetivo",
        "Corrigir os problemas apontados pelo Search Console/PSI: FAQ duplicado, author/datePublished/uploadDate, Review/AggregateRating, Event/Offer, parent_node, imagens e cache de repetição.",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend([
        "",
        "## Limite importante sobre cache",
        "O alerta de cache TTL em GitHub Pages tende a continuar enquanto a origem for GitHub Pages, pois o repositório não controla Cache-Control de assets. O script adicionou service worker e _headers para CDN compatível; para zerar o alerta no PSI, use Cloudflare/cache rules ou hospedagem que aceite headers customizados.",
        "",
        "## Ações",
    ])
    lines.extend(f"- {a}" for a in ACTIONS) if ACTIONS else lines.append("- Nenhuma ação necessária.")
    lines.extend(["", "## Warnings remanescentes"])
    lines.extend(f"- {w}" for w in WARNINGS) if WARNINGS else lines.append("- Nenhum warning estático encontrado nos padrões tratados.")
    lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


def main() -> int:
    for path in sorted(ROOT.rglob("*.html")):
        process_html(path)
    write_sw_and_headers()
    audit_remaining()
    write_report()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
