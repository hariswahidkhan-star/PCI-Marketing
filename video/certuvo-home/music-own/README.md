# Music bed — the homepage film's own

`certuvo-home-bed.mp3` — a 145-second instrumental underscore generated with
**ElevenLabs Music v2** (`eleven_music_v2`, generation `Nr26MykKWrFPl7C47jTH`,
session `pETNmQ6tzqAcn1yl8h1a`, on flow `Hqx2MhTarzYeLbv0a55u`) for **this** film
specifically.

## Why this film does not share `../music`

The shared bed in `../certuvo-cma/music` was written for the 4:35 CMA film. Its
build is deliberately even: measured second by second, it spans about 7 dB from
its quietest passage to its loudest, and the lift it does have arrives around
three minutes — after this film has already ended. Under a 2:17 film it is a
flat carpet.

This bed was prompted to the shape of the eleven beats instead, and measures
about **18 dB** of range:

| Passage | Level | Under |
|---|---|---|
| 0–20 s | ≈ −32 dB, near-bare felt piano | the intimate open, "It's late" |
| 20–90 s | ≈ −16 dB, pulse and pads enter | the credentials, the partnership, the features |
| 90–110 s | rising | the AI features and the study rooms |
| 110–130 s | ≈ −14 dB, the peak | the price and the close |
| 130–137 s | resolving warm | the end card |

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
wherever the narration is present: **21 dB median margin** of voice over music.
The only seconds where the bed comes forward are the gaps between scenes and the
pause before the final line — which is what the bed is there for.

## Licence

Generated in the workspace's own ElevenLabs account under its plan. It is not a
stock library track and carries no third-party credit line.
