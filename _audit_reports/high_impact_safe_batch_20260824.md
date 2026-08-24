# Lote seguro de alto impacto — 24/08/2026

Status geral: **PASS**

## Correções aplicadas

- Selo da home corrigido: removida a referência conflitante a `PRÊMIO 2024` e identificada a Academia da Cachaça como vencedora da categoria Melhor Feijoada no Veja Rio Comer & Beber 2025.
- Destaque de `feijoada.html` corrigido com a mesma atribuição factual.
- Resíduos de 8.255 avaliações substituídos pelo total informado de 8.847 nas homes PT, EN e ES.
- `restaurante-urca.html` removida do sitemap por ser uma página alternativa cuja canonical aponta para `restaurante-morro-da-urca.html`; cinco links internos também passaram a apontar diretamente para a URL canônica.
- Evento de WhatsApp consolidado como `whatsapp_click`, preservando o nome com maior histórico no GA4.
- 16 listeners legados de WhatsApp removidos para impedir dupla contagem do mesmo clique.
- Eventos específicos adicionados para `click_google_maps` e `click_google_reviews`.
- A camada GA4 foi centralizada em `assets/conversion-tracking.js`, eliminando mais de 6 mil linhas inline repetidas e cobrindo 102 páginas publicáveis; páginas de redirecionamento, preview, administração e offline foram excluídas deliberadamente.

## Segurança e validações

- JavaScript compartilhado da camada de eventos: **válido, 0 erros de sintaxe**.
- Cobertura GA4: **102 páginas com base GA4 e camada compartilhada de conversão**.
- GSC structured data post-fix: **PASS**.
- Schema Rating Guard: **PASS**, 110 arquivos, 0 achados.
- FAQ duplicado, Review, Rating e AggregateRating indevidos: **0 pendências**.
- Hreflang PT/EN/ES: **PASS**, nota mínima 100.
- Sitemap XML: **válido**.
- Final Site AAA Master Audit: **97 PASS, 0 WARN, média 10.0/10**.

## Itens deliberadamente não alterados neste lote

- Redirects e regras da Cloudflare.
- Backend/formulário de eventos.
- Diferenças editoriais de estrutura entre PT, EN e ES, que permanecem em lote próprio de revisão.
