---
name: tiktok-publish
description: TikTok 半托管发布工作流 · 自动开 Chrome (snacks/choice 等账号 持久化登录态 cookie 长期存活) + 拉 Lark 视频 + 写 caption/hashtag → 人点 Post。配合 caption-with-hashtags skill 一起用。触发：用户说"发 V[0-9]+" / "post to TikTok" / "publish snacks" / "choice 账号发" / "open TikTok studio" / "把 X 账号打开" / "今天发个 X" / [CLIENT] 任何视频发布。也用在 Cloud / Agent SDK co-work 场景里把这个流程当成一个可复用动作。当前 v1 = 半托管 (人点 Post 反检测) · v2 schedule 全自动化待 selector 调通。
allowed-tools: Bash, Read, Write, Edit
---

# tiktok-publish · 半托管发布 skill

CatchZVibe Studio 内容流水线的最后一公里。给 HG/[CLIENT] 等客户发 TikTok 视频。

## 1 分钟概览

| 项 | 值 |
|---|---|
| **目标平台** | TikTok (US 美区) · 之后 IG/X 同模式扩展 |
| **账号管理** | Playwright persistent context · 每账号一份 cookie ~/.catchzvibe-tiktok/<account> |
| **视频源** | Lark Drive URL (Hank 上传到"待发布成片 - US") 或 本地 .mov/.mp4 |
| **caption 写作** | 调 `caption-with-hashtags` skill · 不要在这里写 |
| **发布时段** | 调 `caption-with-hashtags` skill 的 posting-time 模型 · 永不立即发 |
| **反检测** | Post 那一下留给人手点 · 视频 + caption + hashtag 全 Playwright 自动 |

---

## 当前已知账号

| account | 角色 | 用途 |
|---|---|---|
| `choice` | [CLIENT] 主号 | 哲学独白 / 情感长片 / 节日内容 (V1 V3 V5 V6 V9) |
| `snacks` | [CLIENT] 副号 | ASMR / 产品发现 / 短 hook (V2 V4 V8) |

新账号扩展：跑 `login.ts --account=<新名>` 一次 → 自动落 cookie 到 `~/.catchzvibe-tiktok/<新名>`。

---

## 触发判断

| 用户说 | 行动 |
|---|---|
| "把 X 账号打开" / "open X studio" | 跑 open-studio.ts → 用户自己上传/粘 |
| "发 V[0-9]+" / "post Vx" | 看视频找内容 → caption-with-hashtags → 开 Chrome + 给 caption |
| "schedule V[0-9]+ for <date>" | (v2 待开发) · 现状给时段建议 + 半托管发 |
| "X 账号发了 Y" (事后) | 跑 record-publish.ts 写库 |

---

## 标准工作流 (v1 半托管)

### Step 1: 找视频 + 看内容
- Lark "待发布成片 - US" 路径: `iCloud .../HG_Studio/待发布成片 - US/V<N>_<title>/`
- 或 supabase video_projects 表 `final_video_url` 字段
- 用 `ffmpeg -i <video> -vf fps=0.5,scale=480:-1 /tmp/v<N>-frames/v<N>_%02d.jpg` 抽帧 (每 2s 一帧)
- 看封面 + 关键帧 → 理解视觉锚点 + on-screen 字幕

### Step 2: 写 caption + hashtag
**调用 `caption-with-hashtags` skill** — 不在这里写。把视频内容描述喂进去，让它出 caption + 5-tier hashtag stack。

### Step 3: 决定时段
**也是 `caption-with-hashtags` skill** — posting-time 模型给推荐时段。当前 v1 没接自动排程，给用户时段建议让他手动 Schedule 或 Post Now。

### Step 4: 开 Chrome (持久化账号)
```bash
cd /Users/happyglobal_tk_team/catchzvibe && npx tsx ~/.claude/skills/tiktok-publish/scripts/open-studio.ts --account=<choice|snacks>
```
后台跑 (run_in_background) · Chrome 弹出 · 用户登录态自动恢复 · 直接到 TikTok Studio Upload 页。

### Step 5: 给用户视频路径 + caption 包
按这个格式给（用户复制贴）：

```markdown
## 📦 V<N> · <Title> · <account> 账号

**视频路径：** <Lark URL 或 iCloud 路径>

**视觉锚点：**
- <bullet 1>
- <bullet 2>

**Caption（整块复制）：**
\`\`\`
<caption body>

<hashtag block>
\`\`\`
```

### Step 6: 用户上传 + 粘贴 + 点 Post (或 Schedule)
反检测 · 这一下不自动。

### Step 7: 用户回报 TikTok URL → 写库
```bash
cd /Users/happyglobal_tk_team/catchzvibe && npx tsx scripts/tiktok-publish/record-publish.ts \
  --project=<uuid> --url=<TikTok URL> --account=<choice|snacks> --caption="<chosen caption>"
```

---

## 全自动版本（可选 · 不推荐反检测视角）

catchzvibe 里有 `scripts/tiktok-publish/publish.ts` 端到端版（拉 Lark + 上传 + 写 caption + 等人点 Post）：

```bash
cd /Users/happyglobal_tk_team/catchzvibe && npx tsx scripts/tiktok-publish/publish.ts \
  --account=<choice|snacks> \
  --lark="<Lark URL>" \
  --caption="$(cat <<'EOF'
<multi-line caption with hashtags>
EOF
)"
```

也可以 `--project=<UUID>` 让它自己拉 caption (但会用 Sonnet 4.6 generated caption · 不如手 craft)。

⚠️ 一个 Chrome 进程一个账号 · 多账号并行没问题（不同 user_data_dir）。

---

## TikTok Studio DOM 关键 selectors (供 v2 schedule 自动化用)

从 /tmp/tiktok-publish-fail-*.html 抓的 (2026-05-10)：

| 元素 | Selector |
|---|---|
| 排程区域 | `[data-e2e="schedule_container"]` |
| Post Now radio | `input[name="postSchedule"][value="post_now"]` |
| Schedule radio | `input[name="postSchedule"][value="schedule"]` |
| 日期/时间 input | `input.TUXTextInputCore-input` (readonly · 自定义 picker · click 后操作) |
| Post 按钮 | `[data-e2e="post_video_button"]` (Schedule 模式下 button text 变 "Schedule") |
| Save Draft | `[data-e2e="save_draft_button"]` |
| Discard | `[data-e2e="discard_post_button"]` |
| Caption editor | `div[contenteditable="true"]` (第一个) |
| 草稿检测 | 进上传页后 `div[contenteditable="true"]` 已可见 → 视频已上传过 |

**已知坑：**
- 日期/时间 input 是 `readonly` · 自定义 calendar/time picker · 不能 `fill()` · 要点开 widget 后导航
- 上传页可能延迟显示（draft detection 用 2s timeout 太短 · 实测要 5-8s）
- 上传完成后会弹改版提示 modal · 用 `dismissAnyModals` helper 兜底
- TikTok 用文件名预填 caption · 所以上传前要 copy 到 temp 文件改干净名

---

## 端口到 Cloud / Agent SDK

**Cloud Code / Agent SDK 环境的限制：**
1. 没有 ~/.catchzvibe-tiktok cookie 持久化目录 · 要 OAuth 或重新登录
2. 没有 catchzvibe 仓库（除非也 clone 进去）
3. 没有 Lark API 凭证 · 要带 .env

**端口最小方案：**
1. 把 `~/catchzvibe/scripts/tiktok-publish/` 整个搬进 Cloud workspace
2. 把 `.env.local` (SUPABASE + Lark API key) 设进 secrets
3. 第一次 `login.ts --account=<X>` 跑一次落 cookie
4. 之后调 `publish.ts` 跟本地一样

**或者更轻量：** Cloud 端只做 caption draft + 时段建议，本地 Mac 仍是 publish runtime（cookie + Chrome）。这条路更稳。

---

## 常见错误

| 现象 | 真因 | 修法 |
|---|---|---|
| 60s 找不到 file input | 已有草稿在 studio · draft detection 2s timeout 太短 | 升 timeout 或先 Discard 草稿 |
| caption 里出现长 token | 上传文件名含 Lark file_token · TikTok 默认预填 | 已在 publish.ts 用 makeCleanCopyForTikTok 兜底 |
| Chrome 报 "上次没正常关闭" | SingletonLock 残留 | browser.ts 已 unlink 兜底 |
| 排程 input fill 失败 | input readonly + 自定义 picker | v2 待用点击 widget 流 (上方 selector 表) |
| Top-level await error | `tsx -e` 不支持 · 用 tsx <file> | 写 /tmp/X.ts 再跑 |

---

## 配套 skills

| skill | 用途 |
|---|---|
| `caption-with-hashtags` | 写 caption + 5-tier hashtag + 时段建议 |
| `liblib-poster` | 海报 (静态宣发素材 · 不是发布动作) |

---

## 升级路线

- **v1 (now)**: 半托管 · 开 Chrome + 给 caption · 人点 Post
- **v2**: schedule 自动化通 (用 schedule_container 区域的真 selector + click-widget 导航)
- **v3**: 多账号 batch (一条命令发 N 条 · 跨账号并行)
- **v4**: 跨平台 (IG Reels / X / FB Reels 同模式 · 共用 Lark 视频源)
- **v5**: Cloud co-work 模式 (Cloud 端 plan · Mac 端 execute · 通过 webhook 桥)
