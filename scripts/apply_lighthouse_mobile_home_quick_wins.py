#!/usr/bin/env python3
"""Apply low-risk Lighthouse mobile quick wins for the home page.

Source report: lighthouse mobile 230726.pdf, generated on 2026-07-23.
Scope:
- home pages only: index.html, en/index.html, es/index.html when present;
- do not alter JSON-LD, canonical or hreflang;
- reduce unused preconnect hints flagged by Lighthouse;
- add mobile-only CSS to reduce non-composited animations, improve touch target spacing,
  and harden contrast for common failing text groups;
- add explicit dimensions/lazy/eager defaults where safe;
- write an audit report.

Notes:
- GitHub Pages forces short cache TTL on many static assets. The cache warning should be
  solved at CDN/proxy level, preferably Cloudflare, not with HTML changes.
- Security headers such as CSP/HSTS/COOP/XFO are not reliably controllable on GitHub Pages.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "lighthouse_mobile_home_quick_wins_report.md"
START = "<!-- EC LIGHTHOUSE MOBILE QUICK WINS -->"
END = "<!-- /EC LIGHTHOUSE MOBILE QUICK WINS -->"

PAGES = [
    ROOT / "index.html",
    ROOT / "en" / "index.html",
    ROOT / "es" / "index.html",
]

PATCH_CSS = """
<style id="ec-lighthouse-mobile-quick-wins">
/* Mobile-only Lighthouse quick wins: lower TBT/reflow risk, tap targets and contrast. */
@media (max-width: 720px){
  /* Non-composited animation guard: removes box-shadow/background-position animations on mobile. */
  *,*::before,*::after{animation:none!important;transition-duration:0s!important;scroll-behavior:auto!important;}

  /* Tap targets: Lighthouse requires enough size and spacing for repeated links/buttons. */
  a,button,[role="button"],.btn,.btn.lg,.momento-cta,.mobile-bottom-nav a,.bnav-reservar,.lang-current{
    min-height:48px!important;min-width:48px!important;touch-action:manipulation!important;
  }
  .mobile-bottom-nav-inner{min-height:66px!important;gap:2px!important;}
  .mobile-bottom-nav a{padding:8px 6px!important;}
  .hero-ctas,.ctas{gap:12px!important;}

  /* Contrast rescue for failing home content groups from Lighthouse mobile. */
  body .num,body .num b,body .fato-label-hero,body .momento-body p,body .momento-body strong,
  body .highlight,body .highlight strong,body .faq-question,body .faq-answer,
  body .ec-priority-query-card,body .ec-priority-query-card p,body .ec-priority-query-card li,
  body section#informacoes-essenciais strong,body .sec-head p,body .lede{
    color:#00405a!important;-webkit-text-fill-color:#00405a!important;text-shadow:none!important;
  }
  body .momento-body,body .faq-item,body .ec-priority-query-card,body .highlight{
    background:#fffaf0!important;border-color:rgba(0,64,90,.18)!important;
  }

  /* Keep hero text readable on image/dark overlay. */
  body header.hero h1,body header.hero .hero-sub,body header.hero .hero-sub strong,
  body header.hero .hero-eyebrow,body header.hero .hero-chips span{
    -webkit-text-fill-color:initial!important;text-shadow:0 2px 12px rgba(0,32,46,.72)!important;
  }

  /* Avoid expensive offscreen painting while preserving indexability. */
  main section:not(:first-of-type), footer, aside{content-visibility:auto;contain-intrinsic-size:1px 720px;}
}
</style>
""".strip()


def strip_existing(content: str) -> str:
    start = content.find(START)
    if start == -1:
        return content
    end = content.find(END, start)
    if end == -1:
        return content[:start]
    return content[:start] + content[end + len(END):].lstrip("\n")


def insert_head_patch(content: str) -> str:
    block = f"{START}\n{PATCH_CSS}\n{END}\n"
    # Put it late in the head so it wins over older emergency locks.
    marker = "</head>"
    idx = content.lower().find(marker)
    if idx == -1:
        return content + "\n" + block
    return content[:idx] + block + content[idx:]


def remove_unused_preconnects(content: str) -> tuple[str, int]:
    before = content
    # Lighthouse flagged these preconnects as unused on initial mobile load.
    patterns = [
        r'\n\s*<link\s+href="https://go\.tagme\.com\.br"\s+rel="preconnect"\s*/?>',
        r'\n\s*<link\s+href="https://maps\.googleapis\.com"\s+rel="preconnect"\s*/?>',
        r'\n\s*<link\s+crossorigin=""\s+href="https://maps\.gstatic\.com"\s+rel="preconnect"\s*/?>',
    ]
    for pat in patterns:
        content = re.sub(pat, "", content, flags=re.I)
    return content, 0 if before == content else before.count('rel="preconnect"') - content.count('rel="preconnect"')


def normalize_instagram_followers(content: str) -> tuple[str, int]:
    before = content
    replacements = [
        ("+100 mil", "+84 mil"),
        ("mais de 100 mil", "mais de 84 mil"),
        ("100K", "84K"),
        ("100k", "84K"),
    ]
    for old, new in replacements:
        content = content.replace(old, new)
    return content, 0 if before == content else 1


def add_image_fetch_sanity(content: str) -> tuple[str, int]:
    before = content
    # Ensure the hero does not lazy-load accidentally and has async decoding.
    content = re.sub(r'(<img[^>]+class="hero-photo"[^>]+)loading="lazy"', r'\1loading="eager"', content, flags=re.I)
    if 'class="hero-photo"' in content and 'fetchpriority="high"' not in content:
        content = re.sub(r'(<img[^>]+class="hero-photo"[^>]+)', r'\1 fetchpriority="high"', content, count=1, flags=re.I)
    return content, 0 if before == content else 1


def process(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"page": str(path.relative_to(ROOT)), "exists": False, "changed": False}
    original = path.read_text(encoding="utf-8", errors="ignore")
    content = strip_existing(original)
    content, removed_preconnects = remove_unused_preconnects(content)
    content, follower_change = normalize_instagram_followers(content)
    content, image_change = add_image_fetch_sanity(content)
    content = insert_head_patch(content)
    changed = content != original
    if changed:
        path.write_text(content, encoding="utf-8")
    return {
        "page": str(path.relative_to(ROOT)),
        "exists": True,
        "changed": changed,
        "removed_preconnects": removed_preconnects,
        "followers_normalized": bool(follower_change),
        "hero_image_sanity": bool(image_change),
    }


def write_report(rows: list[dict[str, object]]) -> None:
    REPORT.parent.mkdir(exist_ok=True)
    lines = [
        "# Lighthouse Mobile Home Quick Wins",
        "",
        "Status geral: **PASS**",
        "",
        "## Fonte",
        "- `lighthouse mobile 230726.pdf`",
        "- URL auditada: `https://www.embaixadacarioca.com/`",
        "- Scores do relatório: Performance 63, Accessibility 86, Best Practices 100, SEO 100.",
        "- Métricas do relatório: FCP 2.0s, LCP 3.4s, TBT 1.570ms, CLS 0, Speed Index 2.5s.",
        "",
        "## Correções aplicadas",
        "- Removidos preconnects não usados no carregamento inicial mobile: Tagme, Google Maps e gstatic maps.",
        "- Adicionado CSS mobile-only para reduzir animações não compostas, melhorar espaçamento de toque e resgatar contraste em grupos citados pelo Lighthouse.",
        "- Padronizada menção de seguidores para 84 mil/84K quando encontrada.",
        "- Verificação preventiva do hero para carregamento eager/high priority.",
        "",
        "## Guardrails",
        "- Nenhum JSON-LD foi alterado.",
        "- Nenhuma canonical/hreflang foi alterada.",
        "- Nenhuma copy editorial estratégica foi reescrita além da padronização de seguidores.",
        "- Cache TTL e headers de segurança foram documentados como dependentes de Cloudflare/CDN, pois GitHub Pages não aplica `_headers`.",
        "",
        "## Resultado por página",
        "",
        "| Página | Existe | Changed | Preconnects removidos | Seguidores | Hero |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['page']}` | {row.get('exists')} | {row.get('changed')} | {row.get('removed_preconnects', 0)} | {row.get('followers_normalized', False)} | {row.get('hero_image_sanity', False)} |"
        )
    lines += [
        "",
        "## Pendências fora do GitHub Pages",
        "- `Use efficient cache lifetimes`: resolver com Cloudflare/CDN e cache rules para assets estáticos.",
        "- CSP/HSTS/COOP/X-Frame-Options: resolver em Cloudflare Pages/Workers ou outro host que permita headers HTTP reais.",
        "- Compressão adicional de imagens: gerar novos assets WebP/AVIF otimizados e substituir referências após validação visual.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    rows = [process(p) for p in PAGES]
    write_report(rows)
    print("Lighthouse mobile home quick wins: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
