# Rust standard

Use readable Rust with explicit contracts and errors. Memory safety alone does
not guarantee correct decisions, bounded execution, or correct device behavior.

## Toolchain and structure

Pin the verified toolchain in `rust-toolchain.toml`, declare `rust-version` for
the minimum supported compiler version, and keep workspace dependencies and
lockfiles consistent. New code uses the latest stable toolchain compatible with
its target; document exceptions under the
[dependency standard](dependencies.md).

Keep domain logic independent of transport and hardware where practical. Use
small modules with clear ownership. Prefer existing traits and concrete types;
introduce generic abstractions when they serve real callers or a test boundary.
Preserve `no_std`, allocation, feature, and target constraints.

## Types, errors, and state

- Represent states and outcomes with enums, and units or validated identifiers
  with distinct types where confusion could cause defects. Prefer exhaustive
  matches for closed state sets.
- Parse and validate external data once at the boundary. Check lengths, ranges,
  conversions, and arithmetic overflow. Make rounding and overflow behavior part
  of the contract; saturation is not an automatic solution for invalid readings.
- Return `Result` for expected failure and `Option` for genuine absence. Preserve
  useful context without exposing secrets. Do not discard errors or replace a
  missing measurement with zero.
- Do not use `unwrap`, `expect`, unchecked indexing, or panics to handle fallible
  production input or I/O. An invariant assertion needs a documented reason and
  tested failure behavior. In tests, `expect` can make fixture failure readable.
- Keep ownership clear. Avoid unnecessary clones and shared mutable state, but
  do not trade understandable code for lifetime tricks or premature optimization.

## Keep text at text boundaries

Do not use strings as domain state, error categories, identifiers, units, or
commands when Rust can express the contract. Parse external text once into enums,
newtypes, or validated values. Prefer structured errors over strings that callers
must inspect, and typed structs over `HashMap<String, Value>` property bags.

Use `&str` for borrowed text and `&'static str` for literals. Use owned `String`
only when text must be owned or constructed dynamically; explain non-obvious
ownership needs and avoid formatting just to compare or pass values around.
For embedded text, use a bounded representation with an explicit capacity and
overflow response when the protocol requires it. Choose an existing supported
type rather than adding a crate for a single convenience.

Text messages, user input, and external schemas still contain text. Preserve it
at those boundaries while keeping validated internal state typed. Do not replace
one opaque string with an equally opaque integer; give the value a domain meaning.

## Concurrency and unsafe code

Give tasks an owner, cancellation path, and shutdown behavior. Bound queues,
retries, and timeouts. Do not hold a blocking lock over `.await`. If an async
lock must span an await, explain the ordering and cancellation implications.
Review shared-state updates for races and partial updates.

Prefer safe APIs. Any required `unsafe` belongs in a small boundary with a
`SAFETY` explanation covering the invariants, lifetimes, aliasing, alignment,
synchronization, and target assumptions that apply. Document the caller
obligations of public unsafe APIs. Do not add unsafe `Send` or `Sync`
implementations to silence a compiler error without proving their contract.

Use Miri for supported unsafe code paths, Loom for modeled concurrency, and
property tests or fuzzing for broad inputs where they add evidence. A bounded
verification result applies only to its harness, assumptions, and bounds. Record
unsupported paths; do not describe tool output as a proof of the whole system.

## Origin89 controller constraints

For controller domain and firmware work, apply the stronger local rules: no
allocator in target domain code or its tests, named capacities with defined
behavior when full, no production `unwrap`/`expect`/`panic!`, checked indexing,
exhaustive matches on owned enums, and `#[expect(..., reason = "...")]` rather
than `#[allow]`. Put operations that maintain a type's invariants on that type.
Keep stateless functions free. Keep `///` on public items and `//!` on modules
concise, with reasoning in design docs instead of code banners.

Preserve type-state guards and compile-fail tests. Read the current repository
configuration for host and firmware workspaces and the specification gate. Test
committed protocol artifacts with independent generators; do not retype vector
bytes into a second source. Keep detailed design research in `internal-research`
and the maintained API or operational explanation with its consumers.

## Validation

Use the repository's `just` recipes as the normal entry point; they should call
rustfmt, Clippy, Cargo tests, and any local specification or target checks. Use
the repository's scripts or Cargo aliases first. For a host-only workspace, the
usual checks are:

```sh
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo test --workspace --locked
```

These commands are a host profile, not a universal embedded command. Mixed
workspaces must name the host-testable packages and target-specific build profiles.
Test supported feature combinations explicitly; do not enable `--all-features`
when features are mutually exclusive. Run doctests and MSRV checks when affected.
For firmware, also build the release image for the actual target and inspect its
memory and timing evidence under the [embedded standard](embedded.md).

Cover the [3–4 distinct behavior paths](testing.md) and all relevant extra branches.
Public APIs should document inputs, units, errors, and meaningful examples. New
lint suppressions must be narrow and explain a real constraint. Do not weaken
workspace checks to make a change pass.

Sources: [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/),
[Miri](https://github.com/rust-lang/miri), and
[Kani's verification model](https://model-checking.github.io/kani/).
