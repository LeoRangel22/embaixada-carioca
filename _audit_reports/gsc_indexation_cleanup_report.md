# GSC Indexation Cleanup — 22/08/2026

Status geral: **PASS COM LIMITAÇÃO DE HOSPEDAGEM**

## Fonte de decisão

- Diagnóstico GA4 + Google Search Console de 20/05/2026 a 19/08/2026.
- Verificação HTTP pública realizada em 22/08/2026.
- Auditoria do `sitemap.xml`, canonicals, hreflang e arquivos locais do branch `master`.

## Redirecionamentos verificados ao vivo

| Origem | Resultado atual | Leitura |
|---|---|---|
| `http://www.embaixadacarioca.com/cardapio.html` | `301` para HTTPS | Corrigido no servidor do GitHub Pages |
| `https://embaixadacarioca.com/` | `301` para `https://www.embaixadacarioca.com/` | Corrigido |
| `https://embaixadacarioca.com.br/` | dois redirecionamentos permanentes até `https://www.embaixadacarioca.com/` | Corrigido |
| `https://www.embaixadacarioca.com.br/` | dois redirecionamentos permanentes até `https://www.embaixadacarioca.com/` | Corrigido |
| `/index.html`, `/en/index.html`, `/es/index.html` | `200`, com canonical para as raízes correspondentes | Duplicata consolidada por canonical; sem 301 no GitHub Pages |
| `/cardapio`, `/eventos`, `/feijoada`, `/nossa-visao`, `/contato` | `200`, com canonical para a versão `.html` | Duplicata consolidada por canonical; sem 301 no GitHub Pages |

## Correções aplicadas

- Removidas três entradas duplicadas do sitemap:
  - `en/feijoada.html`;
  - `es/feijoada.html`;
  - `en/restaurant-at-sugarloaf.html`.
- Corrigido o cluster hreflang de `restaurante-com-vista-rio-de-janeiro.html` para apontar à contraparte inglesa existente `en/restaurante-com-vista-rio-de-janeiro.html`.
- Removidos hreflangs EN/ES inexistentes de `feijoada-morro-da-urca.html`; a página permanece PT + `x-default` até haver traduções equivalentes reais.
- Adicionado link editorial visível de `feijoada.html` para `feijoada-morro-da-urca.html`, eliminando a condição de página órfã.
- Atualizados `lastmod` somente nas páginas cuja indexação/hreflang foi materialmente corrigida.

## Estado final do sitemap

- Entradas: **98**.
- URLs únicas: **98**.
- Duplicidades: **0**.
- URLs sem arquivo correspondente no repositório: **0**.
- Arquivos `.webp` tratados como páginas no sitemap principal: **0**.
- Páginas `noindex` dentro do sitemap principal: **0**.

## Limitação conhecida

O GitHub Pages não oferece regras arbitrárias de redirecionamento por caminho. Por isso, aliases sem `.html` e os três `index.html` continuam respondendo `200`, embora os canonicals estejam corretos. Para transformá-los em `301` reais e adicionar cabeçalhos personalizados como HSTS controlado, a solução é colocar o domínio principal atrás de uma camada de edge com regras de redirecionamento, como Cloudflare, ou migrar a publicação para uma plataforma que aplique redirects de servidor.

## Próxima ação no Search Console

1. Reenviar `https://www.embaixadacarioca.com/sitemap.xml`.
2. Solicitar indexação de `https://www.embaixadacarioca.com/feijoada-morro-da-urca.html`.
3. Não solicitar indexação de `/index.html` ou dos aliases sem `.html`; o destino desejado é a URL canônica.
4. Medir novamente cobertura e CTR após o recrawl, sem reescrever as palavras-ouro antes de completar 28 dias da aplicação de 11/08/2026.
