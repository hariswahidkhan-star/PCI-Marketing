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
 # s1 and s11 are deliberately word-for-word unchanged from the previous cut, so
 # both presenter takes and both HeyGen clips are reused rather than re-rendered.
 ('s1', 'Late', [                              # presenter on camera — take reused
   ("It's late. Everyone else is asleep. And you're still here.",
    "It's late. Everyone else is asleep. And you're still here — reading the same page for the third time.", 8.30),
   ("Everyone who ever earned those letters did exactly this.",
    "I know. Because everyone who ever earned those letters did exactly this."),
 ]),
 ('s2', 'The difference', [
   ("Here's the thing nobody tells you.",
    "But here's the thing nobody tells you.", 2.30),
   ("The people who pass and the people who keep re-sitting aren't divided by effort.",
    "The difference between the people who pass and the people who keep re-sitting isn't how hard they work.", 8.40),
   ("They all work hard.",
    "They all work hard."),
 ]),
 ('s3', 'Ten credentials', [
   # NCLEX is a word, not seven letters. Spelled out it was simply wrong.
   ("CMA · CPA · CFA · CIA · CISA · PMP · NCLEX-RN & PN",
    "C M A. C P A. C F A. C I A. C I S A. P M P. En-clex — R N and P N.", 11.60),
   ("And PCI's own: Project Controls, Project Management and Project Finance Leader.",
    "And P C I's own: Project Controls Leader. Project Management Leader. Project Finance Leader.", 19.70),
   ("Ten credentials. One platform.",
    "Ten credentials. One platform."),
 ]),
 ('s4', 'Official partner', [
   ("Certuvo is the official training partner of PCI AI — the Project Controls Institute.",
    "And Sertoovo is the official training partner of P C I A I — the Project Controls Institute."),
 ]),
 ('s5', 'Already inside', [
   ("Inside every course: thousands of verified questions.",
    "Inside every course: thousands of verified questions.", 3.75),
   ("Full mock exams under real timing. Video lectures. Course notes you'll actually keep.",
    "Full-length mock exams, under real timing. Video lectures. Course notes you will actually keep.", 10.95),
   ("Built from research. Mapped to the official blueprint, in the exam's own weightings.",
    "Built from research. Mapped to the official blueprint, in the exam's own weightings."),
 ]),
 ('s6', 'Four judges', [
   ("And when you've worked through them, the AI Question Forge writes more.",
    "And when you have worked through them, the A I Question Forge writes more.", 4.30),
   ("Unlimited new questions — and not one reaches you until it has passed four AI judges.",
    "Unlimited new questions — and not one reaches you until it has passed four A I judges.", 10.80),
   ("Generated. Answer verified. Checked for ambiguity. Matched to the blueprint.",
    "Generated. Answer verified. Checked for ambiguity. Matched to the blueprint."),
 ]),
 ('s7', 'AI Coach', [
   ("Stuck at eleven at night? Call your AI Coach.",
    "Stuck, at eleven at night? Call your A I Coach.", 4.05),
   ("It reads your screen — the question, the numbers, every option.",
    "It reads your screen. The question, the numbers, every option.", 8.60),
   ("It answers with a question, so you leave with the method — not the answer.",
    "And it answers with a question — so you leave with the method, not the answer.", 14.30),
   ("Then, in a mock exam, it switches itself off.",
    "Then, in a mock exam, it switches itself off."),
 ]),
 # s8 is the corrected feature. There are no chat rooms; there is a peer study
 # session where two students share one screen, and either can bring a friend.
 ('s8', 'Study with a peer', [
   ("When you want another mind on it — study with a peer.",
    "And when you want another mind on it — study with a peer.", 3.20),
   ("Share your screen, live. The same question, the same numbers, at the same second.",
    "Share your screen, live. The same question, the same numbers, at the same second.", 9.70),
   ("Bring a friend in. Two of you, one problem, until it gives.",
    "Bring a friend in. Two of you, one problem — until it gives."),
 ]),
 ('s9', 'Readiness', [
   ("Every question you answer moves a line.",
    "And every question you answer moves a line.", 3.10),
   ("Certuvo tracks every domain, and finds the gap you keep falling into.",
    "Sertoovo tracks every domain, and finds the gap you keep falling into.", 8.25),
   ("Not how much you've read. Whether you're ready.",
    "Not how much you have read. Whether you are ready."),
 ]),
 ('s10', 'Start free', [
   ("All of it, for less than the market asks.",
    "All of it, for less than the market asks.", 3.15),
   ("And if you're new — start free. Open it, and see.",
    "And if you are new — start free. Open it, and see for yourself."),
 ]),
 ('s11', 'What you work with', [               # presenter on camera — take reused
   ("So — the difference?",
    "So. The difference?", 1.95),
   ("It was never how hard you work. It's what you work with.",
    "It was never how hard you work. It's what you work with.", 6.70),
   ("Ten credentials. One platform. That's enough.",
    "Ten credentials. One platform. That's enough.", 11.80),
   ("Certuvo. Your exam partner.",
    "Certuvo. Your exam partner."),
 ]),
]

PRESENTER = {'s1', 's11'}

DIRECTION = {
 's1':  "[quiet, intimate, direct to camera] It's late. [pause] Everyone else is asleep. And you're still here \u2014 reading the same page for the third time. [warm, knowing, gentle smile] I know. [slower] Because everyone who ever earned those letters did exactly this.",
 's2':  "[lowered, confiding, leaning in] But here's the thing nobody tells you. [measured] The difference between the people who pass and the people who keep re-sitting isn't how hard they work. [flat, certain, a beat of silence after] They all work hard.",
 's3':  "[clear, gathering pace, proud] C M A. C P A. C F A. C I A. C I S A. P M P. En-clex \u2014 R N and P N. [warmer] And P C I's own: Project Controls Leader. Project Management Leader. Project Finance Leader. [settled, certain] Ten credentials. One platform.",
 's4':  "[authoritative, proud] And Sertoovo is the official training partner of P C I A I \u2014 the Project Controls Institute.",
 's5':  "[opening up, generous] Inside every course: thousands of verified questions. [listing, unhurried] Full-length mock exams, under real timing. Video lectures. Course notes you will actually keep. [deliberate, credible] Built from research. Mapped to the official blueprint, in the exam's own weightings.",
 's6':  "[intrigued, confident] And when you have worked through them, the A I Question Forge writes more. [emphasis] Unlimited new questions \u2014 and not one reaches you until it has passed four A I judges. [crisp, ticking them off] Generated. Answer verified. Checked for ambiguity. Matched to the blueprint.",
 's7':  "[wry, understanding] Stuck, at eleven at night? [warm] Call your A I Coach. [conversational] It reads your screen. The question, the numbers, every option. [quietly impressed] And it answers with a question \u2014 so you leave with the method, not the answer. [firm, a little proud] Then, in a mock exam, it switches itself off.",
 's8':  "[warm, opening out] And when you want another mind on it \u2014 study with a peer. [precise, a little marvelling] Share your screen, live. The same question, the same numbers, at the same second. [warm, human, smiling] Bring a friend in. Two of you, one problem \u2014 until it gives.",
 's9':  "[building, precise] And every question you answer moves a line. Sertoovo tracks every domain, and finds the gap you keep falling into. [slower, landing it] Not how much you have read. [emphasis] Whether you are ready.",
 's10': "[direct, a little defiant] All of it, for less than the market asks. [bright, inviting] And if you are new \u2014 start free. Open it, and see for yourself.",
 's11': "[quiet, to camera, a small smile] So. The difference? [slower, certain] It was never how hard you work. [emphasis] It's what you work with. [warm, final] Ten credentials. One platform. That's enough. [gentle] Certuvo. Your exam partner.",
}

LEGAL = ("All third-party names and marks shown are the property of their respective owners. Certuvo is an "
         "independent preparation provider and is not affiliated with, sponsored by or endorsed by any of them, "
         "except PCI AI, whose official training partner it is. On-screen product views are illustrative. "
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
