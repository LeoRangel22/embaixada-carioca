#!/usr/bin/env python3
"""
Corrige caminhos de imagem relativos quebrados nas páginas en/ e es/
Substitui 'assets/...' por '../assets/...' onde necessário
"""
import os
import re
from bs4 import BeautifulSoup

fixed_total = 0

for lang in ['en', 'es']:
    for fname in os.listdir(lang):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(lang, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        fixed = 0
        
        # Substituir src="assets/... por src="../assets/...
        # Mas NÃO substituir /assets/... ou ../assets/... ou http...
        def fix_src(m):
            global fixed
            prefix = m.group(1)  # src= ou srcset= etc
            quote = m.group(2)   # " ou '
            path = m.group(3)    # assets/...
            fixed += 1
            return f'{prefix}{quote}../assets/{path[7:]}'
        
        # Corrigir src="assets/
        new_content = re.sub(
            r'(src=)(["\'])(assets/)',
            lambda m: f'{m.group(1)}{m.group(2)}../assets/',
            content
        )
        
        # Corrigir srcset="assets/ e srcset='assets/
        new_content = re.sub(
            r'(srcset=)(["\'])(assets/)',
            lambda m: f'{m.group(1)}{m.group(2)}../assets/',
            new_content
        )
        
        # Contar substituições
        count = content.count('src="assets/') + content.count("src='assets/") + \
                content.count('srcset="assets/') + content.count("srcset='assets/")
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  CORRIGIDO {fpath}: {count} substituições")
            fixed_total += count
        else:
            print(f"  OK {fpath}: sem imagens relativas quebradas")

print(f"\nTotal de substituições: {fixed_total}")
