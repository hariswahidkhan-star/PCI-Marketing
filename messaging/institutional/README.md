# Institutional messaging

Approved institutional copy, and the evidence behind it. This directory is the
source every asset in this repository draws institutional claims from, so that a
film, a deck and a landing page make the same statements about PCI in the same
words.

| File | Covers |
|---|---|
| `overview.md` | What PCI is, the credential suite, eligibility, assessment, honest status, PCI World |
| `honorary-routes.md` | Honorary Fellow (PCI) — the one honorary designation |
| `founding-routes.md` | The founding route — one route, one designation |

Each file has the same three parts: the **approved copy**, a **what must not be
said** table giving the reason for each prohibition, and a **claims audit** tracing
every retained claim to a live page or the code that enforces it — the form used
by `video/launch-15s/script.md`.

## How this was built

Copy was reconciled against the shipped platform,
[`hariswahidkhan-star/PCI`](https://github.com/hariswahidkhan-star/PCI), not
against memory or a deck. Where a draft claim had no live source it was removed
rather than softened, and the removal is recorded in the claims audit with a ❌ so
the next person does not reintroduce it.

Three prohibitions carry more weight than the rest, because the site does not
merely omit these claims — it publishes commitments that contradict them:

- **No firm dates.** `founding-status.html`: *"we will not publish firm dates we
  cannot stand behind."*
- **No overstated presence.** `chapters.html`: *"Chapters are in formation; PCI
  does not overstate local presence."*
- **No claim beyond the accreditation page.** `accreditation-status.html`: *"If
  wording anywhere else ever appears to say more than this page does, this page
  prevails."*

## Open — reconcile before the next asset ships

Reconciling this copy surfaced claims used elsewhere in **this repository** that
have no live source on the platform. They are recorded here rather than changed,
because the existing film's claims audit sources them to the launch deck, which is
not in either repository — someone with the deck needs to decide which is right.

| Claim | Used in | Live site |
|---|---|---|
| 25 country chapters | root `README.md`; `video/launch-15s/` shot 3, on screen | Number unpublished; 23 listed; presence actively disclaimed |
| 7 launch languages | root `README.md` | No language count published anywhere |
| Launched 1 September 2026 | root `README.md`; `video/launch-15s/` shot 1, on screen as `NOW LIVE · 1 SEPTEMBER 2026` | No launch date published; firm dates explicitly refused |
| Credential expansion for PCL-AI | — | Homepage and `certifications.html` disagree with each other |

The film is built and committed with those claims on screen. Nothing here changes
it. If the deck cannot substantiate them, shots 1 and 3 need a re-cut, and the
root README's brand-facts table needs the same correction.
