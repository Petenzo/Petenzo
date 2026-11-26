#!/usr/bin/env python3
"""Viral Finder - one command for the whole pipeline.

    python vf.py doctor                         check tools + network access
    python vf.py discover "Kai Cenat GTA 6"      find long streams / VODs
    python vf.py run <URL | file | Drive link>  ingest + cheap scan + verify shortlist + preliminary plan/report
    python vf.py review   --project NAME        apply filled-in reviews_todo.json
    python vf.py competition --project NAME     look for already-reposted clips
    python vf.py plan     --project NAME        Assemble credit plan
    python vf.py report   --project NAME [...]  report.md + report.html

Individual steps: ingest, scan, verify, rank, clip, campaigns, status.
Outputs go to ./viral-finder-output/<project>/ (override with VF_OUTPUT env var).
"""
from __future__ import annotations

import argparse
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from viralfinder import assemble, ranking, research, sources  # noqa: E402
from viralfinder.common import (Project, fmt_duration, fmt_ts, have, load_config, log, read_json,  # noqa: E402
                                timestamp_url, write_json, ytdlp_cmd)
from viralfinder.sources import AccessError  # noqa: E402


# --------------------------------------------------------------------------- helpers
def _campaign_for(proj: Project, explicit: str | None):
    meta = proj.meta()
    saved = meta.get("campaign")
    if explicit:
        c = ranking.match_campaign("", explicit)
        meta["campaign"] = c["id"] if c else "none"
        proj.save_meta(meta)
        return c
    if saved:
        return ranking.match_campaign("", saved)
    return ranking.match_campaign(f"{meta.get('title', '')} {meta.get('uploader', '')} {meta.get('description', '')[:300]}")


def do_rank(proj: Project, cfg: dict, campaign=None) -> list[dict]:
    cands = proj.load("candidates.json", [])
    reviews = proj.load("reviews.json", {}) or {}
    comp = proj.load("competition.json", {}) or {}
    ranked = []
    for c in cands:
        if c["id"] in comp:
            c["competition"] = comp[c["id"]]
        r = ranking.apply_review(c, reviews.get(c["id"]), cfg)
        if campaign and r.get("reviewed"):
            checks = r.get("campaign_checks") or {}
            for k in (campaign.get("per_moment_checks") or {}):
                checks.setdefault(k, None)
            if "not_existing_short" in checks and checks["not_existing_short"] is None and c.get("competition"):
                checks["not_existing_short"] = None if c["competition"]["level"] == "unknown" else c["competition"]["level"] != "many"
            r["campaign_checks"] = checks
            r["recommended"] = r["recommended"] and ranking.campaign_ok(r)
        ranked.append(r)
    ranked.sort(key=lambda m: -m["viral_score"])
    proj.save("ranked.json", ranked)
    return ranked


def do_plan(proj: Project, cfg: dict, budget=None) -> dict:
    ranked = proj.load("ranked.json") or do_rank(proj, cfg, _campaign_for(proj, None))
    dur = proj.meta().get("duration") or max((m["end"] for m in ranked), default=0)
    p = assemble.plan(ranked, dur, cfg, budget)
    proj.save("assemble_plan.json", p)
    return p


def print_plan(p: dict) -> None:
    a, b = p["plan_a_contiguous"], p["plan_b_combined"]
    log(f"\nASSEMBLE PLAN {'(PRELIMINARY - not reviewed yet)' if p['preliminary'] else ''}")
    log(f"  Full video: {p['full_video_cost_credits']} credits ({p['video_duration']})")
    log(f"  Plan A continuous blocks : {a['credits']} credits -> {a['strong_moments']} strong moments ({a['moments_per_credit']}/credit)")
    for i, blk in enumerate(a["blocks"], 1):
        log(f"     credit {i}: {blk['start_ts']} - {blk['end_ts']}  ({blk['strong_moments']} strong, avg {blk['avg_score']})")
    log(f"  Plan B combined segments: {b['credits']} credits -> {b['strong_moments']} strong moments ({b['moments_per_credit']}/credit)")
    for i, sel in enumerate(b["selections"], 1):
        log(f"     credit {i}: " + ", ".join(f"{s['start_ts']}-{s['end_ts']}" for s in sel["segments"]))
    for r in p["recommendations"]:
        log(f"  * {r}")


# --------------------------------------------------------------------------- commands
def cmd_doctor(args, cfg):
    ok = True
    log("Viral Finder - environment check\n")
    for tool, how in [("ffmpeg", "Windows: winget install ffmpeg | macOS: brew install ffmpeg | Linux: sudo apt install ffmpeg"),
                      ("ffprobe", "comes with ffmpeg")]:
        found = have(tool)
        ok &= found
        log(f"  [{'OK' if found else 'MISSING'}] {tool}" + ("" if found else f"  -> install: {how}"))
    y = ytdlp_cmd()
    log(f"  [{'OK' if y else 'MISSING'}] yt-dlp" + ("" if y else "  -> install: pip install -U yt-dlp"))
    ok &= bool(y)
    try:
        import numpy  # noqa: F401
        log("  [OK] numpy")
    except ImportError:
        ok = False
        log("  [MISSING] numpy  -> pip install numpy")
    from viralfinder.transcript import whisper_available
    log(f"  [{'OK' if whisper_available() else 'optional'}] faster-whisper (local transcription of shortlisted moments)"
        + ("" if whisper_available() else "  -> pip install faster-whisper"))
    log("\nNetwork access from THIS machine:")
    for name, url in [("YouTube", "https://www.youtube.com/"), ("Twitch", "https://www.twitch.tv/"),
                      ("Google Drive", "https://drive.google.com/"), ("Google video CDN", "https://redirector.googlevideo.com/")]:
        try:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
            urllib.request.urlopen(req, timeout=10)
            log(f"  [OK] {name}")
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            reachable = "HTTP Error" in msg and "403" not in msg[:30]
            if reachable or "HTTP Error 405" in msg or "HTTP Error 404" in msg:
                log(f"  [OK] {name} (reachable)")
            else:
                log(f"  [BLOCKED] {name}: {msg[:120]}")
                log("      -> Run Claude Code on your own computer, or allow this host in the cloud environment's network settings."
                    " Local files and connectors still work.")
    log(f"\nOutput folder: {Path(os.environ.get('VF_OUTPUT') or cfg['output_root']).resolve()}")
    log("Campaigns: " + ", ".join(c["id"] for c in ranking.list_campaigns()))
    log("\nREADY" if ok else "\nNOT READY - install the missing tools above, then run doctor again.")
    return 0 if ok else 1


def cmd_campaigns(args, cfg):
    for c in ranking.list_campaigns():
        log(f"- {c['id']}: {c['name']}  ({c['_file']})")
    log("Add your own: copy config/campaigns/_template.json, fill it in, save under a new name.")
    return 0


def cmd_discover(args, cfg):
    camp = ranking.match_campaign(args.query, args.campaign)
    extra = ["--cookies-from-browser", args.cookies_from_browser] if args.cookies_from_browser else []
    twitch = args.twitch or (camp or {}).get("twitch_channel")
    after = args.after or ((camp or {}).get("eligibility") or {}).get("footage_date_from")
    rows = research.discover(args.query, args.limit, args.min_minutes, twitch,
                             (camp or {}).get("youtube_channels") if args.channels else None, after, extra)
    out = Path(os.environ.get("VF_OUTPUT") or cfg["output_root"])
    write_json(out / "discovery.json", {"query": args.query, "campaign": (camp or {}).get("id"), "results": rows})
    if camp:
        log(f"\nCampaign detected: {camp['name']} (filtering to footage after {after})")
    log(f"\n{len(rows)} long videos found (>= {args.min_minutes} min):\n")
    for i, r in enumerate(rows[: args.limit], 1):
        d = r["upload_date"]
        d = f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(d) == 8 else "date ?"
        log(f"{i:2d}. [{r['duration']:>8}] {r['title'][:80]}\n     {r['platform']} | {r['channel']} | {d} | {r['url']}")
    log(f"\nSaved: {out / 'discovery.json'}\nNext: python vf.py run <URL>")
    return 0


def cmd_ingest(args, cfg):
    proj = sources.ingest(args.source, args.project, cfg, args.cookies_from_browser, args.no_chat)
    if args.campaign:
        _campaign_for(proj, args.campaign)
    log(f"Project: {proj.root}")
    return proj


def cmd_register(args, cfg):
    """Create a project WITHOUT downloading media - e.g. transcript fetched through a connector (vidIQ) or browser."""
    from viralfinder.common import parse_ts, slugify
    src = sources.detect_source(args.url) if args.url else {"kind": "url"}
    meta = {"title": args.title, "duration": parse_ts(args.duration), "webpage_url": args.url or "", "source_url": args.url or "",
            "source_kind": src.get("kind", "url"), "uploader": args.uploader or "", "upload_date": (args.date or "").replace("-", ""),
            "audio_path": "", "video_path": "", "subtitle_files": [str(Path(f).resolve()) for f in args.transcript or []],
            "chat_files": [str(Path(f).resolve()) for f in args.chat or []], "registered_without_media": True}
    proj = Project.open(args.project or slugify(args.title), cfg, create=True)
    proj.save_meta(meta)
    if args.campaign:
        _campaign_for(proj, args.campaign)
    log(f"Registered (no media downloaded): {proj.root}\nNext: python vf.py scan --project {proj.name}")
    return proj


def cmd_scan(args, cfg):
    from viralfinder.scan import scan
    proj = Project.open(args.project, cfg)
    scan(proj, cfg, use_scenes=args.scenes)
    return proj


def cmd_verify(args, cfg):
    from viralfinder.verify import verify
    proj = Project.open(args.project, cfg)
    ids = args.ids.split(",") if args.ids else None
    verify(proj, cfg, args.top, ids, args.transcribe)
    log(f"\nNext: review the contact sheets listed in {proj.root / 'reviews_todo.json'}")
    return proj


def cmd_review(args, cfg):
    proj = Project.open(args.project, cfg)
    todo_path = Path(args.file) if args.file else proj.root / "reviews_todo.json"
    todo = read_json(todo_path, {}) or {}
    reviews = proj.load("reviews.json", {}) or {}
    moved = 0
    for mid, r in list(todo.items()):
        scores = r.get("scores") or {}
        filled = any(v is not None for v in scores.values()) or r.get("reject")
        if filled:
            reviews[mid] = {k: v for k, v in r.items() if not k.startswith("_")}
            del todo[mid]
            moved += 1
    proj.save("reviews.json", reviews)
    write_json(todo_path, todo)
    log(f"Applied {moved} reviews ({len(reviews)} total). {len(todo)} still waiting in {todo_path.name}.")
    do_rank(proj, cfg, _campaign_for(proj, None))
    return proj


def cmd_rank(args, cfg):
    proj = Project.open(args.project, cfg)
    ranked = do_rank(proj, cfg, _campaign_for(proj, args.campaign))
    log(f"{'ID':6} {'SCORE':>5} {'TIER':4} {'START':8} {'END':8} {'REV':3} {'FOOT':4} REC  reasons")
    for m in ranked[: args.limit]:
        log(f"{m['id']:6} {m['viral_score']:5.0f} {m['tier']:4} {m['start_ts']} {m['end_ts']} "
            f"{'yes' if m['reviewed'] else 'no':3} {'ok' if m['footage_verified'] else '-':4} {'*' if m['recommended'] else ' ':3}  "
            f"{(m.get('description') or '; '.join(m['reasons']))[:70]}")
    return proj


def cmd_competition(args, cfg):
    proj = Project.open(args.project, cfg)
    camp = _campaign_for(proj, None)
    ranked = proj.load("ranked.json") or do_rank(proj, cfg, camp)
    pool = [m for m in ranked if m.get("reviewed") and not m.get("reject")] or ranked[: args.top]
    creator = args.creator or (camp or {}).get("creator") or proj.meta().get("uploader", "")
    topic = args.topic or ""
    extra = ["--cookies-from-browser", proj.meta()["cookies_from_browser"]] if proj.meta().get("cookies_from_browser") else []
    res = research.competition(pool[: args.top], creator, topic, extra=extra)
    old = proj.load("competition.json", {}) or {}
    old.update(res)
    proj.save("competition.json", old)
    do_rank(proj, cfg, camp)
    return proj


def cmd_plan(args, cfg):
    proj = Project.open(args.project, cfg)
    do_rank(proj, cfg, _campaign_for(proj, None))
    p = do_plan(proj, cfg, args.credits)
    print_plan(p)
    return proj


def cmd_report(args, cfg):
    from viralfinder import report
    projs = [Project.open(n, cfg) for n in args.project]
    camp = None
    for p in projs:
        camp = _campaign_for(p, args.campaign) or camp
        do_rank(p, cfg, camp)
        do_plan(p, cfg, args.credits)
    out = Path(args.out) if args.out else (projs[0].root if len(projs) == 1 else Path(os.environ.get("VF_OUTPUT") or cfg["output_root"]) / "combined-report")
    md, html = report.build(projs, cfg, camp, out, args.title or (projs[0].meta().get("title") if len(projs) == 1 else ""))
    log(f"Report written:\n  {md.resolve()}\n  {html.resolve()}")
    return projs[0]


def cmd_status(args, cfg):
    proj = Project.open(args.project, cfg)
    meta = proj.meta()
    log(f"{meta.get('title')}  ({fmt_duration(meta.get('duration', 0))})  {meta.get('webpage_url') or meta.get('local_path')}")
    for f in ["metadata.json", "scan_summary.json", "candidates.json", "reviews_todo.json", "reviews.json",
              "competition.json", "ranked.json", "assemble_plan.json", "report.md"]:
        log(f"  [{'x' if (proj.root / f).exists() else ' '}] {f}")
    todo = proj.load("reviews_todo.json", {}) or {}
    log(f"  waiting for review: {len(todo)}")
    return proj


def cmd_clip(args, cfg):
    from viralfinder.video import cut_clip
    proj = Project.open(args.project, cfg)
    ranked = proj.load("ranked.json") or do_rank(proj, cfg)
    m = next((x for x in ranked if x["id"] == args.id), None)
    if not m:
        raise SystemExit(f"Moment {args.id} not found")
    meta = proj.meta()
    src, off = meta.get("video_path"), 0.0
    if not src:
        sec = proj.root / "sections" / f"{m['id']}.mp4"
        if not sec.exists():
            raise SystemExit("No local footage for this moment. Run verify for it first (downloads only that section).")
        src = str(sec)
        off = parse_offset(m)
    out = proj.root / "clips" / f"{m['id']}_{m['start_ts'].replace(':', '')}.mp4"
    out.parent.mkdir(exist_ok=True)
    cut_clip(src, m["start"] - off, m["end"] - off, out, args.vertical)
    log(f"Preview clip: {out.resolve()}")
    return proj


def parse_offset(m: dict) -> float:
    from viralfinder.common import parse_ts
    al = (m.get("footage_check") or {}).get("alignment") or {}
    return parse_ts(al["section_starts_at"]) if al.get("section_starts_at") else max(0, m["start"] - 5)


def cmd_run(args, cfg):
    """Everything cheap, in one go: ingest -> scan -> verify shortlist -> preliminary plan + report."""
    from viralfinder.scan import scan
    from viralfinder.verify import verify
    src = sources.detect_source(args.source)
    if src["kind"] == "topic":
        log(f"'{args.source}' looks like a search topic -> running discovery instead.\n")
        args.query, args.twitch, args.limit, args.min_minutes, args.after, args.channels = args.source, None, 15, 60, None, True
        return cmd_discover(args, cfg)
    proj = sources.ingest(args.source, args.project, cfg, args.cookies_from_browser, args.no_chat)
    camp = _campaign_for(proj, args.campaign)
    scan(proj, cfg, use_scenes=args.scenes)
    if not args.no_verify:
        verify(proj, cfg, args.top, None, args.transcribe)
    do_rank(proj, cfg, camp)
    p = do_plan(proj, cfg)
    from viralfinder import report
    md, html = report.build([proj], cfg, camp, proj.root, proj.meta().get("title", ""))
    print_plan(p)
    log(f"\nProject folder: {proj.root.resolve()}")
    log(f"Preliminary report: {md.resolve()}")
    log(f"NEXT STEP: review the shortlisted moments in {proj.root / 'reviews_todo.json'} "
        f"(look at each contact_sheet.jpg), then: python vf.py review --project {proj.name} && python vf.py report --project {proj.name}")
    return proj


# --------------------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="vf.py", description="Viral Finder: cheap full-stream scan -> verified viral moments -> Assemble plan")
    ap.add_argument("--config", help="extra JSON config to merge")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("doctor", help="check tools and network access")
    sub.add_parser("campaigns", help="list campaign rule files")

    d = sub.add_parser("discover", help="search for long streams/VODs")
    d.add_argument("query")
    d.add_argument("--twitch", help="Twitch channel name to list VODs from")
    d.add_argument("--limit", type=int, default=15)
    d.add_argument("--min-minutes", type=float, default=60)
    d.add_argument("--after", help="only videos uploaded on/after YYYY-MM-DD")
    d.add_argument("--channels", action="store_true", help="also list the campaign's YouTube channels' streams")
    d.add_argument("--campaign")
    d.add_argument("--cookies-from-browser")

    def common_src(p):
        p.add_argument("source", help="YouTube/Twitch/Drive URL, other video URL, or local file path")
        p.add_argument("--project", help="project folder name (default: from title)")
        p.add_argument("--campaign", help="campaign id (e.g. kai-cenat-gta6) or 'none'")
        p.add_argument("--cookies-from-browser", help="chrome / firefox / edge / safari (for sign-in walls)")
        p.add_argument("--no-chat", action="store_true", help="skip chat replay download")

    i = sub.add_parser("ingest", help="register a source and download audio/subtitles/chat only")
    common_src(i)

    g = sub.add_parser("register", help="create a project from a transcript/chat file without downloading media")
    g.add_argument("--title", required=True)
    g.add_argument("--duration", required=True, help="HH:MM:SS")
    g.add_argument("--url", help="original video URL (for links)")
    g.add_argument("--transcript", nargs="*", help=".srt/.vtt/.json3 files with timestamps")
    g.add_argument("--chat", nargs="*", help="chat replay files")
    g.add_argument("--uploader")
    g.add_argument("--date", help="YYYY-MM-DD")
    g.add_argument("--project")
    g.add_argument("--campaign")

    s = sub.add_parser("scan", help="cheap full-stream scan -> candidates")
    s.add_argument("--project", required=True)
    s.add_argument("--scenes", action="store_true", help="also detect scene changes (local video files only)")

    v = sub.add_parser("verify", help="check shortlisted timestamps against the footage, make contact sheets")
    v.add_argument("--project", required=True)
    v.add_argument("--top", type=int)
    v.add_argument("--ids", help="comma separated moment ids, e.g. m004,m017")
    v.add_argument("--transcribe", action="store_true", help="local Whisper on shortlisted sections without captions")

    r = sub.add_parser("review", help="apply filled-in reviews_todo.json")
    r.add_argument("--project", required=True)
    r.add_argument("--file")

    rk = sub.add_parser("rank", help="show the ranking")
    rk.add_argument("--project", required=True)
    rk.add_argument("--limit", type=int, default=40)
    rk.add_argument("--campaign")

    c = sub.add_parser("competition", help="search for existing reposts of the moments")
    c.add_argument("--project", required=True)
    c.add_argument("--top", type=int, default=15)
    c.add_argument("--creator")
    c.add_argument("--topic", default="")

    p = sub.add_parser("plan", help="Assemble credit plan")
    p.add_argument("--project", required=True)
    p.add_argument("--credits", type=int, help="maximum credits to spend")

    rp = sub.add_parser("report", help="write report.md + report.html")
    rp.add_argument("--project", required=True, nargs="+")
    rp.add_argument("--campaign")
    rp.add_argument("--credits", type=int)
    rp.add_argument("--out")
    rp.add_argument("--title")

    st = sub.add_parser("status", help="what has been done for a project")
    st.add_argument("--project", required=True)

    cl = sub.add_parser("clip", help="export a preview mp4 of one moment")
    cl.add_argument("--project", required=True)
    cl.add_argument("--id", required=True)
    cl.add_argument("--vertical", action="store_true", help="9:16 centre crop")

    rn = sub.add_parser("run", help="ingest + scan + verify + preliminary plan/report in one go")
    common_src(rn)
    rn.add_argument("--top", type=int)
    rn.add_argument("--scenes", action="store_true")
    rn.add_argument("--no-verify", action="store_true")
    rn.add_argument("--transcribe", action="store_true")

    args = ap.parse_args(argv)
    cfg = load_config(args.config)
    fn = globals()[f"cmd_{args.cmd}"]
    try:
        res = fn(args, cfg)
    except AccessError as e:
        log(f"\nACCESS PROBLEM\n{e}")
        return 2
    except FileNotFoundError as e:
        log(f"\n{e}")
        return 2
    return res if isinstance(res, int) else 0


if __name__ == "__main__":
    sys.exit(main())
