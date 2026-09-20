import { chromium } from 'playwright';
import { existsSync, readdirSync } from 'node:fs';
import path from 'node:path'; import { pathToFileURL } from 'node:url';
function fc(){const r='/opt/pw-browsers';for(const d of readdirSync(r).filter(d=>d.startsWith('chromium-')).sort().reverse()){const e=path.join(r,d,'chrome-linux','chrome');if(existsSync(e))return e;}}
const u=pathToFileURL(path.resolve('scene.html'));u.searchParams.set('w',1080);u.searchParams.set('h',1920);
const b=await chromium.launch({executablePath:fc()});
const pg=await b.newPage({viewport:{width:1080,height:1920}});
await pg.goto(u.href,{waitUntil:'load'});await pg.evaluate(()=>document.fonts.ready);
await pg.evaluate(()=>window.seek(7.0));
console.log(await pg.evaluate(()=>{const e=document.getElementById('n2');const cs=getComputedStyle(e);
 return {sw:e.scrollWidth,cw:e.clientWidth,sh:e.scrollHeight,ch:e.clientHeight,fs:cs.fontSize,lh:cs.lineHeight,rect:e.getBoundingClientRect().toJSON()};}));
await b.close();
