# GA4 — eventos principais e funil atual

**Atualizado em:** 31/08/2026

**Status:** configuração principal concluída; reconciliação Tagme pendente

## Evento principal atual

- `ec_event_lead_outbound` foi marcado como evento principal no GA4 em 27/08/2026.
- Ele representa a saída de alta intenção do fluxo de eventos e deve ser acompanhado por origem, campanha, página e idioma.

## Eventos diagnósticos

Os eventos abaixo ajudam a entender navegação e intenção, mas não devem ser marcados indiscriminadamente como conversões principais:

- `click_reservar`
- `click_whatsapp`
- `click_eventos`
- `click_como_chegar`
- `click_cardapio`
- `click_cafe_da_manha`
- `click_almoco`
- `click_idioma`

Marcar todos como evento principal inflaria a taxa de conversão ao misturar microinterações, navegação e leads reais.

## Medição do formulário de eventos

A instrumentação de funil foi publicada em 24/08/2026. Antes de reconstruir o formulário ou substituir o WhatsApp, medir por pelo menos uma ou duas semanas:

1. visualização/alcance do bloco;
2. início do formulário;
3. avanço/preenchimento;
4. clique de saída para o canal de atendimento;
5. lead efetivamente recebido.

## Pendência prioritária

A Tagme ainda não devolve ao GA4 uma confirmação confiável de reserva concluída. É necessário:

- integrar um evento de confirmação, se a plataforma permitir; ou
- reconciliar cliques com reservas concluídas por data, origem e identificador de campanha.

Sem essa etapa, os cliques em reservar medem intenção, não mesas confirmadas.

## Verificação

1. Validar eventos no Realtime/DebugView.
2. Conferir se `ec_event_lead_outbound` aparece uma única vez por ação.
3. Segmentar por idioma e página de origem.
4. Revisar mensalmente a diferença entre leads, reservas iniciadas e reservas concluídas.
