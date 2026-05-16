"""Command line entry point for Repo Refactor Agent."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .verifier import VerifierAgent
from .workflow import run_workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan a repository and generate a refactoring plan.")
    parser.add_argument("root", nargs="?", default=".", help="Repository path to scan.")
    parser.add_argument("--output", "-o", default=None, help="Markdown report path. Defaults to <root>/refactor_plan.md.")
    parser.add_argument("--fail-on-findings", action="store_true", help="Exit with status 2 when findings are detected.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_workflow(Path(args.root), Path(args.output) if args.output else None)

    print(f"Repo Refactor Agent scanned: {result.root}")
    print(f"Findings: {len(result.findings)}")
    print(f"Tasks: {len(result.tasks)}")
    print(f"Report: {result.report_path}")
    print("Verification:")
    for check in result.verification:
        print(f"- {check}")

    if VerifierAgent.has_failures(result.verification):
        return 1
    if args.fail_on_findings and result.findings:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
