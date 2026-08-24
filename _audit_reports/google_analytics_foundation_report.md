# Google Analytics Foundation — Embaixada Carioca

Status geral: **PASS**

## Measurement ID
- G-9GRXVZ55CB

## Estratégia de performance
- GA4 carrega após idle/interação para reduzir trabalho inicial da main thread.
- Eventos de clique forçam carregamento antes de enviar a conversão, preservando medição de CTAs.

## Eventos configurados
- click_reservar
- whatsapp_click
- click_cardapio
- click_como_chegar
- click_google_maps
- click_google_reviews
- click_eventos
- click_cafe_da_manha
- click_almoco
- click_idioma

## Contadores
- html_scanned: 106
- html_updated: 0
- ga_head_installed: 102
- event_layer_installed: 102
- legacy_whatsapp_handlers_removed: 0
- skipped: 4

## Arquivos

## Próximos passos no GA4
- Validar a tag no Tag Assistant.
- Confirmar page_view no relatório Tempo real.
- Marcar click_reservar, whatsapp_click, click_eventos, click_google_maps e click_google_reviews como key events.
- Vincular GA4 ao Google Ads para remarketing e públicos.
- Implementar Consent Mode quando houver banner de consentimento.
