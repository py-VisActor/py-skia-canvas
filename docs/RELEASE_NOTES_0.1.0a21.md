# py-skia-canvas 0.1.0a21

macOS 13 or later now has native CPython 3.13 wheels for Apple Silicon and Intel. Both wheels pass isolated installation, CPU pixel readback, font measurement, PNG, SVG and PDF checks. The Apple Silicon wheel also passes offscreen Metal checks on macOS 13.7.8. Metal also passed on the virtual graphics device of the Intel CI runner. Physical Intel hardware and App/Window presentation remain unverified.

```sh
python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a21
```

For Windows AMD64 and Linux x86_64 with glibc 2.28 or later, use `py-skia-canvas==0.1.0a20`. See the [installation guide](https://github.com/py-VisActor/py-skia-canvas/blob/main/docs/ai/INSTALL.en.md).
