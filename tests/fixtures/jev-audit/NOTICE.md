# Firmware audit fixture provenance

Code and requirement excerpts in `cases.json` are from
[Origin89 firmware](https://github.com/origin89hq/firmware), licensed under
MIT OR Apache-2.0; these excerpts are redistributed under MIT.
Copyright (c) Origin89 contributors. See the repository's
[MIT license](../../../LICENSE-MIT).

Every real excerpt has a GitHub URL with its exact revision and line range:

- Before correction: `f662ddd4a2100c80bd2cce2136ac6b957f61aa75`.
- After correction: `62f13883184035d0e966a76bbe9c76064fa85c88`.
- Review: [F-036 coverage mismatch](https://github.com/origin89hq/firmware/pull/58#discussion_r4057310354).
- Correction: [test: correct partition coverage claims](https://github.com/origin89hq/firmware/commit/62f13883184035d0e966a76bbe9c76064fa85c88).

Claims and labels are pilot annotations based on that review, not verbatim
statements by the author or independently adjudicated ground truth. Two cases
are marked `review-derived`; four altered claims or invented tests are marked
`synthetic`. All belong to the same evaluation group and must stay in the same
dataset split. The full-coverage claim over the corrected test is intentionally
invented; the actual correction keeps F-036 uncovered.

No provider responses are bundled. Unit tests create explicitly synthetic
responses to exercise the evaluator, never to establish model performance.

## Expanded corpus

`expanded.json` adds 24 cases from four PR groups that were not in the original
smoke test. Eighteen cases derive from reviewed changes; six controls deliberately
omit test bodies or overstate host-test scope and are marked `synthetic`.

- [KM43 #43](https://github.com/origin89hq/km43/pull/43): paired tests for names,
  unallocated enum values, unknown event/metric keys, capability ranges, and
  retired metric units. The twelve cases share one PR and are not twelve
  independent changes.
- [Firmware #64](https://github.com/origin89hq/firmware/pull/64): the merged-fragment
  refusal test before and after its assertion fix, plus two controls.
- [Firmware #38](https://github.com/origin89hq/firmware/pull/38): the five-block
  regression test and its six-block correction, plus two controls. The author
  explicitly corrected the earlier mutation-testing claim; use the later review
  reply linked by each case. Historical mutation outcomes were not rerun here.
- [Firmware #54](https://github.com/origin89hq/firmware/pull/54): two narrowly scoped
  host state-machine tests for persistence and reset ordering, plus two controls.

KM43 excerpts are also MIT OR Apache-2.0, redistributed here under MIT with
Copyright (c) Origin89 contributors; the repository MIT license linked above
applies. Every excerpt retains its pinned revision and line range. Requirements
and claims may be annotated summaries of the linked contract; they are not
asserted to be verbatim author statements. Before/after variants retain the same
claim. Source comments remain intact and may disclose the author's assessment.

The question and criteria remain `requirement-coverage-v1`. Labels were prepared
before the expanded live run, without tuning the question on these results.
This is a held-out set of PR groups relative to the original smoke test, but not
an independently adjudicated benchmark. Report both case-kind and group results;
do not pool it with the six development cases to inflate the sample size.

Pre-run screening criteria at confidence threshold 0.8: zero confident false
reassurance, at least 80% correct `partial` choices among gap cases, at least 80%
correct `supported` choices among valid-coverage cases, and review escalation for
every missing-context control. These provisional criteria determine whether to
continue evaluating; they do not authorize CI activation. Include abstentions and
failed requests in denominators. Measure service latency and recorded API cost;
reviewer time and net savings remain unknown without a matched baseline. Do not
change labels after seeing predictions without recording a separate adjudication.
