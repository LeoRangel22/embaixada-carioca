#!/usr/bin/env python3
from pathlib import Path
import csv, re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / '_audit_reports'
REPORT_MD = REPORT_DIR / 'final_design_consistency_lock_report.md'
REPORT_CSV = REPORT_DIR / 'final_design_consistency_lock_details.csv'
SKIP = {'404.html', 'offline.html', 'home-preview.html'}

CSS_START = '<!-- EC Final Design Consistency Lock -->'
CSS_END = '<!-- /EC Final Design Consistency Lock -->'
CSS_RE = re.compile(r'\n*<!-- EC Final Design Consistency Lock -->[\s\S]*?<!-- /EC Final Design Consistency Lock -->\s*', re.I)
HEAD_CLOSE_RE = re.compile(r'</head>', re.I)
HERO_RE = re.compile(r'<header\b(?=[^>]*class=["\'][^"\']*\b(?:hero|page-hero)\b[^"\']*["\'])[^>]*>[\s\S]*?</header>', re.I)
BTN_RE = re.compile(r'<(a|button)\b(?=[^>]*class=["\'][^"\']*\b(?:btn|button|cta)\b[^"\']*["\'])[^>]*>[\s\S]*?</\1>', re.I)
ARROW_RE = re.compile(r'\s*(?:→|↗|›|»|➜|➔|➡|&rarr;|&#8594;|&#x2192;)\s*', re.I)
PIN_RE = re.compile(r'<span\s+class=["\']drawer-icon["\']>\s*📍\s*</span>\s*', re.I)

CSS_BLOCK = CSS_START + r'''
<style id="ec-final-design-consistency-lock">
/* FINAL DESIGN LOCK — linha laranja, botões e frames no padrão visual da home */
@media (min-width:961px){
  header.hero .hero-content .eyebrow.hero-eyebrow,
  header.page-hero .page-hero-content .eyebrow.hero-eyebrow{position:absolute!important;top:96px!important;left:clamp(78px,5.5vw,112px)!important;transform:none!important;margin:0!important;width:calc(100vw - clamp(78px,5.5vw,112px) - 250px)!important;max-width:none!important;white-space:nowrap!important;overflow:hidden!important;display:flex!important;align-items:center!important;gap:14px!important;font-family:"JetBrains Mono",ui-monospace,monospace!important;font-size:9px!important;line-height:1!important;letter-spacing:.31em!important;font-weight:700!important;text-transform:uppercase!important;color:var(--amarelo,#f59b1e)!important;z-index:20!important;border:0!important;outline:0!important;box-shadow:none!important;}
  header.hero .hero-content .eyebrow.hero-eyebrow:before,
  header.page-hero .page-hero-content .eyebrow.hero-eyebrow:before{content:""!important;display:inline-block!important;flex:0 0 34px!important;width:34px!important;height:2px!important;background:var(--amarelo,#f59b1e)!important;}
}

/* Base comum dos botões da hero */
.hero-ctas a,.hero-ctas button,.ctas a,.ctas button,.btn,a.btn,button.btn,.btn-secondary,a.btn-secondary{min-height:60px!important;height:60px!important;padding:0 36px!important;border-radius:999px!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;gap:0!important;font-family:"JetBrains Mono",ui-monospace,monospace!important;font-size:14px!important;line-height:1!important;font-weight:900!important;letter-spacing:.13em!important;text-transform:uppercase!important;text-align:center!important;text-decoration:none!important;white-space:nowrap!important;overflow:hidden!important;}
.btn:after,.btn:before,a.btn:after,button.btn:after,.btn-secondary:after,.btn-secondary:before,.hero-ctas a:after,.ctas a:after{content:none!important;display:none!important;}

/* Somente reserva / TagMe fica laranja */
.hero-ctas a[href*="tagme"],.hero-ctas a[href*="reserv"],.ctas a[href*="tagme"],.ctas a[href*="reserv"],a.btn[href*="tagme"],a.btn[href*="reserv"],.bnav-reservar{border:1px solid var(--amarelo,#f59b1e)!important;background:var(--amarelo,#f59b1e)!important;color:#fff!important;box-shadow:0 9px 0 rgba(0,64,90,.20),0 16px 30px rgba(0,32,46,.18)!important;}

/* Demais botões ficam vazados; no hover invertem */
.hero-ctas a:not([href*="tagme"]):not([href*="reserv"]),.ctas a:not([href*="tagme"]):not([href*="reserv"]),.hero-ctas button:not([data-primary]),.ctas button:not([data-primary]),.btn-secondary,a.btn-secondary{color:var(--areia-pale,#f6efde)!important;border:1px solid rgba(246,239,222,.82)!important;background:rgba(0,32,46,.18)!important;box-shadow:inset 0 0 0 1px rgba(246,239,222,.08),0 10px 26px rgba(0,32,46,.18)!important;backdrop-filter:blur(6px)!important;-webkit-backdrop-filter:blur(6px)!important;}
.hero-ctas a:not([href*="tagme"]):not([href*="reserv"]):hover,.ctas a:not([href*="tagme"]):not([href*="reserv"]):hover,.btn-secondary:hover,a.btn-secondary:hover{background:rgba(246,239,222,.94)!important;border-color:rgba(246,239,222,.98)!important;color:var(--azul1,#00405a)!important;box-shadow:0 12px 28px rgba(0,32,46,.24)!important;}

/* Topo: reservar permanece laranja, sem seta */
nav.top .btn,nav.top a.btn[href*="tagme"]{min-height:60px!important;height:60px!important;width:188px!important;min-width:188px!important;padding:0!important;letter-spacing:.16em!important;border:1px solid var(--amarelo,#f59b1e)!important;background:var(--amarelo,#f59b1e)!important;color:#fff!important;}

/* Frames/pílulas acima dos botões no padrão home */
header.hero .hero-chips,header.page-hero .hero-chips{display:flex!important;flex-wrap:wrap!important;align-items:center!important;gap:8px!important;margin:0!important;border:0!important;outline:0!important;box-shadow:none!important;}
header.hero .hero-chips span,header.hero .hero-chips a,header.page-hero .hero-chips span,header.page-hero .hero-chips a{min-height:36px!important;height:36px!important;padding:0 17px!important;border-radius:999px!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;gap:7px!important;background:rgba(0,32,46,.46)!important;border:1px solid rgba(246,239,222,.30)!important;color:var(--areia-pale,#f6efde)!important;box-shadow:0 8px 22px rgba(0,32,46,.14)!important;backdrop-filter:blur(7px)!important;-webkit-backdrop-filter:blur(7px)!important;font-family:Catamaran,Verdana,system-ui,sans-serif!important;font-size:14px!important;line-height:1!important;font-weight:700!important;text-decoration:none!important;white-space:nowrap!important;}

/* Blindagem contra molduras cinzas */
header.hero,header.page-hero,header.hero .hero-content,header.page-hero .page-hero-content,header.hero .hero-photo,header.page-hero .page-hero-photo,header.hero .hero-overlay,header.page-hero .page-hero-overlay{border:0!important;outline:0!important;box-shadow:none!important;}

@media(max-width:960px){.hero-ctas a,.hero-ctas button,.ctas a,.ctas button,.btn,a.btn,button.btn,.btn-secondary,a.btn-secondary{min-height:54px!important;height:54px!important;padding:0 24px!important;font-size:12px!important;letter-spacing:.10em!important;}nav.top .btn,nav.top a.btn[href*="tagme"]{width:auto!important;min-width:124px!important;height:46px!important;min-height:46px!important;font-size:9.5px!important;}header.hero .hero-chips span,header.hero .hero-chips a,header.page-hero .hero-chips span,header.page-hero .hero-chips a{height:34px!important;min-height:34px!important;padding:0 13px!important;font-size:12px!important;}}
</style>
''' + CSS_END

COUNTERS = {'html_scanned':0,'html_updated':0,'css_injected':0,'button_arrows_removed':0,'pins_removed':0,'audit_pass':0,'audit_warn':0}
DETAILS = []
ACTIONS = []

def is_html(p):
    rel = p.relative_to(ROOT).as_posix()
    return p.suffix.lower()=='.html' and not rel.startswith('_') and '.git' not in p.parts and rel not in SKIP

def remove_arrows(text, rel):
    count = 0
    def repl(m):
        nonlocal count
        old = m.group(0)
        new = ARROW_RE.sub(' ', old)
        new = re.sub(r'\s+</','</',new)
        new = re.sub(r'>\s+','>',new)
        new = re.sub(r'\s{2,}',' ',new)
        if new != old: count += 1
        return new
    text = BTN_RE.sub(repl, text)
    if count:
        COUNTERS['button_arrows_removed'] += count
        ACTIONS.append(f'BUTTON_ARROWS_REMOVED: {rel} ({count})')
    return text

def process(p):
    if not is_html(p): return
    rel = p.relative_to(ROOT).as_posix()
    COUNTERS['html_scanned'] += 1
    original = p.read_text(encoding='utf-8', errors='ignore')
    text, pin_count = PIN_RE.subn('', original)
    if pin_count:
        COUNTERS['pins_removed'] += pin_count
        ACTIONS.append(f'PINS_REMOVED: {rel} ({pin_count})')
    text = remove_arrows(text, rel)
    before = text
    text = CSS_RE.sub('\n', text)
    if HEAD_CLOSE_RE.search(text):
        text = HEAD_CLOSE_RE.sub(CSS_BLOCK + '\n</head>', text, count=1)
    if text != before:
        COUNTERS['css_injected'] += 1
        ACTIONS.append(f'CSS_LOCK: {rel}')
    if text != original:
        p.write_text(text, encoding='utf-8')
        COUNTERS['html_updated'] += 1

def button_arrow_exists(text):
    return any(ARROW_RE.search(m.group(0)) for m in BTN_RE.finditer(text))

def audit(p):
    if not is_html(p): return
    rel = p.relative_to(ROOT).as_posix()
    text = p.read_text(encoding='utf-8', errors='ignore')
    compact = text.replace(' ','')
    has_hero = bool(HERO_RE.search(text))
    checks = {
        'design_lock_present':'ec-final-design-consistency-lock' in text,
        'no_button_arrows':not button_arrow_exists(text),
        'primary_only_reserve_or_tagme':'Somente reserva / TagMe fica laranja' in text,
        'secondary_buttons_invert_on_hover':':hover' in text and 'rgba(246,239,222,.94)' in text,
        'chips_home_standard_lock':(not has_hero) or ('height:36px!important' in compact and 'hero-chips' in text),
        'no_pin_icon_residual':not PIN_RE.search(text),
        'no_gray_frame_lock':'border:0!important' in compact and 'box-shadow:none!important' in compact,
        'hero_line_same_position':(not has_hero) or ('top:96px!important' in compact and 'left:clamp(78px,5.5vw,112px)!important' in compact and 'transform:none!important' in compact),
    }
    status = 'PASS' if all(checks.values()) else 'WARN'
    COUNTERS['audit_pass' if status=='PASS' else 'audit_warn'] += 1
    DETAILS.append({'page':rel,'status':status,'has_hero':has_hero,**checks})

def write_reports():
    REPORT_DIR.mkdir(exist_ok=True)
    warn = [d for d in DETAILS if d['status']=='WARN']
    lines = ['# Final Design Consistency Lock','','## Objetivo','Padronizar linha laranja, botões, frames/pílulas acima dos botões e remover setas/pins residuais. Regra de botão: apenas reserva/TagMe fica laranja; os demais são vazados e invertem no hover.','','## Veredito',f'- Páginas auditadas: {len(DETAILS)}',f'- PASS: {len(DETAILS)-len(warn)}',f'- WARN: {len(warn)}',f"- Status geral: {'PASS' if not warn else 'WARN'}",'','## Contadores']
    lines += [f'- {k}: {v}' for k,v in COUNTERS.items()]
    lines += ['', '## Páginas com WARN']
    if warn:
        for d in warn:
            failed = [k for k,v in d.items() if isinstance(v,bool) and not v]
            lines.append(f"- {d['page']}: {', '.join(failed)}")
    else:
        lines.append('- Nenhuma.')
    lines += ['', '## Ações aplicadas']
    lines += [f'- {a}' for a in ACTIONS] if ACTIONS else ['- Nenhuma alteração necessária.']
    lines += ['', '## Observação', 'Auditoria estática; validar pixels no navegador pós-deploy com cache limpo.', '']
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
