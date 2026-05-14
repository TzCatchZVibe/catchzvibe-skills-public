# Decisions · cvs- 任务决策摘要

> 一条一行 · task_id link + 一句话 · 不存全文 (全文在 `_agent_inbox/helm_to_atlas/<date>_<topic>.md`)。

## 2026-05-14 (Dallas CDT)

- `cvs-2026-05-14-019` · V10 Things Working Dads Do at 3PM @ choice · 排程 17:30 CDT · skip-lint (rule 3 实测 5/6 · drawer/ceiling 不在词表) · force-fresh hotfix 加入 publish.ts
- `cvs-2026-05-14-018` · Constitution v1.0 立宪 (TZ 签字 14:18 CDT) · 3 Obsidian 文件落位 · public mirror 同步
- `cvs-2026-05-14-017` · Atlas inline B/C final · brand_voice_rules v1.1 + routing table v1.1 进 Obsidian
- `cvs-2026-05-14-015` · TZ welfare 关键修正: Dallas TX (不是 CT) · Frida 未来妻子 · low_confidence_queue 走 markdown task syntax
- `cvs-2026-05-14-013` · brand-voice-lint Q1 规则 1 改宽 `\bbest\b[^.!?]*?\bever\b` · daily-brief schema.json
- `cvs-2026-05-14-012` · Atlas web_fetch unlocked · catchzvibe-skills-public 公仓 · 7 URL handoff
- `cvs-2026-05-14-009` · Phase 2 5/5 + v2.0 协议首战 · 含 evey-bridge 验证 + Mac mini clone + persona.md + brand-voice-lint + schema + pre-lint gate

## v1.1 TODO (Atlas cvs-2026-05-14-020 拍板 · 稳定运行 1-2 周后做)

- [ ] pre-commit hook 验 task_id 格式 `cvs-<sender>-YYYY-MM-DD-NNN` (Atlas advice 2: 硬规则用 hook 不用 prose)
- [ ] auto-append task_log.md (commit hook 扫 _agent_inbox/ 新报告)
- [ ] 真 collision 1 次再触发 hook (实测 pain · 不是想象 pain)

## 关键架构决策

- **HELM/Atlas 命名** · 希腊语 (Helm 舵 + Atlas 扛地球) · 跟 Orbie/OMOU/仔仔 (mascot) 区分
- **task_id sender 前缀** (Atlas cvs-2026-05-14-020): `cvs-<sender>-YYYY-MM-DD-NNN` · sender ∈ {atlas, helm, zaizai} · 解 cvs-019 collision
- **Orbie/OMOU 合并** · 同一进程双 persona · 共享 DB · Lark→Orbie · Telegram→OMOU
- **4-Tier 架构** · Brain (HELM+Atlas) / Field (Orbie+OMOU) / Specialist (skill) / Personal (仔仔+[CLIENT_CONTACT]+未来)
- **真相源双仓** · catchzvibe-skills (private) + catchzvibe-skills-public (sanitized mirror)
- **A2A v2.0 协议** · YAML frontmatter · task_id + state + bash CDT 真时间
- `cvs-helm-2026-05-14-025` · AIO Sandbox 装 Mac mini · colima 替 Docker Desktop · 12min (vs 70min 估)
- `cvs-helm-2026-05-14-026` · mcp-agent 装 TZ MacBook · uv tool install (Python 3.12) · 4 servers connected (aio_sandbox/brave/github/fetch) · hello.py orchestrator-worker 跑通
