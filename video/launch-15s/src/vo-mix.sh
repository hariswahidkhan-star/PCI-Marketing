#!/usr/bin/env bash
# Lay the generated voiceover into the 15-second film.
#
# The film's picture and burned-in captions are already locked, so the voice is
# fitted to the script's existing windows rather than the other way round: each
# line is de-silenced, then time-scaled with librubberband (formant-preserving)
# only if it overruns its window. Nothing is re-encoded on the video side.
set -euo pipefail
cd "$(dirname "$0")"
AUD=../audio; DIST=../dist; BUILD=../build
if [[ -z "${FFMPEG:-}" ]]; then
  if command -v ffmpeg >/dev/null; then FFMPEG=ffmpeg
  elif [[ -x ../../intro-75s/src/node_modules/ffmpeg-static/ffmpeg ]]; then FFMPEG=../../intro-75s/src/node_modules/ffmpeg-static/ffmpeg
  else echo "no ffmpeg" >&2; exit 1; fi
fi
mkdir -p "$BUILD"

# line : in : out   (from script.md — identical to the burned-in caption timings)
LINES=("1:0.30:3.25" "2:3.70:6.65" "3:6.95:9.75" "4:10.05:13.00")

dur(){ p="$("$FFMPEG" -hide_banner -i "$1" 2>&1 || true)"
       printf '%s' "$p" | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' | head -1 \
       | awk -F: '{printf "%.3f",($1*3600)+($2*60)+$3}'; }

inputs=(); filters=(); mixin=""
i=0
for row in "${LINES[@]}"; do
  IFS=: read -r n a b <<<"$row"
  win=$(python3 -c "print(f'{$b-$a:.3f}')")
  "$FFMPEG" -hide_banner -loglevel error -y -i "$AUD/vo-$n.mp3" \
    -af "silenceremove=start_periods=1:start_silence=0.02:start_threshold=-50dB:detection=peak,areverse,silenceremove=start_periods=1:start_silence=0.02:start_threshold=-50dB:detection=peak,areverse" \
    -ar 48000 -ac 1 "$BUILD/vo-$n-trim.wav"
  d=$(dur "$BUILD/vo-$n-trim.wav")
  f=$(python3 -c "print(f'{max(1.0, $d/$win):.5f}')")
  delay=$(python3 -c "print(int(round($a*1000)))")
  printf "  line %s  %ss -> window %ss  stretch %s\n" "$n" "$d" "$win" "$f"
  inputs+=(-i "$BUILD/vo-$n-trim.wav")
  ch="[$i:a]"
  [[ "$f" != "1.00000" ]] && ch+="rubberband=tempo=$f:pitch=1:formant=preserved,"
  ch+="adelay=$delay|$delay,apad[v$n]"
  filters+=("$ch"); mixin+="[v$n]"; i=$((i+1))
done

echo "==> voice track"
"$FFMPEG" -hide_banner -loglevel error -y "${inputs[@]}" -filter_complex \
  "$(IFS=';'; echo "${filters[*]}");${mixin}amix=inputs=4:normalize=0:duration=longest,atrim=0:15.0,asetpts=N/SR/TB,loudnorm=I=-18:TP=-1.5:LRA=11[out]" \
  -map "[out]" -ar 48000 -ac 1 -c:a pcm_s16le "$DIST/pci-launch-15s-voiceover.wav"

echo "==> mixed soundtrack (score side-chained under the voice)"
"$FFMPEG" -hide_banner -loglevel error -y \
  -i "$DIST/pci-launch-15s-score.wav" -i "$DIST/pci-launch-15s-voiceover.wav" \
  -filter_complex "[0:a]volume=0.62[bed];[bed][1:a]sidechaincompress=threshold=0.045:ratio=7:attack=12:release=300[duck];\
[duck][1:a]amix=inputs=2:normalize=0:duration=longest,loudnorm=I=-16:TP=-1.5:LRA=11,alimiter=limit=0.95[mix]" \
  -map "[mix]" -ar 48000 -ac 2 -c:a pcm_s16le "$DIST/pci-launch-15s-mixed-soundtrack.wav"

echo "==> re-mux (video stream copied, not re-encoded)"
for f in pci-launch-15s-1920x1080-captions pci-launch-15s-1080x1080-captions pci-launch-15s-1920x1080-clean; do
  [[ -f "$DIST/$f.mp4" ]] || continue
  "$FFMPEG" -hide_banner -loglevel error -y -i "$DIST/$f.mp4" -i "$DIST/pci-launch-15s-mixed-soundtrack.wav" \
    -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -shortest "$BUILD/$f.tmp.mp4"
  mv "$BUILD/$f.tmp.mp4" "$DIST/$f.mp4"
  echo "    $f.mp4"
done
echo "(the silent master is left silent by design)"
