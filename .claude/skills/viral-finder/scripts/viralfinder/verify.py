"""Timestamp verification against the ORIGINAL footage, only for shortlisted moments.

For each shortlisted candidate:
  1. bounds check     - start/end inside the real video duration
  2. footage fetch    - local file: read directly. Remote: download ONLY that section
                        (+/- a few seconds, <=480p) with yt-dlp --download-sections
  3. audio alignment  - cross-correlate the section's loudness envelope with the full
                        stream's envelope to PROVE the section matches the timestamp
                        (and measure any offset in seconds)
  4. contact sheet    - 12 frames with original-timeline timestamps burned in, plus a
                        hook frame. Claude looks at these images (cheap) instead of
                        sending the whole video to an expensive video model.
  5. transcript       - excerpt from captions; or local Whisper on this short section
Then reviews_todo.json is written for Claude/you to score each moment.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from . import audio as audio_mod
from . import transcript as tr
from .common import Project, fmt_ts, log
from .sources import AccessError, download_section, explain_failure
from .video import contact_sheet, extract_frame


def align(section_env: np.ndarray, full_env: np.ndarray, expected_start: float, frame_s: float,
          search_s: float) -> tuple[float, float]:
    """Return (offset_seconds_on_original_timeline, correlation)."""
    fps = 1.0 / frame_s
    n = len(section_env)
    if n < fps * 3:
        return expected_start, 0.0
    lo = int(max(0, (expected_start - search_s) * fps))
    hi = int(min(len(full_env) - n, (expected_start + search_s) * fps))
    if hi <= lo:
        return expected_start, 0.0
    section_env = np.maximum(section_env, -60.0)  # ignore digital silence
    full_env = np.maximum(full_env, -60.0)
    a = section_env.astype(np.float64)
    a = (a - a.mean()) / (a.std() + 1e-9)
    best, best_i = -2.0, lo
    for i in range(lo, hi + 1):
        b = full_env[i: i + n].astype(np.float64)
        b = (b - b.mean()) / (b.std() + 1e-9)
        c = float(np.dot(a, b) / n)
        if c > best:
            best, best_i = c, i
    return best_i / fps, best


def verify(proj: Project, cfg: dict, top_n: int | None = None, ids: list[str] | None = None,
           transcribe: bool = False) -> list[dict]:
    meta = proj.meta()
    vcfg = cfg["verify"]
    cands = proj.load("candidates.json", [])
    if not cands:
        raise RuntimeError("No candidates yet. Run 'scan' first.")
    top_n = top_n or vcfg["top_n"]
    pool = [c for c in cands if (not ids or c["id"] in ids)]
    shortlist = sorted(pool, key=lambda c: -c["signal_value"])[: top_n if not ids else len(pool)]
    dur = meta.get("duration") or 0
    npz = proj.root / "signals_audio.npz"
    if npz.exists():
        full = audio_mod.load(npz)
        full_env, frame_s = full["frame_db"], float(full["frame_s"])
    else:
        full_env, frame_s = None, cfg["analysis"]["frame_seconds"]
    cues = (proj.load("transcript.json", {}) or {}).get("cues", [])
    local_video = meta.get("video_path") or ""
    remote_url = meta.get("webpage_url") or meta.get("source_url") or ""
    cookies = meta.get("cookies_from_browser")
    extra = ["--cookies-from-browser", cookies] if cookies else []
    pad = vcfg["section_padding"]
    by_id = {c["id"]: c for c in cands}
    section_fail = None
    log(f"Verifying {len(shortlist)} shortlisted moments against the original footage ...")
    for i, c in enumerate(shortlist, 1):
        vdir = proj.root / "verification" / c["id"]
        vdir.mkdir(parents=True, exist_ok=True)
        fc = {"checks": [], "ok": False}
        in_bounds = 0 <= c["start"] < c["end"] <= (dur + 1 if dur else c["end"])
        fc["checks"].append({"check": "timestamps inside video duration", "ok": in_bounds,
                             "detail": f"{c['start_ts']}-{c['end_ts']} of {fmt_ts(dur)}"})
        video, label_offset = None, 0.0
        if local_video:
            video = local_video
            fc["checks"].append({"check": "footage source", "ok": True, "detail": "original local file (exact timeline)"})
            fc["alignment"] = {"offset_error_s": 0.0, "correlation": 1.0, "method": "same file"}
        elif remote_url and section_fail is None:
            s0, e0 = max(0, c["start"] - pad), c["end"] + pad
            out = proj.root / "sections" / f"{c['id']}.mp4"
            try:
                if not out.exists():
                    log(f"  [{i}/{len(shortlist)}] {c['id']} downloading section {fmt_ts(s0)}-{fmt_ts(e0)} ...")
                    out = download_section(remote_url, s0, e0, out, vcfg["max_height"], extra)
                if full_env is not None:
                    env = audio_mod.envelope(str(out), int(cfg["analysis"]["audio_sample_rate"]), frame_s)
                    off, corr = align(env, full_env, s0, frame_s, vcfg["alignment_search_seconds"])
                    ok = corr >= vcfg["min_alignment_correlation"]
                    fc["alignment"] = {"section_starts_at": fmt_ts(off), "offset_error_s": round(off - s0, 2),
                                       "correlation": round(corr, 3), "method": "audio envelope cross-correlation"}
                    fc["checks"].append({"check": "downloaded section matches stream audio at this timestamp", "ok": ok,
                                         "detail": f"correlation {corr:.2f}, offset {off - s0:+.1f}s"})
                else:
                    off = s0
                    fc["alignment"] = {"section_starts_at": fmt_ts(off), "method": "requested section (no full audio to align)"}
                    fc["checks"].append({"check": "section alignment", "ok": None,
                                         "detail": "no full-stream audio; timestamps rely on the platform's section download (+/-2 s)"})
                video, label_offset = str(out), off
            except AccessError as e:
                section_fail = str(e)
                fix = explain_failure(meta.get("source_kind", ""), str(e)).splitlines()[0].lstrip("- ")
                fc["checks"].append({"check": "footage section download", "ok": False, "detail": fix})
        if section_fail and not video:
            fc["checks"].append({"check": "visual verification", "ok": False,
                                 "detail": "skipped - footage download is blocked (see first moment for the fix)"})
        if video:
            ls, le = c["start"] - label_offset, c["end"] - label_offset
            sheet = contact_sheet(
                video, ls, le, vdir / "contact_sheet.jpg", n=vcfg["contact_sheet_frames"], label_offset=label_offset)
            hook = extract_frame(video, ls + 1.5, vdir / "hook_frame.jpg")
            peak = extract_frame(video, c["peak"] - label_offset, vdir / "peak_frame.jpg")
            fc["contact_sheet"] = str(sheet) if sheet else ""
            fc["hook_frame"] = str(hook) if hook else ""
            fc["peak_frame"] = str(peak) if peak else ""
            fc["checks"].append({"check": "frames extracted from original footage", "ok": bool(sheet),
                                 "detail": str(sheet) if sheet else "frame extraction failed"})
            if transcribe and tr.whisper_available() and not tr.excerpt(cues, c["start"], c["end"]):
                try:
                    wc = tr.transcribe_file(video, offset=label_offset)
                    c["transcript_excerpt"] = tr.excerpt(wc, c["start"], c["end"])
                    fc["checks"].append({"check": "local whisper transcript of this section", "ok": True, "detail": ""})
                except Exception as e:  # noqa: BLE001
                    fc["checks"].append({"check": "local whisper transcript", "ok": False, "detail": str(e)[:200]})
        fc["ok"] = bool(video) and all(ch["ok"] is not False for ch in fc["checks"])
        c["footage_check"] = fc
        by_id[c["id"]] = c
        log(f"  [{i}/{len(shortlist)}] {c['id']} {c['start_ts']}-{c['end_ts']}  footage_ok={fc['ok']}")
    proj.save("candidates.json", sorted(by_id.values(), key=lambda c: c["start"]))
    write_review_todo(proj, shortlist)
    return shortlist


def write_review_todo(proj: Project, shortlist: list[dict]) -> Path:
    existing = proj.load("reviews.json", {}) or {}
    todo = {}
    for c in sorted(shortlist, key=lambda c: -c["signal_value"]):
        if c["id"] in existing:
            continue
        fc = c.get("footage_check", {})
        todo[c["id"]] = {
            "_look_at": fc.get("contact_sheet", ""),
            "_hook_frame": fc.get("hook_frame", ""),
            "_time": f"{c['start_ts']} - {c['end_ts']} (peak {c['peak_ts']})",
            "_signals": c["reasons"],
            "_transcript": c.get("transcript_excerpt", ""),
            "scores": {"hook": None, "entertainment": None, "originality": None, "emotion": None, "retention": None,
                       "replay": None, "international": None, "visual_clarity": None, "context_free": None},
            "description": "", "why": "", "hook_text": "", "caption": "", "platform": "",
            "start_ts": c["start_ts"], "end_ts": c["end_ts"],
            "campaign_checks": {}, "reject": False, "reject_reason": "",
            "verified_by": "contact sheet + transcript",
        }
    return proj.save("reviews_todo.json", todo)
