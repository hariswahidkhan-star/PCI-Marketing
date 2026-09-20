# Certuvo — the homepage film (2:46)

The premium brand film for the top of certuvo.com. Eleven beats, opening and
closing on camera with the presenter, in the light treatment the CMA films
established: off-white ground, white cards with a blue top rule, Certuvo blue,
and the lecture's red rationed to the numbered tags, the chapter counter, the
progress bar and the one flagged gap in the readiness scene.

**Read `narrative-design.md` before changing the order of anything.** The film
is built on a single withheld question — *the difference isn't how hard you
work* — opened in scene 2 and not answered until scene 11. Move a scene and you
break it.

| # | Scene | Starts | On screen |
|---|---|---|---|
| 1 | Late (presenter) | 0:00 | "It's late. Everyone else is asleep. And you're still here." |
| 2 | The difference | 0:15 | The loop opens: "They all work hard." |
| 3 | Ten credentials | 0:27 | The wall — one card lands on each spoken acronym |
| 4 | Official partner | 0:48 | Certuvo × PCI lockup |
| 5 | Already inside | 0:55 | **Animated:** a field of verified questions fills, then mocks, lectures, notes |
| 6 | Four judges | 1:12 | **Animated:** one question is followed through all four gates |
| 7 | AI Coach | 1:31 | **Animated:** a call, a beam reading the screen, a Socratic reply, then the coach stands down for a mock |
| 8 | Study with a peer | 1:48 | **Animated:** a screen shared live, two cursors on one question, a seat left open for a friend |
| 9 | Readiness | 2:04 | **Animated:** the curve climbs to the exam-ready line, one domain flagged |
| 10 | The price | 2:17 | "Less than the market asks." then "start free" |
| 11 | What you work with (presenter) | 2:25 | The loop closes, then the end card |

## The five animated sequences

Scenes 5 to 9 are the answer to scene 2's question, and each is **shown working
rather than listed**. A feature named is a claim; a feature demonstrated is
evidence. They are driven by `SCENEFX` in `src/scene.html` — one pure function
per scene, taking only the seconds elapsed since that scene's narration began,
so every frame is still reproducible from `t` alone and nothing holds state
between frames.

- **The bank (s5)** fills as a field of question chips rather than a counter. A
  counter states a number Certuvo has not published; a field that fills in front
  of you carries the impression honestly. Provenance follows immediately —
  researched, mapped to the blueprint, in the exam's own weightings — because
  volume without provenance reads as filler.
- **The Forge (s6)** follows one question from "Writing…" through Generated,
  Answer verified, Checked for ambiguity and Matched to the blueprint. Each gate
  ticks on the word that names it; the spine fills; the card clears. Watching one
  item pass a visible process does more for trust in the other thousands than any
  adjective.
- **The Coach (s7)** is shown mid-question at 23:07 on the clock, on a **real,
  fully worked question** rather than a blurred placeholder: fixed overhead of
  $480,000 over 60,000 budgeted units against 54,000 actual, so the volume
  variance is $48,000 unfavourable. The question is written for the film, not
  taken from any awarding body's paper — see `claims-register.md` §5A.6 for the
  working. The beam makes "it reads your screen" legible in a way the sentence
  cannot; the coach quotes those numbers back and then answers **with a
  question**, and only after that does the option light. The order is enforced
  in the animation, because "you leave with the method, not the answer" is the
  claim. Then the mock starts and the coach greys itself out. That restraint is
  the credibility claim.
- **Study with a peer (s8)** is a shared screen, not a room. One person is
  presenting, a second is already on it, and **two named cursors move on the
  same question** and land on the same option — which is the only image that
  reads as shared control. The mic indicator trades between speakers. A dashed
  third seat, "Bring a friend · send them a link", lands last and keeps pulsing
  after everything else has settled. Faces are initials on discs, deliberately:
  stock faces read as stock, abstraction reads as privacy.

  > **This scene replaced a cohort study room and a 24/7 mentor chat** after PCI
  > confirmed neither feature exists. Both claims were traced to live
  > certuvo.com copy — see the warning in `claims-register.md` §6, which is
  > about the site, not the film.
- **Readiness (s9)** draws a curve to a dashed exam-ready threshold with five
  domain bars, one short and flagged red. No numbers anywhere — it illustrates
  the feature, it does not promise a score.

## Voice, presenter, music

- **Voice:** ElevenLabs *Nassim* (`repzAAjoKlgcT2oOAIWt`), `eleven_v3`, eleven
  takes with inline audio direction (`DIRECTION` in `src/vo.py`).
- **Presenter:** a synthetic portrait animated by **HeyGen Avatar IV**
  (`heygen-avatar4`, 1080p) from the untrimmed s1 and s11 takes.
  `src/presenter.py` cuts them to JPEG frames and measures the leading silence
  `sync.py` trims, so the lips match the laid voice track.
- **Music:** `music-own/certuvo-home-bed.mp3`, 170 s, generated for this film
  with `eleven_music_v2` — bare for the first twenty seconds under the intimate
  open, building from a hundred, peaking 125–155 under the price and the close,
  resolving warm. Confirmed instrumental by transcription. Mixed at `BED=0.42`
  under a side-chain to −14 LUFS / −1.5 dBTP; measured narration-to-music margin
  in the 300 Hz – 4 kHz band is **18 dB median**, and the only seconds where the
  bed comes forward are the gaps between scenes.

## Build

```bash
cd src && ./build-serial.sh          # mix, then 1080p ×2, 9:16, 1:1 — one at a time
MIX=0 ./build-serial.sh              # reuse the existing build/mixed.wav
./finish.sh                          # verify, join the stings, verify again, pull the stills
```

**Serial, always.** Four Chromium renders on this four-core box take the load
average past 90; `build-serial.sh` runs one at a time on purpose.

**The bed must be at least as long as the film.** `build-serial.sh` now refuses
to build if it is not: a short bed does not fail on its own, `atrim` simply stops
early and the close plays dry with nothing saying so. That happened once, when
the film grew from 2:17 to 2:42; it now runs 2:46.

`probe.mjs` must be clean at all four sizes before a build — it samples every
0.5 s for page errors, stage overflow, caption collisions, chrome collisions and
clipped text:

```bash
cd src && ./run-probes.sh && tail -6 ../build/probe-*.txt
```

## What is in `dist/`

`certuvo-home-1920x1080-captions.mp4` and `-clean.mp4`,
`certuvo-home-1080x1920-captions.mp4` (9:16),
`certuvo-home-1080x1080-captions.mp4` (1:1), plus `.srt` / `.vtt` in
`captions/`. H.264 High, yuv420p, `+faststart`, AAC 192 kbps 48 kHz.

`-FULL-` versions are the same cut with the Certuvo intro and outro stings
joined on. There is no certifications card between the film and the outro,
unlike the one-minute cut: scene 3 is already the credential wall.

`certuvo-home-poster.jpg` is the frame at 40 s, the complete credential wall.
The other stills are the presenter, the Coach and the close. All come from the
clean cut, so none carries a burned-in caption.

The `-clean` cut has no burned-in captions — use it on the page with the `.vtt`
as a `<track>`, so the captions stay selectable and indexable. The captioned
cuts are for social, where players autoplay muted.

## Before this goes on the home page

Read **`claims-register.md`**. Six things need Certuvo, not the film:

1. **"Thousands of verified questions"** is new in this cut and is a quantity
   claim. The line says *inside every course*, so it has to be true per course,
   not across the platform.
2. **"Less than the market asks"** is comparative and needs a dated
   like-for-like comparison behind it, maintained.
3. **"Official training partner of PCI AI"** appears in the narration, on the
   scene 4 lockup and in the corner of every frame. There should be a written
   partnership record.
4. **A free trial must actually be open to new students.**
5. **The peer screen-share and "bring a friend" (s8) are recorded from a
   written description, not from site copy or a build.** Confirm the peer sees
   the presenter's screen, and that a candidate can invite someone themselves.
6. **certuvo.com still advertises live study rooms and 24/7 mentor chat.** They
   were withdrawn from this film because PCI said the features do not exist. If
   that is right, the live site is a larger exposure than the film was, and it
   was not part of this work.

And Certuvo must satisfy itself it may reproduce the six third-party marks on
the credential wall. If not, swap them for wordmark cards in the pattern already
used for PMP and the three PCI credentials — a change to `src/scene.html` alone.
