# PCI Honorary Fellowship tribute film — "Honoris Causa"

A prestige tribute presenting PCI's honorary distinction to a named recipient.
Reusable: the narration is split so only one short take is regenerated per person.

**Register.** Awards ceremony, not advertising. Obsidian black, champagne gold,
deep red. Restrained — the honour is dignified by understatement.

---

## The one correction that matters

The production brief specified a lower-third reading
`Honorary Fellow — Hon. FPCI`. **`Hon. FPCI` does not exist.** It returns zero
occurrences across the entire platform repository. `FPCI` is real but belongs to
the **membership Fellow** grade — an elected membership tier, not a board-conferred
honour — and the site keeps the two deliberately apart.

The designation this film may use is the one the platform actually issues:

```csharp
// backend/Endpoints/Honorary.cs
designation = "Honorary Fellow (PCI)"
```

This matters more here than in any other asset. A tribute film puts the
post-nominal under a real person's face, and that person will then use it — on a
CV, in a signature block, on a professional profile. Inventing one does lasting
damage to an individual, not just to the brand.

**There is also only one honorary tier.** "Honorary Member" and "Honorary
Advisor" appear on zero live pages. A `[TIER]` token with three options cannot be
filled; the film has one form.

---

## Narration

Split deliberately, so the film is reusable without re-recording the whole read.

### Part 1 — universal (generated once)

> Behind every great project stands a professional who chose to master it.
>
> Who planned when others guessed. Who forecast with honesty. Who held the line
> on integrity — even in the age of intelligent machines.
>
> Because technology can propose. But it takes a professional to decide.
>
> Today, the Project Controls Institute recognises one of those professionals.
>
> For a distinguished career, for advancing the discipline, and for elevating the
> standard of the profession —

### Part 2 — per recipient (regenerated for each conferral)

> — it is our honour to confer upon **[FULL NAME]** the distinction of
> **Honorary Fellow (PCI)**.
>
> **[FULL NAME]**. *Honoris causa.* A leader among those who control what matters.

The sentence break falls on the em dash, so the two parts join seamlessly.

**Voice.** `eleven_v3`, George — the same British narrative voice as
`../launch-15s/` and `../intro-60s/`. One voice across all three films is worth
more than the individually best voice for each.

**Direction.** Reverent, unhurried, never solemn to the point of funereal. A held
pause before the name. The name is said twice; the second time is quieter.

---

## On-screen typography

**On the brand system, not the brief's.** The brief asked for an elegant serif in
gold foil on obsidian. That would make this the one PCI film in a different
typeface, a different palette and without the mark — a second identity for the
ceremonial pieces. Instead the film uses the tokens the other two films use:

| | |
|---|---|
| Ground | `--ink #0F172A`, with the launch film's blue and crimson glow, grid and vignette |
| Lockup | PCI AI mark + wordmark, top-left on every shot, retiring under the end card |
| Eyebrow | Inter 600, `.19em`, uppercase, `#E4785F` (or `#7FA9E8`) |
| Rule | crimson → blue, the signature device |
| Headlines | Archivo 800, `-.023em`, white |
| Gold | **only in the seal**, and only the logo's own gradient `#F7EABC → #E7CB82 → #B8923E` |

The gold is not an invented accent: it is the mark's "AI" treatment. The seal
rings the actual logo in it, so the emblem of the honour *is* the brand mark.

| Moment | Type |
|---|---|
| Name reveal | **[FULL NAME]** in Archivo 800 / `HONORARY FELLOW (PCI)` as eyebrow |
| The seal | `PROJECT CONTROLS INSTITUTE` upper arc · `HONORIS CAUSA` lower arc · the mark at centre |
| Certificate | *Honorary Certificate* — see note below |
| End card | Mark · **PCI AI** · `HONORARY RECOGNITION` · *In recognition of a distinguished contribution to the profession.* · projectcontrolsinstitute.org |

**The certificate wording is not a style choice.** PCI's published honorary policy
requires it: *"Every honorary document, page, application, letter, certificate,
badge and verification record states 'Honorary Recognition' or 'Honorary
Certificate'."* A certificate prop reading anything else contradicts the
Institute's own rule.

---

## Why this film needs no status disclaimer

The brief is right about this. The film honours a **person's career and
contribution** and presents an honour the Institute confers at its own discretion.
It claims nothing about accreditation, examination or competence, so there is
nothing to qualify.

That holds only while the film says `Honorary Fellow (PCI)` and never implies the
examined credential. The published line is:

> An examined PCI credential — PCL-AI, PFL-AI or PML-AI — is always earned by
> passing the examination, on any route.

The tribute must not appear alongside credential imagery that blurs the two.

---

## Before this film is made for anyone

`[FULL NAME]` stays a token until the board has actually conferred the honour on
that person. A tribute film naming someone who has not been conferred is a
fabricated award attached to a real individual. The honorary route is
discretionary — *"PCI may decline any application without stating reasons"* — so
conferral is never assumable from an application.
