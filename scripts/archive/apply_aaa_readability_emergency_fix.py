#!/usr/bin/env python3
from pathlib import Path
import csv, re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / '_audit_reports'
REPORT_MD = REPORT_DIR / 'aaa_readability_emergency_fix_report.md'
REPORT_CSV = REPORT_DIR / 'aaa_readability_emergency_fix_details.csv'
SKIP = {'404.html', 'offline.html', 'home-preview.html'}
START = '<!-- EC AAA Readability Emergency Fix -->'
END = '<!-- /EC AAA Readability Emergency Fix -->'
BLOCK_RE = re.compile(r'\n*<!-- EC AAA Readability Emergency Fix -->[\s\S]*?<!-- /EC AAA Readability Emergency Fix -->\s*', re.I)
HEAD_RE = re.compile(r'</head>', re.I)

CSS = START + r'''
<style id="ec-aaa-readability-emergency-fix">
/* AAA READABILITY EMERGENCY FIX
   Corrige o problema real visto no navegador: textos herdando -webkit-text-fill-color claro em cards claros
   e textos escuros em fundos azul-escuro. Este bloco deve ficar por último no <head>. */
:root{--ec-readable-blue:#00405a;--ec-readable-green:#335d4a;--ec-readable-yellow:#f59b1e;--ec-readable-sand:#ede2c9;--ec-readable-sand-soft:#f6efde;--ec-readable-gray:#485156;--ec-readable-gray-2:#6b7377;}

/* 1) Zera herança problemática de -webkit-text-fill-color */
html body main :where(h1,h2,h3,h4,h5,h6,p,li,span,strong,em,a,small,summary,details,div,td,th,dd,dt,label){-webkit-text-fill-color:currentColor!important;}

/* 2) Padrão em áreas escuras: texto claro, legível */
html body main{color:rgba(237,226,201,.90)!important;}
html body main :where(p,li,small,summary,dd,dt){color:rgba(237,226,201,.88)!important;}
html body main :where(h1,h2,h3,h4,h5,h6){color:var(--ec-readable-sand-soft)!important;text-shadow:none!important;}
html body main :where(strong,b){color:var(--ec-readable-yellow)!important;}
html body main :where(a:not(.btn):not(.btn-secondary)){color:var(--ec-readable-yellow)!important;text-decoration-color:rgba(245,155,30,.55)!important;text-underline-offset:3px!important;}

/* 3) Cards, boxes, rotas, menu e blocos claros: texto escuro obrigatório */
html body main :where(.box,.card,.card-light,.menu-item,.menu-card,.menu-section,.menu-items,.access-direct,.access-section,.access-faq,.access-fact,.access-route,.access-card,.route-card,.guide-card,.place-card,.beach-card,.experience-card,.faq-card,.faq-item,.faq-block,.faq-grid,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details,.ec-sprint4-steps,.ec-r2d2-depth,.ec-final-geo-answer,.light-section,.paper-section,.section-paper,.bg-paper){color:var(--ec-readable-blue)!important;-webkit-text-fill-color:var(--ec-readable-blue)!important;text-shadow:none!important;}
html body main :where(.box,.card,.card-light,.menu-item,.menu-card,.access-fact,.access-route,.access-card,.route-card,.guide-card,.place-card,.beach-card,.experience-card,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details){background-color:var(--ec-readable-sand-soft);}
html body main :where(.box,.card,.card-light,.menu-item,.menu-card,.access-fact,.access-route,.access-card,.route-card,.guide-card,.place-card,.beach-card,.experience-card,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details) :where(h1,h2,h3,h4,h5,h6,.menu-item-name,.title,.card-title){color:var(--ec-readable-blue)!important;-webkit-text-fill-color:var(--ec-readable-blue)!important;text-shadow:none!important;}
html body main :where(.box,.card,.card-light,.menu-item,.menu-card,.access-fact,.access-route,.access-card,.route-card,.guide-card,.place-card,.beach-card,.experience-card,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details) :where(p,li,span,small,summary,dd,dt,.menu-item-desc,.description,.copy){color:var(--ec-readable-gray)!important;-webkit-text-fill-color:var(--ec-readable-gray)!important;text-shadow:none!important;}
html body main :where(.box,.card,.card-light,.menu-item,.menu-card,.access-fact,.access-route,.access-card,.route-card,.guide-card,.place-card,.beach-card,.experience-card,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details) :where(strong,b,.menu-item-price,.tag,.kicker){color:var(--ec-readable-green)!important;-webkit-text-fill-color:var(--ec-readable-green)!important;text-shadow:none!important;}
html body main :where(.box,.card,.card-light,.menu-item,.menu-card,.access-fact,.access-route,.access-card,.route-card,.guide-card,.place-card,.beach-card,.experience-card,.faq-card,.faq-item,.info-card,.content-card,.copy-card,.direct-answer-card,.geo-card,.ec-r2d2-card,.ec-final-geo-card,.ec-final-geo-faq details,.ec-sprint4-faq details) a:not(.btn):not(.btn-secondary){color:#b76f00!important;-webkit-text-fill-color:#b76f00!important;text-shadow:none!important;}

/* 4) Seções claras completas: fundo areia/off-white com textos azuis/cinza */
html body main :where(.access-direct,.access-section,.access-faq,.menu-section,.ec-final-geo-answer,.ec-r2d2-depth,.ec-sprint4-faq,.ec-sprint4-steps,.light-section,.paper-section,.section-paper,.bg-paper){background-color:var(--ec-readable-sand-soft)!important;color:var(--ec-readable-blue)!important;-webkit-text-fill-color:var(--ec-readable-blue)!important;}
html body main :where(.access-direct,.access-section,.access-faq,.menu-section,.ec-final-geo-answer,.ec-r2d2-depth,.ec-sprint4-faq,.ec-sprint4-steps,.light-section,.paper-section,.section-paper,.bg-paper) :where(h1,h2,h3,h4,h5,h6){color:var(--ec-readable-blue)!important;-webkit-text-fill-color:var(--ec-readable-blue)!important;text-shadow:none!important;}
html body main :where(.access-direct,.access-section,.access-faq,.menu-section,.ec-final-geo-answer,.ec-r2d2-depth,.ec-sprint4-faq,.ec-sprint4-steps,.light-section,.paper-section,.section-paper,.bg-paper) :where(p,li,span,small,summary,dd,dt){color:var(--ec-readable-gray)!important;-webkit-text-fill-color:var(--ec-readable-gray)!important;text-shadow:none!important;}

/* 5) Cardápio: garante leitura em todos os cards de produto */
html body main .menu-section-head h2,html body main .menu-section-head .hours,html body main .menu-section-head .tag{color:var(--ec-readable-blue)!important;-webkit-text-fill-color:var(--ec-readable-blue)!important;text-shadow:none!important;}
html body main .menu-item{background:var(--ec-readable-sand)!important;border-color:rgba(0,64,90,.16)!important;}
html body main .menu-item:hover{background:var(--ec-readable-sand-soft)!important;}
html body main .menu-item-badge{background:var(--ec-readable-yellow)!important;color:var(--ec-readable-blue)!important;-webkit-text-fill-color:var(--ec-readable-blue)!important;}

/* 6) FAQ/eventos em fundo escuro: perguntas claras, respostas claras */
html body main :where(.faq,.faq-section,.faq-list,.questions,.qa-grid,.event-faq,.events-faq) :where(h2,h3,h4,summary){color:var(--ec-readable-sand-soft)!important;-webkit-text-fill-color:var(--ec-readable-sand-soft)!important;}
html body main :where(.faq,.faq-section,.faq-list,.questions,.qa-grid,.event-faq,.events-faq) :where(p,li,span){color:rgba(237,226,201,.84)!important;-webkit-text-fill-color:rgba(237,226,201,.84)!important;}

/* 7) Botões preservam hierarquia de marca */
html body main a.btn[href*="tagme"],html body main a.btn[href*="reserv"],html body main .hero-ctas a[href*="tagme"],html body main .hero-ctas a[href*="reserv"],nav.top a.btn[href*="tagme"]{background:var(--ec-readable-yellow)!important;border-color:var(--ec-readable-yellow)!important;color:var(--ec-readable-blue)!important;-webkit-text-fill-color:var(--ec-readable-blue)!important;}
html body main .btn-secondary,html body main a.btn-secondary,html body main .hero-ctas a:not([href*="tagme"]):not([href*="reserv"]),html body main .ctas a:not([href*="tagme"]):not([href*="reserv"]){color:var(--ec-readable-sand-soft)!important;-webkit-text-fill-color:var(--ec-readable-sand-soft)!important;}
html body main .btn-secondary:hover,html body main a.btn-secondary:hover,html body main .hero-ctas a:not([href*="tagme"]):not([href*="reserv"]):hover,html body main .ctas a:not([href*="tagme"]):not([href*="reserv"]):hover{background:var(--ec-readable-sand-soft)!important;color:var(--ec-readable-blue)!important;-webkit-text-fill-color:var(--ec-readable-blue)!important;}
</style>
''' + END

COUNTERS = {'html_scanned': 0, 'html_updated': 0, 'css_injected': 0, 'audit_pass': 0, 'audit_warn': 0}
DETAILS = []

def is_html(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return path.suffix.lower() == '.html' and not rel.startswith('_') and '.git' not in path.parts and rel not in SKIP

def process(path: Path) -> None:
    if not is_html(path):
        return
    rel = path.relative_to(ROOT).as_posix()
    COUNTERS['html_scanned'] += 1
    original = path.read_text(encoding='utf-8', errors='ignore')
    text = BLOCK_RE.sub('\n', original)
    if HEAD_RE.search(text):
        text = HEAD_RE.sub(CSS + '\n</head>', text, count=1)
        COUNTERS['css_injected'] += 1
    if text != original:
        path.write_text(text, encoding='utf-8')
        COUNTERS['html_updated'] += 1

def audit(path: Path) -> None:
    if not is_html(path):
        return
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding='utf-8', errors='ignore')
    compact = text.replace(' ', '').lower()
    checks = {
        'emergency_lock_present': 'ec-aaa-readability-emergency-fix' in text,
        'webkit_currentcolor_reset': '-webkit-text-fill-color:currentcolor!important' in compact,
        'dark_background_text_light': 'rgba(237,226,201,.88)!important' in compact,
        'light_cards_text_dark': 'var(--ec-readable-gray)!important' in compact and 'var(--ec-readable-blue)!important' in compact,
        'menu_item_readable': '.menu-item' in text and 'menu-item-desc' in text,
        'faq_dark_readable': 'event-faq' in text and 'rgba(237,226,201,.84)' in text,
    }
    status = 'PASS' if all(checks.values()) else 'WARN'
    COUNTERS['audit_pass' if status == 'PASS' else 'audit_warn'] += 1
    DETAILS.append({'page': rel, 'status': status, **checks})

def write_reports() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    warn = [d for d in DETAILS if d['status'] == 'WARN']
    lines = [
        '# AAA Readability Emergency Fix', '',
        '## Objetivo',
        'Corrigir problemas reais de contraste: texto claro em cards claros, texto escuro em fundo azul e herança indevida de -webkit-text-fill-color.', '',
        '## Veredito',
        f'- Páginas auditadas: {len(DETAILS)}',
        f'- PASS: {len(DETAILS) - len(warn)}',
        f'- WARN: {len(warn)}',
        f"- Status geral: {'PASS' if not warn else 'WARN'}", '',
        '## Contadores'
    ]
    lines += [f'- {k}: {v}' for k, v in COUNTERS.items()]
    lines += ['', '## Páginas com WARN']
    if warn:
        for d in warn:
            failed = [k for k, v in d.items() if isinstance(v, bool) and not v]
            lines.append(f"- {d['page']}: {', '.join(failed)}")
    else:
        lines.append('- Nenhuma.')
    lines += ['', '## Observação', 'Auditoria estática. A validação final deve ser visual no navegador com cache limpo.', '']
    REPORT_MD.write_text('\n'.join(lines), encoding='utf-8')
    with REPORT_CSV.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(DETAILS[0].keys()) if DETAILS else ['page'])
        writer.writeheader(); writer.writerows(DETAILS)
    print(REPORT_MD.read_text(encoding='utf-8'))

def main() -> int:
    for p in sorted(ROOT.rglob('*.html')):
        process(p)
    for p in sorted(ROOT.rglob('*.html')):
        audit(p)
    write_reports()
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
