#!/usr/bin/env python3
"""
Single source of truth for the PCI AI explainer's narration and captions.

Sixteen scenes across six chapters. Every factual statement traces to a
first-party source; see ../claims-register.md for the audit.

Two texts per segment, because they are different things:
  * `caption` is what a viewer reads   -> "ISO/IEC 17024", "PCL-AI"
  * `spoken`  is what a voice performs -> "I-S-O I-E-C 17024", "P-C-L A-I"

Emits ../captions/*.srt|.vtt, captions.data.js and ../captions/vo-script.md.
Once the read exists, sync.py measures it and timings come from timeline.json.
"""
import json, os, re

# The narration is generated with eleven_v3 — the emotion-capable model — using
# voice "Jim Executive - Authoritative, British and Warm" (tXxkePQsw0G69D8VeDzp),
# a stock library voice and not a clone of any real person.
#
# Direction is carried in the SPOKEN text, per the v3 prompting guide: an ellipsis
# is a longer thoughtful pause, an em-dash a short beat, and capitals mark
# emphasis. At most one capitalised word per scene — for a certification body,
# restraint reads as credibility and melodrama reads as a sales advert.
# The per-scene directed text lives in v3-direction.json.

HERE = os.path.dirname(os.path.abspath(__file__))
CAPDIR = os.path.normpath(os.path.join(HERE, '..', 'captions'))
LEAD, TAIL, GAP = 0.25, 0.25, 0.24

# (scene_id, chapter, [(caption, spoken), ...])
SCENES = [
 ('s1', 'Why PCI AI exists', [
   ("Project controls is the discipline that turns intent into delivery.",
    "Project controls is the discipline that turns intent into delivery."),
   ("Planning, cost, earned value, forecasting, risk and project finance — practised as one integrated whole, not as separate techniques.",
    "Planning, cost, earned value, forecasting, risk and project finance. Practised as one integrated whole, not as separate techniques."),
 ]),
 ('s2', 'Why PCI AI exists', [
   ("Project management has PMI. Accountancy has ACCA. Finance has CFA.",
    "Project management has P-M-I. Accountancy has A-C-C-A. Finance has C-F-A."),
   ("Project controls has had no equivalent — no shared standard, and no professional home.",
    "Project controls has had no equivalent. No shared standard, and no professional home."),
 ]),
 ('s3', 'Why PCI AI exists', [
   ("And the discipline is changing. Schedules, forecasts and cost reports are increasingly supported by AI.",
    "And the discipline is changing. Schedules, forecasts and cost reports are increasingly supported by A-I."),
   ("It can accelerate analysis. It can also create false confidence. Technology does not remove accountability.",
    "It can accelerate analysis. It can also create false confidence. Technology does not remove accountability."),
 ]),
 ('s4', 'The objective', [
   ("PCI AI exists to close that gap: to give project controls a shared standard, an independent credential and a professional home.",
    "P-C-I  A-I exists to close that gap. To give project controls a shared standard, an independent credential, and a professional home."),
   ("Built for how the discipline is practised now, with AI governance at its core.",
    "Built for how the discipline is practised now, with A-I governance at its core."),
 ]),
 ('s5', 'The objective', [
   ("Its mission is to advance the profession through certification, research, professional development, standards, publications and the responsible adoption of AI.",
    "Its mission is to advance the profession through certification, research, professional development, standards, publications, and the responsible adoption of A-I."),
 ]),
 ('s6', 'The objective', [
   ("Its position on that adoption is explicit. It certifies professionals who govern AI — not who defer to it.",
    "Its position on that adoption is explicit. It certifies professionals who govern A-I. Not who defer to it."),
 ]),
 ('s7', 'The certifications', [
   ("The framework is the PCI AI Project Leadership Certification Suite — three AI-era leadership credentials.",
    "The framework is the P-C-I  A-I Project Leadership Certification Suite. Three A-I era leadership credentials."),
 ]),
 ('s8', 'The certifications', [
   ("PCL-AI, for project controls. PFL-AI, for project finance. PML-AI, for project management.",
    "P-C-L  A-I, for project controls. P-F-L  A-I, for project finance. P-M-L  A-I, for project management."),
   ("Finance intelligently. Control predictively. Deliver successfully.",
    "Finance intelligently. Control predictively. Deliver successfully."),
 ]),
 ('s9', 'What is assessed', [
   ("Each credential rests on a published Body of Knowledge.",
    "Each credential rests on a published Body of Knowledge."),
   ("Its first edition defines thirteen domains and sixty-one knowledge areas, weighted forty, forty, twenty.",
    "Its first edition defines thirteen domains and sixty-one knowledge areas, weighted forty, forty, twenty."),
 ]),
 ('s10', 'What is assessed', [
   ("Project accounting and finance. Project management principles. And governed AI.",
    "Project accounting and finance. Project management principles. And governed A-I."),
   ("AI is not an appendix. It is a domain in its own right, and it is embedded through the other twelve.",
    "A-I is not an appendix. It is a domain in its own right, and it is embedded through the other twelve."),
 ]),
 ('s11', 'What is assessed', [
   ("The examination is scenario-based and criterion-referenced.",
    "The examination is scenario-based and criterion-referenced."),
   ("It asks whether you can read a cost position, interpret an earned-value index, judge a risk response, and decide whether an AI-generated forecast can be trusted.",
    "It asks whether you can read a cost position, interpret an earned-value index, judge a risk response, and decide whether an A-I generated forecast can be trusted."),
 ]),
 ('s12', 'What is assessed', [
   ("There are two routes in — an experience route for practitioners, and a Foundation route.",
    "There are two routes in. An experience route for practitioners, and a Foundation route."),
   ("The credential renews on a three-year CPD cycle with a mandatory AI-currency component, and every credential can be verified publicly.",
    "The credential renews on a three-year C-P-D cycle with a mandatory A-I currency component. And every credential can be verified publicly."),
 ]),
 ('s13', 'Industries', [
   ("The discipline is the same wherever capital is deployed at scale, so the credential is written to travel.",
    "The discipline is the same wherever capital is deployed at scale, so the credential is written to travel."),
   ("Energy and utilities. Rail and transportation. Aerospace and defence. Oil and gas. Construction and infrastructure.",
    "Energy and utilities. Rail and transportation. Aerospace and defence. Oil and gas. Construction and infrastructure."),
   ("Aviation. Manufacturing. Data centres. Smart cities. And government programmes.",
    "Aviation. Manufacturing. Data centres. Smart cities. And government programmes."),
 ]),
 ('s14', 'Industries', [
   ("For organisations, the same standard supports team enrolment at scale through corporate programmes, and curriculum alignment through university partnerships.",
    "For organisations, the same standard supports team enrolment at scale through corporate programmes, and curriculum alignment through university partnerships."),
 ]),
 ('s15', 'Integrity', [
   ("PCI is candid about what it is not. It is not accredited by ANAB, IAS, or any ISO/IEC 17024 accreditation body.",
    "P-C-I is candid about what it is not. It is not accredited by A-NAB, I-A-S, or any I-S-O  I-E-C 17024 accreditation body."),
   ("Its framework is developed with reference to those personnel-certification principles, and it says so plainly.",
    "Its framework is developed with reference to those personnel-certification principles, and it says so plainly."),
   ("For a body whose value rests on trust, that restraint is the foundation — not a weakness.",
    "For a body whose value rests on trust, that restraint is the foundation. Not a weakness."),
 ]),
 ('s16', 'Close', [
   ("AI proposes. The professional disposes.",
    "A-I proposes. The professional disposes."),
   ("Discover PCI AI at pciai.org",
    "Discover P-C-I  A-I at P-C-I-A-I dot org."),
 ]),
]


def weight(spoken):
    """Approximate speaking length in word units; spelled letters count 0.6."""
    total = 0.0
    for tok in spoken.split():
        core = tok.strip('.,—-')
        if re.fullmatch(r'(?:[A-Z]-)+[A-Z]', core) or re.fullmatch(r'A-NAB', core):
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
    """Balanced caption lines: fewest lines that fit, at the narrowest width."""
    words = text.split()
    if len(text) <= width:
        return text
    n = min(max(len(_greedy(words, width)), 2), maxlines)
    best = _greedy(words, width)
    for w in range(max(len(x) for x in words), width + 1):
        cand = _greedy(words, w)
        if len(cand) <= n:
            best = cand
            break
    return '\n'.join(best)


def _measured():
    f = os.path.join(HERE, 'timeline.json')
    return json.load(open(f))['segments'] if os.path.exists(f) else None


def build():
    """Placeholder pacing before the read exists; real timings once it does."""
    measured = _measured()
    caps, rows, idx, t = [], [], 0, LEAD
    WPS = 130.0 / 60.0
    for sid, chap, segs in SCENES:
        for cap, spoken in segs:
            idx += 1
            d = weight(spoken) / WPS
            a, b = round(t, 2), round(t + d, 2)
            if measured:
                a, b = round(measured[str(idx)][0], 2), round(measured[str(idx)][1], 2)
            caps.append([a, b, wrap(cap)])
            rows.append((sid, chap, a, b, round(b - a, 2), cap, spoken))
            t = b + GAP
    return caps, rows


def ts(s, comma=True):
    h = int(s // 3600); m = int((s % 3600) // 60); sec = int(s % 60)
    ms = int(round((s - int(s)) * 1000))
    if ms == 1000: sec, ms = sec + 1, 0
    return f"{h:02d}:{m:02d}:{sec:02d}{',' if comma else '.'}{ms:03d}"


def main():
    caps, rows = build()
    os.makedirs(CAPDIR, exist_ok=True)
    with open(os.path.join(CAPDIR, 'pci-explainer.srt'), 'w') as f:
        for i, (a, b, t) in enumerate(caps, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n")
    with open(os.path.join(CAPDIR, 'pci-explainer.vtt'), 'w') as f:
        f.write("WEBVTT\n\n")
        for i, (a, b, t) in enumerate(caps, 1):
            f.write(f"{i}\n{ts(a,False)} --> {ts(b,False)}\n{t}\n\n")
    with open(os.path.join(HERE, 'captions.data.js'), 'w') as f:
        f.write("/* GENERATED by vo.py — do not edit. */\nwindow.__CAPS = " + json.dumps(caps) + ";\n")
    with open(os.path.join(CAPDIR, 'vo-script.md'), 'w') as f:
        f.write("# PCI AI explainer — the read\n\nGenerated by `src/vo.py`. Edit the spec, not this file.\n\n")
        f.write("Pronunciation lives in SPOKEN only; captions never show letter-spelling.\n\n")
        f.write("| Scene | Chapter | In | Out | Spoken (record this) | On-screen caption |\n|---|---|---|---|---|---|\n")
        for sid, chap, a, b, d, cap, sp in rows:
            f.write(f"| {sid} | {chap} | {a:.2f} | {b:.2f} | {sp} | {cap} |\n")
        f.write(f"\n**{len(rows)} segments · ~{sum(weight(r[6]) for r in rows):.0f} word units.**\n")
        f.write("\n## Pronunciation\n\n| Written | Spoken |\n|---|---|\n")
        for a, b in [("PCI AI","P-C-I  A-I"),("PCL-AI","P-C-L  A-I"),("PFL-AI","P-F-L  A-I"),
                     ("PML-AI","P-M-L  A-I"),("pciai.org","P-C-I-A-I dot org"),
                     ("ISO/IEC 17024","I-S-O  I-E-C 17024"),("CPD","C-P-D"),("ANAB","A-NAB")]:
            f.write(f"| {a} | {b} |\n")
    tot = sum(weight(r[6]) for r in rows)
    print(f"segments {len(rows)} | ~{tot:.0f} word units | est {tot/(130/60):.0f}s at 130 wpm")
    if _measured():
        print("  timings taken from timeline.json (locked to the recorded audio)")
    else:
        print(f"  estimated timeline: {caps[-1][1]:.1f}s (placeholder until the read is generated)")


if __name__ == '__main__':
    main()
