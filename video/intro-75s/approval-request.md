# Approval request — paid and irreversible actions

Your standing instruction is that I stop and ask before consuming paid connector
credits or taking an irreversible external action. Everything free has been done;
these five are held. **None of them blocks delivery** — the film is finished and
deliverable now, with picture, burned-in captions and the music bed.

Approve any subset. "Approve A only" is a perfectly good answer, and A is the one
I would actually recommend.

---

### A. Synthesise the voiceover — **recommended**

| | |
|---|---|
| **Exact action** | `ElevenLabs creative_generate_speech` × 15 segments, using voice **"Jim Executive — Authoritative, British and Warm"** (`tXxkePQsw0G69D8VeDzp`), reading `captions/vo-script.md` |
| **Connector** | ElevenLabs |
| **Expected cost** | **1,227 characters.** On most ElevenLabs tiers 1 character = 1 credit, so ≈ **1,227 credits**. Your workspace quota was not exposed by the API, so this is the character count — accurate — and the credit conversion — tier-dependent. |
| **Files affected** | **Creates only.** New: `audio/vo-*.wav`, `dist/…-voiceover.wav`, `dist/…-1920x1080-final.mp4`. No existing file is modified or replaced. |
| **Reversible?** | **The files, yes** — delete and rebuild. **The credits, no.** |
| **Why** | It is the one thing the pipeline genuinely cannot make for itself, and it completes deliverable #10 ("clean voice-over audio") and #11 ("mixed soundtrack"). The read is timed to the hundredth of a second, so it drops straight in. |
| **Safety** | This is a **stock library voice, not a clone.** No real person's voice is cloned, consistent with the brief. |

### B. Generate the visual-treatment deck

| | |
|---|---|
| **Exact action** | `Gamma generate` — a premium treatment/storyboard deck: narrative structure, scene composition, typography, brand colours, on-screen messages, transitions, closing frame, landscape + vertical layouts |
| **Connector** | Gamma |
| **Expected cost** | One Gamma generation. The API does not expose a credit balance or per-generation price, so I cannot quote a number — only that it is one generation against your Gamma plan. |
| **Files affected** | **Creates only** — a new Gamma. The existing *"PCI AI Introduction Film — Launch Kit"* is **not** touched (the Gamma tools cannot edit an existing deck in any case). |
| **Reversible?** | The deck can be deleted; the generation cannot be refunded. |
| **Note** | `storyboard.md` and `shot-list.md` already contain this content in full. The deck is a presentation of work that exists, not new work. |

### C. Generate cinematic B-roll — Higgsfield, and Kling *through* Higgsfield

| | |
|---|---|
| **Exact action** | `Higgsfield generate_video`: 3–4 shots at 5 s — an infrastructure establishing shot and a project-controls environment via **`cinematic_studio_video_v2`**; a data-supported-decision sequence via **`kling3_0`** (this is how the Kling requirement gets met honestly, since the standalone Kling connector will not connect) |
| **Connector** | Higgsfield (carrying Kling v3.0) |
| **Expected cost** | **Unknown, and this is the problem.** Your balance is **80 credits on the "basic" plan** and `models_explore` does not return per-generation pricing. 80 credits is, in my judgement, **likely insufficient** for even one 5-second cinematic generation. `unlim.available: false`, so there are no free trial generations. |
| **Files affected** | Creates new media in your Higgsfield workspace, then downloaded to `assets/generated/`. Nothing overwritten. |
| **Reversible?** | No — generation credits are spent whether or not the output is usable. |
| **Recommendation** | **Hold this one.** The delivered film is a designed, typographic institutional piece and does not need B-roll to work. If you want live-action footage, the honest sequence is: top up credits first, then approve a small test generation, then decide. Also note the delivered film currently contains **zero AI-generated imagery** — approving this changes that, and every generated shot would need labelling in the asset manifest, with no generated environment presented as an actual PCI facility. |

### D. Runway — **not viable, listed for completeness**

| | |
|---|---|
| **Exact action** | The brief's Runway tasks: B-roll, scene continuity, artefact removal, compositing, transitions, aspect adaptation |
| **Connector** | Runway (workspace "Certuvo", 452 credits) |
| **Expected cost** | n/a |
| **Reversible?** | n/a |
| **Status** | **Technically impossible on this plan, not merely unapproved.** `whoami` returns `availableVideoModels: []` and gates video, editVideo, expandVideo, multishotVideo and upscaleImage behind a paid plan. Runway can generate **images only** here. If you want a Runway still (e.g. an alternative poster), say so and I will quote it separately — but every task the brief assigned to Runway needs the video models. |

### E. Render the film through HyperFrames

| | |
|---|---|
| **Exact action** | Inline the fonts and logo as base64 into a single self-contained composition, publish it to a fetchable URL, `import-claude-design-from-url`, then `render_video` |
| **Connector** | HyperFrames by HeyGen |
| **Expected cost** | Per its own authoring guide: **import is free, enhance is free, render is paid at 20 credits per rendered minute** → 75 s ≈ **25 credits**. Free accounts get 3 renders/month. |
| **Files affected** | Creates a hosted HeyGen project. Nothing local is overwritten. |
| **Reversible?** | The project can be deleted; the render credits cannot be refunded. |
| **Recommendation** | **Hold.** This would be a *second, lower-fidelity* production of a film you already have: the HyperFrames path cannot reproduce the per-frame palette interpolation or the three genuine per-aspect layouts, and `compose`/`render_video` are disabled for this client type anyway. Worth doing only if you specifically want the film living inside HeyGen for their enhance/avatar pipeline. |

---

## Not requested, and not done

- **Sending the approval email.** It is saved as a Gmail **draft**. It will not be sent without your explicit say-so.
- **Publishing anywhere** — no upload to YouTube, LinkedIn, or any platform.
- **Replacing any source file.** Nothing was overwritten anywhere. Google Drive was unreachable, so no Drive file was touched even accidentally.
- **Voice cloning.** Not performed, not proposed.

## My recommendation in one line

**Approve A. Hold B, C and E. D is not available.** That gets you the finished
film with a professional narration for roughly 1,200 ElevenLabs characters, and
spends nothing else.
