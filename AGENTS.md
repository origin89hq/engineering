# Working in Origin89 engineering

Read `CONTRIBUTING.md` and `skills/origin89-working/SKILL.md`, then the relevant
skill and guide. Edit the local canonical skills directly; this repository does
not install its own published cache.

Keep common policy in the maintained guides and skills, templates in
`templates/`, and exact project commands in each project repo. Assess
maintenance cost before adding anything. Internal RFCs and research belong in
`origin89hq/internal-research`. Do not add checkout snapshots, stale status
records, or AI filler.

Run `just check` to test the refresh script offline and check links and JSON.
For changed workflows, render `$default-branch`, then run actionlint. Check
changed JSON, skill frontmatter, links, and required notices. Exercise
executable templates in a disposable consumer. See `docs/skill-validation.md`
for skill review scenarios.

Shared skill content refreshes at the next task in repositories that adopt the
bootstrap. Update installed scripts and workflows through PRs in each adopting
repo. Respect the current commit, push, and publication scope.

## Code Review Rules

Read `skills/origin89-review/SKILL.md` and the domain skills relevant to the diff.
This repository owns the canonical files; do not replace them with a published
cache during review.

- Bootstrap changes must preserve local skills and the verified snapshot on
  failure. Flag writes through redirected paths or partial activation after a
  detected conflict; legitimate managed links are intentional.
- Workflow templates must preserve request scope, bounded execution, and token
  permissions. Flag untrusted PR code gaining access to base-repository secrets
  or review-only work acquiring publication or equipment-operation effects.
- Verify that the adopting assistant can load the referenced instructions.
  A remote link or a developer's ignored cache alone does not establish that
  hosted reviews received the shared skills. Keep syntax checks distinct from
  evidence that a live reviewer followed a rule.
