"""
hello.py · cvs-021 sub-task 4 · orchestrator-worker example
连 AIO Sandbox MCP-hub + browser MCP + 用 OpenAI 跑一句任务。

跑法:
    cd ~/.claude-skills-repo/scripts/mcp-agent
    /Users/happyglobal_tk_team/.local/share/uv/tools/mcp-agent/bin/python hello.py
"""
import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

app = MCPApp(
    name="hello_aio_sandbox",
    description="cvs-021 demo · 验 mcp-agent ↔ AIO Sandbox 通信"
)


async def main():
    async with app.run() as agent_app:
        agent = Agent(
            name="sandbox_browser",
            instruction=(
                "You have access to AIO Sandbox MCP-hub at Mac mini via streamable_http. "
                "List the MCP tools available. Then attempt to fetch example.com via any available tool. "
                "Report concisely: tool list + 1-paragraph example.com fetch result."
            ),
            server_names=["aio_sandbox"],
            context=agent_app.context,
        )

        async with agent:
            print("\n=== AIO Sandbox MCP-hub · tools list ===")
            tools = await agent.list_tools()
            for t in (tools.tools if hasattr(tools, "tools") else tools):
                print(f"  - {t.name}: {t.description[:80] if t.description else ''}...")

            print("\n=== LLM task ===")
            llm = await agent.attach_llm(OpenAIAugmentedLLM)
            result = await llm.generate_str(
                message="Use the most appropriate tool to fetch example.com homepage. Return a 1-sentence summary."
            )
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
