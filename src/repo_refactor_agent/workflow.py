"""End-to-end orchestration for the refactoring agent."""

from __future__ import annotations

from pathlib import Path

from .analyzer import AnalyzerAgent
from .models import WorkflowResult
from .planner import PlannerAgent
from .reporter import ReporterAgent
from .scanner import iter_source_files
from .verifier import VerifierAgent


def run_workflow(root: Path, output: Path | None = None) -> WorkflowResult:
    """Run the scanner/analyzer/planner/reporter/verifier chain for *root*."""

    root = root.resolve()
    output = (output or root / "refactor_plan.md").resolve()

    files = [path for path in iter_source_files(root) if path.resolve() != output]
    findings = AnalyzerAgent().analyze(files)
    tasks = PlannerAgent().plan(findings)
    report_path = ReporterAgent().write(root, findings, tasks, output)

    result = WorkflowResult(
        root=root,
        findings=findings,
        tasks=tasks,
        report_path=report_path,
        changed_files=[report_path],
    )
    result.verification = VerifierAgent().verify(result)
    return result
