#!/usr/bin/env bash
# Composite the PCI AI introduction film from source.
#
#   ./build.sh
#
# Rebuilds the brand overlay and re-composites the master. Outputs to ../dist.
#
# NOTE ON REPRODUCIBILITY. The overlay is fully reproducible — overlay.html is
# deterministic in t, so frame N is byte-identical on every run. The FOOTAGE is
# not: the six plates in ../build/shot-*.mp4 were generated once through the
# ElevenLabs Creative connector (ltx-v2-fast) and cannot be regenerated
# identically. Keep them. If they are lost, see ../README.md for the six prompts;
# a regeneration will differ, and the shot windows would need re-checking.
set -euo pipefail
cd "$(dirname "$0")"

BUILD=../build
DIST=../dist
FPS=25
mkdir -p "$BUILD" "$DIST"

command -v ffmpeg >/dev/null || { echo "ffmpeg not on PATH"; exit 1; }
[[ -d node_modules/playwright ]] || npm install --no-audit --no-fund playwright

for n in 01 02 03 04 05 06; do
  [[ -f "$BUILD/shot-$n.mp4" ]] || { echo "missing $BUILD/shot-$n.mp4 — see note above"; exit 1; }
done

echo "==> picture (grade each plate to one look, trim to 10.000s, concat)"
# The six plates are generated independently and do not match: shots 1-4 sit
# around mean luma 40-60, shots 5-6 around 135. That 3x jump is what reads as a
# mismatched cut, so each plate is corrected toward one navy-cool look before a
# shared filmic curve with a highlight rolloff.
LOOK="curves=master='0/0 0.25/0.225 0.75/0.775 1/0.955'"
declare -A G=(
  [01]="eq=brightness=0.030:contrast=1.070:saturation=0.94,colorbalance=rs=-0.02:bs=0.04:bm=0.02"
  [02]="eq=brightness=0.040:contrast=1.090:saturation=0.90,colorbalance=rs=-0.02:bs=0.05:bm=0.02"
  [03]="eq=brightness=0.030:contrast=1.090:saturation=0.90,colorbalance=rs=-0.02:bs=0.05:bm=0.02"
  [04]="eq=brightness=0.005:contrast=1.100:saturation=0.90,colorbalance=rs=-0.02:bs=0.05:bm=0.01"
  [05]="eq=brightness=-0.150:contrast=1.140:saturation=0.78,colorbalance=rs=-0.04:bs=0.09:bm=0.05:bh=0.03"
  [06]="eq=brightness=-0.110:contrast=1.110:saturation=0.82,colorbalance=rs=-0.03:bs=0.07:bm=0.04:bh=0.02"
)
for n in 01 02 03 04 05 06; do
  ffmpeg -hide_banner -loglevel error -y -i "$BUILD/shot-$n.mp4" -t 10.0 \
    -vf "${G[$n]},$LOOK,format=yuv420p" \
    -c:v libx264 -preset slow -crf 17 -profile:v high -level 4.1 \
    -r "$FPS" -an "$BUILD/trim-$n.mp4"
done
printf "file 'trim-%s.mp4'\n" 01 02 03 04 05 06 > "$BUILD/concat.txt"
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i "$BUILD/concat.txt" \
  -c copy "$BUILD/picture.mp4"

echo "==> brand overlay (1500 transparent frames)"
node render-overlay.mjs --w 1920 --h 1080 --fps "$FPS" --out "$BUILD/overlay"

echo "==> mix (voice at -16 LUFS, score ducked beneath it)"
# The score is delayed 2.6s on purpose. eleven_music_v2 wrote its own resolve
# into the last five seconds; undelayed, that fade lands BEFORE the end card and
# the film ends on silence. Delayed, it resolves under the end card instead.
# Never use -shortest here: it clipped the master to 57.1s in an earlier cut.
ffmpeg -hide_banner -loglevel error -y \
  -i ../vo/pci-intro-60s-vo-bed.wav -i ../vo/src-score.mp3 \
  -filter_complex "\
    [0:a]aformat=channel_layouts=stereo:sample_rates=48000,loudnorm=I=-16:TP=-1.5:LRA=11,apad[vo]; \
    [vo]asplit=2[voMix][voKey]; \
    [1:a]aformat=channel_layouts=stereo:sample_rates=48000,loudnorm=I=-20:TP=-3:LRA=7,\
adelay=2600|2600,afade=t=in:st=2.6:d=2.6,apad[m0]; \
    [m0][voKey]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=450:makeup=1[mus]; \
    [voMix][mus]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0[mx]; \
    [mx]alimiter=limit=0.94,atrim=0:60,asetpts=PTS-STARTPTS[a]" \
  -map "[a]" -t 60 -c:a pcm_s24le "$BUILD/mix.wav"

echo "==> composite"
ffmpeg -hide_banner -loglevel error -y \
  -i "$BUILD/picture.mp4" \
  -framerate "$FPS" -i "$BUILD/overlay/%05d.png" \
  -i "$BUILD/mix.wav" \
  -filter_complex "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]" \
  -map "[v]" -map 2:a -t 60 \
  -c:v libx264 -preset slow -crf 20 -profile:v high -level 4.1 \
  -maxrate 6M -bufsize 12M -movflags +faststart \
  -c:a aac -b:a 192k -ar 48000 -ac 2 \
  "$DIST/pci-intro-60s-1920x1080.mp4"

echo "==> poster"
ffmpeg -hide_banner -loglevel error -y -ss 45 -i "$DIST/pci-intro-60s-1920x1080.mp4" \
  -frames:v 1 "$DIST/pci-intro-60s-poster.png"

echo "done -> $DIST"
