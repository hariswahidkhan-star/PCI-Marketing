# Connector execution report — PCI AI 75-second institutional film

Every connector in the directory appears below, whether or not it could be used.
Where something did not work, the actual error is quoted rather than paraphrased.

**Directory audit.** `ListConnectors` returned **15** connectors. Nine were
connected *and* enabled in this chat session; six were not, and no amount of
prompting can call a tool that is not loaded. That is a session/authorisation
state, not a judgement about the products.

---

## A. Connectors used — real actions, already performed

| Connector | Actual action performed | Output | File or preview location | Status | Limitations |
|---|---|---|---|---|---|
| **Notion** | Built a 10-page production workspace: creative brief, source register, verified-claims register, script, storyboard, shot list, production status, connector activity log, asset-licensing register, review checklist | Live Notion workspace, 11 pages | [Parent page](https://app.notion.com/p/3d278df9d44481b28bffe37fe3bca817) (**private** — no destination was named) | ✅ Done | Content mirrors this repository; Notion is the readable copy, the repo is the source of truth |
| **Unsplash** | 40 assets shortlisted across the 7 required themes; public collection created; full licensing register with photographer, profile, photo URL and licence per asset | `assets/unsplash-register.md` + collection `2_SQb2vY4uQ` | [Collection](https://unsplash.com/collections/2_SQb2vY4uQ/pci-ai-75s-institutional-film-visual-reference) | ✅ Done | First `create_collection` returned `422` on a long description; retried shorter and succeeded. **No credible Gantt/programme-wall photography exists on Unsplash** — that beat was not faked. **Reference only: no Unsplash asset appears in the delivered film.** |
| **vidIQ** | `keyword_research` on "project controls" + `score_title` ×3; produced 3 titles, YouTube description, 8 chapters, LinkedIn caption, 20 search phrases, 3 thumbnail wordings, 2 alt texts | `metadata/vidiq-metadata.md` | Repo | ✅ Done | **20 credits spent** (150 → 130), the authorised ceiling. Only one keyword call was affordable, so 12 of 20 phrases are labelled *editorial, not tool-derived*. Honest finding: these are low-volume specialist terms (`project controls` ≈ 4,485/mo) — this is a credibility piece, not a reach play. |
| **Gamma** | `get_gammas` + `read_gamma` on the workspace | Recovered a **pre-existing** deck, *"PCI AI Introduction Film — Launch Kit"* (`g_nwgal8v5rv6fa4e`), from an earlier 60-second effort — **not created by this production** | [Gamma](https://gamma.app/docs/PCI-AI-Introduction-Film-Launch-Kit-s8dspcw0pgi789b) | ✅ Read | **This is the single most valuable connector result of the run.** It records three claims dropped as unsubstantiated; those same figures are listed as "substantiated" in `PCI-Marketing/README.md`. Independently confirmed against the site source — see `claims-register.md` §4. **Generating a new treatment deck is a paid action and is in the approval gate.** |
| **ElevenLabs** | Surveyed voices, then generated **39 narration segments** — 15 for the 75-second film, 4 for the 15-second launch film, 16 for the 4:16 explainer, plus a 4-voice A/B | **Chosen: "Jim Executive — Authoritative, British and Warm"** (`tXxkePQsw0G69D8VeDzp`), used in all three films so they read as one body of work. The 75s and 15s films are on `eleven_multilingual_v2`; the explainer is on **`eleven_v3`**, which takes emotional direction inline from the text | `dist/…-voiceover.wav`, `…-mixed-soundtrack.wav`, and the narration in every master of **all three** films; `../explainer/audio/voice-test/` holds the A/B | ✅ **Delivered** | **~5,400 credits (~$0.98) in total.** Every segment generated one take each (`generations_count: 1`, since the default of 4 would have quadrupled the spend). **No voice cloning** — a stock library voice, not a clone, and not presented as a named person. Two limitations worth recording rather than hiding: a bare `creative_list_voices` returned only 3 voices and the first narrator was picked from those 3 — searching properly returns 22, which is what the A/B corrected; and `eleven_multilingual_v2` has no emotional direction at all, which is why the explainer was re-recorded on `eleven_v3`. On the 75-second film the read came back ~19% slower than the film's design pace, forcing the timeline conform documented in that README. |
| **Runway** | Initially `whoami` only (video was plan-gated). **After the user purchased a package: generated 5 B-roll clips** — 4 × `gen-4.5` and 1 × `kling-3-pro`, all 1080p | 5 clips, 40 s of footage | `assets/generated/README.md` (task IDs + signed URLs) | ✅ **Generated** | **480 credits spent** (12/sec at 1080p); 837 remain. **The clips could not be downloaded**: Runway's CDN `dnznrvs05pmza.cloudfront.net` is refused by the egress policy (`connect_rejected`, 403 to CONNECT), so they could not be composited here. Delivered instead as an **alpha type-layer master** plus a tested `composite.sh`. |
| **Higgsfield** | `balance` + `models_explore` (video, cinematic) | **80 credits, "basic" plan.** Enumerated available models | — | ✅ Inspected | 80 credits is very low for video generation. `unlim.available: false` — no free trial generations. **Useful discovery: Kling v3.0 is reachable *through* Higgsfield** as model `kling3_0`, which is how the Kling requirement can honestly be met (see §B). |
| **HyperFrames by HeyGen** | `list_projects` (empty) + `get-send-to-hyperframes-guide` — read the full authoring contract | Established the only viable path for this client | — | ✅ Inspected | **`compose` and `render_video` are disabled for CLI/IDE clients** by the server's own design — this session is Claude Code, so they are unavailable regardless of approval. The viable path is `import-claude-design-from-url` with one self-contained HTML (fonts/logo inlined as base64). Per the guide: **import is free, enhance is free, render is the paid step** (20 credits/rendered minute). |
| **Gmail** | `create_draft` — approval email saved as a **draft only** | Draft `r120491591506615097` — title, executive summary, preview location, exact 15-segment transcript, connectors used, licensing status, outstanding issues, 12-point approval checklist | Gmail → Drafts | ✅ Done | **Not sent.** The **recipient field is deliberately blank** so it cannot be sent by accident. |

---

## B. Connectors that could not be used — with the exact reason

| Connector | Attempted | Actual error / state | Effect on this production |
|---|---|---|---|
| **Google Drive** | `search_files` for PCI brand material | `MCP server "Google_Drive" requires re-authorization (token expired)` | **Material.** No official logo, brand material or approved descriptions could be retrieved, and **no production folder could be created** — so scripts, storyboards and exports are **not** saved to Drive. Mitigated: the real `logo.svg` and the site's own Archivo/Inter faces were taken from the `PCI-Marketing` repository, and every deliverable is committed to git instead. **Nothing was overwritten** — no source file was touched. |
| **Cloudinary** | — | `enabledInChat: false` — the connector is installed for the org but its tools are **not loaded in this session**, so no call is possible | Normalisation, format optimisation, master preservation and derivative sizes were done **locally with ffmpeg instead**, which is what Cloudinary would have been asked to do. Landscape, vertical and square masters, a high-quality master, clean filenames and version numbers are all delivered — just not via Cloudinary. |
| **Cling** | — | `installState: "needs_reconnect"`, `connected: false`, `enabledInChat: false` | No action possible. Its capabilities could not even be inspected, so no claim is made about what it can or cannot do. |
| **Kling** (listed in the directory as **"Killing"**) | — | `installState: "needs_reconnect"`, `connected: false`, `enabledInChat: false` | The standalone connector is still unusable. **But the requirement is now genuinely met: the Runway package exposes `kling-3-pro` directly**, and the scene-7 closing shot was generated with it (task `2c481573-5e57-40c7-9881-0e66e686f45c`). Kling is also reachable via Higgsfield as `kling3_0`. Note the directory entry appears to be a typo for "Kling". |
| **Microsoft 365** | — | `enabledInChat: false` | Not required by the brief; no production need went unmet. |
| **Tella** | — | Connected at org level but the session reports it **requires authentication**; this session is non-interactive and cannot run an OAuth flow | Not required by the brief; no production need went unmet. |

**To enable these:** Google Drive, Cling, Kling and Tella need re-authorising in
claude.ai → Settings → Connectors. Cloudinary and Microsoft 365 need switching
on for this chat in the conversation's connector settings.

---

## C. What was NOT done, and why — the approval gate

The brief's safety controls require explicit approval before consuming paid
connector credits. Everything above is free or already-authorised. The
credit-consuming actions are held and itemised in **`approval-request.md`**, with
exact cost, files affected and reversibility for each.

**The film is complete and deliverable without any of them.** The only thing
missing is the synthesised voiceover, and the masters ship with picture,
captions and the music bed — exactly as the 15-second film does — so the
approval decision is about upgrading the deliverable, not unblocking it.


---

## D. Connector-by-connector production plan

The plan and its execution, side by side. "Held" means technically possible and
awaiting your approval; "not possible" means the connector cannot do it here.

| Connector | Planned role (from the brief) | Executed | Held / not possible |
|---|---|---|---|
| Google Drive | Retrieve brand material; create a production folder; save all outputs | — | **Not possible** — expired token. Outputs are committed to git instead |
| Notion | 10-part production workspace | ✅ All 10 pages | — |
| Gamma | Visual-treatment + storyboard deck | ✅ Read the workspace; recovered decision-critical prior art | Deck generation **held** (paid) |
| Unsplash | Licensed reference across 7 themes, with creator/URL/licence | ✅ 40 assets + collection + register | — |
| Higgsfield | Cinematic establishing shots and controlled camera moves | ✅ Capability + balance inspected | Generation **held** — 80 credits, likely insufficient |
| Runway | B-roll, continuity, artefact removal, compositing, transitions, aspect adaptation | ✅ Authenticated and inspected | **Not possible** — video models plan-gated (`availableVideoModels: []`) |
| Kling | Complementary motion sequences | — | **Not possible** standalone (needs reconnect). Reachable as `kling3_0` **via Higgsfield** — **held** |
| HyperFrames (HeyGen) | Assemble scenes, pacing, visual continuity | ✅ Projects listed; authoring contract reviewed | `compose`/`render_video` **disabled for this client type**; import path **held** (render ~25 credits) |
| ElevenLabs | Final English narration with the mandated pronunciations | ✅ Voice surveyed and selected | Synthesis **held** — ~1,227 characters |
| Cloudinary | Normalise, optimise, preserve a master, produce 3 ratios, clean filenames | — | **Not possible** — not enabled in session. **Done locally with ffmpeg instead**, in full |
| vidIQ | Titles, description, captions, phrases, chapters, thumbnail wording, alt text | ✅ Complete, 20 credits | Thumbnail scoring skipped (budget) |
| Gmail | Approval email as a draft | ✅ Draft saved | Sending **held** |
| Cling | Any genuine production task | — | **Not possible** — needs reconnect; capabilities could not even be inspected |
| Microsoft 365 | (not assigned) | — | Not enabled in session; nothing went unmet |
| Tella | (not assigned) | — | Requires authorisation; nothing went unmet |
