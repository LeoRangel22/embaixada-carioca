#!/usr/bin/env python3
"""
Structural Restaurant Site Audit — Embaixada Carioca.

Audita os 10 critérios principais de um site de restaurante:
1. Integridade linguística PT/EN/ES
2. SEO técnico
3. SEO local / entidade
4. GEO / respostas para IA
5. UX de reserva e contato
6. Menu/cardápio e oferta gastronômica
7. Performance básica e imagens
8. Acessibilidade básica
9. Dados estruturados
10. Integridade estrutural de links e páginas

Gera relatório com nota e alertas críticos.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_DIR.mkdir(exist_ok=True)

MAIN = [
    "index.html",
    "cafe-da-manha.html",
    "almoco.html",
    "entardecer.html",
    "eventos.html",
    "cardapio.html",
    "guia-do-rio.html",
    "en/index.html",
    "en/cafe-da-manha.html",
    "en/almoco.html",
    "en/entardecer.html",
    "en/eventos.html",
    "en/cardapio.html",
    "en/guia-do-rio.html",
    "es/index.html",
    "es/cafe-da-manha.html",
    "es/almoco.html",
    "es/entardecer.html",
    "es/eventos.html",
    "es/cardapio.html",
    "es/guia-do-rio.html",
]

CRITICAL_TECH_PATTERNS = [
    "send_page_vista",
    "vistaport",
    "page_vista",
]

LANG_PATTERNS = {
    "pt": [r"\bEventos en el\b", r"\bHablar con nuestro\b", r"\bPara qui[eé]n\b", r"\bReuniones matutinas\b", r"\brecibidos con\b", r"\bm[aá]s impresionante\b", r"\bmain dining room\b", r"\bpanoramic terraces?\b", r"\bhospitality team\b", r"\bCapacity varies\b", r"\bStructure &"],
    "en": [r"\bSolicitar orçamento\b", r"\bFalar com nossa equipe\b", r"\bAberto todos os dias\b"],
    "es": [r"\bSolicitar orçamento\b", r"\bFalar com nossa equipe\b", r"\bBreakfast\b", r"\bLunch\b"],
}

INTERNAL_HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)


def read(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def lang_for(rel: str, text: str) -> str:
    if rel.startswith("en/") or 'lang="en"' in text:
        return "en"
    if rel.startswith("es/") or 'lang="es"' in text:
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
        text = path.read_text(encoding="utf-8", errors="ignore")
        lang = lang_for(rel, text)
        for pattern in LANG_PATTERNS.get(lang, []):
            if re.search(pattern, text, re.IGNORECASE):
                issues.append(f"{rel}: padrão suspeito de idioma `{pattern}`")
    return score_from_issues(10, 0.45, len(issues), 7.0), issues


def audit_technical_seo() -> tuple[float, list[str]]:
    issues = []
    for rel in MAIN:
        text = read(rel)
        if not text:
            issues.append(f"{rel}: ausente")
            continue
        if not re.search(r"<title>[^<]{20,70}</title>", text, re.IGNORECASE):
            issues.append(f"{rel}: title ausente ou fora do tamanho ideal")
        if not re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'][^"\']{70,180}["\']', text, re.IGNORECASE):
            issues.append(f"{rel}: description ausente ou fora do tamanho ideal")
        if 'rel="canonical"' not in text and "rel='canonical'" not in text:
            issues.append(f"{rel}: canonical ausente")
        if "hreflang" not in text:
            issues.append(f"{rel}: hreflang ausente")
        if '<meta name="viewport"' not in text and "name='viewport'" not in text:
            issues.append(f"{rel}: viewport ausente")
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        issues.append("sitemap.xml ausente")
    robots = ROOT / "robots.txt"
    if not robots.exists():
        issues.append("robots.txt ausente")
    return score_from_issues(10, 0.18, len(issues), 6.5), issues


def audit_local_entity() -> tuple[float, list[str]]:
    issues = []
    required = ["Morro da Urca", "Parque Bondinho", "Pão de Açúcar", "Embaixada Carioca"]
    for rel in MAIN[:7]:
        text = read(rel)
        for term in required:
            if term not in text:
                issues.append(f"{rel}: falta termo de entidade/local `{term}`")
    return score_from_issues(10, 0.22, len(issues), 7.0), issues


def audit_geo_ai() -> tuple[float, list[str]]:
    issues = []
    question_terms = ["FAQPage", "Perguntas frequentes", "Resposta direta", "Direct answer", "Respuesta directa"]
    for rel in MAIN:
        text = read(rel)
        if text and not any(t in text for t in question_terms):
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
    offer_terms = ["café da manhã", "almoço", "caipirinha", "feijoada", "chope", "cardápio"]
    text_all = "\n".join(read(rel) for rel in MAIN[:7])
    for term in offer_terms:
        if term not in text_all.lower():
            issues.append(f"Oferta: termo ausente no cluster principal `{term}`")
    if not (ROOT / "cardapio.html").exists():
        issues.append("cardapio.html ausente")
    return score_from_issues(10, 0.35, len(issues), 7.0), issues


def audit_performance() -> tuple[float, list[str]]:
    issues = []
    for rel in MAIN:
        path = ROOT / rel
        if path.exists() and path.stat().st_size > 350_000:
            issues.append(f"{rel}: HTML acima de 350 KB")
        text = read(rel)
        if text and "hero.jpg" in text and "hero-1200w.webp" not in text:
            issues.append(f"{rel}: hero JPG sem WebP responsivo")
        if text and "serviceWorker.register" not in text:
            issues.append(f"{rel}: service worker não registrado")
    if not (ROOT / "_headers").exists():
        issues.append("_headers ausente")
    if not (ROOT / "sw.js").exists():
        issues.append("sw.js ausente")
    return score_from_issues(10, 0.14, len(issues), 6.5), issues


def audit_accessibility() -> tuple[float, list[str]]:
    issues = []
    for rel in MAIN:
        text = read(rel)
        if not text:
            continue
        imgs = len(re.findall(r"<img\b", text, re.IGNORECASE))
        imgs_alt = len(re.findall(r"<img\b[^>]*\balt=", text, re.IGNORECASE))
        if imgs_alt < imgs:
            issues.append(f"{rel}: {imgs - imgs_alt} imagem(ns) sem alt")
        if "aria-label" not in text:
            issues.append(f"{rel}: poucos sinais ARIA/labels")
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
            if href.startswith(("http", "mailto:", "tel:", "#", "javascript:")):
                continue
            if href.startswith("/"):
                target = href.split("#")[0].split("?")[0].lstrip("/")
            else:
                target = (path.parent / href.split("#")[0].split("?")[0]).resolve().relative_to(ROOT.resolve()).as_posix() if href else ""
            if not target or target.endswith("/"):
                continue
            if Path(target).suffix and not (ROOT / target).exists():
                issues.append(f"{rel}: link interno possivelmente quebrado -> {href}")
    for rel in MAIN:
        if not (ROOT / rel).exists():
            issues.append(f"página principal ausente: {rel}")
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
    results = []
    all_issues = {}
    for name, fn in audits:
        score, issues = fn()
        results.append((name, round(score, 1), len(issues)))
        all_issues[name] = issues
    avg = round(sum(score for _, score, _ in results) / len(results), 1)
    report = REPORT_DIR / "restaurant_site_10_criteria_audit.md"
    lines = [
        "# Auditoria Profunda — Site de Restaurante Embaixada Carioca",
        "",
        f"## Nota geral estimada: {avg}/10",
        "",
        "## Score por critério",
        "| Critério | Nota | Alertas |",
        "|---|---:|---:|",
    ]
    for name, score, count in results:
        lines.append(f"| {name} | {score}/10 | {count} |")
    lines.extend(["", "## Alertas detalhados"])
    for name, issues in all_issues.items():
        lines.extend(["", f"### {name}"])
        if issues:
            lines.extend(f"- {i}" for i in issues[:80])
            if len(issues) > 80:
                lines.append(f"- ... +{len(issues)-80} alertas adicionais")
        else:
            lines.append("- Nenhum alerta encontrado.")
    lines.extend([
        "",
        "## Veredito",
        "- Nota 9+ só deve ser considerada confirmada se todos os critérios críticos estiverem sem alertas técnicos e linguísticos.",
        "- O relatório é estático e baseado nos arquivos do repositório; validação visual final deve ser feita no navegador após deploy.",
        "",
    ])
    report.write_text("\n".join(lines), encoding="utf-8")
    print(report.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
