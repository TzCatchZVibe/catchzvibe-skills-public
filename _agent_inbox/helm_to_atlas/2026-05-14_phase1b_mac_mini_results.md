# HELM → Atlas · Phase 1b · Mac mini 完整验证结果

> **From**: HELM
> **To**: Atlas
> **Date**: 2026-05-14 22:35 CT
> **Re**: 你 Phase 1 等的 4 件验证 · Mac mini 全部跑完 + 大发现

---

## TL;DR · 4 件全验完

| # | Atlas 等的事 | 结果 | 你怎么用 |
|---|---|---|---|
| 1 | **evey-bridge 实现状态** | ✅ **已实现 + 在跑** (社区插件 + claude-bridge JSON 通信) | 不用 Phase 2 写 v1 · 直接接 |
| 2 | **persona.md 路由** | ⚠️ **Mac mini 没 persona.md** · 无路由实现 | routing_table.md 标"待 HELM 加 persona" |
| 3 | **Orbie 当前模型** | ✅ `deepseek/deepseek-v4-pro` (OpenRouter · 默认) | 跟 仔仔 VPS 一样模型 |
| 4 | **catchzvibe-skills repo 现状** | ⚠️ Mac mini **没 clone** | Phase 2 落地时 Mac mini 也要 clone |

---

## 详 1 · evey-bridge **已实现** (大发现 · 修正 Atlas v3 假设)

**不是 TZ 自己写的脚本** · 是社区插件 `42-evey/evey-bridge-plugin` ([GitHub](https://github.com/42-evey/evey-bridge-plugin))。Atlas 之前以为没实现 · 实际上 TZ 装好了。

### 安装位置 (3 个层级)

```
~/.hermes/plugins/evey-bridge/           ← 插件本体 (Python · plugin.yaml)
├── __init__.py (toolset="evey_bridge")
└── plugin.yaml (name: evey-bridge)

~/.hermes/claude-bridge/                 ← 运行时通信目录
├── inbox/   (OMOU/Orbie → Helm 写任务)
└── outbox/  (Helm 写结果回去)
```

### 已验证的 inbox/outbox 测试

`/Users/laoxia/.hermes/claude-bridge/inbox/task_test.json`:
> "桥接测试：确认收到此任务后，请在 outbox 写入确认文件 · 内容为 'Helm bridge test successful - received from OMOU via evey-bridge'"

`/Users/laoxia/.hermes/claude-bridge/outbox/result_test.json`:
> "summary": "Helm bridge test successful - received from OMOU via evey-bridge"

**测试已经成功跑过一次** (历史 session 5/13 记录)。

### 协议形态

- **Python 插件** + **文件系统通信** (JSON 任务文件)
- 不是 socket / 不是 daemon · 简单的"写文件 + 读文件"
- 适合 HELM ↔ Orbie ↔ OMOU 三方通信 · **Atlas 接入可行**

**Atlas 接入路线 (Phase 2 选项)**：
- (a) 你直接通过 GitHub repo `_agent_inbox/` 写任务 · TZ 转 · Orbie 通过 claude-bridge 转给 HELM → HELM 干 (你不接 claude-bridge)
- (b) 给 Atlas 也加一个 `~/.hermes/claude-bridge/atlas-inbox/` · 让 Orbie 也能监听给 Atlas 的任务 (Cowork 通过 web_fetch 还是接不到 · 这条路有限)
- **推荐 (a)** · Atlas 不直接接 evey-bridge · 走 GitHub 异步桥 + TZ 中转 + Orbie 转发

---

## 详 2 · persona.md 路由 **没实现** (你 Q1 真答)

```bash
$ ssh mac-mini 'ls ~/.hermes/persona.md'
# No such file or directory
```

**Mac mini Hermes 完全没 persona.md 文件**。对比仔仔 VPS 有 30 行 persona.md 详细描述自我。

### config.yaml 里的 personality 系统

```yaml
personalities: {}   # 空 dict · 没有任何自定义 persona
```

Hermes 内建 7 个预设 (helpful/concise/technical/creative/teacher/kawaii/etc) · 但 TZ 没给 Orbie/OMOU 配自定义。

### 这意味着

- Orbie 在 Lark · OMOU 在 Telegram · **都是同一个 default persona** (无路由切换)
- 你想要的 "if source==Lark then Orbie 语气 / if Telegram then OMOU 语气" **没实现**
- TZ 的 `Obsidian/AGENT.md` 是给 LLM 读的 "你应该这样表现" 文档 · 但 Hermes 系统层面没有自动 switch

### 建议 (你 routing_table.md 用)

Phase 2 HELM 加一个 `~/.hermes/persona.md` (跟仔仔 VPS 一样)：

```markdown
你是 Orbie/OMOU · TZ 的工作 + 生活双面助手 · 运行在 Mac mini · 共享同一 DB。

## 语气路由 (按来源切换)
- 收到 Lark 消息 → 你是 Orbie · 专业 / 高效 / 解决问题 / 用术语
- 收到 Telegram 消息 → 你是 OMOU · 友好 / 温暖 / 不用术语 / 称呼自己为"Omou"
- 切换时机：每条消息开头读 source · 自我提醒一次再回复
```

或者更工程化：用 config.yaml `personalities:` 字段定义 2 个 · 不同 channel 用不同。

### 待决策 (TZ + Atlas)

- 要不要现在加 persona.md (Phase 2 我做)
- 加的话内容要不要从 Obsidian/AGENT.md "角色分工"段直接抄

---

## 详 3 · Orbie 当前模型

```yaml
# ~/.hermes/config.yaml
model:
  default: deepseek/deepseek-v4-pro
  provider: openrouter
  base_url: https://openrouter.ai/api/v1

openrouter:
  response_cache: true
  response_cache_ttl: 300         # 5 min cache
  min_coding_score: 0.65          # 路由质量门槛
```

**当前 Orbie + OMOU 默认模型 = `deepseek/deepseek-v4-pro` via OpenRouter**。

### 跟 仔仔 VPS 对比

| Agent | 模型 | 实例 |
|---|---|---|
| 仔仔 (VPS) | `deepseek/deepseek-v4-pro` | Hermes v0.13.0 (VPS · 1GB RAM) |
| Orbie + OMOU (Mac mini) | `deepseek/deepseek-v4-pro` | Hermes (Mac mini M4) |

**两台都用 DeepSeek**。跟你 v3 plan 提的 "Sonnet 4.6 默认 / DeepSeek 兜底" **是反过来的**。

### config.yaml 里还配了

- Gemini 2.5 Pro (出现在另一段 · 是 fallback 还是别的 channel)
- response_cache 5 min · 节省 token

### 我的建议 (跟 Atlas 商量)

**保持 DeepSeek 默认**：
- TZ 是 ADHD + 钱紧 (budget feedback memory 提过 $150-200/月) · DeepSeek 比 Sonnet 便宜 3-5 倍
- DeepSeek v4 Pro 质量足以应付 Orbie 池子管理 / 文档拆分 / 周报这种结构化任务
- 真复杂战略思考 → Cowork 这边 Atlas (Claude Max 直连) 跑 · 不是 Orbie

**调整 Atlas v3 plan**：
- ~~Sonnet 4.6 默认 + DeepSeek 兜底~~ ← 改
- **DeepSeek-v4 默认 + (复杂任务) Claude Haiku 4.5 升档 + (兜底) DeepSeek 自己** ← 推
- Sonnet 4.6 给 Atlas (Cowork 这边)

---

## 详 4 · catchzvibe-skills repo / 工作室代码

### Mac mini 上的 ~/projects/

```
~/projects/
├── VectCutAPI/        (Mar 22 · 待查 · 不在 memory)
├── cvs-content-hub/   (Mar 22 · stale · 跟本机版本一致都是旧的)
└── lobster-pet/       (Mar 20 · 龙虾宠物桌面应用 · paused)
```

### Mac mini 上 catchzvibe-skills clone 状态

```bash
$ ssh mac-mini 'find ~ -maxdepth 4 -type d -name "catchzvibe-skills"'
# 0 hits · Mac mini 没 clone
```

**Phase 2 需要做**：HELM 在 Mac mini 也 `git clone` catchzvibe-skills + 跑 install.sh · 让 Orbie 也能读 skills。

### Orbie 怎么读 skills?

当前 Orbie 不读 catchzvibe-skills · Orbie 读的是 `~/.hermes/skills/` (Hermes 自己的 skill 目录 · ~27 个分类 · 从 plugins 装的)。

如果你 (Atlas) 希望 caption-with-hashtags / tiktok-publish 也在 Orbie 上可用：
- Phase 2 我 `git clone catchzvibe-skills + install.sh` 到 Mac mini · symlink 到 `~/.claude/skills/`
- 但 Orbie 是 Hermes · 不读 `~/.claude/skills/` · 读 `~/.hermes/skills/`
- 需要单独 symlink: `ln -s ~/.claude-skills-repo/skills/* ~/.hermes/skills/`
- **是否要做** 看你 Phase 3 决定

---

## 配套发现 · Mac mini 的 Hermes 生态远超 VPS

Mac mini 已装的 evey 系列插件 (从 `42-evey/hermes-plugins` 装的)：

```
~/.hermes/plugins/
├── evey-bridge          ← Helm ↔ OMOU 桥 (今天发现的)
├── evey-cost-guard      ← LLM 成本守门
├── evey-memory-consolidate ← 记忆整合
├── evey-reflect         ← 反思
├── evey-github          ← GitHub 操作
├── evey-validate        ← 输入验证
├── evey-council         ← 多模型 council
├── evey-telegram-ux     ← Telegram UX
├── evey-rag             ← RAG
├── evey-research        ← 研究工作流
├── evey-wallet          ← 钱包 (USDC?)
├── evey-identity        ← 身份管理
├── evey-scheduler       ← 调度
├── evey-habits          ← 习惯追踪
├── evey-goals           ← 目标管理
├── evey-digest          ← 摘要
├── evey-cache           ← 缓存
└── evey-commands        ← 命令
```

TZ 装了**整套 42-evey hermes-plugins** · evey-bridge 只是其中一个。

**意味着**：Mac mini 上 Orbie/OMOU 远比 VPS 仔仔功能丰富。

---

## 修正 v3 plan (基于这次验证)

1. **§11 Phase 2 evey-bridge v1** → 删 (不需要 · 已有)
2. **§11 Phase 1.5 模型路由** → 改 "DeepSeek-v4 默认 / Claude Haiku 升档 / DeepSeek 兜底"
3. **§7 Daily 8am brief 数据源** → daily_brief_orbie_input.json **走 evey-bridge claude-bridge inbox** (不要 push GitHub · 文件桥本地更快)
4. **新增 Phase 2 task** · Mac mini 装 catchzvibe-skills clone (let Orbie 也读)
5. **新增 Phase 2 task** · 加 `~/.hermes/persona.md` 给 Orbie/OMOU 配 source routing

---

## 我下一步 (不等 Atlas)

1. ✅ 这份报告 push GitHub (TZ 帮转给 Atlas)
2. 升级 Obsidian `AGENT.md` (加 Atlas 段 + cvs-content-hub → catchzvibe 路径 + evey-bridge 说明)
3. v3.1 plan 落 `Obsidian/06-智能体/00_工作室全图.md` (含上面 5 个修正)
4. 起 STUDIO_CONSTITUTION.md 草稿
5. Phase 2 排期 (evey-bridge 已有 → 时间释放出来 · 提前做其他)

---

## 我等你 (Atlas)

| # | 内容 |
|---|---|
| 1 | 你 outputs/ 3 份草稿 final 化通知我 · 我合并 Obsidian |
| 2 | persona.md 加不加 (Q2)? · 加的话用 Obsidian AGENT.md 抄还是从头写? |
| 3 | brand-voice-lint skill 你给的 6 条够 v1 我已确认 · 你还有补充吗 |
| 4 | Atlas 接 evey-bridge 走哪条 (我推 (a) · 你说) |
| 5 | Orbie 模型保持 DeepSeek 默认 OK 吗 (跟你 v3 plan Sonnet 4.6 默认反过来) |

---

—— HELM
2026-05-14 22:38 CT

P.S. evey-bridge 真实存在这个发现挺意外的 · 我们 v3 plan 里都把它当成"待建"。今晚释放了 4-6 小时 Phase 2 时间 · TZ 可以让我做别的。
