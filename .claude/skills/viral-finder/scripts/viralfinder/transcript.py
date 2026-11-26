"""Transcript loading (YouTube json3 / VTT / SRT / Whisper) and cheap text signals.

Optional: transcribe ONLY shortlisted segments with faster-whisper (local, free) when a
platform transcript is missing. Whole-stream transcription is avoided on purpose.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import numpy as np

from .common import parse_ts

TAG_RE = re.compile(r"<[^>]+>")


def _clean(text: str) -> str:
    text = html.unescape(TAG_RE.sub("", text))
    return re.sub(r"\s+", " ", text).strip()


def parse_json3(path: str) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8", errors="ignore"))
    cues = []
    for ev in data.get("events", []):
        segs = ev.get("segs")
        if not segs:
            continue
        start = ev.get("tStartMs", 0) / 1000.0
        dur = ev.get("dDurationMs", 0) / 1000.0
        text = _clean("".join(s.get("utf8", "") for s in segs))
        if not text:
            continue
        cues.append({"start": start, "end": start + max(dur, 0.5), "text": text})
    return _dedupe(cues)


def parse_vtt_srt(path: str) -> list[dict]:
    raw = Path(path).read_text(encoding="utf-8", errors="ignore").replace("\r", "")
    blocks = re.split(r"\n\s*\n", raw)
    cues = []
    time_re = re.compile(r"(\d{1,2}:?\d{2}:\d{2}[.,]\d{1,3}|\d{1,2}:\d{2}[.,]\d{1,3})\s*-->\s*(\d{1,2}:?\d{2}:\d{2}[.,]\d{1,3}|\d{1,2}:\d{2}[.,]\d{1,3})")
    for b in blocks:
        lines = [l for l in b.split("\n") if l.strip()]
        for i, l in enumerate(lines):
            m = time_re.search(l)
            if m:
                start = parse_ts(m.group(1).replace(",", "."))
                end = parse_ts(m.group(2).replace(",", "."))
                text_lines = [_clean(t) for t in lines[i + 1:]]
                text_lines = [t for t in text_lines if t]
                if text_lines:
                    cues.append({"start": start, "end": end, "lines": text_lines})
                break
    # YouTube rolling auto-captions repeat the previous line; keep only new lines.
    out, last = [], ""
    for c in cues:
        for line in c["lines"]:
            if line != last:
                out.append({"start": c["start"], "end": c["end"], "text": line})
                last = line
    return _dedupe(out)


def _dedupe(cues: list[dict]) -> list[dict]:
    out = []
    for c in sorted(cues, key=lambda c: c["start"]):
        if out and c["text"] == out[-1]["text"] and c["start"] - out[-1]["end"] < 2:
            out[-1]["end"] = max(out[-1]["end"], c["end"])
            continue
        if c["end"] - c["start"] < 0.05:
            continue
        out.append(dict(c))
    # trim overlaps so per-second distribution is not double counted
    for a, b in zip(out, out[1:]):
        if a["end"] > b["start"]:
            a["end"] = max(a["start"] + 0.2, b["start"])
    return out


def load_transcript(files: list[str]) -> tuple[list[dict], str]:
    """Pick the best English transcript among downloaded files. Returns (cues, source_file)."""
    if not files:
        return [], ""
    def rank(f: str) -> tuple:
        n = f.lower()
        manual = 0 if ("-orig" not in n and ".en." in n and "auto" not in n) else 1
        fmt = 0 if n.endswith(".json3") else (1 if n.endswith(".vtt") else 2)
        return (manual, fmt)
    for f in sorted(files, key=rank):
        try:
            cues = parse_json3(f) if f.endswith(".json3") else parse_vtt_srt(f)
            if cues:
                return cues, f
        except Exception:  # noqa: BLE001
            continue
    return [], ""


def _count(text: str, phrases: list[str]) -> int:
    t = text.lower()
    n = 0
    for p in phrases:
        pat = r"(?<![a-z0-9'])" + re.escape(p.lower()) + r"(?![a-z0-9'])" if p[:1].isalnum() else re.escape(p.lower())
        n += len(re.findall(pat, t))
    return n


def text_signals(cues: list[dict], n_sec: int, lex: dict) -> dict:
    words = np.zeros(n_sec, np.float32)
    hype = np.zeros(n_sec, np.float32)
    laugh = np.zeros(n_sec, np.float32)
    bleep = np.zeros(n_sec, np.float32)
    for c in cues:
        a, b = int(c["start"]), int(min(max(c["end"], c["start"] + 1), n_sec))
        if a >= n_sec or b <= a:
            continue
        span = b - a
        text = c["text"]
        wc = len(re.findall(r"[A-Za-z0-9']+", text))
        excl = text.count("!")
        caps = len(re.findall(r"\b[A-Z]{3,}\b", text))
        words[a:b] += wc / span
        hype[a:b] += (_count(text, lex.get("hype", [])) + 0.5 * excl + 0.5 * caps + _repetition(text)) / span
        laugh[a:b] += _count(text, lex.get("laughter", [])) / span
        bleep[a:b] += _count(text, lex.get("bleep", [])) / span
    return {"transcript_hype": hype, "transcript_laughter": laugh, "transcript_bleeps": bleep, "speech_rate": words}


def _repetition(text: str) -> float:
    """'no no no no', 'what what what' -> excitement."""
    w = re.findall(r"[a-z']+", text.lower())
    if len(w) < 3:
        return 0.0
    reps = sum(1 for x, y in zip(w, w[1:]) if x == y)
    return min(reps, 4) * 0.5


def excerpt(cues: list[dict], start: float, end: float, max_chars: int = 600) -> str:
    parts = [c["text"] for c in cues if c["end"] > start and c["start"] < end]
    txt = " ".join(parts)
    return txt if len(txt) <= max_chars else txt[: max_chars - 3] + "..."


def snap_points(cues: list[dict]) -> np.ndarray:
    return np.array(sorted({round(c["start"], 2) for c in cues}), dtype=np.float32)


# --------------------------------------------------------------------------- optional whisper
def whisper_available() -> bool:
    try:
        import faster_whisper  # noqa: F401
        return True
    except ImportError:
        return False


def transcribe_file(path: str, offset: float = 0.0, model_size: str = "base.en") -> list[dict]:
    """Transcribe a SHORT file (a shortlisted section). Returns cues on the original timeline."""
    from faster_whisper import WhisperModel  # type: ignore
    model = WhisperModel(model_size, device="auto", compute_type="int8")
    segs, _ = model.transcribe(path, vad_filter=True)
    return [{"start": s.start + offset, "end": s.end + offset, "text": s.text.strip()} for s in segs]
