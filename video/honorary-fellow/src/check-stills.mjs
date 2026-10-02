// Render a handful of frames of scene.html at given times for a visual check.
import { chromium } from 'playwright';
import path from 'node:path'; import fs from 'node:fs';
const [W, H, tag, ...times] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(()=>chromium.launch());
const pg = await b.newPage({ viewport: { width:+W, height:+H }, deviceScaleFactor:1 });
await pg.goto('file://' + path.resolve('scene.html') + `?w=${W}&h=${H}&cc=1&theme=light`);
await pg.waitForTimeout(1500);
for (const t of times){ await pg.evaluate(t=>window.seek(+t), t); await pg.waitForTimeout(80);
  await pg.screenshot({ path: `../build/check/${tag}-${t}.png` }); }
await b.close();
