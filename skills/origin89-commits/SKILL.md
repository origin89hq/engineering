---
name: origin89-commits
description: Prepare or create Git commits in Origin89 repositories with short, specific messages and no attribution trailers. Use when drafting commit messages, organizing a requested commit, or committing reviewed changes.
---

# Origin89 commits

Adapted from Sentry's commit skill. See [NOTICE.md](NOTICE.md) and
[LICENSE](LICENSE) for upstream provenance and terms.

## Message rules

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

Apply the user's current scope: a request to draft a message or prepare a branch
does not authorize a commit or push. When a commit is already requested, proceed
within that scope without asking again. An instruction to keep work uncommitted
or unpushed remains in effect until the user changes it.

After a requested commit, confirm its message and the resulting working-tree
state. Push, amend, rebase, or rewrite history only when included in the task.
