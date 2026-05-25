#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
OUT.mkdir(exist_ok=True)
MD = OUT / 'language_quality_pt_en_es_audit.md'
JSON_OUT = OUT / 'language_quality_pt_en_es_audit.json'

TARGETS = [p for p in ROOT.rglob('*.html') if not any(part.startswith('.') or part in {'node_modules', 'dist', 'build', '_audit_reports'} for part in p.relative_to(ROOT).parts)]

RULES = [
    ('english_bad_breakfast', re.compile(r'\bDo breakfast\b', re.I), 'Use “Breakfast” or “Have breakfast”, not “Do breakfast”.'),
    ('spanish_del_artifact', re.compile(r'(^|[\s>])del([\s<]|$)', re.I), 'Review “del” when it appears as an isolated artifact or mixed-language leftover.'),
    ('portuguese_autoguiada', re.compile(r'\bautoguiada\b', re.I), 'Use “auto-guiada”.'),
    ('wrong_top_location_pt', re.compile(r'topo do pão de açúcar', re.I), 'Use Morro da Urca / primeira parada do Bondinho, not topo do Pão de Açúcar.'),
    ('wrong_top_location_en', re.compile(r'top of sugarloaf', re.I), 'Use Urca Hill / first cable car stop, not top of Sugarloaf.'),
    ('wrong_top_location_es', re.compile(r'cima del pan de azúcar|cima do pão de açúcar', re.I), 'Use Morro da Urca / primera parada del Bondinho.'),
]

TAG_RE = re.compile(r'<[^>]+>')
SCRIPT_STYLE = re.compile(r'<script.*?</script>|<style.*?</style>', re.I | re.S)


def visible_text(html):
    html = SCRIPT_STYLE.sub(' ', html)
    text = TAG_RE.sub(' ', html)
    return re.sub(r'\s+', ' ', text).strip()


def main():
    findings = []
    for path in TARGETS:
        rel = path.relative_to(ROOT).as_posix()
        html = path.read_text(encoding='utf-8', errors='ignore')
        text = visible_text(html)
        for code, pattern, suggestion in RULES:
            for match in pattern.finditer(text):
                start = max(0, match.start() - 80)
                end = min(len(text), match.end() + 80)
                findings.append({
                    'page': rel,
                    'rule': code,
                    'match': match.group(0),
                    'context': text[start:end],
                    'suggestion': suggestion,
                })
    status = 'PASS' if not findings else 'FAIL'
    JSON_OUT.write_text(json.dumps({'status': status, 'findings': findings}, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# PT EN ES Language Quality Audit', '', f'Status geral: **{status}**', f'Findings: **{len(findings)}**', '', '## Regras auditadas', '- “Do breakfast” em inglês.', '- Artefatos de “del” em espanhol/mistura de idioma.', '- “autoguiada” vs “auto-guiada”.', '- Menções erradas a topo do Pão de Açúcar / top of Sugarloaf.', '', '## Achados']
    if not findings:
        lines.append('- Nenhum achado crítico.')
    else:
        for item in findings[:200]:
            lines.append(f"- `{item['page']}` — {item['rule']} — `{item['match']}`")
            lines.append(f"  - Sugestão: {item['suggestion']}")
            lines.append(f"  - Contexto: {item['context']}")
    MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Language quality audit PT EN ES: {status} findings={len(findings)}')
    return 0 if status == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
