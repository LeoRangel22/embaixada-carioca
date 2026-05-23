# Arquitetura de Partials — Embaixada Carioca

## Objetivo

Reduzir retrabalho, duplicação e risco de erro em páginas HTML estáticas.

O site deve migrar gradualmente de edições diretas em dezenas de HTMLs para um sistema simples de geração com partials compartilhados.

## Problemas atuais

- Vários scripts Python fazem correções pontuais em HTML já gerado.
- Header, navegação, head, SEO, schema, hreflang e footer ficam repetidos em muitas páginas.
- Pequenos erros de tradução ou marcação se propagam para várias URLs.
- Scripts `fix_*` de uso único dificultam saber o que ainda é fonte de verdade.

## Modelo recomendado

```text
/src
  /pages
    index.pt.json
    index.en.json
    index.es.json
    almoco.pt.json
    almoco.en.json
    almoco.es.json
  /partials
    head.html
    header.html
    nav.html
    footer.html
    schema.json.j2
    hreflang.html.j2
  /templates
    base.html.j2
    landing.html.j2
    geo.html.j2
/scripts
  build_site.py
  audit_site.py
  apply_p0_schema_jsonld.py
  audit_p0_schema_jsonld.py
```

## Regras de ouro

1. Nenhuma correção estrutural deve ser feita manualmente em 15 páginas.
2. Toda mudança feita em português deve ter equivalente em inglês e espanhol quando houver página correspondente.
3. Schema JSON-LD não pode conter `aggregateRating` quando a nota vier do Google Reviews.
4. Hreflang deve ser gerado a partir de grupos canônicos PT/EN/ES.
5. Scripts temporários devem ser arquivados ou removidos após uso.

## Ordem de migração

### Fase 1 — Estabilização

- Manter os HTMLs atuais.
- Criar scripts de aplicação/auditoria seguros.
- Documentar scripts ativos.
- Bloquear rating no schema.

### Fase 2 — Partials mínimos

- Extrair `head`, `header/nav`, `footer` e `schema`.
- Criar gerador estático simples em Python.
- Rodar build local ou via GitHub Actions.

### Fase 3 — Conteúdo por idioma

- Mover títulos, metas, FAQs e blocos GEO para arquivos estruturados PT/EN/ES.
- Reduzir scripts `fix_*`.
- Auditar similaridade e traduções por idioma.

## Critério de pronto

- `application/ld+json` presente nas páginas prioritárias.
- `aggregateRating` ausente do JSON-LD.
- Hreflang PT/EN/ES/x-default presente.
- Nenhum bloco genérico duplicado no cluster GEO.
- Scripts ativos documentados.
- Scripts obsoletos identificados.
