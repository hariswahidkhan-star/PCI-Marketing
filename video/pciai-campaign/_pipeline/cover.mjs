/* Instagram is the only platform needing a bespoke cover: the grid crops 3:4
   and other surfaces crop 1:1, both from the centre. The films put their
   content in the upper-middle of the safe box, so a centre crop of a strong
   frame keeps the headline — but it has to be checked, not assumed, so this
   writes the full frame and the two crops it will actually be seen as. */
import { chromium } from 'playwright';
import { existsSync, readdirSync, mkdirSync } from 'node:fs';
import path from 'node:path'; import { pathToFileURL } from 'node:url';
function fc(){const r='/opt/pw-browsers';for(const d of readdirSync(r).filter(d=>d.startsWith('chromium-')).sort().reverse()){const e=path.join(r,d,'chrome-linux','chrome');if(existsSync(e))return e;}}
const [tag,t]=[process.argv[2],+process.argv[3]];
const OUT='../dist/covers'; mkdirSync(OUT,{recursive:true});
const u=pathToFileURL(path.resolve('scene.html'));
u.searchParams.set('w',1080);u.searchParams.set('h',1920);u.searchParams.set('cc','1');
const b=await chromium.launch({executablePath:fc(),args:['--force-color-profile=srgb','--font-render-hinting=none','--hide-scrollbars']});
const pg=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
await pg.goto(u.href,{waitUntil:'load'});await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(120);
await pg.evaluate(tt=>window.seek(tt),t);
await pg.screenshot({path:`${OUT}/${tag}-cover-1080x1920.jpg`,quality:92,type:'jpeg'});
// 3:4 centre crop (810x1080) and 1:1 centre crop (1080x1080)
const Y = 260;
await pg.screenshot({path:`${OUT}/${tag}-cover-3x4.jpg`,quality:92,type:'jpeg',clip:{x:135,y:Y,width:810,height:1080}});
await pg.screenshot({path:`${OUT}/${tag}-cover-1x1.jpg`,quality:92,type:'jpeg',clip:{x:0,y:Y,width:1080,height:1080}});
await b.close(); console.log(tag,'cover @',t);
