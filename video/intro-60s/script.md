# PCI AI introduction film — script

60 seconds. Institution voice. British English.

The 15-second launch film announces. This one **explains** — what the discipline
faces, what the Institute is for, and exactly where it stands today. The honest
status beat is not a disclaimer bolted to the end; it is the fifth act of the
argument, and the reason the film is worth believing.

---

## The arithmetic

A professional, unhurried corporate read runs **140–155 words per minute**. Sixty
seconds is therefore **140–155 words wall-to-wall** — and wall-to-wall is wrong
for an authority piece.

This script is **112 words** across nine lines, leaving roughly 14 seconds of
silence distributed as eight beats. The pauses carry the register.

---

## Voiceover

| # | In | Out | Line | Words | Direction |
|---|---|---|---|---|---|
| 1 | 0.60 | 4.18 | Every project runs on numbers someone has to be accountable for. | 11 | Settled, factual. Land "accountable". No lift at the end. |
| 2 | 5.38 | 10.23 | AI can now produce those numbers in seconds. It can also be confidently wrong. | 14 | Second sentence slower. "Confidently wrong" is the hinge of the film — do not soften it, do not sell it. |
| 3 | 11.43 | 14.67 | AI proposes. The professional disposes. | 5 | The doctrine line. Full stop after "proposes" — a real beat. Weight, not volume. |
| 4 | 15.87 | 20.22 | The Project Controls Institute certifies the professional who knows the difference. | 11 | Warm. This is the first mention of the Institute; let the name sit. |
| 5 | 21.42 | 26.83 | Three credentials. One standard. Governed AI at its core, not bolted on. | 12 | Crisp, listed. "Not bolted on" is dry, almost thrown away. |
| 6 | 28.03 | 34.54 | Thirteen domains, sixty-one knowledge areas, and an examination built on judgement rather than recall. | 14 | Even pace through the numbers. Do not accelerate — the specificity is the point. |
| 7 | 35.74 | 41.51 | The only entry requirement is three years' experience, in any field. There is no degree barrier. | 16 | Open, direct. This is the film's most generous line; deliver it as fact, not as a boast. |
| 8 | 42.71 | 48.66 | We are a founding-stage body, and not yet accredited. We are building toward it, and we say so plainly. | 19 | The most important read in the film. Level, unembarrassed. A body that states its own limits is not apologising. |
| 9 | 49.86 | 53.40 | Project controls has a professional home. Help us build it. | 10 | Direct address. Open, unhurried. Do not sell it. |

**Total: 112 words. Tail 53.40–60.00 is score only, under the end card.**

Timings above are **measured from the delivered bed** (`vo/pci-intro-60s-vo-bed.wav`,
60.000 s), not estimated: take 1 was split at its detected line boundaries and
respaced to an even 1.20 s beat. Cue sheet in `vo/cues.json`.

### Casting note
Mid-range, unforced authority. British English. The reference is a national
broadcaster's documentary narration, not a product advert. No upward inflection at
line ends, no smile-in-the-voice, no urgency. A voice that sounds like it has
nothing to prove — because the script's credibility comes from what it declines to
claim.

Consistency with `video/launch-15s/` matters more than the individual choice: the
same voice should carry both films.

### Recording note
- At least **300 ms of clean handle** before line 1 and after line 9.
- Dry, unprocessed WAV (48 kHz / 24-bit) plus a processed pass.
- Two reads of **line 3** — one level, one with a longer beat after "proposes."
- Two reads of **line 8** — the founding-status line must not sound apologetic in
  either take. If it sounds like an apology, the film has failed.

---

## On-screen text (verbatim)

| Shot | Window | Type on screen |
|---|---|---|
| 1 | 0.00–4.78 | `THE DISCIPLINE` — **Every project runs on numbers.** — Planning · cost · forecasting · earned value · risk |
| 2 | 4.78–10.83 | `WHAT CHANGED` — **Seconds to produce. Still yours to defend.** — AI can be confidently wrong |
| 3 | 10.83–15.27 | `THE GOVERNING PRINCIPLE` — **AI proposes.** / **The professional disposes.** |
| 4 | 15.27–20.82 | `THE INSTITUTE` — **Project Controls Institute** — An independent professional body for the integrated discipline |
| 5 | 20.82–27.43 | `THE CREDENTIALS` — **PCL-AI** Project Controls · **PFL-AI** Project Finance · **PML-AI** Project Management — one standard, governed AI at its core |
| 6 | 27.43–35.14 | `THE STANDARD` — **13 domains · 61 knowledge areas** — Scenario-based examination · 40 / 40 / 20 weighting |
| 7 | 35.14–42.11 | `OPEN BY DESIGN` — **Three years' experience. Any field.** — No degree barrier · assessed on capability |
| 8 | 42.11–49.26 | `WHERE WE STAND` — **Founding stage. Not yet accredited.** — Developed with reference to ISO/IEC 17024 personnel-certification principles · building toward formal accreditation · enrolment open, examinations forthcoming |
| 9 | 49.26–60.00 | PCI AI / Project Controls Institute Global, Inc. — "AI proposes. The professional disposes." — projectcontrolsinstitute.org — *Delaware Non-Stock Corporation. Intends to seek 501(c)(3); not yet granted. Not accredited by ANAB, IAS or any ISO/IEC 17024 body.* |

Shot 8 is the film's spine. It holds for **7.15 seconds**, and it is the only
shot whose type is a list of limits rather than a list of strengths — because the
claim it makes is the one a certification body is least expected to make about
itself. It must not be cut short in any edit.

---

## Claims audit

Every factual claim in the film, and where it comes from. Sources are live pages
in `hariswahidkhan-star/PCI`, verified via `messaging/institutional/`.

| Claim | Source | Status |
|---|---|---|
| "AI proposes. The professional disposes." | `index.html` display copy; JSON-LD `slogan` site-wide | ✅ |
| Independent professional body | `about.html`; site-wide footer | ✅ |
| Three credentials — PCL-AI, PFL-AI, PML-AI | `certifications.html` | ✅ |
| Governed AI at the core, not a bolt-on | published position, launch deck p.8 / `index.html` | ✅ published position |
| 13 domains · 61 knowledge areas | `exam-structure.html`; `about.html` | ✅ |
| 40 / 40 / 20 weighting | `exam-structure.html` blueprint | ✅ |
| Scenario-based examination, judgement over recall | `exam-structure.html` — "tests whether you can apply project-controls judgement — not whether you can memorise definitions" | ✅ |
| Three years' experience, any field, no degree barrier | `index.html` hero; `faq.html` | ✅ |
| Founding stage | `founding-status.html` — "We are a founding-stage certification body." | ✅ |
| Not accredited by ANAB, IAS or any ISO/IEC 17024 body | site-wide footer; `accreditation-status.html` | ✅ **on screen in shot 9** |
| "Developed with reference to ISO/IEC 17024 personnel-certification principles" | `accreditation-status.html` — the self-declared permitted phrasing | ✅ **on screen in shot 8** |
| Building toward formal accreditation | `about.html`, `governance.html`, `index.html` | ✅ |
| Enrolment open, examinations forthcoming | site banner; `founding-status.html` | ✅ |
| Delaware Non-Stock Corporation; intends to seek 501(c)(3), not granted | `governance.html`; `about.html` | ✅ **on screen in shot 9** |

### Deliberately absent

Beyond the standing editorial rule — no accreditation claim, no member counts, no
testimonials, no partner logos, no salary or job-outcome promise, no fabricated
social proof — this film also drops three claims that appear in the 15-second
launch film and the root README, because reconciliation against the live platform
found no source for them:

| Dropped | Why |
|---|---|
| "NOW LIVE · 1 SEPTEMBER 2026" | No launch date is published anywhere. `founding-status.html`: "we will not publish firm dates we cannot stand behind." |
| "25 country chapters" | The number is unpublished; 23 are listed; `chapters.html`: "Chapters are in formation; PCI does not overstate local presence." |
| "7 launch languages" | No language count is published on any of the 235 live pages. |

No credential holders are implied anywhere in the film. Per
`founding-status.html`, no one has yet been certified, so the film speaks about
the standard and the invitation — never about people who hold it.
