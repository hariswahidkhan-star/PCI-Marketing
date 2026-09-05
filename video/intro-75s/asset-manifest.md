# Asset and licensing manifest — PCI AI 75-second institutional film

Everything that appears in, or was used to make, the delivered masters.

## 1. What is actually in the film

**The delivered masters contain no stock media and no AI-generated media.**
Every frame is generated from `src/scene.html` — typography, motion, colour and
the S-curve motif computed per frame in a browser. This is worth stating plainly
because it removes an entire class of licensing and disclosure risk.

| Asset | Origin | Licence / rights | Used in the film? |
|---|---|---|---|
| All picture | Generated from `src/scene.html`, this repository | **PCI's own work** | ✅ Every frame |
| Score (`pci-ai-intro-75s-score.wav`) | **Composed from scratch** in `src/music.py` — additive synthesis, Python standard library only. No samples, no loops, no third-party library, no AI generation | **PCI's own work. No licence obligation, no royalties, no attribution required** | ✅ Full 75 s |
| `logo.svg` | The PCI mark, from `PCI-Marketing/video/launch-15s/brand/` | PCI's own | ✅ Top bar, S5, S8 — **used as supplied; not redrawn, recoloured or distorted** |
| Archivo (800) | `brand/archivo-latin.woff2` — the site's own display face | SIL Open Font Licence 1.1 | ✅ All headlines |
| Inter (400/600) | `brand/inter-latin.woff2` — the site's own text face | SIL Open Font Licence 1.1 | ✅ All body, captions, furniture |

**AI-generated media disclosure: none required.** No generative model produced
any pixel or sample in the delivered masters.

## 2. Sourced but NOT used — Unsplash reference set

40 assets were sourced across the seven themes the brief specifies and are
registered in full in `assets/unsplash-register.md` (photo ID, description,
photographer, profile URL, photo URL, direct image URL, licence, cleared status),
with a public collection at
[unsplash.com/collections/2_SQb2vY4uQ](https://unsplash.com/collections/2_SQb2vY4uQ/pci-ai-75s-institutional-film-visual-reference).

| | |
|---|---|
| Count | 40 shortlisted, 26 in the collection |
| Licence | **Unsplash License** — free for commercial use, no permission needed, attribution appreciated but not required |
| Unsplash+ items | **None.** Every asset returned `premium: false`, so all 40 are standard-licence and cleared |
| Status in this film | **Reference only. None appears in any delivered master.** |

If any of these are later cut into a version of the film, credit the
photographers listed in the register; `ThisisEngineering` (11 of the 40) asks for
`© This is Engineering`.

**One honest gap.** Unsplash has no credible Gantt, P6 or programme-wall
photography — searches return marketing dashboards and goal-setting notebooks
that a planner would immediately read as fake. That beat was **not faked**; the
film carries it typographically instead.

## 3. Provenance of the words

| Element | Origin |
|---|---|
| Voiceover script | Supplied in the brief. One hedge removed after verification, and scene timings redistributed — both documented in `claims-register.md` §5 |
| On-screen text | Supplied in the brief, plus the accreditation-status line taken **verbatim** from `PCI/backend/wwwroot/accreditation-status.html` |
| Legal / status lines | Verbatim from the live-site footer |
| Captions | Generated from `src/vo.py`; never hand-typed |

## 4. AI-generated media — five Runway clips (NOT in the delivered masters)

After the Runway package was purchased, five B-roll clips were generated. **They
are not in any delivered master** — Runway's artifact CDN is egress-blocked in
the production environment, so they could not be pulled in and composited.
They live in the Runway workspace; `assets/generated/README.md` has the task IDs,
signed URLs and expiry times.

| Clip | Model | Dur | Scene | Provenance |
|---|---|---|---|---|
| `s1-infrastructure` | Runway `gen-4.5` | 5 s | S1 | **AI-generated** |
| `s2-project-office` | Runway `gen-4.5` | 5 s | S2 | **AI-generated** |
| `s3-analysis` | Runway `gen-4.5` | 10 s | S3 | **AI-generated** |
| `s4-decision-meeting` | Runway `gen-4.5` | 10 s | S4 | **AI-generated** |
| `s7-judgment` | **Kling `kling-3-pro`** (via Runway) | 10 s | S7 | **AI-generated** |

Cost: **480 Runway credits** at 12 credits/second, 1080p. Balance after: 837.

**Disclosure obligations, which apply the moment any of these is used:**

- Label each as AI-generated wherever the film's provenance is stated.
- **No clip depicts an actual PCI facility** and none may be presented as one.
- The people in `s3`, `s4` and `s7` are **generated, not real**. None is a PCI
  employee, examiner, certified professional or named person, and no on-screen
  text identifies any of them. `s4` shows faces clearly despite the prompt
  asking for profiles — usable, but never caption those figures.
- **Scenes 5, 6 and 8 carry no footage by design.** Generated imagery must not
  sit behind the identity, the credential framework or the end card.

The original masters in `dist/` remain **entirely free of AI-generated media** —
that variant is unaffected by any of the above.

## 5. If further generated media is added

If more Higgsfield, Kling or Runway material is added later, then before it ships:

1. Add each clip to this manifest, **labelled as AI-generated**, with the model, prompt and date.
2. Confirm no generated environment is presented as an actual PCI facility.
3. Confirm no generated person is presented as a PCI employee, certified professional or named individual.
4. Re-run the review checklist in the Notion workspace.
