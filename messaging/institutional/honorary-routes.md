# Honorary route — approved copy

Source of truth for how PCI's honorary route is described in marketing. Every
claim below is traced to a live page or to the code that enforces it. Where the
platform has not published something, this file says so rather than filling the
gap.

**Reconciled against** `hariswahidkhan-star/PCI` @ `backend/wwwroot/route-honorary.html`,
`honorary-application.html`, `honorary-verification.html`, `verify.html`,
`membership.html`, `backend/Endpoints/Honorary.cs`,
`docs/HONORARY_ROUTE_AND_REGISTRATION.md`.

---

## The one-line version

> Honorary Fellow (PCI) is a board-conferred recognition of distinguished
> contribution — no examination, always labelled honorary, never the examined
> credential.

---

## Approved copy

The honorary route recognises individuals of standing who have advanced the
profession, the body of knowledge, or PCI's mission.

**There is one honorary designation: Honorary Fellow (PCI).** It is conferred by
the board at its discretion, involves **no examination**, and is always labelled
honorary. It is **never** an examined PCI credential:

> An examined PCI credential — PCL-AI, PFL-AI or PML-AI — is always earned by
> passing the examination, on any route.

Honorary recognition confers no certification, accreditation, registration or
professional qualification, and does not itself certify competence. Honorary
awards carry their own identifier series, **PCI-HON-YYYY-NNNN**, distinct from the
examined series (`PCI-PCLAI-…`, `PCI-PFLAI-…`, `PCI-PMLAI-…`), and are labelled as
honorary recognitions wherever they are verified.

**The route is open.** Applications can be made now, for the board's
consideration. To be considered, an applicant should meet **all** of:

- at least **8 years** of professional experience in project controls, cost
  control, finance, project management or a closely related field;
- of which **at least 3 years at a managerial level** — leading teams, functions,
  programmes or budgets;
- a demonstrable record of distinguished contribution to the profession, supported
  by a résumé/CV and, where available, academic and professional evidence; and
- a completed application with accurate information and the required declarations.

> Meeting the criteria does not entitle an applicant to recognition. Honorary
> Fellow (PCI) is conferred at the sole discretion of the board on the merits of
> each application; PCI may request further information, and may decline any
> application without stating reasons.

**Process.** Apply → board review → identity verification if shortlisted → board
decision. Identity documents are requested only on shortlisting, to keep data to a
minimum.

**Fees.** PCI charges no nomination, assessment or credential fee for honorary
recognition. Optional charges may apply only for printed certificates,
international delivery, replacement documents or ceremony attendance; payment
does not influence the decision and creates no entitlement to recognition. Any
indicated review time is an estimate, not a commitment.

**Conduct.** Applications are subject to PCI's Terms of Use, Code of Ethics,
Conflict of Interest Policy, Complaints Policy, Appeals Policy and Website
Disclaimer. Recognition is discretionary and revocable — it may be declined,
deferred, or withdrawn where it was obtained through inaccurate information or
where continued association would be inappropriate.

---

## What must not be said

| Do not say | Why |
|---|---|
| Honorary Member · Honorary Advisor | Zero occurrences site-wide. Only "Honorary Fellow (PCI)" exists (`Honorary.cs:80`). |
| "Hon. FPCI" | Zero matches repo-wide. The honorary designation has **no published post-nominal**. |
| FPCI as an honorary post-nominal | FPCI is the **membership Fellow** grade (`membership.html:17`, `membership-fellow.html:7`). Conflating the two merges an elected membership grade with a board-conferred honour. |
| "Honorary figures do not direct certification decisions" | **No such statement is published anywhere** — not in `impartiality-policy.html`, `governance.html`, `certification-decision-policy.html`, `certification-integrity.html` or `ethics.html`. An impartiality claim of this shape is currently unsupported. |
| "Final criteria and nomination process will be published before nominations open" | False for this route. Criteria **are** published and the form **is** live. That deferral language belongs to `fellowship-policy.html`, which is about membership Fellowship (FPCI) and does not mention honorary at all. |
| Honorary recognition per credential | One designation, one award series, no certification binding. The credential field on the application is explicitly *optional and informational*. |
| Any honorary "use of marks" licence | No such clause exists on the site. The nearest published rule is a *description* obligation in a Downloads-Centre PDF still marked **external legal review pending**. |

---

## Open issues on the platform (flagged, not ours to fix here)

These are inconsistencies found on the live site while reconciling. They belong in
the platform repo, not this one, but marketing should not quote around them.

1. **`certification.html` is stale** — it says honorary is "conferred by the board,
   **not applied for**", contradicting `route-honorary.html`, `membership.html` and
   the live application form.
2. **Wrong policy link** — the "Read the recognition policy" button on
   `route-honorary.html` points at `fellowship-policy.html`, which contains zero
   occurrences of "honorary" and says its criteria are still "in development". The
   actual Honorary Recognition Policy is a Downloads-Centre document.
3. **Catalogue block in the wrong context** — the shared "This route, for each
   certification" section injects exam fees, pass marks and "Apply now" CTAs onto a
   page whose premise is "no examination".

---

## Claims audit

| Claim | Source | Status |
|---|---|---|
| One designation: "Honorary Fellow (PCI)" | `Honorary.cs:80`; `route-honorary.html`; 26 occurrences site-wide | ✅ |
| Board-conferred, at the board's discretion | `route-honorary.html`; `honorary-application.html` | ✅ |
| No examination | `route-honorary.html` — "It involves no examination" | ✅ |
| Never the examined credential; always labelled honorary | `route-honorary.html`, `membership.html`, `employers.html`, `verify.html` | ✅ heavily repeated |
| Confers no certification, accreditation or qualification | `honorary-application.html` — "not an examined PCI certification or licence… does not itself certify competence or constitute accreditation" | ✅ verbatim |
| Separate identifier series `PCI-HON-YYYY-NNNN` | `verify.html` | ✅ |
| Approval never mints a credential or exam record | `docs/HONORARY_ROUTE_AND_REGISTRATION.md`, test `ha3f` | ✅ enforced |
| Route is open; apply online | live form POSTing `/api/honorary-application`; CTA on `route-honorary.html` | ✅ (⚠️ `certification.html` stale) |
| Criteria: 8 years / 3 managerial / distinguished contribution / declarations | `honorary-application.html` | ✅ published |
| Criteria do not entitle; may decline without reasons | `honorary-application.html` | ✅ verbatim |
| Identity documents only on shortlisting | `honorary-application.html` | ✅ |
| No nomination, assessment or credential fee | `honorary-application.html` | ✅ |
| Code of Ethics applies | `honorary-application.html` governing terms | ⚠️ by reference only; no honorary-specific clause |
| Revocable for cause | `honorary-application.html`; `Honorary.cs:97` revoke endpoint | ✅ |
| Revocation never touches an exam-earned credential | `Honorary.cs:97` — "Revokes ONLY the honorary record" | ✅ |
| Honorary Member / Honorary Advisor tiers | — | ❌ **do not exist**; removed from draft copy |
| "Hon. FPCI" post-nominal | — | ❌ **does not exist**; removed |
| Impartiality — honorary figures not directing certification | — | ❌ **unpublished**; removed. Do not assert until the platform publishes it. |

**Deliberately absent**, per the Institute's editorial rule: no accreditation
claim, no honorary recipient counts or names used as social proof, no suggestion
that honorary recognition is a credential or a route to one, and no implied
third-party recognition.
