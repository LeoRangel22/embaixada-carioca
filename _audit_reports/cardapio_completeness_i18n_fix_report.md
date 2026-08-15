# Cardapio Completeness + I18N Fix

Status geral: **PASS**

## Objetivo
Restaurar no site o conteúdo do cardápio completo e garantir que a página de cardápio tenha a mesma cobertura em português, inglês e espanhol.

## Fonte operacional
- `Cardápio - Embaixada Carioca - Pt e Esp - outubro 2025 digital.pdf`.
- Páginas de referência: entradas, petiscos, sanduíches, saladas, burgers, almoço, especialidades, café da manhã, cafeteria, caipirinhas, drinks, bebidas, cervejas e sobremesas.

## Guardrails
- Nenhum JSON-LD/schema foi alterado.
- Nenhuma canonical/hreflang foi alterada.
- Nenhum rating/review/aggregateRating foi inserido.
- O bloco foi inserido apenas como conteúdo editorial visível do cardápio.

## Resumo
- Seções restauradas por idioma: **12**
- Itens restaurados por idioma: **149**
- Paridade PT/EN/ES: **OK**

## Resultados por página

| Idioma | Página | Changed | Seções | Itens |
|---|---|---:|---:|---:|
| `pt` | `cardapio.html` | True | 12 | 149 |
| `en` | `en/cardapio.html` | False | 12 | 149 |
| `es` | `es/cardapio.html` | False | 12 | 149 |
