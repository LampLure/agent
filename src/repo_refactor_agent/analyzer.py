"""Analyzer agent: converts source files into actionable findings."""

from __future__ import annotations

import ast
from pathlib import Path

from .models import Finding


class AnalyzerAgent:
    """Finds technical debt patterns with deterministic, explainable rules."""

    def analyze(self, files: list[Path]) -> list[Finding]:
        findings: list[Finding] = []
        for path in files:
            text = path.read_text(encoding="utf-8", errors="ignore")
            findings.extend(self._scan_text(path, text))
            if path.suffix == ".py":
                findings.extend(self._scan_python_ast(path, text))
        return sorted(findings, key=lambda item: (str(item.path), item.line, item.rule))

    def _scan_text(self, path: Path, text: str) -> list[Finding]:
        findings: list[Finding] = []
        for index, line in enumerate(text.splitlines(), start=1):
            normalized = line.lower()
            if "todo" in normalized or "fixme" in normalized:
                findings.append(
                    Finding(
                        path=path,
                        line=index,
                        severity="medium",
                        rule="debt-marker",
                        message="发现 TODO/FIXME 标记，说明存在未闭环的技术债。",
                        suggestion="把标记转成带负责人、验收标准和截止时间的任务。",
                    )
                )
            if len(line) > 100:
                findings.append(
                    Finding(
                        path=path,
                        line=index,
                        severity="low",
                        rule="long-line",
                        message="单行过长，影响 Code Review 与后续维护。",
                        suggestion="拆分表达式或提取具名变量。",
                    )
                )
        return findings

    def _scan_python_ast(self, path: Path, text: str) -> list[Finding]:
        try:
            tree = ast.parse(text)
        except SyntaxError as exc:
            return [
                Finding(
                    path=path,
                    line=exc.lineno or 1,
                    severity="high",
                    rule="syntax-error",
                    message="Python 文件无法被 AST 解析。",
                    suggestion="先修复语法错误，再执行自动重构。",
                )
            ]

        findings: list[Finding] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                body_length = (getattr(node, "end_lineno", node.lineno) or node.lineno) - node.lineno + 1
                if body_length > 40:
                    findings.append(
                        Finding(
                            path=path,
                            line=node.lineno,
                            severity="medium",
                            rule="large-function",
                            message=f"函数 `{node.name}` 长度为 {body_length} 行，可能承担过多职责。",
                            suggestion="按输入校验、业务计算、副作用输出拆分小函数。",
                        )
                    )
                arg_count = len(node.args.args) + len(node.args.kwonlyargs)
                if arg_count > 5:
                    findings.append(
                        Finding(
                            path=path,
                            line=node.lineno,
                            severity="medium",
                            rule="too-many-args",
                            message=f"函数 `{node.name}` 有 {arg_count} 个参数，调用方难以理解。",
                            suggestion="引入配置对象或 dataclass 聚合相关参数。",
                        )
                    )
        return findings
