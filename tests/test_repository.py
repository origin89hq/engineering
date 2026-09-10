"""Checks for maintained links and machine-readable templates."""

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


if __name__ == '__main__':
    unittest.main()
