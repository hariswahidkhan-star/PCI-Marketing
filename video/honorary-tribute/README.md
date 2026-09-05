# PCI Honorary Fellowship tribute — "Honoris Causa"

A prestige tribute presenting PCI's honorary distinction to a named recipient.
Built to be reused: only one short narration take is regenerated per person.

| | |
|---|---|
| Duration | 48.000 s |
| Format | 1920×1080, 25 fps |
| Audio | −16.6 LUFS · narration, orchestral score, seal sound design |
| Palette | Obsidian `#08090C` · champagne gold `#C9A24B` · PCI crimson `#C13329` |

---

## Contents

| Path | What it is |
|---|---|
| `script.md` | Narration, typography, and the corrections made to the production brief |
| `src/scene.html` | The film — type and vector, deterministic in `t` |
| `src/render.mjs` | Frame renderer (Playwright + Chromium) |
| `vo/narration-take-1.mp3` | **Take used** — part one, universal, 33.41 s |
| `vo/narration-take-2.mp3` | Alternate, 35.79 s |
| `vo/score.mp3` | Prestige orchestral score, 48 s |
| `vo/sfx-seal.mp3` | Shimmer · resonant tone · foil glint, 8 s |
| `dist/honoris-causa-bed.wav` | The finished audio bed |
| `dist/pci-honoris-causa-1920x1080.mp4` | **The master** |

---

## Why type and vector, not generated footage

The production brief called for generated hero shots — a dignified silhouette, a
medallion, a certificate on marble. Two reasons this is drawn instead.

**Budget.** The shot list plus a 4K upscale exceeds both connector balances
several times over.

**Judgement.** Generated b-roll of "a distinguished professional" is exactly
where AI video looks cheapest, and a tribute is the worst place to look cheap.
Restrained typography on obsidian reads as more expensive, not less — and it
costs nothing to revise when a name changes.

The seal is drawn as SVG: concentric gold rings, the Institute's name on the
upper arc, `HONORIS CAUSA` on the lower, `PCI` at the centre over the crimson
rule. It stays sharp at any size and can be lifted straight out for print.

**Two things caught by looking at rendered frames rather than trusting the
markup.** The seal's lower arc initially rendered upside-down — a `textPath`
sweeping clockwise puts its glyphs inverted, so the arc had to run the other way.
And the end card first used the PCI AI app icon, which is blue and fought the
palette; tinting it with a CSS filter flattened its lettering into a solid gold
blob, so it became a compact version of the vector seal instead.

---

## Personalising

```bash
cd src && node render.mjs --name "Jane Smith" --out ../build/frames
```

Then regenerate **part two** of the narration for that recipient (the template is
in `script.md`), splice it into the bed at ~36 s, and re-encode. Part one, the
score and the sound design are unchanged for every recipient.

`[ RECIPIENT NAME ]` is deliberately visible in the master. It is a template, and
the placeholder makes that unmistakable — a tribute naming someone the board has
not conferred would be a fabricated award attached to a real person.

---

## Rebuilding

```bash
cd src && node render.mjs --w 1920 --h 1080 --fps 25 --out ../build/frames
ffmpeg -framerate 25 -i ../build/frames/%05d.png -i ../dist/honoris-causa-bed.wav \
  -map 0:v -map 1:a -t 48 -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p \
  -movflags +faststart -c:a aac -b:a 192k ../dist/pci-honoris-causa-1920x1080.mp4
```

Fully reproducible: `scene.html` computes every style from `t`, including the
drifting motes, which use a seeded generator rather than randomness.
