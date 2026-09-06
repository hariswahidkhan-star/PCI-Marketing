# Verified-claims register — Honorary Fellow (PCI) film

Every factual statement spoken or shown in the film, traced to the PCI page that
supports it. Anything that could not be traced was **cut or rewritten**, not
softened — the list of those is in §3, because what was removed is the part of a
claims register that actually matters.

---

## 1. How this was verified, and the one limitation

`https://pciai.org` is **unreachable from this build environment** — the agent
proxy answers `403` to `CONNECT` for that host, which is a network-policy denial,
not a fault on PCI's side. The same applies to
`projectcontrolsinstitute.org`.

Verification was therefore done against **`PCI/backend/wwwroot`**, which is the
source the live site is served from: per the platform's own `CLAUDE.md`, one
ASP.NET Core service serves those ~216 static pages, with database overrides
injected at request time. So the wording below is the wording the pages ship
with, but **a DB-side content override could in principle differ from it.**

**Action required before publication:** re-check §2 against the live pages. The
rows most worth re-reading are the eligibility numbers (E1, E2), the benefits
(B1–B4, and the client-asserted C1) and the fee statement (F1), because those are the ones a change to
programme terms would touch first — and the application page states plainly that
PCI "may update these terms, the eligibility criteria and the associated benefits
at any time."

Pages used, all under `PCI/backend/wwwroot/`:

| Key | File |
|---|---|
| **RH** | `route-honorary.html` — the honorary route |
| **HA** | `honorary-application.html` — application, eligibility, programme terms |
| **HV** | `honorary-verification.html` — shortlisted-candidate identity step |
| **DBR** | `digital-badge-registry.html` — the credential registry |
| **VER** | `verify.html` — public verification |

---

## 2. The claims the film makes

### The nature of the recognition

| # | Claim | Source | Quote |
|---|---|---|---|
| N1 | Honorary Fellow (PCI) is a board-conferred recognition of distinguished contribution | RH, HA | *"Honorary Fellow (PCI) is a board-conferred recognition of distinguished contribution to the profession."* |
| N2 | It involves no examination | RH, HA | *"It involves no examination"* |
| N3 | It is separate from PCI's examined certifications — PCL-AI, PFL-AI, PML-AI | RH, HA | *"separate from PCI's examined certifications — PCL-AI, PFL-AI and PML-AI"* |
| N4 | It is not an examined certification, licence or accreditation | HA | *"is not an examined PCI certification or licence, and does not itself certify competence or constitute accreditation, registration or a professional qualification"* |
| N5 | Every application is considered individually | HA | *"conferred at the sole discretion of the board on the merits of each application"* |
| N6 | Recognition is conferred solely at the Board's discretion | RH, HA | *"conferral is at the board's discretion"* |
| N7 | Meeting the criteria does not guarantee recognition | HA | *"Meeting the criteria does not entitle an applicant to recognition."* |
| N8 | Submitting an application creates no entitlement | HA | *"submitting this application creates no entitlement to recognition"* |
| N9 | An examined credential is always earned by passing the examination | RH | *"An examined PCI credential — PCL-AI, PFL-AI or PML-AI — is always earned by passing the examination, on any route."* |

### Eligibility

| # | Claim | Source | Quote |
|---|---|---|---|
| E1 | At least 8 years of professional experience in project controls, cost control, finance, project management or a closely related field | HA | *"At least 8 years of professional experience in project controls, cost control, finance, project management or a closely related field"* |
| E2 | Of which at least 3 years at managerial level | HA | *"of which at least 3 years at a managerial level (leading teams, functions, programmes or budgets)"* |
| E3 | Managerial responsibility includes leading teams, functions, programmes or budgets | HA | as E2 |
| E4 | A demonstrable record of distinguished contribution | HA | *"a demonstrable record of distinguished contribution to the profession"* |
| E5 | A complete and accurate application with the required declarations | HA | *"a completed application with accurate information and the required declarations"* |

### What the applicant provides

| # | Claim | Source | Quote |
|---|---|---|---|
| A1 | Professional profile, résumé/CV, qualifications, career history, evidence of contribution, declarations | HA | Form sections: *"Personal information… Professional information… Qualifications… Professional certifications… Career history… Relevant experience… Brief professional summary… Résumé / CV… Declarations"* |
| A2 | Reviewed confidentially | HA | *"reviewed confidentially, fairly and in context"* |
| A3 | Identity documents are **not** requested at application stage | HA | *"we ask for identity documents only if the board shortlists you… never requested at this stage"* |
| A4 | Shortlisted candidates get a secure personal link for a passport-style photo, one government ID and a declaration | HA, HV | *"Shortlisted candidates receive a secure, personal link to provide a recent passport-style photograph and one valid government-issued ID"* |
| A5 | Those documents are deleted after the decision | HA, HV | *"deleted after the verification decision (or sooner on request), subject to any legal retention obligation"* |

### Fees and benefits

| # | Claim | Source | Quote |
|---|---|---|---|
| F1 | PCI charges no nomination, assessment or credential fee | HA | *"PCI does not charge a nomination, assessment or credential fee for honorary recognition."* |
| F1a | Optional extras, such as attending an awards ceremony, are charged separately and play no part in the decision | HA | *"Optional charges may apply only for printed certificates, international delivery, replacement documents, or attendance at an awards ceremony; payment does not influence the selection or approval decision and creates no entitlement to recognition."* — spoken in the same breath as F1 because a "free" claim followed by an invoice is the complaint a review panel predicted (see §3b) |
| B1 | Recognition as Honorary Fellow (PCI) | RH | route table: *"Honorary · Free · No exam · Honorary Fellow (PCI)"* |
| B2 | The award can be verified publicly, and is labelled honorary — never a passed examination | DBR, VER | DBR: *"every honorary award, can be checked on the verification page"*; VER: *"clearly labelled honorary and never a passed examination"* |
| B3 | Accepted applicants **may** be issued access credentials to the PCI student portal and given access to learning resources and study materials, subject to current programme terms | HA | *"Accepted applicants may be issued access credentials to the PCI student portal and given access to the Institute's learning resources and study materials… may be varied or withdrawn"* |
| B2a | "Your name, on PCI's own public registry — checkable at source" — the pitch's phrasing of B2 (earlier cuts said "the profession's public register"; changed on the review panel's advice because "public register" borrows a statutory ring PCI's self-operated registry does not have) | DBR | *"the credential registry is live from the programme's founding cohort onwards… every honorary award, can be checked on the verification page"* — a public register the award is entered on, not a promise of who else is on it |
| A6 | "One application" | HA | The application is a single form on one page, submitted once: *"Submit your application below for the board's consideration; we will email you a reference"* |
| B4 | Certuvo is PCI's official platform for preparation and study — the film calls it PCI's official preparation platform | site-wide footer; `certification.html` | *"Certuvo is PCI's official platform for preparation and study"*; *"Preparation and training are provided separately by Certuvo, our official partner"* |

### Client-asserted, not yet on the site

| # | Claim | Status |
|---|---|---|
| C1 | Invitations to selected PCI AI events for accepted applicants | **Instructed by PCI after the first cut; not on any honorary page.** Included as *"invitations to selected PCI AI events, subject to programme terms"*. **The application page's "If your application is successful" paragraph should say this before the film is published**, or the film says more than the terms do. |
| C2 | "Books and video lectures" at Certuvo | **Not stated on the site.** The site describes Certuvo as *"structured study and realistic scenario practice"*. The film says *"study material through Certuvo"* and the card reads *"PCI's official preparation platform"* — the supported wording. |
| C4 | "Video lectures" as a learning resource for accepted applicants | **Instructed by PCI; not on any page.** The site says *"the Institute's learning resources and study materials"* and *"official study materials aligned to each certification's body of knowledge"*. Included as instructed, subject to programme terms; the application page should name it before publication. |
| C5 | A "simulation lab" | **Instructed by PCI; not on any page.** The nearest supported wording is Certuvo's *"structured study and realistic scenario practice"*; "simulation" appears on the site only as the Monte Carlo technique inside the Body of Knowledge. Included as instructed, subject to programme terms; same publication condition as C4. |
| C6 | "Course material" | **Supported as a plain-language rendering** of *"study materials"* (HA, and the downloads centre). |
| C3 | "Enhance career" | **Declined.** The brief itself forbids guaranteeing employment, promotion, salary improvement or third-party acceptance, and PCI's own site-wide disclosure says the same. No career-outcome language appears anywhere in the film. |

### The institution (for the authority scene)

All from `PCI/backend/wwwroot/` — `mission-vision.html`, `certification-integrity.html`, the site-wide footer, and the rows already verified in `../explainer/claims-register.md`.

| # | Claim | Source | Quote |
|---|---|---|---|
| I1 | PCI exists to give project controls a standard, a credential and a professional home, built for the AI era | mission-vision | *"PCI exists to give project controls a standard, a credential and a professional home — built for the AI era."* |
| I2 | An independent certifying body; a Delaware Non-Stock Corporation | site-wide footer (219 pages) | *"An independent professional body — a Delaware Non-Stock Corporation"* |
| I3 | Its integrity safeguards: secure proctored exams, verified identity, impartial decisions, enforced ethics, a verifiable registry | certification-integrity | *"secure exams, verified identity, impartial decisions, enforced ethics and a verifiable registry"* |
| I4 | Preparation is separated from assessment | certification-integrity; footer | *"separate training from assessment"*; *"PCI sets and owns the standard and examination; Certuvo provides preparation"* |
| I5 | A Code of Ethics, an impartiality policy and a conflict-of-interest policy | 26 / 217 / 217 pages | policy pages linked site-wide |
| I6 | A published Body of Knowledge: thirteen domains, sixty-one knowledge areas, weighted 40/40/20 | body-of-knowledge (see explainer register) | *"thirteen domains, sixty-one Knowledge Areas, weighted 40/40/20"* |
| I7 | Framework developed **with reference to** ISO/IEC 17024 — and **not accredited** by ANAB, IAS or any ISO/IEC 17024 body | site-wide footer (218 pages) | *"PCI is not currently accredited by ANAB, IAS, or any ISO/IEC 17024 accreditation body — its certification framework is being developed with reference to ISO/IEC 17024 personnel-certification principles."* — **if the film mentions 17024 it must say both halves** |
| I8 | Registry-first: every credential and every honorary award can be checked at source | DBR | *"built registry-first deliberately… Every PCL-AI credential, and every honorary award, can be checked on the verification page"* |
| I9 | "AI proposes. The professional disposes." | site-wide slogan (216 pages) | schema `slogan` |

### Discipline alignment

| # | Claim | Source | Quote |
|---|---|---|---|
| D1 | An applicant may indicate which PCI discipline their contribution aligns to | HA | *"Which PCI certification is your contribution most aligned to?"* |
| D2 | The selection is optional and confers no examined certification | HA | *"Optional. Honorary Fellow (PCI) is a board-conferred recognition and involves no examination — this simply tells the board which discipline your contribution relates to."* |

---

## 3. What the brief asked for that the site does not support

The brief's draft narration and Scene 8 on-screen text contained four benefit
claims I could not trace. The brief's own rule — *"Use only factual claims that
are currently supported by PCI's official website"* — outranks its draft copy, so
these were **changed, not shipped**.

| Requested | Status | What the film says instead |
|---|---|---|
| *"a professional digital badge or credential that may be shared on LinkedIn"* | **Not supported for honorary recognition.** The LinkedIn-shareable badge is described only for earned credentials: *"When you earn a PCI credential, you receive a digital credential you can share…"* (`digital-credentials.html`). No page attaches a badge to the honorary award. | *"recorded so that anyone can verify it at source — and clearly labelled honorary, never a passed examination"* — which **is** supported (B2), and is the stronger claim anyway: a registry entry cannot be forged, and a badge can. |
| *"opportunities or invitations to attend selected PCI events, webinars and professional activities"* | **Not supported.** No honorary page mentions events, webinars or invitations. The only event reference is the opposite — an *optional paid* charge for *"attendance at an awards ceremony"*. | Cut. |
| *"connection with PCI's international professional community"* / *"visibility within a global community of project professionals"* | **Not supported** for honorary recognition specifically. | Cut. |
| *"complimentary access to selected PCI professional resources"* | **Supported with a qualifier**, so the qualifier is kept. | *"may also be given access to selected PCI learning resources, subject to current programme terms."* The word **may** is doing real work and is not decorative. |

Two further corrections:

- **The brief's title framing.** The user's correction is right and is applied
  throughout: this is **Honorary Fellow (PCI)** / honorary recognition, never an
  "honorary certification". The examined certifications are named only as
  PCL-AI, PFL-AI and PML-AI, and only as things the honorary route is *separate
  from*.
- **`fellowship-policy.html` is a different thing** and was deliberately **not**
  used as a source. That page describes the *membership* Fellow grade, whose
  *"criteria and process are in development"* and for which *"nominations"* have
  not opened. The honorary route is live and has an open application. Quoting the
  membership policy here would have described a programme that does not yet
  accept applicants.

---

## 3a. The pitch cut

PCI asked for the film to sell, to maximise applications. The pitch is built
from the levers that are true — no fee (F1), no examination (N2), a public
register (B2a), one application (A6), individual Board review (N5) — in
second-person address with an "apply today" close. What the pitch does **not**
do, on PCI's own rules: it never calls fellows "members" (the honorary route is
a recognition, not a membership grade), never implies scarcity or a deadline,
never promises a career outcome, and keeps every qualifying sentence — board
discretion, no guarantee, no entitlement, not an examined certification —
spoken and on screen. `share-kit.md` carries the same rules into the posts.

## 3b. The authority cut — psychologist, copywriter and a four-judge review

PCI asked for the film to sell harder, to say more about the Institute and its
value, to name the resources a recognised fellow may use, to be louder and more
authoritative, and to have the script judged by a panel — an ACCA member, a PMP
PMO director, a CFA charterholder and a senior project-controls director — with
no time limit. That produced the 13-scene cut. Two scenes are new (the Institute,
I1–I9; putting yourself forward) and one grew (what it opens).

The panel's consensus, and what was done with it:

| Finding | Action |
|---|---|
| "Not **yet** accredited" implies accreditation is in train; the site says *not currently* | Narration now says *"not currently accredited by ANAB, IAS or any ISO/IEC 17024 body"* — the site's own words (I7) |
| "PCI charges no fee" is true but incomplete — the site carries an optional paid awards ceremony | F1a added and **spoken** in the same sentence as F1 |
| "Public register" borrows statutory authority; a self-nominated award with an unnamed board reads as a vanity award | *"PCI's own public registry — checkable at source"*; scene 9 now says you need no sponsor **and** that the Board assesses the record against published criteria, on the evidence |
| The film never says what PCI legally is | I2 spoken: *an independent professional body — a Delaware Non-Stock Corporation* |
| Scene 5 said "cost engineering"; E1 says "cost control" | Corrected in narration and on screen |
| "Apply today" is urgency the site does not support | Dropped; the close is *"Apply for the Board's consideration at pciai.org"* |
| Don't say the discipline "lacked" a standard — it insults AACE, ICEC, RICS | Dropped; scene 3 says what PCI is built to give, not what others lacked |
| Lead the eligibility with the standard, not the floor | *"The floor is eight years… The bar is higher: a demonstrable record of distinguished contribution."* |
| Say what a contribution looks like; set a test the right applicant recognises | Scene 1: *a standard, a method, and the people who carry it forward*; close: *"If your work has outlasted the projects it was done on, it deserves to be recognised."* |
| **Scene 11 ships C1, C4 and C5 — events, video lectures, the simulation lab — which are on no PCI page. All four judges called this a publication blocker.** | **Kept, on PCI's explicit instruction**, with one *"may"* governing every item and *"all subject to current programme terms"*. The condition stands: **the application page must name these before the film is published**, or the scene must be re-recorded without them. |
| Who sits on the Board, who already holds the recognition, how old PCI is — the facts that would most persuade a sceptic | **Not added.** None is on any PCI page, and the film makes no claim it cannot source. PCI can supply them for a future cut. |
| Too long for the audience (the project-controls director) | PCI's instruction was *"don't worry about time"*; the cut runs 4:00, with a 1.1 s beat between topics and a 4.5 % formant-preserved conform PCI asked for ("a little fast and more human", then "add emotions maximum") |

## 4. Claims deliberately not made

Per the brief and PCI's own site-wide disclosure, the film never states or implies:

- accreditation by ANAB, IAS or any ISO/IEC 17024 body — the site says plainly it
  is **not** currently accredited, and the framework is only *"developed with
  reference to"* those principles;
- government recognition, university recognition or employer preference;
- any guarantee of employment, promotion, salary improvement or third-party
  acceptance;
- that honorary recognition is equivalent to passing a PCI examination;
- membership numbers, rankings, partnerships or industry-standard status;
- permanence of any benefit — the site reserves the right to vary or withdraw
  resource access and to change programme terms at any time.

**No staging, development, preview or testing domain appears anywhere in the
film.** The only URL shown is `pciai.org`, and the only address shown is
`Members@pciai.org`.

---

## 5. Media provenance

- **No stock footage and no generated imagery.** Every frame is computed from
  `src/scene.html` — typography, layout and vector motion only. There are no
  photographs of people, so the brief's requirement to represent professionals
  respectfully is met by not depicting anyone: no synthetic person is presented
  as a real PCI fellow, applicant, examiner or board member, which is the failure
  mode a photoreal treatment of this subject would risk.
- **The industry and applicant sequences are typographic**, naming the sectors and
  the roles rather than illustrating them with stand-in imagery.
- **The narration is synthetic** — ElevenLabs *"Holden Pro Voice"*
  (`UudLhsL2DlHkDK0vGwl3`) on `eleven_v3`, the stock library voice the brief
  names, chosen by PCI after a three-voice test and directed phrase by phrase with
  emotional cues (`src/v3-emotion.json`) at PCI's request for a quicker, more
  human and maximally emotional read — the words are unchanged (`audio/voice-test-authority/`). **It is not a clone of any real
  person**, and no real person's voice was used. Every take was transcribed
  back and matched to the script word for word before use.
- **The score is original**, written from scratch in `src/music.py` and
  `video/lib/score_kit.py` using the Python standard library only — no samples, no
  loops, no third-party audio library, and therefore no licence obligation.
- **The PCI logo is PCI's own**, taken from the repository's brand assets. It is
  not redrawn, recoloured or distorted.
