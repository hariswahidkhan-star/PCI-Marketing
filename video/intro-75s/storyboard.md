# Time-coded storyboard — PCI AI 75-second institutional film

75.00 s · 30 fps · delivered at 1920×1080, 1080×1920 and 1080×1080.
Source of truth: `SHOTS` and `CUES` in `src/scene.html`. Keep this file in step.

**Grade note.** The brief says not to make every scene predominantly blue. The
film is graded as a **journey through warmth**: it opens on a warm charcoal,
cools into slate for the disciplines, warms hard into umber for the caution
beat, settles to authoritative ink for governance, and then — at the closing
statement — **inverts entirely to a pale ground**. That inversion is the one
big visual move in the film, and it is timed to the one line that asks
something of the viewer. Colour is carrying the argument, not decorating it.

---

| # | In → Out | Ground | On screen | Motion | Voiceover |
|---|---|---|---|---|---|
| **S1** | 0.00 → 8.50 | Warm charcoal `rgb(20,18,26)`, crimson-weighted glow | Eyebrow `AN INTRODUCTION` · crimson→blue rule · **"Ambition requires control."** · sub: *A controlled, financeable and deliverable outcome takes more than information.* | Left-aligned. Rule wipes from left; headline words rise in a 0.085 s stagger; sub settles last | *Every major project begins with ambition. Turning that ambition into a controlled, financeable and deliverable outcome requires more than information.* |
| **S2** | 8.50 → 16.60 | Slate `rgb(16,25,35)`, cool | Eyebrow `THE INTEGRATED DISCIPLINE` · five pills **SCOPE · SCHEDULE · COST · FINANCE · RISK** · sub naming *performance* and accountable decisions | Pills rise on a 0.115 s stagger, left to right — the disciplines assembling | *Project professionals must connect scope, schedule, cost, finance, risk and performance while making accountable decisions in increasingly complex environments.* |
| **S3** | 16.60 → 26.90 | Umber `rgb(30,21,18)`, warmest in the film | Eyebrow `WHAT AI CHANGES — AND WHAT IT DOES NOT` · four rules: *Accelerate analysis · Identify patterns · Compare scenarios · Support forecasting* · **"Faster analysis does not remove accountability."** | The four capabilities arrive first and settle; the headline lands **after** them, at 1.35 s — the turn in the argument is staged, not stated | *Artificial intelligence can accelerate analysis, identify patterns, compare scenarios and support forecasting. But a convincing AI output is not automatically a reliable project decision.* |
| **S4** | 26.90 → 36.30 | Ink navy `rgb(15,23,42)` — the authority beat | Eyebrow `RESPONSIBLE ADOPTION` · **"Evidence. Governance. Human judgment."** · five columns: *Verified data · Transparent assumptions · Meaningful human review · Clear decision rights · An evidence trail that withstands challenge* | Headline first, then the five requirements on a 0.125 s stagger | *Responsible adoption requires verified data, transparent assumptions, meaningful human review, clear decision rights and an evidence trail that can withstand professional challenge.* |
| **S5** | 36.30 → 47.40 | Near-black blue `rgb(10,15,28)` | **PCI mark at full size** · `PCI AI` · *Project Controls Institute Global, Inc.* · rule · sub on governing AI-supported work | Persistent top bar **retires** so the mark can carry the frame; mark scales 0.88 → 1.00 | *PCI AI — Project Controls Institute Global — focuses on the professional competence needed to govern AI-supported work across project controls, project finance and project management.* |
| **S6** | 47.40 → 57.60 | Graphite plum `rgb(24,20,29)` | Eyebrow `THE CREDENTIAL FRAMEWORK` · three chips **PCL-AI** / **PFL-AI** / **PML-AI** with their disciplines · **the accreditation-status line, on screen** | Chips arrive on a 0.165 s stagger; a single sheen sweeps across them at 48.6–50.0 s. The status line follows at 1.35 s and holds | *Its professional credential framework includes PCL-AI for project controls, PFL-AI for project finance and PML-AI for project management.* |
| **S7** | 57.60 → 70.80 | **LIGHT — `rgb(233,237,244)`, ink type** | Eyebrow `THE PROFESSIONAL JUDGMENT` · **"Trust responsibly. / Challenge professionally. / Remain accountable."** · rule | The full inversion: ground, type, furniture, grid, vignette and the caption box all cross-fade to the light palette over 0.42 s. Three lines rise on a 0.105 s stagger | *The future of project delivery will not be defined by technology alone. It will be shaped by professionals who know when to trust, when to challenge and how to remain accountable.* |
| **S8** | 70.80 → 75.00 | Ink navy `rgb(15,23,42)` | Mark · `PCI AI` · *Project Controls Institute Global, Inc.* · **pciai.org · projectcontrolsinstitute.org** · full legal + accreditation line | Returns to dark. Furniture retires again; mark scales up; URLs then legal | *Discover PCI AI at pciai.org.* (spoken "P-C-I-A-I dot org") |

---

## Continuous elements

**The S-curve.** A single cumulative-progress curve — the project-controls
motif — draws across the background from 1.0 s to 62.0 s, one continuous
stroke spanning the whole film. It is the only element that ignores the cuts,
and it is what makes eight scenes read as one piece. It dims and shifts to a
darker blue under the light scene so it never fights the type.

**Cross-dissolves.** 0.42 s, with a ±1.6 % horizontal parallax — the outgoing
scene drifts left, the incoming settles from the right. No wipes, spins, flares
or zooms. The brief asked for restraint and the cut list keeps it.

**Brand furniture.** Top bar (mark, `PCI AI`, legal name) and the footer rule
with `PROJECT CONTROLS INSTITUTE` / `pciai.org` are persistent, and retire only
for S5 and S8, where the mark is the subject.

**Captions.** Burned in on the captioned masters, from the same source as the
`.srt` and `.vtt` (`src/vo.py`), so the three can never drift. Balanced to a
54-character line, up to three lines. The box inverts with the light scene.

---

## Aspect behaviour

Not a centre-crop. One source, three genuine layouts.

| | 16:9 (1920×1080) | 1:1 (1080×1080) | 9:16 (1080×1920) |
|---|---|---|---|
| Type scale | nominal 1920 | nominal 1350 | nominal 1180 |
| S1 headline | 2 lines | 3 lines | 3 lines |
| Discipline pills | one row of 5 | **wraps to 3 + 2** | **stacked column** |
| Credential chips | one row of 3 | one row of 3, tighter | **stacked column** |
| S3 / S4 lists | 4- and 5-across | narrowed columns | **stacked** |
| Bottom safe area | 19 units | 20 units | 30 units |

The safe areas are sized so nothing collides with a three-line caption. That is
verified mechanically, not by eye: `src/probe.mjs` steps the film every 0.5 s in
all three aspects (450 checks) and asserts that no shot element intersects the
caption box. **Current result: zero collisions, zero page errors.**
