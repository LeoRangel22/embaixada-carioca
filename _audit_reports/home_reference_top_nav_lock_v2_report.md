# Home Reference Top Nav Lock V2

Status geral: **PASS**

## Objetivo
Corrigir os problemas remanescentes vistos no navegador: `eventos.html` fora de padrão, overflow do botão, e linha `Restaurante no Bondinho...` branca em páginas como `cafe-da-manha.html`.

## Correções
- Remoção de CSS legado de navegação, incluindo `nav-standard-css` e blocos `NAV PADRONIZADO` que sobrescreviam o lock final.
- Reaplicação do componente canônico de navegação baseado na home.
- Hide do Google Reviews em larguras até 1500px para evitar overflow horizontal do CTA em `eventos.html`.
- Linha/eyebrow do hero forçada para a tipografia e cor da home: JetBrains Mono 11px, uppercase, amarelo.
- Páginas de eventos mantêm `Solicitar orçamento`.

## Guardrails
- Nenhum JSON-LD/schema foi alterado.
- Nenhuma seção de conteúdo foi alterada fora do `nav.top` e CSS legado de navegação.

## Resumo
- Páginas processadas: **84**
- Páginas alteradas: **84**
- Blocos CSS legados removidos: **203**
- Páginas de eventos com CTA especial: **3**

## Resultados por página

| Página | Changed | Nav substituído | CSS legado removido | CTA evento | Notas |
|---|---:|---:|---:|---:|---|
| `almoco-morro-da-urca.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `almoco.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `cafe-da-manha-com-vista-rio-de-janeiro.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `cafe-da-manha-pao-de-acucar.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `cafe-da-manha.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `caipirinha-com-vista-rio.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `cardapio.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `como-chegar.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `contato.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/almoco-morro-da-urca.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/almoco.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/breakfast-with-a-view-rio-de-janeiro.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/cafe-da-manha-pao-de-acucar.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/cafe-da-manha.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/caipirinha-com-vista-rio.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/cardapio.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/contato.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/entardecer.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/eventos.html` | True | True | 3 | True | legacy-nav-css-removed-home-reference-v2 |
| `en/feijoada-com-vista-rio-de-janeiro.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/feijoada.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/gastronomia-carioca.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/guia-do-rio.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/how-to-get-there.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/index.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/morro-da-urca.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/nossa-visao.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/parque-bondinho.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/por-do-sol-morro-da-urca.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/restaurant-at-urca-hill.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/restaurants-near-sugarloaf-mountain.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/roteiro-meio-dia-urca-pao-de-acucar.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/sugarloaf-cable-car-park.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/sugarloaf-cable-car-restaurant.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/sunset.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `en/where-to-eat-near-sugarloaf.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `entardecer.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/almoco-morro-da-urca.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/almoco.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/atardecer.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/cafe-da-manha-pao-de-acucar.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/cafe-da-manha.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/caipirinha-com-vista-rio.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/cardapio.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/como-llegar.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/contato.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/desayuno-con-vista-rio-de-janeiro.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/donde-comer-cerca-del-pan-de-azucar.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/entardecer.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/eventos.html` | True | True | 3 | True | legacy-nav-css-removed-home-reference-v2 |
| `es/feijoada-com-vista-rio-de-janeiro.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/feijoada.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/gastronomia-carioca.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/guia-do-rio.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/index.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/morro-da-urca.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/nossa-visao.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/parque-bondinho-pan-de-azucar.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/parque-bondinho.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/por-do-sol-morro-da-urca.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/restaurante-bondinho-pan-de-azucar.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/restaurante-morro-da-urca.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/restaurantes-cerca-del-pan-de-azucar.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `es/roteiro-meio-dia-urca-pao-de-acucar.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `eventos.html` | True | True | 1 | True | legacy-nav-css-removed-home-reference-v2 |
| `feijoada-com-vista-rio-de-janeiro.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `feijoada.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `gastronomia-carioca.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `guia-do-rio.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `index.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `morro-da-urca.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `nossa-visao.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `onde-comer-no-pao-de-acucar.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `parque-bondinho-pao-de-acucar.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `parque-bondinho.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
| `por-do-sol-morro-da-urca.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `restaurante-bondinho-pao-de-acucar.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `restaurante-morro-da-urca.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `restaurantes-perto-do-pao-de-acucar.html` | True | True | 2 | False | legacy-nav-css-removed-home-reference-v2 |
| `restaurantes-romanticos-rio-de-janeiro.html` | True | True | 1 | False | legacy-nav-css-removed-home-reference-v2 |
| `roteiro-meio-dia-urca-pao-de-acucar.html` | True | True | 3 | False | legacy-nav-css-removed-home-reference-v2 |
