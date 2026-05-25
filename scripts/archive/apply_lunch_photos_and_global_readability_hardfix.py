#!/usr/bin/env python3
from pathlib import Path
import csv, re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / '_audit_reports'
REPORT_MD = REPORT_DIR / 'lunch_photos_global_readability_hardfix_report.md'
REPORT_CSV = REPORT_DIR / 'lunch_photos_global_readability_hardfix_details.csv'
SKIP = {'404.html', 'offline.html', 'home-preview.html'}

START = '<!-- EC Lunch Photos + Global Readability Hardfix -->'
END = '<!-- /EC Lunch Photos + Global Readability Hardfix -->'
BLOCK_RE = re.compile(r'\n*<!-- EC Lunch Photos \+ Global Readability Hardfix -->[\s\S]*?<!-- /EC Lunch Photos \+ Global Readability Hardfix -->\s*', re.I)
BODY_RE = re.compile(r'</body>', re.I)
HEAD_RE = re.compile(r'</head>', re.I)

LUNCH_PAGES = {
    'almoco.html': {
        'burger': '''<article class="dish-card ec-added-cheeseburger-card">
<div class="photo-ph" data-label="Foto · Cheeseburger de Picanha · almoço Embaixada Carioca"></div>
<div class="dish-card-body">
<span class="tag">Sanduíche da casa</span>
<h3>Cheeseburger de <span class="serif">Picanha.</span></h3>
<p>Hambúrguer suculento de picanha, queijo derretido, pão macio e acompanhamento crocante — uma opção direta para quem quer almoço informal no Morro da Urca.</p>
<div class="price">Consulte<small>disponibilidade do dia</small></div>
</div>
</article>'''
    },
    'en/almoco.html': {
        'burger': '''<article class="dish-card ec-added-cheeseburger-card">
<div class="photo-ph" data-label="Photo · Picanha Cheeseburger · Embaixada Carioca lunch"></div>
<div class="dish-card-body">
<span class="tag">House sandwich</span>
<h3>Picanha <span class="serif">Cheeseburger.</span></h3>
<p>A juicy picanha burger with melted cheese and a soft bun — an easy lunch option for visitors at Urca Hill.</p>
<div class="price">Ask<small>daily availability</small></div>
</div>
</article>'''
    },
    'es/almoco.html': {
        'burger': '''<article class="dish-card ec-added-cheeseburger-card">
<div class="photo-ph" data-label="Foto · Cheeseburger de Picanha · almuerzo Embaixada Carioca"></div>
<div class="dish-card-body">
<span class="tag">Sándwich de la casa</span>
<h3>Cheeseburger de <span class="serif">Picanha.</span></h3>
<p>Hamburguesa jugosa de picanha con queso derretido y pan suave — una opción práctica para almorzar en el Morro da Urca.</p>
<div class="price">Consultar<small>disponibilidad del día</small></div>
</div>
</article>'''
    },
}

CSS = START + r'''
<style id="ec-lunch-photos-global-readability-hardfix">
/* HARD READABILITY FIX — deve ficar no fim do body para vencer CSS anterior */
:root{--ec-blue:#00405a;--ec-green:#335d4a;--ec-yellow:#f59b1e;--ec-sand:#ede2c9;--ec-paper:#f6efde;--ec-gray:#485156;--ec-gray2:#6b7377;}

/* Reset de herança que deixou texto claro em fundo claro */
html body main *{-webkit-text-fill-color:currentColor!important;text-shadow:none!important;}

/* Fundo escuro: texto claro de verdade */
html body main{background-color:var(--ec-blue);color:rgba(246,239,222,.92)!important;}
html body main section:not(.gallery-section):not(.ec-final-geo-answer):not(.light-section):not(.paper-section):not(.section-paper):not(.bg-paper):not(.menu-section){color:rgba(246,239,222,.92)!important;}
html body main section:not(.gallery-section):not(.ec-final-geo-answer):not(.light-section):not(.paper-section):not(.section-paper):not(.bg-paper):not(.menu-section) :where(p,li,span,small,dd,dt,summary,.lede,.copy,.description){color:rgba(246,239,222,.88)!important;}
html body main section:not(.gallery-section):not(.ec-final-geo-answer):not(.light-section):not(.paper-section):not(.section-paper):not(.bg-paper):not(.menu-section) :where(h1,h2,h3,h4,h5,h6){color:var(--ec-paper)!important;}
html body main section:not(.gallery-section):not(.ec-final-geo-answer):not(.light-section):not(.paper-section):not(.section-paper):not(.bg-paper):not(.menu-section) :where(strong,b){color:var(--ec-yellow)!important;}

/* Cards/caixas claras: texto escuro obrigatório */
html body main :where(.card,.box,.guide-card,.place-card,.beach-card,.route-card,.access-card,.access-fact,.access-route,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.menu-item,.menu-card,.dish-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-r2d2-card,.ec-sprint4-faq details,.direct-answer-card,.geo-card){background:var(--ec-paper)!important;color:var(--ec-blue)!important;border-color:rgba(0,64,90,.16)!important;}
html body main :where(.card,.box,.guide-card,.place-card,.beach-card,.route-card,.access-card,.access-fact,.access-route,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.menu-item,.menu-card,.dish-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-r2d2-card,.ec-sprint4-faq details,.direct-answer-card,.geo-card) :where(h1,h2,h3,h4,h5,h6,.title,.card-title,.menu-item-name){color:var(--ec-blue)!important;}
html body main :where(.card,.box,.guide-card,.place-card,.beach-card,.route-card,.access-card,.access-fact,.access-route,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.menu-item,.menu-card,.dish-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-r2d2-card,.ec-sprint4-faq details,.direct-answer-card,.geo-card) :where(p,li,span,small,dd,dt,summary,.copy,.description,.menu-item-desc){color:var(--ec-gray)!important;}
html body main :where(.card,.box,.guide-card,.place-card,.beach-card,.route-card,.access-card,.access-fact,.access-route,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.menu-item,.menu-card,.dish-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-r2d2-card,.ec-sprint4-faq details,.direct-answer-card,.geo-card) :where(strong,b,.tag,.kicker,.menu-item-price){color:var(--ec-green)!important;}
html body main :where(.card,.box,.guide-card,.place-card,.beach-card,.route-card,.access-card,.access-fact,.access-route,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.menu-item,.menu-card,.dish-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-r2d2-card,.ec-sprint4-faq details,.direct-answer-card,.geo-card) a:not(.btn):not(.btn-secondary){color:#b76f00!important;}

/* Seções claras completas */
html body main :where(.menu-section,.gallery-section,.ec-final-geo-answer,.light-section,.paper-section,.section-paper,.bg-paper,.access-direct,.access-section,.access-faq){background:var(--ec-paper)!important;color:var(--ec-blue)!important;}
html body main :where(.menu-section,.gallery-section,.ec-final-geo-answer,.light-section,.paper-section,.section-paper,.bg-paper,.access-direct,.access-section,.access-faq) :where(h1,h2,h3,h4,h5,h6){color:var(--ec-blue)!important;}
html body main :where(.menu-section,.gallery-section,.ec-final-geo-answer,.light-section,.paper-section,.section-paper,.bg-paper,.access-direct,.access-section,.access-faq) :where(p,li,span,small,dd,dt,summary){color:var(--ec-gray)!important;}

/* Página almoço: fotos reais nos placeholders */
html body main .dish-card .photo-ph,html body main .feijoada-feature .photo-ph{position:relative;min-height:260px;background-size:cover!important;background-position:center!important;background-repeat:no-repeat!important;border:0!important;overflow:hidden;}
html body main .dish-card.featured .photo-ph{min-height:360px;}
html body main .photo-ph:before{display:none!important;content:none!important;}
html body main .photo-ph:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,64,90,0) 46%,rgba(0,64,90,.22) 100%);pointer-events:none;}
html body main .photo-ph[data-label*="Feijoada"],html body main .photo-ph[data-label*="feijoada"]{background-image:linear-gradient(180deg,rgba(0,64,90,.06),rgba(0,64,90,.06)),url('/assets/fabio-almoco-mesa-completa.webp')!important;}
html body main .photo-ph[data-label*="Picanha"],html body main .photo-ph[data-label*="picanha"]{background-image:linear-gradient(180deg,rgba(0,64,90,.06),rgba(0,64,90,.06)),url('/assets/fabio-almoco-mesa-completa.webp')!important;}
html body main .photo-ph[data-label*="Picadinho"],html body main .photo-ph[data-label*="picadinho"]{background-image:linear-gradient(180deg,rgba(0,64,90,.06),rgba(0,64,90,.06)),url('/assets/carne-seca-mandioca.webp')!important;}
html body main .photo-ph[data-label*="Bobó"],html body main .photo-ph[data-label*="Bobo"],html body main .photo-ph[data-label*="camarão"],html body main .photo-ph[data-label*="camarao"]{background-image:linear-gradient(180deg,rgba(0,64,90,.06),rgba(0,64,90,.06)),url('/assets/bobo-camarao-real.webp')!important;}
html body main .photo-ph[data-label*="Salmão"],html body main .photo-ph[data-label*="Salmao"],html body main .photo-ph[data-label*="salmão"],html body main .photo-ph[data-label*="salmao"]{background-image:linear-gradient(180deg,rgba(0,64,90,.06),rgba(0,64,90,.06)),url('/assets/fabio-almoco-salmao-pao-acucar.webp')!important;}
html body main .photo-ph[data-label*="Cheeseburger"],html body main .photo-ph[data-label*="cheeseburger"]{background-image:linear-gradient(180deg,rgba(0,64,90,.06),rgba(0,64,90,.06)),url('/assets/almoco-mesa-opt-mobile.webp')!important;}

/* Cardápio: cards de produto legíveis */
html body main .menu-item{background:var(--ec-sand)!important;color:var(--ec-blue)!important;}
html body main .menu-item *{text-shadow:none!important;}
html body main .menu-item :where(h3,h4,.menu-item-name){color:var(--ec-blue)!important;}
html body main .menu-item :where(p,.menu-item-desc,span,small){color:var(--ec-gray)!important;}
html body main .menu-item :where(.price,.menu-item-price,strong){color:#b76f00!important;}

/* Blocos de FAQ em fundo azul: melhora contraste sem virar card branco */
html body main :where(.faq,.faq-section,.faq-list,.questions,.qa-grid,.event-faq,.events-faq) :where(h2,h3,h4,summary){color:var(--ec-paper)!important;}
html body main :where(.faq,.faq-section,.faq-list,.questions,.qa-grid,.event-faq,.events-faq) :where(p,li,span){color:rgba(246,239,222,.86)!important;}

/* Galerias e captions */
html body main .gallery-section figure,html body main .gallery-section figcaption{background:#fff!important;color:var(--ec-gray)!important;}
html body main .gallery-section figcaption{color:var(--ec-gray)!important;}

/* Botões */
html body main a.btn[href*="tagme"],html body main a.btn[href*="reserv"],nav.top a.btn[href*="tagme"]{background:var(--ec-yellow)!important;border-color:var(--ec-yellow)!important;color:var(--ec-blue)!important;}
html body main .btn-secondary,html body main a.btn-secondary,html body main .hero-ctas a:not([href*="tagme"]):not([href*="reserv"]),html body main .ctas a:not([href*="tagme"]):not([href*="reserv"]){color:var(--ec-paper)!important;}
html body main .btn-secondary:hover,html body main a.btn-secondary:hover,html body main .hero-ctas a:not([href*="tagme"]):not([href*="reserv"]):hover,html body main .ctas a:not([href*="tagme"]):not([href*="reserv"]):hover{background:var(--ec-paper)!important;color:var(--ec-blue)!important;}
@media(max-width:760px){html body main .dish-card .photo-ph{min-height:230px;}html body main .dish-card.featured .photo-ph{min-height:270px;}}
</style>
''' + END

COUNTERS = {'html_scanned':0,'html_updated':0,'css_injected':0,'burger_cards_added':0,'audit_pass':0,'audit_warn':0}
DETAILS = []

def is_html(p: Path) -> bool:
    rel = p.relative_to(ROOT).as_posix()
    return p.suffix.lower()=='.html' and not rel.startswith('_') and '.git' not in p.parts and rel not in SKIP

def add_burger_card(text: str, rel: str) -> str:
    if rel not in LUNCH_PAGES or 'ec-added-cheeseburger-card' in text:
        return text
    marker = '<article class="dish-card">\n<div class="photo-ph" data-label="Foto · Filé mignon · banco FOSCO"></div>'
    card = LUNCH_PAGES[rel]['burger'] + '\n'
    if marker in text:
        COUNTERS['burger_cards_added'] += 1
        return text.replace(marker, card + marker, 1)
    # fallback: antes de fechar a grade de pratos
    m = re.search(r'(</article>\s*</div>\s*</div>\s*</section>\s*<!-- FEIJOADA FEATURE -->)', text, re.I)
    if m:
        COUNTERS['burger_cards_added'] += 1
        return text[:m.start()] + '</article>\n' + card + text[m.start()+10:]
    return text

def inject_css(text: str) -> str:
    text = BLOCK_RE.sub('\n', text)
    # inserir antes de </body> para ser o último CSS e vencer blocos anteriores
    if BODY_RE.search(text):
        return BODY_RE.sub(CSS + '\n</body>', text, count=1)
    if HEAD_RE.search(text):
        return HEAD_RE.sub(CSS + '\n</head>', text, count=1)
    return text

def process(p: Path) -> None:
    if not is_html(p): return
    rel = p.relative_to(ROOT).as_posix()
    COUNTERS['html_scanned'] += 1
    original = p.read_text(encoding='utf-8', errors='ignore')
    text = add_burger_card(original, rel)
    before = text
    text = inject_css(text)
    if text != before:
        COUNTERS['css_injected'] += 1
    if text != original:
        p.write_text(text, encoding='utf-8')
        COUNTERS['html_updated'] += 1

def audit(p: Path) -> None:
    if not is_html(p): return
    rel = p.relative_to(ROOT).as_posix()
    text = p.read_text(encoding='utf-8', errors='ignore')
    compact = text.replace(' ','').lower()
    is_lunch = rel in LUNCH_PAGES
    checks = {
        'hardfix_present':'ec-lunch-photos-global-readability-hardfix' in text,
        'css_at_body_end':'</style>\n<!-- /EC Lunch Photos + Global Readability Hardfix -->\n</body>' in text,
        'dark_text_rule':'rgba(246,239,222,.88)!important' in compact,
        'light_card_dark_text_rule':'--ec-gray:#485156' in text and '--ec-blue:#00405a' in text,
        'webkit_reset':'-webkit-text-fill-color:currentColor!important'.lower() in compact,
        'lunch_photo_rules': (not is_lunch) or all(asset in text for asset in ['fabio-almoco-mesa-completa.webp','bobo-camarao-real.webp','carne-seca-mandioca.webp','fabio-almoco-salmao-pao-acucar.webp']),
        'cheeseburger_card': (not is_lunch) or ('ec-added-cheeseburger-card' in text),
    }
    status = 'PASS' if all(checks.values()) else 'WARN'
    COUNTERS['audit_pass' if status=='PASS' else 'audit_warn'] += 1
    DETAILS.append({'page':rel,'status':status,'is_lunch':is_lunch,**checks})

def write_reports():
    REPORT_DIR.mkdir(exist_ok=True)
    warn = [d for d in DETAILS if d['status']=='WARN']
    lines = ['# Lunch Photos + Global Readability Hardfix','','## Objetivo','Corrigir duas falhas visuais críticas: página de almoço sem fotos nos cards principais e contraste insuficiente em páginas claras/escuras.','','## Veredito',f'- Páginas auditadas: {len(DETAILS)}',f'- PASS: {len(DETAILS)-len(warn)}',f'- WARN: {len(warn)}',f"- Status geral: {'PASS' if not warn else 'WARN'}",'','## Almoço — pratos protegidos','- Picanha','- Feijoada','- Bobó de camarão','- Picadinho','- Cheeseburger de Picanha','- Salmão/itens complementares','','## Contadores']
    lines += [f'- {k}: {v}' for k,v in COUNTERS.items()]
    lines += ['', '## Páginas com WARN']
    if warn:
        for d in warn:
            failed = [k for k,v in d.items() if isinstance(v,bool) and not v]
            lines.append(f"- {d['page']}: {', '.join(failed)}")
    else:
        lines.append('- Nenhuma.')
    lines += ['', '## Observação','Auditoria estática. Validar visualmente no navegador com Ctrl+Shift+R, especialmente almoço, cardápio, guia do Rio, eventos, café da manhã e como chegar.','']
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
