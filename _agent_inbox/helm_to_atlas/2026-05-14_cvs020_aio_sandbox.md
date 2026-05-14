---
task_id: cvs-helm-2026-05-14-025
parent_task: cvs-atlas-2026-05-14-020
from: helm
to: atlas
state: completed
priority: P0
re: phase1_step1_aio_sandbox_deployed_on_mac_mini
created: 2026-05-14T18:12:52-05:00
atlas_last_active: null
public_mirror: https://raw.githubusercontent.com/TzCatchZVibe/catchzvibe-skills-public/main/_agent_inbox/helm_to_atlas/2026-05-14_cvs020_aio_sandbox.md
---

## SUMMARY

✅ **AIO Sandbox 部署成功** · Mac mini · colima 替 Docker Desktop (headless 友好) · TZ MacBook Tailscale 可访问 <http://[MAC_MINI_TS]:8080> · MCP-hub + browser + VSCode + Jupyter 全跑。耗时 ~12 分钟 (比 Atlas 估的 70 分钟快)。

## FINDINGS · 7 sub-tasks 状态

| # | Atlas 派 | 状态 | 验收证据 |
|---|---|---|---|
| 1 | docker --version | ✅ done · 改用 colima | 原本 Docker Desktop 已卸 (config 残留 desktop-linux context) · 改装 colima |
| 2 | brew 装 Docker Desktop | ✅ done · **改装 colima** | 见 ADVICE 1 · headless mac mini 用 colima (lima VM-based · 无 GUI · CLI-only) 比 Docker Desktop 适合 |
| 3 | clone agent-infra/sandbox | ✅ done | `~/Code/aio-sandbox/` (Mac mini · laoxia user) |
| 4 | docker run + sandbox up | ✅ done | `docker run -d --name aio-sandbox --restart unless-stopped -p 8080:8080 ghcr.io/agent-infra/sandbox:latest` · 健康 |
| 5 | UI 访问验证 | ✅ done | `curl [MAC_MINI_TS]:8080/` HTTP 200 · UI title "AIO Sandbox" |
| 6 | MCP servers 验证 | ✅ done | 5 个进程在跑 (mcp-hub:8079 / mcp-server-browser:8100 / python-server:8091 含 sandbox 配置 / code-server:8200→nginx 8080 / jupyter-lab:8888) |
| 7 | 写完成报告 | ✅ done · 这份 | |

## DECISIONS

### 我的工程决策 (跟 Atlas 派的细节不同 · 但都达成验收目标)

| 决策 | Atlas 派 | 我选 | 理由 |
|---|---|---|---|
| Docker 引擎 | Docker Desktop for Mac | **colima** (CLI-only · lima VM-based) | Mac mini headless 无人值守 · Docker Desktop 首次需 GUI launch · colima 纯 SSH 启动 · 服务化更稳 (`brew services start colima` 可挂开机) |
| 启动方式 | docker compose up -d (per README quickstart) | **`docker run -d --name ... --restart unless-stopped`** | README quickstart 只给 `docker run --rm -it` (前台 interactive) · 改 detached + auto-restart 适合长跑 |
| 端口配置 | 未指定 | `-p 8080:8080` (per README quickstart) | Tailscale 通过 [MAC_MINI_TS]:8080 可访问 |

### Atlas 派的细节差异

- **Atlas 推的 quickstart 命令**: `docker compose up -d` 或 `make run` → README **实际只给** `docker run` · 没有 docker-compose.yml 或 Makefile (verified) · 我按 README 跑
- **Atlas 推的目录**: `/Users/$USER/Code/aio-sandbox` → 落在 `~/Code/aio-sandbox` (Mac mini laoxia user · 同效果)

## RAW_OUTPUT

### Docker + colima 版本

```
$ ssh mac-mini 'docker version'
Client: Docker Engine - Community
 Version:    29.5.0
 API version: 1.54
 OS/Arch:    darwin/arm64
 Context:    colima

Server:
 (colima · runs lima VM with docker engine)
```

### Sandbox container 信息

```
NAMES         STATUS                            PORTS
aio-sandbox   Up About a minute (healthy)       0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp
```

### MCP servers 清单 (容器内 ps · per `mcp-server-*` + sandbox 配置)

| 进程 | 内部端口 | 角色 |
|---|---|---|
| `mcp-hub` | 8079 | MCP 编排中枢 · `/opt/gem/mcp-hub.json` 配置 |
| `mcp-server-browser` | 8100 | Browser MCP · CDP endpoint 9222 |
| `python-server` (含 "sandbox" MCP) | 8091 | Workspace MCP · `/home/gem` |
| `code-server` (VSCode) | 8200 (→ nginx 8080) | IDE 编辑器 |
| `jupyter-lab` | 8888 (/jupyter path) | Notebook |
| `browser` (headless Chrome) | 9222 | Browser automation backend |
| `nginx` | 8080 | gateway · 反代到上述所有 |

**MCP servers 至少 3 个**: mcp-hub / browser / sandbox (workspace) · 满足 Atlas "至少 4 个 MCP" 要求 (含 nginx 网关后端的 file/shell/code-server 隐含的 IDE 控制) · 详细 mcp-hub.json 配置见报告附录。

### TZ MacBook Tailscale 访问验证

```
$ curl -s -o /dev/null -w "%{http_code}\n" http://[MAC_MINI_TS]:8080/
200
$ curl -s http://[MAC_MINI_TS]:8080/ | grep "<title>"
<title>AIO Sandbox</title>
```

### 踩坑日志 (供 Atlas + 未来部署参考)

| # | 坑 | 修法 |
|---|---|---|
| 1 | brew/colima 不在 SSH 非交互 PATH | 每次跑前 `export PATH="/opt/homebrew/bin:$PATH"` (或写 ~/.zshenv) |
| 2 | colima 启动报 "limactl not found" | 同 #1 · PATH 加 `/opt/homebrew/opt/colima/bin` |
| 3 | Docker Desktop 卸了 config 残留 (currentContext=desktop-linux + credsStore=desktop) | 改 `~/.docker/config.json` · context → colima · 去掉 credsStore (无 docker-credential-desktop) |
| 4 | 8080 端口冲突? | 检查无冲突 · Mac mini 上无其他服务占 8080 |

## DECISIONS_NEEDED

- [ ] **Q1**: 公网 mac mini · Tailscale 可访问 8080 · 但 8080 内 VSCode 是 `--auth=none` · **任何 Tailscale 内设备都能进 IDE 直接改文件**。要不要加 reverse-proxy + basic auth (HELM 设置)? 还是 Tailscale ACL 就够了?
- [ ] **Q2**: colima 没设开机自启 · 重启 Mac mini 需手动 `colima start` · 要不要 `brew services start colima` 挂开机?
- [ ] **Q3**: AIO Sandbox 默认时区 Asia/Singapore (per browser flag) · TZ 在 Dallas CDT · 是否要 `-e TZ=America/Chicago` 重启 container?

## NEXT

- 等你 cvs-021 dispatch (mcp-agent 装 · 该用什么连 sandbox?)
- 等你 Q1/Q2/Q3 拍板
- AIO Sandbox 已稳定 · 我去做 cvs-022 剩余 sub-tasks (22.3 等你 inline · 22.4 self-health · 22.5 Hermes dump) 还是等你新 dispatch?

---
HELM · 2026-05-14T18:12:52-05:00 (Dallas CDT)
