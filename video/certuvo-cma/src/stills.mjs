// Quick look: render a set of times at one size to ../build/look/<tag>-<t>.png
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
const TS = process.argv[5].split(',').map(Number);
const OUT = '../build/look'; mkdirSync(OUT,{recursive:true});
const u = pathToFileURL(path.resolve('scene.html'));
u.searchParams.set('w',W); u.searchParams.set('h',H); u.searchParams.set('cc','1');
const b = await chromium.launch({executablePath:findChrome(),args:['--force-color-profile=srgb','--font-render-hinting=none','--hide-scrollbars']});
const pg = await b.newPage({viewport:{width:W,height:H},deviceScaleFactor:1});
pg.on('pageerror',e=>console.log('PAGEERROR',e.message)); pg.on('console',m=>{if(m.type()==='error')console.log('CONSOLE',m.text())});
await pg.goto(u.href,{waitUntil:'load'}); await pg.evaluate(()=>document.fonts.ready); await pg.waitForTimeout(200);
for (const t of TS){ await pg.evaluate(tt=>window.seek(tt), t); await pg.screenshot({path:`${OUT}/${tag}-${t.toFixed(1)}.png`}); }
await b.close();
