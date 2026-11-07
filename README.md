# py-skia-canvas

中文 | [English](README.en.md)

Python Canvas 绘图库，复用 `skia-canvas@3.0.8` 的 Rust/Skia 核心。支持路径、文本、图像、渐变、滤镜，以及 PNG、JPEG、WebP、SVG、PDF 导出。使用 wheel 不需要 Node、npm、Rust 工具链或 skia-python。

## 安装

需要 **CPython 3.13**，支持 Windows AMD64 和 Linux glibc 2.28+ x86_64。当前版本为 alpha 预发行版。

```shell
python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a19
```

## 最小示例

```python
from pathlib import Path
from py_skia_canvas import Canvas

canvas = Canvas(360, 180)
ctx = canvas.getContext("2d")
ctx.fillStyle = "white"
ctx.fillRect(0, 0, 360, 180)
ctx.fillStyle = "#2878d9"
ctx.fillRect(20, 20, 320, 80)
ctx.font = "24px sans-serif"
ctx.fillStyle = "#16243a"
ctx.fillText("Hello Canvas", 20, 145)
Path("hello.png").write_bytes(canvas.toBufferSync("png"))
```

## 使用与限制

- [用户文档](docs/README.md)：安装、使用指南、API、示例和排错。
- 默认保留原版 GPU 策略；无可用 GPU 时离屏绘制自动回退 CPU。显式 CPU 使用 `canvas.gpu = False`，在绘制前设置。
- Canvas、Context、字体和原生资源在创建线程使用。并行任务应各自创建绘图对象，只传递 bytes 或普通数据。
- 字体由系统或调用者提供，字体、驱动会影响输出。App/Window 需要 GPU 和桌面环境。
- macOS、ARM、musl 和其他 Python ABI 暂无本版本支持的 wheel。Windows 并行 PDF/SVG 文件序列保留上游字体子集限制，处理方式见[使用指南](docs/ai/usage/README.md)。

## 参与开发

修改库本身请从[维护者与 agent 文档](docs/development/README.md)开始。使用库编写应用无需执行维护者构建或验收流程。

[MIT 许可](LICENSE) · [第三方说明](THIRD_PARTY_NOTICES.md)
