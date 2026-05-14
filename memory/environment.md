# Environment · 路径 / SSH / 工具版本

## 本机 (TZ MacBook)

- macOS · Darwin 25.3.0 arm64
- Home: `/Users/happyglobal_tk_team/`
- iCloud: `~/Library/Mobile Documents/com~apple~CloudDocs/`
- Obsidian vault: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/`
- VS Code · Claude Code extension · 这个 session 工作

## Remote · SSH 别名 (`~/.ssh/config` 已配)

| Alias | Host | User | Auth | 服务 |
|---|---|---|---|---|
| `hank-vps` | [VPS_HOST] | root | SSH key (catchzvibe-agents.pub) | 仔仔 (Hermes) |
| `mac-mini` | [MAC_MINI_TS] (Tailscale) | laoxia | Tailscale SSH passwordless | Orbie/OMOU (Hermes) |

## 项目

- **catchzvibe-skills 私仓**: `~/.claude-skills-repo/` (this · HELM 本职)
- **catchzvibe 主仓**: `~/catchzvibe/` (Next.js 16 · catchzvibe.studio · publish.ts 在这)
- **iCloud 素材**: `~/Library/.../HG_Studio/{待发布/已发布}成片 - US/`

## TikTok 账号 cookies (Playwright persistent context)

- `~/.catchzvibe-tiktok/choice/` ([CLIENT] 主号)
- `~/.catchzvibe-tiktok/snacks/` ([CLIENT] 副号)

## API Keys (~/.[UPSTREAM_PLATFORM]/.env)

- BRAVE_API_KEY (web search)
- NOTION_API_KEY (Notion MCP)
- (敏感 · 不出本文件 · 仅引用位置)

## GitHub repos

- private: `github.com/TzCatchZVibe/catchzvibe-skills`
- public: `github.com/TzCatchZVibe/catchzvibe-skills-public`
- 主仓: `github.com/TzCatchZVibe/catchzvibe` (was renamed independent-site-1.0 历史 · 现仍接 catchzvibe push)
- 独立站 v2: `github.com/TzCatchZVibe/independent-site` (Vercel deploy 源)

## 关键 commands

- 发 [CLIENT] 视频: `/open-choice` 或 `/open-snacks`
- 跑 brand-voice-lint: `echo "..." | python3 ~/.claude/skills/brand-voice-lint/scripts/lint.py`
- Discard TikTok 草稿: `npx tsx ~/catchzvibe/scripts/tiktok-publish/discard-draft.ts --account=choice`
- Sanitize → public: `~/.claude-skills-repo/sanitize.sh && cd ~/.claude-skills-repo-public && git push`

## Hermes (远程 agent)

- 仔仔 VPS: Hermes v0.13 · DeepSeek-v4-Pro · Brave search backend · Lark gateway
- Mac mini: Hermes (version 同) · DeepSeek-v4-Pro · 18 个 evey plugins · claude-bridge (Helm ↔ OMOU)
