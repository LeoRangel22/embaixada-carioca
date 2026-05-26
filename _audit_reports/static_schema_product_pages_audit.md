# Static Schema Product Pages Audit

Status geral: **FAIL**

## Critérios
- Restaurant Schema estático no HTML das páginas de produto críticas.
- FAQPage estático com 8 perguntas nas páginas configuradas.
- Nenhum campo de rating/review proibido no HTML.
- Páginas inexistentes são marcadas como SKIP, não como FAIL.

## Resultados por página
- `eventos.html` — **PASS** — Restaurant=True — FAQ=True (8) — changed=True
- `cardapio.html` — **FAIL** — Restaurant=True — FAQ=True (8) — changed=True
  - forbidden: AggregateRating, aggregateRating, bestRating, ratingValue, reviewCount, worstRating
  - forbidden rating/review terms found
- `almoco.html` — **FAIL** — Restaurant=True — FAQ=True (8) — changed=True
  - forbidden: AggregateRating, aggregateRating, bestRating, ratingValue, reviewCount, worstRating
  - forbidden rating/review terms found
- `entardecer.html` — **FAIL** — Restaurant=True — FAQ=True (8) — changed=True
  - forbidden: AggregateRating, aggregateRating, bestRating, ratingValue, reviewCount, worstRating
  - forbidden rating/review terms found
- `feijoada.html` — **FAIL** — Restaurant=True — FAQ=True (8) — changed=True
  - forbidden: AggregateRating, aggregateRating, bestRating, ratingValue, reviewCount, worstRating
  - forbidden rating/review terms found
- `cafe-da-manha.html` — **FAIL** — Restaurant=True — FAQ=True (8) — changed=True
  - forbidden: AggregateRating, aggregateRating, bestRating, ratingValue, reviewCount, worstRating
  - forbidden rating/review terms found
- `morro-da-urca.html` — **FAIL** — Restaurant=True — FAQ=True (8) — changed=True
  - forbidden: AggregateRating, aggregateRating, bestRating, ratingValue, reviewCount, worstRating
  - forbidden rating/review terms found
- `en/sunset.html` — **PASS** — Restaurant=True — FAQ=True (8) — changed=True
- `en/cardapio.html` — **PASS** — Restaurant=True — FAQ=True (8) — changed=True
- `en/almoco.html` — **PASS** — Restaurant=True — FAQ=True (8) — changed=True
- `en/morro-da-urca.html` — **PASS** — Restaurant=True — FAQ=True (8) — changed=True
- `es/atardecer.html` — **PASS** — Restaurant=True — FAQ=True (8) — changed=True
- `es/cardapio.html` — **PASS** — Restaurant=True — FAQ=True (8) — changed=True
- `es/almoco.html` — **PASS** — Restaurant=True — FAQ=True (8) — changed=True
- `es/morro-da-urca.html` — **PASS** — Restaurant=True — FAQ=True (8) — changed=True
