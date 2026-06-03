#!/usr/bin/env python3
"""
Auditoria completa de overflow e flex-wrap no projeto embaixadacarioca.
Identifica padrões problemáticos em todos os arquivos CSS e HTML.
"""

import re
import os
import json
from pathlib import Path

ROOT = Path("/home/ubuntu/embaixada-carioca")
SKIP_DIRS = {".git", "_backups", "node_modules"}

# ─── Padrões de risco ──────────────────────────────────────────────────────────

# overflow:hidden aplicado a seletores que contêm texto visível (botões, links, texto)
OVERFLOW_HIDDEN_RISKY = re.compile(
    r'([^{}\n]*(?:\.btn|\.cta|a\b|button|\.nav|\.link|\.label|\.title|\.text|\.chip|\.tag|\.badge|\.pill|\.menu|\.item|\.card|\.hero|\.bar|\.eyebrow|\.breadcrumb|\.notice|\.notice|\.wrap|\.inner|\.content|\.copy)[^{}\n]*)\{([^}]*overflow\s*:\s*hidden[^}]*)\}',
    re.IGNORECASE
)

# flex-wrap:nowrap em containers que podem ter muitos filhos
FLEX_NOWRAP_RISKY = re.compile(
    r'([^{}\n]*(?:\.btn|\.cta|\.nav|\.link|\.menu|\.hero|\.bar|\.chips|\.tags|\.badges|\.pills|\.items|\.cards|\.wrap|\.inner|\.content|\.copy|\.ctas|\.actions|\.links|\.group|\.row|\.list)[^{}\n]*)\{([^}]*flex-wrap\s*:\s*nowrap[^}]*)\}',
    re.IGNORECASE
)

# overflow:hidden com !important (mais agressivo)
OVERFLOW_HIDDEN_IMPORTANT = re.compile(
    r'([^{}\n]*)\{([^}]*overflow\s*:\s*hidden\s*!important[^}]*)\}',
    re.IGNORECASE
)

# flex-wrap:nowrap com !important
FLEX_NOWRAP_IMPORTANT = re.compile(
    r'([^{}\n]*)\{([^}]*flex-wrap\s*:\s*nowrap\s*!important[^}]*)\}',
    re.IGNORECASE
)

# white-space:nowrap com overflow:hidden no mesmo bloco (truncamento garantido)
NOWRAP_PLUS_OVERFLOW = re.compile(
    r'([^{}\n]*)\{([^}]*(?:white-space\s*:\s*nowrap[^}]*overflow\s*:\s*hidden|overflow\s*:\s*hidden[^}]*white-space\s*:\s*nowrap)[^}]*)\}',
    re.IGNORECASE
)

# max-width muito pequeno em containers de botões
SMALL_MAXWIDTH = re.compile(
    r'([^{}\n]*(?:\.btn|\.cta|\.hero-ctas|\.ctas|\.actions|\.links|\.group)[^{}\n]*)\{([^}]*max-width\s*:\s*(?:\d{1,3}px|min\([^)]*\))[^}]*)\}',
    re.IGNORECASE
)

# ─── Funções auxiliares ────────────────────────────────────────────────────────

def get_css_files():
    """Retorna todos os arquivos CSS do projeto (excluindo backups)."""
    files = []
    for p in ROOT.rglob("*.css"):
        if any(d in p.parts for d in SKIP_DIRS):
            continue
        files.append(p)
    return sorted(files)

def get_html_files():
    """Retorna todos os arquivos HTML do projeto (excluindo backups)."""
    files = []
    for p in ROOT.rglob("*.html"):
        if any(d in p.parts for d in SKIP_DIRS):
            continue
        files.append(p)
    return sorted(files)

def find_inline_css_in_html(html_content):
    """Extrai blocos de CSS inline de arquivos HTML."""
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', html_content, re.DOTALL | re.IGNORECASE)
    return "\n".join(style_blocks)

def audit_css_content(content, source_file):
    """Audita um bloco de CSS e retorna lista de problemas."""
    issues = []
    
    # 1. overflow:hidden + !important em seletores de texto/botões
    for m in OVERFLOW_HIDDEN_IMPORTANT.finditer(content):
        selector = m.group(1).strip().split("\n")[-1].strip()
        props = m.group(2).strip()
        # Filtrar seletores que NÃO são problemáticos (ex: modal, overlay, scroll)
        safe_patterns = ['modal', 'overlay', 'scroll', 'dropdown', 'tooltip', 'popup', 'sidebar', 'drawer', 'shimmer', 'ripple', 'sr-only', 'visually-hidden', 'clip']
        if any(p in selector.lower() for p in safe_patterns):
            continue
        # Verificar se o seletor pode conter texto visível
        text_patterns = ['.btn', 'a.', 'button', '.nav', '.link', '.label', '.title', '.text', '.chip', '.tag', '.badge', '.pill', '.menu', '.item', '.card', '.hero', '.bar', '.eyebrow', '.breadcrumb', '.notice', '.wrap', '.inner', '.content', '.copy']
        is_risky = any(p in selector.lower() for p in text_patterns)
        issues.append({
            'type': 'overflow:hidden!important',
            'severity': 'HIGH' if is_risky else 'MEDIUM',
            'selector': selector[:120],
            'props': props[:200],
            'file': str(source_file.relative_to(ROOT)),
            'risky': is_risky
        })
    
    # 2. flex-wrap:nowrap + !important
    for m in FLEX_NOWRAP_IMPORTANT.finditer(content):
        selector = m.group(1).strip().split("\n")[-1].strip()
        props = m.group(2).strip()
        safe_patterns = ['nav-links', 'breadcrumb-nav', 'pagination', 'tab-', 'stepper']
        if any(p in selector.lower() for p in safe_patterns):
            continue
        issues.append({
            'type': 'flex-wrap:nowrap!important',
            'severity': 'HIGH',
            'selector': selector[:120],
            'props': props[:200],
            'file': str(source_file.relative_to(ROOT)),
            'risky': True
        })
    
    # 3. white-space:nowrap + overflow:hidden no mesmo bloco
    for m in NOWRAP_PLUS_OVERFLOW.finditer(content):
        selector = m.group(1).strip().split("\n")[-1].strip()
        props = m.group(2).strip()
        safe_patterns = ['sr-only', 'visually-hidden', 'clip', 'shimmer', 'eyebrow', 'hero-eyebrow', 'breadcrumb']
        if any(p in selector.lower() for p in safe_patterns):
            continue
        issues.append({
            'type': 'white-space:nowrap + overflow:hidden',
            'severity': 'HIGH',
            'selector': selector[:120],
            'props': props[:200],
            'file': str(source_file.relative_to(ROOT)),
            'risky': True
        })
    
    # 4. overflow:hidden sem !important em seletores de texto/botões
    for m in OVERFLOW_HIDDEN_RISKY.finditer(content):
        selector = m.group(1).strip().split("\n")[-1].strip()
        props = m.group(2).strip()
        # Pular se já foi capturado pelo padrão !important
        if '!important' in props:
            continue
        safe_patterns = ['modal', 'overlay', 'scroll', 'dropdown', 'tooltip', 'popup', 'sidebar', 'drawer', 'shimmer', 'ripple', 'sr-only', 'visually-hidden', 'clip', 'img', 'image', 'photo', 'picture', 'video', 'iframe']
        if any(p in selector.lower() for p in safe_patterns):
            continue
        issues.append({
            'type': 'overflow:hidden (sem !important)',
            'severity': 'MEDIUM',
            'selector': selector[:120],
            'props': props[:200],
            'file': str(source_file.relative_to(ROOT)),
            'risky': True
        })
    
    # 5. flex-wrap:nowrap sem !important em containers de CTAs
    for m in FLEX_NOWRAP_RISKY.finditer(content):
        selector = m.group(1).strip().split("\n")[-1].strip()
        props = m.group(2).strip()
        if '!important' in props:
            continue
        safe_patterns = ['nav-links', 'breadcrumb-nav', 'pagination', 'tab-', 'stepper', 'header', 'nav.top']
        if any(p in selector.lower() for p in safe_patterns):
            continue
        issues.append({
            'type': 'flex-wrap:nowrap (sem !important)',
            'severity': 'MEDIUM',
            'selector': selector[:120],
            'props': props[:200],
            'file': str(source_file.relative_to(ROOT)),
            'risky': True
        })
    
    return issues

def audit_html_for_inline_style(html_content, source_file):
    """Audita atributos style= inline em HTML."""
    issues = []
    # Buscar style="...overflow:hidden..." em elementos de texto
    inline_overflow = re.finditer(r'<([a-z]+)[^>]*\bstyle="([^"]*overflow\s*:\s*hidden[^"]*)"[^>]*>', html_content, re.IGNORECASE)
    for m in inline_overflow:
        tag = m.group(1)
        style = m.group(2)
        safe_tags = ['img', 'video', 'iframe', 'figure', 'div']
        if tag.lower() in safe_tags:
            continue
        issues.append({
            'type': 'inline style overflow:hidden',
            'severity': 'MEDIUM',
            'selector': f'<{tag}> tag',
            'props': style[:200],
            'file': str(source_file.relative_to(ROOT)),
            'risky': True
        })
    return issues

# ─── Execução principal ────────────────────────────────────────────────────────

all_issues = []

# Auditar arquivos CSS
print("=== Auditando arquivos CSS ===")
for css_file in get_css_files():
    try:
        content = css_file.read_text(encoding='utf-8', errors='ignore')
        issues = audit_css_content(content, css_file)
        if issues:
            print(f"  {css_file.relative_to(ROOT)}: {len(issues)} problema(s)")
        all_issues.extend(issues)
    except Exception as e:
        print(f"  ERRO em {css_file}: {e}")

# Auditar CSS inline em arquivos HTML (apenas os principais, não backups)
print("\n=== Auditando CSS inline em HTML ===")
main_html_files = [
    ROOT / "index.html",
    ROOT / "almoco.html",
    ROOT / "cafe-da-manha.html",
    ROOT / "cardapio.html",
    ROOT / "eventos.html",
    ROOT / "como-chegar.html",
    ROOT / "en/index.html",
    ROOT / "es/index.html",
    ROOT / "offline.html",
    ROOT / "404.html" if (ROOT / "404.html").exists() else None,
]
for html_file in main_html_files:
    if html_file is None or not html_file.exists():
        continue
    try:
        content = html_file.read_text(encoding='utf-8', errors='ignore')
        inline_css = find_inline_css_in_html(content)
        if inline_css:
            issues = audit_css_content(inline_css, html_file)
            inline_issues = audit_html_for_inline_style(content, html_file)
            all_issues.extend(issues)
            all_issues.extend(inline_issues)
            total = len(issues) + len(inline_issues)
            if total:
                print(f"  {html_file.relative_to(ROOT)}: {total} problema(s)")
    except Exception as e:
        print(f"  ERRO em {html_file}: {e}")

# ─── Resumo ────────────────────────────────────────────────────────────────────

print(f"\n=== TOTAL: {len(all_issues)} problemas encontrados ===\n")

# Agrupar por tipo e severidade
by_severity = {'HIGH': [], 'MEDIUM': [], 'LOW': []}
for issue in all_issues:
    sev = issue.get('severity', 'LOW')
    by_severity[sev].append(issue)

for sev in ['HIGH', 'MEDIUM', 'LOW']:
    items = by_severity[sev]
    if not items:
        continue
    print(f"\n{'='*60}")
    print(f"SEVERIDADE {sev}: {len(items)} problema(s)")
    print(f"{'='*60}")
    for i, issue in enumerate(items, 1):
        print(f"\n[{i}] {issue['type']}")
        print(f"    Arquivo : {issue['file']}")
        print(f"    Seletor : {issue['selector']}")
        print(f"    Props   : {issue['props'][:150]}")

# Salvar JSON para análise posterior
output_path = ROOT / "scripts/audit_overflow_flexwrap_results.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_issues, f, ensure_ascii=False, indent=2)
print(f"\nResultados salvos em: {output_path}")
