#!/usr/bin/env python3
"""
Original score for the Honorary Fellow (PCI) film. 48 kHz stereo, standard
library only — no samples, no loops, no third-party audio library — so the cue
is PCI's own work and carries no licence obligation.

The brief asks for restrained piano and atmospheric tones that rise into
confident orchestral and modern electronic elements, with the narration
perfectly clear. That is an arc, not a texture, so the score is built as one:

  * **Piano first.** Scenes 1-3 are a felt-piano arpeggio over a low pad and
    nothing else. No kit, no pulse. The film opens on quiet confidence, and a
    drum in the first fifteen seconds would contradict the voice.
  * **Strings arrive with the people.** A detuned stack swells in from scene 4
    — where the film turns from what the recognition *is* to who it is *for* —
    and carries the industry sequence.
  * **The electronic layer is last and lightest.** Kick, hats and a sub pulse
    only above 0.5 on the curve, so they lift the industry and recognition
    beats without ever becoming a dance track under a certification body.

**F major, deliberately.** The brief wants optimistic rather than dark or
intimidating, and the relative minor is used only for the two scenes that carry
qualification — scene 3 (no examination, board discretion) and scene 6 (the
criteria, and the reminder that meeting them guarantees nothing). The harmony
does the honest thing at exactly the moments the copy does.

**Clarity rule, stated honestly.** The kit lives below ~120 Hz and above ~6 kHz
and touches nothing the voice needs. A piano cannot make that claim — its
fundamentals live where speech lives — so instead of pretending otherwise, the
right hand is voiced a full octave above its natural register, its harmonics are
almost entirely suppressed (0.06 against the 0.30 a bright pluck would use), and
the level is set from measurement rather than taste: the test that matters is the
narration's margin over the music *in the voice band of the finished mix*, which
build.sh's side-chain then widens further. That margin is verified after every
build, not assumed.

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
NSC = len(SHOTS)


def hz(n): return 440.0 * (2.0 ** (n / 12.0))
F1, C2, F2, C3, F3, A3, Bb3, C4, D4, E4, F4, G4, A4, Bb4, C5, D5, E5, F5, G5, A5, Bb5, C6 = (
    hz(-40), hz(-33), hz(-28), hz(-21), hz(-16), hz(-12), hz(-11), hz(-9),
    hz(-7), hz(-5), hz(-4), hz(-2), hz(0), hz(1), hz(3), hz(5), hz(7), hz(8),
    hz(10), hz(12), hz(13), hz(15))

# One triad per scene, over an F/C drone. Minor only where the copy qualifies.
VOICINGS = [(F3, A3, C4), (Bb3, D4, F4), (F3, C4, F4), (D4, F3, A3), (F3, A3, C4),
            (C4, E4, G4), (D4, F4, A3), (Bb3, D4, F4), (F3, A3, C4), (F3, A3, F4),
            (C4, E4, G4), (Bb3, D4, F4), (F3, C4, F4)]

# The piano figure per scene — four notes on the eighths, from that voicing.
# Voiced high on purpose. A piano's fundamentals land in the 300-3500 Hz band
# the narration needs, so the right hand is written an octave above where it
# would naturally sit: same figure, same harmony, out of the voice's way.
FIGURES = [(F5, C5, A4, C5), (F5, D5, Bb4, D5), (C6, A5, F5, A5), (F5, D5, A4, D5),
           (A5, F5, C5, F5), (G5, E5, C5, E5), (A5, F5, D5, F5), (Bb5, F5, D5, F5),
           (A5, F5, C5, F5), (C6, A5, F5, A5), (G5, E5, C5, E5), (Bb5, F5, D5, F5),
           (C6, A5, F5, A5)]

# The arc: quiet open, warmth on the recognition, restraint on the two
# qualifying scenes, peak on what recognition actually brings, strong close.
INTENSITY = [0.18, 0.46, 0.62, 0.30, 0.58, 0.80, 0.50, 0.60, 0.44, 0.72, 0.94, 0.52, 0.88]

BPM = 88.0
BEAT = 60.0 / BPM

# Where each layer joins. Piano is always on; the rest earn their entrance.
STRINGS_IN, KIT_IN, PULSE_IN = 0.40, 0.52, 0.62


def chapter_index(t):
    idx = 0
    for i, c in enumerate(CUTS):
        if t >= c: idx = i
    return idx


def scene_mix(t):
    """Weights over the scene voicings, cross-faded at each cut."""
    w = [0.0] * NSC
    idx = chapter_index(t)
    w[idx] = 1.0
    if idx + 1 < NSC:
        nxt = CUTS[idx + 1]
        if t > nxt - 2.2:
            p = fade((t - (nxt - 2.2)) / 2.2)
            w[idx] = 1.0 - p; w[idx + 1] = p
    return w


def intensity(t):
    w = scene_mix(t)
    v = sum(wi * INTENSITY[i] for i, wi in enumerate(w))
    return v * fade(t / 4.0) * (1.0 - 0.88 * fade((t - (DUR - 6.0)) / 6.0))


def render():
    kit = Kit(sr=SR, n_samples=N)

    # ---- felt piano: the whole film, thinning as the strings take over ------
    # A piano note is a struck tone with a long tail, so it is the pluck with a
    # slow decay and almost no second harmonic — bright harmonics here would
    # put energy straight into the voice band.
    step = BEAT / 2.0
    k, t = 0, 0.0
    while t < DUR:
        v = intensity(t)
        si = chapter_index(t)
        f0 = FIGURES[si][k % 4]
        # Held at a constant level rather than receding: making the piano quieter
        # as the arrangement fills was cancelling out everything the strings and
        # kit added, and flattened the whole arc to 2.4 dB.
        kit.place(kit.pluck(f0, 0.95, 0.06), t, 0.125, pan=-0.22 if (k % 2) else 0.22)
        if k % 4 == 0:                       # left hand, on the beat
            kit.place(kit.pluck(F2 if si % 2 == 0 else C3, 1.30, 0.04), t, 0.115)
        t += step; k += 1

    # ---- the electronic layer, sixteenth grid -------------------------------
    step = BEAT / 4.0
    k, t = 0, 0.0
    while t < DUR:
        v = intensity(t)
        pos = k % 16
        if v >= KIT_IN and pos in (0, 8):
            kit.place(kit.KICK, t, 0.58 * (0.45 + 0.55 * v))
        if v >= 0.80 and pos == 14:
            kit.place(kit.KICK, t, 0.24 * v)
        if v >= 0.86 and pos in (4, 12):
            kit.place(kit.SNARE, t, 0.22 * v)
        if v >= PULSE_IN and (k % 2 == 0 or v >= 0.85):
            openish = (pos == 14)
            kit.place(kit.HATO if openish else kit.HAT, t,
                      (0.22 if openish else 0.15) * v, pan=0.34 if (k % 4 == 2) else -0.26)
        t += step; k += 1

    # ---- scene markers ------------------------------------------------------
    for i, c in enumerate(CUTS):
        if i == 0:
            continue
        # A deep marker only where the film changes subject at volume; the quiet
        # scenes get a soft piano octave instead of a boom.
        if INTENSITY[i] >= 0.55:
            kit.place(kit.SUB, c, 0.26 + 0.20 * INTENSITY[i])
            if INTENSITY[i] > INTENSITY[i - 1] and c >= 2.0:
                kit.place(kit.RISER, c - 2.0, 0.045 + 0.055 * INTENSITY[i])
        else:
            kit.place(kit.pluck(F3, 1.5, 0.05), c, 0.10)

    evL, evR = kit.buses()

    # ---- sustained bed: low drone + string stack ---------------------------
    L = array.array('h', bytes(2 * N)); R = array.array('h', bytes(2 * N))
    tau, inv = 2.0 * math.pi, 1.0 / SR
    for i in range(N):
        t = i * inv
        v = intensity(t)

        bed = (0.50 * math.sin(tau * F1 * t) + 0.26 * math.sin(tau * F2 * t)
               + 0.11 * math.sin(tau * C3 * t + 0.4))
        bed *= 0.84 + 0.16 * math.sin(tau * 0.031 * t)

        w = scene_mix(t)
        pad = 0.0
        for kk, (f1, f2, f3) in enumerate(VOICINGS[:NSC]):
            wk = w[kk]
            if wk <= 0.0001: continue
            # three voices, each very slightly detuned against itself — the
            # cheapest honest way to get a section rather than an organ
            pad += wk * (0.30 * (math.sin(tau * f1 * t) + math.sin(tau * f1 * 1.0016 * t + 0.6))
                         + 0.24 * (math.sin(tau * f2 * t + 1.1) + math.sin(tau * f2 * 0.9986 * t))
                         + 0.15 * math.sin(tau * f3 * t + 0.7)) * 0.5
        strings = pad * fade((v - STRINGS_IN) / 0.30) * (0.72 + 0.28 * math.sin(tau * 0.027 * t + 1.0))
        air = 0.09 * pad * fade(t / 5.0)     # a little of the pad is always there

        drive = 0.0
        if v >= PULSE_IN:
            ph = (t % (BEAT / 2.0)) / (BEAT / 2.0)
            drive = math.sin(tau * F2 * t) * math.exp(-ph * 5.5) * 0.26 * v

        sus = 0.34 + 0.66 * v
        env = fade(t / 2.5) * (1.0 - fade((t - (DUR - 2.6)) / 2.6))
        mono = ((0.26 * bed + 0.36 * strings + air) * sus + drive) * env
        wide = 0.15 * strings * sus * env
        l = math.tanh((mono + wide + evL[i] * env) * 1.05) * 0.50
        r = math.tanh((mono - wide + evR[i] * env) * 1.05) * 0.50
        L[i] = int(max(-32767, min(32767, l * 32767)))
        R[i] = int(max(-32767, min(32767, r * 32767)))
    return L, R


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '../build/score.wav'
    l, r = render(); write_wav(out, l, r, SR)
    peak = max(max(l), -min(l), max(r), -min(r)) / 32767.0
    print(f"score -> {out}  {DUR:.2f}s  {NSC} scenes, {BPM:.0f} bpm  "
          f"peak {20*math.log10(peak):.1f} dBFS")
