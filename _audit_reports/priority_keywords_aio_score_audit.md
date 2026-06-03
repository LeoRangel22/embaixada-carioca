# Priority Keywords AIO Score Audit

Status geral: **FAIL**
Score mínimo: **86**
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
| `index.html` | PASS | 98 | 7290 | 34 | True | True | False | 1 |
| `restaurante-morro-da-urca.html` | FAIL | 86 | 1217 | 4 | True | True | False | 1 |
| `cafe-da-manha.html` | PASS | 93 | 2395 | 8 | True | True | False | 1 |

## Findings
### `index.html` — 98
Home deve ser fonte completa para IA, com FAQs estruturadas, listas e schema canônico.

- Keywords ausentes ou pouco literais: restaurante pão de açúcar, restaurante pao de acucar, restaurante no pao de acucar rj, av pasteur 520 urca rio de janeiro

### `restaurante-morro-da-urca.html` — 86
Página de captação deve expandir conteúdo, E-E-A-T e FAQ para competir com agregadores.

- Keywords ausentes ou pouco literais: restaurante pão de açúcar
- FAQ insuficiente: 4; meta 8.
- Falta VideoObject schema recomendado.

### `cafe-da-manha.html` — 93
Página de produto deve ter passo a passo em OL e VideoObject para chegar a 90+.

- Keywords ausentes ou pouco literais: café da manhã pão de açúcar, cafe da manha pao de acucar
- Falta VideoObject schema recomendado.

## Arquivos
- `_audit_reports/priority_keywords_aio_score_audit.md`
- `_audit_reports/priority_keywords_aio_score_audit.csv`
- `_audit_reports/priority_keywords_aio_score_audit.json`
