# 🔤 Toddler Tap & Learn Alphabet

A big, bright, noisy ABC game for toddlers (roughly ages 1½–4). Every tap does
something happy: letters pop, confetti flies, balloons burst, and a friendly
voice says the letter and a word that starts with it.

It's **one HTML file**. Download it, open it, play. No app store, no account,
no internet connection, no ads, and nothing is ever sent anywhere.

---

## For parents — how to get it on your child's device

### The quick way (any computer or tablet)

1. Download `index.html` from this repository
   ([direct link](../../raw/HEAD/index.html) — right-click → *Save link as…*).
2. Double-tap the file. It opens in your browser and the game starts.
3. Tap the **⛶** button on the home screen for full screen.

To keep the game truly self-contained, `index.html` alone is enough — the other
files (`icon.svg`, `manifest.webmanifest`) only add a nicer home-screen icon.

### Put it on the home screen like a real app

Save all the files into one folder, then serve that folder over http (any static
host works — GitHub Pages, or `npx http-server` on your own machine) and open it
on the tablet:

- **iPad / iPhone:** Share button → *Add to Home Screen*
- **Android:** browser menu → *Install app* / *Add to Home screen*

It then launches full screen with no browser bars — much harder for little
fingers to escape — and a service worker caches the whole game on first visit,
so it keeps working with no signal at all: on a plane, in the car, anywhere.

### Keep them in the game

Before handing the tablet over:

- **iPad:** Settings → Accessibility → **Guided Access** (triple-click the side
  button to lock the app open)
- **Android:** Settings → Security → **App pinning** / Screen pinning

---

## The six games

| | Game | What your child does |
|---|---|---|
| 🔤 | **Tap the Letters** | 26 chunky letter tiles. Tap one — it pops, confetti bursts, and a big card says "**E** is for Elephant 🐘". Each new letter earns a ⭐. |
| 🔎 | **Find the Letter** | "Can you find **B**?" — three big choices (four once they're on a roll). Right answers cheer and celebrate; wrong ones get a gentle "try again", never a fail. |
| 🖍️ | **Trace a Letter** | A big dotted letter to scribble over with a finger. The crayon draws in rainbow colours and sparkles as it goes; colour in enough of the letter and it celebrates. Accuracy is not required — enthusiasm is. |
| 🧩 | **What Starts With?** | A picture card (🍊 Orange) and three letters. Which one does the word start with? Tap the picture to hear it again. |
| 🎈 | **Pop the Balloons** | Letter balloons drift up the screen. Tap to pop them with a satisfying *bloop* and hear the letter. |
| 🎵 | **Sing the ABCs** | The real ABC song — the Twinkle Twinkle tune, held notes and all — plays while the board lights up each letter in turn, finishing with a confetti shower. Tap anywhere to stop. |

### 📖 My ABC Book

Every letter your child plays with unlocks a sticker in their ABC Book — a
26-slot album with a rainbow progress bar across the top. Locked letters show a
padlock; unlocked ones show the letter and its picture, and tapping one says it
again. The home screen shows the running count, and it's all still there
tomorrow.

Every ⭐ is saved on the device too. Every 10 stars triggers a full-screen party,
and unlocking the 26th letter sets off a trophy celebration.

## Grown-up settings

Press and **hold** the ⚙️ gear on the home screen for 1.5 seconds — long enough
that a toddler won't land on it by accident.

- **Letter style** — `A B C` (uppercase), `a b c` (lowercase), or `Aa Bb` (both)
- **Talking voice** — on/off (uses the voices already on the device)
- **Which voice** — pick from every English voice your device has, with a 🔊
  preview button. The game auto-picks the most natural one it can find, but
  quality varies by device; if they all sound robotic, most devices can
  download better ones (iPad: Settings → Accessibility → Spoken Content →
  Voices)
- **Letter sounds** — adds the phonic sound ("**A** says *ah*") to the letter
  name. On by default; turn it off if you'd rather teach names first
- **Sound effects** — on/off
- **Gentle music** — a soft background arpeggio, off by default
- **Stars & book** — see the totals, or reset both back to zero

## Toddler-proofing built in

- No links out, no menus to get lost in, no in-app purchases, no ads
- Nothing loads from the internet — the whole game is in the one file
- No data collection; the only things stored are the star count, which letters
  have been unlocked, and your settings — all in the browser's local storage on
  that device. Where a browser blocks storage entirely (a sandboxed preview
  frame, or Safari with all cookies blocked) the game plays normally but says
  so in the settings panel instead of silently losing progress
- Pinch-zoom and double-tap-zoom are disabled so stray taps can't scramble the layout
- Wrong answers are never punished — there's no losing, no timer, no game over
- Speech and animations stop automatically when the screen is locked or the tab
  is hidden, so nothing keeps chattering in a pocket

## Technical notes

Plain HTML, CSS and JavaScript in a single file — no build step, no dependencies.

- Speech uses the browser's built-in `SpeechSynthesis`. Voices are ranked by
  quality — cloud/neural voices first, novelty voices last — and the grown-up
  can override the pick. If a device has no voices the game still works; it
  just plays the sounds without narration.
- The voice is never interrupted twice in quick succession. Cancelling and
  speaking in the same moment wedges the speech queue on iOS and some Android
  engines, after which nothing speaks for the rest of the session, so repeat
  taps wait their turn instead.
- The alphabet song speaks one phrase per musical phrase rather than 26
  separate letters, which is both more natural and the reason the queue stays
  intact.
- Sound effects and music are synthesised live with the Web Audio API, so there
  are no audio files to download. Audio unlocks on the first tap (a mobile
  browser requirement).
- The letter board and the ABC Book measure the screen and pick the tile size and
  column count that fill it best, so they look right on a phone, a tablet, or a
  laptop.
- Tracing uses three stacked canvases — the letter beneath, the child's crayon in
  the middle, the dotted outline on top so the shape stays visible while they
  colour. Completion is measured by sampling the glyph into a grid of points and
  counting how many the crayon passed over (60% is a win).

- `sw.js` caches the game for offline use, and only registers when the page is
  served over http(s) — opening the file directly skips it entirely.

Tested in Chromium across tablet, phone and desktop viewports: every mode in all
three letter-case settings, the song's order and rhythm, the trophy at 26
letters, saved progress surviving a reload, and an offline reload after the
service worker installs.

## License

Proprietary — see `LICENSE`. Buyers get personal use within their own
household; redistribution and resale are not permitted. Set the copyright
holder name in `LICENSE` before selling.
