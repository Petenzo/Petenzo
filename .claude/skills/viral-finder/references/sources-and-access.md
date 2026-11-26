# Connecting video sources

The skill downloads **audio + captions + chat only** for the full scan, and **short low-res sections**
only for shortlisted moments. It never needs your passwords.

Run `VF doctor` first - it shows which sites this computer can reach.

## Where Claude Code runs matters

| Where | YouTube / Twitch / Drive downloads |
|---|---|
| Claude Code on **your own computer** (terminal, VS Code, desktop app) | Works (normal home internet) |
| Claude Code **cloud session** (claude.ai/code) | Often BLOCKED by the environment network policy. Either allow the hosts in the environment settings (youtube.com, www.youtube.com, googlevideo.com hosts, twitch.tv, usher.ttvnw.net, drive.google.com, drive.usercontent.google.com) or run locally. |

Tell the user plainly which case applies when `doctor` shows `BLOCKED`.

## YouTube (videos, livestream recordings)

- Paste the normal link (`youtube.com/watch?v=...`, `youtu.be/...`, `youtube.com/live/...`).
- Live **right now** -> wait until it ends and the replay is processed.
- "Sign in to confirm you're not a bot" -> log in to YouTube in Chrome/Firefox/Edge on the same
  computer, then add `--cookies-from-browser chrome` (or `firefox`, `edge`, `safari`).
  (On Windows, Chrome must be closed for cookie reading to work; Firefox is easier.)
- Members-only / private -> cannot be accessed. Ask for a public VOD or the file.
- Chat replay is downloaded automatically for past livestreams (best signal). Normal uploads have no chat.
- Rate limit (HTTP 429) -> wait 15-30 min or use cookies.

## Twitch VODs

- Paste `https://www.twitch.tv/videos/<id>`. Channel links list VODs: `VF discover "<name>" --twitch <channel>`.
- VODs expire (7 days for most, 60 days for partners) - for older streams use YouTube re-uploads.
- Subscriber-only VODs need `--cookies-from-browser` with a logged-in subscribed account.
- Twitch chat replay: yt-dlp cannot always fetch it. Best option: download chat with
  TwitchDownloader (https://github.com/lay295/TwitchDownloader, "Chat Download" -> JSON) and place the file
  next to a local video as `<video name>.chat.json`, or pass it with `VF register --chat file.json`.
  Without chat the scan still works with audio + captions.

## Google Drive

1. In Drive: right-click the video -> **Share** -> General access -> **Anyone with the link** -> Viewer -> Copy link.
2. Give that link to `/viral-finder`.
- Private file and you don't want to share it publicly: download it to your computer and give the path.
- Claude's Google Drive connector (Settings -> Connectors -> Google Drive) can find files and check
  sharing (`search_files`, `get_file_metadata`, `get_file_permissions`) but is not suitable for
  downloading multi-GB videos. Use it to locate the file and confirm sharing, then download by link.
- Very large files show a "can't scan for viruses" page; yt-dlp normally handles it. If not:
  `pip install gdown` and `gdown --fuzzy "<link>" -O video.mp4`, then use the local file.

## Local files (most reliable, most accurate)

- Any format FFmpeg reads: MP4, MKV, MOV, WEBM, TS, FLV, AVI...
- Give the full path. Tip: drag the file into the terminal window to paste its path.
- Optional sidecar files with the same base name are picked up automatically:
  `stream.en.srt` / `stream.vtt` (captions), `stream.chat.json` / `stream.chat.csv` (chat).
- Local video allows exact frame checks and `--scenes` (scene-change detection).

## Other websites (Kick, X/Twitter, Vimeo, Facebook, direct .mp4/.m3u8 links)

- yt-dlp supports 1000+ sites. Just paste the URL.
- "Unsupported URL" -> open the page in the browser (see browser-research.md) to find a direct
  video link, or download manually and pass the file.

## No footage access at all

Use a transcript with timestamps (vidIQ `vidiq_video_transcript`, YouTube "Show transcript" copied
via browser, Descript export) and `VF register`. Moments found this way are **leads only** - they
must be checked against footage before being recommended.

## Error -> what to tell the user

| Message contains | Tell the user |
|---|---|
| `403 Forbidden (agent proxy` / `Tunnel connection failed` | This environment's network blocks the site. Run locally or allow the host. |
| `Sign in to confirm` | Log into YouTube in your browser; we'll use `--cookies-from-browser`. |
| `Private video` / `members-only` | Not accessible. Need a public link or the file. |
| `HTTP Error 429` | Too many requests - wait 15-30 min. |
| `Unsupported URL` | Site not supported - download manually or find the direct video link. |
| `ffmpeg not found` | Install FFmpeg (winget / brew / apt). |
| Drive `403` / `permission` | Share as "Anyone with the link" or download locally. |
