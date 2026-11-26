"""Viral ranking rubric (0-100) and campaign rules.

Two layers, kept separate and labelled honestly in the report:
  1. signal estimate  - from the cheap scan only (audio/chat/transcript). Unknown
                        criteria sit at a neutral 50, so un-reviewed moments rarely
                        reach the recommendation threshold. That is intentional.
  2. reviewed score   - Claude (or you) looked at the contact sheet + transcript of the
                        shortlisted moment and scored each criterion 1-10 in reviews.json.
Only moments that are footage-checked AND reviewed AND not rejected are 'recommended'.
"""
from __future__ import annotations

import re
from pathlib import Path

from .common import CONFIG_DIR, fmt_ts, parse_ts, read_json

CRITERIA = {
    "hook": "First 3 seconds grab attention",
    "entertainment": "How entertaining / funny / exciting",
    "originality": "Not already heavily reposted",
    "emotion": "Strength of the emotional reaction",
    "retention": "Keeps people watching to the end",
    "replay": "People will rewatch / loop it",
    "international": "Works for a global English-speaking audience",
    "visual_clarity": "Easy to read visually, works in 9:16",
    "context_free": "Understandable without knowing the stream",
}

ORIGINALITY_FROM_COMPETITION = {"none_found": 70, "few": 50, "many": 20, "unknown": 50}


def _clip(v, lo=0, hi=100):
    return max(lo, min(hi, v))


def estimate(c: dict) -> dict:
    sv = max(c.get("signal_value", 0.0), 1e-6)
    b = c.get("signal_breakdown", {})
    emo = max([b.get(k, 0) for k in ("laughter", "shout", "audio_loudness", "transcript_laughter", "chat_hype")] or [0])
    comp = (c.get("competition") or {}).get("level", "unknown")
    return {
        "hook": _clip(35 + 50 * min(c.get("hook_strength", 0) / sv, 1.0)),
        "entertainment": _clip(c.get("signal_score", 50)),
        "originality": ORIGINALITY_FROM_COMPETITION.get(comp, 50),
        "emotion": _clip(40 + 8 * emo, 0, 90),
        "retention": _clip(40 + 50 * c.get("sustain", 0)),
        "replay": _clip(40 + 8 * c.get("sharpness", 0), 0, 90),
        "international": 50,
        "visual_clarity": 50,
        "context_free": 50,
    }


def score(values: dict, weights: dict) -> float:
    tot = sum(weights.values())
    return round(sum(weights[k] * values.get(k, 50) for k in weights) / tot, 1)


def tier(s: float, tiers: dict) -> str:
    for name in ("S", "A", "B"):
        if s >= tiers[name]:
            return name
    return "C"


def apply_review(c: dict, review: dict | None, cfg: dict) -> dict:
    """Merge the auto estimate with a human/Claude review and compute the final score."""
    est = estimate(c)
    c = dict(c)
    c["estimate"] = est
    c["signal_estimate_score"] = score(est, cfg["rubric_weights"])
    if review:
        vals = dict(est)
        for k, v in (review.get("scores") or {}).items():
            if k in CRITERIA and v is not None:
                v = float(v)
                vals[k] = v * 10 if v <= 10 else v  # accept 1-10 or 0-100
        c["criteria"] = vals
        c["viral_score"] = score(vals, cfg["rubric_weights"])
        c["reviewed"] = bool(review.get("scores"))
        for k in ("description", "why", "hook_text", "caption", "platform", "notes", "title_idea",
                  "campaign_checks", "reject", "reject_reason", "verified_by"):
            if k in review:
                c[k] = review[k]
        if review.get("start_ts") or review.get("end_ts"):
            s = parse_ts(review.get("start_ts", c["start"]))
            e = parse_ts(review.get("end_ts", c["end"]))
            if e > s:
                c["start"], c["end"] = s, e
                c["start_ts"], c["end_ts"], c["duration"] = fmt_ts(s), fmt_ts(e), e - s
                c["boundaries_adjusted_by_review"] = True
    else:
        c["criteria"] = est
        c["viral_score"] = c["signal_estimate_score"]
        c["reviewed"] = False
    c["tier"] = tier(c["viral_score"], cfg["tiers"])
    fc = c.get("footage_check") or {}
    c["footage_verified"] = bool(fc.get("ok"))
    c["recommended"] = bool(c["reviewed"] and c["footage_verified"] and not c.get("reject")
                            and c["viral_score"] >= cfg["report"]["min_recommend_score"]
                            and campaign_ok(c))
    return c


def campaign_ok(c: dict) -> bool:
    checks = c.get("campaign_checks") or {}
    return all(v is not False for v in checks.values())


# --------------------------------------------------------------------------- campaigns
def list_campaigns() -> list[dict]:
    out = []
    for f in sorted((CONFIG_DIR / "campaigns").glob("*.json")):
        if f.name.startswith("_"):
            continue
        d = read_json(f, {})
        d["_file"] = str(f)
        out.append(d)
    return out


def match_campaign(text: str, explicit: str | None = None) -> dict | None:
    camps = list_campaigns()
    if explicit:
        if explicit.lower() in ("none", "no", "off"):
            return None
        for c in camps:
            if c["id"] == explicit or Path(c["_file"]).stem == explicit:
                return c
        p = Path(explicit)
        if p.exists():
            return read_json(p, None)
        raise ValueError(f"Campaign '{explicit}' not found in {CONFIG_DIR / 'campaigns'}")
    low = (text or "").lower()
    for c in camps:
        groups = c.get("match_requires_all_groups") or [c.get("match_keywords", [])]
        if all(any(k in low for k in g) for g in groups if g):
            return c
    return None


def eligibility(meta: dict, camp: dict | None) -> list[dict]:
    if not camp:
        return []
    res = []
    el = camp.get("eligibility") or {}
    d_from = (el.get("footage_date_from") or "").replace("-", "")
    up = meta.get("release_date") or meta.get("upload_date") or ""
    if d_from:
        if up:
            ok = up >= d_from
            res.append({"check": f"Footage date on/after {el['footage_date_from']}", "ok": ok,
                        "detail": f"source date {up[:4]}-{up[4:6]}-{up[6:]}" + ("" if ok else " - TOO EARLY, likely not eligible")})
        else:
            res.append({"check": f"Footage date on/after {el['footage_date_from']}", "ok": None,
                        "detail": "date unknown - confirm manually"})
    words = el.get("title_should_contain_any") or []
    if words:
        t = (meta.get("title", "") + " " + meta.get("description", "")).lower()
        ok = any(w in t for w in words)
        res.append({"check": "Title/description mentions the campaign game/topic", "ok": ok if ok else None,
                    "detail": "found" if ok else "not found in title - verify visually that the footage is the right game"})
    return res


def fix_caption(caption: str, camp: dict | None) -> tuple[str, list[str]]:
    """Make sure required mentions/hashtags are present. Returns (caption, notes)."""
    if not camp:
        return caption, []
    notes = []
    rules = camp.get("caption_rules") or {}
    cap = caption or ""
    for m in rules.get("must_mention", []):
        if m.lower() not in cap.lower():
            cap = f"{m} {cap}".strip()
            notes.append(f"added '{m}'")
    for h in rules.get("required_hashtags", []):
        if not re.search(re.escape(h) + r"\b", cap, re.I):
            cap = f"{cap} {h}".strip()
            notes.append(f"added {h}")
    return cap, notes
