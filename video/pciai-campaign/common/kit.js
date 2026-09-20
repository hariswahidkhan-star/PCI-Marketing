/* ===========================================================================
   PCI AI campaign films — shared deterministic runtime.

   Every frame is a pure function of t. No timers, no rAF, no Date, no CSS
   transitions or keyframes, no state carried between calls. seek(t) twice with
   the same t paints the same pixels, which is what lets the renderer
   screenshot frame by frame and lets the probe audit the whole timeline before
   a single frame is encoded.

   A film supplies BEATS (id, in, out) and a per-beat FX map. Sizing, the
   ground, the brand furniture, the safe zones and the shot cross-fade live
   here so ten films cannot drift apart.

   The brand is taken from the platform's own styles.css via the repository
   README, not re-invented: ink #0F172A, crimson #C13329, blue #1D4ED8,
   accent #3B82F6, Archivo 800 display at -0.023em, Inter for everything else.
   The signature device is the crimson-to-blue rule under an uppercase,
   letter-spaced eyebrow.
   =========================================================================== */
(function () {
  /* ---- maths ------------------------------------------------------------- */
  const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x);
  const outCubic = x => 1 - Math.pow(1 - x, 3);
  const outExpo  = x => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x));
  const outQuint = x => 1 - Math.pow(1 - x, 5);
  const inOut    = x => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
  const outBack  = x => { const c = 1.70158, c3 = c + 1; return 1 + c3 * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  /* the single primitive everything is built from */
  const seg = (t, a, b, ease = outCubic) => (b <= a ? (t >= b ? 1 : 0) : ease(clamp((t - a) / (b - a))));
  /* rises and falls inside [a,b] — for anything that should not stay lit */
  const pulse = (t, a, b) => Math.sin(Math.PI * clamp((t - a) / Math.max(1e-6, b - a)));

  /* ---- colour ------------------------------------------------------------ */
  const C_INK    = [15, 23, 42];     // #0F172A  the navy ground
  const C_INK2   = [17, 29, 51];     // #111D33  the raised panel
  const C_CRIM   = [193, 51, 41];    // #C13329
  const C_BLUE   = [29, 78, 216];    // #1D4ED8
  const C_ACC    = [59, 130, 246];   // #3B82F6
  const C_WHITE  = [255, 255, 255];
  const C_SOFT   = [185, 198, 218];  // #B9C6DA  body text on navy
  const C_MUTE   = [126, 144, 172];  // #7E90AC  captions, meta
  const mixc = (a, b, p) =>
    `rgb(${Math.round(a[0] + (b[0] - a[0]) * p)},${Math.round(a[1] + (b[1] - a[1]) * p)},${Math.round(a[2] + (b[2] - a[2]) * p)})`;

  /* ---- stage ------------------------------------------------------------- */
  /* One nominal width per aspect, so a 19.2px base unit scales to any output
     size and the same film reads correctly at 1920x1080 and 1080x1920 without
     a second layout. */
  function setupStage({ nominal = { wide: 1920, sq: 1220, tall: 940 }, base = 19.2 } = {}) {
    const Q = new URLSearchParams(location.search);
    const W = +(Q.get('w') || 1920), H = +(Q.get('h') || 1080);
    const R = W / H;
    const ASPECT = R >= 1.4 ? 'wide' : R >= 0.85 ? 'sq' : 'tall';
    const stage = document.getElementById('stage');
    stage.style.width = W + 'px';
    stage.style.height = H + 'px';
    stage.classList.add(ASPECT);
    const SS = (W / nominal[ASPECT]) * base;
    document.documentElement.style.setProperty('--s', SS.toFixed(4));
    return { W, H, R, ASPECT, SS, CC: Q.get('cc') !== '0' };
  }

  /* A faint mesh so the navy is not dead flat. Drawn once — it never animates,
     so it costs nothing per frame. */
  function drawMesh(W, H, SS) {
    const m = document.getElementById('mesh'); if (!m) return;
    const step = SS * 5, ns = [];
    for (let x = 0; x <= W; x += step) ns.push(`<line x1="${x.toFixed(1)}" y1="0" x2="${x.toFixed(1)}" y2="${H}"/>`);
    for (let y = 0; y <= H; y += step) ns.push(`<line x1="0" y1="${y.toFixed(1)}" x2="${W}" y2="${y.toFixed(1)}"/>`);
    m.setAttribute('viewBox', `0 0 ${W} ${H}`);
    m.innerHTML = `<g stroke="#18243C" stroke-width="1">${ns.join('')}</g>`;
  }

  /* ---- kinetic type ------------------------------------------------------ */
  /* Split an element into word spans once, so a reveal can be driven per word
     from t alone. Idempotent: calling it twice does not re-split.

     It walks the DOM rather than reading textContent, because textContent
     flattens the markup: an explicit <br> disappeared and glued the words on
     either side into one oversized token that broke out of the safe area, and
     every inline accent colour was silently dropped at the same time. Line
     breaks are preserved and each word inherits the class of the element it
     came from. */
  function words(el) {
    if (!el) return [];
    if (el.dataset.split === '1') return [...el.querySelectorAll('.w > i')];
    const frag = document.createDocumentFragment();
    const emit = (text, cls) => {
      for (const w of text.split(/\s+/)) {
        if (!w) continue;
        const s = document.createElement('span'); s.className = 'w';
        const i = document.createElement('i'); i.textContent = w;
        if (cls) i.className = cls;
        s.appendChild(i);
        frag.appendChild(s);
        frag.appendChild(document.createTextNode(' '));
      }
    };
    const walk = (node, cls) => {
      for (const ch of [...node.childNodes]) {
        if (ch.nodeType === 3) emit(ch.textContent, cls);
        else if (ch.nodeName === 'BR') frag.appendChild(document.createElement('br'));
        else if (ch.nodeType === 1) walk(ch, ch.className || cls);
      }
    };
    walk(el, '');
    el.textContent = '';
    el.appendChild(frag);
    el.dataset.split = '1';
    return [...el.querySelectorAll('.w > i')];
  }

  /* Reveal words on a stagger. Each word rises out of its own clip box, which
     is what makes kinetic type read as typeset rather than as items sliding. */
  function revealWords(el, t, t0, { stagger = 0.045, dur = 0.42, rise = 1.0 } = {}) {
    const ws = words(el);
    ws.forEach((w, i) => {
      const p = seg(t, t0 + i * stagger, t0 + i * stagger + dur, outExpo);
      w.style.transform = `translateY(${((1 - p) * rise * 100).toFixed(2)}%)`;
      w.style.opacity = p.toFixed(3);
    });
    return ws.length;
  }

  /* ---- the signature device ---------------------------------------------- */
  /* The crimson-to-blue rule, wiped in from the left. Every film uses it and no
     film draws its own, so the one brand device stays identical across ten. */
  function rule(el, t, t0, { dur = 0.55 } = {}) {
    if (!el) return;
    const p = seg(t, t0, t0 + dur, outExpo);
    el.style.transform = `scaleX(${p.toFixed(4)})`;
    el.style.opacity = p > 0 ? '1' : '0';
  }

  /* ---- counters ---------------------------------------------------------- */
  /* A number that counts up deterministically. Rounded per frame from t, never
     accumulated, so scrubbing backwards shows the same value as scrubbing in. */
  function countTo(el, t, t0, t1, value, { prefix = '', suffix = '' } = {}) {
    if (!el) return;
    const p = seg(t, t0, t1, outQuint);
    el.textContent = prefix + Math.round(value * p).toLocaleString('en-GB') + suffix;
  }

  /* ---- brand furniture --------------------------------------------------- */
  /* The logo is on every frame of every film. It gets its own fast ramp rather
     than riding the common one, because on the common ramp it was still at
     zero for the first frames — and a brand film whose first frames carry no
     brand is the one failure nobody notices until it is published. */
  function furniture(t, DUR, opts = {}) {
    const E = furniture._e || (furniture._e = {
      brand: document.getElementById('brandbar'),
      bar:   document.getElementById('bar'),
      foot:  document.getElementById('foot'),
    });
    const f = clamp(seg(t, 0.02, 0.40)).toFixed(3);
    if (E.brand) E.brand.style.opacity = f;
    if (E.foot)  E.foot.style.opacity = clamp(seg(t, 0.30, 0.90) * (opts.footFade ?? 1)).toFixed(3);
    if (E.bar)   E.bar.style.transform = `scaleX(${clamp(t / DUR).toFixed(4)})`;
  }

  /* ---- shot switching ---------------------------------------------------- */
  /* Only the live beat is painted. Everything else is display:none, so a probe
     measuring overflow never sees a hidden beat's geometry and the renderer
     never composites eleven layers to show one. */
  function activate(BEATS, t) {
    let live = BEATS[0];
    for (const b of BEATS) if (t >= b.in) live = b;
    for (const b of BEATS) {
      const el = document.getElementById(b.id);
      if (!el) continue;
      const on = b === live;
      el.style.display = on ? '' : 'none';
      if (on) {
        // a short lift into each beat, so cuts land rather than jump
        const p = seg(t, b.in, b.in + 0.22, outExpo);
        el.style.opacity = p.toFixed(3);
        el.style.transform = `scale(${(0.995 + 0.005 * p).toFixed(4)})`;
      }
    }
    return live;
  }

  window.PCI = {
    clamp, seg, pulse, outCubic, outExpo, outQuint, inOut, outBack, mixc,
    C_INK, C_INK2, C_CRIM, C_BLUE, C_ACC, C_WHITE, C_SOFT, C_MUTE,
    setupStage, drawMesh, words, revealWords, rule, countTo, furniture, activate,
  };
})();
