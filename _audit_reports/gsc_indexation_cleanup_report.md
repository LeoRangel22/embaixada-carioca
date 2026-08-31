# GSC Indexation Cleanup

**Auditoria original:** 22/08/2026

**Atualização operacional:** 31/08/2026

**Status geral:** PASS — limitação de edge resolvida

## Fonte de decisão

- Diagnósticos GA4 e Google Search Console.
- Verificação HTTP pública em 31/08/2026.
- Auditoria do `sitemap.xml`, canonicals, hreflang e branch `master`.

## Redirecionamentos verificados ao vivo

| Origem | Resultado atual | Leitura |
|---|---|---|
| `http://www.embaixadacarioca.com/cardapio.html` | `301` para HTTPS | Corrigido no Cloudflare |
| `https://embaixadacarioca.com/` | `301` para `https://www.embaixadacarioca.com/` | Corrigido |
| `https://embaixadacarioca.com.br/` | `301` para o domínio `.com` canônico | Corrigido |
| `https://www.embaixadacarioca.com.br/` | `301` para o domínio `.com` canônico | Corrigido |
| `/index.html` | `301` para `/` | Corrigido |
| `/cardapio`, `/eventos` e aliases equivalentes | `301` para a versão canônica `.html` | Corrigido |

As limitações descritas no relatório original pertenciam ao período em que o site dependia do comportamento padrão do GitHub Pages. O domínio público agora é servido pelo Cloudflare Pages, que aplica as regras de edge.

## Correções de indexação preservadas

- Entradas duplicadas removidas do sitemap.
- Hreflang corrigido para contrapartes existentes.
- Páginas sem tradução real não apontam para arquivos inexistentes.
- `feijoada-morro-da-urca.html` possui link editorial e não está órfã.
- Aliases e `index.html` consolidam por `301`, além das canonicals.

## Estado atual do sitemap

- Entradas canônicas: **97**.
- Duplicidades conhecidas: **0**.
- Arquivos de imagem tratados como páginas: **0**.
- Páginas `noindex` no sitemap principal: **0**.
- Sitemap reenviado ao Search Console em 27/08/2026 e processado com 97 páginas.

## Segurança e protocolo

- HTTP → HTTPS: `301`.
- HSTS: ativo em implantação gradual com `max-age=86400`.
- Cabeçalhos de segurança: entregues pelo Cloudflare.

## Próxima ação no Search Console

1. Monitorar o recrawl das URLs canônicas.
2. Não solicitar indexação de `/index.html`, aliases sem `.html` ou variantes `.com.br`.
3. Solicitar indexação apenas de páginas canônicas novas ou materialmente alteradas.
4. Comparar cobertura e CTR depois das janelas de 14 e 28 dias dos lotes de 27/08/2026.
5. Não reenviar o sitemap repetidamente quando não houver alteração material.
