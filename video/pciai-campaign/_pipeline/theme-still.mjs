import { chromium } from 'playwright';
import { existsSync, readdirSync, mkdirSync } from 'node:fs';
import path from 'node:path'; import { pathToFileURL } from 'node:url';
function fc(){const r='/opt/pw-browsers';for(const d of readdirSync(r).filter(d=>d.startsWith('chromium-')).sort().reverse()){const e=path.join(r,d,'chrome-linux','chrome');if(existsSync(e))return e;}}
const [W,H,tag,ts,theme]=[+process.argv[2],+process.argv[3],process.argv[4],process.argv[5].split(',').map(Number),process.argv[6]];
const OUT='../build/look'; mkdirSync(OUT,{recursive:true});
const u=pathToFileURL(path.resolve('scene.html'));
u.searchParams.set('w',W);u.searchParams.set('h',H);u.searchParams.set('cc','1');u.searchParams.set('theme',theme);
const b=await chromium.launch({executablePath:fc(),args:['--force-color-profile=srgb','--font-render-hinting=none','--hide-scrollbars']});
const pg=await b.newPage({viewport:{width:W,height:H},deviceScaleFactor:1});
pg.on('pageerror',e=>console.log('PAGEERROR',e.message));
await pg.goto(u.href,{waitUntil:'load'});await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(150);
for(const t of ts){await pg.evaluate(tt=>window.seek(tt),t);await pg.screenshot({path:`${OUT}/${tag}-${theme}-${t}.png`});}
await b.close(); console.log('ok');
