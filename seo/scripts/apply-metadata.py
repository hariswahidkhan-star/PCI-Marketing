#!/usr/bin/env python3
"""Apply titles, meta descriptions, OG/Twitter tags, og:site_name and (optionally) H1 text
from metadata.json to the static pages. Idempotent; prints what changed.
    usage: python3 seo/scripts/apply-metadata.py /path/to/PCI/backend/wwwroot [--dry-run]
"""
import json, re, sys, os, html
root = sys.argv[1]; dry = '--dry-run' in sys.argv
data = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'metadata.json')))
def esc(s): return html.escape(s, quote=True)
changed = 0
for slug, m in data['pages'].items():
    path = os.path.join(root, slug)
    if not os.path.exists(path): print(f'SKIP {slug}: not a static file (dynamic route?)'); continue
    s = open(path, encoding='utf-8').read(); orig = s
    if 'title' in m:
        s = re.sub(r'<title>[^<]*</title>', f'<title>{esc(m["title"])}</title>', s, count=1)
        s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda x: x.group(1)+esc(m["title"])+x.group(2), s, count=1)
        s = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', lambda x: x.group(1)+esc(m["title"])+x.group(2), s, count=1)
    if 'description' in m:
        assert len(m['description']) <= 155, (slug, len(m['description']))
        for pat in (r'(<meta name="description" content=")[^"]*(")', r'(<meta property="og:description" content=")[^"]*(")', r'(<meta name="twitter:description" content=")[^"]*(")'):
            s = re.sub(pat, lambda x: x.group(1)+esc(m["description"])+x.group(2), s, count=1)
    if data.get('og_site_name'):
        s = re.sub(r'(<meta property="og:site_name" content=")[^"]*(")', lambda x: x.group(1)+esc(data["og_site_name"])+x.group(2), s, count=1)
    if m.get('canonical') == 'self':
        own = data['host'] + '/' + ('' if slug == 'index.html' else slug)
        s = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda x: x.group(1)+own+x.group(2), s, count=1)
        s = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda x: x.group(1)+own+x.group(2), s, count=1)
    elif 'canonical' in m:
        s = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda x: x.group(1)+m['canonical']+x.group(2), s, count=1)
    if 'h1' in m:
        s = re.sub(r'(<h1[^>]*>)(.*?)(</h1>)', lambda x: x.group(1)+m['h1']+x.group(3), s, count=1, flags=re.S)
    if s != orig:
        changed += 1; print(f'UPDATE {slug}')
        if not dry: open(path, 'w', encoding='utf-8').write(s)
print(f'{changed} files {"would change" if dry else "changed"}')
