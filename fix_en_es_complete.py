#!/usr/bin/env python3
"""
Correção completa das páginas EN e ES:
1. Corrigir caminhos de hero-mobile.webp: assets/ -> ../assets/
2. Corrigir caminhos de hero-800w.webp: assets/ -> ../assets/ (no srcset)
3. Verificar e corrigir outros caminhos relativos de assets
"""
import os
import re

fixed_files = 0
total_fixes = 0

for lang in ['en', 'es']:
    for fname in sorted(os.listdir(lang)):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(lang, fname)
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        fixes = 0
        
        # Fix 1: srcset="assets/hero-mobile.webp -> srcset="../assets/hero-mobile.webp
        # (já foi feito para src= mas não para srcset= dentro de <source>)
        new = re.sub(
            r'(srcset=")assets/(hero-mobile\.webp)',
            r'\1../assets/\2',
            content
        )
        if new != content:
            fixes += content.count('srcset="assets/hero-mobile.webp')
            content = new
        
        # Fix 2: srcset="assets/hero-800w.webp -> srcset="../assets/hero-800w.webp
        new = re.sub(
            r'(srcset=")assets/(hero-800w\.webp)',
            r'\1../assets/\2',
            content
        )
        if new != content:
            fixes += content.count('srcset="assets/hero-800w.webp')
            content = new
        
        # Fix 3: Qualquer srcset restante com assets/ (não precedido por ../)
        # Cuidado: não substituir o que já tem ../
        new = re.sub(
            r'(?<!\.\.)(?<!/)srcset="assets/',
            'srcset="../assets/',
            content
        )
        if new != content:
            fixes += 1
            content = new
        
        # Fix 4: Verificar se há src="assets/ ainda (que não foi corrigido pelo fix_image_paths.py)
        # Apenas para tags <source> que podem ter sido perdidas
        new = re.sub(
            r'(<source[^>]*srcset=")assets/',
            r'\1../assets/',
            content
        )
        if new != content:
            fixes += 1
            content = new
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  CORRIGIDO {fpath}: {fixes} fixes")
            fixed_files += 1
            total_fixes += fixes
        else:
            print(f"  OK {fpath}")

print(f"\nTotal: {fixed_files} arquivos corrigidos, {total_fixes} substituições")
