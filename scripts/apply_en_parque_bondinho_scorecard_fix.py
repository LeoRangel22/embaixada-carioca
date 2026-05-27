#!/usr/bin/env python3
"""Fix scorecard gaps on en/parque-bondinho.html.

Targets:
- Add one FAQPage with 8 English questions.
- Add one visible ordered-list section.
- Fix mixed PT/EN title metadata.
- Keep Restaurant/Article/Breadcrumb JSON-LD intact.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "en" / "parque-bondinho.html"
REPORT = ROOT / "_audit_reports" / "en_parque_bondinho_scorecard_fix_report.md"

FAQ_MARKER_START = "<!-- EC EN PARQUE BONDINHO FAQ FIX -->"
FAQ_MARKER_END = "<!-- /EC EN PARQUE BONDINHO FAQ FIX -->"
VISIBLE_START = "<!-- EC EN PARQUE BONDINHO OL FIX -->"
VISIBLE_END = "<!-- /EC EN PARQUE BONDINHO OL FIX -->"
STYLE_ID = "ec-en-parque-bondinho-scorecard-css"
JSONLD_RE = re.compile(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)

FAQS = [
    ("Is Embaixada Carioca inside Sugarloaf Cable Car Park?", "Yes. Embaixada Carioca is located at Morro da Urca, the first stop of the Sugarloaf Cable Car, inside Parque Bondinho Pão de Açúcar."),
    ("Do I need a cable car ticket to visit Embaixada Carioca?", "The usual access is through Sugarloaf Cable Car Park with a cable car ticket to Morro da Urca. If you hike up when the trail is open, you only need a ticket if you use the cable car."),
    ("When do I need to pay for the cable car?", "You need a ticket if you decide to use the cable car to continue to Sugarloaf Mountain or to go down from Morro da Urca to Praia Vermelha."),
    ("Can I reach Morro da Urca by trail?", "Yes. The Morro da Urca trail through Pista Cláudio Coutinho can be an alternative when it is open and allowed by the park rules."),
    ("Where is the entrance to Sugarloaf Cable Car Park?", "The main entrance is at Av. Pasteur, 520, Urca, Rio de Janeiro, next to Praia Vermelha."),
    ("What can I eat at Morro da Urca?", "Embaixada Carioca serves breakfast, Brazilian lunch, feijoada, grilled steak, snacks, caipirinhas, draft beer and drinks during the visit."),
    ("Can I reserve a table at Embaixada Carioca?", "Yes. Reservations are recommended for weekends, holidays, groups and busy hours, especially for breakfast, lunch and special visits."),
    ("Is Embaixada Carioca good for tourists?", "Yes. The restaurant is designed for visitors who want a practical Brazilian food stop with a view during the Sugarloaf Cable Car experience."),
]


@dataclass
class Result:
    status: str
    changed: bool
    faq_pages: int
    faq_questions: int
    ol_count: int
    words: int
    title_ok: bool
    notes: str


def strip_block(source: str, start: str, end: str) -> str:
    return re.sub(re.escape(start) + r"[\s\S]*?" + re.escape(end) + r"\s*", "", source, flags=re.I)


def parse_json(raw: str) -> Any | None:
    try:
        return json.loads(html.unescape(raw.strip()))
    except Exception:
        return None


def typ_has(value: Any, wanted: str) -> bool:
    if isinstance(value, str):
        return value.lower() == wanted.lower()
    if isinstance(value, list):
        return any(typ_has(v, wanted) for v in value)
    return False


def is_faq(obj: Any) -> bool:
    return isinstance(obj, dict) and typ_has(obj.get("@type"), "FAQPage")


def strip_faq(obj: Any) -> tuple[Any | None, int]:
    if is_faq(obj):
        return None, 1
    if isinstance(obj, dict):
        cleaned: dict[str, Any] = {}
        removed = 0
        for key, value in obj.items():
            new_value, count = strip_faq(value)
            removed += count
            if new_value is None:
                continue
            if isinstance(new_value, list) and not new_value:
                continue
            cleaned[key] = new_value
        return cleaned if cleaned else None, removed
    if isinstance(obj, list):
        kept = []
        removed = 0
        for item in obj:
            new_item, count = strip_faq(item)
            removed += count
            if new_item is not None:
                kept.append(new_item)
        return kept, removed
    return obj, 0


def remove_existing_faq_jsonld(source: str) -> tuple[str, int]:
    removed_total = 0
    parts: list[str] = []
    last = 0
    for m in JSONLD_RE.finditer(source):
        opener, raw, closer = m.groups()
        obj = parse_json(raw)
        if obj is None:
            continue
        cleaned, removed = strip_faq(obj)
        if not removed:
            continue
        parts.append(source[last:m.start()])
        if cleaned is not None:
            parts.append(opener + json.dumps(cleaned, ensure_ascii=False, separators=(",", ":")) + closer)
        last = m.end()
        removed_total += removed
    if not removed_total:
        return source, 0
    parts.append(source[last:])
    return "".join(parts), removed_total


def faq_block() -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/en/parque-bondinho.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQS
        ],
    }
    return f"{FAQ_MARKER_START}\n<script type=\"application/ld+json\">{json.dumps(payload, ensure_ascii=False, separators=(',', ':'))}</script>\n{FAQ_MARKER_END}\n"


def ensure_style(source: str) -> str:
    if STYLE_ID in source:
        return source
    css = f"""
<style id="{STYLE_ID}">
.ec-en-bondinho-guide{{background:#fff8ea;color:#00405a;border-top:1px solid rgba(0,64,90,.10);padding:56px 0;font-family:Catamaran,Verdana,system-ui,sans-serif}}
.ec-en-bondinho-guide .wrap{{max-width:1080px;margin:0 auto;padding:0 var(--gutter,64px)}}
.ec-en-bondinho-guide .kicker{{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#527f8f;margin-bottom:12px}}
.ec-en-bondinho-guide h2{{font-size:clamp(28px,3.4vw,46px);line-height:1.1;margin:0 0 16px;color:#00405a}}
.ec-en-bondinho-guide p{{font-size:18px;line-height:1.64;color:#485156;max-width:900px;margin:0 0 16px}}
.ec-en-bondinho-guide ol{{background:#fff;border:1px solid rgba(0,64,90,.12);border-radius:18px;padding:22px 24px 22px 46px;margin:22px 0 0;color:#485156;box-shadow:0 12px 30px rgba(0,64,90,.05)}}
.ec-en-bondinho-guide li{{margin:8px 0;line-height:1.55}}
@media(max-width:760px){{.ec-en-bondinho-guide{{padding:40px 0}}.ec-en-bondinho-guide .wrap{{padding:0 20px}}.ec-en-bondinho-guide p{{font-size:16px}}}}
</style>
""".strip()
    return source.replace("</head>", css + "\n</head>", 1) if "</head>" in source else css + "\n" + source


def visible_block() -> str:
    return f"""
{VISIBLE_START}
<section class="ec-en-bondinho-guide" aria-label="How to visit Sugarloaf Cable Car Park and Embaixada Carioca">
  <div class="wrap">
    <div class="kicker">Visit planning</div>
    <h2>How to combine Sugarloaf Cable Car Park with Embaixada Carioca</h2>
    <p>Embaixada Carioca is at Morro da Urca, the first cable car stop inside Sugarloaf Cable Car Park. The usual way to arrive is with a park ticket through the cable car entrance on Av. Pasteur, 520, in Urca.</p>
    <p>There is also an alternative route through the Morro da Urca trail, when it is open and allowed. Visitors who hike up and remain at Morro da Urca do not need to pay a cable car ticket just to visit Embaixada Carioca. A ticket is required if they use the cable car to continue to Sugarloaf Mountain or to go down to Praia Vermelha.</p>
    <ol>
      <li>Choose whether you will arrive by cable car ticket or by the Morro da Urca trail when it is open.</li>
      <li>If using the cable car, enter Sugarloaf Cable Car Park at Av. Pasteur, 520, Urca.</li>
      <li>Get off at Morro da Urca, the first cable car stop.</li>
      <li>Stop at Embaixada Carioca for breakfast, lunch, feijoada, caipirinhas, draft beer or a group experience.</li>
      <li>Use the cable car ticket if you want to continue to Sugarloaf Mountain or go down to Praia Vermelha by cable car.</li>
    </ol>
  </div>
</section>
{VISIBLE_END}
""".strip()


def insert_head(source: str, payload: str) -> str:
    return source.replace("</head>", payload + "</head>", 1) if "</head>" in source else payload + source


def insert_visible(source: str, payload: str) -> str:
    if "</main>" in source:
        return source.replace("</main>", payload + "\n</main>", 1)
    if "</body>" in source:
        return source.replace("</body>", payload + "\n</body>", 1)
    return source + "\n" + payload


def update_metadata(source: str) -> str:
    source = re.sub(r"<title>.*?</title>", "<title>Sugarloaf Cable Car Park | Embaixada Carioca</title>", source, count=1, flags=re.I | re.S)
    source = re.sub(r'<meta\s+content="[^"]*"\s+property="og:title"\s*/?>', '<meta content="Sugarloaf Cable Car Park | Embaixada Carioca" property="og:title"/>', source, count=1, flags=re.I)
    source = re.sub(r'<meta\s+content="[^"]*"\s+name="keywords"\s*/?>', '<meta content="Sugarloaf Cable Car Park, Sugarloaf cable car tickets, Sugarloaf Mountain Rio de Janeiro, restaurant inside Sugarloaf Cable Car Park, where to eat at Morro da Urca" name="keywords"/>', source, count=1, flags=re.I)
    source = source.replace('"headline":"Bondinho Pão de Açúcar Park: Guia Completo 2026 — Ingressos, Horários e Restaurant"', '"headline":"Sugarloaf Cable Car Park: Complete 2026 Guide — Tickets, Hours and Where to Eat"')
    source = source.replace('"description":"Guia completo do Bondinho Pão de Açúcar Park: ingressos, horários, how to get there, o que fazer e onde comer."', '"description":"Complete guide to Sugarloaf Cable Car Park: tickets, hours, how to get there, what to do and where to eat."')
    return source


def count_faq(source: str) -> tuple[int, int]:
    pages = 0
    questions = 0
    for _, raw, _ in JSONLD_RE.findall(source):
        obj = parse_json(raw)
        if obj is None:
            continue
        stack = [obj]
        while stack:
            item = stack.pop()
            if isinstance(item, dict):
                if is_faq(item):
                    pages += 1
                    main = item.get("mainEntity")
                    if isinstance(main, list):
                        questions += len(main)
                stack.extend(item.values())
            elif isinstance(item, list):
                stack.extend(item)
    return pages, questions


def count_words(source: str) -> int:
    text = re.sub(r"<script[\s\S]*?</script>", " ", source, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"\b[\wÀ-ÿ]{2,}\b", html.unescape(text)))


def apply() -> Result:
    if not PAGE.exists():
        return Result("missing", False, 0, 0, 0, 0, False, "file missing")
    original = PAGE.read_text(encoding="utf-8", errors="ignore")
    updated = strip_block(original, FAQ_MARKER_START, FAQ_MARKER_END)
    updated = strip_block(updated, VISIBLE_START, VISIBLE_END)
    updated, removed = remove_existing_faq_jsonld(updated)
    updated = update_metadata(updated)
    updated = ensure_style(updated)
    updated = insert_head(updated, faq_block())
    updated = insert_visible(updated, visible_block())
    changed = updated != original
    if changed:
        PAGE.write_text(updated, encoding="utf-8")
    faq_pages, faq_questions = count_faq(updated)
    ol_count = len(re.findall(r"<ol\b", updated, flags=re.I))
    words = count_words(updated)
    title_ok = "Parque Bondinho cable car" not in updated and "Sugarloaf Cable Car Park | Embaixada Carioca" in updated
    status = "ok" if faq_pages == 1 and faq_questions == 8 and ol_count >= 1 and title_ok else "fail"
    return Result(status, changed, faq_pages, faq_questions, ol_count, words, title_ok, f"removed_existing_faq={removed}")


def write_report(result: Result) -> int:
    REPORT.parent.mkdir(exist_ok=True)
    overall = "PASS" if result.status == "ok" else "FAIL"
    lines = [
        "# EN Parque Bondinho Scorecard Fix",
        "",
        f"Status geral: **{overall}**",
        "",
        "## Objetivo",
        "Corrigir os gaps de `en/parque-bondinho.html`: FAQ ausente, lista `<ol>` ausente e title misto PT/EN.",
        "",
        "## Resultado",
        f"- Página: `en/parque-bondinho.html`",
        f"- Status: `{result.status}`",
        f"- Changed: `{result.changed}`",
        f"- FAQPage: `{result.faq_pages}`",
        f"- Perguntas FAQ: `{result.faq_questions}`",
        f"- Listas `<ol>`: `{result.ol_count}`",
        f"- Palavras: `{result.words}`",
        f"- Title corrigido: `{result.title_ok}`",
        f"- Notas: `{result.notes}`",
        "",
        "## Guardrails",
        "- Nenhum Rating, Review ou AggregateRating foi inserido.",
        "- Article, BreadcrumbList e Restaurant/mentions existentes foram preservados.",
        "- Foi criado apenas um FAQPage com 8 perguntas em inglês.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"EN Parque Bondinho scorecard fix: {overall}")
    return 0 if overall == "PASS" else 1


def main() -> int:
    return write_report(apply())


if __name__ == "__main__":
    raise SystemExit(main())
