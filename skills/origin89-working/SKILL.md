---
name: origin89-working
description: Apply Origin89 working standards at the start of every repository task, including maintenance cost, documentation placement, workspace structure, tooling, tests, and authorization. Read this baseline before selecting domain skills.
---

# Origin89 working rules

Read the current repository instructions, relevant implementation, and callers.
Preserve unrelated work and stronger project constraints. Repository files own
exact commands, targets, pinouts, and versions; do not maintain snapshots of those
facts in shared guidance. Reconcile conflicting instructions during adoption.

Finish the authorized work. Before running a command, know what it checks and
what it can change. Choose the smallest useful command. Use focused commands
with short timeouts, usually 10–30 seconds. Diagnose a timeout before retrying.
Set a time limit for necessary longer jobs and report progress. Do not waste
time, hide failures, skip required checks, or claim work that did not happen.

Use `just --list` to discover commands. Node/TypeScript uses pnpm and Biome; Rust
uses Cargo, rustfmt, and Clippy. Verify latest stable dependencies when adding or
updating them, preserve compatibility constraints, and pin tools with lockfiles.
Keep publication, flashing, and equipment operation separate from ordinary checks.

For multi-package software, use `apps/` for deployable applications, `crates/`
for Rust code, and `packages/` for TypeScript libraries and shared UI. Use root
pnpm and Cargo workspaces. Preserve a separate MCU workspace where target
constraints require one. Reuse existing APIs and components across packages;
extract shared code when known callers need the same behavior. Do not create
empty folders or speculative libraries.

Use typed Rust state, errors, units, and identifiers. Avoid stringly typed domain
logic and unnecessary owned strings. Test at least 3–4 distinct paths for changed
nontrivial behavior, plus all relevant branches and faults. Keep trivial coverage
proportionate. Equipment changes require the actual target and safety evidence;
tests or language choice cannot establish zero defects.

Before adding code, dependencies, automation, configuration, or docs, identify its
value and maintenance cost. Prefer one source of truth and automate repeated
upkeep. If that is impractical, simplify or choose another approach. Keep a manual
record only when its value and update trigger are clear. Do not add recurring
checkout audits, version inventories, or status reports that will become stale.

Internal RFCs, ADRs, research, and exploratory notes belong in
[internal-research](https://github.com/origin89hq/internal-research). Product
repos keep useful maintained contributor, user, API, and operational docs. Do
not add agent transcripts, session reports, or documentation trees for ceremony.
Preserve required release, hardware, and upstream-license records where the repo
keeps that evidence.

## Track unfinished work

Every confirmed, actionable problem left outside the current fix must have an
issue in the owning repository. A chat note, TODO, or checked-in report is not
enough. Finish the authorized fix first; filing an issue does not excuse leaving
that work incomplete. Do not file speculative improvements or duplicate a defect
already being fixed in the current PR.

Use `gh` with an explicit `--repo owner/repo`, verified from the Git remote:

1. Search with `gh issue list --repo owner/repo --state all --search 'keywords'`.
   Read relevant matches with `gh issue view`. Link an existing open issue when
   it covers the same problem; inspect closed matches before treating it as new.
2. If no open issue covers it, create one:
   `gh issue create --repo owner/repo --title 'Specific problem' --body-file /path/to/issue.md`.
   Replace these example values. Give the trigger or reproduction, expected and
   actual behavior, impact, relevant code or PR links, and a concrete next step.
   Keep the body concise, with one
   physical line per paragraph and no assistant attribution.
3. Read back the created issue with `gh issue view` and include its URL in the
   handoff. One issue should cover one problem, not every symptom or mention.

Respect explicit read-only or no-posting instructions and private security
reporting rules. If issue creation is unavailable or outside the task's posting
authorization, provide a ready-to-file title and body, explain the blocker, and
state that nothing was filed. Do not change token permissions to bypass it.

## Apply the shared skills

Apply [writing](../origin89-writing/SKILL.md) to every document and message.
Remove AI filler and unsupported claims before delivery. Before creating a branch,
committing, pushing, or writing a PR, read [commits](../origin89-commits/SKILL.md):
`<name-or-nickname>/<what-you-are-working-on>` branches, short conventional commit
and PR titles, and no attribution. Preserve legal notices and Git identity.
Respect the task's commit, push, publish, and equipment authorization; do not ask
again for an action already authorized.

For stacked branches or dependent PRs, also read
[gh-stack](../origin89-gh-stack/SKILL.md). It covers layer placement,
non-interactive commands, and stack recovery within the current task scope.

Read the relevant sibling skill for [Rust](../origin89-rust/SKILL.md),
[TypeScript](../origin89-typescript/SKILL.md), [testing](../origin89-testing/SKILL.md),
[review](../origin89-review/SKILL.md), [embedded/hardware](../origin89-embedded/SKILL.md),
[Embassy](../origin89-embassy/SKILL.md), or [brand](../origin89-brand/SKILL.md).
Keep project-specific skills alongside these common rules.
