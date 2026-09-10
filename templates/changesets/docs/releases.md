# Releasing this repository

Follow the [Origin89 release standard](https://github.com/origin89hq/engineering/blob/main/docs/releases.md).

- Packages: list the packages published by this repository.
- Default branch: `main`; update this and `.changeset/config.json` if different.
- Workflow: `.github/workflows/origin89-release.yml`; npm's trusted publisher
  must match this filename.
- Validation: `pnpm check`; describe what it builds and verifies.
- Generated files: list tracked outputs regenerated after version changes.
- Extra release assets: list their names and recovery procedure, or state none.
- Exceptions: describe any deviations from the shared template, or state none.

Contributors run `pnpm changeset` and include the note in their PR.
Maintainers review and merge the generated release PR when ready to publish.
Run the check workflow on `changeset-release/<default-branch>` before merging
if the release PR was created using the default `GITHUB_TOKEN`.

Complete these repository details and the shared activation steps before
enabling publication.
