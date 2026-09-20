# Production spec — PCI AI campaign

Read this and `claims-register.md` before writing a frame. `r1/scene.html` is
the worked reference; copy its structure.

## The set

| Asset | Aspect | Length | Job |
|---|---|---|---|
| r1 | 9:16 | 26s | Manifesto — "AI proposes, the professional disposes" *(built)* |
| r2 | 9:16 | 28–32s | The three credentials: what each is actually for |
| r3 | 9:16 | 28–32s | What the credential assesses — the 13 domains |
| r4 | 9:16 | 28–32s | Verification — can anyone check your credential? |
| r5 | 9:16 | 30–34s | The founding offer |
| v1–v5 | 4:5 primary, 16:9 also | 40–55s | Longer forms of the same five arguments |

**4:5 (1080×1350), not 16:9, is the primary for the five "videos".** LinkedIn's
own organic benchmark puts native documents at 7.00% engagement, multi-image at
6.45% and video at 6.00%, and 16:9 is the weakest of the three ratios in a
mobile feed. 4:5 keeps nearly the mobile height of 9:16, survives desktop and
leaves a text column. 16:9 is rendered too, for YouTube and the website.

## Two grounds

PCI asked for some of the set to be bright. Both treatments are the same
brand — crimson, blue and the crimson-to-blue rule are identical in each; only
the ground, the ink and the panel surfaces move. A film picks its ground with
`class="light"` on `#stage`, and nothing else changes.

| Concept | Reel | 4:5 / 16:9 | Ground | Why |
|---|---|---|---|---|
| 1 · Manifesto | r1 | v1 | **dark** | declarative — navy carries authority |
| 2 · The three credentials | r2 | v2 | **dark** | same register as the manifesto |
| 3 · What it assesses | r3 | v3 | **light** | explanatory — light reads open, and a syllabus should feel legible, not solemn |
| 4 · Verification | r4 | v4 | **dark** | it is a challenge, and it should feel like one |
| 5 · The offer | r5 | v5 | **light** | open and generous, and a light CTA is the cheapest pattern interrupt in a feed of dark thumbnails |

Four of ten bright, paired by concept so the reel and the long cut of the same
argument always match.

Preview either without editing the file: `?theme=light` / `?theme=dark`, or
`node ../_pipeline/theme-still.mjs 1080 1920 <tag> "2,10,20" light`.

**Light grounds fail differently.** Anything hardcoded to `#fff` disappears;
use `var(--fg)`. The accent blue `#3B82F6` is too pale for small text on white,
so `.eyebrow` is switched to `--blue` under `.light` — if you introduce new
small text in an accent colour, check it.

## Hard rules

1. **Frame 1 carries the meaning.** No logo sting, no "welcome to", no
   establishing beat. The institute's name belongs in the last seconds, not the
   first. The opening on-screen line must be readable before any word is spoken,
   because every one of these autoplays muted.
2. **Vertical safe box: y 270→1250, x 65→1015** on 1080×1920. The bottom 35% is
   decorative only — platform caption, handle, audio strip and action rail all
   sit there. The probe fails the build on a violation; do not relax it.
3. **Any number, acronym, code, date, URL or email holds ≥2s.** No exceptions.
   This is where fast editing actually destroys value.
4. **5–7 visual changes per 10s.** Below 4 reads slow. **Above 8 reads as
   evasive** — and "moving too fast to be checked" is precisely the scam
   aesthetic a credentialing body cannot afford. A word reveal, a card entering
   and a beat cut each count as a change; they are not all cuts.
5. **Hold 3–4s on the payoff** — the number, the credential, the code.
6. **No narration on the reels.** They are text-led, so a caption band would
   repeat the headline word for word. Only the 4:5 / 16:9 cuts use `#cc`.
7. **Every claim comes from `claims-register.md`.** Nothing else. In particular
   no accreditation, no outcome or income claim, no member or chapter count, no
   comparison to a named body, and no statistic that is not in §1 of that file.

## The offer, and why it is handled this way

The FTC's Free Guide (16 CFR § 251.1) requires that the terms of a free offer
appear **clearly and conspicuously in close conjunction with the offer** —
expressly *not* as a footnote. Translated to video: the conditions must be in
the **same shot, on screen, legible, at the same moment** as the word "free".

So, in every asset that carries it:

- The offer appears **after the two-thirds point**, never in the hook. A code in
  the first seconds reframes the whole film as an ad, and for a credentialing
  body — which competes on recognition, not price — that is the strongest
  available scam signal.
- The `.offer` component is used unmodified, so the lockup is identical in all
  ten: `APPLY CODE` / `FOUNDINGFREE` / what it grants, in one bordered card.
- **`FOUNDINGFREE` in capitals.** The platform uppercases input before it looks
  the code up, so a lower-case stored value never matches. See `OFFER-SPEC.md`.
- What it grants is stated exactly — membership, study access, exam enrolment —
  in the same card. Not "everything", not "lifetime".
- **No countdown, no "limited places", no invented deadline.** A genuine dated
  deadline converts as well as a fake one and costs no trust; until PCI sets
  one, the films say nothing about limits.
- `info@pciai.org` closes every asset, held ≥2s.

## The kit

`common/kit.js` exposes `window.PCI`. Everything is a pure function of `t`.

| Call | What it does |
|---|---|
| `setupStage()` | sizes the stage, sets `--s`, returns `{W,H,ASPECT,SS,CC}` |
| `drawMesh(W,H,SS)` | the background grid, drawn once |
| `seg(t,a,b,ease)` | 0→1 across `[a,b]`, eased. The primitive everything uses |
| `pulse(t,a,b)` | rises and falls inside `[a,b]` |
| `revealWords(el,t,t0,{stagger,dur,rise})` | per-word kinetic reveal; preserves `<br>` and inline classes |
| `rule(el,t,t0)` | the crimson→blue signature rule, wiped from the left |
| `countTo(el,t,t0,t1,value)` | a counter computed from `t`, never accumulated |
| `activate(BEATS,t)` | shows only the live beat; returns it |
| `furniture(t,DUR,opts)` | logo, footer, progress bar |
| easings | `outCubic outExpo outQuint inOut outBack` · `mixc(a,b,p)` |

Each film must expose `window.__DUR`, `window.seek(t)` and `window.__EL` — the
probe **fails the build on any null in `__EL`**, because a renamed id otherwise
makes a whole beat silently stop animating while every layout check still
passes. That has shipped twice on an earlier project.

Use `calc(var(--s)*Npx)` for every size. `--s` is unitless on purpose so JS can
read it; `calc(var(--s)*N)` without the unit is invalid CSS and the whole
declaration is silently dropped.

## Checks

```bash
cd <film> && node ../_pipeline/probe.mjs 1080 1920 <tag>     # reels
cd <film> && node ../_pipeline/probe.mjs 1080 1350 <tag>     # 4:5
node ../_pipeline/stills.mjs 1080 1920 <tag> "2,10,20"       # look at it
```

A film is not done until the probe exits 0 **and** you have looked at stills.
