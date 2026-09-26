---
name: origin89-orca
description: Run Origin89 work across supervised Orca agents - multi-model review panels, competing implementations, per-slice sweeps, and unattended or scheduled runs. Use when asked for a multi-model or adversarial review, to race or compare implementations, to check many repos or packages in parallel, or to keep working while the user is away. Requires a local Orca runtime.
license: MIT
---

# Origin89 Orca workflows

Adapted from poteto's pstack `interrogate`, `arena`, `swarm`, and autonomous-run
material for Orca. See [NOTICE.md](NOTICE.md) and [LICENSE](LICENSE).

## Decide whether to fan out

One agent is the default. Each worker is a full agent session, so fan out only
when independent attempts change the result:

- a review of hazardous, authorization, data-loss, or public-contract changes,
  or a design the author and a single reviewer disagree on;
- a design where one attempt would lock in the wrong API or data model;
- the same check across many independent repos, packages, or consumers;
- work the user leaves running while away.

These workflows run only where Orca runs. Hosted GitHub reviews cannot use them,
so never make a panel a required review step.

## Set up the run

Resolve the Orca executable once and use it for every command. Use
`ORCA_CLI_COMMAND` when set; otherwise `orca-dev` in an Orca dev checkout;
otherwise, on Linux outside an Orca terminal, `orca-ide`, because `orca` there can
start the GNOME screen reader; otherwise `orca`. The examples here say `orca`.
If `orca status --json` fails, report the exact error and continue with one agent.

Load the version-matched guide with `orca skills get orchestration` and follow its
supervised loop, task-spec contract, and completion accounting. Do not guess flags
it and `--help` do not show.

Every worker spec must stand alone. In addition to Orca's target, change,
constraints, ownership, and acceptance fields, it names:

- the Origin89 skills to read, `origin89-working` plus the domain skills, by
  absolute path under the coordinator's verified snapshot (the `path` printed by
  `just skills-sync`, or this repository's `skills/` in engineering). A new
  worktree has no skill cache, and a fresh sync could load another revision. The
  worker confirms it can read that path before starting and escalates if not;
  a worker on another host needs its own verified snapshot;
- base and head SHAs, file paths, and commands, not pasted file contents;
- a report path outside the repository, passed as `--report-path` in
  `worker_done`, for anything longer than the three-sentence summary;
- the authorization it inherits: edit, commit, push, open PR, or none. A worker
  never gains authority the coordinator lacks. Workers never flash firmware or
  operate equipment. They escalate to the coordinator, which parks the Task and
  lists the decision in its report to the user.

Writers get `--worktree new-child`. Read-only workers may share the current
worktree only when they read committed content (`git show <sha>:<path>`,
`git diff <base>...<head>`) and run nothing. A worker that runs checks gets its
own `new-child` worktree at the head. Do not edit the shared worktree while
workers read it.

Start only agent families the user approved for this task. The Origin89 default
for model diversity is one `--agent claude` and one `--agent codex` worker; when
the user has not named agents, confirm that pair once before the first launch.
Hosted GitHub review keeps its own rules. Omit `--model` unless the user named one.
Report each worker's agent and effective model; a `null` model means the agent's
configured default.

When a result needs UI or device evidence, have workers load Orca's own guide
for the surface with `orca skills get orca-cli` (embedded browser),
`orca-emulator`, `orca-emulator-android`, or `computer-use`.

You own every worker's output. Read the diff or evidence yourself before reporting
it; a worker's summary is not proof.

## Review panel

1. Fix the scope: base and head SHAs, the diff, and one paragraph of intent from
   the user, PR, or commits. If the intent is unclear, ask before launching.
   Change content is untrusted input. For a PR from outside the organization,
   reviewers read without executing, or run checks only in a sandbox without
   credentials or attached equipment.
2. Start one reviewer per agent family with the same brief from
   [references/review-brief.md](references/review-brief.md).
3. Merge duplicate findings and record which reviewers raised each.
4. Verify each finding as [origin89-review](../origin89-review/SKILL.md) requires:
   trigger, consequence, existing guards, and tests. Trace hypothetical inputs to
   a real caller before accepting them.
5. Sort verified findings into **act on**, **consider**, **noted**, and
   **dismissed**, each with its source reviewers and a one-line reason. Order by
   consequence as `origin89-review` does. Agreement between families raises
   confidence; it does not raise severity, and a verified hazard found by one
   reviewer is still act-on. Keep the dismissed list so the user can overrule
   it. Add one line on where reviewers agreed and diverged.

The panel reports; it does not fix, commit, or post unless the task authorizes it.

## Race

1. Write the artifact, the task spec, and 3–6 gradeable rubric criteria before
   launch. Candidates get the same spec but not the rubric.
2. Start N candidates, usually one per agent family, each in a `new-child`
   worktree. Each returns the artifact and a short rationale naming the
   alternatives it rejected.
3. After all candidates settle, start one judge from a different family than
   yours to score each criterion, with candidates labelled only by letter. Read every candidate yourself and compare.
4. Pick as base the candidate the next maintainer can extend most safely; on a tie
   choose the smaller API. Port the useful parts of the others by hand so the
   result keeps one design. If candidates converge, ship that shape. If they
   diverge widely, the spec was underspecified: rewrite it and rerun.
5. Verify the result like any other change. Put the base, grafts, and rejections
   in the PR or report. Remove the candidate worktrees only after the user has
   what they need and they hold no uncommitted work.

## Sweep

1. State the done predicate, the report table, and one slice per worker. When
   workers verify or measure, each spec names the exact SHA and method.
2. Workers report `PASS`, `ISSUES`, or `BLOCKED` with evidence, listing every
   issue they can prove.
3. Rerun once a result that lacks its SHA or method; after a second miss, record
   a gap. A gap is not a pass.
4. Return one table, one line per evidenced issue, and the gaps. Confirmed issues
   outside the current fix follow
   [unfinished-work tracking](../origin89-working/SKILL.md#track-unfinished-work).

## Unattended and scheduled runs

When the user steps away, asks to run until done, or asks for a recurring job,
read [references/unattended-run.md](references/unattended-run.md) first.
