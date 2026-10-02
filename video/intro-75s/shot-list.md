# Shot list — PCI AI 75-second institutional film

Every shot is generated from `src/scene.html`. There is no camera, no stock
plate and no AI-generated imagery in the delivered masters — the "shot" is a
composed frame whose every property is a function of time.

| # | Dur | Elements (selector) | Reveal cue (s after shot in) | Stagger |
|---|---|---|---|---|
| S1 | 8.50 | `.eyebrow` | 0.20 | — |
| | | `.uline` (wipes, scaleX) | 0.36 | — |
| | | `h1 .w` × 3 words | 0.50 | 0.085 |
| | | `.sub` | 1.55 | — |
| S2 | 8.10 | `.eyebrow` | 0.16 | — |
| | | `.pill` × 5 | 0.36 | 0.115 |
| | | `.sub` | 1.30 | — |
| S3 | 10.30 | `.eyebrow` | 0.16 | — |
| | | `.cap4` × 4 | 0.38 | 0.135 |
| | | `h2 .w` × 6 words | 1.35 | 0.080 |
| S4 | 9.40 | `.eyebrow` | 0.16 | — |
| | | `h2 .w` × 4 words | 0.34 | 0.095 |
| | | `.req` × 5 | 1.10 | 0.125 |
| S5 | 11.10 | `#mark` (scales 0.88→1.00) | 0.16 | — |
| | | `.wordmark` | 0.40 | — |
| | | `.uline` | 0.66 | — |
| | | `.sub` | 0.90 | — |
| S6 | 10.20 | `.eyebrow` | 0.16 | — |
| | | `.chip` × 3 | 0.36 | 0.165 |
| | | `.status` (accreditation line) | 1.35 | — |
| | | sheen sweep across chips | 48.60 → 50.00 abs | — |
| S7 | 13.20 | `.eyebrow` | 0.18 | — |
| | | `h2 .w` × 6 words | 0.40 | 0.105 |
| | | `.uline` | 1.65 | — |
| | | **palette inversion to light** | 57.60 → 58.02 abs | — |
| S8 | 4.20 | `#mark8` | 0.14 | — |
| | | `.wordmark` | 0.34 | — |
| | | `.url` (both domains) | 0.60 | — |
| | | `.legal` | 0.86 | — |

**Reveal mechanic.** Each element eases in over 0.66 s on `outExpo`, rising
1.15 em. The rule (`.uline`) wipes horizontally instead of rising. The two
marks scale rather than slide.

**Stills pulled from the render**

| Still | Frame | Why |
|---|---|---|
| Poster | 41.0 s (`01230`) | The identity shot — mark, wordmark and the competence line |
| Thumbnail | 65.0 s (`01950`) | The light closing statement. Highest contrast in the film and the most legible at small size, with no clickbait |

Both are taken from the **clean** (caption-free) 16:9 render.
