# CSS/JS Refactor Opportunity Audit

Status geral: **PASS**

## Objetivo
Mapear oportunidades reais de refactor de CSS/JS sem mexer no visual antes de uma validação controlada no navegador.

## Resumo executivo
- Arquivos HTML analisados: **87**
- Blocos `<style>` inline: **1552**
- Blocos `<script>` inline, incluindo JSON-LD: **1469**
- Peso estimado de CSS inline: **9.059.477 bytes**
- Peso estimado de scripts inline: **1.373.970 bytes**
- Blocos CSS exatos repetidos em 2+ páginas: **20**
- Blocos JS exatos repetidos em 2+ páginas: **20**

## Páginas com maior oportunidade técnica

| Página | Styles inline | Scripts inline | JSON-LD | CSS externo | Imagens | CSS bytes | JS bytes | Prioridade |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `index.html` | 34 | 26 | 8 | 4 | 40 | 163464 | 26928 | alta |
| `es/index.html` | 27 | 30 | 7 | 3 | 34 | 142092 | 25714 | alta |
| `en/index.html` | 27 | 30 | 7 | 3 | 34 | 142173 | 25582 | alta |
| `es/eventos.html` | 23 | 30 | 11 | 3 | 10 | 152098 | 27132 | alta |
| `es/atardecer.html` | 25 | 27 | 8 | 3 | 12 | 152970 | 24249 | alta |
| `en/sunset.html` | 25 | 27 | 8 | 3 | 12 | 153039 | 24163 | alta |
| `es/cafe-da-manha.html` | 25 | 26 | 7 | 3 | 19 | 162921 | 24563 | alta |
| `en/almoco.html` | 25 | 26 | 7 | 3 | 16 | 153238 | 24656 | alta |
| `cafe-da-manha.html` | 28 | 22 | 8 | 4 | 19 | 171689 | 25880 | alta |
| `en/cafe-da-manha.html` | 24 | 26 | 7 | 3 | 19 | 162283 | 24629 | alta |
| `en/eventos.html` | 23 | 27 | 8 | 3 | 10 | 152170 | 24732 | alta |
| `en/entardecer.html` | 24 | 26 | 7 | 3 | 12 | 151670 | 22992 | alta |

## Blocos CSS repetidos — candidatos a extração

| Hash | Páginas | Bytes | Marker provável | Risco | Pode extrair? | Motivo |
|---|---:|---:|---|---|---|---|
| `6c2812d18885` | 85 | 3159 | `ec-lang-dropdown-closed-state-fix` | high | no/partial | visual/readability/page-critical pattern: lock |
| `d9cebd34b57b` | 85 | 2517 | `ec-sprint4-r2d2-aio-conversion-css` | high | no/partial | visual/readability/page-critical pattern: lock |
| `f0b8729a5f03` | 85 | 199 | `ec-orange-eyebrow-position-fix` | high | no/partial | visual/readability/page-critical pattern: page-hero |
| `d44459714a03` | 83 | 4896 | `ec-legibility-contrast-lock` | high | no/partial | visual/readability/page-critical pattern: lock |
| `d5f1cb590c72` | 82 | 9842 | `ec-hero-pao-de-acucar-visual-lock` | high | no/partial | visual/readability/page-critical pattern: lock |
| `84516ec4ddad` | 82 | 8479 | `ec-lunch-photos-global-readability-hardfix` | high | no/partial | visual/readability/page-critical pattern: readability |
| `d22da0263173` | 82 | 7910 | `ec-aaa-readability-emergency-fix` | high | no/partial | visual/readability/page-critical pattern: readability |
| `c42dd71fa0ab` | 82 | 7695 | `ec-brand-manual-alignment` | high | no/partial | visual/readability/page-critical pattern: contrast |
| `f0329c8d85f8` | 82 | 6315 | `ec-home-top-exact-replication-lock` | high | no/partial | visual/readability/page-critical pattern: lock |
| `40bbf2c2c8bf` | 82 | 4776 | `ec-visual-readability-reality-fix` | high | no/partial | visual/readability/page-critical pattern: readability |
| `a0bd1cdda693` | 61 | 5733 | `ec-final-design-consistency-lock` | high | no/partial | visual/readability/page-critical pattern: lock |
| `63e2694eac1d` | 53 | 1197 | `ec-sprint5-quality-consolidation-css` | high | no/partial | visual/readability/page-critical pattern: lock |
| `a4d44586ec93` | 34 | 2800 | `══════════════════════════════════════════` | high | no/partial | visual/readability/page-critical pattern: lock |
| `7acd773d247d` | 31 | 2107 | `bnav-color-fix` | low | yes | recurring utility pattern: nav-rating-badge |
| `c56f571ca40d` | 29 | 5751 | `ec-nav-ux-fixes` | low | yes | recurring utility pattern: lang-switcher |
| `d3ac5e30f85c` | 29 | 1573 | `ec-featured-snippet-ordered-lists-css` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `d9a5ee4aa469` | 28 | 5756 | `ec-nav-ux-fixes` | low | yes | recurring utility pattern: lang-switcher |
| `e47d4916028e` | 28 | 5751 | `ec-nav-ux-fixes` | low | yes | recurring utility pattern: lang-switcher |
| `5dfe83a60153` | 25 | 3043 | `══════════════════════════════════════════` | high | no/partial | visual/readability/page-critical pattern: lock |
| `f2b7de8f1772` | 24 | 1296 | `ec-aaa-closeout-design-lock` | medium | partial | global/layout styles or scripts require visual QA before extraction |

## Blocos JS repetidos — candidatos a extração

| Hash | Páginas | Bytes | Marker provável | Risco | Pode extrair? | Motivo |
|---|---:|---:|---|---|---|---|
| `fd2421dec915` | 85 | 1351 | `ec-lang-dropdown-closed-state-js` | low | yes | recurring utility pattern: lang-switcher |
| `eee95d5e7c2b` | 85 | 311 | `script:eee95d5e7c2b` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `fa3046ebf668` | 82 | 1424 | `ec-visual-readability-reality-js` | high | no/partial | visual/readability/page-critical pattern: menu-item |
| `052d6108a742` | 78 | 187 | `ec-service-worker-register` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `6acf022a56c0` | 77 | 962 | `ec-ga4-base` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `e3b0c44298fc` | 69 | 0 | `script:e3b0c44298fc` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `ae90e8a20548` | 34 | 1285 | `mobile-bottom-nav` | low | yes | recurring utility pattern: mobile-bottom-nav |
| `28bac1b40402` | 28 | 1558 | `nav-drawer` | low | yes | recurring utility pattern: nav-drawer |
| `7602ccd99b72` | 28 | 535 | `─── LANG SWITCHER JS ───` | low | yes | recurring utility pattern: lang-switcher |
| `604c18ae8b34` | 26 | 3282 | `ec-ga4-events` | high | no/partial | visual/readability/page-critical pattern: cardapio |
| `15eb4bae0185` | 26 | 3277 | `ec-ga4-events` | high | no/partial | visual/readability/page-critical pattern: cardapio |
| `c37b17dcbd63` | 25 | 3277 | `ec-ga4-events` | high | no/partial | visual/readability/page-critical pattern: cardapio |
| `72d9e89cd224` | 19 | 910 | `script:72d9e89cd224` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `06b79f2d2e4d` | 19 | 305 | `script:06b79f2d2e4d` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `086277eca290` | 19 | 276 | `script:086277eca290` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `ab6b29f288d0` | 6 | 413 | `script:ab6b29f288d0` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `a54b76654e04` | 3 | 990 | `nav-drawer` | low | yes | recurring utility pattern: nav-drawer |
| `1c552a3e2b95` | 3 | 674 | `script:1c552a3e2b95` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `074d72413665` | 3 | 623 | `script:074d72413665` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `e792dfd95856` | 3 | 487 | `script:e792dfd95856` | medium | partial | global/layout styles or scripts require visual QA before extraction |

## Padrões recorrentes por marcador

| Marcador | Ocorrências | Leitura |
|---|---:|---|
| `js:script:e3b0c44298fc` | 377 | avaliar no refactor |
| `css:══════════════════════════════════════════` | 154 | avaliar no refactor |
| `css:ec-nav-ux-fixes` | 85 | avaliar no refactor |
| `css:ec-orange-eyebrow-position-fix` | 85 | avaliar no refactor |
| `css:ec-sprint4-r2d2-aio-conversion-css` | 85 | avaliar no refactor |
| `css:ec-lang-dropdown-closed-state-fix` | 85 | candidato a asset global |
| `js:ec-lang-dropdown-closed-state-js` | 85 | candidato a asset global |
| `js:script:eee95d5e7c2b` | 85 | avaliar no refactor |
| `css:ec-legibility-contrast-lock` | 83 | avaliar no refactor |
| `css:ec-home-top-exact-replication-lock` | 82 | avaliar no refactor |
| `css:ec-hero-pao-de-acucar-visual-lock` | 82 | avaliar no refactor |
| `css:ec-brand-manual-alignment` | 82 | avaliar no refactor |
| `css:ec-aaa-readability-emergency-fix` | 82 | avaliar no refactor |
| `css:ec-lunch-photos-global-readability-hardfix` | 82 | avaliar no refactor |
| `css:ec-visual-readability-reality-fix` | 82 | avaliar no refactor |
| `js:ec-visual-readability-reality-js` | 82 | avaliar no refactor |
| `js:ec-service-worker-register` | 78 | avaliar no refactor |
| `js:ec-ga4-base` | 77 | avaliar no refactor |
| `js:ec-ga4-events` | 77 | avaliar no refactor |
| `css:ec-final-design-consistency-lock` | 61 | avaliar no refactor |

## Plano de refactor recomendado

### Lote 1 — baixo risco
Extrair para assets globais os padrões de idioma, WhatsApp, navegação mobile, bottom nav, badge de Google Reviews e foco acessível. Esses blocos tendem a ser utilitários e repetíveis.

### Lote 2 — risco médio
Consolidar nav desktop, botões, grids, espaçamentos de seção e cards comuns. Exige teste visual em home, cardápio, almoço, café, eventos e guia.

### Lote 3 — alto risco
Só depois de QA visual: readability locks, contrast locks, hero/page-hero, cardápio e overrides de menu. Esses blocos foram criados para corrigir problemas visuais reais e não devem ser removidos em massa.

## Entrega operacional sugerida
1. Criar `assets/css/ec-components-global.css` para idioma, WhatsApp, nav drawer, bottom nav e badges.
2. Criar `assets/js/ec-ui-global.js` para interações repetidas de menu/idioma/WhatsApp.
3. Incluir os assets globais nas páginas prioritárias.
4. Remover apenas os blocos inline já cobertos, página por página.
5. Rodar auditoria final e validação visual real antes do deploy definitivo.
