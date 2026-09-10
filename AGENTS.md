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
For changed workflows, render `$default-branch` and `$engineering-commit`, then
run actionlint. Check changed JSON, skill frontmatter, links, and required notices. Exercise
executable templates in a disposable consumer. See `docs/skill-validation.md`
for skill review scenarios.

Shared skill content refreshes at the next task in repositories that adopt the
bootstrap. Update installed scripts and workflows through PRs in each adopting
repo. Respect the current commit, push, and publication scope.
