# Certuvo CMA film — claims register

Every factual statement the film makes, where it comes from, and what must be
re-checked before the film is published. The build environment could not reach
imanet.org directly, so the exam facts below were consolidated from several
preparation providers' 2026 summaries of IMA's published material (found by web
search in September 2026) and cross-checked against each other. **Certuvo must
confirm each row against IMA's current CMA Handbook and Content Specification
Outline (CSO) before publication** — IMA changes the exam and its fees on its own
schedule.

Status key: **C** consistent across every source found · **V** verify on
imanet.org before publication · **P** Certuvo product claim — confirm it
describes the live product.

## 1. What the CMA is (s3)

| # | Claim in the film | Source | Status |
|---|---|---|---|
| 1.1 | The CMA is awarded by IMA, the Institute of Management Accountants | IMA | C |
| 1.2 | First awarded in 1972 | IMA's own history of the CMA programme (launched 1972) | C |
| 1.3 | 61 candidates passed in the first year | IMA history: 61 candidates received the CMA in the first examination year | V — a secondary figure; confirm the exact wording on IMA's history page |
| 1.4 | "The credential for management accounting: planning, budgeting, performance, risk, strategy" | Descriptive summary of the CSO domains; not a quotation | C |

## 2. Part 1 — Financial Planning, Performance and Analytics (s4)

Weights as published in IMA's CSO (effective from the 2020 exam and unchanged in
the 2026 CSO summaries found):

| Domain | Weight | Status |
|---|---|---|
| External Financial Reporting Decisions | 15% | C |
| Planning, Budgeting and Forecasting | 20% | C |
| Performance Management | 20% | C |
| Cost Management | 15% | C |
| Internal Controls | 15% | C |
| Technology and Analytics | 15% | C |

Sum 100%. "Engine room" is the film's framing, not IMA's.

## 3. Part 2 — Strategic Financial Management (s5)

| Domain | Weight | Status |
|---|---|---|
| Financial Statement Analysis | 20% | C |
| Corporate Finance | 20% | C |
| Decision Analysis | 25% | C |
| Risk Management | 10% | C |
| Investment Decisions | 10% | C |
| Professional Ethics | 15% | C |

Sum 100%. "Largest single domain" — Decision Analysis at 25% is the largest
single domain in either part. "Boardroom" is the film's framing.

## 4. The exam (s6)

| # | Claim | Source | Status |
|---|---|---|---|
| 4.1 | Each part is a four-hour exam | IMA CMA Handbook | C |
| 4.2 | 100 multiple-choice questions in three hours | IMA CMA Handbook | C |
| 4.3 | Multiple choice is 75% of the score | IMA CMA Handbook | C |
| 4.4 | One hour for the second section | IMA CMA Handbook | C |
| 4.5 | From the September 2026 testing window, two case-based questions replace the essays; each is a short business case followed by up to seven questions | IMA's 2026 exam format announcement as reported by providers | **V** — the single most time-sensitive fact in the film. Confirm the effective window and the "up to seven questions" wording on imanet.org. If IMA's wording differs, re-record s6 (vo.py, DIRECTION s6) and re-render. |
| 4.6 | At least 50% on the multiple choice is required to unlock the second section | IMA CMA Handbook | C |
| 4.7 | Pass mark 360 on a 0–500 scaled score | IMA CMA Handbook | C |
| 4.8 | Three testing windows a year: Jan–Feb, May–Jun, Sep–Oct | IMA CMA Handbook | C |

The film does not state fees, and says so on the end frame ("fees … as published
by IMA"); IMA's entrance and exam fees change and are deliberately kept out of a
video that will be online for a long time.

## 5. Requirements (s7)

| # | Claim | Source | Status |
|---|---|---|---|
| 5.1 | Active IMA membership | IMA CMA Handbook | C |
| 5.2 | Bachelor's degree from an accredited institution **or** an approved professional certification | IMA CMA Handbook | C — the film says "approved professional certification"; IMA's list of accepted certifications is on imanet.org |
| 5.3 | Two continuous years of relevant professional experience | IMA CMA Handbook | C |
| 5.4 | The experience may be completed up to seven years after passing the exam | IMA CMA Handbook | C |
| 5.5 | "So you can sit the exam first" | Follows from 5.4 | C |

The film does not mention the entrance-fee validity window, the three-year
window to pass both parts, or continuing education, none of which is needed
for an introduction; the end frame sends viewers to imanet.org for current
details.

## 6. Why it matters (s8)

| # | Claim | Source | Status |
|---|---|---|---|
| 6.1 | IMA Global Salary Survey 2023: CMAs' median total compensation 21% higher than non-CMAs, worldwide | IMA Global Salary Survey 2023 (global median total compensation, CMA vs non-CMA) | **V** — confirm the 21% figure and that it is the *global* median *total compensation* comparison in the 2023 report; if Certuvo prefers the most recent survey, update the figure, the year in vo.py (s8) and the on-screen note, and re-record s8. |
| 6.2 | Roles: FP&A, controller, finance business partner, "the route to CFO" | Descriptive; no numeric claim | C — "the route to CFO" is framed as a pathway, not a guarantee |

No salary guarantee or employment promise is made. The on-screen note carries
the survey name and year next to the figure.

## 7. How Certuvo prepares you (s9) — product claims

| # | Claim | Status |
|---|---|---|
| 7.1 | Structured study for every domain in both parts, in the exam's own weightings | **P** |
| 7.2 | Scenario-based question banks that mirror the real format, including case-based questions | **P** — "case-based questions" must exist in the product before the September 2026 window claim is made |
| 7.3 | Full-length mock examinations under exam timing | **P** |
| 7.4 | Readiness tracking that tells you when you're ready | **P** |
| 7.5 | Fully online, at your own pace, on any device | **P** |

If any row does not describe the live product, cut it from vo.py (s9), re-record
s9 and re-render. Nothing in the film promises a pass; the end frame states
"Preparation does not guarantee a pass."

## 8. Trademark and independence (end frame)

The end-frame legal text, verbatim in `src/vo.py` (`LEGAL`) and `src/scene.html`:

> CMA® is a registered trademark of the Institute of Management Accountants
> (IMA). Certuvo is an independent preparation provider and is not affiliated
> with, sponsored by or endorsed by IMA. Exam structure, fees and requirements
> as published by IMA for 2026; confirm current details at imanet.org.
> Preparation does not guarantee a pass.

- "CMA®" is written with the ® on its first prominent on-screen use (s3) and in
  the furniture ("CMA® preparation"). The IMA CMA badge supplied as a reference
  (`assets/cma-badge-reference.png`) is **not** used in the film — it is IMA's
  mark and Certuvo is not an IMA partner.
- The presenter is a synthetic person (an ElevenLabs Seedream portrait animated by
  HeyGen Avatar IV). No real person's likeness or voice is used; the voice is
  ElevenLabs' stock "Nassim" voice.

## 9. Things the film deliberately does not say

- No fee amounts. No "easy" or "guaranteed" pass. No pass-rate figures.
- No claim of IMA approval, partnership or accreditation for Certuvo.
- No claim about the number of Certuvo students or their results.
- "Three minutes" is not said on screen: the narration says "in the next three
  minutes" (s2) while the film runs 4:07; see README.md §Known issues.

## 10. Timing evidence

Cue times in `src/scene.html` (`CUES`) are relative to each scene's first caption
and were set from the pauses ffmpeg `silencedetect` found in each take
(`-38 dB`, ≥ 0.26 s); the explicit caption ends in `src/vo.py` (s4, s5, s9) were
taken from the same measurement so a weight rises as it is spoken.
