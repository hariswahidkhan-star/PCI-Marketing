#!/usr/bin/env python3
"""
V1 "Walkthrough" — narration and captions.

A guided tour of one product surface: a rail of every feature stays on screen
while the pane beside it demonstrates them two at a time. Calm, second person,
no hard sell — the film is a demonstration, not a pitch.

Nothing on screen is a real question. Every question, option, explanation and
note is an abstract skeleton or a blurred block; see ../../claims-register.md.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CAPDIR = os.path.normpath(os.path.join(HERE, '..', 'captions'))
NAME = 'certuvo-v1-walkthrough'

SCENES = [
 ('f1', 'The bank', [
   ("Thousands of verified questions, aligned to the syllabus.",
    "Inside every course: thousands of verified questions, aligned to the syllabus."),
   ("And when you've worked through them, more — each one through four stages of validation.",
    "And when you have worked through them, the A I writes more — every one of them through four stages of validation."),
 ]),
 ('f2', 'Under timing', [
   ("Timed quizzes, when you have twenty minutes.",
    "Timed quizzes, for when you have twenty minutes."),
   ("Full mock exams, when you're ready for the real length.",
    "Full mock exams, for when you are ready for the real length."),
 ]),
 ('f3', 'Why, not just what', [
   ("Every answer comes with the explanation.",
    "Every answer comes with the explanation."),
   ("And on any question, help on that question — not a search box.",
    "And on any question, you can ask for help on that question. Not a search box. That one."),
 ]),
 ('f4', 'The Coach', [
   ("Chat with your AI Coach, or call it and keep walking.",
    "Chat with your A I Coach. Or call it, and keep walking."),
   ("It reads your screen, so you never describe what you're looking at.",
    "It reads your screen — so you never have to describe what you are looking at."),
 ]),
 ('f5', 'Together, and in one place', [
   ("Study rooms with your cohort, live.",
    "Study rooms with your cohort. Live."),
   ("And your notes in the same place as the questions that prompted them.",
    "And your notes in the same place as the questions that prompted them."),
 ]),
 ('f6', 'What it finds', [
   ("Analytics that stay on what matters.",
    "Analytics that stay on what matters."),
   ("Certuvo finds the gap you keep falling into, and says so.",
    "Certuvo finds the gap you keep falling into — and says so."),
 ]),
 ('f7', 'Where you are', [
   ("Progress you can see. Streaks that keep you honest.",
    "Progress you can see. And streaks that keep you honest."),
   ("One platform. Certuvo.",
    "One platform. Certuvo."),
 ]),
]

PRESENTER = set()

DIRECTION = {
 'f1': "[calm, assured, guiding] Inside every course: thousands of verified questions, aligned to the syllabus. [warmer] And when you have worked through them, the A I writes more — [precise] every one of them through four stages of validation.",
 'f2': "[even, practical] Timed quizzes, for when you have twenty minutes. [a touch weightier] Full mock exams, for when you are ready for the real length.",
 'f3': "[clear] Every answer comes with the explanation. [leaning in] And on any question, you can ask for help on that question. [pointed] Not a search box. That one.",
 'f4': "[warm, conversational] Chat with your A I Coach. Or call it, and keep walking. [quietly impressed] It reads your screen — so you never have to describe what you are looking at.",
 'f5': "[warm] Study rooms with your cohort. Live. [settled] And your notes in the same place as the questions that prompted them.",
 'f6': "[precise, confident] Analytics that stay on what matters. [slower, pointed] Certuvo finds the gap you keep falling into — and says so.",
 'f7': "[building, warm] Progress you can see. And streaks that keep you honest. [final, certain] One platform. Certuvo.",
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
