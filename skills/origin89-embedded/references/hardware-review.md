# Board and electrical review

Read the controlled schematic, PCB source, BOM, stackup, manufacturer constraints,
datasheets, reference manuals, and errata for the exact revision and components.
Keep each cited limit tied to a document revision and section. Report conflicting
requirements instead of choosing a convenient value.

Check the affected nets and their physical interfaces: pin mappings, footprints,
polarity, power sequencing, reset and boot states, voltage/current limits, return
paths, isolation boundaries, protection, and connector behavior. Include component
tolerances, dissipation, temperature, and environmental conditions where relevant.
Do not invent universal clearance, creepage, impedance, or derating values.

In `origin89-hardware`, use `tools/import_easyeda_export.py` to import new
EasyEDA exports into the board's archive without overwriting dated files. Run
`tools/validate_gerbers.py` with the exact board rules and export, and record
rule results in the revision table. Retain FreeCAD enclosure sources and the
documented Git LFS files.

Run the project's ERC and DRC with its reviewed rule set. Inspect relevant netlist,
BOM, stackup, and fabrication outputs against editable sources. Preserve reviewed
exceptions and explain any new waiver; do not suppress a check to hide a defect.

Verify protection and actuator behavior using the appropriate controlled bench
setup and acceptance limits. A visually plausible render or clean DRC does not
establish electrical or thermal safety. Track firmware pin configuration together
with board revision when one changes the other's behavior.

Keep editable CAD and provenance. Regenerate exports and ensure assembly and
fabrication files identify the reviewed revision. Report missing electrical,
thermal, environmental, or manufacturing evidence before release.
