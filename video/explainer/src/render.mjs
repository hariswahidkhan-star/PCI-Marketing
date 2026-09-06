/**
 * Frame renderer for the PCI Honorary Fellowship tribute film.
 *
 * Drives scene.html by calling window.seek(t) and screenshotting each frame.
 * Unlike the intro film's overlay this renders on an opaque ground — the
 * tribute is type and vector throughout, with no footage beneath it.
 * Deterministic: frame N depends only on t.
 *
 *   node render.mjs --w 1920 --h 1080 --fps 25 --out ../build/frames
 *   node render.mjs --name "Jane Smith"      # personalise the reveal
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
const OUT = path.resolve(HERE, arg('out', '../build/frames'));
// Resumable, chunked rendering: this environment restarts long-running jobs, so
// render in bounded chunks and skip frames that already exist on disk.
const FROM = +arg('from', 0);
const TO   = +arg('to', 0);            // 0 = to the end

const scene = pathToFileURL(path.join(HERE, 'scene.html'));
scene.searchParams.set('w', W);
scene.searchParams.set('h', H);
const THEME=arg('theme',''); if (THEME) scene.searchParams.set('theme', THEME);
const NAME = arg('name', '');
if (NAME) scene.searchParams.set('name', NAME);

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

process.stdout.write(`tribute: ${total} frames @ ${W}x${H} ${FPS}fps${NAME ? ` — "${NAME}"` : ''}\n`);
const last = TO > 0 ? Math.min(TO, total) : total;
let done = 0;
for (let f = FROM; f < last; f++) {
  const out = path.join(OUT, String(f).padStart(5, '0') + '.png');
  if (existsSync(out)) continue;
  await page.evaluate((tt) => window.seek(tt), f / FPS);
  await stage.screenshot({
    path: out,
    animations: 'disabled'
  });
  if (++done % 250 === 0 || f === last - 1) process.stdout.write(`  ${f + 1}/${total}\n`);
}
await browser.close();
process.stdout.write(`frames -> ${OUT}\n`);
