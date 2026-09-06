# PCI AI film — re-voiced with Holden

The user's 75-second PCI AI film, re-voiced with the ElevenLabs **Holden Pro
Voice** and carrying the brand lockup on every frame.

| | |
|---|---|
| Source | `source/original.mov` — 1280×720, 24 fps, 75.0 s, mono voice-over-music |
| Master | `dist/pci-holden-1280x720.mp4` — 78.2 s, −15.8 LUFS |
| Voice | Holden Pro Voice (`UudLhsL2DlHkDK0vGwl3`), `eleven_multilingual_v2`, nine segments |
| Score | `eleven_music_v2`, 76 s instrumental, sidechain-ducked under the voice |
| Overlay | `src/overlay.html` — PCI AI mark · PROJECT CONTROLS INSTITUTE · pciai.org |

## What was done, and why it took the shape it did

**The old voice could not be separated from its music.** The source audio is
effectively mono — a centre-cancel leaves −62.7 dB across the whole band, so
there is no stereo image to exploit. The old track is therefore dropped entirely
(it is never mapped into the output) and a new score goes under the new voice.

**The picture is captioned.** Every narration line is burned in as subtitles, so
the new voice has to land on the caption windows or the words on screen stop
matching the words being said. Scribe transcribed the old read (it also revealed
an uncaptioned spoken ident at the top and an uncaptioned "Discover PCI AI at
pciai.org…" at the end). Caption windows were recovered from scene changes in the
caption band of the picture. The nine Holden segments were then scheduled to
those windows — `vo/schedule.json`.

**Pace.** Holden reads at ~155 wpm; the original ran a brisk ~184. Nine natural
takes total 87.6 s against a 75 s picture. A uniform `atempo=1.18` restores the
original pace, which is what puts the captions back in the same relationship to
the voice they had before. Two segments needed more: the second line is 22 words
inside a 5-second caption window (x1.28, and it still spills ~2 s into the next),
and the closing line needs the end card held for three extra seconds (x1.30).
The hold is a clone of the last frame and is invisible.

**Pronunciation.** The old read ran "PCI AI" and "PCL-AI" together as letters —
Scribe heard "PCII" and "PCLI". The new script spells them out (`P C I, A I`),
and the web addresses are spoken as `P C I A I dot org`.

**Lockup placement.** The source already has eyebrow chips top-centre, captions
along the bottom, and a small PCI badge top-right on later shots. The lockup sits
top-left *below* the chip band (y≈8.6% of frame), with a soft local ground behind
it so it holds on the sunlit skylines, and never touches any of the three.

## Rebuild

```bash
cd src && node render-overlay.mjs --w 1280 --h 720 --fps 24 --dur 78.21 --out ../build/overlay
```
then the mix and composite commands recorded in the session. The schedule is
data, not code: change `vo/schedule.json` to re-time a segment.
