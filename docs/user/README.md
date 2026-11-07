# 用户指南

中文 | [English](README.en.md)

安装名为 `py-skia-canvas`，Python 导入名为 `py_skia_canvas`。先按[根 README 的最小示例](../../README.md#最小示例)生成 PNG，再按以下任务查阅详细参考。

## 安装与运行环境

使用 CPython 3.13，以及 Windows AMD64 或 Linux glibc 2.28+ x86_64：

```shell
python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a19
python -c "import py_skia_canvas as c; print(c.__version__, c.__file__)"
```

使用 wheel 无需编译 Skia。虚拟环境、离线 wheel 和 Windows 路径限制见[安装说明](../ai/INSTALL.md)。

## 绘图与输出

Canvas 初始透明；需要底色时自行绘制。坐标原点在左上，`fillText` 的 y 为基线。先设置字体，再使用同一 font 和宽度测量/绘制。[使用参考](../ai/usage/README.md)覆盖路径、图像、字体、页面和异步示例；[API 参考](../ai/usage/API_REFERENCE.md)是公共名称和参数的查询入口。

| 任务 | API |
| --- | --- |
| 获取编码 bytes | `canvas.toBufferSync("png")` / `await canvas.toBuffer("png")` |
| 写文件 | `canvas.toFileSync(path)` / `await canvas.toFile(path)` |
| 加载编码图像 | `await loadImage(source)` |
| 选择 CPU | 绘制前设置 `canvas.gpu = False` |
| 查看实际后端 | `canvas.engine` |

导出可选 PNG、JPEG、WebP、raw、SVG、PDF；格式、density、质量和页码规则见[输出参考](../ai/usage/README.md)。`loadImageData` 接收 raw 像素，不能代替编码图像解码。

## 资源与部署限制

绘图对象和字体注册属于创建线程。每个 worker 应自行创建 Canvas、加载/注册资源并导出，返回 bytes；不要把已有 Context 交给另一个线程。字体由系统或应用显式提供，family 存在不保证包含所有字符。

离屏绘制无可用 GPU 时自动使用 CPU；App/Window 仍要求 GPU 和桌面。构造 options 的 `gpu=False` 不能替代 CPU setter。Windows 默认并行 PDF/SVG 文件序列保留上游字体子集限制，可在进程启动前显式设置 `RAYON_NUM_THREADS=1`；这不会改变库的默认并发策略。

[示例和图册](../ai/usage/DEMOS.md)提供可运行配方；错误处理见[排错](../ai/usage/TROUBLESHOOTING.md)。修改库源码请转到[维护者目录](../development/README.md)。
