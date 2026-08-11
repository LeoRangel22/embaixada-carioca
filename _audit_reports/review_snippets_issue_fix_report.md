# Review Snippets Issue Fix

Status geral: **PASS**

## Problema do Google Search Console
- A avaliação tem várias classificações agregadas.
- O campo `itemReviewed` não foi encontrado em itens `Review`.
- Estratégia: remover Review, Rating, AggregateRating e seus campos do JSON-LD, preservando os demais schemas.

## Resumo
- Arquivos HTML escaneados: 118
- Arquivos alterados: 19
- Arquivos com termos proibidos remanescentes: 0

## URLs afetadas no XLSX do Search Console

| URL | Arquivo | Changed | Removidos | Remanescentes |
|---|---|---:|---:|---|
| https://www.embaixadacarioca.com/avaliacoes-embaixada-carioca.html | `avaliacoes-embaixada-carioca.html` | False | 0 | — |
| https://www.embaixadacarioca.com/en/reviews-embaixada-carioca.html | `en/reviews-embaixada-carioca.html` | False | 0 | — |
| https://www.embaixadacarioca.com/es/resenas-embaixada-carioca.html | `es/resenas-embaixada-carioca.html` | False | 0 | — |
| https://www.embaixadacarioca.com/morro-da-urca.html | `morro-da-urca.html` | True | 2 | — |
| https://www.embaixadacarioca.com/onde-comer-no-pao-de-acucar.html | `onde-comer-no-pao-de-acucar.html` | False | 0 | — |
| https://www.embaixadacarioca.com/restaurante-morro-da-urca.html | `restaurante-morro-da-urca.html` | True | 2 | — |
| https://www.embaixadacarioca.com/parque-bondinho.html | `parque-bondinho.html` | True | 2 | — |
| https://www.embaixadacarioca.com/o-que-fazer-depois-do-bondinho-pao-de-acucar.html | `o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | False | 0 | — |
| https://www.embaixadacarioca.com/roteiro-meio-dia-urca-pao-de-acucar.html | `roteiro-meio-dia-urca-pao-de-acucar.html` | False | 0 | — |
| https://www.embaixadacarioca.com/cafe-da-manha.html | `cafe-da-manha.html` | True | 2 | — |
| https://www.embaixadacarioca.com/entardecer.html | `entardecer.html` | False | 0 | — |

## Arquivos alterados

- `cafe-da-manha.html` — removidos=2, jsonld=1, parse_errors=0
- `cardapio.html` — removidos=2, jsonld=1, parse_errors=0
- `como-chegar.html` — removidos=2, jsonld=2, parse_errors=0
- `en/cafe-da-manha.html` — removidos=1, jsonld=1, parse_errors=0
- `en/cardapio.html` — removidos=1, jsonld=1, parse_errors=0
- `en/index.html` — removidos=2, jsonld=1, parse_errors=0
- `en/morro-da-urca.html` — removidos=2, jsonld=1, parse_errors=0
- `en/parque-bondinho.html` — removidos=1, jsonld=1, parse_errors=0
- `es/cafe-da-manha.html` — removidos=1, jsonld=1, parse_errors=0
- `es/cardapio.html` — removidos=1, jsonld=1, parse_errors=0
- `es/index.html` — removidos=2, jsonld=1, parse_errors=0
- `es/morro-da-urca.html` — removidos=2, jsonld=1, parse_errors=0
- `es/parque-bondinho.html` — removidos=1, jsonld=1, parse_errors=0
- `eventos.html` — removidos=2, jsonld=2, parse_errors=0
- `index.html` — removidos=2, jsonld=1, parse_errors=0
- `morro-da-urca.html` — removidos=2, jsonld=1, parse_errors=0
- `parque-bondinho.html` — removidos=2, jsonld=1, parse_errors=0
- `restaurante-morro-da-urca.html` — removidos=2, jsonld=1, parse_errors=0
- `restaurante-urca.html` — removidos=2, jsonld=1, parse_errors=0
