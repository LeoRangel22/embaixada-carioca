# Claude Audit Critical Fixes

Status geral: **PASS**

## Objetivo
Atuar sobre os pontos críticos do relatório Claude: padronização do prêmio da feijoada, remoção de alegações institucionais não verificadas, limpeza de portunhol técnico, padronização de seguidores e blindagem contra retorno de review/rating em JSON-LD.

## Formulações canônicas aplicadas
- PT: `Melhor Feijoada do Rio de Janeiro — Veja Rio Comer & Beber 2025/2026`
- EN: `Best Feijoada in Rio de Janeiro — Veja Rio Comer & Beber 2025/2026`
- ES: `Mejor Feijoada de Río de Janeiro — Veja Rio Comer & Beber 2025/2026`

## Guardrails
- Nenhum canonical/hreflang foi alterado.
- Nenhum AggregateRating, Rating ou Review foi adicionado.
- JSON-LD com `review`, `reviewRating` ou `aggregateRating` foi limpo quando encontrado.
- Alegações envolvendo Cantina do MAM foram neutralizadas se presentes no HTML.

## Resumo
- HTML analisados: **116**
- Arquivos alterados: **3**
- Substituições textuais: **3**
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
| `es/feijoada.html` | True | 1 | 0 | award-es-not-prepared-at-academia:1 |
| `es/morro-da-urca.html` | True | 1 | 0 | language-block-rewritten:1 |
| `es/sunset-por-do-sol-rio-de-janeiro.html` | True | 1 | 0 | award-es-not-prepared-at-academia:1 |
