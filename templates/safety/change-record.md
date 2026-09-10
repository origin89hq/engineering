# Safety change record

Use for a change affecting potentially hazardous behavior. Replace the guidance
with evidence. This record does not certify the change.

## Scope and configuration

Record the change, board revision, equipment, firmware hash, target/toolchain,
power domains, control owner, and applicable requirements with document revisions.

## Hazards and verification

| Hazard and trigger | Required invariant and limits | Implementation | Test and stimulus | Observed result and evidence | Reviewer / status |
| --- | --- | --- | --- | --- | --- |
| Specify possible harm and conditions | Include units, timing, and safe output state | File/symbol/revision | Host, simulation, or bench procedure | Artifact, fixture, instruments, configuration | Responsible person and decision |

Cover normal operation, invalid/stale inputs, boundaries, restart/power loss,
disconnects, uncertain commands, actuator disagreement, resource limits, and
update/persistence failure where applicable. Explain exclusions and add the faults
specific to this equipment. Define safe states from the hazard; do not assume
that all outputs should be de-energized.

## Operations and recovery

Record bench isolation/protection, exact target, command effects, physical
interlocks, authorization, stop conditions, and recovery procedure. Keep these
separate from offline build and check commands.

## Release decision

List unresolved hazards and unperformed verification. Record the qualified
independent review and the evidence needed before deployment. If physical testing
was unavailable, keep it pending rather than describing a simulation as bench
validation. Link the final reviewed firmware and hardware artifacts.
