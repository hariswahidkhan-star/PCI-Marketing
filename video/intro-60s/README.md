# PCI AI introduction film — 60 seconds

A longer companion to `../launch-15s/`. Where that film **announces**, this one
**explains**: what the discipline faces, what the Institute is for, and exactly
where it stands today.

| | |
|---|---|
| Duration | 60.000 s |
| Aspect | 16:9, 1080p, 25 fps |
| Voice | ElevenLabs, British narrative register |
| Script | `script.md` — copy, timings, on-screen type, claims audit |
| Cue sheet | `vo/cues.json` |

---

## Contents

| Path | What it is |
|---|---|
| `script.md` | The film. Nine VO beats, nine shot windows, direction notes, claims audit |
| `vo/pci-intro-60s-vo-bed.wav` | **The deliverable voice track** — 60.000 s, 48 kHz / 24-bit mono |
| `vo/pci-intro-60s-vo-take-1.mp3` | Raw ElevenLabs take 1 (47.31 s continuous read) |
| `vo/pci-intro-60s-vo-take-2.mp3` | Raw ElevenLabs take 2 (46.44 s) — the alternate |
| `vo/cues.json` | Measured in/out for all nine lines, machine-readable |

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
negotiable — the eyebrow, the crimson→blue rule and the end card are laid over
the footage in the edit, from the same design tokens as `../launch-15s/`.

---

## What still needs a human

- **Type pass.** On-screen copy is specified verbatim in `script.md`; it is not
  yet burned in. Shot 9's end card carries the legal line and cannot ship without
  it.
- **Grade.** The six clips are generated independently and will not match. They
  need a single pass to the navy/grey palette.
- **Score.** `../launch-15s/src/music.py` produces the house bed; the 6.60 s tail
  is scored, not silent.
- **Listen to beat 8** (42.71 s). The founding-stage line must sound level and
  unembarrassed. Take 2 is the alternate if take 1 reads as apologetic.

---

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
