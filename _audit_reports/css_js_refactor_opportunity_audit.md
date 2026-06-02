# CSS/JS Refactor Opportunity Audit

Status geral: **PASS**

## Objetivo
Mapear oportunidades reais de refactor de CSS/JS sem mexer no visual antes de uma validação controlada no navegador.

## Resumo executivo
- Arquivos HTML analisados: **449**
- Blocos `<style>` inline: **7967**
- Blocos `<script>` inline, incluindo JSON-LD: **8260**
- Peso estimado de CSS inline: **42.264.270 bytes**
- Peso estimado de scripts inline: **7.133.165 bytes**
- Blocos CSS exatos repetidos em 2+ páginas: **20**
- Blocos JS exatos repetidos em 2+ páginas: **20**

## Páginas com maior oportunidade técnica

| Página | Styles inline | Scripts inline | JSON-LD | CSS externo | Imagens | CSS bytes | JS bytes | Prioridade |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `.claude/worktrees/agent-a24c2695706e74023/index.html` | 35 | 31 | 8 | 4 | 40 | 173404 | 26928 | alta |
| `.claude/worktrees/agent-a3cd35fa352f86131/index.html` | 35 | 31 | 8 | 4 | 40 | 173404 | 26928 | alta |
| `.claude/worktrees/agent-a713247c54f24ade4/index.html` | 35 | 31 | 8 | 4 | 40 | 173404 | 26928 | alta |
| `.claude/worktrees/agent-ad572117775518339/index.html` | 35 | 31 | 8 | 4 | 40 | 173404 | 26928 | alta |
| `es/index.html` | 28 | 31 | 8 | 4 | 34 | 152032 | 30122 | alta |
| `en/index.html` | 28 | 31 | 8 | 4 | 34 | 152113 | 29940 | alta |
| `.claude/worktrees/agent-a24c2695706e74023/es/index.html` | 28 | 30 | 7 | 3 | 34 | 152032 | 25714 | alta |
| `.claude/worktrees/agent-a3cd35fa352f86131/es/index.html` | 28 | 30 | 7 | 3 | 34 | 152032 | 25714 | alta |
| `.claude/worktrees/agent-a713247c54f24ade4/es/index.html` | 28 | 30 | 7 | 3 | 34 | 152032 | 25714 | alta |
| `.claude/worktrees/agent-ad572117775518339/es/index.html` | 28 | 30 | 7 | 3 | 34 | 152032 | 25714 | alta |
| `.claude/worktrees/agent-a24c2695706e74023/en/index.html` | 28 | 30 | 7 | 3 | 34 | 152113 | 25582 | alta |
| `.claude/worktrees/agent-a3cd35fa352f86131/en/index.html` | 28 | 30 | 7 | 3 | 34 | 152113 | 25582 | alta |

## Blocos CSS repetidos — candidatos a extração

| Hash | Páginas | Bytes | Marker provável | Risco | Pode extrair? | Motivo |
|---|---:|---:|---|---|---|---|
| `6c2812d18885` | 422 | 3159 | `ec-lang-dropdown-closed-state-fix` | high | no/partial | visual/readability/page-critical pattern: lock |
| `d9cebd34b57b` | 422 | 2517 | `ec-sprint4-r2d2-aio-conversion-css` | high | no/partial | visual/readability/page-critical pattern: lock |
| `f0b8729a5f03` | 422 | 199 | `ec-orange-eyebrow-position-fix` | high | no/partial | visual/readability/page-critical pattern: page-hero |
| `646175092ddf` | 420 | 5101 | `ec-top-nav-viewport-fit-v3-css` | high | no/partial | visual/readability/page-critical pattern: lock |
| `5c95a1281240` | 419 | 11154 | `ec-home-reference-top-nav-lock-v2-css` | high | no/partial | visual/readability/page-critical pattern: lock |
| `d44459714a03` | 414 | 4896 | `ec-legibility-contrast-lock` | high | no/partial | visual/readability/page-critical pattern: lock |
| `d5f1cb590c72` | 409 | 9842 | `ec-hero-pao-de-acucar-visual-lock` | high | no/partial | visual/readability/page-critical pattern: lock |
| `84516ec4ddad` | 409 | 8479 | `ec-lunch-photos-global-readability-hardfix` | high | no/partial | visual/readability/page-critical pattern: readability |
| `d22da0263173` | 409 | 7910 | `ec-aaa-readability-emergency-fix` | high | no/partial | visual/readability/page-critical pattern: readability |
| `c42dd71fa0ab` | 409 | 7695 | `ec-brand-manual-alignment` | high | no/partial | visual/readability/page-critical pattern: contrast |
| `40bbf2c2c8bf` | 409 | 4776 | `ec-visual-readability-reality-fix` | high | no/partial | visual/readability/page-critical pattern: readability |
| `a0bd1cdda693` | 304 | 5733 | `ec-final-design-consistency-lock` | high | no/partial | visual/readability/page-critical pattern: lock |
| `63e2694eac1d` | 265 | 1197 | `ec-sprint5-quality-consolidation-css` | high | no/partial | visual/readability/page-critical pattern: lock |
| `a4d44586ec93` | 170 | 2800 | `══════════════════════════════════════════` | high | no/partial | visual/readability/page-critical pattern: lock |
| `7acd773d247d` | 155 | 2107 | `bnav-color-fix` | low | yes | recurring utility pattern: nav-rating-badge |
| `d3ac5e30f85c` | 144 | 1573 | `ec-featured-snippet-ordered-lists-css` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `c56f571ca40d` | 142 | 5751 | `ec-nav-ux-fixes` | low | yes | recurring utility pattern: lang-switcher |
| `d9a5ee4aa469` | 140 | 5756 | `ec-nav-ux-fixes` | low | yes | recurring utility pattern: lang-switcher |
| `e47d4916028e` | 140 | 5751 | `ec-nav-ux-fixes` | low | yes | recurring utility pattern: lang-switcher |
| `5dfe83a60153` | 125 | 3043 | `══════════════════════════════════════════` | high | no/partial | visual/readability/page-critical pattern: lock |

## Blocos JS repetidos — candidatos a extração

| Hash | Páginas | Bytes | Marker provável | Risco | Pode extrair? | Motivo |
|---|---:|---:|---|---|---|---|
| `e3b0c44298fc` | 449 | 0 | `script:e3b0c44298fc` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `fd2421dec915` | 423 | 1351 | `ec-lang-dropdown-closed-state-js` | low | yes | recurring utility pattern: lang-switcher |
| `eee95d5e7c2b` | 423 | 311 | `script:eee95d5e7c2b` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `fa3046ebf668` | 410 | 1424 | `ec-visual-readability-reality-js` | high | no/partial | visual/readability/page-critical pattern: menu-item |
| `052d6108a742` | 390 | 187 | `ec-service-worker-register` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `6acf022a56c0` | 386 | 962 | `ec-ga4-base` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `ae90e8a20548` | 170 | 1285 | `mobile-bottom-nav` | low | yes | recurring utility pattern: mobile-bottom-nav |
| `28bac1b40402` | 140 | 1558 | `nav-drawer` | low | yes | recurring utility pattern: nav-drawer |
| `7602ccd99b72` | 140 | 535 | `─── LANG SWITCHER JS ───` | low | yes | recurring utility pattern: lang-switcher |
| `604c18ae8b34` | 130 | 3282 | `ec-ga4-events` | high | no/partial | visual/readability/page-critical pattern: cardapio |
| `15eb4bae0185` | 130 | 3277 | `ec-ga4-events` | high | no/partial | visual/readability/page-critical pattern: cardapio |
| `c37b17dcbd63` | 125 | 3277 | `ec-ga4-events` | high | no/partial | visual/readability/page-critical pattern: cardapio |
| `72d9e89cd224` | 95 | 910 | `script:72d9e89cd224` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `06b79f2d2e4d` | 95 | 305 | `script:06b79f2d2e4d` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `086277eca290` | 95 | 276 | `script:086277eca290` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `ab6b29f288d0` | 30 | 413 | `script:ab6b29f288d0` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `e792dfd95856` | 16 | 487 | `script:e792dfd95856` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `c1c5546a5487` | 16 | 367 | `lang-switcher` | low | yes | recurring utility pattern: lang-switcher |
| `12d850e013a7` | 16 | 218 | `script:12d850e013a7` | medium | partial | global/layout styles or scripts require visual QA before extraction |
| `a54b76654e04` | 15 | 990 | `nav-drawer` | low | yes | recurring utility pattern: nav-drawer |

## Padrões recorrentes por marcador

| Marcador | Ocorrências | Leitura |
|---|---:|---|
| `js:script:e3b0c44298fc` | 2716 | avaliar no refactor |
| `css:══════════════════════════════════════════` | 770 | avaliar no refactor |
| `js:ec-lang-dropdown-closed-state-js` | 423 | candidato a asset global |
| `js:script:eee95d5e7c2b` | 423 | avaliar no refactor |
| `css:ec-nav-ux-fixes` | 422 | avaliar no refactor |
| `css:ec-orange-eyebrow-position-fix` | 422 | avaliar no refactor |
| `css:ec-sprint4-r2d2-aio-conversion-css` | 422 | avaliar no refactor |
| `css:ec-lang-dropdown-closed-state-fix` | 422 | candidato a asset global |
| `css:ec-top-nav-viewport-fit-v3-css` | 420 | avaliar no refactor |
| `css:ec-home-reference-top-nav-lock-v2-css` | 419 | avaliar no refactor |
| `css:ec-legibility-contrast-lock` | 414 | avaliar no refactor |
| `js:ec-visual-readability-reality-js` | 410 | avaliar no refactor |
| `css:ec-hero-pao-de-acucar-visual-lock` | 409 | avaliar no refactor |
| `css:ec-brand-manual-alignment` | 409 | avaliar no refactor |
| `css:ec-aaa-readability-emergency-fix` | 409 | avaliar no refactor |
| `css:ec-lunch-photos-global-readability-hardfix` | 409 | avaliar no refactor |
| `css:ec-visual-readability-reality-fix` | 409 | avaliar no refactor |
| `js:ec-service-worker-register` | 390 | avaliar no refactor |
| `js:ec-ga4-base` | 386 | avaliar no refactor |
| `js:ec-ga4-events` | 385 | avaliar no refactor |

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
