# py-skia-canvas

[中文](README.md) | English

A Python Canvas drawing library using the Rust/Skia core from `skia-canvas@3.0.8`. Draw paths, text, images, gradients and effects, then export PNG, JPEG, WebP, SVG or PDF. Using a wheel requires no Node, npm, Rust toolchain or skia-python.

## Install

Requires **CPython 3.13** on Windows AMD64 or Linux glibc 2.28+ x86_64. The current version is an alpha prerelease.

```shell
python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a19
```

## Minimal example

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

## Usage and limitations

- [User documentation](docs/README.en.md): installation, usage guide, API, examples and troubleshooting.
- The original default GPU policy is preserved; offscreen drawing automatically falls back to CPU without a usable GPU. Set `canvas.gpu = False` before drawing to select CPU explicitly.
- Use Canvas, Context, fonts and native resources on their creating thread. Parallel workers create their own drawing objects and return bytes or plain data.
- Fonts come from the system or caller; fonts and drivers affect output. App/Window requires a GPU and desktop.
- This release has no supported wheels for macOS, ARM, musl or other Python ABIs. Windows parallel PDF/SVG file sequences retain an upstream font-subsetting limitation; see the [usage guide](docs/ai/usage/README.en.md) for the workaround.

## Contributing

To modify the library, start with the [maintainer and agent documentation](docs/development/README.en.md). Application users do not need the maintainer build or acceptance workflow.

[MIT license](LICENSE) · [Third-party notices](THIRD_PARTY_NOTICES.md)
