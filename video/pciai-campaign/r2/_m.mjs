import { chromium } from 'playwright';
import { existsSync, readdirSync } from 'node:fs';
import path from 'node:path'; import { pathToFileURL } from 'node:url';
function fc(){const r='/opt/pw-browsers';for(const d of readdirSync(r).filter(d=>d.startsWith('chromium-')).sort().reverse()){const e=path.join(r,d,'chrome-linux','chrome');if(existsSync(e))return e;}}
const u=pathToFileURL(path.resolve('scene.html'));u.searchParams.set('w',1080);u.searchParams.set('h',1920);
const b=await chromium.launch({executablePath:fc()});
const pg=await b.newPage({viewport:{width:1080,height:1920}});
await pg.goto(u.href,{waitUntil:'load'}); await pg.evaluate(()=>document.fonts.ready); await pg.waitForTimeout(200);
for (const t of process.argv[2].split(',').map(Number)){
  await pg.evaluate(tt=>window.seek(tt), t);
  const rows = await pg.evaluate(()=>{
    const o=[];
    for(const el of document.querySelectorAll('#stage *')){
      const cs=getComputedStyle(el);
      if(cs.display==='none'||cs.visibility==='hidden'||+cs.opacity<0.05) continue;
      if(el.closest('[data-decor]')) continue;
      const txt=el.textContent&&el.textContent.trim();
      const leaf=txt&&![...el.children].some(c=>c.textContent&&c.textContent.trim());
      const r=el.getBoundingClientRect();
      if(r.width<1||r.height<1) continue;
      o.push({tag:(el.id||el.className||el.tagName)+'', leaf:!!leaf, x:Math.round(r.left),r:Math.round(r.right),y:Math.round(r.top),bt:Math.round(r.bottom),
        sw:el.scrollWidth, cw:el.clientWidth, sh:el.scrollHeight, ch:el.clientHeight, fs:cs.fontSize});
    }
    return o;
  });
  console.log('--- t='+t);
  for(const r of rows) console.log(`${r.tag.padEnd(22)} leaf=${r.leaf?1:0} box=[${r.x},${r.y} → ${r.r},${r.bt}] scroll=${r.sw}x${r.sh} client=${r.cw}x${r.ch} fs=${r.fs}`);
}
await b.close();
