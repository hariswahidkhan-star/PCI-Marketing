#!/usr/bin/env bash
# Everything after the four renders: verify, join the stings, verify the joins,
# and pull the poster and thumbnail stills. Safe to re-run.
set -euo pipefail
cd "$(dirname "$0")"
DIST=../dist; NAME=certuvo-home
FFMPEG="$PWD/node_modules/ffmpeg-static/ffmpeg"

verify(){ # one file -> "name: Duration · size · errors=N"
  # `ffmpeg -i` with no output file exits 1 by design, and grep exits 1 when it
  # matches nothing. Under `set -euo pipefail` either one kills the script mid
  # audit — which is exactly what happened the first time this ran, silently,
  # after a 50-minute render. Both are contained here.
  local f="$1" e d s
  e=$({ "$FFMPEG" -hide_banner -v error -i "$f" -f null - 2>&1 || true; } | wc -l)
  d=$({ "$FFMPEG" -hide_banner -i "$f" 2>&1 || true; } | { grep -o 'Duration: [0-9:.]*' || true; } | head -1)
  s=$(du -h "$f" | cut -f1)
  printf '%-52s %s · %s · errors=%s\n' "$(basename "$f")" "${d:-?}" "$s" "$e"
}

echo "=== verify renders ==="
for f in "$DIST/$NAME"-1*.mp4; do [[ -s "$f" ]] && verify "$f"; done

echo
echo "=== join intro + film + outro ==="
./join.sh

echo
echo "=== verify joins ==="
for f in "$DIST/$NAME"-FULL-*.mp4; do [[ -s "$f" ]] && verify "$f"; done

echo
echo "=== poster and thumbnails (from the clean cut) ==="
CLEAN="$DIST/$NAME-1920x1080-clean.mp4"
if [[ -s "$CLEAN" ]]; then
  # 3s: the presenter mid-line. 40s: the credential wall complete.
  # 104s: the Coach exchange complete, with the candidate's option lit — 92s
  # used to be used here and lands 1.2s into the scene, before the panel has
  # assembled. 116s: the peer screen-share with both cursors on the question.
  # 130s: the readiness curve. All chosen against the conformed timeline, so
  # they move if the read is re-recorded.
  for t in 3 40 104 116 130; do
    "$FFMPEG" -hide_banner -loglevel error -y -ss "$t" -i "$CLEAN" -frames:v 1 -q:v 2 \
      "$DIST/$NAME-still-${t}s.jpg"
  done
  cp "$DIST/$NAME-still-40s.jpg" "$DIST/$NAME-poster.jpg"
  ls -la "$DIST"/*.jpg
else
  echo "no clean cut yet — skipping stills"
fi
echo
echo "FINISH-DONE"
