#!/usr/bin/env python3
"""
Structural Restaurant Site Audit — Embaixada Carioca.

Audita critérios principais de um site de restaurante:
1. Integridade técnica de tokens
2. Integridade linguística PT/EN/ES
3. SEO técnico
4. SEO local / entidade
5. GEO / respostas para IA
6. UX de reserva e contato
7. Menu/cardápio e oferta gastronômica
8. Performance básica e imagens
9. Acessibilidade básica
10. Dados estruturados
11. Integridade estrutural de links e páginas

Gera relatório com nota e alertas críticos.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_DIR.mkdir(exist_ok=True)

MAIN = [
    "index.html", "cafe-da-manha.html", "almoco.html", "entardecer.html", "eventos.html", "cardapio.html", "guia-do-rio.html",
    "en/index.html", "en/cafe-da-manha.html", "en/almoco.html", "en/entardecer.html", "en/eventos.html", "en/cardapio.html", "en/guia-do-rio.html",
    "es/index.html", "es/cafe-da-manha.html", "es/almoco.html", "es/entardecer.html", "es/eventos.html", "es/cardapio.html", "es/guia-do-rio.html",
]

CRITICAL_TECH_PATTERNS = ["send_page_vista", "vistaport", "page_vista"]

LANG_PATTERNS = {
    "pt": [
        r"\bEventos en el\b", r"\bHablar con nuestro\b", r"\bPara qui[eé]n\b", r"\bReuniones matutinas\b", r"\brecibidos con\b", r"\bm[aá]s impresionante\b",
        r"\bmain dining room\b", r"\bpanoramic terraces?\b", r"\bhospitality team\b", r"\bCapacity varies\b", r"\bStructure &",
    ],
    "en": [r"\bSolicitar orçamento\b", r"\bFalar com nossa equipe\b", r"\bAberto todos os dias\b", r"\bsalão principal\b", r"\bterraços panorâmicos\b", r"\bequipe receptiva\b", r"\bCapacidade variável\b"],
    "es": [r"\bSolicitar orçamento\b", r"\bFalar com nossa equipe\b", r"\bBreakfast\b", r"\bLunch\b", r"\bsalão principal\b", r"\bterraços panorâmicos\b", r"\bequipe receptiva\b", r"\bCapacidade variável\b"],
}

INTERNAL_HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
HTML_LANG_RE = re.compile(r"<html\b[^>]*\blang=[\"']([^\"']+)[\"']", re.IGNORECASE)
META_DESC_RE = re.compile(r'<meta\b(?=[^>]*\bname=["\']description["\'])(?=[^>]*\bcontent=["\']([^"\']{50,220})["\'])[^>]*>', re.IGNORECASE)
VIEWPORT_RE = re.compile(r'<meta\b(?=[^>]*\bname=["\']viewport["\'])(?=[^>]*\bcontent=)[^>]*>', re.IGNORECASE)
TITLE_RE = re.compile(r"<title>\s*([^<]{12,85})\s*</title>", re.IGNORECASE)
NON_VISIBLE_RE = re.compile(r"<script\b[\s\S]*?</script>|<style\b[\s\S]*?</style>|<!-- EC Sprint 1 Structured Data -->[\s\S]*?<!-- /EC Sprint 1 Structured Data -->", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")


def read(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def visible_text(html: str) -> str:
    """Return approximate user-visible text for language QA.

    This intentionally ignores script/style/JSON-LD. Structured data may contain
    technical English tokens, but it should not count as visible language leakage.
    """
    cleaned = NON_VISIBLE_RE.sub(" ", html)
    cleaned = TAG_RE.sub(" ", cleaned)
    return re.sub(r"\s+", " ", cleaned)


def lang_for(rel: str, text: str) -> str:
    match = HTML_LANG_RE.search(text)
    if match:
        value = match.group(1).lower()
        if value.startswith("en"):
            return "en"
        if value.startswith("es"):
            return "es"
    if rel.startswith("en/"):
        return "en"
    if rel.startswith("es/"):
        return "es"
    return "pt"


def html_files() -> list[Path]:
    return [p for p in ROOT.rglob("*.html") if ".git" not in p.parts and not p.relative_to(ROOT).as_posix().startswith("_")]


def score_from_issues(max_score: float, penalty: float, count: int, floor: float = 0.0) -> float:
    return max(floor, max_score - penalty * count)


def audit_language() -> tuple[float, list[str]]:
    issues = []
    for path in html_files():
        rel = path.relative_to(ROOT).as_posix()
        raw = path.read_text(encoding="utf-8", errors="ignore")
        lang = lang_for(rel, raw)
        text = visible_text(raw)
        for pattern in LANG_PATTERNS.get(lang, []):
            if re.search(pattern, text, re.IGNORECASE):
                issues.append(f"{rel}: texto visível contém padrão suspeito de idioma `{pattern}`")
    return score_from_issues(10, 0.5, len(issues), 7.0), issues


def audit_technical_seo() -> tuple[float, list[str]]:
    issues = []
    for rel in MAIN:
        text = read(rel)
        if not text:
            issues.append(f"{rel}: ausente")
            continue
        if not TITLE_RE.search(text):
            issues.append(f"{rel}: title ausente ou fora do tamanho ideal")
        if not META_DESC_RE.search(text):
            issues.append(f"{rel}: description ausente ou fora do tamanho ideal")
        if 'rel="canonical"' not in text and "rel='canonical'" not in text:
            issues.append(f"{rel}: canonical ausente")
        if "hreflang" not in text:
            issues.append(f"{rel}: hreflang ausente")
        if not VIEWPORT_RE.search(text):
            issues.append(f"{rel}: viewport ausente")
    if not (ROOT / "sitemap.xml").exists(): issues.append("sitemap.xml ausente")
    if not (ROOT / "robots.txt").exists(): issues.append("robots.txt ausente")
    return score_from_issues(10, 0.18, len(issues), 6.5), issues


def audit_local_entity() -> tuple[float, list[str]]:
    issues = []
    for rel in MAIN[:7]:
        text = read(rel)
        for term in ["Morro da Urca", "Parque Bondinho", "Pão de Açúcar", "Embaixada Carioca"]:
            if term not in text:
                issues.append(f"{rel}: falta termo de entidade/local `{term}`")
    return score_from_issues(10, 0.22, len(issues), 7.0), issues


def audit_geo_ai() -> tuple[float, list[str]]:
    issues = []
    terms = ["FAQPage", "Perguntas frequentes", "Resposta direta", "Direct answer", "Respuesta directa"]
    for rel in MAIN:
        text = read(rel)
        if text and not any(t in text for t in terms):
            issues.append(f"{rel}: falta bloco claro de resposta direta/FAQ")
    return score_from_issues(10, 0.16, len(issues), 6.8), issues


def audit_reservation_contact() -> tuple[float, list[str]]:
    issues = []
    for rel in MAIN:
        text = read(rel)
        if text and "go.tagme.com.br/embaixadacarioca" not in text:
            issues.append(f"{rel}: CTA TagMe ausente")
        if text and ("wa.me" not in text and "96683" not in text and "eventos@embaixadacarioca.com" not in text):
            issues.append(f"{rel}: contato/WhatsApp/e-mail ausente")
    return score_from_issues(10, 0.16, len(issues), 7.0), issues


def audit_menu_offer() -> tuple[float, list[str]]:
    issues = []
    text_all = "\n".join(read(rel) for rel in MAIN[:7]).lower()
    for term in ["café da manhã", "almoço", "caipirinha", "feijoada", "chope", "cardápio"]:
        if term not in text_all:
            issues.append(f"Oferta: termo ausente no cluster principal `{term}`")
    if not (ROOT / "cardapio.html").exists(): issues.append("cardapio.html ausente")
    return score_from_issues(10, 0.35, len(issues), 7.0), issues


def audit_performance() -> tuple[float, list[str]]:
    issues = []
    for rel in MAIN:
        path = ROOT / rel
        text = read(rel)
        if path.exists() and path.stat().st_size > 350_000:
            issues.append(f"{rel}: HTML acima de 350 KB")
        if text and "hero.jpg" in text and "hero-1200w.webp" not in text and "hero.webp" not in text:
            issues.append(f"{rel}: hero JPG sem WebP responsivo")
        if text and "serviceWorker.register" not in text:
            issues.append(f"{rel}: service worker não registrado")
    if not (ROOT / "_headers").exists(): issues.append("_headers ausente")
    if not (ROOT / "sw.js").exists(): issues.append("sw.js ausente")
    return score_from_issues(10, 0.14, len(issues), 6.5), issues


def audit_accessibility() -> tuple[float, list[str]]:
    issues = []
    for rel in MAIN:
        text = read(rel)
        if not text: continue
        imgs = len(re.findall(r"<img\b", text, re.IGNORECASE))
        imgs_alt = len(re.findall(r"<img\b[^>]*\balt=", text, re.IGNORECASE))
        if imgs_alt < imgs:
            issues.append(f"{rel}: {imgs - imgs_alt} imagem(ns) sem alt")
    return score_from_issues(10, 0.12, len(issues), 7.0), issues


def audit_schema() -> tuple[float, list[str]]:
    issues = []
    for rel in MAIN:
        text = read(rel)
        if text and 'application/ld+json' not in text:
            issues.append(f"{rel}: JSON-LD ausente")
        if text and "Restaurant" not in text and "EventVenue" not in text and "Menu" not in text:
            issues.append(f"{rel}: schema de restaurante/evento/menu fraco ou ausente")
    return score_from_issues(10, 0.18, len(issues), 7.0), issues


def audit_integrity_links() -> tuple[float, list[str]]:
    issues = []
    for path in html_files():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        for href in INTERNAL_HREF_RE.findall(text):
            if href.startswith(("http", "mailto:", "tel:", "#", "javascript:")): continue
            target = href.split("#")[0].split("?")[0]
            if not target or target.endswith("/"): continue
            if target.startswith("/"):
                norm = target.lstrip("/")
            else:
                try:
                    norm = (path.parent / target).resolve().relative_to(ROOT.resolve()).as_posix()
                except Exception:
                    continue
            if Path(norm).suffix and not (ROOT / norm).exists():
                issues.append(f"{rel}: link interno possivelmente quebrado -> {href}")
    for rel in MAIN:
        if not (ROOT / rel).exists(): issues.append(f"página principal ausente: {rel}")
    return score_from_issues(10, 0.08, min(len(issues), 40), 6.5), issues[:60]


def audit_technical_code_tokens() -> tuple[float, list[str]]:
    issues = []
    for path in html_files():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pat in CRITICAL_TECH_PATTERNS:
            if pat in text:
                issues.append(f"{rel}: token técnico quebrado `{pat}`")
    return score_from_issues(10, 1.2, len(issues), 0), issues


def main() -> int:
    audits = [
        ("Integridade técnica de tokens", audit_technical_code_tokens),
        ("Integridade linguística PT/EN/ES", audit_language),
        ("SEO técnico", audit_technical_seo),
        ("SEO local / entidade", audit_local_entity),
        ("GEO / respostas para IA", audit_geo_ai),
        ("Reserva e contato", audit_reservation_contact),
        ("Cardápio e oferta gastronômica", audit_menu_offer),
        ("Performance básica", audit_performance),
        ("Acessibilidade básica", audit_accessibility),
        ("Dados estruturados", audit_schema),
        ("Integridade de links/páginas", audit_integrity_links),
    ]
    results, all_issues = [], {}
    for name, fn in audits:
        score, issues = fn()
        results.append((name, round(score, 1), len(issues)))
        all_issues[name] = issues
    avg = round(sum(score for _, score, _ in results) / len(results), 1)
    report = REPORT_DIR / "restaurant_site_10_criteria_audit.md"
    lines = ["# Auditoria Profunda — Site de Restaurante Embaixada Carioca", "", f"## Nota geral estimada: {avg}/10", "", "## Score por critério", "| Critério | Nota | Alertas |", "|---|---:|---:|"]
    for name, score, count in results:
        lines.append(f"| {name} | {score}/10 | {count} |")
    lines.extend(["", "## Alertas detalhados"])
    for name, issues in all_issues.items():
        lines.extend(["", f"### {name}"])
        if issues:
            lines.extend(f"- {i}" for i in issues[:80])
            if len(issues) > 80: lines.append(f"- ... +{len(issues)-80} alertas adicionais")
        else:
            lines.append("- Nenhum alerta encontrado.")
    lines.extend(["", "## Veredito", "- Nota 9+ só deve ser considerada confirmada se todos os critérios críticos estiverem sem alertas técnicos e linguísticos reais.", "- O relatório é estático e baseado nos arquivos do repositório; validação visual final deve ser feita no navegador após deploy.", ""])
    report.write_text("\n".join(lines), encoding="utf-8")
    print(report.read_text(encoding="utf-8"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
