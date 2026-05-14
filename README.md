# catchzvibe-skills

> Production-ready [Claude Code](https://claude.com/code) skills for short-form video content pipelines.
> Public mirror of internal CatchZ Studio tooling, sanitized of client-specific data.

## Skills

| Skill | Purpose |
|---|---|
| [caption-with-hashtags](skills/caption-with-hashtags/SKILL.md) | Caption writing rules + 5-tier hashtag stack + posting-time model (TikTok 2026 data) |
| [tiktok-publish](skills/tiktok-publish/SKILL.md) | Semi-managed TikTok upload via Playwright persistent context (one cookie per account) |

## Install

```bash
git clone https://github.com/TzCatchZVibe/catchzvibe-skills-public.git ~/.claude-skills-public
~/.claude-skills-public/install.sh
```

Symlinks `skills/*` into `~/.claude/skills/` (Claude Code's standard skill discovery path).

## Architecture

- **`caption-with-hashtags`** encodes a 5-tier hashtag model (Branded / Niche / Category / Mood-Audience / Discovery) plus a posting-time strategy backed by Sprout Social and Buffer's 2026 data studies.
- **`tiktok-publish`** wraps a half-automated browser flow: auto-upload + auto-caption + human clicks Post (anti-detection).

## Philosophy

> "Skills are procedural memory — codified ways your team solves recurring problems. Make them readable by humans, callable by agents."

## License

MIT-style internal use. Adapt freely.

## Maintainer

[CatchZ Studio](https://github.com/TzCatchZVibe)
