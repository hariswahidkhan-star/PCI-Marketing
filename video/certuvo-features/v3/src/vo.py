#!/usr/bin/env python3
"""
V3 "One Session" — narration and captions.

One evening of study, told in order: sit down, quiz, get one wrong, call the
Coach, join the room, and find out what the platform noticed. Features arrive
where a student would actually meet them rather than in a list.

Nothing on screen is a real question. Every question, option, explanation and
note is an abstract skeleton or a blurred block; see ../../claims-register.md.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CAPDIR = os.path.normpath(os.path.join(HERE, '..', 'captions'))
NAME = 'certuvo-v3-onesession'

SCENES = [
 ('f1', 'Sit down', [
   ("Nine at night. You open Certuvo.",
    "Nine at night. You open Certuvo."),
   ("Thousands of verified questions are already there, aligned to your syllabus.",
    "Thousands of verified questions are already there, aligned to your syllabus."),
 ]),
 ('f2', 'Twenty minutes', [
   ("You start with a timed quiz. Twenty minutes.",
    "You start with a timed quiz. Twenty minutes."),
   ("Later in the week, the full mock, at the real length.",
    "Later in the week, you will do the full mock, at the real length."),
 ]),
 ('f3', 'You get one wrong', [
   ("You get one wrong. The explanation is right there.",
    "You get one wrong. The explanation is right there."),
   ("Still not sure? Ask for help on that question. That one.",
    "Still not sure? You ask for help on that question. That one."),
 ]),
 ('f4', 'You call', [
   ("So you call your AI Coach, and keep pacing.",
    "So you call your A I Coach — and keep pacing."),
   ("It's reading your screen. You never describe a thing.",
    "It is already reading your screen. You never describe a thing."),
 ]),
 ('f5', 'You are not alone', [
   ("Your cohort is in a study room. You join for twenty minutes.",
    "Your cohort is in a study room. You join for twenty minutes."),
   ("What you learn goes into your notes, beside the question.",
    "And what you learn goes into your notes, beside the question that prompted it."),
 ]),
 ('f6', 'What it noticed', [
   ("Certuvo has been watching one thing all evening.",
    "And Certuvo has been watching one thing all evening."),
   ("The same gap, three nights running. Now you know.",
    "The same gap. Three nights running. Now you know."),
 ]),
 ('f7', 'Close the laptop', [
   ("Progress up. Streak intact.",
    "Progress up. Streak intact."),
   ("Tomorrow, the same place. Certuvo.",
    "Tomorrow, the same place. Certuvo."),
 ]),
]

PRESENTER = set()

DIRECTION = {
 'f1': "[quiet, intimate, scene-setting] Nine at night. You open Certuvo. [warmer] Thousands of verified questions are already there, aligned to your syllabus.",
 'f2': "[matter of fact] You start with a timed quiz. Twenty minutes. [forward-looking] Later in the week, you will do the full mock, at the real length.",
 'f3': "[wry, understanding] You get one wrong. [reassuring] The explanation is right there. [leaning in] Still not sure? You ask for help on that question. That one.",
 'f4': "[conversational] So you call your A I Coach — and keep pacing. [quietly impressed] It is already reading your screen. You never describe a thing.",
 'f5': "[warm] Your cohort is in a study room. You join for twenty minutes. [settled] And what you learn goes into your notes, beside the question that prompted it.",
 'f6': "[lowered, a little conspiratorial] And Certuvo has been watching one thing all evening. [slower, pointed] The same gap. Three nights running. [certain] Now you know.",
 'f7': "[quiet satisfaction] Progress up. Streak intact. [warm, final] Tomorrow, the same place. Certuvo.",
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
