#!/usr/bin/env python3
"""
Original score for the PCI AI 75-second institutional film.
48 kHz stereo, written from scratch — no samples, no library, no third-party
loop — so the cue is PCI's own work and carries no licence obligation.
Pure standard library: additive synthesis -> WAV.

Musical intent, matched to the cut:

  D minor. A low sustained bed runs under the whole film and a struck bell marks
  each cut, so the picture edit has an audible reason rather than just happening.
  The identity shot (35.85) adds an upper voice. The closing shot (61.66) is the
  one real harmonic event: the picture inverts to a light ground, and the score
  lifts with it into F major, D minor's relative — brightening without becoming
  triumphant. The end card resolves warmly back to the tonic.

  Over that sits a kit on a 104 bpm grid, driven by an intensity curve that
  builds from the opening statement to the closing argument and then **steps
  back for the light inversion** — that moment is carried by the harmony, and
  drums on top of it would fight the thing the picture is doing. Same tempo and
  same kit as the other two films, so the set reads as one body of work.

  Drive comes from rhythm, not level. The kit lives below ~120 Hz and above
  ~6 kHz, leaving the mid-range thin so the narration reads over the top; the
  mix in build.sh side-chains it under the voice on top of that.

  python3 music.py ../build/score.wav
"""
import array
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from score_kit import Kit, write_wav          # noqa: E402

SR = 48_000
DUR = 75.0
N = int(SR * DUR)

# Cut list — must stay in step with SHOTS in scene.html.
CUTS = [0.00, 7.75, 15.94, 26.51, 35.85, 49.99, 61.66, 70.93]
LIGHT_IN = 61.66   # the harmonic lift, with the visual inversion
ENDCARD = 70.93

BPM = 104.0
BEAT = 60.0 / BPM

# The drive curve, as (time, weight) keyframes smoothstepped between. It climbs
# through the argument, peaks on the closing statement, and drops away at the
# light inversion so the harmony can carry that moment on its own.
DRIVE = [(0.00, 0.18), (7.75, 0.42), (15.94, 0.58), (26.51, 0.72),
         (35.85, 0.88), (49.99, 1.00), (61.66, 0.50), (70.93, 0.24), (DUR, 0.0)]


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


def intensity(t):
    """The drive curve at time t — interpolated, so it ramps rather than steps."""
    if t <= DRIVE[0][0]:
        return DRIVE[0][1]
    for (t0, v0), (t1, v1) in zip(DRIVE, DRIVE[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * fade((t - t0) / (t1 - t0))
    return DRIVE[-1][1]


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

    # ---- the kit, on a sixteenth grid -------------------------------------
    # k counts sixteenths from the downbeat: a bar is 16, a beat is 4. Each
    # element asks the drive curve whether it is playing yet, so the
    # arrangement thins and thickens by itself rather than being written out.
    kit = Kit(sr=SR, n_samples=N)
    step = BEAT / 4.0
    k, t = 0, 0.0
    while t < DUR:
        v = intensity(t)
        pos = k % 16
        if v >= 0.22 and pos in (0, 8):
            kit.place(kit.KICK, t, 0.60 * (0.55 + 0.45 * v))
        if v >= 0.80 and pos == 14:
            kit.place(kit.KICK, t, 0.32 * v)
        if v >= 0.66 and pos in (4, 12):
            kit.place(kit.SNARE, t, 0.24 * v)
        if v >= 0.45 and (k % 2 == 0 or v >= 0.82):
            openish = (pos == 14)
            kit.place(kit.HATO if openish else kit.HAT, t,
                      (0.20 if openish else 0.14) * v, pan=0.35 if (k % 4 == 2) else -0.25)
        if v >= 0.40 and k % 2 == 0:
            f0 = (D4, A3, F3, A3)[(k // 2) % 4] if t < LIGHT_IN else (F4, C4, A3, C4)[(k // 2) % 4]
            kit.place(kit.pluck(f0, 0.34, 0.22), t, 0.15 * v,
                      pan=-0.30 if (k % 4) else 0.30)
        t += step; k += 1

    # An impact on the first cut and on the harmonic inversion — the two places
    # the film changes what it is doing.
    kit.place(kit.SUB, 0.0, 0.42)
    kit.place(kit.SUB, LIGHT_IN, 0.46)
    kit.place(kit.RISER, LIGHT_IN - 2.0, 0.10)
    evL, evR = kit.buses()

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
        upper *= swell(t, 35.85, 2.4, 999.0, 0.0) * (0.55 + 0.45 * math.sin(tau * 0.075 * t))
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
        close = 0.20 * math.sin(tau * A2 * t + 0.9) * swell(t, 61.26, 1.8, 8.0, 3.0)

        # ---- sum, shape, place --------------------------------------------
        # The sustained bed follows the curve too. Without this the drone sets a
        # floor the kit cannot get below, and the film measures within a couple
        # of decibels of itself — technically an arc, audibly flat.
        sus = 0.45 + 0.55 * intensity(t)

        env_master = fade(t / 2.5) * (1.0 - fade((t - (DUR - 2.2)) / 2.2))
        mono = ((0.30 * bed + 0.27 * pad + 0.24 * upper) * sus
                + 0.34 * bell + close) * env_master

        # gentle stereo: the pad and bells sit slightly wide, the bed centred
        wide = 0.16 * (pad - upper) * sus * env_master
        l = mono + wide + evL[i] * env_master
        r = mono - wide + evR[i] * env_master

        # soft clip — musical rather than a hard ceiling
        l = math.tanh(l * 1.05) * 0.50
        r = math.tanh(r * 1.05) * 0.50

        left[i] = int(max(-32767, min(32767, l * 32767)))
        right[i] = int(max(-32767, min(32767, r * 32767)))

    return left, right


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '../build/score.wav'
    l, r = render()
    write_wav(out, l, r, SR)
    peak = max(max(l), -min(l), max(r), -min(r)) / 32767.0
    rms = (sum(x * x for x in l[::97]) / len(l[::97])) ** 0.5 / 32767.0
    print(f"score -> {out}  {DUR:.1f}s  peak {20*math.log10(peak):.1f} dBFS  "
          f"rms ~{20*math.log10(rms):.1f} dBFS")
