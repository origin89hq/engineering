# Unsafe and concurrency review

Load this for unsafe code, FFI, atomics, interrupts, DMA, or shared mutable state.

For each unsafe boundary, identify who establishes and preserves pointer validity,
alignment, initialization, ownership, aliasing, and lifetime requirements. Document
the applicable facts in a `SAFETY` comment instead of a bare “this is safe.”
Document caller obligations for public unsafe functions. Prefer an existing safe
abstraction and keep the unsafe region small.

For concurrency, name the owner of each mutable value and the permitted event
orderings. Check lock ordering, re-entrancy, cancellation between state updates,
task shutdown, queue capacity, and backpressure. Explain the synchronization
relationship required by atomics; do not choose an ordering by habit.

For interrupt and DMA paths, verify the MCU's atomic support, interrupt priorities,
critical-section behavior, buffer ownership, alignment, cache coherency, and memory
barriers against the relevant target documentation. A desktop test does not model
all peripheral behavior. Do not invent unsafe `Send` or `Sync` guarantees.

Use supported Miri runs to look for undefined behavior in exercised paths, Loom
to explore modeled interleavings, and a bounded verifier such as Kani when a small
critical invariant is suitable. Record harness assumptions, bounds, unsupported
operations, and tool versions. Do not equate a bounded result with whole-program
or hardware correctness.

Sources: [Rustonomicon](https://doc.rust-lang.org/nomicon/),
[Miri](https://github.com/rust-lang/miri),
[Loom](https://github.com/tokio-rs/loom), and
[Kani](https://model-checking.github.io/kani/).
