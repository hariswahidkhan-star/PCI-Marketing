#!/usr/bin/env bash
# Composite the PCI AI introduction film from source.
#
#   ./build.sh
#
# Rebuilds the brand overlay and re-composites the master. Outputs to ../dist.
#
# NOTE ON REPRODUCIBILITY. The overlay is fully reproducible — overlay.html is
# deterministic in t, so frame N is byte-identical on every run. The FOOTAGE is
# not: the six plates in ../build/shot-*.mp4 were generated once through the
# ElevenLabs Creative connector (ltx-v2-fast) and cannot be regenerated
# identically. Keep them. If they are lost, see ../README.md for the six prompts;
# a regeneration will differ, and the shot windows would need re-checking.
set -euo pipefail
cd "$(dirname "$0")"

BUILD=../build
DIST=../dist
FPS=25
mkdir -p "$BUILD" "$DIST"

command -v ffmpeg >/dev/null || { echo "ffmpeg not on PATH"; exit 1; }
[[ -d node_modules/playwright ]] || npm install --no-audit --no-fund playwright

for n in 01 02 03 04 05 06; do
  [[ -f "$BUILD/shot-$n.mp4" ]] || { echo "missing $BUILD/shot-$n.mp4 — see note above"; exit 1; }
done

echo "==> picture (trim each plate to exactly 10.000s, then concat)"
for n in 01 02 03 04 05 06; do
  ffmpeg -hide_banner -loglevel error -y -i "$BUILD/shot-$n.mp4" -t 10.0 \
    -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -profile:v high -level 4.1 \
    -r "$FPS" -an "$BUILD/trim-$n.mp4"
done
printf "file 'trim-%s.mp4'\n" 01 02 03 04 05 06 > "$BUILD/concat.txt"
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i "$BUILD/concat.txt" \
  -c copy "$BUILD/picture.mp4"

echo "==> brand overlay (1500 transparent frames)"
node render-overlay.mjs --w 1920 --h 1080 --fps "$FPS" --out "$BUILD/overlay"

echo "==> composite + loudness"
# loudnorm to -16 LUFS: the raw TTS bed sits around -28 dB mean, which reads as
# "no voice" on laptop and phone speakers.
ffmpeg -hide_banner -loglevel error -y \
  -i "$BUILD/picture.mp4" \
  -framerate "$FPS" -i "$BUILD/overlay/%05d.png" \
  -i ../vo/pci-intro-60s-vo-bed.wav \
  -filter_complex "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]; \
                   [2:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset slow -crf 20 -profile:v high -level 4.1 \
  -maxrate 6M -bufsize 12M -movflags +faststart \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest \
  "$DIST/pci-intro-60s-1920x1080.mp4"

echo "==> poster"
ffmpeg -hide_banner -loglevel error -y -ss 45 -i "$DIST/pci-intro-60s-1920x1080.mp4" \
  -frames:v 1 "$DIST/pci-intro-60s-poster.png"

echo "done -> $DIST"
