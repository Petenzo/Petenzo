# Viral Finder installer (Windows PowerShell).
#   powershell -ExecutionPolicy Bypass -File install.ps1           -> install packages
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Global   -> also copy to %USERPROFILE%\.claude\skills
param([switch]$Global)
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "== Python packages =="
python -m pip install --upgrade -r "$here\requirements.txt"
Write-Host "== FFmpeg =="
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
  winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
  Write-Host "Close and reopen the terminal so ffmpeg is on PATH."
} else { Write-Host "ffmpeg found" }
if ($Global) {
  $dest = Join-Path $env:USERPROFILE ".claude\skills\viral-finder"
  if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
  New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
  Copy-Item -Recurse $here $dest
  Write-Host "Copied to $dest"
}
python "$here\scripts\vf.py" doctor
Write-Host "Done. In Claude Code type:  /viral-finder <link do filmu>"
