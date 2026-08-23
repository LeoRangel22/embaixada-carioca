# Limpeza de governança dos workflows

Data: 2026-08-22  
Status geral: **PASS**

## Objetivo

Interromper automações legadas que reescreviam HTML, CSS, conteúdo editorial, schema ou relatórios e podiam reintroduzir regressões após correções manuais verificadas.

## Resultado

- Workflows ativos: **7**
- Workflows desativados nesta ação: **26**
- Workflows desativados no total: **30**
- Workflows ativos com escrita automática no conteúdo: **0**

## Workflows mantidos ativos

1. `pages-build-deployment` — publicação nativa do GitHub Pages.
2. `Verify live site` — verificação do site publicado.
3. `Super site standards SEO audit` — auditoria SEO somente de leitura.
4. `Schema JSON-LD CI gate` — validação de dados estruturados.
5. `Accessibility CI` — validação de acessibilidade.
6. `Hreflang Validation` — validação de alternância de idiomas.
7. `i18n Sync Validation` — validação de paridade PT/EN/ES.

## Decisão adicional

O workflow `Update version.json` também foi desativado. Embora não alterasse o conteúdo editorial, ele criava commits automáticos após cada publicação, cancelava o primeiro deploy e iniciava um segundo deploy. A versão publicada passa a ser identificada diretamente pelo SHA do commit/deploy.

## Regra de manutenção

Correções futuras devem ser aplicadas em lotes pequenos, validadas e publicadas por commit explícito. Workflows que alterem conteúdo automaticamente não devem ser reativados sem revisão do código, teste em branch separada e autorização do responsável pelo site.
