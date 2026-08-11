# GSC Search Performance — mapa de palavras prioritárias

Data da análise: **2026-08-11**

Período do arquivo: **últimos 28 dias (2026-07-13 a 2026-08-09)**
Status geral: **PASS**

## Critério de prioridade

- **Ouro / super prioridade:** célula amarela na aba `Consultas`; objetivo preferencial de posição **1 a 3**.
- **Prioritária:** consulta em negrito, sem preenchimento amarelo.
- Total classificado na planilha: **26 palavras-ouro** e **60 palavras prioritárias**.
- Cada intenção foi associada a uma única página principal e ao idioma da consulta, evitando distribuir a mesma palavra entre várias páginas.

## Desempenho geral do período

- Cliques: **1.345**.
- Impressões: **59.201**.
- Maior volume: celular, com **940 cliques** e **43.931 impressões**.
- Algumas células da coluna `Posição` chegaram formatadas como números seriais acima de 45.000. Esses valores foram considerados inválidos para decisões de ranking; cliques, impressões, idioma e prioridade visual foram preservados.

## Palavras-ouro e página canônica definida

| Página principal | Idioma | Palavras-ouro direcionadas | Situação |
|---|---|---|---|
| `restaurante-pao-de-acucar.html` | PT | restaurante pão de açúcar; restaurante no pão de açúcar; restaurante pao de acucar; restaurante pao de acucar rio de janeiro; restaurante no pao de açucar rj; restaurante no pao de acucar; restaurantes pao de acucar | Reforço editorial aplicado |
| `restaurante-morro-da-urca.html` | PT | restaurante morro da urca; restaurante no morro da urca; morro da urca restaurante; restaurantes na urca; restaurantes urca; restaurantes na urca com vista; restaurante na urca rj; restaurante na urca com vista | Reforço editorial aplicado; consolida também a intenção Urca |
| `cafe-da-manha.html` | PT | cafe da manha na urca; cafe da manha no pao de acucar; cafe da manha pao de acucar; cafe da manha no pao de acucar rj | Reforço editorial aplicado |
| `restaurante-bondinho-pao-de-acucar.html` | PT | restaurante no bondinho do pão de açúcar; tem restaurante no bondinho do pão de açúcar | Resposta direta e acesso correto aplicados |
| `restaurantes-perto-do-pao-de-acucar.html` | PT | restaurante perto de mim; restaurantes perto de mim; restaurante perto do pao de acucar | Intenção local reforçada com contexto geográfico |
| `index.html` | PT | restaurante embaixada carioca; embaixada carioca restaurante | Já estava alinhada; mantida para não desestabilizar a home |

## Prioridades por idioma

### Português

| Cluster | Página principal |
|---|---|
| Morro da Urca, Morro da Urca RJ, Morro de Urca | `morro-da-urca.html` |
| Restaurante na Urca / Morro da Urca | `restaurante-morro-da-urca.html` |
| Horário, ingressos e informações do Bondinho | `parque-bondinho.html` |
| Av. Pasteur 520 e endereço | `como-chegar.html` |
| Cardápio da Embaixada Carioca | `cardapio.html` |
| Restaurante no Bondinho | `restaurante-bondinho-pao-de-acucar.html` |
| Restaurante perto do Pão de Açúcar | `restaurantes-perto-do-pao-de-acucar.html` |
| O que fazer na Urca / no Pão de Açúcar | `guia-do-rio.html` e a página específica do roteiro, sem duplicar a intenção comercial |

### Inglês

| Consultas prioritárias | Página principal | Ação |
|---|---|---|
| where to eat breakfast | `en/cafe-da-manha.html` | Bloco editorial em inglês aplicado |
| sugarloaf cable car tickets; sugarloaf mountain tickets official website | `en/parque-bondinho.html` | Conteúdo de tickets apontando para o site oficial |
| sugar loaf cable car av. pasteur 520 urca rio de janeiro; variantes com official/address | `en/parque-bondinho.html` | Endereço e orientação integralmente em inglês |

### Espanhol

| Consultas prioritárias | Página principal | Ação |
|---|---|---|
| pan de azucar entradas | `es/parque-bondinho.html` | Conteúdo de entradas e acesso reescrito em espanhol |
| almuerzo | `es/almoco.html` | Página reforçada e meta description duplicada removida |

## Correções aplicadas

- Reforços visíveis e naturais nas páginas comerciais vencedoras, sem criar novas URLs.
- Diferencial confirmado pelo responsável padronizado em PT/EN/ES: a Embaixada Carioca é o único restaurante do Parque Bondinho com vista direta para o Pão de Açúcar; as demais opções gastronômicas estão voltadas para outros cartões-postais do Rio.
- Conteúdo misturado em português/inglês removido de `en/parque-bondinho.html`.
- Conteúdo misturado em português/espanhol removido de `es/parque-bondinho.html`.
- Alegações não comprovadas de “restaurante oficial” e “único restaurante completo” removidas das versões EN/ES do Parque Bondinho.
- Regra de acesso uniformizada nos dois idiomas: acesso usual pelo Parque Bondinho; trilha como alternativa quando aberta; ingresso necessário para usar o teleférico, seguir ao Pão de Açúcar ou descer à Praia Vermelha de teleférico.
- `es/almoco.html` ficou com uma única meta description e sem a alegação incorreta “melhor feijoada do Brasil”.
- Nenhum canonical ou hreflang foi alterado.
- Nenhum `Review`, `Rating` ou `AggregateRating` foi adicionado ao JSON-LD.

## Páginas alteradas

- `restaurante-pao-de-acucar.html`
- `restaurante-morro-da-urca.html`
- `restaurante-bondinho-pao-de-acucar.html`
- `restaurantes-perto-do-pao-de-acucar.html`
- `cafe-da-manha.html`
- `en/cafe-da-manha.html`
- `en/parque-bondinho.html`
- `es/parque-bondinho.html`
- `es/almoco.html`

## Próxima medição

Comparar o mesmo conjunto no Search Console após **28 dias**, com foco nas palavras-ouro atualmente entre as posições 3 e 10. Não alterar novamente as páginas que já estão entre 1 e 3 antes dessa janela, salvo erro factual ou visual.
