/* =============================================================
   ABC Fun Factory — worksheet renderer
   Every worksheet is built as an SVG/HTML string so it prints
   crisply at any paper size.
   ============================================================= */

/* ---------- tiny helpers ---------- */
function hashSeed(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}
function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function shuffled(arr, rnd) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}
function esc(s) {
  return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

/* ---------- path measuring (used by dot pages) ---------- */
let _measureSvg = null;
function measurePath(d) {
  if (!_measureSvg) {
    _measureSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    _measureSvg.setAttribute('width', '0');
    _measureSvg.setAttribute('height', '0');
    _measureSvg.style.position = 'absolute';
    _measureSvg.style.opacity = '0';
    _measureSvg.style.pointerEvents = 'none';
    document.body.appendChild(_measureSvg);
  }
  const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  p.setAttribute('d', d);
  _measureSvg.appendChild(p);
  return p;
}
function samplePath(d, spacing) {
  const p = measurePath(d);
  const len = p.getTotalLength();
  const pts = [];
  if (!len) { _measureSvg.removeChild(p); return pts; }
  const steps = Math.max(1, Math.round(len / spacing));
  for (let i = 0; i <= steps; i++) {
    const pt = p.getPointAtLength((len / steps) * i);
    pts.push({ x: pt.x, y: pt.y });
  }
  _measureSvg.removeChild(p);
  return pts;
}
function pathTip(d) {
  const p = measurePath(d);
  const len = p.getTotalLength();
  const end = p.getPointAtLength(len);
  const before = p.getPointAtLength(Math.max(0, len - 6));
  const start = p.getPointAtLength(0);
  _measureSvg.removeChild(p);
  return { start, end, angle: Math.atan2(end.y - before.y, end.x - before.x) * 180 / Math.PI };
}

/* ---------- font metrics (measured, never guessed) ---------- */
const _glyphCache = new Map();
let _measureCtx = null;
function clearGlyphCache() { _glyphCache.clear(); }
/* Canvas ink metrics — SVG getBBox() reports the em box, which would make
   every letter the same height no matter what it actually looks like. */
function textMetrics(ch, font, size) {
  const key = `${ch}|${font.stack}|${font.weight}|${size.toFixed(2)}`;
  if (_glyphCache.has(key)) return _glyphCache.get(key);
  if (!_measureCtx) _measureCtx = document.createElement('canvas').getContext('2d');
  _measureCtx.font = `${font.weight} ${size}px ${font.stack}`;
  const tm = _measureCtx.measureText(ch);
  const asc = tm.actualBoundingBoxAscent, desc = tm.actualBoundingBoxDescent;
  const m = {
    w: (tm.actualBoundingBoxRight != null && tm.actualBoundingBoxLeft != null)
      ? Math.max(tm.width, tm.actualBoundingBoxRight + tm.actualBoundingBoxLeft) : tm.width,
    h: (asc != null && desc != null) ? asc + desc : size * 0.7,
    top: asc != null ? -asc : -size * 0.7
  };
  if (!m.h || !isFinite(m.h)) m.h = size * 0.7;
  if (!m.w || !isFinite(m.w)) m.w = size * 0.62 * ch.length;
  _glyphCache.set(key, m);
  return m;
}
/* Size a glyph so its ink fits the slot. refChar anchors the vertical
   rhythm: 'H' for capitals, 'x' so lowercase sits on the x-height. */
function fitSize(ch, font, maxW, maxH, refChar) {
  const ref = textMetrics(refChar, font, 100);
  let size = 100 * (maxH / (ref.h || 70));
  const m = textMetrics(ch, font, size);
  if (maxW && m.w > maxW) size *= maxW / m.w;
  return size;
}
function isLower(ch) { return ch === ch.toLowerCase() && ch !== ch.toUpperCase(); }

/* ---------- letter geometry ---------- */
/* Skeleton space: 100 wide x 170 tall, baseline 125, cap top 18 */
const SKEL_BASELINE = 125, SKEL_CAP = 18, SKEL_CAPH = SKEL_BASELINE - SKEL_CAP;
const SKEL_XH = SKEL_BASELINE - 55;

/* Dot positions for the do-a-dot / dot-to-dot pages. Sampling each stroke
   separately doubles up dots where strokes meet, so near-duplicates are
   dropped while the drawing order is kept. */
function dotPositions(ch, spacing) {
  const out = [];
  const minD = spacing * 0.8;
  strokesFor(ch).forEach(d => {
    if (d.startsWith('DOT')) {
      const q = d.split(/\s+/);
      out.push({ x: parseFloat(q[1]), y: parseFloat(q[2]), pin: true });
      return;
    }
    samplePath(d, spacing).forEach((pt, k, arr) => {
      const prev = arr[k - 1] || pt, next = arr[k + 1] || pt;
      if (out.some(o => Math.hypot(o.x - pt.x, o.y - pt.y) < minD)) return;
      out.push({ x: pt.x, y: pt.y, dx: next.x - prev.x, dy: next.y - prev.y });
    });
  });
  return out;
}

function skelBox(chars) {
  const lower = chars.every(isLower);
  const desc = chars.some(c => 'gjpqy'.indexOf(c) > -1);
  const y0 = lower && !/[bdfhklt]/.test(chars.join('')) ? 40 : 6;
  const y1 = desc ? 170 : 136;
  return { y0, h: y1 - y0 };
}
function strokesFor(ch) {
  return (UPPER_STROKES[ch] || LOWER_STROKES[ch] || ['M50 18 L50 125']);
}

/* Font glyph — the workhorse for tracing rows.
   Stroke weights and dash patterns scale with the letter so a small
   lowercase a gets the same dotted texture as a big capital A. */
function glyphSVG(ch, opts) {
  const o = Object.assign({ x: 0, baseline: 0, size: 200, style: 'model', font: FONTS.school, color: '#333', trace: '#bbb' }, opts);
  const z = o.size;
  const common = `x="${o.x}" y="${o.baseline}" text-anchor="middle" font-family="${o.font.stack}" font-weight="${o.font.weight}" font-size="${z}"`;
  const sw = v => Math.max(1.6, z * v).toFixed(2);
  switch (o.style) {
    case 'dotted':
      return `<text ${common} fill="none" stroke="${o.trace}" stroke-width="${sw(0.024)}" stroke-linecap="round" stroke-dasharray="${(z * 0.006).toFixed(2)} ${(z * 0.05).toFixed(2)}">${esc(ch)}</text>`;
    case 'dashed':
      return `<text ${common} fill="none" stroke="${o.trace}" stroke-width="${sw(0.019)}" stroke-linecap="round" stroke-dasharray="${(z * 0.07).toFixed(2)} ${(z * 0.05).toFixed(2)}">${esc(ch)}</text>`;
    case 'outline':
      return `<text ${common} fill="none" stroke="${o.trace}" stroke-width="${sw(0.016)}">${esc(ch)}</text>`;
    case 'gray':
      return `<text ${common} fill="${o.trace}" opacity="0.55">${esc(ch)}</text>`;
    case 'hollowbig':
      return `<text ${common} fill="#ffffff" stroke="${o.color}" stroke-width="${sw(0.022)}" stroke-linejoin="round">${esc(ch)}</text>`;
    case 'blank':
      return '';
    default:
      return `<text ${common} fill="${o.color}">${esc(ch)}</text>`;
  }
}

/* Skeleton glyph — dotted paths, stroke-order arrows, do-a-dot, dot-to-dot.
   Sizes below are tuned for native scale (s = 1), which is what the dot
   worksheets use, so a dot stays dot-sized instead of ballooning. */
function skeletonSVG(ch, opts) {
  const o = Object.assign({
    cx: 0, baseline: 0, capHeight: 140, xHeight: 0, mode: 'arrows',
    color: '#333', trace: '#bbb', accent: '#f4b400', dotSpacing: 24, counterStart: 1
  }, opts);
  const s = o.xHeight ? o.xHeight / SKEL_XH : o.capHeight / SKEL_CAPH;
  const tx = o.cx - 50 * s;
  const ty = o.baseline - SKEL_BASELINE * s;
  let body = '';
  let n = o.counterStart;

  const label = (x, y, text) =>
    `<text x="${x.toFixed(1)}" y="${y.toFixed(1)}" font-size="5.6" font-weight="700" font-family="'Fredoka',sans-serif" text-anchor="middle" fill="${o.color}">${text}</text>`;

  const dotMode = o.mode === 'dots' || o.mode === 'connect';
  if (!dotMode) strokesFor(ch).forEach((d, i) => {
    if (d.startsWith('DOT')) {
      const q = d.split(/\s+/);
      body += `<circle cx="${q[1]}" cy="${q[2]}" r="6" fill="none" stroke="${o.trace}" stroke-width="3.5" stroke-dasharray="0.5 6" stroke-linecap="round"/>`;
      return;
    }
    {
      body += `<path d="${d}" fill="none" stroke="${o.trace}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="${o.mode === 'arrows' ? '0.5 13' : 'none'}"/>`;
      if (o.mode === 'arrows') {
        const tip = pathTip(d);
        /* nudge the badge clear of the letter so strokes that start close
           together (like the two strokes of a) stay readable */
        const bx = tip.start.x + (tip.start.x > 50 ? 12 : -12);
        const by = tip.start.y + (tip.start.y < 70 ? -10 : 8);
        body += `<circle cx="${bx.toFixed(1)}" cy="${by.toFixed(1)}" r="6.5" fill="${o.accent}"/>`;
        body += `<text x="${bx.toFixed(1)}" y="${(by + 3.4).toFixed(1)}" font-size="9.5" font-weight="700" font-family="sans-serif" text-anchor="middle" fill="#fff">${i + 1}</text>`;
        body += `<g transform="translate(${tip.end.x.toFixed(1)} ${tip.end.y.toFixed(1)}) rotate(${tip.angle.toFixed(1)})"><path d="M-8 -5 L1.5 0 L-8 5 Z" fill="${o.color}"/></g>`;
      }
    }
  });
  if (dotMode) {
    dotPositions(ch, o.dotSpacing).forEach(pt => {
      if (o.mode === 'dots') {
        body += `<circle cx="${pt.x.toFixed(1)}" cy="${pt.y.toFixed(1)}" r="5" fill="none" stroke="${o.trace}" stroke-width="1.8"/>`;
        return;
      }
      let nx = -(pt.dy || 0), ny = pt.dx || 1;
      const len = Math.hypot(nx, ny) || 1;
      nx /= len; ny /= len;
      /* numbers sit off the stroke: under horizontal strokes, outside
         vertical ones, so legs and crossbars never collide */
      const sign = Math.abs(ny) > Math.abs(nx) ? (ny > 0 ? 1 : -1) : (((pt.x - 50) * nx > 0) ? 1 : -1);
      body += `<circle cx="${pt.x.toFixed(1)}" cy="${pt.y.toFixed(1)}" r="2.4" fill="${o.color}"/>`;
      body += label(pt.x + nx * 7.5 * sign, pt.y + ny * 7.5 * sign + 2, n++);
    });
  }
  return `<g transform="translate(${tx.toFixed(2)} ${ty.toFixed(2)}) scale(${s.toFixed(4)})">${body}</g>`;
}
function countDots(ch, spacing) { return dotPositions(ch, spacing).length; }

/* ---------- guide lines ---------- */
function guidesSVG(w, geo, cfg, t) {
  const { top, mid, base, desc } = geo;
  const c = cfg.color ? t.guide : '#9a9a9a';
  if (cfg.lines === 'none') return '';
  if (cfg.lines === 'boxes') {
    let out = '';
    const step = geo.step, n = geo.slots;
    for (let i = 0; i < n; i++) {
      const x = geo.startX + step * i - step * 0.44;
      out += `<rect x="${x.toFixed(1)}" y="${top}" width="${(step * 0.88).toFixed(1)}" height="${base - top}" rx="8" fill="none" stroke="${c}" stroke-width="2" stroke-dasharray="7 6"/>`;
    }
    return out;
  }
  if (cfg.lines === 'baseline') {
    return `<line x1="14" y1="${base}" x2="${w - 14}" y2="${base}" stroke="${c}" stroke-width="3"/>`;
  }
  /* three-line handwriting guide */
  let out = `<line x1="14" y1="${top}" x2="${w - 14}" y2="${top}" stroke="${c}" stroke-width="2"/>` +
            `<line x1="14" y1="${mid}" x2="${w - 14}" y2="${mid}" stroke="${c}" stroke-width="2" stroke-dasharray="12 10"/>` +
            `<line x1="14" y1="${base}" x2="${w - 14}" y2="${base}" stroke="${c}" stroke-width="3"/>`;
  if (cfg.lines === 'threeline-desc') {
    out += `<line x1="14" y1="${desc}" x2="${w - 14}" y2="${desc}" stroke="${c}" stroke-width="1.6" stroke-dasharray="4 8"/>`;
  }
  return out;
}

/* ---------- a single practice row ----------
   The letter always fills the writing band; how many fit on the line is
   worked out from the letter's measured width, so W gets 4 per row and
   i gets 8 instead of everything being squashed to one grid.            */
function traceRow(ch, cfg, t, opts) {
  const o = Object.assign({ showModel: true, guidedShare: 0.55, height: 210 }, opts);
  const W = 1000, H = o.height;
  const geo = {
    top: H * 0.16, mid: H * 0.495, base: H * 0.82, desc: H * 0.97,
    startX: 0, step: 0, slots: 0
  };
  const lower = isLower(ch);
  const inkH = lower ? geo.base - geo.mid : geo.base - geo.top;
  const size = fitSize(ch, cfg.fontObj, 0, inkH, lower ? 'x' : 'H');
  const inkW = textMetrics(ch, cfg.fontObj, size).w;

  const pitch = Math.max(inkW * 1.3, (geo.base - geo.top) * 0.62);
  const usable = W - 30;
  const total = Math.max(4, Math.min(9, Math.floor(usable / pitch)));
  const step = usable / total;
  geo.step = step; geo.startX = 15 + step / 2; geo.slots = total;

  const rest = total - (o.showModel ? 1 : 0);
  const guided = Math.max(1, Math.round(rest * o.guidedShare));
  const blanks = rest - guided;

  let inner = guidesSVG(W, geo, cfg, t);
  let idx = 0;
  const put = (style) => {
    const x = geo.startX + step * idx;
    idx++;
    if (style === 'blank') return '';
    if (style === 'arrows') {
      return skeletonSVG(ch, {
        cx: x, baseline: geo.base, mode: 'arrows',
        capHeight: lower ? 0 : geo.base - geo.top,
        xHeight: lower ? geo.base - geo.mid : 0,
        color: cfg.color ? t.ink : '#333', trace: cfg.color ? t.trace : '#c9c9c9',
        accent: cfg.color ? t.accent : '#999'
      });
    }
    return glyphSVG(ch, {
      x, baseline: geo.base, size, style, font: cfg.fontObj,
      color: cfg.color ? t.ink : '#222', trace: cfg.color ? t.trace : '#c4c4c4'
    });
  };
  /* stroke-order arrows belong on the model letter; the rest stay dotted */
  const arrows = cfg.traceStyle === 'arrows';
  if (o.showModel) inner += put(arrows ? 'arrows' : 'model');
  for (let i = 0; i < guided; i++) inner += put(arrows ? 'dotted' : cfg.traceStyle);
  for (let i = 0; i < blanks; i++) inner += put('blank');

  return `<svg class="row" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Practice row for the letter ${esc(ch)}">${inner}</svg>`;
}

/* row height budget: more rows on the page means shorter rows */
const ROW_HEIGHTS = { 2: 250, 3: 225, 4: 205, 5: 168, 6: 142 };
function rowHeight(cfg, bonus) {
  return (ROW_HEIGHTS[cfg.rows] || 205) * (bonus || 1);
}

/* ---------- letter-hunt grid ---------- */
const LOOKALIKES = {
  A: 'AVHRX', B: 'BDPRE', C: 'COGUQ', D: 'DOBPQ', E: 'EFBLH', F: 'FETPL', G: 'GCOQS', H: 'HNMKA',
  I: 'ITLJF', J: 'JIULT', K: 'KXRYH', L: 'LITEJ', M: 'MNWVH', N: 'NMHUZ', O: 'OQCDG', P: 'PRBFD',
  Q: 'QOGCD', R: 'RPBKA', S: 'SZGC5', T: 'TIFYL', U: 'UVJOC', V: 'VWYUA', W: 'WVMNU', X: 'XKYZV',
  Y: 'YVXTK', Z: 'ZSNXE'
};
function hunterPool(ch, cfg) {
  const pool = (LOOKALIKES[ch.toUpperCase()] || 'ABCDE').split('');
  let out = [];
  pool.forEach(p => {
    if (cfg.letterCase !== 'lower') out.push(p);
    if (cfg.letterCase !== 'upper') out.push(p.toLowerCase());
  });
  return out.filter(x => x.toUpperCase() !== ch.toUpperCase());
}
function huntGrid(ch, cfg, rnd, cols, rows) {
  const targets = cfg.letterCase === 'upper' ? [ch.toUpperCase()]
    : cfg.letterCase === 'lower' ? [ch.toLowerCase()]
      : [ch.toUpperCase(), ch.toLowerCase()];
  const pool = hunterPool(ch, cfg);
  const cells = [];
  const totalCells = cols * rows;
  const hits = Math.max(6, Math.round(totalCells * 0.28));
  for (let i = 0; i < totalCells; i++) {
    cells.push(i < hits ? { ch: targets[i % targets.length], hit: true }
      : { ch: pool[Math.floor(rnd() * pool.length)] || 'x', hit: false });
  }
  return { cells: shuffled(cells, rnd), hits, cols, rows };
}
function huntGridHTML(grid, cfg, t) {
  const cells = grid.cells.map(c =>
    `<span class="hunt-cell${c.hit ? ' is-target' : ''}" style="font-family:${cfg.fontObj.stack}">${esc(c.ch)}</span>`).join('');
  return `<div class="hunt-grid" style="--cols:${grid.cols};--hunt-ink:${cfg.color ? t.ink : '#222'}">${cells}</div>`;
}

/* ---------- picture helpers ---------- */
function pictureCard(word, emoji, cfg, extraClass) {
  return `<div class="pic-card ${extraClass || ''}">
      <div class="pic-emoji">${emoji}</div>
      <div class="pic-word">${esc(word)}</div>
    </div>`;
}
function otherLetterWords(ch, rnd, n) {
  const keys = Object.keys(LETTER_WORDS).filter(k => k !== ch.toUpperCase());
  const picks = shuffled(keys, rnd).slice(0, n);
  return picks.map(k => { const w = LETTER_WORDS[k]; return w[Math.floor(rnd() * w.length)]; });
}

/* ---------- worksheet bodies ---------- */
function letterLabel(ch, cfg) {
  return cfg.letterCase === 'upper' ? ch.toUpperCase()
    : cfg.letterCase === 'lower' ? ch.toLowerCase()
      : ch.toUpperCase() + ch.toLowerCase();
}
function casesToRender(ch, cfg) {
  if (cfg.letterCase === 'upper') return [ch.toUpperCase()];
  if (cfg.letterCase === 'lower') return [ch.toLowerCase()];
  return [ch.toUpperCase(), ch.toLowerCase()];
}

function buildTrace(ch, cfg, t, rnd) {
  const cases = casesToRender(ch, cfg);
  const rowsPerCase = Math.max(1, Math.round(cfg.rows / cases.length));
  const h = rowHeight(cfg, cfg.pictures ? 1 : 1.12);
  let out = '';
  cases.forEach(c => {
    out += `<div class="band"><span class="band-tag">${esc(c)}</span>`;
    for (let i = 0; i < rowsPerCase; i++) {
      out += traceRow(c, cfg, t, {
        showModel: i === 0,
        guidedShare: i === 0 ? 0.6 : 0.4,
        height: h
      });
    }
    out += `</div>`;
  });
  if (cfg.pictures) {
    const words = LETTER_WORDS[ch.toUpperCase()].slice(0, 4);
    out += `<div class="pic-strip">${words.map(w => pictureCard(w[0], w[1], cfg)).join('')}</div>`;
  }
  return out;
}

function buildRainbow(ch, cfg, t) {
  const cases = casesToRender(ch, cfg);
  const crayons = ['#e63946', '#f4a261', '#f7d046', '#2a9d8f', '#3a86ff', '#8338ec'];
  const swatches = crayons.map(c => `<span class="crayon" style="--crayon:${c}"></span>`).join('');
  /* a narrow viewBox makes the letter fill the box once the svg is
     stretched to the page width */
  const W = 420, H = cases.length > 1 ? 190 : 330;
  const boxes = cases.map(c => {
    const geo = {
      top: H * 0.16, mid: H * 0.495, base: H * 0.82, desc: H * 0.97,
      startX: W / 2, step: W, slots: 1
    };
    const lower = isLower(c);
    const inkH = lower ? geo.base - geo.mid : geo.base - geo.top;
    const size = fitSize(c, cfg.fontObj, W * 0.55, inkH, lower ? 'x' : 'H');
    const inner = guidesSVG(W, geo, cfg, t) +
      glyphSVG(c, {
        x: W / 2, baseline: geo.base, size, style: 'hollowbig',
        font: cfg.fontObj, color: cfg.color ? t.ink : '#333'
      });
    return `<div class="rainbow-box"><svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet">${inner}</svg></div>`;
  }).join('');
  return `<div class="crayon-row">${swatches}<span class="crayon-note">Trace me once in every color!</span></div>
    <div class="rainbow-wrap ${cases.length > 1 ? 'two' : 'one'}">${boxes}</div>`;
}

function buildColor(ch, cfg, t, rnd) {
  const word = LETTER_WORDS[ch.toUpperCase()][0];
  const doodles = shuffled(t.doodles, rnd).slice(0, 6);
  const label = letterLabel(ch, cfg);
  const W = 900, H = 560;
  const base = 486, top = 62;
  const size = fitSize(label, cfg.fontObj, W * 0.86, base - top, 'H');
  const glyph = glyphSVG(label, {
    x: W / 2, baseline: base, size, style: 'hollowbig', font: cfg.fontObj,
    color: cfg.color ? t.ink : '#333'
  });
  return `<div class="color-stage">
      <div class="doodle-cloud">${doodles.map((d, i) => `<span class="doodle d${i}">${d}</span>`).join('')}</div>
      <svg class="color-letter" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet">${glyph}</svg>
    </div>
    <div class="color-foot">
      <div class="color-word">${word[1]} <span>${esc(word[0])}</span></div>
      <div class="color-tip">Color the letter, then trace it with your finger!</div>
    </div>`;
}

function buildDot(ch, cfg, t) {
  const cases = casesToRender(ch, cfg);
  const SP = 13;                    /* dot pitch in skeleton units */
  const pad = cases.length > 1 ? 18 : 44;   /* one letter gets more air */
  const cell = 104;
  const bx = skelBox(cases);
  const W = cases.length * cell + pad * 2, H = bx.h;
  let inner = '';
  cases.forEach((c, i) => {
    inner += skeletonSVG(c, {
      cx: pad + cell * i + cell / 2, baseline: SKEL_BASELINE, capHeight: SKEL_CAPH, mode: 'dots',
      color: cfg.color ? t.ink : '#333', trace: cfg.color ? t.ink2 : '#444', dotSpacing: SP
    });
  });
  const total = cases.reduce((n, c) => n + countDots(c, SP), 0);
  return `<svg class="dot-letter" viewBox="0 ${bx.y0} ${W} ${H}" preserveAspectRatio="xMidYMid meet">${inner}</svg>
    <div class="count-strip">
      <span class="count-chip">Dots to fill: <b>${total}</b></span>
      <span class="count-chip">Use a dot marker, sticker or fingerprint!</span>
    </div>`;
}

function buildConnect(ch, cfg, t) {
  const c = cfg.letterCase === 'lower' ? ch.toLowerCase() : ch.toUpperCase();
  const SP = 16;
  const bx = skelBox([c]);
  const W = 150, H = bx.h;
  const inner = skeletonSVG(c, {
    cx: W / 2, baseline: SKEL_BASELINE, capHeight: SKEL_CAPH, mode: 'connect',
    color: cfg.color ? t.ink : '#222', trace: cfg.color ? t.trace : '#bbb', dotSpacing: SP
  });
  const total = countDots(c, SP);
  return `<svg class="dot-letter" viewBox="0 ${bx.y0} ${W} ${H}" preserveAspectRatio="xMidYMid meet">${inner}</svg>
    <div class="count-strip">
      <span class="count-chip">Start at <b>1</b> and connect all the way to <b>${total}</b></span>
      <span class="count-chip">Then trace over your letter again!</span>
    </div>`;
}

function buildFind(ch, cfg, t, rnd) {
  const grid = huntGrid(ch, cfg, rnd, 8, 7);
  return `${huntGridHTML(grid, cfg, t)}
    <div class="count-strip">
      <span class="count-chip">I found <span class="write-box"></span> letters!</span>
      <span class="count-chip">Color each one a different color.</span>
    </div>`;
}

function buildSounds(ch, cfg, t, rnd) {
  const right = shuffled(LETTER_WORDS[ch.toUpperCase()], rnd).slice(0, 3);
  const wrong = otherLetterWords(ch, rnd, 3);
  const all = shuffled(right.concat(wrong), rnd);
  return `<div class="sound-grid">${all.map(w => pictureCard(w[0], w[1], cfg, 'circleable')).join('')}</div>
    <div class="count-strip">
      <span class="count-chip">Circle every picture that starts with <b>${esc(letterLabel(ch, cfg))}</b></span>
      <span class="count-chip">Say each word out loud first!</span>
    </div>`;
}

function buildAllInOne(ch, cfg, t, rnd) {
  const upper = ch.toUpperCase(), lower = ch.toLowerCase();
  const grid = huntGrid(ch, cfg, rnd, 7, 3);
  const words = LETTER_WORDS[upper].slice(0, 3);
  const W = 420, H = 300;
  const quadSize = fitSize(upper + lower, cfg.fontObj, W * 0.8, 200, 'H');
  const colorGlyph = glyphSVG(upper + lower, { x: W / 2, baseline: 255, size: quadSize, style: 'hollowbig', font: cfg.fontObj, color: cfg.color ? t.ink : '#333' });
  return `<div class="mini"><h3 class="mini-title">1. Trace it</h3>
      ${traceRow(upper, cfg, t, { showModel: true, guidedShare: 0.55, height: 170 })}
      ${traceRow(lower, cfg, t, { showModel: true, guidedShare: 0.55, height: 170 })}
    </div>
    <div class="quad">
      <div class="mini"><h3 class="mini-title">2. Find ${esc(upper)} and ${esc(lower)}</h3>${huntGridHTML(grid, cfg, t)}</div>
      <div class="mini"><h3 class="mini-title">3. Color it</h3>
        <svg class="quad-letter" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet">${colorGlyph}</svg>
      </div>
    </div>
    <div class="mini"><h3 class="mini-title">4. Say the words</h3>
      <div class="pic-strip">${words.map(w => pictureCard(w[0], w[1], cfg)).join('')}</div>
    </div>`;
}

function buildPoster(ch, cfg, t, rnd) {
  const upper = ch.toUpperCase(), lower = ch.toLowerCase();
  const words = LETTER_WORDS[upper].slice(0, 4);
  const W = 760, H = 420;
  const posterSize = fitSize(upper, cfg.fontObj, W * 0.4, 300, 'H');
  const inner =
    glyphSVG(upper, { x: W * 0.32, baseline: 370, size: posterSize, style: 'model', font: cfg.fontObj, color: cfg.color ? t.ink : '#222' }) +
    glyphSVG(lower, { x: W * 0.68, baseline: 370, size: posterSize, style: 'hollowbig', font: cfg.fontObj, color: cfg.color ? t.ink2 : '#444' });
  const doodles = shuffled(t.doodles, rnd).slice(0, 3).join(' ');
  return `<svg class="poster-letter" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet">${inner}</svg>
    <div class="poster-words">${words.map(w => pictureCard(w[0], w[1], cfg, 'poster')).join('')}</div>
    <div class="poster-doodles">${doodles}</div>`;
}

const BUILDERS = {
  trace: buildTrace, rainbow: buildRainbow, color: buildColor, dot: buildDot,
  connect: buildConnect, find: buildFind, sounds: buildSounds, allinone: buildAllInOne, poster: buildPoster
};

const INSTRUCTIONS = {
  trace: ch => `Trace each ${ch}, then write your own!`,
  rainbow: ch => `Trace ${ch} in red, orange, yellow, green, blue and purple.`,
  color: ch => `Color the big ${ch} any way you like!`,
  dot: ch => `Dot, stamp or fingerprint your way around ${ch}.`,
  connect: ch => `Connect the dots from 1 to the end to make ${ch}.`,
  find: ch => `Circle every ${ch} you can find.`,
  sounds: ch => `Circle the pictures that begin with ${ch}.`,
  allinone: ch => `Trace it, find it, color it and say it: ${ch}!`,
  poster: ch => `${ch} is for learning — hang me on the wall!`
};

/* ---------- borders ---------- */
function borderHTML(cfg, t, rnd) {
  if (cfg.border === 'doodle') {
    const row = n => Array.from({ length: n }, () => t.doodles[Math.floor(rnd() * t.doodles.length)]).join(' ');
    return `<div class="bd bd-doodle">
      <div class="bd-top">${row(14)}</div><div class="bd-bottom">${row(14)}</div>
      <div class="bd-left">${row(9).split(' ').join('<br>')}</div>
      <div class="bd-right">${row(9).split(' ').join('<br>')}</div>
    </div>`;
  }
  if (cfg.border === 'confetti') {
    const dots = Array.from({ length: 70 }, () => {
      const edge = Math.floor(rnd() * 4);
      const along = rnd() * 100, depth = rnd() * 4.2;
      const pos = edge === 0 ? `top:${depth}%;left:${along}%`
        : edge === 1 ? `bottom:${depth}%;left:${along}%`
          : edge === 2 ? `left:${depth}%;top:${along}%`
            : `right:${depth}%;top:${along}%`;
      const colors = [t.ink, t.ink2, t.accent, t.guide];
      const c = colors[Math.floor(rnd() * colors.length)];
      const s = 6 + rnd() * 10;
      const r = Math.floor(rnd() * 360);
      const round = rnd() > 0.5;
      return `<i style="${pos};width:${s.toFixed(1)}px;height:${s.toFixed(1)}px;background:${c};transform:rotate(${r}deg);border-radius:${round ? '50%' : '2px'}"></i>`;
    }).join('');
    return `<div class="bd bd-confetti">${dots}</div>`;
  }
  if (cfg.border === 'scallop') return `<div class="bd bd-scallop"></div>`;
  if (cfg.border === 'stripe') return `<div class="bd bd-stripe"></div>`;
  if (cfg.border === 'simple') return `<div class="bd bd-simple"></div>`;
  return '';
}

/* ---------- one full sheet ---------- */
function buildSheet(ch, cfg, index) {
  const t = THEMES[cfg.theme];
  const rnd = mulberry32(hashSeed(`${ch}|${cfg.type}|${cfg.letterCase}|${cfg.theme}|${cfg.seed}`));
  const body = BUILDERS[cfg.type](ch, cfg, t, rnd);
  const label = letterLabel(ch, cfg);
  const title = cfg.title && cfg.title.trim() ? esc(cfg.title.trim()) : `Letter ${esc(label)}`;
  const nameLine = cfg.nameLine && cfg.type !== 'poster'
    ? `<div class="name-line"><span>Name <i></i></span><span>Date <i></i></span></div>` : '';
  const footer = cfg.footer
    ? `<div class="ws-foot"><span class="foot-star">${t.doodles[0]}</span>
         <span>${esc(cfg.footerText || 'Great job, super learner!')}</span>
         <span class="foot-star">${t.doodles[1]}</span></div>` : '';

  const vars = cfg.color
    ? `--ink:${t.ink};--ink2:${t.ink2};--accent:${t.accent};--paper:${t.paper};--band:${t.band};--guide:${t.guide};--trace:${t.trace}`
    : `--ink:#222;--ink2:#444;--accent:#666;--paper:#fff;--band:#f4f4f4;--guide:#999;--trace:#c4c4c4`;

  return `<section class="sheet type-${cfg.type} ${cfg.color ? '' : 'inksaver'}" style="${vars}" data-letter="${esc(ch)}" data-index="${index}">
    ${borderHTML(cfg, t, rnd)}
    <div class="sheet-inner">
      <header class="ws-head">
        <div class="ws-title"><span class="ws-badge">${esc(label)}</span><h2>${title}</h2></div>
        ${nameLine}
        <p class="ws-instruction">${INSTRUCTIONS[cfg.type](label)}</p>
      </header>
      <div class="ws-body">${body}</div>
      ${footer}
    </div>
  </section>`;
}

function renderSheets(letters, cfg) {
  return letters.map((ch, i) => buildSheet(ch, cfg, i)).join('');
}
