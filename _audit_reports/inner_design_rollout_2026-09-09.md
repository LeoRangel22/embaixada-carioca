# Lote de design das páginas internas — 09/09/2026

## Escopo entregue

24 páginas: Cardápio, Almoço, Café da Manhã, Eventos, Como Chegar, Guia do Rio, Feijoada e Entardecer, em PT/EN/ES. A abertura usa composição responsiva em fluxo, foto e texto separados no desktop e empilhados no celular.

- Navegação compacta, sem colisão entre avaliações e reserva; fundo sólido também após rolagem.
- Menu e idiomas acessíveis no celular. Links de idioma levam à página equivalente.
- Painel móvel fornecido nas quatro páginas onde faltava e nas três Feijoadas cujo botão não funcionava.
- Botões com uma ação principal, ações secundárias discretas, foco visível e área de toque mínima de 44px.
- Removidos popup automático de WhatsApp e painel lateral redundante com estimativas fixas de pôr do sol. Informações úteis e atribuição dos prêmios preservadas abaixo da abertura.
- Aviso de ingresso com fundo e texto de contraste legível.
- Ícones vetoriais consistentes na navegação inferior das 24 páginas e três homes.

## Refino editorial e fotográfico

Cardápio e Café da Manhã nos três idiomas receberam abertura curta e localizada. Cardápio prioriza explorar categorias, mantendo reserva como alternativa. Itens e preços não foram removidos.

Fotos conferidas visualmente antes do uso:

- Cardápio: `assets/almoco-picanha-grelhada.webp`, prato de carne grelhada com acompanhamentos.
- Café: `assets/cafe/cafe-da-embaixada-mesa-completa.webp`, mesa de café da manhã.
- Música: `assets/fotos/banda-pao-de-acucar-01.webp`, banda com o Pão de Açúcar ao fundo. Substitui duas referências inexistentes em EN/ES e uma imagem de café incorretamente associada a banda em PT.

## Validação

| Verificação | Resultado |
|---|---|
| 24 páginas × 320, 390, 768, 1024, 1440 e 1920px | 144/144 sem overflow horizontal, colisão no topo, erro JS ou imagem quebrada na primeira dobra; menu móvel abre e fecha |
| Regressão das três homes nas mesmas larguras | 18/18 PASS |
| Botões/introdução dentro da abertura e fundo do topo após rolagem | 48/48 PASS (390 e 1440px) |
| Preservação de preços, canonical/hreflang e JSON-LD | PASS nas 24 páginas; única exceção explícita: três URLs de thumbnail corrigidas |
| Chaves duplicadas de JSON-LD | PASS, 115 páginas, zero ocorrências |
| Guard de Review/Rating/AggregateRating | PASS, 115 páginas, zero ocorrências |
| Auditoria hreflang | PASS, mínimo 100 |
| Whitespace/diff | PASS |

Na migração inicial também foi comparado o conteúdo serializado dos cards de Cardápio e Café da Manhã, sem alterações. O sitemap atualiza lastmod somente para URLs do lote presentes nele.

Os testes são verificações específicas, não certificação WCAG AAA nem garantia de todas as seções do site. Capturas locais e resultados detalhados ficam no workspace da tarefa, fora do repositório.

## Próximo lote

1. Refinar galerias, espaçamento e hierarquia das seções abaixo da abertura, começando por Almoço, Feijoada e Eventos.
2. Revisar os textos longos e traduções remanescentes do corpo das páginas; este lote revisou integralmente apenas as seis aberturas de Cardápio/Café.
3. Conferir individualmente outras associações foto/legenda: nomes de arquivos não são fonte confiável.
4. Validar os vídeos reais e seus metadados: há embedUrl legado com slug textual em Entardecer. Os guards estruturais acima não atestam a existência desses vídeos.

Nenhum workflow de autoalteração foi adicionado. O script de migração é manual e idempotente para aberturas já migradas.
