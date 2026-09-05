#!/usr/bin/env bash
# Build the PCI AI 75-second institutional film from source.
#
#   ./build.sh              full build, 30 fps, all masters
#   ./build.sh --fast       15 fps, for checking an edit quickly
#
# Outputs land in ../dist. Everything here is reproducible from this repository.
# The one thing the pipeline cannot make for itself is the voiceover: see
# ../captions/vo-script.md and "Laying the voiceover in" in ../README.md.
set -euo pipefail
cd "$(dirname "$0")"

BUILD="../build"; DIST="../dist"
FPS=30; [[ "${1:-}" == "--fast" ]] && FPS=15
JOBS="${JOBS:-4}"
NAME="pci-ai-intro-75s"

# ffmpeg-static is used when a system ffmpeg is absent; the Playwright bundle
# ships a PNG-only build, which cannot encode H.264.
if [[ -z "${FFMPEG:-}" ]]; then
  if command -v ffmpeg >/dev/null; then FFMPEG=ffmpeg
  elif [[ -x node_modules/ffmpeg-static/ffmpeg ]]; then FFMPEG=node_modules/ffmpeg-static/ffmpeg
  else echo "no ffmpeg: npm install ffmpeg-static" >&2; exit 1; fi
fi
# Capture rather than pipe into grep: under `set -o pipefail`, grep -q exits on
# the first match, ffmpeg takes SIGPIPE, and the pipeline reports failure even
# though the encoder is present.
ENC="$("$FFMPEG" -hide_banner -encoders 2>/dev/null || true)"
case "$ENC" in *libx264*) ;; *) echo "ffmpeg at $FFMPEG has no libx264" >&2; exit 1 ;; esac

mkdir -p "$BUILD" "$DIST"
[[ -d node_modules/playwright ]] || npm install --no-audit --no-fund playwright

echo "==> score"
python3 music.py "$BUILD/score.wav"

echo "==> captions (single source: vo.py -> srt + vtt + burned-in)"
python3 vo.py

echo "==> frames (${JOBS} in parallel @ ${FPS} fps)"
render () { node render.mjs --w "$1" --h "$2" --fps "$FPS" --cc "$3" --out "$BUILD/$4" >"$BUILD/$4.log" 2>&1; }
pids=()
render 1920 1080 1 f-16x9-cc    & pids+=($!)
render 1920 1080 0 f-16x9-clean & pids+=($!)
render 1080 1920 1 f-9x16-cc    & pids+=($!)
render 1080 1080 1 f-1x1-cc     & pids+=($!)
fail=0
for p in "${pids[@]}"; do wait "$p" || fail=1; done
if (( fail )); then echo "a frame render failed — see $BUILD/*.log" >&2; tail -5 "$BUILD"/*.log >&2; exit 1; fi
for d in f-16x9-cc f-16x9-clean f-9x16-cc f-1x1-cc; do
  echo "    $d: $(ls "$BUILD/$d" | wc -l) frames"
done

# $1 frame dir  $2 output  $3 crf  $4 audio(1/0)
encode () {
  local a=(); [[ "$4" == 1 ]] && a=(-i "$BUILD/score.wav" -map 0:v -map 1:a -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest) || a=(-map 0:v -an)
  "$FFMPEG" -hide_banner -loglevel error -y -framerate "$FPS" -i "$BUILD/$1/%05d.png" "${a[@]}" \
    -c:v libx264 -preset slow -crf "$3" -pix_fmt yuv420p -profile:v high -level 4.1 \
    -movflags +faststart "$DIST/$2"
  echo "    $2  $(du -h "$DIST/$2" | cut -f1)"
}

echo "==> encode"
encode f-16x9-cc    "$NAME-1920x1080-captions.mp4" 17 1
encode f-16x9-clean "$NAME-1920x1080-clean.mp4"    17 1
encode f-9x16-cc    "$NAME-1080x1920-captions.mp4" 17 1
encode f-1x1-cc     "$NAME-1080x1080-captions.mp4" 17 1
encode f-16x9-clean "$NAME-1920x1080-silent.mp4"   17 0
echo "==> high-quality master (CRF 12, near-visually-lossless)"
encode f-16x9-clean "$NAME-1920x1080-MASTER.mp4"   12 1

echo "==> stills"
poster=$(printf "%05d" $((FPS * 41)))       # 41.0s — the identity shot
thumb=$(printf "%05d" $((FPS * 65)))        # 65.0s — the light closing statement
cp "$BUILD/f-16x9-clean/$poster.png" "$DIST/$NAME-poster.png"
cp "$BUILD/f-16x9-clean/$thumb.png"  "$DIST/$NAME-thumbnail-1920x1080.png"
"$FFMPEG" -hide_banner -loglevel error -y -i "$DIST/$NAME-thumbnail-1920x1080.png" \
  -vf scale=1280:720 "$DIST/$NAME-thumbnail-1280x720.png"

cp ../captions/*.srt ../captions/*.vtt "$DIST/" 2>/dev/null || true
cp "$BUILD/score.wav" "$DIST/$NAME-score.wav"

echo; ls -la "$DIST"
