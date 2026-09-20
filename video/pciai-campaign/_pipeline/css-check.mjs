import { chromium } from 'playwright';
import { existsSync, readdirSync } from 'node:fs';
import path from 'node:path'; import { pathToFileURL } from 'node:url';
function fc(){const r='/opt/pw-browsers';for(const d of readdirSync(r).filter(d=>d.startsWith('chromium-')).sort().reverse()){const e=path.join(r,d,'chrome-linux','chrome');if(existsSync(e))return e;}}
const u=pathToFileURL(path.resolve('scene.html'));u.searchParams.set('w',1080);u.searchParams.set('h',1920);
const b=await chromium.launch({executablePath:fc()});
const pg=await b.newPage({viewport:{width:1080,height:1920}});
pg.on('requestfailed',r=>console.log('FAILED',r.url().slice(-60),r.failure()?.errorText));
pg.on('response',r=>{ if(r.url().endsWith('.css')||r.url().endsWith('.woff2')||r.url().endsWith('.svg')) console.log('RESP',r.status(),r.url().slice(-40)); });
await pg.goto(u.href,{waitUntil:'load'});
console.log('sheets:', await pg.evaluate(()=>[...document.styleSheets].map(s=>({href:(s.href||'inline').slice(-30), rules:(()=>{try{return s.cssRules.length}catch(e){return 'BLOCKED'}})()}))));
console.log('beat position:', await pg.evaluate(()=>getComputedStyle(document.querySelector('.beat')).position));
console.log('h1 font-size:', await pg.evaluate(()=>getComputedStyle(document.querySelector('#h1')).fontSize));
await b.close();
