#!/usr/bin/env python3
"""
Atualiza o sitemap.xml:
1. Adiciona páginas faltantes
2. Atualiza lastmod das páginas otimizadas para 2026-07-23
"""
import re

TODAY = "2026-07-23"

with open('sitemap.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# ─── Páginas a adicionar (não estão no sitemap) ───────────────────────────────
new_entries = [
    # (pt_url, en_url, es_url)
    (
        "https://www.embaixadacarioca.com/feijoada-morro-da-urca.html",
        "https://www.embaixadacarioca.com/en/feijoada.html",
        "https://www.embaixadacarioca.com/es/feijoada.html",
        "0.8"
    ),
    (
        "https://www.embaixadacarioca.com/restaurante-com-vista-rio-de-janeiro.html",
        "https://www.embaixadacarioca.com/en/restaurant-at-sugarloaf.html",
        "https://www.embaixadacarioca.com/es/restaurante-com-vista-rio-de-janeiro.html",
        "0.8"
    ),
]

def build_url_entry(pt_url, en_url, es_url, priority):
    return f"""  <url>
    <loc>{pt_url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
    <xhtml:link rel="alternate" hreflang="pt-BR" href="{pt_url}" />
    <xhtml:link rel="alternate" hreflang="en" href="{en_url}" />
    <xhtml:link rel="alternate" hreflang="es" href="{es_url}" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{pt_url}" />
  </url>
  <url>
    <loc>{en_url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
    <xhtml:link rel="alternate" hreflang="pt-BR" href="{pt_url}" />
    <xhtml:link rel="alternate" hreflang="en" href="{en_url}" />
    <xhtml:link rel="alternate" hreflang="es" href="{es_url}" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{pt_url}" />
  </url>
  <url>
    <loc>{es_url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
    <xhtml:link rel="alternate" hreflang="pt-BR" href="{pt_url}" />
    <xhtml:link rel="alternate" hreflang="en" href="{en_url}" />
    <xhtml:link rel="alternate" hreflang="es" href="{es_url}" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{pt_url}" />
  </url>"""

# Adicionar entradas novas antes do </urlset>
new_xml = ""
for entry in new_entries:
    new_xml += "\n" + build_url_entry(*entry)

content = content.replace("</urlset>", new_xml + "\n</urlset>")

# ─── Atualizar lastmod das páginas otimizadas ─────────────────────────────────
pages_to_update = [
    "feijoada-morro-da-urca.html",
    "restaurante-com-vista-rio-de-janeiro.html",
    "cafe-da-manha-pao-de-acucar.html",
    "por-do-sol-morro-da-urca.html",
    "en/feijoada.html",
    "en/restaurant-at-sugarloaf.html",
    "en/cafe-da-manha-pao-de-acucar.html",
    "en/sunset.html",
    "es/feijoada.html",
    "es/restaurante-com-vista-rio-de-janeiro.html",
    "es/cafe-da-manha-pao-de-acucar.html",
    "es/atardecer.html",
    "morro-da-urca.html",
    "en/morro-da-urca.html",
    "es/morro-da-urca.html",
]

# Atualizar lastmod para cada URL
for page in pages_to_update:
    # Construir URL base
    if page.startswith('en/'):
        url = f"https://www.embaixadacarioca.com/en/{page[3:]}"
    elif page.startswith('es/'):
        url = f"https://www.embaixadacarioca.com/es/{page[3:]}"
    else:
        url = f"https://www.embaixadacarioca.com/{page}"
    
    # Substituir lastmod para esta URL
    pattern = rf'(<loc>{re.escape(url)}</loc>\s*<lastmod>)[^<]+(</lastmod>)'
    replacement = rf'\g<1>{TODAY}\g<2>'
    new_content = re.sub(pattern, replacement, content)
    if new_content != content:
        content = new_content
        print(f"✓ lastmod atualizado: {url}")
    else:
        print(f"— não encontrado no sitemap: {url}")

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ sitemap.xml atualizado com {len(new_entries)*3} novas entradas")
