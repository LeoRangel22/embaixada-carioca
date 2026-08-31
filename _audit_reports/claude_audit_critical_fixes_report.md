# Claude Audit Critical Fixes

Status geral: **PASS**

## Atualização operacional — 31/08/2026

- Este relatório preserva o snapshot da execução original, mas as formulações factuais abaixo foram atualizadas para a realidade confirmada.
- Google: 4,8 estrelas e 8.847 avaliações.
- Instagram: 84 mil seguidores.
- Schema guards atuais: PASS em 110 arquivos, sem `Review`, `Rating`, `AggregateRating` ou chaves JSON-LD duplicadas.
- Governança atual: 7 workflows ativos e 30 legados desativados. O inventário de 32 arquivos YAML abaixo é histórico e não representa workflows ativos.
- Embaixada Carioca e Cantina do MAM têm os mesmos sócios, conforme confirmação do responsável.
- A relação com a Academia da Cachaça deve ser descrita como parceria formal com vínculo societário familiar, sem afirmar composição societária idêntica.

## Objetivo
Atuar sobre os pontos críticos do relatório Claude: atribuição oficial do prêmio da feijoada à Academia da Cachaça, preservação da parceria institucional confirmada, limpeza de portunhol técnico, padronização de seguidores e blindagem contra retorno de review/rating em JSON-LD.

## Formulações canônicas aplicadas
- PT: `Feijoada da Academia da Cachaça — Melhor Feijoada do Brasil, Prazeres da Mesa 2017, e Melhor Feijoada do Rio, Veja Rio Comer & Beber 2025/2026 — servida na Embaixada Carioca por meio de parceria formal`
- EN: `Academia da Cachaça's feijoada — Best Feijoada in Brazil, Prazeres da Mesa 2017, and Best Feijoada in Rio, Veja Rio Comer & Beber 2025/2026 — served at Embaixada Carioca through a formal partnership`
- ES: `Feijoada de Academia da Cachaça — Mejor Feijoada de Brasil, Prazeres da Mesa 2017, y Mejor Feijoada de Río, Veja Rio Comer & Beber 2025/2026 — servida en Embaixada Carioca mediante una colaboración formal`

## Guardrails
- Nenhum canonical/hreflang foi alterado.
- Nenhum AggregateRating, Rating ou Review foi adicionado.
- JSON-LD com `review`, `reviewRating` ou `aggregateRating` foi limpo quando encontrado.
- A composição societária comum confirmada entre Embaixada Carioca e Cantina do MAM não é removida nem distorcida por este script.
- A Academia da Cachaça é tratada separadamente como parceira formal com vínculo societário familiar, sem afirmar composição societária idêntica.

## Resumo

Os números abaixo pertencem à execução que gerou este relatório e não ao inventário operacional atual.
- HTML analisados: **116**
- Arquivos alterados: **2**
- Substituições textuais: **8**
- Nós/campos JSON-LD de rating/review removidos: **0**
- Workflows encontrados: **32**

## Inventário de workflows

- `.github/workflows/accessibility-ci.yml`
- `.github/workflows/apply-aaa-fixes.yml`
- `.github/workflows/final-86page-aaa-master-audit.yml`
- `.github/workflows/final-design-consistency-lock.yml`
- `.github/workflows/final-growth-items.yml`
- `.github/workflows/green-solid-palette-audit.yml`
- `.github/workflows/gsc-structured-data-issues-fix.yml`
- `.github/workflows/home-reference-top-nav-lock.yml`
- `.github/workflows/hreflang-validation.yml`
- `.github/workflows/i18n-sync-validation.yml`
- `.github/workflows/legibility-contrast-lock.yml`
- `.github/workflows/lunch-photos-global-readability-hardfix.yml`
- `.github/workflows/multilingual-continuous-optimization.yml`
- `.github/workflows/p0-hreflang-pt-en-es.yml`
- `.github/workflows/p0-schema-jsonld.yml`
- `.github/workflows/p1-aio-schema-meta.yml`
- `.github/workflows/phase2-performance-seo-audit.yml`
- `.github/workflows/repo-hygiene.yml`
- `.github/workflows/review-snippets-issue-fix.yml`
- `.github/workflows/schema-ci-gate.yml`
- `.github/workflows/schema-jsonld-duplicate-key-guard.yml`
- `.github/workflows/schema-rating-guard.yml`
- `.github/workflows/stabilize-existing-pages.yml`
- `.github/workflows/static-product-schema-faq.yml`
- `.github/workflows/super-site-standards-seo-audit.yml`
- `.github/workflows/super-workflow-score-gate.yml`
- `.github/workflows/top-nav-standardization.yml`
- `.github/workflows/top-nav-visual-refinement.yml`
- `.github/workflows/update-version.yml`
- `.github/workflows/verify-live-site.yml`
- `.github/workflows/visual-contrast-risk-audit.yml`
- `.github/workflows/visual-readability-reality-fix.yml`

## Pendências encontradas

Nenhuma ocorrência dos termos críticos monitorados.

## Arquivos alterados

| Arquivo | Changed | Substituições | JSON-LD rating/review removidos | Notas |
|---|---:|---:|---:|---|
| `feijoada-morro-da-urca.html` | True | 6 | 0 | award-pt-source-corrected:3; award-year-official-2025:3 |
| `index.html` | True | 2 | 0 | award-pt-source-corrected:1; award-year-official-2025:1 |
