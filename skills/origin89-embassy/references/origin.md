# Project firmware references

Read the consuming repository's current contribution guide and firmware skills.
Keep exact commands, targets, linker limits, pinouts, and measured peripheral
configurations in that repository. Do not duplicate checkout revisions or
configuration inventories in this shared skill.

For the Origin89 controller, consult `.claude/skills/embassy-firmware/references/`
and the applicable behavior, protocol, fault-injection, and bench skills. Preserve
those local workflows during shared-skill adoption. Inspect the current directory
and configuration when paths or tools change.

An unfilled peripheral reference is not a tested recipe. If setup prose disagrees
with manifests, linker scripts, or bench evidence, reconcile the version and target
before using it. Select the actual linker region when measuring flash and RAM;
chip capacity is not necessarily the application budget.

Primary references: [Embassy book](https://embassy.dev/book/) and
[Embassy timeout behavior](https://docs.embassy.dev/embassy-time/git/default/fn.with_timeout.html).
Select documentation matching the pinned crate version before implementation.
