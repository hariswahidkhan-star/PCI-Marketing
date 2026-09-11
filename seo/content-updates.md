# SEO content updates — what to adopt, fix and reject

**Inputs reconciled:** the ChatGPT "PCI AI SEO Implementation Package" (README, manifest, 13 head
fragments, 7 content drafts, organisation JSON-LD, live-site observations, 10 Sep 2026); the
ChatGPT "Keyword and on-page plan" (22 generated routes); the repository audit in
`developer-changes.md`; and PCI's own claim rules from the Honorary Fellow register.

**Domains:** public website **pciai.org**; student portal **https://mypci.org/student**.

---

## 0. Read this first — the domain changed after the site was built

The website was built with projectcontrolsinstitute.org as its domain; PCI has since decided on
pciai.org for the public site and mypci.org/student for the portal. The repository's `main` still
carries the old domain in every canonical, in the sitemap generator's default host, in the redirect
module and in the database seeds. The package's live audit (10 Sep) recorded some pciai.org canonicals
on the live site, so the deployment may already carry partial changes that `main` does not; whoever
deploys should confirm which branch is live, and the migration in `developer-changes.md` Part A brings
the repository in line with the decision either way.

Nothing below has been applied. This is the editorial and technical plan.

---

## 1. Verdict on the two ChatGPT inputs

| Input | Verdict | Why |
|---|---|---|
| **Implementation package** (zip) | **Adopt, with the corrections in §2** | Built against the real pages, uses pciai.org, makes no accreditation, recognition or salary claims, and its live findings check out against the code (see §4). |
| **Keyword and on-page plan** (HTML, 22 routes) | **Reject as a structure; salvage three ideas** | It plans a different, fictional site: trailing-slash routes (`/certification/`, `/regions/`, `/insights/…`), a `/search/` page, and a `/pcp-ai/` "naming guide" for a credential name that never existed. Building it would create 22 duplicates of pages the site already has. Salvage: (a) the regional pages, which already exist, get the same treatment; (b) the "insights" article topics map one-to-one onto existing `blog-*.html` pages; (c) the internal-link anchors are good and can be reused on the existing pages. |

Do not create a PCP-AI page. The term was the other tool's own error; a page for it would rank PCI for
a mistake and confuse candidates.

---

## 2. Corrections to the package before use

- **Portal links.** The drafts link "Apply" to `https://mypci.org/student/register?product=exam&cert=PCL-AI`.
  The repository has no `/student/register` route (the React app registers at `/app/register`, the
  classic panel is `/student.html`). PCI says the portal is at `https://mypci.org/student`. **Verify the
  exact registration URL on the live portal** before any CTA is changed, and use one URL pattern
  everywhere.
- **Organisation JSON-LD.** The package's graph names the organisation "PCI AI" with the legal name as
  `legalName`, which is right, but it **drops `sameAs`, `contactPoint`, `foundingDate` and the
  `EducationalOrganization` type** that the site already declares. Keep those: the LinkedIn and X
  profiles are the site's own declared profiles, not unverified guesses. Merge, do not replace.
- **`/certifications` canonical.** The package proposes `/certifications.html`; the repository plan
  proposed honouring the page's own `/certifications`. Pick `.html` for consistency with the other
  210 pages, and make the bare `/certifications` a 301 to it. Update the sitemap entry to match.
- **About page wording.** The draft restates that PCI is "not currently accredited by a
  personnel-certification accreditation body". That sentence is true and already lives on
  `accreditation-status.html` and `founding-status.html`. PCI removed the same line from the film;
  the About page should link to the status pages rather than repeat the sentence. PCI's call.
- **Forecasting draft.** The package assumed `knowledge-forecasting.html` was thin. It is 1,605 words.
  Use the draft's EAC/ETC worked example as an addition, not a replacement.
- **Simulation-lab keywords** stay on hold, as the package itself says, until the application and
  learning-resource pages name the simulation lab publicly (the register's standing condition C5).

---

## 3. Final page metadata (merged)

Package titles are brand-first ("… | PCI AI"), which is the right pattern now that PCI AI is the
name being built. Where the package did not cover a page, the repository plan's value applies.

| Page | Title | Description | H1 |
|---|---|---|---|
| `/` | PCI AI \| Project Controls Institute | Explore PCI AI certifications from Project Controls Institute: PCL-AI, PFL-AI and PML-AI for project controls, finance and management. | PCI AI: Project Controls Institute |
| `/about.html` | About PCI AI \| Project Controls Institute | Learn about PCI AI, Project Controls Institute Global, Inc., its certification focus, professional standards and approach to responsible AI. | About PCI AI and the Project Controls Institute |
| `/certifications.html` | PCI AI Certifications \| PCL-AI, PFL-AI & PML-AI | Compare PCI AI certifications in project controls, project finance and project management. Explore PCL-AI, PFL-AI and PML-AI and their application routes. | PCI AI Certifications |
| `/certifications/pcl-ai` | Project Controls Certification: PCL-AI \| PCI AI | Explore PCL-AI project controls certification from PCI AI, covering planning, cost, forecasting, risk and responsible AI. Review the certification pathway. | PCL-AI Project Controls Certification |
| `/certifications/pfl-ai` | Project Finance Certification: PFL-AI \| PCI AI | Explore PFL-AI project finance certification from PCI AI, covering financial modelling, capital structure, bankability and responsible AI analysis. | PFL-AI Project Finance Certification |
| `/certifications/pml-ai` | Project Management Certification: PML-AI \| PCI AI | Explore PML-AI project management certification from PCI AI, with governance, leadership, project delivery and responsible use of artificial intelligence. | PML-AI Project Management Certification |
| `/ai-standard.html` | AI Governance for Project Controls \| PCI AI Standard | Explore the PCI AI standard for responsible project controls: validate AI forecasts, explain reporting outputs and retain professional accountability. | The PCI AI Standard for Responsible Project Controls |
| `/body-of-knowledge.html` | PCL-AI Body of Knowledge \| Project Controls \| PCI AI | Explore the PCL-AI Body of Knowledge, connecting project controls, finance, project management and responsible AI across thirteen domains. | keep current |
| `/curriculum.html` | PCL-AI Syllabus & Curriculum \| PCI AI | Review the PCL-AI syllabus across project accounting, finance, management and AI. Explore the knowledge areas and plan your preparation. | PCL-AI Syllabus and Curriculum (today: "Curriculum") |
| `/sample-questions.html` | PCL-AI Sample Questions & Explanations \| PCI AI | Try illustrative PCL-AI sample questions on scheduling, earned value, risk and governed AI, with answers and explanations for familiarisation. | keep current |
| `/insights.html` | Project Controls Guides & Insights \| PCI AI | Explore PCI AI guides to project controls, earned value, forecasting and responsible AI, with practical reading paths for professionals. | Project controls guides and insights (today: "Insights.") |
| `/blog.html` | Project Controls Blog \| PCI AI | Read articles from PCI AI on project controls practice, certification preparation, cost, scheduling and professional development. | keep current |
| `/project-controls-certification-saudi-arabia.html` | Project Controls Certification Saudi Arabia \| PCI AI | Explore PCI AI project controls certification for professionals in Saudi Arabia, with planning, cost control, forecasting and responsible AI. | Project controls certification in Saudi Arabia |
| `/project-controls-certification-uae.html` | Project Controls Certification UAE \| PCI AI | Explore PCI AI project controls certification for professionals in the UAE, with planning, cost control, forecasting and responsible AI. | Project controls certification in the UAE |
| `/project-controls-certification-uk.html` | Project Controls Certification UK \| PCI AI | Explore PCI AI project controls certification for professionals in the UK, with planning, cost control, forecasting and responsible AI. | Project controls certification in the UK |
| `/project-controls-certification-usa.html` | Project Controls Certification USA \| PCI AI | Explore PCI AI project controls certification for professionals in the USA, with planning, cost control, forecasting and responsible AI. | Project controls certification in the USA |
| the 20 pages in `developer-changes.md` Part F | as Part E/F | as Part F | keep current |

Apply the same title and description to `og:title`, `og:description` and the Twitter tags, and set
`og:site_name` to **PCI AI** sitewide. Values live in the file's `<head>` and, where an admin has
edited them, in the `pages` table; change both.

---

## 4. Findings in the package that check out in the code (fix these)

| Finding (package) | Verified in the repository | Fix |
|---|---|---|
| **P0** All three certification detail pages show "0 minutes" and "0% pass mark"; homepage and catalogue show 90 and 65. | `Core/Certs.cs:84-85` treats a per-certification override as present when the column is not C# `null`. A SQL NULL arrives as `DBNull` on at least one provider, so `H.D(DBNull)` becomes 0 and the global 90/65 is never used. | `var dur = c["duration_minutes"] is null or DBNull ? g.Duration : H.D(…)`; same for `pass_mark_pct`; also treat `<= 0` as "use global". Add a test. Then check the certifications rows themselves: a stored 0 must be NULL. |
| **P1** `/certification.html` (2,362 words, PCL-AI) and `/certifications/pcl-ai` (110 words) both describe PCL-AI and both self-canonicalise. | Both exist: the static page and the `CertPage` render from the `certifications` table. | Move the static page's substantive sections into the PCL-AI detail render (or the `certifications` row's long description), then 301 `/certification.html` → `/certifications/pcl-ai`. Check Search Console first; if the static URL has the history, invert the direction. |
| **P1** Main sitemap has 227 URLs including login and reset-password pages. | `Core/Sitemap.Xml` trusts `pages.noindex`, and nothing sets that flag from the file's `<meta name="robots" content="noindex">` at seed time (`PageContent.SeedFromFiles`). | At seed, set `noindex=1` when `RxRobotsNoindex` matches the file; also exclude any path where `Redirects.IsPrivatePath` or `PortalDomain.IsPortalPath` is true. |
| **P1** `/certifications` serves `certifications.html` whose canonical says `/certifications`. | Confirmed (`Program.cs:1933`). | Canonical `.html`; 301 the bare path. |
| **P1** Certification detail URLs are not in the sitemap. | Confirmed: `Sitemap.Xml` never reads the `certifications` table. | Add `SELECT slug, updated_at FROM certifications WHERE active=1`. |
| **P1** Homepage title "Project Controls Institute", H1 "The credential for the people who control projects." | Confirmed in `index.html`. | Title and H1 from §3; keep the strapline as the sub-heading. |
| **P1** Structured data: WebSite name is the legal name; alternateName only "PCI". | Confirmed in `index.html` JSON-LD. | Organisation `name` "PCI AI", `legalName` the legal name, `alternateName` ["Project Controls Institute", "PCI"]; WebSite `name` "PCI AI". Keep `EducationalOrganization`, `sameAs`, `contactPoint`, `foundingDate`. |
| **P1** Three homepage insight cards all link to `/insights.html`. | Confirmed: three `href="insights.html"` on `index.html`. | Link each card to the article its title promises (`blog-evm.html`, `blog-ai-project-controls.html`, `blog-what-is-project-controls.html`) or relabel. |
| **P2** Curriculum title is "Curriculum". | Confirmed. | §3. |
| **P2** Detail pages carry ~110 words. | Confirmed by the render: facts, routes and competencies only. | Add the package's credential copy (§5) plus the approved eligibility, fees, blueprint and renewal facts from the `certifications` row, never hard-coded. |
| **P2** Blog and Insights overlap. | `blog.html` "Blog & Insights"; `insights.html` "Insights". | Blog = dated articles (`/blog/…` and the `blog-*.html` set); Insights = the evergreen guides and reading paths. Retitle both (§3) and cross-link once. |

---

## 5. Content to adopt from the package (after fact review)

| Draft | Words | Destination | Notes |
|---|---|---|---|
| `home.md` | 304 | `index.html` intro and the three credential cards | Keeps the hero design; replaces the copy under the H1. Claims are all site-supported. |
| `about.md` | 273 | `about.html` opening | See §2 on the accreditation sentence. |
| `certifications.md` | 203 | `certifications.html` | Adds a "How to choose" section the page lacks. |
| `pcl-ai.md`, `pfl-ai.md`, `pml-ai.md` | ~290 each | `/certifications/{slug}` long description | Each links to eligibility, handbook, exam structure, sample questions, the AI standard, and the portal. Replace the portal URL per §2. The PML-AI draft correctly avoids re-using the PCL-AI blueprint. |
| `forecasting.md` | 900 | `knowledge-forecasting.html`, as an added section | EAC/ETC/VAC worked example with the sign convention stated. Merge, do not overwrite the existing 1,605 words. |

Every draft passes PCI's claim rules: no "accredited", no "recognised by", no salaries, no pass rates,
no member counts, "built to align with ISO/IEC 17024" wording only. Have a subject expert read the
worked examples before publication; the package says the same.

---

## 6. Existing articles to improve (from the package §6, mapped to real files)

| Page | Improvement | Next-step link |
|---|---|---|
| `blog-what-is-project-controls.html` | A sample monthly reporting workflow and role boundaries | PCL-AI |
| `blog-ai-project-controls.html` | One input-to-review workflow for an AI-assisted forecast, with limitations | AI standard, then PCL-AI |
| `blog-evm.html` | An original earned-value example, interpreted | Sample questions, then PCL-AI |
| `blog-pc-vs-pm.html` | Responsibilities with realistic decision examples | PCL-AI and PML-AI |
| `knowledge-forecasting.html` | The EAC/ETC section from `forecasting.md` | PCL-AI |
| `knowledge-finance.html` | How project-finance analysis relates to controls | PFL-AI |
| `blog-salary-guide.html` | **Source every figure or unpublish.** Salary numbers without a citation break PCI's own rule. | none until sourced |

Two per week after the technical fixes, as the package suggests.

---

## 7. Portal links and cross-domain measurement

- Every "Apply", "Sign in" and "Register" CTA on pciai.org points at `https://mypci.org/student…`.
  Confirm the exact registration path on the live portal, then use it identically on every page and in
  every email template. The repository's `PortalDomain.IsPortalPath` covers `/app` and `/student.html`
  only; if the live portal path is `/student`, add it there so the redirect and noindex logic apply.
- Set up cross-domain measurement (GA4 cross-domain linking for pciai.org and mypci.org) before
  reading any conversion figure; otherwise every application start looks like a new session on the
  portal and the marketing pages get no credit.
- No UTM on internal links between the two domains; UTM is for links PCI places off-site.

---

## 8. Order of work

1. Repository catch-up and the P0 exam-data bug (§0, §4 row 1).
2. Sitemap and canonical fixes (§4 rows 3 to 5), then the metadata in §3 for all pages.
3. Homepage: title, H1, intro copy, insight-card links, JSON-LD merge.
4. Credential pages: copy from §5, PCL-AI consolidation, portal CTA.
5. About, certifications hub, curriculum and insights retitles.
6. Article improvements at two per week (§6); salary guide sourced or unpublished first.
7. Regional pages: titles from §3; no new regional or city pages.

---

## 9. What was not done here

No live check was possible from this environment; the live findings above are the package's, verified
against the repository code rather than against pciai.org. No search volume or ranking data exists in
either input; the package and this document both say so. Nothing in either repository was changed.
