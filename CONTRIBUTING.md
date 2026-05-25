# Contribuindo com o site Embaixada Carioca

## Estrutura do projeto

```
/
├── *.html                  # Páginas em português (raiz)
├── en/                     # Páginas em inglês
├── es/                     # Páginas em espanhol
├── assets/
│   ├── css/
│   │   ├── ec-shared.css           # CSS compartilhado (extraído de inline, 87 páginas)
│   │   └── ec-stabilization-base.css  # CSS base + paleta + contraste
│   ├── ec-bundle.js        # Scripts principais (UI, analytics, schema)
│   ├── geo-proximity.js    # Geolocalização (páginas selecionadas)
│   └── *.webp / *.jpg      # Imagens
├── src/partials/           # Partials reutilizáveis (nav, footer)
│   ├── pt/nav.html         # Nav em português
│   ├── pt/footer.html      # Footer em português
│   ├── en/nav.html
│   ├── en/footer.html
│   ├── es/nav.html
│   └── es/footer.html
├── scripts/                # Scripts ativos de manutenção
│   ├── apply_partials.py   # Aplica nav/footer a todas as páginas
│   ├── validate_lang_sync.py  # Valida sincronização PT/EN/ES
│   └── ...
├── .github/workflows/      # 10 workflows ativos (CI/CD)
├── sw.js                   # Service Worker (cache + offline fallback)
└── _headers                # CSP e headers de segurança (Cloudflare/Netlify)
```

---

## Como fazer mudanças no nav ou footer

Edite o partial → rode o script → revise o diff → commit.

```bash
# 1. Editar o nav em português
nano src/partials/pt/nav.html

# 2. Aplicar a todos os arquivos HTML
python3 scripts/apply_partials.py --partial nav

# 3. Verificar mudanças
git diff --stat

# 4. Commitar
git add -A && git commit -m "Update nav: ..."
```

Para footer: mesma sequência com `--partial footer`.
Para ambos: `python3 scripts/apply_partials.py` (sem `--partial`).

---

## Como adicionar uma nova página

1. Copie a página mais próxima como base (ex: `cp morro-da-urca.html nova-pagina.html`).
2. Edite title, meta description, canonical URL, hreflang e conteúdo.
3. Se a página tiver equivalente em EN/ES, crie `en/nova-pagina.html` e `es/nova-pagina.html`.
4. Adicione a URL no `sitemap.xml`.
5. Rode o validador de sync:

```bash
python3 scripts/validate_lang_sync.py
```

---

## Como manter PT/EN/ES em sincronia

```bash
# Verificar quais páginas estão faltando nos outros idiomas
python3 scripts/validate_lang_sync.py

# Gerar relatório CSV
python3 scripts/validate_lang_sync.py --fix-report
```

O script detecta:
- Páginas PT sem equivalente EN ou ES
- Páginas EN/ES sem equivalente PT (órfãs)
- Hreflang apontando para URLs inexistentes
- Páginas sem `<title>` ou meta description

---

## Como atualizar o CSS

- **CSS compartilhado** (afeta todas as páginas): edite `assets/css/ec-shared.css`
- **CSS base/paleta/contraste**: edite `assets/css/ec-stabilization-base.css`
- Não criar novos arquivos CSS avulsos — consolidar no arquivo existente

---

## Como atualizar o JavaScript

- **Funcionalidades de UI/analytics/schema**: edite `assets/ec-bundle.js`
- **Geolocalização**: edite `assets/geo-proximity.js`
- **Service Worker** (cache/offline): edite `sw.js` e atualize `CACHE_VERSION`

---

## Scripts ativos

| Script | Propósito | Quando usar |
|--------|-----------|-------------|
| `apply_partials.py` | Aplica nav/footer a todas as páginas | Ao mudar nav ou footer |
| `validate_lang_sync.py` | Checa sync PT/EN/ES | Ao adicionar/remover páginas |
| `apply_hreflang_pt_en_es.py` | Aplica hreflang correto | Via workflow p0-hreflang |
| `schema_rating_guard.py` | Valida schema JSON-LD | Via workflow schema-rating-guard |
| `super_site_standards_seo_audit.py` | Auditoria SEO completa | Via workflow super-site-standards |

Scripts obsoletos estão em `scripts/archive/` — não usar.

---

## Workflows ativos (GitHub Actions)

| Workflow | Trigger | Função |
|----------|---------|--------|
| `verify-live-site.yml` | push + schedule | Confirma que o deploy chegou ao site live |
| `super-site-standards-seo-audit.yml` | push | Auditoria SEO e qualidade |
| `schema-rating-guard.yml` | manual | Valida schema JSON-LD |
| `schema-jsonld-duplicate-key-guard.yml` | manual | Detecta chaves duplicadas no schema |
| `p0-hreflang-pt-en-es.yml` | manual | Aplica/audita hreflang multilíngue |
| `p0-schema-jsonld.yml` | manual | Aplica/audita schema JSON-LD |
| `multilingual-continuous-optimization.yml` | manual | Otimização multilíngue |
| `phase2-performance-seo-audit.yml` | push | Auditoria de performance |
| `repo-hygiene.yml` | manual | Limpeza de arquivos legados |
| `super-workflow-score-gate.yml` | manual | Gate de qualidade geral |

---

## Deploy

O site é hospedado no GitHub Pages e faz deploy automaticamente a cada push em `master`.

**Headers de segurança** (CSP, X-Frame-Options, etc.) só funcionam se o site estiver servido por **Cloudflare Pages** ou **Netlify** — o GitHub Pages ignora o arquivo `_headers`.

---

## Convenções

- Imagens: sempre em `.webp` com fallback `.jpg`. Adicionar `srcset` quando variantes responsivas existirem.
- HTML: não adicionar `<style>` blocks inline grandes — CSS vai em `ec-shared.css`.
- JavaScript: não criar arquivos JS avulsos — funcionalidades vão em `ec-bundle.js`.
- Commits: mensagem descritiva em inglês, uma linha de 50-72 chars + detalhes se necessário.
