#!/usr/bin/env python3
from pathlib import Path
import csv, re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / '_audit_reports'
REPORT_MD = REPORT_DIR / 'brand_manual_alignment_report.md'
REPORT_CSV = REPORT_DIR / 'brand_manual_alignment_details.csv'
SKIP = {'404.html', 'offline.html', 'home-preview.html'}

START = '<!-- EC Brand Manual Alignment -->'
END = '<!-- /EC Brand Manual Alignment -->'
BLOCK_RE = re.compile(r'\n*<!-- EC Brand Manual Alignment -->[\s\S]*?<!-- /EC Brand Manual Alignment -->\s*', re.I)
HEAD_RE = re.compile(r'</head>', re.I)

CSS = START + r'''
<style id="ec-brand-manual-alignment">
/* Embaixada Carioca — alinhamento ao Manual da Marca V02
   Paleta oficial: Azul 1 #00405a; Azul 2 #527f8f; Verde #335d4a; Amarelo #f59b1e;
   Areia #ede2c9; Verde 2 #cbded4; Cinzas #485156/#7d8386/#b1b7bc.
   Tipografia oficial: Catamaran + Verdana/sistema.
*/
:root{--ec-azul1:#00405a;--ec-azul2:#527f8f;--ec-verde:#335d4a;--ec-amarelo:#f59b1e;--ec-areia:#ede2c9;--ec-verde2:#cbded4;--ec-cinza1:#485156;--ec-cinza2:#7d8386;--ec-cinza3:#b1b7bc;--azul1:#00405a;--azul2:#527f8f;--verde:#335d4a;--amarelo:#f59b1e;--areia:#ede2c9;--areia-pale:#ede2c9;--verde2:#cbded4;--cinza1:#485156;--cinza2:#7d8386;--cinza3:#b1b7bc;}
html,body{font-family:Catamaran,Verdana,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;background:var(--ec-azul1)!important;color:var(--ec-areia)!important;}
body{color-scheme:dark;}

/* Logo: principal preservada, sem distorção, com contraste adequado em foto/fundo escuro */
.brand-logo,.hero-logo,img[src*="logo"]{object-fit:contain!important;height:auto;max-width:100%;filter:none;}
nav.top .brand-mark{padding:10px 12px!important;min-width:calc(68px + 24px)!important;min-height:calc(68px + 20px)!important;}
nav.top .brand-logo{width:68px!important;height:68px!important;min-width:68px!important;min-height:68px!important;}
@media(max-width:960px){nav.top .brand-mark{padding:8px 10px!important;min-width:64px!important;min-height:64px!important;}nav.top .brand-logo{width:54px!important;height:54px!important;min-width:54px!important;min-height:54px!important;}}

/* Navegação — paleta oficial e legibilidade */
nav.top:not(.scrolled){background:linear-gradient(180deg,rgba(0,64,90,.52) 0%,rgba(0,64,90,.28) 58%,rgba(0,64,90,0) 100%)!important;}
nav.top:not(.scrolled) .nav-links a{font-family:Catamaran,Verdana,system-ui,sans-serif!important;color:var(--ec-areia)!important;-webkit-text-fill-color:var(--ec-areia)!important;font-weight:800!important;letter-spacing:.145em!important;text-shadow:0 2px 10px rgba(0,64,90,.78)!important;}
nav.top.scrolled,nav.top.nav-scrolled,body.scrolled nav.top{background:rgba(237,226,201,.96)!important;border-bottom:1px solid rgba(0,64,90,.16)!important;box-shadow:0 12px 34px rgba(0,64,90,.12)!important;}
nav.top.scrolled .nav-links a,nav.top.nav-scrolled .nav-links a,body.scrolled nav.top .nav-links a{color:var(--ec-azul1)!important;-webkit-text-fill-color:var(--ec-azul1)!important;text-shadow:none!important;}
nav.top.scrolled .brand-logo.light,nav.top.nav-scrolled .brand-logo.light,body.scrolled nav.top .brand-logo.light{display:none!important;}
nav.top.scrolled .brand-logo.dark,nav.top.nav-scrolled .brand-logo.dark,body.scrolled nav.top .brand-logo.dark{display:block!important;}

/* Badges, idioma e chips com cores oficiais */
.nav-rating-badge,.lang-current,header.hero .hero-chips span,header.hero .hero-chips a,header.page-hero .hero-chips span,header.page-hero .hero-chips a{background:rgba(0,64,90,.58)!important;border:1px solid rgba(237,226,201,.34)!important;color:var(--ec-areia)!important;-webkit-text-fill-color:var(--ec-areia)!important;box-shadow:0 8px 22px rgba(0,64,90,.18)!important;}
nav.top.scrolled .nav-rating-badge,nav.top.scrolled .lang-current,nav.top.nav-scrolled .nav-rating-badge,nav.top.nav-scrolled .lang-current,body.scrolled nav.top .nav-rating-badge,body.scrolled nav.top .lang-current{background:rgba(255,255,255,.54)!important;border-color:rgba(0,64,90,.22)!important;color:var(--ec-azul1)!important;-webkit-text-fill-color:var(--ec-azul1)!important;}
.gr-stars{color:var(--ec-amarelo)!important;-webkit-text-fill-color:var(--ec-amarelo)!important;}

/* Títulos e corpo — Catamaran/Verdana e contraste dentro da paleta */
h1,h2,h3,h4,h5,h6{font-family:Catamaran,Verdana,system-ui,sans-serif!important;color:var(--ec-areia)!important;-webkit-text-fill-color:var(--ec-areia)!important;font-weight:600;}
header.hero h1,header.page-hero h1{color:var(--ec-areia)!important;-webkit-text-fill-color:var(--ec-areia)!important;text-shadow:0 3px 18px rgba(0,64,90,.78)!important;}
header.hero h1 em,header.page-hero h1 em,header.hero h1 .serif,header.page-hero h1 .serif{color:var(--ec-amarelo)!important;-webkit-text-fill-color:var(--ec-amarelo)!important;font-style:italic;}
main,.article-body,.article-content,.longform,.story,.guide-content,.rio-guide,.ec-sprint2-geo{font-family:Catamaran,Verdana,system-ui,sans-serif!important;color:rgba(237,226,201,.90)!important;-webkit-text-fill-color:rgba(237,226,201,.90)!important;}
.article-body p,.article-content p,.longform p,.story p,.guide-content p,.rio-guide p,.ec-sprint2-geo p,main .lede,main .copy,main .description{color:rgba(237,226,201,.88)!important;-webkit-text-fill-color:rgba(237,226,201,.88)!important;line-height:1.72;}
.article-body strong,.article-content strong,.longform strong,.story strong,.guide-content strong,.rio-guide strong,main strong{color:var(--ec-amarelo)!important;-webkit-text-fill-color:var(--ec-amarelo)!important;}
.article-body a,.article-content a,.longform a,.story a,.guide-content a,.rio-guide a,main a:not(.btn):not(.btn-secondary){color:var(--ec-amarelo)!important;-webkit-text-fill-color:var(--ec-amarelo)!important;text-underline-offset:3px;}

/* Botões: hierarquia de marca + melhoria de acessibilidade */
a.btn,.btn,button.btn,.hero-ctas a,.ctas a{font-family:Catamaran,Verdana,system-ui,sans-serif!important;font-weight:900!important;letter-spacing:.13em!important;text-transform:uppercase!important;border-radius:999px!important;}
.hero-ctas a[href*="tagme"],.hero-ctas a[href*="reserv"],.ctas a[href*="tagme"],.ctas a[href*="reserv"],a.btn[href*="tagme"],a.btn[href*="reserv"],nav.top a.btn[href*="tagme"]{background:var(--ec-amarelo)!important;border-color:var(--ec-amarelo)!important;color:var(--ec-azul1)!important;-webkit-text-fill-color:var(--ec-azul1)!important;box-shadow:0 9px 0 rgba(0,64,90,.22),0 16px 30px rgba(0,64,90,.20)!important;}
.hero-ctas a:not([href*="tagme"]):not([href*="reserv"]),.ctas a:not([href*="tagme"]):not([href*="reserv"]),.btn-secondary,a.btn-secondary{background:rgba(0,64,90,.20)!important;border:1px solid rgba(237,226,201,.86)!important;color:var(--ec-areia)!important;-webkit-text-fill-color:var(--ec-areia)!important;}
.hero-ctas a:not([href*="tagme"]):not([href*="reserv"]):hover,.ctas a:not([href*="tagme"]):not([href*="reserv"]):hover,.btn-secondary:hover,a.btn-secondary:hover{background:var(--ec-areia)!important;border-color:var(--ec-areia)!important;color:var(--ec-azul1)!important;-webkit-text-fill-color:var(--ec-azul1)!important;}

/* Cards claros mantêm leitura azul/verdes oficiais */
.ec-final-geo-answer,.ec-final-geo-answer *,.light-section,.light-section *,.paper-section,.paper-section *,.section-paper,.section-paper *,.bg-paper,.bg-paper *,.card-light,.card-light *{background-color:inherit;color:var(--ec-azul1)!important;-webkit-text-fill-color:var(--ec-azul1)!important;text-shadow:none!important;}
.ec-final-geo-answer h1,.ec-final-geo-answer h2,.ec-final-geo-answer h3,.light-section h1,.light-section h2,.light-section h3,.paper-section h1,.paper-section h2,.paper-section h3,.section-paper h1,.section-paper h2,.section-paper h3,.bg-paper h1,.bg-paper h2,.bg-paper h3,.card-light h1,.card-light h2,.card-light h3{color:var(--ec-verde)!important;-webkit-text-fill-color:var(--ec-verde)!important;}
.ec-final-geo-answer a,.light-section a,.paper-section a,.section-paper a,.bg-paper a,.card-light a{color:#b76f00!important;-webkit-text-fill-color:#b76f00!important;}

/* Elementos de apoio: ondas/estampas sutis inspiradas no manual */
.brand-wave-bg,.ec-brand-wave-bg{background-image:repeating-linear-gradient(0deg,rgba(237,226,201,.08) 0 1px,transparent 1px 10px);background-blend-mode:soft-light;}
</style>
''' + END

COUNTERS = {'html_scanned':0,'html_updated':0,'css_injected':0,'audit_pass':0,'audit_warn':0}
DETAILS = []

def is_html(p):
    rel = p.relative_to(ROOT).as_posix()
    return p.suffix.lower()=='.html' and not rel.startswith('_') and '.git' not in p.parts and rel not in SKIP

def process(p):
    if not is_html(p): return
    rel = p.relative_to(ROOT).as_posix()
    COUNTERS['html_scanned'] += 1
    original = p.read_text(encoding='utf-8', errors='ignore')
    text = BLOCK_RE.sub('\n', original)
    if HEAD_RE.search(text):
        text = HEAD_RE.sub(CSS + '\n</head>', text, count=1)
        COUNTERS['css_injected'] += 1
    if text != original:
        p.write_text(text, encoding='utf-8')
        COUNTERS['html_updated'] += 1

def audit(p):
    if not is_html(p): return
    rel = p.relative_to(ROOT).as_posix()
    text = p.read_text(encoding='utf-8', errors='ignore')
    compact = text.replace(' ','').lower()
    checks = {
        'brand_lock_present':'ec-brand-manual-alignment' in text,
        'palette_azul1':'#00405a' in compact,
        'palette_verde':'#335d4a' in compact,
        'palette_amarelo':'#f59b1e' in compact,
        'palette_areia':'#ede2c9' in compact,
        'typography_catamaran_verdana':'catamaran' in compact and 'verdana' in compact,
        'logo_protection_rule':'object-fit:contain!important' in compact and 'min-width:68px!important' in compact,
        'cta_accessible_yellow_blue':'color:var(--ec-azul1)!important' in compact and 'background:var(--ec-amarelo)!important' in compact,
        'light_section_brand_text':'color:var(--ec-azul1)!important' in compact,
    }
    status = 'PASS' if all(checks.values()) else 'WARN'
    COUNTERS['audit_pass' if status=='PASS' else 'audit_warn'] += 1
    DETAILS.append({'page':rel,'status':status,**checks})

def write_reports():
    REPORT_DIR.mkdir(exist_ok=True)
    warn = [d for d in DETAILS if d['status']=='WARN']
    lines = ['# Brand Manual Alignment','','## Objetivo','Alinhar o sistema visual do site ao Manual da Marca Embaixada Carioca V02, mantendo melhorias de legibilidade e conversão.','','## Referências aplicadas','- Paleta oficial: Azul 1, Azul 2, Verde, Amarelo, Areia, Verde 2 e Cinzas.','- Logo principal preservada, sem distorção, com proteção e contraste.','- Tipografia oficial: Catamaran + Verdana/sistema.','- Botão de reserva/TagMe com Amarelo oficial e texto Azul 1 para melhor contraste.','- Botões secundários vazados com hover invertido.','','## Veredito',f'- Páginas auditadas: {len(DETAILS)}',f'- PASS: {len(DETAILS)-len(warn)}',f'- WARN: {len(warn)}',f"- Status geral: {'PASS' if not warn else 'WARN'}",'','## Contadores']
    lines += [f'- {k}: {v}' for k,v in COUNTERS.items()]
    lines += ['', '## Páginas com WARN']
    if warn:
        for d in warn:
            failed = [k for k,v in d.items() if isinstance(v,bool) and not v]
            lines.append(f"- {d['page']}: {', '.join(failed)}")
    else:
        lines.append('- Nenhuma.')
    lines += ['', '## Observação','Auditoria estática; validar pixel e contraste no navegador pós-deploy com cache limpo.','']
    REPORT_MD.write_text('\n'.join(lines), encoding='utf-8')
    with REPORT_CSV.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(DETAILS[0].keys()) if DETAILS else ['page'])
        writer.writeheader(); writer.writerows(DETAILS)
    print(REPORT_MD.read_text(encoding='utf-8'))

def main():
    for p in sorted(ROOT.rglob('*.html')): process(p)
    for p in sorted(ROOT.rglob('*.html')): audit(p)
    write_reports(); return 0

if __name__ == '__main__':
    raise SystemExit(main())
