# Developer change list — pciai.org as the primary domain, plus the SEO audit fixes

**For:** the PCI Platform developer (repo `PCI`, branch from `main`).
**From:** the SEO audit of `backend/wwwroot` (235 pages) and the backend's SEO code, 10 Sep 2026.
**Decision that drives this document:** PCI's website is **pciai.org**. The codebase currently treats
`projectcontrolsinstitute.org` as canonical everywhere. This document lists every change needed to make
pciai.org primary without losing the old domain's indexing, then the on-page fixes the audit found.

Nothing in this document has been applied to the repo. Reference files ready to drop in are beside it in
`seo/site-files/`: `sitemap.xml`, `sitemap-index.xml`, `robots.txt`, `llms.txt`.

Order of work matters: **Part A first, as one release.** A half-moved domain (canonicals on one host,
redirects on another) is worse than either state.

---

## Part A — Move the canonical domain to pciai.org

### A1. How the platform already handles the canonical host

Good news first: the site is built for this. `Core/Redirects.cs` reads `CANONICAL_HOST` and 301-redirects
every *known alternate host* page-to-page to `https://{CANONICAL_HOST}` in one hop, GET/HEAD only.
`Core/Sitemap.cs`, `Core/AiVisibility.cs` (robots.txt and llms.txt) and `Core/IndexNowService.cs` all
build URLs from `Redirects.CanonicalBase`. So the live `/sitemap.xml`, `/sitemap-index.xml`, `/robots.txt`
and `/llms.txt` switch host with one environment variable. What does **not** switch automatically is
listed in A3 to A6.

### A2. Environment and hosting (`render.yaml` / the Docker host)

| Variable | Value | Why |
|---|---|---|
| `CANONICAL_HOST` | `pciai.org` | Drives redirects, sitemap, robots, llms.txt, IndexNow |
| `REDIRECT_HOSTS` | `projectcontrolsinstitute.org,www.projectcontrolsinstitute.org` | Old domain becomes a known alternate and 301s page-to-page (the `www.pciai.org` variant is added automatically) |
| `APP_BASE_URL` | `https://pciai.org` | Boot validator requires a public https URL; used for absolute links in mail and certificates |
| `ALLOWED_ORIGIN` | `https://pciai.org` | Must equal `APP_BASE_URL` exactly, no trailing slash |
| `SITE_BASE_URL` | `https://pciai.org` | Where used alongside `APP_BASE_URL` |

Hosting: attach **pciai.org, www.pciai.org, projectcontrolsinstitute.org and www.projectcontrolsinstitute.org**
to the same service with TLS on all four. The old domain must keep resolving and serving TLS for the
redirects to work; do not let its certificate lapse. Keep it attached for at least twelve months.

### A3. Hard-coded defaults in backend code (change to `Redirects.CanonicalBase` or a config value)

Each of these silently keeps the old domain even after A2. File and line are from the current tree.

| File:line | Today | Change to |
|---|---|---|
| `Core/Redirects.cs:19` | default `"projectcontrolsinstitute.org"` | default `"pciai.org"` (so a missing env var still lands on the right host) |
| `Core/CertPage.cs:27` | canonical `"https://projectcontrolsinstitute.org/certifications/" + slug` | `Redirects.CanonicalBase + "/certifications/" + slug` |
| `Core/BlogRender.cs:55,243,297` | OG image and logo URLs on the old host | `Redirects.CanonicalBase + "/assets/…"` |
| `Core/CertIssue.cs:21` | fallback base URL | `Redirects.CanonicalBase` |
| `Core/SocialLinks.cs:99`, `Endpoints/Careers.cs:488` | fallback `https://www.projectcontrolsinstitute.org` (note: **www**, which the site itself redirects away from) | `Redirects.CanonicalBase` |
| `Core/WorldPages.cs:116` | setting default `world_institute_url` | `Redirects.CanonicalBase`; existing databases already hold the old value, see A5 |
| `Core/BacklinkMonitor.cs:23` | setting default `backlink_our_domain` | `Redirects.CanonicalHost`; see A5 |
| `Core/BacklinkMonitor.cs:42`, `Core/ContentLinks.cs:96` | User-Agent `(+https://projectcontrolsinstitute.org)` | `(+{Redirects.CanonicalBase})` |
| `Core/SyndicationConnectors.cs:94` | literal text "Originally published at … projectcontrolsinstitute.org" | `Redirects.CanonicalHost` |
| `Endpoints/Templates.cs:92` | certificate template footer prints `projectcontrolsinstitute.org` | `Redirects.CanonicalHost`. This is printed on issued certificates; existing PDFs are unaffected, new ones must show the right domain |
| `Program.cs:468`, `Core/PortalDomain.cs:7` | comments naming the old host | update the comments so the next reader is not misled |

**Email domain is a separate decision.** `Core/Mailer.cs:34,161`, `Core/OutboxDispatcher.cs:87`
(`no-reply@projectcontrolsinstitute.org`), `Endpoints/Badges.cs:37` (`credentials@…`) and the eight
seeded mailboxes in `Data/CommsSeed.cs:17-24` all use the old domain. Mail can legitimately stay on
projectcontrolsinstitute.org while the website moves; it only needs SPF/DKIM/DMARC to remain correct for
whichever domain sends. If PCI wants mail on pciai.org too, add a `MAIL_DOMAIN` config and derive every
default from it, and set up SPF/DKIM/DMARC for pciai.org **before** switching, or transactional mail will
land in spam. The addresses PCI has already published, **Members@pciai.org** and **careers@pciai.org**,
must exist as real mailboxes on pciai.org either way.

### A4. Static site files under `backend/wwwroot` (scripted, one commit)

The old host appears **4,946 times across 223 HTML files**: `<link rel="canonical">` (221), `og:url`
(217), the JSON-LD `@id`, `url`, `logo` and `sameAs` values, absolute internal links, and the ten
transactional templates in `backend/emails/`. Replace the *web* host, leave the *mail* addresses alone:

```bash
cd backend
# 1. web URLs (scheme + host) → new host
grep -rl 'https://projectcontrolsinstitute.org' wwwroot emails --include='*.html' --include='*.json' --include='*.xml' --include='*.txt' \
  | xargs sed -i 's#https://projectcontrolsinstitute\.org#https://pciai.org#g'
# 2. www variant, same treatment
grep -rl 'https://www.projectcontrolsinstitute.org' wwwroot emails \
  | xargs sed -i 's#https://www\.projectcontrolsinstitute\.org#https://pciai.org#g'
# 3. bare host in visible text that is NOT part of an email address (review this diff by hand)
grep -rn '[^@/.]projectcontrolsinstitute\.org' wwwroot --include='*.html' | grep -v '@projectcontrolsinstitute' | less
```

Then:

- Replace `wwwroot/sitemap.xml` and `wwwroot/robots.txt` (the static fallbacks) with the versions in
  `seo/site-files/`. The live endpoints are generated, but the fallbacks are what a crawler sees if the
  middleware is ever bypassed, and they currently advertise the old host.
- Re-run the audit's grep afterwards; the only remaining matches should be `@projectcontrolsinstitute.org`
  addresses (if mail stays) and the historical text on `founding-status.html` if it names the old domain
  as history.
- `wwwroot/search-index.json` and the built app bundles contain no host references; nothing to do there.

### A5. Values already stored in the database

Existing deployments hold the old host in data, which no code change touches:

```sql
-- take a backup first; run once, inside a transaction
UPDATE site_settings SET svalue = replace(svalue, 'https://projectcontrolsinstitute.org', 'https://pciai.org')
  WHERE svalue LIKE '%projectcontrolsinstitute.org%';
UPDATE site_settings SET svalue = 'pciai.org' WHERE skey = 'backlink_our_domain';
UPDATE pages SET canonical_url = replace(canonical_url, 'https://projectcontrolsinstitute.org', 'https://pciai.org')
  WHERE canonical_url LIKE '%projectcontrolsinstitute.org%';
UPDATE blog_posts SET html = replace(html, 'https://projectcontrolsinstitute.org', 'https://pciai.org')
  WHERE html LIKE '%projectcontrolsinstitute.org%';
```

Check `media`, `site_content` and `page_blocks` for stored absolute URLs the same way. Put this in
`Data/Migrate.cs` only if it is written idempotently (the `replace` form above is); otherwise run it as
a one-off admin script and record it in the changelog.

### A6. The secure-exam client (security-critical, read before touching)

`secureexam/PCI.SecureExam.Core/ClientConfig.cs` pins the client to `AllowedApiHosts =
{ "projectcontrolsinstitute.org", "localhost" }` and defaults `ApiBaseUrl` to
`https://exam.projectcontrolsinstitute.org`. Three facts decide what to do:

- `Redirects.Target` never redirects POST, so a client talking to the old exam host is **not** redirected;
  it simply keeps working as long as that host still serves the API.
- Every installed client carries the allowlist compiled into it. Changing the code changes only clients
  built after the change.
- The allowlist is what stops a malicious launch link pointing the kiosk at another server. Adding a host
  widens the trust boundary and needs the same review as any security change.

Recommendation: **keep the exam API on `exam.projectcontrolsinstitute.org` for now.** Add `"pciai.org"`
to `AllowedApiHosts` (so a future `exam.pciai.org` is trusted), update the copies of `ClientConfig.cs`
in `PCI.SecureExam.Core.RunnableChecks` and the expectations in `PCI.SecureExam.Tests/LaunchParametersTests.cs`
and `RunnableChecks/SecurityChecks.cs`, publish a new client build, and only move the exam host once the
old client population has updated. Do not move the exam API and the website on the same day.

### A7. Tests that assert the old host

`tests/PCI.Backend.Tests/RedirectTests.cs`, `PortalDomainTests.cs`, `IndexNowTests.cs`,
`PassportDocumentsTests.cs`, `tests/integration_test.py`, `tests/passport_documents_test.py`,
`tests/world_og_metadata_test.py`. Update the expected host, or better, make them read
`Redirects.CanonicalBase` / the env var so the suite is host-independent. CI runs these; they will fail
loudly the moment A3 lands, which is the point.

### A8. Search engines and profiles (after deploy, same day)

1. Google Search Console: add the `pciai.org` domain property (DNS TXT verification). Submit
   `https://pciai.org/sitemap-index.xml`. In the **old** property, run **Change of Address** to pciai.org.
2. Bing Webmaster Tools: add pciai.org, submit the sitemap index, use Site Move.
3. IndexNow: the key file is served at `/{key}.txt` on whatever `CanonicalBase` is; re-submit the key on
   the new host once (the service handles URLs after that).
4. Update the website field on the LinkedIn company page and X profile to `https://pciai.org`, and the
   `sameAs` values in the JSON-LD stay as the profile URLs (they do not change).
5. Every external listing in `seo/listings.csv` uses the new host from day one.

### A9. Verification checklist (do not ship without every line green)

```bash
# redirects: one hop, correct target, path preserved
curl -sI https://projectcontrolsinstitute.org/route-honorary.html | grep -iE '^(HTTP|location)'
curl -sI https://www.projectcontrolsinstitute.org/certifications | grep -iE '^(HTTP|location)'
curl -sI https://www.pciai.org/ | grep -iE '^(HTTP|location)'
curl -sI http://pciai.org/ | grep -iE '^(HTTP|location)'          # http → https
# generated files carry the new host only
for f in robots.txt sitemap.xml sitemap-index.xml llms.txt blog-sitemap.xml news-sitemap.xml; do
  echo "== $f"; curl -s https://pciai.org/$f | grep -c 'projectcontrolsinstitute.org'; done   # expect 0 each
# a page's own tags
curl -s https://pciai.org/route-honorary.html | grep -oE '(canonical|og:url)[^>]*'
# no POST is redirected (exam client safety)
curl -s -o /dev/null -w '%{http_code}\n' -X POST https://projectcontrolsinstitute.org/api/health   # not 301
# boot validator and suites
cd backend && python3 tests/settings_test.py && python3 tests/integration_test.py && ./smoke-test.sh
```

---

## Part B — Sitemap

The live `/sitemap.xml` is generated from the `pages` table (`published=1`, `noindex` not set) plus
published blog posts and open job postings. The static `wwwroot/sitemap.xml` is only a fallback. Fixes:

1. **17 indexable pages are absent from the static file** and must be confirmed present in the live one:
   `badge`, `become-a-training-partner`, `careers`, `certifications`, `course-outline`, `directory`,
   `downloads-centre`, `forum`, `honorary-application`, `reviews`, `route-founding`, `route-honorary`,
   `route-standard`, `training-partners` (all `.html`). On staging run
   `curl -s https://pciai.org/sitemap.xml | grep -c route-honorary` and expect 1. If 0, the row in
   `pages` is unpublished or flagged; fix the row, not the file. The three template shells in that list
   of 17 are handled in item 2.
2. **Template shells must never be indexed.** `blog-shell.html`, `careers-detail.html` and
   `certification-detail.html` are server-side templates carrying a literal `{{TITLE}}` / `{{DESC}}` and no
   H1. Add them to `Sitemap.Exclude` in `Core/Sitemap.cs`, add
   `<meta name="robots" content="noindex">` to each file, and set `noindex=1` on their `pages` rows so
   `AiVisibility.LlmsTxt` skips them too.
3. **Honour `pages.canonical_url` in the sitemap.** `certifications.html` declares its canonical as
   `/certifications` (extension-less, served by `Program.cs:1933`), but `Sitemap.Xml` emits
   `/certifications.html`. `PageContent` already loads `canonical_url` overrides; use the same value in
   `Sitemap.Xml` and `LlmsTxt` when present, so the sitemap never lists a URL that canonicalises elsewhere.
4. **Add the certification detail pages.** `/certifications/{slug}` pages (`Core/CertPage.cs`) are
   rendered from the `certifications` table and are not in any sitemap. Add a loop in `Sitemap.Xml` over
   `SELECT slug, updated_at FROM certifications WHERE active=1`.
5. Drop `seo/site-files/sitemap.xml` and `sitemap-index.xml` into `wwwroot/` as the new fallbacks. They
   list all 211 indexable static pages on pciai.org with priorities: 1.0 home, 0.9 for the certification,
   route, honorary, Body of Knowledge, comparison, employer and partner pages, 0.5 for legal pages, 0.8
   otherwise.

---

## Part C — robots.txt

Generated live by `AiVisibility.Robots` and already correct in shape (allow all, disallow private
surfaces, list every sitemap, point at llms.txt). Two fixes:

1. Replace the static fallback `wwwroot/robots.txt` with `seo/site-files/robots.txt` (new host, and the
   private paths brought in line with `Redirects.IsPrivatePath`: it now also disallows
   `/student-login.html`, `/student-dashboard.html` and `/world-admin`).
2. Add the same three paths to the `Private` list the generator uses, if they are not already there, so
   the generated file and the header-level noindex agree.

---

## Part D — llms.txt

Generated live by `AiVisibility.LlmsTxt` from the `pages` table, in six keyword buckets. Three fixes:

1. **Replace the fallback summary text** (`Core/AiVisibility.cs` around line 154). It currently reads
   "the global professional body and certification authority for project controls … worldwide", which is
   a claim the site itself does not make. Fall back to the home page's meta description, which is already
   the second option in that code; delete the third.
2. **Add a "Key facts" block** after the summary, sourced from a new `site_settings` key
   (`llms_key_facts`, editable in the admin) and seeded with the six facts in `seo/site-files/llms.txt`:
   legal entity and status, the four credentials with the "built to align with ISO/IEC 17024" wording, the
   Honorary Fellow (PCI) disclosure sentence, the public registry, the Human Oversight Policy, and the
   Body of Knowledge numbers. This is the block that stops language models inventing accreditation.
3. **Add a "Feeds & machine-readable" section** listing the sitemap index and `feed.xml`, `atom.xml`,
   `feed.json`. The reference file shows the exact shape.

The reference file also assigns pages to buckets slightly better than the current keyword list (it adds
`pcl`, `pfl`, `pml`, `route-`, `human-oversight`, `founding-status`, `contact`, `faq`, `training`,
`partner`, `glossary`), which halves the size of the "More from PCI" catch-all. Port those keywords.

---

## Part E — Titles over 60 characters (4 pages)

| Page | Current (chars) | New |
|---|---|---|
| `certifications.html` | 80 | PCI Certifications: PCL-AI, PFL-AI and PML-AI \| PCI |
| `donate.html` | 68 | Donate to the Project Controls Institute \| PCI |
| `downloads-centre.html` | 63 | Downloads Centre: Policies and Legal Documents \| PCI |
| `honorary-application.html` | 64 | Honorary Fellow (PCI) Application \| PCI |

Titles live in the file's `<title>` and, if an admin has edited it, in `pages.title`. Change both.

---

## Part F — Meta descriptions over 155 characters (20 pages)

All replacements are at or under 155 characters and keep every factual claim of the original.

| Page | New description |
|---|---|
| `become-a-training-partner.html` | Apply to become a recognised PCI Training Partner for PCL-AI exam preparation. The examination and the certification decision stay independent of training. |
| `body-of-knowledge.html` | The competency framework PCL-AI assesses: thirteen domains across project accounting and finance (40%), project management (40%) and governed AI (20%). |
| `certifications.html` | PCI's professional certifications, PCL-AI, PFL-AI and PML-AI: eligibility, application routes, fees, exam information and the Body of Knowledge for each. |
| `course-outline.html` | The complete PCL-AI study outline: thirteen domains and 61 knowledge areas, weighted 40/40/20 across finance, project management and governed AI. |
| `curriculum.html` | Thirteen domains and 61 knowledge areas: project accounting and finance, project management principles and governed AI, weighted 40/40/20 for PCL-AI. |
| `directory.html` | Search the PCI member directory for certified project controls professionals by name, country and certification. Listings are consented and verifiable. |
| `downloads-centre.html` | Every PCI policy, guideline and legal document in one place: enrolment, payment, examination, membership, conduct and governance, as PDF downloads. |
| `downloads.html` | PCI's candidate guidelines and policies: enrolment, payment, examination, membership and conduct, plus the emails you receive at each step. |
| `forum.html` | The PCI community forum, open to everyone: project controls, exam preparation, the Body of Knowledge, AI in project controls and careers, worldwide. |
| `founding-status.html` | An honest account of what the Project Controls Institute has established and what is still in development, including its accreditation roadmap. |
| `honorary-application.html` | Apply for the Board's consideration to be conferred Honorary Fellow (PCI), a recognition of distinguished contribution separate from examined credentials. |
| `index.html` | The Project Controls Institute awards PCL-AI, PFL-AI and PML-AI: credentials uniting project controls, cost engineering and finance with governed AI. |
| `leadership.html` | How the Project Controls Institute is governed, who makes certification decisions, and the open call for founding examiners and subject-matter experts. |
| `reviews.html` | Reviews and testimonials from Project Controls Institute members and students on the PCI certification programmes, moderated and published unedited. |
| `route-founding.html` | The founding route: an invitation-only founding cohort with membership, study and exam access. The credential is still earned by passing the examination. |
| `route-honorary.html` | The honorary route: apply for the Board's consideration to be conferred Honorary Fellow (PCI), a recognition of distinguished contribution, no examination. |
| `sector-aero.html` | Project controls for aerospace and defence: aircraft, spacecraft, defence platforms and advanced technologies, with governed AI and the PCI certifications. |
| `training-partners.html` | Find a recognised PCI Training Partner for PCL-AI exam preparation. Partners prepare candidates; the exam and certification decision stay independent. |
| `university-partnerships.html` | Connect academic programmes to the project controls standard: curriculum alignment, a student pathway to PCI certifications and research collaboration. |
| `why-employers.html` | Why EPC contractors, owners, energy, defence, aerospace and government value PCI certifications: planning, cost, forecasting, risk and AI governance. |

Descriptions live in `<meta name="description">` and, when edited, in `pages.meta_description`. Change both.

---

## Part G — Duplicate page: `downloads.html` and `downloads-centre.html`

Both carry the same description, and `Program.cs:1845-1856` serves `downloads-centre.html` for
`/downloads`. Three URLs, one page. Make `downloads-centre.html` the canonical: give `downloads.html` a
`<link rel="canonical" href="https://pciai.org/downloads-centre.html">` (or 301 it in the same middleware
block), remove `downloads.html` from the sitemap, and use the two distinct descriptions from Part F if
both pages are kept.

---

## Part H — Structured data missing on indexable pages

| Page | Add | Notes |
|---|---|---|
| `certifications.html` | `ItemList` of `EducationalOccupationalCredential` (PCL-AI, PFL-AI, PML-AI, and the AIPC specialist certificate on `ai-cert.html`), each with `name`, `description`, `url`, `recognizedBy` → the Organization `@id` | Copy the credential node already on `index.html`; keep "built to align with ISO/IEC 17024" wording |
| `careers.html` | `BreadcrumbList` + `WebPage` | Individual postings already get `JobPosting` server-side |
| `directory.html` | `BreadcrumbList` + `WebPage` | Do not add `Person` nodes for members without consent |
| `badge.html` | `BreadcrumbList` + `WebPage` | |
| `reviews.html` | `BreadcrumbList` + `WebPage` | **No `AggregateRating`** unless the count and value are computed from real, moderated reviews at render time; a hand-typed rating is a policy violation |

`BreadcrumbList` should be sitewide; the CMS injection layer (`Core/PageContent.cs`) is the right place
to add it once rather than per file.

---

## Part I — Contact addresses on the site

Members@pciai.org and careers@pciai.org appear on **no page**; every page uses hello@projectcontrolsinstitute.org.

1. `contact.html`: add both addresses as `mailto:` links with a one-line purpose each (membership and
   Honorary Fellow enquiries; careers).
2. Footer, sitewide: the footer's contact line is static per file (`.ft-bottom`), so either script it
   across the 214 pages or move the contact line into the `<!--PCI-NAV-FOOTER-->` injection so it is
   maintained in one place. Prefer the injection.
3. Organisation JSON-LD (`index.html` and wherever the graph is repeated): add
   `contactPoint` entries with `contactType` "membership" (Members@pciai.org) and "careers"
   (careers@pciai.org) beside the existing customer-support entry.
4. Confirm both mailboxes exist and are monitored before any of this ships.

---

## Part J — Hand-offs from the off-page programme

1. When the YouTube channel, Crunchbase and Wikidata entries exist, add their URLs to the `sameAs`
   array in the organisation schema.
2. When the Honorary Fellow film is on YouTube, embed it on `route-honorary.html` and add a
   `VideoObject` node (`name`, `description`, `thumbnailUrl`, `uploadDate`, `duration` PT3M50S,
   `embedUrl`, `contentUrl`) referencing the YouTube URL.

---

## Part K — Noted, no action

- `partner.html` has two H1s and `student.html` two; both are `noindex`.
- `admin-chat.html` links to `admin.html`, which does not exist as a file; it is a private page.
- No image on any indexable page lacks `alt`. No indexable page lacks a canonical, an Open Graph title,
  or a single H1 (templates aside). The site is in good technical shape; this list is about the domain
  and the edges.

---

## Suggested commits

1. `Domain: pciai.org canonical` — A2 env changes documented, A3 code defaults, A4 static replace, A5
   migration, A7 tests. One PR, one deploy.
2. `Sitemap: honour canonical_url, exclude template shells, add cert detail pages` — B2 to B4.
3. `SEO: titles, descriptions, downloads canonical, structured data` — E, F, G, H.
4. `Contact: Members@ and careers@ on contact page, footer and schema` — I.
5. `llms.txt: key facts block, feeds section, bucket keywords` — D.
6. `secureexam: trust pciai.org` — A6, its own PR with the security reviewer.
