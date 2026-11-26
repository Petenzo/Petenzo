"""Assemble credit optimiser.   1 credit = 20 minutes of footage (configurable).

A credit buys FOOTAGE, not clips. The goal is to put as many excellent moments as
possible inside every 20-minute footage selection, so each credit yields several
strong clips instead of one.

Three plans are produced and compared:
  A. Contiguous blocks  - the best continuous 20-min windows (always supported).
  B. Combined segments  - non-consecutive moment segments packed into 20-min
                          selections (only if Assemble lets you combine timestamps).
  C. Hot-zone extras    - 2-3 h sections so dense with strong moments that sending
                          the whole section (extra credits) is likely worth it.
"""
from __future__ import annotations

import math

from .common import fmt_duration, fmt_ts


def value(score: float) -> float:
    return max(0.0, min(1.5, ((score - 60) / 30.0))) ** 1.5


def moment_pool(moments: list[dict], cfg: dict) -> tuple[list[dict], bool]:
    """Strong moments to plan with. Returns (pool, preliminary_flag)."""
    a = cfg["assemble"]
    reviewed = [m for m in moments if m.get("reviewed")]
    if reviewed:
        pool = [m for m in moments if m.get("reviewed") and not m.get("reject") and m["viral_score"] >= a["min_moment_score"]]
        return pool, False
    # Nothing reviewed yet -> preliminary plan on signal strength (clearly flagged).
    ranked = sorted(moments, key=lambda m: -m.get("signal_score", 0))
    pool = []
    for m in [x for x in ranked if x.get("signal_score", 0) >= a["min_moment_score"]]:
        mm = dict(m)
        mm["viral_score"] = m.get("signal_score", 0)
        pool.append(mm)
    return pool, True


def contiguous_plan(pool: list[dict], duration: float, cfg: dict, budget: int | None) -> list[dict]:
    a = cfg["assemble"]
    L = a["minutes_per_credit"] * 60
    lead = a["segment_lead_in"]
    remaining = sorted(pool, key=lambda m: m["start"])
    blocks: list[dict] = []
    while remaining and (budget is None or len(blocks) < budget):
        best = None
        starts = {max(0.0, min(m["start"] - lead, max(0.0, duration - L))) for m in remaining}
        for s in starts:
            e = s + L
            if any(not (e <= b["start"] or s >= b["end"]) for b in blocks):
                continue
            inside = [m for m in remaining if m["start"] >= s and m["end"] <= e]
            v = sum(value(m["viral_score"]) for m in inside)
            if inside and (best is None or v > best[0]):
                best = (v, s, e, inside)
        if not best:
            break
        v, s, e, inside = best
        strong = [m for m in inside if m["viral_score"] >= a["min_moment_score"]]
        if blocks and len(strong) < a["min_strong_moments_per_credit"]:
            break  # next credit would not pay for itself
        # tighten the block so it starts just before its first moment
        s2 = max(0.0, min(min(m["start"] for m in inside) - lead, max(0.0, duration - L)))
        blocks.append({"start": s2, "end": min(duration, s2 + L), "start_ts": fmt_ts(s2), "end_ts": fmt_ts(min(duration, s2 + L)),
                       "moments": [m["id"] for m in sorted(inside, key=lambda m: m["start"])],
                       "strong_moments": len(strong), "value": round(v, 2),
                       "avg_score": round(sum(m["viral_score"] for m in inside) / len(inside), 1)})
        ids = {m["id"] for m in inside}
        remaining = [m for m in remaining if m["id"] not in ids]
    return sorted(blocks, key=lambda b: -b["value"])


def combined_plan(pool: list[dict], all_moments: list[dict], cfg: dict, budget: int | None) -> list[dict]:
    a = cfg["assemble"]
    L = a["minutes_per_credit"] * 60
    lead, tail = a["segment_lead_in"], a["segment_tail"]

    def seg(m):
        return {"id": m["id"], "start": max(0.0, m["start"] - lead), "end": m["end"] + tail, "score": m["viral_score"]}

    segs = sorted((seg(m) for m in pool), key=lambda s: -s["score"])
    bins: list[dict] = []
    for idx, s in enumerate(segs):
        ln = s["end"] - s["start"]
        for b in bins:
            if b["used"] + ln <= L:
                b["segs"].append(s)
                b["used"] += ln
                break
        else:
            if budget is not None and len(bins) >= budget:
                continue
            # Open another credit only if enough strong moments are left to justify it.
            if bins and (len(segs) - idx) < a["min_strong_moments_per_credit"]:
                continue
            bins.append({"segs": [s], "used": ln})
    # Free fill: the credit is paid anyway, so top up leftover minutes with the next-best moments.
    used_ids = {s["id"] for b in bins for s in b["segs"]}
    floor = cfg["tiers"]["B"]
    extras = sorted((m for m in all_moments if m["id"] not in used_ids and not m.get("reject")
                     and m.get("viral_score", m.get("signal_score", 0)) >= floor),
                    key=lambda m: -m.get("viral_score", m.get("signal_score", 0)))
    for b in bins:
        for m in list(extras):
            s = seg(m)
            s["score"] = m.get("viral_score", m.get("signal_score", 0))
            s["fill"] = True
            ln = s["end"] - s["start"]
            if b["used"] + ln <= L:
                b["segs"].append(s)
                b["used"] += ln
                extras.remove(m)
    out = []
    for b in bins:
        segs_sorted = sorted(b["segs"], key=lambda s: s["start"])
        out.append({"segments": [{"id": s["id"], "start_ts": fmt_ts(s["start"]), "end_ts": fmt_ts(s["end"]),
                                  "duration": round(s["end"] - s["start"]), "score": s["score"],
                                  "filler": bool(s.get("fill"))} for s in segs_sorted],
                    "footage_minutes": round(b["used"] / 60, 1),
                    "strong_moments": sum(1 for s in b["segs"] if not s.get("fill")),
                    "filler_moments": sum(1 for s in b["segs"] if s.get("fill"))})
    return out


def hot_zones(pool: list[dict], duration: float, cfg: dict) -> list[dict]:
    a = cfg["assemble"]
    W = a["hot_zone_window_minutes"] * 60
    L = a["minutes_per_credit"] * 60
    if duration < W * 1.2 or len(pool) < 4:
        return []
    zones = []
    starts = sorted({max(0.0, min(m["start"], duration - W)) for m in pool})
    for s in starts:
        inside = [m for m in pool if s <= m["start"] and m["end"] <= s + W]
        per20 = len(inside) / (W / L)
        zones.append((per20, s, inside))
    zones.sort(key=lambda z: -z[0])
    picked = []
    for per20, s, inside in zones:
        if per20 < a["hot_zone_min_strong_per_20min"]:
            break
        if any(not (s + W <= p["start"] or s >= p["end"]) for p in picked):
            continue
        picked.append({"start": s, "end": s + W, "start_ts": fmt_ts(s), "end_ts": fmt_ts(s + W),
                       "strong_moments": len(inside), "moments_per_20min": round(per20, 1),
                       "extra_credits": math.ceil(W / L),
                       "avg_score": round(sum(m["viral_score"] for m in inside) / len(inside), 1)})
        if len(picked) >= 2:
            break
    return picked


def plan(moments: list[dict], duration: float, cfg: dict, budget: int | None = None) -> dict:
    a = cfg["assemble"]
    L = a["minutes_per_credit"] * 60
    pool, prelim = moment_pool(moments, cfg)
    full_cost = math.ceil(duration / L) if a["round_partial_credit_up"] else round(duration / L, 2)
    cont = contiguous_plan(pool, duration, cfg, budget)
    comb = combined_plan(pool, moments, cfg, budget)
    zones = hot_zones(pool, duration, cfg)
    cont_cost = len(cont)
    comb_cost = len(comb)
    cont_strong = sum(b["strong_moments"] for b in cont)
    comb_strong = sum(b["strong_moments"] for b in comb)
    comb_total = sum(b["strong_moments"] + b["filler_moments"] for b in comb)
    rec = []
    if a["allow_non_consecutive"] is True:
        rec.append("Use Plan B (combined segments): it packs the most strong moments per credit.")
    elif a["allow_non_consecutive"] is False:
        rec.append("Use Plan A (continuous blocks) - your Assemble setup does not combine timestamps.")
    else:
        rec.append("If Assemble lets you combine non-consecutive timestamps in one selection, use Plan B; otherwise Plan A. "
                   "(Set assemble.allow_non_consecutive to true/false in config.json once you know.)")
    for i, sel in enumerate(comb, 1):
        free = a["minutes_per_credit"] - sel["footage_minutes"]
        if free >= 3:
            rec.append(f"Plan B credit {i} still has {free:.0f} unused minutes you pay for anyway - review more candidates "
                       f"(or lower report.min_recommend_score) to fill it with extra moments at no extra cost.")
    for z in zones:
        rec.append(f"Hot zone {z['start_ts']}-{z['end_ts']}: {z['strong_moments']} strong moments "
                   f"({z['moments_per_20min']} per 20 min). Worth {z['extra_credits']} extra credits ONLY if you want "
                   f"Assemble to find more moments in that section than the scan shortlisted.")
    if prelim:
        rec.insert(0, "PRELIMINARY: no moments have been reviewed yet - this plan uses raw signal strength. "
                      "Review the shortlist first, then re-run 'plan' before spending credits.")
    return {
        "preliminary": prelim,
        "minutes_per_credit": a["minutes_per_credit"],
        "video_duration": fmt_duration(duration),
        "full_video_cost_credits": full_cost,
        "strong_moment_pool": len(pool),
        "plan_a_contiguous": {"credits": cont_cost, "strong_moments": cont_strong,
                              "moments_per_credit": round(cont_strong / cont_cost, 1) if cont_cost else 0, "blocks": cont},
        "plan_b_combined": {"credits": comb_cost, "strong_moments": comb_strong, "total_moments_incl_filler": comb_total,
                            "moments_per_credit": round(comb_strong / comb_cost, 1) if comb_cost else 0, "selections": comb},
        "plan_c_hot_zones": zones,
        "savings_vs_full_video": {"plan_a": full_cost - cont_cost, "plan_b": full_cost - comb_cost},
        "recommendations": rec,
    }
