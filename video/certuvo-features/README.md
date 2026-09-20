# Certuvo feature films — five treatments to choose between

Five product-demonstration films covering the same fourteen features. They are
deliberately different films, not one film in five colours: the point is to make
the choice a real one.

| | Treatment | Length | Voice | What it is |
|---|---|---|---|---|
| **V1** | Walkthrough | 1:05 | Nassim | A rail of all fourteen features stays on screen and lights the pair being shown, while a browser-style pane beside it demonstrates them. One product, toured. |
| **V2** | Card Deck | 0:58 | Nassim | One large card at a time, centred, handing off on a hard vertical seam, with a fourteen-dash deck indicator. A keynote. |
| **V3** | One Session | 1:06 | Nassim | One laptop locked dead centre for the whole film, a time rail stepping 21:04 to 23:05, overlays sliding over a question that never moves. One evening of study. |
| **V4** | Grid Dive | 1:04 | — | Opens on all fourteen as a map, then seven times one column's pair blooms out of its own position into a full-frame demonstration and collapses back. Closes on the map complete. |
| **V5** | Kinetic | 0:46 | — | Huge type snapping in word by word, a compact product panel alternating sides. The fastest and boldest. |

Watch them in `v*/dist/`. Only 1920x1080 is built: the chosen treatment gets
9:16, 1:1 and the rest.

## The rule that shapes every frame

**No real question, answer, explanation or note appears in any of the five.**
Every one is a skeleton bar or a deliberately blurred block from
`common/ui.css` — unreadable by construction rather than by cropping a real
screenshot. Options carry a letter and a bar; the bar is never text.

This lives in the shared kit rather than in each film, so no treatment can break
it by accident. Same for the rest of the visual law: white ground, Certuvo blue
doing the work, and red rationed to four jobs — a timer running low, a detected
knowledge gap, a live indicator, and the numbered tag. The logo is furniture,
present on every frame.

## How it is built

```
common/ui.css        the visual kit — every abstract part the films draw with
common/engine.js     the deterministic runtime, one global (window.CE)
_pipeline/           render, probe, stills, sync — shared by symlink
music/feature-bed.mp3  one bed, generated for these films, trimmed per length
v1..v5/src/scene.html  the five treatments
```

`engine.js` is a classic script rather than an ES module because the renderer
loads the scene over `file://` and Chromium blocks module imports there.

**Every film is a pure function of t.** `seek(t)` uses no timers, no
`requestAnimationFrame`, no `Date`, no CSS transitions or keyframes, and carries
no state between calls. Called twice with the same t it paints the same pixels,
which is what lets the renderer screenshot frame by frame and lets the probe
audit the whole timeline before anything is encoded.

V2 and V3 go one better: their beat timings are derived from the caption times
at runtime rather than hard-coded, so re-running `sync.py` on a new take re-cuts
the film with no hand-copied numbers in the scene at all.

```bash
cd v1/src && node probe.mjs 1920 1080 v1     # must be clean before a build
./build-all.sh                               # all five, serially
./_pipeline/build-one.sh v3 certuvo-v3-onesession
```

**Serial, always.** Concurrent Chromium renders take this box past a load
average of 90. `build-one.sh` decides how to mix by whether a voice track exists
rather than by a flag, so it cannot be set wrong.

## Two traps worth remembering

**A symlinked module resolves to its real path.** `render.mjs` is shared across
the five by symlink, and while it based paths on `import.meta.url` it looked for
the scene in `_pipeline` instead of the variant. It rendered nothing, and the
empty frame stream then failed inside ffmpeg as "Invalid data found when
processing input" — an error that points at the encoder, not the path. Every
probe passed throughout, because `probe.mjs` had always resolved against the
working directory. Both do now.

**`ffmpeg -i` with no output file exits 1 by design**, and `grep` exits 1 on no
match. Under `set -euo pipefail` either one kills a build script silently. It
did, once, after a fifty-minute render.

## Before any of these is published

Read `claims-register.md`. One line needs Certuvo rather than the film:
**"thousands of verified questions"** is said as being *inside every course*, so
it has to be true per course rather than across the platform. Study streaks
appear as a feature with no figure attached, deliberately.

These five name no credential and show no third-party mark, so none of the
trademark exposure in `../certuvo-home/claims-register.md` applies here.
