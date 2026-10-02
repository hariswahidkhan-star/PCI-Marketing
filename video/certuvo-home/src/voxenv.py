#!/usr/bin/env python3
"""
Emit the per-scene narration gain envelope as an ffmpeg `volume` expression.

Every take comes back from the TTS engine at its own normalised level, so the
narration arrives at one loudness for the whole film no matter how the read is
directed. Measured: the bed has a real 8.6 dB swell (LRA 11.0) but the voice is
LRA 2.8, and because the voice is the louder element the finished mix inherited
the voice's flatness — LRA 2.4, which is flatter than either input. Ducking is
not the cause; sweeping the sidechain ratio from 10 down to 2.5 moves LRA by
0.1. The only lever is the voice itself.

So the narration is ridden by scene, the way a mix engineer would, following the
arc narrative-design.md already documents: intimate at the open, authority
through the middle, peak under the price and the close. The steps land in the
0.55 s of silence between scenes, so no step is audible. Range is deliberately
small — 3.2 dB end to end — because the opening is the hook and dropping it
further risks losing it on a phone speaker under muted autoplay.

Measured effect: LRA 2.4 -> 3.6.
"""
import json, os, sys

DB = {'s1': -2.0, 's2': -1.5, 's3': 0.0, 's4': 0.3, 's5': 0.0, 's6': 0.2,
      's7': 0.0, 's8': -0.5, 's9': 0.8, 's10': 1.2, 's11': 0.5}

HERE = os.path.dirname(os.path.abspath(__file__))
shots = json.load(open(os.path.join(HERE, 'timeline.json')))['shots']

missing = [s[0] for s in shots if s[0] not in DB]
if missing:
    sys.exit('voxenv: no gain for scene(s) ' + ', '.join(missing) +
             ' — add them to DB, do not let them default silently')

expr = None
for sid, _name, _vs, ve in reversed(shots):
    lin = 10 ** (DB[sid] / 20.0)
    expr = f'{lin:.4f}' if expr is None else f'if(lt(t,{ve:.3f}),{lin:.4f},{expr})'
print(expr)
