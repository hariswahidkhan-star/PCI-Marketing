#!/usr/bin/env bash
# Rebuild the score and lay it back into the delivered masters.
#
#   ./remux-audio.sh
#
# The score is audio, so there is no reason to re-render the picture to hear a
# change to it. This regenerates score.wav, re-runs the same mix build.sh uses,
# and swaps the audio track on each master with `-c:v copy` — the picture is
# passed through untouched, bit for bit, so the delivered video stays the exact
# encode that was signed off.
#
# Run build.sh instead if the cut or the narration changed: that is new picture.
set -euo pipefail
cd "$(dirname "$0")"
BUILD=../build; DIST=../dist
NAME="pci-ai-intro-75s"

if [[ -z "${FFMPEG:-}" ]]; then
  if command -v ffmpeg >/dev/null; then FFMPEG=ffmpeg
  elif [[ -x node_modules/ffmpeg-static/ffmpeg ]]; then FFMPEG=node_modules/ffmpeg-static/ffmpeg
  else echo "no ffmpeg" >&2; exit 1; fi
fi
mkdir -p "$BUILD"

echo "==> score"
python3 music.py "$BUILD/score.wav"

echo "==> mix (score side-chained under the voice)"
# `level=disabled` matters more than the ceiling. alimiter auto-levels its output
# back to 0 dB by default, so `limit` sets where limiting starts and then the
# result is renormalised — which is why the driven score came back at -0.7 dBTP
# under the old limit=0.95, over the -1.0 dBTP EBU R128 and the social platforms
# expect, and why merely lowering the number made the mix *louder* rather than
# quieter. With auto-level off, 0.79 is a real ceiling at -2.1 dBFS, leaving room
# for the inter-sample peaks AAC reconstructs above it. Loudness is unaffected:
# loudnorm sets the integrated level and the limiter only catches transients.
"$FFMPEG" -hide_banner -loglevel error -y -i "$BUILD/score.wav" -i ../audio/vo-track.wav \
  -filter_complex "[0:a]volume=0.62[bed];\
[bed][1:a]sidechaincompress=threshold=0.045:ratio=7:attack=12:release=300[duck];\
[duck][1:a]amix=inputs=2:normalize=0:duration=longest,\
loudnorm=I=-16:TP=-1.5:LRA=11,alimiter=limit=0.79:level=disabled[mix]" \
  -map "[mix]" -ar 48000 -ac 2 -c:a pcm_s16le "$BUILD/mixed.wav"

echo "==> swap the audio track on each master (video stream copied, never re-encoded)"
for f in "$NAME-1920x1080-captions.mp4" "$NAME-1080x1920-captions.mp4" \
         "$NAME-1080x1080-captions.mp4" "$NAME-1920x1080-clean.mp4" \
         "$NAME-1920x1080-MASTER.mp4"; do
  [[ -f "$DIST/$f" ]] || { echo "    skip $f (not built)"; continue; }
  "$FFMPEG" -hide_banner -loglevel error -y -i "$DIST/$f" -i "$BUILD/mixed.wav" \
    -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest \
    -movflags +faststart "$BUILD/tmp-$f"
  mv "$BUILD/tmp-$f" "$DIST/$f"
  echo "    $f  $(du -h "$DIST/$f" | cut -f1)"
done

# The silent master has no audio track by design — nothing to swap.
cp "$BUILD/score.wav" "$DIST/$NAME-score.wav"
cp "$BUILD/mixed.wav" "$DIST/$NAME-mixed-soundtrack.wav"
echo "==> done"
