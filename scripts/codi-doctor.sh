#!/usr/bin/env bash
set -euo pipefail

if ! command -v codi >/dev/null 2>&1; then
  echo "codi CLI not found on PATH"
  echo "Install the CoDi CLI, then rerun validation or rendering."
  exit 127
fi

codi --help >/dev/null
echo "codi CLI is available: $(command -v codi)"
