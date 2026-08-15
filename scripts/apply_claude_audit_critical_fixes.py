#!/usr/bin/env python3
"""Apply critical fixes from the Claude digital audit.

Scope:
- Standardize all feijoada award language.
- Remove/neutralize unverified institutional claims involving Cantina do MAM.
- Fix common EN portunhol fragments detected in previous scripts.
- Standardize Instagram follower claims to 84K/84 mil.
- Strip review/rating nodes from JSON-LD to avoid review-snippet regressions.
- Audit workflow count and produce a governance report.

Guardrails:
- Does not change canonicals/hreflang.
- Does not add AggregateRating/Rating/Review.
- Does not touch prices unless part of visible text replacement.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "claude_audit_critical_fixes_report.md"
EXCLUDED_DIRS = {
    ".git", "node_modules", "_backups", "_templates",
    "_site", "dist", "build", "tests",
}
HTML_FILES = sorted(
    p for p in ROOT.rglob("*.html")
    if not any(part in EXCLUDED_DIRS for part in p.relative_to(ROOT).parts)
)
WORKFLOW_DIR = ROOT / ".github" / "workflows"
JSONLD_RE = re.compile(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)

PT_AWARD = "Melhor Feijoada do Rio de Janeiro — Veja Rio Comer & Beber 2025/2026"
EN_AWARD = "Best Feijoada in Rio de Janeiro — Veja Rio Comer & Beber 2025/2026"
ES_AWARD = "Mejor Feijoada de Río de Janeiro — Veja Rio Comer & Beber 2025/2026"

TEXT_REPLACEMENTS: list[tuple[str, str, str]] = [
    (r"Melhor\s+Feijoada\s+do\s+Brasil", "Melhor Feijoada do Rio de Janeiro", "award-pt-brasil-to-rio"),
    (r"best\s+feijoada\s+in\s+Brazil", "Best Feijoada in Rio de Janeiro", "award-en-brazil-to-rio"),
    (r"best\s+feijoada\s+of\s+Brazil", "Best Feijoada in Rio de Janeiro", "award-en-of-brazil-to-rio"),
    (r"one\s+of\s+the\s+best\s+feijoadas?\s+in\s+the\s+city", EN_AWARD, "award-en-weak-to-best"),
    (r"one\s+of\s+the\s+best\s+in\s+the\s+city", EN_AWARD, "award-en-generic-weak-to-best"),
    (r"Voted\s+by\s+Veja\s+Rio\s+as\s+one\s+of\s+the\s+best\s+in\s+the\s+city", f"Voted {EN_AWARD}", "award-en-veja-one-of-best"),
    (r"Revista\s+Prazeres\s+da\s+Mesa", "Veja Rio Comer & Beber 2025/2026", "wrong-magazine-prazeres-to-veja"),
    (r"Prazeres\s+da\s+Mesa", "Veja Rio Comer & Beber 2025/2026", "wrong-source-prazeres-to-veja"),
    (r"Veja\s+Rio\s+2025/2026(?!\s+Comer\s*&\s*Beber)", "Veja Rio Comer & Beber 2025/2026", "award-veja-full-name"),
    (r"O\s+sunset\s+m[aá]s\s+bonito\s+do\s+Rio\s+de\s+Janeiro", "The most beautiful sunset in Rio de Janeiro", "en-portunhol-sunset-mas"),
    (r"Servida\s+every\s+day\s+no\s+lunch", "Served daily for lunch", "en-portunhol-servida"),
    (r"drinks\s+e\s+petiscos", "drinks and Brazilian snacks", "en-portunhol-e"),
    (r"O\s+segunof\s+the\s+cable\s+car", "The second section of the cable car", "en-typo-segunof"),
    (r"experi[eê]ncia\s+gastron[oô]micas", "gastronomic experience", "en-portunhol-concordance"),
    (r"Perfeito\s+para\s+o\s+sunset\s+com\s+draft\s+beer\s+no\s+Urca\s+Hill", "Perfect for sunset with draft beer at Urca Hill", "en-portunhol-perfect"),
    (r'<li><a href="/cafe-da-manha\.html">Café da Manhã</a></li>', '<li><a href="/en/cafe-da-manha.html">Breakfast</a></li>', "en-nav-breakfast"),
    (r'<li><a href="/almoco\.html">Almoço</a></li>', '<li><a href="/en/almoco.html">Lunch</a></li>', "en-nav-lunch"),
    (r'<li><a href="/como-chegar\.html">Como Chegar</a></li>', '<li><a href="/en/how-to-get-there.html">How to get there</a></li>', "en-nav-directions"),
    (r'<li><a href="/eventos\.html">Eventos</a></li>', '<li><a href="/en/eventos.html">Events</a></li>', "en-nav-events"),
    (r'<li><a href="/cardapio\.html">Cardápio</a></li>', '<li><a href="/en/cardapio.html">Menu</a></li>', "en-nav-menu"),
    (r'<li><a href="/guia-do-rio\.html">Guia do Rio</a></li>', '<li><a href="/en/guia-do-rio.html">Rio guide</a></li>', "en-nav-rio-guide"),
    (r"Premiada\s+como\s+best\s+in\s+Brazil\s+pela\s+Revista\s+Veja\s+Rio\s+Comer\s*&\s*Beber\s+2025/2026\.", "Winner of Best Feijoada in Rio de Janeiro — Veja Rio Comer & Beber 2025/2026.", "en-award-sentence"),
    (r"Servida\s+every\s+day,?\s+das\s+11:30\s+AM\s+[àa]s\s+5:00\s+PM\.", "Served every day from 11:30 AM to 5:00 PM.", "en-serving-hours"),
    (r"Servida\s+every\s+day\.", "Served every day.", "en-served-daily"),
    (r"O\s+único\s+<strong>lunch\s+dentro\s+do\s+Bondinho\s+Pão\s+de\s+Açúcar\s+Park</strong>,\s+at\s+227\s+meters\s+altitude\s+no\s+Urca\s+Hill\.\s+Award-winning\s+Brazilian\s+gastronomy:\s+picanha\s+à\s+brasileira\s+e\s+a\s+feijoada\s+eleita\s+best\s+in\s+Brazil\s+pela\s+Revista\s+Veja\s+Rio\s+Comer\s*&\s*Beber\s+2025/2026\.\s+Para\s+quién\s+busca\s+<strong>onde\s+have\s+lunch\s+no\s+Rio\s+de\s+Janeiro</strong>\s+com\s+a\s+vista\s+mais\s+bonita\s+da\s+cidade\s+—\s+entre\s+os\s+<strong>restaurantes\s+com\s+vista\s+no\s+Rio\s+de\s+Janeiro</strong>,\s+este\s+es\s+o\s+único\s+atop\s+Urca\s+Hill\.", "The only <strong>lunch inside Bondinho Pão de Açúcar Park</strong>, 227 meters above sea level on Urca Hill. Enjoy Brazilian picanha and the winner of Best Feijoada in Rio de Janeiro — Veja Rio Comer & Beber 2025/2026 — at the park's only restaurant with a direct view of Sugarloaf Mountain.", "en-lunch-hero-rewrite"),
    (r"O\s+<strong>sunset\s+m[aá]s\s+bonito\s+do\s+Rio\s+de\s+Janeiro</strong>\s+—\s+sunset\s+atrás\s+of\s+Sugarloaf\s+Mountain,\s+visto\s+do\s+alto\s+do\s+Urca\s+Hill\.\s+Caipirinha\s+com\s+cachaça\s+Magnífica\s+e\s+draft\s+beer\s+Heineken\s+\(2º\s+best\s+in\s+Brazil\)\.\s+Um\s+dos\s+<strong>lugares\s+m[aá]s\s+bonitos\s+do\s+Rio\s+de\s+Janeiro</strong>\s+para\s+um\s+momento\s+romântico,\s+um\s+aniversário\s+ou\s+simplesmente\s+o\s+fim\s+de\s+um\s+dia\s+perfeito\s+na\s+cidade\.\s+Open\s+daily\s+das\s+5:00\s+PM\s+[àa]s\s+9:00\s+PM\.", "Watch the sun set behind Sugarloaf Mountain from Urca Hill while enjoying a caipirinha made with Magnífica cachaça or an ice-cold Heineken draft beer. It is an ideal setting for a romantic evening, a birthday or a relaxed end to a day in Rio. Open daily from 5:00 PM to 9:00 PM.", "en-sunset-hero-rewrite"),
    (r"O\s+sunset\s+m[aá]s\s+bonito\s+in\s+Rio\s+de\s+Janeiro,\s+com\s+música\s+ao\s+vivo\s+e\s+drinks\s+no\s+Urca\s+Hill\.", "Sunset in Rio de Janeiro with live music and drinks on Urca Hill.", "en-sunset-description"),
    (r"Veja\s+como\s+é\s+o\s+sunset\s+m[aá]s\s+bonito\s+in\s+Rio\s+de\s+Janeiro\s+no\s+Urca\s+Hill\.\s+Música\s+ao\s+vivo,\s+caipirinhas\s+e\s+vista\s+panorâmica\s+dGuanabara\s+Bay\s+e\s+of\s+Sugarloaf\s+Mountain\.", "See sunset from Urca Hill with live music, caipirinhas and panoramic views of Guanabara Bay and Sugarloaf Mountain.", "en-sunset-long-description"),
    (r"A\s+<a\s+href=\"/en/almoco\.html\"\s+title=\"Lunch\s+no\s+Urca\s+Hill\s+com\s+feijoada\s+premiada\">feijoada\s+da\s+Embaixada\s+Carioca</a>\s+é\s+a\s+mesma\s+feijoada\s+premiada\s+da\s+Academia\s+da\s+Cachaça,\s+eleita\s+a\s+best\s+in\s+Brazil\s+pela\s+Revista\s+Veja\s+Rio\s+Comer\s*&amp;\s*Beber\s+2025/2026\.\s+Served\s+daily\s+for\s+lunch,\s+with\s+a\s+view\s+of\s+Sugarloaf\s+Mountain\.\s+Uma\s+experiência\s+que\s+combina\s+gastronomia\s+de\s+alto\s+nível\s+com\s+o\s+cenário\s+m[aá]s\s+bonito\s+do\s+Rio\.", "The <a href=\"/en/almoco.html\" title=\"Lunch on Urca Hill with award-winning feijoada\">Embaixada Carioca feijoada</a> is the award-winning Academia da Cachaça recipe, named Best Feijoada in Rio de Janeiro by Veja Rio Comer &amp; Beber 2025/2026. It is served daily for lunch with a direct view of Sugarloaf Mountain.", "en-morro-feijoada-paragraph"),
    (r"\bno\s+Urca\s+Hill\b", "on Urca Hill", "en-no-urca-to-on"),
    (r"\bcom\s+a\s+vista\s+of\b", "with a view of", "en-com-vista-of"),
    (r"mais\s+de\s+100K\s+seguidores", "mais de 84 mil seguidores", "followers-pt-100k-to-84k"),
    (r"mais\s+de\s+100\s+mil\s+seguidores", "mais de 84 mil seguidores", "followers-pt-100mil-to-84mil"),
    (r"over\s+100K\s+followers", "over 84K followers", "followers-en-100k-to-84k"),
    (r"more\s+than\s+100K\s+followers", "more than 84K followers", "followers-en-100k-to-84k-2"),
    (r"\+100K(?=\s*</div><div[^>]*>\s*Instagram followers)", "84K", "followers-en-counter-to-84k"),
    (r"m[aá]s\s+de\s+100K\s+seguidores", "más de 84K seguidores", "followers-es-100k-to-84k"),
    (r"\+100K(?=\s*</div><div[^>]*>\s*Seguidores)", "84K", "followers-es-counter-to-84k"),
    (r"Instagram\s*·\s*\+100K", "Instagram · 84K", "followers-footer-100k-to-84k"),
    (r"Instagram\s*·\s*\+100\s+mil", "Instagram · 84 mil", "followers-footer-100mil-to-84mil"),
    (r"\+100K", "84K", "followers-generic-100k-to-84k"),
    (r"\+100\s+mil", "84 mil", "followers-generic-100mil-to-84mil"),
]

# Longer, specific institutional claims: neutralize only if found.
CLAIM_PATTERNS: list[tuple[str, str]] = [
    (
        r"<section\b(?:(?!</section>).)*Cantina\s+do\s+MAM(?:(?!</section>).)*</section>",
        "",
    ),
    (
        r"<!--\s*Cantina\s+do\s+MAM.*?-->\s*<div\b.*?@cantinadomam\s*</a>\s*</div></div>",
        "",
    ),
    (
        r"A\s+Embaixada\s+Carioca\s+faz\s+parte\s+do\s+Academia\s+da\s+Cachaça,\s+que\s+inclui\s+também\s+a\s+Academia\s+da\s+Cachaça\s*\([^)]*\)\s+e\s+a\s+Cantina\s+do\s+MAM\s*\([^)]*\),?\s+no\s+Museu\s+de\s+Arte\s+Moderna\.?",
        "A Embaixada Carioca fica no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar, com gastronomia brasileira, feijoada premiada da Academia da Cachaça e vista para o Pão de Açúcar.",
    ),
    (
        r"Embaixada\s+Carioca\s+is\s+part\s+of\s+Academia\s+da\s+Cachaça,\s+which\s+also\s+includes\s+Academia\s+da\s+Cachaça\s*\([^)]*\)\s+and\s+Cantina\s+do\s+MAM\s*\([^)]*\),?\s+at\s+the\s+Museum\s+of\s+Modern\s+Art\.?",
        "Embaixada Carioca is located at Morro da Urca inside Sugarloaf Cable Car Park, serving Brazilian food, the award-winning Academia da Cachaça feijoada and views of Sugarloaf Mountain.",
    ),
]

FORBIDDEN_AFTER = [
    "Prazeres da Mesa",
    "best feijoada in Brazil",
    "Best Feijoada in Brazil",
    "Melhor Feijoada do Brasil",
    "one of the best in the city",
    "Cantina do MAM",
    "100K seguidores",
    "100 mil seguidores",
    "+100K",
    "+100 mil",
    "segunof",
    "Servida every day no lunch",
    "drinks e petiscos",
    "best in Brazil pela",
    "Servida every",
    "sunset más",
    "dGuanabara",
    "Para quién",
    "onde have",
]

@dataclass
class FileResult:
    path: str
    changed: bool
    replacements: int
    jsonld_rating_removed: int
    notes: str


def lang_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt"


def canonical_award_for(path: Path) -> str:
    lang = lang_for(path)
    return EN_AWARD if lang == "en" else ES_AWARD if lang == "es" else PT_AWARD


def parse_json(raw: str) -> Any | None:
    try:
        return json.loads(html.unescape(raw.strip()))
    except Exception:
        return None


def scrub_rating_nodes(
    obj: Any,
    forbidden_types: set[str] | None = None,
) -> tuple[Any, int]:
    """Remove review/rating/aggregateRating keys recursively from JSON-LD."""
    forbidden_types = forbidden_types or {"Review", "Rating", "AggregateRating"}
    removed = 0
    if isinstance(obj, dict):
        node_type = obj.get("@type")
        node_types = node_type if isinstance(node_type, list) else [node_type]
        present_types = [value for value in node_types if value is not None]
        if present_types and all(value in forbidden_types for value in present_types):
            return None, 1
        if isinstance(node_type, list):
            safe_types = [value for value in node_type if value not in forbidden_types]
            removed += len(node_type) - len(safe_types)
            obj = dict(obj)
            obj["@type"] = safe_types
        cleaned = {}
        for k, v in obj.items():
            if k in {
                "review", "reviews", "aggregateRating", "reviewRating",
                "ratingValue", "ratingCount", "reviewCount",
                "bestRating", "worstRating",
            }:
                removed += 1
                continue
            new_v, count = scrub_rating_nodes(v, forbidden_types)
            removed += count
            if new_v is not None:
                cleaned[k] = new_v
        return cleaned, removed
    if isinstance(obj, list):
        new_list = []
        for item in obj:
            new_item, count = scrub_rating_nodes(item, forbidden_types)
            removed += count
            if new_item is not None:
                new_list.append(new_item)
        return new_list, removed
    return obj, 0


def scrub_jsonld(source: str, remove_event: bool = False) -> tuple[str, int]:
    removed_total = 0
    parts: list[str] = []
    last = 0
    for m in JSONLD_RE.finditer(source):
        opener, raw, closer = m.groups()
        obj = parse_json(raw)
        if obj is None:
            continue
        forbidden_types = {"Review", "Rating", "AggregateRating"}
        if remove_event:
            forbidden_types.add("Event")
        cleaned, removed = scrub_rating_nodes(obj, forbidden_types)
        if not removed:
            continue
        parts.append(source[last:m.start()])
        parts.append(opener + "\n" + json.dumps(cleaned, ensure_ascii=False, indent=2) + "\n" + closer)
        last = m.end()
        removed_total += removed
    if not removed_total:
        return source, 0
    parts.append(source[last:])
    return "".join(parts), removed_total


def apply_text_fixes(source: str, path: Path) -> tuple[str, int, list[str]]:
    count_total = 0
    notes: list[str] = []
    updated = source
    page_lang = lang_for(path)
    for pattern, repl, note in TEXT_REPLACEMENTS:
        if note.startswith("en-") and page_lang != "en":
            continue
        updated, count = re.subn(pattern, repl, updated, flags=re.I)
        if count:
            count_total += count
            notes.append(f"{note}:{count}")
    for pattern, repl in CLAIM_PATTERNS:
        updated, count = re.subn(pattern, repl, updated, flags=re.I | re.S)
        if count:
            count_total += count
            notes.append(f"unverified-cantina-claim-removed:{count}")

    return updated, count_total, notes


def process_file(path: Path) -> FileResult:
    rel = path.relative_to(ROOT).as_posix()
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated, replacements, notes = apply_text_fixes(original, path)
    remove_event = path.name == "sunset-por-do-sol-rio-de-janeiro.html"
    updated, rating_removed = scrub_jsonld(updated, remove_event=remove_event)
    if rating_removed:
        notes.append(f"jsonld-rating-review-removed:{rating_removed}")
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return FileResult(rel, changed, replacements, rating_removed, "; ".join(notes) if notes else "no-op")


def scan_remaining() -> dict[str, list[str]]:
    remaining: dict[str, list[str]] = {}
    for path in HTML_FILES:
        text = path.read_text(encoding="utf-8", errors="ignore")
        page_lang = lang_for(path)
        found = []
        en_only = {
            "drinks e petiscos", "best in Brazil pela", "Servida every",
            "sunset más", "dGuanabara", "Para quién", "onde have",
        }
        for term in FORBIDDEN_AFTER:
            if term in en_only and page_lang != "en":
                continue
            if term.lower() in text.lower():
                found.append(term)
        if found:
            remaining[path.relative_to(ROOT).as_posix()] = found
    return remaining


def workflow_inventory() -> list[str]:
    if not WORKFLOW_DIR.exists():
        return []
    return sorted(p.relative_to(ROOT).as_posix() for p in WORKFLOW_DIR.glob("*.yml")) + sorted(p.relative_to(ROOT).as_posix() for p in WORKFLOW_DIR.glob("*.yaml"))


def write_report(results: list[FileResult], remaining: dict[str, list[str]], workflows: list[str]) -> int:
    REPORT.parent.mkdir(exist_ok=True)
    changed = [r for r in results if r.changed]
    status = "PASS" if not remaining else "WARN"
    lines = [
        "# Claude Audit Critical Fixes",
        "",
        f"Status geral: **{status}**",
        "",
        "## Objetivo",
        "Atuar sobre os pontos críticos do relatório Claude: padronização do prêmio da feijoada, remoção de alegações institucionais não verificadas, limpeza de portunhol técnico, padronização de seguidores e blindagem contra retorno de review/rating em JSON-LD.",
        "",
        "## Formulações canônicas aplicadas",
        f"- PT: `{PT_AWARD}`",
        f"- EN: `{EN_AWARD}`",
        f"- ES: `{ES_AWARD}`",
        "",
        "## Guardrails",
        "- Nenhum canonical/hreflang foi alterado.",
        "- Nenhum AggregateRating, Rating ou Review foi adicionado.",
        "- JSON-LD com `review`, `reviewRating` ou `aggregateRating` foi limpo quando encontrado.",
        "- Alegações envolvendo Cantina do MAM foram neutralizadas se presentes no HTML.",
        "",
        "## Resumo",
        f"- HTML analisados: **{len(results)}**",
        f"- Arquivos alterados: **{len(changed)}**",
        f"- Substituições textuais: **{sum(r.replacements for r in results)}**",
        f"- Nós/campos JSON-LD de rating/review removidos: **{sum(r.jsonld_rating_removed for r in results)}**",
        f"- Workflows encontrados: **{len(workflows)}**",
        "",
    ]
    if workflows:
        lines.extend(["## Inventário de workflows", ""])
        for w in workflows:
            lines.append(f"- `{w}`")
        lines.append("")
    if remaining:
        lines.extend(["## Pendências encontradas", ""])
        for rel, terms in remaining.items():
            lines.append(f"- `{rel}`: {', '.join(f'`{t}`' for t in terms)}")
        lines.append("")
    else:
        lines.extend(["## Pendências encontradas", "", "Nenhuma ocorrência dos termos críticos monitorados.", ""])
    lines.extend(["## Arquivos alterados", "", "| Arquivo | Changed | Substituições | JSON-LD rating/review removidos | Notas |", "|---|---:|---:|---:|---|"])
    for r in results:
        if r.changed:
            lines.append(f"| `{r.path}` | {r.changed} | {r.replacements} | {r.jsonld_rating_removed} | {r.notes} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Claude audit critical fixes: {status}")
    return 0 if status in {"PASS", "WARN"} else 1


def main() -> int:
    results = [process_file(path) for path in HTML_FILES]
    remaining = scan_remaining()
    workflows = workflow_inventory()
    return write_report(results, remaining, workflows)


if __name__ == "__main__":
    raise SystemExit(main())
