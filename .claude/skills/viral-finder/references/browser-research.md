# Browser & web research

Use these when `VF discover` / `VF competition` are blocked or give thin results, and for
platforms yt-dlp search does not cover (TikTok, X, Instagram). Always tell the user which method
you used and what you could not access.

## Tool priority

1. `VF discover` / `VF competition` (yt-dlp, free, structured).
2. `WebSearch` tool - quick, no login. Good for finding VOD links, campaign briefs, news of viral moments.
3. vidIQ connector, if connected (load with ToolSearch "vidiq"):
   `vidiq_youtube_search` (find videos), `vidiq_channel_videos` (a channel's uploads/streams),
   `vidiq_video_transcript` (timestamped transcript when downloads are blocked),
   `vidiq_instagram_tiktok_outlier_search` / `vidiq_tiktok_profile_videos` (what is already viral).
   These may use the user's vidIQ quota - mention it before heavy use.
4. Browser automation (Claude in Chrome or the built-in browser) - read the matching browser skill
   first. Use it for pages that need scrolling/JS (Twitch archive pages, TikTok search).
   Never log in on the user's behalf; ask them to log in themselves if needed.

## Finding streams (discovery)

Queries that work:
- `"<creator>" "<game>" full stream` , `"<creator>" "<game>" VOD`, `"<creator>" <game> day 1`
- Channel pages: `youtube.com/@<channel>/streams` (newest livestream replays),
  `twitch.tv/<channel>/videos?filter=archives` (past broadcasts; expire after 7-60 days)
- Fan VOD archive channels often re-upload full streams - prefer the official channel when available.

For each video record: title, URL, **duration**, upload/stream date, channel, whether chat replay
exists. Prefer: full-length (> 2 h), official, eligible date, has chat replay.

## Competition / repost check

For each top moment:
- YouTube: `"<creator>" <key quote or event>` filtered to Shorts (`&sp=EgIYAQ%3D%3D` = under 4 min).
- TikTok: search `<creator> <event>` in the browser; note view counts of matching clips.
- X: `"<creator>" <event> min_faves:500`.
Classify: **none found / few (1-2) / many (3+)**, and save evidence links into the review notes.
Wording in the report: "No similar clip found in the top results we checked on <platforms> on <date>"
- never "original" or "nobody has posted this".

## Campaign briefs

When the user names a campaign, look for its official brief (campaign platform page, Discord, Whop,
Clipping platform) and copy the rules into a campaign JSON. If you cannot access it, ask the user
to paste the rules. Never guess rules.

## Things the browser must NOT be used for

- Downloading copyrighted footage through screen recording.
- Logging in, accepting terms, or posting on the user's behalf.
- Faking engagement in any way.
