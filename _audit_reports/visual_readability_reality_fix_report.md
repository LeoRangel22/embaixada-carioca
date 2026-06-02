# Visual Readability Reality Fix

## Objetivo
Corrigir problemas visuais reais de contraste, especialmente o cardápio com títulos de pratos claros sobre fundo areia.

## Decisão visual
- Nome dos pratos no cardápio: verde escuro oficial `#335d4a`.
- Descrição dos pratos e cards claros: cinza escuro `#485156`.
- Preços: dourado escuro `#9a6500`.
- Fundo escuro: texto areia claro com opacidade alta.

## Veredito
- Páginas auditadas: 91
- PASS: 85
- WARN: 6
- Status geral: WARN

## Contadores
- html_scanned: 91
- html_updated: 85
- css_js_injected: 85
- invalid_rgba_fixed: 0
- audit_pass: 85
- audit_warn: 6

## Páginas com WARN
- src/partials/en/footer.html: reality_fix_present, menu_titles_dark_green_rule, menu_js_guard_present, light_card_dark_text_rule
- src/partials/en/nav.html: reality_fix_present, menu_titles_dark_green_rule, menu_js_guard_present, light_card_dark_text_rule
- src/partials/es/footer.html: reality_fix_present, menu_titles_dark_green_rule, menu_js_guard_present, light_card_dark_text_rule
- src/partials/es/nav.html: reality_fix_present, menu_titles_dark_green_rule, menu_js_guard_present, light_card_dark_text_rule
- src/partials/pt/footer.html: reality_fix_present, menu_titles_dark_green_rule, menu_js_guard_present, light_card_dark_text_rule
- src/partials/pt/nav.html: reality_fix_present, menu_titles_dark_green_rule, menu_js_guard_present, light_card_dark_text_rule
