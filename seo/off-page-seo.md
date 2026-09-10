# Off-page SEO programme — Project Controls Institute

Everything in this document happens **outside** the website: profiles, listings, links,
mentions, syndication, video and social. Nothing here edits a page on the site. Where an
off-page step needs a matching on-page change (the `sameAs` list, an embed), it is marked
**hand-off** and left for the site team.

Built from the site's own declared entity data (`index.html` JSON-LD, 10 Sep 2026) so that
every external profile says exactly what the site says. Where a fact could not be verified
from this environment (no open-web access), it is marked **verify**.

---

## 0. Ground rules that override everything below

**One canonical domain.** The website is **pciai.org**. The codebase still declares
`projectcontrolsinstitute.org` as canonical in every tag, sitemap and schema entry, and the developer
change list (`developer-changes.md`, Part A) moves that to pciai.org. **Every external link, profile
URL and citation points at `https://pciai.org/`** from day one, and projectcontrolsinstitute.org is kept
attached only as a 301 to it. Do not create any listing on the old domain.

**Never claim, anywhere off-site:**

- "accredited", "ANAB", "IAS", or "ISO/IEC 17024 certified". The site says the framework is
  *built to align with* ISO/IEC 17024. That is the only permitted wording.
- "501(c)(3)" as a fact. The site says *pursuing 501(c)(3) recognition, not yet granted*.
- "recognised by", "endorsed by", "approved by" any government, employer or body.
- Salaries, pass rates, member counts, or any number the site does not publish.
- "Honorary certification". The honorary route is **Honorary Fellow (PCI)**, a recognition.
- "PCP-AI". It does not exist. The credentials are **PCL-AI, PFL-AI and PML-AI**.

**Never buy links, join link schemes, or use private blog networks.** Paid placements (a
sponsored newsletter, a paid directory) are fine only with `rel="sponsored"` and are not
counted as link-building.

**British spelling** in every profile and post, matching the site.

---

## 1. Entity baseline — the one record every profile copies

| Field | Value (from the site's schema) |
|---|---|
| Legal name | Project Controls Institute Global, Inc. |
| Display name | Project Controls Institute |
| Short name / brand | PCI · PCI AI |
| Canonical URL | https://pciai.org/ |
| Legacy domain | projectcontrolsinstitute.org, to 301 to pciai.org (see developer change list, Part A) |
| Entity type | Independent certifying body; Delaware Non-Stock Corporation; registered nonprofit pursuing 501(c)(3) recognition (not yet granted) |
| Founded | 2025 |
| Country | United States (no street address is published; do not invent one) |
| General email | hello@projectcontrolsinstitute.org (mail domain is a separate decision; see developer change list, A3) |
| Members / honorary enquiries | Members@pciai.org |
| Careers | careers@pciai.org (**verify** mailbox exists before publishing) |
| Slogan | AI proposes. The professional disposes. |
| Credentials | PCI AI Project Controls Leader (PCL-AI) · PCI AI Project Finance Leader (PFL-AI) · PCI Project Management Leader – AI (PML-AI) · Honorary Fellow (PCI) |
| Existing profiles | LinkedIn: linkedin.com/company/project-control-institute · X: x.com/projectcontrolinstitute |
| Logo | https://pciai.org/assets/logo.png (use the same file everywhere) |

### Boilerplates (copy verbatim; do not paraphrase per platform)

**One line (≤160 chars)**
Independent certifying body for project controls, cost engineering and project finance, with governed AI throughout. Awards PCL-AI, PFL-AI and PML-AI.

**Short (about 50 words)**
The Project Controls Institute is an independent certifying body for the integrated discipline of project controls, cost engineering and project finance, with the governed use of AI treated as part of the discipline. It awards the PCI AI Project Leadership Certification Suite: PCL-AI, PFL-AI and PML-AI. AI proposes; the professional disposes.

**Long (about 100 words)**
Project Controls Institute Global, Inc. is an independent certifying body, a Delaware Non-Stock Corporation and a registered nonprofit pursuing 501(c)(3) recognition, founded in 2025 for the integrated discipline of project controls, cost engineering and project finance. Its published Body of Knowledge sets thirteen domains and sixty-one knowledge areas, and its examined credentials — PCL-AI, PFL-AI and PML-AI — are built to align with ISO/IEC 17024. The Institute's Human Oversight Policy requires a competent professional to govern AI at every consequential step: AI proposes, the professional disposes. Separately, the Board confers Honorary Fellow (PCI) on practitioners of distinguished contribution. Every credential is entered on a public registry, checkable at source.

---

## 2. Owned profiles — the `sameAs` set

These are the profiles search engines use to confirm the entity. Create or complete each
one with the §1 record, the same logo, the same one-line boilerplate, and the canonical URL.
Then **hand-off:** add every new profile URL to the `sameAs` array in the site's organisation
schema, so the site and the profiles vouch for each other.

| Profile | Status | Notes |
|---|---|---|
| LinkedIn company page | Exists | Complete: tagline = slogan; About = long boilerplate; website = canonical; add the three credentials as Products; post the Honorary Fellow film natively. |
| X | Exists | Bio = one-liner; link = canonical; pin the film. |
| YouTube channel | Create | Channel name "Project Controls Institute"; handle `@projectcontrolsinstitute`; About = long boilerplate; link = canonical. Upload the films (§6). |
| Crunchbase | Create | Organisation profile; founded 2025; nonprofit; website = canonical. Free tier is enough. |
| Wikidata item | Create | An *item*, not a Wikipedia article (no notability case yet). Instance of: certification body; official website; inception 2025; country US; LinkedIn/X IDs. This is what knowledge panels read. |
| GitHub organisation | Optional | Only if PCI publishes anything open (the Body of Knowledge index, a badge verifier). An empty org is worse than none. |
| Google Business Profile / Bing Places | Hold | Require a real, verifiable address. The site publishes none. Do not create one with a registered-agent address. |
| Facebook / Instagram | Optional | Only if someone will post monthly. A dead profile with the wrong boilerplate is a negative signal. |

---

## 3. Registries and directories — citations

Consistency matters more than volume. Ten listings that agree beat fifty that drift.

| Listing | Priority | Prerequisite | Note |
|---|---|---|---|
| Delaware Division of Corporations entity record | Automatic | — | Already exists as the legal record; nothing to do but keep the name identical everywhere. |
| Dun & Bradstreet D-U-N-S | High | Legal name + address | Free; underpins many other registries. |
| Candid (GuideStar) nonprofit profile | High, when eligible | IRS determination | **Verify** eligibility: listing depends on IRS recognition. Prepare the profile text now; submit when granted. |
| Crunchbase | High | — | Also serves as a `sameAs` profile (§2). |
| Better Business Bureau | Low | — | Only if PCI wants to answer complaints there; otherwise skip. |
| Course / certification aggregators (Class Central, CourseTalk and similar) | Medium | — | **Verify** each accepts certification bodies rather than courses. List the three credentials with the site's own descriptions; link to `certifications.html`. |
| Planning Planet and project-controls community directories | Medium | — | Community listing plus a member profile for the founders. Engagement, not link-dropping. |
| Professional-body and association aggregators | Medium | — | **Verify** each entry; never accept a category that implies accreditation. |

Track every listing in `listings.csv` beside this file: platform, URL, date, who owns the
login, and whether the boilerplate matches §1. Re-check the whole list quarterly.

---

## 4. Links that PCI controls — partners

The highest-yield links available to a founding-stage institute are the ones its own
partners give it. They are also the most defensible: relevant, editorial, and earned.

- **Training partners** (`training-partners.html`, `become-a-training-partner.html`). Every
  approved partner gets a "PCI Training Partner" badge image plus a snippet that links to
  their listing on the partners page. Their site links to PCI; PCI links back. Make the badge
  part of the partner agreement, not a request afterwards.
- **University partnerships** (`university-partnerships.html`). A `.edu` link is the
  strongest single link PCI can earn. Ask each partner for a mention on their industry-
  partners or professional-development page, linking to the canonical URL, with the
  boilerplate unchanged.
- **Certuvo** (`certuvo.html`, the official preparation platform). Reciprocal links between
  the two sites are legitimate: they are genuinely related. Keep anchors branded
  ("Project Controls Institute", "PCI"), not keyword-stuffed.
- **Honorary Fellows.** When the Board confers the first recognitions, each Fellow gets a
  registry link to share. Those go on personal sites, LinkedIn and employer bios naturally.
  Never ask a Fellow to link as a condition of recognition.
- **Employers on `why-employers.html`.** An employer that recognises PCL-AI in a job
  description or a competency framework is a mention worth a link; ask for one after they
  have used it, not before.

---

## 5. Digital PR — assets that earn links without asking twice

PCI cannot cite statistics it does not have, so its link assets are **positions and
reference material**, which a founding-stage body can own honestly.

| Asset | Why it earns links | Where to pitch |
|---|---|---|
| **The Body of Knowledge** (13 domains, 61 knowledge areas) | A citable, structured reference for a discipline that lacks one in the AI era. Reference material earns the most durable links. | Planning Planet, PM World Journal, university course reading lists, LinkedIn newsletters in project controls |
| **The Human Oversight Policy** ("AI proposes. The professional disposes.") | A quotable position on AI in engineering practice, at a moment when every trade publication is writing about it. | Construction and engineering trade press (ENR, Construction Dive, New Civil Engineer, Infrastructure Intelligence), AI-governance newsletters |
| **PMP vs AACE vs PCL-AI** (`pmp-vs-aace-vs-pcl-ai.html`) | Comparison pages are searched for and linked to by people choosing. Keep it scrupulously fair to the other bodies. | Career forums, Reddit r/projectmanagement and r/civilengineering (as an answer, not a drop), careers advisers |
| **Honorary Fellow (PCI) film** | A four-minute, factual explanation of a recognition route. Video is shareable where text is not. | LinkedIn native, YouTube, partner newsletters |
| **Founding-stage milestones** | First cohort examined; first Honorary Fellows conferred; first university partner; IRS determination when granted. Each is a genuine announcement. | Trade press briefs, LinkedIn, partner channels |
| **Salary guide** (`blog-salary-guide.html`) | Salary content attracts links, **but only if every figure is sourced**. **Verify** the page cites its sources before using it as a link asset; if it does not, do not pitch it. | Careers sites, recruiters' blogs |

**Pitch format.** One paragraph, one link, one asset, from a named person. No press-release
attachments. Offer the founder for comment on AI-in-project-controls stories; that is the
route into trade press for an organisation with no news of its own yet.

**Expert-quote services** (Qwoted, Featured, Help a B2B Writer and similar). Register the
founder and one senior examiner as sources on project controls, cost engineering, EVM and AI
governance. Each accepted quote is a relevant editorial link. Answer only what the person
actually knows.

---

## 6. Video — the films as off-page assets

The site's backend already serves `feed.xml`, `atom.xml`, `feed.json`, `blog-sitemap.xml`
and `news-sitemap.xml`, so syndication is a matter of pointing platforms at them.

- **YouTube.** Upload the Honorary Fellow film (1080 captioned cut, 3:50). Title: "Honorary
  Fellow (PCI) — a recognition conferred by the Board". Description: the YouTube copy in
  `video/honorary-fellow/share-kit.md`, which already carries the chapters and the legal
  line. First link in the description is the canonical honorary route page. Add the 4K
  master later as the definitive upload. Upload the 75-second institutional film and the
  15-second launch film as well.
- **LinkedIn.** Upload natively (not a YouTube link); native video is shown to more people.
  Use the LinkedIn post from the share kit.
- **Vimeo.** Optional mirror for embedding on partner sites without YouTube branding.
- **Hand-off:** embed the film on `route-honorary.html` with `VideoObject` schema pointing at
  the YouTube URL, so the page and the video reinforce each other.

---

## 7. Syndication — the content the site already publishes

- Submit `feed.xml` to Feedly, Flipboard and Inoreader as a publication.
- Republish selected blog articles on **LinkedIn Articles** and **Medium** with the
  canonical link back to the original (Medium's import tool sets `rel=canonical`
  automatically; on LinkedIn, state "First published at pciai.org" with
  the link in the first paragraph).
- Offer the "What is project controls" and "EVM explained" articles to Planning Planet and
  PM World Journal as contributed pieces, with the canonical link in the author line.
- A monthly LinkedIn newsletter from the company page, built from the month's blog posts and
  one registry or policy update. Newsletters compound; posts do not.

---

## 8. Reviews and reputation

- Ask real candidates for a review **after** results are released, never before, and never
  with an incentive. Point them to the reviews page and to LinkedIn recommendations of the
  company page.
- Trustpilot and Google reviews only once there is an address (Google) or a steady flow of
  candidates (Trustpilot). An empty profile with one review looks worse than none.
- Monitor and answer every review, including critical ones, in the same plain register the
  site uses.

---

## 9. Social launch pack

Hashtags belong here and nowhere in page metadata. One reusable set:

`#ProjectControls #ProjectControlsInstitute #PCIAI #PCLAI #CostEngineering #ProjectFinance #EarnedValue #AIinEngineering #GovernedAI`

Use four to six per post, always including `#ProjectControls` and `#ProjectControlsInstitute`.

**LinkedIn (company page, Honorary Fellow film)**

> Some careers deliver projects. Others leave behind a standard, a method, and the people who carry it forward.
>
> Honorary Fellow (PCI) is conferred by the Board of the Project Controls Institute on practitioners of distinguished contribution. No examination: the record is the evidence, and the Board weighs it, individually and at its own discretion.
>
> No nomination, assessment or credential fee. No sponsor required. If recognised, your name is entered on PCI's own public registry, checkable at source.
>
> Meeting the criteria does not guarantee recognition. That is what makes it worth having.
>
> The honorary route: https://pciai.org/route-honorary.html
>
> #ProjectControls #ProjectControlsInstitute #PCIAI #CostEngineering #ProjectFinance

**LinkedIn (company page, certification suite)**

> AI proposes. The professional disposes.
>
> The Project Controls Institute's Human Oversight Policy requires a competent professional to govern AI at every consequential step. Its examined credentials are built on that principle: PCL-AI for project controls, PFL-AI for project finance, PML-AI for project management, each built to align with ISO/IEC 17024, each entered on a public registry.
>
> The Body of Knowledge: thirteen domains, sixty-one knowledge areas, published in full.
>
> https://pciai.org/certifications.html
>
> #ProjectControls #ProjectControlsInstitute #PCLAI #GovernedAI #EarnedValue

**X (thread opener)**

> Honorary Fellow (PCI): conferred by the Board, no examination, no fee, no sponsor. Your record is the evidence. Meeting the criteria does not guarantee recognition. Film and the honorary route: https://pciai.org/route-honorary.html #ProjectControls #ProjectControlsInstitute

**Instagram (square cut, caption)**

> If your work outlasted the projects, let it be recognised. Honorary Fellow (PCI) is conferred by the Board on the record alone. No exam. No fee. Link in bio.
> #ProjectControls #ProjectControlsInstitute #PCIAI #CostEngineering #ProjectFinance #EarnedValue

Every post carries, in a comment or the last line where space allows: *Honorary Fellow (PCI)
is a discretionary, board-conferred recognition involving no examination. It is not an
examined certification, licence or accreditation. Meeting the eligibility criteria or
submitting an application does not guarantee recognition.*

---

## 10. Anchor text and link hygiene

- **Brand anchors first.** "Project Controls Institute", "PCI", "the Institute". Keyword
  anchors ("project controls certification") only where the linking sentence naturally says
  it. A link profile that is mostly exact-match keywords is the pattern search engines
  penalise.
- **Deep links over homepage links.** Point the honorary route, the certifications page, the
  Body of Knowledge and the policy pages at their own URLs.
- **Mark paid placements** `rel="sponsored"`; user-generated placements are fine `nofollow`.
  A nofollow mention from a relevant site is still worth having.
- **UTM tags on links PCI places itself** (`utm_source=linkedin&utm_medium=social&utm_campaign=honorary-fellow`), never on links others give.
- **Do not disavow** unless Search Console shows a manual action. Random low-quality links
  are ignored, not penalised.

---

## 11. Monitoring — how PCI knows it is working

Set up once, check monthly:

- **Google Search Console** and **Bing Webmaster Tools**: the Links report (referring
  domains, top linked pages, anchor text) and brand-query impressions for "Project Controls
  Institute", "PCI AI", "PCL-AI", "Honorary Fellow PCI".
- **Google Alerts** for: "Project Controls Institute", "PCL-AI", "PFL-AI", "PML-AI",
  "Honorary Fellow (PCI)", "projectcontrolsinstitute.org". Every unlinked mention is a link
  request waiting to be sent.
- **Profile audit**: the `listings.csv` checklist, re-verified quarterly against §1.

Monthly one-page report: referring domains (count and new this month), brand-query
impressions, unlinked mentions found and converted, profiles complete out of total, and one
sentence on what shipped.

---

## 12. Ninety-day sequence

This is a sequence because each stage depends on the one before it.

1. **Weeks 1–2 — entity.** Decide the domain (§0). Complete LinkedIn and X to the §1
   record. Create YouTube, Crunchbase and Wikidata. Hand off the `sameAs` update.
2. **Weeks 3–4 — controlled links.** Partner badge and snippet issued to every training and
   university partner. D-U-N-S registered. Candid profile drafted for submission when eligible.
3. **Weeks 5–8 — assets and outreach.** Films live on YouTube and LinkedIn. Body of Knowledge
   and Human Oversight Policy pitched to the trade titles in §5. Founder registered on
   expert-quote services.
4. **Weeks 9–12 — syndication and reviews.** Feed submitted; first LinkedIn newsletter;
   first two articles republished with canonicals; review requests to the first cohort
   after results.
5. **Ongoing.** Monthly report (§11); quarterly listings re-check; one announcement per
   real milestone, never a manufactured one.

---

## 13. What was not done here, and why

- No account was created, no post was published, and no email was sent. Each of those is an
  external action that needs PCI's explicit go-ahead.
- No live search-demand or competitor research: this environment has no open-web access.
  The keyword targets named in §5 and §11 come from the site's own page set, not from
  measured search volume. Run the demand check in Search Console or a keyword tool before
  spending outreach time on any one asset.
- Nothing on the site was changed. The two on-page hand-offs (the `sameAs` array, the video
  embed) are listed so the site team can pick them up.
