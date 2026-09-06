# Verified-claims register — PCI AI explainer (3:53)

Every factual statement the film makes, and where it comes from. This film is
denser than the other two: it names the credentials, the Body of Knowledge, the
examination design, the routes in, the renewal cycle and ten industries. So the
verification burden is higher, and each item is traced individually.

## How verification was done

Both production domains (`pciai.org`, `projectcontrolsinstitute.org`) are blocked
by this environment's egress proxy, and Google Drive's OAuth token is expired.
Verification therefore ran against the **first-party source of the live site** —
`hariswahidkhan-star/PCI`, whose `backend/wwwroot/` *is* the 235-page public
website. **Re-check against the live sites before publication.**

**Searches were run in both numeral and word forms.** The 75-second film's
register initially reported a false negative because it searched only numerals
and the site spells numbers in words; that has been corrected there, and the
lesson is applied throughout here.

---

## Claims made, all verified

| # | Claim in the film | Source |
|---|---|---|
| 1 | Project controls = planning, cost, earned value, forecasting, risk, project finance, as one integrated discipline | `mission-vision.html`: *"the integrated discipline of planning, cost, earned value, forecasting, risk and project finance"* |
| 2 | The PMI / ACCA / CFA comparison, and that project controls has no equivalent | `mission-vision.html`, verbatim: *"PMI is for project management. ACCA is for accountancy. CFA is for finance. PCI is for project controls"* — **PCI's own published analogy**, used here about scope, not status |
| 3 | AI can accelerate analysis but create false confidence; technology does not remove accountability | `why-pci.html`, verbatim: *"AI can accelerate analysis but can also create false confidence"*; *"Technology does not remove accountability"* |
| 4 | PCI exists to give the discipline a shared standard, an independent credential and a professional home | `why-pci.html`, verbatim |
| 5 | The mission statement | `mission-vision.html`, verbatim: *"To advance the profession of project controls through certification, research, professional development, standards, publications, conferences, knowledge sharing and the responsible adoption of AI"* (conferences and knowledge sharing trimmed for length; nothing added) |
| 6 | It certifies professionals who govern AI, not who defer to it | `mission-vision.html`, verbatim |
| 7 | "PCI AI Project Leadership Certification Suite", three AI-era leadership credentials | `certifications.html`, verbatim |
| 8 | PCL-AI / PFL-AI / PML-AI and their disciplines | schema.org `EducationalOccupationalCredential` data + `certifications.html` |
| 9 | "Finance intelligently. Control predictively. Deliver successfully." | `certifications.html`, verbatim |
| 10 | Body of Knowledge, First Edition: **thirteen domains, sixty-one Knowledge Areas** | `body-of-knowledge.html`, verbatim; corroborated on 15 pages |
| 11 | Weighted **40 / 40 / 20** across project accounting & finance, project management principles, governed AI | `body-of-knowledge.html`, verbatim |
| 12 | AI is a domain in its own right and embedded through the other twelve | `exam-structure.html`: *"assessed as a domain in its own right rather than an afterthought, and embedded 'AI in this domain' coverage throughout the other twelve"* |
| 13 | The exam is scenario-based and criterion-referenced | `exam-structure.html` |
| 14 | It asks you to read a cost position, interpret an earned-value index, judge a risk response, and judge whether an AI forecast can be trusted | `exam-structure.html`, closely paraphrased from its own worked list |
| 15 | Two routes: an experience route and a Foundation route | `eligibility-requirements.html` |
| 16 | Three-year CPD cycle with a mandatory AI-currency component | `recert.html` |
| 17 | Every credential is publicly verifiable | `verify.html`, `digital-credentials.html` |
| 18 | The ten industries | The ten `sector-*.html` pages, named exactly as the site names them |
| 19 | Corporate programmes (team enrolment at scale) and university partnerships (curriculum alignment) | `corporate-programs.html`, `university-partnerships.html` |
| 20 | Not accredited by ANAB, IAS or any ISO/IEC 17024 body; developed with reference to those principles | `accreditation-status.html`, verbatim from the site footer |
| 21 | "AI proposes. The professional disposes." | Governing principle, site-wide |
| 22 | Delaware Non-Stock Corporation | Site footer, verbatim |

---

## Deliberately excluded

| Not in the film | Why |
|---|---|
| "25 country chapters" | Unverified, and `chapters.html` states *"Chapters are in formation; PCI does not overstate local presence."* Saying it would contradict the site |
| "1 September 2026 launch" | Not found anywhere in the site source |
| "7 launch languages" | Not found anywhere in the site source |
| Pass mark / item counts | `exam-structure.html` states these are **still to be set** by a job-task analysis and a modified-Angoff study. Quoting a number would be false |
| Any accreditation, recognition, employer preference, ranking, salary or job-outcome claim | Prohibited, and contrary to the Institute's published posture |
| Member counts, testimonials, partner logos | No verified source; the site publishes none |

**The film contains exactly four numbers — 13, 61, 40/40/20 and three-year — and
every one is published verbatim on the site.**

---

## The one editorial judgement worth flagging

Scene 2 names **PMI, ACCA and CFA**. These are real organisations, so the bar is
higher than for ordinary copy. It is included because it is **the Institute's own
published sentence**, and it is framed here as a statement about *scope* — which
disciplines have a professional body — not about parity, quality or standing. No
claim is made about those organisations, and none is implied about PCI relative
to them. If the Institute would rather not name them in video, the line can be
generalised to "other professions have their institutes" with no loss of sense.

## Media provenance

| Media | Origin | Disclosure |
|---|---|---|
| All picture | Generated from `src/scene.html` | PCI's own work; **no stock, no AI imagery** |
| Score | Composed from scratch in `src/music.py` | PCI's own work, no licence obligation |
| **Narration** | **AI-generated speech** — ElevenLabs, voice *"Jim Executive"* | **Synthetic voice, must be disclosed.** A stock library voice, **not a clone**, not presented as a named person |
| Archivo / Inter / logo.svg | The site's own faces and mark | OFL / PCI's own; logo used unmodified |
