# mcp_agent.py
import asyncio
from typing import Dict, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

class MCPAgent:
    def __init__(self):
        self.llm = OpenAI(api_key="your-api-key")
        self.servers = {
            "math": StdioServerParameters(
                command="python",
                args=["mcp_server.py"]
            )
        }
        self.system_prompt = """You are a helpful AI assistant with access to tools. 
                            When asked to perform math or greetings:
                            - Use add(a, b) for arithmetic
                            - Use get_greeting(name) for personalization
                            Always return concise answers."""

    async def process_query(self, query: str) -> str:
        async with stdio_client(self.servers["math"]) as (stdio, write):
            async with ClientSession(stdio, write) as session:
                await session.initialize()

                # Get available tools
                tools = await self._get_tools(session)

                # Get LLM decision
                response = self.llm.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": query}
                    ],
                    tools=[self._format_tool(t) for t in tools]
                )

                # Execute tool call
                tool_call = response.choices[0].message.tool_calls[0]
                return await self._execute_tool(session, tool_call)

    async def _get_tools(self, session: ClientSession) -> list:
        """Get available tools from MCP server"""
        tool_list = await session.list_tools()
        return [t.name for t in tool_list.tools]

    def _format_tool(self, tool_name: str) -> Dict[str, Any]:
        """Create tool schema for LLM"""
        return {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": "MCP server tool",
                "parameters": {"type": "object", "properties": {}}
            }
        }

    async def _execute_tool(self, session: ClientSession, tool_call) -> str:
        """Execute the selected tool and return result"""
        try:
            if tool_call.function.name == "add":
                args = eval(tool_call.function.arguments)
                result = await session.run_tool("add", args)
                return f"Result: {result.result}"
            elif "greeting" in tool_call.function.name:
                name = eval(tool_call.function.arguments)["name"]
                resource = await session.get_resource(f"greeting://{name}")
                return resource.result
            else:
                return "Tool not found"
        except Exception as e:
            return f"Error: {str(e)}"

# Usage
async def main():
    agent = MCPAgent()
    while True:
        query = input("\nYour question: ")
        if query.lower() in ["exit", "quit"]:
            break
        response = await agent.process_query(query)
        print(f"\nAgent: {response}")

if __name__ == "__main__":
    asyncio.run(main())
