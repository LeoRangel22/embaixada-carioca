#!/usr/bin/env python3
"""Add missing og:image and og:url to all pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.embaixadacarioca.com"

# Page-specific og:image mapping (path fragment → image URL)
IMAGE_MAP = [
    ("almoco-morro-da-urca",   BASE + "/assets/fabio-almoco-salmao-pao-acucar.jpg"),
    ("almoco",                 BASE + "/assets/terraco-cheio-almoco.jpg"),
    ("cafe-da-manha-pao-de-acucar", BASE + "/assets/cafe-manha-pao-acucar-frente.jpg"),
    ("cafe-da-manha-com-vista", BASE + "/assets/cafe-manha-vista-pao-acucar.jpg"),
    ("cafe-da-manha",          BASE + "/assets/cafe-da-manha-mesa-opt.jpg"),
    ("breakfast",              BASE + "/assets/cafe-da-manha-mesa-opt.jpg"),
    ("desayuno",               BASE + "/assets/cafe-da-manha-mesa-opt.jpg"),
    ("feijoada",               BASE + "/assets/feijoada-completa-acompanhamentos.jpg"),
    ("eventos",                BASE + "/assets/evento-chandon-opt.jpg"),
    ("event",                  BASE + "/assets/evento-chandon-opt.jpg"),
    ("entardecer",             BASE + "/assets/entardecer-banda-opt.jpg"),
    ("sunset",                 BASE + "/assets/entardecer-banda-opt.jpg"),
    ("atardecer",              BASE + "/assets/entardecer-banda-opt.jpg"),
    ("romantico",              BASE + "/assets/casal-romantico-opt.jpg"),
    ("romantic",               BASE + "/assets/casal-romantico-opt.jpg"),
    ("caipirinha",             BASE + "/assets/cocktails-vista.jpg"),
    ("cardapio",               BASE + "/assets/prato-principal-vista-pao-acucar.jpg"),
    ("restaurante-morro",      BASE + "/assets/hero.jpg"),
    ("restaurant-at-urca",     BASE + "/assets/hero.jpg"),
    ("morro-da-urca",          BASE + "/assets/hero.jpg"),
    ("urca-hill",              BASE + "/assets/hero.jpg"),
    ("sugarloaf",              BASE + "/assets/pao-acucar-bondinho-entardecer.jpg"),
    ("parque-bondinho",        BASE + "/assets/pao-acucar-bondinho-entardecer.jpg"),
    ("pan-de-azucar",          BASE + "/assets/pao-acucar-bondinho-entardecer.jpg"),
    ("onde-comer",             BASE + "/assets/fabio-almoco-picanha-fritas.jpg"),
    ("where-to-eat",           BASE + "/assets/fabio-almoco-picanha-fritas.jpg"),
    ("donde-comer",            BASE + "/assets/fabio-almoco-picanha-fritas.jpg"),
    ("restaurantes-perto",     BASE + "/assets/fabio-almoco-picanha-fritas.jpg"),
    ("restaurants-near",       BASE + "/assets/fabio-almoco-picanha-fritas.jpg"),
    ("restaurantes-cerca",     BASE + "/assets/fabio-almoco-picanha-fritas.jpg"),
    ("guia-do-rio",            BASE + "/assets/pao-acucar-dois-bondinhos.jpg"),
    ("gastronomia",            BASE + "/assets/fabio-chef-wallace-sorrindo.jpg"),
    ("nossa-visao",            BASE + "/assets/equipe-embaixada-carioca.jpg"),
    ("roteiro",                BASE + "/assets/pao-acucar-dois-bondinhos.jpg"),
    ("contato",                BASE + "/assets/hero.jpg"),
    ("como-chegar",            BASE + "/assets/hero.jpg"),
    ("how-to-get",             BASE + "/assets/hero.jpg"),
    ("como-llegar",            BASE + "/assets/hero.jpg"),
]
DEFAULT_IMAGE = BASE + "/assets/hero.jpg"

OG_URL_RE = re.compile(r'<meta[^>]+property=["\']og:url["\'][^>]+/?>', re.I)
OG_IMG_RE = re.compile(r'<meta[^>]+property=["\']og:image["\'][^>]+/?>', re.I)
CANONICAL_RE = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\'][^>]*/?>', re.I)
HEAD_CLOSE_RE = re.compile(r'</head>', re.I)

SKIP = {"404.html", "offline.html", "home-preview.html", "index.html.bak"}


def pick_image(rel):
    rel_lower = rel.lower().replace("\\", "/")
    for fragment, url in IMAGE_MAP:
        if fragment in rel_lower:
            return url
    return DEFAULT_IMAGE


def get_canonical(html):
    m = CANONICAL_RE.search(html)
    return m.group(1) if m else None


def rel_to_url(rel):
    rel = rel.replace("\\", "/")
    if rel == "index.html":
        return BASE + "/"
    if rel.endswith("/index.html"):
        return BASE + "/" + rel[:-len("index.html")]
    return BASE + "/" + rel


def inject_before_head_close(html, tags_html):
    return HEAD_CLOSE_RE.sub(tags_html + "\n</head>", html, count=1)


def process(path):
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    if path.name in SKIP:
        return False

    html = path.read_text(encoding="utf-8")
    original = html
    additions = []

    has_og_url = bool(OG_URL_RE.search(html))
    has_og_img = bool(OG_IMG_RE.search(html))

    if has_og_url and has_og_img:
        return False

    inject = ""

    if not has_og_url:
        canon = get_canonical(html) or rel_to_url(rel)
        inject += f'\n<meta property="og:url" content="{canon}">'
        additions.append("og:url")

    if not has_og_img:
        img = pick_image(rel)
        inject += f'\n<meta property="og:image" content="{img}">'
        inject += f'\n<meta property="og:image:width" content="1200">'
        inject += f'\n<meta property="og:image:height" content="630">'
        inject += f'\n<meta property="og:image:type" content="image/jpeg">'
        additions.append("og:image")

    if inject and "</head>" in html:
        html = inject_before_head_close(html, inject)

    if html != original:
        path.write_text(html, encoding="utf-8")
        print("  " + rel + ": " + ", ".join(additions))
        return True
    return False


def main():
    pages = sorted(ROOT.glob("**/*.html"))
    count = 0
    for path in pages:
        if any(s in str(path) for s in ("node_modules", "_site", ".git")):
            continue
        if process(path):
            count += 1
    print(f"\nTotal: {count} pages updated")


if __name__ == "__main__":
    main()
