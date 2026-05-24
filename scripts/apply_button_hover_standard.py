#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOVER_CSS = """
/* EC global button hover standard */
a.btn:hover,.btn:hover,a.btn:focus-visible,.btn:focus-visible{
  background:var(--azul,#00405a)!important;
  border-color:var(--azul,#00405a)!important;
  color:var(--amarelo,#f59b1e)!important;
  -webkit-text-fill-color:var(--amarelo,#f59b1e)!important;
  transform:translateY(-1px);
}
a.btn.secondary:hover,.btn.secondary:hover,a.btn.secondary:focus-visible,.btn.secondary:focus-visible,
a.btn.ghost:hover,.btn.ghost:hover,a.btn.ghost:focus-visible,.btn.ghost:focus-visible{
  background:var(--paper,var(--areia-pale,#f6efde))!important;
  border-color:var(--paper,var(--areia-pale,#f6efde))!important;
  color:var(--azul,#00405a)!important;
  -webkit-text-fill-color:var(--azul,#00405a)!important;
}
""".strip()

TARGETS = [
    ROOT / 'eventos.html',
    ROOT / 'index.html',
    ROOT / 'almoco.html',
    ROOT / 'cafe-da-manha.html',
    ROOT / 'cardapio.html',
]

for path in TARGETS:
    if not path.exists():
        continue
    html = path.read_text(encoding='utf-8', errors='ignore')
    if 'EC global button hover standard' in html:
        print(f'ok already patched: {path.relative_to(ROOT)}')
        continue
    marker = '</style>'
    if marker not in html:
        print(f'skip no style block: {path.relative_to(ROOT)}')
        continue
    html = html.replace(marker, f'\n{HOVER_CSS}\n{marker}', 1)
    path.write_text(html, encoding='utf-8')
    print(f'patched: {path.relative_to(ROOT)}')
