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
| **Notion** | Built a 10-page production workspace: creative brief, source register, verified-claims register, script, storyboard, shot list, production status, connector activity log, asset-licensing register, review checklist | Live Notion workspace | See the parent page URL reported at the end of this run | ✅ Done | Content mirrors this repository; Notion is the readable copy, the repo is the source of truth |
| **Unsplash** | 40 assets shortlisted across the 7 required themes; public collection created; full licensing register with photographer, profile, photo URL and licence per asset | `assets/unsplash-register.md` + collection `2_SQb2vY4uQ` | [Collection](https://unsplash.com/collections/2_SQb2vY4uQ/pci-ai-75s-institutional-film-visual-reference) | ✅ Done | First `create_collection` returned `422` on a long description; retried shorter and succeeded. **No credible Gantt/programme-wall photography exists on Unsplash** — that beat was not faked. **Reference only: no Unsplash asset appears in the delivered film.** |
| **vidIQ** | `keyword_research` on "project controls" + `score_title` ×3; produced 3 titles, YouTube description, 8 chapters, LinkedIn caption, 20 search phrases, 3 thumbnail wordings, 2 alt texts | `metadata/vidiq-metadata.md` | Repo | ✅ Done | **20 credits spent** (150 → 130), the authorised ceiling. Only one keyword call was affordable, so 12 of 20 phrases are labelled *editorial, not tool-derived*. Honest finding: these are low-volume specialist terms (`project controls` ≈ 4,485/mo) — this is a credibility piece, not a reach play. |
| **Gamma** | `get_gammas` + `read_gamma` on the workspace | Recovered a **pre-existing** deck, *"PCI AI Introduction Film — Launch Kit"* (`g_nwgal8v5rv6fa4e`), from an earlier 60-second effort — **not created by this production** | [Gamma](https://gamma.app/docs/PCI-AI-Introduction-Film-Launch-Kit-s8dspcw0pgi789b) | ✅ Read | **This is the single most valuable connector result of the run.** It records three claims dropped as unsubstantiated; those same figures are listed as "substantiated" in `PCI-Marketing/README.md`. Independently confirmed against the site source — see `claims-register.md` §4. **Generating a new treatment deck is a paid action and is in the approval gate.** |
| **ElevenLabs** | `creative_list_voices` — surveyed the workspace and selected a narrator | **Chosen: "Jim Executive — Authoritative, British and Warm"** (`tXxkePQsw0G69D8VeDzp`). A library voice, described for corporate narration and documentary — matching the brief's "warm, authoritative, internationally understandable" | — | ✅ Voice selected; **synthesis awaiting approval** | Only 3 voices in this workspace. **No voice cloning was performed or proposed** — this is a stock library voice, not a clone of any real person. |
| **Runway** | `whoami` — authenticated, enumerated genuinely available models | Workspace "Certuvo"; **452 credits** | — | ✅ Inspected | **Material finding: `availableVideoModels` is EMPTY.** Every Runway video capability — generate, edit, expand, multi-shot, upscale — is plan-gated on this account. Runway can do **images only** (`nano-banana-pro`, `gen-4`, `seedream-5`, …). The brief's Runway tasks (B-roll, continuity, artefact removal, transitions, aspect adaptation) are **not technically possible** on this plan. |
| **Higgsfield** | `balance` + `models_explore` (video, cinematic) | **80 credits, "basic" plan.** Enumerated available models | — | ✅ Inspected | 80 credits is very low for video generation. `unlim.available: false` — no free trial generations. **Useful discovery: Kling v3.0 is reachable *through* Higgsfield** as model `kling3_0`, which is how the Kling requirement can honestly be met (see §B). |
| **HyperFrames by HeyGen** | `list_projects` (empty) + `get-send-to-hyperframes-guide` — read the full authoring contract | Established the only viable path for this client | — | ✅ Inspected | **`compose` and `render_video` are disabled for CLI/IDE clients** by the server's own design — this session is Claude Code, so they are unavailable regardless of approval. The viable path is `import-claude-design-from-url` with one self-contained HTML (fonts/logo inlined as base64). Per the guide: **import is free, enhance is free, render is the paid step** (20 credits/rendered minute). |
| **Gmail** | `create_draft` — approval email saved as a **draft only** | Draft in the account | Gmail → Drafts | ✅ Done | **Not sent.** Sending requires explicit authorisation, per the brief and standing policy. |

---

## B. Connectors that could not be used — with the exact reason

| Connector | Attempted | Actual error / state | Effect on this production |
|---|---|---|---|
| **Google Drive** | `search_files` for PCI brand material | `MCP server "Google_Drive" requires re-authorization (token expired)` | **Material.** No official logo, brand material or approved descriptions could be retrieved, and **no production folder could be created** — so scripts, storyboards and exports are **not** saved to Drive. Mitigated: the real `logo.svg` and the site's own Archivo/Inter faces were taken from the `PCI-Marketing` repository, and every deliverable is committed to git instead. **Nothing was overwritten** — no source file was touched. |
| **Cloudinary** | — | `enabledInChat: false` — the connector is installed for the org but its tools are **not loaded in this session**, so no call is possible | Normalisation, format optimisation, master preservation and derivative sizes were done **locally with ffmpeg instead**, which is what Cloudinary would have been asked to do. Landscape, vertical and square masters, a high-quality master, clean filenames and version numbers are all delivered — just not via Cloudinary. |
| **Cling** | — | `installState: "needs_reconnect"`, `connected: false`, `enabledInChat: false` | No action possible. Its capabilities could not even be inspected, so no claim is made about what it can or cannot do. |
| **Kling** (listed in the directory as **"Killing"**) | — | `installState: "needs_reconnect"`, `connected: false`, `enabledInChat: false` | The standalone connector is unusable. **However, Kling v3.0 is genuinely reachable via Higgsfield** (`kling3_0`, 3–15 s, 16:9/9:16/1:1, multi-shot) — that is the route proposed in the approval gate. Note the directory entry appears to be a typo for "Kling". |
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
