#!/usr/bin/env python3
"""
audit_fase3_acessibilidade.py — Auditoria WCAG 2.2 AAA Profunda
Embaixada Carioca — embaixadacarioca.com

Verifica:
  A-3.1  Contraste de cores (AA mín 4.5:1 texto normal, AAA 7:1)
  A-3.2  Tag <main> presente
  A-3.3  Skip link (#main-content)
  A-3.4  :focus-visible / outline no CSS
  A-3.5  prefers-reduced-motion no CSS
  A-3.6  Imagens sem alt ou com alt vazio
  A-3.7  Formulários sem label associado
  A-3.8  ARIA roles e landmarks
  A-3.9  lang attribute nas páginas
  A-3.10 Tabindex > 0 (antipadrão)
  A-3.11 Links sem texto descritivo (apenas ícones)
  A-3.12 Headings sem hierarquia lógica
  A-3.13 Botões sem aria-label
  A-3.14 Videos/iframes sem title
"""
from __future__ import annotations
import glob, re, math
from bs4 import BeautifulSoup
from collections import defaultdict

ROOT_PAGES = sorted(glob.glob('*.html') + glob.glob('en/*.html') + glob.glob('es/*.html'))
ROOT_PAGES = [p for p in ROOT_PAGES if p not in ('404.html','offline.html')]

print(f"Total de páginas: {len(ROOT_PAGES)}\n")

# ─────────────────────────────────────────────────────────────
# A-3.1 — Contraste de Cores (análise do CSS)
# ─────────────────────────────────────────────────────────────
print("="*60)
print("A-3.1 CONTRASTE DE CORES — Análise CSS")
print("="*60)

def hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join(c*2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def relative_luminance(rgb):
    vals = []
    for c in rgb:
        s = c / 255
        vals.append(s/12.92 if s <= 0.04045 else ((s+0.055)/1.055)**2.4)
    return 0.2126*vals[0] + 0.7152*vals[1] + 0.0722*vals[2]

def contrast_ratio(c1, c2):
    l1 = relative_luminance(hex_to_rgb(c1))
    l2 = relative_luminance(hex_to_rgb(c2))
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

# Pares de cores críticos extraídos do CSS
COLOR_PAIRS = [
    # (texto, fundo, descrição, tamanho_texto)
    ("#1a1a1a", "#f6efde", "Texto principal sobre paper", "normal"),
    ("#1a1a1a", "#ffffff", "Texto principal sobre branco", "normal"),
    ("#7d8386", "#f6efde", "Cinza secundário sobre paper", "normal"),
    ("#7d8386", "#ffffff", "Cinza secundário sobre branco", "normal"),
    ("#527f8f", "#f6efde", "Azul2 sobre paper", "normal"),
    ("#527f8f", "#ffffff", "Azul2 sobre branco", "normal"),
    ("#c8a96e", "#1a1a1a", "Dourado sobre preto", "normal"),
    ("#c8a96e", "#ffffff", "Dourado sobre branco", "normal"),
    ("#ffffff", "#1a1a1a", "Branco sobre preto", "normal"),
    ("#ffffff", "#527f8f", "Branco sobre azul2", "normal"),
    ("#ffffff", "#c8a96e", "Branco sobre dourado", "normal"),
    ("#1a1a1a", "#c8a96e", "Preto sobre dourado", "normal"),
    ("#527f8f", "#1a1a1a", "Azul2 sobre preto", "normal"),
    ("#f6efde", "#1a1a1a", "Paper sobre preto", "normal"),
    ("#7d8386", "#1a1a1a", "Cinza sobre preto", "normal"),
    # Placeholders e textos de formulário
    ("#9e9e9e", "#ffffff", "Placeholder sobre branco", "normal"),
    ("#9e9e9e", "#f6efde", "Placeholder sobre paper", "normal"),
]

print(f"\n  {'Par de Cores':<45} {'Ratio':>7}  {'AA':>4}  {'AAA':>4}  {'Status'}")
print(f"  {'-'*45} {'-'*7}  {'-'*4}  {'-'*4}  {'-'*10}")

failures_aa = []
failures_aaa = []
for text, bg, desc, size in COLOR_PAIRS:
    try:
        ratio = contrast_ratio(text, bg)
        aa_min = 4.5 if size == "normal" else 3.0
        aaa_min = 7.0 if size == "normal" else 4.5
        aa_pass = ratio >= aa_min
        aaa_pass = ratio >= aaa_min
        aa_str = "✅" if aa_pass else "❌"
        aaa_str = "✅" if aaa_pass else "❌"
        status = "AAA ✅" if aaa_pass else ("AA ✅" if aa_pass else "FALHA ❌")
        print(f"  {desc:<45} {ratio:>7.2f}  {aa_str:>4}  {aaa_str:>4}  {status}")
        if not aa_pass:
            failures_aa.append((desc, text, bg, ratio))
        elif not aaa_pass:
            failures_aaa.append((desc, text, bg, ratio))
    except Exception as e:
        print(f"  {desc:<45} ERRO: {e}")

print(f"\n  Falhas AA (críticas):  {len(failures_aa)}")
for d, t, b, r in failures_aa:
    print(f"    ❌ {d}: {t} sobre {b} = {r:.2f}:1 (mín 4.5)")
print(f"  Falhas AAA (melhoria): {len(failures_aaa)}")
for d, t, b, r in failures_aaa:
    print(f"    ⚠️  {d}: {t} sobre {b} = {r:.2f}:1 (mín 7.0)")

# ─────────────────────────────────────────────────────────────
# A-3.2 — Tag <main> presente
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("A-3.2 TAG <main> PRESENTE")
print("="*60)

no_main = []
for page in ROOT_PAGES:
    with open(page) as f:
        content = f.read()
    if '<main' not in content.lower():
        no_main.append(page)

print(f"\n  Páginas SEM <main>: {len(no_main)}")
for p in no_main[:10]:
    print(f"    {p}")
if len(no_main) > 10:
    print(f"    ... e mais {len(no_main)-10}")

# ─────────────────────────────────────────────────────────────
# A-3.3 — Skip Link
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("A-3.3 SKIP LINK (#main-content)")
print("="*60)

no_skip = []
for page in ROOT_PAGES:
    with open(page) as f:
        content = f.read()
    if 'skip' not in content.lower() and '#main-content' not in content:
        no_skip.append(page)

print(f"\n  Páginas SEM skip link: {len(no_skip)}")
for p in no_skip[:5]:
    print(f"    {p}")

# ─────────────────────────────────────────────────────────────
# A-3.4 — :focus-visible no CSS
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("A-3.4 :focus-visible NO CSS")
print("="*60)

css_files = glob.glob('assets/css/*.css') + glob.glob('*.css')
for css_file in css_files:
    with open(css_file) as f:
        css = f.read()
    has_focus_visible = ':focus-visible' in css
    has_focus = ':focus' in css
    has_outline_none = 'outline: none' in css or 'outline:none' in css
    print(f"\n  {css_file}:")
    print(f"    :focus-visible: {'✅ presente' if has_focus_visible else '❌ AUSENTE'}")
    print(f"    :focus:         {'✅ presente' if has_focus else '❌ ausente'}")
    print(f"    outline:none:   {'⚠️  PRESENTE (remove foco visual)' if has_outline_none else '✅ não encontrado'}")

    # Contar ocorrências
    fv_count = css.count(':focus-visible')
    f_count = css.count(':focus')
    print(f"    Ocorrências :focus-visible: {fv_count}")
    print(f"    Ocorrências :focus: {f_count}")

# ─────────────────────────────────────────────────────────────
# A-3.5 — prefers-reduced-motion
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("A-3.5 prefers-reduced-motion NO CSS")
print("="*60)

for css_file in css_files:
    with open(css_file) as f:
        css = f.read()
    has_prm = 'prefers-reduced-motion' in css
    count = css.count('prefers-reduced-motion')
    print(f"\n  {css_file}: {'✅ presente (' + str(count) + 'x)' if has_prm else '❌ AUSENTE'}")

# ─────────────────────────────────────────────────────────────
# A-3.6 — Imagens sem alt
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("A-3.6 IMAGENS SEM ALT OU COM ALT VAZIO")
print("="*60)

no_alt = defaultdict(list)
empty_alt = defaultdict(list)

for page in ROOT_PAGES:
    with open(page) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src', '')
        alt = img.get('alt')
        if alt is None:
            no_alt[page].append(src[:60])
        elif alt.strip() == '':
            # Alt vazio é OK para imagens decorativas, mas verificar se tem role=presentation
            role = img.get('role', '')
            aria_hidden = img.get('aria-hidden', '')
            if role != 'presentation' and aria_hidden != 'true':
                empty_alt[page].append(src[:60])

total_no_alt = sum(len(v) for v in no_alt.values())
total_empty = sum(len(v) for v in empty_alt.values())
print(f"\n  Imagens SEM atributo alt: {total_no_alt}")
for p, imgs in list(no_alt.items())[:5]:
    print(f"    {p}: {len(imgs)} imagens")
    for img in imgs[:2]: print(f"      {img}")
print(f"\n  Imagens com alt='' sem role=presentation: {total_empty}")
for p, imgs in list(empty_alt.items())[:5]:
    print(f"    {p}: {len(imgs)} imagens")

# ─────────────────────────────────────────────────────────────
# A-3.7 — Formulários sem label
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("A-3.7 FORMULÁRIOS SEM LABEL ASSOCIADO")
print("="*60)

form_issues = []
for page in ROOT_PAGES:
    with open(page) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    for inp in soup.find_all(['input', 'textarea', 'select']):
        inp_type = inp.get('type', 'text')
        if inp_type in ('hidden', 'submit', 'button', 'reset', 'image'):
            continue
        inp_id = inp.get('id', '')
        aria_label = inp.get('aria-label', '')
        aria_labelledby = inp.get('aria-labelledby', '')
        placeholder = inp.get('placeholder', '')
        has_label = False
        if inp_id:
            has_label = bool(soup.find('label', attrs={'for': inp_id}))
        if not has_label and not aria_label and not aria_labelledby:
            form_issues.append((page, inp_type, inp_id or '(sem id)', placeholder[:40]))

print(f"\n  Inputs sem label acessível: {len(form_issues)}")
for p, t, id_, ph in form_issues[:10]:
    print(f"    {p}: <input type={t} id={id_} placeholder={ph}>")

# ─────────────────────────────────────────────────────────────
# A-3.8 — ARIA Landmarks
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("A-3.8 ARIA LANDMARKS E ROLES")
print("="*60)

landmark_issues = []
for page in ROOT_PAGES[:10]:  # Amostra de 10 páginas
    with open(page) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    has_main = bool(soup.find('main')) or bool(soup.find(attrs={'role': 'main'}))
    has_nav = bool(soup.find('nav')) or bool(soup.find(attrs={'role': 'navigation'}))
    has_header = bool(soup.find('header')) or bool(soup.find(attrs={'role': 'banner'}))
    has_footer = bool(soup.find('footer')) or bool(soup.find(attrs={'role': 'contentinfo'}))
    issues = []
    if not has_main: issues.append('sem <main>')
    if not has_nav: issues.append('sem <nav>')
    if not has_header: issues.append('sem <header>')
    if not has_footer: issues.append('sem <footer>')
    status = '✅' if not issues else '⚠️ ' + ', '.join(issues)
    print(f"  {page}: {status}")

# ─────────────────────────────────────────────────────────────
# A-3.9 — lang attribute
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("A-3.9 LANG ATTRIBUTE")
print("="*60)

wrong_lang = []
for page in ROOT_PAGES:
    with open(page) as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    html_tag = soup.find('html')
    lang = html_tag.get('lang', '') if html_tag else ''
    expected = 'en' if page.startswith('en/') else ('es' if page.startswith('es/') else 'pt-BR')
    if not lang:
        wrong_lang.append((page, 'AUSENTE', expected))
    elif not lang.startswith(expected.split('-')[0]):
        wrong_lang.append((page, lang, expected))

print(f"\n  Páginas com lang incorreto ou ausente: {len(wrong_lang)}")
for p, got, exp in wrong_lang[:10]:
    print(f"    {p}: lang='{got}' (esperado: '{exp}')")

# ─────────────────────────────────────────────────────────────
# A-3.10 — tabindex > 0
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("A-3.10 TABINDEX > 0 (ANTIPADRÃO)")
print("="*60)

tabindex_issues = []
for page in ROOT_PAGES:
    with open(page) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    for el in soup.find_all(attrs={'tabindex': True}):
        try:
            val = int(el.get('tabindex', 0))
            if val > 0:
                tabindex_issues.append((page, el.name, val))
        except: pass

print(f"\n  Elementos com tabindex > 0: {len(tabindex_issues)}")
for p, tag, val in tabindex_issues[:5]:
    print(f"    {p}: <{tag} tabindex={val}>")

# ─────────────────────────────────────────────────────────────
# A-3.11 — Links sem texto descritivo
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("A-3.11 LINKS SEM TEXTO DESCRITIVO")
print("="*60)

empty_links = []
for page in ROOT_PAGES:
    with open(page) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        aria_label = a.get('aria-label', '')
        aria_labelledby = a.get('aria-labelledby', '')
        title = a.get('title', '')
        if not text and not aria_label and not aria_labelledby and not title:
            # Verificar se tem imagem com alt
            img = a.find('img')
            if img and img.get('alt', '').strip():
                continue
            empty_links.append((page, a.get('href', '')[:60]))

print(f"\n  Links sem texto acessível: {len(empty_links)}")
for p, href in empty_links[:10]:
    print(f"    {p}: href={href}")

# ─────────────────────────────────────────────────────────────
# A-3.12 — Hierarquia de headings
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("A-3.12 HIERARQUIA DE HEADINGS")
print("="*60)

heading_issues = []
for page in ROOT_PAGES:
    with open(page) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    headings = [(int(h.name[1]), h.get_text(strip=True)[:50])
                for h in soup.find_all(['h1','h2','h3','h4','h5','h6'])]
    h1_count = sum(1 for level, _ in headings if level == 1)
    # Verificar saltos de nível
    skips = []
    for i in range(1, len(headings)):
        prev_level, _ = headings[i-1]
        curr_level, curr_text = headings[i]
        if curr_level > prev_level + 1:
            skips.append(f"H{prev_level}→H{curr_level}: '{curr_text}'")
    if h1_count != 1 or skips:
        heading_issues.append((page, h1_count, skips))

print(f"\n  Páginas com problemas de hierarquia: {len(heading_issues)}")
for p, h1c, skips in heading_issues[:8]:
    issues = []
    if h1c != 1: issues.append(f"{h1c} H1s")
    issues.extend(skips[:2])
    print(f"    {p}: {', '.join(issues)}")

# ─────────────────────────────────────────────────────────────
# A-3.13 — Botões sem aria-label
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("A-3.13 BOTÕES SEM ARIA-LABEL")
print("="*60)

btn_issues = []
for page in ROOT_PAGES:
    with open(page) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    for btn in soup.find_all(['button', 'input']):
        if btn.name == 'input' and btn.get('type') not in ('button','submit','reset'):
            continue
        text = btn.get_text(strip=True)
        aria_label = btn.get('aria-label', '')
        aria_labelledby = btn.get('aria-labelledby', '')
        title = btn.get('title', '')
        if not text and not aria_label and not aria_labelledby and not title:
            btn_issues.append((page, str(btn)[:80]))

print(f"\n  Botões sem texto acessível: {len(btn_issues)}")
for p, btn in btn_issues[:5]:
    print(f"    {p}: {btn}")

# ─────────────────────────────────────────────────────────────
# A-3.14 — iframes sem title
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("A-3.14 IFRAMES SEM TITLE")
print("="*60)

iframe_issues = []
for page in ROOT_PAGES:
    with open(page) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    for iframe in soup.find_all('iframe'):
        if not iframe.get('title'):
            iframe_issues.append((page, iframe.get('src', '')[:60]))

print(f"\n  iframes sem title: {len(iframe_issues)}")
for p, src in iframe_issues[:5]:
    print(f"    {p}: src={src}")

# ─────────────────────────────────────────────────────────────
# RESUMO EXECUTIVO
# ─────────────────────────────────────────────────────────────
print()
print("="*60)
print("RESUMO EXECUTIVO — FASE 3")
print("="*60)
print(f"""
  Critério                          Status
  ─────────────────────────────────────────────────────
  A-3.1  Contraste AA               {len(failures_aa)} falhas críticas
  A-3.1  Contraste AAA              {len(failures_aaa)} melhorias necessárias
  A-3.2  Tag <main>                 {len(no_main)} páginas sem <main>
  A-3.3  Skip link                  {len(no_skip)} páginas sem skip link
  A-3.4  :focus-visible CSS         verificar output acima
  A-3.5  prefers-reduced-motion     verificar output acima
  A-3.6  Imagens sem alt            {total_no_alt} imagens
  A-3.6  Alt vazio sem role         {total_empty} imagens
  A-3.7  Inputs sem label           {len(form_issues)} inputs
  A-3.9  lang incorreto             {len(wrong_lang)} páginas
  A-3.10 tabindex > 0               {len(tabindex_issues)} elementos
  A-3.11 Links sem texto            {len(empty_links)} links
  A-3.12 Hierarquia headings        {len(heading_issues)} páginas
  A-3.13 Botões sem aria-label      {len(btn_issues)} botões
  A-3.14 iframes sem title          {len(iframe_issues)} iframes
""")
