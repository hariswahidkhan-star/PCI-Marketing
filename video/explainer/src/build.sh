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

echo "==> frames + encode @ ${FPS} fps, theme=${THEME}"
# Frames are streamed straight from the renderer into ffmpeg rather than staged
# on disk. At 938 KB a frame the three aspects of this film would want ~22 GB of
# scratch, which does not fit; piping needs none of it and removes a whole class
# of half-written-frame failure. The three aspects still run in parallel.
V=(-c:v libx264 -preset slow -pix_fmt yuv420p -profile:v high -level 4.1 -movflags +faststart)
A=(-c:a aac -b:a 192k -ar 48000 -ac 2)

# Poster and thumbnail are lifted from the clean pass as lossless PNGs, so the
# stills are the rendered pixels and not a frame decoded back out of h264.
POSTER_F=$((FPS*95)); THUMB_F=$((FPS*125))

pipe(){ # w h cc logname -- then ffmpeg output args
  local w=$1 h=$2 cc=$3 log=$4; shift 5
  node render.mjs --w "$w" --h "$h" --fps "$FPS" --cc "$cc" --theme "$THEME" \
       --pipe 1 ${STILLS_ARGS[@]+"${STILLS_ARGS[@]}"} 2>"$BUILD/$log.log" \
    | "$FFMPEG" -hide_banner -loglevel error -y -f image2pipe -c:v png -framerate "$FPS" -i - \
        -i "$BUILD/mixed.wav" "$@" 2>>"$BUILD/$log.log"
}

STILLS_ARGS=()
( pipe 1920 1080 1 f-16x9-cc -- \
    -map 0:v -map 1:a "${V[@]}" -crf 18 "${A[@]}" -shortest "$DIST/$NAME-1920x1080-captions.mp4" ) & p1=$!
( pipe 1080 1920 1 f-9x16-cc -- \
    -map 0:v -map 1:a "${V[@]}" -crf 18 "${A[@]}" -shortest "$DIST/$NAME-1080x1920-captions.mp4" ) & p2=$!
# One clean pass feeds both the delivery encode and the crf 14 master, so the
# frames are rendered once and encoded twice from the same pipe.
( STILLS_ARGS=(--stills "$POSTER_F,$THUMB_F" --stillsdir ../build/stills)
  pipe 1920 1080 0 f-16x9-clean -- \
    -map 0:v -map 1:a "${V[@]}" -crf 18 "${A[@]}" -shortest "$DIST/$NAME-1920x1080-clean.mp4" \
    -map 0:v -map 1:a "${V[@]}" -crf 14 "${A[@]}" -shortest "$DIST/$NAME-1920x1080-MASTER.mp4" ) & p3=$!

fail=0; for p in $p1 $p2 $p3; do wait "$p" || fail=1; done
(( fail )) && { echo "render/encode failed — see $BUILD/*.log" >&2; tail -20 "$BUILD"/*.log >&2; exit 1; }

# The silent master is the clean master without its audio track: a stream copy,
# so it is the same picture bit for bit rather than a second encode of it.
"$FFMPEG" -hide_banner -loglevel error -y -i "$DIST/$NAME-1920x1080-clean.mp4" \
  -map 0:v -c:v copy -an -movflags +faststart "$DIST/$NAME-1920x1080-silent.mp4"

for f in "$NAME-1920x1080-captions.mp4" "$NAME-1080x1920-captions.mp4" \
         "$NAME-1920x1080-clean.mp4" "$NAME-1920x1080-MASTER.mp4" "$NAME-1920x1080-silent.mp4"; do
  echo "    $f  $(du -h "$DIST/$f" | cut -f1)"
done

echo "==> stills"
cp "$BUILD/stills/$(printf '%05d' "$POSTER_F").png" "$DIST/$NAME-poster.png"
cp "$BUILD/stills/$(printf '%05d' "$THUMB_F").png" "$DIST/$NAME-thumbnail-1920x1080.png"
"$FFMPEG" -hide_banner -loglevel error -y -i "$DIST/$NAME-thumbnail-1920x1080.png" -vf scale=1280:720 "$DIST/$NAME-thumbnail-1280x720.png"
cp ../captions/*.srt ../captions/*.vtt "$DIST/" 2>/dev/null || true
cp "$BUILD/score.wav" "$DIST/$NAME-score.wav"
cp ../audio/vo-track.wav "$DIST/$NAME-voiceover.wav"
cp "$BUILD/mixed.wav" "$DIST/$NAME-mixed-soundtrack.wav"
echo; ls -la "$DIST"
