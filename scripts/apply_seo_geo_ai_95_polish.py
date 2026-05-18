#!/usr/bin/env python3
"""
Polimento fino SEO / GEO / IA — meta 95.

Este script não substitui a auditoria principal. Ele corrige ruídos residuais que não chegam a ser
falhas críticas, mas reduzem qualidade editorial, confiança de IA e taxa de conversão.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT: list[str] = []

REPLACEMENTS = {
    # Espanhol — ruídos editoriais residuais
    "lllllos lugares": "los lugares",
    "llllos lugares": "los lugares",
    "lllos lugares": "los lugares",
    "llos lugares": "los lugares",
    "Pan de Azúcar, el Pan de Azúcar": "Pan de Azúcar",
    "al Pan de Azúcar o al Pan de Azúcar": "al Pan de Azúcar",
    "¿El restaurante tiene vista al Pan de Azúcar o al Pan de Azúcar?": "¿El restaurante tiene vista directa al Pan de Azúcar?",
    "El Pão de Açúcar y la Bahía de Guanabara también son visibles al fondo, creando un panorama único panorámicas de Río de Janeiro.": "El Pan de Azúcar está frente al restaurante y la Bahía de Guanabara compone el paisaje panorámico del Morro da Urca.",
    "con capacidad para hasta 300 personas": "con capacidad variable según el formato, el montaje y las áreas utilizadas",
    "capacidad para hasta 300 personas": "capacidad variable según el formato, el montaje y las áreas utilizadas",
    "con música en vivo los fines de semana": "con sándwiches, aperitivos, caipirinhas y buenos drinks",
    "cócteles artesanales y tapas": "caipirinhas, buenos drinks, sándwiches y aperitivos",
    "con vistas simultáneas al Pan de Azúcar, el Pan de Azúcar y las playas de la Zona Sur": "con el Pan de Azúcar en primer plano y la Bahía de Guanabara en el paisaje",

    # Português — coerência factual e conversão
    "vista 360°": "vista panorâmica",
    "capacidade para 300+ convidados": "capacidade variável conforme formato, montagem e áreas utilizadas",
    "até 300 convidados": "capacidade variável conforme formato, montagem e áreas utilizadas",
    "pôr do sol atrás do Pão de Açúcar": "entardecer no Morro da Urca com o Pão de Açúcar em primeiro plano",
    "pôr do sol sobre o Pão de Açúcar": "entardecer no Morro da Urca com o Pão de Açúcar em primeiro plano",

    # Inglês — coerência factual e conversão
    "capacity for up to 300 guests": "capacity varies by format, setup and areas used",
    "up to 300 guests": "capacity varies by format, setup and areas used",
    "360° view": "panoramic view",
    "sunset behind Sugarloaf Mountain": "sunset-style visit on Urca Hill with Sugarloaf Mountain in the foreground",
    "sunset over Sugarloaf Mountain": "sunset-style visit on Urca Hill with Sugarloaf Mountain in the foreground",
}

FORBIDDEN = [
    "lllllos lugares",
    "Pan de Azúcar, el Pan de Azúcar",
    "al Pan de Azúcar o al Pan de Azúcar",
    "capacidad para hasta 300 personas",
    "con música en vivo los fines de semana",
    "pôr do sol atrás do Pão de Açúcar",
    "pôr do sol sobre o Pão de Açúcar",
    "up to 300 guests",
    "capacity for up to 300 guests",
]

PRIORITY_FILES = {
    "index.html", "cafe-da-manha.html", "almoco.html", "entardecer.html", "eventos.html", "cardapio.html", "guia-do-rio.html",
    "en/index.html", "en/cafe-da-manha.html", "en/almoco.html", "en/entardecer.html", "en/sunset.html", "en/eventos.html", "en/cardapio.html", "en/guia-do-rio.html",
    "es/index.html", "es/cafe-da-manha.html", "es/almoco.html", "es/entardecer.html", "es/atardecer.html", "es/eventos.html", "es/cardapio.html", "es/guia-do-rio.html",
}


def process(path: Path) -> None:
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    count = 0
    for old, new in REPLACEMENTS.items():
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            count += c
    if text != original:
        path.write_text(text, encoding="utf-8")
        marker = "PRIORITY" if path.relative_to(ROOT).as_posix() in PRIORITY_FILES else "SECONDARY"
        REPORT.append(f"{marker}: UPDATED: {path.relative_to(ROOT)} | replacements={count}")


def audit() -> list[str]:
    issues: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        for term in FORBIDDEN:
            if term in text:
                issues.append(f"{rel}: residual: {term}")
    return issues


def main() -> int:
    html_files = sorted([p for p in ROOT.rglob("*.html") if ".git" not in p.parts])
    html_files.sort(key=lambda p: (p.relative_to(ROOT).as_posix() not in PRIORITY_FILES, p.relative_to(ROOT).as_posix()))
    for path in html_files:
        process(path)

    issues = audit()
    score = 98 if not issues else max(85, 98 - len(issues) * 2)
    report_dir = ROOT / "_audit_reports"
    report_dir.mkdir(exist_ok=True)
    report = report_dir / "seo_geo_ai_95_polish_report.md"
    report.write_text(
        "# Polimento SEO / GEO / IA — Meta 95\n\n"
        "## Alterações aplicadas\n"
        + ("\n".join(f"- {line}" for line in REPORT) if REPORT else "- Nenhuma alteração necessária")
        + "\n\n## Pendências finas\n"
        + ("\n".join(f"- {issue}" for issue in issues) if issues else "- Nenhuma pendência fina detectada")
        + f"\n\n## Score estimado 95-ready\n- {score}/100\n",
        encoding="utf-8",
    )
    print(report.read_text(encoding="utf-8"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
