#!/usr/bin/env python3
"""Bulk-add GEO signals (containedInPlace + nearbyAttraction) to all remaining pages."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCRIPT_RE = re.compile(
    r'(<script\s[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.I | re.S
)

CONTAINED_IN = {
    "@type": "TouristAttraction",
    "name": "Parque Bondinho Pão de Açúcar",
    "url": "https://bondinho.com.br/",
    "sameAs": "https://en.wikipedia.org/wiki/Sugarloaf_Mountain",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Praça General Tibúrcio, 68",
        "addressLocality": "Rio de Janeiro",
        "addressRegion": "RJ",
        "addressCountry": "BR"
    }
}

NEARBY_PT = [
    {"@type": "TouristAttraction", "name": "Pão de Açúcar",
     "sameAs": "https://en.wikipedia.org/wiki/Sugarloaf_Mountain"},
    {"@type": "TouristAttraction", "name": "Morro da Urca",
     "sameAs": "https://en.wikipedia.org/wiki/Urca_Hill"}
]
NEARBY_EN = [
    {"@type": "TouristAttraction", "name": "Sugarloaf Mountain",
     "sameAs": "https://en.wikipedia.org/wiki/Sugarloaf_Mountain"},
    {"@type": "TouristAttraction", "name": "Urca Hill",
     "sameAs": "https://en.wikipedia.org/wiki/Urca_Hill"}
]
NEARBY_ES = [
    {"@type": "TouristAttraction", "name": "Pan de Azúcar",
     "sameAs": "https://en.wikipedia.org/wiki/Sugarloaf_Mountain"},
    {"@type": "TouristAttraction", "name": "Morro da Urca",
     "sameAs": "https://en.wikipedia.org/wiki/Urca_Hill"}
]

SKIP = {"404.html", "offline.html", "home-preview.html"}
RESTAURANT_TYPES = {"Restaurant", "FoodEstablishment", "LocalBusiness"}


def nearby_for(rel):
    if rel.startswith("en/") or rel.startswith("en\\"):
        return NEARBY_EN
    if rel.startswith("es/") or rel.startswith("es\\"):
        return NEARBY_ES
    return NEARBY_PT


def add_geo(obj, nearby):
    changed = False
    if isinstance(obj, dict):
        t = obj.get("@type", "")
        types = ([t] if isinstance(t, str) else t) if t else []
        if any(x in RESTAURANT_TYPES for x in types):
            if "containedInPlace" not in obj:
                obj["containedInPlace"] = CONTAINED_IN
                changed = True
            if "nearbyAttraction" not in obj:
                obj["nearbyAttraction"] = nearby
                changed = True
        for v in obj.values():
            if add_geo(v, nearby):
                changed = True
    elif isinstance(obj, list):
        for v in obj:
            if add_geo(v, nearby):
                changed = True
    return changed


def process(path, nearby):
    html = path.read_text(encoding="utf-8")
    page_changed = False

    def replace(m):
        nonlocal page_changed
        try:
            obj = json.loads(m.group(2).strip())
        except Exception:
            return m.group(0)
        if add_geo(obj, nearby):
            page_changed = True
            return m.group(1) + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + m.group(3)
        return m.group(0)

    new_html = SCRIPT_RE.sub(replace, html)
    if page_changed:
        path.write_text(new_html, encoding="utf-8")
    return page_changed


def has_restaurant(html):
    for m in SCRIPT_RE.finditer(html):
        try:
            obj = json.loads(m.group(2).strip())
        except Exception:
            continue
        def walk(o):
            if isinstance(o, dict):
                t = o.get("@type", "")
                ts = ([t] if isinstance(t, str) else t) if t else []
                if any(x in RESTAURANT_TYPES for x in ts):
                    return True
                return any(walk(v) for v in o.values())
            if isinstance(o, list):
                return any(walk(v) for v in o)
            return False
        if walk(obj):
            return True
    return False


def has_geo(html):
    return '"containedInPlace"' in html and '"nearbyAttraction"' in html


def main():
    pages = sorted(ROOT.glob("**/*.html"))
    fixed = []
    for path in pages:
        rel = str(path.relative_to(ROOT))
        if any(s in rel for s in ("node_modules", "_site", ".git")):
            continue
        if path.name in SKIP:
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        if has_geo(html) or not has_restaurant(html):
            continue
        nearby = nearby_for(rel)
        if process(path, nearby):
            fixed.append(rel)
            print("  fixed: " + rel)

    print(f"\nTotal: {len(fixed)} pages updated")


if __name__ == "__main__":
    main()
