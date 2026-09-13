/**
 * Frame renderer for the PCI post-launch film.
 *
 * Drives scene.html by calling window.seek(t) and screenshotting each frame, so
 * output is deterministic — no dependency on wall-clock animation timing.
 *
 *   node render.mjs --w 1920 --h 1080 --fps 30 --cc 1 --out ../build/16x9-cc
 *   node render.mjs --w 1920 --h 1080 --fps 30 --cc 1 --pipe 1 | ffmpeg -f image2pipe ...
 *
 * Frames are captured through CDP with `optimizeForSpeed`, which selects a
 * faster PNG compression level. PNG is lossless at every level, so the pixels
 * are byte-identical to the slow setting — only the file is larger. Measured on
 * this film: 254 ms/frame down to 98 ms/frame, and three aspects in parallel go
 * from 1.1 fps aggregate to 25.3 fps. The larger frames are why `--pipe` exists:
 * at 938 KB a frame, three aspects of a 256 s film would want 22 GB of scratch
 * disk, so the default path streams them into ffmpeg and never writes them.
 */
import { chromium } from 'playwright';
import { mkdir, rm, writeFile } from 'node:fs/promises';
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
const PIPE  = arg('pipe', '0') === '1';
// Frames to also write out as individual PNGs, e.g. --stills 2850,3750 --stillsdir ../build/stills
const STILLS = new Set((arg('stills', '') || '').split(',').filter(Boolean).map(Number));
const STILLSDIR = arg('stillsdir', '../build/stills');
const OUT = path.resolve(HERE, arg('out', '../build/frames'));

const scene = pathToFileURL(path.join(HERE, 'scene.html'));
scene.searchParams.set('w', W);
scene.searchParams.set('h', H);
scene.searchParams.set('cc', CC);
scene.searchParams.set('theme', THEME);
scene.searchParams.set('plate', PLATE);

if (!PIPE) {
  if (existsSync(OUT)) await rm(OUT, { recursive: true });
  await mkdir(OUT, { recursive: true });
}
if (STILLS.size) await mkdir(path.resolve(HERE, STILLSDIR), { recursive: true });

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
const cdp = await page.context().newCDPSession(page);

/** Write to a stream, respecting backpressure — ffmpeg reads slower than we render. */
function write(stream, buf) {
  return stream.write(buf) ? Promise.resolve()
                           : new Promise((res) => stream.once('drain', res));
}

/**
 * Capture one frame. Plate mode keeps the alpha channel, which CDP only honours
 * via a transparent background override, so that path stays on the Playwright
 * screenshot API where `omitBackground` does the work.
 */
async function capture() {
  if (PLATE === '1') {
    return stage.screenshot({ animations: 'disabled', omitBackground: true });
  }
  const { data } = await cdp.send('Page.captureScreenshot', {
    format: 'png', optimizeForSpeed: true, captureBeyondViewport: false
  });
  return Buffer.from(data, 'base64');
}

const note = (m) => (PIPE ? process.stderr : process.stdout).write(m);
note(`rendering ${total} frames @ ${W}x${H} ${FPS}fps (cc=${CC} plate=${PLATE} pipe=${PIPE})\n`);

for (let f = 0; f < total; f++) {
  const t = f / FPS;
  await page.evaluate((tt) => window.seek(tt), t);
  const png = await capture();
  if (PIPE) await write(process.stdout, png);
  else await writeFile(path.join(OUT, String(f).padStart(5, '0') + '.png'), png);
  if (STILLS.has(f)) {
    await writeFile(path.resolve(HERE, STILLSDIR, String(f).padStart(5, '0') + '.png'), png);
  }
  if (f % 60 === 0 || f === total - 1) {
    note(`  ${f + 1}/${total}\n`);
  }
}

await browser.close();
if (PIPE) {
  // ffmpeg needs EOF on the pipe to flush its last GOP; letting the process
  // simply exit can truncate the final frames.
  await new Promise((res) => process.stdout.end(res));
  process.stderr.write('frames → stdout\n');
} else {
  process.stdout.write(`frames → ${OUT}\n`);
}
