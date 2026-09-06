# Honorary Fellow (PCI) — lead-generation film (1:59)

A bright, premium institutional film for **PCI AI — Project Controls Institute
Global, Inc.**, inviting distinguished professionals to apply for **Honorary
Fellow (PCI)**. Ten scenes: the question, the recognition, what it is, who may
apply, the industries, the eligibility requirements, the application evidence,
what recognition brings, discipline alignment, and the invitation to apply.

**The one thing this film must never do** is describe Honorary Fellow (PCI) as an
examined certification, licence or accreditation. It is a board-conferred
recognition, involving no examination, separate from PCI's examined
certifications — PCL-AI, PFL-AI and PML-AI. Every scene was written against that
line, and `claims-register.md` traces every statement to the PCI page that
supports it.

```bash
cd src && ./build.sh
```

---

## What is in `dist/`

| File | Use |
|---|---|
| `pci-honorary-fellow-3840x2160-MASTER-captions.mp4` | **4K master, captioned.** Website, YouTube, presentations |
| `pci-honorary-fellow-3840x2160-MASTER-clean.mp4` | 4K master, no burned-in captions |
| `pci-honorary-fellow-1920x1080-captions.mp4` | HD, captioned |
| `pci-honorary-fellow-1920x1080-clean.mp4` | HD, clean — a Lanczos downscale of the 4K clean master |
| `pci-honorary-fellow-1920x1080-silent.mp4` | Picture only |
| `pci-honorary-fellow-1080x1920-captions.mp4` | **9:16 vertical** — LinkedIn, Reels, short-form |
| `pci-honorary-fellow-1080x1080-captions.mp4` | **1:1 square** — LinkedIn, social advertising |
| `…-voiceover.wav` / `…-mixed-soundtrack.wav` / `…-score.wav` | Audio stems |
| `.srt` / `.vtt` / poster / thumbnails | Captions and stills |

The vertical and square cuts are **real layouts, not crops**: the same
`scene.html` lays every scene out again for each aspect, and the audit below runs
against each one separately.

Delivery format is H.264 High (Level 5.1 for the 4K pair, 4.1 for HD), yuv420p,
`+faststart`, AAC 192 kbps 48 kHz — within YouTube, LinkedIn and Vimeo specs
without re-encoding.

---

## Accuracy first

`pciai.org` is unreachable from this build environment (the network policy
answers 403), so verification was done against `PCI/backend/wwwroot` — the
source the live site is served from. The register records this, and names the
rows to re-read against the live pages before publication.

Four benefit claims in the brief's draft narration could not be traced to any
PCI page and were **replaced or cut, not softened**: a LinkedIn-shareable badge
(the site attaches that to *earned* credentials only), event and webinar
invitations, community connection, and community visibility. In their place the
film says what the site does support — that the award is recorded so anyone can
verify it at source, clearly labelled honorary and never a passed examination,
and that accepted applicants *may* receive access to selected learning resources,
subject to programme terms. Detail in `claims-register.md` §3.

One page was deliberately **not** used: `fellowship-policy.html` describes the
*membership* Fellow grade, whose criteria are "in development" and whose
nominations have not opened. The honorary route is live and accepting
applications; quoting the membership policy would have described a programme
that does not exist yet.

---

## The voice, and the duration it forced

Narration is ElevenLabs **"Holden Pro Voice"** (`UudLhsL2DlHkDK0vGwl3`) on
`eleven_v3` — the voice the brief names, a stock library voice, **not a clone of
any real person**. Direction is carried as punctuation per the v3 guide: an
ellipsis is a longer pause, an em-dash a short beat, capitals mark emphasis. The
brief's arc — quiet confidence, building through industries and leadership,
warmth on contribution, strength at the close — is in the density of that
direction, which rises and then resolves.

**The brief's script did not fit its own duration.** Read at the deliberate pace
the brief also asks for, the full narration ran **146 s** against a 105–120 s
cap. Speeding the narrator up 16% would have made a deep, mature read sound
rushed — the one delivery the brief rules out — so six scenes were tightened
and their detail moved on screen, with every mandated statement kept word for
word: eight years, three managerial, no examination, board discretion, no
guarantee, no entitlement, separate from PCL-AI/PFL-AI/PML-AI, and the
discipline-alignment clarification. The tightened read measures 124.2 s; a
**3.9 % formant-preserved conform** lands it at **119.50 s**. `sync.py` refuses
anything past 8 % and asks for a copy trim instead, so a rushed read cannot be
shipped by accident.

Everything downstream reads that measurement. `scene.html` carries no timings;
`vo.py` takes caption windows from `timeline.json`; `music.py` places its scene
markers from the same list. Nothing is hand-nudged.

---

## The score

Original, standard-library-only, no samples and no licence obligation. The brief
asks for restrained piano and atmospheric tones rising into confident orchestral
and modern electronic elements — an arc, so the score is built as one: felt piano
alone for the first three scenes, a detuned string stack arriving where the film
turns to *who it is for*, and a kit only above the midpoint of the curve. F major
throughout, with the relative minor used only under the two scenes that carry
qualification — no examination and board discretion; the criteria and the
reminder that meeting them guarantees nothing.

The kit lives below ~120 Hz and above ~6 kHz. A piano cannot make that claim, so
it is voiced an octave above its natural register with its harmonics almost
suppressed, and the level is set from measurement: in the finished mix, during
the loudest scene, the music adds **−0.3 dB** to the voice band — the narration
is effectively alone where speech lives. Mix: −16.2 LUFS, −2.0 dBTP. The
`alimiter` `level=disabled` note in `build.sh` explains why that ceiling is real.

The kit is shared with the other three films via `video/lib/score_kit.py`; this
file holds only what should differ — tempo (88 bpm), harmony, arrangement, the
curve.

---

## Look

Bright, as the brief requires: a sequence of papers rather than one flat white,
so two minutes of bright never goes clinical. Brand navy, PCI blue and controlled
red accents. **Gold is reserved.** It appears on exactly three honorary beats —
the name of the recognition, what recognition brings, and the close — and never
near the PCL-AI/PFL-AI/PML-AI cards, so it reads as distinction rather than
decoration.

The PCI logo is in the masthead of every scene, and large and animated at the
open and the close. `pciai.org` is in the footer of every scene and on the close
frame with `Members@pciai.org`. The end frame carries the brief's legal text at
a readable size for the whole closing scene.

**No stock footage and no generated imagery.** Every frame is computed from
`scene.html` — typography, layout and vector motion. There are no photographs of
people: no synthetic person is presented as a PCI fellow, applicant or board
member, which is the failure a photoreal treatment of this subject would risk.
The industry and applicant sequences are typographic.

---

## Verified after build

`src/probe.mjs` runs four checks on every aspect, sampled every 0.5 s: page
errors, horizontal overflow (transitions excluded), scene content colliding with
the caption band, and scene content colliding with the fixed furniture. Clean on
16:9, 9:16, 1:1 and 3840×2160 — **952 samples, zero findings.**

Two faults it caught before render are worth recording. The brand assets were
missing from this film's directory, so the first audit measured fallback fonts
and its findings were meaningless. And `vo.py` was reading a timeline key that
`sync.py` never writes, so captions were silently on a 130 wpm estimate rather
than the measured audio — the exact drift the single-source design exists to
prevent. That is now an error, not a fallback.

```
claims-register.md   every statement traced to a PCI page; what was cut, and why
src/vo.py            the read + all three caption forms; measured windows only
src/sync.py          measures the voice, conforms to 119.50s, refuses past 8%
src/scene.html       the film — deterministic, reads its cut list from data
src/music.py         piano -> strings -> kit, F major, from the shared kit
src/build.sh         sync -> captions -> score -> mix -> 4K pair -> HD trio
src/probe.mjs        four-check layout audit
```
