"""Planner agent: transforms findings into prioritized refactoring tasks."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .models import Finding, RefactorTask

SEVERITY_WEIGHT = {"high": 100, "medium": 50, "low": 10}


class PlannerAgent:
    """Groups findings by rule and emits a clear execution plan."""

    def plan(self, findings: list[Finding]) -> list[RefactorTask]:
        grouped: dict[str, list[Finding]] = defaultdict(list)
        for finding in findings:
            grouped[finding.rule].append(finding)

        tasks: list[RefactorTask] = []
        for rule, items in grouped.items():
            priority = sum(SEVERITY_WEIGHT.get(item.severity, 1) for item in items)
            files = tuple(sorted({item.path for item in items}))
            tasks.append(
                RefactorTask(
                    title=self._title_for(rule),
                    rationale=f"命中 {len(items)} 个 `{rule}` 问题，涉及 {len(files)} 个文件。",
                    files=files,
                    priority=priority,
                    checklist=self._checklist_for(rule),
                )
            )
        return sorted(tasks, key=lambda task: task.priority, reverse=True)

    def _title_for(self, rule: str) -> str:
        return {
            "syntax-error": "先修复阻塞自动化分析的语法错误",
            "large-function": "拆分过长函数，降低单点维护风险",
            "too-many-args": "收敛过长参数列表，提升接口可读性",
            "debt-marker": "关闭 TODO/FIXME 技术债标记",
            "long-line": "整理过长代码行，改善评审体验",
        }.get(rule, f"处理 {rule} 问题")

    def _checklist_for(self, rule: str) -> tuple[str, ...]:
        common = "补充或更新回归测试，确保行为不变。"
        table = {
            "syntax-error": ("运行解释器或 linter 定位失败位置。", "修复语法后重新执行扫描。", common),
            "large-function": ("识别函数内部的阶段性逻辑。", "提取具名私有函数并保留原入口。", common),
            "too-many-args": ("找出强相关参数。", "封装为配置对象或 dataclass。", common),
            "debt-marker": ("确认 TODO/FIXME 是否仍有效。", "为有效技术债创建可追踪任务。", common),
            "long-line": ("拆分长字符串或复杂表达式。", "避免为了换行改变运行逻辑。", common),
        }
        return table.get(rule, ("定位根因。", "提交最小可验证修改。", common))
