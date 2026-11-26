#!/usr/bin/env bash
# Viral Finder installer (macOS / Linux).
#   bash install.sh            -> install Python packages, keep skill in this project
#   bash install.sh --global   -> also copy the skill to ~/.claude/skills (works in every folder)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
PY=python3; command -v python3 >/dev/null || PY=python
echo "== Python packages =="
$PY -m pip install --upgrade -r "$HERE/requirements.txt"
echo "== FFmpeg =="
if ! command -v ffmpeg >/dev/null; then
  if command -v brew >/dev/null; then brew install ffmpeg
  elif command -v apt-get >/dev/null; then sudo apt-get update && sudo apt-get install -y ffmpeg
  else echo "Please install FFmpeg manually: https://ffmpeg.org/download.html"; fi
else echo "ffmpeg found"; fi
if [ "$1" = "--global" ]; then
  mkdir -p "$HOME/.claude/skills"
  rm -rf "$HOME/.claude/skills/viral-finder"
  cp -R "$HERE" "$HOME/.claude/skills/viral-finder"
  echo "Copied to $HOME/.claude/skills/viral-finder"
fi
$PY "$HERE/scripts/vf.py" doctor || true
echo "Done. In Claude Code type:  /viral-finder <link do filmu>"
