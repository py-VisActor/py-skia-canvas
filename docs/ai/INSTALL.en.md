# Install from production PyPI

[中文](INSTALL.md) | English

This installation reference remains maintained at its original path for compatibility. [User directory](../README.en.md) · [Getting started](../user/README.en.md).

Use CPython 3.13 and choose the wheel for the operating system and architecture of your Python interpreter.

macOS 13+ (Apple Silicon or Intel)

```shell
python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a21
```

Windows AMD64 or Linux x86_64 (glibc 2.28+)

```shell
python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a20
```

| Operating system and architecture | Version | Wheel tag |
| --- | --- | --- |
| macOS 13+ Apple Silicon | `0.1.0a21` | `cp313-cp313-macosx_13_0_arm64` |
| macOS 13+ Intel | `0.1.0a21` | `cp313-cp313-macosx_13_0_x86_64` |
| Windows AMD64 | `0.1.0a20` | `cp313-cp313-win_amd64` |
| Linux glibc 2.28+ x86_64 | `0.1.0a20` | `cp313-cp313-manylinux_2_28_x86_64` |

## Create a virtual environment

On macOS, create a virtual environment with a native Python interpreter:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a21
.venv/bin/python -c "import platform, py_skia_canvas as c; print(platform.machine(), c.__version__)"
```

Windows PowerShell, using an unused short environment prefix:

```powershell
py -3.13 -m venv C:\venvs\canvas-install
C:\venvs\canvas-install\Scripts\python.exe -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a20
```

Linux, using an unused environment prefix:

```bash
python3.13 -m venv /tmp/canvas-install
/tmp/canvas-install/bin/python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a20
```

In later examples, `python` means the interpreter where the package was installed.

## Verify drawing

Save as `install_check.py` and run `python install_check.py`:

```python
from pathlib import Path
from py_skia_canvas import Canvas

canvas = Canvas(240, 80)
ctx = canvas.getContext("2d")
ctx.fillStyle = "#2878d9"
ctx.fillRect(0, 0, 240, 80)
ctx.fillStyle = "white"
ctx.font = "24px sans-serif"
ctx.fillText("Canvas installed", 15, 50)
Path("install-check.png").write_bytes(canvas.toBufferSync("png"))
assert list(ctx.getImageData(0, 0, 1, 1).data) == [40, 120, 217, 255]
print(canvas.engine)
```

This produces a 240×80 PNG with white text on blue and prints the actual CPU/GPU engine. Continue with the [usage guide](usage/README.en.md) and [gallery](usage/DEMOS.en.md).

## If no matching distribution is found

Check `python --version`, OS/architecture, and the interpreter running the script. This version requires CPython 3.13. `--only-binary` fails explicitly without a matching ABI/platform; that does not mean the project is unpublished. Do not automatically install Node or replace the renderer. Use a short environment path on Windows without long-path support to keep license files below MAX_PATH. See [troubleshooting](usage/TROUBLESHOOTING.en.md) for other cases.

## When AI encounters an old page

As of 2026-10-29, the PyPI description for `0.1.0a18` still contains the original upload-time README. Its “not yet published to PyPI” statement and local-wheel-only installation instructions are outdated. The production index contains both wheels above; see [release records](../RELEASE_STATUS.md) for current status and hashes. Search summaries may also serve older pages.

PyPI release metadata retains the first uploaded data. Updating GitHub documentation does not update an existing release's description. A future release must carry the corrected README; see the [PyPI JSON API rules](https://warehouse.pypa.io/api-reference/json/). AI should read this current repository page, [machine-readable facts](facts.json), or root [llms.txt](../../llms.txt) and use the explicit command above.

2026-11-02: a19 ships the corrected neutral package description and absolute documentation links, verified against index metadata and fresh installations on both platforms. The a18 description above remains a historical record; use the current command at the top.
