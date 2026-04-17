#!/bin/bash
# Setup script — requires Python 3.11 and ffmpeg

set -e

# manimgl does not support Python 3.13+; use 3.11
PYTHON=/opt/homebrew/bin/python3.11

if [ ! -f "$PYTHON" ]; then
  echo "Python 3.11 not found at $PYTHON"
  echo "Install with: brew install python@3.11"
  exit 1
fi

echo "Using $($PYTHON --version)"

$PYTHON -m venv .venv
source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt

echo ""
echo "Setup complete. Activate with: source .venv/bin/activate"
echo ""
echo "System dependencies (install if missing):"
echo "  brew install ffmpeg cairo pkg-config"
echo "  brew install --cask mactex-no-gui   # for LaTeX in animations + PDF build"
