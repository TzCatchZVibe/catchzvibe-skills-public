# Bugs Surfaced · 已知 bug / skill 演化点

> 实操中发现的真问题 · 等 Atlas/HELM 决策怎么修。
> 修完移到 `decisions.md`。

## 待定 (Open)

### Bug-001 · brand-voice-lint rule 3 词表窄

- **发现**: cvs-2026-05-14-019 (V10)
- **现象**: Atlas 写 "ceiling/drawer/3pm/email" 全是合理日常场景锚点 · lint 报 rule 3 missing
- **当前词表**: car/kitchen/office/walk/commute/desk/couch/driveway/车/厨房/办公室/通勤/沙发
- **建议扩词**: `ceiling/drawer/email/afternoon/morning/evening/\d+(am|pm)/workday/meeting/天花板/抽屉/邮件/下午/早上`
- **等**: Atlas Q1 拍板

### Bug-002 · publish.ts 草稿检测 vs discard-draft.ts 不一致

- **发现**: cvs-2026-05-14-019 (V10 第一次跑)
- **现象**: publish.ts 用 `div[contenteditable="true"]` 2s timeout 报"检测到草稿" · discard-draft.ts 用 `[data-e2e="discard_post_button"]` 3s timeout 报"没草稿"
- **建议**: 统一用 `discard_post_button` · 只有真有草稿时才出现
- **当前 workaround**: `--force-fresh=true` flag (Atlas dispatch 后默认 true · per CLAUDE.local.md)

### Bug-003 · task_id collision (HELM + Atlas 各用 cvs-019)

- **发现**: 2026-05-14
- **现象**: HELM 发 V10 用了 cvs-2026-05-14-019 · Atlas 派 memory 系统也用 cvs-2026-05-14-019
- **建议**: 加 sender 前缀 (`helm-019` / `atlas-019`) · OR 共享递增 counter
- **等**: Atlas 拍板

## 已修 (移到 decisions.md 即可)

- ~~lint rule 1 `best ever` 跨词不 catch~~ · cvs-013 改 `\bbest\b[^.!?]*?\bever\b`
- ~~sanitize.sh 漏 .json/.py~~ · cvs-015 加 *.json *.py 进 find
- ~~sanitize.sh .git/ 误报 residue~~ · cvs-015 加 --exclude-dir=.git
- ~~Constitution _待审 → 正式位置漏 mv~~ · cvs-018 完成
