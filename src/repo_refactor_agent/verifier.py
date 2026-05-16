"""Verifier agent for post-run checks."""

from __future__ import annotations

from pathlib import Path

from .models import WorkflowResult


class VerifierAgent:
    """Performs lightweight workflow-level verification."""

    def verify(self, result: WorkflowResult) -> list[str]:
        checks: list[str] = []
        if result.report_path and result.report_path.exists():
            checks.append(f"PASS report-created {result.report_path}")
        else:
            checks.append("FAIL report-created")

        if len(result.tasks) <= len(result.findings) or not result.findings:
            checks.append("PASS task-count-sane")
        else:
            checks.append("FAIL task-count-sane")

        if all(path.exists() for path in result.changed_files):
            checks.append("PASS changed-files-exist")
        else:
            checks.append("FAIL changed-files-exist")
        return checks

    @staticmethod
    def has_failures(checks: list[str]) -> bool:
        return any(check.startswith("FAIL") for check in checks)
