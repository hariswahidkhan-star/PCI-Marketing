#!/usr/bin/env python3
"""
Original score for the PCI AI explainer. 48 kHz stereo, standard library only —
no samples, no loops, no third-party library — so the cue is PCI's own work and
carries no licence obligation.

Nearly four and a half minutes is long enough that a single drone becomes
wallpaper, so the score is driven rather than ambient: a tempo grid with a
pulse, kit and ostinato on top of the harmonic bed, and an intensity curve that
rises and falls with what the film is saying.

It reads the measured cut list from timeline.json (written by sync.py), places a
bell on every scene change and an impact on every chapter change, and shifts
harmony per chapter: D minor for the problem, its relative F major as the
objective arrives, back to D minor for the framework, an open fifth for the
assessment chapters, F major again for industries, and a warm resolve on the
close.

**Thrilling, not loud.** Drive here comes from rhythm and from the shape of the
intensity curve, not from level or from a wall of sound — the film is for a
certification body, and a score that oversells reads as an advert. Two rules
keep it honest:

  - The kit lives below ~120 Hz and above ~6 kHz. The mid-range where the
    narration sits is left deliberately thin, so the music can be busy without
    ever competing with the voice. build.sh then side-chains the whole bed under
    the read on top of that.
  - Intensity *falls* for chapter 6. That chapter is where the Institute states
    plainly what it is not accredited by, and scoring candour like a climax
    would undercut the one moment the film most needs to be believed.

Everything is deterministic: the noise sources are seeded, so the same timeline
renders the same score every time.

The kit itself lives in ../../lib/score_kit.py, shared with the other two films
so there is one drum synth in the repository rather than three. What stays here
is the part that should differ per film: tempo, harmony, arrangement and the
intensity curve.

  python3 music.py ../build/score.wav
"""
import array, json, math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from score_kit import Kit, fade, write_wav          # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48_000

TL = json.load(open(os.path.join(HERE, 'timeline.json')))
DUR = TL['total']
SHOTS = TL['shots']
N = int(SR * DUR)
CUTS = [s[2] for s in SHOTS]
CHAPTERS, seen = [], None
for sid, chap, a, b in SHOTS:
    if chap != seen:
        CHAPTERS.append((chap, a)); seen = chap
CHAP_T = [t for _, t in CHAPTERS]
NCH = len(CHAP_T)


def hz(n): return 440.0 * (2.0 ** (n / 12.0))
D2, A2, D3, F3, G3, A3, C4, D4, E4, F4, A4, D5 = (
    hz(-31), hz(-24), hz(-19), hz(-16), hz(-14), hz(-12), hz(-9), hz(-7), hz(-5), hz(-4), hz(0), hz(5))

# per-chapter triad above the D/A drone
VOICINGS = [(F3, A3, D4), (F3, C4, A3), (F3, A3, D4), (D3, A3, E4),
            (F3, C4, A4), (F3, A3, D4), (D3, F3, A3)]

# The ostinato figure per chapter — four notes, one per eighth, cycling. Same
# pitch set as that chapter's voicing so the pulse is harmony and not decoration.
FIGURES = [(D4, A3, F3, A3), (F4, C4, A3, C4), (D4, A3, D4, F4), (E4, A3, D4, A3),
           (F4, A4, C4, A4), (D4, F4, A3, F4), (D4, F4, A4, F4)]

# Where the film gets loud and where it gets quiet. One weight per chapter:
# problem → objective → framework → assessment → industries → integrity → close.
# Industries is the sweep and takes the peak; integrity pulls right back.
INTENSITY = [0.30, 0.52, 0.70, 0.82, 1.00, 0.26, 0.72]

BPM = 104.0
BEAT = 60.0 / BPM


def chapter_index(t):
    idx = 0
    for i, ct in enumerate(CHAP_T):
        if t >= ct: idx = i
    return idx


def chapter_mix(t):
    """Weights over the chapter voicings, cross-faded at each boundary."""
    w = [0.0] * NCH
    idx = chapter_index(t)
    w[idx] = 1.0
    if idx + 1 < NCH:
        nxt = CHAP_T[idx + 1]
        if t > nxt - 3.0:
            p = fade((t - (nxt - 3.0)) / 3.0)
            w[idx] = 1.0 - p; w[idx + 1] = p
    return w


def intensity(t):
    """The drive curve — chapter weights, cross-faded, so it ramps rather than steps."""
    w = chapter_mix(t)
    v = sum(wi * INTENSITY[i] for i, wi in enumerate(w))
    return v * fade(t / 6.0) * (1.0 - 0.85 * fade((t - (DUR - 7.0)) / 7.0))


def render():
    kit = Kit(sr=SR, n_samples=N)
    place = kit.place
    KICK, SUB, HAT, HATO, SNARE, RISER = (
        kit.KICK, kit.SUB, kit.HAT, kit.HATO, kit.SNARE, kit.RISER)

    # ---- the grid -----------------------------------------------------------
    # One pass over sixteenth notes, k counting from the downbeat: a bar is 16,
    # a beat is 4. Each element asks the intensity curve whether it is playing
    # yet, so the arrangement thins and thickens on its own rather than being
    # arranged bar by bar.
    step = BEAT / 4.0
    k = 0
    t = 0.0
    while t < DUR:
        v = intensity(t)
        pos = k % 16
        ci = chapter_index(t)

        # Kick on 1 and 3, with a pushed eighth before the bar line once the
        # film is really moving — that push is most of what makes it feel urgent.
        if v >= 0.22 and pos in (0, 8):
            place(KICK, t, 0.62 * (0.55 + 0.45 * v))
        if v >= 0.78 and pos == 14:
            place(KICK, t, 0.34 * v)
        # Backbeat on 2 and 4.
        if v >= 0.66 and pos in (4, 12):
            place(SNARE, t, 0.26 * v)
        # Eighths, doubling to sixteenths at the top of the curve.
        if v >= 0.45 and (k % 2 == 0 or v >= 0.80):
            openish = (pos == 14)
            place(HATO if openish else HAT, t,
                  (0.22 if openish else 0.15) * v, pan=0.35 if (k % 4 == 2) else -0.25)
        # The ostinato runs on eighths, alternating sides.
        if v >= 0.40 and k % 2 == 0:
            f0 = FIGURES[ci][(k // 2) % 4]
            place(kit.pluck(f0, 0.34, 0.22), t, 0.17 * v, pan=-0.30 if (k % 4) else 0.30)

        t += step; k += 1

    # ---- chapter markers ----------------------------------------------------
    for i, ct in enumerate(CHAP_T):
        nxt = INTENSITY[i]
        place(SUB, ct, 0.34 + 0.22 * nxt)
        # A riser only into a chapter that lifts. Rising into the candid chapter
        # would promise a climax the film then deliberately refuses to deliver.
        if i > 0 and INTENSITY[i] > INTENSITY[i - 1] and ct >= 2.0:
            place(RISER, ct - 2.0, 0.055 + 0.075 * nxt)

    # ---- scene bells --------------------------------------------------------
    for c in CUTS:
        if any(abs(c - ct) < 0.01 for ct in CHAP_T):
            continue                       # chapter changes already have the impact
        place(kit.pluck(A3, 1.15, 0.34), c, 0.13)

    # ---- the sustained bed --------------------------------------------------
    evL, evR = kit.buses()
    L = array.array('h', bytes(2 * N)); R = array.array('h', bytes(2 * N))
    tau, inv = 2.0 * math.pi, 1.0 / SR
    for i in range(N):
        t = i * inv
        v = intensity(t)

        bed = (0.50 * math.sin(tau * D2 * t) + 0.28 * math.sin(tau * A2 * t)
               + 0.12 * math.sin(tau * D3 * t + 0.4))
        bed *= 0.82 + 0.18 * math.sin(tau * 0.037 * t)

        w = chapter_mix(t)
        pad = 0.0
        for kk, (f1, f2, f3) in enumerate(VOICINGS[:NCH]):
            wk = w[kk]
            if wk <= 0.0001: continue
            pad += wk * (0.30 * math.sin(tau * f1 * t)
                         + 0.26 * math.sin(tau * f2 * t + 1.1)
                         + 0.16 * math.sin(tau * f3 * t + 0.7))
        pad *= fade(t / 3.0) * (0.70 + 0.30 * math.sin(tau * 0.029 * t + 1.0))

        # The bass pulse doubles the kick on the eighths once the film is moving.
        drive = 0.0
        if v >= 0.30:
            ph = (t % (BEAT / 2.0)) / (BEAT / 2.0)
            drive = math.sin(tau * D2 * t) * math.exp(-ph * 5.0) * 0.30 * v

        # The sustained bed follows the curve too. Without this the drone sets a
        # floor the kit cannot get below, and the whole film measures within two
        # decibels of itself — technically an arc, audibly flat.
        sus = 0.42 + 0.58 * v

        env = fade(t / 3.0) * (1.0 - fade((t - (DUR - 3.0)) / 3.0))
        mono = ((0.26 * bed + 0.24 * pad) * sus + drive) * env
        wide = 0.14 * pad * sus * env
        l = mono + wide + evL[i] * env
        r = mono - wide + evR[i] * env
        l = math.tanh(l * 1.05) * 0.50
        r = math.tanh(r * 1.05) * 0.50
        L[i] = int(max(-32767, min(32767, l * 32767)))
        R[i] = int(max(-32767, min(32767, r * 32767)))
    return L, R


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '../build/score.wav'
    l, r = render(); write_wav(out, l, r, SR)
    peak = max(max(l), -min(l), max(r), -min(r)) / 32767.0
    print(f"score -> {out}  {DUR:.2f}s  {len(CUTS)} cuts, {NCH} chapters, "
          f"{BPM:.0f} bpm  peak {20*math.log10(peak):.1f} dBFS")
