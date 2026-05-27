# Language Dropdown Closed State Fix

Status geral: **PASS**

## Problema corrigido
Durante QA visual real, o seletor de idioma apareceu aberto/sem contenção sobre o hero. A correção força estado fechado por padrão e renderiza o dropdown como card contido.

## Guardrails
- Nenhum JSON-LD foi alterado.
- Nenhum schema foi inserido ou removido.
- A alteração é restrita a CSS/JS de UI do seletor de idioma.

## Resumo
- Arquivos HTML analisados: **87**
- Arquivos com seletor de idioma processados: **85**
- Arquivos alterados: **85**
- Arquivos sem seletor de idioma/SKIP: **2**

## Resultados

| Página | Status | Changed |
|---|---|---:|
| `404.html` | ok | True |
| `almoco-morro-da-urca.html` | ok | True |
| `almoco.html` | ok | True |
| `cafe-da-manha-com-vista-rio-de-janeiro.html` | ok | True |
| `cafe-da-manha-pao-de-acucar.html` | ok | True |
| `cafe-da-manha.html` | ok | True |
| `caipirinha-com-vista-rio.html` | ok | True |
| `cardapio.html` | ok | True |
| `como-chegar.html` | ok | True |
| `contato.html` | ok | True |
| `en/almoco-morro-da-urca.html` | ok | True |
| `en/almoco.html` | ok | True |
| `en/breakfast-with-a-view-rio-de-janeiro.html` | ok | True |
| `en/cafe-da-manha-pao-de-acucar.html` | ok | True |
| `en/cafe-da-manha.html` | ok | True |
| `en/caipirinha-com-vista-rio.html` | ok | True |
| `en/cardapio.html` | ok | True |
| `en/contato.html` | ok | True |
| `en/entardecer.html` | ok | True |
| `en/eventos.html` | ok | True |
| `en/feijoada-com-vista-rio-de-janeiro.html` | ok | True |
| `en/feijoada.html` | ok | True |
| `en/gastronomia-carioca.html` | ok | True |
| `en/guia-do-rio.html` | ok | True |
| `en/how-to-get-there.html` | ok | True |
| `en/index.html` | ok | True |
| `en/morro-da-urca.html` | ok | True |
| `en/nossa-visao.html` | ok | True |
| `en/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | ok | True |
| `en/parque-bondinho.html` | ok | True |
| `en/por-do-sol-morro-da-urca.html` | ok | True |
| `en/restaurant-at-urca-hill.html` | ok | True |
| `en/restaurants-near-sugarloaf-mountain.html` | ok | True |
| `en/roteiro-meio-dia-urca-pao-de-acucar.html` | ok | True |
| `en/sugarloaf-cable-car-park.html` | ok | True |
| `en/sugarloaf-cable-car-restaurant.html` | ok | True |
| `en/sunset.html` | ok | True |
| `en/where-to-eat-near-sugarloaf.html` | ok | True |
| `entardecer.html` | ok | True |
| `es/almoco-morro-da-urca.html` | ok | True |
| `es/almoco.html` | ok | True |
| `es/atardecer.html` | ok | True |
| `es/cafe-da-manha-pao-de-acucar.html` | ok | True |
| `es/cafe-da-manha.html` | ok | True |
| `es/caipirinha-com-vista-rio.html` | ok | True |
| `es/cardapio.html` | ok | True |
| `es/como-llegar.html` | ok | True |
| `es/contato.html` | ok | True |
| `es/desayuno-con-vista-rio-de-janeiro.html` | ok | True |
| `es/donde-comer-cerca-del-pan-de-azucar.html` | ok | True |
| `es/entardecer.html` | ok | True |
| `es/eventos.html` | ok | True |
| `es/feijoada-com-vista-rio-de-janeiro.html` | ok | True |
| `es/feijoada.html` | ok | True |
| `es/gastronomia-carioca.html` | ok | True |
| `es/guia-do-rio.html` | ok | True |
| `es/index.html` | ok | True |
| `es/morro-da-urca.html` | ok | True |
| `es/nossa-visao.html` | ok | True |
| `es/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | ok | True |
| `es/parque-bondinho-pan-de-azucar.html` | ok | True |
| `es/parque-bondinho.html` | ok | True |
| `es/por-do-sol-morro-da-urca.html` | ok | True |
| `es/restaurante-bondinho-pan-de-azucar.html` | ok | True |
| `es/restaurante-morro-da-urca.html` | ok | True |
| `es/restaurantes-cerca-del-pan-de-azucar.html` | ok | True |
| `es/roteiro-meio-dia-urca-pao-de-acucar.html` | ok | True |
| `feijoada-com-vista-rio-de-janeiro.html` | ok | True |
| `feijoada.html` | ok | True |
| `gastronomia-carioca.html` | ok | True |
| `guia-do-rio.html` | ok | True |
| `home-preview.html` | ok | True |
| `index.html` | ok | True |
| `morro-da-urca.html` | ok | True |
| `nossa-visao.html` | ok | True |
| `o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | ok | True |
| `offline.html` | ok | True |
| `onde-comer-no-pao-de-acucar.html` | ok | True |
| `parque-bondinho-pao-de-acucar.html` | ok | True |
| `parque-bondinho.html` | ok | True |
| `por-do-sol-morro-da-urca.html` | ok | True |
| `restaurante-bondinho-pao-de-acucar.html` | ok | True |
| `restaurante-morro-da-urca.html` | ok | True |
| `restaurantes-perto-do-pao-de-acucar.html` | ok | True |
| `roteiro-meio-dia-urca-pao-de-acucar.html` | ok | True |

## SKIPs

- `eventos.html` — skip-no-lang-switcher
- `restaurantes-romanticos-rio-de-janeiro.html` — skip-no-lang-switcher

## Validação visual necessária
Conferir desktop e mobile em: `index.html`, `como-chegar.html`, `cardapio.html`, `eventos.html`, `en/index.html`, `es/index.html`.
