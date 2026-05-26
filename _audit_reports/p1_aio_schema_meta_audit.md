# P0 + P1 AIO Schema + Meta Audit

Status geral: **FAIL**

## Critérios
- P0 runtime de contraste/copy presente no repositório e carregado pelo `cafe-da-manha.html`.
- Homes PT/EN/ES com FAQPage e pelo menos 8 perguntas.
- Páginas críticas existentes com Restaurant ou FoodEstablishment schema.
- Meta description presente nas páginas prioritárias.
- Proibido usar aggregateRating/ratingValue/reviewCount/ratingCount/bestRating/worstRating no JSON-LD.

## P0 visual/operacional
- Status: **PASS**
  - geo_proximity_exists: True
  - cafe_page_exists: True
  - cafe_loads_geo_proximity: True
  - has_ecCafeCardapioContrast: True
  - has_ecBondinhoCopyFix: True
  - has_background_aware_strategy: True
  - has_dark_card_detection: True

## P1 FAQ Schema, Restaurant Schema e Meta descriptions
- `index.html` — PASS — meta 137 chars — Restaurant=True — FAQ=True (8)
- `en/index.html` — PASS — meta 134 chars — Restaurant=True — FAQ=True (8)
- `es/index.html` — PASS — meta 127 chars — Restaurant=True — FAQ=True (8)
- `eventos.html` — PASS — meta 134 chars — Restaurant=True — FAQ=True (3)
- `cardapio.html` — FAIL — meta 121 chars — Restaurant=True — FAQ=False (0)
  - forbidden rating/review fields in JSON-LD
  - forbidden: AggregateRating, aggregateRating, bestRating, ratingValue, reviewCount, worstRating
- `almoco.html` — FAIL — meta 126 chars — Restaurant=True — FAQ=False (0)
  - forbidden rating/review fields in JSON-LD
  - forbidden: AggregateRating, aggregateRating, bestRating, ratingValue, reviewCount, worstRating
- `cafe-da-manha.html` — FAIL — meta 128 chars — Restaurant=True — FAQ=True (8)
  - forbidden rating/review fields in JSON-LD
  - forbidden: AggregateRating, aggregateRating, bestRating, ratingValue, reviewCount, worstRating
- `entardecer.html` — FAIL — meta 102 chars — Restaurant=True — FAQ=False (0)
  - forbidden rating/review fields in JSON-LD
  - forbidden: AggregateRating, aggregateRating, bestRating, ratingValue, reviewCount, worstRating
- `en/eventos.html` — PASS — meta 122 chars — Restaurant=True — FAQ=True (8)
- `en/almoco.html` — PASS — meta 125 chars — Restaurant=True — FAQ=True (3)
- `en/cafe-da-manha.html` — PASS — meta 120 chars — Restaurant=True — FAQ=True (8)
- `en/sunset.html` — PASS — meta 103 chars — Restaurant=True — FAQ=False (0)
- `es/eventos.html` — PASS — meta 129 chars — Restaurant=True — FAQ=True (8)
- `es/almoco.html` — PASS — meta 128 chars — Restaurant=True — FAQ=True (3)
- `es/cafe-da-manha.html` — PASS — meta 124 chars — Restaurant=True — FAQ=True (8)
- `es/atardecer.html` — PASS — meta 109 chars — Restaurant=True — FAQ=False (0)
