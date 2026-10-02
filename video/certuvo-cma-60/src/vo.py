#!/usr/bin/env python3
"""
Narration script and captions for the one-minute Certuvo features cut.

Same contract as ../../certuvo-cma/src/vo.py: SCENES of (scene id, chapter,
[(caption, spoken, end_s?), ...]); DIRECTION carries the eleven_v3 tags used to
generate the takes; explicit cue ends are measured on the takes (sync.py).
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CAPDIR = os.path.normpath(os.path.join(HERE, '..', 'captions'))
NAME = 'certuvo-cma-60'

SCENES = [
 ('s1', 'Hook', [                              # presenter on camera
   ("Preparing for the CMA? Here's how Certuvo gets you ready.",
    "Preparing for the CMA? Here's how Certuvo gets you ready."),
 ]),
 ('s2', 'What you get', [
   ("Practice exams that mirror the real format · timed quizzes · full-length mocks.",
    "Practice exams that mirror the real format, with timed quizzes and full-length mocks.", 5.84),
   ("Progress tracking that finds your gaps and tells you when you're ready.",
    "Progress tracking that finds your gaps and tells you when you're ready.", 10.76),
   ("Live study rooms with your cohort · 24/7 chat support from experienced mentors.",
    "Live study rooms with your cohort. And twenty-four seven chat support from experienced mentors."),
 ]),
 ('s3', 'AI inside', [
   ("AI Question Forge: unlimited new questions, each one checked by four AI judges.",
    "The AI Question Forge writes unlimited new questions — each one checked by four AI judges.", 7.13),
   ("AI Coach: chat or call it during practice, in six languages.",
    "And your AI Coach: chat or call it during practice, in six languages.", 12.68),
   ("It reads your screen — and switches itself off during mock exams.",
    "It reads your screen — and switches itself off during mock exams."),
 ]),
 ('s4', 'Start', [                             # presenter on camera
   ("Pick your part. Start today — at certuvo.com",
    "Pick your part. Start today — at certuvo dot com."),
 ]),
]

PRESENTER = {'s1', 's4'}

DIRECTION = {
 's1': "[warm, direct to camera] Preparing for the CMA? [confident] Here's how Certuvo gets you ready.",
 's2': "[clear, structured] Practice exams that mirror the real format, with timed quizzes and full-length mocks. [steady] Progress tracking that finds your gaps and tells you when you're ready. [warm] Live study rooms with your cohort. And twenty-four seven chat support from experienced mentors.",
 's3': "[intrigued] The AI Question Forge writes unlimited new questions — [emphasis] each one checked by four AI judges. [warm, conversational] And your AI Coach: chat or call it during practice, in six languages. It reads your screen — [firm] and switches itself off during mock exams.",
 's4': "[direct, encouraging, to camera] Pick your part. Start today — [clear] at certuvo dot com.",
}

LEGAL = ("CMA® is a registered trademark of the Institute of Management Accountants (IMA). Certuvo is an "
         "independent preparation provider and is not affiliated with, sponsored by or endorsed by IMA. "
         "Preparation does not guarantee a pass.")


def weight(text):
    w = len(re.findall(r"[A-Za-z0-9'’-]+", text))
    return max(1.0, w + 0.6 * text.count(',') + 1.2 * text.count('—') + 1.0 * text.count('.'))


def wrap(text, width=46):
    words = text.split(); lines, cur = [], ''
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur: lines.append(cur)
    return '\n'.join(lines)


def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'\[[^\]]*\]', ' ', s)).strip()


def check_direction():
    norm = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    for sid, _, segs in SCENES:
        want = norm(' '.join(sp for _, sp, *_ in segs))
        got = norm(strip_tags(DIRECTION[sid]))
        if want != got:
            raise SystemExit(f'{sid}: DIRECTION words differ from SCENES\n want: {want}\n  got: {got}')


def _measured():
    p = os.path.join(HERE, 'timeline.json')
    return json.load(open(p)) if os.path.exists(p) else None


def segments():
    out = []
    for sid, chap, segs in SCENES:
        for seg in segs:
            out.append((sid, chap, seg[0], seg[1]))
    return out


def timings():
    m = _measured()
    if not m: raise SystemExit('run sync.py first — timeline.json is missing')
    return m['captions']


def ts(x, comma=True):
    h = int(x // 3600); m = int((x % 3600) // 60); s = x % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.', ',' if comma else '.')


def main():
    check_direction()
    caps = timings()
    os.makedirs(CAPDIR, exist_ok=True)
    srt = []
    for i, (a, b, cap) in enumerate(caps, 1):
        srt.append(f"{i}\n{ts(a)} --> {ts(b)}\n{cap}\n")
    open(os.path.join(CAPDIR, f'{NAME}.srt'), 'w', encoding='utf-8').write('\n'.join(srt))
    vtt = ['WEBVTT', '']
    for a, b, cap in caps:
        vtt.append(f"{ts(a, False)} --> {ts(b, False)}\n{cap}\n")
    open(os.path.join(CAPDIR, f'{NAME}.vtt'), 'w', encoding='utf-8').write('\n'.join(vtt))
    open(os.path.join(HERE, 'captions.data.js'), 'w', encoding='utf-8').write(
        '/* GENERATED by vo.py — do not edit. */\nwindow.__CAPTIONS = ' + json.dumps(caps) + ';\n')
    md = ['# Certuvo features cut (60 s) — narration script', '', f'Legal end frame: {LEGAL}', '']
    for sid, chap, segs in SCENES:
        md.append(f'## {sid} · {chap}' + (' · presenter on camera' if sid in PRESENTER else ''))
        for seg in segs: md.append(f'- {seg[1]}')
        md.append('')
    open(os.path.join(CAPDIR, 'vo-script.md'), 'w', encoding='utf-8').write('\n'.join(md))
    words = sum(len(sp.split()) for _, _, _, sp in segments())
    print(f'segments {len(caps)} | ~{words} words | {caps[-1][1]:.2f}s')


if __name__ == '__main__':
    if os.environ.get('CHECK_ONLY'):
        check_direction(); print('direction ok'); raise SystemExit
    main()
