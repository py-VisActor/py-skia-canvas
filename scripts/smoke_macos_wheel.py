"""Check an installed macOS wheel and exercise native drawing outside the checkout."""

import argparse
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform
import subprocess
import sys
import zipfile

import py_skia_canvas
from py_skia_canvas import Canvas, FontLibrary, _native


def verify_native(wheel, arch):
    installed = Path(_native.__file__).resolve()
    assert installed.is_relative_to(Path(sys.prefix).resolve()), installed
    installed_bytes = installed.read_bytes()
    with zipfile.ZipFile(wheel) as archive:
        assert archive.read(f"py_skia_canvas/{installed.name}") == installed_bytes
    tags = wheel.name.removesuffix(".whl").split("-")
    assert tags[1:] == [version("py-skia-canvas"), "cp313", "cp313", f"macosx_13_0_{arch}"], tags
    assert py_skia_canvas.__version__ == tags[1]
    architectures = subprocess.check_output(["/usr/bin/lipo", "-archs", installed], text=True).split()
    assert architectures == [arch], architectures
    build = subprocess.check_output(["/usr/bin/vtool", "-show-build", installed], text=True).splitlines()
    minimum = [line.split()[1] for line in build if line.strip().startswith("minos ")]
    assert len(minimum) == 1 and tuple(map(int, minimum[0].split("."))) <= (13, 0), build
    libraries = subprocess.check_output(["/usr/bin/otool", "-L", installed], text=True).splitlines()[1:]
    dependencies = [line.split(" (", 1)[0].strip() for line in libraries]
    assert all(path.startswith(("/System/Library/", "/usr/lib/")) for path in dependencies), dependencies
    return {"deploymentTarget": minimum[0], "libraries": dependencies}


def render(canvas, *, cpu=False):
    if cpu:
        canvas.gpu = False
    context = canvas.getContext("2d")
    context.fillStyle = "#2878d9"
    context.fillRect(0, 0, canvas.width, canvas.height)
    assert bytes(context.getImageData(0, 0, 1, 1).data) == bytes((40, 120, 217, 255))
    assert FontLibrary.families
    context.font = "18px sans-serif"
    assert context.measureText("macOS").width > 0
    context.fillStyle = "white"
    context.fillText("macOS", 2, 20)
    assert set(bytes(context.getImageData(0, 0, 40, 24).data)) > {40, 120, 217, 255}
    assert canvas.toBufferSync("png").startswith(b"\x89PNG\r\n\x1a\n")
    assert b"<svg" in canvas.toBufferSync("svg")
    assert canvas.toBufferSync("pdf").startswith(b"%PDF-")
    return canvas.engine


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", type=Path)
    parser.add_argument("--arch", required=True, choices=("arm64", "x86_64"))
    parser.add_argument("--require-metal", action="store_true")
    args = parser.parse_args()
    assert sys.platform == "darwin" and platform.machine() == args.arch
    assert sys.implementation.name == "cpython" and sys.version_info[:2] == (3, 13)
    native = verify_native(args.wheel, args.arch)
    cpu = render(Canvas(40, 24), cpu=True)
    assert cpu["renderer"] == "CPU", cpu
    default = render(Canvas(40, 24))
    metal = default["renderer"] == "GPU" and default.get("api") == "Metal"
    assert metal or default["renderer"] == "CPU", default
    if args.require_metal:
        assert metal, default
    print(json.dumps({
        "status": "PASS",
        "arch": args.arch,
        "macOS": platform.mac_ver()[0],
        "python": platform.python_version(),
        "wheel": args.wheel.name,
        "wheelSha256": hashlib.sha256(args.wheel.read_bytes()).hexdigest(),
        "native": native,
        "cpu": cpu,
        "default": default,
        "metal": metal,
    }, indent=2))


if __name__ == "__main__":
    main()
