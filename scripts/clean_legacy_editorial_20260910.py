"""Targeted editorial cleanup; no schema, prices, menu items or metadata rewriting."""
from pathlib import Path
import re
from html import escape

ROOT = Path(__file__).resolve().parents[1]
COPY = {
    '': ('Café da manhã em imagens', 'Uma mesa de café da manhã e a vista que acompanha a visita.',
         'Mesa de café da manhã com pães, frutas, frios e bebidas quentes', 'Sabores para começar o dia.',
         'Visitante com xícara e o Pão de Açúcar ao fundo', 'Uma pausa com o Pão de Açúcar em primeiro plano.', 'Planeje sua visita'),
    'en/': ('Breakfast in pictures', 'A breakfast spread and the view that makes the visit special.',
            'Breakfast table with bread, fruit, cold cuts and hot drinks', 'A delicious start to the day.',
            'Visitor holding a cup with Sugarloaf Mountain in the background', 'A pause with Sugarloaf Mountain in full view.', 'Plan your visit'),
    'es/': ('El desayuno en imágenes', 'Una mesa de desayuno y la vista que acompaña la visita.',
            'Mesa de desayuno con panes, frutas, fiambres y bebidas calientes', 'Sabores para empezar el día.',
            'Visitante con una taza y el Pan de Azúcar al fondo', 'Una pausa con el Pan de Azúcar en primer plano.', 'Planifica tu visita'),
}
TARGET_CLASSES = {'avaliacoes', 'gallery-section', 'ec-featured-snippet-ol', 'ec-sprint2-geo', 'ec-sprint4-faq',
                  'links-relacionados', 'seo-conversion-block', 'ec-menu-complete', 'ec-aio-low-score-fix'}
REMOVE_IDS = {'ec-fase4-cafe', 'cafe-embaixada-carioca', 'ec-semantic-anchor', 'gsc-cafe-da-manha-urca-pao'}
def schema(text):
    return re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>[\s\S]*?</script>', text)

for prefix, copy in COPY.items():
    for name in ('cafe-da-manha', 'cardapio', 'guia-do-rio'):
        path = ROOT / (prefix + name + '.html')
        text = path.read_text(encoding='utf-8')
        original = schema(text)
        if name == 'cardapio':
            # This second choosing-guide repeats the retained four-step guide.
            text, count = re.subn(r'<section\b[^>]*class="ec-aio-low-score-fix[^>]*>[\s\S]*?</section>', '', text)
            if count:
                assert original == schema(text)
                path.write_text(text, encoding='utf-8')
                print(prefix + name, 'repeated choosing-guide removed:', count)
        removed = 0
        def section(match):
            global removed
            block = match.group()
            tag = re.match(r'<section\b[^>]*>', block).group()
            ident = re.search(r'\bid="([^"]+)"', tag)
            classes = re.search(r'\bclass="([^"]*)"', tag)
            tokens = set(classes.group(1).split()) if classes else set()
            if name == 'cafe-da-manha' and ident and ident.group(1) in REMOVE_IDS:
                removed += 1
                # Keep incoming fragment links usable without retaining duplicate copy.
                return '<span id="' + ident.group(1) + '" class="ec-retired-anchor" aria-hidden="true"></span>'
            if name == 'cafe-da-manha' and 'gallery-section' in tokens:
                figures = []
                for asset, alt, caption in [
                    ('cafe-da-embaixada-mesa-completa.webp', copy[2], copy[3]),
                    ('cafe-espresso-pao-acucar.webp', copy[4], copy[5]),
                ]:
                    figures.append(f'<figure><img src="/assets/cafe/{asset}" alt="{escape(alt, quote=True)}" width="1280" height="853" loading="lazy" decoding="async"/><figcaption>{escape(caption)}</figcaption></figure>')
                block = '<section class="gallery-section ec-breakfast-gallery"><div class="ec-reading-wrap"><h2>' + copy[0] + '</h2><p>' + copy[1] + '</p><div class="ec-breakfast-photo-grid">' + ''.join(figures) + '</div></div></section>'
                tag = re.match(r'<section\b[^>]*>', block).group()
                classes = re.search(r'\bclass="([^"]*)"', tag)
            if tokens & TARGET_CLASSES or (ident and ident.group(1) == 'faq-cafe-da-manha'):
                if classes:
                    newclasses = list(dict.fromkeys(classes.group(1).split() + ['light-section', 'ec-reading-section']))
                    newtag = tag.replace(classes.group(), 'class="' + ' '.join(newclasses) + '"')
                else:
                    newtag = tag[:-1] + ' class="light-section ec-reading-section">'
                block = newtag + block[len(tag):]
            block = re.sub(r'(<div class="ec-kicker">)(?:Resposta direta · SEO \+ GEO|Direct answer · SEO \+ GEO|Respuesta directa · SEO \+ GEO)(</div>)', lambda m: m.group(1) + copy[6] + m.group(2), block)
            return block
        text = re.sub(r'<section\b[^>]*>[\s\S]*?</section>', section, text)
        if 'data-ec-legacy-clean="20260910"' not in text:
            text = text.replace('<body ', '<body id="ec-editorial-page" data-ec-legacy-clean="20260910" ', 1)
        if 'ec-legacy-reading.css?v=20260910a' not in text:
            text = text.replace('</head>', '<link rel="stylesheet" href="/assets/css/ec-legacy-reading.css?v=20260910a"/>\n</head>', 1)
        assert original == schema(text), path
        path.write_text(text, encoding='utf-8')
        print(prefix + name, 'duplicate sections removed:', removed)
