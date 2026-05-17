#!/usr/bin/env python3
"""
1. Atualiza src/srcset das imagens problemáticas nos HTMLs para usar WebP responsivo
2. Cria _headers para cache longo no GitHub Pages (Cloudflare Pages / Netlify)
3. Cria .htaccess para cache longo (Apache)
"""
import os, glob, re
from bs4 import BeautifulSoup

DEPLOY = '/home/ubuntu/embaixada-deploy'

# ── 1. Atualizar imagens nos HTMLs ───────────────────────────────────────────
html_files = glob.glob(f'{DEPLOY}/**/*.html', recursive=True)
html_files += glob.glob(f'{DEPLOY}/*.html')
html_files = list(set(html_files))

# Substituições a fazer:
# A) fabio-almoco-salmao-pao-acucar.jpg → WebP com srcset
# B) hero.jpg → hero.webp com srcset (nas páginas que ainda usam hero.jpg)

changes = {
    # src antigo → (novo src, srcset, sizes)
    'assets/fabio-almoco-salmao-pao-acucar.jpg': (
        'assets/fabio-almoco-salmao-pao-acucar.webp',
        'assets/fabio-almoco-salmao-pao-acucar-400w.webp 400w, assets/fabio-almoco-salmao-pao-acucar-800w.webp 800w, assets/fabio-almoco-salmao-pao-acucar.webp 900w',
        '(max-width: 480px) 400px, (max-width: 900px) 800px, 900px'
    ),
}

total_changes = 0
for html_path in sorted(html_files):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Substituição A: fabio-almoco-salmao-pao-acucar.jpg → WebP responsivo
    if 'fabio-almoco-salmao-pao-acucar.jpg' in content:
        # Substituir src e adicionar srcset
        content = content.replace(
            'src="assets/fabio-almoco-salmao-pao-acucar.jpg"',
            'src="assets/fabio-almoco-salmao-pao-acucar.webp" '
            'srcset="assets/fabio-almoco-salmao-pao-acucar-400w.webp 400w, '
            'assets/fabio-almoco-salmao-pao-acucar-800w.webp 800w, '
            'assets/fabio-almoco-salmao-pao-acucar.webp 900w" '
            'sizes="(max-width: 480px) 400px, (max-width: 900px) 800px, 900px"'
        )
        # Também versão com caminho relativo (subpáginas en/ es/)
        content = content.replace(
            'src="../assets/fabio-almoco-salmao-pao-acucar.jpg"',
            'src="../assets/fabio-almoco-salmao-pao-acucar.webp" '
            'srcset="../assets/fabio-almoco-salmao-pao-acucar-400w.webp 400w, '
            '../assets/fabio-almoco-salmao-pao-acucar-800w.webp 800w, '
            '../assets/fabio-almoco-salmao-pao-acucar.webp 900w" '
            'sizes="(max-width: 480px) 400px, (max-width: 900px) 800px, 900px"'
        )
    
    if content != original:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        total_changes += 1
        print(f"  ✅ {os.path.relpath(html_path, DEPLOY)}")

print(f"\n  Total de arquivos atualizados: {total_changes}")

# ── 2. Criar _headers para Cloudflare Pages / Netlify ────────────────────────
# GitHub Pages não suporta _headers, mas é bom ter para futuras migrações
headers_content = """/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.webp
  Cache-Control: public, max-age=31536000, immutable

/*.jpg
  Cache-Control: public, max-age=31536000, immutable

/*.png
  Cache-Control: public, max-age=31536000, immutable

/*.svg
  Cache-Control: public, max-age=31536000, immutable

/*.woff2
  Cache-Control: public, max-age=31536000, immutable

/*.css
  Cache-Control: public, max-age=86400

/*.js
  Cache-Control: public, max-age=86400

/*.html
  Cache-Control: public, max-age=300, must-revalidate
"""

with open(f'{DEPLOY}/_headers', 'w') as f:
    f.write(headers_content)
print(f"\n✅ _headers criado")

# ── 3. Criar .htaccess para Apache (caso o site migre para servidor próprio) ──
htaccess_content = """# Cache de longa duração para assets estáticos
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType text/css "access plus 1 day"
  ExpiresByType application/javascript "access plus 1 day"
  ExpiresByType text/html "access plus 5 minutes"
</IfModule>

<IfModule mod_headers.c>
  <FilesMatch "\\.(webp|jpg|jpeg|png|svg|woff2)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
  <FilesMatch "\\.(css|js)$">
    Header set Cache-Control "public, max-age=86400"
  </FilesMatch>
</IfModule>

# Compressão gzip
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript
</IfModule>
"""

with open(f'{DEPLOY}/.htaccess', 'w') as f:
    f.write(htaccess_content)
print(f"✅ .htaccess criado")

# ── 4. Verificar resultado ────────────────────────────────────────────────────
print("\n=== Verificação final ===")
with open(f'{DEPLOY}/almoco.html', 'r', encoding='utf-8') as f:
    content = f.read()

if 'fabio-almoco-salmao-pao-acucar.webp' in content and 'srcset' in content:
    print("✅ almoco.html: srcset WebP aplicado")
else:
    print("❌ almoco.html: srcset NÃO aplicado")
