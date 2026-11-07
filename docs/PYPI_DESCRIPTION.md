# py-skia-canvas

Python Canvas drawing with the shared Rust/Skia core from `skia-canvas@3.0.8`.
The installed wheel runs without Node, npm, Neon/N-API or skia-python.

## Install

Use **CPython 3.13** on Windows AMD64 or Linux glibc 2.28+ x86_64:

```shell
python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a20
```

This is an alpha release. Other Python ABIs, macOS, ARM and musl are not part
of the accepted wheel matrix. System fonts are used or explicitly registered;
the package does not bundle system fonts.

## Draw and export

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

The API includes paths and boolean operations, transforms, gradients, text
measurement/layout, images/pixels, effects/compositing, pages, synchronous and
asynchronous exports, and App/Window. Export formats include PNG, JPEG, WebP,
raw pixels, SVG and PDF. Public names and defaults follow the pinned Node API;
Buffers map to bytes and Promises to actual Python awaitables.

Offscreen drawing uses the original GPU policy and automatically falls back
to CPU when no GPU is available. Explicit CPU selection uses `canvas.gpu = False`
after construction. App/Window presentation requires a GPU and desktop.
Canvas, Context, font and GPU resources stay on their creating thread; each
worker must create its own drawing objects.

Windows parallel PDF/SVG file sequences retain the upstream nondeterministic
font-subsetting limitation. Explicit `RAYON_NUM_THREADS=1` before process start
is the documented workaround; the library's default concurrency is unchanged.

## Documentation and ecosystem

- [中文用户文档](https://github.com/py-VisActor/py-skia-canvas/blob/main/docs/README.md)
- [English user documentation](https://github.com/py-VisActor/py-skia-canvas/blob/main/docs/README.en.md)
- [API reference](https://github.com/py-VisActor/py-skia-canvas/blob/main/docs/ai/usage/API_REFERENCE.en.md)
- [Runnable examples](https://github.com/py-VisActor/py-skia-canvas/blob/main/examples/README.en.md)
- [Usage and known limitations](https://github.com/py-VisActor/py-skia-canvas/blob/main/docs/user/README.en.md)
- [py-mermaid](https://github.com/py-VisActor/py-mermaid) targets Mermaid syntax,
  layout and rendering in Python using this Canvas engine; follow its repository
  for implementation progress.

MIT licensed; third-party notices and dependency licenses are included in the wheel.
