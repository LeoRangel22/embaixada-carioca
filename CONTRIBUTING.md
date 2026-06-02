# Como contribuir para o Embaixada Carioca

## Estrutura do projeto
- `/` — páginas em português (idioma padrão)
- `/en/` — páginas em inglês (traduções manuais, manter em sync com PT)
- `/es/` — páginas em espanhol (traduções manuais, manter em sync com PT)
- `/assets/` — imagens (sempre use .webp para servir, .jpg como backup)
- `/assets/css/` — CSS externo (6 arquivos, ver seção CSS abaixo)
- `/assets/fonts/` — fontes e fonts.css
- `/.github/workflows/` — CI/CD (33 workflows, ver seção Workflows)
- `/scripts/` — scripts Python de auditoria e aplicação de fixes
- `/docs/` — documentação de arquitetura

## Adicionando uma nova página

1. Copie uma página existente do mesmo tipo como base
2. Atualize: `<title>`, `<meta name="description">`, hreflang links, JSON-LD schema
3. Adicione a URL no `sitemap.xml`
4. Crie versões EN (`/en/`) e ES (`/es/`) correspondentes
5. Atualize `version.json` com a data e descrição da mudança

## Gerenciando imagens

- **Sempre use WebP** para imagens servidas no HTML (`<img src="...webp">`)
- **Nunca suba PNG/JPG grandes sem WebP equivalente**
- Antes de adicionar: verificar se não há versão existente em `assets/`
- Nomear com kebab-case descritivo: `prato-nome-contexto.webp`
- Rodar `grep -r "nome-da-imagem" --include="*.html"` antes de deletar qualquer imagem

## CSS

O site usa CSS em 3 camadas:
1. `assets/fonts/fonts.css` — fontes
2. `assets/css/ec-stabilization-base.css` — reset e variáveis globais
3. `assets/css/ec-*.css` — módulos temáticos

**Evite** adicionar `<style>` inline nas páginas. Contribuições com CSS inline não serão aceitas.

## Workflows CI/CD

- Workflows `one-off-*` são de uso único e não devem ser re-executados
- Para auditorias: rodar scripts em `scripts/audit_*.py` localmente antes de criar workflow
- Para fixes em massa: criar script em `scripts/apply_*.py`, testar em 1 página, depois aplicar

## Sync PT/EN/ES

Ao modificar conteúdo em qualquer página PT:
1. Verifique se há página correspondente em `/en/` e `/es/`
2. Aplique a mesma modificação nas 3 versões
3. Mantenha os `hreflang` apontando para URLs corretas

## Checklist antes do commit

- [ ] Imagens novas têm versão `.webp`
- [ ] Páginas novas têm hreflang PT/EN/ES
- [ ] Páginas novas estão no sitemap.xml
- [ ] CSS novo está em arquivo externo (não inline)
- [ ] `version.json` atualizado se foi mudança de conteúdo
