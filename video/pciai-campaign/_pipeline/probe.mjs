/**
 * Audit a campaign film across its whole timeline before a frame is encoded.
 *
 *   node probe.mjs 1080 1920 r1
 *
 * Checks, every 0.25 s:
 *   - page errors and console errors
 *   - anything painted outside the stage
 *   - text clipped by its own container
 *   - dead element handles (a null in a film's cache makes a whole beat
 *     silently stop animating while every layout check still passes — that
 *     shipped twice on an earlier project before this check existed)
 *   - SAFE ZONES on vertical: Instagram, TikTok and Shorts all paint their own
 *     UI over the frame. Anything that must be read has to stay clear of it,
 *     and a caption hidden behind the platform's own caption is invisible in a
 *     way no desktop preview ever shows you.
 */
import { chromium } from 'playwright';
import { existsSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

function findChrome() {
  if (process.env.CHROME_PATH && existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH;
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  if (existsSync(root)) for (const d of readdirSync(root).filter(d => d.startsWith('chromium-')).sort().reverse()) {
    const exe = path.join(root, d, 'chrome-linux', 'chrome');
    if (existsSync(exe)) return exe;
  }
}

const W = +process.argv[2], H = +process.argv[3], tag = process.argv[4] || 'probe';
const TALL = W / H < 0.70;   // 9:16 only. 4:5 (0.800) and 1:1 carry no platform chrome.

/* Reserved bands as a fraction of height/width. Platforms move their UI, so
   these are deliberately generous: the cost of a wide margin is a slightly
   smaller headline, the cost of a narrow one is an unreadable post. */
/* Vertical: the box that satisfies Meta's unified spec and Shorts at once on a
   1080x1920 canvas — critical content inside y 270..1250, x 65..1015. The
   bottom 35% is decorative only: it carries the caption, the handle, the audio
   strip and the action rail. This is much stricter than it looks reasonable to
   be, and it is the single most common way a good vertical edit ships
   unreadable.
   4:5 is LinkedIn's strongest single format and has no platform chrome over
   it, so it only needs a print-style margin. */
const SAFE = TALL
  ? { top: 270 / 1920, bottom: 1 - 1250 / 1920, left: 65 / 1080, right: 1 - 1015 / 1080 }
  : { top: 0.035, bottom: 0.035, left: 0.035, right: 0.035 };

const url = pathToFileURL(path.resolve('scene.html'));
url.searchParams.set('w', W); url.searchParams.set('h', H); url.searchParams.set('cc', '1');

const errs = [], out = [], clipped = [], unsafe = [], collide = [];
const browser = await chromium.launch({ executablePath: findChrome(), args: ['--force-color-profile=srgb', '--font-render-hinting=none', '--hide-scrollbars'] });
const pg = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
pg.on('pageerror', e => errs.push('pageerror: ' + e.message));
pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
await pg.goto(url.href, { waitUntil: 'load' });
await pg.evaluate(() => document.fonts.ready);
await pg.waitForTimeout(150);

const DUR = await pg.evaluate(() => window.__DUR);
if (!DUR) { console.log(`${tag}: FAIL — scene exposes no __DUR`); await browser.close(); process.exit(1); }

/* dead handles: a null cached element means a beat animator no-ops */
const dead = await pg.evaluate(() => {
  const reg = window.__EL; if (!reg) return ['__EL not exposed — cannot audit for dead handles'];
  const bad = [];
  for (const [k, v] of Object.entries(reg)) {
    if (Array.isArray(v)) { v.forEach((x, i) => { if (!x) bad.push(`${k}[${i}]`); }); if (!v.length) bad.push(`${k} (empty)`); }
    else if (!v) bad.push(k);
  }
  return bad;
});
if (dead.length) errs.push('dead element handles (beat animators will no-op): ' + dead.join(', '));

for (let t = 0; t <= DUR + 0.001; t = +(t + 0.25).toFixed(2)) {
  await pg.evaluate(tt => window.seek(tt), Math.min(t, DUR));
  const r = await pg.evaluate(({ SAFE }) => {
    const st = document.getElementById('stage'), sb = st.getBoundingClientRect();
    const over = [], clip = [], un = [];
    const SKIP = /^(wash|mesh|stage|barwrap|bar)$/;
    const safeBox = {
      top: sb.top + sb.height * SAFE.top, bottom: sb.bottom - sb.height * SAFE.bottom,
      left: sb.left + sb.width * SAFE.left, right: sb.right - sb.width * SAFE.right,
    };
    /* What matters is where an element is PAINTED, not where its box is. A
       sweep inside a card with overflow:hidden has a box wider than the card
       and paints none of it — measuring the box reports a violation that does
       not exist on screen. So each rect is intersected with every clipping
       ancestor before it is judged. */
    const painted = (el) => {
      let r = el.getBoundingClientRect();
      for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
        const pcs = getComputedStyle(p);
        if (!/hidden|clip|auto|scroll/.test(pcs.overflow + pcs.overflowX + pcs.overflowY)) continue;
        const pr = p.getBoundingClientRect();
        r = { top: Math.max(r.top, pr.top), bottom: Math.min(r.bottom, pr.bottom),
              left: Math.max(r.left, pr.left), right: Math.min(r.right, pr.right) };
      }
      return { ...r, width: r.right - r.left, height: r.bottom - r.top };
    };

    for (const el of document.querySelectorAll('#stage *')) {
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || +cs.opacity < 0.05 || cs.display === 'none') continue;
      if (SKIP.test(el.id)) continue;
      if (el.closest('[data-decor]')) continue;
      const b = painted(el);
      if (b.width < 1 || b.height < 1) continue;
      if (b.right > sb.right + 2 || b.left < sb.left - 2 || b.bottom > sb.bottom + 2 || b.top < sb.top - 2)
        over.push(`${el.className || el.tagName}`);
      // only leaf text is safe-zone checked; a full-bleed wrapper legitimately spans the frame
      // A painted container with no text of its own — a card, a panel, a rule
      // — was invisible to this check, because only leaf text was tested. Its
      // text children could all sit inside the box while the box it is drawn
      // in hangs outside. So anything that actually paints is checked too.
      const paints = cs.backgroundImage !== 'none'
        || (cs.backgroundColor && !/^rgba\(0, 0, 0, 0\)$|^transparent$/.test(cs.backgroundColor))
        || (parseFloat(cs.borderTopWidth) + parseFloat(cs.borderLeftWidth)
          + parseFloat(cs.borderBottomWidth) + parseFloat(cs.borderRightWidth)) > 0.5;
      if (paints && !el.classList.contains('beat')
          && (b.top < safeBox.top - 1 || b.bottom > safeBox.bottom + 1
           || b.left < safeBox.left - 1 || b.right > safeBox.right + 1))
        un.push(`<${el.id ? '#'+el.id : (el.className||el.tagName).toString().split(' ')[0]}> painted outside`);

      const txt = el.textContent && el.textContent.trim();
      const leaf = txt && ![...el.children].some(c => c.textContent && c.textContent.trim());
      if (leaf) {
        if (b.top < safeBox.top - 1 || b.bottom > safeBox.bottom + 1 || b.left < safeBox.left - 1 || b.right > safeBox.right + 1)
          un.push(`"${txt.slice(0, 28)}"`);
        /* Text only counts as clipped if something actually clips it.
           Archivo 800's content box is ~1.084 x its font-size, so any display
           type set tighter than that reports scrollHeight > clientHeight —
           but with overflow visible the glyphs paint in full and nothing is
           lost. Testing the overflow alone made the check demand a looser
           line-height than the design wants, and two films had already been
           loosened to satisfy it before the check itself was the suspect.
           .w is excluded for the opposite reason: it clips deliberately, and
           that clip is the mechanism of the word reveal. */
        let clipper = null;
        for (let p = el; p && p.id !== 'stage'; p = p.parentElement) {
          const c = getComputedStyle(p);
          if (/hidden|clip|auto|scroll/.test(c.overflow + c.overflowX + c.overflowY)) { clipper = p; break; }
        }
        const deliberate = el.classList.contains('w') || el.closest('.w');
        if (clipper && !deliberate
            && (el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 2))
          clip.push(`"${txt.slice(0, 28)}" clipped by ${clipper.id || clipper.className}`);
      }
    }
    /* Content colliding with the brand bar or the footer is invisible to every
       check above: the chrome is inside the safe box and so is the content, so
       both pass while overlapping each other on screen. A beat that grows one
       line is all it takes, and it fails silently in a still you did not
       happen to render. */
    const hit = [];
    const chrome = [document.getElementById('brandbar'), document.getElementById('foot'),
                    document.getElementById('ccbox')].filter(Boolean);
    for (const el of document.querySelectorAll('.beat')) {
      if (getComputedStyle(el).display === 'none') continue;
      for (const kid of el.querySelectorAll('*')) {
        const kcs = getComputedStyle(kid);
        if (kcs.visibility === 'hidden' || +kcs.opacity < 0.05 || kcs.display === 'none') continue;
        const k = kid.getBoundingClientRect();
        if (k.width < 1 || k.height < 1) continue;
        const t = (kid.textContent || '').trim();
        if (t && [...kid.children].some(c => (c.textContent || '').trim())) continue; // leaves only
        for (const c of chrome) {
          const r = c.getBoundingClientRect();
          if (k.left < r.right && k.right > r.left && k.top < r.bottom && k.bottom > r.top)
            hit.push(`"${(t || kid.className || kid.tagName).slice(0, 24)}" over #${c.id}`);
        }
      }
    }

    return { over, clip, un, hit };
  }, { SAFE });
  if (r.over.length) out.push(`t=${t}: ${[...new Set(r.over)].join(', ')}`);
  if (r.clip.length) clipped.push(`t=${t}: ${[...new Set(r.clip)].join(', ')}`);
  if (r.un.length) unsafe.push(`t=${t}: ${[...new Set(r.un)].join(', ')}`);
  if (r.hit.length) collide.push(`t=${t}: ${[...new Set(r.hit)].join(', ')}`);
}
await browser.close();

const show = (name, a) => console.log(`${tag} ${name}: ` + (a.length ? `${a.length} —\n  ` + a.slice(0, 8).join('\n  ') : 'none'));
console.log(`${tag} ${W}x${H} · ${DUR}s`);
show('errors', errs);
show('overflow', out);
show('clipped text', clipped);
show(TALL ? 'outside reels safe area' : 'outside safe margin', unsafe);
show('content over brand bar / footer', collide);
process.exit(errs.length || out.length || clipped.length || unsafe.length || collide.length ? 1 : 0);
