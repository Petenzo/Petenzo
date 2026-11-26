"""Full-stream cheap scan: fuse audio + transcript + chat + scene signals into one
'excitement curve', then pick candidate moments with clean start/end points.

Every signal is normalised against THIS stream's own baseline (robust z-score), so a
naturally loud streamer is not flagged everywhere - only when louder than usual.
"""
from __future__ import annotations

import numpy as np

from . import audio as audio_mod
from . import chat as chat_mod
from . import transcript as tr
from .common import Project, fmt_ts, log


def robust_z(x: np.ndarray) -> np.ndarray:
    med = np.median(x)
    mad = np.median(np.abs(x - med)) * 1.4826
    if mad < 1e-6:
        sd = x.std()
        mad = sd if sd > 1e-6 else 1.0
    return np.clip((x - med) / mad, -3, 8)


def smooth(x: np.ndarray, w: int) -> np.ndarray:
    if w <= 1:
        return x
    k = np.ones(w, np.float32) / w
    return np.convolve(x, k, mode="same")


def rolling_baseline(x: np.ndarray, window_s: int) -> np.ndarray:
    """Median over a moving window (computed on 10 s blocks, then interpolated - fast for 10 h)."""
    blk = 10
    n = len(x)
    nb = max(1, n // blk)
    blocks = np.median(x[: nb * blk].reshape(nb, blk), axis=1)
    half = max(1, window_s // blk // 2)
    base = np.array([np.median(blocks[max(0, i - half): i + half + 1]) for i in range(nb)])
    return np.interp(np.arange(n), np.arange(nb) * blk + blk / 2, base).astype(np.float32)


def audio_derived(sec: dict, cfg: dict) -> dict:
    loud = sec["loud_db"]
    base = rolling_baseline(loud, int(cfg["analysis"]["baseline_minutes"] * 60))
    rel = loud - base
    prev = np.convolve(loud, np.ones(8) / 8, mode="full")[: len(loud)]  # mean of previous ~8 s
    prev = np.concatenate([np.full(2, loud[0]), prev[:-2]])
    surprise = np.maximum(loud - prev, 0)
    cz = robust_z(sec["centroid"])
    shout = np.maximum(rel, 0) * np.maximum(cz, 0)
    return {"audio_loudness": rel, "audio_surprise": surprise, "shout": shout, "laughter": sec["laughter"]}


def scan(proj: Project, cfg: dict, use_scenes: bool = False) -> dict:
    meta = proj.meta()
    a = cfg["analysis"]
    lex = cfg["lexicon"]
    npz = proj.path("signals_audio.npz")
    if meta.get("audio_path"):
        if npz.exists():
            log("  reusing previous audio analysis")
            sec = audio_mod.load(npz)
        else:
            log(f"Scanning audio of '{meta.get('title')}' ...")
            sec = audio_mod.analyze(meta["audio_path"], npz, a["audio_sample_rate"], a["frame_seconds"], meta.get("duration", 0))
        n = len(sec["loud_db"])
        signals = audio_derived(sec, cfg)
        used = ["audio"]
    else:  # transcript/chat-only project (footage could not be downloaded)
        n = int(meta.get("duration") or 0)
        if n <= 0:
            raise RuntimeError("No audio and no duration known - cannot scan.")
        log("  NO AUDIO: transcript/chat-only scan (weaker; moments cannot be footage-verified until audio/video is available)")
        sec = {"loud_db": np.zeros(n, np.float32)}
        signals, used = {}, []

    cues, tsrc = tr.load_transcript(meta.get("subtitle_files", []))
    if cues:
        signals.update(tr.text_signals(cues, n, lex))
        used.append("transcript")
        proj.save("transcript.json", {"source": tsrc, "cues": cues})
        log(f"  transcript: {len(cues)} lines from {tsrc.split('/')[-1]}")
    else:
        log("  transcript: none available (scan continues with audio/chat; shortlisted moments can be transcribed later)")

    chat_stats = {"messages": 0}
    if meta.get("chat_files"):
        cs, chat_stats = chat_mod.chat_signals(meta["chat_files"], n, lex, a["chat_lag_seconds"])
        if cs:
            signals.update(cs)
            used.append("chat")
            log(f"  chat: {chat_stats['messages']} messages")
    chat_samples = chat_stats.pop("_samples", {})

    if use_scenes and meta.get("video_path"):
        from .video import scene_signal
        signals["scene_cuts"] = scene_signal(meta["video_path"], n, a["scene_threshold"], meta.get("duration", 0))
        used.append("scenes")

    if not signals:
        raise RuntimeError("No usable signals (no audio, transcript or chat).")
    weights = cfg["signal_weights"]
    sm = int(a["smooth_seconds"])
    z = {k: smooth(np.maximum(robust_z(v.astype(np.float32)), 0), sm) for k, v in signals.items() if weights.get(k, 0) > 0}
    wsum = sum(weights[k] for k in z)
    fused = sum(weights[k] * z[k] for k in z) / max(wsum, 1e-6)
    # Bonus when several independent signal families agree
    fams = {"audio": ["audio_loudness", "audio_surprise", "shout", "laughter"],
            "text": ["transcript_hype", "transcript_laughter", "transcript_bleeps"],
            "chat": ["chat_rate", "chat_hype"]}
    agree = np.zeros(n, np.float32)
    for keys in fams.values():
        ks = [k for k in keys if k in z]
        if ks:
            agree += (np.max([z[k] for k in ks], axis=0) > 1.5).astype(np.float32)
    fused = fused * (1 + 0.25 * np.maximum(agree - 1, 0))

    cands = pick_candidates(fused, z, sec, cues, meta, cfg, chat_samples)
    np.savez_compressed(proj.path("signals_fused.npz"), fused=fused.astype(np.float32),
                        **{k: v.astype(np.float32) for k, v in z.items()})
    summary = {"duration": meta.get("duration") or n, "seconds_analysed": n, "signals_used": used,
               "chat": chat_stats, "transcript_lines": len(cues), "candidates": len(cands)}
    proj.save("scan_summary.json", summary)
    proj.save("candidates.json", cands)
    log(f"  found {len(cands)} candidate moments (signals used: {', '.join(used)})")
    return summary


def _local_maxima(x: np.ndarray, min_sep: int) -> list[int]:
    order = np.argsort(-x)
    taken = np.zeros(len(x), bool)
    peaks = []
    for i in order:
        if x[i] <= 0:
            break
        if taken[max(0, i - min_sep): i + min_sep + 1].any():
            continue
        peaks.append(int(i))
        taken[i] = True
    return peaks


def pick_candidates(fused, z, sec, cues, meta, cfg, chat_samples) -> list[dict]:
    a = cfg["analysis"]
    n = len(fused)
    hours = n / 3600
    k = int(min(a["max_candidates"], max(a["min_candidates"], hours * a["candidates_per_hour"])))
    peaks = _local_maxima(fused, int(a["peak_min_separation"]))
    min_v = float(a.get("min_signal_value", 1.0))
    chosen = [p for p in peaks[:k] if fused[p] >= min_v]
    snaps = tr.snap_points(cues) if cues else np.array([], np.float32)
    loud = sec["loud_db"]
    out = []
    for rank, p in enumerate(chosen, 1):
        start, end = _boundaries(p, fused, loud, snaps, a, n)
        reasons = _reasons(p, z, sec, cues, chat_samples, start, end)
        out.append({
            # ID = peak time (HHMMSS) so it stays the same if the scan is re-run
            "id": "m" + fmt_ts(p).replace(":", ""),
            "rank_signal": rank,
            "peak": float(p), "peak_ts": fmt_ts(p),
            "start": float(start), "end": float(end),
            "start_ts": fmt_ts(start), "end_ts": fmt_ts(end), "duration": float(end - start),
            "signal_value": round(float(fused[p]), 3),
            # fused value is in 'robust z' units above this stream's baseline: 2 -> ~49, 4 -> ~74, 7 -> ~90
            "signal_score": round(float(100 * (1 - np.exp(-fused[p] / 3.0))), 1),
            "signal_breakdown": {k2: round(float(v[p]), 2) for k2, v in z.items() if v[p] > 0.5},
            "hook_strength": round(float(np.mean(fused[int(start): int(start) + 3])), 3),
            "sustain": round(float(np.mean(fused[int(start): int(end)] > 1.0)), 3),
            "sharpness": round(float(fused[p] - np.median(fused[max(0, p - 60): p + 60])), 3),
            "reasons": reasons,
            "transcript_excerpt": tr.excerpt(cues, start, end) if cues else "",
            "status": "candidate",
        })
    out.sort(key=lambda c: c["start"])
    return out


def _boundaries(p: int, fused, loud, snaps, a, n) -> tuple[float, float]:
    pre, post = a["clip_pre_roll"], a["clip_post_roll"]
    # Extend start backwards while excitement is building (to capture the setup).
    s = p - pre
    thr = 0.5 * fused[p]
    j = p
    while j > p - a["clip_max"] * 0.6 and j > 0 and fused[j] > thr:
        j -= 1
    s = min(s, j - 8)
    e = p + post
    j = p
    while j < p + a["clip_max"] * 0.5 and j < n - 1 and fused[j] > thr:
        j += 1
    e = max(e, j + 4)
    # Snap to sentence starts / quiet points so clips do not begin mid-word.
    s = _snap(s, snaps, loud, -6, 3, prefer_quiet=True)
    e = _snap_end(e, loud, 0, 5)
    s = max(0.0, s)
    e = min(float(n), e)
    if e - s < a["clip_min"]:
        e = min(float(n), s + a["clip_min"])
    if e - s > a["clip_max"]:
        s = max(0.0, p - a["clip_max"] * 0.6)
        e = min(float(n), s + a["clip_max"])
    return round(s, 2), round(e, 2)


def _snap(t, snaps, loud, lo, hi, prefer_quiet=True):
    if len(snaps):
        near = snaps[(snaps >= t + lo) & (snaps <= t + hi)]
        if len(near):
            return float(near[np.argmin(np.abs(near - t))])
    a, b = int(max(0, t + lo)), int(max(1, t + hi))
    seg = loud[a:b]
    return float(a + int(np.argmin(seg))) if len(seg) else float(t)


def _snap_end(t, loud, lo, hi):
    a, b = int(max(0, t + lo)), int(min(len(loud), t + hi))
    seg = loud[a:b]
    return float(a + int(np.argmin(seg)) + 1) if len(seg) else float(t)


def _reasons(p, z, sec, cues, chat_samples, start, end) -> list[str]:
    r = []
    g = lambda k: float(z[k][p]) if k in z else 0.0  # noqa: E731
    if g("audio_loudness") > 2 or g("shout") > 2:
        r.append(f"Voice much louder than usual (shouting/screaming), z={max(g('audio_loudness'), g('shout')):.1f}")
    if g("audio_surprise") > 2:
        r.append("Sudden volume jump after a calmer part (surprise / reaction onset)")
    if g("laughter") > 2:
        r.append("Laughter-like rhythmic audio pattern (heuristic)")
    if g("transcript_hype") > 1.5:
        r.append("Excited words in transcript (e.g. 'no way', 'what', repeated words, CAPS)")
    if g("transcript_laughter") > 1.5:
        r.append("Laughter marked in captions")
    if g("transcript_bleeps") > 1.5:
        r.append("Burst of censored swearing in captions (strong reaction)")
    if g("chat_rate") > 2:
        r.append(f"Chat explodes: message rate z={g('chat_rate'):.1f}")
    if g("chat_hype") > 1.5:
        sample = []
        for s in range(int(start), int(end)):
            sample += chat_samples.get(s, [])
        sample = ", ".join(dict.fromkeys(sample[:6]))
        r.append(f"Chat spamming reaction emotes/words{(': ' + sample) if sample else ''}")
    if g("scene_cuts") > 1.5:
        r.append("Rapid visual changes on screen")
    return r or ["Above-baseline combined excitement (no single dominant signal)"]
