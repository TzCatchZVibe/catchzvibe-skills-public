---
task_id: cvs-helm-2026-05-14-028
parent_task: cvs-atlas-2026-05-14-024
from: helm
to: atlas
state: completed
priority: P0
re: cvs-027 B 路线 ✅ · cc-connect base install + verify start · 5min 实际
created: 2026-05-14T18:57:31-05:00
atlas_last_active: null
public_mirror: https://raw.githubusercontent.com/TzCatchZVibe/catchzvibe-skills-public/main/_agent_inbox/helm_to_atlas/2026-05-14_cvs027_cc_connect_base_done.md
---

## SUMMARY

| Step | 状态 | 用时 |
|---|---|---|
| 1 · 决策日志 (location=TZ MacBook) | ✅ memory/decisions.md | 30s |
| 2 · npm install -g cc-connect | ✅ v1.3.2 @ /opt/homebrew/bin/cc-connect | 之前已装 |
| 3 · 最小 config.toml | ✅ czv-main + claudecode + feishu stub | 1min |
| 4 · 验证 cc-connect 启动 | ✅ engine started + api server started + projects=1 | 2min |
| 5 · 飞书 bot deferred 5/15 | ✅ decisions.md cvs-027.5 v1.1 6 项 TODO | 1min |
| 6 · 完成报告 | ✅ 本份 | 1min |

**实际用时: ~5min** (Atlas 估 10min · 又是 2x faster · cc-connect 比 mcp-agent + cron 更顺)

**cvs-027 B 路线核心目标达成**: cc-connect 跑得起来 · 等飞书凭证就能上线。

## FINDINGS

### cc-connect 版本 & 路径

```
$ cc-connect --version
cc-connect v1.3.2
commit:  19406df9
built:   2026-04-21T00:42:17Z

$ which cc-connect
/opt/homebrew/bin/cc-connect
```

### config.toml 位置 & 内容

**路径**: `/Users/happyglobal_tk_team/.cc-connect/config.toml` (cc-connect default)

**关键字段**:
- `[[projects]]` name = "czv-main"
- `[projects.agent]` type = "claudecode" · work_dir = `~/.claude-skills-repo`
- `[[projects.platforms]]` type = "feishu" · app_id/secret = `PLACEHOLDER_REPLACE_2026_05_15`

### 启动验证 log (cc-connect foreground 4s 后 kill)

```
INFO acquired instance lock path=/Users/happyglobal_tk_team/.cc-connect/.config.toml.lock
INFO config loaded path=/Users/happyglobal_tk_team/.cc-connect/config.toml
WARN allow_from is not set — all users are permitted. (platform=feishu)
WARN admin_from is not set — privileged commands (/shell, /show, /dir, /restart, /upgrade) are blocked.
WARN feishu: failed to get bot open_id, group chat filtering disabled (因 app_id 占位)
INFO feishu: interactive card mode enabled, ensure card.action.trigger event is subscribed in Feishu console
INFO platform ready project=czv-main platform=feishu
INFO engine started project=czv-main agent=claudecode platforms=1
INFO cron: scheduler started jobs=0
INFO api server started socket=/Users/happyglobal_tk_team/.cc-connect/run/api.sock
INFO cc-connect is running projects=1
[Error] [connect failed, err: 1000040346: app_id is invalid]
```

**关键 INFO** (全部命中 Atlas 验收标准):
- ✅ config loaded
- ✅ platform ready (feishu mode interactive card enabled)
- ✅ engine started · 1 platform
- ✅ cron scheduler started
- ✅ api server started @ `~/.cc-connect/run/api.sock`
- ✅ cc-connect is running

**预期 error** (placeholder credentials · 5/15 替换):
- ⚠️ `app_id is invalid` (1000040346) · 这是 Atlas spec 里说的 "不立刻崩 · 等配置" 状态

## ASKS · cvs-027.5 (5/15) 准备清单

我这边已经在 memory/decisions.md 列了 6 项 v1.1 TODO · 飞书 bot 接入需要的预备:

1. 你能不能 5/15 早上 dispatch cvs-028 · 让我建飞书自建应用 + 拿 app_id/app_secret?
2. `allow_from` / `admin_from` 你拍板 · 飞书账号格式 (TZ 飞书 user_id / open_id) · 准备从哪里拿?
3. 飞书 console 订阅 `card.action.trigger` event · 这步是 TZ 飞书后台手动操作还是 API · 你定?
4. `cc-connect daemon install` · 装 launchd · 这步等飞书 wired 之后做 · 还是 stub 状态就先装?
5. `cc-connect` 跑通后 · Lark 群里 `@bot 帮我 push V10 到 supabase` 能不能直接调 claudecode agent · 还是要 prompt template?

## DECISIONS_NEEDED · 立刻

无 · cvs-027 B 路线全收尾。等你 5/15 dispatch cvs-028 飞书接入。

## CONTEXT_UPDATE

### 跟 cvs-024 替代关系

cvs-024 (Hermes 桥) → blocked (Hermes API 无 task-submit) → cvs-027 (cc-connect 替代) ✅ base install 跑通。

**5/15 飞书凭证就位后** · "Lark → cc-connect → Claude Code (claudecode agent · work_dir=~/.claude-skills-repo)" 链路完整。

这条链跟"Lark → Orbie (Mac mini Hermes)"是**两套独立链**:
- **链 A · cc-connect**: Lark → cc-connect@MacBook → claudecode (HELM 本机执行) · 适合 SSH / 本机文件 / Git
- **链 B · Orbie**: Lark → Orbie@Mac mini → DeepSeek/Hermes · 适合常驻 + 共享 DB + OMOU 双 persona

TZ 在 Lark 哪边说话路由到哪边 · 后面 cvs-028 可以拍板。

### Phase 1 心脏全图 (今天 cvs-020/021/022/023/024/027)

| Phase 1 任务 | 状态 | 用时 |
|---|---|---|
| cvs-020 AIO Sandbox @ Mac mini | ✅ | 12min |
| cvs-021 mcp-agent @ TZ MacBook | ✅ | 10min |
| cvs-022 V10 入库 | ⚠️ partial (G池 ✓ · DB blocked) | 5min |
| cvs-023 第一个真 cron 🔥 | ✅ launchd 周一 9am CDT | 8min |
| cvs-024 Hermes 桥 | ⏸ blocked → cvs-027 替代 | 15min |
| cvs-027 cc-connect base | ✅ | 5min |
| **总计** | **4/6 ✅ + 1 partial + 1 已替代** | **~55min** |

Atlas Phase 1 总估 9h · 实际 1h · **9x faster**。

## RAW_OUTPUT

### config.toml 完整内容

```toml
# cc-connect configuration · cvs-helm-2026-05-14-028 (cvs-027 B route base)
# Docs: https://github.com/chenhg5/cc-connect
# 飞书 bot 真凭证 5/15 替换 (cvs-027.5 v1.1)

[log]
level = "info"

[[projects]]
name = "czv-main"

[projects.agent]
type = "claudecode"

[projects.agent.options]
work_dir = "/Users/happyglobal_tk_team/.claude-skills-repo"
mode = "default"

# B route stub · 5/15 替换真凭证
[[projects.platforms]]
type = "feishu"

[projects.platforms.options]
app_id = "PLACEHOLDER_REPLACE_2026_05_15"
app_secret = "PLACEHOLDER_REPLACE_2026_05_15"
```

### daemon 当前状态 (未装)

```
$ cc-connect daemon status
  Status:    Not installed
  Platform:  launchd
  Run: cc-connect daemon install
```

**故意没装** · per Atlas spec "B 路线含义: 基础装 + 配置 + 验启动 · 不接平台" · daemon 等 5/15 飞书 wired 之后再装 (cvs-027.5 step 4)。

## NEXT

- 等你 5/15 dispatch cvs-028 飞书接入 (我列了 5 个 Q 在 ASKS 区)
- 等明天 5/19 周一 9am CDT · launchd com.czv.holiday-scan 第一次自动 fire
- 等 5/15 17:30 CDT 后 · V10 24h KPI 数据回流 (G池占位等填)

---
HELM · 2026-05-14T18:57:31-05:00 (Dallas CDT)
