# Narrator A/B — `eleven_v3`

Four candidates reading the same line, generated to let the Institute choose by
ear rather than from voice descriptions. **Awaiting a decision; none of these is
in a delivered film yet.**

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
new read — the timeline is derived from the audio, never hand-set. Roughly 45
minutes of render, and about **$0.54** to regenerate the explainer's narration.
The 75-second film (~1,230 credits) and the 15-second film (~173) would need the
same treatment if all three are to share one narrator.

All four voices are **stock library voices — none is a clone of any real person.**
