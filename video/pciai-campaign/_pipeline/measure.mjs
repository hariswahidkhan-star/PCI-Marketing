import { chromium } from 'playwright';
import { existsSync, readdirSync } from 'node:fs';
import path from 'node:path'; import { pathToFileURL } from 'node:url';
function fc(){const r='/opt/pw-browsers';for(const d of readdirSync(r).filter(d=>d.startsWith('chromium-')).sort().reverse()){const e=path.join(r,d,'chrome-linux','chrome');if(existsSync(e))return e;}}
const u=pathToFileURL(path.resolve('scene.html'));u.searchParams.set('w',1080);u.searchParams.set('h',1920);u.searchParams.set('cc','1');
const b=await chromium.launch({executablePath:fc()});
const pg=await b.newPage({viewport:{width:1080,height:1920}});
await pg.goto(u.href,{waitUntil:'load'});await pg.evaluate(()=>document.fonts.ready);
await pg.evaluate(()=>window.seek(1.0));
const r=await pg.evaluate(()=>{
  const sb=document.getElementById('stage').getBoundingClientRect();
  // the same box probe.mjs enforces: y 270..1250, x 65..1015 on 1080x1920
  const TALL = sb.width / sb.height < 0.70;
  const f = TALL ? {t:270/1920, b:1-1250/1920, l:65/1080, r:1-1015/1080}
                 : {t:0.035, b:0.035, l:0.035, r:0.035};
  const safe={top:sb.height*f.t,bottom:sb.height*(1-f.b),left:sb.width*f.l,right:sb.width*(1-f.r)};
  const out=[];
  for(const sel of ['#brandbar .wm','#brandbar .tag','#foot span:first-child','#foot span:last-child','#e1','#h1','#ccbox']){
    const el=document.querySelector(sel); if(!el) {out.push([sel,'MISSING']);continue;}
    const x=el.getBoundingClientRect();
    out.push([sel,`t=${x.top.toFixed(0)} b=${x.bottom.toFixed(0)} l=${x.left.toFixed(0)} r=${x.right.toFixed(0)}`]);
  }
  return {safe:`top>=${safe.top.toFixed(0)} bottom<=${safe.bottom.toFixed(0)} left>=${safe.left.toFixed(0)} right<=${safe.right.toFixed(0)}`,out,
          s:getComputedStyle(document.documentElement).getPropertyValue('--s')};
});
console.log('--s =',r.s); console.log('SAFE:',r.safe);
for(const [k,v] of r.out) console.log('  ',k.padEnd(24),v);
await b.close();
