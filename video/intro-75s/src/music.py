#!/usr/bin/env python3
"""
Original ambient score for the PCI AI 75-second institutional film.
48 kHz stereo, written from scratch — no samples, no library, no third-party
loop — so the cue is PCI's own work and carries no licence obligation.
Pure standard library: additive synthesis -> WAV.

Musical intent, matched to the cut:

  D minor, 64 bpm, and deliberately restrained. A low sustained bed runs under
  the whole film. A soft struck bell marks each cut, so the picture edit has an
  audible reason rather than just happening. The identity shot (36.30) adds an
  upper voice. The closing shot (57.60) is the one real harmonic event: the
  picture inverts to a light ground, and the score lifts with it into F major,
  D minor's relative — brightening without becoming triumphant. The end card
  resolves warmly back to the tonic.

  Levels sit around -23 LUFS with a scooped mid-range, so a voiceover reads over
  the top without ducking. See ../README.md for the mix command.

  python3 music.py ../build/score.wav
"""
import array
import math
import struct
import sys

SR = 48_000
DUR = 75.0
N = int(SR * DUR)

# Cut list — must stay in step with SHOTS in scene.html.
CUTS = [0.00, 8.50, 16.60, 26.90, 36.30, 47.40, 57.60, 70.80]
LIGHT_IN = 57.60   # the harmonic lift, with the visual inversion
ENDCARD = 70.80


def hz(semitones_from_a4: float) -> float:
    return 440.0 * (2.0 ** (semitones_from_a4 / 12.0))


D2, A2, D3, F3, A3, C4, D4, E4, F4, A4, D5 = (
    hz(-31), hz(-24), hz(-19), hz(-16), hz(-12), hz(-9),
    hz(-7), hz(-5), hz(-4), hz(0), hz(5),
)


def fade(x: float) -> float:
    """Smooth 0..1 (smoothstep)."""
    x = 0.0 if x < 0.0 else 1.0 if x > 1.0 else x
    return x * x * (3.0 - 2.0 * x)


def swell(t, start, rise, hold, fall):
    if t < start:
        return 0.0
    u = t - start
    if u < rise:
        return fade(u / rise)
    if u < rise + hold:
        return 1.0
    if u < rise + hold + fall:
        return 1.0 - fade((u - rise - hold) / fall)
    return 0.0


def pluck(t, at, decay):
    """Fast attack, exponential decay — a struck bell."""
    if t < at:
        return 0.0
    u = t - at
    attack = fade(u / 0.006) if u < 0.006 else 1.0
    return attack * math.exp(-u / decay)


def render():
    left = array.array('h', bytes(2 * N))
    right = array.array('h', bytes(2 * N))

    tau = 2.0 * math.pi
    inv = 1.0 / SR

    # Master shape: up over the first 2.5 s, down over the last 2.2 s.
    for i in range(N):
        t = i * inv

        # ---- low bed: tonic fifth, always present -------------------------
        bed = (0.50 * math.sin(tau * D2 * t)
               + 0.30 * math.sin(tau * A2 * t)
               + 0.14 * math.sin(tau * D3 * t + 0.4))
        # a slow breath so the drone is not static
        bed *= 0.82 + 0.18 * math.sin(tau * 0.055 * t)

        # ---- pad: D minor through the body, F major from the light scene --
        lift = fade((t - LIGHT_IN) / 2.2)          # 0 before the cut, 1 after
        res = fade((t - ENDCARD) / 1.6)            # resolve on the end card
        minor = (1.0 - lift) + res                 # back to D minor at the end
        major = lift * (1.0 - res)
        minor = min(minor, 1.0)

        pad = minor * (0.34 * math.sin(tau * F3 * t)
                       + 0.30 * math.sin(tau * A3 * t + 1.1)
                       + 0.18 * math.sin(tau * D4 * t + 0.7))
        pad += major * (0.32 * math.sin(tau * F3 * t)
                        + 0.28 * math.sin(tau * C4 * t + 1.1)
                        + 0.20 * math.sin(tau * A3 * t + 0.7)
                        + 0.12 * math.sin(tau * F4 * t + 2.0))
        pad *= swell(t, 1.20, 3.0, 999.0, 0.0) * (0.70 + 0.30 * math.sin(tau * 0.041 * t + 1.0))

        # ---- upper voice: enters on the identity shot ---------------------
        upper = (0.16 * math.sin(tau * D5 * t + 0.3) + 0.10 * math.sin(tau * A4 * t))
        upper *= swell(t, 36.30, 2.4, 999.0, 0.0) * (0.55 + 0.45 * math.sin(tau * 0.075 * t))
        upper *= (1.0 - 0.45 * lift)   # step back so the light scene stays open

        # ---- bells on the cuts --------------------------------------------
        bell = 0.0
        for k, c in enumerate(CUTS):
            if t < c - 0.05 or t > c + 6.0:
                continue
            # the tonic on the first and last cut, the fifth in between
            f = D4 if k in (0, len(CUTS) - 1) else (A3 if k % 2 else F4)
            env = pluck(t, c, 1.55)
            bell += env * (0.30 * math.sin(tau * f * t)
                           + 0.12 * math.sin(tau * f * 2.0 * t)
                           + 0.05 * math.sin(tau * f * 3.01 * t))

        # ---- a single low swell under the closing statement ---------------
        close = 0.20 * math.sin(tau * A2 * t + 0.9) * swell(t, 57.20, 1.8, 8.0, 3.0)

        # ---- sum, shape, place --------------------------------------------
        env_master = fade(t / 2.5) * (1.0 - fade((t - (DUR - 2.2)) / 2.2))
        mono = (0.34 * bed + 0.30 * pad + 0.26 * upper + 0.34 * bell + close) * env_master

        # gentle stereo: the pad and bells sit slightly wide, the bed centred
        wide = 0.16 * (pad - upper) * env_master
        l = mono + wide
        r = mono - wide

        # soft clip — musical rather than a hard ceiling
        l = math.tanh(l * 1.05) * 0.50
        r = math.tanh(r * 1.05) * 0.50

        left[i] = int(max(-32767, min(32767, l * 32767)))
        right[i] = int(max(-32767, min(32767, r * 32767)))

    return left, right


def write_wav(path, left, right):
    data = array.array('h', bytes(4 * N))
    data[0::2] = left
    data[1::2] = right
    raw = data.tobytes()
    with open(path, 'wb') as f:
        f.write(b'RIFF' + struct.pack('<I', 36 + len(raw)) + b'WAVE')
        f.write(b'fmt ' + struct.pack('<IHHIIHH', 16, 1, 2, SR, SR * 4, 4, 16))
        f.write(b'data' + struct.pack('<I', len(raw)) + raw)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '../build/score.wav'
    l, r = render()
    write_wav(out, l, r)
    peak = max(max(l), -min(l), max(r), -min(r)) / 32767.0
    rms = (sum(x * x for x in l[::97]) / len(l[::97])) ** 0.5 / 32767.0
    print(f"score -> {out}  {DUR:.1f}s  peak {20*math.log10(peak):.1f} dBFS  "
          f"rms ~{20*math.log10(rms):.1f} dBFS")
