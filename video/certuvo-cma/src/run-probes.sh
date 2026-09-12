#!/usr/bin/env bash
cd "$(dirname "$0")"
rm -f ../build/probe-*.txt
node probe.mjs 1920 1080 hd > ../build/probe-hd.txt 2>&1
node probe.mjs 1080 1920 pt > ../build/probe-pt.txt 2>&1
node probe.mjs 1080 1080 sq > ../build/probe-sq.txt 2>&1
node probe.mjs 3840 2160 4k > ../build/probe-4k.txt 2>&1
echo PROBES-DONE >> ../build/probe-4k.txt
