#!/usr/bin/env python3
"""
Correção em lote de overflow e flex-wrap problemáticos.

Problemas a corrigir:
1. overflow:hidden nos botões (.hero-ctas a, .btn, etc.) nas subpáginas HTML
   → Trocar por overflow:visible
2. flex-wrap:nowrap no hero-ctas dentro de @media (max-width:720px) no en/index.html e es/index.html
   → Trocar por flex-wrap:wrap
3. overflow:hidden em .btn,.momento-cta dentro de @media (hover:none) (ripple effect)
   → Manter (é intencional para o ripple, mas apenas em touch devices)
   → Porém o bloco ec-final-design-consistency-lock já sobrescreve com overflow:visible
   → Deixar como está (a cascata resolve)
"""

import re
from pathlib import Path

ROOT = Path("/home/ubuntu/embaixada-carioca")

changes = []

# ─── FIX 1: overflow:hidden → overflow:visible nos botões das subpáginas ──────
# Arquivos afetados: almoco.html, cafe-da-manha.html, cardapio.html, en/index.html, es/index.html

SUBPAGES = [
    'almoco.html',
    'cafe-da-manha.html',
    'cardapio.html',
    'en/index.html',
    'es/index.html',
]

# Padrão exato do bloco problemático nos botões
BTN_OVERFLOW_PATTERN = re.compile(
    r'(\.hero-ctas a,\.hero-ctas button,\.ctas a,\.ctas button,\.btn,a\.btn,button\.btn[^{]*\{[^}]*?)'
    r'overflow:hidden(!important)?'
    r'([^}]*\})',
    re.DOTALL
)

for fname in SUBPAGES:
    fpath = ROOT / fname
    if not fpath.exists():
        print(f'SKIP (não existe): {fname}')
        continue
    
    content = fpath.read_text(encoding='utf-8')
    original = content
    
    # Substituir overflow:hidden por overflow:visible nos botões
    def replace_btn_overflow(m):
        important = m.group(2) or ''
        return m.group(1) + 'overflow:visible' + important + m.group(3)
    
    content_new = BTN_OVERFLOW_PATTERN.sub(replace_btn_overflow, content)
    
    if content_new != content:
        fpath.write_text(content_new, encoding='utf-8')
        changes.append(f'FIX1: {fname} — overflow:hidden→visible nos botões')
        print(f'✓ FIX1: {fname} — overflow:hidden→visible nos botões')
    else:
        print(f'  OK (sem alteração): {fname} — botões')

# ─── FIX 2: flex-wrap:nowrap → flex-wrap:wrap no hero-ctas em @media max-width:720px ─
# Arquivos afetados: en/index.html, es/index.html
# O padrão é: @media (max-width:720px){.hero-ctas{flex-wrap:nowrap;gap:10px}

FLEX_NOWRAP_720 = re.compile(
    r'(@media\s*\([^)]*max-width\s*:\s*720px[^)]*\)\s*\{[^}]*?\.hero-ctas\s*\{[^}]*?)'
    r'flex-wrap\s*:\s*nowrap'
    r'([^}]*\})',
    re.DOTALL
)

for fname in ['en/index.html', 'es/index.html']:
    fpath = ROOT / fname
    if not fpath.exists():
        continue
    
    content = fpath.read_text(encoding='utf-8')
    original = content
    
    # Substituir flex-wrap:nowrap por flex-wrap:wrap no hero-ctas dentro de @media max-width:720px
    content_new = FLEX_NOWRAP_720.sub(r'\1flex-wrap:wrap\2', content)
    
    if content_new != content:
        fpath.write_text(content_new, encoding='utf-8')
        changes.append(f'FIX2: {fname} — flex-wrap:nowrap→wrap no hero-ctas @720px')
        print(f'✓ FIX2: {fname} — flex-wrap:nowrap→wrap no hero-ctas @720px')
    else:
        # Tentar padrão mais simples
        simple = re.compile(r'(\.hero-ctas\{[^}]*?)flex-wrap:nowrap([^}]*\})')
        content_new2 = simple.sub(r'\1flex-wrap:wrap\2', content)
        if content_new2 != content:
            fpath.write_text(content_new2, encoding='utf-8')
            changes.append(f'FIX2b: {fname} — flex-wrap:nowrap→wrap no hero-ctas (simples)')
            print(f'✓ FIX2b: {fname} — flex-wrap:nowrap→wrap no hero-ctas (simples)')
        else:
            print(f'  OK (sem alteração): {fname} — flex-wrap')

# ─── FIX 3: .nav-links overflow:hidden no como-chegar.html ───────────────────
# O .nav-links tem overflow:hidden que pode truncar os links de navegação

fpath = ROOT / 'como-chegar.html'
if fpath.exists():
    content = fpath.read_text(encoding='utf-8')
    # Buscar .nav-links com overflow:hidden
    pattern = re.compile(r'(\.nav-links\s*\{[^}]*?)overflow\s*:\s*hidden([^}]*\})')
    content_new = pattern.sub(r'\1overflow:visible\2', content)
    if content_new != content:
        fpath.write_text(content_new, encoding='utf-8')
        changes.append('FIX3: como-chegar.html — overflow:hidden→visible no .nav-links')
        print('✓ FIX3: como-chegar.html — overflow:hidden→visible no .nav-links')
    else:
        print('  OK (sem alteração): como-chegar.html — .nav-links')

# ─── FIX 4: ec-shared.css — .btn, .momento-cta overflow:hidden no ripple ─────
# Este bloco está dentro de @media (hover: none) and (pointer: coarse)
# É intencional para o ripple effect em dispositivos touch
# O bloco ec-final-design-consistency-lock já sobrescreve com overflow:visible
# MAS o ripple effect está dentro de @media (hover:none), que é mais específico
# e pode sobrescrever o ec-final em touch devices
# Solução: remover o overflow:hidden do ripple effect (o ripple não precisa de overflow:hidden
# para funcionar — ele precisa de position:relative, que já está lá)

with open(ROOT / 'assets/css/ec-shared.css') as f:
    content = f.read()

# Padrão: dentro de @media (hover: none) and (pointer: coarse), .btn, .momento-cta com overflow:hidden
# Substituir overflow:hidden por overflow:visible no ripple
RIPPLE_PATTERN = re.compile(
    r'(/\*\s*Ripple effect[^*]*\*/\s*\.btn,\s*\.momento-cta\s*\{[^}]*?)'
    r'overflow\s*:\s*hidden\s*!important'
    r'([^}]*\})',
    re.DOTALL
)

content_new = RIPPLE_PATTERN.sub(r'\1overflow:visible !important\2', content)
if content_new != content:
    (ROOT / 'assets/css/ec-shared.css').write_text(content_new, encoding='utf-8')
    changes.append('FIX4: ec-shared.css — overflow:hidden→visible no ripple effect (.btn, .momento-cta)')
    print('✓ FIX4: ec-shared.css — overflow:hidden→visible no ripple effect')
else:
    print('  OK (sem alteração): ec-shared.css — ripple effect')

# ─── Resumo ────────────────────────────────────────────────────────────────────
print(f'\n=== {len(changes)} correções aplicadas ===')
for c in changes:
    print(f'  • {c}')
