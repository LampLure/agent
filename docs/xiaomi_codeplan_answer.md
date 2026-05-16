# 小米 CodePlan 申请材料示例

## 04 请描述你使用 Agent 或 AI 驱动构建的具体成果

我构建了一个轻量级的自动化代码库重构 Agent：Repo Refactor Agent。它解决的核心痛点是中小团队在代码评审前很难持续、低成本地发现技术债，例如 TODO/FIXME 长期遗留、函数过长、参数过多、语法错误阻塞自动化分析、长行影响 Review 等问题。过去这些问题通常依赖资深工程师人工巡检，效率低且标准不稳定。

核心逻辑流采用多 Agent 协作方式：Scanner Agent 首先遍历仓库并排除依赖目录；Analyzer Agent 对源码执行规则扫描和 Python AST 分析；Planner Agent 将发现的问题按严重程度聚合成可执行的重构任务；Reporter Agent 自动生成 Markdown 重构报告；Verifier Agent 最后检查报告产物和任务数量等工作流不变量。这个流程具备长链推理雏形：从代码事实提取、风险归因、优先级排序到可执行 checklist 输出，形成“扫描—分析—规划—报告—验证”的闭环。

当前项目可以作为申请材料中的可运行证明：用户只需在任意仓库执行 `repo-refactor-agent .`，即可生成 `refactor_plan.md`，用于 PR 附件、团队周报或技术债治理看板。后续可接入真实 LLM API，把规则扫描结果交给模型生成更细粒度的重构补丁，并自动运行测试形成完整 PR。

## 05 使用证明与影响力证明

可提交内容建议：

1. 终端运行日志截图：执行 `PYTHONPATH=src python -m repo_refactor_agent . --output proof/refactor_plan.md` 的输出。
2. Agent 工作流截图：`proof/refactor_plan.md` 中的 Findings、Prioritized Refactor Tasks 和 Core Agent Flow。
3. GitHub 项目链接：填写该仓库地址；如果部署在线 Demo，可填写 README 中的演示地址。
