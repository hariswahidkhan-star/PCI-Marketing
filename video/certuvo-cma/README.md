# Certuvo — The CMA, Part 1 and Part 2 (4:35)

A premium explainer for **Certuvo**'s CMA® preparation: what the Certified
Management Accountant is, exactly what is in Part 1 and Part 2 (all twelve
domains with their weights), how the four-hour exam works — including the
case-based questions that replace the essays from the September 2026 window —
the certification requirements, why it pays, what Certuvo offers (practice
exams, progress tracking, live study rooms, 24/7 mentor chat, the AI Question
Forge and the AI Coach), and a close from an on-camera presenter. Eleven scenes;
a synthetic presenter opens and closes the film, motion graphics carry the rest.

**Look:** the light treatment of certuvo.com and Certuvo's lecture graphics — an
off-white ground, white cards with a blue top rule, Certuvo blue for headings
and accents, and the lecture's red kept small: the numbered tags, the progress
bar, Part 2's bars, the chapter counter and one emphasised word.

- **Voice:** ElevenLabs *Nassim*, `eleven_v3`, directed per scene with audio tags
  (`src/vo.py` → `DIRECTION`). Eleven takes, one per scene, so sentences flow.
- **Presenter:** a Seedream 5 Pro portrait (`assets/presenter-a.png`, no real
  person) animated by **HeyGen Avatar IV** (`heygen-avatar4`, expressive, 1080p)
  from the same Nassim takes, via the ElevenLabs creative flow
  `Hqx2MhTarzYeLbv0a55u`. The clips are `assets/avatar-s2.mp4` and
  `assets/avatar-s11.mp4`; they play inside a video card on the light ground.
- **Music:** a bespoke 250 s underscore from ElevenLabs Music v2
  (`music/certuvo-bed.mp3`, see `music/README.md`), side-chained under the voice.
- **Picture:** one deterministic HTML scene (`src/scene.html`) rendered by
  Playwright at 4K, 1080p, 9:16 and 1:1 — real layouts per aspect, not crops.

```bash
cd src && ./build.sh          # full build, 30 fps  (HD_FIRST=1 for the HD cuts first)
cd src && ./build.sh --fast   # 15 fps check build
```

`claims-register.md` traces every fact in the film to its source and marks
what Certuvo must confirm before publication. `share-kit.md` has the platform
copy.

---

## Scenes

| # | Scene | Starts | What is on screen |
|---|---|---|---|
| 1 | Hook | 0:00 | 2 exams · 4 hours each · plan / control / analyse / **decide** |
| 2 | Welcome (presenter) | 0:09 | Video card + agenda chips |
| 3 | What the CMA is | 0:30 | CMA® mark, IMA, since 1972, 61 first-year passes, the five verbs |
| 4 | Part 1 | 0:55 | Six weighted bars (blue) rising as each domain is named |
| 5 | Part 2 | 1:26 | Six weighted bars (red), Decision Analysis tagged largest |
| 6 | The exam | 1:55 | 4-hour bar (3 h MCQ / 1 h cases), 2 cases · 50 % gate · 360/500, three windows |
| 7 | Requirements | 2:33 | Three lecture-style cards (01–03) + the seven-year path |
| 8 | Why it matters | 2:53 | +21 % counting up, IMA Global Salary Survey 2023, role chips |
| 9 | How Certuvo prepares you | 3:16 | Practice exams · Progress tracking · Live study rooms · 24/7 chat support |
| 10 | AI inside | 3:45 | AI Question Forge (four-judge panel) · AI Coach (calls, reads your screen, Socratic, auto-off in mocks, six languages) |
| 11 | Start (presenter) | 4:14 | Video card + three steps + certuvo.com, then the end card with the legal line |

---

## What is in `dist/`

| File | Use |
|---|---|
| `certuvo-cma-3840x2160-MASTER-captions.mp4` | **4K master, captioned.** Website, YouTube |
| `certuvo-cma-3840x2160-MASTER-clean.mp4` | 4K master, no burned-in captions (use with the `.srt`/`.vtt`) |
| `certuvo-cma-1920x1080-captions.mp4` | HD, captioned |
| `certuvo-cma-1920x1080-clean.mp4` | HD, clean — Lanczos downscale of the 4K clean master |
| `certuvo-cma-1920x1080-silent.mp4` | Picture only |
| `certuvo-cma-1080x1920-captions.mp4` | **9:16 vertical** — Reels, Shorts, TikTok, LinkedIn mobile |
| `certuvo-cma-1080x1080-captions.mp4` | **1:1 square** — LinkedIn, Instagram feed |
| `certuvo-cma.srt` / `.vtt` | Captions (32 cues) |
| `certuvo-cma-poster-3840x2160.png`, `…-thumbnail-*.png` | Stills: the CMA mark (0:36) and the Part 1 weights (1:06) |
| `…-voiceover.wav` / `…-music-bed.wav` / `…-mixed-soundtrack.wav` | Audio stems |

H.264 High (Level 5.1 for 4K, 4.1 for HD), yuv420p, `+faststart`, AAC 192 kbps
48 kHz, −14 LUFS integrated / −1.5 dBTP — inside YouTube, LinkedIn, Instagram
and Vimeo specs without re-encoding.

---

## How it is built

```
src/vo.py          script: captions + spoken lines + eleven_v3 direction; LEGAL end frame
src/sync.py        trims each take, lays the voice track, measures scene bounds and
                   caption boundaries (explicit ends in vo.py where the pauses were
                   measured by hand) → shots.data.js, timeline.json, ../audio/vo-track.wav
src/presenter.py   cuts the two avatar clips to JPEG frames (../build/av/s2, s11) and
                   measures each clip's lead-in silence → presenter.data.js
src/scene.html     the film: eleven <section class="shot">s, cue sheet (CUES) relative
                   to each scene's first caption, window.seek(t) → every style from t.
                   seek() returns a promise: the presenter frame must be decoded
                   before the screenshot.
src/render.mjs     Playwright frame renderer (pipes PNGs straight into ffmpeg)
src/probe.mjs      audit: page errors, stage overflow, caption collisions, chrome
                   collisions, clipped text — at every 0.5 s, per aspect
src/run-probes.sh  the audit at all four output sizes → ../build/probe-*.txt
src/stills.mjs     look-development stills at chosen times → ../build/look/
src/build.sh       sync → captions → presenter frames → music bed → mix → renders
```

The picture is cut to the voice: `sync.py` measures the takes and writes the
cut list; nothing in `scene.html` carries a hand-copied time. Inside a scene,
the cue sheet times are seconds after that scene's narration starts, taken from
the pauses `silencedetect` found in the take (−38 dB, ≥ 0.26 s), so each Part 1
and Part 2 weight bar rises as its domain is named, each feature card as it is
described, and each AI judge as the panel is explained.

### Presenter scenes

The avatar clips were generated from the *untrimmed* takes; `sync.py` trims the
leading silence before laying the voice track, so `presenter.py` measures that
lead the same way and `scene.html` addresses frame `round((t − scene voice start
+ lead) × 30)`. The clip's own audio is not used — the film's voice track is the
same take, mixed once. The clip sits in a rounded video card with a small live
badge; the agenda chips (s2) and the three steps + URL badge (s11) sit beside it
in 16:9 and below it in 1:1 and 9:16.

### Aspect layouts

`scene.html` reads `?w=&h=` and picks a layout: `169`, `sq` (1:1) or `pt`
(9:16). Part 1 / Part 2 are two columns in 16:9 and stack in the narrow
aspects; the exam bar's red segment carries shorter copy there; the facts
become rows in 9:16; the two AI panels stack. `run-probes.sh` must report
`none` on every check at all four sizes before a build is shipped.

---

## Regenerating a take

Each scene is one take. To change a line: edit the caption/spoken pair and the
matching `DIRECTION` entry in `src/vo.py` (`CHECK_ONLY=1 python3 vo.py` asserts
they still match), generate the scene with `eleven_v3` / Nassim
(`repzAAjoKlgcT2oOAIWt`) on the flow, save it as `audio/vo-NN.mp3`, re-measure
the pauses (`ffmpeg -af silencedetect=noise=-38dB:d=0.26`) for the explicit ends
in `vo.py` and the cue delays in `scene.html`, and rebuild. For s2 or s11 also
regenerate the avatar clip from the new take.

---

## Known issues

- **"In the next three minutes"** — the presenter says this in s2; the film runs
  4:35 because the twelve domains, the exam structure, the requirements and
  Certuvo's features are spoken in full rather than skimmed. The on-screen chip
  says "in the next four minutes". Recommended before publication: re-record s2
  with "in the next few minutes" (one take + one avatar clip, ≈ 12,600 ElevenLabs
  credits).
- The avatar clips are 1080p; in the 4K master the presenter card is upscaled
  (bicubic, in the browser). Everything else is rendered at 4K.
- IMA's site was not reachable from the build environment; the exam facts are
  from provider summaries and are marked **V** in `claims-register.md`. The
  Certuvo feature claims are taken from certuvo.com as it read on 12 September
  2026 and are marked **P**.
