# Performance Urgent Quick Wins

Status geral: **PASS**

## Escopo
Correções seguras nas páginas mais pesadas apontadas pelo Phase 2 Performance & SEO Audit.

## O que foi aplicado
- Remoção de prefetch de documentos que competem com o primeiro render.
- Deduplicação exata de blocos inline repetidos dentro da mesma página.
- `decoding=async` em imagens.
- `loading=lazy` em imagens fora do primeiro ativo prioritário.
- `fetchpriority=high` na primeira imagem prioritária quando ausente.
- `defer` em scripts externos sem `async/defer`, preservando JSON-LD.
- `eventos.html`: preload do hero + CSS consolidado de estabilização.

## Resultados por página

| Página | Changed | Prefetch removidos | Styles dup removidos | Scripts dup removidos | Decoding add | Lazy add | Fetchpriority add | Scripts defer | CSS eventos | Preload eventos | Styles atuais | Scripts atuais | Imagens atuais |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `index.html` | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | 34 | 26 | 40 |
| `cafe-da-manha.html` | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | 27 | 22 | 19 |
| `almoco.html` | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | 29 | 18 | 17 |
| `cardapio.html` | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | 29 | 19 | 11 |
| `guia-do-rio.html` | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | 28 | 18 | 9 |
| `eventos.html` | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | 4 | 3 | 4 |

## Próxima fase
A redução pesada de CSS/JS deve ser feita como refactor controlado: extrair blocos globais para assets externos, testar visualmente e só então remover os patches inline redundantes.
