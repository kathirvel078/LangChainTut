import asyncio
import anthropic
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

client = anthropic.Anthropic(api_key="")
async def main():
    server = StdioServerParameters(
        command="python",
        args=["db_mcp_server.py"]
    )

    async with stdio_client(server) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()

            mcp_tools = await session.list_tools()

            tools = [
                {
                    "name": t.name,
                    "description": t.description or "MCP tool",
                    "input_schema": t.inputSchema
                }
                for t in mcp_tools.tools
            ]

            response = client.messages.create(
                model="claude-sonnet-4-0",
                max_tokens=200,
                messages=[{
                    "role": "user",
                    "content": "show me all data"
                }],
                tools=tools
            )

            for block in response.content:
                if block.type == "tool_use":
                    print("Executing MCP tool:", block.name)

                    result = await session.call_tool(
                        block.name,
                        block.input
                    )

                    print("MCP result:", result)

asyncio.run(main())