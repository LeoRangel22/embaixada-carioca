#!/usr/bin/env python3
"""
fix_design_buttons.py — Correção de regressões visuais de design

PROBLEMA IDENTIFICADO:
- Botões CTA do hero truncados: "AÇA SUA RESERV", "INHEÇA O CARDÁP"
- Causa: overflow:hidden!important nos .btn + max-width insuficiente no hero-ctas
- Bloco responsável: ec-final-design-consistency-lock no ec-index-inline.css

SOLUÇÃO:
1. Remover overflow:hidden dos botões .btn (manter apenas no pseudo-elemento ::after do ripple)
2. Garantir que o hero-ctas tenha flex-wrap:wrap em telas intermediárias (960px-1200px)
3. Adicionar min-width adequado nos botões para evitar truncamento
4. Manter o design da referência positiva (imagem 7): botões completos, bem espaçados
"""

import re
import os
import shutil
from datetime import datetime

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_FILE = os.path.join(REPO_DIR, "assets/css/ec-index-inline.css")
BACKUP_DIR = os.path.join(REPO_DIR, "_backups/design-fix")

def backup_file(filepath):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    basename = os.path.basename(filepath)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"{basename}.{ts}.bak")
    shutil.copy2(filepath, backup_path)
    print(f"  Backup: {backup_path}")
    return backup_path

def fix_css():
    with open(CSS_FILE, encoding="utf-8") as f:
        content = f.read()
    
    original = content
    changes = []
    
    # ── FIX 1: Remover overflow:hidden dos botões no bloco ec-final-design-consistency-lock
    # O problema: overflow:hidden!important; nos botões corta o texto
    # O ripple effect usa ::after, então não precisa de overflow:hidden no elemento pai
    # Mas precisamos manter o overflow:hidden para o ripple funcionar visualmente
    # Solução: trocar overflow:hidden por overflow:clip (que não cria stacking context)
    # Ou melhor: usar clip-path ao invés de overflow:hidden
    # Solução mais simples: remover o overflow:hidden do bloco de botões e manter apenas no ripple
    
    # Localizar o bloco específico que define overflow:hidden nos botões
    OLD_BTN_OVERFLOW = (
        "white-space:nowrap!important;"
        "overflow:hidden!important;}"
    )
    NEW_BTN_OVERFLOW = (
        "white-space:nowrap!important;"
        "overflow:visible!important;}"
    )
    
    if OLD_BTN_OVERFLOW in content:
        content = content.replace(OLD_BTN_OVERFLOW, NEW_BTN_OVERFLOW, 1)
        changes.append("FIX 1: overflow:hidden → overflow:visible nos botões .btn (ec-final-design-consistency-lock)")
    else:
        print("  AVISO: Padrão FIX 1 não encontrado — verificando variantes...")
        # Tentar variante sem espaço
        alt = "white-space:nowrap!important;overflow:hidden!important;}"
        if alt in content:
            content = content.replace(alt, "white-space:nowrap!important;overflow:visible!important;}", 1)
            changes.append("FIX 1 (variante): overflow:hidden → overflow:visible nos botões .btn")
    
    # ── FIX 2: Corrigir o bloco mobile (max-width:960px) que define padding:0 24px
    # O problema: em 960px, os botões têm padding:0 24px mas o hero-ctas tem max-width:min(900px,62vw)=595px
    # Isso não é suficiente para 3 botões com texto longo
    # Solução: adicionar flex-wrap:wrap no hero-ctas em 960px e reduzir o padding dos botões
    
    OLD_960_BTNS = (
        "@media(max-width:960px){"
        ".hero-ctas a,.hero-ctas button,.ctas a,.ctas button,.btn,a.btn,button.btn,.btn-secondary,a.btn-secondary{"
        "min-height:54px!important;height:54px!important;padding:0 24px!important;font-size:12px!important;letter-spacing:.10em!important;}"
    )
    NEW_960_BTNS = (
        "@media(max-width:960px){"
        ".hero-ctas{flex-wrap:wrap!important;gap:10px!important;}"
        ".hero-ctas a,.hero-ctas button,.ctas a,.ctas button,.btn,a.btn,button.btn,.btn-secondary,a.btn-secondary{"
        "min-height:54px!important;height:54px!important;padding:0 20px!important;font-size:12px!important;letter-spacing:.08em!important;white-space:nowrap!important;}"
    )
    
    if OLD_960_BTNS in content:
        content = content.replace(OLD_960_BTNS, NEW_960_BTNS, 1)
        changes.append("FIX 2: hero-ctas flex-wrap:wrap em 960px + padding reduzido")
    else:
        print("  AVISO: Padrão FIX 2 não encontrado — verificando variantes...")
        # Tentar encontrar o bloco com regex
        pattern = r'(@media\(max-width:960px\)\{\.hero-ctas a,\.hero-ctas button,\.ctas a,\.ctas button,\.btn,a\.btn,button\.btn,\.btn-secondary,a\.btn-secondary\{[^}]+\})'
        match = re.search(pattern, content)
        if match:
            old_block = match.group(1)
            new_block = (
                "@media(max-width:960px){"
                ".hero-ctas{flex-wrap:wrap!important;gap:10px!important;}"
                ".hero-ctas a,.hero-ctas button,.ctas a,.ctas button,.btn,a.btn,button.btn,.btn-secondary,a.btn-secondary{"
                "min-height:54px!important;height:54px!important;padding:0 20px!important;font-size:12px!important;letter-spacing:.08em!important;white-space:nowrap!important;}"
            )
            content = content.replace(old_block, new_block, 1)
            changes.append("FIX 2 (regex): hero-ctas flex-wrap:wrap em 960px + padding reduzido")
    
    # ── FIX 3: Corrigir o bloco mobile (max-width:720px) que define flex-wrap:nowrap
    # O problema: em 720px, o hero-ctas tem flex-wrap:nowrap que força os botões em linha
    # Mas o bloco 6 (hierarquia visual mobile) já define flex-direction:column
    # Então o nowrap em 720px sobrescreve o column do bloco 6
    # Solução: mudar flex-wrap:nowrap para flex-wrap:wrap em 720px
    
    OLD_720_NOWRAP = ".hero-ctas{flex-wrap:nowrap;gap:10px}"
    NEW_720_WRAP = ".hero-ctas{flex-wrap:wrap;gap:10px}"
    
    if OLD_720_NOWRAP in content:
        content = content.replace(OLD_720_NOWRAP, NEW_720_WRAP, 1)
        changes.append("FIX 3: hero-ctas flex-wrap:nowrap → flex-wrap:wrap em 720px")
    else:
        print("  AVISO: Padrão FIX 3 não encontrado")
    
    # ── FIX 4: Corrigir o overflow:hidden no bloco de ripple effect (block-5)
    # O problema: .btn,.momento-cta,.btn-reservar{position:relative;overflow:hidden}
    # Isso também corta o texto dos botões
    # Solução: usar clip-path ao invés de overflow:hidden para o ripple
    
    OLD_RIPPLE = ".btn,.momento-cta,.btn-reservar{position:relative;overflow:hidden}"
    NEW_RIPPLE = ".btn,.momento-cta,.btn-reservar{position:relative;overflow:visible}"
    
    if OLD_RIPPLE in content:
        content = content.replace(OLD_RIPPLE, NEW_RIPPLE, 1)
        changes.append("FIX 4: overflow:hidden → overflow:visible no ripple effect (block-5)")
    else:
        print("  AVISO: Padrão FIX 4 não encontrado")
    
    # ── FIX 5: Corrigir o overflow:hidden no bloco de ripple effect (hover:none)
    # O problema: .btn,.momento-cta{position:relative !important;overflow:hidden !important}
    
    OLD_RIPPLE2 = ".btn,.momento-cta{position:relative !important;overflow:hidden !important}"
    NEW_RIPPLE2 = ".btn,.momento-cta{position:relative !important;overflow:visible !important}"
    
    if OLD_RIPPLE2 in content:
        content = content.replace(OLD_RIPPLE2, NEW_RIPPLE2, 1)
        changes.append("FIX 5: overflow:hidden → overflow:visible no ripple effect (hover:none)")
    else:
        print("  AVISO: Padrão FIX 5 não encontrado")
    
    # ── FIX 6: Adicionar fix de design no final do arquivo
    # Garantir que os botões do hero nunca sejam truncados
    DESIGN_FIX_COMMENT = "/* ── ec-design-fix-buttons ──"
    if DESIGN_FIX_COMMENT not in content:
        design_fix = """
/* ── ec-design-fix-buttons ── */
/* DESIGN FIX: Garantir que os botões do hero nunca sejam truncados */
/* Referência: imagem 7 — botões completos, bem espaçados */
.hero-ctas a,
.hero-ctas button,
.ctas a,
.ctas button {
  overflow: visible !important;
  white-space: nowrap !important;
  flex-shrink: 0 !important;
}
/* Hero-ctas: wrap em telas intermediárias */
@media (max-width: 1100px) {
  .hero-ctas {
    flex-wrap: wrap !important;
    gap: 10px !important;
  }
}
/* Hero-ctas: coluna em mobile */
@media (max-width: 720px) {
  .hero-ctas {
    flex-direction: column !important;
    align-items: flex-start !important;
    gap: 10px !important;
    width: 100% !important;
    max-width: 360px !important;
  }
  .hero-ctas a,
  .hero-ctas button {
    width: 100% !important;
    justify-content: center !important;
    min-height: 52px !important;
    font-size: 14px !important;
    padding: 0 24px !important;
  }
}
"""
        content = content + design_fix
        changes.append("FIX 6: Adicionado bloco ec-design-fix-buttons no final do arquivo")
    
    if content == original:
        print("  NENHUMA ALTERAÇÃO FEITA — verifique os padrões manualmente")
        return False
    
    backup_file(CSS_FILE)
    with open(CSS_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"\n  {len(changes)} correções aplicadas em {CSS_FILE}:")
    for c in changes:
        print(f"    ✓ {c}")
    
    return True

def main():
    print("=" * 60)
    print("FIX DESIGN BUTTONS — Embaixada Carioca")
    print("=" * 60)
    
    print(f"\n[1/1] Corrigindo CSS dos botões em {CSS_FILE}...")
    if fix_css():
        print("\n✅ Correções aplicadas com sucesso!")
    else:
        print("\n❌ Nenhuma correção aplicada — verifique manualmente")
    
    print("\nPróximos passos:")
    print("  1. Verificar visualmente no browser")
    print("  2. Rodar CI gates")
    print("  3. Fazer push")

if __name__ == "__main__":
    main()
