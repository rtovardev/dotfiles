import json
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
from check import check_auto_title
from manifest import ROOT, links


class AutoTitleTest(unittest.TestCase):
    def validate(self, content):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'config.env'
            path.write_text(content)
            return check_auto_title(path)

    def test_public_config_and_single_writer(self):
        values = check_auto_title(ROOT / 'herdr/auto-title.env')
        self.assertEqual(values['HERDR_AUTO_TITLE_TRANSCRIPT'], 'false')
        self.assertEqual(values['HERDR_AUTO_TITLE_PANES'], 'true')
        self.assertEqual(values['HERDR_AUTO_TITLE_WORKSPACES'], 'true')
        bar = json.loads((ROOT / 'herdr/bar.json').read_text())
        self.assertIs(bar['auto_titles'], False)
        self.assertIs(bar['tab_status'], False)
        config = tomllib.loads((ROOT / 'herdr/config.toml').read_text())
        rows = config['ui']['sidebar']['spaces']['rows']
        self.assertEqual(rows[1][0]['token'], '$topic')
        self.assertTrue(any(key['command'] == 'herdr.auto-title.restart'
                            for key in config['keys']['command']))

    def test_comments_and_valid_settings(self):
        self.assertEqual(self.validate('# comment\n\nHERDR_AUTO_TITLE_POLL_MS=500\n'),
                         {'HERDR_AUTO_TITLE_POLL_MS': '500'})

    def test_invalid_config_is_refused(self):
        for content in ['', 'SECRET=value', 'HERDR_AUTO_TITLE_PANES=yes',
                        'HERDR_AUTO_TITLE_POLL_MS=0', 'HERDR_AUTO_TITLE_POLL_MS=-1',
                        'HERDR_AUTO_TITLE_POLL_MS=abc', 'HERDR_AUTO_TITLE_PANES',
                        'HERDR_AUTO_TITLE_PANES=true\nHERDR_AUTO_TITLE_PANES=false']:
            with self.subTest(content=content), self.assertRaises(ValueError):
                self.validate(content)

    def test_only_public_config_is_linked(self):
        home = Path('/fixture')
        targets = dict(links(home))
        self.assertEqual(targets[ROOT / 'herdr/auto-title.env'],
                         home / '.config/herdr-auto-title/config.env')
        self.assertFalse(any('manual-names' in str(path) for path in targets.values()))


if __name__ == '__main__':
    unittest.main()
