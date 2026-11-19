"""Verify a reviewed release manifest and exactly the wheel bytes it names."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def read_verified(path, row):
    data = path.read_bytes()
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError(f'Artifact SHA or size mismatch: {path.name}')
    return data


def expected_platforms(directory, manifest):
    if manifest['status'] == 'LOCAL_GPU_ACCEPTED':
        if any(manifest['platforms'][name]['status'] != 'ACCEPTED' for name in ('windows', 'linux')):
            raise ValueError('Missing platform acceptance')
        return {'win_amd64', 'manylinux_2_28_x86_64'}

    if manifest['status'] != 'MACOS_ACCEPTED':
        raise ValueError('Missing macOS or Windows/Linux acceptance')
    expected = set()
    for arch in ('arm64', 'x86_64'):
        row = manifest['platforms'][f'macos-{arch}']
        receipt = directory / f'macos-{arch}-smoke.json'
        result = json.loads(read_verified(receipt, row))
        tag = f'macosx_13_0_{arch}'
        wheel = f"py_skia_canvas-{manifest['version']}-cp313-cp313-{tag}.whl"
        if (result['status'] != 'PASS' or result['arch'] != arch or result['wheel'] != wheel
                or result['cpu']['renderer'] != 'CPU'):
            raise ValueError(f'Missing exact CPU wheel smoke for {arch}')
        if arch == 'arm64' and (result['metal'] is not True or result['default'].get('api') != 'Metal'
                                or result['default']['renderer'] != 'GPU'):
            raise ValueError('Missing Apple Silicon Metal smoke')
        if not any(item['file'] == wheel and item['sha256'] == result['wheelSha256']
                   for item in manifest['wheels']):
            raise ValueError(f'Acceptance tested a different wheel: {arch}')
        expected.add(tag)
    return expected


def verify(directory, manifest_sha256):
    """Verify each artifact and its independently reviewed acceptance identity."""
    raw = (directory / 'release-manifest.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != manifest_sha256:
        raise ValueError('Manifest SHA mismatch')
    manifest = json.loads(raw)
    version = manifest['version']
    allowed = {f'py_skia_canvas-{version}-cp313-cp313-{tag}.whl'
               for tag in expected_platforms(directory, manifest)}
    seen = set()
    for row in manifest['wheels']:
        name = row['file']
        if name not in allowed or name in seen:
            raise ValueError('Unsupported or duplicate wheel version/ABI/platform')
        path = directory / name
        if path.resolve().parent != directory.resolve():
            raise ValueError('Invalid wheel path')
        read_verified(path, row)
        seen.add(name)
        with zipfile.ZipFile(path) as archive:
            metadata = archive.read(f'py_skia_canvas-{version}.dist-info/METADATA').decode()
            if '\nName: py-skia-canvas\n' not in metadata or f'\nVersion: {version}\n' not in metadata:
                raise ValueError('Wheel metadata version/name mismatch')
            if any(name.lower().endswith(('.node', '.ttf', '.otf', '.ttc', '.js', '.mjs'))
                   or 'node_modules/' in name or '/references/' in name for name in archive.namelist()):
                raise ValueError('Development/font payload in wheel')
    if seen != allowed or {path.name for path in directory.glob('*.whl')} != allowed:
        raise ValueError('Missing or unexpected wheel in bundle')
    if row := manifest.get('sourceDistribution'):
        if row['file'] != f'py_skia_canvas-{version}.tar.gz':
            raise ValueError('Unexpected source archive')
        read_verified(directory / row['file'], row)
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    manifest = verify(args.directory, args.manifest_sha256)
    print(json.dumps(dict(status='EXACT_REVIEWED_WHEELS', version=manifest['version'], wheels=len(manifest['wheels']))))
