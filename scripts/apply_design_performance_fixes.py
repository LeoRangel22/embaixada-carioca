#!/usr/bin/env python3
"""
Auditoria e correção de Design + Performance — Embaixada Carioca.

Foco:
- detectar hero quebrado / sem imagem;
- corrigir a página entardecer.html que ficou sem fundo por tag de imagem corrompida;
- adicionar preload do hero nas páginas internas prioritárias;
- detectar HTML excessivamente pesado;
- gerar relatório objetivo para design, UX visual e performance percebida.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT: list[str] = []
WARNINGS: list[str] = []

PRIORITY_PAGES = [
    "index.html",
    "cafe-da-manha.html",
    "almoco.html",
    "entardecer.html",
    "eventos.html",
    "cardapio.html",
    "guia-do-rio.html",
    "en/index.html",
    "en/cafe-da-manha.html",
    "en/almoco.html",
    "en/entardecer.html",
    "en/sunset.html",
    "en/eventos.html",
    "es/index.html",
    "es/cafe-da-manha.html",
    "es/almoco.html",
    "es/entardecer.html",
    "es/atardecer.html",
    "es/eventos.html",
]

BROKEN_HERO_PATTERNS = [
    "<entardecer no Morro da Urca com o Pão de Açúcar em primeiro planoiority=\"high\" src=\"/assets/hero.webp\">",
    "<entardecer no Morro da Urca com o Pão de Açúcar em primeiro planoiority='high' src='/assets/hero.webp'>",
]

ENTARDECER_HERO = '''<picture class="page-hero-photo">
  <source srcset="/assets/hero.webp" type="image/webp" />
  <img src="/assets/hero.jpg" alt="Entardecer no Morro da Urca com o Pão de Açúcar em primeiro plano — Embaixada Carioca" loading="eager" fetchpriority="high" decoding="async" />
</picture>'''

PRELOADS = {
    "index.html": "/assets/hero.webp",
    "cafe-da-manha.html": "/assets/hero.webp",
    "almoco.html": "/assets/hero.webp",
    "entardecer.html": "/assets/hero.webp",
    "eventos.html": "/assets/hero.webp",
    "cardapio.html": "/assets/hero.webp",
    "guia-do-rio.html": "/assets/hero.webp",
}

DESIGN_REPLACEMENTS = {
    # Headings/factual copy on entardecer page
    "Pôr do sol<br/>\n<span class=\"serif\">sobre a baía</span> — o entardecer mais bonito do Rio.":
    "Entardecer<br/>\n<span class=\"serif\">no Morro da Urca</span> — drinks, petiscos e Pão de Açúcar.",
    "Cada gole, <span class=\"serif\">o sol descendo</span> — o melhor entardecer do Rio de Janeiro.":
    "Cada gole, <span class=\"serif\">o Rio em cena</span> — caipirinhas, drinks e petiscos no Morro da Urca.",
    "tudo com a vista sobre Baía de Guanabara":
    "tudo com o Pão de Açúcar em primeiro plano e a Baía de Guanabara na paisagem",
    "pôr do sol sobre a cidade": "entardecer no Morro da Urca",
    "sol se põe sobre o Pão de Açúcar": "entardecer acontece no Morro da Urca com o Pão de Açúcar em primeiro plano",
}


def add_preload(text: str, image_path: str) -> tuple[str, int]:
    if f'rel="preload"' in text and image_path in text:
        return text, 0
    preload = f'<link rel="preload" as="image" href="{image_path}" fetchpriority="high" />\n'
    if "<meta charset" in text:
        return text.replace("<meta charset", preload + "<meta charset", 1), 1
    if "<head>" in text:
        return text.replace("<head>", "<head>\n" + preload, 1), 1
    return text, 0


def fix_page(path: Path) -> None:
    if not path.exists():
        return
    rel = path.relative_to(ROOT).as_posix()
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    count = 0

    # Corrigir hero quebrado na página de entardecer.
    for broken in BROKEN_HERO_PATTERNS:
        if broken in text:
            text = text.replace(broken, ENTARDECER_HERO)
            count += 1

    # Corrigir variações de tag corrompida que comecem com <entardecer ... src="/assets/hero.webp">
    text, c = re.subn(r"<entardecer[^>]*src=[\"']/assets/hero\.webp[\"'][^>]*>", ENTARDECER_HERO, text, flags=re.I)
    count += c

    for old, new in DESIGN_REPLACEMENTS.items():
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            count += c

    # Preload de hero para páginas PT prioritárias.
    if rel in PRELOADS:
        text, c = add_preload(text, PRELOADS[rel])
        count += c

    # Garantir mínimo visual para hero sem imagem: fallback gradiente + altura menor em desktop.
    if ".page-hero" in text and "/* Design fallback 95 */" not in text:
        fallback_css = '''\n<style>\n/* Design fallback 95 */\n.page-hero{background:linear-gradient(135deg,#071a23 0%,#0d1f29 48%,#123241 100%);}\n.page-hero-photo img,.page-hero-photo{filter:saturate(1.02) contrast(1.02);}\n@media (min-width: 961px){.page-hero{min-height:72vh}.page-hero-content{padding-top:160px}}\n</style>\n'''
        text = text.replace("</head>", fallback_css + "</head>", 1)
        count += 1

    if text != original:
        path.write_text(text, encoding="utf-8")
        REPORT.append(f"UPDATED: {rel} | changes={count}")


def audit_page(path: Path) -> None:
    if not path.exists():
        return
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="ignore")
    size_kb = len(text.encode("utf-8")) / 1024

    if size_kb > 450:
        WARNINGS.append(f"{rel}: HTML muito pesado ({size_kb:.0f} KB). Recomenda-se extrair CSS inline para arquivo compartilhado e reduzir JSON-LD/FAQ duplicado.")
    if "<entardecer" in text:
        WARNINGS.append(f"{rel}: tag hero corrompida ainda presente.")
    if "class=\"page-hero\"" in text and "page-hero-photo" not in text:
        WARNINGS.append(f"{rel}: page-hero sem imagem .page-hero-photo.")
    if rel in PRELOADS and PRELOADS[rel] not in text:
        WARNINGS.append(f"{rel}: sem preload da imagem principal.")
    if text.count("<style") > 8:
        WARNINGS.append(f"{rel}: excesso de blocos <style> inline ({text.count('<style')}). Impacta manutenção e performance percebida.")
    if text.count("FAQPage") > 1:
        WARNINGS.append(f"{rel}: possível FAQ/schema duplicado.")


def main() -> int:
    for rel in PRIORITY_PAGES:
        fix_page(ROOT / rel)

    for rel in PRIORITY_PAGES:
        audit_page(ROOT / rel)

    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report = report_dir / "design_performance_report.md"
    score = 96 if not WARNINGS else max(72, 96 - min(24, len(WARNINGS) * 2))
    report.write_text(
        "# Auditoria Design + Performance — Embaixada Carioca\n\n"
        "## Correções aplicadas\n"
        + ("\n".join(f"- {line}" for line in REPORT) if REPORT else "- Nenhuma correção automática necessária")
        + "\n\n## Alertas de design/performance\n"
        + ("\n".join(f"- {w}" for w in WARNINGS) if WARNINGS else "- Nenhum alerta crítico nas páginas prioritárias")
        + f"\n\n## Score estimado Design/Performance\n- {score}/100\n\n"
        "## Critérios\n"
        "- Hero com imagem válida e fallback visual.\n"
        "- Preload da imagem principal nas páginas PT prioritárias.\n"
        "- Detecção de HTML excessivamente pesado.\n"
        "- Detecção de CSS inline excessivo.\n"
        "- Detecção de schema/FAQ duplicado.\n",
        encoding="utf-8",
    )
    print(report.read_text(encoding="utf-8"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
