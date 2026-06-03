#!/usr/bin/env python3
"""
fix_css_leak.py — Diagnóstico e correção de CSS vazado fora de tags <style>
===========================================================================
Varre todas as páginas HTML e detecta blocos de CSS que estão sendo
renderizados como texto visível (fora de tags <style> ou <script>).
Corrige automaticamente envolvendo o CSS em <style> ou removendo o bloco
órfão se for duplicata.

Autor: Manus AI — 03/06/2026
"""

import re
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
BACKUP_DIR = ROOT / "_backups" / "fix_css_leak"

# Padrões que indicam CSS vazado (texto CSS fora de tag <style>)
CSS_LEAK_PATTERNS = [
    r'/\*[^*]*BOTTOM\s*NAV[^*]*\*/',
    r'/\*[^*]*bottom.nav[^*]*\*/',
    r'\.mobile-bottom-nav\s*\{',
    r'\.bnav-reservar\s*\{',
    r'\.bnav-icon\s*\{',
    r'border-top-color:\s*rgba\(',
    r'color-scheme:\s*dark',
    r'/\*[^*]*Botão RESERVAR[^*]*\*/',
    r'background:\s*#00405A\s*!important',
    r'ec-fase4-css',
    r'ec-contrast-fixes',
    r'/\*[^*]*BOTTOM[^*]*\*/',
]

def backup(path: Path):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    rel = path.relative_to(ROOT)
    bp = BACKUP_DIR / rel
    bp.parent.mkdir(parents=True, exist_ok=True)
    if not bp.exists():
        shutil.copy2(path, bp)

def is_inside_tag(html: str, pos: int, tag: str) -> bool:
    """Verifica se a posição está dentro de uma tag específica."""
    last_open = html.rfind(f'<{tag}', 0, pos)
    last_close = html.rfind(f'</{tag}>', 0, pos)
    if last_open < 0:
        return False
    return last_open > last_close

def find_css_leaks(html: str) -> list:
    """Encontra todas as posições de CSS vazado fora de tags style/script."""
    leaks = []
    for pattern in CSS_LEAK_PATTERNS:
        for m in re.finditer(pattern, html, re.IGNORECASE):
            pos = m.start()
            in_style = is_inside_tag(html, pos, 'style')
            in_script = is_inside_tag(html, pos, 'script')
            in_head_comment = False
            
            # Verificar se está dentro de um comentário HTML <!-- -->
            last_comment_open = html.rfind('<!--', 0, pos)
            last_comment_close = html.rfind('-->', 0, pos)
            in_comment = last_comment_open > last_comment_close
            
            if not in_style and not in_script and not in_comment:
                leaks.append({
                    'pos': pos,
                    'pattern': pattern,
                    'snippet': html[pos:pos+100].replace('\n', ' '),
                })
    return leaks

def find_orphan_style_content(html: str) -> list:
    """
    Encontra blocos de CSS que estão fora de qualquer tag <style>.
    Procura especificamente por padrões como:
    - Comentários CSS /* ... */ fora de <style>
    - Seletores CSS .classe { } fora de <style>
    - Conteúdo que começa com /* e contém seletores CSS
    """
    orphans = []
    
    # Padrão: bloco que começa com /* e contém CSS
    # Tipicamente: /* comentário */ .seletor { propriedade: valor !important; }
    css_block_pattern = re.compile(
        r'(/\*[^*]*(?:BOTTOM|NAV|nav|bottom|mobile|bnav|fase4|contrast)[^*]*\*/\s*'
        r'(?:\.[\w-]+\s*[,{][^}]*}[\s\n]*)+)',
        re.IGNORECASE | re.DOTALL
    )
    
    for m in css_block_pattern.finditer(html):
        pos = m.start()
        in_style = is_inside_tag(html, pos, 'style')
        in_script = is_inside_tag(html, pos, 'script')
        last_comment_open = html.rfind('<!--', 0, pos)
        last_comment_close = html.rfind('-->', 0, pos)
        in_comment = last_comment_open > last_comment_close
        
        if not in_style and not in_script and not in_comment:
            orphans.append({
                'start': m.start(),
                'end': m.end(),
                'content': m.group(0)[:200],
                'full_match': m.group(0),
            })
    
    return orphans

def fix_page(path: Path) -> dict:
    """Corrige CSS vazado em uma página HTML."""
    html = path.read_text(encoding='utf-8', errors='ignore')
    original_html = html
    
    result = {
        'page': str(path.relative_to(ROOT)),
        'leaks_found': 0,
        'fixed': 0,
        'orphans': [],
        'modified': False,
    }
    
    # 1. Encontrar blocos CSS órfãos (fora de <style>)
    orphans = find_orphan_style_content(html)
    result['leaks_found'] = len(orphans)
    
    if not orphans:
        # Verificar também com os padrões simples
        leaks = find_css_leaks(html)
        if leaks:
            result['leaks_found'] = len(leaks)
            result['orphans'] = [l['snippet'] for l in leaks[:3]]
    else:
        result['orphans'] = [o['content'] for o in orphans[:3]]
    
    if not orphans:
        return result
    
    # 2. Para cada bloco órfão, remover da posição atual e mover para dentro do <head>
    # Processar de trás para frente para preservar posições
    orphans_sorted = sorted(orphans, key=lambda x: x['start'], reverse=True)
    
    css_to_move = []
    for orphan in orphans_sorted:
        css_content = orphan['full_match']
        
        # Verificar se já existe um <style> com esse conteúdo no <head>
        # Se sim, apenas remover o bloco órfão
        # Se não, mover para dentro de um <style> no <head>
        
        # Remover o bloco órfão do HTML
        html = html[:orphan['start']] + html[orphan['end']:]
        css_to_move.append(css_content)
        result['fixed'] += 1
    
    # 3. Verificar se o CSS removido já existe em algum <style> do documento
    # Se não existir, injetar no <head>
    for css_content in css_to_move:
        # Extrair apenas os seletores (sem comentários) para verificar duplicata
        selectors = re.findall(r'\.([\w-]+)\s*[,{]', css_content)
        
        already_exists = False
        if selectors:
            # Verificar se o primeiro seletor já existe em algum <style>
            first_selector = selectors[0] if selectors else ''
            if first_selector:
                style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL | re.IGNORECASE)
                for block in style_blocks:
                    if first_selector in block:
                        already_exists = True
                        break
        
        if not already_exists:
            # Injetar no <head> dentro de um <style>
            style_tag = f'\n<style>\n{css_content}\n</style>\n'
            html = html.replace('</head>', style_tag + '</head>', 1)
    
    if html != original_html:
        backup(path)
        path.write_text(html, encoding='utf-8')
        result['modified'] = True
    
    return result


def scan_all_pages(dry_run: bool = False) -> list:
    """Varre todas as páginas HTML e corrige CSS vazado."""
    pages = []
    
    # Coletar todas as páginas HTML (excluindo backups, scripts e relatórios)
    exclude_dirs = {'_backups', '_audit_reports', 'scripts', 'node_modules', '.git'}
    
    for html_file in sorted(ROOT.glob('**/*.html')):
        # Verificar se está em diretório excluído
        parts = set(html_file.parts)
        if any(d in str(html_file) for d in exclude_dirs):
            continue
        pages.append(html_file)
    
    return pages


def main():
    import sys
    dry_run = '--dry-run' in sys.argv
    
    print("=" * 70)
    print(f"  {'DRY-RUN: ' if dry_run else ''}Diagnóstico e Correção de CSS Vazado")
    print(f"  Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    pages = scan_all_pages()
    print(f"\nTotal de páginas a verificar: {len(pages)}\n")
    
    affected = []
    clean = []
    
    for page in pages:
        if dry_run:
            # Apenas diagnosticar
            html = page.read_text(encoding='utf-8', errors='ignore')
            orphans = find_orphan_style_content(html)
            leaks = find_css_leaks(html) if not orphans else []
            
            if orphans or leaks:
                total = len(orphans) or len(leaks)
                print(f"  ❌ {page.relative_to(ROOT)} — {total} bloco(s) CSS vazado(s)")
                for o in (orphans or leaks)[:2]:
                    snippet = o.get('content', o.get('snippet', ''))[:80]
                    print(f"     → {snippet}")
                affected.append(str(page.relative_to(ROOT)))
            else:
                clean.append(str(page.relative_to(ROOT)))
        else:
            result = fix_page(page)
            if result['leaks_found'] > 0:
                status = '✅ CORRIGIDO' if result['modified'] else '⚠️  DETECTADO (não modificado)'
                print(f"  {status}: {result['page']} — {result['leaks_found']} bloco(s)")
                for snippet in result['orphans'][:2]:
                    print(f"     → {snippet[:80]}")
                affected.append(result['page'])
            else:
                clean.append(result['page'])
    
    print(f"\n{'=' * 70}")
    print(f"  RESUMO")
    print(f"{'=' * 70}")
    print(f"  Páginas com CSS vazado: {len(affected)}")
    print(f"  Páginas limpas:         {len(clean)}")
    
    if affected:
        print(f"\n  Páginas afetadas:")
        for p in affected:
            print(f"    - {p}")
    
    if dry_run:
        print(f"\n  ⚠️  Modo dry-run: nenhum arquivo foi modificado.")
        print(f"  Execute sem --dry-run para aplicar as correções.")


if __name__ == "__main__":
    main()
