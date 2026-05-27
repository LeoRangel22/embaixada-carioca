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
| `index.html` | True | 3 | 0 | 0 | 0 | 0 | 1 | 0 | False | False | 32 | 25 | 40 |
| `cafe-da-manha.html` | True | 0 | 0 | 0 | 0 | 1 | 1 | 0 | False | False | 25 | 21 | 19 |
| `almoco.html` | True | 0 | 0 | 0 | 0 | 1 | 1 | 0 | False | False | 27 | 17 | 17 |
| `cardapio.html` | True | 0 | 0 | 0 | 0 | 1 | 1 | 0 | False | False | 27 | 18 | 11 |
| `guia-do-rio.html` | True | 0 | 0 | 0 | 0 | 1 | 1 | 0 | False | False | 26 | 17 | 9 |
| `eventos.html` | True | 0 | 0 | 0 | 1 | 0 | 1 | 0 | True | True | 3 | 3 | 4 |

## Próxima fase
A redução pesada de CSS/JS deve ser feita como refactor controlado: extrair blocos globais para assets externos, testar visualmente e só então remover os patches inline redundantes.
