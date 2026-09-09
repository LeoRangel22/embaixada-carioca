# Refinamento visual da home — 8 de setembro de 2026

## Escopo

Pequeno ajuste visual nas homes PT, EN e ES. Sem alteração de textos, fotos, links, horários, prêmios, metadados de SEO ou JSON-LD. Páginas internas não foram redesenhadas.

## Ajustes

- Título ligeiramente menor, com entrelinha e distribuição de linhas mais equilibradas.
- Texto de apoio mais contido e com entrelinha confortável.
- Selos informativos com menos peso visual.
- Quadro de prêmios mais compacto, borda discreta e texto menos pesado.
- Botões com espaçamento tipográfico consistente; até 600 px, largura uniforme e altura mínima de 48 px.
- Versão do CSS atualizada nas três homes para evitar reutilização da versão anterior em cache.

## Verificação

- Teste de conteúdo e destinos da home: PASS.
- Guardas de JSON-LD e rating: PASS, 111 arquivos, zero pendências.
- A verificação de layout usa navegador Chromium, sem service worker, em PT/EN/ES e larguras de 320, 390, 768, 1024 e 1440 px. Inclui sobreposição de componentes, overflow horizontal, abertura/fechamento do menu e visibilidade do seletor de idioma.
- Resultado: 15 combinações aprovadas, sem sobreposições entre os componentes testados, sem overflow horizontal e sem erros JavaScript. Menu mobile e seletor de idioma funcionais nas nove combinações até 960 px. Capturas desktop e mobile conferidas visualmente.
- Este refinamento não equivale a uma certificação WCAG AAA.
