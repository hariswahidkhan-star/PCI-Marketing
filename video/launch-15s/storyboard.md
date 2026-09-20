# PCI post-launch film — storyboard

15.0 s · 30 fps · 450 frames · cross-dissolve 0.30 s between shots.

The film is built as five shots over one continuous background. The background is
not wallpaper: a faint **S-curve** — the cumulative-progress curve every project
controls professional reads every month — draws across the entire 15 seconds,
left to right, underneath all five shots. It is the only element that ignores the
cuts, so the film reads as one movement rather than five cards.

---

## Shot 1 — Title · 0.00 → 3.40

Left-aligned, matching launch deck p.1.

| t | Event |
|---|---|
| 0.10 | Topbar (PCI AI lockup) fades up |
| 0.18 | Eyebrow `NOW LIVE · 1 SEPTEMBER 2026` rises |
| 0.34 | Crimson→blue rule wipes left-to-right |
| 0.46 | Headline words rise in 75 ms stagger, masked per line |
| 1.20 | Sub-line fades up |
| 0.30 | **VO 1** — "Project controls now has a professional home." |

**Why left-aligned:** it is the only shot that quotes the deck's cover directly.
Recognition matters most in the first second.

---

## Shot 2 — The governing principle · 3.40 → 6.80

Centred. The film's still point.

| t | Event |
|---|---|
| 3.54 | Eyebrow `THE GOVERNING PRINCIPLE` |
| 3.70 | "AI proposes." — 85 ms word stagger |
| 4.26 | "The professional disposes." — lands as a separate thought |
| 4.80 | Rule wipes |
| 4.98 | Sub-line |
| 3.70 | **VO 2** — the doctrine line |

**Why two beats, not one:** the whole proposition is the gap between the two
sentences. Animating them as one line would throw the idea away.

---

## Shot 3 — What is live · 6.80 → 9.90

Centred. Three chips, then the substantiation row.

| t | Event |
|---|---|
| 6.92 | Eyebrow `LIVE WORLDWIDE` |
| 7.10 | PCL-AI → PFL-AI → PML-AI, 140 ms apart |
| 7.45 | A single light sheen sweeps across the chips (1.1 s) |
| 7.72 | Fact row: 13 domains · 25 chapters · publicly verifiable |
| 6.95 | **VO 3** — "…is live, worldwide." |

**Why the chips stagger:** three credentials arriving together read as a menu.
Arriving in sequence they read as a suite, which is what they are.

---

## Shot 4 — The invitation · 9.90 → 13.10

Centred. The shot the film exists for.

| t | Event |
|---|---|
| 10.02 | Eyebrow `AN OPEN INVITATION` |
| 10.16 | "Help us build it." |
| 10.60 | CONTRIBUTE → SHAPE → SHARE → CONNECT → LEAD, 95 ms apart |
| 11.22 | Sub-line naming what each verb means |
| 10.05 | **VO 4** — "Bring your expertise. Help us build it." |

**Why verbs and not sentences:** the voiceover has 7 words here. The five
invitations from the brief are delivered as type, in rhythm, while the voice makes
the ask. Type carries the specifics; the voice carries the intent. The score lifts
to an added ninth under this shot — the only brightening move in the piece.

---

## Shot 5 — End card · 13.10 → 15.00

Centred. Topbar retires; the mark takes over.

| t | Event |
|---|---|
| 13.20 | Mark scales 0.86 → 1.00 |
| 13.38 | PCI AI wordmark |
| 13.62 | "AI proposes. The professional disposes." |
| 13.84 | projectcontrolsinstitute.org |
| 14.04 | Legal line — Delaware Non-Stock Corporation; not yet accredited |
| 13.10 | **Score only.** No voiceover. |

**Why the legal line is in the film and not just the post copy:** the Institute's
whole position is that it does not overstate. A launch film that omits the
accreditation status while a caption elsewhere carries it would be doing exactly
what the brand says it will not do. It costs 1.9 seconds of screen space and buys
the one thing a certification body cannot buy back.

---

## Score map

D minor, 104 bpm, original (`src/music.py` — synthesised from scratch, no
samples, no licence obligation). The kit itself comes from `video/lib/score_kit.py`,
shared with the other two films so all three sit on one tempo and one drum voice.

Fifteen seconds has no room to build, so the kit is in from the first bar and
tightens rather than arrives: eighths to sixteenths under the ask at 9.90, then
out of the way for the resolve. Its energy sits below ~120 Hz and above ~6 kHz,
leaving the mid-range clear for the read.

| t | Musical event |
|---|---|
| 0.0 | Sub bed enters, 1.6 s attack |
| 0.10, 3.40, 6.80, 9.90, 13.10 | A soft bell on each cut — the edit gets an audible reason |
| 0.5 | Dm pad opens |
| 9.70 | Added 9th lifts under the invitation |
| 13.05 | Resolve to an open D5 under the end card |
| 13.9 → 15.0 | Fade |

Peak −7.4 dBFS, roughly −23 LUFS — sits under a voiceover without ducking.

---

## Frame budget

| Shot | Frames | % |
|---|---|---|
| 1 Title | 102 | 23% |
| 2 Principle | 102 | 23% |
| 3 What is live | 93 | 21% |
| 4 Invitation | 96 | 21% |
| 5 End card | 57 | 13% |

The invitation gets as much screen time as the credential suite. That is
deliberate: the brief's purpose is participation, not enrolment.
