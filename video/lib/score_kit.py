#!/usr/bin/env python3
"""
Shared rhythm engine for the PCI film scores.

Standard library only — no samples, no loops, no third-party audio library — so
every cue built on this remains PCI's own work and carries no licence
obligation. Everything here is deterministic: the noise source is seeded, so the
same arrangement renders byte-identical every time.

This module owns the *sounds and the mixing*. It deliberately owns no musical
decisions: tempo, harmony, arrangement and the intensity curve belong to each
film's own `music.py`, because that is the part that should differ between a
15-second launch cut and a four-minute explainer.

Voicing rule the three films share: **the kit lives below ~120 Hz and above
~6 kHz.** The mid-range where narration sits is left thin, so a score can be
busy without ever competing with the voice.

    from score_kit import Kit
    kit = Kit(sr=48000, n_samples=N)
    kit.place(kit.KICK, t=1.25, gain=0.6)
    evL, evR = kit.buses()
"""
import array
import math
import random

__all__ = ['Kit', 'fade']


def fade(x):
    """Smoothstep 0..1."""
    x = 0.0 if x < 0 else 1.0 if x > 1 else x
    return x * x * (3.0 - 2.0 * x)


class Kit:
    """Percussion and plucks, rendered once into buffers and mixed in at onsets.

    Evaluating every voice at every sample of a four-minute film would be both
    slower and no more accurate — a struck sound is silent for most of its
    timeline, so it is cheaper to render one copy and add it where it lands.
    """

    def __init__(self, sr=48_000, n_samples=0, seed=20260906):
        self.sr = sr
        self.n = n_samples
        self._evL = array.array('f', bytes(4 * n_samples))
        self._evR = array.array('f', bytes(4 * n_samples))
        rng = random.Random(seed)
        self._noise = [rng.uniform(-1.0, 1.0) for _ in range(1 << 16)]
        self._nmask = (1 << 16) - 1
        self._plucks = {}
        self.KICK = self._kick()
        self.SUB = self._sub()
        self.HAT = self._hat(False)
        self.HATO = self._hat(True)
        self.SNARE = self._snare()
        self.RISER = self._riser()

    # -- primitives ---------------------------------------------------------

    def _make(self, seconds, fn):
        n = int(self.sr * seconds)
        b = array.array('f', bytes(4 * n))
        for i in range(n):
            b[i] = fn(i / self.sr)
        return b

    def _nz(self, i):
        return self._noise[i & self._nmask]

    # -- the kit ------------------------------------------------------------

    def _kick(self):
        """Pitch sweep 120 -> 44 Hz. All of its energy sits under the narration."""
        sr = self.sr
        def f(u):
            ph = 44.0 * u + (120.0 - 44.0) * 0.045 * (1.0 - math.exp(-u / 0.045))
            env = math.exp(-u / 0.16) * fade(u / 0.002)
            click = math.exp(-u / 0.004) * self._nz(int(u * sr)) * 0.25
            return math.sin(2 * math.pi * ph) * env + click * env
        return self._make(0.40, f)

    def _sub(self):
        """A deep, slow boom — marks a change of subject, not a beat."""
        sr = self.sr
        def f(u):
            ph = 33.0 * u + 22.0 * 0.09 * (1.0 - math.exp(-u / 0.09))
            env = math.exp(-u / 0.65) * fade(u / 0.004)
            air = math.exp(-u / 0.28) * self._nz(int(u * sr) * 3) * 0.10
            return math.sin(2 * math.pi * ph) * env * 0.95 + air
        return self._make(2.2, f)

    def _hat(self, open_):
        """Filtered noise, high only — nothing here touches the voice band."""
        sr = self.sr
        dec = 0.13 if open_ else 0.028
        def f(u):
            i = int(u * sr) * 7
            hp = self._nz(i) - self._nz(i + 1)   # first-difference high-pass
            return hp * math.exp(-u / dec)
        return self._make(0.30 if open_ else 0.09, f)

    def _snare(self):
        sr = self.sr
        def f(u):
            i = int(u * sr) * 11
            body = 0.35 * math.sin(2 * math.pi * 186.0 * u) * math.exp(-u / 0.055)
            return (self._nz(i) - self._nz(i + 1)) * math.exp(-u / 0.10) * 0.8 + body
        return self._make(0.26, f)

    def _riser(self):
        """Two seconds of rising noise into a change. Tension, then release."""
        sr = self.sr
        def f(u):
            p = u / 2.0
            i = int(u * sr) * 13
            bright = (self._nz(i) - self._nz(i + 1)) * (0.25 + 0.75 * p)
            tone = math.sin(2 * math.pi * (220.0 + 500.0 * p * p) * u) * 0.30 * p
            return (bright * 0.55 + tone) * (p ** 1.6)
        return self._make(2.0, f)

    def pluck(self, f0, decay, harm=0.30):
        """A struck tone. Cached, so a repeated ostinato note costs nothing."""
        key = (round(f0, 3), decay, harm)
        b = self._plucks.get(key)
        if b is None:
            def f(u):
                env = math.exp(-u / decay) * fade(u / 0.004)
                return (math.sin(2 * math.pi * f0 * u)
                        + harm * math.sin(2 * math.pi * f0 * 2 * u + 0.5)) * env
            b = self._make(min(decay * 4.0, 1.6), f)
            self._plucks[key] = b
        return b

    # -- mixing -------------------------------------------------------------

    def place(self, b, t, gain, pan=0.0):
        """Mix a buffer in at time `t`. pan -1 hard left, +1 hard right."""
        start = int(t * self.sr)
        if start >= self.n or start < 0:
            return
        # Equal-power pan: a hard-panned hat must not arrive louder than a
        # centred one, which a naive linear law would do.
        ang = (pan + 1.0) * 0.25 * math.pi
        gl = gain * math.cos(ang) * 1.41421356
        gr = gain * math.sin(ang) * 1.41421356
        n = min(len(b), self.n - start)
        evL, evR = self._evL, self._evR
        for i in range(n):
            v = b[i]
            evL[start + i] += v * gl
            evR[start + i] += v * gr

    def buses(self):
        """The accumulated left/right event buses, to sum with the sustained bed."""
        return self._evL, self._evR


def write_wav(path, left, right, sr=48_000):
    n = len(left)
    d = array.array('h', bytes(4 * n))
    d[0::2] = left
    d[1::2] = right
    raw = d.tobytes()
    import struct
    with open(path, 'wb') as f:
        f.write(b'RIFF' + struct.pack('<I', 36 + len(raw)) + b'WAVE')
        f.write(b'fmt ' + struct.pack('<IHHIIHH', 16, 1, 2, sr, sr * 4, 4, 16))
        f.write(b'data' + struct.pack('<I', len(raw)) + raw)
