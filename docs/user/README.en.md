# User guide

[中文](README.md) | English

Install `py-skia-canvas`; import `py_skia_canvas`. Start by generating a PNG with the [minimal example](../../README.en.md#minimal-example), then use the references below for your task.

## Installation and runtime

Use CPython 3.13 on Windows AMD64 or Linux glibc 2.28+ x86_64:

```shell
python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a20
python -c "import py_skia_canvas as c; print(c.__version__, c.__file__)"
```

Wheels do not require compiling Skia. See [installation](../ai/INSTALL.en.md) for virtual environments, offline wheels and Windows path limitations.

## Drawing and output

A Canvas starts transparent; draw a background when needed. The origin is at the upper left, and `fillText` uses a baseline y coordinate. Set the font before measuring, and measure/draw with the same font and width. The [usage reference](../ai/usage/README.en.md) covers paths, images, fonts, pages and async work; the [API reference](../ai/usage/API_REFERENCE.en.md) lists public names and parameters.

| Task | API |
| --- | --- |
| Get encoded bytes | `canvas.toBufferSync("png")` / `await canvas.toBuffer("png")` |
| Write a file | `canvas.toFileSync(path)` / `await canvas.toFile(path)` |
| Load an encoded image | `await loadImage(source)` |
| Select CPU | Set `canvas.gpu = False` before drawing |
| Inspect the actual backend | `canvas.engine` |

Exports include PNG, JPEG, WebP, raw, SVG and PDF. See the [output reference](../ai/usage/README.en.md) for formats, density, quality and page numbering. `loadImageData` takes raw pixels rather than decoding encoded images.

## Resources and deployment limits

Drawing objects and font registrations belong to their creating thread. Each worker creates its own Canvas, loads/registers resources and exports bytes; do not pass an existing Context to another thread. Fonts come from the system or application. Family availability does not guarantee coverage of every character.

Offscreen drawing automatically uses CPU without a usable GPU; App/Window still requires a GPU and desktop. The constructor's `gpu=False` option is not a replacement for the CPU setter. Windows default parallel PDF/SVG file sequences retain an upstream font-subsetting limitation. Explicitly set `RAYON_NUM_THREADS=1` before starting the process as a workaround; the library's default concurrency is unchanged.

[Examples and gallery](../ai/usage/DEMOS.en.md) provide runnable recipes. See [troubleshooting](../ai/usage/TROUBLESHOOTING.en.md) for errors. To modify the library itself, use the [maintainer directory](../development/README.en.md).
