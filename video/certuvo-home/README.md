# Certuvo — the homepage film (2:17)

The premium brand film for the top of certuvo.com: what Certuvo is, the ten
credentials it prepares candidates for, and every feature that makes it one
platform rather than a stack of them. Eleven beats, opening and closing on
camera with the presenter, in the same light treatment as the CMA films
(`../certuvo-cma`, `../certuvo-cma-60`) — off-white ground, white cards with a
blue top rule, Certuvo blue, and the lecture's red reserved for the numbered
tags, the chapter counter and the progress bar.

| # | Scene | Starts | On screen |
|---|---|---|---|
| 1 | Late (presenter) | 0:00 | "It's late. Everyone else is asleep. And you're still here." |
| 2 | What it is worth | 0:15 | "The room you get invited into. The number on the offer." |
| 3 | Ten credentials | 0:27 | The wall — one card lands on each spoken acronym |
| 4 | Official partner | 0:49 | Certuvo × PCI lockup |
| 5 | Built on research | 0:56 | Researched · Mapped to the blueprint · Rewritten when it changes |
| 6 | What is inside | 1:08 | Verified MCQs · Mock exams · Video lectures · Course notes |
| 7 | AI inside | 1:19 | AI Question Forge (four judges) · AI Coach (calls, reads your screen, six languages, off in mocks) |
| 8 | Not alone | 1:35 | Live study rooms · Mentors 24/7 · Readiness tracking |
| 9 | The price | 1:49 | "Less than the market asks." |
| 10 | Start free | 1:58 | "Start with a free trial." |
| 11 | One platform (presenter) | 2:03 | "Ten credentials. One platform. That's enough." then the end card |

## How the credential wall works (scene 3)

Ten cards in two rows of five. Six are the supplied third-party marks (CMA, CPA,
CFA Institute, Certified Internal Auditor, CISA, NCLEX), cropped to their ink in
`assets/logos/trim-*.png` so they read at even weight. Four are set as
wordmarks rather than logos — **PMP®**, and PCI's own **PCL-AI**, **PML-AI** and
**PFL-AI** — each with its expansion underneath. PMP is type, not PMI's mark,
deliberately: see `claims-register.md` §1.

Cards land one per spoken acronym, so the wall assembles in time with the voice
and is complete on "One platform. All of them."

## The feature scenes (5, 6, 8)

Each row lands complete within half a second, then the **card being spoken about
is raised** — red top rule, filled numbered tag, a small lift — and released as
the voice moves on. That is the `FOCUS` table in `src/scene.html`, alongside the
`CUES` reveal table; both are keyed off measured pauses in the takes, so nothing
is eyeballed. It replaces a slower one-card-at-a-time reveal that left the grid
looking half-empty for seconds at a time.

## Voice, presenter, music

- **Voice:** ElevenLabs *Nassim* (`repzAAjoKlgcT2oOAIWt`), `eleven_v3`, eleven
  takes with inline audio direction (`DIRECTION` in `src/vo.py`).
- **Presenter:** the same synthetic portrait as the CMA films, animated by
  **HeyGen Avatar IV** (`heygen-avatar4`, expressive, 1080p) from the untrimmed
  s1 and s11 takes → `assets/avatar-s1.mp4`, `assets/avatar-s11.mp4`.
  `src/presenter.py` cuts them to JPEG frames and measures the leading silence
  `sync.py` trims, so the lips match the laid voice track.
- **Music:** `music-own/certuvo-home-bed.mp3`, generated for **this** film with
  `eleven_music_v2` — bare for the first twenty seconds under the intimate open,
  building from ninety, peaking 110–130 under the price and the close, resolving
  warm. It has about 18 dB of range against the shared CMA bed's 7, which is why
  this film does not use `../certuvo-cma/music`. Confirmed instrumental by
  transcription (empty transcript). Mixed at `BED=0.42` under a side-chain, to
  −14 LUFS / −1.5 dBTP; the measured narration-to-music margin in the 300 Hz –
  4 kHz band is **21 dB median**, and the only seconds where the music comes
  forward are the scene gaps, by design.

## Build

```bash
cd src && ./build-serial.sh          # mix, then 1080p ×2, 9:16, 1:1 — one at a time
MIX=0 ./build-serial.sh              # reuse the existing build/mixed.wav
```

**Serial, always.** Four Chromium renders on this four-core box take the load
average past 90; `build-serial.sh` runs one at a time on purpose.

The pipeline is the same as the CMA films: `sync.py` measures the takes and
writes `shots.data.js` + `timeline.json`; `vo.py` writes the captions;
`presenter.py` cuts the clips; `scene.html` exposes `window.seek(t)` so every
frame is computed from `t` alone; `render.mjs` drives it over CDP and pipes PNGs
straight into ffmpeg. **`probe.mjs` must be clean at all four sizes before a
build** — it samples every 0.5 s for page errors, stage overflow, caption
collisions, chrome collisions and clipped text:

```bash
cd src && ./run-probes.sh && tail -6 ../build/probe-*.txt
```

## What is in `dist/`

`certuvo-home-1920x1080-captions.mp4` and `-clean.mp4`,
`certuvo-home-1080x1920-captions.mp4` (9:16),
`certuvo-home-1080x1080-captions.mp4` (1:1), plus `.srt` / `.vtt` in
`captions/`. H.264 High, yuv420p, `+faststart`, AAC 192 kbps 48 kHz.

The `-clean` cut has no burned-in captions — use it on the page with the `.vtt`
as a `<track>`, so the captions are selectable and indexable. The captioned cuts
are for social, where players autoplay muted.

## Before this goes on the home page

Read **`claims-register.md`**. Three things need Certuvo, not the film:

1. **"Less than the market asks"** (scene 9) is a comparative price claim and
   needs a dated like-for-like comparison behind it, maintained.
2. **"Official training partner of PCI AI"** appears in the narration, on the
   scene 4 lockup and in the furniture on every frame. There should be a written
   partnership record.
3. **A free trial must actually be open to new students** (scene 10).

And Certuvo must satisfy itself it is entitled to reproduce the six third-party
marks on the credential wall. If not, swap them for wordmark cards in the
pattern already used for PMP and the three PCI credentials — that is a change to
`src/scene.html` alone.
