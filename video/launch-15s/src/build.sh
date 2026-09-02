#!/usr/bin/env bash
# Build the PCI post-launch film from source.
#
#   ./build.sh              full build (all masters)
#   ./build.sh --fast       half frame rate, for checking an edit quickly
#
# Outputs land in ../dist. Everything here is reproducible from the repo — the
# only thing the pipeline cannot make for you is the human voiceover (see
# ../script.md and the "Laying in the voiceover" section of ../README.md).
set -euo pipefail

cd "$(dirname "$0")"
BUILD="../build"
DIST="../dist"
FPS=30
[[ "${1:-}" == "--fast" ]] && FPS=15

mkdir -p "$BUILD" "$DIST"

command -v ffmpeg >/dev/null || { echo "ffmpeg not on PATH"; exit 1; }
[[ -d node_modules/playwright ]] || npm install --no-audit --no-fund playwright

echo "==> score"
python3 music.py "$BUILD/score.wav"

echo "==> frames"
node render.mjs --w 1920 --h 1080 --fps "$FPS" --cc 1 --out "$BUILD/f-16x9-cc"
node render.mjs --w 1920 --h 1080 --fps "$FPS" --cc 0 --out "$BUILD/f-16x9-clean"
node render.mjs --w 1080 --h 1080 --fps "$FPS" --cc 1 --out "$BUILD/f-1x1-cc"

# $1 frame dir, $2 output name
encode () {
  echo "==> encode $2"
  ffmpeg -hide_banner -loglevel error -y \
    -framerate "$FPS" -i "$1/%05d.png" \
    -i "$BUILD/score.wav" \
    -map 0:v -map 1:a \
    -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p \
    -profile:v high -level 4.1 -movflags +faststart \
    -c:a aac -b:a 192k -ar 48000 -ac 2 \
    -shortest "$DIST/$2"
}

encode "$BUILD/f-16x9-cc"    "pci-launch-15s-1920x1080-captions.mp4"
encode "$BUILD/f-16x9-clean" "pci-launch-15s-1920x1080-clean.mp4"
encode "$BUILD/f-1x1-cc"     "pci-launch-15s-1080x1080-captions.mp4"

echo "==> poster"
cp "$BUILD/f-16x9-cc/00420.png" "$DIST/pci-launch-15s-poster.png"

echo "==> silent master (for a studio to lay VO + their own music against)"
ffmpeg -hide_banner -loglevel error -y \
  -framerate "$FPS" -i "$BUILD/f-16x9-clean/%05d.png" \
  -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p \
  -profile:v high -level 4.1 -movflags +faststart \
  "$DIST/pci-launch-15s-1920x1080-silent.mp4"

cp ../captions/*.srt ../captions/*.vtt "$DIST/" 2>/dev/null || true
cp "$BUILD/score.wav" "$DIST/pci-launch-15s-score.wav"

echo
ls -la "$DIST"
