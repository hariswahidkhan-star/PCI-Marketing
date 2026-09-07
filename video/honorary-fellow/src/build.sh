#!/usr/bin/env bash
# Build the Honorary Fellow (PCI) film.
#
#   ./build.sh            full build, 30 fps
#   ./build.sh --fast     15 fps, for checking an edit
#
# Order matters: sync.py runs first, because it measures the recorded narration
# and writes the cut list that scene.html, vo.py and music.py all read.
set -euo pipefail
cd "$(dirname "$0")"
BUILD=../build; DIST=../dist
FPS=30; [[ "${1:-}" == "--fast" ]] && FPS=15
NAME="pci-honorary-fellow"
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

# MUSIC selects the bed under the narration. Default: the ElevenLabs Music v2
# track PCI asked for (see ../music/README.md), trimmed to the film and faded
# out over its last five seconds. MUSIC= (empty) uses the standard-library
# score instead. A produced track is far denser than the synthesised score,
# so it sits lower (BED) before the side-chain; the margin is measured after
# every build, not assumed.
MUSIC="${MUSIC-../music/eleven-music-bed.mp3}"
if [[ -n "$MUSIC" ]]; then
  TOTAL="$(python3 -c "import json;print(json.load(open('timeline.json'))['total'])")"
  FADE_AT="$(python3 -c "print(max(0.0, $TOTAL - 5.0))")"
  "$FFMPEG" -hide_banner -loglevel error -y -i "$MUSIC" \
    -af "atrim=0:$TOTAL,afade=t=in:st=0:d=1.5,afade=t=out:st=$FADE_AT:d=5" \
    -ar 48000 -ac 2 -c:a pcm_s16le "$BUILD/bed.wav"
  # A produced track is dense exactly where speech lives, so under the
  # narration it gets a wide 4 dB dip around 1.5 kHz and a deeper, slower
  # side-chain than the synthesised score needed. Measured on this film:
  # 0.20 + dip = narration 6.0 dB (median) / 3.0 dB (worst) above the music
  # in the voice band at every scene beat, with the music itself still at
  # about -26 dBFS between scenes. 0.24 halved that margin; 0.30 lost it.
  BED="${BED:-0.20}"; BEDFX="equalizer=f=1500:t=q:w=0.8:g=-4,"
  DUCK="threshold=0.035:ratio=10:attack=8:release=400"
else
  cp "$BUILD/score.wav" "$BUILD/bed.wav"; BED="${BED:-0.66}"; BEDFX=""
  DUCK="threshold=0.040:ratio=8:attack=10:release=300"
fi

echo "==> mix (score side-chained under the voice)"
# -14 LUFS, not -16: PCI asked for a louder film, and -14 is what YouTube and
# LinkedIn normalise to, so anything hotter is turned back down on upload and
# anything quieter arrives quieter than the video before it. LRA 9 keeps the
# quiet open from being lost at that level. The bed is up too (0.58 -> 0.66),
# with the side-chain still putting the voice in front — the margin is measured
# after every build. level=disabled matters more than the ceiling: alimiter
# auto-levels back to 0 dB by default, so `limit` only sets where limiting
# starts and the result is then renormalised — which pushes true peak over the
# -1.0 dBTP the platforms expect. 0.85 (-1.4 dBFS) leaves room for the
# inter-sample peaks AAC reconstructs.
"$FFMPEG" -hide_banner -loglevel error -y -i "$BUILD/bed.wav" -i ../audio/vo-track.wav \
  -filter_complex "[0:a]${BEDFX}volume=$BED[bed];\
[bed][1:a]sidechaincompress=$DUCK[duck];\
[duck][1:a]amix=inputs=2:normalize=0:duration=longest,\
loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.85:level=disabled[mix]" \
  -map "[mix]" -ar 48000 -ac 2 -c:a pcm_s16le "$BUILD/mixed.wav"

# Frames stream straight from the renderer into ffmpeg. A 4K frame is ~3 MB of
# lossless PNG, so staging even one pass would want ~11 GB of scratch; piping
# needs none of it. See ../../explainer/README.md for the measurements.
V=(-c:v libx264 -preset slow -pix_fmt yuv420p -movflags +faststart)
A=(-c:a aac -b:a 192k -ar 48000 -ac 2)
POSTER_F=$((FPS*11)); THUMB_F=$((FPS*84))

pipe(){ # w h cc logname -- then ffmpeg output args
  local w=$1 h=$2 cc=$3 log=$4; shift 5
  node render.mjs --w "$w" --h "$h" --fps "$FPS" --cc "$cc" --theme "$THEME" \
       --pipe 1 ${STILLS_ARGS[@]+"${STILLS_ARGS[@]}"} 2>"$BUILD/$log.log" \
    | "$FFMPEG" -hide_banner -loglevel error -y -f image2pipe -c:v png -framerate "$FPS" -i - \
        -i "$BUILD/mixed.wav" "$@" 2>>"$BUILD/$log.log"
}
STILLS_ARGS=()

# Wave 1 — the 4K master pair. Run alone: two 3840x2160 renders plus their
# encodes already saturate four cores, and adding the HD passes here makes all
# five slower than running them in two waves.
wave1(){
echo "==> wave 1: 4K master (captioned + clean) @ ${FPS} fps"
( STILLS_ARGS=(--stills "$POSTER_F,$THUMB_F" --stillsdir ../build/stills)
  pipe 3840 2160 0 f-4k-clean -- \
    -map 0:v -map 1:a "${V[@]}" -profile:v high -level 5.1 -crf 16 "${A[@]}" -shortest \
    "$DIST/$NAME-3840x2160-MASTER-clean.mp4" ) & p1=$!
( pipe 3840 2160 1 f-4k-cc -- \
    -map 0:v -map 1:a "${V[@]}" -profile:v high -level 5.1 -crf 16 "${A[@]}" -shortest \
    "$DIST/$NAME-3840x2160-MASTER-captions.mp4" ) & p2=$!
fail=0; for p in $p1 $p2; do wait "$p" || fail=1; done
(( fail )) && { echo "4K render failed — see $BUILD/*.log" >&2; tail -20 "$BUILD"/f-4k-*.log >&2; exit 1; }

}
wave2(){
echo "==> wave 2: 1080 landscape, 9:16 vertical, 1:1 square"
( pipe 1920 1080 1 f-16x9-cc -- \
    -map 0:v -map 1:a "${V[@]}" -profile:v high -level 4.1 -crf 18 "${A[@]}" -shortest \
    "$DIST/$NAME-1920x1080-captions.mp4" \
    -map 0:v "${V[@]}" -profile:v high -level 4.1 -crf 18 -an \
    "$DIST/$NAME-1920x1080-silent.mp4" ) & q1=$!
( pipe 1080 1920 1 f-9x16-cc -- \
    -map 0:v -map 1:a "${V[@]}" -profile:v high -level 4.1 -crf 18 "${A[@]}" -shortest \
    "$DIST/$NAME-1080x1920-captions.mp4" ) & q2=$!
( pipe 1080 1080 1 f-1x1-cc -- \
    -map 0:v -map 1:a "${V[@]}" -profile:v high -level 4.1 -crf 18 "${A[@]}" -shortest \
    "$DIST/$NAME-1080x1080-captions.mp4" ) & q3=$!
fail=0; for p in $q1 $q2 $q3; do wait "$p" || fail=1; done
(( fail )) && { echo "HD render failed — see $BUILD/*.log" >&2; tail -20 "$BUILD"/f-*.log >&2; exit 1; }

}
# HD_FIRST=1 runs the three HD cuts before the 4K pair, so the files PCI
# actually shares arrive first; the 1080 clean downscale still waits for 4K.
if [[ "${HD_FIRST:-0}" == "1" ]]; then wave2; wave1; else wave1; wave2; fi

# The 1080 clean master is a downscale of the 4K clean master rather than a
# sixth render: same picture, and a Lanczos downscale of 4K is sharper than a
# native 1080 render of the same frames.
"$FFMPEG" -hide_banner -loglevel error -y -i "$DIST/$NAME-3840x2160-MASTER-clean.mp4" \
  -vf scale=1920:1080:flags=lanczos "${V[@]}" -profile:v high -level 4.1 -crf 18 \
  -c:a copy "$DIST/$NAME-1920x1080-clean.mp4"

for f in "$NAME-3840x2160-MASTER-captions.mp4" "$NAME-3840x2160-MASTER-clean.mp4" \
         "$NAME-1920x1080-captions.mp4" "$NAME-1920x1080-clean.mp4" \
         "$NAME-1920x1080-silent.mp4" "$NAME-1080x1920-captions.mp4" \
         "$NAME-1080x1080-captions.mp4"; do
  echo "    $f  $(du -h "$DIST/$f" | cut -f1)"
done

echo "==> stills"
cp "$BUILD/stills/$(printf '%05d' "$POSTER_F").png" "$DIST/$NAME-poster-3840x2160.png"
cp "$BUILD/stills/$(printf '%05d' "$THUMB_F").png" "$DIST/$NAME-thumbnail-3840x2160.png"
"$FFMPEG" -hide_banner -loglevel error -y -i "$DIST/$NAME-thumbnail-3840x2160.png" \
  -vf scale=1920:1080:flags=lanczos "$DIST/$NAME-thumbnail-1920x1080.png"
"$FFMPEG" -hide_banner -loglevel error -y -i "$DIST/$NAME-thumbnail-3840x2160.png" \
  -vf scale=1280:720:flags=lanczos "$DIST/$NAME-thumbnail-1280x720.png"
cp ../captions/*.srt ../captions/*.vtt "$DIST/" 2>/dev/null || true
cp "$BUILD/score.wav" "$DIST/$NAME-score.wav"
cp "$BUILD/bed.wav" "$DIST/$NAME-music-bed.wav"
cp ../audio/vo-track.wav "$DIST/$NAME-voiceover.wav"
cp "$BUILD/mixed.wav" "$DIST/$NAME-mixed-soundtrack.wav"
echo; ls -la "$DIST"
