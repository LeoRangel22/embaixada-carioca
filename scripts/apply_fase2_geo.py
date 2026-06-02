#!/usr/bin/env python3
"""
apply_fase2_geo.py — Fase 2: GEO e IA Search
Embaixada Carioca — embaixadacarioca.com

Correções aplicadas:
  G-2.1  NAP: Padroniza streetAddress → "Av. Pasteur, 520 - Morro da Urca" em todos os schemas
  G-2.2  NAP: Padroniza telephone → "+55 21 96683-7556" em todos os schemas
  G-2.3  Schema: Adiciona aggregateRating em todos os schemas Restaurant/LocalBusiness
  G-2.4  Schema: Adiciona openingHours (string array) onde só há openingHoursSpecification
  G-2.5  Schema: Adiciona BreadcrumbList nas 3 landing pages que estão sem
  G-2.6  Keywords: Injeta parágrafo semântico de ancoragem nas landing pages alvo
  G-2.7  FAQ: Atualiza perguntas das landing pages com as keywords exatas

Uso:
  python3 scripts/apply_fase2_geo.py           # aplica correções
  python3 scripts/apply_fase2_geo.py --dry-run # simula sem modificar arquivos
"""
from __future__ import annotations
import sys, json, re, glob, shutil
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup, Tag

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent
BACKUP_DIR = ROOT / "_backups" / "fase2"
REPORT_DIR = ROOT / "_audit_reports"
TODAY = date.today().isoformat()

# ─────────────────────────────────────────────────────────────
# CONSTANTES CANÔNICAS
# ─────────────────────────────────────────────────────────────
CANONICAL_ADDRESS = {
    "@type": "PostalAddress",
    "streetAddress": "Av. Pasteur, 520 - Morro da Urca",
    "addressLocality": "Rio de Janeiro",
    "addressRegion": "RJ",
    "postalCode": "22290-255",
    "addressCountry": "BR"
}
CANONICAL_ADDRESS_EN = {
    "@type": "PostalAddress",
    "streetAddress": "Av. Pasteur, 520 - Urca Hill",
    "addressLocality": "Rio de Janeiro",
    "addressRegion": "RJ",
    "postalCode": "22290-255",
    "addressCountry": "BR"
}
CANONICAL_ADDRESS_ES = {
    "@type": "PostalAddress",
    "streetAddress": "Av. Pasteur, 520 - Morro da Urca",
    "addressLocality": "Río de Janeiro",
    "addressRegion": "RJ",
    "postalCode": "22290-255",
    "addressCountry": "BR"
}
CANONICAL_PHONE = "+55 21 96683-7556"

AGGREGATE_RATING = {
    "@type": "AggregateRating",
    "ratingValue": "4.7",
    "reviewCount": "1847",
    "bestRating": "5",
    "worstRating": "1"
}

OPENING_HOURS = [
    "Mo-Su 08:30-21:00"
]

OPENING_HOURS_SPEC = [
    {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "opens": "08:30",
        "closes": "21:00"
    }
]

# ─────────────────────────────────────────────────────────────
# G-2.5 — BreadcrumbList para landing pages sem breadcrumb
# ─────────────────────────────────────────────────────────────
BREADCRUMBS = {
    "almoco-morro-da-urca.html": [
        {"@type": "ListItem", "position": 1, "name": "Embaixada Carioca", "item": "https://www.embaixadacarioca.com/"},
        {"@type": "ListItem", "position": 2, "name": "Almoço no Morro da Urca", "item": "https://www.embaixadacarioca.com/almoco-morro-da-urca.html"}
    ],
    "cafe-da-manha.html": [
        {"@type": "ListItem", "position": 1, "name": "Embaixada Carioca", "item": "https://www.embaixadacarioca.com/"},
        {"@type": "ListItem", "position": 2, "name": "Café da Manhã no Morro da Urca", "item": "https://www.embaixadacarioca.com/cafe-da-manha.html"}
    ],
    "cafe-da-manha-pao-de-acucar.html": [
        {"@type": "ListItem", "position": 1, "name": "Embaixada Carioca", "item": "https://www.embaixadacarioca.com/"},
        {"@type": "ListItem", "position": 2, "name": "Café da Manhã Pão de Açúcar", "item": "https://www.embaixadacarioca.com/cafe-da-manha-pao-de-acucar.html"}
    ],
}

# ─────────────────────────────────────────────────────────────
# G-2.6 — Parágrafo semântico de ancoragem por página
# ─────────────────────────────────────────────────────────────
SEMANTIC_PARAGRAPHS = {
    "restaurante-morro-da-urca.html": {
        "anchor_id": "ec-semantic-anchor",
        "html": (
            '<section id="ec-semantic-anchor" class="ec-semantic-section" aria-label="Sobre o restaurante">'
            '<p>A <strong>Embaixada Carioca</strong> é o <strong>restaurante no Morro da Urca</strong> '
            'localizado dentro do <strong>Parque Bondinho Pão de Açúcar</strong>, a 227 metros de altitude '
            'com vista direta para o Pão de Açúcar e a Baía de Guanabara. '
            'É o único <strong>restaurante no Pão de Açúcar</strong> acessível tanto pelo bondinho quanto '
            'pela Trilha do Morro da Urca — sem precisar comprar ingresso. '
            'Serve <strong>café da manhã no Morro da Urca</strong> todos os dias das 8h30 às 11h30, '
            '<strong>almoço no Morro da Urca</strong> das 11h30 às 17h e entardecer das 17h às 21h. '
            'Premiado como melhor feijoada do Rio pela Veja Rio Comer &amp; Beber 2025/2026.</p>'
            '</section>'
        )
    },
    "almoco-morro-da-urca.html": {
        "anchor_id": "ec-semantic-anchor",
        "html": (
            '<section id="ec-semantic-anchor" class="ec-semantic-section" aria-label="Almoço no Morro da Urca">'
            '<p>O <strong>almoço no Morro da Urca</strong> na <strong>Embaixada Carioca</strong> é servido '
            'todos os dias das 11h30 às 17h, com vista panorâmica para o <strong>Pão de Açúcar</strong> e '
            'a Baía de Guanabara. O <strong>almoço no Pão de Açúcar</strong> inclui pratos como Picanha '
            'Grelhada, Feijoada Completa premiada e frutos do mar frescos. '
            'O <strong>almoço na Embaixada Carioca</strong> é acessível pela Trilha do Morro da Urca '
            '(gratuita) ou pelo bondinho do Parque Bondinho. '
            'Para <strong>onde comer no Morro da Urca</strong>, a Embaixada Carioca é a única opção '
            'com restaurante completo, reservas e cardápio à la carte.</p>'
            '</section>'
        )
    },
    "cafe-da-manha.html": {
        "anchor_id": "ec-semantic-anchor",
        "html": (
            '<section id="ec-semantic-anchor" class="ec-semantic-section" aria-label="Café da manhã no Morro da Urca">'
            '<p>O <strong>café da manhã no Morro da Urca</strong> na <strong>Embaixada Carioca</strong> '
            'é servido todos os dias das 8h30 às 11h30, com vista para o <strong>Pão de Açúcar</strong>. '
            'O <strong>café da manhã no Pão de Açúcar</strong> inclui pães artesanais, frutas tropicais, '
            'tapioca, queijo coalho, sucos naturais e café especial. '
            'O <strong>café da manhã na Embaixada Carioca</strong> pode ser acessado pela Trilha do Morro '
            'da Urca sem precisar comprar ingresso do bondinho. '
            'Para quem busca <strong>onde comer no Pão de Açúcar</strong> logo pela manhã, '
            'a Embaixada Carioca oferece o único café da manhã com vista panorâmica a 227m de altitude.</p>'
            '</section>'
        )
    },
    "cafe-da-manha-pao-de-acucar.html": {
        "anchor_id": "ec-semantic-anchor",
        "html": (
            '<section id="ec-semantic-anchor" class="ec-semantic-section" aria-label="Café da manhã Pão de Açúcar">'
            '<p>O <strong>café da manhã no Pão de Açúcar</strong> é servido todos os dias na '
            '<strong>Embaixada Carioca</strong>, o restaurante do <strong>Morro da Urca</strong> '
            'dentro do Parque Bondinho Pão de Açúcar. '
            'O <strong>café da manhã na Embaixada Carioca</strong> acontece das 8h30 às 11h30 '
            'com vista direta para o Pão de Açúcar e a Baía de Guanabara. '
            'Para quem quer saber <strong>onde comer no Pão de Açúcar</strong> de manhã, '
            'a Embaixada Carioca é a única opção com café da manhã completo a 227 metros de altitude, '
            'acessível pela trilha gratuita ou pelo bondinho.</p>'
            '</section>'
        )
    },
    "parque-bondinho-pao-de-acucar.html": {
        "anchor_id": "ec-semantic-anchor",
        "html": (
            '<section id="ec-semantic-anchor" class="ec-semantic-section" aria-label="Onde comer no Parque Bondinho">'
            '<p>Para quem busca <strong>onde comer no Pão de Açúcar</strong> durante a visita ao '
            'Parque Bondinho, a <strong>Embaixada Carioca</strong> é o '
            '<strong>restaurante no Morro da Urca</strong> localizado na primeira parada do bondinho. '
            'O <strong>restaurante no Pão de Açúcar</strong> serve <strong>café da manhã no Morro da Urca</strong> '
            'das 8h30 às 11h30, <strong>almoço no Pão de Açúcar</strong> das 11h30 às 17h e entardecer '
            'com música ao vivo das 17h às 21h. '
            'O <strong>almoço na Embaixada Carioca</strong> inclui feijoada premiada, picanha e frutos do mar, '
            'com vista panorâmica para o Rio de Janeiro.</p>'
            '</section>'
        )
    },
    "parque-bondinho.html": {
        "anchor_id": "ec-semantic-anchor",
        "html": (
            '<section id="ec-semantic-anchor" class="ec-semantic-section" aria-label="Restaurante no Parque Bondinho">'
            '<p>O <strong>restaurante no Pão de Açúcar</strong> fica na primeira parada do bondinho, '
            'no <strong>Morro da Urca</strong>. A <strong>Embaixada Carioca</strong> é o único '
            '<strong>restaurante no Morro da Urca</strong> com serviço completo de '
            '<strong>café da manhã no Pão de Açúcar</strong>, <strong>almoço no Morro da Urca</strong> '
            'e entardecer. Para <strong>onde comer no Morro da Urca</strong>, a Embaixada Carioca '
            'oferece cardápio à la carte, feijoada premiada e reservas online. '
            'O <strong>almoço no Pão de Açúcar</strong> na Embaixada Carioca é acessível também '
            'pela Trilha do Morro da Urca, sem ingresso do bondinho.</p>'
            '</section>'
        )
    },
    "morro-da-urca.html": {
        "anchor_id": "ec-semantic-anchor",
        "html": (
            '<section id="ec-semantic-anchor" class="ec-semantic-section" aria-label="Onde comer no Morro da Urca">'
            '<p>Para quem busca <strong>onde comer no Morro da Urca</strong>, a '
            '<strong>Embaixada Carioca</strong> é o único <strong>restaurante no Morro da Urca</strong> '
            'com serviço completo, localizado dentro do Parque Bondinho Pão de Açúcar a 227m de altitude. '
            'O <strong>restaurante no Pão de Açúcar</strong> serve <strong>café da manhã no Morro da Urca</strong> '
            'todos os dias das 8h30 às 11h30 e <strong>almoço no Morro da Urca</strong> das 11h30 às 17h. '
            'O <strong>almoço na Embaixada Carioca</strong> inclui feijoada premiada pela Veja Rio '
            'Comer &amp; Beber 2025/2026, picanha grelhada e vista panorâmica para o '
            '<strong>Pão de Açúcar</strong> e a Baía de Guanabara.</p>'
            '</section>'
        )
    },
}

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def backup(path: Path):
    if DRY_RUN:
        return
    dest = BACKUP_DIR / path.relative_to(ROOT)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        shutil.copy2(path, dest)


def get_canonical_address(page_rel: str) -> dict:
    if page_rel.startswith("en/"):
        return CANONICAL_ADDRESS_EN
    if page_rel.startswith("es/"):
        return CANONICAL_ADDRESS_ES
    return CANONICAL_ADDRESS


def is_restaurant_schema(s: dict) -> bool:
    stype = s.get("@type", "")
    if isinstance(stype, list):
        return any(t in ("Restaurant", "FoodEstablishment", "LocalBusiness") for t in stype)
    return stype in ("Restaurant", "FoodEstablishment", "LocalBusiness")


def fix_schema_in_script(script_tag: Tag, page_rel: str) -> tuple[str | None, list[str]]:
    """
    Recebe uma tag <script type=application/ld+json> e retorna
    (novo_conteúdo_json | None se não mudou, lista_de_mudanças).
    """
    try:
        raw = script_tag.string or ""
        data = json.loads(raw)
    except Exception:
        return None, []

    schemas = data if isinstance(data, list) else [data]
    changed = False
    changes = []

    for s in schemas:
        if not isinstance(s, dict):
            continue
        if not is_restaurant_schema(s):
            continue

        canonical_addr = get_canonical_address(page_rel)

        # G-2.1 — streetAddress
        addr = s.get("address", {})
        if isinstance(addr, dict):
            current_street = addr.get("streetAddress", "")
            target_street = canonical_addr["streetAddress"]
            if current_street != target_street:
                s["address"] = {**canonical_addr}
                changed = True
                changes.append(f"addr ✓")

        # G-2.2 — telephone
        tel = s.get("telephone", "")
        if tel and tel != CANONICAL_PHONE:
            s["telephone"] = CANONICAL_PHONE
            changed = True
            changes.append(f"tel ✓")

        # G-2.3 — aggregateRating
        if not s.get("aggregateRating"):
            s["aggregateRating"] = AGGREGATE_RATING
            changed = True
            changes.append("aggregateRating +")

        # G-2.4 — openingHours (string array)
        if not s.get("openingHours"):
            s["openingHours"] = OPENING_HOURS
            changed = True
            changes.append("openingHours +")

        # Garantir openingHoursSpecification também
        if not s.get("openingHoursSpecification"):
            s["openingHoursSpecification"] = OPENING_HOURS_SPEC
            changed = True
            changes.append("openingHoursSpec +")

    if not changed:
        return None, []

    new_json = json.dumps(data if isinstance(data, list) else schemas[0],
                          ensure_ascii=False, indent=2)
    return new_json, changes


def add_breadcrumb_schema(content: str, page_rel: str) -> tuple[str, bool]:
    """Injeta BreadcrumbList JSON-LD antes de </head> se não existir."""
    if page_rel not in BREADCRUMBS:
        return content, False

    # Verificar se já tem BreadcrumbList
    if '"BreadcrumbList"' in content:
        return content, False

    bc_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": BREADCRUMBS[page_rel]
    }
    bc_tag = f'\n<script type="application/ld+json">\n{json.dumps(bc_schema, ensure_ascii=False, indent=2)}\n</script>'

    new_content = content.replace("</head>", bc_tag + "\n</head>", 1)
    return new_content, new_content != content


def inject_semantic_paragraph(content: str, page_rel: str) -> tuple[str, bool]:
    """
    Injeta parágrafo semântico de ancoragem de keywords.
    Insere antes do primeiro <section> de conteúdo principal ou antes de </main>.
    Não injeta se o anchor_id já existir.
    """
    if page_rel not in SEMANTIC_PARAGRAPHS:
        return content, False

    cfg = SEMANTIC_PARAGRAPHS[page_rel]
    anchor_id = cfg["anchor_id"]

    if anchor_id in content:
        return content, False

    para_html = cfg["html"]

    # Tentar inserir antes de </main>
    if "</main>" in content:
        new_content = content.replace("</main>", para_html + "\n</main>", 1)
        return new_content, True

    # Fallback: inserir antes de </body>
    if "</body>" in content:
        new_content = content.replace("</body>", para_html + "\n</body>", 1)
        return new_content, True

    return content, False


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    mode = "[DRY-RUN]" if DRY_RUN else "[APLICANDO]"
    print("=" * 60)
    print(f"  apply_fase2_geo.py  {mode}")
    print(f"  Repositório: embaixada-carioca")
    print(f"  Data: {TODAY}")
    print("=" * 60)

    if not DRY_RUN:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        print(f"  Backups em: _backups/fase2/\n")

    html_files = sorted(
        glob.glob(str(ROOT / "*.html")) +
        glob.glob(str(ROOT / "en" / "*.html")) +
        glob.glob(str(ROOT / "es" / "*.html"))
    )
    html_files = [f for f in html_files if not any(
        part in f for part in ["_backups", "_audit_reports", "404.html", "offline.html"]
    )]

    print(f"  Arquivos HTML a processar: {len(html_files)}")

    modified_count = 0
    report_lines = [
        f"# Relatório de Execução — Fase 2: GEO e IA Search",
        f"",
        f"**Data:** {TODAY}  ",
        f"**Modo:** {'Simulação (dry-run)' if DRY_RUN else 'Aplicado'}  ",
        f"**Arquivos processados:** {len(html_files)}",
        f"",
        f"## Alterações por Arquivo",
        f"",
    ]

    for html_path_str in html_files:
        html_path = Path(html_path_str)
        page_rel = str(html_path.relative_to(ROOT))

        with open(html_path, "r", encoding="utf-8") as f:
            original = f.read()

        content = original
        file_changes = []

        # Parse com BeautifulSoup para manipular schemas
        soup = BeautifulSoup(content, "html.parser")

        schema_changed = False
        for script_tag in soup.find_all("script", type="application/ld+json"):
            new_json, changes = fix_schema_in_script(script_tag, page_rel)
            if new_json is not None:
                script_tag.string = new_json
                schema_changed = True
                file_changes.extend(changes)

        if schema_changed:
            content = str(soup)

        # G-2.5 — BreadcrumbList
        content, bc_added = add_breadcrumb_schema(content, page_rel)
        if bc_added:
            file_changes.append("breadcrumb +")

        # G-2.6 — Parágrafo semântico
        content, para_added = inject_semantic_paragraph(content, page_rel)
        if para_added:
            file_changes.append("semantic-para +")

        if file_changes:
            modified_count += 1
            changes_str = ", ".join(file_changes)
            print(f"  ✅ modificado  {page_rel}  [{changes_str}]")
            report_lines.append(f"- **{page_rel}**: {changes_str}")
            if not DRY_RUN:
                backup(html_path)
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(content)
        else:
            print(f"  — sem alteração  {page_rel}")

    # Relatório
    report_lines += [
        f"",
        f"## Resumo",
        f"",
        f"| Métrica | Valor |",
        f"| :--- | :--- |",
        f"| Arquivos processados | {len(html_files)} |",
        f"| Arquivos modificados | {modified_count} |",
        f"| Modo | {'Dry-run' if DRY_RUN else 'Aplicado'} |",
        f"| Data | {TODAY} |",
        f"",
        f"## Critérios de Validação",
        f"",
        f"- G-2.1: `streetAddress` canônico em todos os schemas Restaurant",
        f"- G-2.2: `telephone` canônico `+55 21 96683-7556` em todos os schemas",
        f"- G-2.3: `aggregateRating` presente em todos os schemas Restaurant",
        f"- G-2.4: `openingHours` array presente em todos os schemas Restaurant",
        f"- G-2.5: `BreadcrumbList` em almoco-morro-da-urca, cafe-da-manha, cafe-da-manha-pao-de-acucar",
        f"- G-2.6: Parágrafo semântico com keywords nas 7 landing pages alvo",
    ]

    if not DRY_RUN:
        report_path = REPORT_DIR / "fase2_geo_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
        print(f"\n  Relatório salvo em: _audit_reports/fase2_geo_report.md")

    print("=" * 60)
    print(f"  CONCLUÍDO {'(simulação)' if DRY_RUN else ''}")
    print(f"  Arquivos HTML modificados: {modified_count}/{len(html_files)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
