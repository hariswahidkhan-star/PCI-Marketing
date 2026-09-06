#!/usr/bin/env python3
"""
Single source of truth for the Honorary Fellow (PCI) film's narration and captions.

Ten scenes. Every factual statement traces to a first-party PCI page; see
../claims-register.md for the audit, including the two places where the brief's
draft narration asserted more than the site currently supports and the copy was
changed rather than the claim taken on trust.

Two texts per segment, because they are different things:
  * `caption` is what a viewer reads   -> "PCI AI", "PCL-AI", "pciai.org"
  * `spoken`  is what a voice performs -> "P-C-I A-I", "P-C-L A-I", "P-C-I-A-I dot org"

The caption is the narration word for word; only the pronunciation spelling
differs, which is what the brief's QC line "captions match the narration" means
in practice — a viewer reads what they hear.

THE ONE CLAIM THIS FILM MUST NEVER MAKE: Honorary Fellow (PCI) is not an examined
certification, licence or accreditation. Every scene was written against that.

Emits ../captions/*.srt|.vtt, captions.data.js and ../captions/vo-script.md.
Once the read exists, sync.py measures it and timings come from timeline.json.
"""
import json, os, re

# Narration is generated with eleven_v3 — the emotion-capable model — using
# "Holden Pro Voice" (UudLhsL2DlHkDK0vGwl3), the voice named in the brief. It is
# a stock library voice and NOT a clone of any real person.
#
# Direction is carried in the SPOKEN text, per the v3 prompting guide: an ellipsis
# is a longer thoughtful pause, an em-dash a short beat, capitals mark emphasis.
# The brief asks for quiet confidence at the open, building inspiration through
# the industry and leadership sequences, warmth on contribution, and strength at
# the close — so the density of direction rises and then resolves, rather than
# sitting flat. Capitals stay rare: this is a certification body, and a narrator
# who oversells the recognition undermines it.
# The per-scene directed text lives in v3-direction.json.

HERE = os.path.dirname(os.path.abspath(__file__))
CAPDIR = os.path.normpath(os.path.join(HERE, '..', 'captions'))
LEAD, TAIL, GAP = 0.25, 0.25, 0.24

# (scene_id, chapter, [(caption, spoken), ...])
SCENES = [
 ('s1', 'The question', [
   ("Some professionals deliver successful projects.",
    "Some professionals deliver successful projects."),
   ("Others leave a lasting mark on the people, standards and industries around them.",
    "Others leave a lasting mark on the people, standards and industries around them."),
 ]),
 ('s2', 'The recognition', [
   ("Honorary Fellow of the Project Controls Institute is a board-conferred recognition for distinguished professional contribution, leadership and service.",
    "Honorary Fellow of the Project Controls Institute… is a board-conferred recognition for distinguished professional contribution, leadership and service."),
 ]),
 ('s3', 'What it is', [
   ("It involves no examination, and is separate from PCI's examined certifications.",
    "It involves NO examination — and is separate from P-C-I's examined certifications."),
   ("Every application is considered individually, and recognition is conferred solely at the Board's discretion.",
    "Every application is considered individually… and recognition is conferred solely at the Board's discretion."),
 ]),
 ('s4', 'Who may apply', [
   ("It is intended for experienced leaders whose impact spans project controls, cost engineering, finance, project management or a closely related discipline.",
    "It is intended for experienced leaders… whose impact spans project controls, cost engineering, finance, project management, or a closely related discipline."),
 ]),
 ('s5', 'Global industries', [
   ("Applicants come from infrastructure, energy, technology, aviation, project finance, government and academia.",
    "Applicants come from infrastructure, energy, technology, aviation, project finance, government and academia."),
   ("And every sector where strong professional leadership shapes outcomes.",
    "And every sector where strong professional leadership shapes OUTCOMES."),
 ]),
 ('s6', 'Experience', [
   ("To be considered, applicants need at least eight years of relevant experience, including three at managerial level.",
    "To be considered, applicants need at least eight years of relevant experience… including three at managerial level."),
   ("And a demonstrable record of distinguished contribution. Meeting these criteria does not guarantee recognition.",
    "And a demonstrable record of distinguished contribution. Meeting these criteria does not guarantee recognition."),
 ]),
 ('s7', 'Your evidence', [
   ("Applicants provide a professional profile, résumé, qualifications, career history and evidence of contribution, for confidential review.",
    "Applicants provide a professional profile, résumé, qualifications, career history and evidence of contribution… for confidential review."),
   ("PCI charges no nomination, assessment or credential fee.",
    "P-C-I charges no nomination, assessment or credential fee."),
 ]),
 ('s8', 'Recognition', [
   ("Those selected are recognised as an Honorary Fellow — recorded so anyone can verify it at source, and labelled honorary, never a passed examination.",
    "Those selected are recognised as an Honorary Fellow — recorded so anyone can verify it at source… and labelled honorary, never a passed examination."),
   ("Accepted applicants may also receive access to the PCI student portal, study through Certuvo, and invitations to selected PCI AI events, subject to programme terms.",
    "Accepted applicants may also receive access to the P-C-I student portal, study through Certuvo, and invitations to selected P-C-I A-I events, subject to programme terms."),
 ]),
 ('s9', 'Discipline alignment', [
   ("You may also indicate whether your contribution aligns with project controls, project finance or project management.",
    "You may also indicate whether your contribution aligns with project controls, project finance, or project management."),
 ]),
 ('s10', 'Apply', [
   ("If your leadership has advanced the profession, your contribution deserves consideration.",
    "If your leadership has advanced the profession… your contribution deserves consideration."),
   ("Apply for Honorary Fellow PCI at pciai.org.",
    "Apply for Honorary Fellow P-C-I at… P-C-I-A-I dot org."),
 ]),
]


def weight(text):
    """Rough spoken length. A spelled acronym letter is quick, so count it 0.6."""
    n = 0.0
    for tok in text.split():
        t = tok.strip('.,:;—-…()"\'')
        if re.fullmatch(r'(?:[A-Z]-)+[A-Z]', t):
            n += 0.6 * len(t.split('-'))
        elif t:
            n += 1.0
    return n


def wrap(text, width=46):
    """Balance a caption over the fewest lines, then the most even split.

    A greedy wrap happily leaves a 51-character line under two short ones, which
    reads as a mistake even though nothing overflows. Searching down from the
    full width for the narrowest wrap that still uses the minimum number of lines
    gives an even block instead.
    """
    words = text.split()
    def lay(w):
        lines, cur = [], ''
        for word in words:
            trial = (cur + ' ' + word).strip()
            if len(trial) <= w or not cur:
                cur = trial
            else:
                lines.append(cur); cur = word
        if cur: lines.append(cur)
        return lines
    best = lay(width)
    for w in range(width, 18, -1):
        cand = lay(w)
        if len(cand) > len(best): break
        best = cand
    return '\n'.join(best)


def _measured():
    p = os.path.join(HERE, 'timeline.json')
    return json.load(open(p)) if os.path.exists(p) else None


def segments():
    """(scene_id, chapter, caption, spoken) in order."""
    out = []
    for sid, chap, lines in SCENES:
        for cap, spk in lines:
            out.append((sid, chap, cap, spk))
    return out


def timings():
    """Caption windows. Measured from the recorded read when timeline.json exists.

    sync.py writes the measured window of every caption segment under
    `segments`, keyed by 1-based index in the order segments() yields them. An
    earlier draft of this function looked for a key that sync.py never writes,
    and so fell back to the estimate without saying so — which is precisely the
    silent caption drift the single-source design exists to prevent. If the
    timeline exists, it must be used; anything else is an error, not a fallback.
    """
    tl = _measured()
    segs = segments()
    if tl:
        meas = tl.get('segments') or {}
        if len(meas) != len(segs):
            raise SystemExit(f'timeline.json has {len(meas)} measured segments but vo.py '
                             f'defines {len(segs)} — re-run sync.py after editing SCENES.')
        return [(meas[str(i)][0], meas[str(i)][1], cap)
                for i, (_, _, cap, _) in enumerate(segs, 1)]
    # Pre-recording estimate only, so the film can be laid out before the read.
    t, out = LEAD, []
    for _, _, cap, spk in segs:
        d = weight(spk) / (130.0 / 60.0)
        out.append((round(t, 2), round(t + d, 2), cap)); t += d + GAP
    return out


def ts(x, comma=True):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    sep = ',' if comma else '.'
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.', sep)


def main():
    os.makedirs(CAPDIR, exist_ok=True)
    cues = timings()

    srt = []
    for i, (a, b, cap) in enumerate(cues, 1):
        srt.append(f"{i}\n{ts(a)} --> {ts(b)}\n{wrap(cap)}\n")
    open(os.path.join(CAPDIR, 'pci-honorary-fellow.srt'), 'w', encoding='utf-8').write('\n'.join(srt))

    vtt = ['WEBVTT', '']
    for a, b, cap in cues:
        vtt.append(f"{ts(a, False)} --> {ts(b, False)}\n{wrap(cap)}\n")
    open(os.path.join(CAPDIR, 'pci-honorary-fellow.vtt'), 'w', encoding='utf-8').write('\n'.join(vtt))

    # The burned-in captions come from the same list, so they cannot drift.
    data = [[a, b, wrap(cap)] for a, b, cap in cues]
    open(os.path.join(HERE, 'captions.data.js'), 'w', encoding='utf-8').write(
        'window.__CAPS = ' + json.dumps(data, ensure_ascii=False) + ';\n')

    md = ['# Narration — Honorary Fellow (PCI)', '',
          'Voice: ElevenLabs **"Holden Pro Voice"** (`UudLhsL2DlHkDK0vGwl3`) on `eleven_v3`.',
          'A stock library voice — **not a clone of any real person.**', '',
          '## Mandatory pronunciations', '',
          '| Written | Spoken |', '|---|---|',
          '| PCI AI | P-C-I A-I |', '| PCL-AI | P-C-L A-I |',
          '| PFL-AI | P-F-L A-I |', '| PML-AI | P-M-L A-I |',
          '| pciai.org | P-C-I-A-I dot org |', '', '## The read', '']
    for (a, b, cap), (sid, chap, _, spk) in zip(cues, segments()):
        md.append(f"**{sid} · {chap} · {a:.2f}–{b:.2f}s**\n\n> {spk}\n")
    open(os.path.join(CAPDIR, 'vo-script.md'), 'w', encoding='utf-8').write('\n'.join(md))

    src = 'timeline.json (locked to the recorded audio)' if _measured() else 'estimate at 130 wpm'
    total = cues[-1][1] if cues else 0
    print(f"segments {len(cues)} | ~{sum(weight(s) for _,_,_,s in segments()):.0f} word units "
          f"| {total:.2f}s")
    print(f"  timings taken from {src}")


if __name__ == '__main__':
    main()
