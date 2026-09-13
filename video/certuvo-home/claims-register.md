# Certuvo homepage film — claims register

Every claim the two-minute homepage film makes, where it comes from, and what
Certuvo must confirm or substantiate before the film goes on the home page.

Status key: **P** — Certuvo product claim, traced to certuvo.com wording;
confirm it still describes the live product · **S** — needs substantiation
Certuvo can produce on request · **N** — the film's own framing, not a claim of
fact · **T** — trademark / third-party mark question.

---

## 1. The ten credentials (s3)

The film names ten credentials and shows a mark or wordmark for each. It says
only that Certuvo *prepares candidates for* them. It nowhere says Certuvo is
approved, endorsed, accredited or partnered by any awarding body except PCI AI.

| # | On screen | Awarding body | Status |
|---|---|---|---|
| 1.1 | CMA (supplied IMA badge) | Institute of Management Accountants | **T** |
| 1.2 | CPA (supplied mark) | AICPA / NASBA and the state boards | **T** |
| 1.3 | CFA Institute (supplied mark) | CFA Institute | **T** |
| 1.4 | Certified Internal Auditor (supplied mark) | The Institute of Internal Auditors | **T** |
| 1.5 | CISA (supplied mark) | ISACA | **T** |
| 1.6 | NCLEX (supplied mark) | NCSBN | **T** |
| 1.7 | PMP® set as a wordmark, not the PMI mark | Project Management Institute | **T** |
| 1.8 | PCL-AI — Project Controls Leader | PCI AI | P |
| 1.9 | PML-AI — Project Management Leader | PCI AI | P |
| 1.10 | PFL-AI — Project Finance Leader | PCI AI | P |

**Certuvo must satisfy itself that it is entitled to reproduce each third-party
mark in 1.1–1.6.** Reproducing a certifying body's logo is a different question
from naming its credential, and several of these bodies publish rules for
preparation providers. If Certuvo would rather not reproduce them, replace the
six `.lg` image cards in `src/scene.html` (s3) with wordmark cards in the same
`.wm` / `.wmsub` pattern already used for PMP, PCL-AI, PML-AI and PFL-AI, and
re-run the build; nothing else changes.

**PMP® is set as type, not as PMI's logo**, because PMI's mark usage rules are
the most restrictive of the set. The ® is carried on its first and only
on-screen use.

**Naming note.** The brief listed *"Pcl project control leader"* and *"Pml
project Control leader"* — the same expansion twice. The film uses **Project
Management Leader** for PML, following PCI's own naming. If PCI's live naming
differs, change the two `.wmsub` lines in s3 and the s3 narration in `src/vo.py`,
re-record that take, and re-render.

## 2. Official training partner of PCI AI (s4, and the film's furniture)

| # | Claim | Status |
|---|---|---|
| 2.1 | "Certuvo is the official training partner of PCI AI — the Project Controls Institute" | **S** |

This is the film's single strongest institutional claim: it appears in the
narration, on the s4 lockup, in the top-left furniture on every frame, and is
the one carve-out in the end-frame independence line. It is asserted on
Certuvo's instruction. **A written partnership record between Certuvo and PCI AI
should exist before publication.** The PCI mark is reproduced on the s4 lockup
on the same basis.

## 3. How courses are built (s5)

| # | Claim in the film | Status |
|---|---|---|
| 3.1 | "Every course is built from research. Not recycled." | **S** — describes Certuvo's own process; Certuvo should be able to describe that process if asked |
| 3.2 | "Mapped to the official blueprint, in the exam's own weightings" | P — matches "Blueprint match — aligned to the official exam blueprint and weighting" on certuvo.com |
| 3.3 | "Rewritten the moment the exam changes" | **S** — a commitment about Certuvo's own maintenance cycle, not a published feature. Soften to "kept current with the exam" if the commitment cannot be met |

## 4. What is inside a course (s6)

Traced to certuvo.com as it read on 12 September 2026.

| # | Claim in the film | certuvo.com wording | Status |
|---|---|---|---|
| 4.1 | Verified multiple-choice questions, checked before a student ever sees them | The four-judge validation described at 5.1 is what "verified" refers to | P |
| 4.2 | Full-length mock exams, under real timing | "timed quizzes and full-length mock exams designed to simulate the real testing experience" | P |
| 4.3 | Video lectures, every domain taught end to end | Course video lectures | P |
| 4.4 | Course notes | Course notes | P |

## 5. The AI features (s7)

| # | Claim in the film | certuvo.com wording | Status |
|---|---|---|---|
| 5.1 | AI Question Forge: unlimited new questions, every one checked by four AI judges (Generate · Verify answer · Quality & clarity · Blueprint match) | "Unlimited new questions. Validated by 4 AI judges." | P |
| 5.2 | AI Coach you can chat or call mid-question | "Chat or call your AI Coach during practice" | P |
| 5.3 | Six languages (English · العربية · Français · Español · हिन्दी · Русский) | "Coach speaks 6 languages" | P |
| 5.4 | It reads your screen — the exact question, diagrams, tables and options | "Reads your screen automatically — it sees the exact question, diagrams, tables, and answer options" | P |
| 5.5 | It switches itself off in a mock | "Auto-disabled during mock exams — practice with help, test without it" | P |

## 6. Peer support and readiness (s8)

| # | Claim in the film | certuvo.com wording | Status |
|---|---|---|---|
| 6.1 | Live study rooms — join your cohort by video, practise on shared questions in real time | "Live study rooms — join your cohort by video anytime"; "Practice together on shared questions in real time" | P |
| 6.2 | Mentors on chat, around the clock | "24/7 Chat Support — round-the-clock support from experienced mentors" | P |
| 6.3 | Tracking that tells you when you're ready | "Progress Tracking — smart analytics that highlight strengths, identify knowledge gaps" — "tells you when you're ready" is the film's paraphrase of readiness analytics | P |

## 7. Price (s9) — the claim that needs the most care

| # | Claim in the film | Status |
|---|---|---|
| 7.1 | "All of it costs less than the market asks." On screen: "Less than the market asks." | **S — comparative advertising** |

This is a comparative price claim against unnamed competitors. In most
advertising regimes a claim of this shape must be **capable of substantiation at
the moment it is published**, must be a fair comparison (like for like, current
prices), and must be re-checked when competitors move.

**Before publication Certuvo should hold a dated comparison** — its own price
against the named principal alternatives for the same credential and the same
scope of materials — and should re-check it on a set schedule. If that
comparison cannot be produced and maintained, replace the line: an absolute
statement about Certuvo's own pricing ("One price. Every course.", "Priced so
the cost is never the reason you stop") carries none of this risk. Changing it
means editing s9 in `src/vo.py`, re-recording that take, and re-rendering.

The second half of the scene — "the price of preparing should never be the
reason you stop" — is **N**, a statement of intent, not a factual claim.

## 8. Free trial (s10)

| # | Claim in the film | Status |
|---|---|---|
| 8.1 | "New here? Start with a free trial." | **S** |

The film says only that a free trial exists for new students. It deliberately
does not state a length, a scope, or whether a card is required. **A free trial
must actually be available to new students when the film is published**, and
what it includes should be stated wherever the film is embedded. If the trial is
withdrawn or becomes conditional, cut s10.

## 9. Emotional framing (s1, s2, s11) — not claims of fact

"It's late… you're still here", "everyone who ever earned those letters did
exactly this", "a certification isn't three letters after your name — it's the
room you get invited into, the number on the offer", "Ten credentials. One
platform. That's enough." These are **N**: the film's framing. Note that "the
number on the offer" gestures at a salary benefit without asserting one; no
figure, multiple or percentage appears anywhere in the film, and none should be
added without published evidence.

## 10. Deliberately not said

- No pass rates, pass guarantees, or "easy".
- No student counts, completion rates, defect rates or streak figures — the
  statistics on certuvo.com ("Under 0.1 % defect rate", "3.1× higher
  completion", "47-day avg. active streak", "14k+ studying together") are all
  omitted. They would each need substantiation and they date quickly.
- No salary figures or earnings claims.
- No price, discount or "from £X".
- No claim of approval, accreditation, endorsement or partnership by any
  awarding body other than PCI AI.

## 11. Trademark and independence (end frame)

Verbatim in `src/vo.py` (`LEGAL`) and on the end card in `src/scene.html`:

> All third-party names and marks shown are the property of their respective
> owners. Certuvo is an independent preparation provider and is not affiliated
> with, sponsored by or endorsed by any of them, except PCI AI, whose official
> training partner it is. Preparation does not guarantee a pass.

It holds on screen for about three seconds at full size. **This line must stay
on any cut, crop or re-edit of this film**, including social versions.

## 12. The presenter and the voice

The presenter is a **synthetic person** — an ElevenLabs Seedream portrait
animated by HeyGen Avatar IV (`heygen-avatar4`). No real person's likeness is
used and no real person's voice is cloned. The narration is ElevenLabs' stock
**Nassim** voice (`eleven_v3`). The music bed is generated in Certuvo's own
ElevenLabs workspace (`eleven_music_v2`) and carries no third-party credit line.

Whether an AI presenter should be disclosed on the page is a judgement for
Certuvo; the film does not present the presenter as a named employee, customer
or expert, and makes no claim in his own person.

## 13. Timing evidence

Cue times in `src/scene.html` (`CUES`, `FOCUS`) are relative to each scene's
first caption and were set from the pauses ffmpeg `silencedetect` found in each
take (−38 dB, ≥ 0.24 s). The explicit caption ends in `src/vo.py` come from the
same measurement, so a credential card lands on its spoken acronym and a feature
card is raised while it is being described.
