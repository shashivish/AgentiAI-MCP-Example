from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import FastMCP
import requests

# Initialize the MCP server
mcp = FastMCP("My Example Server")

# Define a tool: addition
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

# Define a resource: greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting."""
    return f"Hello, {name}!"

@mcp.resource("greeting_api://{name}")
def get_greeting(name: str) -> str:
    """Get personalized greeting with external data"""
    try:
        # Call external API (example: user profile service)
        response = requests.get(
            f"https://api.example.com/users/{name}",
            timeout=5  # Always set timeouts!
        )
        response.raise_for_status()  # Raise exception for 4xx/5xx

        user_data = response.json()
        return f"Hello, {user_data['full_name']}! (ID: {user_data['id']})"

    except requests.exceptions.RequestException as e:
        # Fallback to basic greeting if API fails
        return f"Hello, {name}! (Could not fetch profile)"
if __name__ == '__main__':
    mcp.run(transport="stdio")
