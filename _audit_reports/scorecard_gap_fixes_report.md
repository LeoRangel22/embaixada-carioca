# Scorecard Gap Fixes

Status geral: **FAIL**

## Objetivo
Corrigir os gaps apontados no scorecard visual: FAQ incompleto, `parque-bondinho.html` sem FAQ/OL e conteúdo fino em `eventos.html`.

## Guardrails
- FAQPage existente nas páginas-alvo foi substituído por um único FAQPage com 8 perguntas para evitar duplicidade.
- Nenhum AggregateRating, Rating ou Review foi inserido.
- Nenhum Restaurant schema foi removido.
- Alterações visíveis foram aplicadas apenas em `eventos.html` e `parque-bondinho.html`.

## Resumo
- Páginas configuradas: **5**
- Páginas com PASS: **4**
- Páginas com falha: **1**
- Páginas alteradas: **5**

## Resultados por página

| Página | Status | Changed | FAQ | OL | Palavras | Notas |
|---|---|---:|---:|---:|---:|---|
| `index.html` | ok | True | 8 | 2 | 6756 | faq_json_ld_removed=1 |
| `eventos.html` | fail | True | 8 | 3 | 1110 | faq_json_ld_removed=1; visible_depth_block=True |
| `en/cardapio.html` | ok | True | 8 | 1 | 1274 | faq_json_ld_removed=1 |
| `en/almoco.html` | ok | True | 8 | 2 | 1559 | faq_json_ld_removed=1 |
| `parque-bondinho.html` | ok | True | 8 | 1 | 1598 | faq_json_ld_removed=1; visible_depth_block=True |

## Próxima validação
Rodar o Final 86-page AAA master audit e a validação GSC pós-fix para confirmar que não houve duplicidade de FAQPage.
