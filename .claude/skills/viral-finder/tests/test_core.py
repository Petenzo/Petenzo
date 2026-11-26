"""Unit tests: python -m pytest tests  (run from the skill folder)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from viralfinder import assemble, ranking, transcript, verify  # noqa: E402
from viralfinder.common import fmt_ts, load_config, parse_ts, timestamp_url  # noqa: E402
from viralfinder.sources import detect_source  # noqa: E402

CFG = load_config()


def test_timestamps():
    assert fmt_ts(3725.9) == "01:02:05"
    for v in ["01:02:05", "1h2m5s", "3725", 3725, "62:05"]:
        assert parse_ts(v) == 3725
    assert timestamp_url("https://youtu.be/abcdefghijk", 75) == "https://www.youtube.com/watch?v=abcdefghijk&t=75s"
    assert timestamp_url("https://www.twitch.tv/videos/123", 3725) == "https://www.twitch.tv/videos/123?t=1h2m5s"


def test_detect_source():
    assert detect_source("https://www.youtube.com/watch?v=abcdefghijk")["kind"] == "youtube"
    assert detect_source("https://www.twitch.tv/videos/2233445566")["kind"] == "twitch"
    assert detect_source("https://www.twitch.tv/somechannel")["kind"] == "twitch_channel"
    d = detect_source("https://drive.google.com/file/d/1AbCdEfGhIjKlMnOp/view?usp=sharing")
    assert d["kind"] == "gdrive" and d["id"] == "1AbCdEfGhIjKlMnOp"
    assert detect_source("MrBeast newest video")["kind"] == "topic"
    assert detect_source("missing_video.mp4")["kind"] == "missing_file"


def test_alignment_real_vs_wrong():
    rng = np.random.default_rng(0)
    full = np.cumsum(rng.standard_normal(20 * 3600)).astype(np.float32) * 0.3 - 30  # 1 h, 20 fps, non-periodic
    true_start = 1234.5
    i = int(true_start * 20)
    section = full[i:i + 20 * 40] + rng.standard_normal(800) * 0.5
    off, corr = verify.align(section, full, 1230, 0.05, 15)
    assert abs(off - true_start) < 0.1 and corr > 0.9
    wrong = full[int(2500 * 20):int(2500 * 20) + 800]
    off2, corr2 = verify.align(wrong, full, 1230, 0.05, 15)
    assert corr2 < CFG["verify"]["min_alignment_correlation"]


def test_vtt_rolling_dedupe(tmp_path):
    f = tmp_path / "x.en.vtt"
    f.write_text("WEBVTT\n\n00:00:01.000 --> 00:00:03.000\nhello chat\n\n"
                 "00:00:03.000 --> 00:00:05.000\nhello chat\nno way bro\n\n"
                 "00:00:05.000 --> 00:00:07.000\nno way bro\nwhat the [ __ ]\n", encoding="utf-8")
    cues = transcript.parse_vtt_srt(str(f))
    assert [c["text"] for c in cues] == ["hello chat", "no way bro", "what the [ __ ]"]
    sig = transcript.text_signals(cues, 10, CFG["lexicon"])
    assert sig["transcript_hype"][3] > 0 and sig["transcript_bleeps"][5] > 0


def test_no_campaign_by_default_and_optional_rules():
    assert ranking.match_campaign("MrBeast challenge video") is None
    assert ranking.match_campaign("trading podcast episode 12") is None
    camp = {"caption_rules": {"must_mention": ["Creator"], "required_hashtags": ["#TAG"]},
            "eligibility": {"footage_date_from": "2026-11-18"}}
    cap, notes = ranking.fix_caption("he got chased by the cops", camp)
    assert "Creator" in cap and "#TAG" in cap
    assert ranking.fix_caption("plain", None) == ("plain", [])
    assert ranking.eligibility({"upload_date": "20261110"}, camp)[0]["ok"] is False


def test_profiles():
    from viralfinder.common import apply_profile, detect_profile
    assert detect_profile({"title": "Rolex vs Omega - which watch to buy? | Podcast ep. 41"}) == "podcast"
    assert detect_profile({"title": "Day trading lesson: my biggest loss"}) == "podcast"
    assert detect_profile({"title": "Last To Leave Circle Wins $500,000"}) == "entertainment"
    assert detect_profile({"title": "anything", "chat_files": ["x.json"]}) == "stream"
    pc = apply_profile(CFG, "podcast")
    assert pc["analysis"]["clip_max"] == 60 and pc["signal_weights"]["transcript_insight"] > CFG["signal_weights"]["transcript_insight"]
    sig = transcript.text_signals([{"start": 0, "end": 4, "text": "Nobody tells you this: I lost $40,000 in 10 minutes"}], 6, CFG["lexicon"])
    assert sig["transcript_insight"][1] > 0


def _m(i, start, score):
    return {"id": f"m{i}", "start": start, "end": start + 40, "viral_score": score, "reviewed": True,
            "signal_score": score, "start_ts": fmt_ts(start)}


def test_assemble_plan_prefers_dense_block():
    moments = [_m(1, 600, 88), _m(2, 900, 80), _m(3, 1100, 90), _m(4, 1300, 85),   # dense cluster
               _m(5, 5000, 75), _m(6, 9000, 72), _m(7, 12000, 50)]
    p = assemble.plan(moments, 4 * 3600, CFG)
    a = p["plan_a_contiguous"]
    assert a["credits"] == 1 and set(a["blocks"][0]["moments"]) == {"m1", "m2", "m3", "m4"}
    b = p["plan_b_combined"]
    assert b["credits"] == 1 and b["strong_moments"] == 6      # all strong moments fit in one combined credit
    assert p["full_video_cost_credits"] == 12
    assert all(s["id"] != "m7" for sel in b["selections"] for s in sel["segments"])  # weak moment never used


def test_unreviewed_never_recommended():
    c = {"id": "m1", "start": 10, "end": 50, "signal_value": 9, "signal_score": 95, "hook_strength": 9,
         "sustain": 1, "sharpness": 9, "signal_breakdown": {"laughter": 8}, "footage_check": {"ok": True}}
    r = ranking.apply_review(c, None, CFG)
    assert r["recommended"] is False
    r2 = ranking.apply_review(c, {"scores": {k: 9 for k in ranking.CRITERIA}}, CFG)
    assert r2["recommended"] is True and r2["tier"] == "S"
    c["footage_check"] = {"ok": False}
    assert ranking.apply_review(c, {"scores": {k: 9 for k in ranking.CRITERIA}}, CFG)["recommended"] is False


def test_clips_per_credit_cap():
    moments = [_m(i, 600 + i * 300, 85) for i in range(20)]   # 20 strong moments
    b = assemble.plan(moments, 4 * 3600, CFG)["plan_b_combined"]
    assert all(len(sel["segments"]) <= CFG["assemble"]["clips_per_credit"] for sel in b["selections"])
    assert b["credits"] == 2 and b["strong_moments"] == 20
