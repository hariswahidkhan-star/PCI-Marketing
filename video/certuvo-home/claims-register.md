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

The on-screen exchange ("I can see it — $480,000 over 60,000 budgeted units."
→ "Do I use budgeted units or actual?" → "Before I answer: the rate is set
once, in advance. Which of the two numbers was known then?") is **written for
the film** to demonstrate 5A.4. It is not a transcript of a real session. The
exam panel's "Question 14 of 40" and its clock are likewise illustrative
furniture.

### 5A.6 The question shown on screen is original, and it is worked

PCI asked for a proper, comprehensive question on screen rather than blurred
placeholders. The question in s7 and s8 is **written for this film**. It is
deliberately *not* lifted from any institute's released paper or free question
bank, free-to-use or otherwise: reproducing an awarding body's item would raise
exactly the third-party-rights question section 1 is careful about, and a
prep provider showing another body's item is a worse look than showing its own.

The item is standard absorption-costing material and the arithmetic closes:

| Step | Value |
|---|---|
| Budgeted fixed overhead | $480,000 |
| Budgeted production | 60,000 units |
| Fixed overhead absorption rate | $480,000 / 60,000 = **$8.00 per unit** |
| Actual production | 54,000 units |
| Overhead applied | 54,000 × $8.00 = $432,000 |
| Under-absorbed | $480,000 − $432,000 = **$48,000** |
| Volume variance | **$48,000 unfavourable — option B** |

Distractors are the three standard errors: A inverts the sign, C applies the
rate to the wrong base, D denies the variance exists. The film lights B, and
only after the coach has answered with a question — so the sequence on screen
is *coach asks → candidate answers*, never *coach supplies the answer*, which
is what 5A.4 actually claims.

This reverses, **for this film only**, the instruction given for the five
feature-demonstration films ("use abstract cards and blurred placeholders —
never display actual questions or answers"). That instruction still stands for
those five; PCI's later note asked for a real question on the homepage cut.

## 6. Study with a peer (s8) and readiness (s9)

**This section was rewritten after PCI corrected the product description.** The
earlier cut showed a live cohort study room of six people and a 24/7 mentor
chat. PCI's note: *"There are no chat rooms. There is a feature study with your
pear member — this feature will share the screen with the other member like a
google meet and student can bring their friend together."* Both of the earlier
claims are gone from the film.

⚠️ **Site copy to check.** The withdrawn claims were traced to wording on
certuvo.com ("Live study rooms — join your cohort by video anytime" and "24/7
Chat Support — round-the-clock support from experienced mentors"). If those
features do not exist, that wording is a bigger exposure than a film, and
someone should look at the live site. The film has been corrected; the site has
not been checked as part of this work.

| # | Claim in the film | Source | Status |
|---|---|---|---|
| 6.1 | Study with a peer — share your screen live, so both people see the same question and the same numbers at the same second | PCI's description of the feature, quoted above | P |
| 6.2 | Bring a friend into the session — shown as an invite seat reading "Bring a friend · send them a link" | PCI's description of the feature, quoted above | P |
| 6.3 | Every question you answer moves a line; Certuvo tracks every domain and finds the gap you keep falling into | "Progress Tracking — smart analytics that highlight strengths, identify knowledge gaps" | P |
| 6.4 | "Not how much you've read. Whether you're ready." | The film's paraphrase of readiness analytics | P |

**Certuvo should confirm 6.1 and 6.2 against the shipped feature** — they are
recorded here from a written description, not from site copy or a build. Two
details are worth checking specifically, because the film shows both: that the
peer sees the *presenter's* screen (not a synchronised copy of their own), and
that the invitee can be someone the candidate brings in themselves rather than
only an already-enrolled cohort member. PCI's wording says both, and the film
depicts both.

**The two people in the session are invented.** "Amara" and "Jonas" are first
names on coloured initial discs — no photographs, no real students, no
testimonials, and no claim that either exists. Their two cursors move on the
shared screen and land on the same option; the mic indicator trades between
them. That is a depiction of the mechanic, not a recording of a session. No
headcount appears anywhere: certuvo.com's "14k+ studying together" is a
statistic Certuvo would have to substantiate, so it is not used.

**The shared screen shows the same original question as s7**, worked in 5A.6
above. Nothing in the peer panel is copied from an awarding body.

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
- No student counts, session headcounts, completion rates, defect rates or streak figures — the
  statistics on certuvo.com ("Under 0.1 % defect rate", "3.1× higher
  completion", "47-day avg. active streak", "14k+ studying together") are all
  omitted. They would each need substantiation and they date quickly.
- No salary figures or earnings claims, and no readiness score or percentage.
- No price, discount or "from £X".
- No claim of approval, accreditation, endorsement or partnership by any
  awarding body other than PCI AI.
- **No chat rooms and no 24/7 mentor chat.** Both were in the previous cut and
  both were withdrawn on PCI's correction. Do not reinstate either without a
  written confirmation that the feature exists — see section 6.
- No question, item or answer reproduced from any awarding body's paper or
  question bank. The two questions the film shows are its own — see 5A.6.

## 11. Trademark and independence (end frame)

Verbatim in `src/vo.py` (`LEGAL`) and on the end card in `src/scene.html`:

> All third-party names and marks shown are the property of their respective
> owners. Certuvo is an independent preparation provider and is not affiliated
> with, sponsored by or endorsed by any of them, except PCI AI, whose official
> training partner it is. On-screen product views are illustrative. Preparation
> does not guarantee a pass.

The sentence "On-screen product views are illustrative" is **new in this cut**
and must stay: five scenes now depict product interfaces (the question bank, the
Forge, the Coach, the peer screen-share and the readiness chart) that are drawn
for the film rather than screen-recorded. The two exam questions shown inside
them are original and worked — see 5A.6 — but the interfaces around them are
illustrations, not screenshots.

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

The read was re-recorded for scenes 2–10 after PCI's corrections. Scenes 1 and
11 are word-for-word unchanged, so their takes and both presenter clips are
reused rather than re-billed. Two pronunciations were changed in the **spoken**
field only, leaving the caption orthography correct: NCLEX is now read as a
word rather than spelled out, and the brand is written phonetically for the
narrator. PCI reported that a pronunciation is still wrong without naming the
word; a reference take of eight candidate readings was generated so the right
one can be chosen, and **s4, s9 and s11 would need re-recording if the brand
reading is the one at issue** — s11 would also need a new presenter clip.

Film length after conform: **165.76 s** (2 min 46 s) over 11 scenes and 31
captions, plus the intro and outro stings.
