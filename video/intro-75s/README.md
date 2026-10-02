# PCI AI — 75-second institutional film

An introductory film for **PCI AI — Project Controls Institute Global, Inc.**,
addressed to project-controls professionals, project and programme managers,
project-finance professionals, PMO and governance leaders, planners and
schedulers, cost engineers, risk professionals, and organisations adopting AI in
project environments.

Educational and technically credible, and deliberately not an advertisement. The
Institute's published position is that it would *"rather understate than
oversell"*, and this film is held to that standard: **it contains no statistic of
any kind, and it states on screen — twice — that PCI is not accredited.**

Everything here is source. The film rebuilds from this directory with one
command; nothing was hand-placed in an editor, so a copy change is a text edit
and a rebuild rather than a re-cut.

```bash
cd src && ./build.sh
```

---

## What is in `dist/`

| File | Use |
|---|---|
| `pci-ai-intro-75s-1920x1080-captions.mp4` | **Primary.** LinkedIn, YouTube, the website. Burned-in captions. |
| `pci-ai-intro-75s-1080x1920-captions.mp4` | Vertical — Reels, Shorts, TikTok, Stories. A real layout, not a centre-crop. |
| `pci-ai-intro-75s-1080x1080-captions.mp4` | Square — LinkedIn feed. |
| `pci-ai-intro-75s-1920x1080-clean.mp4` | No burned-in captions, for platforms where you upload the `.srt`. |
| `pci-ai-intro-75s-1920x1080-MASTER.mp4` | **High-quality master**, CRF 12, near-visually-lossless. Archive and re-encode from this. |
| `pci-ai-intro-75s-1920x1080-silent.mp4` | Picture only. Hand this to a studio laying their own VO and music. |
| `pci-ai-intro-75s-voiceover.wav` | **Clean voice only**, 48 kHz, no music. |
| `pci-ai-intro-75s-mixed-soundtrack.wav` | **The final mix** — voice over the side-chained score, −15.5 LUFS. |
| `pci-ai-intro-75s-score.wav` | The music bed alone, 48 kHz stereo. |
| `pci-intro-75s.srt` / `.vtt` | Caption files. Timings are identical to the burned-in text **by construction** — see below. |
| `pci-ai-intro-75s-poster.png` | Poster frame (41.0 s — the identity shot). |
| `pci-ai-intro-75s-thumbnail-1920x1080.png` / `-1280x720.png` | Thumbnail (65.0 s — the light closing statement). |

Delivery format is H.264 High@4.1, yuv420p, `+faststart`, AAC 192 kbps 48 kHz —
within LinkedIn, YouTube and Vimeo specs without re-encoding.

---

## The voiceover

**Delivered.** The narration is ElevenLabs *"Jim Executive — Authoritative,
British and Warm"* (`tXxkePQsw0G69D8VeDzp`) — a stock library voice, **not a
clone of any real person**. It is a **synthetic voice** and the asset manifest
records it as such.

Fifteen segments were generated separately rather than as one read, so each line
could be placed against its own timecode. That surfaced a real problem worth
recording: **the read came back at ~130 wpm — 82.4 s of speech for a 75 s film.**
The film had been cut for 153 wpm.

Rather than stretch the picture or re-record, `src/sync.py` derives the single
uniform time-scale that lands the film exactly on 75.00 s — here **1.175x** — and
applies it with `librubberband`, which preserves formants (plain `atempo` thins
the voice at this ratio). The result runs at the pace the film was designed for,
not a rushed one. The whole timeline is then recomputed from where the words
actually fall, and propagated to the cut list, the caption set and the score.

**Everything is derived, nothing is hand-nudged.** Verified after the build:
speech present in all 15 caption windows (−16 to −21 dB RMS), silence in every
gap (−99 dB), 15/15.

`captions/vo-script.md` has the read: 15 segments, timed to the hundredth of a
second, with the mandatory pronunciation table and casting direction. It is
written so a voice artist can record to time on the first take.

### Replacing it with a human read

If a voice artist records the script, drop the WAVs into `audio/trimmed/` as
`vo-01.wav` … `vo-15.wav`, then `python3 src/sync.py && ./src/build.sh`. The
timeline re-derives itself around the new performance — no manual re-timing.
`sync.py` refuses rather than shipping a rushed read if the recording would need
more than 1.25x compression; raise `TARGET` in that case.

To mix a full-length read against the existing picture instead:

```bash
FF=src/node_modules/ffmpeg-static/ffmpeg
$FF -i dist/pci-ai-intro-75s-1920x1080-captions.mp4 -i vo.wav \
    -filter_complex "[0:a]volume=0.42[bed];[1:a]volume=1.0[v];[bed][v]amix=inputs=2:duration=first:normalize=0[a]" \
    -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k \
    dist/pci-ai-intro-75s-final.mp4
```

`volume=0.42` drops the bed about 7.5 dB under the voice — a starting point, not
a rule. The score peaks at −11 dBFS and sits around −21 dBFS RMS with a scooped
mid-range, so heavy ducking should not be necessary. If the read is quieter than
expected, sidechain instead:

```bash
-filter_complex "[0:a][1:a]sidechaincompress=threshold=0.05:ratio=6:attack=12:release=280[bed];[bed][1:a]amix=inputs=2:normalize=0[a]"
```

---

## The B-roll variant

After the Runway package was purchased, five cinematic B-roll clips were
generated — four with Runway `gen-4.5` and the closing shot with Kling
`kling-3-pro`. **They are not in `dist/`.** Runway's artifact CDN is refused by
the production environment's egress policy, so the clips could not be pulled in
and composited there.

What is delivered instead is the piece that actually matters for an editor:

| File | Use |
|---|---|
| `…-16x9-typelayer-alpha.mov` | **ProRes 4444 with alpha.** Drop it over any footage in any NLE — type, furniture, captions and the legibility scrim land in exactly the verified positions and timings |
| `…-16x9-typelayer-alpha.webm` | VP9 with alpha, for web and lightweight review |
| …and the same pair for `9x16` and `1x1` | |

To rebuild the composite yourself:

```bash
# 1. download the five clips from your Runway workspace into assets/generated/
#    (filenames and task IDs are in assets/generated/README.md)
cd src && ./plates.sh        # transparent type-layer frames, if not already built
./composite.sh               # 16:9   -> dist/…-1920x1080-broll-captions.mp4
./composite.sh 1080 1920 9x16
./composite.sh 1080 1080 1x1
```

`composite.sh` fits each clip to its scene, grades it toward the brand palette,
cross-fades at the scene edges, and lays the alpha plate over the top. **It has
been run end-to-end against stand-in clips**, so the pipeline is verified — only
the footage itself is substituted.

**Scenes 5, 6 and 8 deliberately receive no footage.** They carry the identity,
the credential framework and the end card, and generated imagery must not sit
behind the frames that state who PCI is and what it certifies.

One difference worth knowing: in the B-roll variant the scene-7 light inversion
is disabled, because pale type over footage is not reliably legible. The
original masters keep it.

---

## Files

```
claims-register.md     every factual statement, its source, and what was excluded
approval-request.md    the paid actions being held, with cost and reversibility
connector-report.md    what each of the 15 connectors actually did
storyboard.md          shot-by-shot with grade, motion cues and aspect behaviour
shot-list.md           per-element reveal cues and stagger
assets/                Unsplash licensing register (reference only — none used in the film)
metadata/              YouTube + LinkedIn metadata, chapters, search phrases
captions/              .srt, .vtt and the timed read — all generated, never hand-edited
brand/                 Archivo + Inter (the site's own faces) and the PCI mark
src/scene.html         the film itself — deterministic, seek-driven
src/vo.py              THE source of truth for the read and all three caption forms
src/sync.py            conforms the timeline to the recorded voice; writes timeline.json
src/timeline.json      generated — the measured segment placements and scene bounds
src/music.py           the score, synthesised from scratch (stdlib only)
src/render.mjs         Playwright frame renderer
src/probe.mjs          layout + caption-collision audit across all three aspects
src/build.sh           frames -> masters
src/plates.sh          transparent type-layer frames (for the B-roll variant)
src/composite.sh       B-roll + type layer -> composited masters
src/alpha-master.sh    type layer -> ProRes 4444 / VP9 with alpha
dist/                  built output
```

### How the film is built

`scene.html` exposes `window.seek(t)` and computes **every** style from `t`.
There are no CSS animations and no real-time clock, so frame 1,842 is identical
whether it is grabbed in 40 ms or 4 seconds. `render.mjs` seeks and screenshots
2,250 times per aspect; ffmpeg encodes the sequence. That is why the output is
reproducible and why a copy change costs a rebuild rather than a re-cut.

**Captions cannot drift.** The 15-second film's README warns that caption text
lives in three places — the burned-in array, the `.srt` and the `.vtt` — and
must be kept in step by hand. That is a standing invitation to error, so this
film generates all three from one spec in `src/vo.py`. It also carries the
spoken and written forms separately, because they are different things:
the voice says *"P-C-L A-I"*, the caption reads **PCL-AI**.

**Three aspects, three layouts.** The vertical and square cuts are not
centre-crops. Rows become columns, the type scale changes against a different
nominal width, and the bottom safe area deepens. `src/probe.mjs` steps all three
aspects every 0.5 s and asserts that no element collides with the caption band —
**450 checks, currently zero collisions and zero page errors.**

### Changing things

| To change | Edit |
| --- | --- |
| Any on-screen wording | the shot `<section>`s in `src/scene.html` |
| Timing of a cut | `SHOTS` in `src/scene.html` — **and** `SCENES` in `src/vo.py` |
| The scene grade / colour ground | the `bg`, `warm` and `light` fields on `SHOTS` |
| When an element appears | `CUES` in `src/scene.html` |
| Caption or voiceover text | `SCENES` in `src/vo.py`, then rebuild — all three caption forms regenerate |
| The music | `src/music.py` (cut list `CUTS` must match `SHOTS`) |

Colours and type come from `backend/wwwroot/assets/styles.css` in the platform
repo — `--ink #0F172A`, `--crimson #C13329`, `--magenta #3B82F6`, Archivo 800 for
display, Inter for text. Keep them in step with the site rather than drifting.

---

## Editorial position

No accreditation claim. No member or participant count. No testimonial, employer
logo, salary or job-outcome promise. No third-party recognition. **No statistics
at all** — which, as `claims-register.md` §4 sets out, turned out to matter: four
figures circulating in internal brand material could not be found anywhere in the
235-page live-site source, and this film uses none of them.

Scene 6 and the end card both carry the Institute's own accreditation wording,
verbatim from `accreditation-status.html`.
