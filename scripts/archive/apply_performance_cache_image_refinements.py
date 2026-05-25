#!/usr/bin/env python3
"""
Performance Cache + Image Refinements — Embaixada Carioca.

Escopo:
- preparar cache headers para Cloudflare Pages / Netlify;
- adicionar Service Worker para cache de assets em visitas repetidas;
- registrar Service Worker em todas as páginas HTML relevantes;
- trocar hero.jpg simples por picture/srcset WebP responsivo quando seguro;
- aplicar loading/decoding em imagens sem mexer no layout.

Observação:
- GitHub Pages puro não permite controlar Cache-Control por arquivo via HTML.
- O arquivo _headers passa a valer se o domínio estiver atrás de Cloudflare Pages/Netlify.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SW_VERSION = "2026-05-19.1"

HEADERS_CONTENT = """# Cache policy for Cloudflare Pages / Netlify
# GitHub Pages may ignore this file. Use Cloudflare in front of GitHub Pages for full effect.

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.webp
  Cache-Control: public, max-age=31536000, immutable

/*.jpg
  Cache-Control: public, max-age=31536000, immutable

/*.png
  Cache-Control: public, max-age=31536000, immutable

/*.svg
  Cache-Control: public, max-age=31536000, immutable

/*.css
  Cache-Control: public, max-age=31536000, immutable

/*.js
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=600, stale-while-revalidate=86400

/
  Cache-Control: public, max-age=600, stale-while-revalidate=86400

/sitemap.xml
  Cache-Control: public, max-age=3600

/robots.txt
  Cache-Control: public, max-age=3600
"""

SW_CONTENT = f"""/* Embaixada Carioca Service Worker — performance cache */
const EC_CACHE = 'ec-static-{SW_VERSION}';
const EC_ASSETS = [
  '/',
  '/assets/fonts/fonts.css',
  '/assets/logo-branco.svg',
  '/assets/hero-400w.webp',
  '/assets/hero-mobile.webp',
  '/assets/hero-800w.webp',
  '/assets/hero-1200w.webp',
  '/assets/hero.webp'
];

self.addEventListener('install', event => {{
  event.waitUntil(
    caches.open(EC_CACHE).then(cache => cache.addAll(EC_ASSETS)).catch(() => null)
  );
  self.skipWaiting();
}});

self.addEventListener('activate', event => {{
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('ec-static-') && k !== EC_CACHE).map(k => caches.delete(k))))
  );
  self.clients.claim();
}});

self.addEventListener('fetch', event => {{
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  const isStatic = /\.(?:webp|jpg|jpeg|png|svg|css|js|woff2?)$/i.test(url.pathname);
  if (isStatic) {{
    event.respondWith(
      caches.match(req).then(cached => cached || fetch(req).then(resp => {{
        const copy = resp.clone();
        caches.open(EC_CACHE).then(cache => cache.put(req, copy)).catch(() => null);
        return resp;
      }}).catch(() => cached))
    );
  }}
}});
"""

SW_REGISTER = """<!-- EC Performance Cache v1 -->
<script id="ec-service-worker-register">
(function(){
  if (!('serviceWorker' in navigator)) return;
  window.addEventListener('load', function(){
    navigator.serviceWorker.register('/sw.js').catch(function(){});
  });
})();
</script>
<!-- /EC Performance Cache v1 -->"""

SW_REGISTER_RE = re.compile(r"\n*<!-- EC Performance Cache v1 -->[\s\S]*?<!-- /EC Performance Cache v1 -->\s*", re.IGNORECASE)
BODY_CLOSE_RE = re.compile(r"</body>", re.IGNORECASE)
HERO_PRELOAD_RE = re.compile(r'<link\s+rel=["\']preload["\']\s+as=["\']image["\']\s+href=["\']/assets/hero\.jpg["\']\s*/?>', re.IGNORECASE)
HERO_IMG_RE = re.compile(r'<picture class=["\']page-hero-photo["\']><img src=["\']/assets/hero\.jpg["\'] alt=["\']([^"\']*)["\']></picture>', re.IGNORECASE)
GENERIC_IMG_RE = re.compile(r'<img\b(?![^>]*\b(?:loading|fetchpriority)=)[^>]*>', re.IGNORECASE)

REPORT: list[str] = []
COUNTERS = {
    "html_scanned": 0,
    "html_updated": 0,
    "sw_registered": 0,
    "hero_preload_optimized": 0,
    "hero_picture_optimized": 0,
    "lazy_images_marked": 0,
}

EXCLUDED = {"home-preview.html"}


def write_static_files() -> None:
    (ROOT / "_headers").write_text(HEADERS_CONTENT, encoding="utf-8")
    (ROOT / "sw.js").write_text(SW_CONTENT, encoding="utf-8")
    REPORT.append("STATIC: _headers criado para Cloudflare/Netlify")
    REPORT.append("STATIC: sw.js criado para cache de assets em visitas repetidas")


def optimize_hero_preload(text: str) -> str:
    def repl(_: re.Match[str]) -> str:
        COUNTERS["hero_preload_optimized"] += 1
        return ('<link rel="preload" as="image" href="/assets/hero-1200w.webp" '
                'imagesrcset="/assets/hero-400w.webp 400w, /assets/hero-mobile.webp 600w, /assets/hero-800w.webp 800w, /assets/hero-1200w.webp 1200w, /assets/hero.webp 1920w" '
                'imagesizes="100vw" fetchpriority="high" type="image/webp">')
    return HERO_PRELOAD_RE.sub(repl, text)


def optimize_hero_picture(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        alt = match.group(1)
        COUNTERS["hero_picture_optimized"] += 1
        return (f'<picture class="page-hero-photo">'
                f'<source type="image/webp" srcset="/assets/hero-400w.webp 400w, /assets/hero-mobile.webp 600w, /assets/hero-800w.webp 800w, /assets/hero-1200w.webp 1200w, /assets/hero.webp 1920w" sizes="100vw">'
                f'<img src="/assets/hero-1200w.webp" alt="{alt}" width="1920" height="1267" fetchpriority="high" decoding="async">'
                f'</picture>')
    return HERO_IMG_RE.sub(repl, text)


def add_lazy_to_non_hero_images(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        if "page-hero-photo" in tag or "brand-logo" in tag or "fetchpriority=" in tag:
            return tag
        if "<img" not in tag:
            return tag
        if "loading=" not in tag:
            tag = tag[:-1] + ' loading="lazy">'
        if "decoding=" not in tag:
            tag = tag[:-1] + ' decoding="async">'
        COUNTERS["lazy_images_marked"] += 1
        return tag
    return GENERIC_IMG_RE.sub(repl, text)


def register_sw(text: str) -> str:
    text = SW_REGISTER_RE.sub("\n", text)
    if BODY_CLOSE_RE.search(text):
        COUNTERS["sw_registered"] += 1
        return BODY_CLOSE_RE.sub(lambda m: SW_REGISTER + "\n" + m.group(0), text, count=1)
    return text


def process_html(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if rel in EXCLUDED or rel.startswith("_") or ".git" in path.parts:
        return
    COUNTERS["html_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    text = optimize_hero_preload(text)
    text = optimize_hero_picture(text)
    text = add_lazy_to_non_hero_images(text)
    text = register_sw(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["html_updated"] += 1
        REPORT.append(f"UPDATED: {rel}")


def write_report() -> None:
    d = ROOT / "_audit_reports"
    d.mkdir(exist_ok=True)
    p = d / "performance_cache_image_refinements_report.md"
    lines = [
        "# Performance Cache + Image Refinements",
        "",
        "## O que foi feito",
        "- Criado `_headers` para cache longo em Cloudflare Pages/Netlify.",
        "- Criado `sw.js` para cache de assets em visitas repetidas.",
        "- Registrado Service Worker nas páginas HTML.",
        "- Hero das páginas de território convertido para WebP responsivo com `srcset`.",
        "- Imagens não críticas recebem `loading=lazy` e `decoding=async` quando seguro.",
        "",
        "## Limite técnico",
        "- Se o site estiver em GitHub Pages puro, o TTL de 10 minutos dos assets pode continuar aparecendo no Lighthouse. Para resolver totalmente, usar Cloudflare/CDN com regra de cache para `/assets/*`.",
        "",
        "## Contadores",
    ]
    for k, v in COUNTERS.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Arquivos", *[f"- {x}" for x in REPORT], ""])
    p.write_text("\n".join(lines), encoding="utf-8")
    print(p.read_text(encoding="utf-8"))


def main() -> int:
    write_static_files()
    for path in sorted(ROOT.rglob("*.html")):
        process_html(path)
    write_report()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
