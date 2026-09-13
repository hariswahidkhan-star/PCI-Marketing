#!/usr/bin/env bash
# Build ../build/mixed.wav from the bed and the narration. Sourced or run by
# build-serial.sh, remix.sh and complete-v3.sh so there is exactly one mix.
#
# Two passes, deliberately.
#
# loudnorm's single-pass "dynamic" mode normalises in short windows, which
# compresses the programme as a side effect: the ridden mix goes in at LRA 3.6
# and comes out at 2.8, landing at -13.5 instead of -14. Measuring first and
# then applying a single fixed gain keeps the range exactly and hits the target
# exactly. Measured on the v3 mix: dynamic -> I -13.5 / LRA 2.8; two-pass ->
# I -14.0 / LRA 3.6 / TP -1.56 dBTP.
#
# loudnorm's own linear mode will not do this here. The gain needed is +4.1 dB
# and the mix's true peak is -3.46 dBTP, so a linear gain would land at +0.67
# dBTP; loudnorm sees that it would breach the peak target and silently falls
# back to dynamic. The peak reduction is required either way — the crest factor
# is 14.7 dB and -14 LUFS at -1.5 dBTP allows 12.5 — so it is done with a
# limiter on the transients instead of compression across the whole programme.
#
# The gain is measured, never hardcoded: re-record the read and this still
# lands on target.
set -euo pipefail
cd "$(dirname "$0")"
BUILD=../build
FFMPEG=node_modules/ffmpeg-static/ffmpeg
TARGET_I=-14
LIMIT=0.7943          # -2.0 dBFS ceiling; measures -1.56 dBTP, inside the -1.5 spec

[[ -s "$BUILD/bed.wav" ]] || { echo "mixdown: no $BUILD/bed.wav" >&2; exit 1; }
[[ -s ../audio/vo-track.wav ]] || { echo "mixdown: no ../audio/vo-track.wav" >&2; exit 1; }

VOXENV="$(python3 voxenv.py)"
[[ -n "$VOXENV" ]] || { echo "mixdown: voxenv.py produced nothing" >&2; exit 1; }

BED="${BED:-0.42}"
GRAPH="[1:a]volume='$VOXENV':eval=frame,asplit=2[vx1][vx2];\
[0:a]equalizer=f=1800:t=q:w=0.9:g=-3,volume=$BED[bed];\
[bed][vx1]sidechaincompress=threshold=0.035:ratio=10:attack=8:release=400[duck];\
[duck][vx2]amix=inputs=2:normalize=0:duration=longest"

# pass 1 — measure. `ffmpeg -i` with no output exits 1 by design, so contain it.
MEAS="$({ "$FFMPEG" -hide_banner -i "$BUILD/bed.wav" -i ../audio/vo-track.wav \
          -filter_complex "${GRAPH},loudnorm=I=$TARGET_I:TP=-1.5:LRA=11:print_format=json" \
          -f null - 2>&1 || true; } | sed -n '/^{/,/^}/p')"
IN_I="$(printf '%s' "$MEAS" | sed -n 's/.*"input_i"[^-0-9]*\(-\?[0-9.]*\).*/\1/p')"
[[ -n "$IN_I" ]] || { echo "mixdown: could not measure the mix" >&2; echo "$MEAS" >&2; exit 1; }
GAIN="$(awk -v t="$TARGET_I" -v i="$IN_I" 'BEGIN{printf "%.2f", t-i}')"
echo "    measured ${IN_I} LUFS, applying ${GAIN} dB"

# pass 2 — one fixed gain, then a limiter on the peaks only.
"$FFMPEG" -hide_banner -loglevel error -y -i "$BUILD/bed.wav" -i ../audio/vo-track.wav \
  -filter_complex "${GRAPH},volume=${GAIN}dB,alimiter=limit=${LIMIT}:level=disabled[mix]" \
  -map "[mix]" -ar 48000 -ac 2 -c:a pcm_s16le "$BUILD/mixed.wav"

{ "$FFMPEG" -hide_banner -i "$BUILD/mixed.wav" -af ebur128=framelog=quiet -f null - 2>&1 || true; } \
  | grep -E "^    I: |^    LRA: " | head -2
