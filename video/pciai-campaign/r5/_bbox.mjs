import { chromium } from '/home/user/PCI-Marketing/video/explainer/src/node_modules/playwright/index.mjs';
import { existsSync, readdirSync } from 'node:fs';
import path from 'node:path'; import { pathToFileURL } from 'node:url';
function fc(){const r='/opt/pw-browsers';for(const d of readdirSync(r).filter(d=>d.startsWith('chromium-')).sort().reverse()){const e=path.join(r,d,'chrome-linux','chrome');if(existsSync(e))return e;}}
const [W,H]=[+process.argv[2],+process.argv[3]];
const ts=process.argv[4].split(',').map(Number);
const u=pathToFileURL(path.resolve('scene.html'));
u.searchParams.set('w',W);u.searchParams.set('h',H);
const b=await chromium.launch({executablePath:fc(),args:['--font-render-hinting=none','--hide-scrollbars']});
const pg=await b.newPage({viewport:{width:W,height:H}});
await pg.goto(u.href,{waitUntil:'load'});await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(150);
console.log('brandbar', await pg.evaluate(()=>{const r=document.getElementById('brandbar').getBoundingClientRect();return [Math.round(r.top),Math.round(r.bottom)]}));
console.log('foot', await pg.evaluate(()=>{const r=document.getElementById('foot').getBoundingClientRect();return [Math.round(r.top),Math.round(r.bottom)]}));
for(const t of ts){
  await pg.evaluate(tt=>window.seek(tt),t);
  const r = await pg.evaluate(()=>{
    const live=[...document.querySelectorAll('.beat')].find(b=>getComputedStyle(b).display!=='none');
    let top=1e9,bot=-1e9,left=1e9,right=-1e9;const lines=[];
    for(const el of live.querySelectorAll('*')){
      const cs=getComputedStyle(el); if(cs.display==='none')continue;
      const b=el.getBoundingClientRect(); if(b.width<1||b.height<1)continue;
      const txt=(el.textContent||'').trim();
      const leaf=txt&&![...el.children].some(c=>(c.textContent||'').trim());
      if(!leaf&&!el.classList.contains('rule'))continue;
      top=Math.min(top,b.top);bot=Math.max(bot,b.bottom);left=Math.min(left,b.left);right=Math.max(right,b.right);
      lines.push(`${el.className||el.tagName}|${Math.round(b.left)},${Math.round(b.top)}-${Math.round(b.right)},${Math.round(b.bottom)}|${txt.slice(0,22)}`);
    }
    return {id:live.id,top:Math.round(top),bot:Math.round(bot),left:Math.round(left),right:Math.round(right),h:Math.round(bot-top),lines};
  });
  console.log(`t=${t} ${r.id} y ${r.top}..${r.bot} (h=${r.h}) x ${r.left}..${r.right}`);
  if(process.env.V) r.lines.forEach(l=>console.log('   ',l));
}
await b.close();
