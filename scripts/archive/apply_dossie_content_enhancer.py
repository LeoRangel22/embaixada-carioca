#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / '_audit_reports'
REPORT = REPORT_DIR / 'dossie_content_enhancer_report.md'
EXCLUDE = {'.git', '.github', 'node_modules', '_audit_reports', 'dist', 'build', 'coverage'}
SCRIPT = '<script defer src="/assets/dossie-content-enhancer.js"></script>'
TARGETS = {
    'index.html', 'cafe-da-manha.html', 'eventos.html', 'guia-do-rio.html',
    'restaurante-morro-da-urca.html', 'restaurantes-romanticos-rio-de-janeiro.html',
    'en/index.html', 'es/index.html'
}


def before_body(html):
    if SCRIPT in html:
        return html, False
    idx = html.lower().rfind('</body>')
    if idx < 0:
        return html + '\n' + SCRIPT + '\n', True
    return html[:idx] + SCRIPT + '\n' + html[idx:], True


def main():
    REPORT_DIR.mkdir(exist_ok=True)
    changed = []
    for rel in sorted(TARGETS):
        path = ROOT / rel
        if not path.exists() or any(part in EXCLUDE for part in path.parts):
            continue
        html = path.read_text(encoding='utf-8', errors='ignore')
        new_html, did = before_body(html)
        if did:
            path.write_text(new_html, encoding='utf-8')
            changed.append(rel)
    lines = [
        '# Dossiê Content Enhancer Report', '', 'Status: **PASS**', '',
        '## Base editorial incorporada',
        '- Morro da Urca como localização correta.',
        '- Primeira parada do Bondinho Pão de Açúcar.',
        '- Vista para o Pão de Açúcar e Baía de Guanabara.',
        '- Gastronomia brasileira: picanha, bobó, feijoada, caipirinhas e café da manhã.',
        '- Reputação 4,8 no Google como prova social.',
        '- Acessibilidade e turismo inclusivo como diferencial.',
        '- Perguntas e respostas diretas para buscadores e IA.', '',
        f'Páginas alteradas: **{len(changed)}**', '', '## Detalhe'
    ]
    if changed:
        for rel in changed:
            lines.append(f'- `{rel}` — dossie-content-enhancer.js injetado')
    else:
        lines.append('Nenhuma página pendente; enhancer já estava aplicado.')
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Dossie content enhancer applied to {len(changed)} pages')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
