#!/usr/bin/env python3
"""Check PR metadata without checking out or executing the contributor's code."""

import argparse
import json
from pathlib import Path
import re

SUBJECT = re.compile(r"(?:feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(?:\([^()\s]+\))?!?: \S.*")
SHA = re.compile(r"[0-9a-f]{40}")
ATTRIBUTION = re.compile(
    r"^\s*(?:[-*]\s+)?(?:co-authored-by\s*:|generated-by\s*:|"
    r"(?:🤖\s*)?(?:generated|written|created|assisted) (?:with|by) "
    r"(?:\[)?(?:claude|codex|chatgpt|copilot|openai|anthropic)\b)", re.IGNORECASE
)


def prose_lines(body):
    """Yield visible lines outside fenced examples and HTML comments."""
    fence = None
    comment = False
    for number, line in enumerate(body.splitlines(), 1):
        if fence:
            if re.fullmatch(re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*', line.strip()):
                fence = None
            yield number, ''
            continue
        visible = ''
        remaining = line
        while remaining:
            marker = '-->' if comment else '<!--'
            before, found, after = remaining.partition(marker)
            if not comment:
                visible += before
            if not found:
                break
            comment = not comment
            remaining = after
        stripped = visible.strip()
        opening = re.match(r'^(`{3,}|~{3,})', stripped)
        if opening:
            fence = opening[1]
            yield number, ''
            continue
        yield number, visible


def body_errors(body):
    errors = []
    previous = None
    in_list = False
    for number, line in prose_lines(body):
        stripped = line.strip()
        if ATTRIBUTION.match(line):
            errors.append(f'PR body line {number}: remove attribution')
        if not stripped:
            previous = None
            in_list = False
            continue
        if re.match(r'^\s*(?:[-+*]|\d+[.)])\s+', line):
            in_list = True
            previous = None
            continue
        structured = (
            in_list or line.startswith(('    ', '\t'))
            or re.match(r'^(?:#{1,6}\s|>|\[.+\]:\s|</?[A-Za-z][^>]*>$)', stripped)
            or re.match(r'^(?:[-*_]\s*){3,}$|^=+$', stripped)
            or '|' in stripped and (stripped.startswith('|') or stripped.endswith('|'))
        )
        if structured:
            previous = None
            continue
        if previous is not None:
            errors.append(f'PR body line {number}: join hard-wrapped prose into one line per paragraph')
        previous = None if line.endswith(('  ', '\\')) else number
    return errors


def subject_errors(subject, label):
    if (len(subject) > 72 or subject != subject.strip() or '\n' in subject
            or subject.endswith('.') or not SUBJECT.fullmatch(subject)):
        return [f'{label}: use a conventional subject of at most 72 characters, without a trailing period']
    return []


def validate(pr, pages, expected_head=None, branch_owner='lemarier', branch_prefix='david/'):
    """Validate complete REST API responses; malformed or raced snapshots fail closed."""
    if not isinstance(pr, dict) or not isinstance(pages, list):
        raise ValueError('Expected a PR object and paginated commit arrays')
    title, body = pr.get('title'), pr.get('body')
    head, user = pr.get('head'), pr.get('user')
    if (not isinstance(title, str) or body is not None and not isinstance(body, str)
            or not isinstance(head, dict) or not isinstance(user, dict)
            or not isinstance(head.get('ref'), str) or not isinstance(user.get('login'), str)
            or not isinstance(head.get('sha'), str) or not SHA.fullmatch(head['sha'])
            or type(pr.get('commits')) is not int or pr['commits'] < 1):
        raise ValueError('Missing or invalid PR metadata')
    if expected_head is not None and head['sha'] != expected_head:
        raise ValueError('PR head changed; run the check for the current head')
    if any(not isinstance(page, list) for page in pages):
        raise ValueError('Invalid commit page')
    commits = [commit for page in pages for commit in page]
    if len(commits) != pr['commits']:
        raise ValueError('Incomplete commit list or PR changed during the check')
    seen = set()
    for commit in commits:
        if (not isinstance(commit, dict) or not isinstance(commit.get('sha'), str)
                or not SHA.fullmatch(commit['sha']) or commit['sha'] in seen
                or not isinstance(commit.get('commit'), dict)
                or not isinstance(commit['commit'].get('message'), str)
                or not commit['commit']['message']):
            raise ValueError('Invalid or duplicate commit metadata')
        seen.add(commit['sha'])
    if commits[-1]['sha'] != head['sha']:
        raise ValueError('Commit list does not end at the current PR head')
    errors = subject_errors(title, 'PR title') + body_errors(body or '')
    if not branch_prefix or branch_prefix.isspace():
        raise ValueError('Branch prefix must not be empty')
    if user['login'].casefold() == branch_owner.casefold():
        if not head['ref'].startswith(branch_prefix) or head['ref'] == branch_prefix:
            errors.append('PR branch: use the configured owner prefix followed by the work description')
    for index, commit in enumerate(commits, 1):
        message = commit['commit']['message']
        errors += subject_errors(message.splitlines()[0], f'Commit {index}')
        if any(ATTRIBUTION.match(line) for line in message.splitlines()):
            errors.append(f'Commit {index}: remove attribution from the message')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pull_request', type=Path)
    parser.add_argument('commit_pages', type=Path)
    parser.add_argument('--expected-head')
    parser.add_argument('--branch-owner', default='lemarier')
    parser.add_argument('--branch-prefix', default='david/')
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.pull_request.read_text()), json.loads(args.commit_pages.read_text()),
                          args.expected_head, args.branch_owner, args.branch_prefix)
    except (OSError, json.JSONDecodeError) as error:
        # Do not echo untrusted metadata or JSON fragments into workflow commands.
        parser.exit(1, f'Contribution check could not validate metadata ({type(error).__name__}).\n')
    except ValueError as error:
        parser.exit(1, f'Contribution check: {error}\n')
    if errors:
        parser.exit(1, '\n'.join(errors) + '\n')
    print('PR title, commit messages, body formatting, and branch convention passed.')


if __name__ == '__main__':
    main()
