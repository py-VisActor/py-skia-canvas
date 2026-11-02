"""Candidate README regressions using metadata-only zip fixtures, not renderer tests."""
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from check_package_metadata import check


class PackageDescriptionTests(unittest.TestCase):
    def fixture(self, body=None, version='0.1.0a19', documentation=True):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / 'metadata-only-fixture.whl'
        description = body if body is not None else '# Canvas\n\npython -m pip install --index-url https://pypi.org/simple/ --only-binary=:all: py-skia-canvas==0.1.0a19\n'
        text = f'Metadata-Version: 2.4\nName: py-skia-canvas\nVersion: {version}\nRequires-Python: >=3.13,<3.14\nDescription-Content-Type: text/markdown\n'
        if documentation:
            text += 'Project-URL: Documentation, https://github.com/xuanhun/py-skia-canvas/blob/main/docs/ai/README.md\n'
        with zipfile.ZipFile(path, 'w') as archive:
            archive.writestr('fixture.dist-info/METADATA', text+'\n'+description)
        return path

    def test_neutral_release_description_passes_without_loading_native(self):
        self.assertEqual(check(self.fixture(), '0.1.0a19')['status'], 'PACKAGE_METADATA_CHECKED')

    def test_past_upload_unpublished_claim_fails(self):
        path = self.fixture()
        with zipfile.ZipFile(path) as archive:
            text = archive.read('fixture.dist-info/METADATA').decode()
        with zipfile.ZipFile(path, 'w') as archive:
            archive.writestr('fixture.dist-info/METADATA', text+'\nNot yet published to PyPI.\n')
        self.assertEqual(check(path, '0.1.0a19')['status'], 'INCOMPLETE')

    def test_local_wheel_only_installation_fails(self):
        result = check(self.fixture('python -m pip install /path/to/file.whl'), '0.1.0a19')
        self.assertEqual(result['status'], 'INCOMPLETE')

    def test_wrong_release_version_fails(self):
        self.assertEqual(check(self.fixture(), '0.1.0a20')['status'], 'INCOMPLETE')

    def test_relative_documentation_links_fail(self):
        result = check(self.fixture('[Docs](docs/ai/README.md)'), '0.1.0a19')
        self.assertTrue(any('repository-relative' in error for error in result['errors']))

    def test_missing_documentation_metadata_url_fails(self):
        self.assertEqual(check(self.fixture(documentation=False), '0.1.0a19')['status'], 'INCOMPLETE')


if __name__ == '__main__':
    unittest.main()
