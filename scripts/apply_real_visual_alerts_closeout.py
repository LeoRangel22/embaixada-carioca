#!/usr/bin/env python3
"""Close the 17 real visual warnings from the master audit.

The change is deliberately scoped to the reported pages. It adds a shared,
accessible visual layer, restores complete navigation on standalone pages and
replaces generic lunch-room photos with real food photography.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "real_visual_alerts_closeout_2026-08-23.md"
CSS_LINK = '<link href="/assets/css/ec-visual-alerts-closeout.css?v=20260823" rel="stylesheet"/>'

CLOSEOUT_START = "<!-- EC Real Visual Alerts Closeout -->"
CLOSEOUT_END = "<!-- /EC Real Visual Alerts Closeout -->"
CLOSEOUT_RE = re.compile(
    r"\n*<!-- EC Real Visual Alerts Closeout -->[\s\S]*?<!-- /EC Real Visual Alerts Closeout -->\s*",
    re.I,
)
CLOSEOUT_BLOCK = f'''{CLOSEOUT_START}
<style id="ec-visual-readability-reality-fix">
/* EC AAA Closeout Design Lock — final, scoped contrast layer. */
:root{{--ec-vr-blue:#00405a;--ec-vr-green:#335d4a;--ec-vr-yellow:#f59b1e;--ec-vr-paper:#f6efde;--ec-vr-gray:#485156;}}
html body.ec-aaa-visual-page main *{{-webkit-text-fill-color:currentColor!important;}}
html body.ec-aaa-visual-page{{font-family:Catamaran,Verdana,system-ui,sans-serif!important;}}
html body.ec-aaa-visual-page main :is(.card,.answer,.ficha,.format,.qa,.menu-item,.gallery figure,details){{color:var(--ec-vr-gray)!important;}}
html body.ec-aaa-visual-page main :is(.card,.answer,.ficha,.format,.qa,.menu-item,.gallery figure,details) :is(h1,h2,h3,h4,strong,summary){{color:var(--ec-vr-blue)!important;}}
html body.ec-aaa-visual-page main :is(.dark,.contact) :is(p,li,span,small,.lede){{color:rgba(246,239,222,.90)!important;}}
html body.ec-aaa-visual-page main :is(.light-section,.paper-section,.section-paper,.bg-paper,.gallery-section,.ec-lunch-gallery) :is(p,li,span,small,figcaption){{color:var(--ec-vr-gray)!important;}}
html body.ec-aaa-visual-page main #ec-lunch-light-content{{background:var(--ec-vr-paper)!important;color:var(--ec-vr-gray)!important;}}
html body.ec-aaa-visual-page main #ec-lunch-light-content :is(h1,h2,h3,h4,h5,h6){{color:var(--ec-vr-blue)!important;-webkit-text-fill-color:var(--ec-vr-blue)!important;}}
html body.ec-aaa-visual-page main #ec-lunch-light-content :is(p,li,span,small,strong){{color:var(--ec-vr-gray)!important;-webkit-text-fill-color:var(--ec-vr-gray)!important;}}
html body.ec-aaa-visual-page main a.btn[href*="tagme"],html body.ec-aaa-visual-page main a.btn[href*="reserv"],html body.ec-aaa-visual-page nav.top a.ec-nav-cta{{background:var(--ec-vr-yellow)!important;border-color:var(--ec-vr-yellow)!important;color:var(--ec-vr-blue)!important;}}
</style>
{CLOSEOUT_END}'''

HOME_FONT_BLOCK = '''<!-- EC Home Typography Fallback -->
<style id="ec-home-typography-fallback">html body{font-family:Catamaran,Verdana,system-ui,sans-serif}</style>
<!-- /EC Home Typography Fallback -->'''

LANG = {
    "pt": {
        "home": "/", "breakfast": "/cafe-da-manha.html", "lunch": "/almoco.html",
        "access": "/como-chegar.html", "events": "/eventos.html", "menu": "/cardapio.html",
        "labels": ("Café da Manhã", "Almoço", "Como Chegar", "Eventos", "Cardápio"),
        "reserve": "Reservar", "reviews": "mais de 8 mil avaliações", "aria": "Navegação principal",
        "skip": "Pular para o conteúdo principal",
    },
    "en": {
        "home": "/en/", "breakfast": "/en/cafe-da-manha.html", "lunch": "/en/almoco.html",
        "access": "/en/como-chegar.html", "events": "/en/eventos.html", "menu": "/en/cardapio.html",
        "labels": ("Breakfast", "Lunch", "How to Get There", "Events", "Menu"),
        "reserve": "Book", "reviews": "8K+ reviews", "aria": "Main navigation",
        "skip": "Skip to main content",
    },
    "es": {
        "home": "/es/", "breakfast": "/es/cafe-da-manha.html", "lunch": "/es/almoco.html",
        "access": "/es/como-chegar.html", "events": "/es/eventos.html", "menu": "/es/cardapio.html",
        "labels": ("Desayuno", "Almuerzo", "Cómo Llegar", "Eventos", "Menú"),
        "reserve": "Reservar", "reviews": "más de 8 mil reseñas", "aria": "Navegación principal",
        "skip": "Saltar al contenido principal",
    },
}

REVIEW_PAGES = {
    "avaliacoes-embaixada-carioca.html": "pt",
    "en/reviews-embaixada-carioca.html": "en",
    "es/resenas-embaixada-carioca.html": "es",
}
EVENT_PAGES = {
    "eventos-corporativos.html": "pt",
    "en/eventos-corporativos.html": "en",
    "es/eventos-corporativos.html": "es",
}
CONTRAST_PAGES = (
    "feijoada.html", "en/feijoada.html", "es/feijoada.html",
    "restaurante-com-vista-rio-de-janeiro.html",
    "en/restaurante-com-vista-rio-de-janeiro.html",
    "es/restaurante-com-vista-rio-de-janeiro.html",
)
LUNCH_PAGES = {
    "almoco-morro-da-urca.html": {
        "title": "Pratos reais do almoço",
        "captions": (
            "Almoço completo para compartilhar, com pratos e acompanhamentos da casa.",
            "Bobó de camarão — especialidade brasileira servida no almoço.",
            "Salmão ao molho de maracujá com o Pão de Açúcar em primeiro plano.",
        ),
    },
    "en/almoco-morro-da-urca.html": {
        "title": "Real lunch dishes",
        "captions": (
            "Complete lunch to share, with house dishes and sides.",
            "Brazilian shrimp bobó — a lunchtime house speciality.",
            "Salmon with passion-fruit sauce and a front-facing Sugarloaf view.",
        ),
    },
    "es/almoco-morro-da-urca.html": {
        "title": "Platos reales del almuerzo",
        "captions": (
            "Almuerzo completo para compartir, con platos y acompañamientos de la casa.",
            "Bobó de camarones — especialidad brasileña servida en el almuerzo.",
            "Salmón con salsa de maracuyá y vista frontal al Pan de Azúcar.",
        ),
    },
}

DETAILS: list[dict[str, object]] = []


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel: str, text: str, original: str) -> None:
    changed = text != original
    if changed:
        (ROOT / rel).write_text(text, encoding="utf-8")
    DETAILS.append({"page": rel, "changed": changed})


def add_body_classes(text: str, *classes: str) -> str:
    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        current = re.search(r'class="([^"]*)"', tag, re.I)
        values = current.group(1).split() if current else []
        for name in classes:
            if name not in values:
                values.append(name)
        if current:
            return tag[: current.start()] + f'class="{" ".join(values)}"' + tag[current.end() :]
        return tag[:-1] + f' class="{" ".join(values)}">'
    return re.sub(r"<body\b[^>]*>", repl, text, count=1, flags=re.I)


def ensure_head_link(text: str) -> str:
    if "ec-visual-alerts-closeout.css" in text:
        return text
    return re.sub(r"</head>", CSS_LINK + "\n</head>", text, count=1, flags=re.I)


def ensure_closeout(text: str) -> str:
    text = CLOSEOUT_RE.sub("\n", text)
    return re.sub(r"</body>", CLOSEOUT_BLOCK + "\n</body>", text, count=1, flags=re.I)


def lang_switcher(current: str, urls: tuple[str, str, str]) -> str:
    return f'''<details class="ec-lang-switcher">
<summary aria-label="Language"><span class="lang-current">{current.upper()}</span></summary>
<div class="ec-lang-menu"><a href="{urls[0]}">Português</a><a href="{urls[1]}">English</a><a href="{urls[2]}">Español</a></div>
</details>'''


def canonical_nav(lang: str, urls: tuple[str, str, str], quote_href: str | None = None) -> str:
    d = LANG[lang]
    labels = d["labels"]
    cta_text = ({"pt": "Solicitar orçamento", "en": "Request a quote", "es": "Solicitar presupuesto"}[lang]
                if quote_href else d["reserve"])
    cta_href = quote_href or "https://go.tagme.com.br/embaixadacarioca"
    return f'''<a class="ec-skip-link" href="#conteudo-principal">{d["skip"]}</a>
<nav aria-label="{d["aria"]}" class="top ec-aaa-top">
<div class="nav ec-aaa-nav">
<a class="brand" href="{d["home"]}"><img alt="Embaixada Carioca" decoding="async" fetchpriority="high" src="/assets/logo-areia.svg"/><span>Embaixada<br/>Carioca.</span></a>
<div class="links"><a href="{d["breakfast"]}">{labels[0]}</a><a href="{d["lunch"]}">{labels[1]}</a><a href="{d["access"]}">{labels[2]}</a><a href="{d["events"]}">{labels[3]}</a><a href="{d["menu"]}">{labels[4]}</a></div>
<a class="ec-nav-rating" href="https://g.page/r/CU-tJiJIjBUcEAE/review" rel="noopener" target="_blank">Google Reviews · 4.8★<small>{d["reviews"]}</small></a>
{lang_switcher(lang, urls)}
<a class="btn ec-nav-cta" href="{cta_href}">{cta_text}</a>
</div>
</nav>'''


def process_review(rel: str, lang: str) -> None:
    original = read(rel)
    text = ensure_head_link(original)
    text = add_body_classes(text, "ec-aaa-visual-page", "ec-reviews-page")
    urls = ("/avaliacoes-embaixada-carioca.html", "/en/reviews-embaixada-carioca.html", "/es/resenas-embaixada-carioca.html")
    if "class=\"top ec-aaa-top\"" not in text:
        text = re.sub(r"(<body\b[^>]*>)", r"\1\n" + canonical_nav(lang, urls), text, count=1, flags=re.I)
    text = ensure_closeout(text)
    write(rel, text, original)


def process_standalone_feijoada() -> None:
    rel = "feijoada-morro-da-urca.html"
    original = read(rel)
    text = ensure_head_link(original)
    text = add_body_classes(text, "ec-aaa-visual-page", "ec-standalone-feijoada")
    text = re.sub(r"<main>", '<main id="conteudo-principal">', text, count=1, flags=re.I)
    urls = ("/feijoada-morro-da-urca.html", "/en/feijoada.html", "/es/feijoada.html")
    if "class=\"top ec-aaa-top\"" not in text:
        text = re.sub(r"(<body\b[^>]*>)", r"\1\n" + canonical_nav("pt", urls), text, count=1, flags=re.I)
    if "ec-feijoada-photo" not in text:
        photo = '''<figure class="ec-feijoada-photo"><img alt="Feijoada premiada da Embaixada Carioca com acompanhamentos, servida no Morro da Urca" decoding="async" loading="lazy" src="/assets/feijoada-drinks-vista-pao-acucar.webp"/><figcaption>Melhor Feijoada do Rio de Janeiro — Veja Rio Comer &amp; Beber 2025/2026.</figcaption></figure>'''
        text = text.replace("</div>\n<h2>Resposta direta", "</div>\n" + photo + "\n<h2>Resposta direta", 1)
    text = ensure_closeout(text)
    write(rel, text, original)


def process_event(rel: str, lang: str) -> None:
    original = read(rel)
    text = ensure_head_link(original)
    text = add_body_classes(text, "ec-aaa-visual-page", "ec-corporate-events-page")
    ids = {"pt": "conteudo-principal", "en": "main-content", "es": "contenido-principal"}
    urls = ("/eventos-corporativos.html", "/en/eventos-corporativos.html", "/es/eventos-corporativos.html")
    quote = {"pt": "/eventos.html#solicitar-orcamento", "en": "/en/eventos.html#cotacao", "es": "/es/eventos.html#cotacao"}[lang]
    nav = canonical_nav(lang, urls, quote)
    text = re.sub(r"<!-- HEADER -->[\s\S]*?</header>\s*<!-- HERO -->", "<!-- HEADER -->\n" + nav + "\n<!-- HERO -->", text, count=1, flags=re.I)
    text = re.sub(r'<section class="hero">', f'<section class="hero" id="{ids[lang]}">', text, count=1)
    text = ensure_closeout(text)
    write(rel, text, original)


def process_contrast_page(rel: str) -> None:
    original = read(rel)
    text = add_body_classes(original, "ec-aaa-visual-page", "ec-existing-layout")
    if rel.startswith(("en/", "es/")):
        # Nested language pages must resolve shared images from the site root.
        text = text.replace('src="assets/', 'src="/assets/')
        text = text.replace("url('assets/", "url('/assets/")
    text = ensure_closeout(text)
    write(rel, text, original)


def lunch_gallery(title: str, captions: tuple[str, str, str]) -> str:
    assets = (
        ("/assets/fabio-almoco-mesa-completa.webp", captions[0]),
        ("/assets/bobo-camarao-real.webp", captions[1]),
        ("/assets/fabio-almoco-salmao-pao-acucar.webp", captions[2]),
    )
    figures = "".join(
        f'<figure><img alt="{caption}" decoding="async" loading="lazy" src="{src}"/><figcaption>{caption}</figcaption></figure>'
        for src, caption in assets
    )
    return f'<section class="ec-lunch-gallery"><div class="wrap"><h2>{title}</h2><div class="ec-lunch-gallery-grid">{figures}</div></div></section>'


def process_lunch(rel: str, data: dict[str, object]) -> None:
    original = read(rel)
    text = ensure_head_link(original)
    text = add_body_classes(text, "ec-aaa-visual-page", "ec-existing-layout")
    text = text.replace('<section style="padding: 4rem 0; background: var(--areia-pale);">', '<section class="ec-lunch-light-content" id="ec-lunch-light-content" style="padding: 4rem 0; background: var(--areia-pale);">', 1)
    text = text.replace('<section class="ec-lunch-light-content" style="padding: 4rem 0; background: var(--areia-pale);">', '<section class="ec-lunch-light-content" id="ec-lunch-light-content" style="padding: 4rem 0; background: var(--areia-pale);">', 1)
    pattern = re.compile(
        r'<section style="padding: 3rem 0; background: var\(--areia-pale\);">\s*'
        r'<div class="wrap" style="max-width: 900px; margin: 0 auto;">\s*'
        r'<h2[^>]*>(?:Fotos do Restaurante|Restaurant Photos|Fotos del Restaurante)</h2>[\s\S]*?</section>',
        re.I,
    )
    text, count = pattern.subn(lunch_gallery(str(data["title"]), data["captions"]), text, count=1)
    if count != 1 and "ec-lunch-gallery" not in text:
        raise RuntimeError(f"Lunch gallery not found in {rel}")
    text = ensure_closeout(text)
    write(rel, text, original)


def process_home() -> None:
    rel = "index.html"
    original = read(rel)
    text = re.sub(r"\n*<!-- EC Home Typography Fallback -->[\s\S]*?<!-- /EC Home Typography Fallback -->\s*", "\n", original)
    text = re.sub(r"</body>", HOME_FONT_BLOCK + "\n</body>", text, count=1, flags=re.I)
    write(rel, text, original)


def write_report() -> None:
    changed = sum(1 for item in DETAILS if item["changed"])
    lines = [
        "# Fechamento dos 17 alertas visuais reais",
        "",
        "Data: 2026-08-23",
        "",
        "## Escopo",
        "",
        "- Página autônoma da feijoada: navegação, imagem real, hierarquia, tipografia, CTAs e contraste.",
        "- Avaliações PT/EN/ES: topo completo, idiomas, Google Reviews, logo, botões e contraste.",
        "- Eventos corporativos PT/EN/ES: topo canônico com CTA de orçamento, idiomas e responsividade.",
        "- Feijoada e restaurante com vista PT/EN/ES: fechamento de contraste em cards claros.",
        "- Almoço Morro da Urca PT/EN/ES: galeria substituída por três fotos reais de pratos.",
        "- Home: fallback tipográfico explícito e consistente.",
        "",
        "## Guardrails",
        "",
        "- JSON-LD não alterado.",
        "- Nenhum Review, Rating ou AggregateRating adicionado.",
        "- Canonical e hreflang preservados.",
        "- Nenhuma alegação comercial nova adicionada.",
        "",
        "## Resultado da aplicação",
        "",
        f"- Páginas processadas: **{len(DETAILS)}**",
        f"- Páginas alteradas: **{changed}**",
        "",
        "| Página | Alterada |",
        "|---|---:|",
    ]
    lines.extend(f'| `{item["page"]}` | {"Sim" if item["changed"] else "Não"} |' for item in DETAILS)
    lines.extend(["", "A validação final deve ser registrada após a auditoria mestre e o teste visual responsivo.", ""])
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    for rel, lang in REVIEW_PAGES.items():
        process_review(rel, lang)
    process_standalone_feijoada()
    for rel, lang in EVENT_PAGES.items():
        process_event(rel, lang)
    for rel in CONTRAST_PAGES:
        process_contrast_page(rel)
    for rel, data in LUNCH_PAGES.items():
        process_lunch(rel, data)
    process_home()
    write_report()
    print(REPORT.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
