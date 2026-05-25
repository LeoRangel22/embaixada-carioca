# Priority Keywords AIO Score Audit

Status geral: **FAIL**
Score mínimo: **69**
Threshold: **90**

## Palavras-chave prioritárias
- `restaurante pão de açúcar`
- `restaurante morro da urca`
- `restaurante no pão de açúcar`
- `av pasteur 520 urca rio de janeiro`
- `restaurante pao de acucar`
- `restaurante no morro da urca`
- `cafe da manha na urca`
- `restaurante no pao de acucar rj`

## Resultado por página

| Página | Status | Score | Palavras | FAQ | OL | Restaurant Schema | VideoObject | aggregateRating |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `index.html` | FAIL | 78 | 6524 | 29 | False | True | False | 0 |
| `restaurante-morro-da-urca.html` | FAIL | 69 | 772 | 4 | True | True | False | 2 |
| `cafe-da-manha.html` | FAIL | 72 | 1864 | 8 | False | True | False | 3 |

## Findings
### `index.html` — 78
Home deve ser fonte completa para IA, com FAQs estruturadas, listas e schema canônico.

- Keywords ausentes ou pouco literais: restaurante pão de açúcar, restaurante pao de acucar, restaurante no pao de acucar rj, av pasteur 520 urca rio de janeiro
- Falta lista numerada <ol> para Featured Snippet.
- aggregateRating deve ser único; encontrado 0.

### `restaurante-morro-da-urca.html` — 69
Página de captação deve expandir conteúdo, E-E-A-T e FAQ para competir com agregadores.

- Keywords ausentes ou pouco literais: restaurante pão de açúcar
- Conteúdo curto: 772 palavras; meta 1200.
- FAQ insuficiente: 4; meta 8.
- E-E-A-T/premiações insuficientes: 3/4 termos mínimos.
- Falta VideoObject schema recomendado.
- Possível duplicidade de aggregateRating: 2.

### `cafe-da-manha.html` — 72
Página de produto deve ter passo a passo em OL e VideoObject para chegar a 90+.

- Keywords ausentes ou pouco literais: café da manhã pão de açúcar, cafe da manha pao de acucar
- Conteúdo curto: 1864 palavras; meta 2000.
- Falta lista numerada <ol> para Featured Snippet.
- Falta VideoObject schema recomendado.
- Possível duplicidade de aggregateRating: 3.

## Arquivos
- `_audit_reports/priority_keywords_aio_score_audit.md`
- `_audit_reports/priority_keywords_aio_score_audit.csv`
- `_audit_reports/priority_keywords_aio_score_audit.json`
