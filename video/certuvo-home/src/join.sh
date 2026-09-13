#!/usr/bin/env bash
# Join the Certuvo intro sting + film + outro sting into one file per aspect.
#
# No certifications card here: scene 3 of this film IS the credential wall, so a
# card after it would repeat itself. (The one-minute cut needs one because it
# has no wall — see ../../certuvo-cma-60/src/join.sh.)
#
# The stings are 832x464 @ 60 fps, 44.1 kHz; the film is the target size @ 30 fps,
# 48 kHz. Each sting is fitted inside the frame and padded with the film's own
# ground (#F5F7FB) so the join is invisible on the light treatment, then all
# three are concatenated in one pass. Sting audio is normalised to the film's
# -14 LUFS so the level does not jump.
#
# Run this ONCE at a time. Two concurrent runs writing the same outputs produced
# four files with 6,000-9,000 NAL-unit decode errors each.
set -euo pipefail
cd "$(dirname "$0")"
DIST=../dist; NAME="certuvo-home"
FFMPEG=node_modules/ffmpeg-static/ffmpeg
INTRO=../assets/intro.mp4; OUTRO=../assets/outro.mp4
GROUND=0xF5F7FB

join(){ # w h in out
  local W=$1 H=$2 IN=$3 OUT=$4
  [[ -s "$IN" ]] || { echo "skip (missing) $IN"; return 0; }
  echo "==> ${W}x${H}  $(basename "$OUT")"
  local fit="scale=$W:$H:force_original_aspect_ratio=decrease,pad=$W:$H:(ow-iw)/2:(oh-ih)/2:color=$GROUND,fps=30,setsar=1,format=yuv420p"
  "$FFMPEG" -hide_banner -loglevel error -y -i "$INTRO" -i "$IN" -i "$OUTRO" -filter_complex "\
[0:v]$fit[v0];\
[1:v]scale=$W:$H,fps=30,setsar=1,format=yuv420p[v1];\
[2:v]$fit[v2];\
[0:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st=7.5:d=0.5[a0];\
[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];\
[2:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=in:st=0:d=0.4[a2];\
[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]" \
    -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -movflags +faststart \
    -c:a aac -b:a 192k -ar 48000 -ac 2 "$OUT"
}

join 1920 1080 "$DIST/$NAME-1920x1080-captions.mp4" "$DIST/$NAME-FULL-1920x1080-captions.mp4"
join 1920 1080 "$DIST/$NAME-1920x1080-clean.mp4"    "$DIST/$NAME-FULL-1920x1080-clean.mp4"
join 1080 1920 "$DIST/$NAME-1080x1920-captions.mp4" "$DIST/$NAME-FULL-1080x1920-captions.mp4"
join 1080 1080 "$DIST/$NAME-1080x1080-captions.mp4" "$DIST/$NAME-FULL-1080x1080-captions.mp4"
echo "==> joined"; ls -la "$DIST"/*FULL* 2>/dev/null
