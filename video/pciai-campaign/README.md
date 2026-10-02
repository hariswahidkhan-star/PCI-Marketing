# PCI AI — founding enrolment campaign

Ten films for the founding-enrolment push: five vertical reels and five in 4:5
(also rendered 16:9). One deterministic engine, one brand, two grounds.

**Read `OFFER-SPEC.md` before publishing anything.** The promo code has to be
configured a particular way or every viewer who types it correctly is told it
is invalid. That is not a guess — it is what the platform source does.

---

## The set

| | Film | Ground | Length | The argument |
|---|---|---|---|---|
| r1 | Manifesto | dark | 26s | AI will write the schedule. It will not sign it. |
| r2 | Three letters | dark | 30s | Three credentials, and most people need one. |
| r3 | What it assesses | **light** | 30s | Thirteen published domains. Judgement, not recall. |
| r4 | Can anyone check it? | dark | 30s | A credential that cannot be checked is a claim. |
| r5 | Founding enrolment | **light** | 34s | Free because it is early — and no deadline. |
| v1 | The case | dark | 44s | The long form of r1. |
| v2 | Which of the three | dark | 49s | Which credential is yours, and which is not. |
| v3 | What the exam assesses | **light** | 46s | The long form of r3. |
| v4 | A credential nobody can check | dark | 51s | Verification, and that it cuts both ways. |
| v5 | Founding enrolment | **light** | 52s | The offer, fully explained. |

Files land in `dist/` as `pciai-<film>-<size>.mp4`.

**Which file where:** 9:16 to Reels and Shorts · **4:5 to LinkedIn** · 16:9 to
the website, YouTube watch pages and email. `POSTING-KIT.md` has the copy,
titles and hashtags, and explains why 4:5 rather than 16:9 for LinkedIn.

## They ship silent, and that is a decision

The reels are text-led and the 4:5 cuts carry burned captions, so every film
reads with the sound off — which is how all three platforms play them by
default anyway. No paid voice or music has been bought; see
`APPROVAL-GATE.md` for what that would cost and what it would buy.

A silent AAC track is muxed into every file, because some platforms mishandle
a file with no audio stream at all.

The `CAPS` array in each 4:5 film is a real narration script, written to
complement the on-screen type rather than read it back. If a read is
commissioned, the lines already match the picture frame for frame.

## Working on them

```bash
cd <film> && node ../_pipeline/probe.mjs 1080 1920 <film>   # reels
cd <film> && node ../_pipeline/probe.mjs 1080 1350 <film>   # 4:5
cd <film> && node ../_pipeline/probe.mjs 1920 1080 <film>   # 16:9
node ../_pipeline/stills.mjs 1080 1920 <film> "2,10,20"     # look at it
node ../_pipeline/theme-still.mjs 1080 1920 <film> "2,10" light
./_pipeline/build-all.sh                                    # render everything, serially
```

`SPEC.md` is the production spec and it is binding. `claims-register.md` is
the only set of claims any film may make.

### What the probe checks, and why each one exists

Every check here was added because something got through without it:

| Check | Added after |
|---|---|
| page and console errors | — |
| dead element handles | a renamed id silently stopped a whole scene animating on an earlier project, twice, while every layout check passed |
| painted outside the stage | — |
| clipped text | *and later corrected* — it was firing on display type that overflows its content box with nothing clipping it, and two films had been loosened to satisfy a check that was simply wrong |
| outside the vertical safe box | the bottom 35% of a reel is platform chrome; the first layout sat under it |
| content over brand bar, footer or caption | chrome and content can both be inside the safe box while overlapping each other; a 906px beat in a 751px box passed everything |

Rects are measured **after** intersecting with clipping ancestors, because
what matters is where an element is painted, not where its box is.

## Still outstanding for PCI

1. **Create the code** as `OFFER-SPEC.md` specifies, and test it.
2. **Confirm `info@pciai.org` exists and is read.** It appears in all ten and
   in zero platform files today.
3. **Sign off the role mapping** in r2/v2 — which credential is aimed at whom.
   Nothing on screen claims an outcome, but the mapping is the films' own
   reading of the credential names and is not in the claims register.
4. **Decide about `25 country chapters` and `7 launch languages`.** Both are
   called substantiated in the repository README and neither appears anywhere
   in the platform, so both were left out. Point at the substantiation and
   each is one line of copy.
