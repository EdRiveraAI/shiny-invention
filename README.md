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
   ([direct link](../../raw/main/index.html) — right-click → *Save link as…*).
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
fingers to escape.

### Keep them in the game

Before handing the tablet over:

- **iPad:** Settings → Accessibility → **Guided Access** (triple-click the side
  button to lock the app open)
- **Android:** Settings → Security → **App pinning** / Screen pinning

---

## The four games

| | Game | What your child does |
|---|---|---|
| 🔤 | **Tap the Letters** | 26 chunky letter tiles. Tap one — it pops, confetti bursts, and a big card says "**E** is for Elephant 🐘". Each new letter earns a ⭐. |
| 🔎 | **Find the Letter** | "Can you find **B**?" — three big choices (four once they're on a roll). Right answers cheer and celebrate; wrong ones get a gentle "try again", never a fail. |
| 🎈 | **Pop the Balloons** | Letter balloons drift up the screen. Tap to pop them with a satisfying *bloop* and hear the letter. |
| 🎵 | **Sing the ABCs** | The board sings itself A→Z, lighting up each letter in turn, and finishes with a confetti shower. Tap anywhere to stop. |

Every ⭐ is saved on the device. Every 10 stars triggers a full-screen party.

## Grown-up settings

Press and **hold** the ⚙️ gear on the home screen for 1.5 seconds — long enough
that a toddler won't land on it by accident.

- **Letter style** — `A B C` (uppercase), `a b c` (lowercase), or `Aa Bb` (both)
- **Talking voice** — on/off (uses the voice already built into the device)
- **Sound effects** — on/off
- **Gentle music** — a soft background arpeggio, off by default
- **Stars** — see the total, or reset it back to zero

## Toddler-proofing built in

- No links out, no menus to get lost in, no in-app purchases, no ads
- Nothing loads from the internet — the whole game is in the one file
- No data collection; the only thing stored is the star count and your settings,
  in the browser's local storage on that device
- Pinch-zoom and double-tap-zoom are disabled so stray taps can't scramble the layout
- Wrong answers are never punished — there's no losing, no timer, no game over
- Speech and animations stop automatically when the screen is locked or the tab
  is hidden, so nothing keeps chattering in a pocket

## Technical notes

Plain HTML, CSS and JavaScript in a single file — no build step, no dependencies.

- Speech uses the browser's built-in `SpeechSynthesis`. If a device has no voices
  installed the game still works; it just plays the sounds without the narration.
- Sound effects and music are synthesised live with the Web Audio API, so there
  are no audio files to download. Audio unlocks on the first tap (a mobile
  browser requirement).
- The letter board measures the screen and picks the tile size and column count
  that fill it best, so it looks right on a phone, a tablet, or a laptop.

Tested in Chromium on desktop and phone-sized viewports.

## License

MIT — use it, change it, share it with other parents.
