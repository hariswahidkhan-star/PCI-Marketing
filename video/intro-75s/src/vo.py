#!/usr/bin/env python3
"""
Single source of truth for the PCI AI 75-second film's voiceover and captions.

The 15-second film's README warns that caption text lives in three places at
once (the burned-in array, the .srt and the .vtt) and that all three must be
kept in step by hand. That is a standing invitation to drift, so this film
generates all three from the spec below instead.

Emits:
    ../captions/pci-intro-75s.srt      caption file for platforms that take one
    ../captions/pci-intro-75s.vtt      the same, WebVTT
    captions.data.js                   window.__CAPS for the burned-in track
    ../captions/vo-script.md           the read, timed, for the voice artist/TTS

Two texts are carried per segment because they are genuinely different things:
  * `caption` is what a viewer reads   -> "PCI AI", "pciai.org"
  * `spoken`  is what a voice performs -> "P-C-I  A-I", "P-C-I-A-I dot org"
Pronunciation belongs to the read, never to the on-screen text.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CAPDIR = os.path.normpath(os.path.join(HERE, '..', 'captions'))

LEAD, TAIL, GAP = 0.25, 0.25, 0.24

# (scene_id, in, out, [(caption, spoken), ...])
SCENES = [
    ('s1', 0.00, 7.75, [
        ("Every major project begins with ambition.",
         "Every major project begins with ambition."),
        ("Turning that ambition into a controlled, financeable and deliverable outcome requires more than information.",
         "Turning that ambition into a controlled, financeable and deliverable outcome requires more than information."),
    ]),
    ('s2', 7.75, 15.94, [
        ("Project professionals must connect scope, schedule, cost, finance, risk and performance",
         "Project professionals must connect scope, schedule, cost, finance, risk and performance"),
        ("while making accountable decisions in increasingly complex environments.",
         "while making accountable decisions in increasingly complex environments."),
    ]),
    ('s3', 15.94, 26.51, [
        ("Artificial intelligence can accelerate analysis, identify patterns, compare scenarios and support forecasting.",
         "Artificial intelligence can accelerate analysis, identify patterns, compare scenarios and support forecasting."),
        ("But a convincing AI output is not automatically a reliable project decision.",
         "But a convincing A-I output is not automatically a reliable project decision."),
    ]),
    ('s4', 26.51, 35.85, [
        ("Responsible adoption requires verified data, transparent assumptions, meaningful human review,",
         "Responsible adoption requires verified data, transparent assumptions, meaningful human review,"),
        ("clear decision rights and an evidence trail that can withstand professional challenge.",
         "clear decision rights and an evidence trail that can withstand professional challenge."),
    ]),
    ('s5', 35.85, 49.99, [
        ("PCI AI — Project Controls Institute Global — focuses on the professional competence",
         "P-C-I  A-I — Project Controls Institute Global — focuses on the professional competence"),
        ("needed to govern AI-supported work across project controls, project finance and project management.",
         "needed to govern A-I supported work across project controls, project finance and project management."),
    ]),
    ('s6', 49.99, 61.66, [
        ("Its professional credential framework includes PCL-AI for project controls,",
         "Its professional credential framework includes P-C-L  A-I for project controls,"),
        ("PFL-AI for project finance and PML-AI for project management.",
         "P-F-L  A-I for project finance and P-M-L  A-I for project management."),
    ]),
    ('s7', 61.66, 70.93, [
        ("The future of project delivery will not be defined by technology alone.",
         "The future of project delivery will not be defined by technology alone."),
        ("It will be shaped by professionals who know when to trust, when to challenge and how to remain accountable.",
         "It will be shaped by professionals who know when to trust, when to challenge and how to remain accountable."),
    ]),
    ('s8', 70.93, 75.00, [
        ("Discover PCI AI at pciai.org",
         "Discover P-C-I  A-I at P-C-I-A-I dot org."),
    ]),
]


def weight(spoken):
    """Approximate speaking length in 'word units'.

    A spelled acronym is not one word long. "P-C-L  A-I" is five letter names
    and takes roughly as long as three ordinary words, so letters are counted
    at 0.6 units each. Without this the credential scene is allotted far too
    little time and the read has to sprint through the one line the film
    exists to deliver clearly.
    """
    total = 0.0
    for tok in spoken.split():
        core = tok.strip('.,—-')
        if re.fullmatch(r'(?:[A-Z]-)+[A-Z]', core):
            total += len(core.split('-')) * 0.6
        elif core:
            total += 1.0
    return total



def _greedy(words, width):
    lines, cur = [], ''
    for w in words:
        cand = (cur + ' ' + w).strip()
        if cur and len(cand) > width:
            lines.append(cur); cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def wrap(text, width=54, maxlines=3):
    """Break a caption into balanced lines.

    A 110-character caption on one line is unreadable on a phone, which is where
    most of this film will be watched. Broadcast practice is ~42 characters a
    line; 54 is the widest that still survives the 1080x1920 crop.

    Balance matters as much as the cap: greedy wrapping leaves a long line under
    two short ones, which reads as a mistake. So for the smallest line count that
    fits, this searches for the NARROWEST width that still yields that many
    lines -- which is what makes the lines come out even.
    """
    words = text.split()
    longest = max(len(w) for w in words)
    if len(text) <= width:
        return text
    n = len(_greedy(words, width))
    n = min(max(n, 2), maxlines)
    best = _greedy(words, width)
    for w in range(longest, width + 1):
        cand = _greedy(words, w)
        if len(cand) <= n:
            best = cand
            break
    return '\n'.join(best)


def _measured():
    """Caption timings taken from timeline.json when it exists.

    Once the voiceover is generated, the captions must follow the words that
    were actually spoken rather than the pace the film was planned at. sync.py
    writes the real placements; this reads them so all three caption forms and
    the burned-in track stay locked to the audio.
    """
    import json, os
    f = os.path.join(HERE, 'timeline.json')
    if not os.path.exists(f):
        return None
    return json.load(open(f))['segments']


def build():
    measured = _measured()
    caps, rows, idx = [], [], 0
    for sid, s_in, s_out, segs in SCENES:
        win_a, win_b = s_in + LEAD, s_out - TAIL
        span = (win_b - win_a) - GAP * (len(segs) - 1)
        tot = sum(weight(sp) for _, sp in segs)
        t = win_a
        for cap, spoken in segs:
            w = weight(spoken)
            dur = span * (w / tot)
            a, b = round(t, 2), round(t + dur, 2)
            idx += 1
            if measured:
                a, b = round(measured[str(idx)][0], 2), round(measured[str(idx)][1], 2)
                dur = b - a
            caps.append([a, b, wrap(cap)])
            wpm = w / (dur / 60.0)
            rows.append((sid, a, b, round(b - a, 2), cap, spoken, round(wpm)))
            t = b + GAP
    return caps, rows


def ts(sec, comma=True):
    h = int(sec // 3600); m = int((sec % 3600) // 60)
    s = int(sec % 60); ms = int(round((sec - int(sec)) * 1000))
    if ms == 1000:
        s, ms = s + 1, 0
    return f"{h:02d}:{m:02d}:{s:02d}{',' if comma else '.'}{ms:03d}"


def main():
    caps, rows = build()
    os.makedirs(CAPDIR, exist_ok=True)

    with open(os.path.join(CAPDIR, 'pci-intro-75s.srt'), 'w') as f:
        for i, (a, b, txt) in enumerate(caps, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{txt}\n\n")

    with open(os.path.join(CAPDIR, 'pci-intro-75s.vtt'), 'w') as f:
        f.write("WEBVTT\n\n")
        for i, (a, b, txt) in enumerate(caps, 1):
            f.write(f"{i}\n{ts(a, False)} --> {ts(b, False)}\n{txt}\n\n")

    with open(os.path.join(HERE, 'captions.data.js'), 'w') as f:
        f.write("/* GENERATED by vo.py — do not edit. Run: python3 vo.py */\n")
        f.write("window.__CAPS = " + json.dumps(caps) + ";\n")

    with open(os.path.join(CAPDIR, 'vo-script.md'), 'w') as f:
        f.write("# PCI AI — 75-second film: the read\n\n")
        f.write("Generated by `src/vo.py`. Do not hand-edit — edit the spec and regenerate.\n\n")
        f.write("**Pronunciation is carried in the SPOKEN column only.** The caption column is\n")
        f.write("what a viewer reads, and it never shows letter-spelling.\n\n")
        f.write("| Scene | In | Out | Dur | Spoken (record this) | On-screen caption | wpm |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for sid, a, b, d, cap, spoken, wpm in rows:
            f.write(f"| {sid} | {a:.2f} | {b:.2f} | {d:.2f} | {spoken} | {cap} | {wpm} |\n")
        tw = sum(weight(sp) for _, _, _, _, _, sp, _ in rows)
        f.write(f"\n**{len(rows)} segments · ~{tw:.0f} word units · 75.00 s total.**\n")
        f.write("\n## Pronunciation guide (mandatory)\n\n")
        f.write("| Written | Spoken |\n|---|---|\n")
        for a, b in [("PCI AI", "P-C-I  A-I"), ("PCL-AI", "P-C-L  A-I"),
                     ("PFL-AI", "P-F-L  A-I"), ("PML-AI", "P-M-L  A-I"),
                     ("pciai.org", "P-C-I-A-I dot org")]:
            f.write(f"| {a} | {b} |\n")
        f.write("\n## Casting\n\nWarm, authoritative, internationally understandable English. "
                "Mid-range, unforced. The reference is documentary narration, not a product "
                "advert: no upward inflection at line ends, no smile-in-the-voice, no urgency. "
                "Do not clone a real person's voice.\n")

    avg=sum(weight(r[5]) for r in rows)/sum(r[3] for r in rows)*60
    print(f"captions: {len(caps)} segments | mean pace {avg:.0f} wpm")
    if _measured():
        print('  timings taken from timeline.json (locked to the recorded audio)')
        slow = fast = []
    else:
        slow = [r for r in rows if r[6] > 170]
        fast = [r for r in rows if r[6] < 105]
    for r in slow:
        print(f"  WARN fast {r[0]} {r[6]} wpm: {r[4][:52]}")
    for r in fast:
        print(f"  note slow {r[0]} {r[6]} wpm: {r[4][:52]}")
    print("wrote captions/*.srt|vtt|vo-script.md and src/captions.data.js")


if __name__ == '__main__':
    main()
