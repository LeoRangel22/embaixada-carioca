# Visual Contrast Risk Audit

Static guardrail for visual contrast regressions in current pages.

- Global contrast hotfix coverage: PASS
- Breakfast lede sentinel present: PASS
- Breakfast lede sentinel selector: `body[data-screen-label="Café da Manhã"] #o-que-servimos .sec-head p.lede`
- Hero side frame sentinel present: PASS
- Hero side frame selector: `body .ec-page-hero-side-frame`

## index.html
- VISUAL_CHECK: 50 pattern(s) detected but covered by global contrast hotfix
  - covered-by-final-dark-section-lock | dark-section-lede-needs-visual-check | <p> class='lede' | A Embaixada Carioca é o restaurante do Bondinho Pão de Açúcar — o único restaurante com vista direta para o Pão de Açúcar, no alto do Morro da Urca. Acompanha o
  - covered-by-final-dark-section-lock | dark-section-lede-needs-visual-check | <p> class='lede' | 🏆 Melhor Feijoada do Rio de Janeiro — Veja Rio Comer & Beber 2025/2026 · 2º melhor chopp Heineken do Brasil · 4.8★ em mais de 7.779 avaliações no Google.
  - covered-by-final-dark-section-lock | dark-section-lede-needs-visual-check | <p> class='lede' | O Sunset no Bondinho transformou o fim de tarde no alto do Morro da Urca em um evento único no Rio. O DJ Tommax — o DJ do Bondinho — comanda as pick-ups no Jard
  - covered-by-final-dark-section-lock | dark-section-lede-needs-visual-check | <p> class='lede' | Reuniões executivas, almoços corporativos, lançamentos, treinamentos e roteiros premium para grupos — recebidos a 227 metros de altura, com o Pão de Açúcar como
  - covered-by-final-dark-section-lock | dark-section-lede-needs-visual-check | <p> class='lede' | O Restaurante Morro da Urca está aberto todos os dias — café da manhã das 8h30 às 11h30, almoço das 11h30 às 17h e entardecer das 17h às 21h. Um dos melhores re
  - covered-by-light-card-lock | light-text-on-light-bg | <p> class='' | Aberto todos os dias · reservas recomendadas para fins de semana e feijoada.
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h2> class='' | fica dentro do Parque Bondinho Pão de Açúcar, na primeira parada do teleférico, a 227 metros de altitude, com janelões voltados para o Pão de Açúcar e Baía de G
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h3> class='' | Vista direta para o Pão de Açúcar
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h3> class='' | Gastronomia brasileira de verdade
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h3> class='' | Aberto todos os dias, o dia inteiro
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h3> class='' | Eventos privados e corporativos sob consulta, com formatos personalizados para grupos, coquetéis e experiências no Morro da Urca
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h2> class='' | Onde comer no Parque Bondinho o Morro da Urca?
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | A resposta é a Embaixada Carioca — o restaurante do Parque Bondinho Pão de Açúcar, na primeira parada do teleférico, no Morro da Urca. Café da manhã, almoço com
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h3> class='' | Café da Manhã no Morro da Urca
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Todos os dias · 8h30 às 11h30 · Vista panorâmica para o Pão de Açúcar · Pães artesanais, frutas tropicais e café especial.
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Todos os dias · 11h30 às 17h · Especialidade Picanha Brasileira · Feijoada premiada Veja Rio 2025/2026 · Gastronomia carioca.
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h3> class='' | Caipirinha & Chopp no Bondinho
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Todos os dias · Caipirinha com cachaça Magnífica premiada · Chopp Heineken gelado · o mais premiado bar do Parque Bondinho.
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h3> class='' | Eventos Privados no Morro da Urca
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Casamentos, aniversários, eventos corporativos · Capacidade sob consulta · Vista panorâmica para o Pão de Açúcar · único.
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='eyebrow' | Do café da manhã ao happy hour
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h2> class='' | O Cardápio da Embaixada Carioca
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | No Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, servimos gastronomia brasileira de verdade — da empada artesanal ao bobó de camarão, do açaí gelado à
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Servido todos os dias (8h30–11h30). Sucos naturais, água de coco, açaí, frutas frescas e pão de queijo — tudo com vista panorâmica para o Pão de Açúcar.
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Especialidade Picanha Brasileira (400g), Feijoada premiada Veja Rio 2025/2026, Bobó de Camarão cremoso, Bolinho de Bacalhau, Pastel crocante e Empada artesanal 
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Caipirinha com cachaça Magnífica premiada, Chopp Heineken gelado (referência no Rio), sucos naturais de frutas tropicais, água de coco fresca e açaí cremoso.
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Espetinho, Pastel, Empada, Bolinho de Bacalhau, Picadinho e Sanduíches — perfeitos para um lanche rápido entre as atrações do Bondinho.
  - covered-by-final-dark-section-lock | dark-section-lede-needs-visual-check | <p> class='lede' | As perguntas mais comuns de quem busca onde comer no Rio de Janeiro com vista para o Pão de Açúcar.
  - ... +22 more

## cafe-da-manha.html
- VISUAL_CHECK: 15 pattern(s) detected but covered by global contrast hotfix
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Hoje
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | Por do sol às 17h44
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Resumo
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | O café da manhã com vista para o Pão de Açúcar mais especial do Rio de Janeiro — servido todos os dias , das 8h30 às 11h30, no alto do Morro da Urca. Pães artes
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Vista
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | Pão de Açúcar em primeiro plano
  - covered-by-breakfast-sentinel-lock | breakfast-lede-sentinel | <p> class='lede' | Do Café da Embaixada para 2 ao açaí orgânico, ovos na chapa e cafés especiais — servido todos os dias, das 8h30 às 11h30, no alto do Morro da Urca.
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h2> class='' | Restaurante, café da manhã, feijoada, picanha e drinks no Morro da Urca.
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Explore os principais momentos da Embaixada Carioca dentro do Parque Bondinho Pão de Açúcar: café da manhã com vista, almoço brasileiro, feijoada premiada da Ac
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h3> class='' | Tem café da manhã no Pão de Açúcar?
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='faq-answer' | Sim. A Embaixada Carioca serve café da manhã todos os dias, das 8h30 às 11h30, no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com vista direta para 
  - covered-by-light-card-lock | light-text-on-light-bg | <h2> class='' | Café da manhã na Urca, dentro do Parque Bondinho Pão de Açúcar
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h2> class='' | Café da manhã na Urca, dentro do Parque Bondinho Pão de Açúcar
  - covered-by-light-card-lock | light-text-on-light-bg | <p> class='' | Para quem busca café da manhã na Urca, café da manhã no Bondinho Pão de Açúcar ou uma experiência de manhã com vista no Rio de Janeiro, a Embaixada Carioca abre
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Para quem busca café da manhã na Urca, café da manhã no Bondinho Pão de Açúcar ou uma experiência de manhã com vista no Rio de Janeiro, a Embaixada Carioca abre

## almoco.html
- VISUAL_CHECK: 12 pattern(s) detected but covered by global contrast hotfix
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Hoje
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | Por do sol às 17h44
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Resumo
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | O único almoço dentro do Parque Bondinho Pão de Açúcar , a 227 metros de altitude no Morro da Urca. Gastronomia brasileira premiada: picanha à brasileira e a fe
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Vista
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | Pão de Açúcar em primeiro plano
  - covered-by-final-dark-section-lock | dark-section-lede-needs-visual-check | <p> class='lede' | Receitas clássicas da gastronomia brasileira servidas com técnica contemporânea e ingredientes selecionados — o sabor do Brasil com a vista mais bonita do Rio. 
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h3> class='' | O roteiro perfeito: Bondinho + Almoço
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Para otimizar seu tempo e orçamento no Rio de Janeiro, recomendamos combinar a visita ao Parque Bondinho com seu almoço. Ao invés de procurar restaurantes na Ur
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Nossa picanha grelhada (prato mais vendido) e o Chopp Heineken (eleito o melhor da cidade) são as escolhas favoritas de quem busca a autêntica alma carioca após
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h2> class='' | Restaurante, café da manhã, feijoada, picanha e drinks no Morro da Urca.
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Explore os principais momentos da Embaixada Carioca dentro do Parque Bondinho Pão de Açúcar: café da manhã com vista, almoço brasileiro, feijoada premiada da Ac

## cardapio.html
- VISUAL_CHECK: 11 pattern(s) detected but covered by global contrast hotfix
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Hoje
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | Por do sol às 17h44
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Resumo
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | Do café da manhã com vista para o Pão de Açúcar ao entardecer com drinks autorais — o cardápio do Restaurante Morro da Urca celebra a gastronomia brasileira com
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Vista
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | Pão de Açúcar em primeiro plano
  - covered-by-light-card-lock | light-text-on-light-bg | <p> class='' | Café da manhã, almoço com feijoada premiada ou entardecer com drinks autorais — todos com vista para o Pão de Açúcar, no alto do Morro da Urca.
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h2> class='' | Restaurante, café da manhã, feijoada, picanha e drinks no Morro da Urca.
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Explore os principais momentos da Embaixada Carioca dentro do Parque Bondinho Pão de Açúcar: café da manhã com vista, almoço brasileiro, feijoada premiada da Ac
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h3> class='' | Tem feijoada, picanha e chope Heineken no Morro da Urca?
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='faq-answer' | Sim. A Embaixada Carioca serve a feijoada premiada da Academia da Cachaça, Picanha Brasileira, caipirinhas e chope Heineken premiado no Morro da Urca, dentro do

## como-chegar.html
- VISUAL_CHECK: 6 pattern(s) detected but covered by global contrast hotfix
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Hoje
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | Por do sol às 17h44
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Resumo
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | Estamos no Morro da Urca, a primeira parada do Parque Bondinho Pão de Açúcar. O acesso é pela Praia Vermelha, na Avenida Pasteur, 520, Urca.
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Vista
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | Pão de Açúcar em primeiro plano

## eventos.html
- PASS: no static contrast risk patterns found

## guia-do-rio.html
- VISUAL_CHECK: 13 pattern(s) detected but covered by global contrast hotfix
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Hoje
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | Por do sol às 17h44
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Resumo
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | Planejando uma viagem para o Rio de Janeiro? Descobrir o que fazer no Rio exige um roteiro que equilibre os cartões-postais mundiais com a autêntica gastronomia
  - covered-by-hero-side-frame-lock | hero-side-frame-label-sentinel | <span> class='l' | Vista
  - covered-by-hero-side-frame-lock | hero-side-frame-value-sentinel | <span> class='v' | Pão de Açúcar em primeiro plano
  - covered-by-light-card-lock | light-text-on-light-bg | <p> class='' | Café da manhã, almoço ou entardecer — todos com vista de frente para o Pão de Açúcar, no alto do Morro da Urca.
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h2> class='' | Restaurante, café da manhã, feijoada, picanha e drinks no Morro da Urca.
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Explore os principais momentos da Embaixada Carioca dentro do Parque Bondinho Pão de Açúcar: café da manhã com vista, almoço brasileiro, feijoada premiada da Ac
  - covered-by-light-card-lock | light-text-on-light-bg | <h2> class='' | Complete o passeio com a Embaixada Carioca
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <h2> class='' | Complete o passeio com a Embaixada Carioca
  - covered-by-light-card-lock | light-text-on-light-bg | <p> class='' | Se o seu roteiro passa pelo Bondinho, Morro da Urca ou Pão de Açúcar, reserve uma parada para café da manhã, almoço brasileiro, caipirinhas ou uma experiência c
  - covered-by-dark-section-lock | dark-text-on-dark-bg | <p> class='' | Se o seu roteiro passa pelo Bondinho, Morro da Urca ou Pão de Açúcar, reserve uma parada para café da manhã, almoço brasileiro, caipirinhas ou uma experiência c

## Summary
- Total static patterns detected: 107
- Open contrast risks: 0
- Covered patterns requiring browser visual check: 107
- Required next validation: browser screenshots for cafe-da-manha.html, guia-do-rio.html, index.html, almoco.html, cardapio.html and eventos.html after deployment.