"""Cheap full-length audio analysis with FFmpeg + numpy (no AI, no GPU).

FFmpeg decodes the audio to 16 kHz mono PCM and streams it; we never hold the
whole stream in memory. A 10-hour stream takes a few minutes on a laptop.

Per 50 ms frame we compute loudness (dB) and spectral centroid (brightness).
Per second we derive:
  loud_db      - 90th percentile loudness
  centroid     - brightness of voiced frames (shouting/screaming is brighter)
  laughter     - rhythmic 3-7 Hz energy bursts typical of laughter (heuristic)
  voiced       - fraction of frames above the silence floor
"""
from __future__ import annotations

import subprocess
import time
from pathlib import Path

import numpy as np

from .common import log


def decode_frames(path: str, sr: int = 16000, frame_s: float = 0.05, duration_hint: float = 0.0) -> dict:
    frame = int(sr * frame_s)
    chunk_frames = 1200  # 60 s per chunk
    chunk_bytes = frame * chunk_frames * 2
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    window = np.hanning(frame).astype(np.float32)
    freqs = np.fft.rfftfreq(frame, 1.0 / sr).astype(np.float32)
    dbs, cents = [], []
    leftover = b""
    t0 = time.time()
    done_s = 0.0
    last_report = 0.0
    assert proc.stdout is not None
    while True:
        buf = proc.stdout.read(chunk_bytes)
        if not buf:
            break
        buf = leftover + buf
        usable = (len(buf) // (frame * 2)) * frame * 2
        leftover = buf[usable:]
        if usable == 0:
            continue
        x = np.frombuffer(buf[:usable], dtype=np.int16).astype(np.float32) / 32768.0
        X = x.reshape(-1, frame)
        rms = np.sqrt(np.mean(X * X, axis=1) + 1e-12)
        dbs.append(20 * np.log10(rms + 1e-9))
        mag = np.abs(np.fft.rfft(X * window, axis=1))
        cents.append((mag @ freqs) / (mag.sum(axis=1) + 1e-9))
        done_s += X.shape[0] * frame_s
        if done_s - last_report >= 1800:
            last_report = done_s
            pct = f" ({100 * done_s / duration_hint:.0f}%)" if duration_hint else ""
            log(f"  audio scanned: {done_s / 3600:.2f} h{pct}  [{time.time() - t0:.0f}s elapsed]")
    proc.wait()
    if not dbs:
        err = proc.stderr.read().decode(errors="ignore") if proc.stderr else ""
        raise RuntimeError(f"FFmpeg could not decode audio from {path}. {err[-500:]}")
    return {"db": np.concatenate(dbs).astype(np.float32), "centroid": np.concatenate(cents).astype(np.float32),
            "frame_s": frame_s, "sr": sr}


def per_second(frames: dict) -> dict:
    db = frames["db"]
    cent = frames["centroid"]
    fps = int(round(1.0 / frames["frame_s"]))
    n_sec = len(db) // fps
    if n_sec == 0:
        raise RuntimeError("Audio is shorter than one second.")
    D = db[: n_sec * fps].reshape(n_sec, fps)
    C = cent[: n_sec * fps].reshape(n_sec, fps)
    silence_floor = max(np.percentile(db, 20) + 6.0, -60.0)
    voiced_mask = D > silence_floor
    voiced = voiced_mask.mean(axis=1)
    loud = np.percentile(D, 90, axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        centroid = np.where(voiced_mask.any(axis=1), (C * voiced_mask).sum(axis=1) / np.maximum(voiced_mask.sum(axis=1), 1), 0.0)

    # Laughter heuristic: 2-second envelope, energy share in 3-7 Hz modulation band.
    lin = np.power(10.0, db[: n_sec * fps] / 20.0)
    win = 2 * fps
    pad = np.pad(lin, (fps // 2 * 2, win), mode="edge")
    idx = (np.arange(n_sec) * fps)[:, None] + np.arange(win)[None, :]
    W = pad[idx]
    W = W - W.mean(axis=1, keepdims=True)
    spec = np.abs(np.fft.rfft(W * np.hanning(win), axis=1)) ** 2
    mod_f = np.fft.rfftfreq(win, 1.0 / fps)
    band = (mod_f >= 3.0) & (mod_f <= 7.0)
    total = spec[:, 1:].sum(axis=1) + 1e-12
    laughter = (spec[:, band].sum(axis=1) / total) * np.clip(voiced * 1.5, 0, 1)
    return {"loud_db": loud.astype(np.float32), "centroid": centroid.astype(np.float32),
            "laughter": laughter.astype(np.float32), "voiced": voiced.astype(np.float32)}


def analyze(path: str, out_npz: Path, sr: int = 16000, frame_s: float = 0.05, duration_hint: float = 0.0) -> dict:
    t0 = time.time()
    frames = decode_frames(path, sr, frame_s, duration_hint)
    sec = per_second(frames)
    np.savez_compressed(out_npz, frame_db=frames["db"], frame_s=frames["frame_s"], **sec)
    log(f"  audio analysis done: {len(sec['loud_db']) / 3600:.2f} h in {time.time() - t0:.0f}s")
    return sec


def envelope(path: str, sr: int = 16000, frame_s: float = 0.05) -> np.ndarray:
    """Loudness envelope (dB per frame) of any file - used to align downloaded sections."""
    return decode_frames(path, sr, frame_s)["db"]


def load(npz_path: Path) -> dict:
    z = np.load(npz_path)
    return {k: z[k] for k in z.files}
