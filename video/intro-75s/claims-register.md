# Verified-claims register — PCI AI 75-second institutional film

Every factual statement the film makes, and where it comes from. Anything that
could not be traced to a first-party source was removed rather than softened.

---

## 1. How verification was actually done — and one thing that could not be

The brief asks for the two production websites to be reviewed directly.
**That was not possible in this environment.**

| Intended source | Result |
|---|---|
| `https://pciai.org` | **Blocked.** `EGRESS_BLOCKED — Access to pciai.org is blocked by the network egress proxy.` |
| `https://projectcontrolsinstitute.org` | **Blocked.** Same egress-proxy refusal. |
| Google Drive (official logos, brand material, approved descriptions) | **Unavailable.** `MCP server "Google_Drive" requires re-authorization (token expired)`. |

Verification was therefore done against the **first-party source of the live
site**, which this session does have: the platform repository
`hariswahidkhan-star/PCI`. Its `backend/wwwroot/` directory *is* the 235-page
public website — the same HTML the two domains serve. Where this register cites
a page, it cites that file.

This is a good substitute, not a perfect one: it is the source the site is
built from, so it cannot confirm what is **currently deployed** at either
domain. **Confirm this register against the live sites before publication.**

Brand assets were taken from `hariswahidkhan-star/PCI-Marketing`
(`video/launch-15s/brand/`) — the real `logo.svg` and the site's own Archivo and
Inter faces. The logo is used as supplied and is neither redrawn nor distorted.

---

## 2. Claims the film makes — all verified

| # | Claim (as it appears) | Where | Source | Status |
|---|---|---|---|---|
| 1 | "PCI AI" as the brand mark | Furniture, S5, S8 | `accreditation-status.html` header; used site-wide | ✅ |
| 2 | "Project Controls Institute Global, Inc." | Furniture, S5, S8 | schema.org `Organization.name`, `accreditation-status.html` | ✅ |
| 3 | A Delaware Non-Stock Corporation | S8 legal line | Site footer, verbatim | ✅ |
| 4 | Focus is project controls, project finance and project management | S5 | schema.org `description`; site footer "the integrated discipline of project controls, cost engineering and project finance — with governed AI throughout" | ✅ |
| 5 | **PCL-AI** — project controls | S6 | schema.org: "PCI AI Project Controls Leader (PCL-AI)" | ✅ |
| 6 | **PFL-AI** — project finance | S6 | schema.org: "PCI AI Project Finance Leader (PFL-AI)" | ✅ |
| 7 | **PML-AI** — project management | S6 | schema.org: "PCI Project Management Leader – AI (PML-AI)" | ✅ |
| 8 | Not accredited by ANAB, IAS or any ISO/IEC 17024 body; framework developed with reference to ISO/IEC 17024 personnel-certification principles | **S6 and S8, on screen** | `accreditation-status.html`, verbatim from the site footer | ✅ **required, present** |
| 9 | `pciai.org` and `projectcontrolsinstitute.org` | S8 | Both are production domains named in the brief; `projectcontrolsinstitute.org` is the canonical URL throughout the site's schema.org data | ✅ |

**The brief's scene-6 instruction is discharged.** It said: *"If these credentials
cannot be verified from official sources, remove this entire scene."* They were
verified — items 5–7 above — so the scene stays, and the trailing hedge
"subject to verification against official PCI AI information" was **removed from
the read**, because it is no longer true that the point is unverified. That also
bought back ~2 seconds the film needed (see §5).

### Statements that are argument, not fact

Scenes 1–4 and 7 make no claim about PCI. They set out a professional position —
that AI accelerates analysis, that a convincing output is not automatically a
reliable decision, and that responsible adoption needs evidence and human
judgment. Nothing there asserts a fact about the Institute, so nothing there
needs a source. It is consistent with the Institute's published governing
principle, *"AI proposes. The professional disposes."*

---

## 3. Prohibited claims — confirmed absent

Each of these was checked against the finished on-screen text and the read.

| Prohibited | In the film? |
|---|---|
| Accreditation | ❌ Absent — and the **opposite** is stated on screen twice |
| Government endorsement | ❌ Absent |
| University recognition | ❌ Absent |
| Employer preference | ❌ Absent |
| Global ranking | ❌ Absent |
| Industry-standard status | ❌ Absent |
| Partnerships | ❌ Absent |
| Membership numbers | ❌ Absent |
| Certification outcomes | ❌ Absent |
| Salary increases | ❌ Absent |
| Guaranteed career benefits | ❌ Absent |
| Unverified statistics | ❌ Absent — **no statistic of any kind appears** |
| Staging / dev / preview domain | ❌ Absent — only the two production domains appear |

The film carries **no numbers at all**. That is deliberate, and §4 explains why
it turned out to matter.

---

## 4. A conflict between two internal sources — and what was done about it

While inspecting the Gamma workspace, a **pre-existing** deck was found:
*"PCI AI Introduction Film — Launch Kit"* (`g_nwgal8v5rv6fa4e`), from an earlier
60-second effort. **It was not created by this production.** It records that
three claims were dropped from that film because they could not be
substantiated.

Those same three figures are listed as **"Substantiated numbers"** in
`PCI-Marketing/README.md`. So two internal sources disagree. This was checked
directly against the 235-page site source:

> **CORRECTION, made after a second pass.** The first version of this table
> reported the 13-domain figure as unfound. That was a **false negative**: the
> search covered only numeral forms (`13-domain`, `13 domains`) and the site
> spells the number in words. Re-run against word forms, the picture is:

| Figure | In `PCI-Marketing/README.md` | Found in the live-site source? |
|---|---|---|
| "13-domain body of knowledge" | Listed as substantiated | ✅ **VERIFIED — 15 pages** say "thirteen domains". `body-of-knowledge.html`: *"thirteen domains, sixty-one Knowledge Areas, weighted 40/40/20"* |
| "1 September 2026" launch | Listed as fact | ❌ **Not found** — 0 pages, in numerals or words |
| "25 country chapters" | Listed as substantiated | ❌ **Not found** — 0 pages for "twenty-five" or "25 chapters". 25 `chapter-*.html` pages exist, but `chapters.html` states **"Chapters are in formation; PCI does not overstate local presence."** Claiming 25 operating chapters would contradict the site's own caution. |
| "7 launch languages" | Listed as substantiated | ❌ **Not found** — 0 pages |

**Effect on this film: none.** It uses none of the four. That was not luck in
hindsight — the film was built to carry no statistics — but it does mean this
production needed no correction.

**Two things for the Institute to note, outside this film's scope:**

1. `PCI-Marketing/README.md`'s "Substantiated numbers" table is **partly**
   supported: the 13-domain figure is solid, the other three are not.
2. **The existing 15-second launch film carries two unverified figures on
   screen** — `NOW LIVE · 1 SEPTEMBER 2026` in shot 1, and `25 country chapters`
   in shot 3. (`13-domain body of knowledge`, also in shot 3, is fine.) The
   chapters claim is the more serious of the two, because the site explicitly
   declines to overstate local presence. That film needs a decision before
   further distribution. It has not been re-cut here — that call belongs to the
   Institute.

**Lesson recorded for future verification:** search word forms as well as
numerals. A single-form grep produced a confident false negative that was
reported before it was caught.

---

## 5. Changes made to the supplied transcript, and why

The brief allows correction where "verified source material requires" it, and
asks that meaning, professional tone and approximate timing be preserved.

| Change | Reason |
|---|---|
| Removed "…, subject to verification against official PCI AI information" from scene 6 | The credentials **were** verified (§2 items 5–7), so the hedge had become inaccurate. Removing it also relieved the tightest scene in the film. |
| Scene boundaries redistributed in proportion to how much each scene has to say | See below. |
| Added the accreditation-status line to S6, and the full legal line to S8 | Required by the Institute's own published editorial rule; not optional for a certification body. |

### The timing problem, stated plainly

The supplied transcript is **too long for 75 seconds at an unhurried
institutional pace.** Measured, with spelled acronyms counted at their real
spoken length:

- **176 word-units** of copy.
- At **145 wpm** — the middle of the professional-narration band — that is
  **73.0 s of speech**, plus ~5.7 s of scene-edge silence and breaths: a
  **78.7-second film**.
- To fit **75.0 s**, the read must run at **153 wpm**.

153 wpm is at the top of the professional band. It is brisk but not rushed, and
it is what has been built. Two scenes would have been unusable at the literal
timecodes in the brief — scene 7 at 31 words in 10 s is **209 wpm**, and the
closing line at 3 s is **250 wpm** — so scene durations were reallocated in
proportion to content. Every scene now sits at the same ~153 wpm, and no scene
is worse than the average. That matters most for scene 6, where three spelled
acronyms have to land cleanly.

| Scene | Brief | Delivered | Δ |
|---|---|---|---|
| S1 | 0:00–0:08 | 0.00–8.50 | +0.5 |
| S2 | 0:08–0:18 | 8.50–16.60 | −1.4 |
| S3 | 0:18–0:29 | 16.60–26.90 | −2.1 |
| S4 | 0:29–0:40 | 26.90–36.30 | −3.7 |
| S5 | 0:40–0:51 | 36.30–47.40 | −3.6 |
| S6 | 0:51–1:02 | 47.40–57.60 | −4.4 |
| S7 | 1:02–1:12 | 57.60–70.80 | −1.2 |
| S8 | 1:12–1:15 | 70.80–75.00 | −1.2 |
| **Total** | **75.0 s** | **75.00 s** | **0** |

**If you would rather have the unhurried read than the exact 75 seconds**, an
81-second cut at 145 wpm is a one-line change: edit `SCENES` in `src/vo.py` and
`SHOTS` in `src/scene.html`, then rebuild. Say the word and it is done.

---

## 6. Media provenance

| Media | Origin | Licence |
|---|---|---|
| All picture in the delivered masters | **Generated deterministically from `src/scene.html`** in this repository — typography, motion and colour computed in the browser. No stock footage, no AI-generated imagery. | PCI's own work |
| Score | **Composed from scratch** in `src/music.py` — additive synthesis, standard library only, no samples or third-party loops | PCI's own work, no licence obligation |
| Archivo, Inter | The site's own faces, from `brand/` | Open Font Licence |
| `logo.svg` | Supplied PCI mark, used unmodified | PCI's own |
| Unsplash reference set | 40 assets registered in `assets/unsplash-register.md` | Unsplash Licence — **sourced as reference only; none appears in the delivered film** |

Nothing in the film is AI-generated imagery, so the question of labelling
AI-generated media does not arise for the delivered masters. If any Higgsfield,
Kling or Runway material is approved later, it must be labelled as
AI-generated in this register before it ships — and no generated environment may
be presented as an actual PCI facility.
