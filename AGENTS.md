# py-skia-canvas：agent 工作规范

## 1. 适用范围与职责

本文件适用于本仓库所有修改；子目录如有更具体规则，按实际范围读取。
项目负责通用 Canvas Python 接口和唯一 Rust/Skia 核心，不承接业务图表模型。
应用用户从[用户文档](docs/README.md)开始；维护者从[开发目录](docs/development/README.md)开始。
完整技术约束保留在[开发指南](docs/ai/development/README.md#8-不可改变的开发约束)。

## 2. 开始工作

先运行 `git status --short`，识别并保留已有修改，避免覆盖他人工作。
按当前用户请求确定范围、授权、验收条件与任务类型，不自动恢复旧会话目标。
动态版本、发行状态从 [pyproject.toml](pyproject.toml) 和[发行记录](docs/RELEASE_STATUS.md)读取。
旧计划、交接和历史用户授权只作背景，不替代当前任务和实际证据。

按任务选择必读资料：

- 文档：本文件、[文档规范](docs/ai/development/DOCUMENTATION.md)及相关用户页面。
- 实现/兼容：[API 规则](docs/API_COMPATIBILITY.md)、[开发指南](docs/ai/development/README.md)、相关源码与固定上游。
- 构建/发行：[测试与发行](docs/ai/development/TESTING_AND_RELEASE.md)和[发行流程](docs/RELEASE_WORKFLOW.md)。
- 迁移历史：需要时查[实施方案](docs/IMPLEMENTATION_PLAN.md)、[任务清单](docs/TASKS.md)、[会话历史](docs/NEW_SESSION.md)，核对日期和版本。

## 3. 仓库地图

| 路径 | 职责 |
| --- | --- |
| `python/py_skia_canvas` | Python 公共 API、类型转换、异步与宿主接口 |
| `crates/python` | PyO3 绑定及 owner/lifetime 边界 |
| `crates/canvas-core` | 唯一绘图核心；开发用 `crates/node` 也消费此核心 |
| `crates/skia-bindings` | 固定 Skia 构建；来源映射见 `crates/source-map.json` |
| `references/upstream` | 只读上游来源；不作为运行时 fallback |
| `tests` / `scripts` | 独立断言、官方差分、构建和验收工具 |
| `docs/user` / `docs/development` | 用户入口 / 维护者与 agent 入口 |
| `docs/ai` | 兼容路径、详细单一参考与机器事实，不全是历史资料 |
| `docs/changes` / `test-runs` | 变更记录 / 不覆盖的真实执行证据 |

## 4. 常用命令

先检查现有环境；开发依赖见 [requirements-test.txt](requirements-test.txt)，构建工具链见[命令流程](docs/ai/development/WORKFLOW.md)。
本文件不要求每个任务安装依赖或重编 Skia。

```shell
git status --short
python scripts/validate_ai_docs.py
python -m unittest discover -s tests/bootstrap -v
python scripts/validate_bootstrap.py
python scripts/validate_core.py
python scripts/validate_licenses.py
```

纯文档任务只执行相关文档、链接和代码段语法检查；无需重复渲染。
实现任务按影响执行专项断言及实际新候选验证；上列源码检查不证明绘图已通过。
全量 GPU/CPU/STRICT、字体、线程、窗口和导出命令见[测试目录](tests/README.md)，不靠一个通用命令宣称完整验收。

## 5. 修改约束

- 兼容目标固定官方 `skia-canvas@3.0.8`；保留公共命名、默认 GPU 策略和 Python 宿主对应。
- 复用唯一 core，不另写字体、shaping、布局、绘图或混色实现，不加样例/像素补偿。
- 生产 wheel 不依赖 Node、Neon/N-API、skia-python、其他工作区或 `.local`。
- 原生对象遵守创建线程与生命周期约束；不搬 GPU context 到线程池，不添加未经证明的 Send/Sync。
- 只读来源不能直接改写；提取、改名和兼容变更保留来源映射、参数/错误/所有权说明。
- 保留 [MIT 许可](LICENSE)及[第三方说明](THIRD_PARTY_NOTICES.md)；不引入来源或许可不明的字体/资源。
- 用户资料与内部开发资料分开，同批审阅中英文；原始历史报告和图片来源不改写。

## 6. 验证与完成条件

代码、构建、测试、工具变化遵循[完整研发流程](docs/ai/development/AUTONOMOUS_WORKFLOW.md)，记录影响范围和相关文档处理。
先保存修改前证据，再用实际新候选验证；数值与 RGBA 精确差分，不隐藏失败。
新日志与产物写入独立 `test-runs/<new-id>/`，保留真实命令、错误、版本、后端和 SHA。
区分机械检查、功能验证、视觉审阅、发行验收与真实发布；CPU 回退不替代 GPU 验收。
缺字体、GPU、桌面或平台时明确未验证项，不静默跳过后称通过。
完成前检查差异、用户已有修改和相关双语链接；交接实际检查、证据与限制。
commit、push、发布及账户动作依据当前用户授权；记录文件不自行授予外部操作权限。
发布只用已验收的同一工件字节，并分别核实 CI、Release 和包索引状态。
