# Refinamento de seções — Almoço, Feijoada e Eventos

Data: 09/09/2026. Escopo: nove páginas, PT/EN/ES.

## Entrega

- Espaçamento consistente entre seções e largura de leitura controlada.
- Hierarquia de títulos, parágrafos e botões; produtos e descrições preservados.
- Por solicitação expressa do usuário antes da publicação, preços retirados destas nove páginas, inclusive ofertas/valores estáticos do JSON-LD. Porções e descrições permanecem.
- Acesso destacado ao cardápio completo com preços: https://livemenu.app/menu/61cb5857aa455a0012ebbdcf . O endereço legado Tagme redireciona para esse menu; API pública confirmou Embaixada Carioca e produtos em vários idiomas (HTTP 200). A aplicação visual externa não carregou no navegador de teste por falhas de requisição ao serviço, portanto não foi atestada visualmente.
- Galerias com fotos maiores, legendas legíveis, bordas sutis e sem sombras pesadas.
- Galerias de quatro fotos em duas colunas, evitando última foto isolada; uma coluna no celular.
- Grades de pratos, formatos e processo adaptadas a telas pequenas.
- Título do bloco complementar de Feijoada corrigido no tablet.
- Barra móvel de reserva redundante escondida; navegação inferior e CTAs originais permanecem.
- Imagem de pintura associada a música em Eventos substituída pela foto de banda já conferida (`assets/fotos/banda-pao-de-acucar-01.webp`). Não houve revisão factual de todas as outras legendas.

## Verificações

- 27 cenários: nove páginas em 390, 768 e 1440px, sem overflow horizontal, elementos das grades fora da tela ou erros JavaScript.
- A etapa de formatação preservou texto e schema. A etapa autorizada posterior removeu preços e ofertas estáticas, mantendo entidades e produtos e adicionando o link ao cardápio online.
- Guards de dados estruturados: 115 páginas, sem chaves duplicadas e sem Review/Rating/AggregateRating indevido.
- Nenhum workflow novo. Alterações restritas às nove páginas e folha de estilo própria.

## Limites

Este lote não é certificação de acessibilidade AAA nem nova auditoria de horários, alegações ou traduções. A remoção de preços se limita às nove páginas do lote, não às páginas Cardápio nem ao site inteiro. Conteúdo longo/repetitivo e outras associações foto/legenda devem passar por revisão editorial separada.
