#!/bin/bash
# Build script for mdvupy macOS application

set -e

echo "Building mdvupy for macOS..."

# Ensure we're in the project root
cd "$(dirname "$0")"

# Install PyInstaller if not present
echo "Installing PyInstaller..."
uv pip install pyinstaller

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build the app
echo "Building application bundle..."
uv run pyinstaller mdvupy-macos.spec

echo ""
echo "Build complete!"
echo "Application bundle: dist/mdvupy.app"
echo ""
echo "To test the app:"
echo "  open dist/mdvupy.app"
echo ""
echo "To test file association:"
echo "  open -a dist/mdvupy.app test.md"
echo ""
echo "To install (copy to Applications):"
echo "  cp -r dist/mdvupy.app /Applications/"
echo ""
