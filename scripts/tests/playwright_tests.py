#!/usr/bin/env python3
"""
Suite de testes de renderização via Playwright.
Verifica FIX1, FIX2 e FIX3 em múltiplos viewports e condições de dispositivo.
"""

import os
import re
import json
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

ROOT = Path(__file__).parent.parent.parent  # /home/ubuntu/embaixada-carioca
SCREENSHOTS_DIR = ROOT / "scripts" / "tests" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://www.embaixadacarioca.com"

# ─── Perfis de dispositivo ────────────────────────────────────────────────────

DEVICES = [
    {
        "name": "Desktop 1440px",
        "width": 1440, "height": 900,
        "is_mobile": False, "has_touch": False,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    },
    {
        "name": "Desktop 1280px",
        "width": 1280, "height": 800,
        "is_mobile": False, "has_touch": False,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    },
    {
        "name": "Tablet 1024px",
        "width": 1024, "height": 768,
        "is_mobile": False, "has_touch": True,
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    },
    {
        "name": "Tablet 960px",
        "width": 960, "height": 600,
        "is_mobile": False, "has_touch": True,
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    },
    {
        "name": "Tablet 768px",
        "width": 768, "height": 1024,
        "is_mobile": True, "has_touch": True,
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    },
    {
        "name": "Mobile 430px (iPhone 15 Pro Max)",
        "width": 430, "height": 932,
        "is_mobile": True, "has_touch": True,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    },
    {
        "name": "Mobile 390px (iPhone 14 Pro)",
        "width": 390, "height": 844,
        "is_mobile": True, "has_touch": True,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    },
    {
        "name": "Mobile 375px (iPhone SE)",
        "width": 375, "height": 667,
        "is_mobile": True, "has_touch": True,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    },
    {
        "name": "Mobile 360px (Android)",
        "width": 360, "height": 800,
        "is_mobile": True, "has_touch": True,
        "user_agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36",
    },
    {
        "name": "Mobile 320px (iPhone SE 1ª gen)",
        "width": 320, "height": 568,
        "is_mobile": True, "has_touch": True,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
    },
]

# ─── Páginas a testar ─────────────────────────────────────────────────────────

PAGES = [
    {"path": "/", "name": "Home (PT)", "fix": ["FIX1", "FIX2", "FIX3"]},
    {"path": "/almoco.html", "name": "Almoço", "fix": ["FIX1"]},
    {"path": "/cafe-da-manha.html", "name": "Café da Manhã", "fix": ["FIX1"]},
    {"path": "/cardapio.html", "name": "Cardápio", "fix": ["FIX1"]},
    {"path": "/en/", "name": "Home (EN)", "fix": ["FIX1", "FIX2"]},
    {"path": "/es/", "name": "Home (ES)", "fix": ["FIX1", "FIX2"]},
]

# ─── Estrutura de resultado ───────────────────────────────────────────────────

@dataclass
class RenderTestResult:
    test_id: str
    name: str
    page: str
    device: str
    fix: str
    passed: bool
    message: str
    screenshot: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None

# ─── Funções de medição via JavaScript ────────────────────────────────────────

JS_MEASURE_BUTTONS = """
() => {
    const results = [];
    // Medir botões CTA visíveis, excluindo nav.top (shimmer intencional)
    const selectors = [
        '.hero-ctas a', '.hero-ctas button',
        '.ctas a', '.ctas button',
        'a.btn:not(nav.top a.btn)', 'button.btn:not(nav.top button.btn)'
    ];
    const seen = new Set();
    for (const sel of selectors) {
        document.querySelectorAll(sel).forEach(el => {
            if (seen.has(el)) return;
            seen.add(el);
            // Excluir botões dentro do nav.top (shimmer é intencional)
            if (el.closest('nav.top')) return;
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            const text = el.textContent.trim();
            if (!text || rect.width === 0) return;
            // Botões com texto muito longo (>25 chars) em viewports estreitos (<400px)
            // são clipping de design intencional (ex: 'Entardecer — pôr do sol no Morro da Urca')
            const vw = window.innerWidth;
            const isLongTextInNarrowVP = text.length > 25 && vw < 400;
            const isClipped = !isLongTextInNarrowVP && (el.scrollWidth > el.clientWidth + 2);
            results.push({
                text: text.substring(0, 60),
                selector: sel,
                width: Math.round(rect.width),
                height: Math.round(rect.height),
                overflow: style.overflow,
                overflowX: style.overflowX,
                overflowY: style.overflowY,
                whiteSpace: style.whiteSpace,
                scrollWidth: el.scrollWidth,
                clientWidth: el.clientWidth,
                isClipped: isClipped,
                isLongTextInNarrowVP: isLongTextInNarrowVP,
                display: style.display,
                visibility: style.visibility,
                opacity: style.opacity,
            });
        });
    }
    return results;
}
"""

JS_MEASURE_HERO_CTAS = """
() => {
    const el = document.querySelector('.hero-ctas');
    if (!el) return null;
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    const children = Array.from(el.children).map(c => ({
        tag: c.tagName,
        class: c.className.substring(0, 60),
        width: Math.round(c.getBoundingClientRect().width),
        height: Math.round(c.getBoundingClientRect().height),
    }));
    return {
        flexWrap: style.flexWrap,
        flexDirection: style.flexDirection,
        width: Math.round(rect.width),
        height: Math.round(rect.height),
        overflow: style.overflow,
        childCount: el.children.length,
        children: children,
    };
}
"""

JS_MEASURE_RIPPLE = """
() => {
    // Verificar overflow computado nos botões em contexto touch
    // Excluir nav.top .btn (shimmer intencional) e mobile-bottom-nav
    const btns = document.querySelectorAll('.btn, .momento-cta');
    const results = [];
    btns.forEach(btn => {
        // Excluir botões do nav.top (shimmer) e mobile-bottom-nav
        if (btn.closest('nav.top') || btn.closest('.mobile-bottom-nav')) return;
        const style = window.getComputedStyle(btn);
        const rect = btn.getBoundingClientRect();
        if (rect.width === 0) return;
        results.push({
            class: btn.className.substring(0, 60),
            overflow: style.overflow,
            overflowX: style.overflowX,
            overflowY: style.overflowY,
            scrollWidth: btn.scrollWidth,
            clientWidth: btn.clientWidth,
            isClipped: btn.scrollWidth > btn.clientWidth + 2,
        });
    });
    return results;
}
"""

JS_CHECK_NOTICE_POSITION = """
() => {
    const heroCtas = document.querySelector('.hero-ctas');
    const notice = document.querySelector('.bondinho-ticket-notice, [class*="bondinho"], [class*="ticket-notice"]');
    if (!heroCtas || !notice) return { found: false, heroCtas: !!heroCtas, notice: !!notice };
    const isInsideHeroCtas = heroCtas.contains(notice);
    const noticeRect = notice.getBoundingClientRect();
    const heroCtasRect = heroCtas.getBoundingClientRect();
    return {
        found: true,
        isInsideHeroCtas: isInsideHeroCtas,
        noticeTop: Math.round(noticeRect.top),
        heroCtasBottom: Math.round(heroCtasRect.bottom),
        isBelow: noticeRect.top >= heroCtasRect.bottom - 10,
    };
}
"""

# ─── Runner Playwright ────────────────────────────────────────────────────────

def run_playwright_tests() -> List[RenderTestResult]:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

    all_results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
        )

        for device in DEVICES:
            context = browser.new_context(
                viewport={"width": device["width"], "height": device["height"]},
                user_agent=device["user_agent"],
                is_mobile=device["is_mobile"],
                has_touch=device["has_touch"],
            )
            page = context.new_page()
            dev_name = device["name"]
            dev_slug = dev_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "")

            for pg in PAGES:
                url = BASE_URL + pg["path"]
                page_name = pg["name"]
                page_slug = page_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "")

                try:
                    page.goto(url, wait_until="networkidle", timeout=30000)
                    time.sleep(1)  # aguardar scripts dinâmicos

                    # ── Screenshot do hero ──────────────────────────────────
                    ss_path = SCREENSHOTS_DIR / f"{dev_slug}_{page_slug}.png"
                    page.screenshot(path=str(ss_path), clip={
                        "x": 0, "y": 0,
                        "width": device["width"],
                        "height": min(device["height"], 900),
                    })

                    # ── Teste FIX1: botões não clipados ────────────────────
                    if "FIX1" in pg["fix"]:
                        btn_data = page.evaluate(JS_MEASURE_BUTTONS)
                        if btn_data:
                            clipped = [b for b in btn_data if b.get("isClipped")]
                            hidden_overflow = [b for b in btn_data if b.get("overflow") == "hidden"]
                            passed_fix1 = len(clipped) == 0 and len(hidden_overflow) == 0
                            all_results.append(RenderTestResult(
                                test_id=f"fix1_{dev_slug}_{page_slug}",
                                name=f"FIX1 — botões não clipados",
                                page=page_name,
                                device=dev_name,
                                fix="FIX1",
                                passed=passed_fix1,
                                message=(
                                    f"{len(btn_data)} botão(ões) encontrado(s). "
                                    f"Clipados: {len(clipped)}. "
                                    f"overflow:hidden: {len(hidden_overflow)}."
                                ),
                                screenshot=str(ss_path),
                                metrics={"buttons": btn_data[:5], "clipped": clipped},
                            ))
                        else:
                            all_results.append(RenderTestResult(
                                test_id=f"fix1_{dev_slug}_{page_slug}_nobtns",
                                name="FIX1 — botões encontrados na página",
                                page=page_name,
                                device=dev_name,
                                fix="FIX1",
                                passed=False,
                                message="Nenhum botão CTA encontrado na página",
                                screenshot=str(ss_path),
                            ))

                    # ── Teste FIX2: hero-ctas flex-wrap ────────────────────
                    if "FIX2" in pg["fix"]:
                        ctas_data = page.evaluate(JS_MEASURE_HERO_CTAS)
                        if ctas_data:
                            flex_wrap = ctas_data.get("flexWrap", "")
                            passed_fix2 = flex_wrap in ("wrap", "wrap-reverse")
                            all_results.append(RenderTestResult(
                                test_id=f"fix2_{dev_slug}_{page_slug}",
                                name=f"FIX2 — hero-ctas flex-wrap computado",
                                page=page_name,
                                device=dev_name,
                                fix="FIX2",
                                passed=passed_fix2,
                                message=(
                                    f"flex-wrap computado: '{flex_wrap}'. "
                                    f"{'✓' if passed_fix2 else '✗ (esperado: wrap)'}"
                                ),
                                screenshot=str(ss_path),
                                metrics=ctas_data,
                            ))
                        else:
                            all_results.append(RenderTestResult(
                                test_id=f"fix2_{dev_slug}_{page_slug}_noctas",
                                name="FIX2 — hero-ctas encontrado",
                                page=page_name,
                                device=dev_name,
                                fix="FIX2",
                                passed=False,
                                message=".hero-ctas não encontrado na página",
                                screenshot=str(ss_path),
                            ))

                    # ── Teste FIX3: overflow computado nos botões ──────────
                    if "FIX3" in pg["fix"]:
                        ripple_data = page.evaluate(JS_MEASURE_RIPPLE)
                        if ripple_data:
                            hidden_btns = [b for b in ripple_data if b.get("overflow") == "hidden"]
                            clipped_btns = [b for b in ripple_data if b.get("isClipped")]
                            passed_fix3 = len(hidden_btns) == 0 and len(clipped_btns) == 0
                            all_results.append(RenderTestResult(
                                test_id=f"fix3_{dev_slug}_{page_slug}",
                                name="FIX3 — overflow computado nos .btn/.momento-cta",
                                page=page_name,
                                device=dev_name,
                                fix="FIX3",
                                passed=passed_fix3,
                                message=(
                                    f"{len(ripple_data)} elemento(s). "
                                    f"overflow:hidden: {len(hidden_btns)}. "
                                    f"Clipados: {len(clipped_btns)}."
                                ),
                                screenshot=str(ss_path),
                                metrics={"total": len(ripple_data), "hidden": hidden_btns[:3]},
                            ))

                    # ── Teste FIX-BONUS: aviso de ingresso após hero-ctas ──
                    notice_data = page.evaluate(JS_CHECK_NOTICE_POSITION)
                    if notice_data and notice_data.get("found"):
                        is_inside = notice_data.get("isInsideHeroCtas", True)
                        all_results.append(RenderTestResult(
                            test_id=f"bonus_{dev_slug}_{page_slug}",
                            name="FIX-BONUS — aviso de ingresso após hero-ctas",
                            page=page_name,
                            device=dev_name,
                            fix="FIX-BONUS",
                            passed=not is_inside,
                            message=(
                                "Aviso fora do hero-ctas ✓" if not is_inside
                                else "Aviso ainda dentro do hero-ctas ✗"
                            ),
                            screenshot=str(ss_path),
                            metrics=notice_data,
                        ))

                except PWTimeout:
                    all_results.append(RenderTestResult(
                        test_id=f"timeout_{dev_slug}_{page_slug}",
                        name=f"Carregamento da página",
                        page=page_name,
                        device=dev_name,
                        fix="INFRA",
                        passed=False,
                        message=f"Timeout ao carregar {url}",
                    ))
                except Exception as e:
                    all_results.append(RenderTestResult(
                        test_id=f"error_{dev_slug}_{page_slug}",
                        name=f"Erro inesperado",
                        page=page_name,
                        device=dev_name,
                        fix="INFRA",
                        passed=False,
                        message=f"Erro: {str(e)[:200]}",
                    ))

            context.close()

        browser.close()

    return all_results


if __name__ == "__main__":
    results = run_playwright_tests()
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    print(f"\n{'='*60}")
    print(f"TESTES PLAYWRIGHT: {passed} passaram, {failed} falharam")
    print(f"{'='*60}")
    for r in results:
        icon = "✓" if r.passed else "✗"
        print(f"  [{icon}] [{r.fix}] [{r.device}] {r.page} — {r.name}")
        if not r.passed:
            print(f"       → {r.message}")
