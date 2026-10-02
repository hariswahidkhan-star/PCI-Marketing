# Narrator A/B — `eleven_v3`

Four candidates reading the same line, generated to let the Institute choose by
ear rather than from voice descriptions.

> **Decision taken: A — Jim Executive on `eleven_v3`.** It is the narrator in the
> delivered explainer. This was the standing recommendation below, and it keeps
> one voice across all three films. The other three samples are kept because the
> comparison is the evidence for the choice, and because reversing it is a
> re-generation, not a re-edit.

## Why this test exists

Two problems with the narration as first delivered:

1. **The voice pool was searched badly.** A bare `creative_list_voices` call
   returned three voices, and the narrator was chosen from those three. Searching
   properly returns **22**.
2. **The model had no emotional direction.** The films use
   `eleven_multilingual_v2`. **`eleven_v3` is the emotion-capable model** — it
   accepts inline audio-direction tags, and per its prompting guide also responds
   to ellipses (longer, thoughtful pauses), em-dashes (short beats) and sparing
   capitals (emphasis).

All four samples use the same directed text, so the comparison is voice-only:

> Its position on that adoption is explicit. It certifies professionals who
> GOVERN A-I — not who defer to it… The future of project delivery will not be
> defined by technology alone.

## The candidates

| File | Voice | `voice_id` | Character | Length |
|---|---|---|---|---|
| `A-Jim-Executive-british-CURRENT.mp3` | Jim Executive | `tXxkePQsw0G69D8VeDzp` | British, C-suite calm; corporate and investor narration. **The current narrator** — so A also shows what v3 alone adds over v2 | 13.68 s |
| `B-Connery-documentary.mp3` | Connery | `vLZJLcQMJCqxjrHGEVDO` | American, deep cinematic documentary gravitas | 14.56 s |
| `C-Leo-broadcast.mp3` | Leo | `cOHUo8FosWk7BqQhx8nk` | American, four decades broadcast; built to hold long-form | 14.72 s |
| `D-Cameron-cinematic.mp3` | Cameron | `NOpwXiXLWfbN5KhzBTFW` | South African, smooth and rich; luxury and high-trust | 12.56 s |

Cost: 716 credits (~$0.13), one take each (`generations_count: 1`).

## Recommendation

**A on `eleven_v3`.** British reads as institutional for a global standards body,
and it keeps continuity with the two films already delivered. **C** is the
strongest alternative if an American broadcast warmth is preferred.

**More emotion is not automatically better here.** The brief requires the films
not to feel like an exaggerated sales advert, and a certification body's
credibility rests on restraint. v3 is used for warmth and conviction, not drama.

## What changing the voice costs

Switching model or voice re-times the narration, so the picture is re-cut to the
new read — the timeline is derived from the audio, never hand-set.

**What the v3 move actually cost on the explainer:** 16 takes, ~3,300 credits
(about **$0.60**), and the film lengthened from 233.14 s to 256.24 s because the
v3 read is slower and better phrased. No picture was re-cut by hand.

**Still on `eleven_multilingual_v2`:** the 75-second film and the 15-second launch
cut. Both already use *this same voice* — Jim Executive — so all three films share
one narrator today; only the model differs, which affects phrasing and emphasis
rather than who is speaking. Re-recording them on v3 would cost roughly **1,230**
and **173** credits respectively (about $0.26 together) plus a re-render, and the
75-second film would need its conform re-derived because it is cut to an exact
75.00 s. **That spend has not been made**, since it consumes paid credits on
films that are already delivered and signed off.

All four voices are **stock library voices — none is a clone of any real person.**
