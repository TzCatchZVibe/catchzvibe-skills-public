---
name: brand-voice-lint
description: Brand voice 自动审查 · 给 [CLIENT] (HG 客户) 的对外文字 (Hank 剪辑指南 / [CLIENT_CONTACT] 提案 / Vicky 音乐 brief / 任何 caption + 邮件 + 文档) 跑 6 条规则 lint · 输出 YAML 报告 + 违规修复建议。配合 `caption-with-hashtags` skill 用：写完 caption 自动跑 lint · 不通过不发布。触发：用户说"过 brand voice"/"lint 这段文字"/"voice check"/"brand 审查"/"check [CLIENT] voice"。
allowed-tools: Read, Bash, Write
---

# Brand Voice Lint Skill

> 6 条规则 · 自动 lint · 防止外发文字翻车。
> 规则来自 Atlas 战略分析 (2026-05-14) · 沉淀进可执行 Python script。

## 触发场景

任何要外发给 **客户 / 团队 / 平台** 的文字 · 落地前过这个 skill：
- Hank 剪辑指南
- [CLIENT_CONTACT] / Bella / Victor 的提案 / 邮件
- Vicky 的音乐 brief
- TikTok / IG caption (跟 caption-with-hashtags skill 串)
- 公众号文章 / 小红书笔记
- 客户提案 PDF / Word

## 6 条规则 ([CLIENT] 品牌 voice · 跑这个就过)

| # | 规则 | 检查方法 | 违规例 | 合规例 |
|---|---|---|---|---|
| 1 | 不夸大功能 | 黑名单：amazing/incredible/revolutionary/best ever/100%/一定/绝对 | "BEST gummy EVER" | "Tastes like real fruit" |
| 2 | 保留撕扯感 | 必须 ≥1：peel/撕/剥/拉/strip/layer | "Just eat it" | "Peel the outer layer first" |
| 3 | 真实场景锚点 | ≥1 场景词：car/kitchen/office/walk/车/厨房/办公室 | "In a magical land" | "In Freddy's car" |
| 4 | 第二人称 | you/your/你 而非 we/us/our | "We recommend" | "You'll feel" |
| 5 | 不直接卖货 | 黑名单：buy now/link in bio/立即购买/点击购买/DM to buy | "Buy now at link!" | "Find @kozed in bio" |
| 6 | Halal 合规 | "halal" 出现必须配 "certified" ([CLIENT] 是 Halal-certified 产品) | "halal" | "halal-certified" |

## 用法

### 命令行直接跑

```bash
# 从 stdin 输入文字
echo "BEST gummy EVER, buy now!" | python3 ~/.claude/skills/brand-voice-lint/scripts/lint.py

# 从文件
python3 ~/.claude/skills/brand-voice-lint/scripts/lint.py path/to/caption.txt
```

输出 (YAML)：

```yaml
voice_score: 4/6
violations:
  - rule: 1
    name: 不夸大功能
    found: [{text: "BEST", pos: 0}, {text: "EVER", pos: 11}]
    suggestion: 用具体感官替代 · 比如 'tastes like real fruit'
  - rule: 5
    name: 不直接卖货
    found: [{text: "buy now", pos: 17}]
    suggestion: 用 'find @kozed in bio' 间接引导
brand_voice_passed: false
```

### 集成进 publishing 流程

`tiktok-publish` skill 在 type caption 之前 · 先跑 lint：

```typescript
// scripts/publish.ts (伪代码)
const lintResult = exec(`python3 lint.py`, { input: caption });
if (!lintResult.brand_voice_passed) {
  console.error("❌ Brand voice 未通过 · 修复后再发");
  process.exit(1);
}
// 通过才上传
```

## 输出 schema (机器可读)

```yaml
voice_score: <X>/6           # 通过的规则数
violations:                  # 违规列表 (可为空)
  - rule: <int 1-6>          # 规则号
    name: <规则名>             # 中文描述
    found: <匹配内容 or "missing required term">
    suggestion: <修复建议>
brand_voice_passed: <bool>   # 是否全部通过
```

## 规则演化

数据回流后 (30 天 [CLIENT] 真实 TT 表现)：
- 看哪条规则正相关 (高完播率视频都过的) → 加权
- 看哪条规则没用 (低完播视频也过) → 砍 / 重设
- 加新规则 (per Atlas/HELM 复盘)

## 与 caption-with-hashtags skill 的关系

- **caption-with-hashtags** 写 caption + 5-tier hashtag · 不验语义
- **brand-voice-lint** 验语义 · 不写
- 串联：caption-with-hashtags → 输出 caption → brand-voice-lint → pass → tiktok-publish

## 历史

- v0 起源：Atlas 2026-05-14 战略分析 · 整理 [CLIENT] 半年发布数据得出 6 条
- v1.0 落地：HELM 2026-05-15 写 Python lint + SKILL.md (你正在读)
- v1.1 计划：30 天数据回流后跟 G 池一起评估
