"""Discovery (find long streams/VODs for a creator or topic) and competition research
(are these moments already clipped and reposted?).

Uses yt-dlp search (no API key). When the network blocks it, SKILL.md tells Claude to
fall back to WebSearch, the vidIQ connector, or browser research - and to say so.
"""
from __future__ import annotations

import json
import re

from .common import fmt_duration, log, run, ytdlp_cmd
from .sources import AccessError, explain_failure


def _flat(query_url: str, limit: int, extra: list[str] | None = None) -> list[dict]:
    y = ytdlp_cmd()
    if not y:
        raise AccessError("yt-dlp is not installed. Install it with:  pip install -U yt-dlp")
    try:
        out = run(y + ["-J", "--flat-playlist", "--no-warnings", "--playlist-end", str(limit), *(extra or []), query_url],
                  timeout=240).stdout
    except RuntimeError as e:
        raise AccessError(f"Search failed.\n{e}\n\nWhat to do:\n{explain_failure('search', str(e))}") from None
    return (json.loads(out) or {}).get("entries") or []


def _row(e: dict, platform: str) -> dict:
    url = e.get("url") or e.get("webpage_url") or ""
    if platform == "youtube" and url and not url.startswith("http"):
        url = f"https://www.youtube.com/watch?v={url}"
    dur = e.get("duration") or 0
    return {"platform": platform, "title": e.get("title") or "", "url": url,
            "duration_s": float(dur), "duration": fmt_duration(dur) if dur else "unknown",
            "channel": e.get("channel") or e.get("uploader") or "", "views": e.get("view_count"),
            "upload_date": e.get("upload_date") or "", "live_status": e.get("live_status") or ""}


def discover(query: str, limit: int = 25, min_minutes: float = 30, twitch_channel: str | None = None,
             youtube_channels: list[str] | None = None, after: str | None = None,
             extra: list[str] | None = None) -> list[dict]:
    rows: list[dict] = []
    errors = []
    try:
        log(f"Searching YouTube: {query!r}")
        rows += [_row(e, "youtube") for e in _flat(f"ytsearch{limit}:{query}", limit, extra)]
        # long-stream biased search
        rows += [_row(e, "youtube") for e in _flat(f"ytsearch{limit}:{query} full stream", limit, extra)]
    except AccessError as e:
        errors.append(str(e))
    for ch in youtube_channels or []:
        try:
            log(f"Listing channel streams: {ch}")
            rows += [_row(e, "youtube") for e in _flat(ch.rstrip("/") + "/streams", limit, extra)]
        except AccessError as e:
            errors.append(str(e))
    if twitch_channel:
        try:
            log(f"Listing Twitch VODs: {twitch_channel}")
            rows += [_row(e, "twitch") for e in
                     _flat(f"https://www.twitch.tv/{twitch_channel}/videos?filter=archives&sort=time", limit, extra)]
        except AccessError as e:
            errors.append(str(e))
    seen, out = set(), []
    for r in rows:
        if not r["url"] or r["url"] in seen:
            continue
        seen.add(r["url"])
        if r["duration_s"] and r["duration_s"] < min_minutes * 60:
            continue
        if after and r["upload_date"] and r["upload_date"] < after.replace("-", ""):
            continue
        out.append(r)
    q = set(re.findall(r"[a-z0-9]+", query.lower()))
    for r in out:
        t = set(re.findall(r"[a-z0-9]+", r["title"].lower()))
        r["relevance"] = round(len(q & t) / max(len(q), 1), 2)
    out.sort(key=lambda r: (-r["relevance"], -(r["duration_s"] or 0)))
    if not out and errors:
        raise AccessError("\n\n".join(errors))
    return out


STOP = set("the a an and or to of in on at is it this that i you he she we they my your bro yo what oh no yes just like "
           "so but for with be are was were do don't im i'm it's its me us them him her gonna wanna got get".split())


def key_phrase(text: str, n: int = 5) -> str:
    words = [w for w in re.findall(r"[a-z0-9']+", (text or "").lower()) if w not in STOP and len(w) > 2]
    return " ".join(words[:n])


def competition(moments: list[dict], creator: str, topic: str, limit: int = 10,
                extra: list[str] | None = None) -> dict[str, dict]:
    """For each moment search for existing short clips using its key words.
    Result levels: none_found / few / many / unknown. NEVER proof of originality."""
    res = {}
    for m in moments:
        phrase = key_phrase(m.get("description") or m.get("transcript_excerpt") or "")
        if not phrase:
            res[m["id"]] = {"level": "unknown", "query": "", "matches": [], "note": "no text to search with"}
            continue
        q = f"{creator} {topic} {phrase}".strip()
        try:
            entries = _flat(f"ytsearch{limit}:{q}", limit, extra)
        except AccessError as e:
            res[m["id"]] = {"level": "unknown", "query": q, "matches": [], "note": str(e).splitlines()[0]}
            continue
        pw = set(phrase.split())
        matches = []
        for e in entries:
            r = _row(e, "youtube")
            tw = set(re.findall(r"[a-z0-9']+", r["title"].lower()))
            overlap = len(pw & tw) / max(len(pw), 1)
            short = 0 < r["duration_s"] <= 180
            if overlap >= 0.4 or (short and overlap >= 0.25):
                matches.append({"title": r["title"], "url": r["url"], "duration": r["duration"],
                                "views": r["views"], "overlap": round(overlap, 2)})
        level = "none_found" if not matches else ("few" if len(matches) <= 2 else "many")
        res[m["id"]] = {"level": level, "query": q, "matches": matches[:5],
                        "note": "YouTube search top results only - not proof of originality. Also check TikTok/X manually."}
        log(f"  {m['id']}: {level} ({len(matches)} similar)")
    return res
