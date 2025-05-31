# mcp_llm_client.py
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

client = OpenAI(api_key="")  # Replace with your key

# 1. Define available capabilities for LLM
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_greeting",
            "description": "Get personalized greeting",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name to greet"}
                },
                "required": ["name"]
            }
        }
    }
]

async def main():
    # 2. Connect to MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]  # From previous server example
    )

    async with stdio_client(server_params) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()

            # 3. Get user input
            query = input("\nAsk me to add numbers or get a greeting: ")

            # 4. Get LLM decision
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": query}],
                tools=TOOLS,
                tool_choice="auto"
            )

            # 5. Execute tool/resource
            tool_call = completion.choices[0].message.tool_calls[0]
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            print(f"\nLLM selected tool: {func_name} with args: {args}")

            if func_name == "get_greeting":
                # Handle resource via URI
                uri = f"greeting://{args['name']}"
                resource = await session.get_resource(uri)
                print(f"\nResponse: {resource.result}")
            else:
                # Handle tool execution
                result = await session.run_tool(func_name, args)
                print(f"\nResult: {result.result}")

if __name__ == "__main__":
    asyncio.run(main())