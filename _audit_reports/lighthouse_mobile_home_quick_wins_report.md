# Lighthouse Mobile Home Quick Wins

Status geral: **PASS**

## Fonte
- `lighthouse mobile 230726.pdf`
- URL auditada: `https://www.embaixadacarioca.com/`
- Scores do relatório: Performance 63, Accessibility 86, Best Practices 100, SEO 100.
- Métricas do relatório: FCP 2.0s, LCP 3.4s, TBT 1.570ms, CLS 0, Speed Index 2.5s.

## Correções aplicadas
- Removidos preconnects não usados no carregamento inicial mobile: Tagme, Google Maps e gstatic maps.
- Adicionado CSS mobile-only para reduzir animações não compostas, melhorar espaçamento de toque e resgatar contraste em grupos citados pelo Lighthouse.
- Padronizada menção de seguidores para 84 mil/84K quando encontrada.
- Verificação preventiva do hero para carregamento eager/high priority.

## Guardrails
- Nenhum JSON-LD foi alterado.
- Nenhuma canonical/hreflang foi alterada.
- Nenhuma copy editorial estratégica foi reescrita além da padronização de seguidores.
- O lote foi criado antes da migração do domínio público. Em 31/08/2026, Cloudflare Pages já aplica `_headers`, CSP, HSTS curto e redirecionamentos de edge.

## Resultado por página

| Página | Existe | Changed | Preconnects removidos | Seguidores | Hero |
|---|---:|---:|---:|---:|---:|
| `index.html` | True | True | 3 | True | False |
| `en/index.html` | True | True | 3 | True | False |
| `es/index.html` | True | True | 3 | True | False |

## Estado atual do edge — 31/08/2026
- `Use efficient cache lifetimes`: continua como oportunidade de medição e ajuste fino para assets estáticos; não é mais limitação de hospedagem.
- CSP e cabeçalhos de segurança: ativos no Cloudflare Pages.
- HSTS: ativo em implantação gradual com `max-age=86400`.
- HTTP, aliases, `index.html` e variantes `.com.br`: redirecionamentos permanentes ativos.
- Compressão adicional de imagens: gerar novos assets WebP/AVIF otimizados e substituir referências após validação visual.
