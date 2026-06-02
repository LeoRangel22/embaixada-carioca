# Relatório de Execução — Fase 1: Higiene de Código
**Data:** 2026-06-02  
**Modo:** DRY-RUN (simulação — nenhum arquivo foi modificado)  
**Repositório:** LeoRangel22/embaixada-carioca

---

## Resumo Executivo

| Métrica | Resultado |
| :--- | :--- |
| Arquivos HTML processados | 47 |
| Arquivos HTML modificados | 0 |
| CSS duplicados removidos (T-1.1) | 0 |
| JS duplicados removidos (T-1.1) | 0 |
| Títulos otimizados (T-1.2) | 0 |
| Descriptions otimizadas (T-1.3) | 0 |
| Tags hreflang adicionadas (T-1.4) | 0 |
| Imagens com srcset adicionado (T-1.5) | 0 |
| URLs no sitemap sem lastmod (T-1.6) | 0 |
| URLs no sitemap corrigidas (T-1.6) | 0 |

---

## Detalhamento por Arquivo

| Arquivo | Modificado | CSS Dup. | JS Dup. | Título | Desc. | Hreflang | Srcset |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `almoco-morro-da-urca.html` | — | — | — | — | — | — | — |
| `almoco.html` | — | — | — | — | — | — | — |
| `cafe-da-manha-com-vista-rio-de-janeiro.html` | — | — | — | — | — | — | — |
| `cafe-da-manha-pao-de-acucar.html` | — | — | — | — | — | — | — |
| `cafe-da-manha.html` | — | — | — | — | — | — | — |
| `caipirinha-com-vista-rio.html` | — | — | — | — | — | — | — |
| `cardapio.html` | — | — | — | — | — | — | — |
| `como-chegar.html` | — | — | — | — | — | — | — |
| `en/almoco-morro-da-urca.html` | — | — | — | — | — | — | — |
| `en/almoco.html` | — | — | — | — | — | — | — |
| `en/cafe-da-manha.html` | — | — | — | — | — | — | — |
| `en/caipirinha-com-vista-rio.html` | — | — | — | — | — | — | — |
| `en/cardapio.html` | — | — | — | — | — | — | — |
| `en/entardecer.html` | — | — | — | — | — | — | — |
| `en/eventos.html` | — | — | — | — | — | — | — |
| `en/gastronomia-carioca.html` | — | — | — | — | — | — | — |
| `en/guia-do-rio.html` | — | — | — | — | — | — | — |
| `en/how-to-get-there.html` | — | — | — | — | — | — | — |
| `en/index.html` | — | — | — | — | — | — | — |
| `en/sunset.html` | — | — | — | — | — | — | — |
| `entardecer.html` | — | — | — | — | — | — | — |
| `es/almoco.html` | — | — | — | — | — | — | — |
| `es/atardecer.html` | — | — | — | — | — | — | — |
| `es/cafe-da-manha.html` | — | — | — | — | — | — | — |
| `es/cardapio.html` | — | — | — | — | — | — | — |
| `es/como-llegar.html` | — | — | — | — | — | — | — |
| `es/entardecer.html` | — | — | — | — | — | — | — |
| `es/eventos.html` | — | — | — | — | — | — | — |
| `es/gastronomia-carioca.html` | — | — | — | — | — | — | — |
| `es/guia-do-rio.html` | — | — | — | — | — | — | — |
| `es/index.html` | — | — | — | — | — | — | — |
| `es/nossa-visao.html` | — | — | — | — | — | — | — |
| `es/o-que-fazer-depois-do-bondinho-pao-de-acucar.html` | — | — | — | — | — | — | — |
| `es/parque-bondinho-pan-de-azucar.html` | — | — | — | — | — | — | — |
| `es/parque-bondinho.html` | — | — | — | — | — | — | — |
| `es/por-do-sol-morro-da-urca.html` | — | — | — | — | — | — | — |
| `es/restaurante-morro-da-urca.html` | — | — | — | — | — | — | — |
| `feijoada-com-vista-rio-de-janeiro.html` | — | — | — | — | — | — | — |
| `guia-do-rio.html` | — | — | — | — | — | — | — |
| `index.html` | — | — | — | — | — | — | — |
| `morro-da-urca.html` | — | — | — | — | — | — | — |
| `parque-bondinho-pao-de-acucar.html` | — | — | — | — | — | — | — |
| `parque-bondinho.html` | — | — | — | — | — | — | — |
| `por-do-sol-morro-da-urca.html` | — | — | — | — | — | — | — |
| `restaurante-morro-da-urca.html` | — | — | — | — | — | — | — |
| `restaurantes-romanticos-rio-de-janeiro.html` | — | — | — | — | — | — | — |
| `roteiro-meio-dia-urca-pao-de-acucar.html` | — | — | — | — | — | — | — |

---

## Critérios de Validação

Execute o script de auditoria para confirmar que todos os critérios foram atendidos:

```bash
python3 scripts/audit_fase1.py
```

Resultados esperados após a execução:

- `grep -c "ec-contrast-fixes.css" index.html` → `1`
- `grep -c "dossie-content-enhancer.js" index.html` → `1`
- Títulos com problemas: `0`
- Descriptions com problemas: `0`
- URLs no sitemap sem lastmod: `0`

