import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
from install import install
from restore import restore
from manifest import links


class InstallTest(unittest.TestCase):
    def test_plan_apply_repeat_and_restore_regular_and_broken_links(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            home = Path(directory)
            rc = home / '.zshrc'
            rc.write_text('original config\n')
            broken = home / '.config/atuin/config.toml'
            broken.parent.mkdir(parents=True)
            broken.symlink_to('/missing/previous/atuin.toml')
            install(home)
            self.assertFalse(rc.is_symlink())
            self.assertEqual(rc.read_text(), 'original config\n')
            backup = install(home, True)
            self.assertIsNotNone(backup)
            for source, target in links(home):
                self.assertEqual(target.resolve(), source.resolve())
            self.assertIsNone(install(home, True))
            restore(backup, True)
            self.assertEqual(rc.read_text(), 'original config\n')
            self.assertEqual(str(broken.readlink()), '/missing/previous/atuin.toml')
            self.assertFalse((home / '.zprofile').exists())

    def test_restore_refuses_later_user_changes(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            home = Path(directory)
            backup = install(home, True)
            rc = home / '.zshrc'
            rc.unlink()
            rc.write_text('new user work')
            with self.assertRaises(RuntimeError):
                restore(backup, True)
            self.assertEqual(rc.read_text(), 'new user work')
            self.assertTrue((home / '.zshenv').is_symlink())


if __name__ == '__main__':
    unittest.main()
