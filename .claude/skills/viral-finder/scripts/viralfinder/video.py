"""FFmpeg video helpers: scene-change detection, frame sampling, contact sheets.

All of these are cheap and local. Contact sheets let Claude *look* at a shortlisted
moment through ~12 frames instead of sending minutes of video to an AI video model.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import numpy as np

from .common import fmt_ts, log, run

PTS_RE = re.compile(r"pts_time:([0-9.]+)")


def scene_changes(video: str, start: float = 0.0, duration: float | None = None, threshold: float = 0.35,
                  fps: float = 2.0) -> list[float]:
    """Timestamps (seconds, original timeline) of hard cuts / big visual changes.
    Analyses a 160px-wide, 2 fps version - fast even for long files."""
    cmd = ["ffmpeg", "-nostdin", "-hide_banner"]
    if start:
        cmd += ["-ss", f"{start:.2f}"]
    if duration:
        cmd += ["-t", f"{duration:.2f}"]
    cmd += ["-i", video, "-an", "-vf", f"fps={fps},scale=160:-2,select='gt(scene,{threshold})',showinfo", "-f", "null", "-"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return [start + float(m.group(1)) for m in PTS_RE.finditer(p.stderr)]


def scene_signal(video: str, n_sec: int, threshold: float, duration: float) -> np.ndarray:
    log("  scene detection on local video (low-res, 2 fps) ...")
    cuts = scene_changes(video, threshold=threshold)
    sig = np.zeros(n_sec, np.float32)
    for c in cuts:
        i = int(c)
        if 0 <= i < n_sec:
            sig[i] += 1
    return sig


def extract_frame(video: str, t: float, out: Path, width: int = 640) -> Path | None:
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{max(t, 0):.2f}", "-i", video, "-frames:v", "1",
           "-vf", f"scale={width}:-2", "-q:v", "4", str(out)]
    subprocess.run(cmd, capture_output=True)
    return out if out.exists() else None


def contact_sheet(video: str, start: float, end: float, out: Path, n: int = 12, cols: int = 4,
                  width: int = 384, label_offset: float = 0.0) -> Path | None:
    """One image with n frames sampled evenly across [start, end], each stamped with its
    ORIGINAL-timeline timestamp (label_offset = where 'video' starts on the original timeline)."""
    out.parent.mkdir(parents=True, exist_ok=True)
    dur = max(end - start, 1.0)
    times = [start + dur * (i + 0.5) / n for i in range(n)]
    tmp_dir = out.parent / (out.stem + "_tiles")
    tmp_dir.mkdir(exist_ok=True)
    tiles = []
    for i, t in enumerate(times):
        f = tmp_dir / f"{i:02d}.jpg"
        label = fmt_ts(t + label_offset).replace(":", r"\:")
        cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{max(t, 0):.2f}", "-i", video, "-frames:v", "1",
               "-vf", f"scale={width}:-2,drawtext=text='{label}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6",
               "-q:v", "5", str(f)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if not f.exists():  # drawtext may be unavailable (no fontconfig) -> retry plain
            cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{max(t, 0):.2f}", "-i", video,
                   "-frames:v", "1", "-vf", f"scale={width}:-2", "-q:v", "5", str(f)]
            subprocess.run(cmd, capture_output=True)
        if f.exists():
            tiles.append(f)
    if not tiles:
        return None
    rows = (len(tiles) + cols - 1) // cols
    inputs = []
    for t in tiles:
        inputs += ["-i", str(t)]
    # pad missing tiles by repeating the last one
    while len(inputs) // 2 < rows * cols:
        inputs += ["-i", str(tiles[-1])]
    k = rows * cols
    lay = []
    for i in range(k):
        r, c = divmod(i, cols)
        x = "+".join(["w0"] * c) or "0"
        y = "+".join(["h0"] * r) or "0"
        lay.append(f"{x}_{y}")
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", *inputs, "-filter_complex",
           f"xstack=inputs={k}:layout={'|'.join(lay)}", "-q:v", "4", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    for t in tiles:
        t.unlink(missing_ok=True)
    try:
        tmp_dir.rmdir()
    except OSError:
        pass
    return out if out.exists() else None


def cut_clip(video: str, start: float, end: float, out: Path, vertical: bool = False) -> Path:
    """Optional: export a preview clip (re-encoded, frame accurate). 9:16 center crop if vertical."""
    vf = "crop=ih*9/16:ih,scale=1080:1920" if vertical else "scale=-2:720"
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{start:.2f}", "-i", video, "-t", f"{end - start:.2f}",
         "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-c:a", "aac", "-b:a", "128k", str(out)])
    return out
