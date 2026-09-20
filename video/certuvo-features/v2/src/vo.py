#!/usr/bin/env python3
"""
V2 "Card Deck" — narration and captions.

One feature per full-frame card, a strict rhythm, each card building itself and
handing off with a clean wipe. The delivery is short and declarative to match:
the film should feel like a confident keynote, not a voiceover.

Nothing on screen is a real question. Every question, option, explanation and
note is an abstract skeleton or a blurred block; see ../../claims-register.md.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CAPDIR = os.path.normpath(os.path.join(HERE, '..', 'captions'))
NAME = 'certuvo-v2-carddeck'

SCENES = [
 ('f1', 'Verified', [
   ("Thousands of verified questions. Aligned to the syllabus.",
    "Thousands of verified questions. Aligned to the syllabus."),
   ("Then unlimited more — written by AI, cleared by four judges.",
    "Then unlimited more. Written by A I. Cleared by four judges."),
 ]),
 ('f2', 'Timed', [
   ("A twenty-minute quiz. Or the full mock, at real length.",
    "A twenty-minute quiz. Or the full mock, at real length."),
   ("Same clock. Same pressure.",
    "Same clock. Same pressure."),
 ]),
 ('f3', 'Explained', [
   ("Every answer, explained.",
    "Every answer, explained."),
   ("And help on the question in front of you — not a search box.",
    "And help on the question in front of you. Not a search box."),
 ]),
 ('f4', 'Coach', [
   ("Chat. Or call.",
    "Chat. Or call."),
   ("It reads your screen, so you never describe the question.",
    "It reads your screen. So you never have to describe the question."),
 ]),
 ('f5', 'Not alone', [
   ("Study rooms. Your cohort, live.",
    "Study rooms. Your cohort, live."),
   ("Notes, kept beside the question that prompted them.",
    "And notes, kept beside the question that prompted them."),
 ]),
 ('f6', 'The gap', [
   ("Analytics that stay on what matters.",
    "Analytics that stay on what matters."),
   ("It finds the gap you keep falling into.",
    "It finds the gap you keep falling into."),
 ]),
 ('f7', 'Ready', [
   ("Progress you can see. Streaks that keep you honest.",
    "Progress you can see. Streaks that keep you honest."),
   ("Fourteen ways to get ready. One platform. Certuvo.",
    "Fourteen ways to get ready. One platform. Certuvo."),
 ]),
]

PRESENTER = set()

DIRECTION = {
 'f1': "[crisp, declarative] Thousands of verified questions. Aligned to the syllabus. [building] Then unlimited more. Written by A I. Cleared by four judges.",
 'f2': "[brisk] A twenty-minute quiz. Or the full mock, at real length. [flat, certain] Same clock. Same pressure.",
 'f3': "[clean] Every answer, explained. [pointed] And help on the question in front of you. Not a search box.",
 'f4': "[short, confident] Chat. Or call. [quietly impressed] It reads your screen. So you never have to describe the question.",
 'f5': "[warm but brisk] Study rooms. Your cohort, live. [settled] And notes, kept beside the question that prompted them.",
 'f6': "[precise] Analytics that stay on what matters. [slower, landing it] It finds the gap you keep falling into.",
 'f7': "[building] Progress you can see. Streaks that keep you honest. [final, proud] Fourteen ways to get ready. One platform. Certuvo.",
}

LEGAL = ("Product views are illustrative: every question, option, explanation and note shown is an abstract "
         "placeholder, not real exam content. All third-party names and marks are the property of their "
         "respective owners. Preparation does not guarantee a pass.")

def weight(text):
    w = len(re.findall(r"[A-Za-z0-9'’-]+", text))
    return max(1.0, w + 0.6 * text.count(',') + 1.2 * text.count('—') + 1.0 * text.count('.'))

def wrap(text, width=46):
    words = text.split(); lines, cur = [], ''
    for w in words:
        if len(cur) + len(w) + 1 > width and cur: lines.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    if cur: lines.append(cur)
    return '\n'.join(lines)

def strip_tags(s): return re.sub(r'\s+', ' ', re.sub(r'\[[^\]]*\]', ' ', s)).strip()

def check_direction():
    norm = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    for sid, _, segs in SCENES:
        want = norm(' '.join(sp for _, sp, *_ in segs))
        got = norm(strip_tags(DIRECTION[sid]))
        if want != got: raise SystemExit(f'{sid}: DIRECTION differs\n want: {want}\n  got: {got}')

def _measured():
    p = os.path.join(HERE, 'timeline.json')
    return json.load(open(p)) if os.path.exists(p) else None

def segments():
    return [(sid, chap, seg[0], seg[1]) for sid, chap, segs in SCENES for seg in segs]

def timings():
    m = _measured()
    if not m: raise SystemExit('run sync.py first — timeline.json is missing')
    return m['captions']

def ts(x, comma=True):
    h = int(x // 3600); m = int((x % 3600) // 60); s = x % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.', ',' if comma else '.')

def main():
    check_direction()
    caps = timings(); os.makedirs(CAPDIR, exist_ok=True)
    open(os.path.join(CAPDIR, f'{NAME}.srt'), 'w', encoding='utf-8').write(
        '\n'.join(f"{i}\n{ts(a)} --> {ts(b)}\n{c}\n" for i, (a, b, c) in enumerate(caps, 1)))
    open(os.path.join(CAPDIR, f'{NAME}.vtt'), 'w', encoding='utf-8').write(
        '\n'.join(['WEBVTT', ''] + [f"{ts(a,False)} --> {ts(b,False)}\n{c}\n" for a, b, c in caps]))
    open(os.path.join(HERE, 'captions.data.js'), 'w', encoding='utf-8').write(
        '/* GENERATED by vo.py — do not edit. */\nwindow.__CAPTIONS = ' + json.dumps(caps) + ';\n')
    md = [f'# {NAME} — narration', '', f'Legal end frame: {LEGAL}', '']
    for sid, chap, segs in SCENES:
        md.append(f'## {sid} · {chap}')
        md += [f'- {s[1]}' for s in segs] + ['']
    open(os.path.join(CAPDIR, 'vo-script.md'), 'w', encoding='utf-8').write('\n'.join(md))
    print(f'segments {len(caps)} | ~{sum(len(sp.split()) for _,_,_,sp in segments())} words | {caps[-1][1]:.2f}s')

if __name__ == '__main__':
    if os.environ.get('CHECK_ONLY'): check_direction(); print('direction ok'); raise SystemExit
    main()
