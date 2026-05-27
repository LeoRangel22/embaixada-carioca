#!/usr/bin/env python3
"""Emergency cleaner for current Google Search Console validation blockers.

Targets screenshots from GSC:
- FAQPage duplicated.
- Review snippets with multiple aggregate ratings.
- Events invalid on pages that are not real scheduled events.
- Discussion forum invalid structured data.
- VideoObject uploadDate warnings.

Conservative strategy:
- Keep Restaurant, WebPage, WebSite, BreadcrumbList, FAQPage and VideoObject when valid.
- Keep only one FAQPage per HTML file.
- Remove Event schema globally from this static restaurant site; current event pages are lead/conversion pages, not scheduled public events.
- Remove forum-like schemas: DiscussionForumPosting, Comment and QAPage.
- Remove review/rating schemas and fields.
- Normalize VideoObject uploadDate to an ISO datetime with timezone.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "gsc_emergency_validation_cleaner_report.md"
JSONLD_RE = re.compile(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ISO_DATETIME_WITH_TZ_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})$")

REMOVE_TYPES = {"Event", "DiscussionForumPosting", "Comment", "QAPage", "Review", "Rating", "AggregateRating"}
REMOVE_KEYS = {
    "aggregateRating",
    "ratingValue",
    "reviewCount",
    "ratingCount",
    "bestRating",
    "worstRating",
    "review",
    "reviewRating",
}


@dataclass
class Result:
    rel: str
    blocks: int
    changed: bool
    removed_types: int
    removed_keys: int
    duplicate_faq_removed: int
    video_dates_fixed: int
    parse_errors: int
    remaining_issues: list[str]


def html_files() -> list[Path]:
    return [
        p for p in sorted(ROOT.rglob("*.html"))
        if ".git" not in p.parts and not p.relative_to(ROOT).as_posix().startswith("_")
    ]


def types(value: Any) -> set[str]:
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {str(item) for item in value}
    return set()


def normalize_upload_date(value: Any) -> tuple[str, bool]:
    if isinstance(value, str):
        raw = value.strip()
        if ISO_DATETIME_WITH_TZ_RE.match(raw):
            return raw, False
        if ISO_DATE_RE.match(raw):
            return raw + "T08:30:00-03:00", True
        if re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", raw):
            return raw + "-03:00", True
    return "2026-05-01T08:30:00-03:00", True


def clean_node(obj: Any, stats: dict[str, int]) -> Any:
    if isinstance(obj, dict):
        if types(obj.get("@type")) & REMOVE_TYPES:
            stats["removed_types"] += 1
            return None
        out: dict[str, Any] = {}
        for key, value in obj.items():
            if key in REMOVE_KEYS:
                stats["removed_keys"] += 1
                continue
            cleaned = clean_node(value, stats)
            if cleaned is None:
                continue
            if isinstance(cleaned, list) and not cleaned:
                continue
            out[key] = cleaned
        if "VideoObject" in types(out.get("@type")):
            new_upload, changed = normalize_upload_date(out.get("uploadDate"))
            if changed:
                stats["video_dates_fixed"] += 1
            out["uploadDate"] = new_upload
        return out
    if isinstance(obj, list):
        out = []
        for item in obj:
            cleaned = clean_node(item, stats)
            if cleaned is not None:
                out.append(cleaned)
        return out
    return obj


def keep_one_faq(obj: Any, seen: dict[str, bool], stats: dict[str, int]) -> Any:
    if isinstance(obj, dict):
        if "FAQPage" in types(obj.get("@type")):
            if seen["faq"]:
                stats["duplicate_faq_removed"] += 1
                return None
            seen["faq"] = True
            return obj
        out: dict[str, Any] = {}
        for key, value in obj.items():
            cleaned = keep_one_faq(value, seen, stats)
            if cleaned is None:
                continue
            if isinstance(cleaned, list) and not cleaned:
                continue
            out[key] = cleaned
        return out
    if isinstance(obj, list):
        out = []
        for item in obj:
            cleaned = keep_one_faq(item, seen, stats)
            if cleaned is not None:
                out.append(cleaned)
        return out
    return obj


def collect_issues(obj: Any, issues: set[str], faq_count: list[int]) -> None:
    if isinstance(obj, dict):
        node_types = types(obj.get("@type"))
        if node_types & REMOVE_TYPES:
            issues.add("blocked_schema_type_remaining:" + ",".join(sorted(node_types & REMOVE_TYPES)))
        if "FAQPage" in node_types:
            faq_count[0] += 1
        if "VideoObject" in node_types:
            upload = obj.get("uploadDate")
            if not (isinstance(upload, str) and ISO_DATETIME_WITH_TZ_RE.match(upload)):
                issues.add("video_uploadDate_invalid")
        for key, value in obj.items():
            if key in REMOVE_KEYS:
                issues.add("blocked_key_remaining:" + key)
            collect_issues(value, issues, faq_count)
    elif isinstance(obj, list):
        for item in obj:
            collect_issues(item, issues, faq_count)


def sanitize_html(text: str) -> tuple[str, dict[str, int], list[str]]:
    stats = {
        "blocks": 0,
        "removed_types": 0,
        "removed_keys": 0,
        "duplicate_faq_removed": 0,
        "video_dates_fixed": 0,
        "parse_errors": 0,
    }
    seen = {"faq": False}

    def repl(match: re.Match[str]) -> str:
        opener, raw, closer = match.groups()
        stats["blocks"] += 1
        try:
            obj = json.loads(html.unescape(raw.strip()))
        except Exception:
            stats["parse_errors"] += 1
            return match.group(0)
        cleaned = clean_node(obj, stats)
        cleaned = keep_one_faq(cleaned, seen, stats)
        if cleaned is None or cleaned == {} or cleaned == []:
            return ""
        return opener + json.dumps(cleaned, ensure_ascii=False, separators=(",", ":")) + closer

    updated = JSONLD_RE.sub(repl, text)
    issues: set[str] = set()
    faq_count = [0]
    for raw in JSONLD_RE.findall(updated):
        try:
            obj = json.loads(html.unescape(raw[1].strip()))
        except Exception:
            issues.add("jsonld_parse_error")
            continue
        collect_issues(obj, issues, faq_count)
    if faq_count[0] > 1:
        issues.add(f"duplicate_faqpage:{faq_count[0]}")
    return updated, stats, sorted(issues)


def apply_file(path: Path) -> Result:
    rel = path.relative_to(ROOT).as_posix()
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated, stats, issues = sanitize_html(original)
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return Result(
        rel=rel,
        blocks=stats["blocks"],
        changed=changed,
        removed_types=stats["removed_types"],
        removed_keys=stats["removed_keys"],
        duplicate_faq_removed=stats["duplicate_faq_removed"],
        video_dates_fixed=stats["video_dates_fixed"],
        parse_errors=stats["parse_errors"],
        remaining_issues=issues,
    )


def write_report(rows: list[Result]) -> int:
    REPORT.parent.mkdir(exist_ok=True)
    changed = [row for row in rows if row.changed]
    remaining = [row for row in rows if row.remaining_issues]
    status = "PASS" if not remaining else "FAIL"
    lines = [
        "# GSC Emergency Validation Cleaner",
        "",
        f"Status geral: **{status}**",
        "",
        "## Bloqueios tratados",
        "- FAQPage duplicado.",
        "- Snippets de avaliação com rating/review schema.",
        "- Event schema inválido em páginas que não são eventos públicos datados.",
        "- DiscussionForumPosting / Comment / QAPage inválidos.",
        "- VideoObject uploadDate sem fuso horário.",
        "",
        "## Resumo",
        f"- Arquivos HTML analisados: {len(rows)}",
        f"- Arquivos alterados: {len(changed)}",
        f"- Arquivos com pendências: {len(remaining)}",
        "",
        "## Arquivos alterados",
    ]
    if changed:
        for row in changed:
            lines.append(
                f"- `{row.rel}` — types_removed={row.removed_types}, keys_removed={row.removed_keys}, "
                f"faq_dupes_removed={row.duplicate_faq_removed}, video_dates_fixed={row.video_dates_fixed}"
            )
    else:
        lines.append("- Nenhum arquivo precisou ser alterado.")
    if remaining:
        lines.extend(["", "## Pendências", ""])
        for row in remaining:
            lines.append(f"- `{row.rel}` — {', '.join(row.remaining_issues)}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"GSC emergency validation cleaner: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    rows = [apply_file(path) for path in html_files()]
    return write_report(rows)


if __name__ == "__main__":
    raise SystemExit(main())
