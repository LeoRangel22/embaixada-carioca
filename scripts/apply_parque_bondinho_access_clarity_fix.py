#!/usr/bin/env python3
"""Clarify access/ticket rules on parque-bondinho.html.

Business rule to enforce:
- Usual access to Embaixada Carioca/Morro da Urca is by Parque Bondinho ticket.
- Alternative access is the Morro da Urca trail when open.
- If the visitor reaches Morro da Urca by trail and stays there, no ticket is needed.
- Ticket payment is needed to use the cable car: either to continue to Pão de Açúcar
  or to go down to Praia Vermelha by cable car.

This script only changes visible editorial content and meta description. It does not touch JSON-LD.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "parque_bondinho_access_clarity_fix_report.md"
PAGE = ROOT / "parque-bondinho.html"

BLOCK_START = "<!-- EC PARQUE BONDINHO ACCESS CLARITY FIX -->"
BLOCK_END = "<!-- /EC PARQUE BONDINHO ACCESS CLARITY FIX -->"
STYLE_ID = "ec-parque-bondinho-access-clarity-css"

META_DESC_RE = re.compile(r"<meta\b(?=[^>]*name=[\"']description[\"'])(?=[^>]*content=[\"'][^\"']*[\"'])[^>]*>", re.I | re.S)
OG_DESC_RE = re.compile(r"<meta\b(?=[^>]*property=[\"']og:description[\"'])(?=[^>]*content=[\"'][^\"']*[\"'])[^>]*>", re.I | re.S)

BAD_PATTERNS = [
    # Overly broad or potentially wrong statements are replaced with the precise access rule.
    (
        re.compile(r"A Embaixada Carioca é acessível sem ingresso do bondinho[^<.]*[.]?", re.I),
        "A Embaixada Carioca pode ser acessada pela trilha do Morro da Urca quando ela estiver aberta; nesse caso, o visitante só precisa pagar ingresso se decidir usar o teleférico para subir ao Pão de Açúcar ou descer para a Praia Vermelha.",
    ),
    (
        re.compile(r"Não é necessário comprar ingresso do Bondinho para acessar a Embaixada Carioca[^<.]*[.]?", re.I),
        "Não é necessário comprar ingresso do Bondinho se o acesso for feito pela trilha e a visita ficar restrita ao Morro da Urca; o ingresso é necessário para usar o teleférico.",
    ),
    (
        re.compile(r"É necessário adquirir o bilhete do Parque Bondinho Pão de Açúcar para ter acesso ao local[.]?", re.I),
        "O acesso mais comum é pelo ingresso do Parque Bondinho Pão de Açúcar; a alternativa é subir pela trilha do Morro da Urca quando ela estiver aberta.",
    ),
]


@dataclass
class Result:
    status: str
    changed: bool
    replacements: int
    has_clarity_block: bool
    has_required_phrase: bool


def strip_existing(source: str) -> str:
    return re.sub(re.escape(BLOCK_START) + r"[\s\S]*?" + re.escape(BLOCK_END) + r"\s*", "", source, flags=re.I)


def ensure_style(source: str) -> str:
    if STYLE_ID in source:
        return source
    css = f"""
<style id="{STYLE_ID}">
.ec-access-clarity{{background:#fff8ea;color:#00405a;border-top:1px solid rgba(0,64,90,.10);border-bottom:1px solid rgba(0,64,90,.08);padding:56px 0;font-family:Catamaran,Verdana,system-ui,sans-serif}}
.ec-access-clarity .ec-wrap{{width:min(1080px,calc(100% - 44px));margin:0 auto}}
.ec-access-clarity .ec-kicker{{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#527f8f;margin-bottom:12px}}
.ec-access-clarity h2{{font-size:clamp(28px,3.4vw,48px);line-height:1.08;margin:0 0 16px;color:#00405a;font-weight:900;letter-spacing:-.02em}}
.ec-access-clarity p{{font-size:18px;line-height:1.62;color:#485156;max-width:920px;margin:0 0 18px}}
.ec-access-clarity ul{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px;list-style:none;padding:0;margin:24px 0 0}}
.ec-access-clarity li{{background:#fff;border:1px solid rgba(0,64,90,.12);border-radius:18px;padding:18px;color:#485156;line-height:1.48;box-shadow:0 12px 30px rgba(0,64,90,.05)}}
.ec-access-clarity strong{{color:#335d4a}}
@media(max-width:760px){{.ec-access-clarity{{padding:40px 0}}.ec-access-clarity p{{font-size:16px}}}}
</style>
""".strip()
    if "</head>" in source:
        return source.replace("</head>", css + "\n</head>", 1)
    return css + "\n" + source


def update_meta(source: str) -> str:
    desc = "Como funciona o acesso à Embaixada Carioca no Parque Bondinho: pelo bondinho com ingresso ou pela trilha do Morro da Urca quando aberta; ingresso só para usar teleférico."
    source = META_DESC_RE.sub(f'<meta content="{desc}" name="description"/>', source, count=1)
    source = OG_DESC_RE.sub(f'<meta content="{desc}" property="og:description"/>', source, count=1)
    return source


def clarity_block() -> str:
    return f"""
{BLOCK_START}
<section class="ec-access-clarity" aria-label="Como funciona o acesso ao Morro da Urca e à Embaixada Carioca">
  <div class="ec-wrap">
    <div class="ec-kicker">Acesso ao Morro da Urca</div>
    <h2>Precisa pagar ingresso para chegar à Embaixada Carioca?</h2>
    <p>O acesso mais comum à Embaixada Carioca é pelo <strong>Parque Bondinho Pão de Açúcar</strong>, com ingresso do bondinho até o Morro da Urca. Também existe a alternativa de subir pela <strong>trilha do Morro da Urca</strong>, pela Pista Cláudio Coutinho, quando ela estiver aberta e liberada.</p>
    <p>Se você chegar pela trilha e permanecer apenas no Morro da Urca, <strong>não é necessário pagar ingresso do Bondinho para visitar a Embaixada Carioca</strong>. O ingresso passa a ser necessário se você decidir usar o teleférico para <strong>subir ao Pão de Açúcar</strong> ou para <strong>descer à Praia Vermelha de teleférico</strong>.</p>
    <ul>
      <li><strong>Acesso usual:</strong> entrada pelo Parque Bondinho, na Av. Pasteur, 520, com ingresso do bondinho.</li>
      <li><strong>Alternativa gratuita:</strong> trilha do Morro da Urca quando estiver aberta, respeitando horários e regras do parque.</li>
      <li><strong>Quando paga ingresso:</strong> ao usar o teleférico para subir ao Pão de Açúcar ou para descer à Praia Vermelha.</li>
    </ul>
  </div>
</section>
{BLOCK_END}
""".strip()


def insert_block(source: str, html: str) -> str:
    if "</main>" in source:
        return source.replace("</main>", html + "\n</main>", 1)
    if "</body>" in source:
        return source.replace("</body>", html + "\n</body>", 1)
    return source + "\n" + html


def apply() -> Result:
    if not PAGE.exists():
        return Result("missing", False, 0, False, False)
    original = PAGE.read_text(encoding="utf-8", errors="ignore")
    updated = strip_existing(original)
    replacements = 0
    for pattern, replacement in BAD_PATTERNS:
        updated, count = pattern.subn(replacement, updated)
        replacements += count
    updated = update_meta(updated)
    updated = ensure_style(updated)
    updated = insert_block(updated, clarity_block())
    changed = updated != original
    if changed:
        PAGE.write_text(updated, encoding="utf-8")
    lower = updated.lower()
    required = [
        "trilha do morro da urca",
        "descer à praia vermelha de teleférico",
        "subir ao pão de açúcar",
        "não é necessário pagar ingresso",
    ]
    return Result(
        "ok" if all(term in lower for term in required) else "fail",
        changed,
        replacements,
        BLOCK_START.lower() in lower,
        all(term in lower for term in required),
    )


def write_report(result: Result) -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    status = "PASS" if result.status == "ok" else "FAIL"
    lines = [
        "# Parque Bondinho Access Clarity Fix",
        "",
        f"Status geral: **{status}**",
        "",
        "## Objetivo",
        "Corrigir a inconsistência editorial sobre ingresso/acesso no `parque-bondinho.html`.",
        "",
        "## Regra oficial aplicada",
        "- O acesso usual à Embaixada Carioca é pelo Parque Bondinho, com ingresso do bondinho até o Morro da Urca.",
        "- A alternativa é subir pela trilha do Morro da Urca quando ela estiver aberta.",
        "- Se o visitante chegar pela trilha e permanecer no Morro da Urca, não precisa pagar ingresso do Bondinho para visitar a Embaixada Carioca.",
        "- O ingresso é necessário se o visitante usar o teleférico para subir ao Pão de Açúcar ou descer à Praia Vermelha.",
        "",
        "## Resultado",
        f"- Página: `parque-bondinho.html`",
        f"- Status: `{result.status}`",
        f"- Changed: `{result.changed}`",
        f"- Substituições de frases potencialmente inconsistentes: `{result.replacements}`",
        f"- Bloco de clareza inserido: `{result.has_clarity_block}`",
        f"- Frases obrigatórias presentes: `{result.has_required_phrase}`",
        "",
        "## Guardrails",
        "- Nenhum JSON-LD foi alterado.",
        "- Nenhum schema foi inserido ou removido.",
        "- A alteração é editorial/visível e limitada à regra de acesso.",
    ]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Parque Bondinho access clarity fix: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    return write_report(apply())


if __name__ == "__main__":
    raise SystemExit(main())
