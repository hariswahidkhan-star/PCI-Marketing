import { chromium } from 'playwright';
import { existsSync, readdirSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
function findChrome(){
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  if (existsSync(root)) for (const d of readdirSync(root).filter(d=>d.startsWith('chromium-')).sort().reverse()){
    const exe = path.join(root,d,'chrome-linux','chrome'); if (existsSync(exe)) return exe;
  }
}
const [W,H,tag] = [+process.argv[2], +process.argv[3], process.argv[4]];
const OUT = '../build/probe'; mkdirSync(OUT,{recursive:true});
const u = pathToFileURL(path.resolve('scene.html'));
u.searchParams.set('w',W); u.searchParams.set('h',H); u.searchParams.set('cc','1');u.searchParams.set('theme',process.env.THEME||'light');
const b = await chromium.launch({executablePath:findChrome(),args:['--force-color-profile=srgb','--font-render-hinting=none','--hide-scrollbars']});
const pg = await b.newPage({viewport:{width:W,height:H},deviceScaleFactor:1});
const errs=[]; pg.on('pageerror',e=>errs.push('PAGEERROR '+e.message));
pg.on('console',m=>{if(m.type()==='error')errs.push('CONSOLE '+m.text())});
await pg.goto(u.href,{waitUntil:'load'}); await pg.evaluate(()=>document.fonts.ready); await pg.waitForTimeout(200);
// overflow audit across the whole timeline
const bad = [], collide = [], chrome = [];
const DURP = await pg.evaluate(()=>window.__DUR);
const CUTS = await pg.evaluate(()=>(window.__SHOTS||[]).map(s=>s[2]));
  const TS=[]; for(let t=0.5;t<DURP;t+=0.5) TS.push(+t.toFixed(1));
  for (const t of TS){
  await pg.evaluate(tt=>window.seek(tt), t);
  const o = await pg.evaluate(()=>{
    const st=document.getElementById('stage'), sb=st.getBoundingClientRect(), out=[];
    for (const el of document.querySelectorAll('#stage *')){
      const cs=getComputedStyle(el); if(cs.visibility==='hidden'||+cs.opacity<0.02) continue;
      const r=el.getBoundingClientRect(); if(r.width===0) continue;
      if (r.left < sb.left-1 || r.right > sb.right+1)
        out.push((el.id||el.className||el.tagName)+' ['+Math.round(r.left-sb.left)+'..'+Math.round(r.right-sb.left)+'] of '+Math.round(sb.width));
    } return [...new Set(out)];
  });
  // A shot is *supposed* to be off-stage mid-transition — it slides in from the
  // right while the outgoing one slides left, and #stage is overflow:hidden, so
  // that is the effect working rather than a layout fault. Only overflow away
  // from a cut is a real finding.
  const moving = CUTS.some(c => Math.abs(t - c) < 0.7);
  const real = o.filter(x => !/^glow/.test(x));
  if (real.length && !moving) bad.push(`t=${t}: `+real.join(' | '));

  // Caption collision: the caption block must never overlap live content. This
  // is the check that actually protects legibility, and it is the reason the
  // padding-bottom values in scene.html are what they are.
  const hit = await pg.evaluate(() => {
    const cc = document.getElementById('ccbox');
    if (!cc) return null;
    const cs = getComputedStyle(cc);
    if (cs.visibility === 'hidden' || +getComputedStyle(document.getElementById('cc')).opacity < 0.02) return null;
    const cr = cc.getBoundingClientRect();
    if (cr.width === 0 || cr.height === 0) return null;
    const st = document.getElementById('stage').getBoundingClientRect();
    const skip = new Set(['cc', 'ccbox', 'stage', 'vig', 'glow', 'glow2', 'progress', 'progwrap']);
    for (const el of document.querySelectorAll('#stage *')) {
      if (skip.has(el.id) || el.closest('#cc')) continue;
      // Only leaf content can collide. A shot wrapper or a column is the full
      // width of the stage by construction and overlaps the caption band
      // trivially — flagging those would report a collision on every frame and
      // tell us nothing about legibility.
      if (el.querySelector('*')) continue;
      // checkVisibility folds in ancestor opacity. Reading the element's own
      // computed opacity is not enough here: every shot stays in the DOM and is
      // hidden by setting opacity on its wrapper, so a leaf inside an off-screen
      // shot still reports opacity 1 and would be flagged on frames where it is
      // nowhere near the screen.
      if (!el.checkVisibility({ opacityProperty: true, visibilityProperty: true })) continue;
      const s2 = getComputedStyle(el);
      if (+s2.opacity < 0.05) continue;
      const host = el.closest('.shot');
      if (host && +getComputedStyle(host).opacity < 0.35) continue;
      const painted = el.textContent.trim()
        || s2.backgroundImage !== 'none'
        || !/^(rgba\(0, 0, 0, 0\)|transparent)$/.test(s2.backgroundColor);
      if (!painted) continue;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      if (r.width * r.height > st.width * st.height * 0.55) continue;
      if (r.left < cr.right && r.right > cr.left && r.top < cr.bottom && r.bottom > cr.top)
        return (el.id || el.className || el.tagName) + ' "'
             + el.textContent.trim().slice(0, 28) + '" overlaps the caption';
    }
    return null;
  });
  if (hit) collide.push(`t=${t}: ${hit}`);

  // Chrome collision: the masthead, the chapter rail and the footer are fixed
  // furniture. Scene content overrunning into them is the failure mode that a
  // caption-only check misses — and the one that actually looks broken, because
  // two pieces of type land on top of each other.
  const ch = await pg.evaluate(() => {
    const chrome = ['topbar', 'chapter', 'footl', 'footr', 'footrule']
      .map(id => document.getElementById(id)).filter(Boolean)
      .filter(e => e.checkVisibility({ opacityProperty: true }) && +getComputedStyle(e).opacity > 0.05)
      .map(e => ({ id: e.id, r: e.getBoundingClientRect() }));
    for (const el of document.querySelectorAll('#stage .shot *')) {
      if (el.querySelector('*')) continue;
      if (!el.checkVisibility({ opacityProperty: true, visibilityProperty: true })) continue;
      const host = el.closest('.shot');
      if (host && +getComputedStyle(host).opacity < 0.35) continue;
      if (!el.textContent.trim()) continue;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      for (const c of chrome) {
        if (r.left < c.r.right && r.right > c.r.left && r.top < c.r.bottom && r.bottom > c.r.top)
          return `"${el.textContent.trim().slice(0, 24)}" overruns #${c.id}`;
      }
    }
    return null;
  });
  if (ch) chrome.push(`t=${t}: ${ch}`);
  if ([8,24,38,55,70,86,98,112,125,140,155,170,178,192,210,229].includes(t)) await pg.locator('#stage').screenshot({path:path.join(OUT,`${tag}-t${String(t).padStart(2,'0')}.png`),animations:'disabled'});
}
console.log(tag+' errors: '+(errs.length?errs.join('\n  '):'none'));
console.log(tag+' overflow: '+(bad.length?'\n  '+bad.join('\n  '):'none')+'  (transitions excluded)');
console.log(tag+' caption collisions: '+(collide.length?'\n  '+collide.join('\n  '):'none')+`  (${TS.length} samples)`);
console.log(tag+' chrome collisions: '+(chrome.length?'\n  '+chrome.join('\n  '):'none'));
if (errs.length || bad.length || collide.length || chrome.length) process.exitCode = 1;
await b.close();
