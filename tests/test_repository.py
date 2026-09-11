"""Checks for maintained links, bundled licenses, and machine-readable templates."""

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def test_relative_markdown_links_resolve(self):
        for path in ROOT.rglob('*.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                with self.subTest(file=str(path.relative_to(ROOT)), target=target):
                    self.assertTrue((path.parent / target.split('#', 1)[0]).exists())

    def test_json_fragments_parse(self):
        for path in (ROOT / 'templates').rglob('*.json'):
            with self.subTest(file=str(path.relative_to(ROOT))):
                self.assertIsInstance(json.loads(path.read_text()), dict)

    def test_skill_licenses_travel_with_each_folder(self):
        for entry in (ROOT / 'skills').glob('*/SKILL.md'):
            with self.subTest(skill=entry.parent.name):
                header = entry.read_text().split('---', 2)[1]
                licenses = re.findall(r'^license: (.+)$', header, re.MULTILINE)
                self.assertEqual(len(licenses), 1)
                license_id = licenses[0]
                folder = entry.parent
                if (folder / 'NOTICE.md').exists():
                    titles = {'MIT': 'MIT License', 'Apache-2.0': 'Apache License'}
                    self.assertIn(license_id, titles)
                    self.assertTrue((folder / 'LICENSE').read_text().lstrip().startswith(titles[license_id]))
                    self.assertIn(f'licensed under {license_id}', (folder / 'NOTICE.md').read_text())
                else:
                    self.assertEqual(license_id, 'MIT OR Apache-2.0')
                    for name in ('LICENSE-MIT', 'LICENSE-APACHE'):
                        self.assertEqual((folder / name).read_bytes(), (ROOT / name).read_bytes())


if __name__ == '__main__':
    unittest.main()
