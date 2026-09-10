# Integrating the Origin89 brand package

Use `@origin89/brand` for identity assets and semantic colors in Origin89
product interfaces, websites, docs sites, and branded exports. Do not maintain
independent copies of the palette, redraw logos, reconstruct the wordmark with a
font, or generate replacement Buddy artwork in a consumer repo. Repositories
without a branded interface do not need a runtime dependency.

The package contains tokens, fonts, logos, icons, artwork, and a JSON manifest.
It does not export React, Astro, or other UI components. Each application owns
its layout and accessible components while using the shared assets and tokens.

## Select and install a release

From the workspace that will use the package, check the published releases:

```sh
pnpm view @origin89/brand dist-tags --json
```

Select the latest stable published version, inspect its changelog and exports,
then install it with `pnpm add -E @origin89/brand@<verified-version>`. Replace the
placeholder before running. In a monorepo, add it to the packages that import it.
Commit the manifest and pnpm lockfile. A local brand version, Git tag, or prepared
release PR is not evidence that the same version can be installed from npm.

Use an explicit dependency for code that imports brand. Build-only integrations
can use a dev dependency if deployment builds install it. Production builds must
resolve a released package from the lockfile, not a sibling checkout, branch URL,
floating CDN endpoint, or runtime `latest` lookup.

## Import the public exports

Import the plain token sheet once through the application's global CSS entry.
This example requires a CSS bundler that resolves package imports:

```css
@import "@origin89/brand/tokens/themes.css";

body {
  background: var(--color-page);
  color: var(--color-fg);
}

a { color: var(--color-link); }
```

For Tailwind projects supporting `@theme`, use the package's
`@origin89/brand/tokens/tailwind.css` export with the framework's normal import
order. Add `themes.css` when supporting OS preference or explicit theme switching.
The Tailwind sheet alone contains dark values. Test explicit `data-theme="light"`
and `data-theme="dark"` on the root element as well as OS preference when enabled.

Use the manifest to discover available assets and typography. In a compatible
Node ESM build script:

```js
import brand from "@origin89/brand" with { type: "json" };

console.log(brand.version, brand.logos.primarySymbol);
```

Browser frameworks may use their own JSON-import handling. Use the asset URL
mechanism provided by that framework; an npm package specifier is not a browser
URL. Supported asset exports include `@origin89/brand/logos/*`, `icons/*`,
`fonts/*`, and `art/*`. For example, the package contains
`logos/origin89-horizontal-blue.svg` and `fonts/InterTight-600.ttf`.
Check the installed manifest before selecting a Buddy pose or file name.

The equipment-scout artwork belongs in brand's editable scene and release
pipeline. A consumer may use `art/buddy-equipment-scout-transparent.webp` only
when its installed release includes that file. Do not fetch the scene from an
unpublished checkout during a production build.

Verify that the production build retains the brand styles. If styles are
missing, inspect the installed package's `sideEffects` metadata and the
bundler's CSS handling.

## Use the identity consistently

Use semantic roles such as `--color-action`, `--color-on-fill`, `--color-link`,
`--color-focus`, and the surface/text tokens. Map a framework's theme variables
to these tokens instead of copying their hex values. Keep product-specific
layout and spacing local. Request new shared roles in brand when needed.

Use the outlined logo files and a variant suitable for its background. Preserve
aspect ratio and artwork. Load the font families, weights, and files listed in
`brand.typography`; retain their OFL license files when redistributing fonts.
Do not use the wordmark font as a substitute for the provided logo artwork.

Choose a Buddy pose that matches the task, stays legible at its displayed size,
and has appropriate alt text. Hide decorative artwork from assistive technology.
New poses, logo variants, and shared palette changes go through the brand
repository with editable sources, regenerated assets, verification, and a
Changeset.

Keep status meaning accessible: alarms, estimated values, stale readings, and
missing data need text, shape, or another non-color cue. Preserve freshness and
units. A missing measurement must not become zero. Test focus and contrast in the
actual composition; token checks alone do not validate a finished interface.

## Static sites, native apps, and generated documents

If a consumer cannot bundle npm assets, add a reproducible build step that reads
the installed package and copies or converts an explicit set of manifest-listed
files. Record package version, source path, and source SHA-256 from `brand.files`.
For conversions, also record the conversion command/settings and output hash.
Carry applicable font and asset terms into distribution. Do not hand-edit outputs.

Make regeneration part of the consumer's documented build/check process and fail
when required files are missing or copies have drifted. Native apps and firmware
displays may compile tokens/assets into their own format through this build step;
they do not need Node or npm at runtime.

## Verify and update

Before merging an integration or upgrade, run a production build and check asset
resolution, fonts, supported themes, keyboard focus, responsive layouts, and
relevant status states. Check the built output for missing CSS or URLs. For copied
assets, verify provenance and regeneration. Keep package upgrades in reviewable PRs
and include screenshots when appearance changes.

The package's marks and artwork have different terms from its tokens and fonts.
Preserve the package license and applicable notices; installing it does not grant
unlimited rights to brand a third-party product as Origin89.

Sources: [brand package and usage](https://github.com/origin89hq/brand),
[public exports](https://github.com/origin89hq/brand/blob/main/package.json), and
[package terms](https://github.com/origin89hq/brand/blob/main/LICENSE.md).
