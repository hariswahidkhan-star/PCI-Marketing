#!/usr/bin/env bash
# Everything left after build-serial.sh died partway: the two 16:9 masters are
# rendered and verified, the 9:16 and 1:1 are not.
#
# build-serial.sh was killed by an edit made to it while bash was still
# executing it. Bash reads a script incrementally from disk rather than loading
# it whole, so editing a running script shifts the byte offsets under the live
# process and it resumes mid-token. Hence this file: one script, written once,
# run to completion, never touched while it runs.
#
# Order matters. The mix is rebuilt first so the two remaining renders mux the
# corrected audio directly and only the two finished masters need a remux.
set -euo pipefail
cd "$(dirname "$0")"
BUILD=../build; DIST=../dist; NAME=certuvo-home; FPS=30
FFMPEG=node_modules/ffmpeg-static/ffmpeg

echo "==> 1/4  rebuild the mix with the narration ride"
./mixdown.sh

echo "==> 2/4  swap the new audio into the two finished 16:9 masters (-c:v copy)"
for f in "$DIST/$NAME"-1920x1080-captions.mp4 "$DIST/$NAME"-1920x1080-clean.mp4; do
  [[ -s "$f" ]] || { echo "MISSING $f" >&2; exit 1; }
  echo "    $(basename "$f")"
  "$FFMPEG" -hide_banner -loglevel error -y -i "$f" -i "$BUILD/mixed.wav" \
    -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 \
    -movflags +faststart -shortest "$f.tmp.mp4"
  mv "$f.tmp.mp4" "$f"
done

echo "==> 3/4  render the two aspects the dead build never reached"
# The stale v2 files are removed first so a crash here cannot leave an old cut
# sitting in dist/ looking current.
rm -f "$DIST/$NAME-1080x1920-captions.mp4" "$DIST/$NAME-1080x1080-captions.mp4"
V=(-c:v libx264 -preset medium -pix_fmt yuv420p -movflags +faststart)
A=(-c:a aac -b:a 192k -ar 48000 -ac 2)
one(){
  local w=$1 h=$2 cc=$3 log=$4 out=$5
  echo "    ${w}x${h} cc=$cc"
  node render.mjs --w "$w" --h "$h" --fps "$FPS" --cc "$cc" --pipe 1 2>"$BUILD/$log.log" \
    | "$FFMPEG" -hide_banner -loglevel error -y -f image2pipe -c:v png -framerate "$FPS" -i - \
        -i "$BUILD/mixed.wav" -map 0:v -map 1:a "${V[@]}" -crf 19 "${A[@]}" -shortest "$out" 2>>"$BUILD/$log.log"
}
one 1080 1920 1 s-9x16 "$DIST/$NAME-1080x1920-captions.mp4"
one 1080 1080 1 s-1x1  "$DIST/$NAME-1080x1080-captions.mp4"

echo "==> 4/4  verify, join the stings, verify the joins, pull the stills"
# The joined FULL files are stale too; join.sh overwrites them, but removing
# them first means a failure leaves nothing misleading behind.
rm -f "$DIST/$NAME"-FULL-*.mp4
./finish.sh

echo "COMPLETE-V3-DONE"
