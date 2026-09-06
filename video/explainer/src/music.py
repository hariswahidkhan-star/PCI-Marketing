#!/usr/bin/env python3
"""
Original score for the PCI AI explainer. 48 kHz stereo, standard library only —
no samples, no loops, no third-party library — so the cue is PCI's own work and
carries no licence obligation.

Nearly four minutes is long enough that a single drone becomes wallpaper, so the
score is built in chapters rather than as one bed. It reads the measured cut list
from timeline.json (written by sync.py), places a soft bell on every scene change
and a deeper one on every chapter change, and shifts harmony per chapter:
D minor for the problem, its relative F major as the objective arrives, back to
D minor for the framework, an open fifth for the assessment chapters, F major
again for industries, and a warm resolve on the close.

Levels sit low with a scooped mid-range so the narration reads over the top.

  python3 music.py ../build/score.wav
"""
import array, json, math, os, struct, sys

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


def hz(n): return 440.0 * (2.0 ** (n / 12.0))
D2, A2, D3, F3, G3, A3, C4, D4, E4, F4, A4, D5 = (
    hz(-31), hz(-24), hz(-19), hz(-16), hz(-14), hz(-12), hz(-9), hz(-7), hz(-5), hz(-4), hz(0), hz(5))

# per-chapter triad above the D/A drone
VOICINGS = [(F3, A3, D4), (F3, C4, A3), (F3, A3, D4), (D3, A3, E4),
            (F3, C4, A4), (F3, A3, D4), (D3, F3, A3)]


def fade(x):
    x = 0.0 if x < 0 else 1.0 if x > 1 else x
    return x * x * (3.0 - 2.0 * x)


def pluck(t, at, decay):
    if t < at: return 0.0
    u = t - at
    return (fade(u / 0.006) if u < 0.006 else 1.0) * math.exp(-u / decay)


def chapter_mix(t):
    """Weights over the chapter voicings, cross-faded at each boundary."""
    w = [0.0] * len(CHAP_T)
    idx = 0
    for i, ct in enumerate(CHAP_T):
        if t >= ct: idx = i
    w[idx] = 1.0
    if idx + 1 < len(CHAP_T):
        nxt = CHAP_T[idx + 1]
        if t > nxt - 3.0:
            p = fade((t - (nxt - 3.0)) / 3.0)
            w[idx] = 1.0 - p; w[idx + 1] = p
    return w


def render():
    L = array.array('h', bytes(2 * N)); R = array.array('h', bytes(2 * N))
    tau, inv = 2.0 * math.pi, 1.0 / SR
    for i in range(N):
        t = i * inv
        bed = (0.50 * math.sin(tau * D2 * t) + 0.28 * math.sin(tau * A2 * t)
               + 0.12 * math.sin(tau * D3 * t + 0.4))
        bed *= 0.82 + 0.18 * math.sin(tau * 0.037 * t)

        w = chapter_mix(t)
        pad = 0.0
        for k, (f1, f2, f3) in enumerate(VOICINGS[:len(w)]):
            if w[k] <= 0.0001: continue
            pad += w[k] * (0.30 * math.sin(tau * f1 * t)
                           + 0.26 * math.sin(tau * f2 * t + 1.1)
                           + 0.16 * math.sin(tau * f3 * t + 0.7))
        pad *= fade(t / 3.0) * (0.70 + 0.30 * math.sin(tau * 0.029 * t + 1.0))

        bell = 0.0
        for c in CUTS:
            if t < c - 0.05 or t > c + 5.0: continue
            deep = any(abs(c - ct) < 0.01 for ct in CHAP_T)
            f = D4 if deep else A3
            env = pluck(t, c, 1.9 if deep else 1.25)
            amp = 0.34 if deep else 0.19
            bell += env * amp * (math.sin(tau * f * t) + 0.34 * math.sin(tau * f * 2 * t))

        env = fade(t / 3.0) * (1.0 - fade((t - (DUR - 3.0)) / 3.0))
        mono = (0.34 * bed + 0.30 * pad + 0.30 * bell) * env
        wide = 0.14 * pad * env
        l = math.tanh((mono + wide) * 1.05) * 0.46
        r = math.tanh((mono - wide) * 1.05) * 0.46
        L[i] = int(max(-32767, min(32767, l * 32767)))
        R[i] = int(max(-32767, min(32767, r * 32767)))
    return L, R


def write_wav(path, L, R):
    d = array.array('h', bytes(4 * N)); d[0::2] = L; d[1::2] = R
    raw = d.tobytes()
    with open(path, 'wb') as f:
        f.write(b'RIFF' + struct.pack('<I', 36 + len(raw)) + b'WAVE')
        f.write(b'fmt ' + struct.pack('<IHHIIHH', 16, 1, 2, SR, SR * 4, 4, 16))
        f.write(b'data' + struct.pack('<I', len(raw)) + raw)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '../build/score.wav'
    l, r = render(); write_wav(out, l, r)
    peak = max(max(l), -min(l), max(r), -min(r)) / 32767.0
    print(f"score -> {out}  {DUR:.2f}s  {len(CUTS)} cuts, {len(CHAP_T)} chapters  "
          f"peak {20*math.log10(peak):.1f} dBFS")
