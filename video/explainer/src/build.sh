#!/usr/bin/env bash
# Build the PCI AI explainer.
#
#   ./build.sh            full build, 30 fps
#   ./build.sh --fast     15 fps, for checking an edit
#
# Order matters: sync.py must run first, because it measures the recorded
# narration and writes the cut list that scene.html, vo.py and music.py all read.
set -euo pipefail
cd "$(dirname "$0")"
BUILD=../build; DIST=../dist
FPS=30; [[ "${1:-}" == "--fast" ]] && FPS=15
NAME="pci-ai-explainer"
# theme=light is the film's look; THEME=dark renders the ink variant from the
# same source, no other change required.
THEME="${THEME:-light}"

if [[ -z "${FFMPEG:-}" ]]; then
  if command -v ffmpeg >/dev/null; then FFMPEG=ffmpeg
  elif [[ -x node_modules/ffmpeg-static/ffmpeg ]]; then FFMPEG=node_modules/ffmpeg-static/ffmpeg
  else echo "no ffmpeg" >&2; exit 1; fi
fi
ENC="$("$FFMPEG" -hide_banner -encoders 2>/dev/null || true)"
case "$ENC" in *libx264*) ;; *) echo "ffmpeg has no libx264" >&2; exit 1 ;; esac
mkdir -p "$BUILD" "$DIST"

echo "==> conform timeline to the recorded voice"
python3 sync.py
echo "==> captions"
python3 vo.py
echo "==> score"
python3 music.py "$BUILD/score.wav"

echo "==> mix (score side-chained under the voice)"
"$FFMPEG" -hide_banner -loglevel error -y -i "$BUILD/score.wav" -i ../audio/vo-track.wav \
  -filter_complex "[0:a]volume=0.60[bed];\
[bed][1:a]sidechaincompress=threshold=0.045:ratio=7:attack=12:release=320[duck];\
[duck][1:a]amix=inputs=2:normalize=0:duration=longest,\
loudnorm=I=-16:TP=-1.5:LRA=11,alimiter=limit=0.95[mix]" \
  -map "[mix]" -ar 48000 -ac 2 -c:a pcm_s16le "$BUILD/mixed.wav"

echo "==> frames @ ${FPS} fps, theme=${THEME}"
render(){ node render.mjs --w "$1" --h "$2" --fps "$FPS" --cc "$3" --theme "$THEME" --out "$BUILD/$4" >"$BUILD/$4.log" 2>&1; }
pids=()
render 1920 1080 1 f-16x9-cc    & pids+=($!)
render 1920 1080 0 f-16x9-clean & pids+=($!)
render 1080 1920 1 f-9x16-cc    & pids+=($!)
fail=0; for p in "${pids[@]}"; do wait "$p" || fail=1; done
(( fail )) && { echo "frame render failed — see $BUILD/*.log" >&2; tail -5 "$BUILD"/*.log >&2; exit 1; }
for d in f-16x9-cc f-16x9-clean f-9x16-cc; do echo "    $d: $(ls "$BUILD/$d" | wc -l) frames"; done

encode(){ local a=(); [[ "$4" == 1 ]] && a=(-i "$BUILD/mixed.wav" -map 0:v -map 1:a -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest) || a=(-map 0:v -an)
  "$FFMPEG" -hide_banner -loglevel error -y -framerate "$FPS" -i "$BUILD/$1/%05d.png" "${a[@]}" \
    -c:v libx264 -preset slow -crf "$3" -pix_fmt yuv420p -profile:v high -level 4.1 \
    -movflags +faststart "$DIST/$2"
  echo "    $2  $(du -h "$DIST/$2" | cut -f1)"; }

echo "==> encode"
encode f-16x9-cc    "$NAME-1920x1080-captions.mp4" 18 1
encode f-16x9-clean "$NAME-1920x1080-clean.mp4"    18 1
encode f-9x16-cc    "$NAME-1080x1920-captions.mp4" 18 1
encode f-16x9-clean "$NAME-1920x1080-silent.mp4"   18 0
echo "==> high-quality master"
encode f-16x9-clean "$NAME-1920x1080-MASTER.mp4"   14 1

echo "==> stills"
cp "$BUILD/f-16x9-clean/$(printf '%05d' $((FPS*95))).png" "$DIST/$NAME-poster.png"
cp "$BUILD/f-16x9-clean/$(printf '%05d' $((FPS*125))).png" "$DIST/$NAME-thumbnail-1920x1080.png"
"$FFMPEG" -hide_banner -loglevel error -y -i "$DIST/$NAME-thumbnail-1920x1080.png" -vf scale=1280:720 "$DIST/$NAME-thumbnail-1280x720.png"
cp ../captions/*.srt ../captions/*.vtt "$DIST/" 2>/dev/null || true
cp "$BUILD/score.wav" "$DIST/$NAME-score.wav"
cp ../audio/vo-track.wav "$DIST/$NAME-voiceover.wav"
cp "$BUILD/mixed.wav" "$DIST/$NAME-mixed-soundtrack.wav"
echo; ls -la "$DIST"
