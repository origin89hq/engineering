"""Regression cases for contribution metadata, including untrusted PR text."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / '.github/actions/contribution/check.py'
spec = importlib.util.spec_from_file_location('contribution', SCRIPT)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
A, B = 'a' * 40, 'b' * 40


def metadata():
    return ({'title': 'perf: batch archived readings', 'body': 'Fetch archived readings in batches.\n\nValidation: success, invalid keys, limits, and upstream failures passed.',
             'head': {'ref': 'alex/batch-readings', 'sha': A}, 'user': {'login': 'alex-dev'}, 'commits': 1},
            [[{'sha': A, 'commit': {'message': 'perf: batch archived readings'}}]])


class ContributionTests(unittest.TestCase):
    def test_valid_metadata_and_legitimate_commit_body(self):
        pr, pages = metadata()
        pages[0][0]['commit']['message'] += '\n\nKeep batches bounded because the upstream API\nlimits each request.'
        self.assertEqual(check.validate(pr, pages, A), [])

    def test_long_pr_prose_is_valid_without_column_wrapping(self):
        pr, pages = metadata()
        pr['body'] = 'A paragraph can exceed eighty columns. ' * 10
        self.assertEqual(check.validate(pr, pages), [])

    def test_subject_boundaries_and_conventional_types(self):
        for subject in ('fix: ' + 'x' * 67, 'fix(worker)!: reject stale input', 'ci: check contributions', 'perf: batch reads'):
            with self.subTest(subject=subject):
                self.assertEqual(check.subject_errors(subject, 'Title'), [])
        for subject in ('fix: ' + 'x' * 68, 'Read the documents', 'fix: ', 'fix: sentence.', ' fix: space', 'fix: space ', 'fix: first\nfix: second'):
            with self.subTest(subject=subject):
                self.assertTrue(check.subject_errors(subject, 'Title'))

    def test_each_commit_is_checked_across_pages(self):
        pr, pages = metadata()
        pr['commits'] = 2
        pages.insert(0, [{'sha': B, 'commit': {'message': 'Update stuff'}}])
        self.assertTrue(any('Commit 1:' in error for error in check.validate(pr, pages)))
        pages[0][0]['commit']['message'] = 'fix: handle missing readings'
        self.assertEqual(check.validate(pr, pages), [])

    def test_attribution_in_commits_and_pr_body_is_rejected(self):
        for footer in ('Co-authored-by: Someone <someone@example.com>', 'Generated-by: an assistant',
                       '🤖 Generated with [Claude Code](https://example.com)', 'Written by Codex'):
            with self.subTest(footer=footer):
                pr, pages = metadata()
                pr['body'] += '\n\n' + footer
                pages[0][0]['commit']['message'] += '\n\n' + footer
                errors = check.validate(pr, pages)
                self.assertEqual(sum('remove attribution' in error for error in errors), 2)

    def test_discussing_ai_or_showing_a_footer_example_is_allowed(self):
        pr, pages = metadata()
        pr['title'] = pages[0][0]['commit']['message'] = 'fix: disable Claude attribution'
        pr['body'] = 'The settings disable attribution.\n\n```text\nCo-authored-by: example\n```'
        self.assertEqual(check.validate(pr, pages), [])

    def test_personal_prefix_has_no_shared_default(self):
        pr, pages = metadata()
        for branch in ('alex/batch-readings', 'sam/batch-readings', 'existing-branch'):
            with self.subTest(branch=branch):
                pr['head']['ref'] = branch
                self.assertEqual(check.validate(pr, pages), [])

    def test_nickname_prefix_applies_only_to_configured_contributor(self):
        pr, pages = metadata()
        config = {'branch_owner': 'alex-dev', 'branch_prefix': 'alex/'}
        self.assertEqual(check.validate(pr, pages, **config), [])
        pr['head']['ref'] = 'perf/batch-readings'
        self.assertTrue(any('PR branch:' in error for error in check.validate(pr, pages, **config)))
        pr['user']['login'] = 'another-contributor'
        self.assertEqual(check.validate(pr, pages, **config), [])
        pr['user']['login'] = 'github-actions[bot]'
        pr['head']['ref'] = 'changeset-release/main'
        self.assertEqual(check.validate(pr, pages, **config), [])
        pr['user']['login'] = 'ALEX-DEV'
        pr['head']['ref'] = 'alex/batch-readings'
        self.assertEqual(check.validate(pr, pages, **config), [])
        pr['head']['ref'] = 'alex/'
        self.assertTrue(check.validate(pr, pages, **config))

    def test_explicit_repository_branch_convention_can_be_configured(self):
        pr, pages = metadata()
        pr['head']['ref'] = 'release/prepare'
        self.assertEqual(check.validate(pr, pages, branch_owner='alex-dev', branch_prefix='release/'), [])

    def test_partial_or_whitespace_branch_configuration_fails(self):
        pr, pages = metadata()
        for owner, prefix in (('alex-dev', ''), ('', 'alex/'), (' ', 'alex/'), ('alex-dev', ' '), (' alex-dev', 'alex/'), ('alex-dev', 'alex/ ')):
            with self.subTest(owner=owner, prefix=prefix), self.assertRaisesRegex(ValueError, 'Configure'):
                check.validate(pr, pages, branch_owner=owner, branch_prefix=prefix)

    def test_hard_wrapped_paragraphs_are_rejected(self):
        for body in ('First part of a paragraph\ncontinues here.',
                     '## Change\n\nFirst part\nsecond part\n\n## Validation\n\nPassed.',
                     '<!-- hint -->\nFirst part\nsecond part'):
            with self.subTest(body=body):
                self.assertTrue(any('hard-wrapped' in error for error in check.body_errors(body)))

    def test_markdown_structures_and_intentional_breaks_are_preserved(self):
        cases = [
            '## Change\n\nOne paragraph.\n\nAnother paragraph.',
            '- First item\n  continued\n- Second item',
            '1. First item\n   continued\n2. Second item',
            '| Path | Result |\n| --- | --- |\n| Invalid | Rejected |',
            '> Quoted line\n> another quoted line',
            '```python\nfirst()\nsecond()\n```',
            '~~~~text\n```\nfirst\nsecond\n~~~~',
            '<!-- First hint\ncontinued hint -->\nOne paragraph.',
            'First line  \nIntentional break.',
            'First line\\\nIntentional break.',
            'Heading\n=======\n\nParagraph.',
            '    first()\n    second()',
            '[one]: https://example.com\n[two]: https://example.org',
            '<details>\n<summary>Details</summary>\n\nA paragraph.\n\n</details>',
        ]
        for body in cases:
            with self.subTest(body=body):
                self.assertEqual(check.body_errors(body), [])

    def test_prose_after_fences_comments_and_lists_is_still_checked(self):
        for prefix in ('```text\nexample\n```\n', '```html\n<!--\n```\n', '<!-- comment -->\n', '- A list\n\n'):
            with self.subTest(prefix=prefix):
                self.assertTrue(check.body_errors(prefix + 'First line\nsecond line'))

    def test_missing_null_and_malformed_metadata_fail_closed(self):
        pr, pages = metadata()
        invalid = [None, [], {}, pr | {'title': None}, pr | {'body': []}, pr | {'head': {}},
                   pr | {'user': {}}, pr | {'commits': True}, pr | {'commits': 0}]
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                check.validate(value, pages)
        pr['body'] = None
        self.assertEqual(check.validate(pr, pages), [])

    def test_incomplete_duplicate_and_raced_commit_lists_fail_closed(self):
        pr, pages = metadata()
        for bad in (None, [], [{}], [[{}]], [[pages[0][0], pages[0][0]]]):
            with self.subTest(pages=bad), self.assertRaises(ValueError):
                check.validate(pr, bad)
        with self.assertRaisesRegex(ValueError, 'head changed'):
            check.validate(pr, pages, B)
        changed = copy.deepcopy(pages)
        changed[0][0]['sha'] = B
        with self.assertRaisesRegex(ValueError, 'current PR head'):
            check.validate(pr, changed)
        pr['commits'] = 2
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            check.validate(pr, [pages[0] * 2])

    def test_cli_handles_success_failure_and_untrusted_text_without_echoing_it(self):
        with tempfile.TemporaryDirectory() as scratch:
            pr_path, pages_path = Path(scratch) / 'pr.json', Path(scratch) / 'commits.json'
            pr, pages = metadata()
            pages_path.write_text(json.dumps(pages))
            for title, expected in ((pr['title'], 0), ('::error::untrusted workflow command', 1)):
                pr['title'] = title
                pr_path.write_text(json.dumps(pr))
                result = subprocess.run([sys.executable, str(SCRIPT), str(pr_path), str(pages_path)],
                                        text=True, capture_output=True, timeout=5)
                self.assertEqual(result.returncode, expected)
                self.assertNotIn('::error::', result.stdout + result.stderr)
            pr_path.write_text('not json')
            result = subprocess.run([sys.executable, str(SCRIPT), str(pr_path), str(pages_path)],
                                    text=True, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn('not json', result.stderr)


if __name__ == '__main__':
    unittest.main()
