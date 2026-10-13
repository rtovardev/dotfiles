import contextlib
import importlib.util
import io
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / 'scripts/patch-herdr-bar.py'
spec = importlib.util.spec_from_file_location('patch_herdr_bar', SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError('No se puede cargar patch-herdr-bar.py')
patcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patcher)


class HerdrPatchTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'plugin'
        self.root.mkdir()
        self.run_git('init', '-q')
        self.source = self.root / 'source.txt'
        self.source.write_text('original\n')
        self.run_git('add', 'source.txt')
        self.run_git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                     'commit', '-qm', 'fixture')
        self.commit = self.run_git('rev-parse', 'HEAD').stdout.strip()
        self.patch = self.root.parent / 'fixture.patch'
        self.source.write_text('pi support\n')
        self.patch.write_text(self.run_git('diff').stdout)
        self.source.write_text('original\n')

    def run_git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], check=True,
                              capture_output=True, text=True)

    def apply(self, apply=False, commit=None, root=None):
        with contextlib.redirect_stdout(io.StringIO()):
            return patcher.apply_patch(root or self.root, apply, self.patch,
                                       commit or self.commit)

    def test_plan_does_not_modify_plugin(self):
        self.assertFalse(self.apply())
        self.assertEqual(self.source.read_text(), 'original\n')
        self.assertEqual(self.run_git('status', '--porcelain').stdout, '')

    def test_apply_is_idempotent(self):
        self.assertTrue(self.apply(True))
        self.assertEqual(self.source.read_text(), 'pi support\n')
        self.assertFalse(self.apply(True))

    def test_other_revision_is_refused_without_mutation(self):
        with self.assertRaisesRegex(RuntimeError, 'Parche limitado'):
            self.apply(True, commit='0' * 40)
        self.assertEqual(self.source.read_text(), 'original\n')

    def test_conflicting_user_changes_are_preserved(self):
        self.source.write_text('user changes\n')
        with self.assertRaisesRegex(RuntimeError, 'no aplica limpiamente'):
            self.apply(True)
        self.assertEqual(self.source.read_text(), 'user changes\n')

    def test_subdirectory_and_non_repository_are_refused(self):
        child = self.root / 'child'
        child.mkdir()
        for root in (child, self.root.parent):
            with self.subTest(root=root), self.assertRaisesRegex(RuntimeError, 'raíz Git'):
                self.apply(True, root=root)
        self.assertEqual(self.source.read_text(), 'original\n')
