"""Pruebas del traslado de bytes y del rechazo de fuentes incompletas."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('base_414', Path(__file__).with_name('base_414.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def sha(b):
    return hashlib.sha256(b).hexdigest()


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.source = self.folder / 'source'
        self.source.mkdir()
        self.root_before = m.ROOT
        m.ROOT = self.folder / 'target'
        self.addCleanup(setattr, m, 'ROOT', self.root_before)
        self.files = {'codigo.py': b'print(1)\r\n', 'datos.xlsx': b'opaque\x00bytes'}
        manifest = b'original manifest\r\n'
        for name, content in self.files.items():
            (self.source / name).write_bytes(content)
        (self.source / 'MANIFIESTO_SHA256.txt').write_bytes(manifest)
        self.data = {'manifest_sha256': sha(manifest), 'archive_prefix': 'munger_v2_r1/',
                     'files': [{'path': n, 'sha256': sha(b), 'storage': 'git' if n.endswith('.py') else 'release_asset'}
                               for n, b in self.files.items()]}

    def test_materializes_exact_bytes_and_is_idempotent(self):
        m.materialize(self.data, self.source, False)
        self.assertTrue(m.verify(self.data)['complete'])
        self.assertEqual((m.ROOT / 'codigo.py').read_bytes(), self.files['codigo.py'])
        before = (m.ROOT / 'codigo.py').stat().st_mtime_ns
        m.materialize(self.data, self.source, False)
        self.assertEqual(before, (m.ROOT / 'codigo.py').stat().st_mtime_ns)

    def test_git_only_excludes_binary(self):
        m.materialize(self.data, self.source, True)
        self.assertTrue(m.verify(self.data, True)['complete'])
        self.assertFalse((m.ROOT / 'datos.xlsx').exists())
        self.assertFalse(m.verify(self.data)['complete'])

    def test_missing_binary_rejects_even_git_only_before_writes(self):
        (self.source / 'datos.xlsx').unlink()
        with self.assertRaises(FileNotFoundError):
            m.materialize(self.data, self.source, True)
        self.assertFalse(m.ROOT.exists())

    def test_changed_source_rejects_before_writes(self):
        (self.source / 'datos.xlsx').write_bytes(b'changed')
        with self.assertRaises(ValueError):
            m.materialize(self.data, self.source, False)
        self.assertFalse(m.ROOT.exists())

    def test_changed_destination_is_preserved(self):
        m.ROOT.mkdir()
        (m.ROOT / 'datos.xlsx').write_bytes(b'new work')
        with self.assertRaises(ValueError):
            m.materialize(self.data, self.source, False)
        self.assertEqual((m.ROOT / 'datos.xlsx').read_bytes(), b'new work')
        self.assertFalse((m.ROOT / 'codigo.py').exists())

    def test_destination_symlink_rejected(self):
        m.ROOT.mkdir()
        (m.ROOT / 'codigo.py').symlink_to(self.source / 'codigo.py')
        with self.assertRaises(ValueError):
            m.materialize(self.data, self.source, False)

    def test_complete_zip_and_wrong_zip(self):
        archive = self.folder / 'full.zip'
        with zipfile.ZipFile(archive, 'w') as z:
            for p in self.source.iterdir():
                z.write(p, 'munger_v2_r1/' + p.name)
        self.data.update(zip_size=archive.stat().st_size, zip_sha256=sha(archive.read_bytes()))
        m.materialize(self.data, archive, False)
        self.assertTrue(m.verify(self.data)['complete'])
        archive.write_bytes(archive.read_bytes() + b'changed')
        with self.assertRaises(ValueError):
            m.materialize(self.data, archive, False)


if __name__ == '__main__':
    unittest.main()
