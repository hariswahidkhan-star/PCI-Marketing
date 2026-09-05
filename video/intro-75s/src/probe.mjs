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
u.searchParams.set('w',W); u.searchParams.set('h',H); u.searchParams.set('cc','1');
const b = await chromium.launch({executablePath:findChrome(),args:['--force-color-profile=srgb','--font-render-hinting=none','--hide-scrollbars']});
const pg = await b.newPage({viewport:{width:W,height:H},deviceScaleFactor:1});
const errs=[]; pg.on('pageerror',e=>errs.push('PAGEERROR '+e.message));
pg.on('console',m=>{if(m.type()==='error')errs.push('CONSOLE '+m.text())});
await pg.goto(u.href,{waitUntil:'load'}); await pg.evaluate(()=>document.fonts.ready); await pg.waitForTimeout(200);
// overflow audit across the whole timeline
const bad = [];
const TS=[]; for(let t=0.5;t<75;t+=0.5) TS.push(+t.toFixed(1));
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
  const real=o.filter(x=>!/^glow/.test(x)); if (real.length) bad.push(`t=${t}: `+real.join(' | '));
  if ([1,5,12,21,32,42,53,65,73].includes(t)) await pg.locator('#stage').screenshot({path:path.join(OUT,`${tag}-t${String(t).padStart(2,'0')}.png`),animations:'disabled'});
}
console.log(tag+' errors: '+(errs.length?errs.join('\n  '):'none'));
console.log(tag+' overflow: '+(bad.length?'\n  '+bad.join('\n  '):'none'));
await b.close();
