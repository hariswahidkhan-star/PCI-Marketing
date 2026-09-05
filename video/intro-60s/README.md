# PCI AI introduction film — 60 seconds

A longer companion to `../launch-15s/`. Where that film **announces**, this one
**explains**: what the discipline faces, what the Institute is for, and exactly
where it stands today.

| | |
|---|---|
| Duration | 60.000 s |
| Aspect | 16:9, 1080p, 25 fps |
| Voice | ElevenLabs `eleven_v3`, British narrative register, directed read |
| Score | ElevenLabs `eleven_music_v2`, instrumental, ducked under the voice |
| Script | `script.md` — copy, timings, on-screen type, claims audit |
| Cue sheet | `vo/cues.json` |

---

## Contents

| Path | What it is |
|---|---|
| `script.md` | The film. Nine VO beats, nine shot windows, direction notes, claims audit |
| `vo/pci-intro-60s-vo-bed.wav` | **The deliverable voice track** — 60.000 s, 48 kHz / 24-bit mono |
| `vo/src-v3a.mp3` | **Take used** — `eleven_v3` directed read, 54.44 s |
| `vo/src-v3b.mp3` | `eleven_v3` alternate, 57.47 s |
| `vo/src-score.mp3` | The orchestral score, 60 s instrumental |
| `vo/pci-intro-60s-VOICE-ONLY.mp3` | Voice with no picture or score — for checking the read |
| `vo/pci-intro-60s-vo-take-1.mp3` | Earlier `eleven_multilingual_v2` take (47.31 s) |
| `vo/pci-intro-60s-vo-take-2.mp3` | Earlier alternate (46.44 s) |
| `vo/cues.json` | Measured in/out for all nine lines, machine-readable |
| `src/overlay.html` | The brand overlay — type only, transparent ground, deterministic in `t` |
| `src/render-overlay.mjs` | Frame renderer (Playwright + Chromium) |
| `src/build.sh` | Rebuilds the overlay and re-composites the master |
| `dist/pci-intro-60s-1920x1080.mp4` | **The master** — 60.000 s, branded, voiced |
| `dist/pci-intro-60s-1920x1080-compat.mp4` | Same film, maximum-compatibility encode (H.264 Main / L4.0, AAC-LC 44.1 kHz, mp42) |
| `dist/pci-intro-60s-FULL-MIX.mp3` | Complete soundtrack — voice **and** score — as plain audio |
| `dist/pci-intro-60s-poster.png` | Poster frame (45 s, the founding-stage shot) |

---

## How the voice track was made

Not a raw TTS dump. The bed is cut to the storyboard:

1. **Two takes generated** through the ElevenLabs connector
   (`eleven_multilingual_v2`, voice *George — Warm, Captivating Storyteller*),
   chosen against the casting note both films share: *"a national broadcaster's
   documentary narration, not a product advert."*
2. **Line boundaries measured**, not guessed — `silencedetect` at `-38 dB / 0.25 s`
   over take 1, treating gaps ≥ 0.60 s as line breaks.
3. **Split and respaced** to an even **1.20 s** beat: 0.60 s lead-in, 43.19 s of
   speech, eight beats, 6.60 s score-only tail under the end card.
4. **Script re-timed to the result.** Every in/out in `script.md` is measured from
   this bed, so the type and the voice cut from the same numbers.

Reproduce the analysis with:

```bash
ffmpeg -i vo/pci-intro-60s-vo-take-1.mp3 \
  -af silencedetect=noise=-38dB:d=0.25 -f null -
```

## Rebuilding

```bash
cd src && ./build.sh
```

### Rebuilding at 4K

`build.sh` reads its output size from the source plates and needs no edits: drop
3840×2160 versions of `build/shot-01..06.mp4` in place and re-run. The overlay is
resolution independent — its scale unit derives from stage width, so the type,
the crimson→blue rule and the lockup hold their proportions — and the bitrate
ceiling steps from 6M to 28M automatically. The script refuses to run if the six
plates are not all the same width, because a mismatched concat produces a broken
stream rather than an obvious error.

**Getting 4K plates.** Runway's video upscaler does this, and its 40 s limit is
fine — each plate is 10.28 s. One plate was upscaled as a pilot and the result is
good. Two things stopped it going further, both measured rather than assumed:

- **Cost.** 941 credits for one 10.28 s plate, so ~5,646 for six. Worth checking
  the balance before starting.
- **Retrieval.** Upload and upscale both work from a CLI session, but Runway
  serves finished assets from a CDN this environment's egress policy blocks. The
  results have to be fetched from the Runway library, or the whole step run from
  a machine without that restriction.

**The decision was to ship at 1080p.** For a 60-second institutional film that
plays embedded on a site or in a social feed, resolution is not the weak link —
the plates being generated rather than photographed matters more, and no amount
of upscaling changes that. The 4K path above stays documented so it can be taken
later without re-deriving any of it.

The overlay is fully reproducible — `overlay.html` computes every style from `t`,
so frame N is byte-identical on every run. **The footage is not.** The six plates
in `build/` were generated once and cannot be regenerated identically; keep them.
Their prompts are in the shot table above if they are ever lost.

---

## How the picture was made

Six 10-second shot groups, one per 10 s window, generated through the ElevenLabs
Creative connector (`ltx-v2-fast`, 1080p, 25 fps, `generate_audio: false` so
nothing competes with the narration), then assembled by a **composition** node
that appends the six clips to one video track and lays the voiceover bed
underneath.

| Window | Carries | Image |
|---|---|---|
| 0–10 s | Numbers, accountability, confidently wrong | Infrastructure site, blue hour, cranes still |
| 10–20 s | The governing principle; the Institute | Hands paused over a printed schedule |
| 20–30 s | Credentials; thirteen domains | Ordered structural geometry, tracking |
| 30–40 s | Three years, any field, no degree barrier | Dim corridor opening into daylight |
| 40–50 s | **Founding stage, not yet accredited** | A building frame still under scaffold |
| 50–60 s | The invitation; end card | Dawn over a completed bridge, high headroom |

Shot 5 is the spine, and its image is the argument: something honestly
mid-construction, not a finished tower. It must not be cut short.

**No on-screen text is generated.** Every prompt says *no text, no signage*.
Generative models render type unreliably, and this brand's type is not
negotiable. All type is rendered separately by `src/overlay.html` — the PCI AI
lockup, the eyebrows, the crimson→blue rule, the credential chips and the end
card — using the tokens lifted verbatim from `../launch-15s/src/scene.html`, then
composited over the footage. Both films are one system, not two lookalikes.

Three shots carry their own darker ground (`.shot.heavy`, `.shot.card`). The
plates behind them — an overcast sky, a bright doorway, a dawn horizon — cannot
hold white type or, more importantly, the legal line on the shared scrim alone.
The ground fades with its shot, so it never darkens a neighbour.

### If a player reports no audio

The master carries a correct AAC-LC stereo track at 48 kHz, `DISPOSITION:default=1`,
start time 0.000 on both streams, −15.9 LUFS integrated and −1.5 dB peak, and it
decodes end to end without error. If a player is silent anyway, work down this
list rather than re-encoding blindly:

1. **Play `dist/pci-intro-60s-FULL-MIX.mp3`.** It is the same soundtrack with no
   video container. If that plays and the MP4 does not, the file is fine and the
   video playback path is the problem.
2. **Try `-compat.mp4`.** Main profile at level 4.0 with AAC-LC at 44.1 kHz suits
   older and stricter players than High profile at 48 kHz.
3. **Download rather than preview.** Inline previews in chat and mail clients
   commonly start muted or drop audio entirely.

Note that both tracks carry an **edit list** (`elst`). This looks suspicious and
is not: AAC encoder priming delay produces one in nearly every AAC/MP4 file, it
survives every muxer flag, and it is not the cause of a silent track.

**Sound.** The voice is normalised to **−16 LUFS**; the raw TTS bed sits around
−28 dB mean, which reads as *no voice* on laptop and phone speakers. The score
sits beneath it through a sidechain compressor keyed off the voice, so it opens
in the gaps and steps back under every line. The finished master measures
**−15.9 LUFS integrated, LRA 2.9**.

The score is delayed **2.6 s**. `eleven_music_v2` wrote its own resolve into the
final five seconds; undelayed, that fade lands *before* the end card and the film
ends on silence. Delayed, it resolves under the end card.

**Grade.** The plates are corrected toward one navy-cool look before a shared
filmic curve. Measured mean luma ran ~40 on shots 1–4 and ~135 on shots 5–6 — a
3× jump that reads as a mismatched cut; after grading the gap is ~1.8×, which is
as far as it goes without crushing the sky.

---

## Status

**Shipping at 1080p.** The master is final: 60.000 s, 1920×1080 at 25 fps,
H.264 + AAC, −15.9 LUFS integrated, faststart set, clean decode end to end.
Script, voice, score, grade, brand type and mix are all done.

One open question remains, and it is editorial rather than technical: whether the
launch deck substantiates the three claims this film drops (see below). Nothing
in the film depends on the answer — it already omits them — but the 15-second
launch film and the root README do.
- **Score.** `../launch-15s/src/music.py` produces the house bed; the 6.60 s tail
  is scored, not silent.
- **Listen to beat 8** (42.71 s). The founding-stage line must sound level and
  unembarrassed. Take 2 is the alternate if take 1 reads as apologetic.

---

## Campaign assets held outside this repository

Produced through connectors; not committed here because they live in their own
services (or, in Runway's case, on a CDN this environment cannot reach).

| Asset | Where |
|---|---|
| Launch deck | `gamma.app/docs/s8dspcw0pgi789b` |
| Production record | Notion, private draft |
| Reference photography | Unsplash collection `cT9cX9Vgg80` (private) — 3 plates incl. the *ThisisEngineering* library |
| Key art still | Runway task `fbcc61d7-37c3-4b1a-a3fa-119226e6ebb3`, 16:9 2K |
| Stakeholder email | Gmail **draft** — written, not sent |

## Distribution research

Keyword demand does not sit where the brand name does:

| Keyword | Est. monthly | Competition |
|---|---|---|
| `project controls certification` | **<750** | — |
| `project control academy` | 4,246 | 11.8 |
| `pmp certification` | 6,373 | 23.7 |
| `project management` | 190,340 | 39.6 |

Plan distribution around where the demand is, not around our own category name.

**On titles.** CTR scoring ranked fear-based and outcome-promising titles highest
— including one implying certification is obtainable today, and one implying job
loss. Both were rejected: they contradict the editorial rule, and for a body
whose product is trust a CTR gain is the wrong trade. Recommended title, scoring
87: *"Introducing PCI: The new standard for AI in project controls."*

## The editorial rule still applies

Every claim in this film traces to a live platform page via
`../../messaging/institutional/`. Three claims that appear in the 15-second film
and the root README are **deliberately absent here**, because reconciliation
against the live platform found no source for them: the 1 September 2026 launch
date, the 25-country chapter count, and the seven launch languages. See the
claims audit in `script.md`.

No credential holders are implied anywhere. Nobody has yet been certified, so the
film speaks about the standard and the invitation — never about people who hold
it.
