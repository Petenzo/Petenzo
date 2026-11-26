"""Chat replay parsing. Chat bursts are one of the strongest cheap viral signals:
viewers spam KEKW / LMAO / 'CLIP IT' seconds after something great happens.

Supported:
  * YouTube live chat replay (yt-dlp  *.live_chat.json, one JSON per line)
  * TwitchDownloaderCLI chat JSON  ({"comments": [{"content_offset_seconds", "message": {"body"}}]})
  * chat-downloader JSON list       ([{"time_in_seconds", "message"}])
  * CSV / TXT lines                 "seconds,message"  or  "HH:MM:SS message"
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import numpy as np

from .common import parse_ts


def _yt_line(obj: dict) -> tuple[float, str] | None:
    r = obj.get("replayChatItemAction") or {}
    off = r.get("videoOffsetTimeMsec")
    if off is None:
        return None
    for act in r.get("actions", []):
        item = (act.get("addChatItemAction") or {}).get("item") or {}
        rend = item.get("liveChatTextMessageRenderer") or item.get("liveChatPaidMessageRenderer")
        if not rend:
            continue
        parts = []
        for run in (rend.get("message") or {}).get("runs", []):
            if "text" in run:
                parts.append(run["text"])
            elif "emoji" in run:
                sc = (run["emoji"].get("shortcuts") or [""])[0]
                parts.append(run["emoji"].get("emojiId", "") if len(run["emoji"].get("emojiId", "")) <= 2 else sc)
        return int(off) / 1000.0, " ".join(parts)
    return None


def parse_chat_file(path: str) -> list[tuple[float, str]]:
    p = Path(path)
    raw = p.read_text(encoding="utf-8", errors="ignore")
    msgs: list[tuple[float, str]] = []
    stripped = raw.lstrip()
    if p.suffix.lower() in (".json", ".jsonl") or stripped[:1] in "{[":
        # whole-document JSON?
        try:
            data = json.loads(raw)
            if isinstance(data, dict) and "comments" in data:
                for c in data["comments"]:
                    body = (c.get("message") or {}).get("body") or ""
                    msgs.append((float(c.get("content_offset_seconds", 0)), body))
                return msgs
            if isinstance(data, list):
                for c in data:
                    t = c.get("time_in_seconds", c.get("content_offset_seconds", c.get("offset")))
                    m = c.get("message", c.get("text", ""))
                    if isinstance(m, dict):
                        m = m.get("body", "")
                    if t is not None:
                        msgs.append((float(t), str(m)))
                return msgs
        except json.JSONDecodeError:
            pass
        for line in raw.splitlines():  # JSON lines (YouTube live_chat)
            line = line.strip()
            if not line:
                continue
            try:
                r = _yt_line(json.loads(line))
            except json.JSONDecodeError:
                continue
            if r:
                msgs.append(r)
        return msgs
    # CSV / TXT
    for row in csv.reader(raw.splitlines()):
        if not row:
            continue
        if len(row) >= 2:
            try:
                msgs.append((parse_ts(row[0]), ",".join(row[1:])))
                continue
            except ValueError:
                pass
        m = re.match(r"\[?(\d{1,2}:\d{2}(?::\d{2})?)\]?\s+(.*)", ",".join(row))
        if m:
            msgs.append((parse_ts(m.group(1)), m.group(2)))
    return msgs


def chat_signals(files: list[str], n_sec: int, lex: dict, lag: float) -> tuple[dict, dict]:
    msgs: list[tuple[float, str]] = []
    for f in files:
        try:
            msgs.extend(parse_chat_file(f))
        except Exception:  # noqa: BLE001
            continue
    if not msgs:
        return {}, {"messages": 0}
    rate = np.zeros(n_sec, np.float32)
    hype = np.zeros(n_sec, np.float32)
    terms = [t.lower() for t in lex.get("chat_hype", [])]
    pats = [re.compile(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])") if t[:1].isalnum() else re.compile(re.escape(t)) for t in terms]
    top_by_sec: dict[int, list[str]] = {}
    for t, text in msgs:
        s = int(t - lag)  # viewers react a few seconds AFTER the moment
        if s < 0 or s >= n_sec:
            continue
        rate[s] += 1
        low = text.lower()
        h = sum(1 for p in pats if p.search(low))
        if h:
            hype[s] += h
            top_by_sec.setdefault(s, []).append(text[:40])
    stats = {"messages": len(msgs), "files": files, "lag_seconds": lag,
             "_samples": {k: v[:5] for k, v in top_by_sec.items()}}
    return {"chat_rate": rate, "chat_hype": hype}, stats
