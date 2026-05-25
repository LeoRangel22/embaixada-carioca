# Green Solid Palette Audit — Embaixada Carioca

Status: **WARN**
Arquivos HTML verificados: **87**
Páginas com fundo verde sólido real: **43**
Páginas com CSS verde importado diretamente: **0**
Páginas com CSS base: **7**
CSS base importa padrão verde: **True**
Avisos: **38**

## Critério eficiente
- A auditoria ignora mera declaração de variável em `:root`, como `--verde`.
- Só conta como sinal real: `background/background-color` verde aplicado ou classes semânticas de seção verde.
- Página coberta = importa `ec-green-solid-palette.css` diretamente ou importa `ec-stabilization-base.css` quando este já importa o padrão verde.

## Avisos
- `404.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `en/almoco.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `en/cafe-da-manha.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `en/cardapio.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `en/entardecer.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `en/eventos.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `en/feijoada.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `en/gastronomia-carioca.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `en/guia-do-rio.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `en/index.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `en/morro-da-urca.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `en/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `en/parque-bondinho.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `en/roteiro-meio-dia-urca-pao-de-acucar.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `en/sunset.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `entardecer.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `es/almoco.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `es/atardecer.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `es/cafe-da-manha.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `es/cardapio.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `es/entardecer.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `es/eventos.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `es/feijoada.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `es/gastronomia-carioca.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `es/guia-do-rio.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `es/index.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `es/morro-da-urca.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `es/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `es/parque-bondinho.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `es/roteiro-meio-dia-urca-pao-de-acucar.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `eventos.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `feijoada.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `gastronomia-carioca.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `morro-da-urca.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `o-que-fazer-depois-do-bondinho-pao-de-acucar.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `offline.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `parque-bondinho.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `roteiro-meio-dia-urca-pao-de-acucar.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.

## Resumo por página
- `404.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `almoco-morro-da-urca.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `almoco.html` — OK — green_signal=True source=background declaration direct_green_css=False base_css=True covered=True
- `cafe-da-manha-com-vista-rio-de-janeiro.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `cafe-da-manha-pao-de-acucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `cafe-da-manha.html` — OK — green_signal=True source=background declaration direct_green_css=False base_css=True covered=True
- `caipirinha-com-vista-rio.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `cardapio.html` — OK — green_signal=True source=background declaration direct_green_css=False base_css=True covered=True
- `como-chegar.html` — OK — green_signal=False source=- direct_green_css=False base_css=True covered=True
- `contato.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/almoco-morro-da-urca.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/almoco.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `en/breakfast-with-a-view-rio-de-janeiro.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/cafe-da-manha-pao-de-acucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/cafe-da-manha.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `en/caipirinha-com-vista-rio.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/cardapio.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `en/contato.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/entardecer.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `en/eventos.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `en/feijoada-com-vista-rio-de-janeiro.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/feijoada.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `en/gastronomia-carioca.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `en/guia-do-rio.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `en/how-to-get-there.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/index.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `en/morro-da-urca.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `en/nossa-visao.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `en/parque-bondinho.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `en/por-do-sol-morro-da-urca.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/restaurant-at-urca-hill.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/restaurants-near-sugarloaf-mountain.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/roteiro-meio-dia-urca-pao-de-acucar.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `en/sugarloaf-cable-car-park.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/sugarloaf-cable-car-restaurant.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/sunset.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `en/where-to-eat-near-sugarloaf.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `entardecer.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/almoco-morro-da-urca.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/almoco.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/atardecer.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/cafe-da-manha-pao-de-acucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/cafe-da-manha.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/caipirinha-com-vista-rio.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/cardapio.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/como-llegar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/contato.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/desayuno-con-vista-rio-de-janeiro.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/donde-comer-cerca-del-pan-de-azucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/entardecer.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/eventos.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/feijoada-com-vista-rio-de-janeiro.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/feijoada.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/gastronomia-carioca.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/guia-do-rio.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/index.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/morro-da-urca.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/nossa-visao.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/parque-bondinho-pan-de-azucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/parque-bondinho.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/por-do-sol-morro-da-urca.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/restaurante-bondinho-pan-de-azucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/restaurante-morro-da-urca.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/restaurantes-cerca-del-pan-de-azucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/roteiro-meio-dia-urca-pao-de-acucar.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `eventos.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `feijoada-com-vista-rio-de-janeiro.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `feijoada.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `gastronomia-carioca.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `guia-do-rio.html` — OK — green_signal=True source=background declaration direct_green_css=False base_css=True covered=True
- `home-preview.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `index.html` — OK — green_signal=True source=background declaration direct_green_css=False base_css=True covered=True
- `morro-da-urca.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `nossa-visao.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `o-que-fazer-depois-do-bondinho-pao-de-acucar.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `offline.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `onde-comer-no-pao-de-acucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `parque-bondinho-pao-de-acucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `parque-bondinho.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `por-do-sol-morro-da-urca.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `restaurante-bondinho-pao-de-acucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `restaurante-morro-da-urca.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `restaurantes-perto-do-pao-de-acucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `restaurantes-romanticos-rio-de-janeiro.html` — OK — green_signal=False source=- direct_green_css=False base_css=True covered=True
- `roteiro-meio-dia-urca-pao-de-acucar.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
