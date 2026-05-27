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
- Arquivos alterados: **27**
- Arquivos sem seletor de idioma/SKIP: **2**

## Resultados

| Página | Status | Changed |
|---|---|---:|
| `404.html` | ok | False |
| `almoco-morro-da-urca.html` | ok | False |
| `almoco.html` | ok | True |
| `cafe-da-manha-com-vista-rio-de-janeiro.html` | ok | False |
| `cafe-da-manha-pao-de-acucar.html` | ok | False |
| `cafe-da-manha.html` | ok | True |
| `caipirinha-com-vista-rio.html` | ok | False |
| `cardapio.html` | ok | True |
| `como-chegar.html` | ok | False |
| `contato.html` | ok | False |
| `en/almoco-morro-da-urca.html` | ok | False |
| `en/almoco.html` | ok | True |
| `en/breakfast-with-a-view-rio-de-janeiro.html` | ok | False |
| `en/cafe-da-manha-pao-de-acucar.html` | ok | False |
| `en/cafe-da-manha.html` | ok | True |
| `en/caipirinha-com-vista-rio.html` | ok | False |
| `en/cardapio.html` | ok | True |
| `en/contato.html` | ok | False |
| `en/entardecer.html` | ok | True |
| `en/eventos.html` | ok | True |
| `en/feijoada-com-vista-rio-de-janeiro.html` | ok | False |
| `en/feijoada.html` | ok | True |
| `en/gastronomia-carioca.html` | ok | False |
| `en/guia-do-rio.html` | ok | False |
| `en/how-to-get-there.html` | ok | False |
| `en/index.html` | ok | True |
| `en/morro-da-urca.html` | ok | True |
| `en/nossa-visao.html` | ok | False |
| `en/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | ok | False |
| `en/parque-bondinho.html` | ok | True |
| `en/por-do-sol-morro-da-urca.html` | ok | False |
| `en/restaurant-at-urca-hill.html` | ok | False |
| `en/restaurants-near-sugarloaf-mountain.html` | ok | False |
| `en/roteiro-meio-dia-urca-pao-de-acucar.html` | ok | False |
| `en/sugarloaf-cable-car-park.html` | ok | False |
| `en/sugarloaf-cable-car-restaurant.html` | ok | False |
| `en/sunset.html` | ok | True |
| `en/where-to-eat-near-sugarloaf.html` | ok | False |
| `entardecer.html` | ok | True |
| `es/almoco-morro-da-urca.html` | ok | False |
| `es/almoco.html` | ok | True |
| `es/atardecer.html` | ok | True |
| `es/cafe-da-manha-pao-de-acucar.html` | ok | False |
| `es/cafe-da-manha.html` | ok | True |
| `es/caipirinha-com-vista-rio.html` | ok | False |
| `es/cardapio.html` | ok | True |
| `es/como-llegar.html` | ok | False |
| `es/contato.html` | ok | False |
| `es/desayuno-con-vista-rio-de-janeiro.html` | ok | False |
| `es/donde-comer-cerca-del-pan-de-azucar.html` | ok | False |
| `es/entardecer.html` | ok | True |
| `es/eventos.html` | ok | True |
| `es/feijoada-com-vista-rio-de-janeiro.html` | ok | False |
| `es/feijoada.html` | ok | True |
| `es/gastronomia-carioca.html` | ok | False |
| `es/guia-do-rio.html` | ok | False |
| `es/index.html` | ok | True |
| `es/morro-da-urca.html` | ok | True |
| `es/nossa-visao.html` | ok | False |
| `es/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | ok | False |
| `es/parque-bondinho-pan-de-azucar.html` | ok | False |
| `es/parque-bondinho.html` | ok | False |
| `es/por-do-sol-morro-da-urca.html` | ok | False |
| `es/restaurante-bondinho-pan-de-azucar.html` | ok | False |
| `es/restaurante-morro-da-urca.html` | ok | False |
| `es/restaurantes-cerca-del-pan-de-azucar.html` | ok | False |
| `es/roteiro-meio-dia-urca-pao-de-acucar.html` | ok | False |
| `feijoada-com-vista-rio-de-janeiro.html` | ok | False |
| `feijoada.html` | ok | True |
| `gastronomia-carioca.html` | ok | False |
| `guia-do-rio.html` | ok | False |
| `home-preview.html` | ok | False |
| `index.html` | ok | True |
| `morro-da-urca.html` | ok | True |
| `nossa-visao.html` | ok | False |
| `o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | ok | False |
| `offline.html` | ok | False |
| `onde-comer-no-pao-de-acucar.html` | ok | False |
| `parque-bondinho-pao-de-acucar.html` | ok | False |
| `parque-bondinho.html` | ok | True |
| `por-do-sol-morro-da-urca.html` | ok | False |
| `restaurante-bondinho-pao-de-acucar.html` | ok | False |
| `restaurante-morro-da-urca.html` | ok | False |
| `restaurantes-perto-do-pao-de-acucar.html` | ok | False |
| `roteiro-meio-dia-urca-pao-de-acucar.html` | ok | False |

## SKIPs

- `eventos.html` — skip-no-lang-switcher
- `restaurantes-romanticos-rio-de-janeiro.html` — skip-no-lang-switcher

## Validação visual necessária
Conferir desktop e mobile em: `index.html`, `como-chegar.html`, `cardapio.html`, `eventos.html`, `en/index.html`, `es/index.html`.
