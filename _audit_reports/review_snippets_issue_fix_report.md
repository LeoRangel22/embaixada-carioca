# Review Snippets Issue Fix

Status geral: **PASS**

## Problema do Google Search Console
- A avaliação tem várias classificações agregadas.
- Estratégia: remover AggregateRating e campos de rating do JSON-LD, preservando os demais schemas.

## Resumo
- Arquivos HTML escaneados: 87
- Arquivos alterados: 21
- Arquivos com termos proibidos remanescentes: 0

## URLs afetadas no XLSX do Search Console

| URL | Arquivo | Changed | Removidos | Remanescentes |
|---|---|---:|---:|---|
| https://www.embaixadacarioca.com/morro-da-urca.html | `morro-da-urca.html` | False | 0 | — |
| https://www.embaixadacarioca.com/onde-comer-no-pao-de-acucar.html | `onde-comer-no-pao-de-acucar.html` | True | 2 | — |
| https://www.embaixadacarioca.com/restaurante-morro-da-urca.html | `restaurante-morro-da-urca.html` | True | 2 | — |
| https://www.embaixadacarioca.com/parque-bondinho.html | `parque-bondinho.html` | True | 2 | — |
| https://www.embaixadacarioca.com/o-que-fazer-depois-do-bondinho-pao-de-acucar.html | `o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | True | 2 | — |
| https://www.embaixadacarioca.com/roteiro-meio-dia-urca-pao-de-acucar.html | `roteiro-meio-dia-urca-pao-de-acucar.html` | True | 2 | — |
| https://www.embaixadacarioca.com/cafe-da-manha.html | `cafe-da-manha.html` | False | 0 | — |
| https://www.embaixadacarioca.com/entardecer.html | `entardecer.html` | False | 0 | — |

## Arquivos alterados

- `404.html` — removidos=1, jsonld=1, parse_errors=0
- `almoco-morro-da-urca.html` — removidos=1, jsonld=3, parse_errors=0
- `cafe-da-manha-pao-de-acucar.html` — removidos=1, jsonld=3, parse_errors=0
- `caipirinha-com-vista-rio.html` — removidos=2, jsonld=4, parse_errors=0
- `contato.html` — removidos=2, jsonld=4, parse_errors=0
- `feijoada-com-vista-rio-de-janeiro.html` — removidos=1, jsonld=3, parse_errors=0
- `gastronomia-carioca.html` — removidos=3, jsonld=4, parse_errors=0
- `guia-do-rio.html` — removidos=2, jsonld=5, parse_errors=0
- `home-preview.html` — removidos=1, jsonld=1, parse_errors=0
- `nossa-visao.html` — removidos=2, jsonld=4, parse_errors=0
- `o-que-fazer-depois-do-bondinho-pao-de-acucar.html` — removidos=2, jsonld=7, parse_errors=0
- `offline.html` — removidos=1, jsonld=1, parse_errors=0
- `onde-comer-no-pao-de-acucar.html` — removidos=2, jsonld=5, parse_errors=0
- `parque-bondinho-pao-de-acucar.html` — removidos=2, jsonld=5, parse_errors=0
- `parque-bondinho.html` — removidos=2, jsonld=5, parse_errors=0
- `por-do-sol-morro-da-urca.html` — removidos=1, jsonld=3, parse_errors=0
- `restaurante-bondinho-pao-de-acucar.html` — removidos=2, jsonld=5, parse_errors=0
- `restaurante-morro-da-urca.html` — removidos=2, jsonld=5, parse_errors=0
- `restaurantes-perto-do-pao-de-acucar.html` — removidos=2, jsonld=5, parse_errors=0
- `restaurantes-romanticos-rio-de-janeiro.html` — removidos=0, jsonld=1, parse_errors=0
- `roteiro-meio-dia-urca-pao-de-acucar.html` — removidos=2, jsonld=7, parse_errors=0
