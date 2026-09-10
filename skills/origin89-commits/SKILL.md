---
name: origin89-commits
description: Prepare branches, commits, pushes, and pull requests in Origin89 repositories. Use before creating a branch, committing, pushing, or drafting or editing PR metadata; preserve the task authorization and use short messages without attribution.
---

# Origin89 branches, commits, and pull requests

Adapted from Sentry's commit skill. See [NOTICE.md](NOTICE.md) and
[LICENSE](LICENSE) for upstream provenance and terms.

## Branches and authorization

Name branches `<name-or-nickname>/<what-you-are-working-on>`, such as
`alex/batch-readings` or `sam/fix-release`. Use the contributor's established
prefix when known. Otherwise, suggest their name, username, or nickname as the
prefix. Follow an exact branch name when the user requests one. Put the kind of
change in the commit prefix.

Start independent work from the current remote default branch unless the task
selects another base. Preserve unrelated work with an isolated worktree when
needed. Before creating a branch, check its name and base. Do not silently
rename an existing published branch or replace an open PR to fix its name.

Preparing changes does not authorize a commit or push. Carry authorization
already given in the task forward, including later corrections, and keep any
instruction to leave work uncommitted or unpushed in force until changed.

## Commit and PR title rules

- Use a short, imperative subject that names the change. Aim for 50 characters;
  stay within 72. No trailing period.
- Use a familiar prefix such as `fix:`, `feat:`, `docs:`, `test:`,
  `refactor:`, or `chore:`. Add a scope only when it makes the subject clearer.
- Prefer a subject alone. Add a short body only to explain a reason or constraint
  that the diff and subject cannot convey. Put detailed validation in the PR.
- Never add attribution to the message: no `Co-authored-by`, generated-by
  trailers, assistant signatures, AI/tool credits, or similar footers.
- Use the configured Git author and signing settings. The message rule does not
  change authorship metadata or require rewriting existing commits.
- Use these same rules for the PR title: squash merges use it as the commit
  subject. Include `perf:`, `build:`, `ci:`, `style:`, or `revert:` where appropriate.
- Release bumps come from Changesets, not from the commit prefix.

Examples:

```text
fix: sync brand manifest version
feat: add Buddy scout pose
docs: add shared release guidance
```

## Preparing the commit

Read the status and diff, including anything already staged. Group changes
around one purpose and stage only the intended files or hunks. Preserve unrelated
work and existing staged changes. Run the repository's relevant checks and
inspect the staged diff before committing.

After a requested commit, confirm its message and the resulting working-tree
state. Push, amend, rebase, or rewrite history only when included in the task.

## Push and PR checks

Before pushing, inspect the commits ahead of the selected base and their full
messages, the diff, the destination remote, and the branch name. Push an explicit
branch ref. After a push, verify that the remote head and PR contain the commits
that were checked. A local pass is not evidence about an older remote head.
When an authorized rebase needs a force push, use a lease against the previously
observed remote head; never force-push the default branch.

Keep one result per PR. Describe the problem and resulting behavior, then the
checks actually run and any material compatibility or rollout constraint. A
small change usually needs one or two paragraphs plus validation. Summarize
covered paths; do not paste every test name, create a table full of `n/a`, or
recount the work session. Use a table only when it makes comparisons clearer.

Write each prose paragraph in a GitHub PR, issue, or comment on one physical
line. GitHub renders those newlines as visible breaks, so do not hard-wrap at
80 columns or copy README source wrapping into the body. Use blank lines between
paragraphs and preserve intentional Markdown lists, tables, and code blocks.
Commit body wrapping and repository Markdown formatting follow their own rules.

Pass multiline bodies through a file or structured API, then read back the
published title and body to verify their content. Keep AI/tool attribution out
of PR descriptions as well as commits. If a later commit changes behavior or
validation, update the PR around its final state.
