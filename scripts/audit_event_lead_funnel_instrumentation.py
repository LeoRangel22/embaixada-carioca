from __future__ import annotations

from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "assets" / "event-lead-funnel.js"
REPORT = ROOT / "_audit_reports" / "event_lead_funnel_instrumentation_2026-08-24.md"
PAGES = {
    "eventos.html": "ec-event-lead-form",
    "en/eventos.html": "ec-event-lead-form-en",
    "es/eventos.html": "ec-event-lead-form-es",
}
EVENTS = (
    "ec_event_form_view",
    "ec_event_form_cta_click",
    "ec_event_form_start",
    "ec_event_form_submit_attempt",
    "ec_event_form_validation_error",
    "ec_event_form_valid",
)


def main() -> int:
    asset = ASSET.read_text(encoding="utf-8") if ASSET.exists() else ""
    asset_checks = {
        "asset_exists": ASSET.exists(),
        "all_funnel_events_present": all(event in asset for event in EVENTS),
        "event_format_group_present": "event_format_group" in asset,
        "guest_count_band_present": "guest_count_band" in asset,
        "ga4_delivery_present": "window.gtag('event', eventName" in asset,
        "no_direct_personal_value_payload": not any(
            marker in asset
            for marker in (
                "name_value:",
                "email_value:",
                "phone_value:",
                "contact_value:",
                "message_value:",
                "notes_value:",
            )
        ),
    }

    page_rows = []
    for relative, form_id in PAGES.items():
        html = (ROOT / relative).read_text(encoding="utf-8")
        checks = {
            "form": f'id="{form_id}"' in html,
            "asset_once": html.count("/assets/event-lead-funnel.js") == 1,
            "outbound_preserved": "wa.me/5521966837556" in html and "ec_event_lead_outbound" in asset,
        }
        page_rows.append((relative, checks, all(checks.values())))

    passed = all(asset_checks.values()) and all(row[2] for row in page_rows)
    status = "PASS" if passed else "FAIL"
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Event Lead Funnel Instrumentation Audit",
        "",
        f"- Data: {date.today().isoformat()}",
        f"- Status geral: **{status}**",
        "- Escopo: funil de solicitação de eventos em PT, EN e ES",
        "",
        "## Eventos instrumentados",
        "",
    ]
    lines.extend(f"- `{event}`" for event in EVENTS)
    lines.extend(
        [
            "- `ec_event_lead_outbound` (evento já existente e preservado)",
            "",
            "## Privacidade e segmentação",
            "",
            "- Nenhum nome, telefone, e-mail, data ou mensagem é enviado pelo novo instrumento.",
            "- O tipo de evento é convertido em categoria normalizada.",
            "- O número de convidados é convertido em faixa (`1-20`, `21-50`, `51-100`, `101-150`, `151_plus`).",
            "- Idioma, caminho da página, posição do CTA e destino do CTA são registrados.",
            "",
            "## Validação do ativo",
            "",
        ]
    )
    for name, ok in asset_checks.items():
        lines.append(f"- {name}: **{'PASS' if ok else 'FAIL'}**")

    lines.extend(
        [
            "",
            "## Validação por página",
            "",
            "| Página | Formulário | Script único | Saída WhatsApp + medição preservadas | Status |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for relative, checks, row_passed in page_rows:
        lines.append(
            f"| `{relative}` | {'PASS' if checks['form'] else 'FAIL'} | "
            f"{'PASS' if checks['asset_once'] else 'FAIL'} | "
            f"{'PASS' if checks['outbound_preserved'] else 'FAIL'} | "
            f"**{'PASS' if row_passed else 'FAIL'}** |"
        )

    lines.extend(
        [
            "",
            "## Leitura do funil no GA4",
            "",
            "1. CTA de orçamento → `ec_event_form_cta_click`.",
            "2. Formulário visto → `ec_event_form_view`.",
            "3. Primeira interação → `ec_event_form_start`.",
            "4. Tentativa de envio → `ec_event_form_submit_attempt`.",
            "5. Erro ou formulário válido → `ec_event_form_validation_error` / `ec_event_form_valid`.",
            "6. Abertura da mensagem pronta → `ec_event_lead_outbound`.",
            "",
            "A decisão sobre substituir o fluxo do WhatsApp por envio próprio deve ser tomada após uma janela mínima de 14 dias de dados.",
            "",
        ]
    )
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"{status}: {REPORT.relative_to(ROOT)}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
