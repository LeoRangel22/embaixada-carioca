# Comparação do diagnóstico v9 com o repositório e o site publicado

Data da verificação: 2026-08-24

Atualização operacional: **31/08/2026**

> O retrato atual supersede as pendências externas deste relatório: Cloudflare Pages é a hospedagem pública principal; HSTS curto está ativo; aliases, HTTP, `index.html` e `.com.br` respondem com 301; o sitemap foi reenviado em 27/08 e processado com 97 páginas. Consulte `docs/current-site-status.md`.

Status geral: **PASS COM AÇÕES EXTERNAS PENDENTES**

## Resumo executivo

O diagnóstico v9 acerta a direção estratégica — conversão, distribuição e qualidade dos dados devem ter prioridade sobre novas páginas —, mas alguns itens já estavam resolvidos ou foram medidos incorretamente. As correções verificáveis no repositório foram aplicadas sem reintroduzir `Review`, `Rating` ou `AggregateRating`.

## Comparação objetiva

| Item do diagnóstico | Estado verificado | Decisão |
|---|---|---|
| 7 workflows ativos | Confirmado no GitHub | Manter os 7; 30 workflows legados estão desativados |
| 17 alertas visuais | Fechados no relatório visual existente | Não criar novos locks de CSS sem regressão visual comprovada |
| Paridade do cardápio | Confirmada: 12 seções e 149 itens em PT/EN/ES | Manter como fonte única e revisar apenas legendas/fotos |
| JSON-LD sem review/rating | Confirmado pelos guards | Preservar a proibição |
| HTTP para HTTPS | O site publicado já responde **301** | Item do diagnóstico está desatualizado |
| `.com.br` para `.com` | As variantes testadas já respondem **301** | Item do diagnóstico está desatualizado |
| HSTS | Ativo desde a migração para Cloudflare Pages, `max-age=86400` | Monitorar antes de ampliar |
| Home com dois Restaurant | Incorreto: havia **1 Restaurant** | Nenhuma fusão necessária |
| Home com dois WebPage | Confirmado | Corrigido: mantido apenas o bloco mais completo |
| `g.co/kgs/embaixadacarioca` | Não verificável como entidade oficial | Removido do `sameAs` |
| TripAdvisor | O perfil usado no schema não foi confirmado como o restaurante do Morro da Urca | Removido do `sameAs` das páginas públicas |
| `/restaurante-urca.html` órfã | Confirmado: publicado em 200 com canonical para outra URL | Redirect 301 adicionado para `/restaurante-morro-da-urca.html` |
| Selo EN da feijoada | Já estava correto: Academia da Cachaça + Veja Rio 2025/2026 | Não alterar |
| Ano do prêmio | O diagnóstico usa 2025 em trechos | Preservado o fato informado pelo responsável: Veja Rio **2025/2026** e Prazeres da Mesa **2017** |
| Seguidores | Arquivos `llms.txt` ainda diziam 100K | Corrigido para 84 mil/84K |
| Avaliações | Arquivos de IA ainda citavam Google e TripAdvisor sem base | Corrigido para Google: 4,8 estrelas e 8.847 avaliações |
| Eventos de Maps e Reviews | Já existem em `assets/conversion-tracking.js` | Não duplicar eventos |
| Sitemap com 144 URLs | Não confirmado: há **97 entradas canônicas `<url>`** | Contar entradas canônicas, não alternates hreflang |
| `lastmod` desatualizado | Confirmado nas páginas prioritárias | Atualizado para home, Café da Manhã, Como Chegar e Eventos |

## Correções implementadas nesta rodada

- `sameAs` limpo de referências não verificadas.
- Entidade `WebPage` única na home.
- Redirect permanente de `/restaurante-urca.html` para a URL canônica.
- `lastmod` atualizado nas páginas prioritárias alteradas.
- Arquivos `llms.txt` em PT/EN/ES atualizados com 84 mil seguidores, 8.847 avaliações e horários consistentes.
- Acesso por Bondinho ou trilha explicado corretamente em EN/ES.
- Relação formal com Academia da Cachaça e Cantina do MAM preservada.

## Validações concluídas

- Schema rating guard: **PASS**, 110 arquivos, 0 ocorrências.
- JSON-LD duplicate key guard: **PASS**, 110 arquivos, 0 ocorrências.
- GSC structured data pós-fix: **PASS**.
- Hreflang PT/EN/ES: **PASS**, nota mínima 100.
- Links internos e snippets: **PASS**, 16/16 páginas e 0 links quebrados.
- Cardápio PT/EN/ES: **PASS**, 12 seções e 149 itens por idioma.
- Home: **1 Restaurant** e **1 WebPage**.

## Próximas ações por impacto

### P0 — configuração externa

1. **Concluído:** HSTS ativado no Cloudflare com `max-age=86400`; validar estabilidade antes de ampliar.
2. **Concluído:** sitemap reenviado em 27/08/2026 e processado com 97 páginas; agora monitorar recrawl e URLs consolidadas.

### P1 — dados e conversão

1. Filtrar tráfego automatizado no GA4 antes de redefinir metas.
2. Unificar agrupamento de ChatGPT/IA e padronizar UTMs de GBP, Instagram, QR da mesa e QR da conta.
3. Integrar reserva concluída da Tagme ou criar uma forma confiável de reconciliação com o GA4.
4. Decidir um envio próprio para o formulário de eventos; hoje o fluxo termina no WhatsApp.

### P2 — conteúdo dependente do negócio

1. Publicar capacidade correta por formato de evento, faixa de investimento, casos e PDF comercial — somente após receber dados aprovados.
2. Publicar calendário real do Entardecer e adicionar `Event` apenas para datas confirmadas.
3. Trabalhar CTR do cluster Bondinho com títulos e respostas alinhados a informações oficiais; não inventar preços ou horários do parque.
4. Escalar canais já eficientes: blog do Bondinho, Instagram, assistentes de IA e programa de avaliações.

## Itens deliberadamente não implementados

- Novas páginas sem antes consolidar indexação e conversão.
- `Review`, `Rating` ou `AggregateRating` no JSON-LD.
- Preços, capacidades, line-up ou datas não fornecidos pelo negócio.
- Novos patches visuais genéricos sem falha reproduzida.
