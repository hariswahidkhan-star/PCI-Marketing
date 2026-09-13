# Pronunciation reference

PCI's note on the v2 cut was *"Also pronunciation is not correct"* without
naming the word. Rather than guess and re-record blind, this take reads the
three candidates aloud so the right one can simply be pointed at.

`certuvo-pronunciation-options.mp3` — 27 s, the same narrator (Nassim,
`repzAAjoKlgcT2oOAIWt`) that reads the film, eight readings with a beat between
each:

| # | Reading | Note |
|---|---|---|
| 1 | Certuvo — as spelled | what the v2 cut used |
| 2 | Ser-TOO-vo | **what the current cut uses** |
| 3 | Sir-tuh-vo | |
| 4 | Cher-TOO-vo | |
| 5 | "En-clex", RN and PN | **what the current cut uses** |
| 6 | N-C-L-E-X, RN and PN | what the v2 cut used |
| 7 | "See-suh" | |
| 8 | C-I-S-A | **what the current cut uses** |

## What changing it costs

Caption text and spoken text are separate fields in `src/vo.py`, so a
pronunciation is changed by editing the *spoken* string only — the caption
orthography stays correct either way. But the audio has to be re-generated.

- **Brand name (readings 1–4).** Said in **s4, s9 and s11**. s4 and s9 are
  narration only and are cheap to redo. **s11 is on camera**, so it needs a new
  narration take *and* a new HeyGen presenter clip at roughly **$165**. That is
  the only expensive consequence in the whole change, and it needs approval
  before it is spent.
- **NCLEX (readings 5–6).** Said in **s3** only. Narration only, cheap.
- **CISA (readings 7–8).** Said in **s3** only. Narration only, cheap.

So: if the word PCI meant was NCLEX or CISA, the fix is a few cents. If it was
the brand, it is $165 and an approval.
