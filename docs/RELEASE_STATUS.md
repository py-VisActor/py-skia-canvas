# 发布状态

## 0.1.0a19 已发布（2026-11-02）

**0.1.0a19 已发布到正式 PyPI、TestPyPI 和 GitHub Release。** 首轮支持 CPython 3.13、Windows AMD64、Linux glibc 2.28+ x86_64。三个来源均独立下载核 SHA，并在仓库外、空 PATH、`-I`、无 pip 缓存的新环境安装复验。

```shell
python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a19
```

本版包含已审阅的研发流程/CI/双语文档、负面证据状态拒绝修复、包描述变化后的证据失效检查、独立的中性 PyPI 说明与绝对文档链接，以及 py-mermaid 生态入口。Canvas 的绘图、字体、布局、混色、编码与默认 GPU/CPU 算法未改变；版本升级使用新构建 wheel，未改写或重传 a18。

| 文件 | SHA256 |
| --- | --- |
| `py_skia_canvas-0.1.0a19-cp313-cp313-win_amd64.whl` | `d77dbeeef61b5d41398105cce66a28f513d7c5dc06a1635de745d33e9688f99f` |
| `py_skia_canvas-0.1.0a19-cp313-cp313-manylinux_2_28_x86_64.whl` | `c21dfdb17d8dc50d0e4f490116f21b3b1d7c30e57acf975409197c05ec1d1089` |

发行源码为 `6de163ee10252f36c02be49cd85f43cff4381053`。已验收 archive SHA 为 `ceb21401b8d84d02e4b7d4937c81fd7b123f4610b1adb02feee7124c38e5337e`，manifest SHA 为 `4ffdff4018fe20a519f6708624376721091f0774997f983b16cb065338680b04`。

| 外部门禁 | 实际记录 |
| --- | --- |
| 源码 CI | [41416692180](https://github.com/xuanhun/py-skia-canvas/actions/runs/41416692180)：74 bootstrap、35 workflow、6 API ledger 检查通过 |
| GitHub Release | [v0.1.0a19](https://github.com/xuanhun/py-skia-canvas/releases/tag/v0.1.0a19)：公开下载 SHA、双平台独立安装通过 |
| 同字节暂存 | [41417023911](https://github.com/xuanhun/py-skia-canvas/actions/runs/41417023911)：下载 archive 与 manifest 核 SHA；独立下载 Actions artifact 再次核验通过 |
| TestPyPI | [0.1.0a19](https://test.pypi.org/project/py-skia-canvas/0.1.0a19/)；[41417174000](https://github.com/xuanhun/py-skia-canvas/actions/runs/41417174000) 上传成功，双平台独立安装通过 |
| PyPI | [0.1.0a19](https://pypi.org/project/py-skia-canvas/0.1.0a19/)；[41417637089](https://github.com/xuanhun/py-skia-canvas/actions/runs/41417637089) 上传成功，双平台独立安装通过 |

本地新 wheel 在每个平台的 GPU、CPU 上各通过 203 普通 + 203 STRICT 精确对照，每后端 12 组实际字体/glyph/surface 观测、118 GPU / 23 CPU 生命周期测试。Linux 另通过无网络/Node/GPU/Vulkan loader 容器的六格式探针与 23 CPU 测试，以及原生 Vulkan surface/queue-submit 观测。每个公开来源安装后，各平台独立通过 203 普通 + 203 STRICT GPU 对照、12 组实际 GPU 字形/表面观测及 23 CPU 生命周期测试。

以上为本版相关子集复验，不累计为全 API 新覆盖。原 Windows 默认并行 PDF/SVG 文件序列非确定性、窗口 GPU 要求、其他 ABI/平台未验收等限制保留。既有图册保留 a18 的原始 PNG 和 provenance，没有重标版本。

实际 PyPI/TestPyPI 描述包含 a19 安装命令、绝对文档链接和 Documentation URL；a18 的旧描述保留其历史字节。审查与实际证据见 [任务记录](changes/20261102-review-release-a19.json)，本地原始记录为 `20261102-a19-acceptance-review-01`、`20261102-a19-installed-github-01`、`20261102-a19-installed-testpypi-02`、`20261102-a19-installed-pypi-01`。工具探针的早期失败及修复前结果完整保留。

## 0.1.0a18 历史发布记录

2026-10-29，**py-skia-canvas 0.1.0a18 已发布到正式 PyPI**。GitHub Release、TestPyPI、PyPI 的下载和 Windows/Linux 独立安装门禁均已完成，发布的两个 wheel 与本地 GPU/CPU 验收字节精确相同。

> 安装说明勘误（2026-10-29）：直接读取正式 PyPI JSON API 后确认，`0.1.0a18` 的项目说明仍保存首次上传时的旧 README，含“尚未发布到 PyPI”和仅本地 wheel 安装的过时表述。两个 wheel 实际已发布且 SHA 未变。当前安装入口为 [中文](ai/INSTALL.md) / [English](ai/INSTALL.en.md) / [llms.txt](../llms.txt)。GitHub 文档更新不会修改该版本的 PyPI 说明；PyPI 保留首次上传的版本元数据，详见[官方 JSON API 规则](https://warehouse.pypa.io/api-reference/json/)。后续新发行物须携带修正后的 README；本次文档修正不替换已验收 wheel。

## 安装与支持范围

```shell
python -m pip install --only-binary=:all: py-skia-canvas==0.1.0a18
```

支持 CPython 3.13、Windows AMD64、Linux glibc 2.28+ x86_64。macOS、其他 ABI/架构未验收。Python 运行不需要 Node/npm、Neon/N-API、skia-python 或源码工作区。首发只向两个包索引上传已验收 wheel，未发布 sdist。

## 发行物与来源

| 文件 | SHA256 |
| --- | --- |
| `py_skia_canvas-0.1.0a18-cp313-cp313-win_amd64.whl` | `9efce11f1340a9bfbb69387f0757abe1635b3ff45528ce07e69dc30771049b74` |
| `py_skia_canvas-0.1.0a18-cp313-cp313-manylinux_2_28_x86_64.whl` | `2e641429ceedaca260037abba217e13189a16a1168571fa430857e06b2734071` |

发行源码提交为 `8b5611dc7911d9ebc470c949a396807515690aac`；后续 main 提交记录状态与安装文档。未重编或替换已验收的 native/wheel。来源映射见 Release 资产 `publication-provenance-0.1.0a18-ci2.json`。

原 GPU 证据包 `reviewed-wheels.zip` SHA 为 `4884291b61d3143db7a681067abd223101b864b5baf1aa457a0a8e9b6136827c`，manifest SHA 为 `1489613964763c29de7884353744ceeb754e3853eb8ec8684815116af0491e29`。独立 CPU 包 `cpu-validation-0.1.0a18.zip` SHA 为 `7ba80b8a642747de9a6f7b3800ba3b1b47fbf4865ff7b839d6e8b80e226a010d`。

## 各自通过的外部门禁

| 门禁 | 实际记录 |
| --- | --- |
| 源码 CI | [40708692406](https://github.com/xuanhun/py-skia-canvas/actions/runs/40708692406)：74 项 bootstrap、源码/许可/API 检查通过 |
| GitHub Release | [v0.1.0a18](https://github.com/xuanhun/py-skia-canvas/releases/tag/v0.1.0a18)：发行文件由公开 URL 重新下载，SHA 精确一致；两端独立安装回验通过 |
| 同字节暂存 | [40709164905](https://github.com/xuanhun/py-skia-canvas/actions/runs/40709164905)：独立下载 Actions artifact 后再次核对 wheel 和 manifest |
| TestPyPI | [0.1.0a18](https://test.pypi.org/project/py-skia-canvas/0.1.0a18/)；[发布第二次运行](https://github.com/xuanhun/py-skia-canvas/actions/runs/40709439674/attempts/2) 成功，独立安装回验通过 |
| PyPI | [0.1.0a18](https://pypi.org/project/py-skia-canvas/0.1.0a18/)；[发布第三次运行](https://github.com/xuanhun/py-skia-canvas/actions/runs/40792287866/attempts/3) 成功，独立安装回验通过 |

三个发行来源各自使用禁用 pip 缓存、仓库外全新环境、Python `-I` 和空 PATH。每个平台、每个来源均精确通过 203 普通与 203 STRICT 差分用例、12 组实际 GPU 字形/表面观测、118 项 GPU 生命周期和 23 项 CPU 测试；安装后的 native SHA 也与本地验收相同。这些是发行安装后的独立子集复核，不累计为迁移覆盖的新用例，也不替代原完整 [迁移验收](COMPLETION_REPORT.md) 和 [纯 CPU 验收](CPU_RENDER_REPORT.md)。

主记录分别为 `20261028-github-installed-5`、`20261029-testpypi-installed-1`、`20261029-pypi-installed-1`；独立复核分别为 `20261028-github-installed-review-2`、`20261029-testpypi-installed-review-1`、`20261029-pypi-installed-review-1`。Release 附带各来源安装验收摘要及 `pypi-release-verification-0.1.0a18.zip`。

## 继承限制与部署边界

- Windows 默认并发 PDF/SVG 文件序列保留用户已接受的原版非确定性限制；`RAYON_NUM_THREADS=1` 为已验证的规避方式，库默认线程数未改。
- 无 GPU 时离屏绘制与导出自动回退 CPU；App/Window 屏幕呈现保留原版 GPU 要求。
- Windows 未启用长路径支持时，过深的虚拟环境会令许可文件触及 `MAX_PATH`；短路径环境已验证。未改系统注册表或 wheel 许可负载。
- 系统字体不捆绑。发行复验发现 Windows 14 个系统字体文件与早期清单不同；Node A 和 Python 使用新的同一资源清单精确比较，旧证据完整保留。Linux 字体指纹未变。

早期失败和修复记录全部保留：首次 CI 的路径排序/开发解析器安装问题、TestPyPI/PyPI 的 `invalid-publisher`、Windows 深路径安装失败，均未静默跳过。两个索引的 Trusted Publisher 现已分别生效；三个 GitHub 发布 environment 均仅允许 main。普通 CI 通过、实际 GPU 验收和发行物安装验收继续分开记录。
