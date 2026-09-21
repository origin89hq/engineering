# JEV requirement audit pilot

The pilot asks whether supplied tests support a stated requirement-coverage
claim. It prepares TypeSafe Choice requests and evaluates saved responses. It
has an explicitly invoked live runner for a small smoke test. It does not inspect
a live PR, execute source excerpts, post comments, or install a CI workflow.
Normal `just check` remains offline.

The first consumer is firmware requirement review. A source parser can establish
that a compiled test cites a requirement and contains an assertion. This pilot
tests whether a semantic judgment can help identify assertions that cover only
part of the cited obligation. Results are advisory, including `supported`.

## Prepare requests

Run from the engineering repository with Python 3.10 or newer:

```sh
python3 tools/jev_audit.py prepare \
  --cases tests/fixtures/jev-audit/cases.json \
  --model jev-1.13.0 > /tmp/jev-requests.json
```

The output contains one `body` per case, shaped for the
[TypeSafe API](https://docs.typesafe.ai/api), plus a case ID and request hash.
Only `body` belongs in a future API request. Expected labels, label rationales,
case kind, and review conclusions stay outside the request. Each body's hash
includes the question version, criteria, model, and evidence. Changed inputs
invalidate old recordings. Model aliases are refused.

Each case has `claim`, `requirement`, and evidence excerpts with source locations.
The tool only reads the supplied JSON; it never follows source URLs or opens
paths mentioned in excerpts. Requests have a 60,000-byte limit, at most 12
excerpts per case, and at most 64 cases per invocation. Oversized requests fail
without truncation. These are local byte bounds, not measured token counts or
a substitute for checking the provider's current context limits before live use.

## Run a live smoke test

Only run this command after approving the case evidence for transmission to
TypeSafe. The bundled cases contain pinned firmware excerpts and synthetic
controls. The separate runner uses the same request bodies as `prepare` and
sends no labels or review conclusions.

Store `TYPESAFE_API_KEY=value` in a private file outside the repository, such as
`~/.config/origin89/typesafe.env`, with permissions `600`. The runner reads this
as a single literal assignment; it does not execute shell syntax. Alternatively,
omit `--api-key-file` and supply `TYPESAFE_API_KEY` through the environment.

```sh
python3 tools/jev_audit_live.py \
  --cases tests/fixtures/jev-audit/cases.json \
  --model jev-1.13.0 \
  --api-key-file ~/.config/origin89/typesafe.env \
  --max-calls 6 \
  --output /tmp/jev-live.json
```

The output must not already exist. The runner creates it with mode `600`, saves
each completed attempt, and stops on the first service or invalid-answer failure.
There are at most six calls per invocation, no automatic retries, no redirects,
a fixed HTTPS endpoint, 20-second socket timeouts, and a 64,000-byte response
limit. Request bounds still apply. The call limit bounds usage, not a guaranteed
dollar amount; check provider pricing before running. A timeout may still incur
provider charges, which remain unknown without reported usage. Do not blindly
rerun a failed batch. An interrupted run can leave incomplete output; inspect it
before any further paid attempt.

Evaluate the recording using the command below. A smoke test can reveal concrete
failures; six related cases cannot establish general accuracy or savings.

## Evaluate a recording

A recording has this envelope. This example contains no model results:

```json
{"version": 1, "origin": "synthetic", "observations": []}
```

Every observation must contain an `id` from the prepared batch, its
`request_sha256`, and measured `elapsed_ms`. Include exactly one of:

- `response`: the original TypeSafe response containing `model`, `answers`, and
  `usage`. The answer key is `coverage`; the answer type is `choice`, with
  `choice`, `confidence`, and a complete `probabilities` distribution.
- `error`: a bounded description of the failed attempt, such as `timeout`.

Declare the recording's origin as `synthetic` for mocks or `live` for real calls.
The tool trusts this declaration; a JSON file cannot authenticate a provider run.
Never mix mocked and real answers in one recording. Each observation describes
one attempt. Cost estimates cover recorded response usage only, not omitted
retries, cached historical calls, or downstream review. Errors and missing usage
make the total cost unknown. Prices are supplied explicitly and never assumed.

```sh
python3 tools/jev_audit.py evaluate \
  --cases tests/fixtures/jev-audit/cases.json \
  --model jev-1.13.0 \
  --recording /path/to/recording.json \
  --threshold 0.8 > /tmp/jev-report.json
```

Replace the recording path. The threshold is an experimental example, not a
calibrated release policy. Optional `--input-price` and `--output-price` take
USD per million tokens; provide both after checking current pricing.

The report includes valid-answer accuracy, the correct fraction of all cases,
a confusion matrix, false gap flags, false reassurance, review workload (both flagged gaps and
uncertain/failed cases),
known usage, and recorded latency. Group summaries and a hash of the case
annotations preserve the comparison across related examples. Counts are also separated by review-derived
and synthetic case kind. Missing, stale, malformed, or failed answers
remain explicit rows requiring review. Live responses may round probabilities
to hundredths: the validator accepts a non-unit sum only when those rounding
intervals can contain one. It retains the raw values and flags the row as
`rounded_probabilities`; larger or unexplained discrepancies remain invalid. Low confidence and insufficient context
also require review. `no_gap_indicated` means only that this question raised no
gap; it never grants merge approval. Exit zero means the report was produced,
not that a PR passed. Savings remain unknown without a measured baseline.

## Seed examples and evaluation limits

The [case bundle](../tests/fixtures/jev-audit/cases.json) contains two cases
derived from [firmware PR #58's reviewed coverage correction](https://github.com/origin89hq/firmware/pull/58#discussion_r4057310354)
and four explicitly synthetic controls. Sources are exact excerpts from pinned
before/after commits. [Fixture provenance](../tests/fixtures/jev-audit/NOTICE.md)
explains how the labels were prepared and what they do not establish.

The original test has a reduced partition fixture and asserts flash-plan bounds.
The corrected production-table test reads the shipped CSV and asserts all six
partitions. That supports the narrower table-layout claim, while full F-036
coverage remains partial because the permanent recovery window is not tested.
Other controls cover a deliberately overstated claim, missing helper context,
an unrelated assertion, and a source comment that tries to dictate the answer.

The separate [expanded corpus](../tests/fixtures/jev-audit/expanded.json) adds
24 cases across four other PR groups; its provenance and pre-run screening
criteria are in the fixture notice. Keep these results separate from the original
six development cases. For live evaluation, prepare reviewed subsets of at most
six cases and run each subset explicitly; preserve IDs and recombine observations
against the unchanged complete case file for the final report.

All six original cases share one PR group. They are development examples, not an
independent benchmark. Labels were prepared from the review and correction;
they have not received a separate human labeling pass. Existing source comments
can reveal the author's coverage assessment, so a live evaluation must also
include cases where names or comments are misleading. Passing the synthetic
response tests establishes harness behavior only; it says nothing about Jev's
accuracy, prompt-injection resistance, cost savings, or hardware safety.

Before live evaluation, have a reviewer confirm the labels and add independently
reviewed PRs with both valid coverage and real gaps. Separate tuning and held-out
examples by PR group, keeping before/after variants together. Set acceptance
criteria before examining held-out results. Compare false reassurance, detection,
false alarms, abstention, reviewer time, latency, and total cost with the existing
review process. Live runs need authorization for source data, credentials, spend, and collection
of usage. The runner does not retry failures. CI adoption is a separate
step after these measurements; keep existing compiler, test, and review gates.

## Maintenance and checks

`tools/jev_audit.py` owns the question, criteria, response validation, and report.
Change `VERSION` when the question's meaning changes; request hashes also change
when its text or criteria change. Preserve existing pinned fixtures when adding
new cases rather than silently rewriting their historical evidence.

Run `just check`. The tests exercise preparation, source/label separation,
stale recordings, missing answers, uncertainty, invalid distributions, failure
reporting, cost uncertainty, bounded inputs, and the CLI in a disposable directory.
No credentials or paid calls are needed.
