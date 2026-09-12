#!/usr/bin/env python3
"""
Single source of truth for the Honorary Fellow (PCI) film's narration and captions.

Thirteen scenes. Every factual statement traces to a first-party PCI page; see
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
# Each segment is (caption, spoken) or (caption, spoken, end_s). end_s is the
# midpoint of the silence the segment ends on, measured in the trimmed take
# (ffmpeg silencedetect at -38 dB; chosen so the implied speaking rate stays
# level across the scene, since the take's transcript carries no word times). Given explicitly so a
# caption changes exactly where the narrator breathes rather than at the
# nearest silence to a proportional guess — the v3 read spells out P-C-I and
# I-S-O I-E-C slowly, which throws proportional splits off by a phrase.
SCENES = [
 ('s1', 'The question', [
   ("Some careers deliver projects.",
    "Some careers deliver projects.", 3.00),
   ("Others leave behind a standard, a method — and the people who carry it forward.",
    "Others leave behind a standard, a method… and the people who carry it forward."),
 ]),
 ('s2', 'The recognition', [
   ("Honorary Fellow (PCI): conferred by the Board of an independent professional body,",
    "Honorary Fellow, P-C-I… conferred by the Board of an independent professional body —", 5.69),
   ("in recognition of distinguished contribution, leadership and service.",
    "in recognition of distinguished contribution, leadership and service.", 10.49),
   ("Your name, on PCI's own public registry — checkable at source.",
    "Your name — on P-C-I's own public registry… checkable at source."),
 ]),
 ('s3', 'The Institute', [
   ("The Project Controls Institute is an independent professional body —",
    "The Project Controls Institute is an independent professional body —", 4.44),
   ("a Delaware Non-Stock Corporation —",
    "a Delaware Non-Stock Corporation —", 7.09),
   ("built to give the discipline a shared standard, an independent credential",
    "built to give the discipline a shared standard, an independent credential…", 12.09),
   ("and a professional home for the AI era.",
    "and a professional home for the A-I era.", 15.46),
   ("Its published Body of Knowledge sets thirteen domains and sixty-one knowledge areas.",
    "Its published Body of Knowledge sets thirteen domains and sixty-one knowledge areas.", 21.27),
   ("And every credential it confers is entered on a registry anyone can check.",
    "And every credential it confers… is entered on a registry anyone can check."),
 ]),
 ('s4', 'What it is', [
   ("It involves no examination. The record is the evidence, and the Board weighs it.",
    "It involves no examination. The record is the evidence… and the Board weighs it.", 6.26),
   ("It is separate from PCI's examined certifications — PCL-AI, PFL-AI and PML-AI.",
    "It is separate from P-C-I's examined certifications — P-C-L A-I, P-F-L A-I and P-M-L A-I.", 17.81),
   ("Every application is considered individually,",
    "Every application is considered individually…", 21.36),
   ("and recognition is conferred solely at the Board's discretion.",
    "and recognition is conferred solely at the Board's discretion."),
 ]),
 ('s5', 'Who may apply', [
   ("If you have led teams, shaped standards, taught, published or governed —",
    "If you have led teams, shaped standards, taught, published or governed —", 5.26),
   ("in project controls, cost control, finance, project management or a closely related discipline — you may apply.",
    "in project controls, cost control, finance, project management, or a closely related discipline — you may apply."),
 ]),
 ('s6', 'Industries', [
   ("From construction and energy to technology, aviation, project finance, government and academia:",
    "From construction and energy… to technology, aviation, project finance, government and academia.", 6.78),
   ("wherever leadership shapes outcomes,",
    "Wherever leadership shapes OUTCOMES,", 9.29),
   ("your contribution counts.",
    "your contribution counts."),
 ]),
 ('s7', 'Eligibility', [
   ("The floor is eight years' experience, three of them at managerial level —",
    "The floor is eight years of professional experience… three of them at managerial level —", 5.43),
   ("leading teams, functions, programmes or budgets.",
    "leading teams, functions, programmes or budgets.", 9.20),
   ("The bar is higher: a demonstrable record of distinguished contribution.",
    "The bar is higher — a demonstrable record of distinguished contribution.", 14.66),
   ("Meeting the criteria does not guarantee recognition.",
    "Meeting the criteria does not guarantee recognition."),
 ]),
 ('s8', 'Your application', [
   ("PCI charges no nomination, assessment or credential fee.",
    "P-C-I charges no nomination, assessment, or credential fee.", 4.05),
   ("Optional extras, such as attending an awards ceremony, are charged separately and play no part in the decision.",
    "Optional extras — such as attending an awards ceremony — are charged separately, and play no part in the decision.", 11.31),
   ("Recognition is awarded solely on merit.",
    "Recognition is awarded solely on merit.", 14.33),
   ("One application: your profile, résumé, career history and evidence, reviewed confidentially by the Board.",
    "One application… your profile, résumé, career history and evidence — reviewed confidentially by the Board."),
 ]),
 ('s9', 'Putting yourself forward', [
   ("You need no sponsor to be considered.",
    "You need no sponsor to be considered.", 2.55),
   ("You put your own record forward.",
    "You put your own record forward.", 5.06),
   ("The Board then assesses it against published criteria, on the evidence —",
    "The Board then assesses it against published criteria… on the evidence —", 10.28),
   ("and does so confidentially.",
    "and does so confidentially."),
 ]),
 ('s10', 'The registry', [
   ("Those recognised are entered on PCI's own public registry: checkable at source by anyone,",
    "Those recognised are entered on P-C-I's own public registry… checkable at source by anyone —", 6.38),
   ("labelled honorary, never a passed examination.",
    "labelled honorary, never a passed examination."),
 ]),
 ('s11', 'What it opens', [
   ("If recognised, you may also be given access to the PCI student portal and the Institute's learning resources —",
    "If recognised, you may also be given access to the P-C-I student portal, and the Institute's learning resources —", 7.03),
   ("video lectures, course material and the simulation lab.",
    "video lectures, course material, and the simulation lab.", 11.14),
   ("The same terms may extend to study through Certuvo, PCI's official preparation platform,",
    "The same terms may extend to study through Certuvo, P-C-I's official preparation platform…", 17.48),
   ("and invitations to selected PCI AI events — all subject to current programme terms.",
    "and invitations to selected P-C-I A-I events — all subject to current programme terms."),
 ]),
 ('s12', 'Discipline alignment', [
   ("Tell the Board which discipline your contribution aligns to:",
    "Tell the Board which discipline your contribution aligns to —", 4.69),
   ("project controls, project finance or project management.",
    "project controls, project finance, or project management.", 7.75),
   ("Optional, and it confers no examined certification.",
    "Optional… and it confers no examined certification."),
 ]),
 ('s13', 'Apply', [
   ("If your work has outlasted the projects it was done on, it deserves to be recognised.",
    "If your work has outlasted the projects it was done on… it deserves to be recognised.", 6.00),
   ("Apply for the Board's consideration at pciai.org.",
    "Apply for the Board's consideration — at P-C-I-A-I dot org.", 11.53),
   ("Questions to Members@pciai.org.",
    "Questions… to Members, at P-C-I-A-I dot org."),
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
        for cap, spk, *_ in lines:
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
