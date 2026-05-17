#!/usr/bin/env python3
"""
fix_mobile_nav.py
Corrige o fundo branco/bege do nav mobile nas páginas internas.
PROBLEMA: nav.top.scrolled tem background branco/areia no mobile
SOLUÇÃO: No mobile (max-width: 720px), forçar fundo escuro no nav (scrolled ou não)
"""
import os
import glob
import re

FIX_CSS = """
/* ── MOBILE NAV FIX: fundo escuro no mobile (scrolled ou não) ── */
@media (max-width: 720px) {
  /* No mobile, o nav sempre tem fundo escuro (independente do scroll) */
  nav.top,
  nav.top.scrolled {
    background: rgba(0, 20, 30, 0.88) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-bottom-color: rgba(255,255,255,0.08) !important;
  }
  nav.top .nav-inner,
  nav.top.scrolled .nav-inner {
    color: var(--areia-pale, #F5EDD6) !important;
  }
  nav.top .nav-links a,
  nav.top.scrolled .nav-links a,
  nav.top .lang-current,
  nav.top.scrolled .lang-current,
  nav.top .lang-current span,
  nav.top.scrolled .lang-current span {
    color: var(--areia-pale, #F5EDD6) !important;
  }
  nav.top .brand-logo.light,
  nav.top.scrolled .brand-logo.light {
    display: block !important;
  }
  nav.top .brand-logo.dark,
  nav.top.scrolled .brand-logo.dark {
    display: none !important;
  }
  /* Badge de avaliações no mobile: cor clara */
  nav.top .nav-rating-badge,
  nav.top.scrolled .nav-rating-badge {
    color: var(--areia-pale, #F5EDD6) !important;
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.25) !important;
  }
  /* Seletor de idioma no mobile: cor clara */
  nav.top .lang-current,
  nav.top.scrolled .lang-current {
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.25) !important;
  }
}
"""

# Encontrar todos os arquivos HTML (exceto index.html)
html_files = []
for pattern in ['*.html', 'en/*.html', 'es/*.html']:
    html_files.extend(glob.glob(pattern))

# Excluir index.html (home) — a home já tem comportamento correto
html_files = [f for f in html_files if f not in ('index.html', 'en/index.html', 'es/index.html')]

print(f"Total de arquivos: {len(html_files)}")

fixed = 0
skipped = 0
errors = []

for filepath in sorted(html_files):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pular se já foi corrigido
        if 'MOBILE NAV FIX' in content:
            skipped += 1
            continue
        
        # Estratégia 1: Adicionar o fix no bloco nav-standard-css (antes do </style>)
        if '<style id="nav-standard-css">' in content:
            # Encontrar o fechamento do bloco nav-standard-css
            idx = content.find('<style id="nav-standard-css">')
            end_idx = content.find('</style>', idx)
            if end_idx != -1:
                # Inserir o fix antes do </style>
                new_content = content[:end_idx] + FIX_CSS + content[end_idx:]
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                fixed += 1
                print(f"  ✅ {filepath} (via nav-standard-css)")
                continue
        
        # Estratégia 2: Adicionar antes do </head>
        if '</head>' in content:
            fix_block = f'<style id="mobile-nav-fix">{FIX_CSS}</style>\n'
            new_content = content.replace('</head>', fix_block + '</head>', 1)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed += 1
            print(f"  ✅ {filepath} (via </head>)")
            continue
        
        print(f"  ⚠️ {filepath} — não encontrou ponto de inserção")
        errors.append(filepath)
        
    except Exception as e:
        print(f"  ❌ {filepath}: {e}")
        errors.append(filepath)

print(f"\nResultado: {fixed} corrigidos, {skipped} já OK, {len(errors)} erros")
if errors:
    print("Erros:", errors)
