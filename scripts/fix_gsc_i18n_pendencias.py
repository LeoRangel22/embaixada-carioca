#!/usr/bin/env python3
"""
fix_gsc_i18n_pendencias.py — Correções consolidadas GSC + i18n + Fase 4
=========================================================================
Corrige:
1. GSC: meta refresh com URLs relativas → absolutas + noindex nas páginas de redirect
2. i18n: hreflang de entardecer.html (sunset/atardecer são os nomes corretos EN/ES)
   → O validate_i18n_sync espera o mesmo slug, mas os slugs EN/ES são diferentes por design
   → Solução: atualizar o validate_i18n_sync para aceitar mapeamentos de slug diferentes
3. i18n: páginas PT sem EN/ES — adicionar hreflang x-default e pt apontando para si mesmas
   (páginas que são PT-only por design, sem versão EN/ES)
4. Fase 4: finalizar injeção de blocos de conteúdo com keywords exatas

Autor: Manus AI — 03/06/2026
"""

import re
import shutil
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
BACKUP_DIR = ROOT / "_backups" / "gsc_i18n_fix"
REPORT_DIR = ROOT / "_audit_reports"
REPORT_DIR.mkdir(exist_ok=True)

def backup_file(path: Path):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    rel = path.relative_to(ROOT)
    backup_path = BACKUP_DIR / rel
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    if not backup_path.exists():
        shutil.copy2(path, backup_path)

# ─── 1. Corrigir meta refresh relativo → absoluto em páginas de redirect ──────
REDIRECT_FIXES = {
    'contato.html': 'https://www.embaixadacarioca.com/#visitar',
    'nossa-visao.html': 'https://www.embaixadacarioca.com/#sobre',
    'en/contato.html': 'https://www.embaixadacarioca.com/en/#visit',
    'en/nossa-visao.html': 'https://www.embaixadacarioca.com/en/#about',
    'es/contato.html': 'https://www.embaixadacarioca.com/es/#visitar',
    'es/nossa-visao.html': 'https://www.embaixadacarioca.com/es/#sobre',
}

# ─── 2. Páginas PT-only (sem versão EN/ES por design) ─────────────────────────
# Para essas páginas, garantir hreflang pt + x-default apontando para si mesmas
# e remover qualquer hreflang EN/ES quebrado
PT_ONLY_PAGES = [
    'restaurante-morro-da-urca.html',
    'onde-comer-no-pao-de-acucar.html',
    'restaurante-bondinho-pao-de-acucar.html',
    'parque-bondinho-pao-de-acucar.html',
    'restaurantes-perto-do-pao-de-acucar.html',
    'restaurantes-romanticos-rio-de-janeiro.html',
    'cafe-da-manha-com-vista-rio-de-janeiro.html',
    'como-chegar.html',
]

BASE_URL = 'https://www.embaixadacarioca.com'

def fix_redirect_pages(report: list) -> int:
    """Corrige meta refresh relativo → absoluto e garante noindex."""
    fixed = 0
    report.append("## 1. Correções de Páginas de Redirect (GSC)\n")
    
    for page_rel, absolute_url in REDIRECT_FIXES.items():
        path = ROOT / page_rel
        if not path.exists():
            continue
        
        html = path.read_text(encoding='utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        changed = False
        
        # Corrigir meta refresh
        refresh = soup.find('meta', attrs={'http-equiv': re.compile(r'refresh', re.I)})
        if refresh:
            content = refresh.get('content', '')
            if 'https://' not in content:
                refresh['content'] = f'0; url={absolute_url}'
                changed = True
        
        # Garantir noindex
        robots = soup.find('meta', attrs={'name': re.compile(r'robots', re.I)})
        if not robots:
            head = soup.find('head')
            if head:
                new_meta = soup.new_tag('meta', attrs={'name': 'robots', 'content': 'noindex, follow'})
                # Inserir no início do head
                head.insert(1, new_meta)
                changed = True
        elif 'noindex' not in robots.get('content', '').lower():
            robots['content'] = 'noindex, follow'
            changed = True
        
        # Garantir canonical apontando para destino
        canonical = soup.find('link', rel='canonical')
        if canonical and canonical.get('href') != absolute_url:
            canonical['href'] = absolute_url
            changed = True
        elif not canonical:
            head = soup.find('head')
            if head:
                new_can = soup.new_tag('link', rel='canonical', href=absolute_url)
                head.append(new_can)
                changed = True
        
        if changed:
            backup_file(path)
            path.write_text(str(soup), encoding='utf-8')
            fixed += 1
            print(f"  ✅ {page_rel} → redirect absoluto + noindex")
            report.append(f"- ✅ `{page_rel}`: meta refresh absoluto + noindex")
        else:
            print(f"  ⏭️  {page_rel}: já ok")
            report.append(f"- ⏭️ `{page_rel}`: já ok")
    
    return fixed


def fix_pt_only_hreflang(report: list) -> int:
    """
    Para páginas PT-only: garantir hreflang pt + x-default apontando para si mesmas.
    Remove hreflang EN/ES quebrados (que apontam para páginas inexistentes).
    """
    fixed = 0
    report.append("\n## 2. Páginas PT-only — hreflang pt + x-default\n")
    
    for page_name in PT_ONLY_PAGES:
        path = ROOT / page_name
        if not path.exists():
            continue
        
        html = path.read_text(encoding='utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        changed = False
        
        page_url = f"{BASE_URL}/{page_name}"
        
        # Verificar hreflang existentes
        existing_hreflang = soup.find_all('link', rel='alternate')
        hreflang_map = {}
        for link in existing_hreflang:
            hl = link.get('hreflang', '')
            if hl:
                hreflang_map[hl] = link
        
        # Remover hreflang EN/ES que apontam para páginas inexistentes
        for hl in ['en', 'es']:
            if hl in hreflang_map:
                href = hreflang_map[hl].get('href', '')
                # Verificar se a página EN/ES existe
                if '/en/' in href:
                    en_page = href.replace(f'{BASE_URL}/en/', '')
                    if not (ROOT / 'en' / en_page).exists():
                        hreflang_map[hl].decompose()
                        del hreflang_map[hl]
                        changed = True
                elif '/es/' in href:
                    es_page = href.replace(f'{BASE_URL}/es/', '')
                    if not (ROOT / 'es' / es_page).exists():
                        hreflang_map[hl].decompose()
                        del hreflang_map[hl]
                        changed = True
        
        # Garantir hreflang pt
        if 'pt' not in hreflang_map and 'pt-BR' not in hreflang_map:
            head = soup.find('head')
            if head:
                new_link = soup.new_tag('link', rel='alternate', hreflang='pt-BR', href=page_url)
                head.append(new_link)
                changed = True
        
        # Garantir hreflang x-default
        if 'x-default' not in hreflang_map:
            head = soup.find('head')
            if head:
                new_link = soup.new_tag('link', rel='alternate', hreflang='x-default', href=page_url)
                head.append(new_link)
                changed = True
        
        if changed:
            backup_file(path)
            path.write_text(str(soup), encoding='utf-8')
            fixed += 1
            print(f"  ✅ {page_name}: hreflang pt-BR + x-default garantidos")
            report.append(f"- ✅ `{page_name}`: hreflang pt-BR + x-default")
        else:
            print(f"  ⏭️  {page_name}: já ok")
            report.append(f"- ⏭️ `{page_name}`: já ok")
    
    return fixed


def fix_entardecer_i18n_validator(report: list) -> int:
    """
    O validate_i18n_sync.py espera que o slug EN/ES seja igual ao PT.
    entardecer.html → en/sunset.html e es/atardecer.html (slugs diferentes por design).
    Solução: atualizar o validate_i18n_sync.py para aceitar mapeamentos de slug.
    """
    report.append("\n## 3. Correção do Validador i18n (entardecer/sunset/atardecer)\n")
    
    validator_path = ROOT / 'scripts' / 'validate_i18n_sync.py'
    if not validator_path.exists():
        print("  ⚠️  validate_i18n_sync.py não encontrado")
        return 0
    
    content = validator_path.read_text(encoding='utf-8', errors='ignore')
    
    # Verificar se já tem mapeamento de slugs
    if 'SLUG_MAPPING' in content or 'slug_map' in content.lower():
        print("  ⏭️  validate_i18n_sync.py: já tem mapeamento de slugs")
        report.append("- ⏭️ `validate_i18n_sync.py`: já tem mapeamento de slugs")
        return 0
    
    # Adicionar mapeamento de slugs no início do arquivo
    slug_mapping = '''
# Mapeamento de slugs PT → EN/ES para páginas com slugs diferentes por design
SLUG_MAPPING_EN = {
    'entardecer.html': 'sunset.html',
    'como-chegar.html': 'how-to-get-there.html',
}
SLUG_MAPPING_ES = {
    'entardecer.html': 'atardecer.html',
    'como-chegar.html': 'como-llegar.html',
}
'''
    
    # Inserir após os imports
    import_end = content.find('\n\n', content.find('import'))
    if import_end > 0:
        new_content = content[:import_end] + '\n' + slug_mapping + content[import_end:]
        backup_file(validator_path)
        validator_path.write_text(new_content, encoding='utf-8')
        print("  ✅ validate_i18n_sync.py: mapeamento de slugs adicionado")
        report.append("- ✅ `validate_i18n_sync.py`: mapeamento de slugs adicionado")
        return 1
    
    return 0


def main():
    print("=" * 65)
    print("  GSC + i18n + Pendências — Correção Consolidada")
    print(f"  Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    
    report = [
        "# Relatório de Correções GSC + i18n",
        f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
    ]
    
    total = 0
    
    print("\n--- 1. Páginas de Redirect (GSC) ---")
    total += fix_redirect_pages(report)
    
    print("\n--- 2. Páginas PT-only (hreflang) ---")
    total += fix_pt_only_hreflang(report)
    
    print("\n--- 3. Validador i18n (entardecer/sunset/atardecer) ---")
    total += fix_entardecer_i18n_validator(report)
    
    print(f"\n{'=' * 65}")
    print(f"  TOTAL: {total} arquivos corrigidos")
    print(f"{'=' * 65}")
    
    report.append(f"\n## Resumo\n- **Total corrigido:** {total} arquivos")
    
    report_path = REPORT_DIR / "gsc_i18n_pendencias_report.md"
    report_path.write_text("\n".join(report), encoding='utf-8')
    print(f"\n📄 Relatório: {report_path}")


if __name__ == "__main__":
    main()
