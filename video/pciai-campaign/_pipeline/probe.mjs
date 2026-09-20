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

const errs = [], out = [], clipped = [], unsafe = [];
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
    const SKIP = /^(wash|mesh|stage|barwrap)$/;
    const safeBox = {
      top: sb.top + sb.height * SAFE.top, bottom: sb.bottom - sb.height * SAFE.bottom,
      left: sb.left + sb.width * SAFE.left, right: sb.right - sb.width * SAFE.right,
    };
    for (const el of document.querySelectorAll('#stage *')) {
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || +cs.opacity < 0.05 || cs.display === 'none') continue;
      if (SKIP.test(el.id)) continue;
      if (el.closest('[data-decor]')) continue;
      const b = el.getBoundingClientRect();
      if (b.width < 1 || b.height < 1) continue;
      if (b.right > sb.right + 2 || b.left < sb.left - 2 || b.bottom > sb.bottom + 2 || b.top < sb.top - 2)
        over.push(`${el.className || el.tagName}`);
      // only leaf text is safe-zone checked; a full-bleed wrapper legitimately spans the frame
      const txt = el.textContent && el.textContent.trim();
      const leaf = txt && ![...el.children].some(c => c.textContent && c.textContent.trim());
      if (leaf) {
        if (b.top < safeBox.top - 1 || b.bottom > safeBox.bottom + 1 || b.left < safeBox.left - 1 || b.right > safeBox.right + 1)
          un.push(`"${txt.slice(0, 28)}"`);
        // .w is the word-reveal box: overflow:hidden is the mechanism that
        // makes a word rise out of its own clip, so mid-reveal it is supposed
        // to be clipped. Everything else that overflows its box is a fault.
        const deliberate = el.classList.contains('w') || el.closest('.w');
        if (!deliberate && (el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 2))
          clip.push(`"${txt.slice(0, 28)}"`);
      }
    }
    return { over, clip, un };
  }, { SAFE });
  if (r.over.length) out.push(`t=${t}: ${[...new Set(r.over)].join(', ')}`);
  if (r.clip.length) clipped.push(`t=${t}: ${[...new Set(r.clip)].join(', ')}`);
  if (r.un.length) unsafe.push(`t=${t}: ${[...new Set(r.un)].join(', ')}`);
}
await browser.close();

const show = (name, a) => console.log(`${tag} ${name}: ` + (a.length ? `${a.length} —\n  ` + a.slice(0, 8).join('\n  ') : 'none'));
console.log(`${tag} ${W}x${H} · ${DUR}s`);
show('errors', errs);
show('overflow', out);
show('clipped text', clipped);
show(TALL ? 'outside reels safe area' : 'outside safe margin', unsafe);
process.exit(errs.length || out.length || clipped.length || unsafe.length ? 1 : 0);
