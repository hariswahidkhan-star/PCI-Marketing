# PCI-Marketing

Marketing assets for the **Project Controls Institute Global, Inc.** — the
brand-facing work that sits alongside the platform itself.

The platform lives in [`hariswahidkhan-star/PCI`](https://github.com/hariswahidkhan-star/PCI)
(ASP.NET Core 8 backend, React apps, the 235-page public site, PCI World). This
repository holds the campaign and content assets that point at it. Nothing here
deploys; nothing here is a second copy of the site.

---

## Contents

| Path | What it is |
|---|---|
| `video/launch-15s/` | 15-second post-launch film — sources, script, captions and built masters |

---

## Brand facts these assets are built on

Kept here so every asset in this repository is checked against the same set
rather than against memory.

**Identity.** Project Controls Institute Global, Inc. — a Delaware Non-Stock
Corporation. It **intends to seek** 501(c)(3) recognition; tax-exempt status has
**not** been granted. Platform launched **1 September 2026**.

**Governing principle.** *"AI proposes. The professional disposes."*

**Credentials.** Three, as one suite:

| | |
|---|---|
| **PCL-AI** | PCI AI Project Controls Leader — the flagship |
| **PFL-AI** | PCI AI Project Finance Leader |
| **PML-AI** | PCI Project Management Leader – AI |

**Substantiated numbers.** 13-domain body of knowledge · 25 country chapters ·
7 launch languages · 3 credentials · every credential publicly verifiable at
`/verify.html`.

**Domains.** `projectcontrolsinstitute.org` (hub) · `pciai.org` · `pciglobal.ai` ·
`pciworld.org` · `credentialfinder.org`

**Design system** — taken from `backend/wwwroot/assets/styles.css` in the platform
repo, not re-invented here:

| Token | Value | Use |
|---|---|---|
| `--ink` | `#0F172A` | the navy ground |
| `--crimson` | `#C13329` | eyebrow labels, rule left stop |
| `--magenta` | `#3B82F6` | accent, rule right stop |
| `--blue` | `#1D4ED8` | primary action |
| display | **Archivo** 800, `-0.023em` | headlines |
| text | **Inter** 400/600 | everything else |

The signature device is the crimson→blue rule under an uppercase, letter-spaced
eyebrow. It appears on the site, in the launch deck, and in the film.

---

## The editorial rule

**PCI would rather understate than oversell.** This is not a style preference —
for a certification body, trust is the entire product, and the Institute publishes
its own limits on its own site.

Every asset in this repository must therefore:

- **Never** claim accreditation. PCI is **not** accredited by ANAB, IAS, or any
  ISO/IEC 17024 body. The permitted phrasing is "developed with reference to
  ISO/IEC 17024 principles" and "building toward formal accreditation".
- **Never** imply tax-exempt status has been granted.
- **Never** promise jobs, salaries, or third-party recognition.
- **Never** use fabricated social proof — no invented member counts, testimonials,
  percentiles, or partner logos.
- Cite third-party statistics **as published, with the source named on screen**.
- Distinguish an examined credential from **Honorary Fellow (PCI)**, which is
  board-conferred, always labelled honorary, and never the examined certification.
- Keep PCI World described as **educational practice** — challenges do not grant
  or affect any certification, membership or credential.

Each asset directory carries its own claims audit tracing every factual statement
to the launch deck or a live page. See `video/launch-15s/script.md` for the
worked example.

---

## Building

Each asset directory is self-contained and documents its own build. For the film:

```bash
cd video/launch-15s/src && ./build.sh
```

Requires Node 18+, Python 3.10+, ffmpeg with libx264/aac, and a Chromium that
Playwright can drive.
