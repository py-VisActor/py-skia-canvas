"""Read-only release-description checks on candidate wheels, separate from rendering."""
from __future__ import annotations

import argparse
from email.parser import Parser
import hashlib
import json
from pathlib import Path
import re
import zipfile


def check(wheel: Path, version: str) -> dict:
    """Check package/version/Python/README links and installation; never alter wheel bytes.

    Input is a wheel path and intended release version. Returns scoped metadata
    result/errors, raises on malformed zip/metadata. No native code/threads loaded.
    Historical accepted wheels can fail this new description-quality gate without
    invalidating their separate rendering acceptance.
    """
    errors = []
    payload = wheel.read_bytes()
    with zipfile.ZipFile(wheel) as archive:
        entries = [p for p in archive.namelist() if p.endswith('.dist-info/METADATA')]
        if len(entries) != 1:
            raise ValueError('Wheel must contain exactly one METADATA')
        text = archive.read(entries[0]).decode('utf-8')
    metadata = Parser().parsestr(text)
    description = metadata.get_payload()
    expected = f'python -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas=={version}'
    if metadata.get('Name') != 'py-skia-canvas' or metadata.get('Version') != version:
        errors.append('Candidate package/version differs from intended release')
    if set(metadata.get('Requires-Python', '').replace(' ', '').split(',')) != {'>=3.13', '<3.14'}:
        errors.append('Expected the currently supported CPython 3.13 range')
    if not metadata.get('Description-Content-Type', '').startswith('text/markdown'):
        errors.append('Expected a Markdown project description')
    if expected not in description:
        errors.append('Description must show the intended release installation command')
    if re.search(r'尚未发布|未发布到\s*PyPI|not yet published|not published to (?:production )?PyPI', description, re.I):
        errors.append('Description contains an upload-time unpublished claim that will become stale')
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', description):
        if not re.match(r'https?://|#', target):
            errors.append(f'PyPI description has a repository-relative link: {target}')
    if not any(re.match(r'Documentation,\s*https://', url, re.I) for url in metadata.get_all('Project-URL', [])):
        errors.append('Metadata must provide an absolute Documentation project URL')
    return dict(status='PACKAGE_METADATA_CHECKED' if not errors else 'INCOMPLETE', wheel=wheel.name, version=version,
                wheelSha256=hashlib.sha256(payload).hexdigest(), errors=errors,
                limitation='Description/installation/link checks only; no wheel runtime, rendering or publication acceptance.')


def main():
    """Check one candidate, optionally write a fresh report; exit nonzero on failures."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('wheel', type=Path)
    parser.add_argument('--version', required=True)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if args.out is not None and args.out.exists():
        parser.error('Evidence exists; choose a fresh --out')
    result = check(args.wheel, args.version)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open('x', encoding='utf-8') as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not result['errors'] else 1)


if __name__ == '__main__':
    main()
