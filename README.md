# f1r3lang.ai — website

Marketing/documentation site for **f1r3lang** (formerly Rholang), the concurrent smart contract language of the F1R3FLY execution layer.

Static HTML/CSS/JS — no build step, same stack as f1r3fly.io.

## Structure

```
index.html          Home — SELECT-FROM-WHERE-DO hook, pillars, AI, lineage
language.html       Developer tour: the door, writes, SQL translation table,
                    witnessed transactions, core model, execution, what's new
get-started.html    Docker node, first contract, docs links
research.html       The research program: language definitions (three rungs),
                    generated conditions, graded where-clauses, honest status
ecosystem.html      Node, interpreter, editors, LSP, community
css/styles.css      All styles; brand tokens in :root
js/main.js          Mobile nav + scroll reveal
images/             Logo SVGs
```

## Positioning note (2026-08-27, per Greg's paper)

Site content is based on "MeTTaIL for the Working Software Developer" (L.G. Meredith,
Aug 2026). **"MeTTaIL" is an internal code name and does not appear in site copy** —
it is described as "the language definition block / toolchain." The name is visible
only where GitHub repo paths are linked (mettail-rust), which are public artifacts.
f1r3lang is the overarching public name. The quantum reading is deliberately fenced
("a fenced fragment," not "a quantum language") — keep that honesty if editing.

## Brand status

Logo: `images/f1r3lang-logo-v1.svg` (f1r3lang brand v1, 08.27.2026 — more options in progress).
Palette: F1R3FLY system — Brand Yellow `#F3D630`, Brand Sky `#3FA9F5`, rule gradient Yellow→Sky, primary button uses the developer gradient `#007BC4 → #009188` from f1r3fly.io.
Foundation: background `#0A0A0A`, Josefin Sans + Source Sans 3, JetBrains Mono for code.
The old Rholang logo SVGs remain in `images/` for reference and can be deleted.

To iterate the brand: swap the logo SVG and the token values at the top of `css/styles.css` (`--accent`, `--accent-2`, `--rule-gradient`). Nothing else should need to change.

A light-background version is planned; dark is the primary.

© F1R3FLY Industries, 2026
