#!/usr/bin/env python3
from pathlib import Path
import csv, re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / '_audit_reports'
REPORT_MD = REPORT_DIR / 'legibility_contrast_lock_report.md'
REPORT_CSV = REPORT_DIR / 'legibility_contrast_lock_details.csv'
SKIP = {'404.html', 'offline.html', 'home-preview.html'}
START = '<!-- EC Legibility Contrast Lock -->'
END = '<!-- /EC Legibility Contrast Lock -->'
BLOCK_RE = re.compile(r'\n*<!-- EC Legibility Contrast Lock -->[\s\S]*?<!-- /EC Legibility Contrast Lock -->\s*', re.I)
HEAD_RE = re.compile(r'</head>', re.I)

CSS = START + r'''
<style id="ec-legibility-contrast-lock">
/* Legibilidade real: menu, hero e corpo em áreas escuras */
nav.top:not(.scrolled) .nav-links a,
nav.top:not(.scrolled) .nav-links a:link,
nav.top:not(.scrolled) .nav-links a:visited{color:rgba(246,239,222,.98)!important;-webkit-text-fill-color:rgba(246,239,222,.98)!important;text-shadow:0 2px 10px rgba(0,32,46,.78)!important;opacity:1!important;}
nav.top.scrolled,nav.top.nav-scrolled,body.scrolled nav.top{background:rgba(246,239,222,.96)!important;border-bottom:1px solid rgba(0,64,90,.14)!important;box-shadow:0 10px 32px rgba(0,32,46,.12)!important;backdrop-filter:blur(12px)!important;-webkit-backdrop-filter:blur(12px)!important;}
nav.top.scrolled .nav-links a,nav.top.nav-scrolled .nav-links a,body.scrolled nav.top .nav-links a{color:#00405a!important;-webkit-text-fill-color:#00405a!important;text-shadow:none!important;opacity:1!important;font-weight:900!important;}
nav.top.scrolled .brand-logo.light,nav.top.nav-scrolled .brand-logo.light,body.scrolled nav.top .brand-logo.light{display:none!important;}
nav.top.scrolled .brand-logo.dark,nav.top.nav-scrolled .brand-logo.dark,body.scrolled nav.top .brand-logo.dark{display:block!important;}
nav.top.scrolled .lang-current,nav.top.nav-scrolled .lang-current,body.scrolled nav.top .lang-current{color:#00405a!important;-webkit-text-fill-color:#00405a!important;background:rgba(255,255,255,.58)!important;border-color:rgba(0,64,90,.24)!important;text-shadow:none!important;}
nav.top.scrolled a.nav-rating-badge,nav.top.nav-scrolled a.nav-rating-badge,body.scrolled nav.top a.nav-rating-badge{background:rgba(255,255,255,.62)!important;border-color:rgba(0,64,90,.24)!important;color:#00405a!important;-webkit-text-fill-color:#00405a!important;}
header.hero h1,header.page-hero h1{color:#f6efde!important;-webkit-text-fill-color:#f6efde!important;text-shadow:0 3px 18px rgba(0,32,46,.76)!important;}
header.hero h1 .serif,header.page-hero h1 .serif,header.hero h1 em,header.page-hero h1 em{color:#f59b1e!important;-webkit-text-fill-color:#f59b1e!important;}
header.hero .hero-sub,header.page-hero .lede{color:rgba(246,239,222,.95)!important;-webkit-text-fill-color:rgba(246,239,222,.95)!important;text-shadow:0 2px 14px rgba(0,32,46,.72)!important;}
body{background:#00202e!important;}
.article-body,.article-content,.longform,.story,.guide-content,.rio-guide,.ec-sprint2-geo{color:rgba(246,239,222,.88)!important;font-size:18px!important;line-height:1.72!important;}
.article-body p,.article-content p,.longform p,.story p,.guide-content p,.rio-guide p,.ec-sprint2-geo p,main .lede,main .copy,main .description{color:rgba(246,239,222,.87)!important;-webkit-text-fill-color:rgba(246,239,222,.87)!important;}
.article-body li,.article-content li,.longform li,.story li,.guide-content li,.rio-guide li{color:rgba(246,239,222,.88)!important;}
.article-body h1,.article-body h2,.article-body h3,.article-content h1,.article-content h2,.article-content h3,.longform h1,.longform h2,.longform h3,.story h1,.story h2,.story h3,.guide-content h1,.guide-content h2,.guide-content h3,.rio-guide h1,.rio-guide h2,.rio-guide h3,.ec-sprint2-geo h2,main section:not(.ec-final-geo-answer) h1,main section:not(.ec-final-geo-answer) h2,main section:not(.ec-final-geo-answer) h3{color:#f6efde!important;-webkit-text-fill-color:#f6efde!important;text-shadow:0 2px 12px rgba(0,32,46,.38)!important;}
.article-body .serif,.article-content .serif,.longform .serif,.story .serif,.guide-content .serif,.rio-guide .serif,main section:not(.ec-final-geo-answer) em{color:#f2b24a!important;-webkit-text-fill-color:#f2b24a!important;}
.article-body strong,.article-content strong,.longform strong,.story strong,.guide-content strong,.rio-guide strong,main section:not(.ec-final-geo-answer) strong{color:#f5b548!important;-webkit-text-fill-color:#f5b548!important;}
.article-body a,.article-content a,.longform a,.story a,.guide-content a,.rio-guide a,main section:not(.ec-final-geo-answer) a{color:#f2b24a!important;-webkit-text-fill-color:#f2b24a!important;text-underline-offset:3px!important;}
.article-body .highlight,.article-content .highlight,.longform .highlight,.story .highlight,.guide-content .highlight,.rio-guide .highlight{background:rgba(246,239,222,.08)!important;border-left:3px solid #f59b1e!important;color:rgba(246,239,222,.92)!important;}
.ec-final-geo-answer,.ec-final-geo-answer *,.light-section,.light-section *,.paper-section,.paper-section *,.section-paper,.section-paper *,.bg-paper,.bg-paper *,.card-light,.card-light *{color:#00405a!important;-webkit-text-fill-color:#00405a!important;text-shadow:none!important;}
.ec-final-geo-answer a,.light-section a,.paper-section a,.section-paper a,.bg-paper a,.card-light a{color:#c47e15!important;-webkit-text-fill-color:#c47e15!important;}
@media(max-width:960px){.article-body,.article-content,.longform,.story,.guide-content,.rio-guide{font-size:16px!important;line-height:1.64!important;}}
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
    compact = text.replace(' ','')
    checks = {
        'contrast_lock_present':'ec-legibility-contrast-lock' in text,
        'menu_light_state_dark_text':'color:#00405a!important' in compact,
        'menu_photo_state_light_text':'rgba(246,239,222,.98)' in text,
        'body_dark_text_lightened':'color:#f6efde!important' in compact,
        'body_paragraph_legible':'rgba(246,239,222,.87)' in text,
    }
    status = 'PASS' if all(checks.values()) else 'WARN'
    COUNTERS['audit_pass' if status=='PASS' else 'audit_warn'] += 1
    DETAILS.append({'page':rel,'status':status,**checks})

def write_reports():
    REPORT_DIR.mkdir(exist_ok=True)
    warn = [d for d in DETAILS if d['status']=='WARN']
    lines = ['# Legibility Contrast Lock','','## Objetivo','Aumentar a legibilidade do menu e do corpo em áreas escuras, preservando seções claras com texto azul.','','## Veredito',f"- Páginas auditadas: {len(DETAILS)}",f"- PASS: {len(DETAILS)-len(warn)}",f"- WARN: {len(warn)}",f"- Status geral: {'PASS' if not warn else 'WARN'}",'','## Contadores']
    lines += [f'- {k}: {v}' for k,v in COUNTERS.items()]
    lines += ['', '## Páginas com WARN']
    lines += ['- Nenhuma.'] if not warn else [f"- {d['page']}: " + ', '.join(k for k,v in d.items() if isinstance(v,bool) and not v) for d in warn]
    lines.append('')
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
