#!/usr/bin/env python3
"""
fix_nav_v3.py
Correções:
1. Hamburguer: background-color: #F5EDD6 → transparent (o botão não deve ter fundo areia,
   apenas as barrinhas <span> devem ser claras)
2. Bottom nav: remover o item "Reservar" (bnav-reservar) de todos os arquivos
"""
import os
import re
import glob

# ─── PATCH 1: Corrigir o CSS do hamburguer ────────────────────────────────────
# O bloco atual (inserido pelo fix_mobile_colors.py) é:
#   .nav-hamburger,
#   .nav-hamburger span,
#   .nav-hamburger::before,
#   .nav-hamburger::after {
#     color: #F5EDD6 !important;
#     background-color: #F5EDD6 !important;  ← isso pinta o BOTÃO de areia
#     border-color: #F5EDD6 !important;
#   }
#
# Correto: o botão (.nav-hamburger) deve ter background transparent.
# Apenas as barrinhas (.nav-hamburger span) devem ter background #F5EDD6.

OLD_HAM_CSS = """\
  /* Hamburguer: cor clara */
  .nav-hamburger,
  .nav-hamburger span,
  .nav-hamburger::before,
  .nav-hamburger::after {
    color: #F5EDD6 !important;
    background-color: #F5EDD6 !important;
    border-color: #F5EDD6 !important;
  }"""

NEW_HAM_CSS = """\
  /* Hamburguer: botão transparente, barrinhas claras */
  .nav-hamburger {
    color: #F5EDD6 !important;
    background-color: transparent !important;
    border-color: transparent !important;
  }
  .nav-hamburger span,
  .nav-hamburger::before,
  .nav-hamburger::after {
    background-color: #F5EDD6 !important;
    border-color: #F5EDD6 !important;
  }"""

# ─── PATCH 2: Remover item Reservar do bottom nav ────────────────────────────
# Padrão HTML do item a remover (pode variar ligeiramente entre páginas):
# <a href="https://go.tagme.com.br/embaixadacarioca" class="bnav-reservar" ...>...</a>
# Também pode aparecer como href diferente mas com class="bnav-reservar"

BNAV_RESERVAR_PATTERN = re.compile(
    r'\s*<a[^>]+class="bnav-reservar"[^>]*>.*?</a>',
    re.DOTALL
)

# ─── Coletar todos os arquivos HTML ──────────────────────────────────────────
html_files = (
    glob.glob('*.html') +
    glob.glob('en/*.html') +
    glob.glob('es/*.html')
)
html_files = [f for f in html_files if not f.startswith('_')]

ok_ham = 0
ok_bnav = 0
skip = 0

for path in sorted(html_files):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # PATCH 1: corrigir hamburguer CSS
    if OLD_HAM_CSS in content:
        content = content.replace(OLD_HAM_CSS, NEW_HAM_CSS, 1)
        ok_ham += 1
        changed = True

    # PATCH 2: remover bnav-reservar
    new_content, n = BNAV_RESERVAR_PATTERN.subn('', content)
    if n > 0:
        content = new_content
        ok_bnav += 1
        changed = True

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {path} (ham={'fix' if OLD_HAM_CSS in open(path).read() == False else 'ok'}, bnav={n} removidos)")
    else:
        skip += 1

print(f"\nResultado: {ok_ham} hamburguer corrigidos | {ok_bnav} bnav-reservar removidos | {skip} sem alteração")
