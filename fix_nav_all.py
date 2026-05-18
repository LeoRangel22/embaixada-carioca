#!/usr/bin/env python3
"""
Corrige o nav de todas as subpáginas PT, EN e ES para ficar idêntico à home.
Problemas encontrados:
1. CTA ausente (todas as subpáginas)
2. Badge ausente (páginas de momento)
3. Seletor de idioma ausente (páginas de momento)
4. page-hero-photo ausente (gastronomia, morro-da-urca, parque-bondinho)
5. hero-eyebrow ausente (feijoada, gastronomia, morro-da-urca, parque-bondinho, roteiro, o-que-fazer)
"""
import re
from pathlib import Path
from bs4 import BeautifulSoup

# ============================================================
# NAV TEMPLATES POR IDIOMA
# ============================================================

NAV_PT = '''<nav class="top" id="topnav">
<div class="nav-inner">
<a aria-label="Embaixada Carioca · início" class="brand-mark" href="/">
<img alt="Embaixada Carioca — Restaurante com Vista para o Pão de Açúcar, Morro da Urca, Rio de Janeiro" class="brand-logo light" loading="eager" src="{prefix}assets/logo-areia.svg"/>
<img alt="Embaixada Carioca · Restaurante no Morro da Urca, Rio de Janeiro" class="brand-logo dark" loading="eager" src="{prefix}assets/logo-azul.svg"/>
</a>
<ul class="nav-links">
<li><a href="{prefix}cafe-da-manha.html">Café da Manhã</a></li>
<li><a href="{prefix}almoco.html">Almoço</a></li>
<li><a href="{prefix}entardecer.html">Entardecer</a></li>
<li><a href="{prefix}eventos.html">Eventos</a></li>
<li><a href="{prefix}cardapio.html">Cardápio</a></li>
<li><a href="{prefix}guia-do-rio.html">Guia do Rio</a></li>
</ul>
<a aria-label="WhatsApp Embaixada Carioca" class="nav-wa-btn" href="https://wa.me/5521966837556?text=Ol%C3%A1%21%20Vim%20pelo%20site%20da%20Embaixada%20Carioca%20e%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es." rel="noopener" target="_blank" title="WhatsApp · +55 21 96683-7556">
<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M17.779 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.779-.767.779-.94 1.164-.173.199-.347.779-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.779-.52.149-.174.198-.298.298-.497.779-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.779.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.779h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"></path></svg>
</a>
<a aria-label="4.8 estrelas · mais de 7.779 avaliações no Google" class="nav-rating-badge" href="https://www.google.com/maps/place/Embaixada+Carioca" rel="noopener" target="_blank" title="Ver avaliações no Google"><span class="nav-rating-stars">4.8★</span><span class="nav-rating-count">7.779 avaliações</span></a>
<div aria-label="Selecionar idioma" class="lang-switcher" role="navigation">
<button aria-expanded="false" aria-haspopup="true" aria-label="Idioma atual: PT" class="lang-current">
<span class="lang-flag">🇧🇷</span>
<span>PT</span>
<span class="lang-arrow">▼</span>
</button>
<div class="lang-dropdown" role="menu">
<a class="active" href="{prefix}" hreflang="pt-BR" role="menuitem">
<span class="lang-flag">🇧🇷</span>
<span class="lang-name">Português</span> <span class="lang-check">✓</span>
</a>
<a class="" href="{prefix_en}{page_en}" hreflang="en" role="menuitem">
<span class="lang-flag">🇺🇸</span>
<span class="lang-name">English</span>
</a>
<a class="" href="{prefix_es}{page_es}" hreflang="es" role="menuitem">
<span class="lang-flag">🇪🇸</span>
<span class="lang-name">Español</span>
</a>
</div>
</div>
<button aria-controls="nav-drawer" aria-expanded="false" aria-label="Abrir menu de navegação" class="nav-hamburger" id="nav-hamburger">
<span></span><span></span><span></span>
</button>
<a class="btn" href="https://go.tagme.com.br/embaixadacarioca">Reservar →</a>
</div>
</nav>'''

NAV_EN = '''<nav class="top" id="topnav">
<div class="nav-inner">
<a aria-label="Embaixada Carioca · home" class="brand-mark" href="/en/">
<img alt="Embaixada Carioca — Restaurant with View of Sugarloaf Mountain, Morro da Urca, Rio de Janeiro" class="brand-logo light" loading="eager" src="{prefix}assets/logo-areia.svg"/>
<img alt="Embaixada Carioca · Restaurant at Morro da Urca, Rio de Janeiro" class="brand-logo dark" loading="eager" src="{prefix}assets/logo-azul.svg"/>
</a>
<ul class="nav-links">
<li><a href="{prefix}cafe-da-manha.html">Breakfast</a></li>
<li><a href="{prefix}almoco.html">Lunch</a></li>
<li><a href="{prefix}entardecer.html">Sunset</a></li>
<li><a href="{prefix}eventos.html">Events</a></li>
<li><a href="{prefix}cardapio.html">Menu</a></li>
<li><a href="{prefix}guia-do-rio.html">Rio Guide</a></li>
</ul>
<a aria-label="WhatsApp Embaixada Carioca" class="nav-wa-btn" href="https://wa.me/5521966837556?text=Hello%21%20I%20found%20you%20on%20the%20Embaixada%20Carioca%20website%20and%20would%20like%20more%20information." rel="noopener" target="_blank" title="WhatsApp · +55 21 96683-7556">
<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M17.779 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.779-.767.779-.94 1.164-.173.199-.347.779-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.779-.52.149-.174.198-.298.298-.497.779-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.779.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.779h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"></path></svg>
</a>
<a aria-label="4.8 stars · over 7,779 Google reviews" class="nav-rating-badge" href="https://www.google.com/maps/place/Embaixada+Carioca" rel="noopener" target="_blank" title="See reviews on Google"><span class="nav-rating-stars">4.8★</span><span class="nav-rating-count">7,779 reviews</span></a>
<div aria-label="Select language" class="lang-switcher" role="navigation">
<button aria-expanded="false" aria-haspopup="true" aria-label="Current language: EN" class="lang-current">
<span class="lang-flag">🇺🇸</span>
<span>EN</span>
<span class="lang-arrow">▼</span>
</button>
<div class="lang-dropdown" role="menu">
<a class="" href="{prefix_pt}{page_pt}" hreflang="pt-BR" role="menuitem">
<span class="lang-flag">🇧🇷</span>
<span class="lang-name">Português</span>
</a>
<a class="active" href="{prefix}" hreflang="en" role="menuitem">
<span class="lang-flag">🇺🇸</span>
<span class="lang-name">English</span> <span class="lang-check">✓</span>
</a>
<a class="" href="{prefix_es}{page_es}" hreflang="es" role="menuitem">
<span class="lang-flag">🇪🇸</span>
<span class="lang-name">Español</span>
</a>
</div>
</div>
<button aria-controls="nav-drawer" aria-expanded="false" aria-label="Open navigation menu" class="nav-hamburger" id="nav-hamburger">
<span></span><span></span><span></span>
</button>
<a class="btn" href="https://go.tagme.com.br/embaixadacarioca">Book →</a>
</div>
</nav>'''

NAV_ES = '''<nav class="top" id="topnav">
<div class="nav-inner">
<a aria-label="Embaixada Carioca · inicio" class="brand-mark" href="/es/">
<img alt="Embaixada Carioca — Restaurante con Vista al Pan de Azúcar, Morro da Urca, Río de Janeiro" class="brand-logo light" loading="eager" src="{prefix}assets/logo-areia.svg"/>
<img alt="Embaixada Carioca · Restaurante en el Morro da Urca, Río de Janeiro" class="brand-logo dark" loading="eager" src="{prefix}assets/logo-azul.svg"/>
</a>
<ul class="nav-links">
<li><a href="{prefix}cafe-da-manha.html">Desayuno</a></li>
<li><a href="{prefix}almoco.html">Almuerzo</a></li>
<li><a href="{prefix}entardecer.html">Atardecer</a></li>
<li><a href="{prefix}eventos.html">Eventos</a></li>
<li><a href="{prefix}cardapio.html">Menú</a></li>
<li><a href="{prefix}guia-do-rio.html">Guía de Río</a></li>
</ul>
<a aria-label="WhatsApp Embaixada Carioca" class="nav-wa-btn" href="https://wa.me/5521966837556?text=Hola%21%20Encontr%C3%A9%20el%20sitio%20de%20Embaixada%20Carioca%20y%20me%20gustar%C3%ADa%20m%C3%A1s%20informaci%C3%B3n." rel="noopener" target="_blank" title="WhatsApp · +55 21 96683-7556">
<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M17.779 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.779-.767.779-.94 1.164-.173.199-.347.779-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.779-.52.149-.174.198-.298.298-.497.779-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.779.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.779h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"></path></svg>
</a>
<a aria-label="4.8 estrellas · más de 7.779 reseñas en Google" class="nav-rating-badge" href="https://www.google.com/maps/place/Embaixada+Carioca" rel="noopener" target="_blank" title="Ver reseñas en Google"><span class="nav-rating-stars">4.8★</span><span class="nav-rating-count">7.779 reseñas</span></a>
<div aria-label="Seleccionar idioma" class="lang-switcher" role="navigation">
<button aria-expanded="false" aria-haspopup="true" aria-label="Idioma actual: ES" class="lang-current">
<span class="lang-flag">🇪🇸</span>
<span>ES</span>
<span class="lang-arrow">▼</span>
</button>
<div class="lang-dropdown" role="menu">
<a class="" href="{prefix_pt}{page_pt}" hreflang="pt-BR" role="menuitem">
<span class="lang-flag">🇧🇷</span>
<span class="lang-name">Português</span>
</a>
<a class="" href="{prefix_en}{page_en}" hreflang="en" role="menuitem">
<span class="lang-flag">🇺🇸</span>
<span class="lang-name">English</span>
</a>
<a class="active" href="{prefix}" hreflang="es" role="menuitem">
<span class="lang-flag">🇪🇸</span>
<span class="lang-name">Español</span> <span class="lang-check">✓</span>
</a>
</div>
</div>
<button aria-controls="nav-drawer" aria-expanded="false" aria-label="Abrir menú de navegación" class="nav-hamburger" id="nav-hamburger">
<span></span><span></span><span></span>
</button>
<a class="btn" href="https://go.tagme.com.br/embaixadacarioca">Reservar →</a>
</div>
</nav>'''

# ============================================================
# MAPEAMENTO DE PÁGINAS
# ============================================================
# Páginas PT → EN/ES equivalentes
PAGE_MAP = {
    'almoco.html': ('almoco.html', 'almoco.html'),
    'almoco-morro-da-urca.html': ('almoco-morro-da-urca.html', 'almoco-morro-da-urca.html'),
    'cafe-da-manha.html': ('cafe-da-manha.html', 'cafe-da-manha.html'),
    'cafe-da-manha-pao-de-acucar.html': ('cafe-da-manha-pao-de-acucar.html', 'cafe-da-manha-pao-de-acucar.html'),
    'caipirinha-com-vista-rio.html': ('caipirinha-com-vista-rio.html', 'caipirinha-com-vista-rio.html'),
    'cardapio.html': ('cardapio.html', 'cardapio.html'),
    'entardecer.html': ('entardecer.html', 'entardecer.html'),
    'eventos.html': ('eventos.html', 'eventos.html'),
    'feijoada.html': ('feijoada.html', 'feijoada.html'),
    'feijoada-com-vista-rio-de-janeiro.html': ('feijoada-com-vista-rio-de-janeiro.html', 'feijoada-com-vista-rio-de-janeiro.html'),
    'gastronomia-carioca.html': ('gastronomia-carioca.html', 'gastronomia-carioca.html'),
    'guia-do-rio.html': ('guia-do-rio.html', 'guia-do-rio.html'),
    'morro-da-urca.html': ('morro-da-urca.html', 'morro-da-urca.html'),
    'o-que-fazer-depois-do-bondinho-pao-de-acucar.html': ('o-que-fazer-depois-do-bondinho-pao-de-acucar.html', 'o-que-fazer-depois-do-bondinho-pao-de-acucar.html'),
    'parque-bondinho.html': ('parque-bondinho.html', 'parque-bondinho.html'),
    'por-do-sol-morro-da-urca.html': ('por-do-sol-morro-da-urca.html', 'por-do-sol-morro-da-urca.html'),
    'roteiro-meio-dia-urca-pao-de-acucar.html': ('roteiro-meio-dia-urca-pao-de-acucar.html', 'roteiro-meio-dia-urca-pao-de-acucar.html'),
}

# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================
def fix_nav(filepath, nav_template, prefix, prefix_pt, prefix_en, prefix_es, page_pt, page_en, page_es):
    content = filepath.read_text(encoding='utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    
    nav = soup.find('nav', class_='top')
    if not nav:
        print(f"  ⚠️  {filepath.name}: nav.top não encontrado, pulando")
        return False
    
    # Gerar novo nav
    new_nav_html = nav_template.format(
        prefix=prefix,
        prefix_pt=prefix_pt,
        prefix_en=prefix_en,
        prefix_es=prefix_es,
        page_pt=page_pt,
        page_en=page_en,
        page_es=page_es
    )
    
    # Substituir nav no HTML
    nav_str = str(nav)
    new_content = content.replace(nav_str, new_nav_html, 1)
    
    if new_content == content:
        # Tentar substituição por regex
        new_content = re.sub(r'<nav class="top"[^>]*>.*?</nav>', new_nav_html, content, count=1, flags=re.DOTALL)
    
    if new_content != content:
        filepath.write_text(new_content, encoding='utf-8')
        return True
    else:
        print(f"  ⚠️  {filepath.name}: substituição falhou")
        return False

# ============================================================
# PROCESSAR PÁGINAS PT
# ============================================================
print("=== CORRIGINDO PÁGINAS PT ===")
fixed_pt = 0
for page_pt, (page_en, page_es) in PAGE_MAP.items():
    fp = Path(page_pt)
    if not fp.exists():
        print(f"  ⚠️  {page_pt}: não encontrado")
        continue
    nav_html = NAV_PT.format(
        prefix='',
        prefix_en='en/',
        prefix_es='es/',
        page_pt=page_pt,
        page_en=page_en,
        page_es=page_es
    )
    content = fp.read_text(encoding='utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    nav = soup.find('nav', class_='top')
    if nav:
        new_content = content.replace(str(nav), nav_html, 1)
        if new_content != content:
            fp.write_text(new_content, encoding='utf-8')
            print(f"  ✅ {page_pt}")
            fixed_pt += 1
        else:
            print(f"  ⚠️  {page_pt}: substituição falhou (str)")
    else:
        print(f"  ⚠️  {page_pt}: nav não encontrado")

# ============================================================
# PROCESSAR PÁGINAS EN
# ============================================================
print(f"\n=== CORRIGINDO PÁGINAS EN ===")
fixed_en = 0
for page_pt, (page_en, page_es) in PAGE_MAP.items():
    fp = Path(f'en/{page_en}')
    if not fp.exists():
        print(f"  ⚠️  en/{page_en}: não encontrado")
        continue
    nav_html = NAV_EN.format(
        prefix='../',
        prefix_pt='../',
        prefix_en='',
        prefix_es='../es/',
        page_pt=page_pt,
        page_en=page_en,
        page_es=page_es
    )
    content = fp.read_text(encoding='utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    nav = soup.find('nav', class_='top')
    if nav:
        new_content = content.replace(str(nav), nav_html, 1)
        if new_content != content:
            fp.write_text(new_content, encoding='utf-8')
            print(f"  ✅ en/{page_en}")
            fixed_en += 1
        else:
            print(f"  ⚠️  en/{page_en}: substituição falhou")
    else:
        print(f"  ⚠️  en/{page_en}: nav não encontrado")

# ============================================================
# PROCESSAR PÁGINAS ES
# ============================================================
print(f"\n=== CORRIGINDO PÁGINAS ES ===")
fixed_es = 0
for page_pt, (page_en, page_es) in PAGE_MAP.items():
    fp = Path(f'es/{page_es}')
    if not fp.exists():
        print(f"  ⚠️  es/{page_es}: não encontrado")
        continue
    nav_html = NAV_ES.format(
        prefix='../',
        prefix_pt='../',
        prefix_en='../en/',
        prefix_es='',
        page_pt=page_pt,
        page_en=page_en,
        page_es=page_es
    )
    content = fp.read_text(encoding='utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    nav = soup.find('nav', class_='top')
    if nav:
        new_content = content.replace(str(nav), nav_html, 1)
        if new_content != content:
            fp.write_text(new_content, encoding='utf-8')
            print(f"  ✅ es/{page_es}")
            fixed_es += 1
        else:
            print(f"  ⚠️  es/{page_es}: substituição falhou")
    else:
        print(f"  ⚠️  es/{page_es}: nav não encontrado")

print(f"\n=== RESUMO ===")
print(f"PT: {fixed_pt}/{len(PAGE_MAP)} corrigidas")
print(f"EN: {fixed_en}/{len(PAGE_MAP)} corrigidas")
print(f"ES: {fixed_es}/{len(PAGE_MAP)} corrigidas")
print(f"Total: {fixed_pt + fixed_en + fixed_es} páginas")
