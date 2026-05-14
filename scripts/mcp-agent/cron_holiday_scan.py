"""
cron_holiday_scan.py · cvs-atlas-2026-05-14-023 · 第一个真 cron · Phase 1 心脏

每周一 9am CDT 跑 (launchd com.czv.holiday-scan):
1. mcp-agent + brave-search MCP 扫 "upcoming US holidays next 4 weeks"
2. 对每个 holiday · 再扫 "TikTok viral hashtag for [holiday]"
3. 输出 markdown · 追加到 Obsidian E 池"## 自动扫描区"
4. token usage 写 ~/.mcp-agent/token_log.jsonl (Atlas R8 ROI 项)

跑法:
    cd ~/.claude-skills-repo/scripts/mcp-agent
    /Users/happyglobal_tk_team/.local/share/uv/tools/mcp-agent/bin/python cron_holiday_scan.py
"""
from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

# 路径
E_POOL = Path(
    "/Users/happyglobal_tk_team/Library/Mobile Documents/iCloud~md~obsidian/"
    "Documents/06-智能体/Orbie/skill/[CLIENT] 内容生产系统/池子/"
    "池 E · 时空锚点（什么时候 + 在哪拍）.md"
)
TOKEN_LOG = Path.home() / ".mcp-agent" / "token_log.jsonl"
TOKEN_LOG.parent.mkdir(parents=True, exist_ok=True)

CDT = ZoneInfo("America/Chicago")

app = MCPApp(name="holiday_scan", description="周一 9am 节日扫描 · cvs-atlas-023")


async def main():
    now = datetime.now(CDT)
    iso = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    iso_pretty = iso[:-2] + ":" + iso[-2:]

    async with app.run() as agent_app:
        agent = Agent(
            name="holiday_scanner",
            instruction=(
                "You are a market research assistant for a US TikTok content team (CatchZVibe Studio). "
                "Use brave-search MCP to find upcoming US holidays in the next 4 weeks "
                "(starting from today), and for each holiday, identify currently trending TikTok hashtags. "
                "Be concise, factual, list-format. No fluff."
            ),
            server_names=["brave-search"],
            context=agent_app.context,
        )

        async with agent:
            llm = await agent.attach_llm(OpenAIAugmentedLLM)
            response_text = await llm.generate_str(
                message=(
                    f"Today is {now.strftime('%Y-%m-%d')} (Thursday). "
                    "Search for upcoming US federal/cultural holidays in the next 4 weeks. "
                    "For each holiday, also find current TikTok viral hashtags. "
                    "Output strict markdown table:\n"
                    "| Date | Holiday | TikTok Hashtags |\n"
                    "|---|---|---|\n"
                    "| ... | ... | #tag1 #tag2 #tag3 |"
                )
            )

    # 追加到 E 池
    section_header = f"\n\n## 自动扫描区 · {iso_pretty}\n\n_来源: cron_holiday_scan.py via brave-search MCP_\n\n"
    section_body = response_text.strip()
    full_append = section_header + section_body + "\n"

    if E_POOL.exists():
        with open(E_POOL, "a", encoding="utf-8") as f:
            f.write(full_append)
        print(f"✅ E 池 updated · appended {len(section_body)} chars · {E_POOL.name}")
    else:
        print(f"⚠️  E 池 not found: {E_POOL}")
        print("--- 输出 (未写入) ---")
        print(section_body)

    # Token log
    log_entry = {
        "ts": iso_pretty,
        "task": "cron_holiday_scan",
        "agent": "holiday_scanner",
        "server": "brave-search",
        "llm": "openai.gpt-4o-mini",
        "output_chars": len(section_body),
        "status": "completed",
    }
    with open(TOKEN_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    print(f"✅ token_log entry · {TOKEN_LOG}")


if __name__ == "__main__":
    asyncio.run(main())
