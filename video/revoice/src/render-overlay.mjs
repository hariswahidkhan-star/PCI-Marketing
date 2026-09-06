/**
 * Brand-overlay frame renderer for the 60-second introduction film.
 *
 * Drives overlay.html by calling window.seek(t) and screenshotting each frame
 * with a transparent background, so the result composites over the generated
 * footage in ffmpeg. Deterministic: frame N depends only on t.
 *
 *   node render-overlay.mjs --w 1920 --h 1080 --fps 25 --out ../build/overlay
 */
import { chromium } from 'playwright';
import { mkdir, rm } from 'node:fs/promises';
import { existsSync, readdirSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url));

/** Same Chromium resolution as ../../launch-15s/src/render.mjs — an image's
 *  baked-in build often differs from the one playwright pins. */
function findChrome() {
  if (process.env.CHROME_PATH && existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH;
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  if (existsSync(root)) {
    for (const d of readdirSync(root).filter(d => d.startsWith('chromium-')).sort().reverse()) {
      const exe = path.join(root, d, 'chrome-linux', 'chrome');
      if (existsSync(exe)) return exe;
    }
  }
  return undefined;
}

function arg(name, dflt) {
  const i = process.argv.indexOf('--' + name);
  return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : dflt;
}

const W = +arg('w', 1920), H = +arg('h', 1080), FPS = +arg('fps', 25);
const OUT = path.resolve(HERE, arg('out', '../build/overlay'));

const scene = pathToFileURL(path.join(HERE, 'overlay.html'));
scene.searchParams.set('w', W);
scene.searchParams.set('h', H);
const DURQ=arg('dur',''); if (DURQ) scene.searchParams.set('dur', DURQ);

if (existsSync(OUT)) await rm(OUT, { recursive: true });
await mkdir(OUT, { recursive: true });

const browser = await chromium.launch({
  executablePath: findChrome(),
  args: ['--force-color-profile=srgb', '--font-render-hinting=none',
         '--disable-lcd-text', '--hide-scrollbars']
});
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await page.goto(scene.href, { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);   // else frame 0 renders fallback metrics
await page.waitForTimeout(250);

const DUR = await page.evaluate(() => window.__DUR);
const total = Math.round(DUR * FPS);
const stage = page.locator('#stage');

process.stdout.write(`overlay: ${total} frames @ ${W}x${H} ${FPS}fps\n`);
for (let f = 0; f < total; f++) {
  await page.evaluate((tt) => window.seek(tt), f / FPS);
  await stage.screenshot({
    path: path.join(OUT, String(f).padStart(5, '0') + '.png'),
    omitBackground: true,          // transparent ground — this is the whole point
    animations: 'disabled'
  });
  if (f % 250 === 0 || f === total - 1) process.stdout.write(`  ${f + 1}/${total}\n`);
}
await browser.close();
process.stdout.write(`frames -> ${OUT}\n`);
