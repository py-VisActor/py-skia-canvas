# 文档、示例与发布说明交付规范

中文 | [English](DOCUMENTATION.en.md)

文档是功能交付的一部分。AI 实现新行为、修复错误、变更参数/异常、构建/平台或研发工具时，必须先判断文档影响，完成相关更新，再进行最终检查。[完整流程](AUTONOMOUS_WORKFLOW.md)与 [workflow.json](workflow.json)规定执行及记录格式。

受众分层：根 README 和 PyPI 介绍面向库用户，只保留安装、最小例子、能力/限制及用户文档链接；正式用户目录为 [docs/README](../../README.md) 和 [docs/user](../../user/README.md)。维护者与 agent 从 [docs/development](../../development/README.md)进入。`docs/ai/usage` 与 INSTALL 仍是有效单一参考，保留旧路径以兼容链接/图像来源；不复制整套形成双源。会话、计划、验收与本机报告放在开发/证据入口，原历史证据不改写。

## 1. 按影响更新资料

| 主题 | 触发条件 | 需审阅的资料 |
| --- | --- | --- |
| entry | 安装方式、能力/限制、入口或版本状态 | 根 README 双语、AI README 双语、llms.txt、facts.json |
| installation | ABI/平台/依赖/索引/部署变化 | INSTALL 双语、公开安装命令、支持矩阵 |
| api | 导出、签名、默认值、单位、返回、异常/所有权变化 | API_REFERENCE 双语、源码契约、相关 API ledger/status |
| usage | 调用方式、行为、错误处理、线程/async 变化 | usage README、TROUBLESHOOTING 双语 |
| demos | 新可见能力、图像/文本/导出/窗口变化 | 可运行例子、DEMOS/示例 README 双语、相关输出图和 manifest |
| development | 工具、依赖、构建、验证、恢复或 CI 变化 | 开发指南、WORKFLOW、验收说明和本流程双语 |
| release | 候选/验收/索引状态、版本、包元数据变化 | RELEASE_STATUS、facts、wheel 描述、发行证据 |

主题的真实路径见机器规则。每项选择 `updated` 或 `unchanged`，并给出具体理由与审阅路径。`updated` 必须有对应 Git 差异，成对文档须同时包含中文和英文；`unchanged` 应解释为何实际行为、签名与使用方式均不需要修改。不能仅填“已检查”“无影响”。

代码符合既有文档的纯修复可以保留文档正文，仍应记录审阅结论；新增公开扩展必须更新 API/使用文档。缺少影响分析不构成“无需更新”。

## 2. 方法级契约

每个新增/迁移入口都应写清：

- 功能与有效输入，包括省略参数、undefined/null 和重载。
- 参数单位、默认值、数值/字符串边界及读取/转换顺序。
- 返回值/类型、同步/awaitable 与调用时快照语义。
- 异常条件、忽略无效值/STRICT 行为和失败副作用。
- 创建线程、所有权、父子生命周期与可跨线程的数据。
- 固定上游位置、共享 core 调用与相关场景/断言。

文档名与实现名沿用同一公共 API；不把 browser Canvas 或其他 Python 库的默认行为复制过来。错误修复描述应给出触发输入和前后结果。

## 3. 双语、例子与图片

中文保留原路径，英文为 `.en.md`，每页互链。示例代码、CLI 参数和图片引用相同，说明文字分别完整描述限制；机器规则和 JSON 事实共用一份。历史报告不为翻译改写事实。

先在实际候选/已安装 wheel 上执行新的或受影响的 demo，检查尺寸、像素/指标与实际 backend，再复制原始 PNG 到固定 assets 路径。保留版本、wheel SHA、脚本 SHA、输出 SHA 和原始 run；更新 manifest 与两种图册的说明/alt 文本。仅文档措辞变更不重渲染图片；未受影响的既有图像保留其原来源，不伪装成新候选输出。

`validate_ai_docs.py` 检查本地链接、语言路由、章节结构、Python AST/命令一致性、公开导出、版本事实和图片来源。语法/链接通过不证明翻译语义、图片审阅或用户说明正确；AI 仍需按实际行为阅读。

## 4. 源码候选、公开版本与图片基线

| 字段/资料 | 表示什么 | 何时更新 |
| --- | --- | --- |
| pyproject / Python / crate / lock | 当前源码候选 | 实现或准备新发行版时协调变更 |
| `facts.sourceVersion` | 与源码一致的候选版本 | 与 pyproject/Python 同步 |
| `facts.version`、`installation.version` | 公开文档与安装命令的发行版本 | 明确切换公开文档基线时一起更新 |
| `installation.publishedToPyPI` / release records | 实际索引状态 | 查询并验证实际发布后更新，不能从 CI 推断 |
| `acceptedWheels.version`、assets manifest | 图像对应的已验收实现基线 | 取得新输出与 provenance 后更新 |

例如已发布为 `0.1.0a18`、源码候选为 `0.1.0a19` 时，安装页可以继续安装 a18，sourceVersion 为 a19；新增候选 API 必须标明适用版本/未发行状态，不能让旧 wheel 用户复制不可用入口。不得仅为消除校验错误，提前把候选写成已发布或给旧图换版本标签。

## 5. 上传前检查实际 wheel 描述

打包描述由 `pyproject.toml` 的 `readme` 指向 `docs/PYPI_DESCRIPTION.md`；该文件采用独立的英文发行说明和绝对链接。根 README 双语继续承担仓库导航与当前安装状态。文档校验同时检查实际打包描述的代码和链接，不能只审阅根 README。

PyPI 的项目说明取自上传时的 METADATA，不随 GitHub README 自动变化。新发布采用中性的安装/能力说明；动态“尚未发布”之类措辞会永久过时，发行过程状态放到 RELEASE_STATUS。PyPI 中的文档/图片链接要可独立访问，不能依赖仓库相对路径；提供绝对 Documentation project URL。

在正确源码中完成描述、链接和版本修正后构建；替换命令中的占位文件与版本，再检查实际候选：

```shell
python scripts/check_package_metadata.py dist/NEW_CANDIDATE.whl --version NEW_VERSION --out test-runs/NEW_METADATA/report.json
```

该工具只读 wheel，检查包名、版本、Python 范围、安装命令、过时发布措辞和链接。它不会修改已验收 wheel，也不代替 native/安装验收。旧 a18 发行物可能因其历史 README 不满足新增质量门槛；记录限制，保留原 wheel，不能改字节后冒充同一验收物。

描述检查通过后，用同一 wheel 完成实际验收，再冻结/发布。上传后分别检查索引返回的版本、描述和文件 SHA。若内容错误，准备新版本；不删除重传旧文件、不上传占位包。

## 6. 完成交付前的文档核对

1. 用户只读入口页即可找到适用版本、正式索引安装命令和 ABI/平台条件。
2. API 的签名、单位、默认值、错误和线程限制与实际实现一致。
3. 新/改变的流程有可运行示例和真实输出，图片/代码没有伪造或过期标签。
4. 中文和英文同时表达所有限制，代码与命令保持一致。
5. 公开安装版本、源码候选、图片基线与索引状态分别准确。
6. 相关文档在任务记录中已处理；最终文档检查在最后一次编辑之后执行。
7. 如授权同步，确认 GitHub 实际可读；如授权发布，确认 PyPI 实际内容。旧搜索缓存不视为新文档已传播。

按任务记录附加真实证据并做本地校验，流程见 [AUTONOMOUS_WORKFLOW](AUTONOMOUS_WORKFLOW.md)。
