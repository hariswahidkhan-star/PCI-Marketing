#!/usr/bin/env bash
# Rebuild the audio mix and swap it into the already-rendered masters.
#
# The picture is a pure function of t and does not depend on the audio at all,
# so an audio change never needs a re-render: -c:v copy lifts the existing video
# stream across untouched. This exists because the narration ride (voxenv.py)
# was added after a 50-minute serial render had already started.
#
# Run after build-serial.sh has finished all four renders, and before finish.sh
# joins the stings — join.sh reads its audio from these masters.
set -euo pipefail
cd "$(dirname "$0")"
BUILD=../build; DIST=../dist; NAME=certuvo-home
FFMPEG=node_modules/ffmpeg-static/ffmpeg

[[ -s "$BUILD/bed.wav" ]] || { echo "no $BUILD/bed.wav — run build-serial.sh first" >&2; exit 1; }

echo "==> remix (voice ridden by scene)"
./mixdown.sh

# ffmpeg refuses to write its own input, so each master is rebuilt beside itself
# and moved into place only after ffmpeg has exited cleanly. A partial file that
# has replaced a good master is worse than no change at all.
for f in "$DIST/$NAME"-1920x1080-captions.mp4 "$DIST/$NAME"-1920x1080-clean.mp4 \
         "$DIST/$NAME"-1080x1920-captions.mp4 "$DIST/$NAME"-1080x1080-captions.mp4; do
  [[ -s "$f" ]] || { echo "skip (missing) $(basename "$f")"; continue; }
  echo "==> $(basename "$f")"
  "$FFMPEG" -hide_banner -loglevel error -y -i "$f" -i "$BUILD/mixed.wav" \
    -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 \
    -movflags +faststart -shortest "$f.tmp.mp4"
  mv "$f.tmp.mp4" "$f"
done

echo "==> remixed"
{ "$FFMPEG" -hide_banner -i "$BUILD/mixed.wav" -af ebur128=framelog=quiet -f null - 2>&1 || true; } \
  | grep -E "I: |LRA: " | head -2
