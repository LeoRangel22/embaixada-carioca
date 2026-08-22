#!/usr/bin/env python3
"""Post-fix validator for Google Search Console structured data issues.

Validates current repository against the GSC exports uploaded on 2026-05-27:
- FAQ duplicate FAQPage.
- Review snippets aggregate ratings.
- Discussion forum invalid forum schema.
- Unparsable structured data / duplicate unique JSON keys.
- Events missing offers or performer.
- Videos uploadDate without timezone.

This script does not modify HTML. It only writes a validation report.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
REPORT_MD = REPORT_DIR / "gsc_postfix_structured_data_validation.md"
JSONLD_RE = re.compile(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
ISO_DATETIME_WITH_TZ_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})$")

REVIEW_FORBIDDEN_TYPES = {"AggregateRating", "Rating", "Review"}
REVIEW_FORBIDDEN_KEYS = {"aggregateRating", "ratingValue", "reviewCount", "ratingCount", "bestRating", "worstRating", "review", "reviewRating"}
FORUM_TYPES = {"DiscussionForumPosting", "Comment"}


@dataclass
class PageCheck:
    rel: str
    jsonld_blocks: int
    parse_errors: int
    duplicate_keys: int
    faq_count: int
    review_terms: list[str]
    forum_terms: list[str]
    event_issues: list[str]
    video_issues: list[str]

    @property
    def issues(self) -> list[str]:
        out: list[str] = []
        if self.parse_errors:
            out.append(f"jsonld_parse_errors={self.parse_errors}")
        if self.duplicate_keys:
            out.append(f"duplicate_keys={self.duplicate_keys}")
        if self.faq_count > 1:
            out.append(f"duplicate_FAQPage={self.faq_count}")
        if self.review_terms:
            out.append("review_terms=" + ",".join(self.review_terms))
        if self.forum_terms:
            out.append("forum_terms=" + ",".join(self.forum_terms))
        out.extend(self.event_issues)
        out.extend(self.video_issues)
        return out


def html_files() -> list[Path]:
    excluded = {".git", ".github", ".codex-work", "node_modules", "dist", "build", "_site", "_audit_reports", "_backups", "archive", "_templates", "src", "scripts"}
    return [
        p for p in sorted(ROOT.rglob("*.html"))
        if not (set(p.relative_to(ROOT).parts) & excluded)
    ]


def type_values(value: Any) -> set[str]:
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {str(v) for v in value}
    return set()


def pairs_hook(counter: dict[str, int]):
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                counter["duplicate_keys"] += 1
            out[key] = value
        return out
    return hook


def walk(obj: Any, stats: dict[str, Any]) -> None:
    if isinstance(obj, dict):
        types = type_values(obj.get("@type"))
        if "FAQPage" in types:
            stats["faq_count"] += 1
        for t in sorted(types & REVIEW_FORBIDDEN_TYPES):
            stats["review_terms"].add(t)
        for t in sorted(types & FORUM_TYPES):
            stats["forum_terms"].add(t)
        for key in obj.keys():
            if key in REVIEW_FORBIDDEN_KEYS:
                stats["review_terms"].add(key)

        if "Event" in types:
            if "offers" not in obj:
                stats["event_issues"].add("event_offers_missing")
            if "performer" not in obj:
                stats["event_issues"].add("event_performer_missing")
            offers = obj.get("offers")
            if isinstance(offers, dict):
                for key in ["price", "priceCurrency", "validFrom"]:
                    if key not in offers:
                        stats["event_issues"].add(f"event_offer_{key}_missing")

        if "VideoObject" in types:
            upload = obj.get("uploadDate")
            if not (isinstance(upload, str) and ISO_DATETIME_WITH_TZ_RE.match(upload)):
                stats["video_issues"].add("video_uploadDate_invalid_or_missing_timezone")

        for value in obj.values():
            walk(value, stats)
    elif isinstance(obj, list):
        for item in obj:
            walk(item, stats)


def check_file(path: Path) -> PageCheck:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="ignore")
    stats: dict[str, Any] = {
        "jsonld_blocks": 0,
        "parse_errors": 0,
        "duplicate_keys": 0,
        "faq_count": 0,
        "review_terms": set(),
        "forum_terms": set(),
        "event_issues": set(),
        "video_issues": set(),
    }
    for match in JSONLD_RE.finditer(text):
        stats["jsonld_blocks"] += 1
        raw = match.group(1).strip()
        counter = {"duplicate_keys": 0}
        try:
            obj = json.loads(html.unescape(raw), object_pairs_hook=pairs_hook(counter))
        except Exception:
            stats["parse_errors"] += 1
            continue
        stats["duplicate_keys"] += counter["duplicate_keys"]
        walk(obj, stats)
    return PageCheck(
        rel=rel,
        jsonld_blocks=stats["jsonld_blocks"],
        parse_errors=stats["parse_errors"],
        duplicate_keys=stats["duplicate_keys"],
        faq_count=stats["faq_count"],
        review_terms=sorted(stats["review_terms"]),
        forum_terms=sorted(stats["forum_terms"]),
        event_issues=sorted(stats["event_issues"]),
        video_issues=sorted(stats["video_issues"]),
    )


def write_report(rows: list[PageCheck]) -> int:
    REPORT_DIR.mkdir(exist_ok=True)
    problem_rows = [r for r in rows if r.issues]
    status = "PASS" if not problem_rows else "FAIL"

    lines = [
        "# GSC Post-fix Structured Data Validation",
        "",
        f"Status geral: **{status}**",
        "",
        "## Critérios validados",
        "- Nenhum FAQPage duplicado por página.",
        "- Nenhum AggregateRating/Rating/Review ou campo de rating/review no JSON-LD.",
        "- Nenhum DiscussionForumPosting/Comment no JSON-LD.",
        "- Nenhuma chave JSON-LD duplicada detectada via parser com object_pairs_hook.",
        "- Event schema, quando presente, deve ter offers e performer.",
        "- VideoObject, quando presente, deve ter uploadDate com fuso horário.",
        "",
        "## Resumo",
        f"- Arquivos HTML analisados: {len(rows)}",
        f"- Arquivos com pendências: {len(problem_rows)}",
        "",
    ]

    if problem_rows:
        lines.extend(["## Pendências", "", "| Arquivo | Pendências |", "|---|---|"])
        for row in problem_rows:
            lines.append(f"| `{row.rel}` | {'; '.join(row.issues)} |")
    else:
        lines.append("## Pendências")
        lines.append("")
        lines.append("- Nenhuma.")

    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"GSC post-fix structured data validation: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    rows = [check_file(path) for path in html_files()]
    return write_report(rows)


if __name__ == "__main__":
    raise SystemExit(main())
