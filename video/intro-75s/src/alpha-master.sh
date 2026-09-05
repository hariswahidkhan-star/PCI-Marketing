#!/usr/bin/env bash
# Encode the transparent type layer as a delivery master.
#
# This is the professional handoff for the B-roll variant: drop it over any
# footage in any NLE and the typography, brand furniture, captions and the
# legibility scrim land in exactly the verified positions and timings.
#
#   ./alpha-master.sh [16x9|9x16|1x1]          VP9/WebM with alpha (default)
#   PRORES=1 ./alpha-master.sh 16x9             also write ProRes 4444
#
# ProRes 4444 is the NLE-native alpha format, but at 1920x1080 / 75 s it is
# roughly 3 GB per aspect — too large to commit or hand over casually — so it
# is opt-in. The VP9/WebM master carries the same alpha in a few megabytes and
# imports into every modern editor and browser.
set -euo pipefail
cd "$(dirname "$0")"
TAG="${1:-16x9}"; FPS=30; NAME="pci-ai-intro-75s"
PLATE="../build/p-${TAG}-cc"; DIST=../dist
if [[ -z "${FFMPEG:-}" ]]; then
  if command -v ffmpeg >/dev/null; then FFMPEG=ffmpeg
  elif [[ -x node_modules/ffmpeg-static/ffmpeg ]]; then FFMPEG=node_modules/ffmpeg-static/ffmpeg
  else echo "no ffmpeg" >&2; exit 1; fi
fi
[[ -d "$PLATE" ]] || { echo "missing $PLATE — run ./plates.sh" >&2; exit 1; }
mkdir -p "$DIST"

if [[ "${PRORES:-0}" == "1" ]]; then
  echo "==> ProRes 4444 with alpha (~3 GB — editorial master)"
  "$FFMPEG" -hide_banner -loglevel error -y -framerate $FPS -i "$PLATE/%05d.png" \
    -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le \
    "$DIST/$NAME-${TAG}-typelayer-alpha.mov"
fi

echo "==> VP9/WebM with alpha (delivery master)"
"$FFMPEG" -hide_banner -loglevel error -y -framerate $FPS -i "$PLATE/%05d.png" \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 28 -row-mt 1 -an \
  "$DIST/$NAME-${TAG}-typelayer-alpha.webm"

ls -la "$DIST/$NAME-${TAG}-typelayer-alpha."*
