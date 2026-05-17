#!/usr/bin/env python3
"""
fix_bnav_color.py
Solução definitiva para fonte preta no bottom nav das subpáginas.

Estratégia: Adicionar um <style> tag IMEDIATAMENTE ANTES do </body>
com as regras do bottom nav usando especificidade máxima (body .mobile-bottom-nav a)
e !important. Isso garante que seja a última regra CSS aplicada e vença qualquer
outra regra anterior.
"""
import glob
import re

# CSS a injetar antes de </body>
BNAV_FINAL_CSS = """
<style id="bnav-color-fix">
/* ── BOTTOM NAV: cor final garantida ─────────────────────────────────── */
body .mobile-bottom-nav { background: #00405A !important; }
body .mobile-bottom-nav a { color: rgba(245,237,214,0.82) !important; }
body .mobile-bottom-nav .bnav-icon { color: rgba(245,237,214,0.82) !important; }
body .mobile-bottom-nav a.bnav-reservar,
body .mobile-bottom-nav .bnav-reservar { background: #E8C547 !important; color: #00405A !important; }
body .mobile-bottom-nav a.bnav-reservar .bnav-icon,
body .mobile-bottom-nav .bnav-reservar .bnav-icon { color: #00405A !important; }
</style>"""

html_files = (
    glob.glob('*.html') +
    glob.glob('en/*.html') +
    glob.glob('es/*.html')
)
html_files = [f for f in html_files if not f.startswith('_')]

ok = 0
skip = 0

for path in sorted(html_files):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Não duplicar
    if 'bnav-color-fix' in content:
        skip += 1
        continue

    # Inserir antes de </body>
    if '</body>' in content:
        content = content.replace('</body>', BNAV_FINAL_CSS + '\n</body>', 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        ok += 1
        print(f"  ✅ {path}")
    else:
        skip += 1

print(f"\nResultado: {ok} arquivos corrigidos | {skip} ignorados")
