#!/usr/bin/env bash
# Composite Runway B-roll under the PCI AI type layer.
#
#   ./composite.sh                 build the 16:9 B-roll variant
#   ./composite.sh 1080 1920 9x16  build another aspect
#
# WHY THIS IS A SEPARATE SCRIPT. Runway's artifact CDN
# (dnznrvs05pmza.cloudfront.net) is blocked by the egress policy of the
# environment the film was produced in, so the generated clips could not be
# pulled in and composited there. Download them from your Runway workspace
# into ../assets/generated/ using the filenames below, then run this.
#
# Clips expected in ../assets/generated/ (any duration; they are fitted):
#   s1-infrastructure.mp4   s2-project-office.mp4   s3-analysis.mp4
#   s4-decision-meeting.mp4 s7-judgment.mp4
#
# Scenes 5, 6 and 8 deliberately get NO footage. They carry the identity, the
# credential framework and the end card, and generated imagery must never sit
# behind those frames — it would risk reading as an actual PCI facility.
set -euo pipefail
cd "$(dirname "$0")"

W="${1:-1920}"; H="${2:-1080}"; TAG="${3:-16x9}"
FPS=30; NAME="pci-ai-intro-75s"
GEN=../assets/generated; BUILD=../build/comp-$TAG; DIST=../dist
PLATE="../build/p-${TAG}-cc"

if [[ -z "${FFMPEG:-}" ]]; then
  if command -v ffmpeg >/dev/null; then FFMPEG=ffmpeg
  elif [[ -x node_modules/ffmpeg-static/ffmpeg ]]; then FFMPEG=node_modules/ffmpeg-static/ffmpeg
  else echo "no ffmpeg" >&2; exit 1; fi
fi
[[ -d "$PLATE" ]] || { echo "missing alpha plate frames: $PLATE (run plates.sh)" >&2; exit 1; }
mkdir -p "$BUILD" "$DIST"

# scene:  start  end  source            matte colour (used when no clip)
SCENES=(
  "0.00  8.50  s1-infrastructure   0x141219"
  "8.50  16.60 s2-project-office   0x101923"
  "16.60 26.90 s3-analysis         0x1E1512"
  "26.90 36.30 s4-decision-meeting 0x0F172A"
  "36.30 47.40 -                   0x0A0F1C"
  "47.40 57.60 -                   0x18141D"
  "57.60 70.80 s7-judgment         0x0F172A"
  "70.80 75.00 -                   0x0F172A"
)

echo "==> background segments (${W}x${H})"
i=0; list="$BUILD/segments.txt"; : > "$list"
for row in "${SCENES[@]}"; do
  read -r a b src colour <<<"$row"
  dur=$(python3 -c "print(f'{$b-$a:.3f}')")
  out="$BUILD/seg$(printf '%02d' $i).mp4"
  clip="$GEN/$src.mp4"
  if [[ "$src" != "-" && -f "$clip" ]]; then
    # `ffmpeg -i` with no output file exits 1 by design; under `set -o pipefail`
    # that would abort the script, so the probe is isolated with `|| true`.
    probe="$("$FFMPEG" -hide_banner -i "$clip" 2>&1 || true)"
    srcdur=$(printf '%s' "$probe" | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' | head -1 \
             | awk -F: '{print ($1*3600)+($2*60)+$3}')
    [[ -n "$srcdur" ]] || { echo "could not read duration of $clip" >&2; exit 1; }
    # Fit the clip to the scene: trim if it is longer, ease it out if shorter.
    ratio=$(python3 -c "print(f'{max(1.0, $dur/$srcdur):.5f}')")
    # Grade toward the brand: hold back saturation, lift the blacks slightly,
    # and let the plate's scrim carry legibility rather than crushing here.
    "$FFMPEG" -hide_banner -loglevel error -y -i "$clip" -filter_complex \
      "[0:v]setpts=PTS*${ratio},fps=${FPS},scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},\
eq=saturation=0.72:contrast=1.04:brightness=-0.035,colorbalance=rs=-0.02:bs=0.05:gm=-0.01,\
trim=duration=${dur},setpts=PTS-STARTPTS,fade=t=in:st=0:d=0.42,fade=t=out:st=$(python3 -c "print(f'{$dur-0.42:.3f}')"):d=0.42[v]" \
      -map "[v]" -an -c:v libx264 -preset medium -crf 16 -pix_fmt yuv420p -r $FPS "$out"
  else
    "$FFMPEG" -hide_banner -loglevel error -y -f lavfi \
      -i "color=c=${colour}:s=${W}x${H}:r=${FPS}:d=${dur}" \
      -an -c:v libx264 -preset medium -crf 16 -pix_fmt yuv420p "$out"
  fi
  echo "file '$(basename "$out")'" >> "$list"
  printf "    seg%02d %5ss  %s\n" $i "$dur" "$([[ $src == - ]] && echo matte || echo $src)"
  i=$((i+1))
done

echo "==> concat background"
"$FFMPEG" -hide_banner -loglevel error -y -f concat -safe 0 -i "$list" \
  -c:v libx264 -preset medium -crf 16 -pix_fmt yuv420p -r $FPS "$BUILD/bg.mp4"

echo "==> overlay type layer + score"
"$FFMPEG" -hide_banner -loglevel error -y \
  -i "$BUILD/bg.mp4" \
  -framerate $FPS -i "$PLATE/%05d.png" \
  -i ../build/score.wav \
  -filter_complex "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]" \
  -map "[v]" -map 2:a -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p \
  -profile:v high -level 4.1 -movflags +faststart \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest \
  "$DIST/$NAME-${W}x${H}-broll-captions.mp4"

echo
ls -la "$DIST/$NAME-${W}x${H}-broll-captions.mp4"
