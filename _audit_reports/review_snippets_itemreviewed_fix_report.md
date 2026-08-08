# Review Snippets — itemReviewed Fix

Status geral: **PASS**

## Problema identificado

O Search Console apontou erro em **Snippets de avaliação**: `O campo "itemReviewed" não foi encontrado`.

A causa era a existência de blocos `Review`, `reviewRating` e `aggregateRating` nas páginas de avaliações. Cada review individual entrava como item de snippet de avaliação e o Google exigia `itemReviewed`.

## Estratégia adotada

A estratégia escolhida foi **remover dados estruturados de Review/Rating** dessas páginas, em vez de tentar qualificar review snippet. Motivos:

- evita erro `itemReviewed`;
- evita exposição indevida a rich results de avaliações baseadas em reviews de terceiros;
- mantém a página como conteúdo editorial de confiança;
- preserva JSON-LD seguro com `WebPage`, `BreadcrumbList` e `Restaurant` sem rating/review.

## Páginas corrigidas

| Página | Ação | Status |
|---|---|---:|
| `en/reviews-embaixada-carioca.html` | Removido schema `Review`, `Rating`, `AggregateRating`; recriada página editorial EN | PASS |
| `avaliacoes-embaixada-carioca.html` | Removido schema `Review`, `Rating`, `AggregateRating`; recriada página editorial PT | PASS |
| `es/resenas-embaixada-carioca.html` | Removido schema `Review`, `Rating`, `AggregateRating`; recriada página editorial ES | PASS |

## Guardrails

- Canonicals preservadas por idioma.
- Hreflang PT/EN/ES/x-default preservado.
- Nenhum `Review`, `Rating`, `reviewRating` ou `aggregateRating` foi mantido nas páginas corrigidas.
- As páginas continuam indexáveis.
- O conteúdo visível passa a apresentar resumo editorial das avaliações, sem marcação estruturada de review individual.

## Próximo passo no Search Console

Após o deploy do GitHub Pages:

1. Abrir o erro **Snippets de avaliação → O campo `itemReviewed` não foi encontrado**.
2. Clicar em **Validar a correção**.
3. Aguardar o novo rastreamento do Google.

## Observação

A correção remove a elegibilidade dessas páginas específicas a review snippets, mas também remove o erro. Para restaurante, a marcação estruturada principal deve continuar concentrada em `Restaurant`, `WebPage`, `FAQPage`, `Menu` e `BreadcrumbList`, evitando reviews de terceiros marcadas diretamente no site.
