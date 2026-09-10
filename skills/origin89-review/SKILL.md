---
name: origin89-review
description: Review Origin89 code changes for demonstrated defects, compatibility, test coverage, and safety consequences. Use for requested code reviews and final implementation review; preserve whether the task asks for findings or fixes.
---

# Origin89 review

Adapted from Sentry's code-review and find-bugs skills for Origin89. See
[NOTICE.md](NOTICE.md) and [LICENSE](LICENSE) for upstream provenance and terms.

## Establish the review scope

Read the requested diff, including untracked or staged work when relevant. Verify
the comparison base instead of assuming a branch name. If output is truncated,
read the missing portions before drawing a conclusion. Inspect callers, contracts,
tests, and applicable repository instructions around the changed behavior.

A review request authorizes inspection and relevant checks. Make edits only when
fixing is part of the task. Do not commit, push, or post a review without that
authorization; preserve any authorization already given.

Verify the repository's `just check` reaches its required checks.
Node/TypeScript uses Biome alongside type checking, tests, and builds; Rust and
hardware retain their required checks. Do not treat a formatting pass as
behavioral verification.

## Follow the consequences

Trace inputs through validation, state changes, persistence, external calls, and
outputs. Prioritize hazards, authorization defects, data loss, runtime failures,
compatibility breaks, and unbounded resource use. Check rollback and recovery
when a change can partially succeed. Focus checks on the actual code and threat
model; do not attach a generic security checklist to every file.

For equipment control, inspect safe-state handling, stale or invalid readings,
command/feedback disagreement, reboot behavior, retries, and timing bounds. Use
the installed embedded skill or the repository's safety procedure when relevant.
For Rust, inspect ownership, panic paths, unsafe contracts, and synchronization.

Require 3–4 distinct behavioral paths for changed nontrivial functions, plus all
additional relevant branches. Check that assertions establish the contract and
would catch the suspected failure. Simple code may have fewer meaningful paths;
hazardous code can need many more. Look beyond test counts and coverage totals.

Before reporting a defect, verify its trigger and consequence, search for a guard
elsewhere, and inspect the existing tests. Distinguish demonstrated issues from
unverified concerns. Do not manufacture findings or block on personal style.

## Deliver actionable findings

Lead with findings ordered by consequence. For each, give the file and line,
trigger, effect, evidence, and a concrete correction. Name the checks actually
run and any missing environment or evidence. If nothing actionable was found,
say so with the review limits. Do not claim that a clean review proves safety.
