#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
B=../build
node render.mjs --w 1920 --h 1080 --fps 30 --cc 1 --plate 1 --out $B/p-16x9-cc    > $B/p1.log 2>&1 &
node render.mjs --w 1920 --h 1080 --fps 30 --cc 0 --plate 1 --out $B/p-16x9-clean > $B/p2.log 2>&1 &
node render.mjs --w 1080 --h 1920 --fps 30 --cc 1 --plate 1 --out $B/p-9x16-cc    > $B/p3.log 2>&1 &
node render.mjs --w 1080 --h 1080 --fps 30 --cc 1 --plate 1 --out $B/p-1x1-cc     > $B/p4.log 2>&1 &
wait
echo "plates done"
