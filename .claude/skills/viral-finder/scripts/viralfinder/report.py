"""Easy-to-read report (Markdown + standalone HTML) with sections A-I."""
from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

from .common import fmt_duration, timestamp_url
from .ranking import CRITERIA, eligibility, fix_caption


def _link(url: str, label: str) -> str:
    return f"[{label}]({url})" if url else label


def build(projects: list, cfg: dict, campaign: dict | None, out_dir: Path, title: str = "") -> tuple[Path, Path]:
    L = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    L.append(f"# Viral Finder Report{(' - ' + title) if title else ''}")
    L.append(f"_Generated {now}. Campaign rules applied: **{campaign['name'] if campaign else 'none (generic analysis)'}**._\n")
    L.append("> **How to read this:** *Recommended* moments were found by the cheap full-stream scan, checked against the "
             "original footage (frames + audio alignment) and scored by review. *Unreviewed candidates* are signal-only and "
             "must not be treated as verified.\n")

    all_moments, inaccessible, plans = [], [], []
    for p in projects:
        meta = p.meta()
        ranked = p.load("ranked.json", [])
        plan = p.load("assemble_plan.json", {})
        summ = p.load("scan_summary.json", {})
        for m in ranked:
            m["_meta"] = meta
            m["_project"] = p.name
        all_moments += ranked
        plans.append((p, meta, plan, summ))
        for m in ranked:
            fc = m.get("footage_check") or {}
            if fc and not fc.get("ok"):
                bad = [c for c in fc.get("checks", []) if c.get("ok") is False]
                if bad:
                    inaccessible.append((meta.get("title"), m["id"], m["start_ts"], bad[0]["check"], bad[0]["detail"]))

    # ---------------- A
    L.append("## A. Best videos to analyze\n")
    L.append("| Video | Duration | Date | Signals used | Candidates | Recommended | Campaign eligibility |")
    L.append("|---|---|---|---|---|---|---|")
    for p, meta, plan, summ in plans:
        rec = sum(1 for m in all_moments if m["_project"] == p.name and m.get("recommended"))
        el = eligibility(meta, campaign)
        el_txt = "; ".join(("OK " if e["ok"] else ("CHECK " if e["ok"] is None else "FAIL ")) + e["check"] for e in el) or "-"
        d = meta.get("upload_date") or ""
        d = f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(d) == 8 else "-"
        L.append(f"| {_link(meta.get('webpage_url', ''), meta.get('title', p.name))} | {fmt_duration(meta.get('duration', 0))} | {d} | "
                 f"{', '.join(summ.get('signals_used', []))} | {summ.get('candidates', 0)} | {rec} | {el_txt} |")
    L.append("")

    rec_all = sorted([m for m in all_moments if m.get("recommended")], key=lambda m: -m["viral_score"])
    rec_all = rec_all[: cfg["report"]["max_recommended"]]
    unrev = sorted([m for m in all_moments if not m.get("reviewed") and not m.get("reject")],
                   key=lambda m: -m.get("signal_score", 0))

    # ---------------- B + F
    L.append("## B. Best timestamps across the stream (recommended, verified)\n")
    if not rec_all:
        L.append("_No moment is fully recommended yet. Review the shortlist (reviews_todo.json) and re-run `report`._\n")
    else:
        L.append("| # | Score | Tier | Start | End | Dur | Moment | Video |")
        L.append("|---|---|---|---|---|---|---|---|")
        for i, m in enumerate(rec_all, 1):
            meta = m["_meta"]
            url = timestamp_url(meta.get("webpage_url", ""), m["start"], meta.get("source_kind", ""))
            L.append(f"| {i} | **{m['viral_score']:.0f}** | {m['tier']} | {_link(url, m['start_ts'])} | {m['end_ts']} | "
                     f"{fmt_duration(m['duration'])} | {(m.get('description') or '')[:90]} | {meta.get('title', '')[:40]} |")
        L.append("")

    L.append("## C + D. Best footage selections for Ssemble and estimated credit consumption\n")
    for p, meta, plan, summ in plans:
        if not plan:
            L.append(f"_No plan yet for {meta.get('title')}. Run `plan`._\n")
            continue
        L.append(f"### {meta.get('title', p.name)}\n")
        if plan.get("preliminary"):
            L.append("> **PRELIMINARY** - based on raw signals; review moments before spending credits.\n")
        L.append(f"- Whole video would cost **{plan['full_video_cost_credits']} credits** "
                 f"({plan['video_duration']} at {plan['minutes_per_credit']} min/credit).")
        a, b = plan["plan_a_contiguous"], plan["plan_b_combined"]
        L.append(f"- **Plan A - continuous 20-min blocks:** {a['credits']} credits, {a['strong_moments']} strong moments "
                 f"({a['moments_per_credit']} per credit). Saves {plan['savings_vs_full_video']['plan_a']} credits.")
        L.append(f"- **Plan B - combined non-consecutive segments:** {b['credits']} credits, {b['strong_moments']} strong moments "
                 f"+ {b['total_moments_incl_filler'] - b['strong_moments']} free filler ({b['moments_per_credit']} strong per credit). "
                 f"Saves {plan['savings_vs_full_video']['plan_b']} credits.")
        for r in plan.get("recommendations", []):
            L.append(f"- {r}")
        L.append("\n**Plan A blocks (paste these ranges into Ssemble):**\n")
        L.append("| Credit | Start | End | Strong moments | Avg score | Moment IDs |")
        L.append("|---|---|---|---|---|---|")
        for i, blk in enumerate(a["blocks"], 1):
            url = timestamp_url(meta.get("webpage_url", ""), blk["start"], meta.get("source_kind", ""))
            L.append(f"| {i} | {_link(url, blk['start_ts'])} | {blk['end_ts']} | {blk['strong_moments']} | {blk['avg_score']} | {', '.join(blk['moments'])} |")
        L.append("\n**Plan B selections (each = 1 credit, segments in chronological order):**\n")
        for i, sel in enumerate(b["selections"], 1):
            slots = f", {sel['strong_moments'] + sel['filler_moments']}/{plan['clips_per_credit']} clip slots" if plan.get("clips_per_credit") else ""
            L.append(f"- Credit {i} ({sel['footage_minutes']} min, {sel['strong_moments']} strong + {sel['filler_moments']} filler{slots}): " +
                     ", ".join(f"{s['start_ts']}-{s['end_ts']}{' (filler)' if s['filler'] else ''}" for s in sel["segments"]))
        if plan.get("plan_c_hot_zones"):
            L.append("\n**Plan C - hot zones (optional extra credits):**\n")
            for z in plan["plan_c_hot_zones"]:
                L.append(f"- {z['start_ts']}-{z['end_ts']}: {z['strong_moments']} strong moments, {z['moments_per_20min']}/20 min, "
                         f"avg score {z['avg_score']} -> +{z['extra_credits']} credits")
        L.append("")

    L.append("## E. Number of potential clips\n")
    tiers = {t: sum(1 for m in rec_all if m["tier"] == t) for t in ("S", "A", "B")}
    L.append(f"- Recommended clips: **{len(rec_all)}** (S-tier {tiers['S']}, A-tier {tiers['A']}, B-tier {tiers['B']})")
    L.append(f"- Unreviewed candidates still in the pool: {len(unrev)}")
    L.append("- Ssemble may generate extra clips from the same footage; these counts are moments verified by this skill.\n")

    L.append("## F. Ranking of the strongest moments (details)\n")
    for i, m in enumerate(rec_all, 1):
        meta = m["_meta"]
        url = timestamp_url(meta.get("webpage_url", ""), m["start"], meta.get("source_kind", ""))
        cap, notes = fix_caption(m.get("caption", ""), campaign)
        L.append(f"### {i}. {m.get('title_idea') or (m.get('description') or m['id'])[:70]}  - {m['viral_score']:.0f}/100 ({m['tier']})\n")
        L.append(f"- **Video:** {meta.get('title', '')}")
        L.append(f"- **Original URL:** {meta.get('webpage_url') or meta.get('local_path', '')}")
        L.append(f"- **Jump to moment:** {url or '-'}")
        L.append(f"- **Start:** {m['start_ts']}  **End:** {m['end_ts']}  **Duration:** {fmt_duration(m['duration'])}  (peak {m['peak_ts']})")
        L.append(f"- **What happens:** {m.get('description', '')}")
        L.append(f"- **Why it is interesting:** {m.get('why', '')}")
        L.append(f"- **Suggested hook:** {m.get('hook_text', '')}")
        L.append(f"- **Suggested caption:** {cap}{('  _(' + ', '.join(notes) + ')_') if notes else ''}")
        L.append(f"- **Recommended platform:** {m.get('platform', '')}")
        crit = m.get("criteria", {})
        L.append("- **Scores:** " + ", ".join(f"{k} {crit.get(k, 0):.0f}" for k in CRITERIA))
        comp = m.get("competition") or {}
        if comp:
            L.append(f"- **Competition check:** {comp.get('level')} - {comp.get('note', '')}")
            for mt in comp.get("matches", [])[:3]:
                L.append(f"  - similar: [{mt['title']}]({mt['url']})")
        else:
            L.append("- **Competition check:** not run - originality unknown")
        fc = m.get("footage_check", {})
        al = fc.get("alignment") or {}
        L.append(f"- **Verification:** {m.get('verified_by', 'frames + transcript')}; alignment: "
                 f"{al.get('method', '-')} (corr {al.get('correlation', '-')}); contact sheet: `{fc.get('contact_sheet', '')}`")
        if m.get("campaign_checks"):
            L.append("- **Campaign checks:** " + ", ".join(f"{k}={'yes' if v else ('NO' if v is False else '?')}" for k, v in m["campaign_checks"].items()))
        L.append(f"- **Signals:** {'; '.join(m.get('reasons', []))}\n")

    L.append("## G. Editing hooks and captions (copy-paste)\n")
    for i, m in enumerate(rec_all, 1):
        cap, _ = fix_caption(m.get("caption", ""), campaign)
        L.append(f"{i}. **[{m['start_ts']}]** Hook: _{m.get('hook_text', '')}_  \n   Caption: {cap}")
    L.append("")

    L.append("## H. Links to original sources\n")
    for p, meta, plan, summ in plans:
        L.append(f"- {meta.get('title', p.name)}: {meta.get('webpage_url') or meta.get('local_path', '')}"
                 f"{(' (channel: ' + meta['uploader'] + ')') if meta.get('uploader') else ''}")
    L.append("")

    L.append("## I. Footage that could not be accessed or verified\n")
    if not inaccessible and all(not (m.get('footage_check') is None and m.get('reviewed')) for m in all_moments):
        L.append("- Nothing blocked for the shortlisted moments.")
    for t, mid, ts, chk, det in inaccessible:
        L.append(f"- {t} / {mid} @ {ts}: **{chk}** failed - {det.splitlines()[0][:200]}")
    if unrev:
        L.append(f"- {len(unrev)} candidates were found by signals only and NOT reviewed (top 10 below). They are not verified recommendations:")
        for m in unrev[:10]:
            meta = m["_meta"]
            url = timestamp_url(meta.get("webpage_url", ""), m["start"], meta.get("source_kind", ""))
            L.append(f"  - {m['id']} {_link(url, m['start_ts'])}-{m['end_ts']} signal {m.get('signal_score', 0):.0f}: {'; '.join(m.get('reasons', [])[:2])}")
    if campaign:
        L.append("\n### Campaign rules to respect when posting\n")
        for r in campaign.get("content_rules", []) + campaign.get("audience_rules", []):
            L.append(f"- {r}")
        L.append(f"- Allowed platforms: {', '.join(campaign.get('allowed_platforms', []))}")
        cr = campaign.get("caption_rules", {})
        L.append(f"- Captions must mention: {', '.join(cr.get('must_mention', []))}; required hashtags: {', '.join(cr.get('required_hashtags', []))}")
    md = "\n".join(L) + "\n"
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "report.md"
    md_path.write_text(md, encoding="utf-8")
    html_path = out_dir / "report.html"
    html_path.write_text(md_to_html(md, title or "Viral Finder Report"), encoding="utf-8")
    return md_path, html_path


def md_to_html(md: str, title: str) -> str:
    """Tiny Markdown subset -> HTML (headings, tables, lists, bold/italic, links, quotes)."""
    def inline(s: str) -> str:
        s = html.escape(s)
        s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"(?<![\w*])_([^_]+)_(?!\w)", r"<i>\1</i>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        return s
    out, in_table, in_list = [], False, False
    for line in md.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(re.fullmatch(r"-+", c) for c in cells):
                continue
            if not in_table:
                out.append("<table><tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells) + "</tr>")
                in_table = True
            else:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
            continue
        if in_table:
            out.append("</table>")
            in_table = False
        if re.match(r"^\s*(-|\d+\.)\s", line):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li style='margin-left:{(len(line) - len(line.lstrip())) * 8}px'>{inline(re.sub(r'^\s*(-|\d+\.)\s', '', line))}</li>")
            continue
        if in_list and not line.startswith("   "):
            out.append("</ul>")
            in_list = False
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
        elif line.startswith(">"):
            out.append(f"<blockquote>{inline(line.lstrip('> '))}</blockquote>")
        elif line.strip():
            out.append(f"<p>{inline(line)}</p>")
    if in_table:
        out.append("</table>")
    if in_list:
        out.append("</ul>")
    css = """
:root{--bg:#fff;--fg:#1a1a1a;--mut:#666;--line:#e3e3e3;--acc:#5b3df5;--soft:#f5f3ff}
@media (prefers-color-scheme:dark){:root{--bg:#141414;--fg:#eee;--mut:#aaa;--line:#333;--acc:#a593ff;--soft:#1f1b2e}}
body{background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,-apple-system,Segoe UI,sans-serif;max-width:1100px;margin:0 auto;padding:16px}
h1{font-size:26px}h2{margin-top:36px;border-bottom:2px solid var(--acc);padding-bottom:4px}h3{margin-top:24px}
table{border-collapse:collapse;width:100%;display:block;overflow-x:auto;font-size:13px}th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
th{background:var(--soft)}a{color:var(--acc)}blockquote{background:var(--soft);margin:12px 0;padding:10px 14px;border-left:4px solid var(--acc)}
code{font-size:12px;color:var(--mut)}li{margin:3px 0}"""
    return f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title><style>{css}</style></head><body>{''.join(out)}</body></html>"
