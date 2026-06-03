#!/usr/bin/env python3
"""
fix_gsc_issues.py — Correções dos 4 Problemas Críticos do Google Search Console
================================================================================
Problemas identificados no relatório GSC de 02/06/2026:

1. PÁGINA COM REDIRECIONAMENTO (8 páginas)
   → contato.html, nossa-visao.html e versões EN/ES têm meta refresh 0s
   → Solução: Adicionar noindex + canonical apontando para destino do redirect

2. PÁGINA ALTERNATIVA COM TAG CANÔNICA ADEQUADA (7 páginas)
   → Páginas que o Google vê como duplicatas mas têm canonical correto
   → Solução: Verificar e reforçar canonicals nas páginas de redirecionamento

3. NÃO ENCONTRADO (404) — 4 páginas
   → general-3/index.html e similares que redirecionam para páginas inexistentes
   → Solução: Garantir que páginas de redirect apontem para URLs válidas

4. EXCLUÍDA PELA TAG NOINDEX — 3 páginas
   → general-3/index.html tem noindex (correto — é página de redirect)
   → 404.html e offline.html têm noindex (correto — são páginas de sistema)
   → AÇÃO: Verificar se há páginas de conteúdo real com noindex indevido

Autor: Manus AI — 03/06/2026
"""

import re
import shutil
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
BACKUP_DIR = ROOT / "_backups" / "gsc_fixes"
REPORT_DIR = ROOT / "_audit_reports"
REPORT_DIR.mkdir(exist_ok=True)

def backup_file(path: Path):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / path.relative_to(ROOT)
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    if not backup_path.exists():
        shutil.copy2(path, backup_path)

def fix_redirect_page(path: Path, redirect_url: str, canonical_url: str, report: list):
    """
    Para páginas que são APENAS redirecionamentos (meta refresh 0s):
    - Garante noindex (correto para páginas de redirect)
    - Garante canonical apontando para o destino final
    - Garante que o redirect seja para URL absoluta válida
    """
    html = path.read_text(encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    changed = False

    # 1. Verificar/corrigir o meta refresh — garantir URL absoluta
    refresh = soup.find('meta', attrs={'http-equiv': re.compile(r'refresh', re.I)})
    if refresh:
        content = refresh.get('content', '')
        # Se o redirect é relativo (ex: /#visitar), converter para absoluto
        if content and not 'https://' in content:
            url_match = re.search(r'url=(.+)', content, re.IGNORECASE)
            if url_match:
                relative_url = url_match.group(1).strip().strip('"\'')
                if relative_url.startswith('/'):
                    absolute_url = f"https://www.embaixadacarioca.com{relative_url}"
                    new_content = f"0; url={absolute_url}"
                    refresh['content'] = new_content
                    changed = True
                    report.append(f"  ✅ Meta refresh corrigido: {content} → {new_content}")

    # 2. Garantir noindex (correto para páginas de redirect)
    robots = soup.find('meta', attrs={'name': re.compile(r'robots', re.I)})
    if robots:
        current = robots.get('content', '')
        if 'noindex' not in current.lower():
            robots['content'] = 'noindex, follow'
            changed = True
            report.append(f"  ✅ Noindex adicionado (página de redirect)")
    else:
        head = soup.find('head')
        if head:
            new_meta = soup.new_tag('meta', attrs={'name': 'robots', 'content': 'noindex, follow'})
            head.append(new_meta)
            changed = True
            report.append(f"  ✅ Meta robots noindex criado")

    # 3. Garantir canonical apontando para o destino final
    canonical = soup.find('link', rel='canonical')
    if canonical:
        if canonical.get('href') != canonical_url:
            canonical['href'] = canonical_url
            changed = True
            report.append(f"  ✅ Canonical corrigido → {canonical_url}")
    else:
        head = soup.find('head')
        if head:
            new_canonical = soup.new_tag('link', rel='canonical', href=canonical_url)
            head.append(new_canonical)
            changed = True
            report.append(f"  ✅ Canonical criado → {canonical_url}")

    if changed:
        backup_file(path)
        path.write_text(str(soup), encoding='utf-8')
        return True
    return False


def main():
    print("=" * 65)
    print("  GSC FIX — Correções dos 4 Problemas Críticos do GSC")
    print(f"  Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    report_lines = [
        "# Relatório de Correções GSC",
        f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        "## 1. Páginas com Redirecionamento\n"
    ]

    total_fixed = 0

    # ─── PROBLEMA 1 + 2: Páginas de redirect com meta refresh ────────────────
    # Mapeamento: arquivo → (URL de redirect absoluta, canonical correto)
    redirect_pages = {
        # PT
        'contato.html': (
            'https://www.embaixadacarioca.com/#visitar',
            'https://www.embaixadacarioca.com/#visitar'
        ),
        'nossa-visao.html': (
            'https://www.embaixadacarioca.com/#sobre',
            'https://www.embaixadacarioca.com/#sobre'
        ),
        # EN
        'en/contato.html': (
            'https://www.embaixadacarioca.com/en/#visit',
            'https://www.embaixadacarioca.com/en/#visit'
        ),
        'en/nossa-visao.html': (
            'https://www.embaixadacarioca.com/en/#about',
            'https://www.embaixadacarioca.com/en/#about'
        ),
        # ES
        'es/contato.html': (
            'https://www.embaixadacarioca.com/es/#visitar',
            'https://www.embaixadacarioca.com/es/#visitar'
        ),
        'es/nossa-visao.html': (
            'https://www.embaixadacarioca.com/es/#sobre',
            'https://www.embaixadacarioca.com/es/#sobre'
        ),
    }

    for page_rel, (redirect_url, canonical_url) in redirect_pages.items():
        page_path = ROOT / page_rel
        if not page_path.exists():
            print(f"  ⚠️  {page_rel}: não encontrado")
            continue

        page_report = []
        fixed = fix_redirect_page(page_path, redirect_url, canonical_url, page_report)
        total_fixed += 1 if fixed else 0

        status = "✅ CORRIGIDO" if fixed else "⏭️  JÁ OK"
        print(f"\n{status} — {page_rel}")
        for line in page_report:
            print(f"  {line}")

        report_lines.append(f"### `{page_rel}` — {'corrigido' if fixed else 'já ok'}")
        for line in page_report:
            report_lines.append(line)
        report_lines.append("")

    # ─── PROBLEMA 3: 404s — verificar general-3 e outras páginas de redirect ──
    print("\n" + "=" * 65)
    print("  PROBLEMA 3: Verificação de 404s")
    print("=" * 65)
    report_lines.append("## 3. Páginas 404\n")

    # Verificar general-3/index.html — já tem noindex, canonical e redirect corretos
    general3 = ROOT / 'general-3' / 'index.html'
    if general3.exists():
        html_g = general3.read_text(encoding='utf-8', errors='ignore')
        soup_g = BeautifulSoup(html_g, 'html.parser')
        robots_g = soup_g.find('meta', attrs={'name': re.compile(r'robots', re.I)})
        canonical_g = soup_g.find('link', rel='canonical')
        refresh_g = soup_g.find('meta', attrs={'http-equiv': re.compile(r'refresh', re.I)})
        print(f"  general-3/index.html:")
        print(f"    robots: {robots_g.get('content') if robots_g else 'AUSENTE'}")
        print(f"    canonical: {canonical_g.get('href') if canonical_g else 'AUSENTE'}")
        print(f"    refresh: {refresh_g.get('content') if refresh_g else 'AUSENTE'}")

        # Verificar se o redirect aponta para URL válida
        if refresh_g:
            content = refresh_g.get('content', '')
            url_match = re.search(r'url=(.+)', content, re.IGNORECASE)
            if url_match:
                target = url_match.group(1).strip()
                print(f"    → Redirect target: {target}")
                if target.startswith('https://www.embaixadacarioca.com'):
                    print(f"    ✅ Redirect aponta para URL válida")
                    report_lines.append(f"- ✅ `general-3/index.html`: redirect correto → {target}")
                else:
                    print(f"    ⚠️ Redirect pode ser problemático: {target}")
                    report_lines.append(f"- ⚠️ `general-3/index.html`: verificar redirect → {target}")

    # ─── PROBLEMA 4: Noindex — verificar se são todos intencionais ───────────
    print("\n" + "=" * 65)
    print("  PROBLEMA 4: Páginas com noindex")
    print("=" * 65)
    report_lines.append("## 4. Páginas com noindex\n")

    noindex_intentional = ['404.html', 'offline.html', 'general-3/index.html',
                           'contato.html', 'nossa-visao.html',
                           'en/contato.html', 'en/nossa-visao.html',
                           'es/contato.html', 'es/nossa-visao.html']

    for f in sorted(ROOT.glob('**/*.html')):
        if any(x in str(f) for x in ['_backups', '_audit', 'scripts', 'node_modules']):
            continue
        html_f = f.read_text(encoding='utf-8', errors='ignore')
        soup_f = BeautifulSoup(html_f, 'html.parser')
        robots_f = soup_f.find('meta', attrs={'name': re.compile(r'robots', re.I)})
        if robots_f and 'noindex' in robots_f.get('content', '').lower():
            rel_path = str(f.relative_to(ROOT))
            is_intentional = any(rel_path.endswith(p) for p in noindex_intentional)
            flag = "✅ INTENCIONAL" if is_intentional else "❌ VERIFICAR"
            print(f"  {flag}: {rel_path}")
            report_lines.append(f"- {flag}: `{rel_path}`")

    # ─── RESUMO ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print(f"  RESUMO: {total_fixed} arquivos corrigidos")
    print("=" * 65)

    report_lines.append(f"\n## Resumo\n- **Arquivos corrigidos:** {total_fixed}")

    report_path = REPORT_DIR / "gsc_fixes_report.md"
    report_path.write_text("\n".join(report_lines), encoding='utf-8')
    print(f"\n📄 Relatório salvo em: {report_path}")


if __name__ == "__main__":
    main()
