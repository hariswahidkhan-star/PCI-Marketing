# PCI AI — the explainer

A chaptered film: why PCI exists, what its objective is, and what each of the
three credentials is for. 2:48, 1920×1080, on the brand system.

| | |
|---|---|
| Structure | Ident · 01 Why PCI exists · 02 The objective · 03 The principle · 04 The credentials (suite, then PCL-AI, PFL-AI, PML-AI) · 05 The standard · 06 Open by design · 07 Where we stand · close |
| Voice | Holden Pro Voice, `eleven_multilingual_v2`, twelve chapter takes |
| Score | `eleven_music_v2`, 150 s, time-stretched to length with pitch preserved |
| Facts | Every claim traces to a live page or the platform's own FAQ seed — see `script.md` |

## Organising devices

The brief was "properly organised", so the organisation is visible on screen:

- **A chapter marker top-right** — `02 / 07 · THE OBJECTIVE` — on every chapter,
  so the viewer always knows where they are.
- **A progress rule along the bottom**, crimson→blue, filling over the film.
- **Chapter numbers in the eyebrows**, and the credentials sub-numbered
  `1 of 3`, `2 of 3`, `3 of 3` so the suite reads as one section.
- **One layout per kind of content.** Statements are left-aligned headlines;
  each credential is a card (code and full name on the left, who it is for and
  what it covers on the right); the standard is a fact row and a weighted bar.

## Contents

| Path | What it is |
|---|---|
| `script.md` | Chapter narration and the claims audit |
| `src/scene.html` | The film — deterministic in `t`; shot windows injected from `vo/cues.json` |
| `src/render.mjs` | Frame renderer (Playwright + Chromium) |
| `vo/ch00..ch11.mp3` | The twelve chapter takes |
| `vo/score.mp3` | The score |
| `vo/cues.json` | Measured chapter timings and derived shot windows |
| `dist/pci-explainer-1920x1080.mp4` | **The master** |
| `dist/pci-explainer-VOICE-ONLY.mp3` | Narration alone |

## How the timing works

Chapters are recorded separately and trimmed at both ends, so their measured
durations drive everything: a 1.0 s lead, a 1.15 s beat between chapters, a
slightly longer breath before the credentials, the standard and the status
chapter, and a 3 s tail under the end card. Shot windows are the midpoints of
those beats, injected into `scene.html` by the build, so the type cuts on the
same numbers as the voice. Change a take and the whole film re-times itself.

## Rebuilding

```bash
cd src && node render.mjs --w 1920 --h 1080 --fps 25 --out ../build/frames
```

then mix `build/voice-bed.wav` with `vo/score.mp3` (voice at −16 LUFS, score at
−21 sidechain-ducked, `atempo` = 150 / total) and encode against the frames.
The overlay is reproducible frame for frame; the takes and the score are not.
