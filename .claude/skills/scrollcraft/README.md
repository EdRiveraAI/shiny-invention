# scrollcraft

A Claude Code skill that builds premium, scroll-driven interactive landing
pages, and holds them to a real design standard. Scroll becomes the timeline:
video scrubs frame by frame under the wheel, sections pin while their argument
advances, rails pan sideways, headlines assemble line by line, and the page
verifies its own contrast, motion and accessibility by screenshotting itself.

Vendored from <https://github.com/nateherkai/scroll-craft> (MIT, © Nate Herk).
Upstream ships it as the `nateherk-design` plugin; here it lives as a plain
project skill under `.claude/skills/`, so it loads with no plugin install.

## What it does

- **Interviews the human first** — vibe, journey, energy curve, owned assets —
  before generating anything.
- **Picks one of eight mutually exclusive page grammars** (filmic one-shot,
  chaptered editorial, live surface, continuous world, typographic poster,
  gallery, split stage, rhythmic cutlist) plus one bespoke signature move, so
  two builds cannot quietly converge.
- **Enforces a fingerprint gate** — a new build must differ from every page in
  your registry on at least 4 of 6 dimensions.
- **Builds on a design floor** — typography, spacing scale, six colour roles,
  five depth tools, motion — not on an animation library.
- **Generates assets** through kie.ai, or builds entirely from footage and
  photos you already own.
- **Verifies its own work** with a headless browser pass that reports dead
  scroll, cues that never reach full opacity, per-line contrast measured on the
  composited page, and clips that silently failed to decode.

## Prerequisites

| Requirement | Why | Notes |
| --- | --- | --- |
| **Node 18+** | every script | |
| **A full ffmpeg build** | encoding clips so they scrub rather than play | Stripped ffmpeg builds lack `scale`; `SCROLLCRAFT_FFMPEG` overrides the search |
| **`playwright-core` + Chrome** | the verification pass | `npm i playwright-core` **in the build folder**; `SCROLLCRAFT_CHROME` overrides |
| **`KIE_AI_API_KEY`** | only to *generate* assets | Optional — see `.env.example`. Bring-your-own-assets builds need no key and no spend |

## First run

```bash
node .claude/skills/scrollcraft/scripts/doctor.mjs              # preflight: says exactly what is missing
node .claude/skills/scrollcraft/scripts/workspace.mjs --ensure  # creates the workspace and an empty registry
```

Run `doctor` first. The common setup faults (stripped ffmpeg, missing WebP
muxer, `playwright-core` resolving from the wrong directory) all surface later
as misleading errors otherwise.

## Workspace

Builds and the fingerprint registry live in one directory, resolved in this
order — first hit wins:

1. `SCROLLCRAFT_HOME`
2. the nearest `.scrollcraft.json` walking up from the current directory:
   `{ "workspace": "path/to/builds" }`
3. `<project root>/scrollcraft`

Builds land in `<workspace>/builds/<name>/`; the registry is
`<workspace>/FINGERPRINTS.md`, seeded from `templates/FINGERPRINTS.md`. It
starts empty, and that is correct — the gate exists to stop you repeating
yourself. `EXAMPLES.md` is the author's twelve-row table, included as
illustration of a filled registry, not as constraint.

## Layout

```
SKILL.md            the procedure: interview, grammar, score, build, verify
references/
  uniqueness.md     eight page grammars, the signature move, the fingerprint gate
  feel.md           the feeling curve, the engineered peak, the feel check
  devices.md        nine scroll devices and the cue contract
  worldflight.md    continuous-world mode: one fixed stage, no seams
  worlds.md         art direction, and the style-preamble method
  taste.md          the design floor: spacing, type, colour, depth, motion
  assets.md         generation, camera moves, encoding for scrubbing
  verify.md         the harness, and what it cannot tell you
  template.html     a starting skeleton, not a layout
engine/             scrollcraft.js + .css — the mechanism, never edited per project
templates/          the empty registry a new workspace is seeded from
scripts/            doctor · workspace · kie · encode · serve · shoot · worldflight-assert
```

`CHANGELOG.md` records what broke on each build and the rule that came out of
it, rather than a feature list.

## The one rule that matters most

The engine is the mechanism and it is **never edited per project**. Theme it
with six colour tokens and two fonts, write your own semantic HTML, and drive
anything bespoke off the `--sc-p` custom property the engine publishes.

## Known limitations (upstream)

- Only ever run on Windows. The scripts search Windows, macOS and Linux
  locations for ffmpeg and Chrome, but no build has been done on a Mac.
- Generated video is a real spend; a ten-leg continuous-world flight is the
  expensive case. Building from your own assets costs nothing.
- It is opinionated on purpose, and will refuse the layouts and palettes that
  make AI pages recognisable.

## Licence

MIT — see [LICENSE](LICENSE). Demo captures of the three reference builds are
in the [upstream README](https://github.com/nateherkai/scroll-craft).
