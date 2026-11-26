"""Identify a source (YouTube / Twitch / Google Drive / local file / URL / search topic),
read its metadata, and download ONLY what the cheap scan needs (audio + subtitles + chat).

Video is never downloaded in full unless the source is already a local file.
Short video sections are downloaded later, only for shortlisted moments (see verify.py).
"""
from __future__ import annotations

import glob
import json
import re
from pathlib import Path

from .common import Project, have, log, run, ytdlp_cmd, extract_youtube_id

VIDEO_EXT = {".mp4", ".mkv", ".mov", ".webm", ".avi", ".m4v", ".flv", ".ts", ".mpg", ".mpeg", ".wmv"}
AUDIO_EXT = {".m4a", ".mp3", ".wav", ".aac", ".opus", ".ogg", ".flac"}


class AccessError(RuntimeError):
    """Raised when a source cannot be reached. Message explains what the user must do."""


# --------------------------------------------------------------------------- detect
def detect_source(inp: str) -> dict:
    s = inp.strip().strip('"').strip("'")
    p = Path(s).expanduser()
    if p.exists():
        if p.is_dir():
            return {"kind": "local_dir", "path": str(p.resolve())}
        return {"kind": "local", "path": str(p.resolve())}
    low = s.lower()
    if re.match(r"^https?://", low) or low.startswith("www."):
        url = s if low.startswith("http") else "https://" + s
        if "youtube.com" in low or "youtu.be" in low:
            return {"kind": "youtube", "url": url, "id": extract_youtube_id(url)}
        if "twitch.tv" in low:
            m = re.search(r"/videos/(\d+)", url)
            kind = "twitch" if m else "twitch_channel"
            return {"kind": kind, "url": url, "id": m.group(1) if m else None}
        if "drive.google.com" in low or "docs.google.com" in low:
            return {"kind": "gdrive", "url": url, "id": gdrive_id(url)}
        if "kick.com" in low:
            return {"kind": "kick", "url": url}
        return {"kind": "url", "url": url}
    if re.search(r"\.(mp4|mkv|mov|webm|avi|m4v|ts)$", low):
        return {"kind": "missing_file", "path": s}
    return {"kind": "topic", "query": s}


def gdrive_id(url: str) -> str | None:
    for pat in [r"/file/d/([A-Za-z0-9_-]{10,})", r"[?&]id=([A-Za-z0-9_-]{10,})", r"/folders/([A-Za-z0-9_-]{10,})"]:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return None


# --------------------------------------------------------------------------- errors -> guidance
def explain_failure(kind: str, err: str) -> str:
    e = err.lower()
    tips = []
    if "403" in e and "proxy" in e or "tunnel connection failed" in e or "no rule or network setting allows" in e:
        tips.append("The network of THIS environment blocks the site (proxy 403). Run Claude Code on your own computer, "
                    "or allow the host (youtube.com, googlevideo.com, twitch.tv, ttvnw.net, drive.google.com) in the cloud environment's network settings. "
                    "Alternative: download the video yourself and give me the local file path.")
    if "sign in to confirm" in e or "not a bot" in e:
        tips.append("YouTube wants a signed-in browser. Run again with  --cookies-from-browser chrome  (or firefox/edge) "
                    "while you are logged in to YouTube in that browser on this computer.")
    if "private video" in e or "members-only" in e or "join this channel" in e:
        tips.append("The video is private or members-only. Only the owner/members can access it. Use a public VOD or a file you own.")
    if "subscriber-only" in e or "sub-only" in e or ("twitch" in kind and "403" in e):
        tips.append("Twitch VOD is subscriber-only or expired. Twitch deletes VODs after 7-60 days. Use the YouTube re-upload or a local copy.")
    if kind == "gdrive" and ("403" in e or "permission" in e or "cannot retrieve" in e or "access denied" in e or "login" in e):
        tips.append("Google Drive file is not shared publicly. In Drive: right-click the file > Share > General access > 'Anyone with the link' (Viewer). "
                    "Or download it to your computer and give me the local path. Or connect the Google Drive connector in Claude (Settings > Connectors).")
    if "too many requests" in e or "429" in e:
        tips.append("Rate limited (429). Wait 10-30 minutes, or use --cookies-from-browser.")
    if "unsupported url" in e:
        tips.append("yt-dlp does not support this website. Download the video manually and give me the local file path, "
                    "or open it in the browser so I can find a direct video link.")
    if "ffmpeg" in e and "not found" in e:
        tips.append("FFmpeg is missing. Install it: Windows 'winget install ffmpeg', macOS 'brew install ffmpeg', Linux 'sudo apt install ffmpeg'.")
    if not tips:
        tips.append("Unknown access error. Try: update yt-dlp (pip install -U yt-dlp), add --cookies-from-browser chrome, "
                    "or download the video manually and pass the local file path.")
    return "\n".join(f"- {t}" for t in tips)


# --------------------------------------------------------------------------- metadata
def probe_local(path: str) -> dict:
    out = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path]).stdout
    info = json.loads(out)
    fmt = info.get("format", {})
    streams = info.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), None)
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)
    tags = fmt.get("tags", {}) or {}
    return {
        "title": tags.get("title") or Path(path).stem,
        "duration": float(fmt.get("duration") or 0),
        "source_kind": "local",
        "local_path": path,
        "webpage_url": "",
        "has_video": v is not None,
        "has_audio": a is not None,
        "width": v.get("width") if v else None,
        "height": v.get("height") if v else None,
        "upload_date": (tags.get("creation_time") or "")[:10].replace("-", ""),
        "uploader": tags.get("artist") or "",
    }


def probe_remote(url: str, extra_args: list[str] | None = None) -> dict:
    y = ytdlp_cmd()
    if not y:
        raise AccessError("yt-dlp is not installed. Install it with:  pip install -U yt-dlp")
    try:
        out = run(y + ["-J", "--no-playlist", "--no-warnings", *(extra_args or []), url], timeout=180).stdout
    except RuntimeError as e:
        raise AccessError(str(e)) from None
    info = json.loads(out)
    subs = sorted((info.get("subtitles") or {}).keys())
    autos = sorted((info.get("automatic_captions") or {}).keys())
    return {
        "title": info.get("title") or "",
        "duration": float(info.get("duration") or 0),
        "webpage_url": info.get("webpage_url") or url,
        "id": info.get("id"),
        "extractor": info.get("extractor_key") or info.get("extractor"),
        "uploader": info.get("uploader") or info.get("channel") or "",
        "channel_url": info.get("channel_url") or info.get("uploader_url") or "",
        "upload_date": info.get("upload_date") or "",
        "release_date": info.get("release_date") or "",
        "view_count": info.get("view_count"),
        "is_live": info.get("is_live"),
        "was_live": info.get("was_live"),
        "live_status": info.get("live_status"),
        "subtitle_langs": subs,
        "auto_caption_langs": [a for a in autos if a.startswith("en")][:5],
        "has_live_chat": "live_chat" in subs or "rechat" in subs,
        "chapters": [{"start": c.get("start_time"), "end": c.get("end_time"), "title": c.get("title")}
                     for c in (info.get("chapters") or [])],
        "description": (info.get("description") or "")[:2000],
    }


# --------------------------------------------------------------------------- downloads
def download_audio(url: str, out_dir: Path, extra_args: list[str] | None = None) -> Path:
    """Audio only: ~30 MB per hour instead of 1-3 GB per hour of video."""
    y = ytdlp_cmd()
    tmpl = str(out_dir / "audio.%(ext)s")
    args = y + ["--no-playlist", "--no-warnings", "-f", "bestaudio[abr<=96]/bestaudio/worstaudio/worst",
                "-o", tmpl, "--no-part", "--concurrent-fragments", "8", *(extra_args or []), url]
    log("  downloading audio only (cheap) ...")
    try:
        run(args, capture=True)
    except RuntimeError as e:
        raise AccessError(str(e)) from None
    files = [f for f in glob.glob(str(out_dir / "audio.*")) if not f.endswith((".part", ".ytdl"))]
    if not files:
        raise AccessError("Audio download produced no file.")
    return Path(files[0])


def download_subs_and_chat(url: str, out_dir: Path, extra_args: list[str] | None = None, want_chat: bool = True) -> dict:
    """English subtitles/auto-captions + live chat replay (YouTube live_chat, Twitch rechat). Best effort."""
    y = ytdlp_cmd()
    res = {"subtitles": [], "chat": []}
    tmpl = str(out_dir / "subs.%(ext)s")
    base = y + ["--no-playlist", "--no-warnings", "--skip-download", "-o", tmpl, *(extra_args or [])]
    try:
        run(base + ["--write-subs", "--write-auto-subs", "--sub-langs", "en.*,en,-live_chat",
                    "--sub-format", "json3/vtt/srt/best", url], check=False, timeout=600)
    except Exception as e:  # noqa: BLE001
        log(f"  subtitles: {e}")
    if want_chat:
        try:
            log("  downloading chat replay (if available; can take a few minutes for long streams) ...")
            run(base + ["--write-subs", "--sub-langs", "live_chat,rechat", url], check=False, timeout=3600)
        except Exception as e:  # noqa: BLE001
            log(f"  chat: {e}")
    for f in sorted(glob.glob(str(out_dir / "subs.*"))):
        if "live_chat" in f or "rechat" in f:
            res["chat"].append(f)
        elif f.endswith((".vtt", ".srt", ".json3", ".json")):
            res["subtitles"].append(f)
    return res


def download_section(url: str, start: float, end: float, out_path: Path, max_height: int = 480,
                     extra_args: list[str] | None = None) -> Path:
    """Download just [start, end] seconds of a remote video at low resolution (for frame checks)."""
    y = ytdlp_cmd()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fmt = f"bv*[height<={max_height}]+ba/b[height<={max_height}]/worst"
    args = y + ["--no-playlist", "--no-warnings", "-f", fmt, "--download-sections", f"*{start:.0f}-{end:.0f}",
                "--merge-output-format", "mp4", "-o", str(out_path), "--no-part", *(extra_args or []), url]
    try:
        run(args, timeout=900)
    except RuntimeError as e:
        raise AccessError(str(e)) from None
    if not out_path.exists():
        cands = glob.glob(str(out_path.with_suffix("")) + "*")
        if cands:
            return Path(cands[0])
        raise AccessError("Section download produced no file.")
    return out_path


def extract_audio_local(video_path: str, out_dir: Path) -> Path:
    """For local files we do not copy audio - ffmpeg reads the original directly."""
    return Path(video_path)


def find_sidecar_files(video_path: str) -> dict:
    """Find .srt/.vtt/chat json next to a local video (same base name)."""
    p = Path(video_path)
    res = {"subtitles": [], "chat": []}
    for f in sorted(p.parent.glob(p.stem + "*")):
        n = f.name.lower()
        if f == p:
            continue
        if n.endswith((".srt", ".vtt", ".json3")):
            res["subtitles"].append(str(f))
        elif ("chat" in n and n.endswith((".json", ".jsonl", ".csv", ".txt"))):
            res["chat"].append(str(f))
    return res


# --------------------------------------------------------------------------- ingest
def ingest(inp: str, project_name: str | None, cfg: dict, cookies_from_browser: str | None = None,
           skip_chat: bool = False) -> Project:
    from .common import slugify
    src = detect_source(inp)
    kind = src["kind"]
    extra = ["--cookies-from-browser", cookies_from_browser] if cookies_from_browser else []

    if kind == "topic":
        raise AccessError(f"'{inp}' is a search topic, not a video. Use: vf.py discover \"{inp}\"")
    if kind == "missing_file":
        raise AccessError(f"File not found: {src['path']}. Check the path (drag the file into the terminal to paste its full path).")
    if kind == "local_dir":
        raise AccessError("That is a folder. Give me one video file, or run ingest once per file.")
    if kind == "twitch_channel":
        raise AccessError("That is a Twitch channel, not a VOD. Use: vf.py discover --twitch CHANNEL  to list VODs, then ingest one VOD URL.")

    if kind == "local":
        meta = probe_local(src["path"])
        if not meta["has_audio"]:
            raise AccessError("This file has no audio track - audio is required for the cheap scan.")
        proj = Project.open(project_name or slugify(meta["title"]), cfg, create=True)
        side = find_sidecar_files(src["path"])
        meta.update({"audio_path": src["path"], "video_path": src["path"] if meta["has_video"] else "",
                     "subtitle_files": side["subtitles"], "chat_files": side["chat"]})
        proj.save_meta(meta)
        log(f"Local file registered: {meta['title']} ({meta['duration']/3600:.2f} h)")
        return proj

    url = src["url"]
    try:
        meta = probe_remote(url, extra)
    except AccessError as e:
        raise AccessError(f"Could not read video info for {url}\n{e}\n\nWhat to do:\n{explain_failure(kind, str(e))}") from None
    if meta.get("is_live"):
        raise AccessError("This stream is LIVE right now. Wait until it ends and the VOD is available, then run again.")
    meta["source_kind"] = kind
    meta["source_url"] = url
    proj = Project.open(project_name or slugify(meta["title"] or src.get("id") or "video"), cfg, create=True)
    log(f"Source: {meta['title']}  |  {meta['duration']/3600:.2f} h  |  {meta['uploader']}  |  {meta['webpage_url']}")
    try:
        audio = download_audio(url, proj.media_dir, extra)
    except AccessError as e:
        proj.save_meta(meta)
        raise AccessError(f"Audio download failed.\n{e}\n\nWhat to do:\n{explain_failure(kind, str(e))}") from None
    side = download_subs_and_chat(url, proj.media_dir, extra, want_chat=not skip_chat)
    meta.update({"audio_path": str(audio), "video_path": "", "subtitle_files": side["subtitles"],
                 "chat_files": side["chat"], "cookies_from_browser": cookies_from_browser or ""})
    proj.save_meta(meta)
    log(f"  audio: {audio.name} | subtitles: {len(side['subtitles'])} | chat files: {len(side['chat'])}")
    return proj
