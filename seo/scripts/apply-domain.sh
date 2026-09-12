#!/usr/bin/env bash
# Replace the old web host with pciai.org across the static site and email templates.
# Leaves e-mail addresses (…@projectcontrolsinstitute.org) untouched. Idempotent.
#   usage: seo/scripts/apply-domain.sh /path/to/PCI/backend
set -uo pipefail
B="${1:?path to PCI/backend}"; NEW="https://pciai.org"
for old in 'https://www.projectcontrolsinstitute.org' 'https://projectcontrolsinstitute.org' 'http://www.projectcontrolsinstitute.org' 'http://projectcontrolsinstitute.org'; do
  { grep -rl --include="*.html" --include="*.json" --include="*.xml" --include="*.txt" --include="*.webmanifest" -F "$old" "$B/wwwroot" "$B/emails" 2>/dev/null || true; } \
    | xargs -r sed -i "s#${old//./\\.}#${NEW}#g"
done
# Plausible analytics tag: the data-domain must be the site the visits belong to
{ grep -rl --include="*.html" -F 'data-domain="projectcontrolsinstitute.org"' "$B/wwwroot" 2>/dev/null || true; } \
  | xargs -r sed -i 's#data-domain="projectcontrolsinstitute\.org"#data-domain="pciai.org"#g'
echo "remaining web-host references (should be 0):"
grep -rn --include='*.html' --include='*.json' --include='*.xml' --include='*.txt' -E 'https?://(www\.)?projectcontrolsinstitute\.org' "$B/wwwroot" "$B/emails" | wc -l
echo "bare-host mentions outside e-mail addresses (review by hand):"
grep -rn --include='*.html' -E '(^|[^@/.A-Za-z0-9-])projectcontrolsinstitute\.org' "$B/wwwroot" | grep -v '@projectcontrolsinstitute' | cut -c1-160 | head -40
