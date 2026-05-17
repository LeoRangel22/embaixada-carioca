#!/usr/bin/env python3
"""
fix_nav_v4.py
1. Remover o botão "Reservar mesa" do geo-proximity.js (banner de distância)
2. Restaurar o item RESERVAR no bottom nav de todos os arquivos HTML
3. Restaurar o CSS do bnav-reservar no fix_mobile_colors
"""
import os
import re
import glob

# ─── PATCH 1: Remover botão Reservar do geo-proximity.js ─────────────────────
GEO_JS = 'assets/geo-proximity.js'

with open(GEO_JS, 'rb') as f:
    geo_content = f.read()

# Remover o trecho do botão Reservar no HTML gerado pelo JS
# Trecho: <a href="https://go.tagme.com.br/embaixadacarioca" ... class="ec-geo-btn ec-geo-btn-res">'+b.cta_reserve+'</a>
REMOVE_START = b'<a href="https://go.tagme.com.br/embaixadacarioca" target="_blank" rel="noopener" class="ec-geo-btn ec-geo-btn-res">'
REMOVE_END_MARKER = b"</a>"

idx_start = geo_content.find(REMOVE_START)
if idx_start > 0:
    # Encontrar o fim: '</a>' após o início
    idx_end = geo_content.find(REMOVE_END_MARKER, idx_start) + len(REMOVE_END_MARKER)
    removed = geo_content[idx_start:idx_end]
    print(f"Removendo do geo-proximity.js: {removed[:80]}...")
    geo_content = geo_content[:idx_start] + geo_content[idx_end:]
    with open(GEO_JS, 'wb') as f:
        f.write(geo_content)
    print("✅ Botão Reservar removido do geo-proximity.js")
else:
    print("⚠️  Botão Reservar já removido ou não encontrado no geo-proximity.js")

# ─── PATCH 2: Restaurar RESERVAR no bottom nav HTML ──────────────────────────
# O item a restaurar (igual ao original):
BNAV_RESERVAR_HTML = '\n    <a href="https://go.tagme.com.br/embaixadacarioca" class="bnav-reservar" aria-label="Reservar"><span class="bnav-icon">📅</span>Reservar</a>'

# Padrão para encontrar o fim do bottom nav (antes do </div></nav>)
# Inserir antes do fechamento do inner div
BNAV_INNER_END = '</div>\n</nav>\n<!-- /MOBILE BOTTOM NAV -->'
BNAV_INNER_END_ALT = '  </div>\n</nav>\n<!-- /MOBILE BOTTOM NAV -->'

# Para EN e ES, o texto do link pode ser diferente
BNAV_RESERVAR_EN = '\n    <a href="https://go.tagme.com.br/embaixadacarioca" class="bnav-reservar" aria-label="Reserve"><span class="bnav-icon">📅</span>Reserve</a>'
BNAV_RESERVAR_ES = '\n    <a href="https://go.tagme.com.br/embaixadacarioca" class="bnav-reservar" aria-label="Reservar"><span class="bnav-icon">📅</span>Reservar</a>'

# ─── PATCH 3: Restaurar CSS do bnav-reservar no bloco fix_mobile_colors ──────
# O CSS a restaurar no bloco @media (max-width: 720px) do fix_mobile_colors
BNAV_ICON_CSS_END = """  .mobile-bottom-nav .bnav-icon {
    color: rgba(245, 237, 214, 0.75) !important;
  }"""

BNAV_RESERVAR_CSS = """  .mobile-bottom-nav .bnav-icon {
    color: rgba(245, 237, 214, 0.75) !important;
  }
  /* Botão RESERVAR no bottom nav: fundo amarelo + texto azul */
  .mobile-bottom-nav .bnav-reservar,
  .mobile-bottom-nav a.bnav-reservar {
    background: #E8C547 !important;
    color: #00405A !important;
  }
  .mobile-bottom-nav .bnav-reservar .bnav-icon,
  .mobile-bottom-nav a.bnav-reservar .bnav-icon {
    color: #00405A !important;
  }"""

# ─── Processar todos os arquivos HTML ────────────────────────────────────────
html_files = (
    glob.glob('*.html') +
    glob.glob('en/*.html') +
    glob.glob('es/*.html')
)
html_files = [f for f in html_files if not f.startswith('_')]

ok_html = 0
ok_css = 0

for path in sorted(html_files):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    is_en = path.startswith('en/')
    is_es = path.startswith('es/')

    # Determinar o texto do botão conforme idioma
    if is_en:
        reservar_html = BNAV_RESERVAR_EN
    else:
        reservar_html = BNAV_RESERVAR_HTML  # PT e ES usam "Reservar"

    # PATCH 2: Restaurar item RESERVAR no bottom nav (se não existir)
    if 'bnav-reservar' not in content and '<nav class="mobile-bottom-nav"' in content:
        # Encontrar o fechamento do inner div do bottom nav
        # Padrão: o último </a> antes do </div></nav><!-- /MOBILE BOTTOM NAV -->
        # Inserir após o último </a> dentro do mobile-bottom-nav-inner
        nav_start = content.find('<nav class="mobile-bottom-nav"')
        nav_end = content.find('<!-- /MOBILE BOTTOM NAV -->', nav_start)
        if nav_start > 0 and nav_end > 0:
            nav_block = content[nav_start:nav_end]
            # Encontrar o último </a> no bloco
            last_a_end = nav_block.rfind('</a>')
            if last_a_end > 0:
                insert_pos = nav_start + last_a_end + 4  # após o </a>
                content = content[:insert_pos] + reservar_html + content[insert_pos:]
                ok_html += 1
                changed = True

    # PATCH 3: Restaurar CSS do bnav-reservar (se não existir)
    if 'bnav-reservar' not in content.split('</style>')[0] and BNAV_ICON_CSS_END in content:
        # Verificar se o CSS do bnav-reservar já existe
        if '.mobile-bottom-nav .bnav-reservar' not in content:
            content = content.replace(BNAV_ICON_CSS_END, BNAV_RESERVAR_CSS, 1)
            ok_css += 1
            changed = True

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {path}")

print(f"\nResultado: {ok_html} HTML restaurados | {ok_css} CSS restaurados")
