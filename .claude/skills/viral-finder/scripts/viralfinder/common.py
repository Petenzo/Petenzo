"""Shared helpers: time formatting, config, project workspace, subprocess, JSON."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = SKILL_DIR / "config"


# --------------------------------------------------------------------------- time
def fmt_ts(seconds: float) -> str:
    """Seconds -> HH:MM:SS (rounded down to whole seconds)."""
    s = max(0, int(seconds))
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"


def parse_ts(value: Any) -> float:
    """Accepts 3725, "3725", "01:02:05", "62:05", "1h2m5s", "1:02:05.500"."""
    if isinstance(value, (int, float)):
        return float(value)
    v = str(value).strip().lower()
    if re.fullmatch(r"\d+(\.\d+)?", v):
        return float(v)
    m = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+(?:\.\d+)?)s)?", v)
    if m and any(m.groups()):
        h, mi, s = m.groups()
        return int(h or 0) * 3600 + int(mi or 0) * 60 + float(s or 0)
    parts = v.split(":")
    if 2 <= len(parts) <= 3:
        parts = [float(p) for p in parts]
        while len(parts) < 3:
            parts.insert(0, 0.0)
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    raise ValueError(f"Cannot parse timestamp: {value!r}")


def fmt_duration(seconds: float) -> str:
    s = int(round(seconds))
    if s < 60:
        return f"{s}s"
    if s < 3600:
        return f"{s // 60}m {s % 60:02d}s"
    return f"{s // 3600}h {(s % 3600) // 60:02d}m"


def timestamp_url(url: str, seconds: float, kind: str = "") -> str:
    """Deep link to a moment in the original source when the platform supports it."""
    if not url:
        return ""
    s = int(seconds)
    if kind == "youtube" or "youtube.com" in url or "youtu.be" in url:
        vid = extract_youtube_id(url)
        if vid:
            return f"https://www.youtube.com/watch?v={vid}&t={s}s"
    if kind == "twitch" or "twitch.tv" in url:
        base = url.split("?")[0]
        return f"{base}?t={s // 3600}h{(s % 3600) // 60}m{s % 60}s"
    return url


def extract_youtube_id(url: str) -> str | None:
    m = re.search(r"(?:v=|youtu\.be/|/live/|/shorts/|/embed/)([A-Za-z0-9_-]{11})", url)
    return m.group(1) if m else None


# --------------------------------------------------------------------------- io
def read_json(path: Path, default: Any = None) -> Any:
    path = Path(path)
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    tmp.replace(path)
    return path


def deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(extra_path: str | None = None) -> dict:
    cfg = read_json(CONFIG_DIR / "config.json", {})
    user_cfg = Path.cwd() / "viral-finder.config.json"
    for p in [user_cfg, Path(extra_path) if extra_path else None]:
        if p and p.exists():
            cfg = deep_merge(cfg, read_json(p, {}))
    return cfg


PROFILE_WORDS = {
    "podcast": ["podcast", "interview", "episode", "ep.", "talk", "q&a", "trading", "trader", "stocks", "crypto",
                "watch", "watches", "rolex", "business", "money", "finance", "lesson", "explained", "story", "advice"],
    "entertainment": ["challenge", "survive", "vs", "last to", "$", "won", "win", "prank", "vlog", "i tried", "spent"],
}


def detect_profile(meta: dict) -> str:
    if meta.get("chat_files") or meta.get("was_live") or meta.get("live_status") == "was_live":
        return "stream"
    t = f"{meta.get('title', '')} {meta.get('description', '')[:300]}".lower()
    scores = {p: sum(1 for w in ws if w in t) for p, ws in PROFILE_WORDS.items()}
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "stream" if any(w in t for w in ["stream", "live", "gameplay", "playing"]) else "general"
    return best


def apply_profile(cfg: dict, profile: str) -> dict:
    prof = (cfg.get("profiles") or {}).get(profile) or {}
    prof = {k: v for k, v in prof.items() if k not in ("description", "_comment")}
    out = deep_merge(cfg, prof)
    out["active_profile"] = profile
    return out


def slugify(text: str, max_len: int = 60) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", text or "").strip("-").lower()
    return (s[:max_len].strip("-")) or "video"


# --------------------------------------------------------------------------- process
def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def run(cmd: list[str], check: bool = True, capture: bool = True, timeout: int | None = None) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, check=check, capture_output=capture, text=True, timeout=timeout)
    except subprocess.CalledProcessError as e:
        msg = (e.stderr or e.stdout or "").strip().splitlines()[-8:]
        raise RuntimeError(f"Command failed: {' '.join(cmd[:3])} ...\n" + "\n".join(msg)) from None


def ytdlp_cmd() -> list[str]:
    if have("yt-dlp"):
        return ["yt-dlp"]
    try:
        import yt_dlp  # noqa: F401
        return [sys.executable, "-m", "yt_dlp"]
    except ImportError:
        return []


def log(msg: str) -> None:
    print(msg, flush=True)


# --------------------------------------------------------------------------- project
class Project:
    """A folder holding everything about ONE video: metadata, signals, candidates, reviews."""

    def __init__(self, root: Path):
        self.root = Path(root)

    @classmethod
    def open(cls, name_or_path: str, cfg: dict | None = None, create: bool = False) -> "Project":
        p = Path(name_or_path)
        if not (p.is_absolute() or p.exists()):
            out_root = Path(os.environ.get("VF_OUTPUT") or (cfg or load_config()).get("output_root", "viral-finder-output"))
            p = out_root / name_or_path
        if not p.exists():
            if not create:
                raise FileNotFoundError(f"Project not found: {p}. Run 'ingest' first.")
            p.mkdir(parents=True, exist_ok=True)
            (p / ".gitignore").write_text("media/\nsections/\nframes/\n*.npz\n", encoding="utf-8")
        return cls(p)

    # paths -----------------------------------------------------------------
    @property
    def name(self) -> str:
        return self.root.name

    def path(self, *parts: str) -> Path:
        q = self.root.joinpath(*parts)
        q.parent.mkdir(parents=True, exist_ok=True)
        return q

    @property
    def media_dir(self) -> Path:
        d = self.root / "media"
        d.mkdir(exist_ok=True)
        return d

    def meta(self) -> dict:
        return read_json(self.root / "metadata.json", {})

    def save_meta(self, meta: dict) -> None:
        write_json(self.root / "metadata.json", meta)

    def load(self, name: str, default: Any = None) -> Any:
        return read_json(self.root / name, default)

    def save(self, name: str, data: Any) -> Path:
        return write_json(self.root / name, data)
