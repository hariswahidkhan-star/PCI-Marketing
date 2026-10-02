#!/usr/bin/env bash
# Serial build: one render at a time. The parallel waves in build.sh saturate
# a 4-core box (five Chromium instances took load average past 90), so this
# renders each aspect on its own and joins the intro/outro afterwards.
set -euo pipefail
cd "$(dirname "$0")"
BUILD=../build; DIST=../dist; NAME="certuvo-cma-60"; FPS=30
FFMPEG=node_modules/ffmpeg-static/ffmpeg
mkdir -p "$BUILD" "$DIST"
[[ -s "$BUILD/mixed.wav" ]] || { echo "no $BUILD/mixed.wav — run build.sh up to the mix first" >&2; exit 1; }
V=(-c:v libx264 -preset medium -pix_fmt yuv420p -movflags +faststart)
A=(-c:a aac -b:a 192k -ar 48000 -ac 2)

one(){ # w h cc log -- ffmpeg output args
  local w=$1 h=$2 cc=$3 log=$4; shift 5
  echo "==> ${w}x${h} cc=$cc"
  node render.mjs --w "$w" --h "$h" --fps "$FPS" --cc "$cc" --pipe 1 2>"$BUILD/$log.log" \
    | "$FFMPEG" -hide_banner -loglevel error -y -f image2pipe -c:v png -framerate "$FPS" -i - \
        -i "$BUILD/mixed.wav" "$@" 2>>"$BUILD/$log.log"
}

one 1920 1080 1 s-16x9 -- -map 0:v -map 1:a "${V[@]}" -crf 19 "${A[@]}" -shortest "$DIST/$NAME-1920x1080-captions.mp4"
one 1920 1080 0 s-16x9-clean -- -map 0:v -map 1:a "${V[@]}" -crf 19 "${A[@]}" -shortest "$DIST/$NAME-1920x1080-clean.mp4"
one 1080 1920 1 s-9x16 -- -map 0:v -map 1:a "${V[@]}" -crf 19 "${A[@]}" -shortest "$DIST/$NAME-1080x1920-captions.mp4"
one 1080 1080 1 s-1x1 -- -map 0:v -map 1:a "${V[@]}" -crf 19 "${A[@]}" -shortest "$DIST/$NAME-1080x1080-captions.mp4"
echo "==> renders done"; ls -la "$DIST"
