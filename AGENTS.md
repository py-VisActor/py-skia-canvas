# py-skia-canvas：AI 工作入口

进入本仓库后，按本文件定位任务、读取规则并执行。通用文档入口：[中文](docs/ai/README.md) / [English](docs/ai/README.en.md)；机器事实：[facts.json](docs/ai/facts.json)。本项目是通用 Canvas 库。

## 1. 开始工作

修改仓库前，先读以下资料：

1. [新会话状态](docs/NEW_SESSION.md)
2. [实施方案](docs/IMPLEMENTATION_PLAN.md)
3. [API 兼容规则](docs/API_COMPATIBILITY.md)
4. [任务清单](docs/TASKS.md)

随后检查 `git status --short`，识别并保留用户已有修改。当前发行状态以 [RELEASE_STATUS](docs/RELEASE_STATUS.md)及实际证据为准；早期计划、旧 docstring 和历史“未发布/待迁移”文字不能覆盖当前记录。

## 2. 按任务进入流程

| 当前任务 | 必读入口 |
| --- | --- |
| 使用已发布包开发应用 | [安装](docs/ai/INSTALL.md) → [使用指南](docs/ai/usage/README.md) → [API](docs/ai/usage/API_REFERENCE.md) |
| 新功能、修复、重构、测试、构建或工具修改 | [开发指南及完整约束](docs/ai/development/README.md) → [AI 研发流程](docs/ai/development/AUTONOMOUS_WORKFLOW.md) → [构建与差分命令](docs/ai/development/WORKFLOW.md) |
| 文档、示例或图像修改 | [文档交付规范](docs/ai/development/DOCUMENTATION.md) → [示例图册](docs/ai/usage/DEMOS.md) |
| wheel 验收或发布 | [测试与发布](docs/ai/development/TESTING_AND_RELEASE.md) → [发行流程](docs/RELEASE_WORKFLOW.md) |

**所有仓库修改都必须遵守[开发指南中的完整约束](docs/ai/development/README.md#8-不可改变的开发约束)。** 英文对应见 [Development guide](docs/ai/development/README.en.md#8-development-constraints)。

## 3. 执行顺序

1. 明确需求、验收标准、已有授权和资源，按语义影响选择任务 kind/areas。
2. 先保存修改前证据，再修改唯一实现并补充独立断言。生产变化用新候选 wheel 验证；日常对照固定官方 Node A，不要求每批重编 Node。
3. 按影响执行普通/STRICT、GPU/CPU、字体、导出、线程/生命周期及窗口检查。缺资源时明确保留未验收项，继续其他独立工作。
4. 同批更新相关中英文文档、可运行示例、实际图像及安装/发行说明；无需改动的主题给出具体审阅理由。
5. 代码、测试、构建或工具变化创建 `docs/changes/<task-id>.json`；通过统一检查、附加真实报告，再做本地证据校验。命令和规则见[完整流程](docs/ai/development/AUTONOMOUS_WORKFLOW.md)及 [workflow.json](docs/ai/development/workflow.json)。
6. 审阅差异和证据，按当前任务授权完成外部操作；交接已完成项、实际检查、文档、限制与下一步。

纯文档任务运行相关文档/链接/示例检查，无需重编 Skia 或重复无关渲染测试。

## 4. 判断是否完成

- 区分计划、实现、限定范围验证、发行验收和真实发布；CI 的记录检查不等于 GPU/CPU 或全 API 通过。
- 新证据使用新的 `test-runs/<run-id>/`；失败记录保留，源码或文档变化后不得冒用过期结果。
- 当前用户授权范围决定 commit/push、Release 和包索引操作；任务记录本身不授予权限，也不需要重复索取本次已获得的授权。
- 不清楚兼容边界或需要改变默认行为时，按开发约束取得用户决策；普通实现选择和可独立推进的工作继续完成。

自动化能力与真实环境依赖见[流程审查](docs/ai/development/WORKFLOW_AUDIT.md)。
