# Accessibility WCAG AA Baseline

## Objetivo

Substituir o antigo workflow que mascarava a falha do Pa11y por uma medição reproduzível, com relatório JSON e limite regressivo.

## Estado inicial

- Páginas críticas testadas: 16
- Páginas aprovadas antes deste lote: 0
- Ocorrências automatizadas: 845
- Contraste: 839
- Outras ocorrências estruturais: 6

## Correções deste lote

- O workflow não usa mais `continue-on-error`.
- O Pa11y gera `pa11y-report.json` para download no GitHub Actions.
- Node.js atualizado para a versão 24.
- Pa11y CI fixado na versão principal 4.
- `como-chegar.html` passou de 5 ocorrências para 0.
- Corrigidos link de salto, contraste dos links/CTA e uma informação contraditória sobre estacionamento no JSON-LD.
- O CSS de contraste existente passou a ser carregado nas páginas PT críticas que ainda não o utilizavam.

## Linha de base

- Limite inicial: 840 ocorrências.
- O workflow falha se houver regressão acima desse número.
- O limite deve ser reduzido após cada lote aprovado.
- Esta linha de base não significa conformidade integral; significa que a dívida passou a ser medida e não pode mais aumentar silenciosamente.

## Próximo lote

1. `parque-bondinho.html` — 14 ocorrências iniciais.
2. `entardecer.html` — 21 ocorrências iniciais.
3. `eventos.html` e `morro-da-urca.html` — 26 ocorrências iniciais cada.
4. Páginas de almoço, café da manhã, cardápio e homes multilíngues.
