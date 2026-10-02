#!/usr/bin/env bash
# Render every film, one at a time.
#
# Serial on purpose: concurrent Chromium renders took a 4-core box past load
# average 90 on an earlier project. One render at a time is slower on paper
# and faster in practice.
#
# The films ship SILENT. They are built to work silent — the reels are
# text-led and the 4:5 cuts carry burned captions — and no paid voice or
# music has been authorised. A silent AAC track is muxed in anyway, because
# some platforms mishandle a file with no audio stream at all, and an
# uploader hitting that at 2am is a worse failure than a few KB of silence.
set -euo pipefail
cd "$(dirname "$0")/.."
PIPE=_pipeline; DIST=dist; FPS=30
FFMPEG=$PIPE/node_modules/ffmpeg-static/ffmpeg
mkdir -p "$DIST"

V=(-c:v libx264 -preset medium -pix_fmt yuv420p -movflags +faststart -crf 19)
A=(-c:a aac -b:a 128k -ar 48000 -ac 2)

one(){ # dir w h label
  local d=$1 w=$2 h=$3 label=$4
  local out="$DIST/pciai-$d-$label.mp4"
  echo "==> $d  ${w}x${h}"
  ( cd "$d" && node ../$PIPE/render.mjs --w "$w" --h "$h" --fps "$FPS" --cc 1 --pipe 1 2>"../build/$d-$label.log" ) \
    | "$FFMPEG" -hide_banner -loglevel error -y \
        -f image2pipe -c:v png -framerate "$FPS" -i - \
        -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
        -map 0:v -map 1:a "${V[@]}" "${A[@]}" -shortest "$out" 2>>"build/$d-$label.log"
  ls -lh "$out" | awk '{print "    "$9"  "$5}'
}

for d in r1 r2 r3 r4 r5; do one "$d" 1080 1920 "1080x1920"; done
for d in v1 v2 v3 v4 v5; do
  one "$d" 1080 1350 "1080x1350"
  one "$d" 1920 1080 "1920x1080"
done
echo "ALL-RENDERS-DONE"
