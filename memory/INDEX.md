# Memory Index · HELM 持久 context

> CLAUDE.md @ import 这个 · 跨 session 跨重启保留。

| 文件 | 内容 |
|---|---|
| `decisions.md` | cvs- 任务决策摘要 · 一条一行 |
| `task_log.md` | cvs- task_id 历史 · append-only |
| `tz_preferences.md` | TZ 偏好沉淀 (从 ~/.claude/projects/ auto-memory feedback 文件) |
| `environment.md` | 路径 / SSH 目标 / 工具版本 |
| `bugs_surfaced.md` | 已知 bug / skill 演化点 (lint 规则 3 / draft 检测 等) |

## 怎么用

- 启动新 session · CLAUDE.md @import INDEX.md → Claude 看到这个目录 → 按需 Read 各文件
- 每次完成 cvs-NNN 任务 · 追加一行到 `decisions.md` + `task_log.md`
- 任何 bug / 异常 → `bugs_surfaced.md` append

## 演化路线

- v1 (现在): 5 个 markdown 文件 · 手动 append
- v1.1 (本周): pre-commit hook 验 task_id 格式 + auto-append task_log
- v2 (本月): 真有 pain point 再考虑 mem0 / Letta 持久 vector store
