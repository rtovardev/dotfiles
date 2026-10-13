import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
from install import install
from manifest import links
from restore import restore


class InstallTest(unittest.TestCase):
    def test_plan_apply_repeat_and_restore_regular_and_broken_links(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            home = Path(directory)
            rc = home / '.zshrc'
            rc.write_text('original config\n')
            herdr = home / '.config/herdr/config.toml'
            herdr.parent.mkdir(parents=True)
            herdr.write_text('onboarding = false\n')
            registry = herdr.parent / 'plugins.json'
            registry.write_text('[]\n')
            bar = herdr.parent / 'plugins/config/herdr-bar/config.json'
            bar.parent.mkdir(parents=True)
            bar.write_text('{"auto_titles": false}\n')
            private = herdr.parent / 'plugins/config/heeler/private.json'
            private.parent.mkdir(parents=True)
            private.write_text('{"fixture": "preserve"}\n')
            auto_title = home / '.config/herdr-auto-title/config.env'
            auto_title.parent.mkdir(parents=True)
            auto_title.write_text('HERDR_AUTO_TITLE_MAX_LENGTH=40\n')
            manual = auto_title.parent / 'manual-names.json'
            manual.write_text('{"locked": {}}\n')
            broken = home / '.config/atuin/config.toml'
            broken.parent.mkdir(parents=True)
            broken.symlink_to('/missing/previous/atuin.toml')
            install(home)
            self.assertFalse(rc.is_symlink())
            self.assertEqual(rc.read_text(), 'original config\n')
            self.assertFalse(herdr.is_symlink())
            self.assertFalse(bar.is_symlink())
            self.assertEqual(bar.read_text(), '{"auto_titles": false}\n')
            self.assertEqual(auto_title.read_text(), 'HERDR_AUTO_TITLE_MAX_LENGTH=40\n')
            backup = install(home, True)
            if backup is None:
                self.fail('install --apply no creó el respaldo')
            for source, target in links(home):
                self.assertEqual(target.resolve(), source.resolve())
            self.assertEqual(registry.read_text(), '[]\n')
            self.assertEqual(private.read_text(), '{"fixture": "preserve"}\n')
            self.assertEqual(manual.read_text(), '{"locked": {}}\n')
            self.assertIsNone(install(home, True))
            restore(backup, True)
            self.assertEqual(rc.read_text(), 'original config\n')
            self.assertEqual(herdr.read_text(), 'onboarding = false\n')
            self.assertFalse(herdr.is_symlink())
            self.assertEqual(bar.read_text(), '{"auto_titles": false}\n')
            self.assertFalse(bar.is_symlink())
            self.assertEqual(private.read_text(), '{"fixture": "preserve"}\n')
            self.assertEqual(auto_title.read_text(), 'HERDR_AUTO_TITLE_MAX_LENGTH=40\n')
            self.assertFalse(auto_title.is_symlink())
            self.assertEqual(manual.read_text(), '{"locked": {}}\n')
            self.assertEqual(registry.read_text(), '[]\n')
            self.assertEqual(str(broken.readlink()), '/missing/previous/atuin.toml')
            self.assertFalse((home / '.zprofile').exists())

    def test_restore_refuses_later_user_changes(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            home = Path(directory)
            backup = install(home, True)
            if backup is None:
                self.fail('install --apply no creó el respaldo')
            rc = home / '.zshrc'
            rc.unlink()
            rc.write_text('new user work')
            with self.assertRaises(RuntimeError):
                restore(backup, True)
            self.assertEqual(rc.read_text(), 'new user work')
            self.assertTrue((home / '.zshenv').is_symlink())


if __name__ == '__main__':
    unittest.main()
