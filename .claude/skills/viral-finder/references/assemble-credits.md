# Ssemble credit optimisation

**1 credit = 20 minutes of footage = about 12 clips from Ssemble.** So the ideal selection holds
exactly ~12 strong moments: fewer wastes clip slots, more wastes moments (Ssemble still makes ~12).
Plan B therefore puts at most `clips_per_credit` (12) moments into one credit.

 A credit pays for footage, not for clips. The goal is
many excellent moments per 20 minutes so each credit yields several strong clips.

## The math

- Whole stream: `ceil(duration / 20 min)` credits. 10 h = 30 credits, mostly paying for boring parts.
- The cheap scan costs **0 credits** and finds where the good parts are.
- Plan A / B usually cut cost by 70-95 % while keeping the strongest moments.

## Plan A - continuous 20-minute blocks (always works)

The planner slides a 20-min window over the stream and picks the windows that contain the most
strong (>= 70) moments, weighted by score (an S-tier moment counts far more than a B).
A new block is only added if it contains at least `min_strong_moments_per_credit` (default 3)
strong moments - otherwise that credit would not pay for itself.

## Plan B - combined non-consecutive segments (if Ssemble allows it)

Each strong moment becomes a segment (20 s lead-in + moment + 10 s tail). Segments are packed
(best first) into 20-minute selections, listed chronologically. 20 min fits ~15-20 moments, so
this gives the most strong moments per credit. If a selection still has free minutes, the next
best moments (>= B tier) are added as **free filler** - you pay for the full credit anyway.

Ask the user once whether their Ssemble workflow accepts multiple timestamp ranges in one
selection, then set `assemble.allow_non_consecutive` to `true`/`false` in
`viral-finder.config.json` so the report recommends the right plan.

## Plan C - hot zones (optional extra credits)

A 2-hour window with >= 3 strong moments per 20 minutes is a "hot zone": the stream was
exceptionally good there and the scan probably missed some quieter gems. Sending the whole
zone (6 credits for 2 h) can be worth it. Recommend it **only** when:
- the report lists the zone, and
- the reviewed moments there average >= 80, and
- the user wants volume (many clips) more than minimum cost.

## Credit-saving checklist

1. Never send a full stream before the cheap scan.
2. Review the shortlist before spending - preliminary plans use raw signals.
3. Reject moments that fail campaign rules **before** planning (they waste footage).
4. Prefer Plan B when allowed; otherwise use Plan A blocks in order of value and stop when a
   block's strong-moment count drops.
5. Use `--credits N` to get the best plan for a fixed budget.
6. Across several videos, compare `moments_per_credit` per video and spend on the best video first.
7. If a credit has unused minutes (the report says so), review more candidates to fill it for free.

## Settings (`config/config.json` -> `assemble`)

| Key | Default | Meaning |
|---|---|---|
| minutes_per_credit | 20 | footage per credit |
| round_partial_credit_up | true | a partial block costs a full credit |
| allow_non_consecutive | "ask" | true / false once known |
| segment_lead_in / segment_tail | 20 / 10 s | context around each moment |
| min_moment_score | 70 | what counts as "strong" |
| min_strong_moments_per_credit | 3 | minimum to justify another credit |
| hot_zone_window_minutes | 120 | hot-zone size |
| hot_zone_min_strong_per_20min | 3 | hot-zone density threshold |
