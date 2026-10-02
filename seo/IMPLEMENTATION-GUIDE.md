# PCI AI SEO implementation guide

A step-by-step runbook a developer can follow by hand, or hand to Claude Code (prompt in §14).
Every step names the file and line, shows the exact change, and ends with a check. Steps are in the
order they must run. The reasoning behind each step is in `developer-changes.md` and
`content-updates.md`; this document is the "do this" version.

**Repositories:** platform code in `PCI` (branch from `main`); this guide, its scripts and reference
files in `PCI-Marketing/seo/`. **Domains:** website `pciai.org`; student portal `https://mypci.org/student`;
legacy `projectcontrolsinstitute.org` (301 to pciai.org). **Verified here:** the scripts in §3 and §8 were
dry-run against a copy of `backend/wwwroot` and are idempotent; the C# patches were written against
the current `main` line numbers but could not be compiled in this environment (no .NET SDK), so §12's
build and test run is mandatory before pushing.

Claim rules apply to every word you type on the site: never "accredited", "ANAB", "IAS" or "ISO/IEC
17024 certified" (only "built to align with ISO/IEC 17024"); never "501(c)(3)" as a fact; never
"recognised by"; no salaries, pass rates or member counts the site does not publish; the honorary route
is "Honorary Fellow (PCI)", a recognition; there is no "PCP-AI".

---

## 0. Why, and the starting inventory

The website was built with `projectcontrolsinstitute.org` as its domain. PCI has since decided the
public website is `pciai.org` and the student portal is `mypci.org/student`. Everything below migrates
the old domain out of the code, the pages, the database and the tests, and turns the old domain into a
page-for-page 301. Record the starting state first so the end state can be proven in the PR:

```bash
cd PCI && git fetch origin && git log -1 --format='%h %cd' origin/main
grep -rl "projectcontrolsinstitute.org" backend/wwwroot/*.html | wc -l                          # 223 at the time of writing
grep -rn "projectcontrolsinstitute.org" backend/Core backend/Endpoints backend/Program.cs | wc -l # about 25
curl -s https://pciai.org/route-honorary.html | grep -oE '(canonical|og:url)[^>]*'
curl -s https://pciai.org/sitemap.xml | head -3
curl -sI https://mypci.org/student | grep -iE '^(HTTP|location|x-robots)'
```

If the live site serves something `origin/main` does not contain (canonicals already on pciai.org,
a `/student` route), note it in the PR and confirm with whoever deploys which branch is live before
merging; do not guess.

Create the working branch:

```bash
git checkout -b seo/pciai-domain-and-audit origin/main
```

---

## 1. Environment (hosting console / `render.yaml`)

Set all of these in the same deploy. Half of them is worse than none (see `developer-changes.md` A10).

| Variable | Value |
|---|---|
| `CANONICAL_HOST` | `pciai.org` |
| `REDIRECT_HOSTS` | `projectcontrolsinstitute.org,www.projectcontrolsinstitute.org` |
| `APP_BASE_URL` | `https://pciai.org` |
| `ALLOWED_ORIGIN` | `https://pciai.org` |
| `SITE_BASE_URL` | `https://pciai.org` |
| `PORTAL_BASE_URL` | `https://mypci.org` |
| `PORTAL_HOSTS` | `www.mypci.org` |

Attach `pciai.org`, `www.pciai.org`, `projectcontrolsinstitute.org` and `www.projectcontrolsinstitute.org`
to the service with TLS on all four. Keep the old domain attached for at least twelve months.

**Check (after deploy, §13):** old-domain URLs return one 301 to the same path on pciai.org.

---

## 2. Code defaults that still carry the old domain

Apply each change exactly. Line numbers are from `origin/main` at 2 August 2026; if they have moved,
search for the quoted text.

### 2.1 `backend/Core/Redirects.cs:19`

```diff
-            ? h : "projectcontrolsinstitute.org";
+            ? h : "pciai.org";
```

Also update the summary comment at the top of the file (lines 4-11) to name `pciai.org` as the
approved canonical.

### 2.2 `backend/Core/CertPage.cs:27`

```diff
-        var canonical = "https://projectcontrolsinstitute.org/certifications/" + slug;
+        var canonical = Redirects.CanonicalBase + "/certifications/" + slug;
```

### 2.3 `backend/Core/BlogRender.cs:55, 243, 297`

```diff
-        if (string.IsNullOrWhiteSpace(img)) return "https://projectcontrolsinstitute.org/assets/og-image.jpg";
+        if (string.IsNullOrWhiteSpace(img)) return Redirects.CanonicalBase + "/assets/og-image.jpg";
```
```diff
-            canonical, "website", "https://projectcontrolsinstitute.org/assets/og-image.jpg", head.ToString(), sb.ToString(),
+            canonical, "website", Redirects.CanonicalBase + "/assets/og-image.jpg", head.ToString(), sb.ToString(),
```
```diff
-                ["logo"] = new Dictionary<string, object?> { ["@type"] = "ImageObject", ["url"] = "https://projectcontrolsinstitute.org/assets/apple-touch-icon.png" }
+                ["logo"] = new Dictionary<string, object?> { ["@type"] = "ImageObject", ["url"] = Redirects.CanonicalBase + "/assets/apple-touch-icon.png" }
```

### 2.4 `backend/Core/CertIssue.cs:21`

```diff
-        if (string.IsNullOrEmpty(b)) b = "https://projectcontrolsinstitute.org";
+        if (string.IsNullOrEmpty(b)) b = Redirects.CanonicalBase;
```

### 2.5 `backend/Core/SocialLinks.cs:99` and `backend/Endpoints/Careers.cs:488`

```diff
-        if (string.IsNullOrWhiteSpace(baseUrl)) baseUrl = "https://www.projectcontrolsinstitute.org";
+        if (string.IsNullOrWhiteSpace(baseUrl)) baseUrl = Redirects.CanonicalBase;
```

(`Careers.cs` sits in `PCI.Backend.Endpoints`; add `using PCI.Backend.Core;` if it is not already there.)

### 2.6 `backend/Core/WorldPages.cs:116`

```diff
-        Settings.Str(db, "world_institute_url", "https://projectcontrolsinstitute.org");
+        Settings.Str(db, "world_institute_url", Redirects.CanonicalBase);
```

### 2.7 `backend/Core/BacklinkMonitor.cs:23, 42` and `backend/Core/ContentLinks.cs:96`

```diff
-    public static string OurDomain(Db db) => Settings.Str(db, "backlink_our_domain", "projectcontrolsinstitute.org").Trim().ToLowerInvariant();
+    public static string OurDomain(Db db) => Settings.Str(db, "backlink_our_domain", Redirects.CanonicalHost).Trim().ToLowerInvariant();
```
```diff
-            req.Headers.TryAddWithoutValidation("User-Agent", "PCI-BacklinkMonitor/1.0 (+https://projectcontrolsinstitute.org)");
+            req.Headers.TryAddWithoutValidation("User-Agent", "PCI-BacklinkMonitor/1.0 (+" + Redirects.CanonicalBase + ")");
```
```diff
-            req.Headers.TryAddWithoutValidation("User-Agent", "PCI-LinkChecker/1.0 (+https://projectcontrolsinstitute.org)");
+            req.Headers.TryAddWithoutValidation("User-Agent", "PCI-LinkChecker/1.0 (+" + Redirects.CanonicalBase + ")");
```

### 2.8 `backend/Core/SyndicationConnectors.cs:94`

```diff
-        var html = post.Html + $"\n<p><em>Originally published at <a href=\"{post.CanonicalUrl}\">projectcontrolsinstitute.org</a>.</em></p>";
+        var html = post.Html + $"\n<p><em>Originally published at <a href=\"{post.CanonicalUrl}\">{Redirects.CanonicalHost}</a>.</em></p>";
```

### 2.9 `backend/Endpoints/Templates.cs:92` (printed on issued documents)

```diff
-                        $"issued {day}", "projectcontrolsinstitute.org" }
+                        $"issued {day}", Redirects.CanonicalHost }
```

### 2.10 `backend/Core/PortalDomain.cs:84-87` — the live portal path is `/student`

```diff
     public static bool IsPortalPath(PathString path) =>
         path.StartsWithSegments("/app")
+        || path.StartsWithSegments("/student")
         || path.Equals("/student.html", StringComparison.OrdinalIgnoreCase)
```

`StartsWithSegments("/student")` matches `/student` and `/student/…` but not `/student.html` or
`/students.html`, which is what we want. Update the comment on line 7 to say pciai.org.

### 2.11 Email domain — decision, not a patch

`Core/Mailer.cs:34,161`, `Core/OutboxDispatcher.cs:87`, `Endpoints/Badges.cs:37`, `Data/CommsSeed.cs:17-24`
default to `…@projectcontrolsinstitute.org`. Leave them if mail stays on that domain. If mail moves to
pciai.org, set up SPF, DKIM and DMARC for pciai.org **first**, then introduce a `MAIL_DOMAIN` variable and
derive the defaults from it. Either way, `Members@pciai.org` and `careers@pciai.org` must exist.

**Check:** `grep -rn "projectcontrolsinstitute.org" backend/Core backend/Endpoints backend/Program.cs`
returns only mail addresses and comments you have deliberately kept.

---

## 3. Static site: domain replace and the fallback files

```bash
cd PCI-Marketing && ./seo/scripts/apply-domain.sh ../PCI/backend
```

The script replaces `https://projectcontrolsinstitute.org` and the `www`/`http` variants with
`https://pciai.org` in every `.html`, `.json`, `.xml` and `.txt` under `backend/wwwroot` and
`backend/emails`, leaves e-mail addresses alone, switches the **Plausible analytics tag**
(`data-domain="projectcontrolsinstitute.org"`, present on every page) to `pciai.org`, prints the
remaining count (must be 0), then lists any bare-host mentions outside e-mail addresses for review by
hand (on the current tree there are none once the Plausible tag is switched).

**Plausible:** add `pciai.org` as a site in the Plausible dashboard before this deploys, or every
visit after the switch is dropped. Keep the old site for its history. If the portal should be
measured too, add `mypci.org` there and in the portal's own pages; do not share one Plausible site
across both domains.

Then replace the static fallbacks:

```bash
cp seo/site-files/sitemap.xml ../PCI/backend/wwwroot/sitemap.xml
cp seo/site-files/robots.txt  ../PCI/backend/wwwroot/robots.txt
```

**Check:** `grep -rl "projectcontrolsinstitute.org" ../PCI/backend/wwwroot/*.html | wc -l` counts only
files that mention the old domain as history or as an e-mail address.

---

## 4. Database values (one-off, with a backup)

Add to `backend/Data/Migrate.cs`, after the `AddCol` block (around line 100), so every environment
converges on boot. The `replace()` form is idempotent on both providers.

```csharp
// Domain move: values captured while projectcontrolsinstitute.org was canonical (idempotent).
db.Exec("UPDATE site_settings SET svalue = replace(svalue, 'https://projectcontrolsinstitute.org', 'https://pciai.org') WHERE svalue LIKE '%projectcontrolsinstitute.org%'");
db.Exec("UPDATE site_settings SET svalue = 'pciai.org' WHERE skey = 'backlink_our_domain' AND svalue = 'projectcontrolsinstitute.org'");
db.Exec("UPDATE pages SET canonical_url = replace(canonical_url, 'https://projectcontrolsinstitute.org', 'https://pciai.org') WHERE canonical_url LIKE '%projectcontrolsinstitute.org%'");
try { db.Exec("UPDATE blog_posts SET html = replace(html, 'https://projectcontrolsinstitute.org', 'https://pciai.org') WHERE html LIKE '%projectcontrolsinstitute.org%'"); } catch { /* table absent on first boot */ }
try { db.Exec("UPDATE page_blocks SET cvalue = replace(cvalue, 'https://projectcontrolsinstitute.org', 'https://pciai.org') WHERE cvalue LIKE '%projectcontrolsinstitute.org%'"); } catch { }
try { db.Exec("UPDATE site_content SET cvalue = replace(cvalue, 'https://projectcontrolsinstitute.org', 'https://pciai.org') WHERE cvalue LIKE '%projectcontrolsinstitute.org%'"); } catch { }
```

Check the column names against `schema.sql` before committing (`page_blocks.cvalue`,
`site_content.cvalue`, `blog_posts.html`). Do not touch e-mail address settings.

**Check:** boot locally twice; the second boot logs no change and the suites in §12 pass.

---

## 5. Certification detail pages show "0 minutes" and "0% pass mark"

`backend/Core/Certs.cs:84-85`. A SQL NULL comes back as `DBNull` on the MySQL provider (and can on
SQLite through the shared reader), which is not C# `null`, so the override branch runs and `H.D`
yields 0.

```diff
-        var dur = c["duration_minutes"] is null ? g.Duration : H.D(c["duration_minutes"]);
-        var pass = c["pass_mark_pct"] is null ? g.Pass : H.D(c["pass_mark_pct"]);
+        // NULL means "use the global exam setting". A NULL arrives as DBNull on some providers and
+        // an operator may have saved 0 by mistake; neither is a real override.
+        var durRaw = c["duration_minutes"]; var passRaw = c["pass_mark_pct"];
+        var dur = durRaw is null or DBNull || H.D(durRaw) <= 0 ? g.Duration : H.D(durRaw);
+        var pass = passRaw is null or DBNull || H.D(passRaw) <= 0 ? g.Pass : H.D(passRaw);
```

Add `backend/tests/PCI.Backend.Tests/CertsCfgTests.cs`:

```csharp
using PCI.Backend.Core;
using PCI.Backend.Data;
using Xunit;

namespace PCI.Backend.Tests;

public class CertsCfgTests : IClassFixture<DbFixture>
{
    readonly Db _db;
    public CertsCfgTests(DbFixture f) => _db = f.Db;

    [Fact]
    public void NullOverridesFallBackToGlobalExamSettings()
    {
        var id = Certs.DefaultId;                                   // seeded PCL-AI row
        _db.Execute("UPDATE certifications SET duration_minutes=NULL, pass_mark_pct=NULL WHERE id=?", id);
        var cfg = Certs.Cfg(_db, id);
        Assert.Equal(H.Cfg(_db).Duration, cfg.Duration);
        Assert.Equal(H.Cfg(_db).Pass, cfg.Pass);
        Assert.True(cfg.Duration > 0 && cfg.Pass > 0);
    }

    [Fact]
    public void ZeroIsNotAnOverride()
    {
        var id = Certs.DefaultId;
        _db.Execute("UPDATE certifications SET duration_minutes=0, pass_mark_pct=0 WHERE id=?", id);
        var cfg = Certs.Cfg(_db, id);
        Assert.True(cfg.Duration > 0 && cfg.Pass > 0);
    }

    [Fact]
    public void RealOverrideWins()
    {
        var id = Certs.DefaultId;
        _db.Execute("UPDATE certifications SET duration_minutes=120, pass_mark_pct=70 WHERE id=?", id);
        var cfg = Certs.Cfg(_db, id);
        Assert.Equal(120, cfg.Duration); Assert.Equal(70, cfg.Pass);
        _db.Execute("UPDATE certifications SET duration_minutes=NULL, pass_mark_pct=NULL WHERE id=?", id);
    }
}
```

If `Certs.DefaultId` is not the seeded PCL-AI id in the test fixture, use
`_db.Scalar<long>("SELECT id FROM certifications WHERE code='PCL-AI'")`. Then run the row check on
production data: `SELECT code, duration_minutes, pass_mark_pct FROM certifications;` and set any stored
0 to NULL.

**Check:** `/certifications/pcl-ai`, `/pfl-ai`, `/pml-ai` show the same duration and pass mark as the
homepage and catalogue, and the same values the certification owner confirms.

---

## 6. Sitemap, robots and llms.txt generators

### 6.1 The `pages` table is seeded from `schema.sql`, and it overrides the files

`backend/schema.sql` seeds 215 `pages` rows **with** `title`, `meta_description` and `noindex`
(lines ~489 onward), and `Core/PageContent.cs` injects `pages.title` / `pages.meta_description` /
`pages.canonical_url` over the file whenever they are set. Two consequences:

- Changing a `<title>` in a file does nothing on an installed site until the row changes too. §8 runs
  `seo/site-files/pages-metadata.sql` for that, and the same values must go into the `schema.sql`
  seed rows so a fresh install agrees (then `python3 tools/sqlite_to_mysql.py` to regenerate
  `schema.mysql.sql`).
- The seed marks `login.html`, `reset-password.html` and the student pages `noindex=1` already, but
  `enrol.html` and the three template shells are seeded `noindex=0`. The SQL in §8 fixes the rows;
  the patch below stops the same drift for any page added later.

`backend/Core/PageScan.cs:319-320` — set `noindex` from the file for pages the seed does not know:

```diff
             foreach (var slug in perPage.Keys)
                 db.Execute("INSERT OR IGNORE INTO pages(slug) VALUES(?)", slug);
+            // A page that ships with <meta name="robots" content="noindex"> must never enter the
+            // sitemap or llms.txt. Only ever sets the flag; an operator can still clear it in Admin.
+            foreach (var (slug, html) in noindexFiles)
+                db.Execute("UPDATE pages SET noindex=1 WHERE slug=? AND (noindex IS NULL OR noindex=0)", slug);
```

and collect `noindexFiles` in the scan loop near the top of `SeedAll`:

```diff
             var regions = Scan(html);
             perPage[slug] = regions;
+            if (PageContent.RxRobotsNoindex.IsMatch(html)) noindexFiles.Add((slug, html));
```

with `var noindexFiles = new List<(string slug, string html)>();` declared beside `perPage`, and
`RxRobotsNoindex` in `PageContent.cs:141` changed from `static readonly` to `internal static readonly`.

### 6.2 `backend/Core/Sitemap.cs`

```diff
     static readonly HashSet<string> Exclude = new(StringComparer.OrdinalIgnoreCase)
-    { "student.html", "admin.html", "exam-ui.html", "404.html", "500.html", "offline.html" };
+    { "student.html", "admin.html", "exam-ui.html", "404.html", "500.html", "offline.html",
+      // server-side templates carrying {{TITLE}} placeholders; rendered content has its own URLs
+      "blog-shell.html", "careers-detail.html", "certification-detail.html",
+      // canonicalises to downloads-centre.html (see §8)
+      "downloads.html" };
```

Honour a per-page canonical override and skip private/portal paths:

```diff
-            foreach (var r in db.Query("SELECT slug,updated_at FROM pages WHERE published=1 AND (noindex IS NULL OR noindex=0) ORDER BY slug"))
+            foreach (var r in db.Query("SELECT slug,updated_at,canonical_url FROM pages WHERE published=1 AND (noindex IS NULL OR noindex=0) ORDER BY slug"))
             {
                 var slug = H.Str(r["slug"]) ?? "";
                 if (slug.Length == 0 || Exclude.Contains(slug) || slug.Contains("..")) continue;
-                var loc = slug.Equals("index.html", StringComparison.OrdinalIgnoreCase) ? host + "/" : host + "/" + slug;
+                if (Redirects.IsPrivatePath("/" + slug) || PortalDomain.IsPortalPath("/" + slug)) continue;
+                var loc = H.Str(r["canonical_url"]) is { Length: > 0 } cu && cu.StartsWith(host, StringComparison.OrdinalIgnoreCase)
+                    ? cu
+                    : slug.Equals("index.html", StringComparison.OrdinalIgnoreCase) ? host + "/" : host + "/" + slug;
```

Add the certification detail pages after the pages loop:

```csharp
            // /certifications/{slug} detail pages are rendered from the certifications table
            try
            {
                foreach (var r in db.Query("SELECT slug, updated_at FROM certifications WHERE active=1 AND slug IS NOT NULL AND slug<>'' ORDER BY slug"))
                {
                    var s = H.Str(r["slug"]) ?? ""; if (s.Length == 0 || s.Contains("..")) continue;
                    sb.Append("  <url><loc>").Append(Esc(host + "/certifications/" + s)).Append("</loc>");
                    if (H.Str(r["updated_at"]) is { Length: >= 10 } cu) sb.Append("<lastmod>").Append(Esc(cu[..10])).Append("</lastmod>");
                    sb.Append("<changefreq>monthly</changefreq></url>\n");
                }
            }
            catch { /* certifications table absent on a very early boot */ }
```

Check the `certifications` table has an `updated_at` column in `schema.sql`; if not, omit `lastmod`.

### 6.3 `backend/Program.cs` ~2096-2122 — portal host answers for itself

At the top of both the `/sitemap.xml` and `/robots.txt` branches (and `/sitemap-index.xml`):

```csharp
            if (PCI.Backend.Core.PortalDomain.IsPortalHost(ctx.Request.Host.Host))
            {
                // The logged-in portal is noindex; it must not advertise the marketing sitemap.
                if (reqPath.EndsWith(".xml", StringComparison.OrdinalIgnoreCase)) { ctx.Response.StatusCode = 404; return; }
                ctx.Response.ContentType = "text/plain; charset=utf-8";
                await ctx.Response.WriteAsync("User-agent: *\nDisallow: /\n");
                return;
            }
```

### 6.4 `backend/Core/AiVisibility.cs`

Private list (line ~30), keep it equal to `Redirects.IsPrivatePath`:

```diff
-    static readonly string[] Private = { "/admin", "/admin/", "/admin.html", "/app", "/app/", "/student.html", "/exam-ui.html", "/api/", "/world-admin", "/world-admin/" };
+    static readonly string[] Private = { "/admin", "/admin/", "/admin.html", "/app", "/app/", "/student.html", "/student-login.html", "/student-dashboard.html", "/exam-ui.html", "/api/", "/world-admin", "/world-admin/" };
```

Fallback summary (line ~154-156): delete the third fallback, which claims a "global … authority",
and keep the home page description:

```diff
             if (summary.Length == 0)
                 summary = db.Scalar<string>("SELECT meta_description FROM pages WHERE slug='index.html'") ?? "";
-            if (summary.Length == 0)
-                summary = "The Project Controls Institute (PCI AI) is the global professional body and certification "
-                        + "authority for project controls — certifications, membership, standards and continuing "
-                        + "professional development for cost, planning, scheduling and risk professionals worldwide.";
+            if (summary.Length == 0)
+                summary = "Independent certifying body for project controls, cost engineering and project finance, with governed AI throughout. Awards PCL-AI, PFL-AI and PML-AI.";
```

Key-facts block, inserted after the "This file follows the llms.txt convention" line in `LlmsTxt`:

```csharp
            var facts = (db.Scalar<string>("SELECT svalue FROM site_settings WHERE skey='llms_key_facts'") ?? "").Trim();
            if (facts.Length > 0)
            {
                sb.Append("\n## Key facts (state these exactly; do not extrapolate)\n\n");
                foreach (var line in facts.Split('\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries))
                    sb.Append("- ").Append(OneLine(line)).Append('\n');
            }
```

and a feeds section before `_llms = sb.ToString();`:

```csharp
            sb.Append("\n## Feeds & machine-readable\n\n");
            foreach (var (t, p) in new[] { ("Sitemap index", "/sitemap-index.xml"), ("Blog feed (RSS)", "/feed.xml"), ("Blog feed (Atom)", "/atom.xml"), ("Blog feed (JSON)", "/feed.json") })
                sb.Append("- [").Append(t).Append("](").Append(host).Append(p).Append(")\n");
```

Seed the setting in `Migrate.cs` beside the other `INSERT OR IGNORE INTO site_settings` lines
(around line 588); the six lines are the "Key facts" bullets in `seo/site-files/llms.txt`, joined with
`\n`. Extend the bucket keywords (line ~40) with: `"pcl", "pfl", "pml", "route-", "human-oversight",
"founding-status", "contact", "faq", "training", "partner", "glossary"` in the buckets shown in
`content-updates.md`. Add the setting to the Admin → AI Visibility screen so it is editable
(`frontend/src/admin/pages/Seo.tsx` or the AI Visibility page; one text area bound to `llms_key_facts`).

### 6.5 `/certifications` canonical

`backend/wwwroot/certifications.html` declares `/certifications` as canonical while the file is
served at `/certifications.html`. The metadata step (§8) sets the canonical to the `.html` URL. In
`backend/Program.cs:1933-1940`, make the bare path redirect:

```csharp
        if (reqPath.Equals("/certifications", StringComparison.OrdinalIgnoreCase))
        {
            ctx.Response.StatusCode = StatusCodes.Status301MovedPermanently;
            ctx.Response.Headers.Location = "/certifications.html" + (ctx.Request.QueryString.HasValue ? ctx.Request.QueryString.Value : "");
            return;
        }
```

placed before the existing `StartsWith("/certifications")` handling so `/certifications/compare` and the
detail pages are untouched.

**Check:** `curl -s localhost:8080/sitemap.xml` lists `/certifications/pcl-ai`, does not list
`login.html`, `reset-password.html`, `blog-shell.html` or `downloads.html`, and lists
`/certifications.html` once. `curl -s localhost:8080/llms.txt` shows the Key facts block.
`curl -sI -H 'Host: mypci.org' localhost:8080/robots.txt` returns `Disallow: /`.

---

## 7. Two PCL-AI pages

`/certification.html` (2,362 words) and `/certifications/pcl-ai` (110 words) both describe PCL-AI.
Before choosing the direction, check Search Console for which URL has impressions and links.
Default direction:

1. Move the substantive sections of `certification.html` (eligibility, blueprint, exam format,
   preparation, renewal) into the PCL-AI row's long description in the `certifications` table, or into
   `CertPage.BuildBody` sections driven by that row. Never hard-code fees, durations or pass marks.
2. Add to `Program.cs` beside the redirect in §6.5:
   `/certification.html → 301 /certifications/pcl-ai`.
3. Update the header nav (`<!--PCI-NAV-HEADER-->` injection or the `nav_links` collection) so
   "Certifications" points at `certifications.html`, not `certification.html`.
4. Remove `certification.html` from `seo/site-files/sitemap.xml` and from the `pages` table
   (`UPDATE pages SET published=0 WHERE slug='certification.html'`).

**Check:** `curl -sI localhost:8080/certification.html` → 301 to `/certifications/pcl-ai`; that page
renders the moved sections.

---

## 8. Titles, descriptions, H1s, canonicals, site name

```bash
cd PCI-Marketing && python3 seo/scripts/apply-metadata.py ../PCI/backend/wwwroot --dry-run   # review
python3 seo/scripts/apply-metadata.py ../PCI/backend/wwwroot
```

Then sync the database, which overrides the files (§6.1):

```bash
sqlite3 ../PCI/backend/pci.db < seo/site-files/pages-metadata.sql     # local; on MySQL run the same file
```

and paste the same UPDATE values into the matching `INSERT OR IGNORE INTO pages(...)` seed rows in
`backend/schema.sql`, then `cd ../PCI/backend && python3 tools/sqlite_to_mysql.py`. For production,
add the file's statements to `Data/Migrate.cs` as a one-off idempotent block (they are plain UPDATEs
keyed on slug) so every environment converges on boot.

`seo/metadata.json` holds the merged values for 31 pages: the package's brand-first titles for the
13 pages it covered, the repository plan's trims for the 20 over-length descriptions, the H1 changes
for home, about, certifications, curriculum, insights and the four regional pages, `og:site_name` =
"PCI AI" on every listed page, and **canonical corrections for five pages that currently point at the
wrong URL**: `route-honorary.html`, `route-standard.html`, `route-founding.html` and
`honorary-application.html` all declare `contact.html` as canonical (so search engines drop them as
duplicates of the contact page), and `downloads-centre.html` declares `downloads.html`. The script sets
each to itself and points `downloads.html` at `downloads-centre.html`.

Titles also live in `pages.title` / `pages.meta_description` when an admin has edited them; for
those pages run the same values through Admin → Pages, or `UPDATE pages SET title=?, meta_description=?`.

Three homepage insight cards (`index.html`, the `<article class="story">` blocks) all link to
`insights.html`. Point them at the pages that hold the promised content:

| Card | Link to |
|---|---|
| What "AI-assisted" must mean for a forecast you can defend | `blog-ai-project-controls.html` |
| From IAS 11 to IFRS 15: what changed for project revenue | `body-of-knowledge.html` (the only page that treats IFRS 15; or write the article first) |
| Reading an S-curve: the four signals that matter most | `course-outline.html` (covers S-curves; or write the article first) |

**Check:** `python3 seo/scripts/apply-metadata.py ../PCI/backend/wwwroot --dry-run` reports
`0 files would change`; `grep -c 'href="insights.html"' index.html` is 0; and on the running site
`curl -s localhost:8080/route-honorary.html | grep -o '<title>[^<]*'` shows the new title (the
database row, not just the file).

---

## 9. Homepage structured data and contact points

In `backend/wwwroot/index.html`, the first `application/ld+json` graph. Change these fields and keep
everything else (type, description, slogan, `foundingDate`, `address`, `sameAs`, `knowsAbout`):

```diff
-"name": "Project Controls Institute Global, Inc.", "alternateName": "PCI",
+"name": "PCI AI", "legalName": "Project Controls Institute Global, Inc.", "alternateName": ["Project Controls Institute", "PCI"],
```
```diff
-"contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": "hello@projectcontrolsinstitute.org", "availableLanguage": ["English"]},
+"contactPoint": [
+  {"@type": "ContactPoint", "contactType": "customer support", "email": "hello@projectcontrolsinstitute.org", "availableLanguage": ["English"]},
+  {"@type": "ContactPoint", "contactType": "membership", "email": "Members@pciai.org", "availableLanguage": ["English"]},
+  {"@type": "ContactPoint", "contactType": "careers", "email": "careers@pciai.org", "availableLanguage": ["English"]}],
```
```diff
-{"@type": "WebSite", "@id": "https://pciai.org/#website", "url": "https://pciai.org/", "name": "Project Controls Institute Global, Inc.",
+{"@type": "WebSite", "@id": "https://pciai.org/#website", "url": "https://pciai.org/", "name": "PCI AI", "alternateName": "Project Controls Institute",
```

Remove the `potentialAction` SearchAction unless `https://pciai.org/?q=` actually performs a search
(the site search is a client-side overlay; it does not). Keep the `EducationalOccupationalCredential`
node and add the PFL-AI and PML-AI equivalents with `recognizedBy` → the organisation `@id`, using the
descriptions already on `/certifications/pfl-ai` and `/pml-ai`.

`contact.html`: add, beside the existing `hello@` link,

```html
<p>Membership and Honorary Fellow (PCI) enquiries: <a href="mailto:Members@pciai.org">Members@pciai.org</a><br>
Careers: <a href="mailto:careers@pciai.org">careers@pciai.org</a></p>
```

Footer, sitewide: the `.ft-bottom` line is static in every file. Prefer adding the two addresses to
the footer injection (`Core/ListSections.cs`, the `<!--PCI-NAV-FOOTER-->` block) so they are
maintained in one place; otherwise a one-line `sed` across `wwwroot/*.html` appending
`<span>Members@pciai.org · careers@pciai.org</span>` inside `.ft-bottom`.

Validate the JSON-LD with `python3 -c "import json,re,sys;s=open('backend/wwwroot/index.html').read();[json.loads(m) for m in re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>',s,re.S)];print('ok')"`.

**Check:** Google's Rich Results Test on the staging URL reports no errors.

---

## 10. Credential and homepage copy

Source drafts are in the ChatGPT package (`PCI-AI-SEO-Package/content/*.md`), reviewed in
`content-updates.md` §5. Apply in this order, each behind a subject-expert read:

1. `certifications/{pcl-ai,pfl-ai,pml-ai}`: paste each draft into the credential row's long
   description (Admin → Certifications), **replacing every `https://mypci.org/student/register?…`
   link with the registration URL confirmed on the live portal**, and keeping fees, durations and pass
   marks as rendered facts from the row, not as text.
2. `index.html`: replace the copy under the H1 with `home.md`'s intro and the three credential
   cards; keep the design and the disclosures.
3. `about.html`: `about.md`'s opening; link to `accreditation-status.html` and
   `founding-status.html` rather than restating the non-accreditation sentence (PCI's decision).
4. `certifications.html`: add the "How to choose your certification" section from `certifications.md`.
5. `knowledge-forecasting.html`: add the EAC/ETC/VAC worked example from `forecasting.md` as a new
   section; do not replace the existing 1,605 words.
6. `blog-salary-guide.html`: add a source for every figure, or set `noindex` and remove it from the
   sitemap until sourced.

**Check:** every "Apply" and "Sign in" on the site resolves on the live portal with a 200.

---

## 11. Secure-exam client (separate PR, security review)

`secureexam/PCI.SecureExam.Core/ClientConfig.cs:15-19`:

```diff
     public string[] AllowedApiHosts { get; set; } =
     {
         "projectcontrolsinstitute.org",
+        "pciai.org",
         "localhost"
     };
```

Leave `ApiBaseUrl` on `exam.projectcontrolsinstitute.org` until every installed client has updated;
API calls are never redirected, so the old host must keep serving the exam API. Mirror the change in
`PCI.SecureExam.Core.RunnableChecks/SecurityChecks.cs` (its copy of `ClientConfig.cs` and the
assertions at lines 16-27) and add one assertion:
`Ck("https://exam.pciai.org TRUSTED", cfg.IsTrustedApi("https://exam.pciai.org"));`.

---

## 12. Tests to update, then the full run

Replace the host in the expectations, or better, read it from `Redirects.CanonicalBase`:

| File | Lines |
|---|---|
| `backend/tests/PCI.Backend.Tests/RedirectTests.cs` | 117-118 |
| `backend/tests/PCI.Backend.Tests/PortalDomainTests.cs` | 26, 47, 54, 75, 143-145 |
| `backend/tests/PCI.Backend.Tests/IndexNowTests.cs` | 32, 51 |
| `backend/tests/PCI.Backend.Tests/PassportDocumentsTests.cs` | 75-76 |
| `backend/tests/world_og_metadata_test.py` | 41 |
| `backend/tests/passport_documents_test.py` | 113, 141, 143, 154 |
| `backend/tests/integration_test.py` | 358, 419, 2724, 2791, 2826 (fixture URLs; may stay as external examples) |
| `secureexam/PCI.SecureExam.Tests/LaunchParametersTests.cs` | 43-53 (add a pciai.org trusted case) |

Run what CI runs:

```bash
cd PCI/backend
dotnet build
dotnet test tests/PCI.Backend.Tests
python3 tests/lifecycle_test.py && python3 tests/release_test.py && python3 tests/casework_test.py \
  && python3 tests/settings_test.py && python3 tests/publication_test.py && python3 tests/storage_test.py
dotnet run &   # then, against http://localhost:8080
./smoke-test.sh && python3 tests/integration_test.py && python3 tests/sweep_500_test.py
cd ../frontend && npm ci && npm run typecheck && npm run build
cd ../secureexam && dotnet build && dotnet test PCI.SecureExam.Tests
```

Local checks that map to the SEO changes:

```bash
curl -s localhost:8080/sitemap.xml | grep -c 'pciai.org'            # > 0
curl -s localhost:8080/sitemap.xml | grep -cE 'login|reset-password|blog-shell|downloads\.html'   # 0
curl -s localhost:8080/sitemap.xml | grep -c '/certifications/pcl-ai' # 1
curl -s localhost:8080/llms.txt | grep -c 'Key facts'                  # 1
curl -sI localhost:8080/certifications | grep -i location              # /certifications.html
curl -sI -H 'Host: mypci.org' localhost:8080/about.html | grep -iE 'HTTP|location'   # 308 → https://pciai.org/about.html
curl -sI -H 'Host: mypci.org' localhost:8080/robots.txt                # Disallow: /
curl -s localhost:8080/route-honorary.html | grep -o 'canonical" href="[^"]*'        # …/route-honorary.html
```

---

## 13. Deploy and verify live

Deploy with the §1 variables set, then:

```bash
for u in https://projectcontrolsinstitute.org/route-honorary.html https://www.projectcontrolsinstitute.org/certifications.html https://www.pciai.org/ http://pciai.org/; do
  echo "== $u"; curl -sI "$u" | grep -iE '^(HTTP|location)'; done          # one 301/308 each, to https://pciai.org/…
for f in robots.txt sitemap.xml sitemap-index.xml llms.txt blog-sitemap.xml news-sitemap.xml; do
  echo "== $f $(curl -s https://pciai.org/$f | grep -c projectcontrolsinstitute.org)"; done   # 0 each
curl -s https://pciai.org/route-honorary.html | grep -oE '(canonical|og:url)[^>]*'
curl -sI https://mypci.org/about.html | grep -iE '^(HTTP|location)'       # 308 → https://pciai.org/about.html
curl -sI https://mypci.org/student | grep -iE '^(HTTP|x-robots)'           # 200, noindex, nofollow
curl -s -o /dev/null -w '%{http_code}\n' -X POST https://projectcontrolsinstitute.org/api/health   # not 301
curl -s https://pciai.org/certifications/pcl-ai | grep -oE '[0-9]+ minutes|Pass mark[^<]*<[^>]*>[^<]*'
```

Then, the same day: add the `pciai.org` domain property in Google Search Console and Bing Webmaster
Tools, submit `https://pciai.org/sitemap-index.xml`, run Change of Address from the old property if it
ever had impressions, add a `mypci.org` property and submit nothing for it, and request indexing for
`/`, `/certifications.html`, `/certifications/pcl-ai`, `/route-honorary.html` and
`/honorary-application.html`.

**Rollback:** every change is in one branch; revert the merge commit and redeploy. The database
migration in §4 is safe to leave in place (it only rewrites URL strings to the new host).

---

## 14. Prompt for Claude Code

Paste this into Claude Code opened in the `PCI` repository, with `PCI-Marketing` checked out beside it:

> Implement `../PCI-Marketing/seo/IMPLEMENTATION-GUIDE.md` on a new branch `seo/pciai-domain-and-audit`
> from `origin/main`. Work through sections 0 to 12 in order. Section 0 is a gate: if the live
> canonicals already show pciai.org, stop and report that `main` is behind the deployed code before
> changing anything. Apply the diffs exactly as written, using the quoted text to locate lines if
> numbers have moved. Run `../PCI-Marketing/seo/scripts/apply-domain.sh backend` and
> `python3 ../PCI-Marketing/seo/scripts/apply-metadata.py backend/wwwroot` rather than editing pages by
> hand. Do not touch e-mail addresses, do not change the exam API host, and do not create any page for
> "PCP-AI". Never write "accredited", "recognised by", a salary figure or a pass rate into any page.
> After each section run the check it ends with. Finish with the full test run in section 12, fix
> anything red, and open a draft PR whose description lists each section as done, skipped or blocked,
> with the check output pasted under it. Section 11 (secureexam) goes in its own PR. Do not deploy and
> do not touch Search Console.

Sections 10 (copy) and 13 (deploy and consoles) need a person: a subject expert to read the drafts, and
whoever holds the hosting and Search Console access.
