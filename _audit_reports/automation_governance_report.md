# Automation governance report

**Status geral: PASS**

## Objetivo

Impedir que rotinas automáticas de correção reescrevam HTML, CSS, JavaScript e conteúdo editorial a cada publicação.

## Resultado

- 22 workflows mutantes foram convertidos para execução exclusivamente manual (`workflow_dispatch`).
- Os workflows continuam disponíveis para uso deliberado, mas não são mais disparados por alterações no site.
- Os gates automáticos somente de validação foram preservados.
- O workflow nativo de versionamento/publicação foi preservado.

## Validações automáticas preservadas

- Accessibility CI
- Hreflang validation
- I18N sync validation
- Schema CI gate
- Super site standards SEO audit
- Verify live site
- Update version / GitHub Pages

## Regra operacional

Um fixer só deve ser executado manualmente depois de revisão do diff. Nenhum fixer pode publicar alegações factuais, traduções ou alterações visuais sem validação humana.
