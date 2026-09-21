/* =============================================================
   ABC Fun Factory — UI wiring
   ============================================================= */
(function () {
  const $ = sel => document.querySelector(sel);
  const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
  const VOWELS = ['A', 'E', 'I', 'O', 'U'];
  const STORE_KEY = 'abc-fun-factory.v1';

  const state = {
    letters: ['A'],
    type: 'trace',
    theme: 'jungle',
    letterCase: 'both',
    font: 'school',
    traceStyle: 'dotted',
    lines: 'threeline',
    border: 'confetti',
    rows: 4,
    paper: 'letter',
    title: '',
    footerText: '',
    color: true,
    nameLine: true,
    footer: true,
    pictures: true,
    seed: 1,
    zoom: 0 /* 0 = fit to stage */
  };

  /* ---------- build the dropdowns from the data tables ---------- */
  function fillSelect(el, entries, selected) {
    el.innerHTML = entries.map(([v, label]) =>
      `<option value="${v}"${v === selected ? ' selected' : ''}>${label}</option>`).join('');
  }
  function buildOptions() {
    fillSelect($('#type'), Object.entries(WORKSHEET_TYPES).map(([k, v]) => [k, v.name]), state.type);
    fillSelect($('#theme'), Object.entries(THEMES).map(([k, v]) => [k, v.name]), state.theme);
    fillSelect($('#font'), Object.entries(FONTS).map(([k, v]) => [k, v.name]), state.font);
    fillSelect($('#border'), Object.entries(BORDERS), state.border);
  }

  /* ---------- letter picker ---------- */
  function buildLetterGrid() {
    $('#letterGrid').innerHTML = ALPHABET.map(ch =>
      `<button type="button" class="letter-btn" data-letter="${ch}">${ch}</button>`).join('');
  }
  function paintLetterGrid() {
    document.querySelectorAll('.letter-btn').forEach(b => {
      b.classList.toggle('on', state.letters.includes(b.dataset.letter));
    });
    const n = state.letters.length;
    $('#letterCount').textContent = n === 0
      ? 'Pick at least one letter to see a worksheet'
      : `${n} letter${n === 1 ? '' : 's'} selected`;
  }

  /* ---------- form <-> state ---------- */
  const FIELDS = ['type', 'theme', 'letterCase', 'font', 'traceStyle', 'lines', 'border', 'rows', 'paper', 'title', 'footerText'];
  const SWITCHES = ['color', 'nameLine', 'footer', 'pictures'];

  function syncFormFromState() {
    FIELDS.forEach(k => { const el = $('#' + k); if (el) el.value = state[k]; });
    SWITCHES.forEach(k => { const el = $('#' + k); if (el) el.checked = !!state[k]; });
    $('#typeBlurb').textContent = WORKSHEET_TYPES[state.type].blurb;
  }
  function readForm() {
    FIELDS.forEach(k => { const el = $('#' + k); if (el) state[k] = el.value; });
    SWITCHES.forEach(k => { const el = $('#' + k); if (el) state[k] = el.checked; });
    state.rows = parseInt(state.rows, 10) || 4;
  }

  /* ---------- paper size drives @page ---------- */
  let pageStyle = document.createElement('style');
  document.head.appendChild(pageStyle);
  function applyPaper() {
    const size = state.paper === 'a4' ? 'A4 portrait' : 'Letter portrait';
    pageStyle.textContent = `@page { size: ${size}; margin: 0; }`;
    $('#sheets').classList.toggle('a4', state.paper === 'a4');
  }

  /* ---------- preview zoom ---------- */
  function applyZoom() {
    const stage = $('#sheets');
    const sheetW = (state.paper === 'a4' ? 8.27 : 8.5) * 96;
    const avail = stage.parentElement.clientWidth - 8;
    const fit = Math.min(1, avail / sheetW);
    const z = state.zoom > 0 ? state.zoom : fit;
    stage.style.zoom = z;
    $('#zoomLabel').textContent = state.zoom > 0 ? Math.round(z * 100) + '%' : 'Fit';
  }

  /* ---------- render ---------- */
  function cfg() {
    return Object.assign({}, state, { fontObj: FONTS[state.font] });
  }
  function render() {
    const sheets = $('#sheets');
    if (!state.letters.length) {
      sheets.innerHTML = `<p class="hint" style="padding:60px 0">👆 Choose a letter to build a worksheet.</p>`;
      $('#stageInfo').textContent = '0 pages';
      return;
    }
    const letters = ALPHABET.filter(ch => state.letters.includes(ch));
    sheets.innerHTML = renderSheets(letters, cfg());
    $('#stageInfo').textContent = `${letters.length} page${letters.length === 1 ? '' : 's'} · ${WORKSHEET_TYPES[state.type].name.replace(/^\S+\s/, '')}`;
    applyPaper();
    applyZoom();
    save();
  }

  /* ---------- persistence ---------- */
  function save() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch (e) { /* private mode */ }
  }
  function load() {
    try {
      const raw = localStorage.getItem(STORE_KEY);
      if (!raw) return;
      const saved = JSON.parse(raw);
      Object.keys(state).forEach(k => { if (k in saved) state[k] = saved[k]; });
      if (!Array.isArray(state.letters)) state.letters = ['A'];
      if (!WORKSHEET_TYPES[state.type]) state.type = 'trace';
      if (!THEMES[state.theme]) state.theme = 'jungle';
      if (!FONTS[state.font]) state.font = 'school';
      if (!BORDERS[state.border]) state.border = 'confetti';
    } catch (e) { /* ignore bad storage */ }
  }

  /* ---------- events ---------- */
  function wire() {
    $('#controls').addEventListener('change', () => { readForm(); syncFormFromState(); render(); });
    $('#controls').addEventListener('input', e => {
      if (e.target.type === 'text') { readForm(); render(); }
    });
    $('#controls').addEventListener('submit', e => e.preventDefault());

    $('#letterGrid').addEventListener('click', e => {
      const btn = e.target.closest('.letter-btn');
      if (!btn) return;
      const ch = btn.dataset.letter;
      const i = state.letters.indexOf(ch);
      if (i > -1) state.letters.splice(i, 1); else state.letters.push(ch);
      paintLetterGrid(); render();
    });

    document.querySelectorAll('[data-pick]').forEach(btn => {
      btn.addEventListener('click', () => {
        const p = btn.dataset.pick;
        state.letters =
          p === 'all' ? ALPHABET.slice() :
          p === 'vowels' ? VOWELS.slice() :
          p === 'consonants' ? ALPHABET.filter(c => !VOWELS.includes(c)) :
          p === 'first10' ? ALPHABET.slice(0, 10) : [];
        paintLetterGrid(); render();
      });
    });

    $('#btnShuffle').addEventListener('click', () => { state.seed = Math.floor(Math.random() * 1e9); render(); });
    $('#btnPrint').addEventListener('click', () => { applyPaper(); window.print(); });

    $('#zoomIn').addEventListener('click', () => {
      const stage = $('#sheets');
      state.zoom = Math.min(2, (parseFloat(stage.style.zoom) || 1) + 0.15);
      applyZoom();
    });
    $('#zoomOut').addEventListener('click', () => {
      const stage = $('#sheets');
      const next = (parseFloat(stage.style.zoom) || 1) - 0.15;
      state.zoom = next <= 0.3 ? 0 : next;
      applyZoom();
    });

    let raf;
    window.addEventListener('resize', () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(applyZoom); });

    document.addEventListener('keydown', e => {
      if (e.target.matches('input, select, textarea')) return;
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'p') return; /* let the browser print */
      if (e.key.toLowerCase() === 'r') { state.seed = Math.floor(Math.random() * 1e9); render(); }
    });
  }

  /* ---------- go ---------- */
  function init() {
    load();
    buildOptions();
    buildLetterGrid();
    syncFormFromState();
    paintLetterGrid();
    wire();
    render();
    /* re-render once webfonts land so letter metrics are right */
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { clearGlyphCache(); render(); });
  }
  document.addEventListener('DOMContentLoaded', init);
})();
