# Honorary Fellow (PCI) — lead-generation film (4:11)

A bright, premium institutional film for **PCI AI — Project Controls Institute
Global, Inc.**, inviting distinguished professionals to apply for **Honorary
Fellow (PCI)**. Thirteen scenes: the question, the recognition, the Institute,
what it is, who may apply, the industries, the eligibility requirements, the
application, putting yourself forward, the registry, what recognition opens,
discipline alignment, and the invitation to apply.

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
and what accepted applicants *may* receive, subject to programme terms. Detail
in `claims-register.md` §3 and §3a.

One page was deliberately **not** used: `fellowship-policy.html` describes the
*membership* Fellow grade, whose criteria are "in development" and whose
nominations have not opened. The honorary route is live and accepting
applications; quoting the membership policy would have described a programme
that does not exist yet.

---

## The pitch cut

After the first cut PCI asked for the film to *sell* — maximum applications,
and they will share it. The copy was rewritten as a pitch without changing a
single fact: second-person address throughout, the true levers in the order
that converts (**no fee → no examination → PCI's own registry → one application
→ individual Board review**), a hero line on the application scene, and a
benefits grid. What the pitch does **not** do, on PCI's own rules: it never
calls fellows "members" — the honorary route is a recognition, not a
membership grade — never implies scarcity or a deadline, never promises a
career outcome, and keeps every qualifying sentence spoken and on screen.
`share-kit.md` carries the same rules into the LinkedIn post, YouTube
description and short caption, with a "do not add" list for the lines that
read well and are all prohibited. "Enhance career" was declined outright: the
brief and PCI's site-wide disclosure both forbid career-outcome claims.

## The authority cut

PCI's next round asked for more: a harder sell built with a psychologist and a
professional copywriter, more about the Institute and its value, the resources
a recognised fellow may use (video lectures, course material, the simulation
lab), a louder mix, a more authoritative voice, no time limit — and the script
judged by a panel of an ACCA member, a PMP PMO director, a CFA charterholder and
a senior project-controls director.

The panel's verdicts and every edit they produced are in `claims-register.md`
§3b. The ones that changed the film: *"not yet accredited"* became the site's
own *"not currently accredited by ANAB, IAS or any ISO/IEC 17024 body"*; the
optional awards-ceremony charge is now spoken in the same breath as "no fee";
"public register" became *"PCI's own public registry — checkable at source"*;
the self-nomination scene now pairs *no sponsor needed* with the Board's
scrutiny against published criteria; the narration says what PCI legally is;
"cost engineering" was corrected to the site's "cost control"; "apply today"
went; and the close sets a test rather than paying a compliment.

**One thing the panel flagged that PCI overruled.** All four judges called the
benefits scene a publication blocker: video lectures, the simulation lab and
PCI AI events are on no PCI page. They are in the film on PCI's explicit
instruction, with one "may" governing every item and "all subject to current
programme terms" — and the register's condition stands: **the application page
must name them before the film is published.** What the panel asked for and
could not be given — who sits on the Board, who already holds the recognition,
how old PCI is — is absent because no PCI page states it.

## Pacing

Thirteen scenes, no time-scaling, a **1.5-second beat** between every topic: the
caption clears, a moment of silence, the picture changes, and only then does
the next topic begin with the voice. Running time **250.54 s**. `sync.py`'s
cap is 300 s and it still refuses anything past 8 %, so a rushed read cannot be
shipped by accident.

Captions are cut to the breath. The v3 read spells out P-C-I and I-S-O I-E-C
slowly, so proportional caption splits drifted by a phrase; `vo.py` now carries
the measured end of each cue — the midpoint of the silence it ends on, from
`silencedetect` at −38 dB, chosen from the candidates so that the implied
speaking rate stays level across the scene — and `sync.py` uses those directly. Fifty cues,
two lines each, three at most — which is also what lets the caption band sit
higher and gives the three densest scenes their room.

## The voice

Narration is ElevenLabs **"Holden Pro Voice"** (`UudLhsL2DlHkDK0vGwl3`) on
`eleven_v3` — the voice the brief names, a stock library voice, **not a clone
of any real person**. When PCI asked for a more authoritative read, three
candidates were tested on the same two scenes (`audio/voice-test-authority/`):
Holden directed harder, Jim Executive (the narrator of PCI's other three
films) and Leo. **PCI chose Holden**, so every scene is directed `[deep, slow,
commanding]`, with punctuation carrying the rest per the v3 guide: an ellipsis
is a longer pause, an em-dash a short beat, capitals mark emphasis. The full
Jim Executive read of the same script is kept in `audio/jim-executive-authority/`
and the previous cut's Holden takes in `audio/old-paced-holden/`; switching is
one re-generation.

Every take was transcribed back (ElevenLabs Scribe) and matched against its
script word for word before it was used — v3 can improvise, and a narration
that drifts from the register would be a claim nobody checked.

Everything downstream reads the measured audio. `scene.html` carries no
timings; `vo.py` takes caption windows from `timeline.json`; `music.py` places
its scene markers from the same list. Nothing is hand-nudged.

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
the loudest scene the narration sits **7.1 dB** above the music in the voice
band, measured in the finished mix (speech against the music-only beat that
follows it). PCI asked for a louder film, so the
mix now targets **−14 LUFS** — what YouTube and LinkedIn normalise to, so it
arrives as loud as the platform allows and no quieter than the video before it.
Measured: **−14.2 LUFS integrated, −1.5 dBTP.** The `alimiter` `level=disabled` note in
`build.sh` explains why that ceiling is real.

The kit is shared with the other three films via `video/lib/score_kit.py`; this
file holds only what should differ — tempo (88 bpm), harmony, arrangement, the
curve.

---

## Look

Bright, as the brief requires: a sequence of papers rather than one flat white,
so four minutes of bright never goes clinical. Brand navy, PCI blue and controlled
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

`src/probe.mjs` runs five checks on every aspect, sampled every 0.5 s: page
errors, horizontal overflow (transitions excluded), scene content colliding with
the caption band, scene content colliding with the fixed furniture, and **text
clipped inside its own box**. Clean on 16:9, 9:16, 1:1 and 3840×2160 — **2,004
samples, zero findings.**

It earned its keep again on this cut. The first probe of the authority script
returned findings in six scenes: the new Institute scene and the enlarged
role and industry lists were taller than their padding box, and cues of up to
seven lines were rising into everything above them. The fix was structural —
compact stats, the dense pill size for the two long lists, one note in place of
a sub-headline and a note on the application scene, and captions cut to the
breath — and the probe was re-run on all four sizes until it returned nothing.

The fifth check exists because PCI found what the other four could not: a card
subtitle cut off mid-word ("LABELLED HONORA"). The card is `overflow:hidden`
for its corner radius, so a `white-space:nowrap` subtitle wider than the card
was swallowed silently rather than pushed out where the stage-overflow check
would see it. The `nowrap` is gone, the check now compares every text leaf
against the nearest clipping ancestor, and it found the same fault in scene 3
on its first run. The `.ln` reveal mask is excluded — it clips on purpose.

Two faults it caught before render are worth recording. The brand assets were
missing from this film's directory, so the first audit measured fallback fonts
and its findings were meaningless. And `vo.py` was reading a timeline key that
`sync.py` never writes, so captions were silently on a 130 wpm estimate rather
than the measured audio — the exact drift the single-source design exists to
prevent. That is now an error, not a fallback.

```
claims-register.md   every statement traced to a PCI page; what was cut, and why
src/vo.py            the read + all three caption forms; measured windows only
src/sync.py          measures the voice; explicit cue ends; refuses past 8%
src/scene.html       the film — deterministic, reads its cut list from data
src/music.py         piano -> strings -> kit, F major, from the shared kit
src/build.sh         sync -> captions -> score -> mix -> 4K pair -> HD trio
src/probe.mjs        five-check layout audit
share-kit.md         LinkedIn, YouTube and short-form copy, same rules as the film
```
