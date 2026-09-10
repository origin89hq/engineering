# Writing standard

Apply this to every AI-written document, comment, commit message, PR description,
release note, and conversation message for Origin89. Edit before delivering it;
the reader does not need a report about the editing pass.

State the result or problem early. Use plain words, concrete nouns, and direct
verbs. Preserve the writer's voice and useful technical details. Choose a length
that answers the reader's question; do not pad a short answer into an essay.

## Remove filler and unsupported claims

- Remove generic praise, sales language, theatrical openings, rhetorical
  question-and-answer pairs, and repeated conclusions.
- Replace vague adjectives such as “robust,” “seamless,” and “industry-leading”
  with a mechanism or evidence. If there is no evidence, remove the claim.
- Cut stock phrases such as “it's worth noting,” “delve,” “leverage,” and
  “we're excited to announce” from original prose. Keep literal quotes, API names,
  and technical terms intact when their exact text matters.
- Avoid forced contrasts, dramatic fragments, decorative emphasis, and repeated
  sentence patterns. Use headings, lists, and tables when they help the reader.
- Preserve clear house style, including lowercase after a colon. Do not
  mechanically capitalize words or treat capitalization alone as AI filler.
- Keep uncertainty precise. Do not replace “tested on the simulator” with “safe,”
  or “prepared locally” with “released.” Never claim zero defects or certification
  from a code review, language choice, or passing test suite.

Do not invent measurements, quotations, commands, citations, or user benefits.
Link a primary source for externally sourced technical claims when useful.
Documentation commands need a working directory, prerequisites, and a clear
distinction between executable examples and placeholders. Check commands against
the repository; do not execute a hazardous example merely to verify its syntax.

## Keep documentation current

Follow the [documentation placement rules](documentation.md). Do not add research
reports, agent transcripts, checkout snapshots, or copied release/version status
to standing guidance. Link to the source of truth. A new page needs a reader, a
use, and a practical update path; automate repeated upkeep or simplify the material.

## Match the format

| Writing | Include |
| --- | --- |
| Progress message | What changed, what was learned, and the next useful step |
| Final engineering response | Result, relevant checks, and remaining limits |
| PR description | Concrete problem, resulting behavior, and validation |
| Commit message | Short imperative subject; body only for a necessary reason |
| Release note | What changes for consumers and any required migration |
| Technical guide | Task, prerequisites, verified steps, and failure behavior |

Commit messages never include co-author or AI/tool attribution. Preserve required
upstream license and copyright notices in source files; those serve a different
purpose from commit-message credits.

Before sending, remove any sentence that repeats the point without adding useful
information. Check that the remaining claims match the evidence and that a
colleague can understand the wording on the first read.
