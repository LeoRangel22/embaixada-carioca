# Implementação do briefing GA4/GSC — 2026-08-15

Status geral: **PASS**

## Escopo concluído

- Titles, canonicals e meta descriptions auditados nas 104 páginas HTML ativas de PT/EN/ES.
- Home, cardápio e página Morro da Urca com titles de 58, 59 e 58 caracteres.
- Nenhuma página ativa com title, canonical ou meta description ausente ou duplicada.
- Schema `Restaurant` preservado nas páginas comerciais prioritárias.
- Nenhum `Review`, `Rating`, `AggregateRating`, `aggregateRating`, `ratingValue`, `ratingCount` ou `reviewCount` indevido no JSON-LD.
- Páginas de avaliações PT/EN/ES mantidas indexáveis, com CTA direto para avaliação no Google e NAP visível.
- Endereço e telefone padronizados nas páginas comerciais: Av. Pasteur, 520 - Urca, Rio de Janeiro - RJ, 22290-240; +55 21 96683-7556.
- `morro-da-urca.html` aprofundada com imagens reais, textos alternativos, contexto de acesso e links internos.
- Navegação e trechos públicos das páginas inglesas prioritárias reescritos em inglês natural.
- Menções ao prêmio padronizadas por idioma.
- Alegações não verificadas sobre Cantina do MAM/grupo removidas ou ausentes.
- Contadores e links de seguidores padronizados em 84K / 84 mil.
- Cardápio completo restaurado com 12 seções e 149 itens em cada idioma, com paridade PT/EN/ES.

## Formulação oficial do prêmio

- PT: `Melhor Feijoada do Rio de Janeiro — Veja Rio Comer & Beber 2025/2026`
- EN: `Best Feijoada in Rio de Janeiro — Veja Rio Comer & Beber 2025/2026`
- ES: `Mejor Feijoada de Río de Janeiro — Veja Rio Comer & Beber 2025/2026`

## Decisão de conformidade sobre avaliações

O briefing sugeria `aggregateRating`. A marcação não foi adicionada porque avaliações controladas pela própria entidade em páginas de `LocalBusiness`/`Organization` são consideradas autoatribuídas e não qualificam para o recurso de estrelas do Google. A prova social continua visível e os CTAs levam diretamente ao Google, sem marcar avaliações no JSON-LD.

## Validações executadas

| Verificação | Resultado |
|---|---:|
| GSC post-fix structured data | PASS |
| Schema rating guard | PASS — 0 ocorrências |
| JSON-LD duplicate key guard | PASS — 0 ocorrências |
| Hreflang PT/EN/ES | PASS — score mínimo 100 |
| Title/canonical/meta description únicos | PASS — 0 problemas em 104 páginas |
| Termos críticos de portunhol nas páginas EN | PASS — 0 ocorrências monitoradas |
| Paridade do cardápio PT/EN/ES | PASS — 12 seções e 149 itens por idioma |
| NAP nas páginas comerciais | PASS — 0 páginas comerciais pendentes |
| Integridade do diff | PASS |

## Verificação desktop

- Viewport conferido em 1440 × 900.
- Hero ocupa a primeira dobra sem overflow horizontal.
- CTA principal visível antes da rolagem.
- Imagem principal com carregamento prioritário.
- A leitura externa de métricas exatas de Core Web Vitals pelo PageSpeed Insights não pôde ser concluída nesta rodada porque a API pública retornou limite de cota (`429`). Não foi registrada estimativa artificial.

## Relatórios relacionados

- `_audit_reports/cardapio_completeness_i18n_fix_report.md`
- `_audit_reports/claude_audit_critical_fixes_report.md`
- `_audit_reports/gsc_postfix_structured_data_validation.md`
- `_audit_reports/schema_rating_guard_report.md`
- `_audit_reports/schema_jsonld_duplicate_key_report.md`
