#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 input.png [output.icns]"
  exit 1
fi

INPUT="$1"
BASENAME="${INPUT%.*}"
OUTPUT="${2:-$BASENAME.icns}"
ICONSET="${BASENAME}.iconset"

# Ensure iconutil is available
if ! command -v iconutil >/dev/null 2>&1; then
  echo "Error: 'iconutil' not found. Install Xcode or Xcode Command Line Tools."
  exit 1
fi

# Ensure ImageMagick is available
if ! command -v magick >/dev/null 2>&1 && ! command -v convert >/dev/null 2>&1; then
  echo "Error: ImageMagick not found (no 'magick' or 'convert' in PATH)."
  exit 1
fi

# Pick ImageMagick command name
if command -v magick >/dev/null 2>&1; then
  IM="magick"
else
  IM="convert"
fi

# Create the .iconset folder
rm -rf "$ICONSET"
mkdir "$ICONSET"

# Generate all required sizes
# @1x sizes
$IM "$INPUT" -resize 16x16   "$ICONSET/icon_16x16.png"
$IM "$INPUT" -resize 32x32   "$ICONSET/icon_16x16@2x.png"
$IM "$INPUT" -resize 32x32   "$ICONSET/icon_32x32.png"
$IM "$INPUT" -resize 64x64   "$ICONSET/icon_32x32@2x.png"
$IM "$INPUT" -resize 128x128 "$ICONSET/icon_128x128.png"
$IM "$INPUT" -resize 256x256 "$ICONSET/icon_128x128@2x.png"
$IM "$INPUT" -resize 256x256 "$ICONSET/icon_256x256.png"
$IM "$INPUT" -resize 512x512 "$ICONSET/icon_256x256@2x.png"
$IM "$INPUT" -resize 512x512 "$ICONSET/icon_512x512.png"
$IM "$INPUT" -resize 1024x1024 "$ICONSET/icon_512x512@2x.png"

# Build the .icns
iconutil -c icns "$ICONSET" -o "$OUTPUT"

echo "Created $OUTPUT (and intermediate $ICONSET folder)"
