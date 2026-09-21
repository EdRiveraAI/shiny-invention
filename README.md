# 🔤 ABC Fun Factory

A fun, colorful **A–Z alphabet worksheet generator** for the preschool niche.
Pick your letters, pick a design from the drop-down menus, and print — no
accounts, no build step, no dependencies.

Open `index.html` in any modern browser and you're generating worksheets.

---

## What it makes

Nine worksheet styles, all driven by drop-down menus:

| Style | What lands on the page |
| --- | --- |
| ✏️ **Trace & Write** | Guided tracing rows plus free-practice space, with picture words |
| 🌈 **Rainbow Trace** | One giant hollow letter to trace once in every crayon color |
| 🎨 **Color the Big Letter** | Huge bubble letter framed by themed doodles to color |
| 🔵 **Do-A-Dot Letter** | The letter drawn as open circles for dot markers, stickers or fingerprints |
| 🔢 **Dot-to-Dot Letter** | Numbered dots that build the letter — counting and letter shape in one |
| 🔍 **Find & Circle** | A grid of look-alike letters to hunt through |
| 🔊 **Beginning Sounds** | Six big picture cards; circle the ones starting with the letter |
| ⭐ **All-In-One Practice** | Trace, find, color and say the words on a single page |
| 🖼️ **Letter Poster** | Big display letter with picture words, for the wall |

## The drop-down menus

| Menu | Options |
| --- | --- |
| **Worksheet style** | The nine designs above |
| **Color theme** | Jungle Safari · Under the Sea · Outer Space · Farm Friends · Dino Days · Candy Rainbow · Woodland Forest · Fairy Tale |
| **Letter case** | Both (Aa) · Uppercase only · Lowercase only |
| **Letter font** | School Print · Rounded Bubble · Comic Fun · Handwriting · Chunky Block |
| **Tracing style** | Dotted · Dashed · Hollow outline · Light gray · Stroke-order arrows |
| **Writing guide lines** | Three-line handwriting · Three-line + descender · Single baseline · Letter boxes · No lines |
| **Page border** | Confetti dots · Theme doodles · Scalloped frame · Candy stripe · Simple line · None |
| **Practice rows** | 2 (easy) · 4 (standard) · 6 (lots of practice) |
| **Paper size** | US Letter · A4 |

Plus a custom page title, a custom footer message, and switches for full
color / ink-saver black & white, the name & date line, the footer, and the
picture words.

## Using it

1. Open `index.html`.
2. Tap letters in the picker (or **All A–Z**, **Vowels**, **Consonants**, **A–J**).
   Every selected letter becomes its own page.
3. Choose a design from the drop-downs — the preview updates as you go.
4. **🎲 Shuffle** re-rolls the randomized parts (letter-hunt grids, beginning-sound
   pictures, doodle placement). Pressing <kbd>R</kbd> does the same.
5. **🖨️ Print / Save PDF** — one worksheet per page. In the print dialog set
   margins to *None* and turn on *Background graphics* for full color.

Your settings are remembered in the browser between visits.

## How it works

Plain HTML, CSS and JavaScript — no framework, no bundler, no network calls
beyond the optional Google Fonts link (it falls back to system fonts offline).

```
index.html            page shell and the control panel
assets/css/styles.css app chrome, worksheet layout, print rules
assets/js/data.js     letter skeletons, themes, picture words, fonts
assets/js/render.js   the worksheet renderer (SVG builders)
assets/js/app.js      state, drop-down wiring, preview, print
```

A few details worth knowing if you extend it:

- **Letter skeletons.** `UPPER_STROKES` / `LOWER_STROKES` hold a single-stroke
  school alphabet as SVG paths in a shared 100 × 170 box (ascender 15,
  x-height 55, baseline 125, descender 160). These drive the do-a-dot,
  dot-to-dot and stroke-order-arrow pages. Dots are sampled along the paths at
  print time and de-duplicated where strokes meet.
- **Real font metrics.** Letters are sized from measured ink bounds (canvas
  `actualBoundingBox*`), not from a guessed cap-height ratio, so every font
  option sits correctly on the writing lines and lowercase rides the x-height.
- **Rows fit themselves.** How many letters go on a practice line is computed
  from the letter's measured width, so `W` gets four per row and `i` gets nine
  instead of everything being squashed into one grid.
- **Deterministic randomness.** Each page seeds its own RNG from the letter,
  design and shuffle seed, so the preview and the printout always match.

## Adding your own

- **A theme:** add an entry to `THEMES` in `data.js` (colors + eight doodle
  emoji). It shows up in the drop-down automatically.
- **Picture words:** edit `LETTER_WORDS` — four words with an emoji each.
- **A worksheet style:** write a `buildX(ch, cfg, theme, rnd)` function in
  `render.js` that returns HTML, then register it in `BUILDERS`,
  `WORKSHEET_TYPES` and `INSTRUCTIONS`.

## License

Do whatever you like with it — print it, remix it, hand it out freely.
