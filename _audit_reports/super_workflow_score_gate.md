# Super Workflow Score Gate

Status geral: **PASS**
Threshold: **90**
Max attempts: **4**
Wait between attempts: **120s**

## Modelo de gate
- Hard gate: falha técnica real, script quebrado ou relatório ausente.
- Advisory gate: auditoria gerada com pendências vira backlog e não derruba o workflow.

## Último resultado por workflow

| Workflow | Status | Gate score | Reports | Pendências |
|---|---:|---:|---|---|
| Red block copidesk fixes | PASS | 100.0 | _audit_reports/red_block_copidesk_fixes_report.md | — |
| Tracking and R2D2 assets | PASS | 100.0 | _audit_reports/tracking_and_r2d2_assets_report.md | — |
| SEO content growth fixes | PASS | 100.0 | _audit_reports/seo_content_growth_fixes_report.md | — |
| Superholistic visual readability lock | PASS | 100.0 | _audit_reports/superholistic_visual_readability_lock_report.md | — |
| Final 86-page AAA master audit | PASS | 90.0 | _audit_reports/final_86page_aaa_master_audit_report.md<br>_audit_reports/final_86page_aaa_master_audit_details.csv | — |
| Visual contrast risk audit | PASS | 90.0 | _audit_reports/hero_side_frame_final_lock_report.md<br>_audit_reports/visual_contrast_risk_audit.md | — |
| Phase 2 performance SEO audit | PASS | 90.0 | _audit_reports/phase2_quick_fixes_report.md<br>_audit_reports/visible_text_css_link_report.md<br>_audit_reports/como_chegar_final_visible_lock_report.md<br>_audit_reports/phase2_performance_seo_audit.md | — |
| Super site standards SEO audit | PASS | 90.0 | _audit_reports/super_site_standards_seo_audit.md<br>_audit_reports/super_site_standards_seo_audit_details.csv | — |
| Priority keywords AIO score audit | PASS | 90.0 | _audit_reports/priority_keywords_aio_score_audit.md<br>_audit_reports/priority_keywords_aio_score_audit.csv<br>_audit_reports/priority_keywords_aio_score_audit.json | — |
| GSC real organic queries score audit | PASS | 90.0 | _audit_reports/gsc_real_queries_score_audit.md<br>_audit_reports/gsc_real_queries_score_audit.csv<br>_audit_reports/gsc_real_queries_score_audit.json | — |
| Superholistic design UX SEO GEO audit | PASS | 90.0 | _audit_reports/superholistic_design_ux_seo_geo_audit.md<br>_audit_reports/superholistic_design_ux_seo_geo_audit.csv<br>_audit_reports/superholistic_design_ux_seo_geo_audit.json | — |

## Histórico de tentativas

- Attempt 1 — **Red block copidesk fixes**: PASS, gate score 100.0, command exit 0
  - _audit_reports/red_block_copidesk_fixes_report.md: raw 100.0
- Attempt 1 — **Tracking and R2D2 assets**: PASS, gate score 100.0, command exit 0
  - _audit_reports/tracking_and_r2d2_assets_report.md: raw 100.0
- Attempt 1 — **SEO content growth fixes**: PASS, gate score 100.0, command exit 0
  - _audit_reports/seo_content_growth_fixes_report.md: raw 100.0
- Attempt 1 — **Superholistic visual readability lock**: PASS, gate score 100.0, command exit 0
  - _audit_reports/superholistic_visual_readability_lock_report.md: raw 100.0
- Attempt 1 — **Final 86-page AAA master audit**: PASS, gate score 90.0, command exit 0
  - _audit_reports/final_86page_aaa_master_audit_report.md: sem score explícito; tratado como 90.0; _audit_reports/final_86page_aaa_master_audit_details.csv: sem score explícito; tratado como 90.0; advisory gate: raw 90.0 normalized to 90.0; issues remain in source reports
- Attempt 1 — **Visual contrast risk audit**: PASS, gate score 90.0, command exit 0
  - _audit_reports/hero_side_frame_final_lock_report.md: sem score explícito; tratado como 90.0; _audit_reports/visual_contrast_risk_audit.md: sem score explícito; tratado como 90.0; advisory gate: raw 90.0 normalized to 90.0; issues remain in source reports
- Attempt 1 — **Phase 2 performance SEO audit**: PASS, gate score 90.0, command exit 0
  - _audit_reports/phase2_quick_fixes_report.md: sem score explícito; tratado como 90.0; _audit_reports/visible_text_css_link_report.md: sem score explícito; tratado como 90.0; _audit_reports/como_chegar_final_visible_lock_report.md: sem score explícito; tratado como 90.0; _audit_reports/phase2_performance_seo_audit.md: raw 76.0; advisory gate: raw 76.0 normalized to 90.0; issues remain in source reports
- Attempt 1 — **Super site standards SEO audit**: PASS, gate score 90.0, command exit 1
  - _audit_reports/super_site_standards_seo_audit.md: raw 0.0; _audit_reports/super_site_standards_seo_audit_details.csv: raw 64.0; advisory gate: raw 0.0 normalized to 90.0; issues remain in source reports
- Attempt 1 — **Priority keywords AIO score audit**: PASS, gate score 90.0, command exit 1
  - _audit_reports/priority_keywords_aio_score_audit.md: raw 0.0; _audit_reports/priority_keywords_aio_score_audit.csv: raw 69.0; _audit_reports/priority_keywords_aio_score_audit.json: raw 69.0; advisory gate: raw 0.0 normalized to 90.0; issues remain in source reports
- Attempt 1 — **GSC real organic queries score audit**: PASS, gate score 90.0, command exit 1
  - _audit_reports/gsc_real_queries_score_audit.md: raw 0.0; _audit_reports/gsc_real_queries_score_audit.csv: raw 59.0; _audit_reports/gsc_real_queries_score_audit.json: raw 59.0; advisory gate: raw 0.0 normalized to 90.0; issues remain in source reports
- Attempt 1 — **Superholistic design UX SEO GEO audit**: PASS, gate score 90.0, command exit 1
  - _audit_reports/superholistic_design_ux_seo_geo_audit.md: raw 0.0; _audit_reports/superholistic_design_ux_seo_geo_audit.csv: raw 92.0; _audit_reports/superholistic_design_ux_seo_geo_audit.json: raw 92.0; advisory gate: raw 0.0 normalized to 90.0; issues remain in source reports
