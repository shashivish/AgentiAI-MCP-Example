import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def run_mcp_client():
    result = asyncio.run(sync_main())
    return result

async def sync_main():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
        env=None
    )

    # Result placeholders
    tool_result = None
    resource_text = None

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # Call the 'add' tool
            tool_response = await session.call_tool("add", {"a": 3, "b": 4})
            tool_result = tool_response.content[0].text

            # Get the 'greeting' resource
            resource_response = await session.read_resource("greeting://Alice")
            resource_text = resource_response.contents[0].text

    return tool_result, resource_text


if __name__ == "__main__":
    tool_result, greeting = run_mcp_client()
    print("Tool response:", tool_result)
    print("Greeting:", greeting)
