#!/usr/bin/env python3
"""
Script principal de testes — Embaixada Carioca.
Orquestra testes estáticos + Playwright e gera relatório HTML.

Uso:
    python3 run_tests.py                  # testes estáticos + Playwright (site ao vivo)
    python3 run_tests.py --static-only    # apenas testes estáticos (sem browser)
    python3 run_tests.py --fast           # Playwright com menos viewports
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(Path(__file__).parent))

from static_tests import run_all_static_tests
from report_generator import generate_html_report


def run_playwright_limited(fast: bool = False):
    """Executa testes Playwright com seleção de dispositivos."""
    from playwright_tests import run_playwright_tests, DEVICES, PAGES
    import playwright_tests as pt

    if fast:
        # Apenas 4 viewports representativos
        pt.DEVICES = [
            d for d in DEVICES
            if d["name"] in [
                "Desktop 1440px",
                "Tablet 960px",
                "Mobile 390px (iPhone 14 Pro)",
                "Mobile 360px (Android)",
            ]
        ]
        # Apenas 3 páginas
        pt.PAGES = [p for p in PAGES if p["path"] in ["/", "/almoco.html", "/en/"]]

    return run_playwright_tests()


def main():
    parser = argparse.ArgumentParser(description="Suite de testes — Embaixada Carioca")
    parser.add_argument("--static-only", action="store_true", help="Apenas testes estáticos")
    parser.add_argument("--fast", action="store_true", help="Playwright com menos viewports")
    parser.add_argument("--output", default=None, help="Caminho do relatório HTML de saída")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = args.output or str(ROOT / "scripts" / "tests" / f"report_{timestamp}.html")
    latest_path = str(ROOT / "scripts" / "tests" / "report_latest.html")

    print("\n" + "="*60)
    print("  EMBAIXADA CARIOCA — SUITE DE TESTES")
    print("  overflow & flex-wrap audit: FIX1 · FIX2 · FIX3")
    print("="*60)

    # ── Testes estáticos ──────────────────────────────────────────────────────
    print("\n[1/2] Executando testes estáticos...")
    static_results = run_all_static_tests()
    s_pass = sum(1 for r in static_results if r.passed)
    s_fail = len(static_results) - s_pass
    print(f"      → {s_pass} passaram, {s_fail} falharam ({len(static_results)} total)")

    for r in static_results:
        icon = "✓" if r.passed else "✗"
        print(f"  [{icon}] [{r.fix}] {r.name} ({r.file})")
        if not r.passed:
            print(f"       → {r.message}")

    # ── Testes Playwright ─────────────────────────────────────────────────────
    render_results = []
    if not args.static_only:
        print("\n[2/2] Executando testes de renderização (Playwright)...")
        if args.fast:
            print("      → Modo rápido: 4 viewports × 3 páginas")
        else:
            print(f"      → Modo completo: 10 viewports × 6 páginas")
        try:
            render_results = run_playwright_limited(fast=args.fast)
            r_pass = sum(1 for r in render_results if r.passed)
            r_fail = len(render_results) - r_pass
            print(f"      → {r_pass} passaram, {r_fail} falharam ({len(render_results)} total)")
        except Exception as e:
            print(f"      ✗ Erro nos testes Playwright: {e}")
    else:
        print("\n[2/2] Testes Playwright ignorados (--static-only)")

    # ── Relatório ─────────────────────────────────────────────────────────────
    print(f"\n[Relatório] Gerando HTML...")
    generate_html_report(static_results, render_results, output_path)
    generate_html_report(static_results, render_results, latest_path)

    # ── Resumo final ──────────────────────────────────────────────────────────
    all_results = static_results + render_results
    total = len(all_results)
    passed = sum(1 for r in all_results if r.passed)
    failed = total - passed
    rate = round(passed / total * 100) if total > 0 else 0

    print("\n" + "="*60)
    print(f"  RESULTADO FINAL: {passed}/{total} testes passaram ({rate}%)")
    if failed > 0:
        print(f"  ✗ {failed} teste(s) falharam:")
        for r in all_results:
            if not r.passed:
                dev = getattr(r, "device", "")
                pg = getattr(r, "page", "")
                loc = f" [{dev}] [{pg}]" if dev else ""
                print(f"    • [{r.fix}]{loc} {r.name}")
                print(f"      → {r.message}")
    else:
        print("  ✓ Todos os testes passaram!")
    print("="*60)
    print(f"\n  Relatório: {output_path}")
    print(f"  Último:    {latest_path}\n")

    # Salvar JSON com resultados
    json_path = output_path.replace(".html", ".json")
    results_data = []
    for r in all_results:
        d = {
            "test_id": r.test_id,
            "name": r.name,
            "fix": getattr(r, "fix", ""),
            "passed": r.passed,
            "message": r.message,
            "file": getattr(r, "file", ""),
            "device": getattr(r, "device", ""),
            "page": getattr(r, "page", ""),
        }
        results_data.append(d)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"timestamp": timestamp, "total": total, "passed": passed, "failed": failed, "results": results_data}, f, ensure_ascii=False, indent=2)
    print(f"  JSON:      {json_path}\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
