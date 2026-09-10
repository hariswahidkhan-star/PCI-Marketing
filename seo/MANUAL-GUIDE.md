# PCI AI SEO manual guide

**Live facts this guide is written against.** Public website: **https://pciai.org** (live). Student
portal: **https://mypci.org/student** (live; login surface, never indexed). Legacy domain:
projectcontrolsinstitute.org, which must 301 to pciai.org page-for-page. Prepared 10 September 2026 from
the site's own source (235 pages), the backend's SEO generators, the ChatGPT SEO package's live audit,
and PCI's claim rules. Companion files sit beside this guide in `PCI-Marketing/seo/`:
`site-files/sitemap.xml`, `sitemap-index.xml`, `robots.txt`, `llms.txt`, `pages-metadata.sql`,
`metadata.json`, and `scripts/apply-domain.sh`, `scripts/apply-metadata.py`. Exact code diffs are in
`IMPLEMENTATION-GUIDE.md`; the prompt for Claude is `CLAUDE-PROMPT.md`.

Everything below can be done by hand from this document alone. Nothing here has been applied.

---

## 1. Rules that override everything

- Never write "accredited", "ANAB", "IAS" or "ISO/IEC 17024 certified". The only permitted wording is "built to align with ISO/IEC 17024".
- Never state 501(c)(3) as a fact. The site's wording is "pursuing 501(c)(3) recognition, not yet granted".
- Never write "recognised by", "endorsed by" or "approved by" any government, employer or body.
- No salaries, pass rates, member counts or any number the site does not already publish.
- The honorary route is "Honorary Fellow (PCI)", a recognition. Never "honorary certification".
- There is no "PCP-AI". The credentials are PCL-AI, PFL-AI and PML-AI (plus the AIPC specialist certificate). Never create a page for PCP-AI.
- British spelling throughout. One primary keyword per page, used once in the title, once in the H1 and once in the first 100 words, never stuffed.

---

## 2. Domain and hosting settings (do first, in one deploy)

The backend already generates `/sitemap.xml`, `/sitemap-index.xml`, `/robots.txt` and `/llms.txt`
from one host setting, and 301-redirects known alternate hosts. Set:

| Variable | Value |
|---|---|
| `CANONICAL_HOST` | `pciai.org` |
| `REDIRECT_HOSTS` | `projectcontrolsinstitute.org,www.projectcontrolsinstitute.org` |
| `APP_BASE_URL` | `https://pciai.org` |
| `ALLOWED_ORIGIN` | `https://pciai.org` |
| `SITE_BASE_URL` | `https://pciai.org` |
| `PORTAL_BASE_URL` | `https://mypci.org` |
| `PORTAL_HOSTS` | `www.mypci.org` |

Attach pciai.org, www.pciai.org, projectcontrolsinstitute.org and www.projectcontrolsinstitute.org to
the same service with TLS. Keep the old domain for at least twelve months. In Plausible, add
`pciai.org` as a site before the deploy; every page's analytics tag changes to
`data-domain="pciai.org"`.

If the repository's `main` still says `projectcontrolsinstitute.org` while the live site already
says `pciai.org`, the live code is newer than `main`: merge the deployed source into `main` before
changing anything, or the next deploy reverts the live domain.

---

## 3. Keyword map

One primary keyword per page. Search volumes are not measured; priorities are editorial, from the
package's 63-term map and PCI's own targets. Confirm against Search Console after four weeks.

| Priority | Keyword group | Page |
|---|---|---|
| P1 | PCI AI, PCIai, PCI AI institute, Project Controls Institute, Project Controls Institute Global (Inc), PCI project controls | `/` |
| P1 | PCI AI certifications, PCI certifications, PCI AI certification courses | `/certifications.html` |
| P1 | project controls certification, PCL-AI, PCL-AI certification, project controls leader certification, online project controls certification | `/certifications/pcl-ai` |
| P1 | project finance certification, PFL-AI, PFL-AI certification, AI project finance certification | `/certifications/pfl-ai` |
| P1 | AI project management certification, PML-AI, PML-AI certification, project management leader certification | `/certifications/pml-ai` |
| P1 | Honorary Fellow PCI, PCI honorary fellow application | `/route-honorary.html`, `/honorary-application.html` |
| P2 | PCI AI standard, AI governance project controls, responsible AI project controls | `/ai-standard.html` |
| P2 | human oversight AI policy | `/human-oversight.html` |
| P2 | PCL-AI body of knowledge, project controls body of knowledge | `/body-of-knowledge.html` |
| P2 | PCL-AI syllabus, PCL-AI curriculum | `/curriculum.html` |
| P2 | PCL-AI sample questions | `/sample-questions.html` |
| P2 | what is project controls, project controls meaning | `/blog-what-is-project-controls.html` |
| P2 | project controls vs project management | `/blog-pc-vs-pm.html` |
| P2 | earned value management explained, CPI and SPI explained | `/blog-evm.html` |
| P2 | AI in project controls, AI project forecasting | `/blog-ai-project-controls.html` |
| P2 | project cost forecasting, estimate at completion | `/knowledge-forecasting.html` |
| P2 | PMP vs AACE vs PCL-AI | `/pmp-vs-aace-vs-pcl-ai.html` |
| P2 | project controls certification Saudi Arabia / Riyadh, UAE / Dubai, UK, USA | the four `/project-controls-certification-*.html` pages |
| P2 | verify PCI credential | `/verify.html` |
| P3 | PCI, PCI institute, PCI certification (ambiguous acronym) | `/` only; measure before investing |
| Hold | project controls simulation lab | no page until the lab is publicly described |

Never create spelling-variant pages ("Project Control Institute"), city clones, or a PCP-AI page.

---

## 4. On-page tags for every targeted page

Apply the title to `<title>`, `og:title` and `twitter:title`; the description to
`<meta name="description">`, `og:description` and `twitter:description`; the canonical to
`<link rel="canonical">` and `og:url`. Set `og:site_name` to **PCI AI** on every page. Titles are at
most 60 characters, descriptions at most 155. "Keep current" means the existing value already meets
the rules.

**The database overrides the files.** The `pages` table is seeded with titles and descriptions and the
server injects them over the file. Change both: the file, and the row (`site-files/pages-metadata.sql`
contains every UPDATE below, plus the `certifications` rows for the three detail pages). Then put the
same values in the `schema.sql` seed rows so a fresh install agrees.

| URL | Primary keyword | Title (≤60) | Meta description (≤155) | H1 | Canonical |
|---|---|---|---|---|---|
| `/` | PCI AI | PCI AI \| Project Controls Institute | Explore PCI AI certifications from Project Controls Institute: PCL-AI, PFL-AI and PML-AI for project controls, finance and management. | PCI AI: Project Controls Institute | `https://pciai.org/` |
| `/about.html` | Project Controls Institute | About PCI AI \| Project Controls Institute | Learn about PCI AI, Project Controls Institute Global, Inc., its certification focus, professional standards and approach to responsible AI. | About PCI AI and the Project Controls Institute | `https://pciai.org/about.html` |
| `/certifications.html` | PCI AI certifications | PCI AI Certifications \| PCL-AI, PFL-AI & PML-AI | Compare PCI AI certifications in project controls, project finance and project management. Explore PCL-AI, PFL-AI and PML-AI and their application routes. | PCI AI Certifications | `https://pciai.org/certifications.html` |
| `/certifications/pcl-ai` | project controls certification | Project Controls Certification: PCL-AI \| PCI AI | Explore PCL-AI project controls certification from PCI AI, covering planning, cost, forecasting, risk and responsible AI. Review the certification pathway. | PCL-AI Project Controls Certification | `https://pciai.org/certifications/pcl-ai` |
| `/certifications/pfl-ai` | project finance certification | Project Finance Certification: PFL-AI \| PCI AI | Explore PFL-AI project finance certification from PCI AI, covering financial modelling, capital structure, bankability and responsible AI analysis. | PFL-AI Project Finance Certification | `https://pciai.org/certifications/pfl-ai` |
| `/certifications/pml-ai` | AI project management certification | Project Management Certification: PML-AI \| PCI AI | Explore PML-AI project management certification from PCI AI, with governance, leadership, project delivery and responsible use of artificial intelligence. | PML-AI Project Management Certification | `https://pciai.org/certifications/pml-ai` |
| `/ai-standard.html` | AI governance project controls | AI Governance for Project Controls \| PCI AI Standard | Explore the PCI AI standard for responsible project controls: validate AI forecasts, explain reporting outputs and retain professional accountability. | The PCI AI Standard for Responsible Project Controls | `https://pciai.org/ai-standard.html` |
| `/body-of-knowledge.html` | PCL-AI body of knowledge | PCL-AI Body of Knowledge \| Project Controls \| PCI AI | Explore the PCL-AI Body of Knowledge, connecting project controls, finance, project management and responsible AI across thirteen domains. | keep current | `https://pciai.org/body-of-knowledge.html` |
| `/curriculum.html` | PCL-AI syllabus | PCL-AI Syllabus & Curriculum \| PCI AI | Review the PCL-AI syllabus across project accounting, finance, management and AI. Explore the knowledge areas and plan your preparation. | PCL-AI Syllabus and Curriculum | `https://pciai.org/curriculum.html` |
| `/sample-questions.html` | PCL-AI sample questions | PCL-AI Sample Questions & Explanations \| PCI AI | Try illustrative PCL-AI sample questions on scheduling, earned value, risk and governed AI, with answers and explanations for familiarisation. | keep current | `https://pciai.org/sample-questions.html` |
| `/insights.html` | project controls guides | Project Controls Guides & Insights \| PCI AI | Explore PCI AI guides to project controls, earned value, forecasting and responsible AI, with practical reading paths for professionals. | Project controls guides and insights | `https://pciai.org/insights.html` |
| `/blog.html` | project controls blog | Project Controls Blog \| PCI AI | Read articles from PCI AI on project controls practice, certification preparation, cost, scheduling and professional development. | keep current | `https://pciai.org/blog.html` |
| `/project-controls-certification-saudi-arabia.html` | project controls certification Saudi Arabia | Project Controls Certification Saudi Arabia \| PCI AI | Explore PCI AI project controls certification for professionals in Saudi Arabia, with planning, cost control, forecasting and responsible AI. | Project controls certification in Saudi Arabia | `https://pciai.org/project-controls-certification-saudi-arabia.html` |
| `/project-controls-certification-uae.html` | project controls certification UAE | Project Controls Certification UAE \| PCI AI | Explore PCI AI project controls certification for professionals in the UAE, with planning, cost control, forecasting and responsible AI. | Project controls certification in the UAE | `https://pciai.org/project-controls-certification-uae.html` |
| `/project-controls-certification-uk.html` | project controls certification UK | Project Controls Certification UK \| PCI AI | Explore PCI AI project controls certification for professionals in the UK, with planning, cost control, forecasting and responsible AI. | Project controls certification in the UK | `https://pciai.org/project-controls-certification-uk.html` |
| `/project-controls-certification-usa.html` | project controls certification USA | Project Controls Certification USA \| PCI AI | Explore PCI AI project controls certification for professionals in the USA, with planning, cost control, forecasting and responsible AI. | Project controls certification in the USA | `https://pciai.org/project-controls-certification-usa.html` |
| `/donate.html` | donate Project Controls Institute | Donate to the Project Controls Institute \| PCI | keep current | keep current | `https://pciai.org/donate.html` |
| `/downloads-centre.html` | PCI policies downloads | Downloads Centre: Policies and Legal Documents \| PCI | Every PCI policy, guideline and legal document in one place: enrolment, payment, examination, membership, conduct and governance, as PDF downloads. | keep current | `https://pciai.org/downloads-centre.html` |
| `/honorary-application.html` | Honorary Fellow PCI application | Honorary Fellow (PCI) Application \| PCI | Apply for the Board's consideration to be conferred Honorary Fellow (PCI), a recognition of distinguished contribution separate from examined credentials. | keep current | `https://pciai.org/honorary-application.html` |
| `/become-a-training-partner.html` | become a PCI training partner | keep current | Apply to become a recognised PCI Training Partner for PCL-AI exam preparation. The examination and the certification decision stay independent of training. | keep current | `https://pciai.org/become-a-training-partner.html` |
| `/course-outline.html` | PCL-AI course outline | keep current | The complete PCL-AI study outline: thirteen domains and 61 knowledge areas, weighted 40/40/20 across finance, project management and governed AI. | keep current | `https://pciai.org/course-outline.html` |
| `/directory.html` | PCI member directory | keep current | Search the PCI member directory for certified project controls professionals by name, country and certification. Listings are consented and verifiable. | keep current | `https://pciai.org/directory.html` |
| `/downloads.html` | PCI guidelines | keep current | PCI's candidate guidelines and policies: enrolment, payment, examination, membership and conduct, plus the emails you receive at each step. | keep current | `https://pciai.org/downloads-centre.html` |
| `/forum.html` | project controls forum | keep current | The PCI community forum, open to everyone: project controls, exam preparation, the Body of Knowledge, AI in project controls and careers, worldwide. | keep current | `https://pciai.org/forum.html` |
| `/founding-status.html` | PCI founding status | keep current | An honest account of what the Project Controls Institute has established and what is still in development, including its accreditation roadmap. | keep current | `https://pciai.org/founding-status.html` |
| `/leadership.html` | PCI leadership and governance | keep current | How the Project Controls Institute is governed, who makes certification decisions, and the open call for founding examiners and subject-matter experts. | keep current | `https://pciai.org/leadership.html` |
| `/reviews.html` | PCI reviews | keep current | Reviews and testimonials from Project Controls Institute members and students on the PCI certification programmes, moderated and published unedited. | keep current | `https://pciai.org/reviews.html` |
| `/route-founding.html` | PCI founding route | keep current | The founding route: an invitation-only founding cohort with membership, study and exam access. The credential is still earned by passing the examination. | keep current | `https://pciai.org/route-founding.html` |
| `/route-honorary.html` | Honorary Fellow PCI | keep current | The honorary route: apply for the Board's consideration to be conferred Honorary Fellow (PCI), a recognition of distinguished contribution, no examination. | keep current | `https://pciai.org/route-honorary.html` |
| `/sector-aero.html` | project controls aerospace defence | keep current | Project controls for aerospace and defence: aircraft, spacecraft, defence platforms and advanced technologies, with governed AI and the PCI certifications. | keep current | `https://pciai.org/sector-aero.html` |
| `/training-partners.html` | PCI training partner | keep current | Find a recognised PCI Training Partner for PCL-AI exam preparation. Partners prepare candidates; the exam and certification decision stay independent. | keep current | `https://pciai.org/training-partners.html` |
| `/university-partnerships.html` | PCI university partnerships | keep current | Connect academic programmes to the project controls standard: curriculum alignment, a student pathway to PCI certifications and research collaboration. | keep current | `https://pciai.org/university-partnerships.html` |
| `/why-employers.html` | PCI certification for employers | keep current | Why EPC contractors, owners, energy, defence, aerospace and government value PCI certifications: planning, cost, forecasting, risk and AI governance. | keep current | `https://pciai.org/why-employers.html` |
| `/route-standard.html` | PCL-AI standard route | Standard Route to PCL-AI Certification \| PCI AI | The standard route to PCL-AI: create a free account on the student portal, activate membership, book the examination and earn the credential. | keep current | `https://pciai.org/route-standard.html` |
| `/blog-evm.html` | earned value management explained | Earned Value Management Explained: EV, CPI, SPI \| PCI AI | Earned value management explained: how EV, PV and AC combine into CPI, SPI and a defensible forecast, with a worked example from PCI AI. | keep current | `https://pciai.org/blog-evm.html` |
| `/blog-ai-project-controls.html` | AI in project controls | AI in Project Controls: What Changes, What Doesn't \| PCI AI | AI in project controls: where it improves forecasting, reporting and risk, where a professional must still decide, and how PCI AI governs it. | keep current | `https://pciai.org/blog-ai-project-controls.html` |
| `/blog-pc-vs-pm.html` | project controls vs project management | Project Controls vs Project Management \| PCI AI | Project controls vs project management: who owns which decisions, how the roles work together on a real delay, and which career path fits you. | keep current | `https://pciai.org/blog-pc-vs-pm.html` |
| `/blog-what-is-project-controls.html` | what is project controls | What Is Project Controls? A Practical Guide \| PCI AI | What is project controls? Scope, schedule, cost, risk and forecasting working together, with a monthly reporting example and where AI fits, from PCI AI. | keep current | `https://pciai.org/blog-what-is-project-controls.html` |
| `/knowledge-forecasting.html` | project cost forecasting | Project Cost Forecasting: EAC and ETC Explained \| PCI AI | Project cost forecasting explained: estimate at completion, estimate to complete and variance at completion, with a worked example and review checks. | Project cost forecasting: EAC and ETC | `https://pciai.org/knowledge-forecasting.html` |
| `/contact.html` | contact PCI AI | Contact PCI AI \| Membership, Certification and Careers | Contact PCI AI: Members@pciai.org for membership and Honorary Fellow (PCI) enquiries, careers@pciai.org for careers, and general questions by email. | keep current | `https://pciai.org/contact.html` |
| `/verify.html` | verify PCI credential | Verify a PCI Credential \| Public Registry \| PCI AI | Verify a PCI AI credential at source: confirm a professional's PCL-AI, PFL-AI, PML-AI or Honorary Fellow (PCI) status on the Institute's public registry. | keep current | `https://pciai.org/verify.html` |
| `/human-oversight.html` | human oversight AI policy | Human Oversight Policy for AI \| PCI AI | PCI AI's Human Oversight Policy: a competent professional governs AI at every consequential step. AI proposes; the professional disposes. | keep current | `https://pciai.org/human-oversight.html` |
| `/membership-fellow.html` | PCI Fellow membership | Fellow Membership \| Project Controls Institute \| PCI AI | Fellow membership, the Institute's most senior grade, recognising distinguished contribution to the project controls profession: benefits and how to apply. | keep current | `https://pciai.org/membership-fellow.html` |
| `/eligibility-requirements.html` | PCL-AI eligibility | PCL-AI Eligibility Requirements \| PCI AI | keep current | keep current | `https://pciai.org/eligibility-requirements.html` |
| `/exam-structure.html` | PCL-AI exam structure | PCL-AI Exam Structure and Blueprint \| PCI AI | keep current | keep current | `https://pciai.org/exam-structure.html` |
| `/handbook.html` | PCL-AI candidate handbook | PCL-AI Candidate Handbook \| PCI AI | keep current | keep current | `https://pciai.org/handbook.html` |
| `/pmp-vs-aace-vs-pcl-ai.html` | PMP vs AACE vs PCL-AI | PMP vs AACE vs PCL-AI: Compare Scope and Purpose \| PCI AI | PMP vs AACE credentials vs PCL-AI, compared by scope, role and evidence, without assuming equivalence or recognition. A positioning guide from PCI AI. | keep current | `https://pciai.org/pmp-vs-aace-vs-pcl-ai.html` |
| `/knowledge-finance.html` | project finance for project controls | Project Finance for Project Controls \| PCI AI | How major projects are funded and why project controls must speak the language of project finance: structures, bankability, coverage ratios, PFL-AI. | keep current | `https://pciai.org/knowledge-finance.html` |

Five pages currently declare the **wrong canonical** and are therefore not being indexed:
`route-honorary.html`, `route-standard.html`, `route-founding.html` and `honorary-application.html`
point at `contact.html`; `downloads-centre.html` points at `downloads.html`. Set each to itself as in
the table, and point `downloads.html` at `downloads-centre.html`.

Robots meta stays `index, follow, max-image-preview:large` on every page in the table. These pages
are `noindex` and must stay out of the sitemap: login, forgot/reset-password, the student pages,
enrol/enroll, checkout, payment-success/failed, exam-ui, admin-chat, platform-preview, partner,
index-launcher, coming-soon, 404, and the three template shells `blog-shell.html`,
`careers-detail.html`, `certification-detail.html`.

---

## 5. Structured data

**Homepage organisation graph.** Replace the first `application/ld+json` block on `index.html` with
this graph. It keeps everything the site already declares (type, profiles, founding date, slogan)
and changes only the names, adds the legal name, the two published contact addresses and the two
missing credentials. Remove the old `SearchAction`: the site search is a client-side overlay and
`?q=` performs no search.

```json
{"@context": "https://schema.org", "@graph": [
 {"@type": ["EducationalOrganization", "Organization"], "@id": "https://pciai.org/#organization",
  "name": "PCI AI", "legalName": "Project Controls Institute Global, Inc.",
  "alternateName": ["Project Controls Institute", "PCI"],
  "url": "https://pciai.org/", "logo": "https://pciai.org/assets/logo.png",
  "slogan": "AI proposes. The professional disposes.",
  "description": "An independent certifying body (a Delaware Non-Stock Corporation and a registered nonprofit organisation pursuing 501(c)(3) tax-exempt recognition, not yet granted) for the integrated discipline of project controls, cost engineering and project finance, with governed AI throughout. Awards the PCI AI Project Leadership Certification Suite: PCI AI Project Controls Leader (PCL-AI), PCI AI Project Finance Leader (PFL-AI) and PCI Project Management Leader – AI (PML-AI).",
  "foundingDate": "2025", "areaServed": "Worldwide",
  "address": {"@type": "PostalAddress", "addressCountry": "US"},
  "email": "hello@projectcontrolsinstitute.org",
  "contactPoint": [
   {"@type": "ContactPoint", "contactType": "customer support", "email": "hello@projectcontrolsinstitute.org", "availableLanguage": ["English"]},
   {"@type": "ContactPoint", "contactType": "membership", "email": "Members@pciai.org", "availableLanguage": ["English"]},
   {"@type": "ContactPoint", "contactType": "careers", "email": "careers@pciai.org", "availableLanguage": ["English"]}],
  "sameAs": ["https://www.linkedin.com/company/project-control-institute", "https://x.com/projectcontrolinstitute"],
  "knowsAbout": ["Project controls", "Cost engineering", "Project finance", "Earned value management", "Forecasting", "Project risk", "Governed artificial intelligence"]},
 {"@type": "WebSite", "@id": "https://pciai.org/#website", "url": "https://pciai.org/",
  "name": "PCI AI", "alternateName": "Project Controls Institute", "inLanguage": "en-GB",
  "publisher": {"@id": "https://pciai.org/#organization"}},
 {"@type": "EducationalOccupationalCredential", "@id": "https://pciai.org/#pcl-ai",
  "name": "PCI AI Project Controls Leader (PCL-AI)", "url": "https://pciai.org/certifications/pcl-ai",
  "description": "The integrated project-controls credential: planning, cost engineering, earned value, forecasting, risk and project finance with the governed use of AI. Built to align with ISO/IEC 17024.",
  "credentialCategory": "Professional certification", "recognizedBy": {"@id": "https://pciai.org/#organization"}, "inLanguage": "en-GB"},
 {"@type": "EducationalOccupationalCredential", "@id": "https://pciai.org/#pfl-ai",
  "name": "PCI AI Project Finance Leader (PFL-AI)", "url": "https://pciai.org/certifications/pfl-ai",
  "description": "Project finance, financial modelling, capital structure, bankability, coverage ratios, PPP and concession structures, financial close and AI-enabled analysis. Built to align with ISO/IEC 17024.",
  "credentialCategory": "Professional certification", "recognizedBy": {"@id": "https://pciai.org/#organization"}, "inLanguage": "en-GB"},
 {"@type": "EducationalOccupationalCredential", "@id": "https://pciai.org/#pml-ai",
  "name": "PCI Project Management Leader – AI (PML-AI)", "url": "https://pciai.org/certifications/pml-ai",
  "description": "Project management, leadership and delivery: governance, planning, execution, agile and hybrid delivery and AI-enabled project management. Built to align with ISO/IEC 17024.",
  "credentialCategory": "Professional certification", "recognizedBy": {"@id": "https://pciai.org/#organization"}, "inLanguage": "en-GB"}
]}
```

**Every marketing page:** one `BreadcrumbList`, generated once in the content injector rather than
pasted into 200 files. Shape:

```json
{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
 {"@type": "ListItem", "position": 1, "name": "PCI AI", "item": "https://pciai.org/"},
 {"@type": "ListItem", "position": 2, "name": "Certifications", "item": "https://pciai.org/certifications.html"},
 {"@type": "ListItem", "position": 3, "name": "PCL-AI", "item": "https://pciai.org/certifications/pcl-ai"}]}
```

**Pages with no structured data today** (`certifications.html`, `careers.html`, `directory.html`,
`badge.html`, `reviews.html`): add `BreadcrumbList` and `WebPage`. On `certifications.html` add an
`ItemList` whose items are the three credential `@id`s above plus the AIPC certificate on
`ai-cert.html`. **Never** add `AggregateRating` to `reviews.html` unless the value and count are
computed from real moderated reviews at render time.

**Honorary route page,** once the film is on YouTube:

```json
{"@context": "https://schema.org", "@type": "VideoObject",
 "name": "Honorary Fellow (PCI): a recognition conferred by the Board",
 "description": "Honorary Fellow (PCI) is a discretionary, board-conferred recognition involving no examination. It is not an examined certification, licence or accreditation. Meeting the eligibility criteria or submitting an application does not guarantee recognition.",
 "thumbnailUrl": "https://pciai.org/assets/honorary-fellow-thumbnail.jpg",
 "uploadDate": "YYYY-MM-DD", "duration": "PT3M50S",
 "contentUrl": "https://www.youtube.com/watch?v=VIDEO_ID", "embedUrl": "https://www.youtube.com/embed/VIDEO_ID",
 "publisher": {"@id": "https://pciai.org/#organization"}}
```

---

## 6. Sitemap, robots.txt and llms.txt

The live files are generated by the backend from `CANONICAL_HOST`. The static files in
`site-files/` are the wwwroot fallbacks and the review copies; drop them into `backend/wwwroot/`.

**Sitemap rules the generator must follow** (see `IMPLEMENTATION-GUIDE.md` §6 for the code):

- Host `https://pciai.org`; `index.html` listed as `/`; every other page as `/slug.html`.
- Include only `pages` rows with `published=1` and `noindex` not set, minus `student.html`,
  `admin.html`, `exam-ui.html`, `404.html`, `500.html`, `offline.html`, the three template shells and
  `downloads.html`; never a path that is private (`/admin`, `/app`, `/api`, student pages) or a
  portal path (`/student`, `/student.html`, `/reset-password.html`).
- Honour `pages.canonical_url` when set, so a page never appears under a URL that canonicalises elsewhere.
- Add `/certifications/pcl-ai`, `/pfl-ai`, `/pml-ai` from the `certifications` table (`active=1`).
- Published blog posts, news posts and open job postings stay, as today.
- `/certifications` (bare) becomes a 301 to `/certifications.html`; `/certification.html` (the old
  PCL-AI page) becomes a 301 to `/certifications/pcl-ai` after its content is moved (§8).
- On the portal host (mypci.org): `/sitemap.xml`, `/sitemap-index.xml` answer 404; `/robots.txt`
  answers `User-agent: *` / `Disallow: /`. The portal already sends `X-Robots-Tag: noindex, nofollow`.

The reference `site-files/sitemap.xml` lists all 211 indexable static pages with priorities (1.0
home; 0.9 certifications, routes, honorary, Body of Knowledge, comparison, employers, partners; 0.5
legal; 0.8 otherwise).

**Sitemap index** (`https://pciai.org/sitemap-index.xml`), submitted to Search Console and Bing:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://pciai.org/sitemap.xml</loc></sitemap>
  <sitemap><loc>https://pciai.org/blog-sitemap.xml</loc></sitemap>
  <sitemap><loc>https://pciai.org/news-sitemap.xml</loc></sitemap>
  <sitemap><loc>https://pciai.org/world-sitemap.xml</loc></sitemap>
</sitemapindex>
```

**robots.txt** (`https://pciai.org/robots.txt`):

```
User-agent: *
Allow: /

# Private / authenticated surfaces — kept out of search and AI indexes. Defence in
# depth: also protected by authentication, noindex meta tags and an X-Robots-Tag header.
Disallow: /admin
Disallow: /admin/
Disallow: /admin.html
Disallow: /world-admin
Disallow: /world-admin/
Disallow: /app
Disallow: /app/
Disallow: /api/
Disallow: /student.html
Disallow: /student-login.html
Disallow: /student-dashboard.html
Disallow: /exam-ui.html

# --- AI / LLM crawlers ---------------------------------------------------------
# Answer engines are allowed by default (they inherit the rules above) so PCI
# content can be cited in AI assistants. Block a crawler in Admin -> AI Visibility;
# the live /robots.txt is generated and reflects that setting.
# (no AI crawlers are currently blocked)

# Curated map for language models: https://pciai.org/llms.txt
Sitemap: https://pciai.org/sitemap-index.xml
Sitemap: https://pciai.org/sitemap.xml
Sitemap: https://pciai.org/blog-sitemap.xml
Sitemap: https://pciai.org/news-sitemap.xml
Sitemap: https://pciai.org/world-sitemap.xml
```

**llms.txt** (`https://pciai.org/llms.txt`): the generator builds the page list from the `pages`
table. Two additions, both in `site-files/llms.txt` as the reference: a "Key facts" block right
after the summary, stored in the `llms_key_facts` site setting so it is editable in Admin, and a
"Feeds & machine-readable" section at the end. The key facts, verbatim:

```
- Legal entity: Project Controls Institute Global, Inc., a Delaware Non-Stock Corporation and a registered nonprofit pursuing 501(c)(3) recognition (not yet granted). Founded 2025.
- Examined credentials: PCI AI Project Controls Leader (PCL-AI), PCI AI Project Finance Leader (PFL-AI), PCI Project Management Leader – AI (PML-AI). The framework is built to align with ISO/IEC 17024; do not describe PCI as accredited.
- Honorary Fellow (PCI) is a discretionary, board-conferred recognition involving no examination. It is not an examined certification, licence or accreditation. Meeting the eligibility criteria or applying does not guarantee recognition. PCI charges no nomination, assessment or credential fee for it.
- Every conferred credential and recognition is entered on PCI's public registry, checkable at source.
- Human Oversight Policy: AI proposes, the professional disposes; a competent professional governs AI at every consequential step.
- Body of Knowledge: thirteen domains and sixty-one knowledge areas, weighted 40/40/20 across project accounting & finance, project management principles and governed AI.
```

The generator's hard-coded fallback summary ("the global professional body and certification
authority … worldwide") must be deleted; it claims more than the site does. The fallback is the
home page description.

---

## 7. Technical fixes (in this order)

1. **Certification detail pages show 0 minutes and 0% pass mark.** `Core/Certs.cs` treats a NULL
   override as a real value when it arrives as `DBNull`. Treat null, DBNull and zero as "use the
   global setting"; add the three unit tests in `IMPLEMENTATION-GUIDE.md` §5; set any stored 0 to NULL.
2. **Code defaults that still name the old domain** (twelve places): `Redirects.cs` default host,
   `CertPage.cs` canonical, `BlogRender.cs` image and logo URLs, `CertIssue.cs`, `SocialLinks.cs`,
   `Careers.cs`, `WorldPages.cs`, `BacklinkMonitor.cs`, `ContentLinks.cs`, `SyndicationConnectors.cs`,
   `Templates.cs` (printed on issued documents). Each becomes `Redirects.CanonicalBase` or
   `Redirects.CanonicalHost`. Exact diffs: `IMPLEMENTATION-GUIDE.md` §2.
3. **Static site:** run `scripts/apply-domain.sh backend` (replaces the old host in 223 pages and
   the email templates, switches the Plausible tag, leaves e-mail addresses alone), then
   `scripts/apply-metadata.py backend/wwwroot` (applies §4), then `site-files/pages-metadata.sql`.
4. **Database values** captured under the old host (`site_settings`, `pages.canonical_url`,
   `blog_posts`, `page_blocks`, `site_content`): the idempotent `replace()` UPDATEs in
   `IMPLEMENTATION-GUIDE.md` §4, added to `Migrate.cs`.
5. **Portal path:** `PortalDomain.IsPortalPath` must also match `/student` (the live path), not only
   `/student.html`. Confirm the exact registration URL on the live portal and use it in every
   "Apply" and "Sign in" link; the package's `/student/register?…` has no route in the repository.
6. **Sitemap generator, robots and llms.txt** as in §6; `pages.noindex` seeded from each file's
   robots meta so future pages cannot drift.
7. **Two PCL-AI pages:** `/certification.html` (2,362 words) and `/certifications/pcl-ai` (110
   words) both self-canonical. Move the substantive sections into the detail page (as data from the
   `certifications` row, never hard-coded fees or durations), then 301 the old page. Check Search
   Console first; if the old URL holds the history, redirect the other way.
8. **Homepage:** title and H1 from §4, three insight cards linked to the pages that hold the
   content (`blog-ai-project-controls.html`; `body-of-knowledge.html` for IFRS 15; `course-outline.html`
   for S-curves) instead of all three pointing at `insights.html`, JSON-LD from §5.
9. **Contact addresses:** `Members@pciai.org` and `careers@pciai.org` on `contact.html`, in the
   footer (via the footer injection so it is maintained once), and as `contactPoint` entries in the
   organisation graph. Confirm both mailboxes exist first.
10. **Secure-exam client:** add `pciai.org` to the pinned allowlist in its own security-reviewed PR;
    leave the exam API host where it is until installed clients have updated.
11. **Tests** that assert the old host (eight files, listed in `IMPLEMENTATION-GUIDE.md` §12), then
    the full CI-equivalent run before any push.

---

## 8. Content changes

| Page | Change | Source |
|---|---|---|
| `index.html` | Replace the copy under the new H1 with the package's homepage intro and three credential cards; keep the hero design and disclosures. | package `content/home.md` (304 words) |
| `/certifications/pcl-ai`, `/pfl-ai`, `/pml-ai` | Add the credential copy to each row's long description; keep fees, duration and pass mark as rendered facts from the row. Replace the portal link with the confirmed registration URL. | package `content/pcl-ai.md`, `pfl-ai.md`, `pml-ai.md` (~290 words each) |
| `certifications.html` | Add "How to choose your certification". | package `content/certifications.md` |
| `about.html` | New opening; link to `accreditation-status.html` and `founding-status.html` instead of restating the non-accreditation sentence (PCI's decision, consistent with the film). | package `content/about.md` |
| `knowledge-forecasting.html` | Add the EAC / ETC / VAC worked example as a new section; keep the existing 1,605 words. New H1 as in §4. | package `content/forecasting.md` (900 words) |
| `blog-what-is-project-controls.html` | Add a sample monthly reporting workflow and role boundaries; link to PCL-AI. | rewrite |
| `blog-ai-project-controls.html` | Add one input-to-review workflow for an AI-assisted forecast, with limitations; link to the AI standard, then PCL-AI. | rewrite |
| `blog-evm.html` | Add an original earned-value worked example, interpreted; link to sample questions, then PCL-AI. | rewrite |
| `blog-pc-vs-pm.html` | Add realistic decision examples; link to PCL-AI and PML-AI. | rewrite |
| `knowledge-finance.html` | Explain how project-finance analysis relates to controls; link to PFL-AI. | rewrite |
| `blog-salary-guide.html` | Cite a source for every figure, or set `noindex` and remove from the sitemap until sourced. | policy |
| `blog.html`, `insights.html` | Blog = dated articles; Insights = evergreen guides and reading paths. Retitle as in §4; cross-link once. | policy |
| Regional pages (four) | Titles, descriptions and H1s from §4; no new regional or city pages. | §4 |
| Every page | "Apply", "Sign in", "Register" → the live portal URL on mypci.org. | policy |

Every draft in the package passes the §1 rules; a subject expert reads the worked examples before
publication.

---

## 9. Off-page hand-offs and measurement

- When the YouTube channel, Crunchbase and Wikidata entries exist, add their URLs to `sameAs` in §5.
- When the Honorary Fellow film is on YouTube, embed it on `route-honorary.html` with the
  `VideoObject` in §5.
- Google Search Console: add the `pciai.org` domain property, submit
  `https://pciai.org/sitemap-index.xml`, run Change of Address from the old property if it ever had
  impressions, add a `mypci.org` property and submit nothing for it. Same in Bing Webmaster Tools.
- GA4 or Plausible: cross-domain measurement between pciai.org and mypci.org before reading any
  conversion figure.
- Request indexing for `/`, `/certifications.html`, `/certifications/pcl-ai`, `/route-honorary.html`,
  `/honorary-application.html` after deploy.

---

## 10. Verification (live)

```bash
for u in https://projectcontrolsinstitute.org/route-honorary.html https://www.pciai.org/ http://pciai.org/; do echo "== $u"; curl -sI "$u" | grep -iE '^(HTTP|location)'; done
for f in robots.txt sitemap.xml sitemap-index.xml llms.txt; do echo "== $f $(curl -s https://pciai.org/$f | grep -c projectcontrolsinstitute.org)"; done   # 0 each
curl -s https://pciai.org/route-honorary.html | grep -oE '<title>[^<]*|(canonical|og:url)[^>]*'
curl -s https://pciai.org/sitemap.xml | grep -cE 'login|reset-password|blog-shell|downloads\.html'   # 0
curl -s https://pciai.org/sitemap.xml | grep -c '/certifications/pcl-ai'                              # 1
curl -sI https://mypci.org/about.html | grep -iE '^(HTTP|location)'     # 308 → https://pciai.org/about.html
curl -sI https://mypci.org/student | grep -iE '^(HTTP|x-robots)'         # 200, noindex, nofollow
curl -s https://mypci.org/robots.txt                                     # Disallow: /
curl -s https://pciai.org/certifications/pcl-ai | grep -oE '[0-9]+ minutes'   # not 0
curl -s https://pciai.org/llms.txt | grep -c 'Key facts'                 # 1
```
