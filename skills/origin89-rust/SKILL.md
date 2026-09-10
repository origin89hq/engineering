---
name: origin89-rust
description: Implement, refactor, debug, or review Rust in Origin89 repositories with explicit contracts, reliable errors, and targeted verification. Covers host Rust and no_std constraints; use the embedded skill as well for physical control or hardware work.
---

# Origin89 Rust

Read the local toolchain, workspace manifest, feature profiles, tests, and
instructions for the affected crate. Use the repository's exact commands and
preserve its MSRV, target, and allocation constraints. Verify current stable crate
versions and APIs before adding or upgrading dependencies; keep the lockfile.

Use `just` recipes when available; they run Cargo, rustfmt, Clippy, and local
target checks. Do not replace those checks with generic formatting tools.

## Implement the contract

- Use enums for states and outcomes, and distinct types for units or validated
  values when mixing them could cause defects. Make transitions exhaustive.
- Validate external input, lengths, numeric conversions, and arithmetic bounds.
  Return errors for expected failure. Preserve missing and stale states explicitly.
- Avoid `unwrap`, `expect`, unchecked indexing, and panics for fallible production
  input or I/O. Document any invariant assertion and its failure behavior.
- Preserve error context without logging secrets. Do not discard a `Result` or
  turn a failure into an optimistic default to continue execution.
- Keep ownership and lifetimes understandable. Use existing abstractions; avoid
  incidental clones, shared mutation, and generalization without real callers.
- Bound retries, queues, and waits. Define cancellation and shutdown. Do not hold
  a blocking lock across `.await`; justify an async lock that spans an await.

Keep strings at text boundaries. Use enums for states and commands, newtypes for
IDs and units, and structured errors instead of string comparisons. Avoid
`HashMap<String, Value>` as a domain model. Borrow `&str` when possible, use
`&'static str` for literals, and allocate `String` only for real ownership or
dynamic-text needs. Embedded text needs a bounded capacity and overflow behavior.
Parse once into validated types; do not repeatedly format and parse values.

When changing unsafe code, FFI, atomics, DMA, or shared mutable state, read
[the unsafe and concurrency checklist](references/unsafe-and-concurrency.md).
For firmware or physical control, also apply the installed embedded skill or
local safety procedure. A successful compile cannot establish hardware safety.

For controller domain/firmware code, preserve its stricter no-allocation and
no-production-panic rules, named capacities and defined behavior when full,
exhaustive matches without wildcard arms on owned enums, and `#[expect]` with a
reason instead of `#[allow]`. Keep operations that maintain a type's invariants
on that type and retain compile-fail type-state tests. Load the local Embassy,
behavior, protocol, and bench skills for those tasks; shared guidance must not
replace their exact commands and hardware evidence.

## Verify

Add a regression test for a bug and cover 3–4 distinct behavior paths for each
changed nontrivial function. Include invalid data, boundaries, and recovery where
applicable. Extend coverage for every relevant branch; do not pad trivial accessors.

Run focused tests, formatting, Clippy, and the required affected-workspace checks.
For a host-only workspace, the baseline is `cargo fmt --all -- --check`,
`cargo clippy --workspace --all-targets --locked -- -D warnings`, and
`cargo test --workspace --locked`. Mixed workspaces need their documented host
packages and embedded targets instead. Do not assume `--all-features` is valid.

Test public API examples and supported feature/MSRV combinations when affected.
Keep lint exceptions narrow and explained. Report exact commands and limits;
never describe tests, a verifier, or Rust itself as guaranteeing zero defects.
