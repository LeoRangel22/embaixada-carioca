# Contribuindo com o site Embaixada Carioca

Este documento descreve o processo atual de manutenção. Para o estado operacional do ambiente publicado, consulte [docs/current-site-status.md](docs/current-site-status.md).

## Princípios

- `master` é a branch ligada à produção no Cloudflare Pages.
- Mudanças devem ser pequenas, revisáveis e verificadas no site publicado.
- Conteúdo factual não pode ser inventado ou alterado por substituições automáticas.
- Scripts mutantes são ferramentas manuais, não uma camada de otimização contínua.
- Os 30 workflows legados desativados devem permanecer desativados até decisão explícita.
- Nunca use `git add .` sem verificar o status; adicione apenas os arquivos do lote.

## Estrutura do projeto

```text
/
├── *.html                  páginas em português
├── en/                     páginas em inglês
├── es/                     páginas em espanhol
├── assets/                 CSS, JavaScript, imagens e fontes
├── src/partials/           componentes reutilizáveis por idioma
├── scripts/                validadores e ferramentas manuais
├── _audit_reports/         relatórios datados
├── docs/                   documentação operacional
├── .github/workflows/      workflows ativos e legados desativados
├── sw.js                   service worker
├── _headers                cabeçalhos aplicados pelo Cloudflare Pages
├── _redirects              regras de redirecionamento
└── sitemap.xml             URLs canônicas
```

## Fluxo recomendado

1. Atualize a branch local a partir de `origin/master`.
2. Faça a alteração no menor conjunto possível de arquivos.
3. Revise o diff, incluindo conteúdo multilíngue e dados estruturados.
4. Rode as validações proporcionais ao risco.
5. Faça commit descritivo e push para `master`.
6. Aguarde o Cloudflare Pages publicar e confirme o domínio canônico.
7. Verifique os workflows ativos no GitHub Actions.

## Adicionar ou alterar páginas

Ao criar ou alterar uma página comercial:

1. Defina uma intenção de busca canônica e evite canibalização.
2. Atualize `title`, description, canonical, Open Graph e Twitter.
3. Mantenha equivalentes em PT/EN/ES quando a rota fizer parte do conjunto multilíngue.
4. Confira os quatro hreflangs: `pt-BR`, `en`, `es` e `x-default`.
5. Atualize `sitemap.xml` somente se a URL canônica mudou ou foi criada.
6. Preserve o JSON-LD seguro.

## Dados estruturados

É proibido adicionar ao JSON-LD sem nova decisão de conformidade:

- `Review`
- `Rating`
- `AggregateRating`
- `review`
- `reviewRating`
- `aggregateRating`
- contagens ou notas de avaliações

Validações obrigatórias após mudanças em HTML ou schema:

```bash
python scripts/schema_rating_guard.py --check
python scripts/schema_jsonld_duplicate_key_guard.py --check
```

## Idiomas e hreflang

```bash
python scripts/audit_hreflang_pt_en_es.py
python scripts/validate_i18n_sync.py
```

O validador confirma a existência das contrapartes. Diferenças editoriais advisory ainda exigem revisão humana: não traduza por substituição palavra a palavra e não publique portunhol.

## CSS, JavaScript e imagens

- Prefira arquivos compartilhados já existentes em `assets/`.
- Não acrescente novos “locks” globais para corrigir um caso isolado.
- CSS visual de alto impacto exige QA desktop e mobile.
- Atualize a versão do service worker quando a mudança precisar invalidar cache.
- Use WebP/AVIF e dimensões responsivas sem prejudicar a foto original.
- Legendagem de fotos deve corresponder ao prato real do cardápio.

## Workflows ativos

Somente estes sete permanecem ativos:

| Workflow | Papel |
|---|---|
| Pages build and deployment | publicação secundária de segurança no GitHub Pages |
| Verify live site | verificação do domínio publicado |
| Super site standards SEO audit | auditoria SEO somente de leitura |
| Schema JSON-LD CI gate | proteção dos dados estruturados |
| Accessibility CI | validação de acessibilidade |
| Hreflang Validation | validação multilíngue |
| i18n Sync Validation | paridade estrutural PT/EN/ES |

O Cloudflare Pages é a hospedagem pública principal. O workflow nativo do GitHub Pages foi mantido por decisão do responsável, mas não é o destino canônico do DNS.

## Scripts mutantes

Arquivos com prefixos `apply_*`, `fix_*` ou `enforce_*` podem modificar muitas páginas. Antes de executá-los:

1. leia o código;
2. confirme o escopo;
3. faça snapshot do status;
4. rode em uma branch ou lote isolado;
5. revise o diff completo;
6. valide visual, idiomas, schema e links;
7. publique somente o resultado aprovado.

## Fatos que exigem consistência

- Google: 4,8 estrelas e 8.847 avaliações.
- Instagram: 84 mil seguidores.
- Único restaurante do Parque Bondinho com vista direta para o Pão de Açúcar.
- Melhor Feijoada do Brasil: Prazeres da Mesa, 2017.
- Melhor Feijoada do Rio: Veja Rio Comer & Beber, 2025/2026.
- A feijoada é da Academia da Cachaça e é servida na Embaixada Carioca por parceria formal.
