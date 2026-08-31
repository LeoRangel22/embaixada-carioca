# Scripts — Embaixada Carioca

Automação de manutenção e auditoria do site estático.

---

## Estado operacional — 31/08/2026

Este diretório contém tanto validadores atuais quanto ferramentas históricas que já modificaram o site em massa. A existência de um script não significa que ele esteja autorizado para execução automática.

- Validadores somente de leitura podem rodar nos sete workflows ativos.
- Scripts `apply_*`, `fix_*` e outros mutantes são exclusivamente manuais.
- Trinta workflows legados de correção automática estão desativados por decisão de governança.
- Nenhum fixer deve ser executado sem leitura do código, escopo explícito, revisão completa do diff e validação posterior.
- Traduções, alegações factuais, schema e CSS global exigem revisão humana.
- A documentação operacional atual está em `docs/current-site-status.md`.

### Validadores de referência

| Script | Finalidade atual |
|---|---|
| `schema_rating_guard.py --check` | Impede `Review`, `Rating`, `AggregateRating` e campos derivados no JSON-LD |
| `schema_jsonld_duplicate_key_guard.py --check` | Detecta chaves JSON-LD duplicadas |
| `audit_hreflang_pt_en_es.py` | Audita PT/EN/ES/x-default |
| `validate_i18n_sync.py` | Confere paridade estrutural multilíngue |
| `super_site_standards_seo_audit.py` | Auditoria SEO somente de leitura |
| `validate_restaurant_search_cluster.py` | Valida o cluster restaurante/restaurantes sem reescrever snippets |

---

## Convenção de Nomes

| Prefixo | Finalidade |
|---|---|
| `audit_*.py` | Auditoria/relatório — lê arquivos e imprime análise, não modifica HTML |
| `apply_*.py` | Modifica HTML em massa — aplica correções ou injeções em múltiplas páginas |
| `fix_*.py` | Correção pontual — atua em problemas específicos e delimitados |
| `enforce_*.py` / `schema_*.py` | Validação/proteção de schemas JSON-LD |
| `run_*.py` / `validate_*.py` | Orquestração ou validação pós-deploy |

---

## Inventário de scripts mutantes — execução manual

### CSS / Infraestrutura Visual

| Script | Descrição |
|---|---|
| `update_css_references.py` | Injeta links para `ec-base.css` e `ec-theme.css` em HTMLs que referenciam os CSS "patch" antigos |
| `apply_button_hover_standard.py` | Aplica o padrão de hover/focus de botões em páginas estáticas |
| `apply_legibility_contrast_lock.py` | Força contraste mínimo em seções problemáticas identificadas por auditoria visual |
| `apply_visible_text_css_link.py` | Injeta link para `ec-visible-text-lock.css` nos HTMLs que ainda não o possuem |
| `apply_superholistic_visual_readability_lock.py` | Injeta link para o CSS de legibilidade superholística em todas as páginas |
| `apply_como_chegar_final_visible_lock.py` | Trava de visibilidade final para a página Como Chegar |
| `apply_hero_pao_de_acucar_visual_lock.py` | Trava visual do hero na página Pão de Açúcar |
| `apply_hero_side_frame_final_lock.py` | Trava final do side-frame do hero em páginas de produto |
| `apply_orange_eyebrow_position_fix.py` | Corrige posicionamento do eyebrow laranja no hero |
| `apply_lunch_photos_and_global_readability_hardfix.py` | Adiciona fotos de almoço e aplica correção global de legibilidade |

### Navegação / Header / Footer

| Script | Descrição |
|---|---|
| `apply_top_nav_standardization.py` | Padroniza HTML do nav superior em todas as páginas |
| `apply_top_nav_viewport_fit_v3.py` | Ajusta o nav superior para caber corretamente em qualquer viewport (v3) |
| `apply_top_nav_visual_refinement.py` | Refinamentos visuais finos no nav superior |
| `apply_home_reference_top_nav_lock.py` | Usa a Home como referência para travar o nav superior |
| `apply_home_reference_top_nav_lock_v2.py` | Versão 2 da trava do nav baseada na Home |
| `apply_home_top_exact_replication_audit.py` | Replica exatamente o nav da Home nas demais páginas |
| `apply_lang_dropdown_closed_state_fix.py` | Corrige o estado fechado do dropdown de idioma |
| `apply_nav_language_review_fixes.py` | Correções de revisão no seletor de idioma do nav |
| `apply_subpage_home_header_final_override.py` | Override final do header das subpáginas para igualar à Home |

### SEO / Schema / Structured Data

| Script | Descrição |
|---|---|
| `apply_p0_schema_jsonld.py` | Injeta schemas JSON-LD prioritários (P0) |
| `apply_p1_aio_schema_meta.py` | Injeta schemas AIO e meta tags de prioridade P1 |
| `apply_static_product_schema_faq.py` | Adiciona schema de Produto e FAQ em páginas estáticas |
| `apply_static_schema_product_full_coverage.py` | Cobertura completa de schema de Produto em todo o site |
| `apply_hreflang_pt_en_es.py` | Insere/atualiza atributos hreflang PT/EN/ES em todas as páginas |
| `apply_gsc_ctr_optimization.py` | Otimizações de CTR baseadas em dados do Google Search Console |
| `apply_gsc_structured_data_issues_fix.py` | Corrige problemas de dados estruturados detectados no GSC |
| `apply_gsc_emergency_validation_cleaner.py` | Remove dados estruturados inválidos detectados em validação emergencial |
| `enforce_jsonld_rating_safety.py` | Garante que ratings em JSON-LD estejam dentro dos limites seguros |
| `schema_jsonld_duplicate_key_guard.py` | Remove chaves duplicadas em blocos JSON-LD |
| `schema_rating_guard.py` | Protege valores de rating contra sobrescrita indevida |
| `validate_gsc_postfix_structured_data.py` | Valida dados estruturados após aplicação de fixes do GSC |

### Conteúdo / Qualidade Editorial

| Script | Descrição |
|---|---|
| `apply_aaa_editorial_fixes.py` | Correções editoriais para atingir nível AAA de qualidade de conteúdo |
| `apply_aaa_readability_emergency_fix.py` | Fix emergencial de legibilidade para páginas abaixo do limiar AAA |
| `apply_aaa_site_fixes.py` | Correções gerais de qualidade AAA em todo o site |
| `apply_aio_low_score_editorial_fixes.py` | Correções editoriais em páginas com score AIO baixo |
| `apply_brand_manual_alignment.py` | Alinha textos e elementos visuais ao manual de marca |
| `apply_cardapio_completeness_i18n_fix.py` | Completa o cardápio com traduções faltantes (PT/EN/ES) |
| `apply_dossie_content_enhancer.py` | Enriquece conteúdo do dossiê editorial do restaurante |
| `apply_duplicate_faq_schema_cleaner.py` | Remove schemas FAQ duplicados nas páginas |
| `apply_featured_snippet_ordered_lists.py` | Formata listas ordenadas para otimizar captura de featured snippets |
| `apply_final_86page_aaa_master_audit_v2.py` | Auditoria mestre AAA em 86 páginas (v2, versão atual) |
| `apply_final_aaa_closeout_fixes.py` | Fixes de fechamento da fase de auditoria AAA |
| `apply_final_design_consistency_lock.py` | Trava de consistência de design na camada final |
| `apply_final_geo_direct_answer_fixes.py` | Corrige blocos de resposta direta geolocalizada |
| `apply_final_growth_items.py` | Aplica itens de crescimento final identificados em auditoria |
| `apply_final_quality_repairs.py` | Reparos de qualidade da fase final |
| `apply_geo_cluster_deduplication.py` | Remove clusters geo duplicados nas páginas |
| `apply_home_hero_efficiency_fixes.py` | Melhora eficiência (LCP, CLS) do hero da Home |
| `apply_home_high_intent_95_fixes.py` | Fixes de conversão para páginas de alta intenção (score ≥95) |
| `apply_internal_linking_keyword_cluster_fixes.py` | Corrige e adiciona links internos baseados em clusters de keywords |
| `apply_language_integrity_guard.py` | Garante integridade de idioma (evita mistura PT/EN/ES por acidente) |
| `apply_language_score9_fixes.py` | Fixes para páginas com score de idioma abaixo de 9 |
| `apply_locale_restore_after_repairs.py` | Restaura atributos de locale após reparos que os apagaram |
| `apply_multilingual_continuous_optimization.py` | Otimização contínua do conteúdo multilíngue |
| `apply_parque_bondinho_access_clarity_fix.py` | Melhora clareza das instruções de acesso ao Parque Bondinho |
| `apply_phase2_quick_fixes.py` | Fixes rápidos da fase 2 do projeto |
| `apply_priority_aaa_warn_fixes.py` | Corrige avisos de prioridade AAA gerados por auditoria |
| `apply_priority_query_conversion_fixes.py` | Fixes de conversão para queries de alta prioridade |
| `apply_red_block_copidesk_fixes.py` | Aplica correções de copidesk nos blocos marcados em vermelho |
| `apply_review_snippets_issue_fix.py` | Corrige problemas em snippets de avaliações |
| `apply_rich_results_performance_fixes.py` | Melhora performance dos rich results no Google |
| `apply_scorecard_gap_fixes.py` | Fecha lacunas identificadas no scorecard de qualidade |
| `apply_seo_content_growth_fixes.py` | Adiciona conteúdo SEO para crescimento orgânico |
| `apply_seo_geo_ai_95_polish.py` | Polimento final de SEO/GEO/AI para atingir score 95 |
| `apply_site_integrity_refinements.py` | Refinamentos de integridade geral do site |
| `apply_topic_authority_clusters.py` | Adiciona/aprimora seções de autoridade temática |

### Analytics / Performance

| Script | Descrição |
|---|---|
| `apply_google_analytics_foundation.py` | Injeta base do Google Analytics (GA4) em todas as páginas |
| `apply_google_review_link_fix.py` | Corrige links para avaliações do Google em todas as páginas |
| `apply_design_performance_fixes.py` | Fixes de performance visual (imagens, layout shift) |
| `apply_performance_cache_image_refinements.py` | Adiciona cache hints e refinamentos de imagens para performance |
| `apply_performance_urgent_quick_wins.py` | Aplica ganhos rápidos e urgentes de performance |
| `apply_tracking_and_r2d2_assets.py` | Injeta assets de tracking e componentes R2D2 de conversão |
| `apply_live_visual_postdeploy_fixes.py` | Fixes visuais aplicados após deploy, baseados em inspeção ao vivo |

### Eventos / Páginas Específicas

| Script | Descrição |
|---|---|
| `apply_en_parque_bondinho_scorecard_fix.py` | Corrige scorecard da página EN do Parque Bondinho |
| `apply_event_quote_link_email_fix.py` | Corrige links de cotação e e-mail na página de eventos |
| `apply_sprint123_final_visual_validation.py` | Validação visual final dos sprints 1, 2 e 3 combinados |
| `apply_structural_restaurant_site_audit.py` | Auditoria estrutural completa do site do restaurante |
| `apply_visual_readability_reality_fix_v3.py` | Trava de legibilidade baseada em realidade visual (v3, versão atual) |
| `polish_eventos_page.py` | Polimento final da página de eventos |
| `stabilize_existing_pages_before_landings.py` | Estabiliza páginas existentes antes de criar novas landing pages |

### Auditoria / Relatórios

| Script | Descrição |
|---|---|
| `audit_css_js_refactor_opportunities.py` | Identifica oportunidades de refatoração de CSS e JS |
| `audit_existing_pages_content_structure.py` | Audita estrutura de conteúdo das páginas existentes |
| `audit_geo_cluster_deduplication.py` | Detecta e relata clusters geo duplicados |
| `audit_green_solid_palette.py` | Audita uso da paleta verde sólida no site |
| `audit_gsc_real_queries_score.py` | Calcula score das queries reais do GSC |
| `audit_hreflang_pt_en_es.py` | Audita implementação de hreflang PT/EN/ES |
| `audit_internal_links_and_snippets.py` | Audita links internos e snippets de conteúdo |
| `audit_language_quality_pt_en_es.py` | Avalia qualidade do conteúdo nos três idiomas |
| `audit_multilingual_ai_search_score.py` | Pontua o site para motores de busca AI multilíngue |
| `audit_p0_schema_jsonld.py` | Audita schemas JSON-LD prioritários (P0) |
| `audit_p1_aio_schema_meta.py` | Audita schemas AIO e meta tags de prioridade P1 |
| `audit_phase2_performance_seo.py` | Audita performance e SEO da fase 2 |
| `audit_priority_keywords_aio_score.py` | Pontua keywords prioritárias para score AIO |
| `audit_visual_contrast_risks.py` | Detecta riscos de contraste visual em todas as páginas |
| `holistic_site_audit.py` | Auditoria holística completa do site |
| `super_site_standards_seo_audit.py` | Auditoria de padrões SEO avançados |
| `superholistic_design_ux_seo_geo_audit.py` | Auditoria combinada de design, UX, SEO e GEO |
| `run_super_workflow_score_gate.py` | Executa o fluxo completo de score gate antes de deploy |
| `fix_cardapio_visual_readability_base.py` | Corrige legibilidade base do cardápio (fix pontual) |
| `fix_existing_pages_content_structure.py` | Corrige estrutura de conteúdo em páginas existentes (fix pontual) |

---

## Scripts Arquivados

Scripts obsoletos foram movidos para `scripts/archive/`. São versões antigas substituídas por versões mais recentes, ou scripts de fases/sprints específicos já concluídos que não precisam ser reexecutados.

Ver: [`scripts/archive/`](archive/)
