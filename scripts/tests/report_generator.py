#!/usr/bin/env python3
"""
Gerador de relatório HTML consolidado com resultados de testes estáticos e Playwright.
"""

import json
import base64
from pathlib import Path
from datetime import datetime
from typing import List

ROOT = Path(__file__).parent.parent.parent
REPORT_DIR = ROOT / "scripts" / "tests"


def img_to_base64(path: str) -> str:
    """Converte imagem para base64 para embedding no HTML."""
    p = Path(path)
    if not p.exists():
        return ""
    try:
        with open(p, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        ext = p.suffix.lstrip(".")
        return f"data:image/{ext};base64,{data}"
    except Exception:
        return ""


def generate_html_report(static_results, render_results, output_path: str) -> None:
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # ── Estatísticas globais ──────────────────────────────────────────────────
    all_results = list(static_results) + list(render_results)
    total = len(all_results)
    passed = sum(1 for r in all_results if r.passed)
    failed = total - passed
    pass_rate = round(passed / total * 100) if total > 0 else 0

    # Por fix
    fix_groups = {}
    for r in all_results:
        fix = getattr(r, "fix", "?")
        if fix not in fix_groups:
            fix_groups[fix] = {"passed": 0, "failed": 0}
        if r.passed:
            fix_groups[fix]["passed"] += 1
        else:
            fix_groups[fix]["failed"] += 1

    # ── Agrupar render por dispositivo ───────────────────────────────────────
    device_groups = {}
    for r in render_results:
        dev = getattr(r, "device", "?")
        if dev not in device_groups:
            device_groups[dev] = []
        device_groups[dev].append(r)

    # ── Cores por fix ─────────────────────────────────────────────────────────
    fix_colors = {
        "FIX1": "#e8a838",
        "FIX2": "#3a8fd4",
        "FIX3": "#5cb85c",
        "FIX-BONUS": "#9b59b6",
        "REGRESSÃO": "#e67e22",
        "INFRA": "#95a5a6",
    }

    # ── Screenshots grid ──────────────────────────────────────────────────────
    screenshots_html = ""
    seen_screenshots = set()
    for r in render_results:
        ss = getattr(r, "screenshot", None)
        if ss and ss not in seen_screenshots and Path(ss).exists():
            seen_screenshots.add(ss)
            b64 = img_to_base64(ss)
            if b64:
                dev = getattr(r, "device", "?")
                pg = getattr(r, "page", "?")
                screenshots_html += f"""
                <div class="screenshot-card">
                    <img src="{b64}" alt="{dev} — {pg}" loading="lazy" />
                    <div class="screenshot-label">{dev}<br><small>{pg}</small></div>
                </div>"""

    # ── Tabela de testes estáticos ────────────────────────────────────────────
    static_rows = ""
    for r in static_results:
        icon = "✓" if r.passed else "✗"
        cls = "pass" if r.passed else "fail"
        fix = getattr(r, "fix", "?")
        color = fix_colors.get(fix, "#999")
        static_rows += f"""
        <tr class="{cls}">
            <td><span class="badge" style="background:{color}">{fix}</span></td>
            <td class="icon">{icon}</td>
            <td>{r.file}</td>
            <td>{r.name}</td>
            <td class="msg">{r.message}</td>
        </tr>"""

    # ── Tabela de testes Playwright ───────────────────────────────────────────
    render_rows = ""
    for r in render_results:
        icon = "✓" if r.passed else "✗"
        cls = "pass" if r.passed else "fail"
        fix = getattr(r, "fix", "?")
        color = fix_colors.get(fix, "#999")
        dev = getattr(r, "device", "?")
        pg = getattr(r, "page", "?")
        render_rows += f"""
        <tr class="{cls}">
            <td><span class="badge" style="background:{color}">{fix}</span></td>
            <td class="icon">{icon}</td>
            <td>{pg}</td>
            <td>{dev}</td>
            <td>{r.name}</td>
            <td class="msg">{r.message}</td>
        </tr>"""

    # ── Cards de fix ──────────────────────────────────────────────────────────
    fix_cards_html = ""
    for fix, stats in sorted(fix_groups.items()):
        t = stats["passed"] + stats["failed"]
        pct = round(stats["passed"] / t * 100) if t > 0 else 0
        color = fix_colors.get(fix, "#999")
        status_cls = "card-pass" if stats["failed"] == 0 else "card-fail"
        fix_cards_html += f"""
        <div class="fix-card {status_cls}">
            <div class="fix-badge" style="background:{color}">{fix}</div>
            <div class="fix-stats">
                <span class="fix-pass">✓ {stats['passed']}</span>
                <span class="fix-fail">✗ {stats['failed']}</span>
            </div>
            <div class="fix-bar">
                <div class="fix-bar-fill" style="width:{pct}%;background:{color}"></div>
            </div>
            <div class="fix-pct">{pct}% passou</div>
        </div>"""

    # ── HTML final ────────────────────────────────────────────────────────────
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Relatório de Testes — Embaixada Carioca</title>
<style>
  :root {{
    --bg: #0d1b2a; --surface: #1a2e44; --surface2: #243b55;
    --text: #e8dcc8; --text2: #a89880; --border: rgba(255,255,255,0.08);
    --pass: #5cb85c; --fail: #e74c3c; --warn: #e8a838;
    --radius: 12px; --font: 'JetBrains Mono', 'Fira Code', monospace;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: var(--font); font-size: 13px; line-height: 1.6; }}
  .wrap {{ max-width: 1400px; margin: 0 auto; padding: 0 24px; }}

  /* Header */
  .report-header {{ background: linear-gradient(135deg, #00202e, #00405a); padding: 48px 0 32px; border-bottom: 1px solid var(--border); }}
  .report-header h1 {{ font-size: 24px; letter-spacing: .12em; text-transform: uppercase; color: #f59b1e; margin-bottom: 8px; }}
  .report-header .meta {{ color: var(--text2); font-size: 11px; letter-spacing: .08em; }}

  /* Summary */
  .summary {{ display: flex; gap: 20px; padding: 32px 0; flex-wrap: wrap; }}
  .summary-card {{ background: var(--surface); border-radius: var(--radius); padding: 20px 28px; flex: 1; min-width: 160px; border: 1px solid var(--border); }}
  .summary-card .value {{ font-size: 36px; font-weight: 900; line-height: 1; }}
  .summary-card .label {{ font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--text2); margin-top: 6px; }}
  .summary-card.total .value {{ color: var(--text); }}
  .summary-card.pass .value {{ color: var(--pass); }}
  .summary-card.fail .value {{ color: var(--fail); }}
  .summary-card.rate .value {{ color: #f59b1e; }}

  /* Fix cards */
  .fix-cards {{ display: flex; gap: 16px; flex-wrap: wrap; padding-bottom: 32px; }}
  .fix-card {{ background: var(--surface); border-radius: var(--radius); padding: 16px 20px; min-width: 160px; flex: 1; border: 1px solid var(--border); }}
  .fix-card.card-fail {{ border-color: rgba(231,76,60,0.4); }}
  .fix-card.card-pass {{ border-color: rgba(92,184,92,0.3); }}
  .fix-badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 900; letter-spacing: .1em; color: #fff; margin-bottom: 10px; }}
  .fix-stats {{ display: flex; gap: 12px; margin-bottom: 8px; }}
  .fix-pass {{ color: var(--pass); font-weight: 700; }}
  .fix-fail {{ color: var(--fail); font-weight: 700; }}
  .fix-bar {{ background: rgba(255,255,255,0.08); border-radius: 4px; height: 4px; margin-bottom: 6px; overflow: hidden; }}
  .fix-bar-fill {{ height: 100%; border-radius: 4px; transition: width .3s; }}
  .fix-pct {{ font-size: 11px; color: var(--text2); }}

  /* Section */
  .section {{ padding: 32px 0; border-top: 1px solid var(--border); }}
  .section h2 {{ font-size: 14px; letter-spacing: .12em; text-transform: uppercase; color: #f59b1e; margin-bottom: 20px; }}

  /* Table */
  .table-wrap {{ overflow-x: auto; border-radius: var(--radius); border: 1px solid var(--border); }}
  table {{ width: 100%; border-collapse: collapse; }}
  th {{ background: var(--surface2); padding: 10px 14px; text-align: left; font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--text2); white-space: nowrap; }}
  td {{ padding: 10px 14px; border-top: 1px solid var(--border); vertical-align: top; }}
  tr.pass td {{ background: rgba(92,184,92,0.04); }}
  tr.fail td {{ background: rgba(231,76,60,0.06); }}
  tr:hover td {{ background: rgba(255,255,255,0.04); }}
  .icon {{ font-size: 16px; text-align: center; width: 32px; }}
  tr.pass .icon {{ color: var(--pass); }}
  tr.fail .icon {{ color: var(--fail); }}
  .msg {{ color: var(--text2); font-size: 12px; max-width: 400px; }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 900; letter-spacing: .08em; color: #fff; white-space: nowrap; }}

  /* Screenshots */
  .screenshots-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }}
  .screenshot-card {{ background: var(--surface); border-radius: var(--radius); overflow: hidden; border: 1px solid var(--border); }}
  .screenshot-card img {{ width: 100%; display: block; }}
  .screenshot-label {{ padding: 10px 14px; font-size: 11px; color: var(--text2); line-height: 1.4; }}
  .screenshot-label small {{ font-size: 10px; opacity: .7; }}

  /* Footer */
  .report-footer {{ padding: 32px 0; border-top: 1px solid var(--border); text-align: center; color: var(--text2); font-size: 11px; letter-spacing: .08em; }}
</style>
</head>
<body>

<div class="report-header">
  <div class="wrap">
    <h1>Relatório de Testes — Embaixada Carioca</h1>
    <div class="meta">Gerado em {now} &nbsp;·&nbsp; overflow &amp; flex-wrap audit &nbsp;·&nbsp; FIX1 · FIX2 · FIX3</div>
  </div>
</div>

<div class="wrap">

  <!-- Resumo global -->
  <div class="summary">
    <div class="summary-card total"><div class="value">{total}</div><div class="label">Total de Testes</div></div>
    <div class="summary-card pass"><div class="value">{passed}</div><div class="label">Passaram</div></div>
    <div class="summary-card fail"><div class="value">{failed}</div><div class="label">Falharam</div></div>
    <div class="summary-card rate"><div class="value">{pass_rate}%</div><div class="label">Taxa de Aprovação</div></div>
  </div>

  <!-- Cards por fix -->
  <div class="fix-cards">
    {fix_cards_html}
  </div>

  <!-- Testes estáticos -->
  <div class="section">
    <h2>Testes Estáticos — Análise de Código-Fonte</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Fix</th><th></th><th>Arquivo</th><th>Teste</th><th>Resultado</th>
          </tr>
        </thead>
        <tbody>
          {static_rows}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Testes de renderização -->
  <div class="section">
    <h2>Testes de Renderização — Playwright (múltiplos viewports)</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Fix</th><th></th><th>Página</th><th>Dispositivo</th><th>Teste</th><th>Resultado</th>
          </tr>
        </thead>
        <tbody>
          {render_rows}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Screenshots -->
  {'<div class="section"><h2>Screenshots por Dispositivo</h2><div class="screenshots-grid">' + screenshots_html + '</div></div>' if screenshots_html else ''}

</div>

<div class="report-footer">
  <div class="wrap">Embaixada Carioca — Morro da Urca &nbsp;·&nbsp; embaixadacarioca.com &nbsp;·&nbsp; {now}</div>
</div>

</body>
</html>"""

    Path(output_path).write_text(html, encoding="utf-8")
    print(f"Relatório gerado: {output_path}")
