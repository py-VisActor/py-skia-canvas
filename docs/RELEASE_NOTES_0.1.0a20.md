# 0.1.0a20 发行说明

中文 | [English](RELEASE_NOTES_0.1.0a20.en.md)

本次为文档和包元数据修订，不改变 Canvas 绘图、字体、编码、默认后端或运行时依赖。实际发布和平台验证状态见[发行记录](RELEASE_STATUS.md)。

- 中英文 README 和 PyPI 介绍聚焦安装、最小示例与使用限制。
- [用户文档](README.md)、[用户指南](user/README.md)与[维护者目录](development/README.md)分开；既有 `docs/ai` API 参考继续维护，旧链接仍有效。
- 项目链接使用当前 `py-VisActor/py-skia-canvas` 仓库；Documentation 指向用户文档目录。
- AGENTS 规范按职责、开始工作、仓库地图、命令、修改约束及验证六节组织。

版本仍为 alpha。支持 CPython 3.13、Windows AMD64 和 Linux glibc 2.28+ x86_64；其他 ABI/平台未列入发行范围。字体、线程所有权、窗口 GPU 要求与 Windows 并行矢量文件序列限制保持不变，详见[用户指南](user/README.md)。
