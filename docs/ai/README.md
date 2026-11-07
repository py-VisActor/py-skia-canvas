# 兼容入口与 agent 资料

中文 | [English](README.en.md)

本目录保留旧链接与机器资料。新用户请从[用户文档](../README.md)或[用户指南](../user/README.md)开始；修改库请从[维护者与 agent 目录](../development/README.md)开始。

## 安装快捷方式

适用 CPython 3.13、Windows AMD64 或 Linux glibc 2.28+ x86_64：

```shell
python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a20
```

## 路径与职责

- [INSTALL](INSTALL.md)、[使用参考](usage/README.md)、[API](usage/API_REFERENCE.md)、[图册](usage/DEMOS.md)和[排错](usage/TROUBLESHOOTING.md)仍是有效且持续维护的用户资料。保留路径以维持引用及图像来源，不复制到新目录形成双源。
- [development](development/README.md)是库维护者和 agent 的详细研发规则，应用用户不需要执行。
- [facts.json](facts.json)和 [llms.txt](../../llms.txt)提供机器导航；[VALIDATION](VALIDATION.md)和 assets 来源清单保存既有证据，不代表本次重新渲染或重新发行。

本目录名 `ai` 不表示所有页面只供 AI 使用。后续新增用户指南放入 `docs/user`，新增维护者导航放入 `docs/development`；旧详细参考继续在其唯一位置维护。
