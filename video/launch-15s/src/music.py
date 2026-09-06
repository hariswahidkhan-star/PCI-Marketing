#!/usr/bin/env python3
"""
Original score for the PCI post-launch film — 15 seconds, 48 kHz stereo.

Written from scratch (no samples, no external library, no third-party loop), so
the cue is PCI's own work and carries no licence obligation. Pure standard
library: additive synthesis -> WAV.

Musical intent, matched to the cut:
  D minor. A low sustained bed under the whole film; a soft bell on each cut so
  the picture edit has an audible reason; a gentle lift under the invitation
  (shot 4); a warm resolve to the tonic on the end card.

  Fifteen seconds has no time to build, so the kit is in from the first bar and
  simply tightens: eighths to sixteenths under the ask, then out of the way for
  the resolve. 104 bpm and the same kit as the 75-second film and the explainer,
  so the three read as one body of work.

  Drive comes from rhythm, not level. The kit lives below ~120 Hz and above
  ~6 kHz, leaving the mid-range thin so the narration reads over the top; the
  mix side-chains it under the voice on top of that.

  python3 music.py ../build/score.wav
"""
import array
import math
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from score_kit import Kit          # noqa: E402

SR = 48_000
DUR = 15.0
N = int(SR * DUR)

# --- pitches (equal temperament, A4 = 440) --------------------------------
def hz(semitones_from_a4: float) -> float:
    return 440.0 * (2.0 ** (semitones_from_a4 / 12.0))

D2, A2, D3, F3, A3, D4, F4, A4, D5, E5, G4 = (
    hz(-31), hz(-24), hz(-19), hz(-16), hz(-12), hz(-7), hz(-4), hz(0), hz(5), hz(7), hz(-2)
)

# --- envelopes ------------------------------------------------------------
def fade(x: float) -> float:
    """Equal-power-ish smooth 0..1."""
    x = 0.0 if x < 0.0 else 1.0 if x > 1.0 else x
    return x * x * (3.0 - 2.0 * x)

def swell(t: float, start: float, rise: float, hold: float, fall: float) -> float:
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

def pluck(t: float, at: float, decay: float) -> float:
    """Fast attack, exponential decay — a struck bell."""
    if t < at:
        return 0.0
    u = t - at
    attack = fade(u / 0.006) if u < 0.006 else 1.0
    return attack * math.exp(-u / decay)

# --- voices ---------------------------------------------------------------
CUTS = [0.10, 3.40, 6.80, 9.90, 13.10]          # bell on every picture cut
BELL_F = [D5, A4, D5, F4 * 2, D4 * 2]           # falling-then-resolving contour
BELL_G = [0.16, 0.13, 0.13, 0.15, 0.19]

def pad(t: float, f: float, detune: float) -> float:
    """Two slightly detuned sines + a quiet octave: a soft synth pad."""
    a = math.sin(2.0 * math.pi * f * t)
    b = math.sin(2.0 * math.pi * (f * (1.0 + detune)) * t + 0.7)
    c = math.sin(2.0 * math.pi * f * 2.0 * t + 1.3) * 0.16
    return (a + b) * 0.5 + c

BPM = 104.0
BEAT = 60.0 / BPM

# Drive keyframes: in from the top, tightening under the ask at 9.90, then
# stepping aside for the resolve so the end card is harmony and not drums.
DRIVE = [(0.00, 0.55), (3.40, 0.72), (6.80, 0.86), (9.90, 1.00),
         (12.60, 0.85), (13.10, 0.30), (DUR, 0.0)]


def intensity(t: float) -> float:
    if t <= DRIVE[0][0]:
        return DRIVE[0][1]
    for (t0, v0), (t1, v1) in zip(DRIVE, DRIVE[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * fade((t - t0) / (t1 - t0))
    return DRIVE[-1][1]


# --- the kit, on a sixteenth grid -----------------------------------------
# k counts sixteenths from the downbeat: a bar is 16, a beat is 4.
kit = Kit(sr=SR, n_samples=N)
_k, _t = 0, 0.0
while _t < DUR:
    _v = intensity(_t)
    _pos = _k % 16
    if _v >= 0.22 and _pos in (0, 8):
        kit.place(kit.KICK, _t, 0.58 * (0.55 + 0.45 * _v))
    if _v >= 0.86 and _pos == 14:
        kit.place(kit.KICK, _t, 0.30 * _v)
    if _v >= 0.66 and _pos in (4, 12):
        kit.place(kit.SNARE, _t, 0.22 * _v)
    if _v >= 0.45 and (_k % 2 == 0 or _v >= 0.90):
        _open = (_pos == 14)
        kit.place(kit.HATO if _open else kit.HAT, _t,
                  (0.19 if _open else 0.13) * _v, pan=0.35 if (_k % 4 == 2) else -0.25)
    if _v >= 0.40 and _k % 2 == 0:
        _f = (D4, A3, F3, A3)[(_k // 2) % 4]
        kit.place(kit.pluck(_f, 0.32, 0.22), _t, 0.14 * _v, pan=-0.30 if (_k % 4) else 0.30)
    _t += BEAT / 4.0
    _k += 1
kit.place(kit.SUB, 0.10, 0.40)
kit.place(kit.RISER, 7.90, 0.09)
evL, evR = kit.buses()

left = array.array("h", bytes(2 * N))
right = array.array("h", bytes(2 * N))

for i in range(N):
    t = i / SR

    # Sub bed: the tonic under everything, gently breathing.
    breathe = 0.86 + 0.14 * math.sin(2.0 * math.pi * 0.11 * t)
    sig = 0.30 * math.sin(2.0 * math.pi * D2 * t) * breathe * swell(t, 0.0, 1.6, 11.4, 2.0)
    sig += 0.13 * math.sin(2.0 * math.pi * A2 * t + 0.4) * swell(t, 0.4, 2.2, 10.4, 2.0)

    # Chord bed: Dm through the body, opening to a brighter Dm(add9) under the
    # invitation, resolving to an open D5 on the end card.
    body = swell(t, 0.5, 2.4, 9.4, 2.6)
    sig += 0.115 * pad(t, D3, 0.0016) * body
    sig += 0.085 * pad(t, F3, 0.0021) * body
    sig += 0.075 * pad(t, A3, 0.0013) * body

    # Lift under shot 4 (the ask) — an added 9th, the only "brightening" move.
    lift = swell(t, 9.70, 1.5, 1.9, 1.6)
    sig += 0.070 * pad(t, E5, 0.0011) * lift
    sig += 0.055 * pad(t, G4, 0.0018) * lift

    # Resolve on the end card.
    res = swell(t, 13.05, 0.9, 0.6, 1.4)
    sig += 0.085 * pad(t, D4, 0.0009) * res
    sig += 0.060 * pad(t, A4, 0.0014) * res

    # Bells on the cuts.
    for at, f, g in zip(CUTS, BELL_F, BELL_G):
        e = pluck(t, at, 1.05)
        if e > 1e-4:
            sig += g * e * (
                math.sin(2.0 * math.pi * f * t)
                + 0.34 * math.sin(2.0 * math.pi * f * 2.0 * t)
                + 0.13 * math.sin(2.0 * math.pi * f * 3.01 * t)
            )

    # The sustained material follows the drive curve, so the kit is not fighting
    # a drone that never gets out of its way.
    sig *= 0.50 + 0.50 * intensity(t)

    # Master fades.
    sig *= fade(t / 0.9) * (1.0 - fade((t - 13.9) / 1.1))
    sig += (evL[i] + evR[i]) * 0.5 * fade(t / 0.4) * (1.0 - fade((t - 13.9) / 1.1))

    # Soft saturation keeps peaks polite without a limiter.
    sig = math.tanh(sig * 1.15) * 0.62

    # Cheap stereo width: a few samples of inter-channel delay on the pad.
    _kenv = fade(t / 0.4) * (1.0 - fade((t - 13.9) / 1.1))
    l = sig + (evL[i] - (evL[i] + evR[i]) * 0.5) * _kenv
    r = (sig * 0.94 + 0.06 * math.sin(2.0 * math.pi * D3 * (t - 0.0009)) * body * 0.115
         + (evR[i] - (evL[i] + evR[i]) * 0.5) * _kenv)

    left[i] = max(-32768, min(32767, int(l * 32767)))
    right[i] = max(-32768, min(32767, int(r * 32767)))

# --- interleave + write ---------------------------------------------------
inter = array.array("h", bytes(4 * N))
inter[0::2] = left
inter[1::2] = right
raw = inter.tobytes()

out = sys.argv[1] if len(sys.argv) > 1 else "score.wav"
with open(out, "wb") as fh:
    fh.write(b"RIFF")
    fh.write(struct.pack("<I", 36 + len(raw)))
    fh.write(b"WAVEfmt ")
    fh.write(struct.pack("<IHHIIHH", 16, 1, 2, SR, SR * 4, 4, 16))
    fh.write(b"data")
    fh.write(struct.pack("<I", len(raw)))
    fh.write(raw)

peak = max(max(left), -min(left), max(right), -min(right)) / 32767.0
print(f"{out}  {DUR:.2f}s  {SR} Hz stereo  peak {20 * math.log10(peak):.1f} dBFS")
