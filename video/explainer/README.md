# PCI AI — explainer film (3:53)

A structured explainer for **PCI AI — Project Controls Institute Global, Inc.**
answering four questions in order: **why the Institute exists**, **what its
objective is**, **what the three certifications actually are and assess**, and
**which industries they support**.

Where the 75-second film makes an argument, this one gives the detail behind it.
It is organised into **seven chapters across sixteen scenes**, with a chapter
rail and a progress bar on screen throughout — four minutes is long enough that
a viewer needs to know where they are.

**The film is bright.** It runs on a light ground: ink type on paper, with the
brand blue and crimson doing the accent work. Both themes come from one source —
`?theme=light` (the default) and `?theme=dark` — so the ink treatment is a flag,
not a fork:

```bash
THEME=dark ./build.sh      # the original dark-ground cut, same everything else
```

```bash
cd src && ./build.sh
```

---

## What is in `dist/`

| File | Use |
|---|---|
| `pci-ai-explainer-1920x1080-captions.mp4` | **Primary.** Website, YouTube, LinkedIn |
| `pci-ai-explainer-1080x1920-captions.mp4` | Vertical — a real layout, not a crop |
| `pci-ai-explainer-1920x1080-clean.mp4` | No burned-in captions; upload the `.srt` |
| `pci-ai-explainer-1920x1080-MASTER.mp4` | High-quality master (CRF 14) |
| `pci-ai-explainer-1920x1080-silent.mp4` | Picture only |
| `…-voiceover.wav` / `…-mixed-soundtrack.wav` / `…-score.wav` | Audio stems |
| `.srt` / `.vtt` / poster / 2 thumbnails | Captions and stills |

**No 1:1 cut.** Nobody watches a four-minute square video. It is one command
away if you want it: `node render.mjs --w 1080 --h 1080 --cc 1 --out ../build/f-1x1-cc`.

---

## Voice first, picture second

This film reverses the order the other two were built in, and it is the better
way round.

The narration was generated **one scene at a time** — sixteen takes, not thirty —
so sentences that belong together were synthesised together and keep their
natural phrasing. `src/sync.py` then measures the result: it de-silences each
scene, finds the caption boundaries by detecting the reader's own internal
pauses, lays the scenes out with a 0.62 s beat between them, and writes
`timeline.json` and `shots.data.js`.

**Everything downstream reads that measurement.** `scene.html` carries no
timings of its own; `vo.py` takes caption times from it; `music.py` places a bell
on every scene change and a deeper one on every chapter change from the same
list. So the cut, the captions and the score cannot drift from the voice, because
none of them is written by hand.

Nothing is time-stretched. There is no fixed duration to hit, so the film simply
runs at the pace the read wants — 233.14 s.

**One honest note:** silence detection found the segment boundaries in fifteen of
sixteen scenes. Scene 16 fell back to a proportional split by word weight, and
`sync.py` prints which scenes did so rather than hiding it.

## Why bright is not just "the dark one inverted"

A light ground is easy to get wrong across four minutes: a single flat white
goes clinical fast. So the light set is a **sequence of papers** — warm, cool,
cream — graded exactly the way the dark set moves through warmth. The ambient
glows are damped to 55 %, because on paper they shift the ground far more than
they do on ink.

The accent also changes step. On the dark ground the film uses `#3B82F6`; on
paper it uses **`#1D4ED8`**, the deeper brand blue, which is the step that holds
contrast against white — and the one validated against a light surface.

## The examination-weighting chart

Scene 10 shows the 40/40/20 split as **three separate direct-labelled bars, not
one stacked bar.** A stacked bar would have needed three categorical hues, and
the two brand blues fail a colourblind-safety check against each other — the
validator returned a normal-vision ΔE of 13.9, below the floor of 15. Rather than
introduce an off-brand fourth colour, the form changed: with each bar named in
place, identity comes from the label and colour is only reinforcement. Brand blue
carries the two 40 % discipline groups; crimson marks governed AI as the distinct
third.

The pair was re-validated against the **light** surface when the film went
bright — it is a different check, not the same one — and passes: ΔE 27.7 protan,
35.6 normal vision, both marks above 3:1 contrast against the ground.

## Files

```
claims-register.md   every statement traced to a first-party page
src/vo.py            the read + all three caption forms
src/sync.py          measures the voice; writes timeline.json + shots.data.js
src/scene.html       the film — deterministic, reads its cut list from data
src/music.py         chapter-aware score, from scratch, stdlib only
src/build.sh         sync -> captions -> score -> mix -> frames -> masters
src/probe.mjs        layout + caption-collision audit (0 collisions, 0 errors)
```

Verified after build: **zero page errors and zero caption collisions** across all
three aspects, sampled every 0.5 s.
