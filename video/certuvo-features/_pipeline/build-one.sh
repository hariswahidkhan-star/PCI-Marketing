#!/usr/bin/env bash
# Build one feature film at 1080p 16:9 for the selection round.
#
#   ../_pipeline/build-one.sh <variant> <name>
#
# Narrated variants (v1-v3) mix the recorded voice over the shared bed with a
# side-chain; the music-only variants (v4, v5) take the bed alone at full level
# because there is no voice to duck it under. Which one you get is decided by
# whether ../audio/vo-track.wav exists, not by a flag, so it cannot be set wrong.
#
# Only 16:9 is built here. The other aspects are for whichever treatment is
# chosen — rendering twenty files nobody will watch is not thrift, it is waste.
set -euo pipefail
cd "$(dirname "$0")/../$1/src"
NAME="$2"; FPS=30
BUILD=../build; DIST=../dist; BED=../../music/feature-bed.mp3
FFMPEG="$PWD/node_modules/ffmpeg-static/ffmpeg"
mkdir -p "$BUILD" "$DIST"

TOTAL="$(node -e "const fs=require('fs');const m=fs.readFileSync('shots.data.js','utf8').match(/__DURATION\s*=\s*([0-9.]+)/);process.stdout.write(m[1])")"
FADE_AT="$(awk -v t="$TOTAL" 'BEGIN{printf "%.2f", (t-3.0 > 0 ? t-3.0 : 0)}')"

BEDLEN="$({ "$FFMPEG" -hide_banner -i "$BED" 2>&1 || true; } | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' | head -1 \
          | awk -F: '{printf "%.2f", $1*3600+$2*60+$3}')"
awk -v b="$BEDLEN" -v t="$TOTAL" 'BEGIN{exit !(b+0 >= t+0)}' || {
  echo "bed is ${BEDLEN}s but $1 is ${TOTAL}s — the tail would be silent" >&2; exit 1; }

echo "==> $1 · ${TOTAL}s · bed ${BEDLEN}s"
"$FFMPEG" -hide_banner -loglevel error -y -i "$BED" \
  -af "atrim=0:$TOTAL,afade=t=in:st=0:d=1.2,afade=t=out:st=$FADE_AT:d=3" \
  -ar 48000 -ac 2 -c:a pcm_s16le "$BUILD/bed.wav"

if [[ -s ../audio/vo-track.wav ]]; then
  echo "==> mix: voice over bed"
  "$FFMPEG" -hide_banner -loglevel error -y -i "$BUILD/bed.wav" -i ../audio/vo-track.wav \
    -filter_complex "[0:a]equalizer=f=1800:t=q:w=0.9:g=-3,volume=0.40[bed];\
[bed][1:a]sidechaincompress=threshold=0.035:ratio=10:attack=8:release=400[duck];\
[duck][1:a]amix=inputs=2:normalize=0:duration=first,\
loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.85:level=disabled[mix]" \
    -map "[mix]" -ar 48000 -ac 2 -c:a pcm_s16le "$BUILD/mixed.wav"
else
  echo "==> music only: no voice to duck under, so the bed runs at full level"
  "$FFMPEG" -hide_banner -loglevel error -y -i "$BUILD/bed.wav" \
    -af "loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.85:level=disabled" \
    -ar 48000 -ac 2 -c:a pcm_s16le "$BUILD/mixed.wav"
fi

echo "==> render 1920x1080"
node render.mjs --w 1920 --h 1080 --fps "$FPS" --cc 1 --pipe 1 2>"$BUILD/render.log" \
  | "$FFMPEG" -hide_banner -loglevel error -y -f image2pipe -c:v png -framerate "$FPS" -i - \
      -i "$BUILD/mixed.wav" -map 0:v -map 1:a \
      -c:v libx264 -preset medium -profile:v high -level 4.1 -crf 19 -pix_fmt yuv420p -movflags +faststart \
      -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest "$DIST/$NAME-1920x1080.mp4" 2>>"$BUILD/render.log"

E=$({ "$FFMPEG" -hide_banner -v error -i "$DIST/$NAME-1920x1080.mp4" -f null - 2>&1 || true; } | wc -l)
D=$({ "$FFMPEG" -hide_banner -i "$DIST/$NAME-1920x1080.mp4" 2>&1 || true; } | { grep -o 'Duration: [0-9:.]*' || true; } | head -1)
printf '==> %s  %s · %s · errors=%s\n' "$NAME" "$D" "$(du -h "$DIST/$NAME-1920x1080.mp4" | cut -f1)" "$E"
