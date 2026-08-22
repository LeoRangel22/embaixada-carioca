# Factual integrity and events funnel report

**Status geral: PASS**

## Correções aplicadas

- Removido o identificador fictício do TripAdvisor das homes PT, EN e ES e de `como-chegar.html`.
- Números voláteis de avaliações foram substituídos nas homes por faixas estáveis e localizadas por idioma.
- Capacidade de eventos passou a ser informada como variável conforme formato, montagem e áreas utilizadas.
- Removidas capacidades máximas não confirmadas do conteúdo e do JSON-LD de eventos.
- Corrigido o redirecionamento circular do antigo `formulario.html`.
- Criado formulário integrado em `eventos.html` com nome, contato, data, convidados e formato.
- Corrigidos os formulários equivalentes em `en/eventos.html` e `es/eventos.html`, com textos e mensagens no idioma correto.
- O formulário informa corretamente que a solicitação só é enviada após confirmação no WhatsApp.
- As páginas corporativas PT, EN e ES não simulam mais um envio bem-sucedido sem backend; elas direcionam ao formulário funcional do idioma correspondente.

## Eventos de medição

- `ec_event_form_start`: primeira interação com o formulário.
- `ec_event_lead_outbound`: abertura da mensagem estruturada no WhatsApp.

## Proteções factuais

- Nenhuma alegação sobre Cantina do MAM ou composição societária foi adicionada.
- Nenhuma capacidade fixa foi mantida sem confirmação documental.
- Nenhum `Review`, `Rating` ou `AggregateRating` foi adicionado ao JSON-LD.
