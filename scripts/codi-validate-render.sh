#!/usr/bin/env bash
set -euo pipefail

file="${1:?usage: codi-validate-render.sh <file.codi> [output.svg]}"
output="${2:-${file%.codi}.svg}"

codi validate "$file"
codi render "$file" --format svg -o "$output"
echo "$output"
