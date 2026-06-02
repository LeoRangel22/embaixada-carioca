#!/usr/bin/env python3
"""
apply_fase1_higiene.py — Fase 1: Higiene de Código
Embaixada Carioca (www.embaixadacarioca.com)

Correções aplicadas (todas idempotentes e seguras):
  T-1.1  Remoção de duplicações de CSS e JS
  T-1.2  Otimização de títulos longos (>60 chars) — PT, EN, ES
  T-1.3  Otimização de meta descriptions longas (>160 chars)
  T-1.4  Implementação de hreflang faltante (cafe-da-manha-com-vista)
  T-1.5  Configuração de srcset em imagens com variantes disponíveis
  T-1.6  Atualização de <lastmod> no sitemap.xml

Segurança:
  - Backup automático de todos os arquivos modificados em _backups/fase1/
  - Modo dry-run via --dry-run (simula sem gravar)
  - Relatório detalhado em _audit_reports/fase1_higiene_report.md
  - Idempotente: pode ser executado múltiplas vezes sem efeito colateral

Uso:
  python3 scripts/apply_fase1_higiene.py            # aplica tudo
  python3 scripts/apply_fase1_higiene.py --dry-run  # simula sem gravar
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
import xml.etree.ElementTree as ET

# ─────────────────────────────────────────────────────────────
# Caminhos raiz
# ─────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / "_backups" / "fase1"
REPORT_DIR = ROOT / "_audit_reports"
REPORT_PATH = REPORT_DIR / "fase1_higiene_report.md"
TODAY = date.today().isoformat()  # ex: "2026-06-02"

# ─────────────────────────────────────────────────────────────
# T-1.1 — Recursos duplicados a remover (CSS e JS)
# ─────────────────────────────────────────────────────────────
# Mapeamento: arquivo → lista de recursos que aparecem 2x e devem ter
# a segunda ocorrência removida.
DUPLICATE_RESOURCES: dict[str, list[str]] = {
    "index.html": [
        "/assets/css/ec-contrast-fixes.css",
        "/assets/dossie-content-enhancer.js",
    ],
    "almoco.html":                    ["/assets/css/ec-contrast-fixes.css"],
    "cafe-da-manha.html":             ["/assets/css/ec-contrast-fixes.css"],
    "cardapio.html":                  ["/assets/css/ec-contrast-fixes.css"],
    "como-chegar.html":               ["/assets/css/ec-contrast-fixes.css"],
    "guia-do-rio.html":               ["/assets/css/ec-contrast-fixes.css"],
    "restaurante-morro-da-urca.html": ["/assets/css/ec-contrast-fixes.css"],
}

# ─────────────────────────────────────────────────────────────
# T-1.2 — Títulos otimizados (PT, EN, ES)
# ─────────────────────────────────────────────────────────────
TITLE_FIXES: dict[str, str] = {
    # PT
    "index.html":
        "Embaixada Carioca | Restaurante no Morro da Urca com Vista",
    "morro-da-urca.html":
        "Morro da Urca | Restaurante Embaixada Carioca com Vista",
    "restaurantes-romanticos-rio-de-janeiro.html":
        "Restaurante Romântico no Rio com Vista | Embaixada Carioca",
    "almoco-morro-da-urca.html":
        "Onde Almoçar no Morro da Urca | Embaixada Carioca",
    "parque-bondinho-pao-de-acucar.html":
        "Onde Comer no Parque Bondinho Pão de Açúcar | Embaixada",
    "cafe-da-manha.html":
        "Café da Manhã no Morro da Urca | Embaixada Carioca",
    "por-do-sol-morro-da-urca.html":
        "Pôr do Sol no Morro da Urca | Embaixada Carioca",
    "roteiro-meio-dia-urca-pao-de-acucar.html":
        "Roteiro de Meio Dia na Urca | Embaixada Carioca",
    "cafe-da-manha-com-vista-rio-de-janeiro.html":
        "Café da Manhã com Vista no Rio | Embaixada Carioca",
    # EN
    "en/index.html":
        "Brazilian Restaurant at Urca Hill with Sugarloaf View | Embaixada",
    "en/almoco-morro-da-urca.html":
        "Where to Lunch at Morro da Urca | Embaixada Carioca",
    "en/cafe-da-manha.html":
        "Breakfast at Urca Hill with Sugarloaf View | Embaixada",
    # ES
    "es/por-do-sol-morro-da-urca.html":
        "Atardecer en el Pan de Azúcar y Morro da Urca | Embaixada",
    "es/como-llegar.html":
        "Cómo Llegar al Pan de Azúcar y Morro da Urca | Embaixada",
    "es/eventos.html":
        "Eventos con Vista en Río de Janeiro | Embaixada Carioca",
    "es/gastronomia-carioca.html":
        "Gastronomía Carioca: Platos Típicos y Dónde Comer | 2026",
    "es/guia-do-rio.html":
        "Guía de Río: Morro da Urca y Pan de Azúcar | Embaixada",
    "es/nossa-visao.html":
        "Nuestra Visión | Embaixada Carioca — Restaurante Urca",
    "es/parque-bondinho-pan-de-azucar.html":
        "Parque Bondinho Pan de Azúcar: dónde comer en Morro da Urca",
    "es/parque-bondinho.html":
        "Parque Bondinho Pão de Açúcar | Restaurante Embaixada",
    "es/restaurante-morro-da-urca.html":
        "Restaurante en Morro da Urca con Vista al Pan de Azúcar",
    # EN — páginas adicionais
    "en/caipirinha-com-vista-rio.html":
        "Caipirinha in Rio with a View | Embaixada Carioca",
    "en/eventos.html":
        "Events with a View in Rio de Janeiro | Embaixada Carioca",
    "en/gastronomia-carioca.html":
        "Carioca Gastronomy: Typical Dishes & Where to Eat | 2026",
    "en/guia-do-rio.html":
        "Rio Guide: Urca Hill & Sugarloaf | Embaixada Carioca",
    "en/how-to-get-there.html":
        "How to Get to Sugarloaf Cable Car Park | Embaixada Carioca",
    "en/index.html":
        "Brazilian Restaurant at Urca Hill with Sugarloaf View",
}

# ─────────────────────────────────────────────────────────────
# T-1.3 — Meta descriptions otimizadas
# ─────────────────────────────────────────────────────────────
DESCRIPTION_FIXES: dict[str, str] = {
    "parque-bondinho-pao-de-acucar.html": (
        "Onde comer no Pão de Açúcar? A Embaixada Carioca fica no Morro da Urca "
        "(Parque Bondinho) e serve café da manhã, almoço e feijoada premiada com vista direta."
    ),
    "parque-bondinho.html": (
        "Saiba como acessar a Embaixada Carioca no Parque Bondinho: subida de "
        "bondinho com ingresso ou pela Trilha do Morro da Urca. Veja dicas de acesso."
    ),
    "es/o-que-fazer-depois-do-bondinho-pao-de-acucar.html": (
        "Qué hacer después del teleférico del Parque Bondinho: restaurantes, playas "
        "y actividades en Río de Janeiro. Guía completa para turistas."
    ),
    "en/eventos.html": (
        "Corporate events and celebrations at Morro da Urca inside Sugarloaf Cable Car Park, "
        "with Brazilian food and panoramic views. Request a quote."
    ),
}

# ─────────────────────────────────────────────────────────────
# T-1.4 — Hreflang faltante
# ─────────────────────────────────────────────────────────────
HREFLANG_FIXES: dict[str, list[tuple[str, str]]] = {
    "cafe-da-manha-com-vista-rio-de-janeiro.html": [
        ("pt-BR",    "https://www.embaixadacarioca.com/cafe-da-manha-com-vista-rio-de-janeiro.html"),
        ("en",       "https://www.embaixadacarioca.com/en/cafe-da-manha-com-vista-rio-de-janeiro.html"),
        ("es",       "https://www.embaixadacarioca.com/es/cafe-da-manha-com-vista-rio-de-janeiro.html"),
        ("x-default","https://www.embaixadacarioca.com/cafe-da-manha-com-vista-rio-de-janeiro.html"),
    ],
}

# ─────────────────────────────────────────────────────────────
# T-1.5 — Srcset para imagens com variantes disponíveis no repo
# ─────────────────────────────────────────────────────────────
# Mapeamento: src original → (srcset, sizes)
SRCSET_FIXES: dict[str, tuple[str, str]] = {
    "/assets/hero.webp": (
        "/assets/hero-400w.webp 400w, /assets/hero-800w.webp 800w, /assets/hero-1200w.webp 1200w",
        "100vw",
    ),
    "assets/hero.webp": (
        "/assets/hero-400w.webp 400w, /assets/hero-800w.webp 800w, /assets/hero-1200w.webp 1200w",
        "100vw",
    ),
    "/assets/cafe-da-manha-mesa-opt.webp": (
        "/assets/cafe-da-manha-mesa-opt-400w.webp 400w, /assets/cafe-da-manha-mesa-opt-800w.webp 800w",
        "(max-width: 600px) 400px, (max-width: 1024px) 800px, 560px",
    ),
    "/assets/gin-tonic-vista.webp": (
        "/assets/gin-tonic-vista-400w.webp 400w, /assets/gin-tonic-vista-800w.webp 800w",
        "(max-width: 600px) 400px, (max-width: 1024px) 800px, 560px",
    ),
    "/assets/fabio-almoco-salmao-pao-acucar.webp": (
        "/assets/fabio-almoco-salmao-pao-acucar-400w.webp 400w, /assets/fabio-almoco-salmao-pao-acucar-800w.webp 800w",
        "(max-width: 600px) 400px, (max-width: 1024px) 800px, 800px",
    ),
    "assets/fabio-almoco-salmao-pao-acucar.webp": (
        "/assets/fabio-almoco-salmao-pao-acucar-400w.webp 400w, /assets/fabio-almoco-salmao-pao-acucar-800w.webp 800w",
        "(max-width: 600px) 400px, (max-width: 1024px) 800px, 800px",
    ),
}

# ─────────────────────────────────────────────────────────────
# Resultado por arquivo
# ─────────────────────────────────────────────────────────────
@dataclass
class FileResult:
    rel: str
    changed: bool = False
    t11_removed_css: int = 0
    t11_removed_js: int = 0
    t12_title_fixed: bool = False
    t13_desc_fixed: bool = False
    t14_hreflang_added: int = 0
    t15_srcset_added: int = 0
    errors: list[str] = field(default_factory=list)


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
def backup(path: Path) -> None:
    """Copia o arquivo original para _backups/fase1/ antes de modificar."""
    dest = BACKUP_DIR / path.relative_to(ROOT)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        shutil.copy2(path, dest)


def remove_duplicate_resource(source: str, resource: str) -> tuple[str, int]:
    """
    Remove a segunda (e subsequentes) ocorrências de um <link> ou <script>
    que referencie `resource`. A primeira ocorrência é preservada.
    Retorna (novo_source, quantidade_removida).
    """
    # Padrão para <link rel="stylesheet" href="...resource...">
    link_pattern = re.compile(
        r'[ \t]*<link\b[^>]*\bhref=["\']' + re.escape(resource) + r'["\'][^>]*>\s*\n?',
        re.IGNORECASE,
    )
    # Padrão para <script src="...resource..."></script>
    script_pattern = re.compile(
        r'[ \t]*<script\b[^>]*\bsrc=["\']' + re.escape(resource) + r'["\'][^>]*></script>\s*\n?',
        re.IGNORECASE,
    )

    removed = 0
    for pattern in (link_pattern, script_pattern):
        matches = list(pattern.finditer(source))
        if len(matches) > 1:
            # Remover da última para a primeira para não deslocar índices
            for m in reversed(matches[1:]):
                source = source[: m.start()] + source[m.end() :]
                removed += 1
    return source, removed


def fix_title(source: str, new_title: str) -> tuple[str, bool]:
    """Substitui o conteúdo da tag <title>. Retorna (novo_source, alterado)."""
    pattern = re.compile(r'(<title>)(.*?)(</title>)', re.IGNORECASE | re.DOTALL)
    m = pattern.search(source)
    if not m:
        return source, False
    current = m.group(2).strip()
    if current == new_title:
        return source, False
    new_source = pattern.sub(lambda _: f"{m.group(1)}{new_title}{m.group(3)}", source, count=1)
    return new_source, True


def fix_description(source: str, new_desc: str) -> tuple[str, bool]:
    """
    Substitui o content da meta description em TODAS as ocorrências.
    Suporta ambas as ordens: name-antes-content e content-antes-name.
    Retorna (novo_source, alterado).
    """
    changed = False

    # Padrão 1: <meta name="description" content="...">
    pattern1 = re.compile(
        r'(<meta\s+name=["\']description["\']\s+content=["\'])(.*?)(["\'])',
        re.IGNORECASE | re.DOTALL,
    )
    # Padrão 2: <meta content="..." name="description"/>
    pattern2 = re.compile(
        r'(<meta\s+content=["\'])(.*?)(["\'](?:[^>]*?)\s+name=["\']description["\'][^>]*>)',
        re.IGNORECASE | re.DOTALL,
    )

    for pat in (pattern1, pattern2):
        def _replacer(match: re.Match) -> str:
            nonlocal changed
            current = match.group(2).strip()
            if current == new_desc:
                return match.group(0)
            changed = True
            return f"{match.group(1)}{new_desc}{match.group(3)}"
        source = pat.sub(_replacer, source)

    return source, changed


def add_hreflang(source: str, hreflangs: list[tuple[str, str]]) -> tuple[str, int]:
    """
    Insere tags hreflang após a tag <link rel="canonical">.
    Não insere se já existirem tags hreflang no documento.
    Retorna (novo_source, quantidade_adicionada).
    """
    # Verificar se já existem hreflang
    if re.search(r'<link\b[^>]*\bhreflang=', source, re.IGNORECASE):
        return source, 0

    canonical_pattern = re.compile(
        r'(<link\s+[^>]*\brel=["\']canonical["\'][^>]*>)',
        re.IGNORECASE,
    )
    m = canonical_pattern.search(source)
    if not m:
        return source, 0

    tags = "\n".join(
        f'  <link rel="alternate" hreflang="{lang}" href="{href}">'
        for lang, href in hreflangs
    )
    new_source = source[: m.end()] + "\n" + tags + source[m.end() :]
    return new_source, len(hreflangs)


def add_srcset_to_img(source: str, img_src: str, srcset: str, sizes: str) -> tuple[str, int]:
    """
    Adiciona srcset e sizes a tags <img> com src igual a img_src,
    somente se ainda não tiverem srcset.
    Retorna (novo_source, quantidade_modificada).
    """
    # Regex que captura a tag <img> completa
    img_pattern = re.compile(r'<img\b[^>]*>', re.IGNORECASE | re.DOTALL)
    count = 0
    result = []
    last = 0

    for m in img_pattern.finditer(source):
        tag = m.group(0)
        # Verificar se este img tem o src alvo e não tem srcset
        src_match = re.search(r'\bsrc=["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if src_match and src_match.group(1) == img_src and 'srcset=' not in tag.lower():
            # Inserir srcset e sizes antes do fechamento >
            close = tag.rfind('>')
            insertion = f' srcset="{srcset}" sizes="{sizes}"'
            tag = tag[:close] + insertion + tag[close:]
            count += 1
        result.append(source[last: m.start()])
        result.append(tag)
        last = m.end()

    result.append(source[last:])
    return "".join(result), count


# ─────────────────────────────────────────────────────────────
# Processamento de um arquivo HTML
# ─────────────────────────────────────────────────────────────
def process_html(rel: str, dry_run: bool) -> FileResult:
    path = ROOT / rel
    result = FileResult(rel=rel)

    if not path.exists():
        result.errors.append(f"Arquivo não encontrado: {rel}")
        return result

    original = path.read_text(encoding="utf-8", errors="ignore")
    source = original

    # T-1.1 — Remover duplicações
    for resource in DUPLICATE_RESOURCES.get(rel, []):
        source, removed = remove_duplicate_resource(source, resource)
        if resource.endswith(".css"):
            result.t11_removed_css += removed
        else:
            result.t11_removed_js += removed

    # T-1.2 — Corrigir título
    if rel in TITLE_FIXES:
        source, changed = fix_title(source, TITLE_FIXES[rel])
        result.t12_title_fixed = changed

    # T-1.3 — Corrigir description
    if rel in DESCRIPTION_FIXES:
        source, changed = fix_description(source, DESCRIPTION_FIXES[rel])
        result.t13_desc_fixed = changed

    # T-1.4 — Adicionar hreflang
    if rel in HREFLANG_FIXES:
        source, added = add_hreflang(source, HREFLANG_FIXES[rel])
        result.t14_hreflang_added = added

    # T-1.5 — Adicionar srcset
    for img_src, (srcset, sizes) in SRCSET_FIXES.items():
        source, added = add_srcset_to_img(source, img_src, srcset, sizes)
        result.t15_srcset_added += added

    result.changed = source != original

    if result.changed and not dry_run:
        backup(path)
        path.write_text(source, encoding="utf-8")

    return result


# ─────────────────────────────────────────────────────────────
# T-1.6 — Atualizar sitemap.xml
# ─────────────────────────────────────────────────────────────
def process_sitemap(dry_run: bool) -> tuple[int, int]:
    """
    Adiciona <lastmod>TODAY</lastmod> em todas as URLs sem lastmod.
    Retorna (total_sem_lastmod, total_corrigido).
    """
    sitemap_path = ROOT / "sitemap.xml"
    if not sitemap_path.exists():
        return 0, 0

    # Usar manipulação de texto para preservar formatação original
    content = sitemap_path.read_text(encoding="utf-8")
    original = content

    # Padrão: <url> ... <loc>...</loc> sem <lastmod> ... </url>
    # Inserir <lastmod> após <loc>...</loc> quando não existir lastmod no bloco
    url_block_pattern = re.compile(
        r'(<url>)(.*?)(</url>)',
        re.DOTALL | re.IGNORECASE,
    )

    total_sem = 0
    total_fixed = 0

    def fix_url_block(m: re.Match) -> str:
        nonlocal total_sem, total_fixed
        block = m.group(2)
        if '<lastmod>' in block.lower():
            return m.group(0)  # já tem lastmod
        total_sem += 1
        # Inserir após </loc>
        loc_end = re.search(r'</loc>', block, re.IGNORECASE)
        if loc_end:
            new_block = (
                block[: loc_end.end()]
                + f"\n    <lastmod>{TODAY}</lastmod>"
                + block[loc_end.end() :]
            )
            total_fixed += 1
            return m.group(1) + new_block + m.group(3)
        return m.group(0)

    content = url_block_pattern.sub(fix_url_block, content)

    if content != original and not dry_run:
        backup(sitemap_path)
        sitemap_path.write_text(content, encoding="utf-8")

    return total_sem, total_fixed


# ─────────────────────────────────────────────────────────────
# Relatório Markdown
# ─────────────────────────────────────────────────────────────
def write_report(results: list[FileResult], sitemap_stats: tuple[int, int], dry_run: bool) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    mode = "DRY-RUN (simulação — nenhum arquivo foi modificado)" if dry_run else "APLICADO"

    lines += [
        f"# Relatório de Execução — Fase 1: Higiene de Código",
        f"**Data:** {TODAY}  ",
        f"**Modo:** {mode}  ",
        f"**Repositório:** LeoRangel22/embaixada-carioca",
        "",
        "---",
        "",
        "## Resumo Executivo",
        "",
    ]

    total_changed = sum(1 for r in results if r.changed)
    total_css = sum(r.t11_removed_css for r in results)
    total_js = sum(r.t11_removed_js for r in results)
    total_titles = sum(1 for r in results if r.t12_title_fixed)
    total_descs = sum(1 for r in results if r.t13_desc_fixed)
    total_hreflang = sum(r.t14_hreflang_added for r in results)
    total_srcset = sum(r.t15_srcset_added for r in results)
    sitemap_sem, sitemap_fixed = sitemap_stats

    lines += [
        f"| Métrica | Resultado |",
        f"| :--- | :--- |",
        f"| Arquivos HTML processados | {len(results)} |",
        f"| Arquivos HTML modificados | {total_changed} |",
        f"| CSS duplicados removidos (T-1.1) | {total_css} |",
        f"| JS duplicados removidos (T-1.1) | {total_js} |",
        f"| Títulos otimizados (T-1.2) | {total_titles} |",
        f"| Descriptions otimizadas (T-1.3) | {total_descs} |",
        f"| Tags hreflang adicionadas (T-1.4) | {total_hreflang} |",
        f"| Imagens com srcset adicionado (T-1.5) | {total_srcset} |",
        f"| URLs no sitemap sem lastmod (T-1.6) | {sitemap_sem} |",
        f"| URLs no sitemap corrigidas (T-1.6) | {sitemap_fixed} |",
        "",
        "---",
        "",
        "## Detalhamento por Arquivo",
        "",
        "| Arquivo | Modificado | CSS Dup. | JS Dup. | Título | Desc. | Hreflang | Srcset |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for r in results:
        changed_icon = "✅" if r.changed else "—"
        lines.append(
            f"| `{r.rel}` | {changed_icon} | {r.t11_removed_css or '—'} | "
            f"{r.t11_removed_js or '—'} | {'✅' if r.t12_title_fixed else '—'} | "
            f"{'✅' if r.t13_desc_fixed else '—'} | "
            f"{r.t14_hreflang_added if r.t14_hreflang_added else '—'} | "
            f"{r.t15_srcset_added if r.t15_srcset_added else '—'} |"
        )
        for err in r.errors:
            lines.append(f"| ⚠️ ERRO em `{r.rel}`: {err} | | | | | | | |")

    lines += [
        "",
        "---",
        "",
        "## Critérios de Validação",
        "",
        "Execute o script de auditoria para confirmar que todos os critérios foram atendidos:",
        "",
        "```bash",
        "python3 scripts/audit_fase1.py",
        "```",
        "",
        "Resultados esperados após a execução:",
        "",
        "- `grep -c \"ec-contrast-fixes.css\" index.html` → `1`",
        "- `grep -c \"dossie-content-enhancer.js\" index.html` → `1`",
        "- Títulos com problemas: `0`",
        "- Descriptions com problemas: `0`",
        "- URLs no sitemap sem lastmod: `0`",
        "",
    ]

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n  Relatório salvo em: {REPORT_PATH.relative_to(ROOT)}")


# ─────────────────────────────────────────────────────────────
# Coleta de todos os arquivos HTML a processar
# ─────────────────────────────────────────────────────────────
def collect_targets() -> list[str]:
    """
    Retorna todos os arquivos HTML do repositório que precisam de alguma
    das correções T-1.1 a T-1.5. Exclui 404.html e offline.html.
    """
    targets: set[str] = set()
    targets.update(DUPLICATE_RESOURCES.keys())
    targets.update(TITLE_FIXES.keys())
    targets.update(DESCRIPTION_FIXES.keys())
    targets.update(HREFLANG_FIXES.keys())

    # Para T-1.5 (srcset), precisamos varrer todos os HTMLs
    EXCLUDED_DIRS = {"_backups", "_audit_reports", "scripts", "node_modules", ".git"}
    for html_path in ROOT.glob("**/*.html"):
        rel = str(html_path.relative_to(ROOT))
        # Excluir pastas internas e páginas de erro
        if rel.split("/")[0] in EXCLUDED_DIRS:
            continue
        if rel in ("404.html", "offline.html"):
            continue
        content = html_path.read_text(encoding="utf-8", errors="ignore")
        for img_src in SRCSET_FIXES:
            if f'src="{img_src}"' in content or f"src='{img_src}'" in content:
                targets.add(rel)
                break

    return sorted(targets)


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fase 1: Higiene de Código — Embaixada Carioca"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula as correções sem modificar nenhum arquivo.",
    )
    args = parser.parse_args()
    dry_run: bool = args.dry_run

    mode_label = "[DRY-RUN]" if dry_run else "[APLICANDO]"
    print(f"\n{'='*60}")
    print(f"  apply_fase1_higiene.py  {mode_label}")
    print(f"  Repositório: {ROOT.name}")
    print(f"  Data: {TODAY}")
    print(f"{'='*60}\n")

    if not dry_run:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        print(f"  Backups em: _backups/fase1/\n")

    targets = collect_targets()
    print(f"  Arquivos HTML a processar: {len(targets)}\n")

    results: list[FileResult] = []
    for rel in targets:
        r = process_html(rel, dry_run)
        results.append(r)
        status = "✅ modificado" if r.changed else "— sem alteração"
        details = []
        if r.t11_removed_css:  details.append(f"CSS dup. -{r.t11_removed_css}")
        if r.t11_removed_js:   details.append(f"JS dup. -{r.t11_removed_js}")
        if r.t12_title_fixed:  details.append("título ✓")
        if r.t13_desc_fixed:   details.append("desc. ✓")
        if r.t14_hreflang_added: details.append(f"hreflang +{r.t14_hreflang_added}")
        if r.t15_srcset_added: details.append(f"srcset +{r.t15_srcset_added}")
        detail_str = f"  [{', '.join(details)}]" if details else ""
        print(f"  {status}  {rel}{detail_str}")
        for err in r.errors:
            print(f"    ⚠️  {err}", file=sys.stderr)

    # T-1.6 — Sitemap
    print(f"\n  Processando sitemap.xml (T-1.6)...")
    sitemap_stats = process_sitemap(dry_run)
    print(f"  URLs sem lastmod: {sitemap_stats[0]}  |  Corrigidas: {sitemap_stats[1]}")

    # Relatório
    write_report(results, sitemap_stats, dry_run)

    # Resumo final
    total_changed = sum(1 for r in results if r.changed)
    print(f"\n{'='*60}")
    print(f"  CONCLUÍDO {'(simulação)' if dry_run else ''}")
    print(f"  Arquivos HTML modificados: {total_changed}/{len(results)}")
    print(f"  Sitemap URLs corrigidas:   {sitemap_stats[1]}/{sitemap_stats[0]}")
    print(f"{'='*60}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
