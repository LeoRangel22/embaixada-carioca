# Existing Pages Content Structure Audit

Scope: current pages only. No new landing pages were created.

## index.html
- CSS consolidated link: already present
- H1 count: 1 — PASS
  - H1: Restaurante no Morro da Urca — a alma carioca em frente ao Pão de Açúcar.
- H2 count: 27
- H2 duplicates: PASS
- Images: 40
- Alt OK: 40
- Alt missing: 0
- Alt generic: 0
- Alt non-strategic: 0
- Strategic internal links: PASS
- WARN: high repeated phrase signals:
  - morro da urca: 94 uses (12.51/1k words)
  - pão de açúcar: 131 uses (17.43/1k words)
  - parque bondinho: 54 uses (7.19/1k words)
  - vista para o pão de açúcar: 12 uses (1.6/1k words)
  - café da manhã com vista: 12 uses (1.6/1k words)
  - restaurante no morro da urca: 9 uses (1.2/1k words)
  - rio de janeiro: 64 uses (8.52/1k words)
  - embaixada carioca: 77 uses (10.25/1k words)

## cafe-da-manha.html
- CSS consolidated link: already present
- H1 count: 1 — PASS
  - H1: Café da manhã com vista para o Pão de Açúcar — Morro da Urca.
- H2 count: 10
- H2 duplicates: PASS
- Images: 19
- Alt OK: 19
- Alt missing: 0
- Alt generic: 0
- Alt non-strategic: 0
- Strategic internal links: PASS
- WARN: high repeated phrase signals:
  - morro da urca: 24 uses (11.84/1k words)
  - pão de açúcar: 35 uses (17.27/1k words)
  - parque bondinho: 11 uses (5.43/1k words)
  - vista para o pão de açúcar: 14 uses (6.91/1k words)
  - café da manhã com vista: 11 uses (5.43/1k words)
  - rio de janeiro: 16 uses (7.89/1k words)
  - embaixada carioca: 14 uses (6.91/1k words)

## almoco.html
- CSS consolidated link: already present
- H1 count: 1 — PASS
  - H1: Almoço premiado no Pão de Açúcar — Restaurante Morro da Urca.
- H2 count: 10
- H2 duplicates: PASS
- Images: 17
- Alt OK: 17
- Alt missing: 0
- Alt generic: 0
- Alt non-strategic: 0
- Strategic internal links: PASS
- WARN: high repeated phrase signals:
  - morro da urca: 25 uses (17.56/1k words)
  - pão de açúcar: 24 uses (16.85/1k words)
  - parque bondinho: 10 uses (7.02/1k words)
  - rio de janeiro: 15 uses (10.53/1k words)
  - embaixada carioca: 9 uses (6.32/1k words)

## cardapio.html
- CSS consolidated link: already present
- H1 count: 1 — PASS
  - H1: Cardápio completo — Embaixada Carioca, Morro da Urca.
- H2 count: 12
- H2 duplicates: PASS
- Images: 11
- Alt OK: 11
- Alt missing: 0
- Alt generic: 0
- Alt non-strategic: 0
- Strategic internal links: PASS
- WARN: high repeated phrase signals:
  - morro da urca: 17 uses (11.76/1k words)
  - pão de açúcar: 23 uses (15.92/1k words)
  - vista para o pão de açúcar: 8 uses (5.54/1k words)
  - rio de janeiro: 13 uses (9.0/1k words)
  - embaixada carioca: 12 uses (8.3/1k words)

## como-chegar.html
- CSS consolidated link: already present
- H1 count: 1 — PASS
  - H1: Como chegar à Embaixada Carioca no Morro da Urca
- H2 count: 6
- H2 duplicates: PASS
- Images: 3
- Alt OK: 3
- Alt missing: 0
- Alt generic: 0
- Alt non-strategic: 0
- WARN: missing strategic internal links:
  - index.html
- WARN: high repeated phrase signals:
  - morro da urca: 18 uses (16.84/1k words)
  - pão de açúcar: 15 uses (14.03/1k words)
  - parque bondinho: 13 uses (12.16/1k words)
  - embaixada carioca: 8 uses (7.48/1k words)

## eventos.html
- CSS consolidated link: already present
- H1 count: 1 — PASS
  - H1: Eventos no Morro da Urca — com vista para o Pão de Açúcar.
- H2 count: 9
- H2 duplicates: PASS
- Images: 10
- Alt OK: 10
- Alt missing: 0
- Alt generic: 0
- Alt non-strategic: 0
- Strategic internal links: PASS
- WARN: high repeated phrase signals:
  - morro da urca: 22 uses (14.91/1k words)
  - pão de açúcar: 20 uses (13.55/1k words)
  - parque bondinho: 9 uses (6.1/1k words)
  - vista para o pão de açúcar: 10 uses (6.78/1k words)
  - rio de janeiro: 13 uses (8.81/1k words)
  - embaixada carioca: 8 uses (5.42/1k words)

## guia-do-rio.html
- CSS consolidated link: already present
- H1 count: 1 — PASS
  - H1: Roteiro Rio de Janeiro O Guia Definitivo.
- H2 count: 15
- H2 duplicates: PASS
- Images: 9
- Alt OK: 9
- Alt missing: 0
- Alt generic: 0
- Alt non-strategic: 0
- Strategic internal links: PASS
- WARN: high repeated phrase signals:
  - morro da urca: 28 uses (7.49/1k words)
  - pão de açúcar: 35 uses (9.37/1k words)
  - parque bondinho: 13 uses (3.48/1k words)
  - rio de janeiro: 29 uses (7.76/1k words)
  - embaixada carioca: 29 uses (7.76/1k words)

## Summary
- Total issues/signals: 41
- Auto-fix applied: consolidated CSS link injection only.
- Manual/next automated passes: headings normalization, alt text rewrite, internal link insertion, copy deduplication.
