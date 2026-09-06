/**
 * Frame renderer for the PCI post-launch film.
 *
 * Drives scene.html by calling window.seek(t) and screenshotting each frame, so
 * output is deterministic — no dependency on wall-clock animation timing.
 *
 *   node render.mjs --w 1920 --h 1080 --fps 30 --cc 1 --out ../build/16x9-cc
 */
import { chromium } from 'playwright';
import { mkdir, rm } from 'node:fs/promises';
import { existsSync, readdirSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url));

/**
 * Locate a Chromium. The npm playwright package pins a build number that often
 * differs from the one baked into a CI image, and a mismatch aborts launch with
 * "Executable doesn't exist". Prefer an explicit CHROME_PATH, then any
 * chromium-* already on the box, and only then playwright's own download.
 */
function findChrome() {
  if (process.env.CHROME_PATH && existsSync(process.env.CHROME_PATH)) {
    return process.env.CHROME_PATH;
  }
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  if (existsSync(root)) {
    const dirs = readdirSync(root)
      .filter((d) => d.startsWith('chromium-'))
      .sort()
      .reverse();
    for (const d of dirs) {
      const exe = path.join(root, d, 'chrome-linux', 'chrome');
      if (existsSync(exe)) return exe;
    }
  }
  return undefined; // let playwright resolve its own
}

function arg(name, dflt) {
  const i = process.argv.indexOf('--' + name);
  return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : dflt;
}

const W   = +arg('w', 1920);
const H   = +arg('h', 1080);
const FPS = +arg('fps', 30);
const CC  = arg('cc', '1');
const THEME = arg('theme', 'light');
const PLATE = arg('plate', '0');
const OUT = path.resolve(HERE, arg('out', '../build/frames'));

const scene = pathToFileURL(path.join(HERE, 'scene.html'));
scene.searchParams.set('w', W);
scene.searchParams.set('h', H);
scene.searchParams.set('cc', CC);
scene.searchParams.set('theme', THEME);
scene.searchParams.set('plate', PLATE);

if (existsSync(OUT)) await rm(OUT, { recursive: true });
await mkdir(OUT, { recursive: true });

const browser = await chromium.launch({
  executablePath: findChrome(),
  args: ['--force-color-profile=srgb', '--font-render-hinting=none',
         '--disable-lcd-text', '--hide-scrollbars']
});
const page = await browser.newPage({
  viewport: { width: W, height: H },
  deviceScaleFactor: 1
});
if (PLATE === '1') await page.emulateMedia({ colorScheme: 'dark' });

await page.goto(scene.href, { waitUntil: 'load' });
// Webfonts must be resident before frame 0, or the first frames render fallback metrics.
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(250);

const DUR = await page.evaluate(() => window.__DUR);
const total = Math.round(DUR * FPS);
const stage = page.locator('#stage');

process.stdout.write(`rendering ${total} frames @ ${W}x${H} ${FPS}fps (cc=${CC} plate=${PLATE})\n`);

for (let f = 0; f < total; f++) {
  const t = f / FPS;
  await page.evaluate((tt) => window.seek(tt), t);
  await stage.screenshot({
    path: path.join(OUT, String(f).padStart(5, '0') + '.png'),
    animations: 'disabled',
    // plate mode keeps the alpha channel so ffmpeg can lay this over footage
    omitBackground: PLATE === '1'
  });
  if (f % 60 === 0 || f === total - 1) {
    process.stdout.write(`  ${f + 1}/${total}\n`);
  }
}

await browser.close();
process.stdout.write(`frames → ${OUT}\n`);
