#!/usr/bin/env python3
"""
Valida sincronização PT/EN/ES entre os HTML do site Embaixada Carioca.

Checks:
  1. Para cada arquivo PT (raiz), verifica se existe equivalente em /en/ e /es/.
  2. Para arquivos que existem nos 3 idiomas, verifica:
     a. Se os hreflang tags apontam para os URLs corretos.
     b. Se o número de headings principais (h1, h2) é similar (±1).
  3. Gera relatório em _audit_reports/i18n_sync_report.md
  4. Retorna exit code 1 se houver páginas PT sem equivalente EN ou ES.

Uso: python scripts/validate_i18n_sync.py
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Mapeamento de slugs PT → EN/ES para páginas com slugs diferentes por design
SLUG_MAPPING_EN = {
    'entardecer.html': 'sunset.html',
    'como-chegar.html': 'how-to-get-there.html',
}
SLUG_MAPPING_ES = {
    'entardecer.html': 'atardecer.html',
    'como-chegar.html': 'como-llegar.html',
}


ROOT = Path(__file__).parent.parent

# Diretórios de cada idioma
DIRS = {
    "pt": ROOT,
    "en": ROOT / "en",
    "es": ROOT / "es",
}

# URLs base por idioma
BASE_URLS = {
    "pt": "https://www.embaixadacarioca.com",
    "en": "https://www.embaixadacarioca.com/en",
    "es": "https://www.embaixadacarioca.com/es",
}

# Arquivos a ignorar (infraestrutura, não conteúdo)
# Inclui: páginas de sistema, páginas de redirect e páginas PT-only por design estratégico
IGNORE_FILES = {
    "404.html",
    "offline.html",
    "contato.html",
    "nossa-visao.html",
    # Páginas PT-only: landing pages estratégicas sem versão EN/ES por design
    "restaurante-morro-da-urca.html",
    "onde-comer-no-pao-de-acucar.html",
    "restaurante-bondinho-pao-de-acucar.html",
    "parque-bondinho-pao-de-acucar.html",
    "restaurantes-perto-do-pao-de-acucar.html",
    "restaurantes-romanticos-rio-de-janeiro.html",
    "cafe-da-manha-com-vista-rio-de-janeiro.html",
    "como-chegar.html",
}

# Mapeamento de nome de arquivo para slug canônico (sem extensão, sem path)
def slug(filename):
    return Path(filename).stem


def list_html_files(directory):
    """Lista todos os HTML em um diretório (não recursivo)."""
    d = Path(directory)
    if not d.exists():
        return []
    return sorted([
        f.name for f in d.iterdir()
        if f.suffix == ".html" and f.name not in IGNORE_FILES and not f.name.startswith("_")
    ])


def extract_hreflang(content):
    """Extrai todos os hreflang do conteúdo HTML."""
    pattern = r'<link[^>]+hreflang=["\']([^"\']+)["\'][^>]+href=["\']([^"\']+)["\'][^>]*/?>|<link[^>]+href=["\']([^"\']+)["\'][^>]+hreflang=["\']([^"\']+)["\'][^>]*/?>'
    result = {}
    for m in re.finditer(pattern, content, re.IGNORECASE):
        if m.group(1):
            result[m.group(1)] = m.group(2)
        elif m.group(4):
            result[m.group(4)] = m.group(3)
    return result


def count_headings(content, tags=("h1", "h2")):
    """Conta o número de tags de heading no conteúdo."""
    count = 0
    for tag in tags:
        count += len(re.findall(rf"<{tag}[\s>]", content, re.IGNORECASE))
    return count


def expected_hreflang_url(filename, lang):
    """Calcula a URL canônica esperada para um arquivo em um dado idioma."""
    base = BASE_URLS[lang]
    # index.html -> /  ou  /en/  ou  /es/
    if filename == "index.html":
        return base + "/"
    # Usar mapeamento de slug para idiomas com slug diferente por design
    if lang == "en" and filename in SLUG_MAPPING_EN:
        return f"{base}/{SLUG_MAPPING_EN[filename]}"
    if lang == "es" and filename in SLUG_MAPPING_ES:
        return f"{base}/{SLUG_MAPPING_ES[filename]}"
    return f"{base}/{filename}"


def check_hreflang(content, filename, lang, issues):
    """Verifica se os hreflang tags apontam para os URLs corretos."""
    hreflang = extract_hreflang(content)
    if not hreflang:
        issues.append(f"    - Sem hreflang tags")
        return

    # Verifica PT, EN, ES e x-default
    expected = {
        "pt-BR": expected_hreflang_url(filename, "pt"),
        "en": expected_hreflang_url(filename, "en"),
        "es": expected_hreflang_url(filename, "es"),
        "x-default": expected_hreflang_url(filename, "pt"),
    }
    for lang_code, expected_url in expected.items():
        if lang_code not in hreflang:
            issues.append(f"    - Faltando hreflang '{lang_code}'")
        elif hreflang[lang_code].rstrip("/") != expected_url.rstrip("/"):
            issues.append(
                f"    - hreflang '{lang_code}': esperado '{expected_url}', encontrado '{hreflang[lang_code]}'"
            )


def run_validation():
    pt_files = list_html_files(DIRS["pt"])
    en_files = list_html_files(DIRS["en"])
    es_files = list_html_files(DIRS["es"])

    en_set = set(en_files)
    es_set = set(es_files)

    lines = []
    lines.append("# Relatório de Sincronização i18n PT/EN/ES")
    lines.append(f"\nGerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append(f"- PT: {len(pt_files)} arquivos")
    lines.append(f"- EN: {len(en_files)} arquivos")
    lines.append(f"- ES: {len(es_files)} arquivos\n")

    missing_en = []
    missing_es = []
    hreflang_issues = {}
    heading_issues = {}

    for filename in pt_files:
        has_en = filename in en_set
        has_es = filename in es_set

        if not has_en:
            missing_en.append(filename)
        if not has_es:
            missing_es.append(filename)

        # Se existir nos 3 idiomas, verifica hreflang e headings
        if has_en and has_es:
            file_issues = []

            # Ler arquivos
            contents = {}
            for lang, d in DIRS.items():
                path = d / filename
                if path.exists():
                    try:
                        with open(path, encoding="utf-8", errors="replace") as f:
                            contents[lang] = f.read()
                    except Exception as e:
                        file_issues.append(f"    - Erro ao ler {lang}/{filename}: {e}")

            # Verificar hreflang em cada idioma
            for lang, content in contents.items():
                lang_issues = []
                check_hreflang(content, filename, lang, lang_issues)
                if lang_issues:
                    file_issues.extend([f"    [{lang.upper()}] {i.strip()}" for i in lang_issues])

            # Verificar headings
            heading_counts = {lang: count_headings(c) for lang, c in contents.items()}
            if len(heading_counts) == 3:
                counts = list(heading_counts.values())
                min_c, max_c = min(counts), max(counts)
                if max_c - min_c > 1:
                    file_issues.append(
                        f"    - Headings (h1+h2) desbalanceados: "
                        f"PT={heading_counts.get('pt',0)}, "
                        f"EN={heading_counts.get('en',0)}, "
                        f"ES={heading_counts.get('es',0)} (diferença > 1)"
                    )

            if file_issues:
                hreflang_issues[filename] = file_issues

    # Seção: páginas PT sem EN
    lines.append("## Páginas PT sem equivalente EN\n")
    if missing_en:
        for f in missing_en:
            lines.append(f"- `{f}`")
    else:
        lines.append("_Nenhuma. Todas as páginas PT têm equivalente EN._")

    # Seção: páginas PT sem ES
    lines.append("\n## Páginas PT sem equivalente ES\n")
    if missing_es:
        for f in missing_es:
            lines.append(f"- `{f}`")
    else:
        lines.append("_Nenhuma. Todas as páginas PT têm equivalente ES._")

    # Seção: problemas de hreflang e headings
    lines.append("\n## Problemas de hreflang e headings (páginas existentes nos 3 idiomas)\n")
    if hreflang_issues:
        for filename, issues in sorted(hreflang_issues.items()):
            lines.append(f"### `{filename}`\n")
            for issue in issues:
                lines.append(issue)
            lines.append("")
    else:
        lines.append("_Nenhum problema encontrado._")

    # Seção: resumo
    total_issues = len(missing_en) + len(missing_es) + len(hreflang_issues)
    lines.append("\n## Resumo\n")
    lines.append(f"| Métrica | Valor |")
    lines.append(f"|---------|-------|")
    lines.append(f"| Páginas PT | {len(pt_files)} |")
    lines.append(f"| PT sem EN | {len(missing_en)} |")
    lines.append(f"| PT sem ES | {len(missing_es)} |")
    lines.append(f"| Com problemas hreflang/headings | {len(hreflang_issues)} |")
    lines.append(f"| Total de issues | {total_issues} |")

    report = "\n".join(lines) + "\n"

    # Escrever relatório
    audit_dir = ROOT / "_audit_reports"
    audit_dir.mkdir(exist_ok=True)
    report_path = audit_dir / "i18n_sync_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Relatório gerado: {report_path}")
    print(f"  PT: {len(pt_files)} arquivos")
    print(f"  EN: {len(en_files)} arquivos")
    print(f"  ES: {len(es_files)} arquivos")
    print(f"  PT sem EN: {len(missing_en)}")
    print(f"  PT sem ES: {len(missing_es)}")
    print(f"  Problemas hreflang/headings: {len(hreflang_issues)}")

    # Exit code 1 se houver páginas PT sem EN ou ES
    if missing_en or missing_es:
        print(f"\nFAIL: {len(missing_en)} PT sem EN, {len(missing_es)} PT sem ES", file=sys.stderr)
        sys.exit(1)
    else:
        print("\nOK: todas as páginas PT têm equivalentes EN e ES.")


if __name__ == "__main__":
    run_validation()
