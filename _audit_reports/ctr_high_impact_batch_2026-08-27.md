# Lote de alto impacto — CTR Search Console

**Data:** 2026-08-27
**Status:** PASS

## Base de decisão

Exportação do Google Search Console dos últimos 7 dias, com dados de 19 a 25 de agosto de 2026.

- `almoço no pao de açucar`: posição 2,29 e CTR 0%.
- `almoço pao de acucar`: posição 2,00 e CTR 0%.
- `/en/where-to-eat-near-sugarloaf.html`: 110 impressões, posição 6,29 e CTR 0%.
- `/es/donde-comer-cerca-del-pan-de-azucar.html`: 41 impressões, posição 6,93 e CTR 0%.

## Alterações aplicadas

### `almoco.html`

- Title alinhado à consulta exata `almoço no Pão de Açúcar`.
- Description, Open Graph e Twitter alinhados ao mesmo posicionamento.
- Diferencial factual preservado: único restaurante do parque com vista direta para o Pão de Açúcar.

### `en/where-to-eat-near-sugarloaf.html`

- Removidos `Best Restaurant` e `top-rated` do snippet.
- Title passou a combinar intenção, local e marca.
- Description, Open Graph e Twitter passaram a usar apenas o diferencial factual verificável.

### `es/donde-comer-cerca-del-pan-de-azucar.html`

- Removida a alegação genérica `el mejor restaurante`.
- Title passou a combinar intenção, local e marca.
- Description, Open Graph e Twitter passaram a usar apenas o diferencial factual verificável.

### `sitemap.xml`

- `lastmod` atualizado para `2026-08-27` nas três páginas alteradas.

## Validações

- Schema rating guard: PASS — 110 arquivos, 0 ocorrências proibidas.
- JSON-LD duplicate key guard: PASS — 110 arquivos, 0 chaves duplicadas.
- Hreflang PT/EN/ES: PASS — nota mínima 100.
- i18n: todas as páginas PT possuem equivalentes EN e ES.

## Guardrails

- Nenhuma alteração em `Review`, `Rating`, `AggregateRating` ou outros dados estruturados.
- Nenhuma nova página criada.
- Titles do cluster restaurante/Bondinho publicado em 27/08 foram preservados para permitir medição limpa.
- Revisar o efeito em 14 dias e decidir com uma janela consolidada de 28 dias.
