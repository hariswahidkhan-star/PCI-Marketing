/* ===========================================================================
   Certuvo feature films — the shared deterministic runtime.

   Every treatment is a pure function of t. Nothing animates on a clock, nothing
   holds state between frames, and seek(t) called twice with the same t paints
   the same pixels — which is what lets the renderer screenshot frame by frame
   and lets the probe audit the whole timeline before a single frame is encoded.

   A treatment supplies: SHOTS (id, label, in, out), a per-shot FX map, and an
   optional reveal list. Everything else — sizing, furniture, the wash, the
   cross-fade between shots — is here.
   =========================================================================== */

(function(){
/* ---- maths ---------------------------------------------------------------- */
const clamp = (x, a = 0, b = 1) => x < a ? a : x > b ? b : x;
const outCubic = x => 1 - Math.pow(1 - x, 3);
const outExpo  = x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x);
const outQuint = x => 1 - Math.pow(1 - x, 5);
const inOut    = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const outBack  = x => { const c = 1.70158, c3 = c + 1; return 1 + c3 * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
/* seg(t, a, b) -> 0..1 across [a,b], eased. The single primitive everything uses. */
const seg = (t, a, b, ease = outCubic) => b <= a ? (t >= b ? 1 : 0) : ease(clamp((t - a) / (b - a)));
/* a one-shot pulse that rises and falls inside [a,b] */
const pulse = (t, a, b) => Math.sin(Math.PI * clamp((t - a) / Math.max(1e-6, b - a)));

/* ---- colour --------------------------------------------------------------- */
const C_BLUE = [41, 95, 237], C_BLUE3 = [108, 155, 255], C_RED = [229, 69, 63];
const C_WHITE = [255, 255, 255], C_SKEL = [231, 236, 247], C_LINE = [230, 235, 245];
const C_LINE2 = [216, 224, 240], C_MUTE = [154, 164, 178], C_TINT = [238, 243, 255];
const C_INK = [11, 18, 32], C_SUB = [75, 85, 99];
const mixc = (a, b, p) => `rgb(${Math.round(a[0] + (b[0] - a[0]) * p)},${Math.round(a[1] + (b[1] - a[1]) * p)},${Math.round(a[2] + (b[2] - a[2]) * p)})`;

/* ---- stage ---------------------------------------------------------------- */
function setupStage({ nominal = { wide: 1920, sq: 1350, tall: 1180 }, base = 19.2 } = {}){
  const Q = new URLSearchParams(location.search);
  const W = +(Q.get('w') || 1920), H = +(Q.get('h') || 1080);
  const R = W / H, ASPECT = R >= 1.40 ? 'wide' : (R >= 0.85 ? 'sq' : 'tall');
  const N = nominal[ASPECT];
  const stage = document.getElementById('stage');
  stage.style.width = W + 'px'; stage.style.height = H + 'px';
  stage.classList.add(ASPECT);
  const SS = W / N * base;
  document.documentElement.style.setProperty('--s', SS.toFixed(4));
  return { W, H, ASPECT, SS, CC: Q.get('cc') !== '0' };
}

/* a faint square mesh, drawn once, so the white sheet is not dead flat */
function drawMesh(W, H, SS){
  const m = document.getElementById('mesh'); if (!m) return;
  const step = SS * 4.5, ns = [];
  for (let x = 0; x <= W; x += step) ns.push(`<line x1="${x}" y1="0" x2="${x}" y2="${H}"/>`);
  for (let y = 0; y <= H; y += step) ns.push(`<line x1="0" y1="${y}" x2="${W}" y2="${y}"/>`);
  m.setAttribute('viewBox', `0 0 ${W} ${H}`);
  m.innerHTML = `<g stroke="#EDF1FA" stroke-width="1">${ns.join('')}</g>`;
}

/* ---- furniture: logo, counter, progress. On every frame, by instruction. --- */
function furniture(t, DUR, { label, index, total, fade = 1 }){
  const E = furniture._e || (furniture._e = {
    brand: document.getElementById('brandbar'), count: document.getElementById('count'),
    n: document.querySelector('#count .n'), c: document.querySelector('#count .c'),
    bar: document.getElementById('bar'), barwrap: document.getElementById('barwrap'),
    fl: document.getElementById('footl'), fr: document.getElementById('footr'),
  });
  // The logo is required on EVERY frame, so the brandbar gets its own faster
  // ramp than the rest of the furniture. On the common ramp it was still at
  // zero for the first few frames of every film, which broke the one rule the
  // brief states twice.
  const f = clamp(seg(t, 0.15, 1.0) * fade).toFixed(3);
  const fb = clamp(seg(t, 0.02, 0.45) * fade).toFixed(3);
  if (E.brand) E.brand.style.opacity = fb;
  for (const el of [E.count, E.barwrap, E.fl, E.fr]) if (el) el.style.opacity = f;
  if (E.n) E.n.textContent = String(index).padStart(2, '0') + ' / ' + String(total).padStart(2, '0');
  if (E.c) E.c.textContent = label;
  if (E.bar) E.bar.style.transform = `scaleX(${(t / DUR).toFixed(4)})`;
}

/* the ambient wash — slow, never noticeable, keeps the white from going flat */
function wash(t, DUR, warm = 0){
  const a = document.getElementById('wash'), b = document.getElementById('wash2');
  const d = t / DUR;
  if (a){ a.style.transform = `translate(${(-14 + d * 32).toFixed(2)}%, ${(-12 + Math.sin(d * 6.4) * 9).toFixed(2)}%) scale(${(1.04 + d * .18).toFixed(3)})`;
          a.style.opacity = (0.55 + 0.45 * (1 - warm)).toFixed(3); }
  if (b){ b.style.transform = `translate(${(28 - d * 24).toFixed(2)}%, ${(20 - Math.cos(d * 5.3) * 11).toFixed(2)}%) scale(${(1.12 - d * .08).toFixed(3)})`;
          b.style.opacity = (0.18 + 0.82 * warm).toFixed(3); }
}

/* ---- shots: cross-fade + a small lateral push, exactly as the films use ---- */
function paintShots(t, SHOTS, DUR, XF = 0.45, push = 1.3){
  let best = -1, cur = SHOTS[0];
  const out = [];
  for (const s of SHOTS){
    const fi = s.in <= 0 ? 1 : seg(t, s.in, s.in + XF);
    const fo = s.out >= DUR ? 1 : 1 - seg(t, s.out - XF, s.out);
    const o = fi * fo;
    const el = document.getElementById(s.id);
    if (el){
      el.style.opacity = o.toFixed(3);
      el.style.visibility = o < 0.002 ? 'hidden' : 'visible';
      const dx = (1 - fi) * push - (s.out >= DUR ? 0 : (1 - fo) * push);
      el.style.transform = `translateX(${dx.toFixed(3)}%)`;
    }
    if (o > best){ best = o; cur = s; }
    out.push({ shot: s, o });
  }
  return { wts: out, cur };
}

/* ---- reveals: [selector, secondsAfterShotStart, stagger] ------------------- */
function buildReveals(SHOTS, CUES){
  const A = [];
  for (const s of SHOTS){
    const root = document.getElementById(s.id); if (!root) continue;
    const seen = new Map();
    for (const [sel, d, stagger = 0] of (CUES[s.id] || [])){
      const els = [...root.querySelectorAll(sel)];
      if (stagger === 0 && els.length > 1){
        const k = seen.get(sel) || 0; seen.set(sel, k + 1);
        if (els[k]) A.push({ el: els[k], start: s.in + d });
      } else {
        els.forEach((el, i) => A.push({ el, start: s.in + d + i * stagger }));
      }
    }
  }
  return A;
}
function paintReveals(t, ANIM, { rise = 0.62, lift = 0.9, scale = 0 } = {}){
  for (const a of ANIM){
    const p = seg(t, a.start, a.start + rise, outExpo);
    a.el.style.opacity = p.toFixed(3);
    const sc = scale ? ` scale(${(1 - scale + scale * p).toFixed(4)})` : '';
    a.el.style.transform = `translateY(${((1 - p) * lift).toFixed(3)}em)${sc}`;
  }
}

/* ---- parts ---------------------------------------------------------------- */
function fillChipField(el, n, cols){
  if (!el) return [];
  el.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
  const f = document.createDocumentFragment();
  for (let i = 0; i < n; i++) f.appendChild(document.createElement('i'));
  el.appendChild(f);
  return [...el.children];
}
/* light a chip field left-to-right with a row lag; p is 0..1 over the whole field */
function paintChipField(chips, cols, u, start, per, hold = 0.28){
  chips.forEach((c, i) => {
    const col = i % cols, row = (i / cols) | 0;
    const at = start + col * per + row * per * 0.48;
    const p = seg(u, at, at + hold, outCubic);
    c.style.backgroundColor = p > 0.5 ? mixc(C_SKEL, C_BLUE, (p - 0.5) * 2 * 0.85) : 'rgb(231,236,247)';
    c.style.transform = `scaleY(${(0.6 + 0.4 * p).toFixed(3)})`;
  });
}
function setRing(ring, p, { colour = null } = {}){
  const fill = ring.querySelector('.rfill'); if (!fill) return;
  const r = +fill.getAttribute('r'), C = 2 * Math.PI * r;
  fill.setAttribute('stroke-dasharray', C.toFixed(2));
  fill.setAttribute('stroke-dashoffset', (C * (1 - clamp(p))).toFixed(2));
  if (colour) fill.style.stroke = colour;
}
function setWave(bars, u, live, speed = 5.2){
  bars.forEach((b, i) => { b.style.height = (22 + 66 * Math.abs(Math.sin(u * speed + i * 0.8)) * live).toFixed(1) + '%'; });
}
function setBeam(beam, u, a, b, { width = 640, from = -40 } = {}){
  if (!beam) return;
  const sw = seg(u, a, b, inOut);
  const on = seg(u, a, a + 0.3) * (1 - seg(u, b - 0.2, b + 0.25));
  beam.style.opacity = on.toFixed(3);
  beam.style.transform = `translateX(${(from + sw * width).toFixed(1)}%)`;
}
/* draw a polyline path progressively; pts are [x,y] in viewBox units */
function pathTo(pts, frac){
  const n = pts.length, last = 1 + clamp(frac) * (n - 1);
  const k = Math.floor(last), f = last - k;
  const out = pts.slice(0, Math.max(2, k + 1)).map(p => p.slice());
  if (k > 0 && k < n){
    const a = pts[k - 1], b = pts[k];
    out[out.length - 1] = [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f];
  }
  return { d: 'M' + out.map(p => `${p[0].toFixed(1)},${p[1].toFixed(1)}`).join('L'), end: out[out.length - 1] };
}

/* ---- captions ------------------------------------------------------------- */
function paintCaptions(t, CAPS, { box, wrap, on }){
  if (!on || !CAPS || !CAPS.length){ if (wrap) wrap.style.opacity = '0'; return; }
  const cue = CAPS.find(c => t >= c[0] - 0.14 && t <= c[1] + 0.14);
  if (!cue){ wrap.style.opacity = '0'; return; }
  const p = Math.min(seg(t, cue[0] - 0.14, cue[0] + 0.16), 1 - seg(t, cue[1] - 0.02, cue[1] + 0.14));
  wrap.style.opacity = clamp(p).toFixed(3);
  if (box.__txt !== cue[2]){ box.__txt = cue[2]; box.textContent = cue[2]; }
  box.style.transform = `translateY(${((1 - clamp(p)) * 0.4).toFixed(3)}em)`;
}


/* one global, so a plain <script src> works from a file:// page */
window.CE = { clamp, outCubic, outExpo, outQuint, inOut, outBack, seg, pulse, C_BLUE, C_BLUE3, C_RED, C_WHITE, C_SKEL, C_LINE, C_LINE2, C_MUTE, C_TINT, C_INK, C_SUB, mixc, setupStage, drawMesh, furniture, wash, paintShots, buildReveals, paintReveals, fillChipField, paintChipField, setRing, setWave, setBeam, pathTo, paintCaptions };
})();
