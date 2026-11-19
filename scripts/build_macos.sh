#!/usr/bin/env bash
# Build an architecture-specific CPython 3.13 wheel using the macOS Metal backend.
set -euo pipefail
cd "$(dirname "$0")/.."

python=${PY_SKIA_BUILD_PYTHON:-python3.13}
case "$(uname -m)" in
    arm64) target=aarch64-apple-darwin ;;
    x86_64) target=x86_64-apple-darwin ;;
    *) echo "Unsupported macOS architecture" >&2; exit 1 ;;
esac
"$python" -c 'import platform, sys; assert sys.platform == "darwin" and sys.implementation.name == "cpython" and sys.version_info[:2] == (3, 13); assert platform.machine() == sys.argv[1], "Use a native interpreter for this architecture"' "$(uname -m)"
export MACOSX_DEPLOYMENT_TARGET=13.0
export CARGO_TARGET_DIR=${CARGO_TARGET_DIR:-"$PWD/target"}
"$python" -m maturin build --release --locked --interpreter "$python" --target "$target" --out "${PY_SKIA_WHEEL_OUT:-dist}"
