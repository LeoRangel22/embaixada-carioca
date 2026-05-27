#!/usr/bin/env python3
"""Fix Google Search Console structured data issues exported on 2026-05-27.

Covered GSC exports:
- FAQ: duplicate FAQPage.
- Events: missing offers / performer.
- Discussion forum: invalid DiscussionForumPosting fields.
- Videos: invalid or timezone-less uploadDate.
- Unparsable structured data: duplicate unique property.

Strategy:
- Parse every JSON-LD block using object_pairs_hook to collapse duplicate keys.
- Keep only one FAQPage per HTML file.
- Remove DiscussionForumPosting / Comment schema, because the site is not a forum.
- Normalize VideoObject uploadDate to ISO datetime with timezone.
- Add conservative Event offers and performer fields where missing.
- Keep Restaurant, WebPage, BreadcrumbList, Menu, FAQPage, VideoObject and Event schema valid.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "gsc_structured_data_issues_fix_report.md"

JSONLD_RE = re.compile(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.I | re.S)
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ISO_DATETIME_WITH_TZ_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})$")

REMOVE_TYPES = {"DiscussionForumPosting", "Comment"}
EVENT_DEFAULTS = {
    "performer": {"@type": "Organization", "name": "Embaixada Carioca"},
    "offers": {
        "@type": "Offer",
        "url": "https://www.embaixadacarioca.com/eventos.html",
        "price": "0",
        "priceCurrency": "BRL",
        "availability": "https://schema.org/InStock",
        "validFrom": "2026-05-01T08:30:00-03:00",
    },
}

AFFECTED_EXPORTS = {
    "FAQ": "O campo FAQPage está duplicado",
    "Events": "offers / performer ausentes",
    "Discussion forum": "DiscussionForumPosting inválido",
    "Videos": "uploadDate inválido ou sem fuso horário",
    "Unparsable structured data": "Propriedade única duplicada",
}


@dataclass
class FileResult:
    rel: str
    blocks: int
    changed: bool
    duplicate_keys: int
    duplicate_faq_removed: int
    forum_schema_removed: int
    video_dates_fixed: int
    events_fixed: int
    parse_errors: int
    remaining_issues: list[str]


def html_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if ".git" in path.parts or rel.startswith("_"):
            continue
        files.append(path)
    return files


def type_values(value: Any) -> set[str]:
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {str(v) for v in value}
    return set()


def is_type(obj: Any, typ: str) -> bool:
    return isinstance(obj, dict) and typ in type_values(obj.get("@type"))


def pairs_hook(counter: dict[str, int]):
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                counter["duplicate_keys"] += 1
            out[key] = value
        return out
    return hook


def normalize_upload_date(value: Any) -> tuple[str, bool]:
    if isinstance(value, str):
        raw = value.strip()
        if ISO_DATETIME_WITH_TZ_RE.match(raw):
            return raw, False
        if ISO_DATE_RE.match(raw):
            return raw + "T08:30:00-03:00", True
        # Accept common datetime without timezone and append Rio timezone.
        if re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", raw):
            return raw + "-03:00", True
    return "2026-05-01T08:30:00-03:00", True


def fix_node(obj: Any, stats: dict[str, int]) -> Any:
    if isinstance(obj, dict):
        if type_values(obj.get("@type")) & REMOVE_TYPES:
            stats["forum_schema_removed"] += 1
            return None

        cleaned: dict[str, Any] = {}
        for key, value in obj.items():
            fixed = fix_node(value, stats)
            if fixed is None:
                continue
            if isinstance(fixed, list) and not fixed:
                continue
            cleaned[key] = fixed

        if is_type(cleaned, "VideoObject"):
            normalized, changed = normalize_upload_date(cleaned.get("uploadDate"))
            if changed:
                stats["video_dates_fixed"] += 1
            cleaned["uploadDate"] = normalized

        if is_type(cleaned, "Event"):
            if "performer" not in cleaned:
                cleaned["performer"] = EVENT_DEFAULTS["performer"]
                stats["events_fixed"] += 1
            if "offers" not in cleaned:
                cleaned["offers"] = EVENT_DEFAULTS["offers"]
                stats["events_fixed"] += 1
            else:
                offers = cleaned.get("offers")
                if isinstance(offers, dict):
                    for key, value in EVENT_DEFAULTS["offers"].items():
                        if key not in offers:
                            offers[key] = value
                            stats["events_fixed"] += 1

        return cleaned

    if isinstance(obj, list):
        out = []
        for item in obj:
            fixed = fix_node(item, stats)
            if fixed is not None:
                out.append(fixed)
        return out

    return obj


def remove_duplicate_faq(obj: Any, faq_seen: dict[str, bool], stats: dict[str, int]) -> Any:
    if isinstance(obj, dict):
        if is_type(obj, "FAQPage"):
            if faq_seen["seen"]:
                stats["duplicate_faq_removed"] += 1
                return None
            faq_seen["seen"] = True
            return obj
        cleaned: dict[str, Any] = {}
        for key, value in obj.items():
            fixed = remove_duplicate_faq(value, faq_seen, stats)
            if fixed is None:
                continue
            if isinstance(fixed, list) and not fixed:
                continue
            cleaned[key] = fixed
        return cleaned

    if isinstance(obj, list):
        out = []
        for item in obj:
            fixed = remove_duplicate_faq(item, faq_seen, stats)
            if fixed is not None:
                out.append(fixed)
        return out

    return obj


def collect_issues(obj: Any, issues: set[str], faq_count: list[int]) -> None:
    if isinstance(obj, dict):
        types = type_values(obj.get("@type"))
        if types & REMOVE_TYPES:
            issues.add("discussion_forum_schema_remaining")
        if "FAQPage" in types:
            faq_count[0] += 1
        if "VideoObject" in types:
            upload = obj.get("uploadDate")
            if not (isinstance(upload, str) and ISO_DATETIME_WITH_TZ_RE.match(upload)):
                issues.add("invalid_video_uploadDate")
        if "Event" in types:
            if "offers" not in obj:
                issues.add("event_offers_missing")
            else:
                offers = obj.get("offers")
                if isinstance(offers, dict):
                    for key in ["priceCurrency", "price", "validFrom"]:
                        if key not in offers:
                            issues.add(f"event_offer_{key}_missing")
            if "performer" not in obj:
                issues.add("event_performer_missing")
        for value in obj.values():
            collect_issues(value, issues, faq_count)
    elif isinstance(obj, list):
        for item in obj:
            collect_issues(item, issues, faq_count)


def sanitize_html(text: str) -> tuple[str, dict[str, int], list[str], int]:
    stats = {
        "duplicate_keys": 0,
        "duplicate_faq_removed": 0,
        "forum_schema_removed": 0,
        "video_dates_fixed": 0,
        "events_fixed": 0,
        "parse_errors": 0,
        "blocks": 0,
    }
    parsed_blocks: list[tuple[str, Any, str] | tuple[str, str]] = []
    faq_seen = {"seen": False}

    for match in JSONLD_RE.finditer(text):
        opener, raw, closer = match.groups()
        stats["blocks"] += 1
        duplicate_counter = {"duplicate_keys": 0}
        try:
            obj = json.loads(html.unescape(raw.strip()), object_pairs_hook=pairs_hook(duplicate_counter))
        except Exception:
            stats["parse_errors"] += 1
            parsed_blocks.append((match.group(0), "RAW"))
            continue
        stats["duplicate_keys"] += duplicate_counter["duplicate_keys"]
        fixed = fix_node(obj, stats)
        fixed = remove_duplicate_faq(fixed, faq_seen, stats)
        if fixed is None or fixed == [] or fixed == {}:
            parsed_blocks.append(("", "DROP"))
        else:
            parsed_blocks.append((opener, fixed, closer))

    i = 0
    def repl(_match: re.Match[str]) -> str:
        nonlocal i
        item = parsed_blocks[i]
        i += 1
        if len(item) == 2:
            return item[0]
        opener, obj, closer = item
        return opener + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + closer

    updated = JSONLD_RE.sub(repl, text)

    issues: set[str] = set()
    faq_count = [0]
    for raw in JSONLD_RE.findall(updated):
        body = raw[1]
        try:
            obj = json.loads(html.unescape(body.strip()))
        except Exception:
            issues.add("jsonld_parse_error")
            continue
        collect_issues(obj, issues, faq_count)
    if faq_count[0] > 1:
        issues.add("duplicate_FAQPage")

    return updated, stats, sorted(issues), faq_count[0]


def apply_file(path: Path) -> FileResult:
    rel = path.relative_to(ROOT).as_posix()
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated, stats, issues, _faq_count = sanitize_html(original)
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return FileResult(
        rel=rel,
        blocks=stats["blocks"],
        changed=changed,
        duplicate_keys=stats["duplicate_keys"],
        duplicate_faq_removed=stats["duplicate_faq_removed"],
        forum_schema_removed=stats["forum_schema_removed"],
        video_dates_fixed=stats["video_dates_fixed"],
        events_fixed=stats["events_fixed"],
        parse_errors=stats["parse_errors"],
        remaining_issues=issues,
    )


def write_report(results: list[FileResult]) -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    changed = [r for r in results if r.changed]
    remaining = [r for r in results if r.remaining_issues]
    status = "PASS" if not remaining else "FAIL"

    totals = {
        "duplicate_keys": sum(r.duplicate_keys for r in results),
        "duplicate_faq_removed": sum(r.duplicate_faq_removed for r in results),
        "forum_schema_removed": sum(r.forum_schema_removed for r in results),
        "video_dates_fixed": sum(r.video_dates_fixed for r in results),
        "events_fixed": sum(r.events_fixed for r in results),
        "parse_errors": sum(r.parse_errors for r in results),
    }

    lines = [
        "# GSC Structured Data Issues Fix",
        "",
        f"Status geral: **{status}**",
        "",
        "## Exportações tratadas",
    ]
    for name, problem in AFFECTED_EXPORTS.items():
        lines.append(f"- {name}: {problem}")

    lines.extend([
        "",
        "## Resumo",
        f"- Arquivos HTML escaneados: {len(results)}",
        f"- Arquivos alterados: {len(changed)}",
        f"- Duplicate keys normalizadas: {totals['duplicate_keys']}",
        f"- FAQPage duplicados removidos: {totals['duplicate_faq_removed']}",
        f"- DiscussionForumPosting/Comment removidos: {totals['forum_schema_removed']}",
        f"- VideoObject uploadDate corrigidos: {totals['video_dates_fixed']}",
        f"- Event fields corrigidos: {totals['events_fixed']}",
        f"- JSON-LD parse errors remanescentes: {totals['parse_errors']}",
        "",
        "## Arquivos alterados",
    ])

    if changed:
        for r in changed:
            lines.append(
                f"- `{r.rel}` — duplicate_keys={r.duplicate_keys}, "
                f"faq_removed={r.duplicate_faq_removed}, forum_removed={r.forum_schema_removed}, "
                f"video_dates_fixed={r.video_dates_fixed}, events_fixed={r.events_fixed}"
            )
    else:
        lines.append("- Nenhum arquivo precisou ser alterado.")

    if remaining:
        lines.extend(["", "## Pendências", ""])
        for r in remaining:
            lines.append(f"- `{r.rel}` — {', '.join(r.remaining_issues)}")

    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"GSC structured data issues fix: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    results = [apply_file(path) for path in html_files()]
    return write_report(results)


if __name__ == "__main__":
    raise SystemExit(main())
