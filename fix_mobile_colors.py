#!/usr/bin/env python3
"""
fix_mobile_colors.py
Corrige as cores do menu inferior (mobile-bottom-nav) e do nav superior mobile.

PROBLEMA:
1. Bottom nav: fundo e texto aparecem em preto no celular
2. Nav superior: links e seletor de idioma aparecem em preto no celular

SOLUÇÃO:
- Substituir o bloco MOBILE NAV FIX existente por uma versão mais robusta
- Usar cores hardcoded (não variáveis CSS) com !important
- Adicionar color-scheme: dark para evitar interferência do dark mode do sistema
- Cobrir todos os seletores necessários para bottom nav e nav superior
"""
import os
import glob
import re

# CSS de fix ATUALIZADO — mais robusto, cobre bottom nav e nav superior
# Usa cores hardcoded para evitar problemas com variáveis CSS não resolvidas
# e !important para garantir precedência sobre qualquer outra regra

NEW_FIX_CSS = """
/* ── MOBILE NAV FIX v2: cores corretas no mobile (nav superior + bottom nav) ── */
@media (max-width: 720px) {
  /* ── NAV SUPERIOR: fundo escuro + texto claro ── */
  nav.top,
  nav.top.scrolled {
    background: rgba(0, 20, 30, 0.92) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-bottom-color: rgba(255,255,255,0.08) !important;
    color-scheme: dark !important;
  }
  /* Todos os textos dentro do nav superior: cor clara */
  nav.top *,
  nav.top.scrolled * {
    color: #F5EDD6 !important;
  }
  /* Exceção: botão RESERVAR mantém cor escura no texto */
  nav.top .btn,
  nav.top.scrolled .btn,
  nav.top .btn-reservar,
  nav.top.scrolled .btn-reservar {
    color: #00405A !important;
    background: #E8C547 !important;
    border-color: #E8C547 !important;
  }
  /* Seletor de idioma: fundo semitransparente claro */
  nav.top .lang-current,
  nav.top.scrolled .lang-current {
    background: rgba(255,255,255,0.15) !important;
    border-color: rgba(255,255,255,0.3) !important;
    color: #F5EDD6 !important;
  }
  /* Logo: mostrar versão clara */
  nav.top .brand-logo.light,
  nav.top.scrolled .brand-logo.light {
    display: block !important;
  }
  nav.top .brand-logo.dark,
  nav.top.scrolled .brand-logo.dark {
    display: none !important;
  }
  /* Hamburguer: cor clara */
  .nav-hamburger,
  .nav-hamburger span,
  .nav-hamburger::before,
  .nav-hamburger::after {
    color: #F5EDD6 !important;
    background-color: #F5EDD6 !important;
    border-color: #F5EDD6 !important;
  }

  /* ── BOTTOM NAV: fundo azul escuro + texto claro ── */
  .mobile-bottom-nav {
    background: #00405A !important;
    border-top-color: rgba(255,255,255,0.15) !important;
    color-scheme: dark !important;
  }
  .mobile-bottom-nav a {
    color: rgba(245, 237, 214, 0.75) !important;
    background: transparent !important;
  }
  .mobile-bottom-nav a:hover,
  .mobile-bottom-nav a:active,
  .mobile-bottom-nav a:focus {
    color: #E8C547 !important;
    background: rgba(255,255,255,0.06) !important;
  }
  .mobile-bottom-nav .bnav-icon {
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
  }
  .mobile-bottom-nav .bnav-reservar:hover,
  .mobile-bottom-nav .bnav-reservar:active {
    background: #d4b03a !important;
    color: #00405A !important;
  }
}
"""

# Encontrar todos os arquivos HTML
html_files = []
for pattern in ['*.html', 'en/*.html', 'es/*.html']:
    html_files.extend(glob.glob(pattern))

print(f"Total de arquivos: {len(html_files)}")

updated = 0
new_fix = 0
errors = []

for filepath in sorted(html_files):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Estratégia 1: Substituir o bloco MOBILE NAV FIX existente
        if 'MOBILE NAV FIX' in content:
            # Encontrar o início e fim do bloco fix
            fix_start = content.find('/* ── MOBILE NAV FIX')
            if fix_start == -1:
                fix_start = content.find('MOBILE NAV FIX')
                # Recuar para encontrar o início do comentário
                fix_start = content.rfind('/*', 0, fix_start)
            
            # Encontrar o fim do bloco @media que contém o fix
            # O fix termina com "}\n" após o último "}"
            media_start = content.find('@media (max-width: 720px)', fix_start)
            if media_start != -1:
                # Encontrar o fechamento do @media
                depth = 0
                i = media_start
                while i < len(content):
                    if content[i] == '{':
                        depth += 1
                    elif content[i] == '}':
                        depth -= 1
                        if depth == 0:
                            fix_end = i + 1
                            break
                    i += 1
                
                # Substituir o bloco fix
                old_fix = content[fix_start:fix_end]
                new_content = content[:fix_start] + NEW_FIX_CSS.strip() + content[fix_end:]
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated += 1
                print(f"  ✅ {filepath} (fix atualizado)")
                continue

        # Estratégia 2: Adicionar o fix no bloco nav-standard-css
        if '<style id="nav-standard-css">' in content:
            idx = content.find('<style id="nav-standard-css">')
            end_idx = content.find('</style>', idx)
            if end_idx != -1:
                new_content = content[:end_idx] + '\n' + NEW_FIX_CSS + content[end_idx:]
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                new_fix += 1
                print(f"  ✅ {filepath} (fix adicionado)")
                continue

        # Estratégia 3: Adicionar antes do </head>
        if '</head>' in content:
            fix_block = f'<style id="mobile-nav-fix">{NEW_FIX_CSS}</style>\n'
            new_content = content.replace('</head>', fix_block + '</head>', 1)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            new_fix += 1
            print(f"  ✅ {filepath} (fix adicionado via head)")
            continue

        print(f"  ⚠️ {filepath} — não encontrou ponto de inserção")
        errors.append(filepath)

    except Exception as e:
        print(f"  ❌ {filepath}: {e}")
        errors.append(filepath)

print(f"\nResultado: {updated} atualizados, {new_fix} novos, {len(errors)} erros")
if errors:
    print("Erros:", errors)
