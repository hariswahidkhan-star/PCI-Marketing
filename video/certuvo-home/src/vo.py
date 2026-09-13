#!/usr/bin/env python3
"""
Narration script and captions for the Certuvo homepage film (2 minutes).

Same contract as the CMA films: SCENES of (scene id, chapter, [(caption, spoken,
end_s?), ...]); DIRECTION holds the eleven_v3 tags used to generate each take;
explicit cue ends are measured on the takes and read by sync.py.

Claims that need Certuvo's sign-off before this goes on the home page are listed
in ../claims-register.md — in particular the comparative price line in s9 and
the free-trial line in s10.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CAPDIR = os.path.normpath(os.path.join(HERE, '..', 'captions'))
NAME = 'certuvo-home'

SCENES = [
 ('s1', 'Late', [                              # presenter on camera
   ("It's late. Everyone else is asleep. And you're still here.",
    "It's late. Everyone else is asleep. And you're still here — reading the same page for the third time.", 8.30),
   ("Everyone who ever earned those letters did exactly this.",
    "I know. Because everyone who ever earned those letters did exactly this."),
 ]),
 ('s2', 'What it is worth', [
   ("A certification isn't three letters after your name.",
    "A certification isn't three letters after your name.", 3.12),
   ("It's the room you get invited into. The number on the offer.",
    "It's the room you get invited into. The number on the offer.", 7.59),
   ("The moment your judgement is the one they trust.",
    "The moment your judgement is the one they trust."),
 ]),
 ('s3', 'Ten credentials', [
   ("CMA · CPA · CFA · CIA · CISA · PMP · NCLEX-RN & PN",
    "C M A. C P A. C F A. C I A. C I S A. P M P. N C L E X — R N and P N.", 11.20),
   ("And PCI's own: Project Controls, Project Management and Project Finance Leader.",
    "And P C I's own: Project Controls Leader. Project Management Leader. Project Finance Leader.", 18.90),
   ("One platform. All of them.",
    "One platform. All of them."),
 ]),
 ('s4', 'Official partner', [
   ("Certuvo is the official training partner of PCI AI — the Project Controls Institute.",
    "And Certuvo is the official training partner of P C I A I — the Project Controls Institute."),
 ]),
 ('s5', 'Built on research', [
   ("Every course is built from research. Not recycled.",
    "Every course is built from research. Not recycled.", 3.82),
   ("Mapped to the official blueprint, in the exam's own weightings — and rewritten when the exam changes.",
    "Mapped to the official blueprint, in the exam's own weightings — and rewritten the moment the exam changes."),
 ]),
 ('s6', 'What is inside', [
   ("Verified multiple-choice questions. Full-length mock exams, under real timing.",
    "Verified multiple-choice questions. Full-length mock exams, under real timing.", 6.05),
   ("Video lectures. And course notes you'll actually keep.",
    "Video lectures. And course notes you will actually keep."),
 ]),
 ('s7', 'AI inside', [
   ("Unlimited new questions from the AI Question Forge — every one checked by four AI judges.",
    "Unlimited new questions from the A I Question Forge — every single one checked by four A I judges.", 7.10),
   ("An AI Coach you can call mid-question, in six languages. It reads your screen.",
    "An A I Coach you can call mid-question, in six languages. It reads your screen.", 13.14),
   ("And it switches itself off in a mock.",
    "And it switches itself off in a mock."),
 ]),
 ('s8', 'Not alone', [
   ("You are not doing this alone. Live study rooms with your cohort.",
    "You are not doing this alone. Live study rooms with your cohort.", 4.83),
   ("Mentors on chat, around the clock.",
    "Mentors on chat, around the clock.", 7.77),
   ("And tracking that tells you when you're ready — not just how much you've read.",
    "And tracking that tells you when you are ready — not just how much you have read."),
 ]),
 ('s9', 'The price', [
   ("All of it costs less than the market asks.",
    "And all of it costs less than the market asks.", 3.38),
   ("Because the price of preparing should never be the reason you stop.",
    "Because the price of preparing should never be the reason you stop."),
 ]),
 ('s10', 'Start free', [
   ("New here? Start with a free trial.",
    "New here? Start with a free trial.", 2.56),
   ("Open it, and see for yourself.",
    "Open it, and see for yourself."),
 ]),
 ('s11', 'One platform', [                     # presenter on camera
   ("Ten credentials. One platform. That's enough.",
    "Ten credentials. One platform. That's enough.", 4.60),
   ("Certuvo. Your exam partner.",
    "Certuvo. Your exam partner."),
 ]),
]

PRESENTER = {'s1', 's11'}

DIRECTION = {
 's1':  "[quiet, intimate, direct to camera] It's late. [pause] Everyone else is asleep. And you're still here — reading the same page for the third time. [warm, knowing, gentle smile] I know. [slower] Because everyone who ever earned those letters did exactly this.",
 's2':  "[building, resolute] A certification isn't three letters after your name. [emphasis] It's the room you get invited into. The number on the offer. [slower, weighty] The moment your judgement is the one they trust.",
 's3':  "[clear, gathering pace, proud] C M A. C P A. C F A. C I A. C I S A. P M P. N C L E X — R N and P N. [warmer] And P C I's own: Project Controls Leader. Project Management Leader. Project Finance Leader. [settled, certain] One platform. All of them.",
 's4':  "[authoritative, proud] And Certuvo is the official training partner of P C I A I — the Project Controls Institute.",
 's5':  "[deliberate, credible] Every course is built from research. [pointed] Not recycled. Mapped to the official blueprint, in the exam's own weightings — and rewritten the moment the exam changes.",
 's6':  "[clear, generous, listing] Verified multiple-choice questions. Full-length mock exams, under real timing. Video lectures. [warmer] And course notes you will actually keep.",
 's7':  "[intrigued, confident] Unlimited new questions from the A I Question Forge — [emphasis] every single one checked by four A I judges. [warm, conversational] An A I Coach you can call mid-question, in six languages. It reads your screen. [firm] And it switches itself off in a mock.",
 's8':  "[warm, human] You are not doing this alone. Live study rooms with your cohort. Mentors on chat, around the clock. [steady, reassuring] And tracking that tells you when you are ready — not just how much you have read.",
 's9':  "[direct, a little defiant] And all of it costs less than the market asks. [slower, sincere] Because the price of preparing should never be the reason you stop.",
 's10': "[bright, inviting] New here? [warm] Start with a free trial. Open it, and see for yourself.",
 's11': "[quietly certain, to camera, warm] Ten credentials. One platform. [slower, with a smile] That's enough. [gentle, final] Certuvo. Your exam partner.",
}

LEGAL = ("All third-party names and marks shown are the property of their respective owners. Certuvo is an "
         "independent preparation provider and is not affiliated with, sponsored by or endorsed by any of them, "
         "except PCI AI, whose official training partner it is. Preparation does not guarantee a pass.")


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
    md = ['# Certuvo homepage film — narration script', '', f'Legal end frame: {LEGAL}', '']
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
