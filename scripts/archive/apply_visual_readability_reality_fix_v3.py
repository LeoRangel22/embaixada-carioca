#!/usr/bin/env python3
from pathlib import Path
import csv, re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / '_audit_reports'
REPORT_MD = REPORT_DIR / 'visual_readability_reality_fix_report.md'
REPORT_CSV = REPORT_DIR / 'visual_readability_reality_fix_details.csv'
START = '<!-- EC Visual Readability Reality Fix -->'
END = '<!-- /EC Visual Readability Reality Fix -->'
BLOCK_RE = re.compile(r'\n*<!-- EC Visual Readability Reality Fix -->[\s\S]*?<!-- /EC Visual Readability Reality Fix -->\s*', re.I)
BODY_RE = re.compile(r'</body>', re.I)
HEAD_RE = re.compile(r'</head>', re.I)
SKIP = {'404.html','offline.html','home-preview.html'}
INVALID_RGBA_RE = re.compile(r'rgba\([^)]*(?:237\.779|245,237\.779|37\.779|\d+\.\d+\s*,\s*\d+\s*,\s*\d+\s*,)[^)]*\)', re.I)

FIX_BLOCK = START + r'''
<style id="ec-visual-readability-reality-fix">
/* VISUAL READABILITY REALITY FIX V3
   Correção baseada em print real: no cardápio, o nome do prato deve ser verde escuro e legível no fundo areia. */
:root{--ec-vr-blue:#00405a;--ec-vr-green:#335d4a;--ec-vr-yellow:#f59b1e;--ec-vr-sand:#ede2c9;--ec-vr-paper:#f6efde;--ec-vr-gray:#485156;--ec-vr-price:#9a6500;}
html body main *{-webkit-text-fill-color:currentColor!important;}
html body main .menu-section .menu-item,html body main .menu-grid .menu-item,html body main .menu-item{background:var(--ec-vr-sand)!important;color:var(--ec-vr-gray)!important;border-color:rgba(0,64,90,.16)!important;}
html body main .menu-section .menu-item :is(h1,h2,h3,h4,.menu-item-name,.item-name,.dish-name,.title,.card-title),html body main .menu-grid .menu-item :is(h1,h2,h3,h4,.menu-item-name,.item-name,.dish-name,.title,.card-title),html body main .menu-item :is(h1,h2,h3,h4,.menu-item-name,.item-name,.dish-name,.title,.card-title){color:var(--ec-vr-green)!important;-webkit-text-fill-color:var(--ec-vr-green)!important;font-weight:900!important;text-shadow:none!important;opacity:1!important;}
html body main .menu-section .menu-item :is(p,li,span,small,.menu-item-desc,.item-desc,.description,.copy),html body main .menu-grid .menu-item :is(p,li,span,small,.menu-item-desc,.item-desc,.description,.copy),html body main .menu-item :is(p,li,span,small,.menu-item-desc,.item-desc,.description,.copy){color:var(--ec-vr-gray)!important;-webkit-text-fill-color:var(--ec-vr-gray)!important;text-shadow:none!important;opacity:1!important;}
html body main .menu-section .menu-item :is(.price,.menu-item-price,.item-price),html body main .menu-grid .menu-item :is(.price,.menu-item-price,.item-price),html body main .menu-item :is(.price,.menu-item-price,.item-price){color:var(--ec-vr-price)!important;-webkit-text-fill-color:var(--ec-vr-price)!important;font-weight:900!important;text-shadow:none!important;}
html body main .menu-item :is(.tag,.badge,.kicker){color:var(--ec-vr-blue)!important;-webkit-text-fill-color:var(--ec-vr-blue)!important;text-shadow:none!important;}
html body main .menu-item :is(.tag.win,.badge.win,.premiada,.premiado){background:var(--ec-vr-yellow)!important;color:var(--ec-vr-blue)!important;-webkit-text-fill-color:var(--ec-vr-blue)!important;}
html body main :is(.card,.box,.guide-card,.place-card,.beach-card,.route-card,.access-card,.access-fact,.access-route,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details){background-color:var(--ec-vr-paper)!important;color:var(--ec-vr-gray)!important;border-color:rgba(0,64,90,.14)!important;}
html body main :is(.card,.box,.guide-card,.place-card,.beach-card,.route-card,.access-card,.access-fact,.access-route,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details) :is(h1,h2,h3,h4,h5,h6,.title,.card-title){color:var(--ec-vr-blue)!important;-webkit-text-fill-color:var(--ec-vr-blue)!important;font-weight:850!important;text-shadow:none!important;opacity:1!important;}
html body main :is(.card,.box,.guide-card,.place-card,.beach-card,.route-card,.access-card,.access-fact,.access-route,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details) :is(p,li,span,small,dd,dt,summary,.copy,.description){color:var(--ec-vr-gray)!important;-webkit-text-fill-color:var(--ec-vr-gray)!important;text-shadow:none!important;opacity:1!important;}
html body main section:not(.menu-section):not(.gallery-section):not(.light-section):not(.paper-section):not(.section-paper):not(.bg-paper):not(.ec-final-geo-answer) :is(p,li,span,small,dd,dt,.lede,.copy,.description){color:rgba(246,239,222,.90)!important;-webkit-text-fill-color:rgba(246,239,222,.90)!important;opacity:1!important;text-shadow:none!important;}
html body main section:not(.menu-section):not(.gallery-section):not(.light-section):not(.paper-section):not(.section-paper):not(.bg-paper):not(.ec-final-geo-answer) :is(h1,h2,h3,h4,h5,h6){color:var(--ec-vr-paper)!important;-webkit-text-fill-color:var(--ec-vr-paper)!important;opacity:1!important;text-shadow:none!important;}
html body main .gallery-section :is(figure,figcaption,.caption){background:#fff!important;color:var(--ec-vr-gray)!important;-webkit-text-fill-color:var(--ec-vr-gray)!important;}
html body main a.btn[href*="tagme"],html body main a.btn[href*="reserv"],nav.top a.btn[href*="tagme"]{background:var(--ec-vr-yellow)!important;border-color:var(--ec-vr-yellow)!important;color:var(--ec-vr-blue)!important;-webkit-text-fill-color:var(--ec-vr-blue)!important;}
</style>
<script id="ec-visual-readability-reality-js">
(function(){
  function setImportant(el, prop, val){ if(el && el.style) el.style.setProperty(prop, val, 'important'); }
  function fixMenu(){
    document.querySelectorAll('main .menu-item h1, main .menu-item h2, main .menu-item h3, main .menu-item h4, main .menu-item .menu-item-name, main .menu-item .item-name, main .menu-item .dish-name, main .menu-item .title, main .menu-item .card-title').forEach(function(el){setImportant(el,'color','#335d4a');setImportant(el,'-webkit-text-fill-color','#335d4a');setImportant(el,'text-shadow','none');setImportant(el,'opacity','1');setImportant(el,'font-weight','900');});
    document.querySelectorAll('main .menu-item p, main .menu-item .menu-item-desc, main .menu-item .item-desc, main .menu-item .description, main .menu-item small').forEach(function(el){setImportant(el,'color','#485156');setImportant(el,'-webkit-text-fill-color','#485156');setImportant(el,'text-shadow','none');setImportant(el,'opacity','1');});
    document.querySelectorAll('main .menu-item .price, main .menu-item .menu-item-price, main .menu-item .item-price').forEach(function(el){setImportant(el,'color','#9a6500');setImportant(el,'-webkit-text-fill-color','#9a6500');setImportant(el,'font-weight','900');});
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fixMenu, {once:true}); else fixMenu();
  window.addEventListener('load', fixMenu, {once:true});
})();
</script>
''' + END

COUNTERS = {'html_scanned':0,'html_updated':0,'css_js_injected':0,'invalid_rgba_fixed':0,'audit_pass':0,'audit_warn':0}
DETAILS=[]

def is_html(p: Path) -> bool:
    rel = p.relative_to(ROOT).as_posix()
    return p.suffix.lower()=='.html' and not rel.startswith('_') and '.git' not in p.parts and rel not in SKIP

def clean_invalid_rgba(text: str) -> tuple[str,int]:
    before = text
    text = text.replace('rgba(237.779,201,', 'rgba(237,226,201,')
    text = text.replace('rgba(245,237.779,0.82)', 'rgba(245,237,229,0.82)')
    text = text.replace('rgba(37.779,102,', 'rgba(37,211,102,')
    # Só considera inválido quando o padrão está dentro de rgba(...), não quando aparece em texto legítimo como 7.779 avaliações.
    return text, 0 if text == before else 1

def inject(text: str) -> tuple[str,bool]:
    before=text
    text = BLOCK_RE.sub('\n', text)
    if BODY_RE.search(text): text = BODY_RE.sub(FIX_BLOCK+'\n</body>', text, count=1)
    elif HEAD_RE.search(text): text = HEAD_RE.sub(FIX_BLOCK+'\n</head>', text, count=1)
    return text, text != before

def process(p: Path):
    COUNTERS['html_scanned'] += 1
    original = p.read_text(encoding='utf-8', errors='ignore')
    text, n = clean_invalid_rgba(original)
    text, injected = inject(text)
    COUNTERS['invalid_rgba_fixed'] += n
    if injected: COUNTERS['css_js_injected'] += 1
    if text != original:
        p.write_text(text, encoding='utf-8')
        COUNTERS['html_updated'] += 1

def audit(p: Path):
    rel = p.relative_to(ROOT).as_posix()
    text = p.read_text(encoding='utf-8', errors='ignore')
    compact = text.replace(' ','').lower()
    is_menu = rel.endswith('cardapio.html') or 'cardapio' in rel or rel.endswith('menu.html') or 'menu' in rel
    checks = {
        'reality_fix_present':'ec-visual-readability-reality-fix' in text,
        'menu_titles_dark_green_rule':'color:var(--ec-vr-green)!important' in compact and '#335d4a' in compact,
        'menu_js_guard_present':'ec-visual-readability-reality-js' in text,
        'light_card_dark_text_rule':'--ec-vr-gray:#485156' in compact and '--ec-vr-blue:#00405a' in compact,
        'invalid_rgba_clean':not INVALID_RGBA_RE.search(text),
        'menu_page_guard':(not is_menu) or ('main .menu-item h1' in text and '#335d4a' in text),
    }
    status = 'PASS' if all(checks.values()) else 'WARN'
    COUNTERS['audit_pass' if status=='PASS' else 'audit_warn'] += 1
    DETAILS.append({'page':rel,'status':status,**checks})

def write_reports():
    REPORT_DIR.mkdir(exist_ok=True)
    warn=[d for d in DETAILS if d['status']=='WARN']
    lines=['# Visual Readability Reality Fix','','## Objetivo','Corrigir problemas visuais reais de contraste, especialmente o cardápio com títulos de pratos claros sobre fundo areia.','','## Decisão visual','- Nome dos pratos no cardápio: verde escuro oficial `#335d4a`.','- Descrição dos pratos e cards claros: cinza escuro `#485156`.','- Preços: dourado escuro `#9a6500`.','- Fundo escuro: texto areia claro com opacidade alta.','','## Veredito',f"- Páginas auditadas: {COUNTERS['html_scanned']}",f"- PASS: {COUNTERS['audit_pass']}",f"- WARN: {COUNTERS['audit_warn']}",f"- Status geral: {'PASS' if not warn else 'WARN'}",'','## Contadores']
    lines += [f'- {k}: {v}' for k,v in COUNTERS.items()]
    lines += ['', '## Páginas com WARN']
    if warn:
        for d in warn:
            failed=[k for k,v in d.items() if isinstance(v,bool) and not v]
            lines.append(f"- {d['page']}: {', '.join(failed)}")
    else: lines.append('- Nenhuma.')
    lines.append('')
    REPORT_MD.write_text('\n'.join(lines), encoding='utf-8')
    fieldnames=['page','status','reality_fix_present','menu_titles_dark_green_rule','menu_js_guard_present','light_card_dark_text_rule','invalid_rgba_clean','menu_page_guard']
    with REPORT_CSV.open('w', newline='', encoding='utf-8') as f:
        writer=csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader(); writer.writerows(DETAILS)
    print(REPORT_MD.read_text(encoding='utf-8'))

def main():
    for p in sorted(ROOT.rglob('*.html')):
        if is_html(p): process(p)
    for p in sorted(ROOT.rglob('*.html')):
        if is_html(p): audit(p)
    write_reports(); return 0

if __name__ == '__main__':
    raise SystemExit(main())
