#!/usr/bin/env bash
set -euo pipefail

if ! command -v codi >/dev/null 2>&1; then
  echo "codi CLI not found (not on PATH and not a shell alias/function)"
  echo "Do not fabricate SVG/PNG/validation output without it."
  echo "Make codi available on PATH or as an alias/function, then rerun validation or rendering."
  exit 127
fi

codi --help >/dev/null
echo "codi CLI is available: $(command -v codi)"
