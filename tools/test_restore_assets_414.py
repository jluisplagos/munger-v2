"""Verifica conservación de binarios y rechazo de alteraciones al recuperarlos."""
import hashlib
from pathlib import Path
import tempfile
import unittest
import zipfile
import base_414 as base
import restore_assets_414 as assets


def sha(b):
    return hashlib.sha256(b).hexdigest()


class AssetsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        previous = base.ROOT
        base.ROOT = self.folder / 'target'
        self.addCleanup(setattr, base, 'ROOT', previous)
        self.content = b'original binary\x00\xff\r\n'
        h = sha(self.content)
        self.data = {'manifest_sha256': sha(b'manifest'), 'files': [
            {'path': 'a.xlsx', 'sha256': h, 'storage': 'release_asset'},
            {'path': 'sub/b.xlsx', 'sha256': h, 'storage': 'release_asset'},
            {'path': 'missing.pdf', 'sha256': sha(b'missing'), 'storage': 'release_asset'}]}
        self.bundle = self.folder / 'assets.zip'
        with zipfile.ZipFile(self.bundle, 'w') as z:
            z.writestr('objects/' + h, self.content)
        self.meta = {'bundle_size': self.bundle.stat().st_size, 'bundle_sha256': base.sha_file(self.bundle), 'objects': [h]}
        base.ROOT.mkdir()
        (base.ROOT / 'MANIFIESTO_SHA256.txt').write_bytes(b'manifest')

    def test_aliases_restored_without_claiming_complete(self):
        report = assets.restore(self.bundle, self.meta, self.data)
        self.assertEqual(report['binary_files_restored'], 2)
        self.assertFalse(report['complete'])
        self.assertEqual(report['missing'], ['missing.pdf'])
        for name in ['a.xlsx', 'sub/b.xlsx']:
            self.assertEqual((base.ROOT / name).read_bytes(), self.content)
        self.assertEqual(assets.restore(self.bundle, self.meta, self.data)['binary_files_restored'], 0)

    def test_wrong_bundle_hash_changes_nothing(self):
        self.bundle.write_bytes(self.bundle.read_bytes() + b'changed')
        with self.assertRaises(ValueError):
            assets.restore(self.bundle, self.meta, self.data)
        self.assertFalse((base.ROOT / 'a.xlsx').exists())

    def test_wrong_object_hash_changes_nothing(self):
        with zipfile.ZipFile(self.bundle, 'w') as z:
            z.writestr('objects/' + self.meta['objects'][0], b'changed')
        self.meta.update(bundle_size=self.bundle.stat().st_size, bundle_sha256=base.sha_file(self.bundle))
        with self.assertRaises(ValueError):
            assets.restore(self.bundle, self.meta, self.data)
        self.assertFalse((base.ROOT / 'a.xlsx').exists())

    def test_modified_destination_preserved_before_any_copy(self):
        (base.ROOT / 'sub').mkdir()
        (base.ROOT / 'sub/b.xlsx').write_bytes(b'new work')
        with self.assertRaises(ValueError):
            assets.restore(self.bundle, self.meta, self.data)
        self.assertEqual((base.ROOT / 'sub/b.xlsx').read_bytes(), b'new work')
        self.assertFalse((base.ROOT / 'a.xlsx').exists())

    def test_unknown_object_rejected(self):
        self.meta['objects'].append(sha(b'unknown'))
        with self.assertRaises(ValueError):
            assets.restore(self.bundle, self.meta, self.data)
        self.assertFalse((base.ROOT / 'a.xlsx').exists())


if __name__ == '__main__':
    unittest.main()
