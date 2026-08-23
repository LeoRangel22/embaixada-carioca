# High-Traffic English Editorial Fix

Date: 2026-08-23
Overall status: **PASS**

## Scope

Natural-English review of the seven highest-value commercial pages, covering visible copy, metadata, FAQ content and JSON-LD labels.

## Results

| Page | Status | Remaining blocked phrases | JSON-LD errors | Unsafe rating schema |
|---|---:|---:|---:|---:|
| `en/index.html` | PASS | 0 | 0 | no |
| `en/eventos.html` | PASS | 0 | 0 | no |
| `en/cardapio.html` | PASS | 0 | 0 | no |
| `en/cafe-da-manha.html` | PASS | 0 | 0 | no |
| `en/almoco.html` | PASS | 0 | 0 | no |
| `en/feijoada.html` | PASS | 0 | 0 | no |
| `en/sunset.html` | PASS | 0 | 0 | no |

## Guardrails

- No Review, Rating or AggregateRating schema introduced.
- Every JSON-LD block on the target pages remains parseable.
- Canonical and hreflang URLs were preserved, except the incorrect English feijoada `og:url`, which now points to its own page.
- The feijoada award is attributed to Academia da Cachaça and its formal partnership with Embaixada Carioca.
- Event capacity remains variable by format; unsupported fixed-capacity claims were removed from the main English events page.
