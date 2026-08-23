# Revisão editorial PT/EN/ES — lote 2

Data: 2026-08-23

## Status geral

**PASS — equivalência editorial e comercial revisada nas oito famílias deste lote.**

O critério aplicado foi equivalência semântica, factual e de conversão. Não foram copiadas seções redundantes apenas para igualar a quantidade de títulos entre os idiomas.

## Famílias revisadas

| Família | Correções principais | Resultado |
|---|---|---|
| `almoco-morro-da-urca.html` | Hero EN/ES, resumo, vista, navegação, perguntas práticas e termos de acesso | PASS |
| `almoco.html` | Nomes e descrições de pratos, unidades, galeria, CTAs, resumo do hero e prêmio em EN/ES | PASS |
| `eventos.html` | Resumos EN/ES, WhatsApp e FAQ comercial em inglês, incluindo acesso, horários e personalização | PASS |
| `index.html` | Resíduos de idioma em ES e formulação defensável do diferencial de vista direta ao Pan de Azúcar | PASS |
| `morro-da-urca.html` | Alegação de exclusividade corrigida; conteúdo ES reescrito em espanhol natural; acesso, horários e comparação factual | PASS |
| `parque-bondinho.html` | Horários coerentes; termos ES; seção de planejamento e regra de ingresso/trilha espelhada semanticamente | PASS |
| `restaurante-com-vista-rio-de-janeiro.html` | Bloco legado de almoço localizado em EN/ES; pratos, prêmio, galeria, CTA e mensagens comerciais | PASS |
| `sunset-por-do-sol-rio-de-janeiro.html` | Bloco legado de almoço localizado em EN/ES e alinhado ao conteúdo de atardecer | PASS |

## Regras factuais preservadas

- Embaixada Carioca é apresentada como o único restaurante **dentro do Parque Bondinho com vista direta e frontal para o Pão de Açúcar**.
- O acesso usual é pelo Parque Bondinho, com ingresso do teleférico.
- A trilha do Morro da Urca é alternativa quando estiver aberta e autorizada.
- Quem chega pela trilha e permanece no Morro da Urca não precisa comprar ingresso apenas para visitar a Embaixada Carioca.
- O ingresso é necessário para usar o teleférico, continuar ao Pão de Açúcar ou descer à Praia Vermelha de teleférico.
- Café da manhã: 8:30–11:30. Almoço e feijoada: a partir de 11:30. Restaurante: 8:30–21:00.
- Prêmio padronizado como Melhor Feijoada do Rio de Janeiro — Veja Rio Comer & Beber 2025/2026, em colaboração com Academia da Cachaça.

## Validações

| Validação | Resultado |
|---|---:|
| Páginas PT sem equivalente EN | 0 |
| Páginas PT sem equivalente ES | 0 |
| JSON-LD com chaves duplicadas | 0 — PASS |
| `Review`, `Rating` ou `AggregateRating` indevido | 0 — PASS |
| Validação GSC pós-correção | PASS |
| Auditoria mestre V2 | 81 PASS, 17 WARN, média 9,8/10 |

## Observação sobre os 12 avisos de headings

O validador de sincronização continua sinalizando 12 diferenças numéricas de `h1+h2`. Esses avisos são diagnósticos de estrutura, não ausência de páginas, hreflang quebrado ou falha de tradução. As diferenças remanescentes decorrem principalmente de blocos SEO redundantes em PT e de seções editoriais internacionais específicas. Duplicar títulos para zerar a contagem reduziria a qualidade e poderia aumentar canibalização ou conteúdo repetitivo.

## Pendências fora do escopo deste lote

Os 17 avisos da auditoria mestre são majoritariamente locks visuais/contraste, páginas de avaliações, eventos corporativos e a página autônoma `feijoada-morro-da-urca.html`. Não representam regressão de JSON-LD nem falta de equivalentes EN/ES neste lote e devem ser tratados em lotes próprios com validação visual.
