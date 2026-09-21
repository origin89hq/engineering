# TypeSafe skill provenance

The bundled [upstream skill](references/typesafe-ai/SKILL.md) and its
[license](references/typesafe-ai/LICENSE) come from
[typesafe-ai/skills](https://github.com/typesafe-ai/skills/tree/65a39f393687675ce170e6094757de20370365b9/skills/typesafe-ai),
revision `65a39f393687675ce170e6094757de20370365b9`, licensed under MIT.
Copyright (c) 2026 TypeSafe AI. Upstream files are preserved unchanged.
The Origin89 entrypoint and development guidance are also licensed under MIT.

Install or update using one method: in a disposable directory, run
`npx skills add typesafe-ai/skills --skill typesafe-ai --agent codex --copy --yes`.
Review the installed files and upstream revision, replace the bundled reference
folder and license together, and update this notice and the root
`skills-lock.json` from that installation. Preserve local Origin89 guidance.
Run `just check` before publishing the change. Do not run the installer through
the engineering discovery symlink, which points to the maintained reference.

Engineering exposes the bundled upstream skill through
`.agents/skills/typesafe-ai`. Adopting repositories receive `origin89-typesafe`
and its complete references through the existing shared bootstrap after the
engineering change is published. No bootstrap namespace change is needed.
