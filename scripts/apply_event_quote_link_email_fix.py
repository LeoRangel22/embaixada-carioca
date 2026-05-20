#!/usr/bin/env python3
"""
Event Quote Link + Email Fix — Embaixada Carioca

Pedidos aplicados:
1. Em eventos.html, o botão "Solicitar cotação" deve apontar para:
   https://leorangel22.github.io/main/formulario.html
2. Todos os e-mails de eventos devem usar .com.br:
   eventos@embaixadacarioca.com.br

Também aplica equivalentes nas páginas EN/ES de eventos para manter consistência multilíngue.
"""
from __future__ import annotations

from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "event_quote_link_email_fix_report.md"
REPORT_CSV = REPORT_DIR / "event_quote_link_email_fix_details.csv"

FORM_URL = "https://leorangel22.github.io/main/formulario.html"
CORRECT_EMAIL = "eventos@embaixadacarioca.com.br"
WRONG_EMAIL_RE = re.compile(r"eventos@embaixadacarioca\.com(?!\.br)", re.I)

EVENT_PAGES = {
    "eventos.html": "Solicitar cotação",
    "en/eventos.html": "Request a quote",
    "es/eventos.html": "Solicitar cotización",
}

ANCHOR_RE = re.compile(r"<a\b([^>]*?)>([\s\S]*?)</a>", re.I)
HREF_RE = re.compile(r"href=(['\"])(.*?)\1", re.I)
QUOTE_TEXT_RE = re.compile(
    r"(solicitar\s+(?:or[cç]amento|cota[cç][aã]o)|pedir\s+cota[cç][aã]o|request\s+a\s+quote|ask\s+for\s+a\s+quote|solicitar\s+cotizaci[oó]n|pedir\s+cotizaci[oó]n)",
    re.I,
)
BUTTON_TEXT_RE = re.compile(
    r"(<button\b[^>]*>)([\s\S]*?)(</button>)",
    re.I,
)

SKIP_DIRS = {".git", "node_modules", ".next", "dist", "build"}
COUNTERS = {
    "files_scanned": 0,
    "files_updated": 0,
    "email_replacements": 0,
    "event_quote_links_updated": 0,
    "event_quote_texts_updated": 0,
    "form_buttons_updated": 0,
    "warnings": 0,
}
DETAILS: list[dict[str, object]] = []
WARNINGS: list[str] = []


def should_scan(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    return path.suffix.lower() in {".html", ".htm", ".js", ".json", ".md", ".txt", ".xml"}


def normalize_event_email(text: str, rel: str) -> str:
    text, count = WRONG_EMAIL_RE.subn(CORRECT_EMAIL, text)
    if count:
        COUNTERS["email_replacements"] += count
        DETAILS.append({"file": rel, "action": "email_replaced", "count": count})
    return text


def clean_anchor_text(html: str) -> str:
    html = re.sub(r"\s*(?:→|↗|›|»|➜|➔|➡|&rarr;|&#8594;|&#x2192;)\s*", "", html, flags=re.I)
    return re.sub(r"\s+", " ", html).strip()


def update_event_quote_anchors(text: str, rel: str, label: str) -> str:
    def repl(match: re.Match[str]) -> str:
        attrs = match.group(1)
        inner = match.group(2)
        href_match = HREF_RE.search(attrs)
        href = href_match.group(2) if href_match else ""
        inner_plain = re.sub(r"<[^>]+>", " ", inner)
        is_quote = bool(QUOTE_TEXT_RE.search(inner_plain)) or href in {"#cotacao", "#orcamento", "#quote", "#form", "#formulario"}
        if not is_quote:
            return match.group(0)
        if href_match:
            attrs_new = HREF_RE.sub(f'href="{FORM_URL}"', attrs, count=1)
        else:
            attrs_new = attrs + f' href="{FORM_URL}"'
        if "target=" not in attrs_new.lower():
            attrs_new += ' target="_blank"'
        if "rel=" not in attrs_new.lower():
            attrs_new += ' rel="noopener"'
        COUNTERS["event_quote_links_updated"] += 1
        if clean_anchor_text(inner) != label:
            COUNTERS["event_quote_texts_updated"] += 1
        return f"<a{attrs_new}>{label}</a>"

    return ANCHOR_RE.sub(repl, text)


def update_form_button_label(text: str, rel: str, label: str) -> str:
    # Mantém o formulário existente, mas padroniza a chamada para cotação e tira seta.
    def repl(match: re.Match[str]) -> str:
        full = match.group(0)
        inner_plain = re.sub(r"<[^>]+>", " ", match.group(2))
        if not QUOTE_TEXT_RE.search(inner_plain) and "pedido de orçamento" not in inner_plain.lower():
            return full
        COUNTERS["form_buttons_updated"] += 1
        return match.group(1) + label + match.group(3)
    return BUTTON_TEXT_RE.sub(repl, text)


def process_file(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    COUNTERS["files_scanned"] += 1
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = normalize_event_email(original, rel)
    if rel in EVENT_PAGES:
        label = EVENT_PAGES[rel]
        before = text
        text = update_event_quote_anchors(text, rel, label)
        text = update_form_button_label(text, rel, label)
        if text != before:
            DETAILS.append({"file": rel, "action": "quote_cta_updated", "count": 1})
        if FORM_URL not in text:
            WARNINGS.append(f"{rel}: external quote form URL not found after processing")
            COUNTERS["warnings"] += 1
        if WRONG_EMAIL_RE.search(text):
            WARNINGS.append(f"{rel}: old .com event email still found")
            COUNTERS["warnings"] += 1
    if text != original:
        path.write_text(text, encoding="utf-8")
        COUNTERS["files_updated"] += 1


def audit() -> None:
    # Garantias finais principais.
    for rel, label in EVENT_PAGES.items():
        path = ROOT / rel
        if not path.exists():
            WARNINGS.append(f"Missing event page: {rel}")
            COUNTERS["warnings"] += 1
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if FORM_URL not in text:
            WARNINGS.append(f"{rel}: missing {FORM_URL}")
            COUNTERS["warnings"] += 1
        if WRONG_EMAIL_RE.search(text):
            WARNINGS.append(f"{rel}: wrong event email remains")
            COUNTERS["warnings"] += 1
    # Busca global do e-mail antigo.
    for path in ROOT.rglob("*"):
        if path.is_file() and should_scan(path):
            rel = path.relative_to(ROOT).as_posix()
            text = path.read_text(encoding="utf-8", errors="ignore")
            if WRONG_EMAIL_RE.search(text):
                WARNINGS.append(f"{rel}: old eventos@embaixadacarioca.com remains")
                COUNTERS["warnings"] += 1


def write_reports() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    lines = [
        "# Event Quote Link + Email Fix",
        "",
        "## Objetivo",
        f"Apontar os CTAs de cotação de eventos para `{FORM_URL}` e normalizar o e-mail de eventos para `{CORRECT_EMAIL}`.",
        "",
        "## Veredito",
        f"- Status geral: {'PASS' if COUNTERS['warnings'] == 0 else 'WARN'}",
        f"- Warnings: {COUNTERS['warnings']}",
        "",
        "## Contadores",
    ]
    for key, value in COUNTERS.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Warnings"])
    lines.extend(f"- {w}" for w in WARNINGS) if WARNINGS else lines.append("- Nenhum.")
    lines.extend(["", "## Ações"])
    for d in DETAILS:
        lines.append(f"- {d['file']}: {d['action']} ({d['count']})")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    with REPORT_CSV.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["file", "action", "count"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for d in DETAILS:
            writer.writerow(d)
    print(REPORT_MD.read_text(encoding="utf-8"))


def main() -> int:
    for path in sorted(ROOT.rglob("*")):
        if path.is_file() and should_scan(path):
            process_file(path)
    audit()
    write_reports()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
