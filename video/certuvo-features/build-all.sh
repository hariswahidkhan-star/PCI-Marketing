#!/usr/bin/env bash
# Build all five treatments, one at a time. Serial on purpose: four concurrent
# Chromium renders on this box take the load average past 90.
set -euo pipefail
cd "$(dirname "$0")"
./_pipeline/build-one.sh v1 certuvo-v1-walkthrough
./_pipeline/build-one.sh v2 certuvo-v2-carddeck
./_pipeline/build-one.sh v3 certuvo-v3-onesession
./_pipeline/build-one.sh v4 certuvo-v4-griddive
./_pipeline/build-one.sh v5 certuvo-v5-kinetic
echo "ALL-FIVE-DONE"
ls -la v*/dist/*.mp4
