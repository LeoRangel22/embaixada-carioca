# Schema Rating Guard Report

Status: **PASS**
Mode: **fix**

## Regra de segurança
- JSON-LD não pode conter `aggregateRating` quando a nota vem do Google Reviews.
- JSON-LD não pode conter `ratingValue`, `reviewCount`, `ratingCount`, `bestRating` ou `worstRating` ligados a avaliações externas.
- A nota do Google pode continuar no texto visível da página, mas não no schema estruturado.

Arquivos HTML verificados: **94**
Achados: **0**

## Arquivos alterados / verificados
- `404.html` — ok — blocos JSON-LD: 1 — inválidos: 0
- `almoco-morro-da-urca.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `almoco.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `cafe-da-manha-com-vista-rio-de-janeiro.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `cafe-da-manha-pao-de-acucar.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `cafe-da-manha.html` — ok — blocos JSON-LD: 8 — inválidos: 0
- `caipirinha-com-vista-rio.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `cardapio.html` — ok — blocos JSON-LD: 6 — inválidos: 0
- `como-chegar.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `contato.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `en/almoco-morro-da-urca.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `en/almoco.html` — ok — blocos JSON-LD: 7 — inválidos: 0
- `en/breakfast-with-a-view-rio-de-janeiro.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `en/cafe-da-manha-pao-de-acucar.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `en/cafe-da-manha.html` — ok — blocos JSON-LD: 7 — inválidos: 0
- `en/caipirinha-com-vista-rio.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `en/cardapio.html` — ok — blocos JSON-LD: 6 — inválidos: 0
- `en/contato.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `en/entardecer.html` — ok — blocos JSON-LD: 7 — inválidos: 0
- `en/eventos.html` — ok — blocos JSON-LD: 8 — inválidos: 0
- `en/feijoada-com-vista-rio-de-janeiro.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `en/feijoada.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `en/gastronomia-carioca.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `en/guia-do-rio.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `en/how-to-get-there.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `en/index.html` — ok — blocos JSON-LD: 7 — inválidos: 0
- `en/morro-da-urca.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `en/nossa-visao.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `en/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` — ok — blocos JSON-LD: 7 — inválidos: 0
- `en/parque-bondinho.html` — ok — blocos JSON-LD: 6 — inválidos: 0
- `en/por-do-sol-morro-da-urca.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `en/restaurant-at-urca-hill.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `en/restaurants-near-sugarloaf-mountain.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `en/roteiro-meio-dia-urca-pao-de-acucar.html` — ok — blocos JSON-LD: 6 — inválidos: 0
- `en/sugarloaf-cable-car-park.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `en/sugarloaf-cable-car-restaurant.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `en/sunset.html` — ok — blocos JSON-LD: 8 — inválidos: 0
- `en/where-to-eat-near-sugarloaf.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `entardecer.html` — ok — blocos JSON-LD: 7 — inválidos: 0
- `es/almoco-morro-da-urca.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `es/almoco.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `es/atardecer.html` — ok — blocos JSON-LD: 8 — inválidos: 0
- `es/cafe-da-manha-pao-de-acucar.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `es/cafe-da-manha.html` — ok — blocos JSON-LD: 7 — inválidos: 0
- `es/caipirinha-com-vista-rio.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `es/cardapio.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `es/como-llegar.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `es/contato.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `es/desayuno-con-vista-rio-de-janeiro.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `es/donde-comer-cerca-del-pan-de-azucar.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `es/entardecer.html` — ok — blocos JSON-LD: 7 — inválidos: 0
- `es/eventos.html` — ok — blocos JSON-LD: 11 — inválidos: 0
- `es/feijoada-com-vista-rio-de-janeiro.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `es/feijoada.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `es/gastronomia-carioca.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `es/guia-do-rio.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `es/index.html` — ok — blocos JSON-LD: 7 — inválidos: 0
- `es/morro-da-urca.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `es/nossa-visao.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `es/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` — ok — blocos JSON-LD: 7 — inválidos: 0
- `es/parque-bondinho-pan-de-azucar.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `es/parque-bondinho.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `es/por-do-sol-morro-da-urca.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `es/restaurante-bondinho-pan-de-azucar.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `es/restaurante-morro-da-urca.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `es/restaurantes-cerca-del-pan-de-azucar.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `es/roteiro-meio-dia-urca-pao-de-acucar.html` — ok — blocos JSON-LD: 6 — inválidos: 0
- `eventos.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `feijoada-com-vista-rio-de-janeiro.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `feijoada.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `gastronomia-carioca.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `general-3/index.html` — ok — blocos JSON-LD: 0 — inválidos: 0
- `guia-do-rio.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `home-preview.html` — ok — blocos JSON-LD: 1 — inválidos: 0
- `index.html` — ok — blocos JSON-LD: 8 — inválidos: 0
- `morro-da-urca.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `nossa-visao.html` — ok — blocos JSON-LD: 4 — inválidos: 0
- `o-que-fazer-depois-do-bondinho-pao-de-acucar.html` — ok — blocos JSON-LD: 7 — inválidos: 0
- `offline.html` — ok — blocos JSON-LD: 1 — inválidos: 0
- `onde-comer-no-pao-de-acucar.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `parque-bondinho-pao-de-acucar.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `parque-bondinho.html` — ok — blocos JSON-LD: 6 — inválidos: 0
- `por-do-sol-morro-da-urca.html` — ok — blocos JSON-LD: 3 — inválidos: 0
- `restaurante-bondinho-pao-de-acucar.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `restaurante-morro-da-urca.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `restaurantes-perto-do-pao-de-acucar.html` — ok — blocos JSON-LD: 5 — inválidos: 0
- `restaurantes-romanticos-rio-de-janeiro.html` — ok — blocos JSON-LD: 1 — inválidos: 0
- `roteiro-meio-dia-urca-pao-de-acucar.html` — ok — blocos JSON-LD: 7 — inválidos: 0
- `src/partials/en/footer.html` — ok — blocos JSON-LD: 0 — inválidos: 0
- `src/partials/en/nav.html` — ok — blocos JSON-LD: 0 — inválidos: 0
- `src/partials/es/footer.html` — ok — blocos JSON-LD: 0 — inválidos: 0
- `src/partials/es/nav.html` — ok — blocos JSON-LD: 0 — inválidos: 0
- `src/partials/pt/footer.html` — ok — blocos JSON-LD: 0 — inválidos: 0
- `src/partials/pt/nav.html` — ok — blocos JSON-LD: 0 — inválidos: 0
