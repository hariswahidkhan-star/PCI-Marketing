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

## 3. How courses are built (s5, the provenance strip)

| # | Claim in the film | Status |
|---|---|---|
| 3.1 | Spoken: "Built from research." On screen: "Researched" | **S** — describes Certuvo's own process; Certuvo should be able to describe that process if asked |
| 3.2 | "Mapped to the official blueprint, in the exam's own weightings" | P — matches "Blueprint match — aligned to the official exam blueprint and weighting" on certuvo.com |

**"Not recycled" and "rewritten the moment the exam changes" have been cut.**
Both were in the earlier version of this film. The first is a negative claim
about other providers' materials that Certuvo would have to be able to defend;
the second is a commitment about a maintenance cycle rather than a published
feature. Neither is worth the exposure for one clause, and the scene reads no
weaker without them. If Certuvo wants the maintenance commitment back, it can
be added to the provenance strip in s5 of `src/scene.html` without re-recording,
because it is on screen only.

## 4. What is already inside a course (s5) — including the quantity claim

Traced to certuvo.com as it read on 12 September 2026, except row 4.1.

| # | Claim in the film | Source | Status |
|---|---|---|---|
| 4.1 | **"Thousands of verified questions"** — spoken, and on screen as "Thousands already in the bank" | Certuvo's instruction | **S — quantity claim** |
| 4.2 | Every one checked before a student sees it | The four-judge validation at 5.1 is what "verified" refers to | P |
| 4.3 | Full-length mock exams, under real timing | "timed quizzes and full-length mock exams designed to simulate the real testing experience" | P |
| 4.4 | Video lectures, every domain taught end to end | Course video lectures | P |
| 4.5 | Course notes | Course notes | P |
| 4.6 | Built from research, mapped to the official blueprint, in the exam's own weightings | "Blueprint match — aligned to the official exam blueprint and weighting" | P / **S** for "built from research" |

**4.1 is a quantity claim and it is new in this cut.** "Thousands" means at
least two thousand to an ordinary listener. **Certuvo must be able to show that
each course it sells carries a bank of that size**, because the line says
"inside every course", not "across the platform". If the true figure is lower
for some credentials, the honest fixes are: say "thousands across the platform"
(and change the on-screen line to match), or drop the number and keep "a bank of
verified questions", which the visual already carries on its own.

Deliberately **no exact figure** is shown. The bank is drawn as a field of
question chips filling in rather than a counter, because a counter states a
number Certuvo has not published and invites the reader to check it.

## 5. The Forge and the four judges (s6)

| # | Claim in the film | certuvo.com wording | Status |
|---|---|---|---|
| 5.1 | Unlimited new questions, and not one reaches you until it has passed four AI judges | "Unlimited new questions. Validated by 4 AI judges." | P |
| 5.2 | The four gates, in order: Generated · Answer verified · Checked for ambiguity · Matched to the blueprint | Generate · Verify answer · Quality & clarity · Blueprint match | P — reworded, same four |
| 5.3 | On screen: "re-solved independently", "anything unclear is rejected", "the exam's current weighting" | The site's own descriptions of the same four steps | P |

The scene shows **one** question being generated and passing all four gates.
That is a depiction of the described process, not a recording of the product.
The end frame carries "On-screen product views are illustrative."

## 5A. The AI Coach (s7)

| # | Claim in the film | certuvo.com wording | Status |
|---|---|---|---|
| 5A.1 | Call your AI Coach mid-question | "Chat or call your AI Coach during practice" | P |
| 5A.2 | It reads your screen — the exact question, the diagrams, the options | "Reads your screen automatically — it sees the exact question, diagrams, tables, and answer options" | P |
| 5A.3 | Six languages | "Coach speaks 6 languages: English · العربية · Français · Español · हिन्दी · Русский" | P |
| 5A.4 | It teaches you to think, not memorise — shown as the coach answering a question with a question | "It uses the Socratic method to teach you to think, not memorize" | P |
| 5A.5 | In a mock exam it switches itself off | "Auto-disabled during mock exams — practice with help, test without it" | P |

The on-screen exchange ("I can see the question on your screen" → "I don't know
which cost to allocate" → "Before I answer — which of those costs changes when
volume changes?") is **written for the film** to demonstrate 5A.4. It is not a
transcript of a real session. The exam panel's "Question 14 of 40" and its
clock are likewise illustrative furniture.

## 6. The study room (s8) and readiness (s9)

| # | Claim in the film | certuvo.com wording | Status |
|---|---|---|---|
| 6.1 | Live study rooms — your cohort, on video, working the same question in real time | "Live study rooms — join your cohort by video anytime"; "Practice together on shared questions in real time" | P |
| 6.2 | Mentors on chat, around the clock | "24/7 Chat Support — round-the-clock support from experienced mentors" | P |
| 6.3 | Every question you answer moves a line; Certuvo tracks every domain and finds the gap you keep falling into | "Progress Tracking — smart analytics that highlight strengths, identify knowledge gaps" | P |
| 6.4 | "Not how much you've read. Whether you're ready." | The film's paraphrase of readiness analytics | P |

**The people in the study room are invented.** Six tiles carry first names and
initials on coloured discs — no photographs, no real students, no testimonials,
and no claim that any of them exist. Abstract avatars were chosen over stock
faces for exactly this reason. No headcount is shown: certuvo.com's "14k+
studying together" is a statistic Certuvo would have to substantiate, so it is
not used.

**The readiness chart carries no numbers.** No score, no percentage, no
timescale, no axis values — a rising curve, a dashed "exam-ready" threshold, and
five domain bars of which one is short and flagged. It illustrates that the
product tracks readiness by domain. It does not predict, promise or imply any
outcome, and the card is labelled "illustrative" on its face. The five domain
names are real CMA Part 1 domains, used as a plausible example.

## 7. Price (s10) — the claim that needs the most care

| # | Claim in the film | Status |
|---|---|---|
| 7.1 | "All of it, for less than the market asks." On screen: "Less than the market asks." | **S — comparative advertising** |

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

Changing it means editing s10 in `src/vo.py`, re-recording that take, and
re-rendering.

## 8. Free trial (s10)

| # | Claim in the film | Status |
|---|---|---|
| 8.1 | "And if you are new — start free." | **S** |

The film says only that a free trial exists for new students. It deliberately
does not state a length, a scope, or whether a card is required. **A free trial
must actually be available to new students when the film is published**, and
what it includes should be stated wherever the film is embedded. If the trial is
withdrawn or becomes conditional, cut the second half of s10.

## 9. Framing, not claims of fact (s1, s2, s11)

The film opens and closes on a claim about **effort**, not about outcomes:

> The difference between the people who pass and the people who keep re-sitting
> isn't how hard they work. They all work hard. … It was never how hard you
> work. It's what you work with.

This is **N** — the film's framing, and the device that holds it together (see
`narrative-design.md`). Read strictly it is a generalisation about candidates,
not a claim about Certuvo, and it promises nothing: it does not say Certuvo
makes the difference, that its users pass, or that anyone else's materials fail.
It should stay that way. If it is ever tightened into "Certuvo is the
difference", it becomes an outcome claim and needs evidence.

"It's late… you're still here" and "Ten credentials. One platform. That's
enough." are likewise framing. Nothing in the film gestures at salary or
earnings — the earlier cut's "the number on the offer" has been cut.

## 10. Deliberately not said

- No pass rates, pass guarantees, or "easy".
- No student counts, room headcounts, completion rates, defect rates or streak figures — the
  statistics on certuvo.com ("Under 0.1 % defect rate", "3.1× higher
  completion", "47-day avg. active streak", "14k+ studying together") are all
  omitted. They would each need substantiation and they date quickly.
- No salary figures or earnings claims, and no readiness score or percentage.
- No price, discount or "from £X".
- No claim of approval, accreditation, endorsement or partnership by any
  awarding body other than PCI AI.

## 11. Trademark and independence (end frame)

Verbatim in `src/vo.py` (`LEGAL`) and on the end card in `src/scene.html`:

> All third-party names and marks shown are the property of their respective
> owners. Certuvo is an independent preparation provider and is not affiliated
> with, sponsored by or endorsed by any of them, except PCI AI, whose official
> training partner it is. On-screen product views are illustrative. Preparation
> does not guarantee a pass.

The sentence "On-screen product views are illustrative" is **new in this cut**
and must stay: four scenes now depict product interfaces (the question bank, the
Forge, the Coach, the study room and the readiness chart) that are drawn for the
film rather than screen-recorded.

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

Cue times in `src/scene.html` (`CUES`, `FOCUS`, `SCENEFX`) are relative to each
scene's first caption and were set from the pauses ffmpeg `silencedetect` found
in each take (−38 dB, ≥ 0.24 s). The explicit caption ends in `src/vo.py` come
from the same measurement, so a credential card lands on its spoken acronym,
each of the four judges ticks on the word that names it, and the coach switches
itself off on "then, in a mock exam".
