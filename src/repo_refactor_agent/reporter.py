"""Report generation for the workflow."""

from __future__ import annotations

from pathlib import Path

from .models import Finding, RefactorTask


class ReporterAgent:
    """Writes a Markdown report that can be attached to PRs or applications."""

    def write(self, root: Path, findings: list[Finding], tasks: list[RefactorTask], output: Path) -> Path:
        output.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Repo Refactor Agent Report",
            "",
            "## Executive Summary",
            f"- Scanned repository: `{root}`",
            f"- Findings: **{len(findings)}**",
            f"- Prioritized tasks: **{len(tasks)}**",
            "",
            "## Core Agent Flow",
            "1. **Scanner Agent** enumerates source-like files and excludes dependencies/build output.",
            "2. **Analyzer Agent** applies deterministic rules and Python AST checks.",
            "3. **Planner Agent** groups findings into prioritized refactoring tasks.",
            "4. **Reporter Agent** writes a reviewable report for PR or workflow evidence.",
            "5. **Verifier Agent** checks report completeness and workflow invariants.",
            "",
            "## Findings",
            "| File | Line | Severity | Rule | Message | Suggestion |",
            "| --- | ---: | --- | --- | --- | --- |",
        ]
        if findings:
            lines.extend(finding.as_markdown(root) for finding in findings)
        else:
            lines.append("| - | - | info | clean | 未发现当前规则覆盖的问题。 | 保持测试和评审流程。 |")

        lines.extend(["", "## Prioritized Refactor Tasks"])
        if tasks:
            for index, task in enumerate(tasks, start=1):
                relative_files = ", ".join(f"`{path.relative_to(root) if path.is_relative_to(root) else path}`" for path in task.files)
                lines.extend(
                    [
                        f"### {index}. {task.title}",
                        f"- Priority score: {task.priority}",
                        f"- Rationale: {task.rationale}",
                        f"- Files: {relative_files}",
                        "- Checklist:",
                    ]
                )
                lines.extend(f"  - [ ] {item}" for item in task.checklist)
                lines.append("")
        else:
            lines.append("当前没有需要排期的重构任务。")

        output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        return output
