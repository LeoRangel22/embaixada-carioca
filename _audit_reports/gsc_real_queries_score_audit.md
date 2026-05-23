# GSC Real Organic Queries Score Audit

Status geral: **FAIL**
Score mínimo: **59**
Threshold: **90**

## Base
- Fonte: print do Search Console / Google organic search queries
- Período: 15–21 mai. 2026
- Total visível no print: 75 cliques, 1.888 impressões, CTR 3,97%

## Critério de score
- 55% cobertura do cluster de intenção no texto visível
- 15% title alinhado à intenção
- 15% meta description alinhada à intenção
- 10% H1 alinhado à intenção
- 5% presença exata ou semântica da consulta

## Páginas-alvo
- `index.html` — FAIL — score 86 — cobertos 6/7
  - Faltando: av pasteur
- `restaurante-morro-da-urca.html` — PASS — score 100 — cobertos 5/5
- `cafe-da-manha.html` — PASS — score 100 — cobertos 4/4
- `como-chegar.html` — FAIL — score 80 — cobertos 4/5
  - Faltando: av pasteur

## Consultas abaixo de 90
- `avaliações sobre embaixada carioca` → `index.html` — score 59, cluster reviews, impr. 112, cliques 0, CTR 0.0% — Reforçar cluster na página: 
- `av pasteur 520 - urca rio de janeiro` → `como-chegar.html` — score 78, cluster address, impr. 22, cliques 0, CTR 0.0% — Reforçar cluster na página: av pasteur
- `avenida pasteur 520` → `como-chegar.html` — score 78, cluster address, impr. 17, cliques 0, CTR 0.0% — Reforçar cluster na página: av pasteur
- `embaixada carioca` → `index.html` — score 85, cluster brand, impr. 293, cliques 45, CTR 15.36% — Reforçar cluster na página: 
- `embaixada` → `index.html` — score 85, cluster brand, impr. 30, cliques 2, CTR 6.67% — Reforçar cluster na página: 

## Todas as consultas
- `embaixada carioca` → `index.html` — score 85 — cluster=100, title=100, desc=0, h1=100, exact=True
- `avaliações sobre embaixada carioca` → `index.html` — score 59 — cluster=100, title=0, desc=0, h1=0, exact=False
- `morro da urca` → `restaurante-morro-da-urca.html` — score 100 — cluster=100, title=100, desc=100, h1=100, exact=True
- `restaurante urca` → `restaurante-morro-da-urca.html` — score 99 — cluster=100, title=100, desc=100, h1=100, exact=False
- `restaurante pão de açucar` → `index.html` — score 99 — cluster=100, title=100, desc=100, h1=100, exact=False
- `restaurante morro da urca` → `restaurante-morro-da-urca.html` — score 100 — cluster=100, title=100, desc=100, h1=100, exact=True
- `restaurante na urca` → `restaurante-morro-da-urca.html` — score 99 — cluster=100, title=100, desc=100, h1=100, exact=False
- `restaurante no pão de açúcar` → `index.html` — score 100 — cluster=100, title=100, desc=100, h1=100, exact=True
- `embaixada` → `index.html` — score 85 — cluster=100, title=100, desc=0, h1=100, exact=True
- `restaurante no morro da urca` → `restaurante-morro-da-urca.html` — score 100 — cluster=100, title=100, desc=100, h1=100, exact=True
- `restaurantes urca` → `restaurante-morro-da-urca.html` — score 99 — cluster=100, title=100, desc=100, h1=100, exact=False
- `av pasteur 520 - urca rio de janeiro` → `como-chegar.html` — score 78 — cluster=83, title=70, desc=70, h1=70, exact=False
- `restaurante pao de acucar` → `index.html` — score 99 — cluster=100, title=100, desc=100, h1=100, exact=False
- `cafe da manha pao de acucar` → `cafe-da-manha.html` — score 99 — cluster=100, title=100, desc=100, h1=100, exact=False
- `avenida pasteur 520` → `como-chegar.html` — score 78 — cluster=83, title=70, desc=70, h1=70, exact=False
- `cafe da manha na urca` → `cafe-da-manha.html` — score 100 — cluster=100, title=100, desc=100, h1=100, exact=True
- `restaurantes na urca` → `restaurante-morro-da-urca.html` — score 99 — cluster=100, title=100, desc=100, h1=100, exact=False
- `morro da urca rio de janeiro` → `restaurante-morro-da-urca.html` — score 99 — cluster=100, title=100, desc=100, h1=100, exact=False
- `restaurante no pao de açucar rj` → `index.html` — score 99 — cluster=100, title=100, desc=100, h1=100, exact=False
- `café da manhã na urca` → `cafe-da-manha.html` — score 100 — cluster=100, title=100, desc=100, h1=100, exact=True
- `restaurante bondinho` → `index.html` — score 99 — cluster=100, title=100, desc=100, h1=100, exact=False
