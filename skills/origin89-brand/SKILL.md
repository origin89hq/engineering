---
name: origin89-brand
description: Integrate or update the Origin89 brand package in product interfaces, websites, documentation sites, native apps, and branded exports. Use shared tokens, fonts, logos, and Buddy assets with versioned provenance; create new identity assets in the brand repository.
license: MIT OR Apache-2.0
---

# Origin89 brand integration

Inspect the consumer's framework, dependency, lockfile, global styles, and asset
pipeline. Check the installed `@origin89/brand` manifest and public exports.
Verify the latest published stable version before adding or upgrading it with
pnpm and an exact version. A local version or Git tag may still be unpublished.

Use shared semantic tokens, fonts, logos, icons, and Buddy artwork. Do not redraw
the identity, copy hex values into a second palette, or recreate the wordmark
with text. The package provides assets and tokens, not application components.
Keep layout and accessible component behavior in the consuming app.

Load `@origin89/brand/tokens/themes.css` through the framework's global CSS entry.
For compatible Tailwind setups, use its `tokens/tailwind.css` export and add the
theme sheet for light/dark switching. Check CSS retention in production builds.
If styles are missing, inspect the installed package's `sideEffects` metadata and
the bundler's CSS handling. Map framework theme roles to brand variables and test
supported themes and focus states.

Select logos, artwork, and font files from the installed manifest. Use the
framework's asset-URL mechanism rather than a raw npm specifier in browser markup.
Preserve aspect ratios, font licenses, and brand-use terms. Give informative
images useful alt text and hide decorative images from assistive technology.
Never assume a pose from the brand checkout is available in the installed package.

For consumers unable to bundle npm assets, use a deterministic build step with
an explicit manifest-based allowlist. Record package version, source path/hash,
and conversion settings/output hashes where relevant. Verify regenerated outputs;
do not hand-edit copied assets or add a Node dependency to firmware runtime.

New shared tokens, logos, or Buddy poses belong in the brand repository with
editable sources, generated outputs, validation, and a Changeset. Consumer
production builds must use released packages rather than unpublished branches.

Validate a production build, asset URLs, fonts, responsive layouts, supported
themes, keyboard focus, contrast, and status meaning. Alarms and data-quality
states need a non-color cue; missing readings must not become zero. Report the
package version used and any unavailable release or unperformed visual check.
