/* =============================================================
   ABC Fun Factory — data tables
   Letter skeletons, themes, picture words, fonts, borders.
   All coordinates live in a 100 x 170 box:
     ascender 15 | x-height top 55 | baseline 125 | descender 160
   ============================================================= */

/* ---------- Uppercase stroke skeletons ---------- */
const UPPER_STROKES = {
  A: ['M15 125 L50 18 L85 125', 'M29 86 L71 86'],
  B: ['M26 18 L26 125', 'M26 18 L58 18 A 27 26 0 0 1 58 70 L26 70', 'M26 70 L61 70 A 28 27 0 0 1 61 125 L26 125'],
  C: ['M80 38 A 45 53 0 1 0 80 105'],
  D: ['M26 18 L26 125', 'M26 18 L50 18 A 35 53 0 0 1 50 125 L26 125'],
  E: ['M80 18 L26 18 L26 125 L80 125', 'M26 71 L70 71'],
  F: ['M80 18 L26 18 L26 125', 'M26 71 L70 71'],
  G: ['M80 38 A 45 53 0 1 0 80 105 L80 74 L57 74'],
  H: ['M25 18 L25 125', 'M75 18 L75 125', 'M25 71 L75 71'],
  I: ['M30 18 L70 18', 'M50 18 L50 125', 'M30 125 L70 125'],
  J: ['M70 18 L70 95 A 25 25 0 0 1 20 95'],
  K: ['M25 18 L25 125', 'M76 18 L28 71', 'M45 55 L78 125'],
  L: ['M26 18 L26 125 L78 125'],
  M: ['M22 125 L22 18 L50 82 L78 18 L78 125'],
  N: ['M25 125 L25 18 L75 125 L75 18'],
  O: ['M50 18 A 32 53 0 1 1 49.9 18'],
  P: ['M26 18 L26 125', 'M26 18 L57 18 A 27 26 0 0 1 57 71 L26 71'],
  Q: ['M50 18 A 32 53 0 1 1 49.9 18', 'M60 95 L86 128'],
  R: ['M26 18 L26 125', 'M26 18 L57 18 A 27 26 0 0 1 57 71 L26 71', 'M52 71 L78 125'],
  S: ['M78 34 C 78 12 26 12 26 44 C 26 70 76 70 76 98 C 76 130 24 130 22 108'],
  T: ['M20 18 L80 18', 'M50 18 L50 125'],
  U: ['M25 18 L25 90 A 25 35 0 0 0 75 90 L75 18'],
  V: ['M22 18 L50 125 L78 18'],
  W: ['M15 18 L32 125 L50 48 L68 125 L85 18'],
  X: ['M25 18 L75 125', 'M75 18 L25 125'],
  Y: ['M25 18 L50 72 L75 18', 'M50 72 L50 125'],
  Z: ['M25 18 L75 18 L25 125 L75 125']
};

/* ---------- Lowercase stroke skeletons ---------- */
const LOWER_STROKES = {
  a: ['M78 72 A 26 27 0 1 0 78 110', 'M78 56 L78 125'],
  b: ['M25 15 L25 125', 'M25 70 A 26 27 0 1 1 25 110'],
  c: ['M75 72 A 26 27 0 1 0 75 110'],
  d: ['M75 15 L75 125', 'M75 70 A 26 27 0 1 0 75 110'],
  e: ['M27 93 L76 93', 'M76 93 A 27 27 0 1 0 71 112'],
  f: ['M74 30 A 20 18 0 0 0 43 46 L43 125', 'M24 62 L66 62'],
  g: ['M78 70 A 26 27 0 1 0 78 110', 'M78 56 L78 140 A 26 20 0 0 1 32 149'],
  h: ['M25 15 L25 125', 'M25 80 C 30 57 75 59 75 92 L75 125'],
  i: ['M50 60 L50 125', 'DOT 50 34'],
  j: ['M60 60 L60 137 A 22 18 0 0 1 23 146', 'DOT 60 34'],
  k: ['M25 15 L25 125', 'M70 62 L30 98', 'M45 85 L73 125'],
  l: ['M50 15 L50 125'],
  m: ['M25 60 L25 125', 'M25 78 C 28 58 52 58 52 80 L52 125', 'M52 78 C 55 58 78 58 78 80 L78 125'],
  n: ['M25 60 L25 125', 'M25 78 C 30 56 75 59 75 86 L75 125'],
  o: ['M50 56 A 26 34 0 1 1 49.9 56'],
  p: ['M25 60 L25 160', 'M25 70 A 26 27 0 1 1 25 110'],
  q: ['M75 60 L75 160', 'M75 70 A 26 27 0 1 0 75 110'],
  r: ['M30 60 L30 125', 'M30 80 C 35 60 60 57 73 63'],
  s: ['M72 70 C 72 53 32 52 32 72 C 32 90 68 92 68 110 C 68 130 31 129 28 116'],
  t: ['M45 30 L45 110 A 18 16 0 0 0 74 117', 'M24 62 L67 62'],
  u: ['M25 60 L25 100 A 25 25 0 0 0 75 100 L75 60', 'M75 100 L75 125'],
  v: ['M25 60 L50 125 L75 60'],
  w: ['M18 60 L33 125 L50 80 L67 125 L82 60'],
  x: ['M28 60 L72 125', 'M72 60 L28 125'],
  y: ['M25 60 L52 118', 'M78 60 L40 160'],
  z: ['M28 60 L72 60 L28 125 L72 125']
};

/* ---------- Picture words (emoji keeps it printer friendly) ---------- */
const LETTER_WORDS = {
  A: [['Apple','🍎'],['Ant','🐜'],['Alligator','🐊'],['Airplane','✈️']],
  B: [['Ball','⚽'],['Bear','🐻'],['Banana','🍌'],['Bee','🐝']],
  C: [['Cat','🐱'],['Cake','🎂'],['Car','🚗'],['Cow','🐄']],
  D: [['Dog','🐶'],['Duck','🦆'],['Donut','🍩'],['Drum','🥁']],
  E: [['Elephant','🐘'],['Egg','🥚'],['Eagle','🦅'],['Ear','👂']],
  F: [['Fish','🐠'],['Frog','🐸'],['Flower','🌸'],['Fox','🦊']],
  G: [['Goat','🐐'],['Grapes','🍇'],['Gift','🎁'],['Guitar','🎸']],
  H: [['Hat','👒'],['Horse','🐴'],['House','🏠'],['Heart','❤️']],
  I: [['Ice Cream','🍦'],['Iguana','🦎'],['Insect','🐞'],['Island','🏝️']],
  J: [['Jellyfish','🪼'],['Juice','🧃'],['Jar','🫙'],['Jet','🛩️']],
  K: [['Kite','🪁'],['Key','🔑'],['Koala','🐨'],['Kangaroo','🦘']],
  L: [['Lion','🦁'],['Leaf','🍃'],['Lemon','🍋'],['Ladybug','🐞']],
  M: [['Moon','🌙'],['Mouse','🐭'],['Monkey','🐵'],['Milk','🥛']],
  N: [['Nest','🪺'],['Nose','👃'],['Nuts','🥜'],['Noodles','🍜']],
  O: [['Octopus','🐙'],['Orange','🍊'],['Owl','🦉'],['Onion','🧅']],
  P: [['Pig','🐷'],['Pizza','🍕'],['Penguin','🐧'],['Pear','🍐']],
  Q: [['Queen','👸'],['Quilt','🧶'],['Question','❓'],['Quail','🐦']],
  R: [['Rainbow','🌈'],['Rabbit','🐰'],['Robot','🤖'],['Rocket','🚀']],
  S: [['Sun','☀️'],['Star','⭐'],['Snake','🐍'],['Strawberry','🍓']],
  T: [['Tree','🌳'],['Tiger','🐯'],['Turtle','🐢'],['Train','🚂']],
  U: [['Umbrella','☂️'],['Unicorn','🦄'],['Ukulele','🪕'],['UFO','🛸']],
  V: [['Violin','🎻'],['Volcano','🌋'],['Van','🚐'],['Vegetables','🥕']],
  W: [['Whale','🐳'],['Watermelon','🍉'],['Wagon','🚚'],['Worm','🪱']],
  X: [['X-ray','🩻'],['Xylophone','🎼'],['Box','📦'],['Six','6️⃣']],
  Y: [['Yarn','🧶'],['Yo-yo','🪀'],['Yak','🐃'],['Yogurt','🍨']],
  Z: [['Zebra','🦓'],['Zipper','🧥'],['Zoo','🏞️'],['Zero','0️⃣']]
};

/* ---------- Themes ---------- */
const THEMES = {
  jungle: {
    name: '🦁 Jungle Safari',
    ink: '#1f6b3a', ink2: '#b4531a', accent: '#f4b400', paper: '#f4fbef',
    band: '#dff2d2', guide: '#7fb069', trace: '#9fc79a',
    doodles: ['🦁','🐘','🌴','🐒','🦒','🦓','🍌','🐍']
  },
  ocean: {
    name: '🐠 Under the Sea',
    ink: '#0a6ea3', ink2: '#11897f', accent: '#ff9f1c', paper: '#eefaff',
    band: '#d5f0fb', guide: '#57b8e0', trace: '#9dd3ea',
    doodles: ['🐠','🐙','🐳','🦀','🐚','🌊','🐟','⭐']
  },
  space: {
    name: '🚀 Outer Space',
    ink: '#4b2e83', ink2: '#c2185b', accent: '#ffd23f', paper: '#f6f2ff',
    band: '#e7defb', guide: '#8f7bd6', trace: '#b7a6e8',
    doodles: ['🚀','🪐','⭐','🌙','👽','🛸','☄️','🌟']
  },
  farm: {
    name: '🐮 Farm Friends',
    ink: '#a83232', ink2: '#7a5c2e', accent: '#f2b807', paper: '#fffaf0',
    band: '#fdeccd', guide: '#d59a4a', trace: '#e3bd8b',
    doodles: ['🐮','🐷','🐔','🚜','🌻','🐴','🥕','🧺']
  },
  dino: {
    name: '🦕 Dino Days',
    ink: '#2e7d5b', ink2: '#5b6d1f', accent: '#ef6c33', paper: '#f2fbf6',
    band: '#d8f0e3', guide: '#67ad8b', trace: '#a3d3bc',
    doodles: ['🦕','🦖','🌋','🥚','🦴','🌿','🪨','🐊']
  },
  candy: {
    name: '🍭 Candy Rainbow',
    ink: '#d81b74', ink2: '#7b3fbf', accent: '#ffc233', paper: '#fff5fa',
    band: '#ffe0ef', guide: '#f07ab0', trace: '#f7b4d2',
    doodles: ['🍭','🧁','🍬','🌈','🍩','🍦','🎈','⭐']
  },
  woodland: {
    name: '🦉 Woodland Forest',
    ink: '#6b4423', ink2: '#3f7a43', accent: '#e58b2a', paper: '#fdf8ef',
    band: '#eee1cd', guide: '#b08957', trace: '#d3bb98',
    doodles: ['🦉','🦊','🍄','🌲','🐿️','🍂','🐻','🪵']
  },
  fairytale: {
    name: '🏰 Fairy Tale',
    ink: '#7048a8', ink2: '#c2255c', accent: '#f6c445', paper: '#fdf4ff',
    band: '#f0e0fb', guide: '#a97fd4', trace: '#c9b0e6',
    doodles: ['🏰','🦄','👑','🐉','🧚','⭐','🪄','🌈']
  }
};

/* ---------- Letter fonts ---------- */
const FONTS = {
  school:  { name: 'School Print',   stack: "'Andika','Century Gothic','Trebuchet MS',sans-serif", weight: 700 },
  bubble:  { name: 'Rounded Bubble', stack: "'Baloo 2','Fredoka','Trebuchet MS',sans-serif",       weight: 800 },
  comic:   { name: 'Comic Fun',      stack: "'Comic Neue','Comic Sans MS',cursive",                weight: 700 },
  hand:    { name: 'Handwriting',    stack: "'Patrick Hand','Bradley Hand',cursive",               weight: 400 },
  chunky:  { name: 'Chunky Block',   stack: "'Fredoka','Arial Black',sans-serif",                  weight: 700 }
};

/* ---------- Worksheet styles ---------- */
const WORKSHEET_TYPES = {
  trace:    { name: '✏️ Trace & Write',        blurb: 'Warm-up rows, guided tracing, then free practice.' },
  rainbow:  { name: '🌈 Rainbow Trace',        blurb: 'Trace the big letter in every crayon color.' },
  color:    { name: '🎨 Color the Big Letter', blurb: 'Giant bubble letter with themed doodles to color.' },
  dot:      { name: '🔵 Do-A-Dot Letter',      blurb: 'Dot markers or fingerprints along the letter path.' },
  connect:  { name: '🔢 Dot-to-Dot Letter',    blurb: 'Count and connect numbered dots to build the letter.' },
  find:     { name: '🔍 Find & Circle',        blurb: 'Hunt the target letter in a grid of look-alikes.' },
  sounds:   { name: '🔊 Beginning Sounds',     blurb: 'Circle the pictures that start with the letter.' },
  allinone: { name: '⭐ All-In-One Practice',  blurb: 'Trace, find, color and sort on a single page.' },
  poster:   { name: '🖼️ Letter Poster',        blurb: 'Big display letter with picture words for the wall.' }
};

/* ---------- Page borders ---------- */
const BORDERS = {
  confetti: 'Confetti dots',
  doodle:   'Theme doodles',
  scallop:  'Scalloped frame',
  stripe:   'Candy stripe',
  simple:   'Simple line',
  none:     'No border'
};
