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

# Mix: the score sits under the voice, side-chained so it steps back only while
# the voice is actually speaking rather than being flatly attenuated throughout.
VO="../audio/vo-track.wav"
AUDIO="$BUILD/score.wav"
if [[ -f "$VO" ]]; then
  echo "==> mix voiceover + score"
# `level=disabled` matters more than the ceiling. alimiter auto-levels its output
# back to 0 dB by default, so `limit` sets where limiting starts and then the
# result is renormalised — which is why the driven score came back at -0.7 dBTP
# under the old limit=0.95, over the -1.0 dBTP EBU R128 and the social platforms
# expect, and why merely lowering the number made the mix *louder* rather than
# quieter. With auto-level off, 0.79 is a real ceiling at -2.1 dBFS, leaving room
# for the inter-sample peaks AAC reconstructs above it. Loudness is unaffected:
# loudnorm sets the integrated level and the limiter only catches transients.
  "$FFMPEG" -hide_banner -loglevel error -y -i "$BUILD/score.wav" -i "$VO" \
    -filter_complex "[0:a]volume=0.62[bed];\
[bed][1:a]sidechaincompress=threshold=0.045:ratio=7:attack=12:release=300[duck];\
[duck][1:a]amix=inputs=2:normalize=0:duration=longest,\
loudnorm=I=-16:TP=-1.5:LRA=11,alimiter=limit=0.79:level=disabled[mix]" \
    -map "[mix]" -ar 48000 -ac 2 -c:a pcm_s16le "$BUILD/mixed.wav"
  AUDIO="$BUILD/mixed.wav"
else
  echo "==> no voice track at $VO — encoding with score only"
fi

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
  local a=(); [[ "$4" == 1 ]] && a=(-i "$AUDIO" -map 0:v -map 1:a -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest) || a=(-map 0:v -an)
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
[[ -f "$VO" ]] && cp "$VO" "$DIST/$NAME-voiceover.wav"
[[ -f "$BUILD/mixed.wav" ]] && cp "$BUILD/mixed.wav" "$DIST/$NAME-mixed-soundtrack.wav"

echo; ls -la "$DIST"
