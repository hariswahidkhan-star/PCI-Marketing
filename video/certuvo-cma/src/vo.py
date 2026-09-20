#!/usr/bin/env python3
"""
Narration script and captions for the Certuvo CMA film ("The CMA, Part 1 and Part 2").

SCENES: (scene id, chapter, [(caption, spoken, end_s?), ...]). Captions are what the
viewer reads; `spoken` is what the narrator says (numbers spelled the way Nassim
should read them). An optional third element is the measured end of the cue inside
its take, in seconds — filled in after the takes exist (see sync.py).

DIRECTION: the same spoken text with eleven_v3 audio tags, one entry per scene, used
only to generate the takes. Tags never reach the captions.

Facts are from IMA's published CMA structure as reported in September 2026 by
multiple preparation providers (the IMA site is not reachable from the build
environment); every figure is listed in ../claims-register.md with its source and
must be re-checked against imanet.org before publication.

Emits ../captions/*.srt|.vtt, captions.data.js and ../captions/vo-script.md.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CAPDIR = os.path.normpath(os.path.join(HERE, '..', 'captions'))
NAME = 'certuvo-cma'

SCENES = [
 ('s1', 'Hook', [
   ("Two exams. Four hours each.",
    "Two exams. Four hours each."),
   ("One credential that says you can plan, control, analyse — and decide.",
    "One credential that says you can plan, control, analyse… and decide."),
 ]),
 ('s2', 'Welcome', [                          # presenter on camera
   ("Welcome to Certuvo. In the next three minutes: the CMA, exactly as it stands in 2026.",
    "Welcome to Certuvo. In the next three minutes, I'll walk you through the Certified Management Accountant — the CMA — exactly as it stands in 2026."),
   ("What's in Part 1. What's in Part 2. How the exam works. How to be ready.",
    "What's in Part One. What's in Part Two. How the exam works. And how to prepare so that, on the day, nothing surprises you."),
 ]),
 ('s3', 'What the CMA is', [
   ("Awarded by IMA, the Institute of Management Accountants, since 1972.",
    "The CMA is awarded by IMA — the Institute of Management Accountants. It has been earned since 1972, when the first sixty-one candidates passed."),
   ("The credential for management accounting: planning, budgeting, performance, risk, strategy.",
    "It is the credential for management accounting: the people who plan, budget, measure performance, manage risk and support strategy — not just report what already happened."),
 ]),
 ('s4', 'Part 1', [
   ("Part 1 — Financial Planning, Performance and Analytics. Six domains.",
    "Part One is Financial Planning, Performance and Analytics. Six domains.", 5.45),
   ("External Financial Reporting Decisions 15% · Planning, Budgeting and Forecasting 20% · Performance Management 20%",
    "External Financial Reporting Decisions, fifteen per cent. Planning, Budgeting and Forecasting, twenty. Performance Management, twenty.", 15.42),
   ("Cost Management 15% · Internal Controls 15% · Technology and Analytics 15%",
    "Cost Management, fifteen. Internal Controls, fifteen. And Technology and Analytics, fifteen.", 23.51),
   ("Part 1 is the engine room: how the numbers are built, budgeted, measured and controlled.",
    "Think of Part One as the engine room: how the numbers are built, budgeted, measured and controlled."),
 ]),
 ('s5', 'Part 2', [
   ("Part 2 — Strategic Financial Management. Six domains.",
    "Part Two is Strategic Financial Management. Six domains again.", 4.56),
   ("Financial Statement Analysis 20% · Corporate Finance 20% · Decision Analysis 25%",
    "Financial Statement Analysis, twenty per cent. Corporate Finance, twenty. Decision Analysis — the largest single domain — twenty-five.", 14.72),
   ("Risk Management 10% · Investment Decisions 10% · Professional Ethics 15%",
    "Risk Management, ten. Investment Decisions, ten. And Professional Ethics, fifteen.", 22.13),
   ("Part 2 is the boardroom: what the numbers mean, and what you decide because of them.",
    "Part Two is the boardroom: what the numbers mean, and what you decide because of them."),
 ]),
 ('s6', 'The exam', [
   ("Each part: 4 hours. 100 multiple-choice questions in 3 hours — 75% of the score.",
    "Each part is a four-hour exam. One hundred multiple-choice questions in three hours — seventy-five per cent of your score."),
   ("Then 1 hour: from the September 2026 window, two case-based questions replace the essays.",
    "Then one hour for the second section. From the September 2026 window, two case-based questions replace the old essays: a short business case, then up to seven questions on it."),
   ("At least 50% on the multiple choice unlocks the second section. Pass mark: 360 of 500.",
    "You need at least fifty per cent on the multiple choice to unlock that section. The pass mark is three hundred and sixty out of five hundred."),
   ("Three windows a year: Jan–Feb · May–Jun · Sep–Oct",
    "Three testing windows a year: January to February, May to June, September to October."),
 ]),
 ('s7', 'Requirements', [
   ("To be certified: IMA membership · a bachelor's degree or approved certification · 2 years' relevant experience",
    "To be certified, you need an active IMA membership, a bachelor's degree or an approved professional certification, and two continuous years of relevant experience."),
   ("The experience can be completed up to 7 years after passing — so you can sit the exam first.",
    "And the experience can be completed up to seven years after you pass. So you can sit the exam first, and finish the experience later."),
 ]),
 ('s8', 'Why it matters', [
   ("IMA Global Salary Survey 2023: CMAs' median total compensation 21% higher than non-CMAs worldwide.",
    "IMA's own Global Salary Survey reports that CMAs earn more than their non-certified peers — twenty-one per cent higher median total compensation worldwide, in the 2023 survey."),
   ("The roles follow: FP&A · controller · finance business partner · the route to CFO.",
    "And the roles follow: financial planning and analysis, controller, finance business partner — and the route to CFO."),
 ]),
 ('s9', 'How Certuvo prepares you', [
   ("Certuvo prepares you for exactly this exam.",
    "Certuvo prepares you for exactly this exam.", 3.08),
   ("Practice exams: scenario-based questions in the real format · timed quizzes · full-length mocks.",
    "Practice exams: scenario-based questions in the real format, with timed quizzes and full-length mock exams that simulate the testing experience.", 13.24),
   ("Progress tracking: your strengths, your gaps, and when you're ready.",
    "Progress tracking that shows your strengths, finds your knowledge gaps, and tells you when you're ready.", 19.62),
   ("Live study rooms with your cohort · 24/7 chat support from experienced mentors.",
    "Live study rooms, where you practise with your cohort in real time. And twenty-four seven chat support from experienced mentors."),
 ]),
 ('s10', 'AI inside', [
   ("AI Question Forge: unlimited new questions on any topic, validated by four AI judges.",
    "Then the AI. Certuvo's Question Forge writes unlimited new questions on any topic — and every one passes a panel of four AI judges before you ever see it.", 11.59),
   ("AI Coach: chat or call during practice, in six languages. It reads your screen.",
    "And your AI Coach: chat or call it during practice, in six languages. It reads the question on your screen, and teaches you to think — not memorise.", 21.95),
   ("Auto-disabled during mock exams. Practise with help. Test without it.",
    "During mock exams it switches itself off. Practise with help. Test without it."),
 ]),
 ('s11', 'Start', [                           # presenter on camera
   ("Pick your part. Choose a testing window. Start preparing with Certuvo today.",
    "Pick your part. Choose a testing window. And start preparing with Certuvo today."),
   ("certuvo.com",
    "certuvo dot com."),
   ("The exam is hard by design. Being ready for it doesn't have to be.",
    "The exam is hard by design. Being ready for it… doesn't have to be."),
 ]),
]

# Scenes delivered by the on-camera presenter (the rest are motion graphics).
PRESENTER = {'s2', 's11'}

# eleven_v3 direction: the spoken lines of each scene with audio tags. Words match
# SCENES exactly once the tags are stripped (checked by build).
DIRECTION = {
 's1':  "[confident, low, deliberate] Two exams. Four hours each. [pause] [rising, assured] One credential that says you can plan, control, analyse… [beat] and decide.",
 's2':  "[warm, welcoming, direct to camera] Welcome to Certuvo. In the next three minutes, I'll walk you through the Certified Management Accountant — the CMA — exactly as it stands in 2026. [clear, measured] What's in Part One. What's in Part Two. How the exam works. [reassuring] And how to prepare so that, on the day, nothing surprises you.",
 's3':  "[authoritative, steady] The CMA is awarded by IMA — the Institute of Management Accountants. It has been earned since 1972, when the first sixty-one candidates passed. [thoughtful, building] It is the credential for management accounting: the people who plan, budget, measure performance, manage risk and support strategy — [pointed] not just report what already happened.",
 's4':  "[clear, structured] Part One is Financial Planning, Performance and Analytics. Six domains. [even, listing, slight pause between items] External Financial Reporting Decisions, fifteen per cent. Planning, Budgeting and Forecasting, twenty. Performance Management, twenty. Cost Management, fifteen. Internal Controls, fifteen. And Technology and Analytics, fifteen. [warm, summarising] Think of Part One as the engine room: how the numbers are built, budgeted, measured and controlled.",
 's5':  "[clear, structured] Part Two is Strategic Financial Management. Six domains again. [even, listing] Financial Statement Analysis, twenty per cent. Corporate Finance, twenty. Decision Analysis — [emphasis] the largest single domain — twenty-five. Risk Management, ten. Investment Decisions, ten. And Professional Ethics, fifteen. [warm, summarising] Part Two is the boardroom: what the numbers mean, and what you decide because of them.",
 's6':  "[practical, precise] Each part is a four-hour exam. One hundred multiple-choice questions in three hours — seventy-five per cent of your score. [attentive] Then one hour for the second section. From the September 2026 window, two case-based questions replace the old essays: a short business case, then up to seven questions on it. [firm] You need at least fifty per cent on the multiple choice to unlock that section. The pass mark is three hundred and sixty out of five hundred. [brisk] Three testing windows a year: January to February, May to June, September to October.",
 's7':  "[plain, helpful] To be certified, you need an active IMA membership, a bachelor's degree or an approved professional certification, and two continuous years of relevant experience. [encouraging] And the experience can be completed up to seven years after you pass. So you can sit the exam first, and finish the experience later.",
 's8':  "[assured, factual] IMA's own Global Salary Survey reports that CMAs earn more than their non-certified peers — twenty-one per cent higher median total compensation worldwide, in the 2023 survey. [confident, forward-looking] And the roles follow: financial planning and analysis, controller, finance business partner — and the route to CFO.",
 's9':  "[proud, warm] Certuvo prepares you for exactly this exam. [clear, structured] Practice exams: scenario-based questions in the real format, with timed quizzes and full-length mock exams that simulate the testing experience. [steady] Progress tracking that shows your strengths, finds your knowledge gaps, and tells you when you're ready. [warm, inviting] Live study rooms, where you practise with your cohort in real time. And twenty-four seven chat support from experienced mentors.",
 's10': "[intrigued, confident] Then the AI. Certuvo's Question Forge writes unlimited new questions on any topic — [emphasis] and every one passes a panel of four AI judges before you ever see it. [warm, conversational] And your AI Coach: chat or call it during practice, in six languages. It reads the question on your screen, and teaches you to think — [pointed] not memorise. [firm, reassuring] During mock exams it switches itself off. [slower] Practise with help. Test without it.",
 's11': "[direct, encouraging, to camera] Pick your part. Choose a testing window. And start preparing with Certuvo today. [clear] certuvo dot com. [quietly confident, slower] The exam is hard by design. Being ready for it… doesn't have to be.",
}

LEGAL = ("CMA® is a registered trademark of the Institute of Management Accountants (IMA). Certuvo is an "
         "independent preparation provider and is not affiliated with, sponsored by or endorsed by IMA. Exam "
         "structure, fees and requirements as published by IMA for 2026; confirm current details at imanet.org. "
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
    md = ['# Certuvo CMA film — narration script', '', f'Legal end frame: {LEGAL}', '']
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
