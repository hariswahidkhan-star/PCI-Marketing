# Music bed — the homepage film's own

`certuvo-home-bed.mp3` — a 170-second instrumental underscore generated with
**ElevenLabs Music v2** (`eleven_music_v2`, generation `2DCV03LU122ZScJk9Qgj`,
session `Nv8TCLKkskscvFRZTDIt`, on flow `Hqx2MhTarzYeLbv0a55u`) for **this** film
specifically.

It replaces a 145-second first version, generated when the film ran 2:17. The
reworked film runs 2:42, and a bed shorter than the film does not fail loudly:
`atrim` stops early and the close plays dry. `src/build-serial.sh` now refuses
to build in that case.

## Why this film does not share `../music`

The shared bed in `../certuvo-cma/music` was written for the 4:35 CMA film. Its
build is deliberately even: measured second by second, it spans about 7 dB from
its quietest passage to its loudest, and the lift it does have arrives around
three minutes — after this film has already ended. Under a 2:17 film it is a
flat carpet.

This bed was prompted to the shape of the eleven beats instead, and measures
about **19 dB** of range:

| Passage | Level | Under |
|---|---|---|
| 0–20 s | ≈ −27 dB, near-bare felt piano | the intimate open, "It's late" |
| 20–55 s | rising | the open loop and the credential wall |
| 55–100 s | ≈ −16 dB, pulse, pads and strings | the partnership, the bank, the Forge |
| 100–125 s | rising | the Coach and the study room |
| 125–150 s | ≈ −13.4 dB, the peak | readiness, the price, the close |
| 150–162 s | resolving to solo piano | the presenter's last lines and the end card |

Major key, 92 BPM, no vocals, 1–4 kHz kept sparse by prompt so the narration
sits on top. **Confirmed instrumental**: the generation reported
`Instrumental: False` (the flag was not set), so it was transcribed with
`eleven_scribe_v1` — the transcript came back empty, at 0.12 language
probability. There is no sung or spoken word in it.

## How it is mixed

`src/build-serial.sh` trims it to the film's exact length, fades in over two
seconds and out over the last four, dips it 3 dB around 1.8 kHz, drops it to
`BED=0.42` and side-chains it under the voice, then normalises the whole mix to
−14 LUFS / −1.5 dBTP.

Measured on the finished mix, in the 300 Hz – 4 kHz voice band, second by second
wherever the narration is present: **18 dB median margin** of voice over music.
The only seconds where the bed comes forward are the gaps between scenes and the
pause before the final line — which is what the bed is there for.

## Licence

Generated in the workspace's own ElevenLabs account under its plan. It is not a
stock library track and carries no third-party credit line.
