# Repo Refactor Agent

Repo Refactor Agent is a small, runnable demo of an AI/Agent-style codebase refactoring assistant. It is intentionally lightweight: no paid API key is required, but the workflow is structured like a production coding agent so it can be extended with LLM calls later.

## Pain Point

Engineering teams often accumulate technical debt that is easy to ignore during daily development: stale TODO/FIXME markers, oversized functions, too many parameters, syntax errors that block tooling, and long lines that slow down review. Repo Refactor Agent turns those scattered signals into a prioritized Markdown plan that can be attached to a PR or used as evidence for an Agent workflow.

## Agent Workflow

1. **Scanner Agent** enumerates source-like files and skips dependency/build directories.
2. **Analyzer Agent** applies deterministic rules plus Python AST analysis.
3. **Planner Agent** groups findings into prioritized refactoring tasks.
4. **Reporter Agent** writes a Markdown report with findings and checklists.
5. **Verifier Agent** checks report generation and workflow invariants.

## Quick Start

```bash
PYTHONPATH=src python -m repo_refactor_agent . --output proof/refactor_plan.md
```

Or after installation:

```bash
repo-refactor-agent . --output proof/refactor_plan.md
```

## Example Output

```text
Repo Refactor Agent scanned: /path/to/repo
Findings: 3
Tasks: 2
Report: /path/to/repo/proof/refactor_plan.md
Verification:
- PASS report-created /path/to/repo/proof/refactor_plan.md
- PASS task-count-sane
- PASS changed-files-exist
```

## Xiaomi CodePlan Application Text

A ready-to-edit Chinese application answer is available in [`docs/xiaomi_codeplan_answer.md`](docs/xiaomi_codeplan_answer.md).
