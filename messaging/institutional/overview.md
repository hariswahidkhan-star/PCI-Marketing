# Institution overview — approved copy

Source of truth for how PCI itself is described in marketing. Every claim below is
traced to a live page. Where the platform has not published something, this file
says so rather than filling the gap.

**Reconciled against** `hariswahidkhan-star/PCI` @ `backend/wwwroot/about.html`,
`governance.html`, `accreditation-status.html`, `certifications.html`,
`exam-structure.html`, `index.html`, `verify.html`, `founding-status.html`,
`chapters.html`, `world/preview/`.

> **The governing constraint.** `accreditation-status.html` states: *"This page is
> the authoritative statement of our accreditation position… If wording anywhere
> else ever appears to say more than this page does, this page prevails."*
> Marketing copy is "anywhere else". It never leads that page.

---

## Approved copy

**The Project Controls Institute** is an independent professional body building a
modern certification standard for project controls in the AI era. Its credentials
unite the disciplines complex projects actually depend on — planning and
scheduling, cost control, forecasting, earned value, project finance, risk,
reporting — and the responsible use of AI across all of them.

PCI exists because the work is changing. AI can now forecast, analyse and report
in seconds, but it can be confidently wrong. PCI's governing principle:

> **AI proposes. The professional disposes.**

Accountability, judgment and integrity remain human.

### The credentials

Three, as one suite. Use the full expansions exactly as published — the third is
constructed differently from the first two, and that is deliberate, not a typo:

| Credential | Full name |
|---|---|
| **PCL-AI** *(flagship)* | PCI AI Project Controls Leader |
| **PFL-AI** | PCI AI Project Finance Leader |
| **PML-AI** | PCI Project Management Leader – AI |

The standard rests on a **thirteen-domain Body of Knowledge (61 Knowledge Areas)**,
sampled by the published exam blueprint in three weighted groups — project
accounting and finance 40%, project management principles 40%, AI knowledge and
practical approach 20%.

### Open by design

The only entry requirement is **three years' professional experience in any field**
— no degree barrier. Assessment is **scenario-based multiple choice (single best
answer)**, **proctored, online or at a test centre**, measuring capability rather
than pedigree.

### Honest status

PCI is at its **founding stage**. Stated plainly, and in this order:

- A **Delaware Non-Stock Corporation** (formed 2 October 2025; Delaware File No.
  10353271). It **intends to seek** recognition under Section 501(c)(3); tax-exempt
  status **has not yet been granted**, and contributions are **not currently
  represented as tax-deductible**.
- PCI is **not currently accredited by ANAB, IAS, or any ISO/IEC 17024 accreditation
  body**. Its certification framework is **developed with reference to ISO/IEC 17024
  personnel-certification principles** — design intent, not granted recognition.
  PCI is **building toward formal accreditation rather than claiming it**.
- PCI credentials are **not government-recognised or formally accredited**.
  Recognition may vary by employer, industry, institution and jurisdiction. PCI
  guarantees no employment, promotion, salary improvement, immigration benefit,
  licensing eligibility or third-party acceptance.
- **Enrolment is open; examinations are forthcoming; no one has yet been
  certified.** The exam item count and pass mark are not yet fixed — they follow a
  formal job-task analysis and a modified-Angoff standard-setting study.
- Public credential verification is **live as a mechanism**; the register is new.

### PCI World

A global learning and challenge platform operated by the Institute, currently a
**pre-launch preview**. PCI World challenges are **educational practice and
professional-development evidence** — they are not certification examinations, and
completing one **does not grant or affect any PCI certification, membership or
credential**. All names, organisations and messages in the preview are invented
for those pages.

---

## What must not be said

| Do not say | Why |
|---|---|
| **PCP-AI** | Retired acronym. Zero occurrences in live public HTML; `SeedContent.cs` ships a migration rewriting `PCP-AI` → `PCL-AI` and calls it "the retired acronym". Survives only in seed data, tests, docs filenames and the legacy `generate.py`. |
| "Certified Project Controls Professional — AI" | The homepage still carries this expansion for PCL-AI; `certifications.html` says "PCI AI Project Controls Leader". A live contradiction, likely rename residue. Use the `certifications.html` form. |
| **"25 country chapters"** | The number is published nowhere. 23 are listed. `chapters.html` says "Chapters are in formation; PCI does not overstate local presence." Using it would overstate presence the site declines to claim. |
| **"7 launch languages"** | No language count is published on any of the 235 pages. No source. |
| **"Launched 1 September 2026"** / any firm date | No launch date is published anywhere, and `founding-status.html` commits: "we will not publish firm dates we cannot stand behind." |
| "Applied for 501(c)(3)" | The published verb is **"intends to seek"**. "Applied for" upgrades it. |
| "Donations are tax-deductible" | Published formula is the negative: "not currently represented as tax-deductible". |
| "Accredited", "ISO/IEC 17024 certified", "aligned to ISO/IEC 17024" as a claim of standing | Only "developed with reference to … principles" and "building toward formal accreditation" are permitted. |
| "Remote-proctored" as the only mode | Published claim is "Proctored, online or at a test centre". Remote is one of two modes. |
| "Twelve-competency framework" | `about.html` publishes both a twelve-competency model and the thirteen-domain BoK without disambiguating. Use thirteen domains. |
| Any pass mark, item count or exam duration | Not yet set; pending job-task analysis and standard-setting study. |
| Anything implying credential holders exist | "No one has yet been certified." |

---

## Claims audit

| Claim | Source | Status |
|---|---|---|
| Independent professional body | `about.html`; footer blurb site-wide | ✅ |
| Delaware Non-Stock Corporation, formed 2 Oct 2025, File No. 10353271 | `governance.html`; `about.html` | ✅ |
| Intends to seek 501(c)(3); not granted; not represented as tax-deductible | `accreditation-status.html`; `about.html`; `founding-status.html` | ✅ verbatim |
| Not accredited by ANAB, IAS or any ISO/IEC 17024 body | site-wide footer; `accreditation-status.html` | ✅ verbatim |
| "Developed with reference to ISO/IEC 17024 personnel-certification principles" | `accreditation-status.html` — self-declared permitted phrasing | ✅ |
| "Building toward formal accreditation rather than claiming it" | `about.html`, `verify.html`, `governance.html`, `index.html` | ✅ |
| No guarantee of employment, salary, licensing or third-party acceptance | site-wide footer | ✅ |
| Three credentials; PCL-AI is flagship | `certifications.html`; `ai-cert.html` — "the flagship PCL-AI" | ✅ |
| Full credential names as tabled | `certifications.html` meta description | ✅ verbatim, asymmetry preserved |
| 13 domains / 61 Knowledge Areas / 40-40-20 weighting | `exam-structure.html`; `about.html`; `founding-status.html` | ✅ |
| Three years' experience, any field, no degree barrier | `index.html` hero; `faq.html`; `eligibility-requirements.html` | ✅ (⚠️ policy pages soften to "around three years") |
| Scenario-based MCQ, single best answer | `exam-structure.html` | ✅ |
| Proctored, online or at a test centre | `index.html` | ✅ |
| Pass mark and item count not yet set | `exam-structure.html` | ✅ published limit |
| Enrolment open; no one yet certified | site banner; `founding-status.html` | ✅ |
| Verification mechanism live | `verify.html` | ✅ (⚠️ register is empty; do not imply holders) |
| "AI proposes. The professional disposes." | `index.html` display copy; JSON-LD `slogan` site-wide | ✅ |
| PCI World is educational practice, does not affect certification | `world/preview/` footer disclaimer | ✅ verbatim |
| 25 country chapters | — | ❌ **unpublished and contradicted**; removed |
| 7 launch languages | — | ❌ **no source anywhere**; removed |
| Launched 1 September 2026 | — | ❌ **no source; contradicts a published commitment**; removed |

**Deliberately absent**, per the Institute's editorial rule: no accreditation
claim, no member or participant counts, no testimonials, no employer or partner
logos, no salary or job-outcome promise, no third-party recognition, and no
fabricated social proof of any kind.
