# Green Solid Palette Audit — Embaixada Carioca

Status: **WARN**
Arquivos HTML verificados: **87**
Páginas com fundo verde sólido real: **43**
Páginas com CSS verde importado diretamente: **28**
Páginas com CSS base: **7**
CSS base importa padrão verde: **True**
Avisos: **10**

## Critério eficiente
- A auditoria ignora mera declaração de variável em `:root`, como `--verde`.
- Só conta como sinal real: `background/background-color` verde aplicado ou classes semânticas de seção verde.
- Página coberta = importa `ec-green-solid-palette.css` diretamente ou importa `ec-stabilization-base.css` quando este já importa o padrão verde.

## Avisos
- `404.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
- `entardecer.html` — Página tem fundo verde sólido real, mas não carrega o padrão verde sólido. Fonte: background declaration.
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
- `en/almoco.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `en/breakfast-with-a-view-rio-de-janeiro.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/cafe-da-manha-pao-de-acucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/cafe-da-manha.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `en/caipirinha-com-vista-rio.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/cardapio.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `en/contato.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/entardecer.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `en/eventos.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `en/feijoada-com-vista-rio-de-janeiro.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/feijoada.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `en/gastronomia-carioca.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `en/guia-do-rio.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `en/how-to-get-there.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/index.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `en/morro-da-urca.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `en/nossa-visao.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `en/parque-bondinho.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `en/por-do-sol-morro-da-urca.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/restaurant-at-urca-hill.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/restaurants-near-sugarloaf-mountain.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/roteiro-meio-dia-urca-pao-de-acucar.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `en/sugarloaf-cable-car-park.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/sugarloaf-cable-car-restaurant.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `en/sunset.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `en/where-to-eat-near-sugarloaf.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `entardecer.html` — WARN — green_signal=True source=background declaration direct_green_css=False base_css=False covered=False
- `es/almoco-morro-da-urca.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/almoco.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `es/atardecer.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `es/cafe-da-manha-pao-de-acucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/cafe-da-manha.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `es/caipirinha-com-vista-rio.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/cardapio.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `es/como-llegar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/contato.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/desayuno-con-vista-rio-de-janeiro.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/donde-comer-cerca-del-pan-de-azucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/entardecer.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `es/eventos.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `es/feijoada-com-vista-rio-de-janeiro.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/feijoada.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `es/gastronomia-carioca.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `es/guia-do-rio.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `es/index.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `es/morro-da-urca.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `es/nossa-visao.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `es/parque-bondinho-pan-de-azucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/parque-bondinho.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
- `es/por-do-sol-morro-da-urca.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/restaurante-bondinho-pan-de-azucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/restaurante-morro-da-urca.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/restaurantes-cerca-del-pan-de-azucar.html` — OK — green_signal=False source=- direct_green_css=False base_css=False covered=False
- `es/roteiro-meio-dia-urca-pao-de-acucar.html` — OK — green_signal=True source=background declaration direct_green_css=True base_css=False covered=True
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
