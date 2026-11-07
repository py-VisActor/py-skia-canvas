# 维护者与 agent 文档

中文 | [English](README.en.md)

本目录面向修改 py-skia-canvas 本身的维护者与 AI agent。使用库开发应用请读[用户文档](../README.md)，无需执行以下内部流程。

## 规则与工作流程

- [AGENTS.md](../../AGENTS.md)：稳定规则、授权与工作边界。
- [开发指南及完整约束](../ai/development/README.md)：架构、唯一 core、来源和线程边界。
- [完整研发流程](../ai/development/AUTONOMOUS_WORKFLOW.md) · [命令流程](../ai/development/WORKFLOW.md) · [机器规则](../ai/development/workflow.json)。
- [文档规范](../ai/development/DOCUMENTATION.md)：双语、示例、受众分层与包描述。
- [测试与发行](../ai/development/TESTING_AND_RELEASE.md) · [发行流程](../RELEASE_WORKFLOW.md) · [测试工具](../../tests/README.md)。
- [API 兼容规则](../API_COMPATIBILITY.md) · [Python 宿主对应](../PYTHON_HOST_PROFILE.md)。

## 状态、来源与历史

[发行记录](../RELEASE_STATUS.md)记录公开发行事实；[来源目录](../../references/README.md)记录固定上游和许可。[实施方案](../IMPLEMENTATION_PLAN.md)、[任务清单](../TASKS.md)、[会话交接](../NEW_SESSION.md)和[迁移报告](../COMPLETION_REPORT.md)保留开发历史，阅读时核对其日期和适用版本。

原 `docs/ai/development` 继续作为详细开发规则的单一维护源；本目录是正式维护者导航，不复制整套规范。原 `docs/ai/usage` 和 `INSTALL` 仍是有效用户参考，并非历史弃用页。原始验证报告、图片和来源 SHA 保持不变。

## 文档分类索引

[逐文件受众清单](documentation-inventory.json)区分用户、开发、历史、证据与许可资料。旧路径保留来源上下文；清单不把旧验收提升为当前功能结论。
