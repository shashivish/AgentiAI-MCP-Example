# agno_mcp_integration.py
import asyncio
from agno.agent import Agent
from agno.tools.mcp import MCPTools
from agno.models.openai import OpenAIChat

async def main():
    # 1. Configure MCP Server Connection (your existing mcp_server.py)
    mcp_command = "python mcp_server.py"
    mcp_args = ["mcp_server.py"]

    # 2. Initialize MCP Tools for Agno
    async with MCPTools(command=mcp_command) as mcp_tools:
        # 3. Create Agno Agent with MCP integration
        agent = Agent(
            name="Math & Greeting Agent",
            model=OpenAIChat(id="gpt-4.1-mini"),
            tools=[mcp_tools],
            instructions="""
                You are an AI assistant with access to math and greeting tools.
                Rules:
                1. For arithmetic questions, use the 'add' tool
                2. For greeting requests, use the 'greeting' resource
                3. Always verify input types before tool calls
                4. Return results in clean markdown format
            """,
            show_tool_calls=True,
            markdown=True
        )

        # 4. Interactive loop
        while True:
            query = input("\nYour request: ").strip()
            if query.lower() in ["exit", "quit"]:
                break

            try:
                await agent.aprint_response(query, stream=True)
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
