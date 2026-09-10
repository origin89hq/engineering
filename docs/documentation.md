# Documentation that earns its place

Keep documentation when it helps someone use, develop, operate, or maintain the
repository. Put setup and common commands in the README or contribution guide.
Use `docs/` for maintained material that needs its own page: a public API, a
troubleshooting guide, or an explanation of a difficult constraint.

Internal RFCs, ADRs, research comparisons, exploratory designs, and
investigation notes belong in
[internal-research](https://github.com/origin89hq/internal-research).
Contributors with access work there. Public contributors can propose changes in
an issue or PR; maintainers handle internal discussion in the private repo. Keep
the public explanation needed to understand and use the accepted behavior. Do
not expose private material to make a public link work.

Do not commit agent transcripts, session summaries, “research completed”
reports, or new `docs/` and `adr/` trees without a reader and a concrete use.
Report routine work and validation in the PR or task response. Keep hardware
test evidence and release provenance in the repository's existing evidence and
release records.

Before adding a document or recurring record, decide:

- Who uses it, and what decision or task does it help?
- Where does the authoritative information live?
- What changes would make this copy wrong, and how will those changes update it?

Prefer a direct link, a generated view, or a checked example to a second copy of
configuration. Do not maintain checkout hashes, inspection dates, current release
status, dependency inventories, or copies of another repo's command list in
standing guidance. Read the current configuration when doing the work. Preserve
revisions when they identify an actual release, artifact, measurement, or required
upstream attribution; produce that metadata automatically where possible.

Every addition has upkeep. Automate repeated checks and regeneration. If reliable
automation is impractical, simplify the design or use an existing source. Keep a
manual record only when its value justifies the work and its update trigger is
clear. Remove superseded material instead of adding another page that contradicts it.

Apply the [writing standard](writing.md) to all prose, including messages. AI
filler, invented evidence, and repetitive status language do not belong here.
