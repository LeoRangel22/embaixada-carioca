# GA4 measurement plan

## Eventos canônicos

| Evento | Momento | Conversão principal |
|---|---|---|
| `ec_event_form_start` | Primeira interação no formulário de eventos | Não |
| `ec_event_lead_outbound` | Abertura da solicitação estruturada no WhatsApp | Sim |
| `ec_reservation_click` | Clique para iniciar reserva | Sim |
| `ec_outbound_conversion_click` | Clique em canal externo de conversão | Conforme o canal |

## Princípios

- Não registrar `form_submit` quando não existe confirmação de recebimento por servidor.
- Não duplicar eventos para a mesma interação.
- Incluir `page_path`, canal e identificação do formulário quando aplicável.
- Considerar como lead confirmado apenas a etapa comprovável no sistema de destino.
