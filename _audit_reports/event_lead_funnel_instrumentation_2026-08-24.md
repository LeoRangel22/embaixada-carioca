# Event Lead Funnel Instrumentation Audit

- Data: 2026-08-24
- Status geral: **PASS**
- Escopo: funil de solicitação de eventos em PT, EN e ES

## Eventos instrumentados

- `ec_event_form_view`
- `ec_event_form_cta_click`
- `ec_event_form_start`
- `ec_event_form_submit_attempt`
- `ec_event_form_validation_error`
- `ec_event_form_valid`
- `ec_event_lead_outbound` (evento já existente e preservado)

## Privacidade e segmentação

- Nenhum nome, telefone, e-mail, data ou mensagem é enviado pelo novo instrumento.
- O tipo de evento é convertido em categoria normalizada.
- O número de convidados é convertido em faixa (`1-20`, `21-50`, `51-100`, `101-150`, `151_plus`).
- Idioma, caminho da página, posição do CTA e destino do CTA são registrados.

## Validação do ativo

- asset_exists: **PASS**
- all_funnel_events_present: **PASS**
- event_format_group_present: **PASS**
- guest_count_band_present: **PASS**
- no_direct_personal_value_payload: **PASS**

## Validação por página

| Página | Formulário | Script único | Saída WhatsApp preservada | Status |
|---|---:|---:|---:|---:|
| `eventos.html` | PASS | PASS | PASS | **PASS** |
| `en/eventos.html` | PASS | PASS | PASS | **PASS** |
| `es/eventos.html` | PASS | PASS | PASS | **PASS** |

## Leitura do funil no GA4

1. CTA de orçamento → `ec_event_form_cta_click`.
2. Formulário visto → `ec_event_form_view`.
3. Primeira interação → `ec_event_form_start`.
4. Tentativa de envio → `ec_event_form_submit_attempt`.
5. Erro ou formulário válido → `ec_event_form_validation_error` / `ec_event_form_valid`.
6. Abertura da mensagem pronta → `ec_event_lead_outbound`.

A decisão sobre substituir o fluxo do WhatsApp por envio próprio deve ser tomada após uma janela mínima de 14 dias de dados.
