# Viral Finder - user guide

Finds the most viral moments in long streams and videos, verifies the timestamps against the
original footage, and tells you which 20-minute footage selections to give Ssemble so every
credit produces as many strong clips as possible.

You type one command; Claude runs everything and explains the results.

```
/viral-finder Kai Cenat GTA 6 Marathon
/viral-finder https://www.youtube.com/watch?v=XXXXXXXXXXX
/viral-finder https://www.twitch.tv/videos/1234567890
/viral-finder https://drive.google.com/file/d/XXXX/view
/viral-finder C:\Users\me\Videos\stream.mp4
```

---

## 1. Install (once)

You need: **Claude Code**, **Python 3.9+**, **FFmpeg**.

**Windows** (PowerShell, inside this folder):
```
powershell -ExecutionPolicy Bypass -File .claude\skills\viral-finder\install.ps1 -Global
```
**macOS / Linux**:
```
bash .claude/skills/viral-finder/install.sh --global
```
`--global` / `-Global` copies the skill to your user skills folder so `/viral-finder` works in
any folder. Without it, the skill works when Claude Code is opened in this project.

The installer ends with a check. Everything should say `OK`.

## 2. Activate

Open Claude Code in any folder (it saves results to `viral-finder-output/` there) and type
`/viral-finder` followed by a topic, link or file. You can also just ask:
"find viral moments in this stream: <link>". If `/viral-finder` doesn't appear, restart Claude Code.

## 3. Connect video sources

| Source | What you do |
|---|---|
| YouTube | Nothing. If you see "Sign in to confirm you're not a bot", log in to YouTube in Chrome/Firefox and say "use my Chrome cookies". |
| Twitch | Nothing for public VODs. VODs expire after 7-60 days - use YouTube re-uploads for older streams. |
| Google Drive | Share the file: right-click > Share > **Anyone with the link** (Viewer) > Copy link. Or download it and give the path. |
| Local files | Give the path (drag the file into the terminal). Most reliable and most accurate. |
| Other sites | Paste the link; most video sites work. If not, download manually. |

Nothing needs your passwords. Optional Claude connectors (Settings > Connectors) that help:
**Google Drive** (find files), **vidIQ** (YouTube search + transcripts when downloads are blocked).

**Cloud sessions (claude.ai/code):** the cloud environment may block YouTube/Twitch/Drive. Either
run Claude Code on your own computer (recommended for video work) or allow those websites in the
environment's network settings.

## 4. Search for streams

`/viral-finder Kai Cenat GTA 6 Marathon` -> Claude searches YouTube (+ the campaign's Twitch
channel), lists long videos with **duration, date and links**, flags ones that don't qualify for
the campaign, and asks which to analyse.

## 5. Analyse videos

Claude runs the cheap scan on the **whole** video (no credits used):
- downloads **audio only** (~30 MB per hour) + captions + chat replay,
- detects shouting, sudden reactions, laughter, hype words, censored swearing, chat explosions,
- picks ~8 candidate moments per hour with clean start/end times,
- downloads only short low-res pieces of the best ~25, proves each timestamp by matching the audio,
- makes a 12-frame picture per moment and looks at it, scores it, writes hook + caption.

## 6. Select footage for Ssemble

The report (`viral-finder-output/<video>/report.md` and `report.html`) shows:
- **Plan A** - the best continuous 20-minute blocks (paste start-end into Ssemble),
- **Plan B** - several short moments combined into one 20-minute selection (if Ssemble lets you),
- **Plan C** - extra credits for a "hot zone" only when it's exceptionally dense,
- cost of each plan vs. sending the whole stream.

Sections of the report: A best videos, B best timestamps, C+D Ssemble selections & credits,
E number of clips, F ranking with details, G hooks & captions, H source links, I what couldn't be verified.

## 7. Minimise credit usage

- Never send a whole stream first - let the scan decide (it's free).
- Spend only after the review (a plan marked PRELIMINARY is not ready).
- Tell Claude once whether Ssemble accepts combined timestamps - Plan B is far cheaper per clip.
- Use a budget: "plan for max 5 credits".
- If a credit has unused minutes, ask Claude to review more moments to fill it for free.
- Analyse the best video first; compare "moments per credit" between videos.

## 8. Limitations

- **Signals are heuristics.** Loud/laughing/chat-spam moments are found reliably; quiet funny
  moments (deadpan jokes, visual gags with no reaction) can be missed. Hot-zone extra credits exist for this.
- **Review = sampled frames + transcript**, not watching every second. Use `clip` previews for the top picks.
- **Captions:** auto-captions can be wrong; without captions, local Whisper (optional) only
  transcribes shortlisted moments.
- **Twitch chat replay** often needs TwitchDownloader (see references/sources-and-access.md).
- **Originality** is checked against search results, never guaranteed.
- **Campaign rules** like audience location (50% US/CA/UK/AU/NZ) depend on your posting account -
  the skill cannot verify them.
- **Ssemble details** (whether combined timestamps are allowed, partial credit rounding) are
  settings you confirm; defaults assume 20 min/credit, rounded up.
- Private, members-only, subscriber-only or expired videos cannot be accessed.
- Download speed limits how fast a 10-hour stream can be scanned (the analysis itself takes minutes).

## Files

```
viral-finder/
  SKILL.md                    instructions Claude follows
  README.md                   this guide
  install.sh / install.ps1    installers
  requirements.txt
  config/config.json          all settings (weights, clip lengths, credit size)
  config/campaigns/*.json     campaign rules (kai-cenat-gta6.json, _template.json)
  scripts/vf.py               the command Claude runs
  scripts/viralfinder/        modules: sources, audio, transcript, chat, video, scan,
                              verify, ranking, research, assemble, report
  references/                 access guide, browser research, scoring rubric, credit guide
  tests/                      python -m pytest tests
```
