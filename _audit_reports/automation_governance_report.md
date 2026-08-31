# Automation governance report

**Atualizado em:** 31/08/2026

**Status geral:** PASS

## Objetivo

Impedir que rotinas automáticas reescrevam HTML, CSS, JavaScript, traduções ou alegações factuais a cada publicação.

## Estado atual confirmado

- Workflows ativos: **7**.
- Workflows legados desativados: **30**.
- Automações mutantes permanecem desativadas mesmo quando o arquivo YAML continua no repositório.
- Cloudflare Pages é a hospedagem pública principal ligada ao branch `master`.
- O workflow nativo do GitHub Pages foi mantido como publicação secundária, não como origem canônica do domínio.

## Workflows ativos autorizados

| Workflow | Tipo | Decisão |
|---|---|---|
| Pages build and deployment | publicação secundária | manter |
| Verify live site | verificação do site publicado | manter |
| Super site standards SEO audit | auditoria somente de leitura | manter |
| Schema JSON-LD CI gate | gate de schema | manter |
| Accessibility CI | gate de acessibilidade | manter |
| Hreflang Validation | gate multilíngue | manter |
| i18n Sync Validation | gate de paridade estrutural | manter |

## Workflows desativados

Os 30 workflows desativados incluem fixers visuais, schema/hreflang mutante, otimização multilíngue contínua, auditorias que commitavam alterações e lotes pontuais já concluídos. A desativação é intencional e não deve ser revertida em massa.

## Regra operacional

Um fixer só pode ser executado quando houver:

1. objetivo e arquivos-alvo definidos;
2. leitura prévia do script;
3. snapshot do estado do repositório;
4. revisão humana do diff completo;
5. validação de schema, idiomas, links e visual quando aplicável;
6. commit restrito aos arquivos aprovados;
7. confirmação no domínio publicado.

Nenhum fixer pode publicar alegações factuais, traduções ou alterações visuais sem validação humana.
