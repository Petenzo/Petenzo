# Scoring rubric (review step)

Score each criterion **1-10** from what you actually saw (contact sheet, hook frame) and read
(transcript, chat samples). The script converts to a weighted 0-100 viral score:

| Criterion | Weight | 9-10 looks like | 1-3 looks like |
|---|---|---|---|
| hook | 15 | First 3 s already shows the reaction / chaos / a strong line | Slow build-up, menus, silence |
| entertainment | 15 | Genuinely funny / shocking / hype, people would send it to friends | Mild chuckle, routine gameplay |
| emotion | 12 | Screaming, crying-laughing, rage, disbelief | Neutral talking |
| context_free | 12 | Anyone understands it instantly | Needs stream lore / an earlier event |
| originality | 10 | No similar clip found; unusual situation | Already reposted many times / generic |
| retention | 10 | Tension until the payoff at the end | Payoff in second 2, then nothing |
| international | 10 | Visual/physical comedy, universal reaction, clear English | Slang-heavy, local references, heavy talking |
| replay | 8 | Short, punchy, loopable, quotable | Long and meandering |
| visual_clarity | 8 | Face cam + gameplay both readable, works when cropped 9:16 | Tiny facecam, dark/cluttered screen |

## Talking content (podcast profile: interviews, trading, watches, business, education)

The frames matter less, the words matter more. Translate the criteria like this:
- **hook** - a bold claim, number or question in the first 3 s ("I lost $2M because of one rule").
- **entertainment** - surprising, useful or controversial insight; a story with a payoff; real laughter.
- **emotion** - conviction, anger, shock, a heated disagreement, a big laugh.
- **context_free** - the point is complete inside the clip (setup + payoff), no "as I said earlier".
- **visual_clarity** - speaker clearly visible, works with captions in 9:16.
Best clips: one clear idea, one strong line, 20-60 s.

## Any other niche (sports, cooking, tech, expert content...)

Ask: "would the people who watch this kind of video stop scrolling for this?" For expert audiences
the best clips are non-obvious tips, expensive mistakes, strong opinions and real numbers - a calm
voice is fine. For general audiences, prefer surprise, humour and emotion.

Tiers: **S >= 85**, **A >= 75**, **B >= 65**. Only >= 70 is recommended (config `report.min_recommend_score`).
Be strict: most moments of a 10 h stream are B or C. A good stream gives roughly 5-15 S/A moments.

## Reject when

- The "excitement" is a song, an ad read, a donation alert, or a game cutscene without reaction.
- It needs too much context to make sense.
- A campaign rule fails (only when a campaign is active).
- The clip would mislead (cutting so it looks like something that didn't happen).

## Boundaries

- Start 1-3 s before the action begins (enough setup to understand, no dead air).
- End right after the payoff/reaction peak (+1-2 s of aftermath laugh).
- Typical length: 15-60 s; 60-90 s only for a story with a strong arc.
- Only change start/end to timestamps visible in the contact sheet or transcript.

## Hook text formulas (first 3 seconds, on-screen, <= 8 words)

- Disbelief: "He did NOT expect that..."
- Stakes: "One mistake ruined everything"
- Curiosity: "Wait for the cop at the end"
- Direct quote: the funniest line in quotes, if it stands alone.
Avoid clickbait that the clip doesn't deliver (misleading = campaign violation).

## Caption formula

`<what happens in plain words> <emoji?> <required mention> <required hashtags> <2-3 topic hashtags>`
e.g. `He tried to outrun the cops and instantly regretted it 😭 #gaming #funny`
or `This trader lost $40,000 in 10 minutes - here's why #trading #money`
The report auto-adds missing required mentions/hashtags for the active campaign.

## Platform choice

- **TikTok** - fastest reactions, chaotic moments, 15-35 s.
- **YouTube Shorts** - slightly longer stories, searchable topics (game name in title), 20-55 s.
- **Instagram Reels** - very visual, loopable, relatable.
- **X** - quotable lines and "you have to see this" moments; landscape is fine.
