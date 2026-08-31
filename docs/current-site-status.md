# Estado atual do site — Embaixada Carioca

**Atualizado em:** 31/08/2026

**Domínio canônico:** `https://www.embaixadacarioca.com/`

**Repositório:** `LeoRangel22/embaixada-carioca`

**Branch de produção:** `master`

Este é o documento de referência para o estado operacional atual. Relatórios datados em `_audit_reports/` registram o momento em que foram gerados e podem conter limitações já superadas.

## Arquitetura publicada

| Camada | Estado atual |
|---|---|
| Hospedagem pública principal | Cloudflare Pages |
| Projeto Pages | `embaixada-carioca.pages.dev` |
| Plano Cloudflare | Free — suficiente para o uso atual |
| DNS de `www` | CNAME para o projeto Cloudflare Pages |
| Fonte de produção | GitHub, branch `master` |
| GitHub Pages | publicação secundária mantida; não é o destino canônico do DNS |

## Rede, redirecionamentos e segurança

Verificado ao vivo em 31/08/2026:

- `http://www.embaixadacarioca.com/...` responde `301` para HTTPS.
- `https://embaixadacarioca.com/` consolida em `https://www.embaixadacarioca.com/`.
- `.com.br`, com e sem `www`, responde `301` para o domínio `.com` canônico.
- `/index.html` responde `301` para `/`.
- aliases como `/cardapio` e `/eventos` respondem `301` para suas URLs `.html`.
- HSTS está ativo em fase gradual: `max-age=86400`.
- CSP, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` e `Permissions-Policy` são entregues pelo Cloudflare.

O HSTS ainda não deve ser descrito como implantação definitiva com subdomínios/preload. A ampliação depende de monitoramento sem regressões.

## Indexação

- `sitemap.xml`: 97 URLs canônicas.
- Sitemap reenviado ao Search Console em 27/08/2026 e processado com 97 páginas.
- URLs alternativas e aliases não devem ser solicitados para indexação; o destino é sempre a canonical.
- O próximo passo é acompanhar recrawl, indexação e CTR, não reenviar repetidamente sem mudança material.

## Idiomas e conteúdo

- Português, inglês e espanhol publicados.
- Hreflang PT/EN/ES/x-default: PASS, nota mínima 100.
- Todas as páginas PT do escopo i18n possuem contrapartes EN e ES.
- Permanecem 12 diferenças editoriais advisory de títulos/seções que exigem revisão humana, sem impedir a validação estrutural.
- Cardápio: 12 seções e 149 itens por idioma na última auditoria de paridade.

## Entidade e fatos oficiais

- Diferencial: único restaurante dentro do Parque Bondinho com vista direta para o Pão de Açúcar.
- Avaliação Google: 4,8 estrelas e 8.847 avaliações.
- Instagram: 84 mil seguidores.
- Melhor Feijoada do Brasil: Academia da Cachaça, Prazeres da Mesa, 2017.
- Melhor Feijoada do Rio: Veja Rio Comer & Beber, 2025/2026.
- A feijoada da Academia da Cachaça é servida na Embaixada Carioca por parceria formal.
- Embaixada Carioca e Cantina do MAM têm os mesmos sócios, conforme confirmação do responsável.

## JSON-LD

- Guard de rating/review: PASS em 110 arquivos, 0 ocorrências proibidas.
- Guard de chaves duplicadas: PASS em 110 arquivos, 0 chaves duplicadas.
- Não usar `Review`, `Rating`, `AggregateRating` ou campos derivados no JSON-LD.
- Prova social pode existir visualmente, sem marcação estruturada de avaliações.

## Analytics e conversão

- Instrumentação de funil implantada em 24/08/2026.
- `ec_event_lead_outbound` marcado como evento principal no GA4 em 27/08/2026.
- Cliques de navegação e microinterações devem continuar como eventos diagnósticos, não como conversões principais.
- Reserva concluída na Tagme ainda precisa de integração ou reconciliação confiável com o GA4.
- Formulário de eventos deve ser medido por etapas antes de uma troca de canal ou reconstrução.

## SEO em medição

O lote de CTR de 27/08/2026 atualizou:

- `almoco.html` para consultas de “almoço no Pão de Açúcar”;
- `en/where-to-eat-near-sugarloaf.html`;
- `es/donde-comer-cerca-del-pan-de-azucar.html`.

Os títulos do cluster restaurante/Bondinho também foram estabilizados. Não reescrever antes de:

- leitura direcional em 10/09/2026 (14 dias);
- decisão com janela consolidada em 24/09/2026 (28 dias).

## Governança de automações

Ativos: 7 workflows.

1. Pages build and deployment.
2. Verify live site.
3. Super site standards SEO audit.
4. Schema JSON-LD CI gate.
5. Accessibility CI.
6. Hreflang Validation.
7. i18n Sync Validation.

Desativados: 30 workflows legados de correção automática ou execução manual perigosa. Não reativar em lote.

## Próximas ações de alto impacto

1. Monitorar o HSTS curto e ampliar gradualmente somente após validar todos os hosts HTTPS.
2. Medir o lote de CTR nas datas previstas, usando página + consulta + país/idioma.
3. Fechar a medição de reservas concluídas da Tagme.
4. Medir o funil de eventos antes de decidir novo formulário ou novo canal de envio.
5. Publicar capacidades, faixas de investimento e calendário apenas com dados comerciais aprovados.
6. Continuar a revisão editorial nativa das 12 diferenças PT/EN/ES.
7. Monitorar respostas 5xx/erros transitórios no Cloudflare.
