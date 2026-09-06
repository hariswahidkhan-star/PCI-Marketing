#!/usr/bin/env python3
"""
Conform the explainer's timeline to the recorded narration.

The read was generated one scene at a time, so sentences inside a scene flow
naturally instead of being stitched from separately-synthesised fragments. That
buys prosody but costs sub-timings, so this recovers them: each scene's audio is
de-silenced at the ends, then split at its own internal pauses to find the
caption boundaries. Where silence detection does not find the expected number of
breaks, it falls back to splitting by word weight and says so.

Unlike the 75-second film there is no fixed duration to hit, so nothing is
time-scaled. The picture is cut to the voice at its natural pace.

Emits ../audio/vo-track.wav and timeline.json (scene bounds + caption times).
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.normpath(os.path.join(HERE, '..', 'audio'))
TRIM = os.path.join(AUD, 'trimmed')
FFMPEG = os.environ.get('FFMPEG') or os.path.join(HERE, 'node_modules', 'ffmpeg-static', 'ffmpeg')

LEAD, TAIL = 0.30, 0.85
GAP_SCENE = 0.36        # the beat between scenes; also where the picture cuts

# The brief specifies a 105-120s master. The read is measured first and the
# picture follows it, so the only lever left is a uniform time-scale — applied
# with librubberband, which preserves formants where plain atempo thins the
# voice. MAX_STRETCH is a refusal, not a clamp: this narrator is directed to be
# deep and deliberate, and past about 8% the read stops sounding that way, so
# the build stops and asks for a copy trim rather than quietly shipping a
# rushed one. Getting here already cost one round of exactly that trim.
TARGET = 120.00
MAX_STRETCH = 1.08
SILENCE_DB = '-38dB'
MIN_SIL = 0.26          # a pause shorter than this is phrasing, not a boundary
SR = 48000

sys.path.insert(0, HERE)
import vo as VO


def run(args):
    return subprocess.run(args, capture_output=True, text=True).stderr


def dur(path):
    for line in run([FFMPEG, '-hide_banner', '-i', path]).splitlines():
        if 'Duration:' in line:
            h, m, s = line.split('Duration:')[1].split(',')[0].strip().split(':')
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise SystemExit(f'no duration for {path}')


def trim_all():
    os.makedirs(TRIM, exist_ok=True)
    de = ('silenceremove=start_periods=1:start_silence=0.02:start_threshold=-50dB:detection=peak,'
          'areverse,'
          'silenceremove=start_periods=1:start_silence=0.02:start_threshold=-50dB:detection=peak,'
          'areverse')
    for i in range(1, len(VO.SCENES) + 1):
        src = os.path.join(AUD, f'vo-{i:02d}.mp3')
        dst = os.path.join(TRIM, f'vo-{i:02d}.wav')
        subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-i', src,
                        '-af', de, '-ar', str(SR), '-ac', '1', dst], check=True)


def internal_breaks(path):
    """Midpoints of internal silences — candidate segment boundaries."""
    out = run([FFMPEG, '-hide_banner', '-i', path, '-af',
               f'silencedetect=noise={SILENCE_DB}:d={MIN_SIL}', '-f', 'null', '-'])
    starts = [float(m) for m in re.findall(r'silence_start: ([\d.]+)', out)]
    ends = [float(m) for m in re.findall(r'silence_end: ([\d.]+)', out)]
    return [round((s + e) / 2, 3) for s, e in zip(starts, ends)]


def main():
    print('==> trimming')
    trim_all()

    caps, scenes, t = [], [], LEAD
    fallbacks = []
    for idx, (sid, chap, segs) in enumerate(VO.SCENES):
        p = os.path.join(TRIM, f'vo-{idx+1:02d}.wav')
        d = dur(p)
        need = len(segs) - 1
        if need:
            br = internal_breaks(p)
            if len(br) > need:
                # keep the longest silences when the reader breathed more than expected
                sil = sorted(br)
                # choose breaks closest to the proportional split points
                w = [VO.weight(s) for _, s in segs]
                tot = sum(w)
                targets, acc = [], 0.0
                for k in range(need):
                    acc += w[k]
                    targets.append(d * acc / tot)
                br = [min(sil, key=lambda x: abs(x - tgt)) for tgt in targets]
                br = sorted(set(br))
            if len(br) != need:
                w = [VO.weight(s) for _, s in segs]
                tot = sum(w)
                br, acc = [], 0.0
                for k in range(need):
                    acc += w[k]
                    br.append(round(d * acc / tot, 3))
                fallbacks.append(sid)
        else:
            br = []

        edges = [0.0] + br + [d]
        for k, (cap, spoken) in enumerate(segs):
            caps.append([round(t + edges[k], 2), round(t + edges[k + 1], 2), VO.wrap(cap)])
        scenes.append([sid, chap, round(t, 3), round(t + d, 3)])
        t += d
        if idx < len(VO.SCENES) - 1:
            t += GAP_SCENE

    natural = t + TAIL

    # Conform to the brief's window. A factor at or below 1.0 means the read
    # already fits and nothing is touched — the film is simply as long as the
    # narration wants to be, which is always the better outcome.
    f = natural / TARGET
    if f > MAX_STRETCH:
        raise SystemExit(
            f'read is {natural:.2f}s against a {TARGET:.2f}s target — that needs '
            f'{f:.3f}x, past the {MAX_STRETCH}x ceiling. Trim the copy in vo.py '
            f'rather than speeding up the narrator.')
    if f > 1.0:
        print(f'==> conform {natural:.2f}s -> {TARGET:.2f}s  ({f:.4f}x, formant-preserved)')
        scale = 1.0 / f
        for c in caps:
            c[0] = round(c[0] * scale, 2); c[1] = round(c[1] * scale, 2)
        for sc in scenes:
            sc[2] = round(sc[2] * scale, 3); sc[3] = round(sc[3] * scale, 3)
        total = round(TARGET, 2)
    else:
        f = 1.0
        total = round(natural, 2)

    # scene cut points sit in the middle of the inter-scene gap
    cuts = [0.0]
    for i in range(len(scenes) - 1):
        cuts.append(round((scenes[i][3] + scenes[i + 1][2]) / 2, 3))
    cuts.append(total)
    shots = [[scenes[i][0], scenes[i][1], cuts[i], cuts[i + 1]] for i in range(len(scenes))]

    print('==> voice track')
    parts, filt = [], []
    for i in range(1, len(VO.SCENES) + 1):
        parts += ['-i', os.path.join(TRIM, f'vo-{i:02d}.wav')]
    for i, (sid, chap, a, b) in enumerate(scenes):
        delay = int(round(a * 1000))
        filt.append(f'[{i}:a]adelay={delay}|{delay},apad[a{i}]')
    mix = ''.join(f'[a{i}]' for i in range(len(scenes)))
    tail = (f'rubberband=tempo={f:.5f}:pitch=1:formant=preserved,' if f > 1.0 else '')
    filt.append(f'{mix}amix=inputs={len(scenes)}:normalize=0:duration=longest,'
                f'{tail}atrim=0:{total:.3f},asetpts=N/SR/TB,'
                f'loudnorm=I=-18:TP=-1.5:LRA=11[out]')
    subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y'] + parts +
                   ['-filter_complex', ';'.join(filt), '-map', '[out]',
                    '-ar', str(SR), '-ac', '1', '-c:a', 'pcm_s16le',
                    os.path.join(AUD, 'vo-track.wav')], check=True)

    # the picture reads its cut list from the same measurement, so scene.html
    # never carries hand-copied timings
    with open(os.path.join(HERE, 'shots.data.js'), 'w') as f:
        f.write('/* GENERATED by sync.py — do not edit. */\n')
        f.write('window.__DURATION = %.3f;\n' % total)
        f.write('window.__SHOTS = ' + json.dumps(shots) + ';\n')

    json.dump({'total': total,
               'segments': {str(i + 1): c[:2] for i, c in enumerate(caps)},
               'captions': caps, 'shots': shots},
              open(os.path.join(HERE, 'timeline.json'), 'w'), indent=2)

    print(f'film length {total:.2f}s ({total/60:.2f} min) · {len(caps)} captions · {len(shots)} scenes')
    if fallbacks:
        print(f'  note: proportional split used (silence detection inconclusive) for: {", ".join(fallbacks)}')
    for sid, chap, a, b in shots:
        print(f'  {sid:4} {chap:20} {a:7.2f} -> {b:7.2f}  ({b-a:5.2f}s)')


if __name__ == '__main__':
    main()
