# Correções do diagnóstico SEO — 8 de setembro de 2026

## Resultado geral

**Status: PASS**

O lote corrige os problemas informados nos três CSVs do diagnóstico e amplia a verificação para todas as 97 URLs canônicas do `sitemap.xml`.

## Fontes analisadas

- `www.embaixadacarioca.com_SEOAnalysisSummary_2026_09_08.csv`
- `www.embaixadacarioca.com_IssueDetailsBySeverity_9_8_2026.csv`
- `www.embaixadacarioca.com_FailingUrls_9_8_2026.csv`

O detalhamento recebido informava:

- 2 páginas com resposta HTTP 4xx;
- 6 páginas com título excessivamente longo;
- 1 página com tag HTML aninhada dentro de `<title>`;
- 3 páginas com mais de um `<h1>`.

O arquivo de URLs continha apenas `como-chegar.html`. Essa página já estava correta no repositório (título simples, um H1 e URL válida), portanto o lote usou uma varredura estrutural das 97 URLs do sitemap para localizar e corrigir as ocorrências reais.

## Correções aplicadas

### URLs e links

- Links EN de “How to Get There” agora apontam diretamente para `/en/how-to-get-there.html`.
- Links ES de “Cómo Llegar” agora apontam diretamente para `/es/como-llegar.html`.
- Botões que apontavam para `/reservas.html` agora abrem o sistema oficial Tagme.
- Adicionado redirecionamento 301 de `/es/como-chegar.html` para `/es/como-llegar.html`.
- Adicionado redirecionamento 301 de `/reservas.html` para o sistema oficial Tagme.

### Títulos

- Removida a tag `<a>` inválida de dentro do título de `entardecer.html`.
- Encurtados seis títulos com 70 ou mais caracteres, preservando a principal intenção de busca em PT, EN e ES.

### Hierarquia de conteúdo

- Corrigidos H1 duplicados nas versões PT, EN e ES de `feijoada.html`.
- Corrigidos H1 duplicados nas versões PT, EN e ES de `restaurante-com-vista-rio-de-janeiro.html`.
- Cada página mantém um único H1 alinhado à sua intenção principal; o título editorial secundário passou a H2.

### Recrawl

- Atualizado o `lastmod` no sitemap para as 19 páginas alteradas neste lote.

## Validação pós-correção

| Critério | Resultado |
|---|---:|
| URLs canônicas verificadas | 97 |
| Títulos com 70 ou mais caracteres | 0 |
| Tags HTML dentro de `<title>` | 0 |
| Páginas sem exatamente um H1 | 0 |
| Links internos para as URLs antigas corrigidas | 0 |
| Schema com `Review`, `Rating` ou `AggregateRating` indevido | 0 |
| JSON-LD com chaves duplicadas | 0 |
| Auditoria hreflang PT/EN/ES | PASS |

## Observação

O redirecionamento 301 entra em vigor após a publicação no Cloudflare Pages. Os títulos e headings estarão no site assim que o deploy do commit terminar.
