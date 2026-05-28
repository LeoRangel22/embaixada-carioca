# Top Nav Viewport Fit V3

Status geral: **PASS**

## Objetivo
Corrigir o overflow visual remanescente do topo em larguras reais de navegador, especialmente `eventos.html`, e travar a cor da linha/eyebrow em amarelo nas páginas internas.

## Correções
- CSS final inserido como último bloco de navegação no `<head>`.
- Google Reviews oculto em larguras até 1800px para impedir corte lateral.
- Em páginas com CTA de evento (`formulario.html`), Google Reviews é oculto sempre.
- Idioma é oculto abaixo de 1500px para preservar menu e CTA.
- Botão `Solicitar orçamento` recebe largura controlada para não sair da tela.
- Linha/eyebrow do hero é forçada para amarelo, JetBrains Mono, 11px, uppercase.

## Guardrails
- Nenhum JSON-LD/schema foi alterado.
- Nenhum conteúdo de seção foi alterado.
- Apenas CSS final de navegação foi inserido/atualizado.

## Resumo
- Páginas processadas: **84**
- Páginas alteradas: **84**
- Páginas com CTA de evento: **3**

## Resultados por página

| Página | Changed | CTA evento detectado | Notas |
|---|---:|---:|---|
| `almoco-morro-da-urca.html` | True | False | final-css-order-viewport-fit |
| `almoco.html` | True | False | final-css-order-viewport-fit |
| `cafe-da-manha-com-vista-rio-de-janeiro.html` | True | False | final-css-order-viewport-fit |
| `cafe-da-manha-pao-de-acucar.html` | True | False | final-css-order-viewport-fit |
| `cafe-da-manha.html` | True | False | final-css-order-viewport-fit |
| `caipirinha-com-vista-rio.html` | True | False | final-css-order-viewport-fit |
| `cardapio.html` | True | False | final-css-order-viewport-fit |
| `como-chegar.html` | True | False | final-css-order-viewport-fit |
| `contato.html` | True | False | final-css-order-viewport-fit |
| `en/almoco-morro-da-urca.html` | True | False | final-css-order-viewport-fit |
| `en/almoco.html` | True | False | final-css-order-viewport-fit |
| `en/breakfast-with-a-view-rio-de-janeiro.html` | True | False | final-css-order-viewport-fit |
| `en/cafe-da-manha-pao-de-acucar.html` | True | False | final-css-order-viewport-fit |
| `en/cafe-da-manha.html` | True | False | final-css-order-viewport-fit |
| `en/caipirinha-com-vista-rio.html` | True | False | final-css-order-viewport-fit |
| `en/cardapio.html` | True | False | final-css-order-viewport-fit |
| `en/contato.html` | True | False | final-css-order-viewport-fit |
| `en/entardecer.html` | True | False | final-css-order-viewport-fit |
| `en/eventos.html` | True | True | final-css-order-viewport-fit |
| `en/feijoada-com-vista-rio-de-janeiro.html` | True | False | final-css-order-viewport-fit |
| `en/feijoada.html` | True | False | final-css-order-viewport-fit |
| `en/gastronomia-carioca.html` | True | False | final-css-order-viewport-fit |
| `en/guia-do-rio.html` | True | False | final-css-order-viewport-fit |
| `en/how-to-get-there.html` | True | False | final-css-order-viewport-fit |
| `en/index.html` | True | False | final-css-order-viewport-fit |
| `en/morro-da-urca.html` | True | False | final-css-order-viewport-fit |
| `en/nossa-visao.html` | True | False | final-css-order-viewport-fit |
| `en/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | True | False | final-css-order-viewport-fit |
| `en/parque-bondinho.html` | True | False | final-css-order-viewport-fit |
| `en/por-do-sol-morro-da-urca.html` | True | False | final-css-order-viewport-fit |
| `en/restaurant-at-urca-hill.html` | True | False | final-css-order-viewport-fit |
| `en/restaurants-near-sugarloaf-mountain.html` | True | False | final-css-order-viewport-fit |
| `en/roteiro-meio-dia-urca-pao-de-acucar.html` | True | False | final-css-order-viewport-fit |
| `en/sugarloaf-cable-car-park.html` | True | False | final-css-order-viewport-fit |
| `en/sugarloaf-cable-car-restaurant.html` | True | False | final-css-order-viewport-fit |
| `en/sunset.html` | True | False | final-css-order-viewport-fit |
| `en/where-to-eat-near-sugarloaf.html` | True | False | final-css-order-viewport-fit |
| `entardecer.html` | True | False | final-css-order-viewport-fit |
| `es/almoco-morro-da-urca.html` | True | False | final-css-order-viewport-fit |
| `es/almoco.html` | True | False | final-css-order-viewport-fit |
| `es/atardecer.html` | True | False | final-css-order-viewport-fit |
| `es/cafe-da-manha-pao-de-acucar.html` | True | False | final-css-order-viewport-fit |
| `es/cafe-da-manha.html` | True | False | final-css-order-viewport-fit |
| `es/caipirinha-com-vista-rio.html` | True | False | final-css-order-viewport-fit |
| `es/cardapio.html` | True | False | final-css-order-viewport-fit |
| `es/como-llegar.html` | True | False | final-css-order-viewport-fit |
| `es/contato.html` | True | False | final-css-order-viewport-fit |
| `es/desayuno-con-vista-rio-de-janeiro.html` | True | False | final-css-order-viewport-fit |
| `es/donde-comer-cerca-del-pan-de-azucar.html` | True | False | final-css-order-viewport-fit |
| `es/entardecer.html` | True | False | final-css-order-viewport-fit |
| `es/eventos.html` | True | True | final-css-order-viewport-fit |
| `es/feijoada-com-vista-rio-de-janeiro.html` | True | False | final-css-order-viewport-fit |
| `es/feijoada.html` | True | False | final-css-order-viewport-fit |
| `es/gastronomia-carioca.html` | True | False | final-css-order-viewport-fit |
| `es/guia-do-rio.html` | True | False | final-css-order-viewport-fit |
| `es/index.html` | True | False | final-css-order-viewport-fit |
| `es/morro-da-urca.html` | True | False | final-css-order-viewport-fit |
| `es/nossa-visao.html` | True | False | final-css-order-viewport-fit |
| `es/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | True | False | final-css-order-viewport-fit |
| `es/parque-bondinho-pan-de-azucar.html` | True | False | final-css-order-viewport-fit |
| `es/parque-bondinho.html` | True | False | final-css-order-viewport-fit |
| `es/por-do-sol-morro-da-urca.html` | True | False | final-css-order-viewport-fit |
| `es/restaurante-bondinho-pan-de-azucar.html` | True | False | final-css-order-viewport-fit |
| `es/restaurante-morro-da-urca.html` | True | False | final-css-order-viewport-fit |
| `es/restaurantes-cerca-del-pan-de-azucar.html` | True | False | final-css-order-viewport-fit |
| `es/roteiro-meio-dia-urca-pao-de-acucar.html` | True | False | final-css-order-viewport-fit |
| `eventos.html` | True | True | final-css-order-viewport-fit |
| `feijoada-com-vista-rio-de-janeiro.html` | True | False | final-css-order-viewport-fit |
| `feijoada.html` | True | False | final-css-order-viewport-fit |
| `gastronomia-carioca.html` | True | False | final-css-order-viewport-fit |
| `guia-do-rio.html` | True | False | final-css-order-viewport-fit |
| `index.html` | True | False | final-css-order-viewport-fit |
| `morro-da-urca.html` | True | False | final-css-order-viewport-fit |
| `nossa-visao.html` | True | False | final-css-order-viewport-fit |
| `o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | True | False | final-css-order-viewport-fit |
| `onde-comer-no-pao-de-acucar.html` | True | False | final-css-order-viewport-fit |
| `parque-bondinho-pao-de-acucar.html` | True | False | final-css-order-viewport-fit |
| `parque-bondinho.html` | True | False | final-css-order-viewport-fit |
| `por-do-sol-morro-da-urca.html` | True | False | final-css-order-viewport-fit |
| `restaurante-bondinho-pao-de-acucar.html` | True | False | final-css-order-viewport-fit |
| `restaurante-morro-da-urca.html` | True | False | final-css-order-viewport-fit |
| `restaurantes-perto-do-pao-de-acucar.html` | True | False | final-css-order-viewport-fit |
| `restaurantes-romanticos-rio-de-janeiro.html` | True | False | final-css-order-viewport-fit |
| `roteiro-meio-dia-urca-pao-de-acucar.html` | True | False | final-css-order-viewport-fit |
