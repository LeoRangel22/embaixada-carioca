#!/usr/bin/env python3
"""
Add missing internal links between cluster pages and areaServed to Restaurant schemas.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCRIPT_RE = re.compile(
    r'(<script\s[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.I | re.S
)

AREA_SERVED_PT = [
    {"@type": "City", "name": "Rio de Janeiro",
     "sameAs": "https://en.wikipedia.org/wiki/Rio_de_Janeiro"},
    {"@type": "Neighborhood", "name": "Urca, Rio de Janeiro"},
    {"@type": "AdministrativeArea", "name": "Zona Sul do Rio de Janeiro"}
]
AREA_SERVED_EN = [
    {"@type": "City", "name": "Rio de Janeiro",
     "sameAs": "https://en.wikipedia.org/wiki/Rio_de_Janeiro"},
    {"@type": "Neighborhood", "name": "Urca, Rio de Janeiro"},
    {"@type": "AdministrativeArea", "name": "South Zone of Rio de Janeiro"}
]
AREA_SERVED_ES = [
    {"@type": "City", "name": "Río de Janeiro",
     "sameAs": "https://en.wikipedia.org/wiki/Rio_de_Janeiro"},
    {"@type": "Neighborhood", "name": "Urca, Río de Janeiro"},
    {"@type": "AdministrativeArea", "name": "Zona Sur de Río de Janeiro"}
]

RESTAURANT_TYPES = {"Restaurant", "FoodEstablishment", "LocalBusiness"}

RELATED_LINK_STYLE = (
    'style="display:block;margin:1.5rem 0;padding:.9rem 1.1rem;'
    'background:#f0f7ff;border-radius:8px;border-left:4px solid #1d4ed8;'
    'color:#1d4ed8;font-weight:600;text-decoration:none;font-size:.95rem"'
)


def area_for(rel):
    if rel.startswith("en/"):
        return AREA_SERVED_EN
    if rel.startswith("es/"):
        return AREA_SERVED_ES
    return AREA_SERVED_PT


def add_area_served(obj, area):
    changed = False
    if isinstance(obj, dict):
        t = obj.get("@type", "")
        types = ([t] if isinstance(t, str) else t) if t else []
        if any(x in RESTAURANT_TYPES for x in types):
            if "areaServed" not in obj:
                obj["areaServed"] = area
                changed = True
        for v in obj.values():
            if add_area_served(v, area):
                changed = True
    elif isinstance(obj, list):
        for v in obj:
            if add_area_served(v, area):
                changed = True
    return changed


def apply_area_served(html, area):
    changed = False
    def replace(m):
        nonlocal changed
        try:
            obj = json.loads(m.group(2).strip())
        except Exception:
            return m.group(0)
        if add_area_served(obj, area):
            changed = True
            return m.group(1) + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + m.group(3)
        return m.group(0)
    return SCRIPT_RE.sub(replace, html), changed


def inject_link(html, href, text, marker):
    link = (
        f'\n<div class="related-link" style="margin:1.5rem 0;padding:.9rem 1.1rem;'
        f'background:#f0f7ff;border-radius:8px;border-left:4px solid #1d4ed8">'
        f'<a href="{href}" {RELATED_LINK_STYLE}>{text} &rarr;</a></div>\n'
    )
    if marker in html:
        return html.replace(marker, link + marker, 1), True
    return html, False


def find_marker(html, markers):
    for m in markers:
        if m in html:
            return m
    return None


# ── Internal links to add ─────────────────────────────────────────────────────

INTERNAL_LINKS = {
    "almoco.html": [
        ("/restaurante-morro-da-urca.html", "Conheça o Restaurante Morro da Urca"),
    ],
    "cafe-da-manha.html": [
        ("/cafe-da-manha-pao-de-acucar.html", "Café da Manhã no Pão de Açúcar"),
        ("/restaurante-morro-da-urca.html", "Conheça o Restaurante Morro da Urca"),
    ],
    "restaurante-morro-da-urca.html": [
        ("/almoco-morro-da-urca.html", "Almoço especial no Morro da Urca"),
    ],
    "almoco-morro-da-urca.html": [
        ("/onde-comer-no-pao-de-acucar.html", "Onde comer no Pão de Açúcar"),
        ("/restaurante-morro-da-urca.html", "Sobre o Restaurante Morro da Urca"),
    ],
    "onde-comer-no-pao-de-acucar.html": [
        ("/almoco-morro-da-urca.html", "Almoço especial no Morro da Urca"),
    ],
}

INSERTION_MARKERS = ["</article>", "</main>", "<footer", "</section>"]


def process_page(rel):
    path = ROOT / rel
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8")
    original = html
    changes = []

    # areaServed
    area = area_for(rel)
    html, ch = apply_area_served(html, area)
    if ch:
        changes.append("areaServed")

    # internal links
    links = INTERNAL_LINKS.get(rel, [])
    marker = find_marker(html, INSERTION_MARKERS)
    for href, text in links:
        slug = href.strip("/").replace(".html", "")
        if slug not in html:
            if marker:
                html, ok = inject_link(html, href, text, marker)
                if ok:
                    changes.append("link→" + slug.split("/")[-1][:20])

    if html != original:
        path.write_text(html, encoding="utf-8")
        print("  " + rel + ": " + ", ".join(changes))


def bulk_area_served():
    """Add areaServed to ALL pages not yet having it."""
    pages = sorted(ROOT.glob("**/*.html"))
    count = 0
    for path in pages:
        if any(s in str(path) for s in ("node_modules", "_site", ".git")):
            continue
        if path.name in ("404.html", "offline.html", "home-preview.html"):
            continue
        if "areaServed" in path.read_text(encoding="utf-8", errors="ignore"):
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        area = area_for(rel)
        html = path.read_text(encoding="utf-8")
        new_html, changed = apply_area_served(html, area)
        if changed:
            path.write_text(new_html, encoding="utf-8")
            count += 1
    print(f"  areaServed bulk: {count} pages updated")


def main():
    print("Adding areaServed (bulk) + internal links...")
    bulk_area_served()
    print("Adding internal links to cluster pages...")
    for rel in INTERNAL_LINKS:
        process_page(rel)
    print("Done.")


if __name__ == "__main__":
    main()
