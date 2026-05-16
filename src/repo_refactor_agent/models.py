"""Shared data models for the refactoring workflow."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    """A single code-quality issue discovered by the analyzer."""

    path: Path
    line: int
    severity: str
    rule: str
    message: str
    suggestion: str

    def as_markdown(self, root: Path) -> str:
        relative = self.path.relative_to(root) if self.path.is_relative_to(root) else self.path
        return (
            f"| `{relative}` | {self.line} | {self.severity} | {self.rule} | "
            f"{self.message} | {self.suggestion} |"
        )


@dataclass(frozen=True)
class RefactorTask:
    """A task generated from one or more findings."""

    title: str
    rationale: str
    files: tuple[Path, ...]
    priority: int
    checklist: tuple[str, ...]


@dataclass
class WorkflowResult:
    """Result returned by the agent workflow."""

    root: Path
    findings: list[Finding] = field(default_factory=list)
    tasks: list[RefactorTask] = field(default_factory=list)
    report_path: Path | None = None
    changed_files: list[Path] = field(default_factory=list)
    verification: list[str] = field(default_factory=list)
