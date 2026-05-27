# Duplicate FAQ Schema Cleaner

Status geral: **PASS**

## Objetivo
Garantir no máximo um `FAQPage` por URL nas páginas críticas apontadas pelo relatório de FAQ duplicado.

## Guardrails
- Nós não-FAQ em JSON-LD são preservados.
- Nenhum AggregateRating, Rating ou Review é inserido.
- Casos especiais `es/cardapio.html` e `es/almoco.html` mantêm o bloco estático completo de 8 perguntas.

## Resumo
- Páginas analisadas: **11**
- Páginas com PASS: **11**
- Páginas com falha: **0**
- Páginas alteradas: **8**

## Resultados por página

| Página | Status | Changed | FAQ antes | Perguntas antes | FAQ depois | Perguntas depois | FAQ removidos | Notas |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `index.html` | ok | True | 2 | 16 | 1 | 8 | 1 | kept:no-id:8; stripped-faq-preserved-nonfaq:ec-static-product-schema-faq:8 |
| `en/index.html` | ok | True | 2 | 16 | 1 | 8 | 1 | kept:ec-p1-aio-schema-meta:8; stripped-faq-preserved-nonfaq:ec-static-product-schema-faq:8 |
| `es/index.html` | ok | True | 2 | 16 | 1 | 8 | 1 | kept:ec-p1-aio-schema-meta:8; stripped-faq-preserved-nonfaq:ec-static-product-schema-faq:8 |
| `feijoada.html` | ok | True | 2 | 16 | 1 | 8 | 1 | kept:no-id:8; stripped-faq-preserved-nonfaq:ec-static-product-schema-faq:8 |
| `cafe-da-manha.html` | ok | True | 2 | 16 | 1 | 8 | 1 | kept:no-id:8; stripped-faq-preserved-nonfaq:ec-static-product-schema-faq:8 |
| `eventos.html` | ok | True | 2 | 16 | 1 | 8 | 1 | kept:no-id:8; stripped-faq-preserved-nonfaq:ec-static-product-schema-faq:8 |
| `en/cardapio.html` | ok | True | 2 | 16 | 1 | 8 | 1 | kept:no-id:8; stripped-faq-preserved-nonfaq:ec-static-product-schema-faq:8 |
| `es/cardapio.html` | ok | False | 1 | 8 | 1 | 8 | 0 | kept:ec-static-product-schema-faq:8 |
| `en/almoco.html` | ok | True | 2 | 16 | 1 | 8 | 1 | kept:no-id:8; stripped-faq-preserved-nonfaq:ec-static-product-schema-faq:8 |
| `es/almoco.html` | ok | False | 1 | 8 | 1 | 8 | 0 | kept:ec-static-product-schema-faq:8 |
| `parque-bondinho.html` | ok | False | 1 | 8 | 1 | 8 | 0 | kept:no-id:8 |
