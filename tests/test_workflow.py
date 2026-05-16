from pathlib import Path

from repo_refactor_agent.analyzer import AnalyzerAgent
from repo_refactor_agent.planner import PlannerAgent
from repo_refactor_agent.workflow import run_workflow


def test_analyzer_detects_todo_and_long_function(tmp_path: Path) -> None:
    sample = tmp_path / "sample.py"
    body = "\n".join(f"    value += {index}" for index in range(42))
    sample.write_text(f"def noisy(value):\n{body}\n    return value  # TODO: split this\n", encoding="utf-8")

    findings = AnalyzerAgent().analyze([sample])

    assert {finding.rule for finding in findings} >= {"debt-marker", "large-function"}


def test_planner_prioritizes_high_severity(tmp_path: Path) -> None:
    broken = tmp_path / "broken.py"
    broken.write_text("def bad(:\n", encoding="utf-8")

    findings = AnalyzerAgent().analyze([broken])
    tasks = PlannerAgent().plan(findings)

    assert tasks[0].title.startswith("先修复")
    assert tasks[0].priority >= 100


def test_workflow_writes_report_and_verifies(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("# FIXME: add auth guard\nprint('demo')\n", encoding="utf-8")

    result = run_workflow(tmp_path)

    assert result.report_path is not None
    assert result.report_path.exists()
    assert "Repo Refactor Agent Report" in result.report_path.read_text(encoding="utf-8")
    assert all(check.startswith("PASS") for check in result.verification)
