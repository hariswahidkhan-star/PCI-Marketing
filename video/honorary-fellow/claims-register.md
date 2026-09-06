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
| B1 | Recognition as Honorary Fellow (PCI) | RH | route table: *"Honorary · Free · No exam · Honorary Fellow (PCI)"* |
| B2 | The award can be verified publicly, and is labelled honorary — never a passed examination | DBR, VER | DBR: *"every honorary award, can be checked on the verification page"*; VER: *"clearly labelled honorary and never a passed examination"* |
| B3 | Accepted applicants **may** be issued access credentials to the PCI student portal and given access to learning resources and study materials, subject to current programme terms | HA | *"Accepted applicants may be issued access credentials to the PCI student portal and given access to the Institute's learning resources and study materials… may be varied or withdrawn"* |
| B4 | Certuvo is PCI's official platform for preparation and study — the film calls it PCI's official preparation platform | site-wide footer; `certification.html` | *"Certuvo is PCI's official platform for preparation and study"*; *"Preparation and training are provided separately by Certuvo, our official partner"* |

### Client-asserted, not yet on the site

| # | Claim | Status |
|---|---|---|
| C1 | Invitations to selected PCI AI events for accepted applicants | **Instructed by PCI after the first cut; not on any honorary page.** Included as *"invitations to selected PCI AI events, subject to programme terms"*. **The application page's "If your application is successful" paragraph should say this before the film is published**, or the film says more than the terms do. |
| C2 | "Books and video lectures" at Certuvo | **Not stated on the site.** The site describes Certuvo as *"structured study and realistic scenario practice"*. The film says *"study material through Certuvo"* and the card reads *"PCI's official preparation platform"* — the supported wording. |
| C3 | "Enhance career" | **Declined.** The brief itself forbids guaranteeing employment, promotion, salary improvement or third-party acceptance, and PCI's own site-wide disclosure says the same. No career-outcome language appears anywhere in the film. |

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
  (`UudLhsL2DlHkDK0vGwl3`) on `eleven_v3`, a stock library voice. **It is not a
  clone of any real person**, and no real person's voice was used.
- **The score is original**, written from scratch in `src/music.py` and
  `video/lib/score_kit.py` using the Python standard library only — no samples, no
  loops, no third-party audio library, and therefore no licence obligation.
- **The PCI logo is PCI's own**, taken from the repository's brand assets. It is
  not redrawn, recoloured or distorted.
