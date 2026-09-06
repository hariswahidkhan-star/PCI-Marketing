# Founding route — approved copy

Source of truth for how PCI's founding route is described in marketing. Every
claim below is traced to a live page or to the code that enforces it. Where the
platform has not published something, this file says so rather than filling the
gap.

**Reconciled against** `hariswahidkhan-star/PCI` @ `backend/wwwroot/route-founding.html`,
`founding-status.html`, `membership.html`, `backend/Endpoints/Founding.cs`,
`backend/tests/founding_test.py`, `backend/tests/PCI.Backend.Tests/FoundingGatesTests.cs`.

---

## The one-line version

> A limited founding cohort, joined by invitation during the founding stage.
> Founding waives the fees, not the examination.

---

## Approved copy

Founding routes are a **time-limited, founding-stage** opportunity to help
establish PCI and its community.

**There is one founding route and one founding designation.** A person on it is a
**Founding Member**; collectively they are **the founding cohort**. The route is
joined **by invitation, using a founding code** — it is not open self-serve
enrolment.

Founding members receive membership, study access and examination access, and are
recognised as early builders of the standard. During the founding window the
institute waives the membership and examination fees.

**Founding status recognises early participation and support. It does not grant a
credential.** The examination is unchanged — the same real, proctored exam, marked
to the same standard, with an independent certification decision. The founding
cohort is *early*, not *exempt*:

> The credential is still earned by passing the exam — founding waives the fees,
> not the examination.

An examined PCI credential — **PCL-AI, PFL-AI or PML-AI** — is always earned by
passing the examination, on any route.

### What founding participants can expect

Published as confirmed, not deferred:

- Membership, full study access and examination entry, at no fee while the window
  is open
- Recognition as an early builder of the standard
- The opportunity to help shape the standard through consultation
- An honest view of where the institute stands — including that recognition is
  *intended* to grow, with **no current third-party recognition promised**

---

## What must not be said

| Do not say | Why |
|---|---|
| Founding Employer · Founding Partner · Founding Chapter Lead | Zero occurrences across all 235 live pages. These designations do not exist. |
| Any multi-tier founding structure | `Founding.cs:9` — "ONE founding route". `AdminMgmt.cs:346` normalises `founding_member`/`founding_candidate` → `founding` and rejects anything else as `bad_founding_route`. |
| A founding cohort *per credential* | The grant is hardcoded to the default certification (`Founding.cs:117`, pinned by `FoundingGatesTests.cs:230`). Per-certification routes are Phase 4 and unbuilt. |
| A named deadline, cap or cohort size | None is published. The window end date is injected at runtime and only when a window is open (`membership.html:64`). |
| A founding fee or discount amount | Founding is published as free / "fees waived". No amount is published. |
| "Fees and benefits will be published before enrolment opens" | That deferral belongs to the refund policy page, not to founding. Founding entitlements are published as confirmed. |
| "Founding members are the first certified" | `founding-status.html`: "First certified cohort — Upcoming. No one has yet been certified." |
| "Enrolment is open" as an unqualified claim | Whether a window is open is data-driven. `Founding.cs:181` returns `open:false` when no active in-window code exists, and `membership.html` ships the founding block `display:none` until the API says otherwise. |

**Adjacent but different — do not merge into founding-route copy:**
*Founding contributors* (chapter volunteering, e.g. `chapter-us.html`), *founding
group* (chapter formation), *founding cohort of training partners*
(`training-partners.html`), and *Founding examiner panel & SMEs* (internal
appointments). Four separate things that share a word.

---

## Claims audit

| Claim | Source | Status |
|---|---|---|
| One founding route, one designation | `Founding.cs:9`; `AdminMgmt.cs:346-348`; test `F0d` | ✅ enforced in code |
| "Founding Member" is the published designation | `route-founding.html:11`; `founding-status.html:7` | ✅ |
| "the founding cohort" | `route-founding.html:9` | ✅ |
| Joined by invitation, during the founding stage | `route-founding.html:10` — "joined by invitation during the founding stage" | ✅ |
| Time-limited, no published end date | `membership.html` — "Founding programme — limited period"; end date injected at runtime | ✅ limited ✅ no date published |
| Receives membership + study + exam access | `route-founding.html:11`; `FoundingCard.tsx:37-44` | ✅ |
| Fees waived; published as free | `route-founding.html:15` (route table: Founding / Free / Yes / earned); `membership.html` | ✅ no amount published |
| Credential still earned by passing the exam | `route-founding.html:11`, `:18`; `membership.html`; `FoundingCard.tsx:180` | ✅ published verbatim |
| No credential without a passed exam | test `F10`: `COUNT(*) FROM issued_credentials WHERE attempt_id IS NULL` must be 0 | ✅ hard invariant |
| Same real, proctored examination | `membership.html` — "the same real, proctored PCL-AI exam" | ✅ |
| No current third-party recognition | `founding-status.html:7` — "We promise no current third-party recognition." | ✅ published limit |
| Opportunity to shape the standard | `founding-status.html:7` — "You can help shape the standard through consultation" | ✅ |
| No one certified yet | `founding-status.html:7` — "First certified cohort — Upcoming." | ✅ |
| Founding Employer / Partner / Chapter Lead | — | ❌ **do not exist**; removed from draft copy |
| Per-credential founding cohorts | — | ❌ **not built**; grant is single-certification |
| Published fee amount, deadline or cap | — | ❌ **not published**; do not invent |

**Deliberately absent**, per the Institute's editorial rule: no accreditation
claim, no participant counts, no testimonials, no employer or partner logos, no
salary or job-outcome promise, no third-party recognition, and no suggestion that
paying or joining early shortens the path to a credential.
