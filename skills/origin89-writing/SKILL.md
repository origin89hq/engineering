---
name: origin89-writing
description: Write or edit all Origin89 AI-authored documentation, comments, commit messages, PRs, release notes, and conversation messages in clear, specific language without AI filler. Apply a quiet editing pass before delivery, including routine updates.
license: Apache-2.0
---

# Origin89 writing

Adapted from Sentry's blog-writing-guide for everyday Origin89 engineering prose.
See [NOTICE.md](NOTICE.md) and [LICENSE](LICENSE) for upstream provenance and terms.

Write for the reader's actual task. State the result or problem early, use concrete
words and direct verbs, and preserve the user's voice and technical meaning.
Edit before delivering any AI-written prose, including short progress messages.
Do not add an editing report unless the user requested editorial feedback.

Remove generic praise, marketing claims, theatrical openings, forced contrasts,
question-and-answer theatrics, repeated conclusions, and decorative formatting.
Cut stock phrases such as “delve,” “leverage,” “it's worth noting,” and “we're
excited to announce.” Replace vague adjectives with evidence or delete the claim.
Preserve literal quotes, API names, and precise technical terms.

Keep the length proportional to the task. Use headings, lists, and tables only
when they help readers find or compare information. Avoid repeating the same
sentence structure or turning every answer into a formal report. Preserve clear
house style, including lowercase after colons; capitalization alone is not AI
filler. Change punctuation when it improves clarity, not to enforce a blanket
formatting preference.

Check every claim against the evidence. Preserve uncertainty, prerequisites,
version context, and limitations. Do not invent measurements, sources, commands,
or user benefits. Distinguish prepared, tested, merged, published, and verified
on hardware. Never claim zero errors or certification from tests or AI review.

For engineering results, explain what changed, why, the checks actually run, and
material gaps. For PRs, describe the concrete problem and final behavior. For
release notes, describe the consumer effect. Commit messages use a short imperative
subject and no co-author or AI/tool attribution; keep upstream licenses in files.

Put internal RFCs, ADRs, research, and exploratory notes in `internal-research`.
Keep product documentation only when it helps a concrete task. Avoid checkout
hashes, copied inventories, and session reports in standing guidance; link the
source of truth and automate upkeep, or simplify. Keep required artifact and
license provenance in its established workflow.

Verify documentation commands and mark placeholders. Do not execute publishing
or hardware commands solely to check a writing example. End when the reader has
the result or next action; remove a closing paragraph that only repeats it.
