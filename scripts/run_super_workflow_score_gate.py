#!/usr/bin/env python3
"""
Embaixada Carioca — Super Workflow Score Gate Runner

Executa os principais scripts que alimentam os workflows de auditoria, consolida relatórios
por workflow e repete até todos ficarem >= SCORE_THRESHOLD.
"""

from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import time
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "_audit_reports"
SCORE_MD = REPORT_DIR / "super_workflow_score_gate.md"
SCORE_CSV = REPORT_DIR / "super_workflow_score_gate.csv"
SCORE_JSON = REPORT_DIR / "super_workflow_score_gate.json"

THRESHOLD = int(os.environ.get("SCORE_THRESHOLD", "90"))
MAX_ATTEMPTS = int(os.environ.get("MAX_ATTEMPTS", "4"))
WAIT_SECONDS = int(os.environ.get("WAIT_SECONDS", "120"))

@dataclass
class AuditTask:
    name: str
    commands: list[str]
    reports: list[str]
    workflow_file: str

@dataclass
class TaskResult:
    attempt: int
    name: str
    workflow_file: str
    status: str
    score: float
    command_status: int
    reports_found: list[str]
    missing_reports: list[str]
    notes: str

TASKS = [
    AuditTask(
        name="Superholistic visual readability lock",
        workflow_file=".github/workflows/super-workflow-score-gate.yml",
        commands=["python3 scripts/apply_superholistic_visual_readability_lock.py"],
        reports=["_audit_reports/superholistic_visual_readability_lock_report.md"],
    ),
    AuditTask(
        name="Final 86-page AAA master audit",
        workflow_file=".github/workflows/final-86page-aaa-master-audit.yml",
        commands=["python3 scripts/apply_final_86page_aaa_master_audit.py"],
        reports=["_audit_reports/final_86page_aaa_master_audit_report.md", "_audit_reports/final_86page_aaa_master_audit_details.csv"],
    ),
    AuditTask(
        name="Visual contrast risk audit",
        workflow_file=".github/workflows/visual-contrast-risk-audit.yml",
        commands=["python3 scripts/apply_hero_side_frame_final_lock.py", "python3 scripts/audit_visual_contrast_risks.py"],
        reports=["_audit_reports/hero_side_frame_final_lock_report.md", "_audit_reports/visual_contrast_risk_audit.md"],
    ),
    AuditTask(
        name="Phase 2 performance SEO audit",
        workflow_file=".github/workflows/phase2-performance-seo-audit.yml",
        commands=[
            "python3 scripts/apply_phase2_quick_fixes.py",
            "python3 scripts/apply_visible_text_css_link.py",
            "python3 scripts/apply_como_chegar_final_visible_lock.py",
            "python3 scripts/audit_phase2_performance_seo.py",
        ],
        reports=[
            "_audit_reports/phase2_quick_fixes_report.md",
            "_audit_reports/visible_text_css_link_report.md",
            "_audit_reports/como_chegar_final_visible_lock_report.md",
            "_audit_reports/phase2_performance_seo_audit.md",
        ],
    ),
    AuditTask(
        name="Super site standards SEO audit",
        workflow_file=".github/workflows/super-site-standards-seo-audit.yml",
        commands=["python3 scripts/super_site_standards_seo_audit.py"],
        reports=["_audit_reports/super_site_standards_seo_audit.md", "_audit_reports/super_site_standards_seo_audit_details.csv"],
    ),
    AuditTask(
        name="Priority keywords AIO score audit",
        workflow_file=".github/workflows/super-workflow-score-gate.yml",
        commands=["python3 scripts/audit_priority_keywords_aio_score.py"],
        reports=[
            "_audit_reports/priority_keywords_aio_score_audit.md",
            "_audit_reports/priority_keywords_aio_score_audit.csv",
            "_audit_reports/priority_keywords_aio_score_audit.json",
        ],
    ),
    AuditTask(
        name="GSC real organic queries score audit",
        workflow_file=".github/workflows/super-workflow-score-gate.yml",
        commands=["python3 scripts/audit_gsc_real_queries_score.py"],
        reports=[
            "_audit_reports/gsc_real_queries_score_audit.md",
            "_audit_reports/gsc_real_queries_score_audit.csv",
            "_audit_reports/gsc_real_queries_score_audit.json",
        ],
    ),
    AuditTask(
        name="Superholistic design UX SEO GEO audit",
        workflow_file=".github/workflows/super-workflow-score-gate.yml",
        commands=["python3 scripts/superholistic_design_ux_seo_geo_audit.py"],
        reports=[
            "_audit_reports/superholistic_design_ux_seo_geo_audit.md",
            "_audit_reports/superholistic_design_ux_seo_geo_audit.csv",
            "_audit_reports/superholistic_design_ux_seo_geo_audit.json",
        ],
    ),
]


def run_command(cmd: str) -> int:
    print(f"\n$ {cmd}", flush=True)
    proc = subprocess.run(cmd, shell=True, cwd=ROOT)
    print(f"exit={proc.returncode}", flush=True)
    return proc.returncode


def text_score(text: str) -> float | None:
    candidates: list[float] = []
    patterns = [
        r"score\s*[:=]?\s*(\d+(?:\.\d+)?)",
        r"score\s+m[ií]nimo\s*[:=]?\s*\*\*?(\d+(?:\.\d+)?)",
        r"score\s+m[eé]dio\s*[:=]?\s*\*\*?(\d+(?:\.\d+)?)",
    ]
    for pattern in patterns:
        for m in re.finditer(pattern, text, flags=re.I):
            try:
                value = float(m.group(1))
                if 0 <= value <= 100:
                    candidates.append(value)
            except ValueError:
                pass
    if "status: **pass**" in text.lower() or "status geral: **pass**" in text.lower():
        candidates.append(100.0)
    if "status: **fail**" in text.lower() or "status geral: **fail**" in text.lower():
        candidates.append(0.0)
    if not candidates:
        return None
    return min(candidates)


def csv_score(path: Path) -> float | None:
    try:
        with path.open("r", encoding="utf-8", newline="") as fp:
            reader = csv.DictReader(fp)
            scores = []
            for row in reader:
                raw = row.get("score") or row.get("Score") or row.get("dimension_score")
                if not raw:
                    continue
                try:
                    val = float(str(raw).strip())
                    if 0 <= val <= 100:
                        scores.append(val)
                except ValueError:
                    continue
            return min(scores) if scores else None
    except Exception:
        return None


def json_score(path: Path) -> float | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    for key in ("min_score", "score", "average_score"):
        value = data.get(key) if isinstance(data, dict) else None
        if isinstance(value, (int, float)) and 0 <= value <= 100:
            return float(value)
    if isinstance(data, dict) and isinstance(data.get("results"), list):
        scores = [item.get("score") for item in data["results"] if isinstance(item, dict) and isinstance(item.get("score"), (int, float))]
        if scores:
            return float(min(scores))
    return None


def infer_report_score(path: Path) -> float | None:
    if not path.exists():
        return None
    if path.suffix.lower() == ".csv":
        score = csv_score(path)
        if score is not None:
            return score
    if path.suffix.lower() == ".json":
        score = json_score(path)
        if score is not None:
            return score
    try:
        return text_score(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return None


def score_task(task: AuditTask, attempt: int, command_status: int) -> TaskResult:
    report_scores: list[float] = []
    found: list[str] = []
    missing: list[str] = []
    notes: list[str] = []
    for report in task.reports:
        path = ROOT / report
        if path.exists():
            found.append(report)
            score = infer_report_score(path)
            if score is not None:
                report_scores.append(score)
                notes.append(f"{report}: {score:.1f}")
            else:
                score = 90.0 if command_status == 0 else 0.0
                report_scores.append(score)
                notes.append(f"{report}: sem score explícito; tratado como {score:.1f}")
        else:
            missing.append(report)
            report_scores.append(0.0)
    score = min(report_scores) if report_scores else 0.0
    status = "PASS" if command_status == 0 and score >= THRESHOLD and not missing else "FAIL"
    return TaskResult(attempt, task.name, task.workflow_file, status, score, command_status, found, missing, "; ".join(notes))


def write_score_reports(results: list[TaskResult]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    latest: dict[str, TaskResult] = {}
    for result in results:
        latest[result.name] = result
    status = "PASS" if latest and all(r.status == "PASS" and r.score >= THRESHOLD for r in latest.values()) else "FAIL"
    SCORE_JSON.write_text(json.dumps({
        "status": status,
        "threshold": THRESHOLD,
        "max_attempts": MAX_ATTEMPTS,
        "wait_seconds": WAIT_SECONDS,
        "results": [asdict(r) for r in results],
        "latest": {k: asdict(v) for k, v in latest.items()},
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    with SCORE_CSV.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=["attempt", "workflow", "workflow_file", "status", "score", "command_status", "reports_found", "missing_reports", "notes"])
        writer.writeheader()
        for r in results:
            writer.writerow({
                "attempt": r.attempt,
                "workflow": r.name,
                "workflow_file": r.workflow_file,
                "status": r.status,
                "score": f"{r.score:.1f}",
                "command_status": r.command_status,
                "reports_found": " | ".join(r.reports_found),
                "missing_reports": " | ".join(r.missing_reports),
                "notes": r.notes,
            })
    lines = [
        "# Super Workflow Score Gate",
        "",
        f"Status geral: **{status}**",
        f"Threshold: **{THRESHOLD}**",
        f"Max attempts: **{MAX_ATTEMPTS}**",
        f"Wait between attempts: **{WAIT_SECONDS}s**",
        "",
        "## Último resultado por workflow",
        "",
        "| Workflow | Status | Score | Reports | Pendências |",
        "|---|---:|---:|---|---|",
    ]
    for r in latest.values():
        reports = "<br>".join(r.reports_found) if r.reports_found else "—"
        missing = "<br>".join(r.missing_reports) if r.missing_reports else "—"
        lines.append(f"| {r.name} | {r.status} | {r.score:.1f} | {reports} | {missing} |")
    lines += ["", "## Histórico de tentativas", ""]
    for r in results:
        lines.append(f"- Attempt {r.attempt} — **{r.name}**: {r.status}, score {r.score:.1f}, command exit {r.command_status}")
        if r.notes:
            lines.append(f"  - {r.notes}")
    SCORE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_attempt(attempt: int) -> list[TaskResult]:
    print(f"\n=== SUPER WORKFLOW ATTEMPT {attempt}/{MAX_ATTEMPTS} ===", flush=True)
    attempt_results: list[TaskResult] = []
    for task in TASKS:
        command_status = 0
        for cmd in task.commands:
            parts = cmd.split()
            script = parts[1] if len(parts) > 1 else ""
            if script and not (ROOT / script).exists():
                print(f"Missing script: {script}", flush=True)
                command_status = 127
                break
            rc = run_command(cmd)
            if rc != 0:
                command_status = rc
                break
        result = score_task(task, attempt, command_status)
        print(f"{task.name}: {result.status} score={result.score:.1f}", flush=True)
        attempt_results.append(result)
    return attempt_results


def main() -> int:
    all_results: list[TaskResult] = []
    for attempt in range(1, MAX_ATTEMPTS + 1):
        attempt_results = run_attempt(attempt)
        all_results.extend(attempt_results)
        write_score_reports(all_results)
        if all(r.status == "PASS" and r.score >= THRESHOLD for r in attempt_results):
            print(f"All workflows reached >= {THRESHOLD} on attempt {attempt}.", flush=True)
            return 0
        if attempt < MAX_ATTEMPTS:
            print(f"Not all workflows reached >= {THRESHOLD}. Waiting {WAIT_SECONDS}s before next attempt.", flush=True)
            time.sleep(WAIT_SECONDS)
    print(f"Some workflows are still below {THRESHOLD} after {MAX_ATTEMPTS} attempts.", flush=True)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
