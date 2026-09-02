# PCI post-launch film — 15 seconds

A 15-second film introducing the Project Controls Institute platform after the
1 September 2026 launch, and inviting the profession to help build it.

Everything here is source. The film is rebuilt from this directory with one
command; nothing was hand-placed in an editor, so a copy change is a text edit and
a rebuild rather than a re-cut.

```bash
cd src && ./build.sh
```

---

## What is in `dist/`

| File | Use |
|---|---|
| `pci-launch-15s-1920x1080-captions.mp4` | **Primary.** LinkedIn, YouTube, the website. Burned-in captions. |
| `pci-launch-15s-1080x1080-captions.mp4` | LinkedIn feed — square takes more vertical space on mobile. |
| `pci-launch-15s-1920x1080-clean.mp4` | No burned-in captions, for platforms where you upload the `.srt`. |
| `pci-launch-15s-1920x1080-silent.mp4` | Picture only. Hand this to a studio laying their own VO and music. |
| `pci-launch-15s-score.wav` | The music bed on its own, 48 kHz stereo. |
| `pci-launch-15s.srt` / `.vtt` | Caption files, timings identical to the burned-in text. |
| `pci-launch-15s-poster.png` | Thumbnail / poster frame. |

H.264 High@4.1, yuv420p, `+faststart`, AAC 192 kbps 48 kHz — within LinkedIn,
YouTube and Vimeo specs without re-encoding.

---

## The one thing this pipeline cannot produce

**The voiceover.** A broadcast-quality human read is not something that can be
synthesised here, and shipping a robotic scratch track labelled "professional
voiceover" would be worse than shipping none. So the delivered masters carry
**picture, captions and the music bed** — everything except the voice.

`script.md` has the read: four lines, 27 words, with in/out times to the
hundredth of a second, casting direction and recording notes. It is written so a
voice artist can record to time on the first take.

### Laying the voiceover in

Record to the timings in `script.md`, export a 48 kHz WAV with the first word
starting at **0.30 s**, then:

```bash
ffmpeg -i dist/pci-launch-15s-1920x1080-captions.mp4 \
       -i vo.wav \
       -filter_complex "[0:a]volume=0.42[bed];[1:a]volume=1.0[vo];[bed][vo]amix=inputs=2:duration=first:normalize=0[a]" \
       -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k \
       dist/pci-launch-15s-final.mp4
```

`volume=0.42` drops the bed about 7.5 dB under the voice — a good starting point,
not a rule. If the read is quieter than expected, sidechain instead:

```bash
-filter_complex "[0:a][1:a]sidechaincompress=threshold=0.05:ratio=6:attack=12:release=280[bed];[bed][1:a]amix=inputs=2:normalize=0[a]"
```

The music was written to leave room in the mid-range for a voice, so heavy ducking
should not be necessary.

---

## Files

```
script.md          the read: 27 words, timed, with the word-count arithmetic
                   that drives it, plus a 30s alternate cut
storyboard.md      shot-by-shot with every animation cue and the score map
captions/          .srt and .vtt — timings match the burned-in captions exactly
brand/             Archivo + Inter (the site's own faces) and the PCI mark
src/scene.html     the film itself — deterministic, seek-driven
src/render.mjs     Playwright frame renderer
src/music.py       the score, synthesised from scratch (stdlib only)
src/build.sh       frames → masters
dist/              built output
```

### How the film is built

`scene.html` exposes `window.seek(t)` and computes **every** style from `t`. There
are no CSS animations and no real-time clock, so frame 218 is identical whether it
is grabbed in 40 ms or 4 seconds. `render.mjs` seeks and screenshots 450 times;
ffmpeg encodes the sequence. That is why the output is reproducible and why a copy
change costs a rebuild rather than a re-cut.

Both aspect ratios come from the same source. The square crop is not a centre-cut
of the 16:9 — the headline breaks across three lines instead of two, the verb row
and credential chips shrink, and the bottom safe area deepens so nothing collides
with the caption band.

### Changing things

| To change | Edit |
|---|---|
| Any on-screen wording | the shot `<section>`s in `src/scene.html` |
| Timing of a cut | `SHOTS` in `src/scene.html` |
| When an element appears | `CUES` in `src/scene.html` |
| Caption text or timing | `CAPS` in `scene.html` **and** `captions/*.srt` + `.vtt` (keep all three in step) |
| The music | `src/music.py` |

Colours and type come from `backend/wwwroot/assets/styles.css` in the platform
repo — `--ink #0F172A`, `--crimson #C13329`, `--magenta #3B82F6`, Archivo 800 for
display, Inter for text. Keep them in step with the site rather than drifting.

---

## Editorial position

The Institute's stated posture is that it would "rather understate than oversell",
and the film is held to that standard rather than to advertising conventions.

There is no accreditation claim, no member or participant count, no testimonial,
no employer logo, and no salary or job-outcome promise. The end card carries the
Delaware Non-Stock Corporation status and the "not yet accredited; developed with
reference to ISO/IEC 17024" line **in the film**, not only in the post copy.

`script.md` has the full claims audit — every factual statement in the film traced
to the launch deck or a live page on the site.

---

## Publishing notes

- **LinkedIn autoplays muted.** Use a captions master. This is why the burned-in
  version is the primary deliverable rather than a nicety.
- The first 3 seconds have to work with no sound: shot 1 states what the thing is
  in type alone.
- Post copy should carry the invitation in full — the five verbs in shot 4 are a
  prompt, and the copy is where "how do I actually contribute" gets answered with
  a link.
- The 20-post launch pack in the platform repo (`docs/marketing/`) is the natural
  follow-on sequence once this film has run.
