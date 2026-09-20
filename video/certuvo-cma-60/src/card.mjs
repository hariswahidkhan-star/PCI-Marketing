// Screenshot card.html at each output size → ../build/card-<w>x<h>.png
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
mkdirSync('../build',{recursive:true});
const b = await chromium.launch({executablePath:findChrome(),args:['--force-color-profile=srgb','--font-render-hinting=none','--hide-scrollbars']});
for (const [W,H] of [[1920,1080],[1080,1920],[1080,1080],[3840,2160]]){
  const u = pathToFileURL(path.resolve('card.html'));
  u.searchParams.set('w',W); u.searchParams.set('h',H);
  const pg = await b.newPage({viewport:{width:W,height:H},deviceScaleFactor:1});
  pg.on('pageerror',e=>console.log('PAGEERROR',e.message));
  await pg.goto(u.href,{waitUntil:'load'});
  await pg.evaluate(()=>document.fonts.ready);
  await pg.waitForTimeout(300);
  const over = await pg.evaluate(()=>{
    const st=document.getElementById('stage'), sb=st.getBoundingClientRect(), out=[];
    for (const el of document.querySelectorAll('#stage *')){
      if (el.id==='glow') continue;
      const r=el.getBoundingClientRect();
      if (r.width && (r.left<sb.left-1||r.right>sb.right+1||r.top<sb.top-1||r.bottom>sb.bottom+1))
        out.push((el.className||el.tagName)+' ['+Math.round(r.top-sb.top)+'..'+Math.round(r.bottom-sb.top)+'] of '+Math.round(sb.height));
    } return [...new Set(out)];
  });
  console.log(`${W}x${H} overflow: ${over.length?over.join(' | '):'none'}`);
  await pg.screenshot({path:`../build/card-${W}x${H}.png`});
  await pg.close();
}
await b.close();
