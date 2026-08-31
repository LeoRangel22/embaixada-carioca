# Embaixada Carioca — site oficial

Site multilíngue do restaurante Embaixada Carioca, no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar.

**Domínio canônico:** `https://www.embaixadacarioca.com/`

**Branch de produção:** `master`

**Hospedagem pública principal:** Cloudflare Pages (plano Free)

**Última revisão deste documento:** 31/08/2026

## Estado atual

- Publicação principal no Cloudflare Pages, ligada ao repositório GitHub.
- `www.embaixadacarioca.com` aponta para `embaixada-carioca.pages.dev`.
- HTTP, domínio sem `www`, `.com.br`, aliases sem `.html` e `index.html` usam redirecionamentos permanentes para as URLs canônicas.
- HSTS ativo em implantação gradual, atualmente com `max-age=86400`.
- CSP e demais cabeçalhos de segurança são entregues pelo Cloudflare.
- `sitemap.xml` contém 97 URLs canônicas.
- Conteúdo em português, inglês e espanhol, com hreflang validado.
- JSON-LD protegido contra `Review`, `Rating`, `AggregateRating` e chaves duplicadas indevidas.
- Sete workflows de validação/publicação permanecem ativos; 30 automações mutantes legadas estão desativadas.

O retrato operacional completo e as pendências atuais estão em [docs/current-site-status.md](docs/current-site-status.md).

## Estrutura principal

```text
*.html                  páginas em português
en/                     páginas em inglês
es/                     páginas em espanhol
assets/                 CSS, JavaScript, imagens e fontes
scripts/                validadores e ferramentas manuais
_audit_reports/         relatórios datados e evidências de execução
.github/workflows/      publicação e gates de validação
_headers                 cabeçalhos aplicados pelo Cloudflare Pages
_redirects               redirecionamentos aplicados no edge
robots.txt               regras para rastreadores
sitemap.xml              mapa canônico do site
```

## Regras de manutenção

1. Trate `master` como fonte de produção.
2. Revise o diff antes de qualquer commit.
3. Não execute scripts `apply_*` em massa sem escopo, revisão humana e validação posterior.
4. Não reative workflows legados sem decisão explícita.
5. Preserve as formulações factuais de prêmios, avaliações, seguidores e parceria institucional.
6. Não adicione `Review`, `Rating` ou `AggregateRating` ao JSON-LD.
7. Ao alterar uma página comercial, conferir a contraparte PT/EN/ES, canonical, hreflang e sitemap.
8. Não reescrever títulos do lote de CTR de 27/08/2026 antes das janelas de medição previstas.

## Validações essenciais

```bash
python scripts/schema_rating_guard.py --check
python scripts/schema_jsonld_duplicate_key_guard.py --check
python scripts/audit_hreflang_pt_en_es.py
python scripts/validate_i18n_sync.py
python scripts/validate_restaurant_search_cluster.py
```

## Fatos editoriais de referência

- Diferencial: único restaurante dentro do Parque Bondinho com vista direta para o Pão de Açúcar.
- Google: 4,8 estrelas e 8.847 avaliações.
- Instagram: 84 mil seguidores.
- Feijoada da Academia da Cachaça: Melhor Feijoada do Brasil pela Prazeres da Mesa em 2017 e Melhor Feijoada do Rio pela Veja Rio Comer & Beber 2025/2026, servida na Embaixada Carioca por parceria formal.

## Contato

- Telefone: +55 21 96683-7556
- E-mail: eventos@embaixadacarioca.com.br
- Endereço: Av. Pasteur, 520 — Urca, Rio de Janeiro
