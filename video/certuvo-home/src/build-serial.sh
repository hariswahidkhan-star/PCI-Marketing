#!/usr/bin/env bash
# Serial build: one render at a time. The parallel waves in build.sh saturate
# a 4-core box (five Chromium instances took load average past 90), so this
# renders each aspect on its own and joins the intro/outro afterwards.
set -euo pipefail
cd "$(dirname "$0")"
BUILD=../build; DIST=../dist; NAME="certuvo-home"; FPS=30
FFMPEG=node_modules/ffmpeg-static/ffmpeg
mkdir -p "$BUILD" "$DIST"

# ---- audio: conform, then mix the voice over the bed -------------------------
# MIX=0 reuses an existing $BUILD/mixed.wav (for resuming an interrupted render
# against the exact same audio).
if [[ "${MIX:-1}" == "1" ]]; then
  echo "==> conform timeline to the recorded voice"
  python3 sync.py >/dev/null
  python3 vo.py
  python3 presenter.py

  # This film has its own bed (../music-own/certuvo-home-bed.mp3), generated to
  # match its eleven beats: bare for the first twenty seconds under the intimate
  # open, building from ninety, peaking 110-130 under the price and the close,
  # resolving warm. Its dynamic range is ~18 dB against the shared CMA bed's ~7,
  # so it sits higher (BED) and needs a gentler dip than a dense produced track:
  # the prompt already keeps 1-4 kHz sparse for the narration.
  MUSIC="${MUSIC-../music-own/certuvo-home-bed.mp3}"
  TOTAL="$(python3 -c "import json;print(json.load(open('timeline.json'))['total'])")"
  # A bed shorter than the film does not fail: atrim just stops early and amix
  # pads the tail with silence, so the close plays dry and nothing says so.
  # Caught it once when the film grew from 2:17 to 2:42 — never again.
  # ffmpeg -i with no output file exits 1 by design, which pipefail would treat
  # as a build failure — hence the `|| true`.
  BEDLEN="$({ "$FFMPEG" -hide_banner -i "$MUSIC" 2>&1 || true; } | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' | head -1 \
            | awk -F: '{printf "%.2f", $1*3600+$2*60+$3}')"
  [[ -n "$BEDLEN" ]] || { echo "could not read the duration of $MUSIC" >&2; exit 1; }
  awk -v b="$BEDLEN" -v t="$TOTAL" 'BEGIN{exit !(b+0 >= t+0)}' || {
    echo "bed is ${BEDLEN}s but the film is ${TOTAL}s — the last $(awk -v b="$BEDLEN" -v t="$TOTAL" 'BEGIN{printf "%.1f", t-b}')s would be silent." >&2
    echo "regenerate ../music-own/certuvo-home-bed.mp3 at the new length (see ../music-own/README.md)" >&2
    exit 1; }
  FADE_AT="$(python3 -c "print(max(0.0, $TOTAL - 4.0))")"
  "$FFMPEG" -hide_banner -loglevel error -y -i "$MUSIC" \
    -af "atrim=0:$TOTAL,afade=t=in:st=0:d=2.0,afade=t=out:st=$FADE_AT:d=4" \
    -ar 48000 -ac 2 -c:a pcm_s16le "$BUILD/bed.wav"

  # the bed level, its EQ notch, the duck and the two-pass loudness pass all
  # live in mixdown.sh, so there is one mix and not three copies of it
  echo "==> mix (voice ridden by scene, bed side-chained under it)"
  ./mixdown.sh
fi
[[ -s "$BUILD/mixed.wav" ]] || { echo "no $BUILD/mixed.wav" >&2; exit 1; }
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
