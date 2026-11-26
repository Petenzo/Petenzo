# How it works (and how to extend it)

```
input ─► sources.py   detect type, metadata (yt-dlp/ffprobe), download audio + captions + chat only
      ─► audio.py     ffmpeg -> 16 kHz PCM stream -> per 50 ms loudness + brightness -> per second:
                      loudness, laughter-rhythm (3-7 Hz bursts), voiced ratio
      ─► transcript.py json3/vtt/srt parsing (YouTube rolling-caption dedupe), hype words, CAPS,
                      repetition ("no no no"), laughter tags, [ __ ] bleeps, speech rate
      ─► chat.py      YouTube live_chat / TwitchDownloader / chat-downloader / CSV -> message rate,
                      reaction emotes (KEKW, LMAO, 💀...), shifted back by chat lag (8 s)
      ─► video.py     (optional, local video) scene cuts at 2 fps / 160 px
      ─► scan.py      robust z-score per signal vs THIS stream's baseline -> weighted fusion,
                      +25 % per extra agreeing signal family -> peaks (>= 45 s apart) ->
                      boundaries (build-up/aftermath, snapped to sentence start / quiet point)
      ─► verify.py    shortlist only: bounds, section download, audio cross-correlation
                      (proves the footage matches the timestamp), contact sheet + hook frame
      ─► (Claude review via reviews_todo.json)
      ─► research.py  discovery + competition search
      ─► ranking.py   9-criterion rubric, tiers, campaign rules, caption fixing
      ─► assemble.py  plans A / B / C
      ─► report.py    report.md + report.html (sections A-I)
```

## Signal score

`signal_score = 100 * (1 - exp(-v/3))` where `v` is the fused robust-z value at the peak:
v=2 -> 49, v=4 -> 74, v=7 -> 90. It means "how unusual this second is for this stream", not
"how viral". The viral score needs the review.

## Unreviewed scores stay low on purpose

Criteria the scan cannot know (context_free, international, visual_clarity) are set to 50 until
reviewed, so unreviewed moments rarely pass 70 and are never "recommended".

## Tuning

- Streamer is always loud -> raise `audio_loudness` weight less, raise `chat_*` weights.
- Too few candidates -> `candidates_per_hour` up, `peak_min_separation` down.
- Clips cut too tight -> `clip_pre_roll` / `clip_post_roll` up.
- Chat seems late/early -> `chat_lag_seconds`.

## Extending

- **New signal:** compute a per-second numpy array in `scan.scan()` and add it to `signals`
  with a weight in `config.json -> signal_weights`. It is normalised and fused automatically.
- **New source:** add detection in `sources.detect_source()` and a download path in `ingest()`;
  anything that ends with an audio file + optional captions/chat works with the rest unchanged.
- **New campaign:** copy `config/campaigns/_template.json`.
- **AI video model for the final check:** only call it on `VF clip` exports of shortlisted moments.

## Tests

`python -m pytest tests` from the skill folder.
