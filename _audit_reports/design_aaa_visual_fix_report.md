# Design AAA Visual Fix

Status geral: **PASS**

Data: 2026-08-15

## Escopo corrigido

- Hero mobile de `cardapio.html` com título e CTAs novamente visíveis.
- Hero mobile de `cafe-da-manha.html` com título e CTAs novamente visíveis.
- Conteúdo editorial/SEO retirado de dentro do hero e mantido visível após a primeira dobra.
- Linha redundante de avaliações removida do topo da home.
- Navegação de `eventos.html` alinhada à home, preservando `Solicitar orçamento`.
- Tipografia dos títulos principais padronizada.
- Caminho da imagem de café da manhã corrigido nas homes EN/ES.

## Validação responsiva

| Largura | Overflow horizontal | Títulos visíveis | Imagens quebradas |
|---:|---:|---:|---:|
| 390 px | Não | Sim | 0 |
| 768 px | Não | Sim | 0 |
| 1440 px | Não | Sim | 0 |
| 1920 px | Não | Sim | 0 |

Páginas verificadas:

- `index.html`
- `cardapio.html`
- `cafe-da-manha.html`
- `eventos.html`
- `en/index.html`
- `es/index.html`

## Guardrails

- Nenhum JSON-LD/schema foi alterado.
- Nenhum `Review`, `Rating` ou `AggregateRating` foi adicionado.
- Canonical e hreflang foram preservados.
- O conteúdo completo do cardápio não foi alterado.
