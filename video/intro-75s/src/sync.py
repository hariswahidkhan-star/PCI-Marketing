#!/usr/bin/env python3
"""
Conform the film's timeline to the ACTUAL voiceover.

The film was cut to a 153 wpm design pace. The synthesised read came back at
roughly 130 wpm -- 82.4 s of speech for a 75 s film -- so picture and voice have
to be reconciled. Rather than stretching the picture or rushing the read, every
segment is time-scaled by one uniform factor back to the pace the film was
designed for, using librubberband (formant-preserving), and the whole timeline
is then recomputed from the resulting durations.

That factor is derived, not guessed: it is exactly what makes the film land on
TARGET seconds. If it ever exceeds MAX_STRETCH the script refuses rather than
shipping a rushed read -- extend TARGET instead.

Emits:
    ../audio/vo-track.wav        the full-length voice track, silent where the film is
    timeline.json                segment placements + scene bounds, for vo.py/scene.html/music.py
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.normpath(os.path.join(HERE, '..', 'audio'))
TRIM = os.path.join(AUD, 'trimmed')

TARGET = 75.00
MAX_STRETCH = 1.25
LEAD, TAIL = 0.25, 0.60
GAP_IN, GAP_SCENE = 0.18, 0.40
SR = 48000

# which segments belong to which scene (1-indexed segment numbers)
SCENES = [('s1', [1, 2]), ('s2', [3, 4]), ('s3', [5, 6]), ('s4', [7, 8]),
          ('s5', [9, 10]), ('s6', [11, 12]), ('s7', [13, 14]), ('s8', [15])]

FFMPEG = os.environ.get('FFMPEG') or os.path.join(HERE, 'node_modules', 'ffmpeg-static', 'ffmpeg')


def dur(path):
    out = subprocess.run([FFMPEG, '-hide_banner', '-i', path],
                         capture_output=True, text=True).stderr
    for line in out.splitlines():
        if 'Duration:' in line:
            h, m, s = line.split('Duration:')[1].split(',')[0].strip().split(':')
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise SystemExit(f'no duration for {path}')


def main():
    d = {i: dur(os.path.join(TRIM, f'vo-{i:02d}.wav')) for i in range(1, 16)}
    speech = sum(d.values())

    n_in = sum(len(s) - 1 for _, s in SCENES)
    n_sc = len(SCENES) - 1
    fixed = LEAD + TAIL + GAP_IN * n_in + GAP_SCENE * n_sc
    budget = TARGET - fixed
    f = speech / budget

    print(f'speech {speech:.2f}s + fixed {fixed:.2f}s = {speech+fixed:.2f}s natural')
    print(f'target {TARGET:.2f}s -> uniform stretch factor {f:.4f}')
    if f > MAX_STRETCH:
        raise SystemExit(f'refusing: {f:.3f}x exceeds MAX_STRETCH {MAX_STRETCH}. '
                         f'Raise TARGET to about {speech/MAX_STRETCH + fixed:.0f}s instead.')
    if f < 1.0:
        print('note: read is shorter than the target; padding with silence rather than slowing it')
        f = 1.0

    # place every segment, then derive scene bounds from the placements
    placed, t = {}, LEAD
    bounds = []
    for si, (sid, segs) in enumerate(SCENES):
        start = t
        for k, i in enumerate(segs):
            nd = d[i] / f
            placed[i] = (round(t, 3), round(t + nd, 3), round(nd, 3))
            t += nd
            if k < len(segs) - 1:
                t += GAP_IN
        end = t
        # the cut sits in the middle of the gap between scenes
        bounds.append([sid, start, end])
        if si < len(SCENES) - 1:
            t += GAP_SCENE

    total = t + TAIL
    # scene in/out points: butt-joined at the midpoint of each inter-scene gap
    cuts = [0.0]
    for i in range(len(bounds) - 1):
        cuts.append(round((bounds[i][2] + bounds[i + 1][1]) / 2, 3))
    cuts.append(round(total, 3))
    scenes = [[bounds[i][0], cuts[i], cuts[i + 1]] for i in range(len(bounds))]

    print(f'film length {total:.2f}s (target {TARGET:.2f})')

    # ---- build the voice track ----
    parts, filt = [], []
    for i in range(1, 16):
        parts += ['-i', os.path.join(TRIM, f'vo-{i:02d}.wav')]
    for i in range(1, 16):
        a, _, _ = placed[i]
        delay = int(round(a * 1000))
        # rubberband preserves formants; atempo would thin the voice at this ratio
        chain = f'[{i-1}:a]'
        if abs(f - 1.0) > 0.001:
            chain += f'rubberband=tempo={f:.5f}:pitch=1:formant=preserved,'
        chain += f'adelay={delay}|{delay},apad[a{i}]'
        filt.append(chain)
    mix = ''.join(f'[a{i}]' for i in range(1, 16))
    filt.append(f'{mix}amix=inputs=15:normalize=0:duration=longest,'
                f'atrim=0:{total:.3f},asetpts=N/SR/TB,'
                f'loudnorm=I=-18:TP=-1.5:LRA=11[out]')
    out = os.path.join(AUD, 'vo-track.wav')
    cmd = [FFMPEG, '-hide_banner', '-loglevel', 'error', '-y'] + parts + \
          ['-filter_complex', ';'.join(filt), '-map', '[out]',
           '-ar', str(SR), '-ac', '1', '-c:a', 'pcm_s16le', out]
    subprocess.run(cmd, check=True)
    print(f'voice track -> {out}  {dur(out):.2f}s')

    json.dump({'target': TARGET, 'total': round(total, 3), 'stretch': round(f, 5),
               'segments': {str(k): v for k, v in placed.items()},
               'scenes': scenes},
              open(os.path.join(HERE, 'timeline.json'), 'w'), indent=2)
    print('timeline.json written')
    for sid, a, b in scenes:
        print(f'  {sid}  {a:6.2f} -> {b:6.2f}  ({b-a:5.2f}s)')


if __name__ == '__main__':
    main()
