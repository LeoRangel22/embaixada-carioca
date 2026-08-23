# Revisão editorial de seções PT/EN/ES — Lote 1

Data: 2026-08-23  
Status geral: **PASS com diferenças estruturais justificadas**

## Escopo

- `cafe-da-manha.html`, `en/cafe-da-manha.html`, `es/cafe-da-manha.html`
- `cardapio.html`, `en/cardapio.html`, `es/cardapio.html`
- `guia-do-rio.html`, `en/guia-do-rio.html`, `es/guia-do-rio.html`
- `feijoada.html`, `en/feijoada.html`, `es/feijoada.html`

## Critério adotado

A revisão verificou equivalência semântica e comercial, não igualdade mecânica do número de `h1/h2`. Blocos SEO repetidos na página PT não foram copiados para EN/ES quando o mesmo objetivo já era atendido por uma seção localizada. Isso evita conteúdo redundante e páginas artificialmente infladas.

## Resultado por grupo

| Grupo | Resultado | Ações principais |
|---|---|---|
| Café da Manhã | PASS | A estrutura comercial essencial já estava equivalente. Foram localizados breadcrumb, resumo lateral e atendimento WhatsApp em ES. Não foram duplicados blocos SEO redundantes da página PT. |
| Cardápio | PASS | A cobertura do cardápio completo permanece em 12 seções e 149 itens por idioma. Foram corrigidos nomes, descrições, unidades, preços, badges, CTAs, atendimento e JSON-LD editorial em EN/ES. |
| Guia do Rio | PASS | O guia útil já existia nos três idiomas. Foram localizados hero, resumo, CTA, links relacionados, metadados editoriais, rodapé e atendimento em EN/ES. |
| Feijoada | PASS | Foram localizados hero, cards de pratos, unidades, CTA, galeria, atendimento e Menu/MenuItem JSON-LD. A formulação do prêmio permanece canônica e segura nos três idiomas. |

## Correção adicional de legenda

A imagem `assets/bobo-camarao-real.webp` estava identificada incorretamente como risoto de camarão. A legenda e o texto alternativo foram corrigidos para **bobó de camarão** em PT, EN e ES.

## Guardrails validados

- JSON-LD duplicate key guard: **PASS** — 110 arquivos, 0 ocorrências.
- Schema rating guard: **PASS** — nenhum `Review`, `Rating` ou `AggregateRating` indevido.
- GSC post-fix structured data validation: **PASS**.
- Paridade de arquivos: **PASS** — nenhuma página PT sem equivalente EN ou ES.

## Interpretação das diferenças de headings

O relatório geral ainda sinaliza estes quatro grupos por diferença numérica de headings. Neste lote, os avisos são tratados como **advisory**, porque a revisão confirmou cobertura semântica e comercial e identificou duplicações/variações estruturais legítimas na página PT. Os alertas não representam seção comercial ausente nos idiomas internacionais.

## Próximo lote

Revisar as oito diferenças restantes:

1. `almoco-morro-da-urca.html`
2. `almoco.html`
3. `eventos.html`
4. `index.html`
5. `morro-da-urca.html`
6. `parque-bondinho.html`
7. `restaurante-com-vista-rio-de-janeiro.html`
8. `sunset-por-do-sol-rio-de-janeiro.html`
