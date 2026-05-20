# Sprint 2 Locale Quality Fix

## Objetivo
Corrigir rótulos visíveis em PT que vazaram para páginas EN/ES nos blocos GEO e landings de café da manhã.

## Contadores
- html_scanned: 86
- html_updated: 18
- en_fixes: 32
- es_fixes: 32
- pt_fixes: 0
- warnings: 4

## Correções
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | 'Resposta direta · SEO + GEO' -> 'Direct answer · SEO + GEO' | 1
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | '>Café<' -> '>Breakfast<' | 1
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | '>Almoço<' -> '>Lunch<' | 1
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | '>Entardecer<' -> '>Sunset<' | 1
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | '>Cardápio<' -> '>Menu<' | 1
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | 'href="/cafe-da-manha.html"' -> 'href="/en/cafe-da-manha.html"' | 1
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | 'href="/almoco.html"' -> 'href="/en/almoco.html"' | 1
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | 'href="/entardecer.html"' -> 'href="/en/entardecer.html"' | 1
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | 'href="/cardapio.html"' -> 'href="/en/cardapio.html"' | 1
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | '<a class="brand" href="/">Embaixada Carioca</a>' -> '<a class="brand" href="/en/">Embaixada Carioca</a>' | 1
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | 'Morro da Urca · Parque Bondinho Pão de Açúcar' -> 'Urca Hill · Sugarloaf Cable Car Park' | 2
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | '>Como chegar<' -> '>How to get there<' | 1
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | 'href="/guia-do-rio.html"' -> 'href="/en/guia-do-rio.html"' | 1
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | 'Por que essa página existe?' -> 'Why does this page exist?' | 1
- EN_FIXES: en/breakfast-with-a-view-rio-de-janeiro.html | 'Esta landing foi criada para responder diretamente às buscas de alta intenção sobre café da manhã com vista, restaurantes no Morro da Urca e experiências dentro do Parque Bondinho Pão de Açúcar.' -> 'This page was created to answer high-intent searches about breakfast with a view, restaurants at Urca Hill and experiences inside Sugarloaf Cable Car Park.' | 1
- UPDATED: en/breakfast-with-a-view-rio-de-janeiro.html
- EN_FIXES: en/cafe-da-manha.html | 'aria-label="Resposta direta para busca e IA"' -> 'aria-label="Direct answer for search and AI"' | 1
- EN_FIXES: en/cafe-da-manha.html | 'Resposta direta · SEO + GEO' -> 'Direct answer · SEO + GEO' | 1
- UPDATED: en/cafe-da-manha.html
- EN_FIXES: en/guia-do-rio.html | 'aria-label="Resposta direta para busca e IA"' -> 'aria-label="Direct answer for search and AI"' | 1
- EN_FIXES: en/guia-do-rio.html | 'Resposta direta · SEO + GEO' -> 'Direct answer · SEO + GEO' | 1
- UPDATED: en/guia-do-rio.html
- EN_FIXES: en/index.html | 'aria-label="Resposta direta para busca e IA"' -> 'aria-label="Direct answer for search and AI"' | 1
- EN_FIXES: en/index.html | 'Resposta direta · SEO + GEO' -> 'Direct answer · SEO + GEO' | 1
- UPDATED: en/index.html
- EN_FIXES: en/restaurant-at-urca-hill.html | 'href="/cardapio.html"' -> 'href="/en/cardapio.html"' | 1
- EN_FIXES: en/restaurant-at-urca-hill.html | 'Morro da Urca · Parque Bondinho Pão de Açúcar' -> 'Urca Hill · Sugarloaf Cable Car Park' | 1
- UPDATED: en/restaurant-at-urca-hill.html
- EN_FIXES: en/restaurants-near-sugarloaf-mountain.html | 'href="/cardapio.html"' -> 'href="/en/cardapio.html"' | 1
- EN_FIXES: en/restaurants-near-sugarloaf-mountain.html | 'Morro da Urca · Parque Bondinho Pão de Açúcar' -> 'Urca Hill · Sugarloaf Cable Car Park' | 1
- UPDATED: en/restaurants-near-sugarloaf-mountain.html
- EN_FIXES: en/sugarloaf-cable-car-park.html | 'href="/cardapio.html"' -> 'href="/en/cardapio.html"' | 1
- EN_FIXES: en/sugarloaf-cable-car-park.html | 'Morro da Urca · Parque Bondinho Pão de Açúcar' -> 'Urca Hill · Sugarloaf Cable Car Park' | 1
- UPDATED: en/sugarloaf-cable-car-park.html
- EN_FIXES: en/sugarloaf-cable-car-restaurant.html | 'href="/cardapio.html"' -> 'href="/en/cardapio.html"' | 1
- EN_FIXES: en/sugarloaf-cable-car-restaurant.html | 'Morro da Urca · Parque Bondinho Pão de Açúcar' -> 'Urca Hill · Sugarloaf Cable Car Park' | 1
- UPDATED: en/sugarloaf-cable-car-restaurant.html
- EN_FIXES: en/where-to-eat-near-sugarloaf.html | 'href="/cardapio.html"' -> 'href="/en/cardapio.html"' | 1
- EN_FIXES: en/where-to-eat-near-sugarloaf.html | 'Morro da Urca · Parque Bondinho Pão de Açúcar' -> 'Urca Hill · Sugarloaf Cable Car Park' | 1
- UPDATED: en/where-to-eat-near-sugarloaf.html
- ES_FIXES: es/cafe-da-manha.html | 'aria-label="Resposta direta para busca e IA"' -> 'aria-label="Respuesta directa para búsqueda e IA"' | 1
- ES_FIXES: es/cafe-da-manha.html | 'Resposta direta · SEO + GEO' -> 'Respuesta directa · SEO + GEO' | 1
- UPDATED: es/cafe-da-manha.html
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | 'Resposta direta · SEO + GEO' -> 'Respuesta directa · SEO + GEO' | 1
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | '>Café<' -> '>Desayuno<' | 1
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | '>Almoço<' -> '>Almuerzo<' | 1
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | '>Entardecer<' -> '>Atardecer<' | 1
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | '>Cardápio<' -> '>Menú<' | 1
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | 'href="/cafe-da-manha.html"' -> 'href="/es/cafe-da-manha.html"' | 1
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | 'href="/almoco.html"' -> 'href="/es/almoco.html"' | 1
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | 'href="/entardecer.html"' -> 'href="/es/entardecer.html"' | 1
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | 'href="/cardapio.html"' -> 'href="/es/cardapio.html"' | 1
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | '<a class="brand" href="/">Embaixada Carioca</a>' -> '<a class="brand" href="/es/">Embaixada Carioca</a>' | 1
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | 'Morro da Urca · Parque Bondinho Pão de Açúcar' -> 'Morro da Urca · Parque Bondinho Pan de Azúcar' | 2
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | '>Como chegar<' -> '>Cómo llegar<' | 1
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | 'href="/guia-do-rio.html"' -> 'href="/es/guia-do-rio.html"' | 1
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | 'Por que essa página existe?' -> '¿Por qué existe esta página?' | 1
- ES_FIXES: es/desayuno-con-vista-rio-de-janeiro.html | 'Esta landing foi criada para responder diretamente às buscas de alta intenção sobre café da manhã com vista, restaurantes no Morro da Urca e experiências dentro do Parque Bondinho Pão de Açúcar.' -> 'Esta página fue creada para responder directamente a búsquedas de alta intención sobre desayuno con vista, restaurantes en el Morro da Urca y experiencias dentro del Parque Bondinho Pan de Azúcar.' | 1
- UPDATED: es/desayuno-con-vista-rio-de-janeiro.html
- ES_FIXES: es/donde-comer-cerca-del-pan-de-azucar.html | 'href="/cardapio.html"' -> 'href="/es/cardapio.html"' | 1
- ES_FIXES: es/donde-comer-cerca-del-pan-de-azucar.html | 'Morro da Urca · Parque Bondinho Pão de Açúcar' -> 'Morro da Urca · Parque Bondinho Pan de Azúcar' | 1
- UPDATED: es/donde-comer-cerca-del-pan-de-azucar.html
- ES_FIXES: es/guia-do-rio.html | 'aria-label="Resposta direta para busca e IA"' -> 'aria-label="Respuesta directa para búsqueda e IA"' | 1
- ES_FIXES: es/guia-do-rio.html | 'Resposta direta · SEO + GEO' -> 'Respuesta directa · SEO + GEO' | 1
- UPDATED: es/guia-do-rio.html
- ES_FIXES: es/index.html | 'aria-label="Resposta direta para busca e IA"' -> 'aria-label="Respuesta directa para búsqueda e IA"' | 1
- ES_FIXES: es/index.html | 'Resposta direta · SEO + GEO' -> 'Respuesta directa · SEO + GEO' | 1
- UPDATED: es/index.html
- ES_FIXES: es/parque-bondinho-pan-de-azucar.html | 'href="/cardapio.html"' -> 'href="/es/cardapio.html"' | 1
- ES_FIXES: es/parque-bondinho-pan-de-azucar.html | 'Morro da Urca · Parque Bondinho Pão de Açúcar' -> 'Morro da Urca · Parque Bondinho Pan de Azúcar' | 1
- UPDATED: es/parque-bondinho-pan-de-azucar.html
- ES_FIXES: es/restaurante-bondinho-pan-de-azucar.html | 'href="/cardapio.html"' -> 'href="/es/cardapio.html"' | 1
- ES_FIXES: es/restaurante-bondinho-pan-de-azucar.html | 'Morro da Urca · Parque Bondinho Pão de Açúcar' -> 'Morro da Urca · Parque Bondinho Pan de Azúcar' | 1
- UPDATED: es/restaurante-bondinho-pan-de-azucar.html
- ES_FIXES: es/restaurante-morro-da-urca.html | 'href="/cardapio.html"' -> 'href="/es/cardapio.html"' | 1
- ES_FIXES: es/restaurante-morro-da-urca.html | 'Morro da Urca · Parque Bondinho Pão de Açúcar' -> 'Morro da Urca · Parque Bondinho Pan de Azúcar' | 1
- UPDATED: es/restaurante-morro-da-urca.html
- ES_FIXES: es/restaurantes-cerca-del-pan-de-azucar.html | 'href="/cardapio.html"' -> 'href="/es/cardapio.html"' | 1
- ES_FIXES: es/restaurantes-cerca-del-pan-de-azucar.html | 'Morro da Urca · Parque Bondinho Pão de Açúcar' -> 'Morro da Urca · Parque Bondinho Pan de Azúcar' | 1
- UPDATED: es/restaurantes-cerca-del-pan-de-azucar.html

## Alertas remanescentes
- VISIBLE_LANG_WARNING: en/cafe-da-manha.html [en] contém 'Café'
- VISIBLE_LANG_WARNING: en/guia-do-rio.html [en] contém 'Café'
- VISIBLE_LANG_WARNING: es/cafe-da-manha.html [es] contém 'Café'
- VISIBLE_LANG_WARNING: es/guia-do-rio.html [es] contém 'Café'
